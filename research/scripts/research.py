#!/usr/bin/env python3
"""Kanamecide multi-agent research-memory CLI (Python stdlib only).

Run from anywhere (paths are anchored to this file):

    python research/scripts/research.py status
    python research/scripts/research.py --help

The system itself is a plain Markdown knowledge base. This script only reads YAML
front-matter, scaffolds new records, validates them, and prints summaries. It never
rewrites an existing record (so research history is never silently overwritten).
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

RESEARCH_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = RESEARCH_DIR.parent

AGENTS_DIR = RESEARCH_DIR / "agents"
HYP_DIR = RESEARCH_DIR / "hypotheses"
DEB_DIR = RESEARCH_DIR / "debates"
DEC_DIR = RESEARCH_DIR / "decisions"
EXP_DIR = RESEARCH_DIR / "experiments"
FAIL_DIR = RESEARCH_DIR / "failures"
REV_DIR = RESEARCH_DIR / "reviews"
TPL_DIR = RESEARCH_DIR / "templates"
CTX_DIR = RESEARCH_DIR / "context"
WORK_DIR = RESEARCH_DIR / "work"
HO_DIR = RESEARCH_DIR / "handoffs"
RUN_DIR = RESEARCH_DIR / "runs"
SES_DIR = RESEARCH_DIR / "sessions"
QUESTIONS_DIR = RESEARCH_DIR / "questions"
PRINCIPLES_DIR = RESEARCH_DIR / "principles"
EVIDENCE_DIR = RESEARCH_DIR / "evidence"
PROJECT_STATE = RESEARCH_DIR / "project_state.md"

# --- Closed status vocabularies (DEC-0009: an unknown status is a LOUD error) ---
# `status` is the LIFECYCLE field; the scientific verdict of an experiment lives in
# `result`. Conflating them is what made E-0010 vanish from index.md (R-0003 F8).
STATUS_VOCAB = {
    "hypothesis": {"OPEN", "TESTING", "SUPPORTED", "REJECTED", "INCONCLUSIVE", "SUPERSEDED"},
    "debate": {"OPEN", "ROUTED", "RESOLVED", "SUPERSEDED"},
    "decision": {"ACTIVE", "SUPERSEDED", "PROPOSED"},
    "experiment": {"PENDING", "RUNNING", "COMPLETED", "ABANDONED"},
    "failure": {"RECORDED"},
    "review": {"DRAFT", "IN_REVIEW", "COMPLETED"},
    "work": {"OPEN", "IN_PROGRESS", "BLOCKED", "DONE", "CANCELLED"},
    "handoff": {"REQUESTED", "ACCEPTED", "DONE", "REJECTED", "WITHDRAWN"},
    "run": {"PLANNED", "RUNNING", "COMPLETED", "FAILED", "ABANDONED"},
    "session": {"OPEN", "CLOSED"},
    # DEC-0011: Layer-3/4 record kinds (open questions, strategic/meta principles,
    # evidence inventory). An unknown status is a LOUD error, as for every other kind.
    "question": {"OPEN", "INVESTIGATING", "ANSWERED", "BLOCKED", "ABANDONED", "SUPERSEDED"},
    "principle": {"ACTIVE", "REVISED", "RETIRED"},
    "evidence": {"REGISTERED", "SUPERSEDED", "LOST"},
}
QUESTION_OPEN = {"OPEN", "INVESTIGATING", "BLOCKED"}
# Verdict prefixes accepted in an experiment's `result` (free-form text may follow).
RESULT_PREFIXES = ("PASS", "FAIL", "FAILED", "WIN", "LOSS", "NEUTRAL", "INCONCLUSIVE")

HYPOTHESIS_ACTIVE = {"OPEN", "TESTING"}
DEBATE_OPEN = {"OPEN"}
EXP_PENDING = {"PENDING", None}
EXP_RUNNING = {"RUNNING"}
WORK_OPEN = {"OPEN", "IN_PROGRESS", "BLOCKED"}
HO_OPEN = {"REQUESTED", "ACCEPTED"}
RUN_LIVE = {"PLANNED", "RUNNING"}

# Experiments created on/after this date must carry the DEC-0009 pre-registration
# sections. Older records are grandfathered (warned, never failed): records are
# append-only and are not rewritten to satisfy new tooling.
PRE_REG_EFFECTIVE_DATE = "2026-09-15"
PRE_REG_SECTIONS = (
    "## Pre-Registered Decision Rule",
    "## Power And Sample Size",
    "## Sample Validity",
    "## Provenance",
)

# The sacred perft anchor. Its SINGLE protected home is research/project_state.md
# (DEC-0009 / R-0003 F12). Any change to these numbers is a correctness regression.
PERFT_ANCHOR_SECTION = "## Certified Perft Anchors"
PERFT_ANCHOR = (
    ("startpos d1-5", ("20", "400", "8902", "197281", "4865609")),
    ("kiwipete d3", ("97,862", "97862")),
    ("cpw3 d4", ("43,238", "43238")),
    ("cpw4 d4", ("422,333", "422333")),
    ("cpw5 d4", ("2,103,487", "2103487")),
    ("cpw6 d4", ("3,894,594", "3894594")),
)

# Repo-root hygiene (DEC-0009 / R-0003 F9). Root-level scratch that predates the
# policy is listed in research/scripts/root_grandfathered.txt as DEBT; anything that
# is not sanctioned and not listed there is an error, so "junk deleted" claims become
# checkable instead of prose.
SANCTIONED_ROOT_FILES = {
    ".gitignore", "README.md", "LICENSE", "CMakeLists.txt", "build.bat", "research.bat",
}
GRANDFATHERED_LIST = RESEARCH_DIR / "scripts" / "root_grandfathered.txt"

# PROJECT_STATE.md machine block. `reflects` is what makes F7 ("memory went stale and
# silently misled") detectable instead of invisible.
META_BLOCK_RE = re.compile(r"<!--\s*research-meta(.*?)-->", re.DOTALL)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def meta_block(text: str) -> dict:
    """Parse the `<!-- research-meta ... -->` block in project_state.md."""
    m = META_BLOCK_RE.search(text)
    if not m:
        return {}
    return parse_simple_yaml(m.group(1))


def body_section(text: str, heading: str) -> str:
    """Return the body of `# heading` up to the next heading, or '' if absent."""
    lines = text.splitlines()
    start = None
    h = heading.strip().rstrip(":").strip().lower()
    for i, ln in enumerate(lines):
        s = ln.strip().rstrip(":").strip().lower()
        if s == h or s.startswith(h + " "):
            start = i + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("#"):
            end = j
            break
    return "\n".join(lines[start:end]).strip()


def load_grandfathered() -> set:
    if not GRANDFATHERED_LIST.exists():
        return set()
    out = set()
    for ln in read_text(GRANDFATHERED_LIST).splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            out.add(ln)
    return out


def root_hygiene_problems() -> list:
    allowed = load_grandfathered()
    problems = []
    for p in sorted(REPO_ROOT.iterdir()):
        if not p.is_file():
            continue
        if p.name in SANCTIONED_ROOT_FILES:
            continue
        if p.name in allowed:
            continue
        problems.append(
            f"repo root: '{p.name}' is not a sanctioned root file and is not in "
            f"research/scripts/root_grandfathered.txt (DEC-0009 hygiene policy)"
        )
    return problems


def today() -> str:
    return date.today().isoformat()


def parse_simple_yaml(text: str) -> dict:
    """Parse the tiny YAML subset used in front-matter: scalars, inline lists, bools."""
    data = {}
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if not key:
            continue
        if val == "" or val.lower() in ("null", "none", "~"):
            data[key] = None
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            data[key] = [x.strip().strip("'\"") for x in inner.split(",")] if inner else []
        elif val.lower() == "true":
            data[key] = True
        elif val.lower() == "false":
            data[key] = False
        else:
            data[key] = val.strip("'\"")
    return data


_FM_RE = re.compile(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", re.DOTALL)


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = _FM_RE.match(text)
    if not m:
        return {}
    return parse_simple_yaml(m.group(1))


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    m = _FM_RE.match(text)
    return text[m.end():] if m else text


def _is_record_path(p: Path) -> bool:
    if not p.is_file() or p.suffix.lower() != ".md":
        return False
    if p.name.startswith("_") or p.name in ("README.md", "index.md"):
        return False
    return True


def scan(directory: Path, kind: str) -> list:
    if not directory.exists():
        return []
    out = []
    for p in sorted(directory.glob("*.md")):
        if not _is_record_path(p):
            continue
        fm = parse_frontmatter(p)
        if fm.get("type") != kind:
            continue
        fm["_path"] = p
        fm["_id"] = fm.get("id") or p.stem
        out.append(fm)
    return out


def next_id(directory: Path, prefix: str, width: int) -> str:
    maxn = 0
    if directory.exists():
        for p in directory.glob("*.md"):
            m = re.match(rf"{re.escape(prefix)}(\d+)", p.name)
            if m:
                maxn = max(maxn, int(m.group(1)))
    return f"{prefix}{maxn + 1:0{width}d}"


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "untitled"


def render(template_name: str, **kw) -> str:
    text = (TPL_DIR / template_name).read_text(encoding="utf-8")
    for k, v in kw.items():
        text = text.replace("{{" + k + "}}", str(v))
    return text


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(RESEARCH_DIR)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def write_new(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        print(f"REFUSED (already exists, not overwriting): {path}")
        sys.exit(1)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"created: {path}")


def discover_agents() -> list:
    if not AGENTS_DIR.exists():
        return []
    out = []
    for d in sorted(AGENTS_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith("_"):
            continue
        profile_path = d / "profile.md"
        pos_path = d / "current_position.md"
        if not profile_path.exists():
            continue  # not fully registered yet
        profile = parse_frontmatter(profile_path)
        pos = parse_frontmatter(pos_path) if pos_path.exists() else {}
        out.append({
            "name": d.name,
            "role": profile.get("role"),
            "confidence": pos.get("confidence"),
            "focus": pos.get("focus"),
            "_dir": d,
        })
    return out


def fmt(v):
    if v is None or v == "":
        return "—"
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, (int, float)):
        return f"{v:.2f}"
    return str(v)


PRIORITY = {"high": 2, "medium": 1, "low": 0}


def priority_rank(e) -> int:
    return PRIORITY.get(str(e.get("priority")).lower(), 0)


def cmd_status(a):
    hyps = scan(HYP_DIR, "hypothesis")
    debates = scan(DEB_DIR, "debate")
    experiments = scan(EXP_DIR, "experiment")
    failures = scan(FAIL_DIR, "failure")
    work = scan(WORK_DIR, "work")
    handoffs = scan(HO_DIR, "handoff")
    runs = scan(RUN_DIR, "run")
    sessions = scan(SES_DIR, "session")

    n_active_hyps = sum(1 for h in hyps if h.get("status") in HYPOTHESIS_ACTIVE)
    n_open_debates = sum(1 for d in debates if d.get("status") in DEBATE_OPEN)
    n_pending = sum(1 for e in experiments if e.get("status") in EXP_PENDING)
    n_running = sum(1 for e in experiments if e.get("status") in EXP_RUNNING)
    n_wins = sum(1 for e in experiments if str(e.get("result") or "").upper().startswith(("WIN", "PASS")))
    n_losses = sum(1 for e in experiments if str(e.get("result") or "").upper().startswith(("LOSS", "FAIL")))
    n_open_work = sum(1 for w in work if w.get("status") in WORK_OPEN)
    n_open_ho = sum(1 for h in handoffs if h.get("status") in HO_OPEN)
    n_live_runs = sum(1 for r in runs if r.get("status") in RUN_LIVE)
    n_bad = sum(1 for recs, kind in ((hyps, "hypothesis"), (debates, "debate"),
                                     (experiments, "experiment"), (work, "work"),
                                     (handoffs, "handoff"), (runs, "run"))
                for r in recs if str(r.get("status")) not in STATUS_VOCAB[kind])

    print("PROJECT RESEARCH STATUS")
    print()
    print(f"  Active hypotheses:     {n_active_hyps}")
    print(f"  Open disagreements:    {n_open_debates}")
    print(f"  Experiments pending:   {n_pending}")
    print(f"  Experiments running:   {n_running}")
    print(f"  Experiment wins:       {n_wins}")
    print(f"  Experiment losses:     {n_losses}")
    print(f"  Failures recorded:     {len(failures)}")
    print(f"  Open work items:       {n_open_work}")
    print(f"  Open handoffs:         {n_open_ho}")
    print(f"  Live runs:             {n_live_runs}")
    print(f"  Sessions recorded:     {len(sessions)}")
    if n_bad:
        print(f"  OUT-OF-VOCABULARY STATUSES: {n_bad}  <- run `validate` (records may be invisible)")
    print()

    if getattr(a, "brief", False):
        return

    if n_open_work:
        print("Open work items:")
        for w in work:
            if w.get("status") in WORK_OPEN:
                print(f"  {w['_id']:<8} round {str(w.get('round') or '—'):<4} {str(w.get('owner') or '—'):<24} "
                      f"{w.get('status'):<12} {w.get('title') or ''}")
        print()

    print("Agents:")
    agents = discover_agents()
    if not agents:
        print("  (none)")
    for ag in agents:
        print(f"  {ag['name']:<28} conf={fmt(ag['confidence']):<8} {ag['focus'] or '—'}")
    print()

    most = None
    for d in debates:
        nparts = len(d.get("participants") or [])
        if most is None or nparts > len(most.get("participants") or []):
            most = d
    if most:
        nparts = len(most.get("participants") or [])
        ttl = most.get("title") or most.get("question") or "(untitled)"
        print("Most disputed question:")
        print(f"  {most['_id']} — {ttl}  ({nparts} participants, status={most.get('status') or 'OPEN'})")
    else:
        print("Most disputed question: —")
    print()

    cand = [e for e in experiments if e.get("status") in EXP_PENDING or e.get("status") in EXP_RUNNING]
    if cand:
        cand.sort(key=priority_rank, reverse=True)
        top = cand[0]
        print("Highest-value unresolved experiment:")
        print(f"  {top['_id']} — {top.get('title') or '(untitled)'}  (status={top.get('status')}, priority={top.get('priority') or 'unspecified'})")
    else:
        print("Highest-value unresolved experiment: —")


def cmd_agents(_args):
    agents = discover_agents()
    if not agents:
        print("(no agents registered)")
        return
    for a in agents:
        print(a["name"])
        print(f"  role:       {a['role'] or '—'}")
        print(f"  confidence: {fmt(a['confidence'])}")
        print(f"  focus:      {a['focus'] or '—'}")
        print()


def _list(noun: str, directory: Path, kind: str):
    records = scan(directory, kind)
    print(f"{noun}: {len(records)}")
    print()
    for r in records:
        extra = ""
        if kind == "hypothesis":
            extra = f"  conf={fmt(r.get('confidence'))}"
        elif kind == "experiment":
            extra = f"  result={r.get('result') or '—'}"
        elif kind == "decision" and r.get("superseded_by"):
            extra = f"  superseded_by={r['superseded_by']}"
        if r.get("example"):
            extra += "  [EXAMPLE]"
        ttl = r.get("title") or "(untitled)"
        print(f"  {r['_id']:<10} {str(r.get('status') or '—'):<12} {ttl}{extra}")
    print()


def cmd_hypotheses(_args): _list("Hypotheses", HYP_DIR, "hypothesis")
def cmd_debates(_args): _list("Debates", DEB_DIR, "debate")
def cmd_decisions(_args): _list("Decisions", DEC_DIR, "decision")
def cmd_experiments(_args): _list("Experiments", EXP_DIR, "experiment")
def cmd_failures(_args): _list("Failures", FAIL_DIR, "failure")


def _scaffold(kind_dir: Path, prefix: str, width: int, tpl: str, args_title, extra=None):
    nid = next_id(kind_dir, prefix, width)
    title = args_title or "Untitled"
    slug = slugify(title)
    content = render(tpl, ID=nid, TITLE=title, DATE=today(), **(extra or {}))
    path = kind_dir / f"{nid}-{slug}.md"
    write_new(path, content)
    print("  (fill in the body; all fields are placeholders.)")
    return path


def cmd_new_hypothesis(a): _scaffold(HYP_DIR, "H-", 4, "hypothesis.md", a.title)
def cmd_new_debate(a): _scaffold(DEB_DIR, "D-", 4, "debate.md", a.title)
def cmd_new_decision(a): _scaffold(DEC_DIR, "DEC-", 4, "decision.md", a.title)
def cmd_new_experiment(a): _scaffold(EXP_DIR, "E-", 5, "experiment.md", a.title)
def cmd_new_failure(a): _scaffold(FAIL_DIR, "F-", 4, "failure.md", a.title)


def cmd_new_review(a):
    _scaffold(REV_DIR, "R-", 4, "review.md", a.title,
              {"REVIEWER": a.reviewer or "", "TARGET": a.target or ""})


def cmd_new_agent(a):
    name = a.name.strip().lower().replace(" ", "-")
    if not name:
        print("Agent name required.")
        sys.exit(1)
    base = AGENTS_DIR / name
    if base.exists():
        print(f"REFUSED (agent already exists): {base}")
        sys.exit(1)
    (base / "reports").mkdir(parents=True)
    (base / "reports" / ".gitkeep").write_text("", encoding="utf-8")
    for fname, tpl in (("profile.md", "agent_profile.md"),
                       ("current_position.md", "current_position.md"),
                       ("beliefs.md", "beliefs.md")):
        (base / fname).write_text(render(tpl, AGENT=name, ROLE=a.role or "", DATE=today()),
                                  encoding="utf-8", newline="\n")
        print(f"created: {base / fname}")
    print(f"registered agent '{name}' (role='{a.role or ''}').")


def cmd_report(a):
    base = AGENTS_DIR / a.agent
    if not base.exists():
        print(f"Unknown agent '{a.agent}'. Register it with `new-agent` first.")
        sys.exit(1)
    title = a.title or "Analysis"
    stem = f"{today()}-{slugify(title)}"
    reports = base / "reports"
    reports.mkdir(exist_ok=True)
    path = reports / f"{stem}.md"
    n = 2
    while path.exists():
        path = reports / f"{stem}-{n}.md"
        n += 1
    path.write_text(render("report.md", AGENT=a.agent, TITLE=title, DATE=today()),
                    encoding="utf-8", newline="\n")
    print(f"created: {path}")


def _collect_section(title: str, directory: Path, kind: str, matches) -> list:
    L = [f"## {title}", ""]
    found = False
    for r in scan(directory, kind):
        if matches(r["_path"]):
            found = True
            L.append(f"### {r['_id']} — {r.get('title') or '(untitled)'}")
            L.append("")
            L.extend(strip_frontmatter(r["_path"].read_text(encoding="utf-8")).splitlines())
            L.append("")
    if not found:
        L.append("(no matching records)")
        L.append("")
    return L


def cmd_context(a):
    topic = (a.topic or "").strip()
    if not topic:
        print("Provide --topic.")
        sys.exit(1)
    tokens = [t for t in re.split(r"[,\s]+", topic.lower()) if t]
    CTX_DIR.mkdir(parents=True, exist_ok=True)

    def matches(path: Path) -> bool:
        try:
            text = path.read_text(encoding="utf-8").lower()
        except OSError:
            return False
        return any(tok in text for tok in tokens)

    L = ["# Context Pack: " + topic, "",
         "> Auto-generated briefing (derived artifact — the record files remain the source of truth).",
         f"> Generated: {today()}; topic tokens: {', '.join(tokens)}", "",
         "## Project State Summary", ""]
    ps = RESEARCH_DIR / "project_state.md"
    L.extend(strip_frontmatter(ps.read_text(encoding="utf-8")).splitlines() if ps.exists() else ["(missing)"])
    L.append("")
    L.extend(_collect_section("Hypotheses", HYP_DIR, "hypothesis", matches))
    L.extend(_collect_section("Debates", DEB_DIR, "debate", matches))
    L.extend(_collect_section("Decisions", DEC_DIR, "decision", matches))
    L.extend(_collect_section("Experiments", EXP_DIR, "experiment", matches))
    L.extend(_collect_section("Failures", FAIL_DIR, "failure", matches))
    L.extend(_collect_section("Reviews", REV_DIR, "review", matches))
    L.extend(["## Agent Positions", ""])
    for ag in discover_agents():
        pos_path = ag["_dir"] / "current_position.md"
        if matches(pos_path):
            L.append(f"### {ag['name']}")
            L.append("")
            L.extend(strip_frontmatter(pos_path.read_text(encoding="utf-8")).splitlines())
            L.append("")
        else:
            L.append(f"- **{ag['name']}** — focus: {ag['focus'] or '—'} (confidence {fmt(ag['confidence'])})")
    L.append("")
    out = CTX_DIR / f"{slugify(topic)}.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(f"generated: {out}")


def _index_lines() -> list:
    L = ["# Research Index", "",
         "> Auto-generated by `research update`. Do not edit by hand — edit the records and rerun.",
         f"> Last generated: {today()}", ""]

    rendered = []

    def section(title, directory, kind, statuses=None, predicate=None):
        L.append(f"## {title}")
        L.append("")
        recs = scan(directory, kind)
        if statuses is not None:
            recs = [r for r in recs if r.get("status") in statuses]
        if predicate is not None:
            recs = [r for r in recs if predicate(r)]
        if not recs:
            L.append("(none)")
            L.append("")
            return
        for r in recs:
            rendered.append(r["_path"])
            tag = "  [EXAMPLE]" if r.get("example") else ""
            verdict = ""
            if kind == "experiment" and r.get("result") not in (None, ""):
                verdict = f"  result={str(r.get('result'))[:24]}"
            if kind == "decision" and r.get("superseded_by"):
                verdict = f"  superseded_by={r['superseded_by']}"
            L.append(
                f"- [{r['_id']}]({rel(r['_path'])}) — {r.get('title') or '(untitled)'} — "
                f"status={r.get('status') or '—'}{verdict}{tag}"
            )
        L.append("")

    section("Active Hypotheses", HYP_DIR, "hypothesis", HYPOTHESIS_ACTIVE)
    section("Closed Hypotheses", HYP_DIR, "hypothesis",
            {"SUPPORTED", "REJECTED", "INCONCLUSIVE", "SUPERSEDED"})
    section("Open Disagreements", DEB_DIR, "debate", {"OPEN"})
    section("Routed / Resolved Disagreements", DEB_DIR, "debate", {"ROUTED", "RESOLVED", "SUPERSEDED"})
    section("Pending / Running Experiments", EXP_DIR, "experiment", EXP_PENDING | EXP_RUNNING)
    section("Completed Experiments", EXP_DIR, "experiment", {"COMPLETED", "ABANDONED"})
    section("Failures", FAIL_DIR, "failure")
    section("Decisions", DEC_DIR, "decision")
    section("Reviews", REV_DIR, "review")
    section("Open Questions", QUESTIONS_DIR, "question", QUESTION_OPEN)
    section("Closed Questions", QUESTIONS_DIR, "question", {"ANSWERED", "ABANDONED", "SUPERSEDED"})
    section("Principles", PRINCIPLES_DIR, "principle")
    section("Evidence", EVIDENCE_DIR, "evidence")
    section("Work Items (open)", WORK_DIR, "work", WORK_OPEN)
    section("Work Items (closed)", WORK_DIR, "work", {"DONE", "CANCELLED"})
    section("Handoffs (open)", HO_DIR, "handoff", HO_OPEN)
    section("Runs (live)", RUN_DIR, "run", RUN_LIVE)
    section("Runs (finished)", RUN_DIR, "run", {"COMPLETED", "FAILED", "ABANDONED"})
    section("Sessions", SES_DIR, "session")

    # Completeness self-check: no record may be scanned but unrendered. A silent drop
    # (the E-0010/F8 failure) makes this section non-empty instead of invisible.
    all_records = []
    for directory, kind in ((HYP_DIR, "hypothesis"), (DEB_DIR, "debate"), (DEC_DIR, "decision"),
                            (EXP_DIR, "experiment"), (FAIL_DIR, "failure"), (REV_DIR, "review"),
                            (QUESTIONS_DIR, "question"), (PRINCIPLES_DIR, "principle"),
                            (EVIDENCE_DIR, "evidence"),
                            (WORK_DIR, "work"), (HO_DIR, "handoff"), (RUN_DIR, "run"),
                            (SES_DIR, "session")):
        all_records.extend(scan(directory, kind))
    missing = [r for r in all_records if r["_path"] not in rendered]
    L.append("## Unrendered Records (bug — report this)")
    L.append("")
    if not missing:
        L.append("(none — every scanned record appears above)")
    else:
        for r in missing:
            L.append(f"- !!! {r['_id']} ({rel(r['_path'])}) status={r.get('status')!r} "
                     f"type={r.get('type')!r} — NOT RENDERED")
    L.append("")

    L.append("## Agent Positions")
    L.append("")
    for ag in discover_agents():
        L.append(f"- [{ag['name']}]({rel(ag['_dir'] / 'current_position.md')}) — "
                 f"confidence {fmt(ag['confidence'])} — {ag['focus'] or '—'}")
    L.append("")
    return L


def cmd_update(_args):
    (RESEARCH_DIR / "index.md").write_text("\n".join(_index_lines()) + "\n", encoding="utf-8", newline="\n")
    print(f"updated: {RESEARCH_DIR / 'index.md'}")


def _section_filled(text: str, heading: str) -> bool:
    body = body_section(text, heading)
    for ln in body.splitlines():
        s = ln.strip()
        if s and set(s) - set(".-* "):
            return True
    return False


def _record_problems(directory: Path, kind: str, required: set, seen: dict, warnings: list):
    """Per-record structural checks: type, example flag, required fields, status vocabulary."""
    problems = []
    for p in sorted(directory.glob("*.md")):
        if not _is_record_path(p):
            continue
        text = read_text(p)
        fm = parse_frontmatter(p)
        if not fm:
            problems.append(f"{rel(p)}: missing/invalid front-matter")
            continue
        if fm.get("type") != kind:
            problems.append(f"{rel(p)}: type={fm.get('type')!r}, expected {kind!r}")
            continue
        if "example" not in fm or fm["example"] not in (True, False):
            problems.append(f"{rel(p)}: missing boolean 'example' field")
        for f in required:
            if f not in fm or fm[f] in (None, ""):
                problems.append(f"{rel(p)}: missing required field '{f}'")
        # LOUD failure on unknown status (DEC-0009 / R-0003 F8); the old tool silently
        # dropped such records from index.md instead.
        status = fm.get("status")
        vocab = STATUS_VOCAB.get(kind, set())
        if status is None:
            problems.append(f"{rel(p)}: missing required field 'status'")
        elif str(status) not in vocab:
            problems.append(
                f"{rel(p)}: status={status!r} is not in the {kind} vocabulary "
                f"({', '.join(sorted(vocab))}) — see DEC-0009"
            )
        rid = fm.get("id") or p.stem
        if rid in seen:
            problems.append(f"{rel(p)}: duplicate id {rid} (also {rel(seen[rid])})")
        seen[rid] = p
        if not strip_frontmatter(text).strip():
            problems.append(f"{rel(p)}: empty body")
        problems.extend(_kind_specific_problems(kind, fm, text, p, warnings))
    return problems


def _kind_specific_problems(kind: str, fm: dict, text: str, p: Path, warnings: list):
    problems = []
    if kind == "experiment":
        if fm.get("status") in ("RUNNING", "COMPLETED"):
            missing = [h for h in PRE_REG_SECTIONS if not _section_filled(text, h)]
            created = str(fm.get("created") or "")
            if created >= PRE_REG_EFFECTIVE_DATE:
                for h in missing:
                    problems.append(
                        f"{rel(p)}: status={fm.get('status')} but section '{h}' is "
                        f"absent/empty — DEC-0009 requires pre-registration"
                    )
            elif missing:
                warnings.append(
                    f"{rel(p)}: legacy record (created {created}) lacks "
                    f"{'/'.join(m[3:] for m in missing)} — grandfathered, not enforced"
                )
        res = fm.get("result")
        if isinstance(res, str) and res.strip() and not res.strip().upper().startswith(RESULT_PREFIXES):
            warnings.append(
                f"{rel(p)}: result={res[:48]!r} does not start with a verdict "
                f"({', '.join(RESULT_PREFIXES)})"
            )
    if kind == "work" and str(fm.get("status")) == "DONE":
        if not fm.get("exit_check"):
            problems.append(f"{rel(p)}: DONE without an exit_check (DEC-0009 gate 2)")
        if not fm.get("evidence"):
            problems.append(f"{rel(p)}: DONE without evidence (DEC-0009 gate 1)")
        if not fm.get("verified_by") or str(fm.get("verification_verdict")) != "VERIFIED":
            problems.append(
                f"{rel(p)}: DONE but not independently verified "
                f"(verified_by / verification_verdict) — DEC-0009 gate 3"
            )
        elif str(fm.get("verified_by")) == str(fm.get("owner")):
            problems.append(
                f"{rel(p)}: DONE with verified_by == owner — self-verification is not "
                f"verification (DEC-0009 gate 3)"
            )
    if kind == "run" and str(fm.get("status")) in ("RUNNING", "PLANNED"):
        for f in ("command", "heartbeat", "checkpoint"):
            if not fm.get(f):
                problems.append(f"{rel(p)}: {fm.get('status')} run without '{f}'")
        hb = fm.get("heartbeat")
        if hb and not (REPO_ROOT / str(hb)).exists():
            warnings.append(
                f"{rel(p)}: heartbeat '{hb}' is not on disk — a run claiming RUNNING with "
                f"no heartbeat is a FALSE liveness claim (R-0003 F2)"
            )
    return problems


def cmd_validate(_args):
    problems = []
    warnings = []
    seen = {}
    specs = [
        (HYP_DIR, "hypothesis", {"status", "created"}),
        (DEB_DIR, "debate", {"status", "created"}),
        (DEC_DIR, "decision", {"status", "created"}),
        (EXP_DIR, "experiment", {"status", "created"}),
        (FAIL_DIR, "failure", {"created"}),
        (REV_DIR, "review", {"created"}),
        (WORK_DIR, "work", {"status", "created", "owner", "title"}),
        (HO_DIR, "handoff", {"status", "created", "from", "to", "title"}),
        (RUN_DIR, "run", {"status", "created", "title"}),
        (SES_DIR, "session", {"status", "created", "agent"}),
        (QUESTIONS_DIR, "question", {"status", "created"}),
        (PRINCIPLES_DIR, "principle", {"status", "created"}),
        (EVIDENCE_DIR, "evidence", {"status", "created", "path"}),
    ]
    for directory, kind, required in specs:
        problems.extend(_record_problems(directory, kind, required, seen, warnings))

    # Cross-record: every handoff must point at a real work item.
    work_ids = {w["_id"] for w in scan(WORK_DIR, "work")}
    for ho in scan(HO_DIR, "handoff"):
        wid = ho.get("work_item")
        if wid and str(wid) not in work_ids:
            problems.append(f"{rel(ho['_path'])}: work_item={wid!r} does not exist in research/work/")

    for ag in discover_agents():
        for f in ("profile.md", "current_position.md", "beliefs.md"):
            if not (ag["_dir"] / f).exists():
                problems.append(f"{ag['name']}/{f}: missing")

    # DEC-0011 derived-layer checks (advisory): memory integrity beyond the record files.
    try:
        import memorylib as M
        _nodes = M.load_nodes()
        _code = M.code_nodes()
        for d in M.missing_reference_targets(_nodes):
            warnings.append(f"dangling id {d['id']} referenced by {d['referenced_by'][:3]}")
        for ev in M.evidence_inventory(_nodes):
            if ev["path"] and not ev["exists"]:
                warnings.append(f"evidence {ev['id']}: path missing on disk: {ev['path']}")
            if ev["exists"] and ev["sha256_recorded"] and ev["sha256"].lower() != str(ev["sha256_recorded"]).lower():
                problems.append(f"evidence {ev['id']}: sha256 drift on {ev['path']} "
                                f"(recorded {str(ev['sha256_recorded'])[:12]}…, on-disk {ev['sha256'][:12]}…)")
        n_contra = len(M.contradiction_candidates(_nodes))
        if n_contra:
            warnings.append(f"{n_contra} contradiction candidate(s) — run `research.py contradictions`")
    except Exception as exc:  # the layer must never make validate fail by crashing
        warnings.append(f"derived-layer checks skipped (memorylib error: {exc})")

    problems.extend(_project_state_problems())
    problems.extend(root_hygiene_problems())

    if warnings:
        print("Validation WARNINGS (grandfathered / advisory — not failures):")
        for w in warnings:
            print(f"  - {w}")
        print()
    if problems:
        print("Validation FAILED:")
        for p in problems:
            print(f"  - {p}")
        print()
        print(f"{len(problems)} problem(s). See research/SYSTEM.md for the gates.")
        sys.exit(1)
    print("Validation OK — statuses are in-vocabulary; the perft anchor and project_state.md "
          "consistency are verified; repo-root hygiene is respected.")


def _project_state_problems() -> list:
    """The sacred perft anchor + staleness consistency (DEC-0009 / R-0003 F7, F12)."""
    problems = []
    text = read_text(PROJECT_STATE)
    if not text:
        return ["project_state.md: missing or empty"]
    anchor = body_section(text, PERFT_ANCHOR_SECTION)
    if not anchor:
        problems.append(
            f"project_state.md: '{PERFT_ANCHOR_SECTION}' section is missing — the perft "
            f"anchor has exactly one protected home, and this is it (R-0003 F12)"
        )
    else:
        flat = anchor.replace(" ", "")
        for name, variants in PERFT_ANCHOR:
            if not any(v in flat for v in variants):
                problems.append(
                    f"project_state.md perft anchor: expected count for {name} "
                    f"({variants[0]}) not found — SACRED: any change is a regression"
                )
    meta = meta_block(text)
    if not meta:
        return problems + [
            "project_state.md: missing the `<!-- research-meta ... -->` block "
            "(last_updated / reflects / not_reflected) — it cannot be staleness-checked"
        ]
    def _list(v):
        if isinstance(v, str):
            return [v]
        return [str(x) for x in (v or [])]
    accounted = set(_list(meta.get("reflects"))) | set(_list(meta.get("not_reflected")))
    last_updated = str(meta.get("last_updated") or "")
    newest = ""
    for rec in scan(EXP_DIR, "experiment") + scan(DEC_DIR, "decision"):
        if rec.get("example"):
            continue
        if rec.get("type") == "experiment" and rec.get("status") != "COMPLETED":
            continue
        if rec.get("type") == "decision" and rec.get("status") != "ACTIVE":
            continue
        rid = str(rec.get("_id"))
        if rid not in accounted:
            problems.append(
                f"project_state.md: '{rid}' is final ({rec.get('status')}) but is neither in "
                f"`reflects` nor in `not_reflected` — memory is stale or silent (R-0003 F7)"
            )
        newest = max(newest, str(rec.get("completed") or rec.get("created") or ""))
    if last_updated and newest and last_updated < newest:
        problems.append(
            f"project_state.md: last_updated={last_updated} is older than the newest final "
            f"record ({newest}) — re-update it before the round can close"
        )
    return problems


def cmd_megaprompt(_args):
    path = RESEARCH_DIR / "AGENT_MEGAPROMPT.md"
    if not path.exists():
        print(f"missing: {path}")
        sys.exit(1)
    print(path.read_text(encoding="utf-8"))


def _fmt_work(w) -> str:
    return (f"  {w['_id']:<8} r{str(w.get('round') or '—'):<3} "
            f"{str(w.get('owner') or '—'):<24} {str(w.get('status')):<12} "
            f"{w.get('title') or ''}")


def cmd_work(_args):
    work = scan(WORK_DIR, "work")
    if not work:
        print("(no work items — a round is defined by its work items; see SYSTEM.md §4)")
        return
    print(f"Work items: {len(work)}")
    print()
    for w in work:
        print(_fmt_work(w))
        if w.get("deliverable"):
            print(f"           deliverable: {w['deliverable']}")
        if w.get("exit_check"):
            print(f"           exit_check:  {w['exit_check']}")
        if str(w.get("status")) == "DONE":
            print(f"           verified_by: {w.get('verified_by')} "
                  f"({w.get('verification_verdict')})")
    print()


def cmd_round(a):
    rid = str(a.round)
    work = [w for w in scan(WORK_DIR, "work") if str(w.get("round")) == rid]
    if not work:
        print(f"No work items recorded for round {rid}.")
        sys.exit(1)
    print(f"ROUND {rid} — exit check")
    print()
    bad = []
    for w in work:
        st = str(w.get("status"))
        verdict = str(w.get("verification_verdict") or "—")
        ok = st == "DONE" and verdict == "VERIFIED"
        print(f"  [{'PASS' if ok else 'FAIL'}] {_fmt_work(w).strip()}")
        if not ok:
            why = []
            if st != "DONE":
                why.append(f"status={st}")
            if verdict != "VERIFIED":
                why.append(f"verification={verdict}")
            if not w.get("evidence"):
                why.append("no evidence")
            if not w.get("exit_check"):
                why.append("no exit_check")
            print(f"          -> {', '.join(why)}")
            bad.append(w)
    print()
    print(f"{len(work) - len(bad)}/{len(work)} work items DONE and verified.")
    if bad:
        print()
        print("ROUND NOT CLOSED. Remaining work items:")
        for w in bad:
            print(_fmt_work(w))
        sys.exit(1)
    print("ROUND CLOSED — every work item is DONE and independently verified.")


def cmd_handoffs(_args):
    hos = scan(HO_DIR, "handoff")
    if not hos:
        print("(no handoffs)")
        return
    for h in hos:
        print(f"  {h['_id']:<8} {str(h.get('status')):<11} {str(h.get('from')):<24} -> "
              f"{str(h.get('to')):<24} {h.get('work_item') or '—'}  {h.get('title') or ''}")
    print()


def cmd_runs(_args):
    runs = scan(RUN_DIR, "run")
    if not runs:
        print("(no runs recorded)")
        return
    from datetime import datetime
    now = datetime.now()
    for r in runs:
        st = str(r.get("status"))
        hb = r.get("heartbeat")
        hb_path = (REPO_ROOT / str(hb)) if hb else None
        detail = ""
        if hb_path and hb_path.exists():
            age = (now - datetime.fromtimestamp(hb_path.stat().st_mtime)).total_seconds()
            last = ""
            try:
                last = read_text(hb_path).strip().splitlines()[-1]
            except IndexError:
                pass
            liveness = "ALIVE?" if age <= 120 else "STALE"
            detail = f"  heartbeat {age:6.0f}s ago ({liveness}) last={last[:80]}"
        elif hb:
            detail = "  heartbeat MISSING"
        print(f"  {r['_id']:<10} {st:<10} pid={str(r.get('pid') or '—'):<8} {r.get('title') or ''}{detail}")
    print()
    print("Contract: a job that outlives one shell command MUST have a heartbeat, a")
    print("checkpoint and a resume command (SYSTEM.md §6). A RUN claiming RUNNING with a")
    print("missing/stale heartbeat is a FALSE liveness claim — never report it as running.")


def cmd_sessions(_args):
    ses = scan(SES_DIR, "session")
    if not ses:
        print("(no session records)")
        return
    for s in ses:
        print(f"  {s['_id']:<10} {str(s.get('created')):<12} {str(s.get('agent')):<24} "
              f"round {str(s.get('round') or '—'):<4} {s.get('title') or ''}")
    print()


def cmd_next(_args):
    work = [w for w in scan(WORK_DIR, "work") if w.get("status") in WORK_OPEN]
    hos = [h for h in scan(HO_DIR, "handoff") if h.get("status") in HO_OPEN]
    exps = [e for e in scan(EXP_DIR, "experiment")
            if e.get("status") in EXP_PENDING or e.get("status") in EXP_RUNNING]
    print("NEXT ACTION (bootstrap: run this first, then read the record it points at)")
    print()
    if work:
        work.sort(key=priority_rank, reverse=True)
        w = work[0]
        print(f"  1. Work item {w['_id']} (round {w.get('round')}) owned by {w.get('owner')}:")
        print(f"     {w.get('title')}")
        print(f"     deliverable : {w.get('deliverable') or '—'}")
        print(f"     exit_check  : {w.get('exit_check') or '—'}")
        print(f"     record      : {rel(w['_path'])}")
    else:
        print("  1. No open work items. A round must be opened with work items (SYSTEM.md §4).")
    print()
    if hos:
        h = hos[0]
        print(f"  2. Open handoff {h['_id']}: {h.get('from')} -> {h.get('to')} — {h.get('title')}")
        print(f"     {rel(h['_path'])}")
    else:
        print("  2. No open handoffs.")
    print()
    if exps:
        exps.sort(key=priority_rank, reverse=True)
        e = exps[0]
        print(f"  3. Unresolved experiment {e['_id']} (priority {e.get('priority')}): {e.get('title')}")
        print(f"     {rel(e['_path'])}")
    else:
        print("  3. No pending/running experiments.")
    print()
    print("  Then: reproduce the anchor (`build\\Release\\kana.exe` -> ALL TESTS PASSED) before")
    print("  trusting any inherited number.")


def cmd_new_work(a):
    _scaffold(WORK_DIR, "W-", 4, "work_item.md", a.title,
              {"ROUND": a.round or "1", "OWNER": a.owner or ""})
    print(f"  set `exit_check` and `deliverable` in the record (round {a.round or 1}).")


def cmd_new_handoff(a):
    _scaffold(HO_DIR, "HO-", 4, "handoff.md", a.title,
              {"FROM": a.sender or "", "TO": a.to or "", "WORK": a.work or "null"})


def cmd_new_run(a):
    _scaffold(RUN_DIR, "RUN-", 4, "run.md", a.title, {"WORK": a.work or "null"})


def cmd_new_session(a):
    base = AGENTS_DIR / a.agent
    if not base.exists():
        print(f"Unknown agent '{a.agent}'. Register it with `new-agent` first.")
        sys.exit(1)
    _scaffold(SES_DIR, "S-", 4, "session.md", a.title or f"{a.agent} session",
              {"AGENT": a.agent, "ROUND": a.round or "1"})


def _ml_run(a, cmd: str) -> int:
    """Forward a derived-intelligence command to memorylib (DEC-0011). memorylib is
    imported lazily here so `import memorylib` <- `import research` never cycles."""
    import memorylib as M
    return M.run_derived(cmd, getattr(a, "margs", []))


def cmd_search(a): return _ml_run(a, "search")
def cmd_graph(a): return _ml_run(a, "graph")
def cmd_beliefs(a): return _ml_run(a, "beliefs")
def cmd_contradictions(a): return _ml_run(a, "contradictions")
def cmd_duplicates(a): return _ml_run(a, "duplicates")
def cmd_questions(a): return _ml_run(a, "questions")
def cmd_principles(a):
    _list("Principles", PRINCIPLES_DIR, "principle")
def cmd_revivals(a): return _ml_run(a, "revivals")
def cmd_timeline(a): return _ml_run(a, "timeline")
def cmd_codemap(a): return _ml_run(a, "codemap")
def cmd_audit(a): return _ml_run(a, "audit")
def cmd_evidence_list(a):
    if getattr(a, "margs", None):
        return _ml_run(a, "evidence")
    _list("Evidence", EVIDENCE_DIR, "evidence")
def cmd_state(a):
    import memorylib as M
    argv = getattr(a, "margs", [])
    if "--write" in argv or a.write:
        argv = [x for x in argv if x != "--write"]
        argv.append("--write")
        return M.run_derived("state", argv)
    return M.run_derived("state", argv)


def cmd_new_question(a): _scaffold(QUESTIONS_DIR, "Q-", 4, "question.md", a.title)
def cmd_new_principle(a): _scaffold(PRINCIPLES_DIR, "PR-", 4, "principle.md", a.title)


def cmd_new_evidence(a):
    p = _scaffold(EVIDENCE_DIR, "EV-", 4, "evidence.md", a.title,
                  {"PATH": getattr(a, "path", "") or ""})
    print("  fill `path` and (optionally) `regenerate:`; then run `research.py evidence` "
          "to capture the sha256 of the artifact on disk.")
    return p


def cmd_hygiene(a):
    """Classification of root-level files: sanctioned / grandfathered-debt /
    unsanctioned-new / unreferenced-candidate. Read-only unless --json is requested."""
    import memorylib as M
    sanctioned = SANCTIONED_ROOT_FILES
    grand = load_grandfathered()
    nodes = M.load_nodes()
    corpus = "\n".join(n["text"] + "\n" + n["title"] for n in nodes.values())
    rows = []
    for pth in sorted(REPO_ROOT.iterdir()):
        if not pth.is_file():
            continue
        name = pth.name
        cls = ("sanctioned" if name in sanctioned else
               "grandfathered-debt" if name in grand else "unsanctioned-NEW")
        referenced = name in corpus
        rows.append({"file": name, "class": cls, "referenced_in_records": referenced,
                     "size": pth.stat().st_size})
    counts = {"sanctioned": 0, "grandfathered-debt": 0, "unsanctioned-NEW": 0}
    for r in rows:
        counts[r["class"]] += 1
    unreferenced_debt = [r for r in rows if r["class"] == "grandfathered-debt"
                         and not r["referenced_in_records"]]
    if getattr(a, "json", False):
        print(M.json_dump({"counts": counts, "unreferenced_debt_candidates": unreferenced_debt,
                           "files": rows}))
        return 0
    print(f"Root file classes: {counts}")
    print(f"Grandfathered files with no record referencing them (W-0006 shrink candidates): "
          f"{len(unreferenced_debt)}")
    for r in unreferenced_debt[:30]:
        print(f"  {r['file']}  ({r['size']} B)")
    return 0


def cmd_schema(a):
    import memorylib as M
    out = {"schema_version": M.SCHEMA_VERSION,
           "record_kinds": sorted(set(M.STATUS_VOCAB) | {"report", "doc", "code"}),
           "layers": M.LAYERS,
           "relation_kinds": sorted(set(M.EDGE_STRUCTURAL.values()) | set(M.EDGE_ACTOR.values())
                                    | {"mentions", "touches-code"}),
           "verdict_prefixes": list(RESULT_PREFIXES),
           "confidence_labels": [name for _, name in M.CONFIDENCE_LADDER]}
    print(M.json_dump(out))
    return 0


def cmd_selftest(a):
    """Run the memory-system self-tests (research/scripts/tests_memory.py) and return
    its exit code — the memory layer is software and it must prove itself."""
    import subprocess as _sp
    root = Path(__file__).resolve().parent
    exe = sys.executable
    rc = _sp.call([exe, str(root / "tests_memory.py")], cwd=str(REPO_ROOT))
    print("selftest:", "OK" if rc == 0 else f"FAILED (exit {rc})")
    return rc


def build_parser():
    p = argparse.ArgumentParser(prog="research", description="Kanamecide multi-agent research-memory CLI")
    sub = p.add_subparsers(dest="command", required=True)
    st = sub.add_parser("status")
    st.add_argument("--brief", action="store_true", help="counters only (cheap bootstrap read)")
    st.set_defaults(func=cmd_status)
    sub.add_parser("agents").set_defaults(func=cmd_agents)
    sub.add_parser("hypotheses").set_defaults(func=cmd_hypotheses)
    sub.add_parser("debates").set_defaults(func=cmd_debates)
    sub.add_parser("decisions").set_defaults(func=cmd_decisions)
    sub.add_parser("experiments").set_defaults(func=cmd_experiments)
    sub.add_parser("failures").set_defaults(func=cmd_failures)
    sub.add_parser("work").set_defaults(func=cmd_work)
    sub.add_parser("handoffs").set_defaults(func=cmd_handoffs)
    sub.add_parser("runs").set_defaults(func=cmd_runs)
    sub.add_parser("sessions").set_defaults(func=cmd_sessions)
    sub.add_parser("next").set_defaults(func=cmd_next)
    sub.add_parser("update").set_defaults(func=cmd_update)
    sub.add_parser("validate").set_defaults(func=cmd_validate)
    sub.add_parser("megaprompt").set_defaults(func=cmd_megaprompt)

    srd = sub.add_parser("round", help="machine-checkable round exit criterion")
    srd.add_argument("--round", "-r", required=True)
    srd.set_defaults(func=cmd_round)

    for name, dest in (("new-hypothesis", "cmd_new_hypothesis"), ("new-debate", "cmd_new_debate"),
                       ("new-decision", "cmd_new_decision"), ("new-experiment", "cmd_new_experiment"),
                       ("new-failure", "cmd_new_failure")):
        sp = sub.add_parser(name)
        sp.add_argument("--title", "-t")
        sp.set_defaults(func=globals()[dest])

    sw = sub.add_parser("new-work")
    sw.add_argument("--title", "-t")
    sw.add_argument("--round", "-r")
    sw.add_argument("--owner")
    sw.set_defaults(func=cmd_new_work)

    sh = sub.add_parser("new-handoff")
    sh.add_argument("--title", "-t")
    sh.add_argument("--from", dest="sender")
    sh.add_argument("--to")
    sh.add_argument("--work")
    sh.set_defaults(func=cmd_new_handoff)

    sur = sub.add_parser("new-run", help="scaffold a RUN record (prefer runjob.py, which fills it)")
    sur.add_argument("--title", "-t")
    sur.add_argument("--work")
    sur.set_defaults(func=cmd_new_run)

    sss = sub.add_parser("new-session")
    sss.add_argument("agent")
    sss.add_argument("--title", "-t")
    sss.add_argument("--round", "-r")
    sss.set_defaults(func=cmd_new_session)

    spr = sub.add_parser("new-review")
    spr.add_argument("--title", "-t")
    spr.add_argument("--reviewer")
    spr.add_argument("--target")
    spr.set_defaults(func=cmd_new_review)

    spa = sub.add_parser("new-agent")
    spa.add_argument("name")
    spa.add_argument("--role")
    spa.set_defaults(func=cmd_new_agent)

    sr = sub.add_parser("report")
    sr.add_argument("agent")
    sr.add_argument("--title", "-t")
    sr.set_defaults(func=cmd_report)

    sc = sub.add_parser("context")
    sc.add_argument("--topic", "-t", required=True)
    sc.set_defaults(func=cmd_context)

    # ---- DEC-0011: derived-intelligence layer (search/graph/beliefs/audit/...) ----
    for name, fn in (("search", cmd_search), ("graph", cmd_graph),
                     ("beliefs", cmd_beliefs), ("contradictions", cmd_contradictions),
                     ("duplicates", cmd_duplicates), ("questions", cmd_questions),
                     ("revivals", cmd_revivals), ("timeline", cmd_timeline),
                     ("codemap", cmd_codemap), ("audit", cmd_audit),
                     ("evidence", cmd_evidence_list)):
        sp = sub.add_parser(name)
        sp.add_argument("margs", nargs=argparse.REMAINDER)
        sp.set_defaults(func=fn)
    ss = sub.add_parser("state", help="write/print the generated research state (state.md + state.json)")
    ss.add_argument("--write", action="store_true")
    ss.add_argument("margs", nargs=argparse.REMAINDER)
    ss.set_defaults(func=cmd_state)
    sub.add_parser("schema").set_defaults(func=cmd_schema)
    sh = sub.add_parser("hygiene", help="classify repo-root files (sanctioned / debt / new / unreferenced)")
    sh.add_argument("--json", action="store_true")
    sh.set_defaults(func=cmd_hygiene)
    sub.add_parser("selftest", help="run the memory-system unit tests").set_defaults(func=cmd_selftest)

    sq = sub.add_parser("new-question")
    sq.add_argument("--title", "-t")
    sq.set_defaults(func=cmd_new_question)
    spr2 = sub.add_parser("new-principle")
    spr2.add_argument("--title", "-t")
    spr2.set_defaults(func=cmd_new_principle)
    sev = sub.add_parser("new-evidence")
    sev.add_argument("--title", "-t")
    sev.add_argument("--path")
    sev.set_defaults(func=cmd_new_evidence)
    return p


def main(argv=None):
    # Prevent UnicodeEncodeError when a non-UTF8 Windows console can't encode an
    # em dash / arrow in a record title or prompt. Files on disk stay UTF-8 either way.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    p = build_parser()
    args, extra = p.parse_known_args(argv)
    if extra and hasattr(args, "margs"):
        args.margs = list(extra) + list(getattr(args, "margs", []) or [])
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
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

# Status vocabularies used by `status`.
HYPOTHESIS_ACTIVE = {"OPEN", "TESTING"}
DEBATE_OPEN = {"OPEN", "UNRESOLVED", None}
EXP_PENDING = {"PENDING", None}
EXP_RUNNING = {"RUNNING"}


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


def cmd_status(_args):
    hyps = scan(HYP_DIR, "hypothesis")
    debates = scan(DEB_DIR, "debate")
    experiments = scan(EXP_DIR, "experiment")
    failures = scan(FAIL_DIR, "failure")

    n_active_hyps = sum(1 for h in hyps if h.get("status") in HYPOTHESIS_ACTIVE)
    n_open_debates = sum(1 for d in debates if d.get("status") in DEBATE_OPEN)
    n_pending = sum(1 for e in experiments if e.get("status") in EXP_PENDING)
    n_running = sum(1 for e in experiments if e.get("status") in EXP_RUNNING)
    n_wins = sum(1 for e in experiments if e.get("result") == "WIN")
    n_losses = sum(1 for e in experiments if e.get("result") == "LOSS")

    print("PROJECT RESEARCH STATUS")
    print()
    print(f"  Active hypotheses:     {n_active_hyps}")
    print(f"  Open disagreements:    {n_open_debates}")
    print(f"  Experiments pending:   {n_pending}")
    print(f"  Experiments running:   {n_running}")
    print(f"  Experiment wins:       {n_wins}")
    print(f"  Experiment losses:     {n_losses}")
    print(f"  Failures recorded:     {len(failures)}")
    print()

    print("Agents:")
    agents = discover_agents()
    if not agents:
        print("  (none)")
    for a in agents:
        print(f"  {a['name']:<28} conf={fmt(a['confidence']):<8} {a['focus'] or '—'}")
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

    def section(title, directory, kind, statuses=None):
        L.append(f"## {title}")
        L.append("")
        recs = scan(directory, kind)
        if statuses:
            recs = [r for r in recs if r.get("status") in statuses]
        if not recs:
            L.append("(none)")
            L.append("")
            return
        for r in recs:
            tag = "  [EXAMPLE]" if r.get("example") else ""
            L.append(f"- [{r['_id']}]({rel(r['_path'])}) — {r.get('title') or '(untitled)'} — status={r.get('status') or '—'}{tag}")
        L.append("")

    section("Active Hypotheses", HYP_DIR, "hypothesis", HYPOTHESIS_ACTIVE)
    section("Open Disagreements", DEB_DIR, "debate", DEBATE_OPEN)
    section("Pending / Running Experiments", EXP_DIR, "experiment", EXP_PENDING | EXP_RUNNING)
    section("Completed Experiments", EXP_DIR, "experiment", {"COMPLETED"})
    section("Failures", FAIL_DIR, "failure")
    section("Decisions", DEC_DIR, "decision")

    L.append("## Agent Positions")
    L.append("")
    for ag in discover_agents():
        L.append(f"- [{ag['name']}]({rel(ag['_dir'] / 'current_position.md')}) — confidence {fmt(ag['confidence'])} — {ag['focus'] or '—'}")
    L.append("")
    return L


def cmd_update(_args):
    (RESEARCH_DIR / "index.md").write_text("\n".join(_index_lines()) + "\n", encoding="utf-8", newline="\n")
    print(f"updated: {RESEARCH_DIR / 'index.md'}")


def cmd_validate(_args):
    problems = []
    specs = [
        (HYP_DIR, "hypothesis", {"status", "created"}),
        (DEB_DIR, "debate", {"status", "created"}),
        (DEC_DIR, "decision", {"status", "created"}),
        (EXP_DIR, "experiment", {"status", "created"}),
        (FAIL_DIR, "failure", {"created"}),
        (REV_DIR, "review", {"created"}),
    ]
    for directory, kind, required in specs:
        seen = {}
        for p in sorted(directory.glob("*.md")):
            if not _is_record_path(p):
                continue
            fm = parse_frontmatter(p)
            if not fm:
                problems.append(f"{rel(p)}: missing/invalid front-matter")
                continue
            if fm.get("type") != kind:
                problems.append(f"{rel(p)}: type={fm.get('type')!r}, expected {kind!r}")
            if "example" not in fm or fm["example"] not in (True, False):
                problems.append(f"{rel(p)}: missing boolean 'example' field")
            for f in required:
                if f not in fm or fm[f] in (None, ""):
                    problems.append(f"{rel(p)}: missing required field '{f}'")
            i = fm.get("id") or p.stem
            if i in seen:
                problems.append(f"{rel(p)}: duplicate id {i} (also {rel(seen[i])})")
            seen[i] = p
            if not strip_frontmatter(p.read_text(encoding="utf-8")).strip():
                problems.append(f"{rel(p)}: empty body")
    for ag in discover_agents():
        for f in ("profile.md", "current_position.md", "beliefs.md"):
            if not (ag["_dir"] / f).exists():
                problems.append(f"{ag['name']}/{f}: missing")
    if problems:
        print("Validation FAILED:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("Validation OK — records are consistent; facts/opinions/decisions are separated by directory.")


def build_parser():
    p = argparse.ArgumentParser(prog="research", description="Kanamecide multi-agent research-memory CLI")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sub.add_parser("agents").set_defaults(func=cmd_agents)
    sub.add_parser("hypotheses").set_defaults(func=cmd_hypotheses)
    sub.add_parser("debates").set_defaults(func=cmd_debates)
    sub.add_parser("decisions").set_defaults(func=cmd_decisions)
    sub.add_parser("experiments").set_defaults(func=cmd_experiments)
    sub.add_parser("failures").set_defaults(func=cmd_failures)
    sub.add_parser("update").set_defaults(func=cmd_update)
    sub.add_parser("validate").set_defaults(func=cmd_validate)

    for name, dest in (("new-hypothesis", "cmd_new_hypothesis"), ("new-debate", "cmd_new_debate"),
                       ("new-decision", "cmd_new_decision"), ("new-experiment", "cmd_new_experiment"),
                       ("new-failure", "cmd_new_failure")):
        sp = sub.add_parser(name)
        sp.add_argument("--title", "-t")
        sp.set_defaults(func=globals()[dest])

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
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
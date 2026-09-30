#!/usr/bin/env python3
"""imem_core.py — the institutional-memory store: records, anchors, links, index.

WHY THIS MODULE EXISTS (measured, not argued — see agents/chief-architect/reports):
  * 75 of 208 records carry >= 8 record ids that appear ONLY in prose, so no tool can
    check them. Every "seam"/"pointer"/"L1376" repair session in S-0024..S-0033 is the
    cost of that blindness.
  * Line-number pointers (`L1376-L1377`) rot with every edit, so they had to be
    re-pinned by hand, in prose, across many sessions.
  * Findings (B1..B7, F-U1..F-U14, X1..X5, Z1..Z4) exist only as bold prose, so closure
    of a critique is a human reading exercise rather than a computed state.

DESIGN RULES (inherited from DEC-0007/0009/0011, never violated here):
  1. Markdown + YAML records remain the ONLY canonical store. This module is DERIVED
     (SQLite + JSON under research/_index/) and disposable: delete it and rebuild.
  2. Nothing here rewrites a record unless a command is explicitly asked to.
  3. Stdlib only, offline, deterministic: same corpus -> byte-identical outputs.
  4. Legacy records are grandfathered: a missing new field is a WARNING with a default,
     never a rewrite.

New primitives (normative description: research/INFRASTRUCTURE.md):
  * ANCHOR  — every heading gets a stable slug; `REC#slug` is a pointer that survives
              edits, and `anchors:` pins sha8 of a block, so drift is detectable and
              re-pinnable by one command instead of one session.
  * LINK    — typed edges from front-matter (authoritative), inline `[[ID#anchor]]`
              tokens, and prose ids (provenance-only, flagged).
  * FINDING — a machine-closeable defect raised by a review (findings/FND-####).
  * CLAIM   — an atomic, typed, direction-bearing statement (claims/CLM-####) the
              contradiction/priority engines reason over.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import research as R  # noqa: E402  (canonical paths, front-matter parser, id allocation)

RESEARCH_DIR = R.RESEARCH_DIR
REPO_ROOT = R.REPO_ROOT
INDEX_DIR = RESEARCH_DIR / "_index"
DB_PATH = INDEX_DIR / "imem.sqlite"
SNAPSHOT_PATH = INDEX_DIR / "imem.json"

CLAIMS_DIR = RESEARCH_DIR / "claims"
FINDINGS_DIR = RESEARCH_DIR / "findings"
ANALYSIS_DIR = RESEARCH_DIR / "_analysis"

SCHEMA_VERSION = 3

KIND_DIR = {
    "hypothesis": "hypotheses", "debate": "debates", "decision": "decisions",
    "experiment": "experiments", "failure": "failures", "review": "reviews",
    "work": "work", "handoff": "handoffs", "run": "runs", "session": "sessions",
    "question": "questions", "principle": "principles", "evidence": "evidence",
    "claim": "claims", "finding": "findings",
}
DIR_KIND = {v: k for k, v in KIND_DIR.items()}

# Legacy kinds keep research.py's vocabulary verbatim so the two tools can never
# disagree about a status.
STATUS_VOCAB_EXTRA = {
    "claim": {"OPEN", "SUPPORTED", "REJECTED", "INCONCLUSIVE", "SUPERSEDED", "UNTESTED",
              "DISPUTED"},
    "finding": {"OPEN", "RESOLVED", "DISPUTED", "WITHDRAWN", "SUPERSEDED"},
}
SEVERITY = ("blocking", "major", "minor", "nit")
SEVERITY_RANK = {s: i for i, s in enumerate(SEVERITY)}

# `direction` is a closed vocabulary rather than free text: free text is what made the
# H-0005-vs-H-0006 conflict need a hand-written antonym list.
DIRECTION = {
    "higher": 1, "increase": 1, "improves": 1, "faster": 1, "better": 1,
    "lower": -1, "decrease": -1, "regresses": -1, "slower": -1, "worse": -1,
    "no_effect": 0, "unchanged": 0, "non_monotonic": 0, "context_dependent": 0,
}
EPISTEMIC = ("observation", "fact", "hypothesis", "conjecture", "heuristic", "theorem",
             "proof", "implementation-detail", "benchmark-result", "correlational",
             "causal", "speculation", "question", "decision", "rejected")
DOMAINS = ("search", "evaluation", "movegen", "board", "hashing", "tt", "hardware",
           "data", "training", "process", "theory", "uci", "perft")

BUDGET_BYTES = 60_000
LINE_POINTER_RE = re.compile(r"(?<![A-Za-z0-9_])L(\d{3,5})(?:\s*[-\u2013]\s*L?(\d{3,5}))?")
ID_RE = re.compile(r"(?<![\w-])((?:H|D|DEC|E|F|R|Q|PR|EV|W|HO|RUN|S|CLM|FND)-\d{2,5})(?![\w-])")
INLINE_LINK_RE = re.compile(
    r"\[\[\s*((?:H|D|DEC|E|F|R|Q|PR|EV|W|HO|RUN|S|CLM|FND)-\d{2,5})"
    r"\s*(?:#([A-Za-z0-9._-]+))?\s*\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
FRONTMATTER_FENCE = re.compile(r"^---\s*$")
SKIP_DIR_PREFIXES = ("context/", "templates/", "scripts/", "manifests/", "_index/",
                     "_analysis/")


def today() -> str:
    return date.today().isoformat()


def sha8(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def norm_text(text: str) -> str:
    """Whitespace-normalized form used for hashing. Normalizing before hashing is what
    makes a content pin survive re-indentation and CRLF/LF churn — the two things that
    broke the hand-maintained pins in E-0013. Normalization is per line (leading and
    trailing whitespace per line is insignificant; the line structure is not)."""
    lines = [re.sub(r"[ \t]+", " ", ln.replace("\r", "")).strip()
             for ln in text.replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    while lines and not lines[0]:
        lines.pop(0)
    return "\n".join(lines)


def slugify(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[`*_\[\](){}<>#|:;,.!?'\u201c\u201d\u2018\u2019/\\]+", " ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-{2,}", "-", s).strip("-")[:80] or "section"


def jdump(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""



def as_list(v) -> list:
    if v in (None, "", [], {}):
        return []
    if isinstance(v, list):
        return [x for x in v if x not in (None, "")]
    return [v]


def as_float(v, default=None):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def split_frontmatter(text: str):
    """(fm_text, body) without a YAML library."""
    lines = text.splitlines()
    if not lines or not FRONTMATTER_FENCE.match(lines[0]):
        return "", text
    for i in range(1, len(lines)):
        if FRONTMATTER_FENCE.match(lines[i]):
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return "", text


# --- anchors --------------------------------------------------------------------------

@dataclass
class Block:
    """A heading-delimited block of a record. `slug` is the durable anchor name."""
    slug: str
    level: int
    title: str
    start: int          # 1-based line of the heading
    end: int            # 1-based line of the next heading (or EOF), exclusive
    body: str
    sha8: str

    def as_dict(self):
        return {"slug": self.slug, "level": self.level, "title": self.title,
                "start": self.start, "end": self.end, "sha8": self.sha8}


def blocks_of(body: str) -> list:
    """Every heading-delimited block, with a slug unique within the record.

    Duplicate headings get `-2`, `-3` suffixes in document order, so an anchor never
    silently means two different things — the failure mode that made "seam 8" and
    "B5 s2" ambiguous in E-0013.
    """
    lines = body.splitlines()
    heads = [(i, HEADING_RE.match(l)) for i, l in enumerate(lines)]
    heads = [(i, m) for i, m in heads if m]
    out, used = [], {}
    for idx, (i, m) in enumerate(heads):
        nxt = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        title = m.group(2)
        base = slugify(title)
        used[base] = used.get(base, 0) + 1
        slug = base if used[base] == 1 else f"{base}-{used[base]}"
        chunk = "\n".join(lines[i + 1:nxt]).strip()
        out.append(Block(slug=slug, level=len(m.group(1)), title=title, start=i + 1,
                         end=nxt, body=chunk, sha8=sha8(norm_text(chunk))))
    return out


def anchor_table(text: str) -> dict:
    """slug -> sha8 for a record's body blocks (the machine-pinnable view)."""
    _, body = split_frontmatter(text)
    return {b.slug: b.sha8 for b in blocks_of(body)}


def parse_pointer(pointer: str):
    """'E-0013#z1-severed-sentence' -> ('E-0013', 'z1-severed-sentence')."""
    if "#" in pointer:
        rec, _, anchor = pointer.partition("#")
        return (rec or None, anchor or None)
    return (pointer, None)


def suggest_anchor(want: str, anchors) -> str:
    """Cheapest mechanical suggestion for a broken anchor: prefix match, then best token
    overlap. Deterministic tie-break by name; no fuzzy library, no network."""
    if not anchors or not want:
        return None
    if want in anchors:
        return want
    cands = [a for a in anchors if a.startswith(want[:12])]
    if not cands:
        want_t = set(want.split("-"))
        scored = []
        for a in anchors:
            a_t = set(a.split("-"))
            if not a_t:
                continue
            scored.append((len(want_t & a_t) / len(want_t | a_t), a))
        scored.sort(key=lambda kv: (-kv[0], kv[1]))
        return scored[0][1] if scored and scored[0][0] >= 0.34 else None
    cands.sort(key=lambda a: (abs(len(a) - len(want)), a))
    return cands[0]


# --- records ---------------------------------------------------------------------------

# front-matter field -> edge kind. These are AUTHORITATIVE links (a machine wrote them as
# data), unlike prose mentions.
EDGE_FIELDS = {
    "tests": "tests", "hypothesis": "tests", "supports": "supports",
    "contradicts": "contradicts", "depends_on": "depends-on", "target": "reviews",
    "supersedes": "supersedes", "superseded_by": "superseded-by", "verifies": "verifies",
    "verified_by": "verified-by", "derived_from": "derived-from", "implements": "implements",
    "falsified_by": "falsified-by", "answers": "answers", "blocked_by": "blocked-by",
    "resolved_by": "resolved-by", "evidence": "evidences", "cites": "cites",
    "related": "related", "owner": "owned-by", "author": "authored-by",
    "reviewer": "reviewed-by", "agent": "authored-by", "from": "requested-by",
    "to": "requested-of", "amends": "amends", "review": "raised-in",
    "revisit_when": "revisit-trigger", "tested_by": "tested-by",
    "evidence_for": "supports", "evidence_against": "contradicts",
    "implemented_by": "implemented-in", "touches-code": "implemented-in",
    "raised_by": "raised-by", "resolved_by_agent": "resolved-by",
}
# Which typed edges a reviewer may rely on when walking the graph (the vocabulary the
# INFRASTRUCTURE doc publishes).
RELATIONS = ("tests", "tested-by", "supports", "contradicts", "depends-on", "supersedes",
             "superseded-by", "verifies", "verified-by", "derived-from", "implements",
             "implemented-in", "falsified-by", "answers", "blocked-by", "resolved-by",
             "evidences", "cites", "related", "owned-by", "authored-by", "reviewed-by",
             "raised-by", "raised-in", "amends", "revisit-trigger", "mentions")


@dataclass
class Record:
    key: str                 # repo-relative posix path under research/
    path: Path
    fm: dict
    type: str
    id: str
    title: str
    status: str
    body: str
    text: str
    blocks: list
    links_fm: list = None      # [(rel, dst_id, dst_anchor, weight)]
    links_inline: list = None
    ids_prose: list = None
    anchors_pinned: dict = None
    size: int = 0

    def as_dict(self):
        return {"key": self.key, "id": self.id, "type": self.type, "title": self.title,
                "status": self.status, "size": self.size,
                "fm": {k: v for k, v in self.fm.items()},
                "blocks": [b.as_dict() for b in self.blocks],
                "anchors_pinned": self.anchors_pinned or {}}


def guess_type(path: Path, fm: dict) -> str:
    t = str(fm.get("type") or "")
    if t in KIND_DIR or t == "report":
        return t
    rel = path.relative_to(RESEARCH_DIR).as_posix()
    parts = rel.split("/")
    if len(parts) >= 2 and parts[-2] == "reports":
        return "report"
    for part in parts[:-1]:
        if part in DIR_KIND:
            return DIR_KIND[part]
    return "doc"


def load_record(path: Path) -> Record:
    text = read_text(path)
    fm = R.parse_frontmatter(path)
    body = R.strip_frontmatter(text)
    rel = path.relative_to(RESEARCH_DIR).as_posix()
    typ = guess_type(path, fm)
    rec = Record(key=rel, path=path, fm=fm or {}, type=typ,
                 id=str((fm or {}).get("id") or path.stem),
                 title=str((fm or {}).get("title") or (fm or {}).get("name") or path.stem),
                 status=str((fm or {}).get("status") or "\u2014"),
                 body=body, text=text, blocks=blocks_of(body), size=len(text))
    rec.anchors_pinned = {str(k): str(v) for k, v in (as_dict_pairs(fm.get("anchors"))).items()}
    rec.links_fm, rec.links_inline, rec.ids_prose = extract_links(rec)
    return rec


def as_dict_pairs(v) -> dict:
    """Accept either a mapping or a list of 'slug: hash' / 'slug=hash' strings."""
    out = {}
    if isinstance(v, dict):
        return {str(k): str(x) for k, x in v.items()}
    for item in as_list(v):
        s = str(item)
        for sep in (":", "="):
            if sep in s:
                k, _, x = s.partition(sep)
                out[k.strip()] = x.strip()
                break
    return out


def extract_links(rec: Record):
    """Three tiers of linkage, kept separate so a reader can weigh them:

    * front-matter (authoritative; machine-checked),
    * inline `[[ID#anchor]]` (explicit, still machine-checked),
    * prose mentions (provenance only — flagged by lint, never trusted as structure).
    """
    fm_links, anchor_seen = [], set()
    for field, rel in EDGE_FIELDS.items():
        for val in as_list(rec.fm.get(field)):
            s = str(val)
            rid, anchor = parse_pointer(s)
            if not rid or not ID_RE.fullmatch(rid):
                continue
            anchor_seen.add(anchor)
            fm_links.append((rel, rid, anchor, field))
    inline = []
    for m in INLINE_LINK_RE.finditer(rec.body):
        inline.append(("mentions", m.group(1), m.group(2), "inline"))
    fm_ids = {r for _, r, _, _ in fm_links}
    prose = sorted((set(ID_RE.findall(rec.body)) - fm_ids) - {rec.id})
    return fm_links, inline, prose


SRC_PATH_RE = re.compile(r"\b((?:src|tools)/[A-Za-z0-9_./-]+\.(cpp|h|py))\b")
COMMIT_RE = re.compile(r"(?<![\w./-])([0-9a-f]{7,10})(?![\w./-])")


def code_refs(text: str):
    files = sorted(set(m[0] for m in SRC_PATH_RE.findall(text)))
    commits = sorted({m for m in COMMIT_RE.findall(text) if any(c in "abcdef" for c in m)})
    return files, commits


def load_corpus(with_reports: bool = True, extra_dirs=()):
    """{key: Record} for every knowledge-bearing .md under research/, plus warnings.

    Warnings (not errors) are returned alongside, so a caller can report what it could
    not parse instead of silently dropping it — "silence is a bug" (DEC-0011 rule 2).
    """
    records, warnings = {}, []
    for p in sorted(RESEARCH_DIR.rglob("*.md")):
        rel = p.relative_to(RESEARCH_DIR).as_posix()
        if p.name.startswith("_") or p.name in ("index.md", "state.md", ".gitkeep"):
            continue
        if rel.startswith(SKIP_DIR_PREFIXES):
            continue
        if not with_reports and "/reports/" in rel:
            continue
        if extra_dirs and not any(rel.startswith(d) for d in extra_dirs):
            continue
        try:
            rec = load_record(p)
        except Exception as exc:                      # never drop a file silently
            warnings.append({"area": "parse", "rel": rel, "msg": f"unreadable: {exc!r}"})
            continue
        records[rel] = rec
        if rec.type not in ("report", "doc"):
            missing = [k for k in ("id", "type", "status") if not rec.fm.get(k)]
            if missing:
                warnings.append({"area": "frontmatter", "rel": rel,
                                 "msg": "missing " + ", ".join(missing) + " (grandfathered)"})
    return records, warnings


def records_of_type(records: dict, *types) -> list:
    want = set(types)
    return [r for r in sorted(records.values(), key=lambda x: x.id) if r.type in want]


def id_index(records: dict) -> dict:
    idx = {}
    for rec in records.values():
        idx.setdefault(rec.id, []).append(rec)
    return idx


def by_id(records: dict, rid: str):
    for rec in records.values():
        if rec.id == rid:
            return rec
    return None


def anchors_of(records: dict, rid: str) -> dict:
    rec = by_id(records, rid)
    return anchor_table(rec.text) if rec else {}



# --- the compiled index (SQLite; derived, disposable) ---------------------------------

DDL = """
CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE IF NOT EXISTS records (
  key TEXT PRIMARY KEY, id TEXT, type TEXT, title TEXT, status TEXT, size INTEGER,
  created TEXT, updated TEXT, owner TEXT, confidence TEXT, result TEXT,
  sha256 TEXT, fm_json TEXT);
CREATE TABLE IF NOT EXISTS blocks (
  key TEXT, slug TEXT, level INTEGER, title TEXT, start INTEGER, "end" INTEGER,
  sha8 TEXT, pinned TEXT, body TEXT, PRIMARY KEY (key, slug));
CREATE TABLE IF NOT EXISTS links (
  src_key TEXT, src_id TEXT, rel TEXT, dst_id TEXT, dst_anchor TEXT, field TEXT,
  tier TEXT, resolved TEXT);
CREATE TABLE IF NOT EXISTS code_refs (key TEXT, path TEXT, commit_hash TEXT, tier TEXT);
CREATE TABLE IF NOT EXISTS tags (key TEXT, tag TEXT);
CREATE INDEX IF NOT EXISTS links_dst ON links(dst_id);
CREATE INDEX IF NOT EXISTS recs_type ON records(type, status);
"""


def file_sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return "unreadable"


def link_resolves(records: dict, dst: str, anchor) -> str:
    idx = id_index(records)
    if dst not in idx:
        return "no"
    if anchor:
        rec = idx[dst][0]
        if anchor not in {b.slug for b in rec.blocks}:
            return "anchor-missing"
    return "yes"


def build_db(records: dict, path: Path = DB_PATH) -> dict:
    """Rebuild the SQLite index from scratch (deterministic content; the file is cache)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    con = sqlite3.connect(str(path))
    con.executescript(DDL)
    n_links = n_bad = 0
    for key, rec in sorted(records.items()):
        files, commits = code_refs(rec.text)
        con.execute(
            "INSERT OR REPLACE INTO records VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (key, rec.id, rec.type, rec.title, rec.status, rec.size,
             str(rec.fm.get("created") or ""),
             str(rec.fm.get("last_updated") or rec.fm.get("closed")
                 or rec.fm.get("completed") or ""),
             str(rec.fm.get("owner") or rec.fm.get("author") or rec.fm.get("agent") or ""),
             str(rec.fm.get("confidence") or ""), str(rec.fm.get("result") or "")[:200],
             hashlib.sha256(rec.text.encode("utf-8")).hexdigest(),
             jdump(rec.fm).strip()))
        for b in rec.blocks:
            con.execute('INSERT OR REPLACE INTO blocks VALUES (?,?,?,?,?,?,?,?,?)',
                        (key, b.slug, b.level, b.title, b.start, b.end, b.sha8,
                         (rec.anchors_pinned or {}).get(b.slug, ""), b.body[:4000]))
        fm_set = {(rel, dst) for rel, dst, anch, fld in rec.links_fm}
        for rel, dst, anch, fld in rec.links_fm + rec.links_inline:
            tier = "frontmatter" if (rel, dst) in fm_set else "inline"
            st = link_resolves(records, dst, anch)
            if st != "yes":
                n_bad += 1
            con.execute("INSERT INTO links VALUES (?,?,?,?,?,?,?,?)",
                        (key, rec.id, rel, dst, anch or "", fld, tier, st))
            n_links += 1
        for f in files:
            con.execute("INSERT INTO code_refs VALUES (?,?,?,?)", (key, f, "", "path"))
        for c in commits:
            con.execute("INSERT INTO code_refs VALUES (?,?,?,?)", (key, "", c, "commit"))
        for t in as_list(rec.fm.get("tags")):
            con.execute("INSERT INTO tags VALUES (?,?)", (key, str(t)))
    con.execute("INSERT OR REPLACE INTO meta VALUES ('schema_version', ?)",
                (str(SCHEMA_VERSION),))
    con.execute("INSERT OR REPLACE INTO meta VALUES ('generated', ?)", (today(),))
    con.execute("INSERT OR REPLACE INTO meta VALUES ('records', ?)", (str(len(records)),))
    con.commit()
    con.close()
    return {"db": DB_PATH.relative_to(REPO_ROOT).as_posix(), "records": len(records),
            "links": n_links, "unresolved_links": n_bad}


# --- lint: mechanical memory integrity ------------------------------------------------

PROSE_LINK_WARN_AT = 8        # measured: 75 of 208 legacy records sit at or above this


def vocab_for(typ: str):
    v = dict(R.STATUS_VOCAB)
    v.update(STATUS_VOCAB_EXTRA)
    return v.get(typ)


def lint(records: dict, findings: list, claims: list, warnings: list = None) -> dict:
    """Every check here exists because a measured pathology made it necessary. Output is
    `problems` (blocking), `warnings` (advisory), `findings` (work queue for agents)."""
    problems, warns, queue = [], [], []
    idx = id_index(records)
    for w in (warnings or []):
        warns.append(w)

    for key, rec in sorted(records.items()):
        vocab = vocab_for(rec.type)
        if vocab and rec.status not in vocab:
            problems.append({"area": "status", "rel": key,
                             "msg": f"status={rec.status!r} not in the {rec.type} vocabulary"})
        # 1. links declared in front matter must resolve (id AND anchor)
        for rel, dst, anchor, fld in rec.links_fm:
            st = link_resolves(records, dst, anchor)
            if st == "no":
                problems.append({"area": "link", "rel": key,
                                 "msg": f"{fld}: {dst} does not exist (unresolvable link)"})
            elif st == "anchor-missing":
                sug = suggest_anchor(anchor, anchors_of(records, dst).keys())
                problems.append({"area": "link", "rel": key,
                                 "msg": f"{fld}: {dst}#{anchor} has no such anchor"
                                        + (f" — did you mean {dst}#{sug}?" if sug else "")})
        # 2. inline links
        for rel, dst, anchor, fld in rec.links_inline:
            st = link_resolves(records, dst, anchor)
            if st != "yes":
                problems.append({"area": "inline-link", "rel": key,
                                 "msg": f"[[{dst}{'#' + anchor if anchor else ''}]] does not resolve"})
        # 3. prose-only ids: not an error (history is append-only) but a retrieval debt
        if len(rec.ids_prose) >= PROSE_LINK_WARN_AT:
            warns.append({"area": "prose-links", "rel": key,
                          "msg": f"{len(rec.ids_prose)} ids appear only in prose "
                                 f"(uncheckable) — declare the ones you mean in front matter "
                                 f"or as [[ID]]"})
        # 4. line-number pointers rot; anchors do not
        lp = LINE_POINTER_RE.findall(rec.body)
        if lp:
            warns.append({"area": "line-pointer", "rel": key,
                          "msg": f"{len(lp)} line-number pointer(s) (e.g. L{lp[0][0]}) — "
                                 f"use REC#anchor instead"})
        # 5. size budget (a 214 KB record is unreadable and un-repairable)
        if rec.size > BUDGET_BYTES and str(rec.fm.get("kind") or "") != "container":
            warns.append({"area": "budget", "rel": key,
                          "msg": f"{rec.size} bytes > {BUDGET_BYTES} budget — split into "
                                 f"atomic records or set `kind: container` with a rationale"})
        # 6. pinned anchors must still match the block
        for slug, pin in (rec.anchors_pinned or {}).items():
            actual = {b.slug: b.sha8 for b in rec.blocks}.get(slug)
            if actual is None:
                problems.append({"area": "anchor", "rel": key,
                                 "msg": f"anchors: pins '{slug}' but no such heading remains"})
            elif pin and pin != actual:
                warns.append({"area": "anchor-drift", "rel": key,
                              "msg": f"anchor '{slug}' pinned {pin} but block hashes {actual} "
                                     f"— re-pin after reviewing the change (`imem repin`)"})
    # 7. findings block their targets
    by_target = {}
    for f in findings:
        if str(f.fm.get("status")) == "OPEN" and f.fm.get("severity") == "blocking":
            tgt, _ = parse_pointer(str(f.fm.get("target") or ""))
            by_target.setdefault(tgt, []).append(f.id)
    for tgt, fids in sorted(by_target.items()):
        rec = by_id(records, tgt) if tgt else None
        if rec is None:
            queue.append({"area": "finding", "msg": f"blocking findings {fids} target missing "
                                                     f"record {tgt}"})
            continue
        gate = str(rec.fm.get("status")) in ("RUNNING", "COMPLETED")
        (problems if gate else queue).append(
            {"area": "finding", "rel": rec.key,
             "msg": f"{rec.status} target carries OPEN blocking findings: {', '.join(fids)}"})
    return {"problems": problems, "warnings": warns, "findings": queue}


# --- repair: mechanical, reviewable, opt-in ------------------------------------------

def render_anchors_block(pairs: dict) -> list:
    """Canonical anchors declaration, using the SAME YAML subset research.py parses:
    an inline list of 'slug:sha8' strings. (Nested maps are not in the subset, and a
    pin format the project's own parser cannot read would be a trap, not a feature.)"""
    items = ", ".join(f'"{k}:{pairs[k]}"' for k in sorted(pairs))
    return [f"anchors: [{items}]"] if pairs else ["anchors: []"]


def repin_frontmatter(text: str, pairs: dict, section: str = "anchors") -> str:
    """Return `text` with its front-matter `anchors:` declaration replaced by `pairs`.

    Surgical on purpose: the body is returned byte-identical, and only the named
    front-matter section is touched. Handles both forms a legacy record may use:
    a scalar/inline value on the key line, and an indented block sequence below it.
    This is the mechanical replacement for the hand-written 're-pin' sessions
    (S-0032 Z3, S-0039 RULING 3).
    """
    lines = text.splitlines()
    if not lines or not FRONTMATTER_FENCE.match(lines[0]):
        return text
    end = None
    for i in range(1, len(lines)):
        if FRONTMATTER_FENCE.match(lines[i]):
            end = i
            break
    if end is None:
        return text
    head, fm, tail = lines[:1], lines[1:end], lines[end:]
    out, i, replaced = [], 0, False
    while i < len(fm):
        line = fm[i]
        if re.match(rf"^{re.escape(section)}\s*:", line):
            out.extend(render_anchors_block(pairs))
            i += 1
            while i < len(fm) and fm[i].strip() and (fm[i].startswith((" ", "\t")) or
                                                     fm[i].lstrip().startswith("- ")):
                i += 1
            replaced = True
            continue
        out.append(line)
        i += 1
    if not replaced:
        out.extend(render_anchors_block(pairs))
    return "\n".join(head + out + tail) + ("\n" if text.endswith("\n") else "")


def repin_file(path: Path, only_slugs=None) -> dict:
    text = read_text(path)
    table = anchor_table(text)
    if only_slugs:
        keep = {k: v for k, v in table.items() if k in set(only_slugs)}
    else:
        keep = table
    new_text = repin_frontmatter(text, keep)
    changed = new_text != text
    if changed:
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return {"rel": path.relative_to(RESEARCH_DIR).as_posix(), "anchors": len(keep),
            "changed": changed}


def new_record(kind: str, title: str, body_lines=None, extra=None) -> Path:
    """Scaffold a claim/finding/other record with the next free id (never overwrites)."""
    if kind not in KIND_DIR:
        raise ValueError(f"unknown kind {kind!r}")
    directory = RESEARCH_DIR / KIND_DIR[kind]
    directory.mkdir(parents=True, exist_ok=True)
    prefix = {"claim": "CLM-", "finding": "FND-", "hypothesis": "H-",
              "decision": "DEC-", "experiment": "E-", "question": "Q-",
              "principle": "PR-", "work": "W-", "review": "R-", "failure": "F-",
              "run": "RUN-", "handoff": "HO-", "session": "S-",
              "evidence": "EV-", "debate": "D-"}[kind]
    width = {"experiment": 5}.get(kind, 4)
    rid = R.next_id(directory, prefix, width)
    fm = {"id": rid, "type": kind, "title": f'"{title}"', "status": "OPEN",
          "example": "false", "created": today()}
    for k, v in (extra or {}).items():
        fm[k] = v
    path = directory / f"{rid}-{R.slugify(title)}.md"
    text = ["---"] + [f"{k}: {v}" for k, v in fm.items()] + ["---", ""]
    text += [f"# {rid}", ""]
    text += (body_lines or [])
    R.write_new(path, "\n".join(text) + "\n")
    return path


# --- snapshot: a human- and git-friendly JSON view of the index -----------------------

def write_snapshot(records: dict, out: dict, path: Path = SNAPSHOT_PATH) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(jdump(out), encoding="utf-8", newline="\n")
    return {"snapshot": path.relative_to(REPO_ROOT).as_posix(),
            "records": len(records), "bytes": path.stat().st_size}


if __name__ == "__main__":       # tiny self-demo: python imem_core.py <ID>
    recs, _w = load_corpus()
    target = sys.argv[1] if len(sys.argv) > 1 else None
    if target:
        rec = by_id(recs, target)
        if rec is None:
            print(f"no record {target}")
            raise SystemExit(1)
        print(f"{rec.id} {rec.type} {rec.status} {rec.size}B {rec.key}")
        for b in rec.blocks[:40]:
            print(f"  {b.slug:52} {b.sha8}  L{b.start}-{b.end}")
    else:
        print(f"records={len(recs)}")


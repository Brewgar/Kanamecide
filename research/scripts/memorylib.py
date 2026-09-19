#!/usr/bin/env python3
"""memorylib.py — the derived-intelligence layer of the Kanamecide research memory.

WHY THIS EXISTS (DEC-0011, amends DEC-0007/DEC-0009).
DEC-0007 gave the project a disciplined, append-only, human-readable record store.
DEC-0009 gave it verification gates and coordination records. Neither gave it:

  * typed relations between records (a knowledge graph that is actually populated);
  * ranked retrieval (the old `context --topic` dumped whole files by substring match
    into a single 139 KB pack);
  * contradiction / duplication / revival detection (the H-0005 backwards bound and the
    H-0006-vs-D-0003 bound conflict were found by hand, a round late);
  * a computed "current best belief" projection with the evidence rollup attached;
  * a persistent open-questions registry (Q-####);
  * a first-class evidence registry with hashes and regeneration commands;
  * code/provenance traceability (record -> src file/symbol -> commit -> experiment);
  * memory-integrity audits, observability metrics, and tests for the memory itself.

DESIGN RULES (load-bearing, in priority order):
  1. The Markdown records remain the ONLY source of truth (DEC-0007 retained).
     Everything here is DERIVED and recomputable: delete it and re-run; nothing is lost.
  2. Nothing here rewrites a record, invents a fact, or merges two records. Detectors
     emit CANDIDATES; an agent decides. Silence is a bug, so every scan reports what it
     could not read instead of dropping it.
  3. Every derived stance is labelled a PROJECTION with the record ids it came from: a
     pointer that says "go read these records", never a conclusion.
  4. Stdlib only, offline, deterministic: same repo -> byte-identical output.
  5. Backwards compatible: legacy records load with documented defaults and are reported
     as warnings, never errors (records are append-only).

Used by `research.py` (canonical CLI) and by `kgraph.py` (compatibility shim).
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import research as R  # canonical paths + front-matter/record primitives (no side effects)

RESEARCH_DIR = R.RESEARCH_DIR
REPO_ROOT = R.REPO_ROOT

QUESTIONS_DIR = RESEARCH_DIR / "questions"
PRINCIPLES_DIR = RESEARCH_DIR / "principles"
EVIDENCE_DIR = RESEARCH_DIR / "evidence"
SRC_DIR = REPO_ROOT / "src"
TOOLS_DIR = REPO_ROOT / "tools"

SCHEMA_VERSION = 2

# L0 raw evidence (evidence/) | L1 events (work/handoff/run/session/experiment)
# L2 knowledge (hypothesis/debate/decision/review/failure) | L3 state (generated)
# L4 strategic+meta (principles/) | L5 agent memory (agents/) | L6 meta (audit metrics)
LAYERS = {
    "evidence": 0, "run": 1, "work": 1, "handoff": 1, "session": 1, "experiment": 1,
    "hypothesis": 2, "debate": 2, "decision": 2, "review": 2, "failure": 2,
    "question": 3, "principle": 4, "report": 5, "doc": 6,
}

STATUS_VOCAB = dict(R.STATUS_VOCAB)
STATUS_VOCAB.update({
    "question": {"OPEN", "INVESTIGATING", "ANSWERED", "BLOCKED", "ABANDONED", "SUPERSEDED"},
    "principle": {"ACTIVE", "REVISED", "RETIRED"},
    "evidence": {"REGISTERED", "SUPERSEDED", "LOST"},
})

# front-matter field -> edge kind (src record -> dst record)
EDGE_STRUCTURAL = {
    "hypothesis": "tests", "tests": "tests", "supports": "supports",
    "contradicts": "contradicts", "depends_on": "depends-on", "target": "reviews",
    "superseded_by": "superseded_by", "supersedes": "supersedes",
    "work_item": "work_item", "verifies": "verifies", "derived_from": "derived-from",
    "implements": "implements", "falsifier": "falsified-by", "revisit_when": "revisit-when",
    "answers": "answers", "blocked_by": "blocked-by", "resolved_by": "resolved_by",
    "evidence": "evidenced-by", "source": "sourced-from", "related": "related",
}
EDGE_ACTOR = {
    "reviewer": "reviewed-by", "owner": "owned-by", "agent": "authored-by",
    "author": "authored-by", "from": "from-agent", "to": "to-agent",
    "verified_by": "verified-by",
}
VERDICT_POSITIVE = ("PASS", "WIN")
VERDICT_NEGATIVE = ("FAIL", "FAILED", "LOSS")
VERDICT_NEUTRAL = ("NEUTRAL", "INCONCLUSIVE")

CONFIDENCE_LADDER = (
    (0.00, "speculative"), (0.30, "plausible"), (0.55, "likely"),
    (0.75, "strongly supported"), (0.90, "high-author-confidence"),
)

ID_RE = re.compile(r"\b(?:DEC|H|D|E|F|R|W|HO|RUN|S|Q|PR|EV)-\d{3,5}\b")
SRC_PATH_RE = re.compile(r"\bsrc[\\/]([\w.\-]+)")
TOOLS_PATH_RE = re.compile(r"\btools[\\/]([\w.\-/]+)")
COMMIT_RE = re.compile(r"(?<![\w./-])([0-9a-f]{7,10})(?![\w./-])")


def commit_refs(text: str) -> set:
    """Short git hashes written in prose. Require at least one hex letter so a numeric
    count like 4865609 (4,865,609 perft nodes) is never mistaken for a commit."""
    return {m for m in COMMIT_RE.findall(text) if any(c in "abcdef" for c in m) and len(m) <= 40}

_SKIP_DIR_PREFIXES = ("context/", "templates/", "scripts/", "runs/")


def today() -> str:
    return date.today().isoformat()


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def confidence_label(v) -> str:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return "—"
    lab = CONFIDENCE_LADDER[0][1]
    for lo, name in CONFIDENCE_LADDER:
        if x >= lo:
            lab = name
    return lab


def sha256_file(path: Path) -> str:
    try:
        h = hashlib.sha256()
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return "unreadable"


def as_list(v) -> list:
    if v in (None, "", [], {}):
        return []
    return list(v) if isinstance(v, list) else [v]


def json_dump(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


# --- corpus ----------------------------------------------------------------------

def _guess_kind(relpath: str, fm: dict) -> str:
    t = fm.get("type")
    if t:
        return str(t)
    guess = {"hypotheses": "hypothesis", "debates": "debate", "decisions": "decision",
             "experiments": "experiment", "failures": "failure", "reviews": "review",
             "work": "work", "handoffs": "handoff", "questions": "question",
             "principles": "principle", "evidence": "evidence",
             "sessions": "session", "runs": "run"}
    for part in relpath.replace("\\", "/").split("/")[:-1]:
        if part in guess:
            return guess[part]
    return "doc"


def load_nodes(include_reports: bool = True) -> dict:
    """{node_key: node} for every knowledge-bearing .md under research/.

    Agent reports ARE included: they were previously invisible to index.md, to
    `validate`, and to retrieval — 115 KB of the project's deepest analysis (R-0005 F1).
    """
    nodes: dict = {}
    for p in sorted(RESEARCH_DIR.rglob("*.md")):
        rel = p.relative_to(RESEARCH_DIR).as_posix()
        if p.name.startswith("_") or p.name in ("index.md", "state.md", ".gitkeep"):
            continue
        if rel.startswith(_SKIP_DIR_PREFIXES):
            continue
        if not include_reports and "/reports/" in rel:
            continue
        fm = R.parse_frontmatter(p)
        body = R.strip_frontmatter(R.read_text(p))
        kind = _guess_kind(rel, fm)
        nodes[rel] = {
            "key": rel,
            "id": str(fm.get("id") or p.stem),
            "kind": kind,
            "layer": LAYERS.get(kind, 2),
            "path": p,
            "rel": rel,
            "title": str(fm.get("title") or fm.get("name") or p.stem.replace("-", " ")),
            "status": str(fm.get("status") or "—"),
            "created": str(fm.get("created") or fm.get("last_updated") or ""),
            "closed": str(fm.get("closed") or fm.get("completed") or ""),
            "example": bool(fm.get("example")),
            "tags": fm.get("tags") if isinstance(fm.get("tags"), list) else [],
            "fm": fm,
            "text": body,
        }
    return nodes


def id_index(nodes: dict) -> dict:
    """Record id -> [node keys]. Ambiguous ids map to ALL their nodes (never silently)."""
    idx: dict = {}
    for k, n in nodes.items():
        idx.setdefault(n["id"], []).append(k)
    return idx


def fm_refs(fm: dict, field: str) -> list:
    out = []
    for x in as_list(fm.get(field)):
        out.extend(ID_RE.findall(str(x)))
    return out


def missing_reference_targets(nodes: dict) -> list:
    """Ids referenced anywhere (front-matter or prose) that no record defines."""
    known = set(id_index(nodes))
    seen: dict = {}
    for key, n in nodes.items():
        refs = set(ID_RE.findall(n["text"])) | set(ID_RE.findall(n["title"]))
        for field in EDGE_STRUCTURAL:
            refs |= set(fm_refs(n["fm"], field))
        for ref in sorted(refs):
            if ref not in known:
                seen.setdefault(ref, []).append(key)
    return [{"id": rid, "referenced_by": sorted(set(s))} for rid, s in sorted(seen.items())]


# --- code nodes (phase-2 traceability: record -> code -> commit -> experiment) ----

_SYM_RE = re.compile(
    r"^\s*(?:static\s+|inline\s+|constexpr\s+|const\s+|template\s*<[^>]*>\s*)*"
    r"(?:[A-Za-z_][\w:<>,*&\s]*?)\b(\w+)\s*\([^;]*\)\s*(?:const\s*)?\{", re.M)
_TYPE_RE = re.compile(r"^\s*(?:struct|class|enum(?:\s+class)?)\s+(\w+)", re.M)


def code_nodes() -> dict:
    """{node_key: code node} for src/ and tools/ files (files + declared symbols)."""
    out: dict = {}
    for base, prefix in ((SRC_DIR, "src"), (TOOLS_DIR, "tools")):
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file() or p.suffix.lower() not in (".cpp", ".h", ".hpp", ".cc", ".py"):
                continue
            rel = f"{prefix}/{p.relative_to(base).as_posix()}"
            text = p.read_text(encoding="utf-8", errors="replace")
            syms = sorted(set(_SYM_RE.findall(text)) | set(_TYPE_RE.findall(text)))
            out[rel] = {
                "key": rel, "kind": "code", "layer": 5, "path": p, "rel": rel,
                "title": rel, "status": "PRESENT", "created": "", "closed": "",
                "example": False, "tags": [prefix], "symbols": syms,
                "lines": text.count("\n") + 1, "sha256": sha256_file(p),
                "fm": {}, "text": text,
            }
    return out
# --- graph ------------------------------------------------------------------------

def build_graph(nodes: dict, code: dict | None = None):
    """Return (edges, idx). edges: sorted list of dicts {src, kind, dst, why}.

    Typed edges come from front-matter relations (EDGE_STRUCTURAL), actor fields
    (EDGE_ACTOR), explicit code/commit touchpoints (src/ or tools/ paths and short
    commit hashes written anywhere in a record), and `mentions` from prose record ids.
    """
    code = code if code is not None else {}
    idx = id_index(nodes)
    edges = []

    def add(src, kind, dst, why):
        if src != dst:
            edges.append({"src": src, "kind": kind, "dst": dst, "why": why})

    for key, n in nodes.items():
        for field, ekind in EDGE_STRUCTURAL.items():
            for ref in fm_refs(n["fm"], field):
                for dst in idx.get(ref, []):
                    add(key, ekind, dst, f"front-matter {field}={ref}")
        for field, ekind in EDGE_ACTOR.items():
            actor = n["fm"].get(field)
            if not actor:
                continue
            for key2, n2 in nodes.items():
                if key2 == key:
                    continue
                if n2["fm"].get("agent") == actor or n2["id"] == str(actor):
                    add(key, ekind, key2, f"front-matter {field}={actor}")
        # code touchpoints
        for m in sorted(set(SRC_PATH_RE.findall(n["text"])) | set(SRC_PATH_RE.findall(n["title"]))):
            for ck in code:
                if ck.endswith("/" + m):
                    add(key, "touches-code", ck, "src/ path in prose")
        for m in sorted(set(TOOLS_PATH_RE.findall(n["text"]))):
            for ck in code:
                if ck.endswith("/" + m):
                    add(key, "touches-code", ck, "tools/ path in prose")
        # prose id mentions
        for ref in sorted(set(ID_RE.findall(n["text"])) | set(ID_RE.findall(n["title"]))):
            for dst in idx.get(ref, []):
                add(key, "mentions", dst, f"prose id {ref}")
    # merge duplicate (src,kind,dst) triples, keeping sorted `why` provenance
    merged: dict = {}
    for e in edges:
        k = (e["src"], e["kind"], e["dst"])
        merged.setdefault(k, set()).add(e["why"])
    out = [{"src": s, "kind": k, "dst": d, "why": sorted(ws)}
           for (s, k, d), ws in sorted(merged.items())]
    return out, idx


def edges_of(edges, key: str):
    """(incoming, outgoing) edge lists for a node key."""
    inc = [(e["kind"], e["src"], e["why"]) for e in edges if e["dst"] == key]
    outg = [(e["kind"], e["dst"], e["why"]) for e in edges if e["src"] == key]
    return inc, outg


def neighbours(edges, key: str, depth: int = 1) -> dict:
    """BFS over the undirected edge set. {node_key: (distance, first_edge_kind)}."""
    if depth < 1:
        return {}
    adj: dict = {}
    for e in edges:
        adj.setdefault(e["src"], []).append((e["dst"], e["kind"]))
        adj.setdefault(e["dst"], []).append((e["src"], e["kind"]))
    seen = {key: (0, "self")}
    frontier = [key]
    for d in range(1, depth + 1):
        nxt = []
        for cur in frontier:
            for other, kind in sorted(adj.get(cur, [])):
                if other not in seen:
                    seen[other] = (d, kind)
                    nxt.append(other)
        frontier = nxt
    seen.pop(key, None)
    return seen


# --- text IR (BM25) ---------------------------------------------------------------

_STOP = set(("the a an and or of to in on for with by is are was were be been this that "
    "these those it its as at from into not no yes per via vs we i you they them our one "
    "two all any each same only than then so such when where which who what how why do "
    "does did can could should would will shall may must if else but also more most least "
    "s t re").split())


def tokens(text: str) -> list:
    return [t for t in re.split(r"[^a-z0-9]+", text.lower())
            if len(t) > 2 and t not in _STOP and not t.isdigit()]


def _doc_terms(n: dict) -> dict:
    tf: dict = {}
    for t in tokens(n["title"]):
        tf[t] = tf.get(t, 0) + 3
    for t in tokens(" ".join(map(str, n["tags"]))):
        tf[t] = tf.get(t, 0) + 2
    for t in tokens(n["text"]):
        tf[t] = tf.get(t, 0) + 1
    return tf


def bm25_rank(nodes: dict, query: str, limit: int = 20):
    """Okapi BM25 (k1=1.5, b=0.75) over title x3 / tags x2 / body x1. Deterministic."""
    qtokens = tokens(query)
    if not qtokens:
        return []
    docs, lens, dfs = {}, {}, {}
    for k, n in nodes.items():
        tf = _doc_terms(n)
        docs[k], lens[k] = tf, sum(tf.values())
        for t in tf:
            dfs[t] = dfs.get(t, 0) + 1
    N = max(1, len(docs))
    avg = sum(lens.values()) / N
    k1, b = 1.5, 0.75
    scores = {}
    for k, tf in docs.items():
        s = 0.0
        for t in qtokens:
            if t not in tf:
                continue
            idf = math.log(1 + (N - dfs[t] + 0.5) / (dfs[t] + 0.5))
            s += idf * (tf[t] * (k1 + 1)) / (tf[t] + k1 * (1 - b + b * lens[k] / max(avg, 1e-9)))
        if s > 0:
            scores[k] = s
    return sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]


def snippet(text: str, query: str, width: int = 240) -> str:
    toks = set(tokens(query))
    for m in re.finditer(r"\S+", text):
        if m.group(0).lower().strip(".,;:()\"'`*_#|/-") in toks:
            a = max(0, m.start() - width // 2)
            b = min(len(text), m.start() + width // 2)
            return re.sub(r"\s+", " ", text[a:b]).strip()
    return re.sub(r"\s+", " ", text[:width]).strip()
# --- projections (derived views; labelled PROJECTION — never a conclusion) ----------

def strconv(v) -> str:
    return "" if v in (None, "") else str(v)


def _verdict_group(result) -> str:
    s = str(result or "").strip().upper()
    for p in VERDICT_POSITIVE:
        if s.startswith(p):
            return "positive"
    for p in VERDICT_NEGATIVE:
        if s.startswith(p):
            return "negative"
    for p in VERDICT_NEUTRAL:
        if s.startswith(p):
            return "neutral"
    return "unverdicted"


def belief_rollup(nodes: dict, edges=None) -> list:
    """Per-hypothesis evidence rollup — the Layer-3 'current best belief' input.

    A number of experiments is NOT proof: each one is reported with its id, verdict and
    location so the reader follows the provenance. Everything here is a PROJECTION: it
    points, it never concludes.
    """
    experiments = [n for n in nodes.values() if n["kind"] == "experiment"]
    hyps = [n for n in nodes.values() if n["kind"] == "hypothesis"]
    out = []
    for h in sorted(hyps, key=lambda n: n["id"]):
        hid = h["id"]
        tested, pos, neg = [], [], []
        for e in experiments:
            if e["example"]:
                continue
            linked = hid in set(fm_refs(e["fm"], "hypothesis"))
            if not linked and hid in set(ID_RE.findall(e["text"])):
                linked = True
            if not linked:
                continue
            rec = {
                "id": e["id"], "title": e["title"], "status": e["status"],
                "verdict": _verdict_group(e["fm"].get("result")),
                "result": str(e["fm"].get("result") or "")[:160],
                "rel": e["rel"],
            }
            tested.append(rec)
            if rec["verdict"] == "positive":
                pos.append(rec["id"])
            elif rec["verdict"] == "negative":
                neg.append(rec["id"])
        conf = h["fm"].get("confidence")
        fal = h["fm"].get("falsifier")
        out.append({
            "id": hid, "title": h["title"], "status": h["status"],
            "confidence": conf, "calibration": confidence_label(conf),
            "agents_supporting": sorted(as_list(h["fm"].get("agents_supporting"))),
            "agents_opposing": sorted(as_list(h["fm"].get("agents_opposing"))),
            "experiments_testing": sorted(tested, key=lambda r: r["id"]),
            "experiments_positive": pos, "experiments_negative": neg,
            "n_experiments": len(tested),
            "falsifier": strconv(fal),
            "example": h["example"], "rel": h["rel"],
            "assess": "PROJECTION — follow the linked records; a verdict count is not a fact.",
        })
    return out
# --- CHUNK 4a END ---


def _token_set(text: str) -> set:
    return set(tokens(text))


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# Conservative antonym pairs used only to *surface* candidate contradictions.
_DIR_PAIRS = [("increase", "decrease"), ("faster", "slower"), ("better", "worse"),
              ("wins", "loses"), ("improves", "regresses"), ("higher", "lower"),
              ("non-positive", "positive"), ("copy-make", "make-unmake")]


def contradiction_candidates(nodes: dict, edges=None) -> list:
    """Candidate contradictions (never merged; every entry is a task for an agent)."""
    out = []
    idx = id_index(nodes)
    for n in nodes.values():
        for ref in fm_refs(n["fm"], "contradicts"):
            for dst in idx.get(ref, []):
                out.append({"kind": "declared", "a": n["id"], "b": nodes[dst]["id"],
                            "why": f"front-matter contradicts -> {ref}",
                            "a_rel": n["rel"], "b_rel": nodes[dst]["rel"]})
    recs = [n for n in nodes.values() if n["kind"] in ("hypothesis", "decision", "failure")
            and not n["example"]]
    tag_groups: dict = {}
    for n in recs:
        for t in n["tags"]:
            tag_groups.setdefault(t, []).append(n)
    for tag, group in sorted(tag_groups.items()):
        if len(group) < 2 or len(group) > 60:
            continue
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a, b = group[i], group[j]
                ov = _jaccard(_token_set(a["title"] + " " + a["text"][:2000]),
                              _token_set(b["title"] + " " + b["text"][:2000]))
                if ov < 0.18:
                    continue
                la = (a["title"] + " " + a["text"]).lower()
                lb = (b["title"] + " " + b["text"]).lower()
                hits = sorted({f"{x}/{y}" for x, y in _DIR_PAIRS if (x in la and y in lb) or (y in la and x in lb)})
                if hits:
                    out.append({"kind": "semantic", "a": a["id"], "b": b["id"],
                                "why": f"shared tag '{tag}' (overlap {ov:.2f}) with opposing direction words {hits}",
                                "a_rel": a["rel"], "b_rel": b["rel"]})
    per_hyp: dict = {}
    for e in nodes.values():
        if e["kind"] != "experiment" or e["example"]:
            continue
        vg = _verdict_group(e["fm"].get("result"))
        if vg in ("positive", "negative"):
            for hid in fm_refs(e["fm"], "hypothesis"):
                per_hyp.setdefault(hid, []).append((e, vg))
    for hid, lst in sorted(per_hyp.items()):
        if len({g for _, g in lst}) > 1:
            out.append({"kind": "experiment-conflict", "a": hid, "b": hid,
                        "why": "experiments testing " + hid + " have opposing verdicts: "
                               + ", ".join(f"{e['id']}={g}" for e, g in lst),
                        "a_rel": "", "b_rel": ""})
    return sorted(out, key=lambda x: (x["a"], x["b"], x["why"]))


def duplicate_candidates(nodes: dict, threshold: float = 0.55) -> list:
    """Pairs of records that look like the same idea. CANDIDATES only — never merged."""
    recs = [n for n in nodes.values() if n["kind"] in ("hypothesis", "question", "failure", "decision")]
    sigs = [(n, _token_set(n["title"] + " " + " ".join(map(str, n["tags"])))) for n in recs]
    out = []
    for i in range(len(sigs)):
        for j in range(i + 1, len(sigs)):
            a, sa = sigs[i]
            b, sb = sigs[j]
            ov = _jaccard(sa, sb)
            if ov >= threshold:
                out.append({"a": a["id"], "b": b["id"], "score": round(ov, 3),
                            "kinds": [a["kind"], b["kind"]],
                            "a_rel": a["rel"], "b_rel": b["rel"]})
    return sorted(out, key=lambda x: (-x["score"], x["a"], x["b"]))

def questions_view(nodes: dict) -> list:
    qs = [n for n in nodes.values() if n["kind"] == "question"]
    out = []
    for q in sorted(qs, key=lambda n: n["id"]):
        out.append({
            "id": q["id"], "title": q["title"], "status": q["status"],
            "priority": q["fm"].get("priority") or "medium",
            "created": q["created"], "rel": q["rel"],
            "depends_on": as_list(q["fm"].get("depends_on")),
            "blocked_by": as_list(q["fm"].get("blocked_by")),
            "related_hypotheses": as_list(q["fm"].get("hypotheses")),
            "related_experiments": as_list(q["fm"].get("experiments")),
            "suggested_experiments": as_list(q["fm"].get("suggested_experiments")),
        })
    return out


def revival_candidates(nodes: dict) -> list:
    """Rejected / abandoned / inconclusive / superseded records with a revisit condition —
    and those without one (so an agent can write one)."""
    out = []
    for n in nodes.values():
        if n["kind"] not in ("failure", "hypothesis", "experiment", "question", "decision"):
            continue
        dead = (n["status"] in ("REJECTED", "ABANDONED", "INCONCLUSIVE", "SUPERSEDED", "CANCELLED")
                or _verdict_group(n["fm"].get("result")) in ("negative", "neutral"))
        if not dead or n["example"]:
            continue
        out.append({
            "id": n["id"], "kind": n["kind"], "title": n["title"], "status": n["status"],
            "created": n["created"],
            "revisit_when": strconv(n["fm"].get("revisit_when") or n["fm"].get("reopen_when")),
            "why_it_died": (strconv(n["fm"].get("result")) or strconv(n["fm"].get("status_reason")))[:200],
            "rel": n["rel"],
            "note": "CANDIDATE: a newer architecture, hardware, or design may change the answer.",
        })
    return sorted(out, key=lambda x: (x["kind"], x["id"]))


def timeline(nodes: dict) -> list:
    rows = []
    for n in nodes.values():
        when = n["closed"] or n["created"] or "9999-99-99"
        rows.append({"when": when, "id": n["id"], "kind": n["kind"],
                     "status": n["status"], "title": n["title"], "rel": n["rel"],
                     "example": n["example"]})
    return sorted(rows, key=lambda r: (r["when"], r["kind"], r["id"]))
# --- audit (memory integrity + observability) --------------------------------------

def evidence_inventory(nodes: dict) -> list:
    out = []
    for n in nodes.values():
        if n["kind"] != "evidence":
            continue
        path = n["fm"].get("path") or n["fm"].get("file")
        exists, sha = False, None
        if path:
            pp = Path(str(path))
            pp = pp if pp.is_absolute() else (REPO_ROOT / str(path))
            exists = pp.exists()
            if exists:
                sha = sha256_file(pp)
        out.append({
            "id": n["id"], "title": n["title"], "status": n["status"],
            "path": str(path) if path else None, "exists": exists, "sha256": sha,
            "sha256_recorded": n["fm"].get("sha256"),
            "kind": n["fm"].get("kind") or n["fm"].get("evidence_kind"),
            "regenerate": n["fm"].get("regenerate"),
            "cites": as_list(n["fm"].get("cites")), "rel": n["rel"],
        })
    return sorted(out, key=lambda x: x["id"])


def audit(nodes: dict, code: dict) -> dict:
    """The memory system's self-check. Every entry points at a record; nothing is corrected
    silently. `problems` should block closing a round; `warnings` and `findings` are advisory."""
    idx = id_index(nodes)
    edges, _ = build_graph(nodes, code)
    problems, warnings, findings = [], [], []

    for m in missing_reference_targets(nodes):
        findings.append({"severity": "warning", "area": "provenance",
                          "msg": f"dangling id {m['id']} referenced by {m['referenced_by'][:4]}"})

    for n in nodes.values():
        vocab = STATUS_VOCAB.get(n["kind"])
        if vocab and n["status"] not in vocab:
            problems.append({"area": "status", "rel": n["rel"],
                             "msg": f"status={n['status']!r} not in the {n['kind']} vocabulary"})

    for n in nodes.values():
        if n["kind"] == "experiment" and n["status"] == "COMPLETED" and not n["example"]:
            if "## Provenance" not in n["text"]:
                warnings.append({"area": "experiment", "rel": n["rel"],
                                 "msg": "COMPLETED without a '## Provenance' section (legacy grandfathered)"})
            if str(n["fm"].get("result") or "").strip() == "":
                warnings.append({"area": "experiment", "rel": n["rel"],
                                 "msg": "COMPLETED but result empty"})

    for n in nodes.values():
        if n["kind"] == "hypothesis" and n["status"] in ("SUPPORTED",) and not n["example"]:
            if not [e for e in nodes.values() if e["kind"] == "experiment"
                    and n["id"] in fm_refs(e["fm"], "hypothesis")]:
                findings.append({"severity": "warning", "area": "epistemics", "rel": n["rel"],
                                 "msg": f"{n['id']} SUPPORTED but no experiment tests it"})

    for rid, keys in sorted(idx.items()):
        if len(keys) > 1:
            findings.append({"severity": "warning", "area": "ids",
                             "msg": f"id {rid} is ambiguous ({len(keys)} nodes): " + ", ".join(keys)})

    for ev in evidence_inventory(nodes):
        if ev["path"] and not ev["exists"]:
            findings.append({"severity": "warning", "area": "evidence", "rel": ev["rel"],
                             "msg": f"evidence path missing: {ev['path']}"})
        if ev["exists"] and ev["sha256_recorded"] and \
                ev["sha256"].lower() != str(ev["sha256_recorded"]).lower():
            problems.append({"area": "evidence", "rel": ev["rel"],
                             "msg": f"sha256 drift on {ev['path']}: recorded "
                                    f"{str(ev['sha256_recorded'])[:12]}… vs on-disk {ev['sha256'][:12]}…"})

    by_kind: dict = {}
    for n in nodes.values():
        by_kind[n["kind"]] = by_kind.get(n["kind"], 0) + 1
    by_status: dict = {}
    for n in nodes.values():
        if n["kind"] in STATUS_VOCAB:
            by_status[n["status"]] = by_status.get(n["status"], 0) + 1
    metric = {
        "records_total": len(nodes), "code_files": len(code), "edges_total": len(edges),
        "by_kind": by_kind, "by_status": by_status,
        "contradiction_candidates": len(contradiction_candidates(nodes)),
        "duplicate_candidates": len(duplicate_candidates(nodes)),
        "open_questions": sum(1 for q in questions_view(nodes)
                              if q["status"] in ("OPEN", "INVESTIGATING", "BLOCKED")),
        "revival_candidates": len(revival_candidates(nodes)),
        "dangling_ids": len(missing_reference_targets(nodes)),
        "legacy_experiments_without_pre_registration": sum(
            1 for n in nodes.values()
            if n["kind"] == "experiment" and n["status"] in ("COMPLETED", "RUNNING")
            and "## Pre-Registered Decision Rule" not in n["text"]),
    }
    return {"generated": now_iso(), "schema_version": SCHEMA_VERSION,
            "problems": problems, "warnings": warnings, "findings": findings,
            "metrics": metric}
# --- CHUNK 5a END ---


def codemap(nodes: dict, code: dict) -> list:
    """record -> code files -> commits mentioned (the provenance chain for an idea)."""
    edges, _ = build_graph(nodes, code)
    by_src: dict = {}
    for e in edges:
        if e["kind"] == "touches-code":
            by_src.setdefault(e["src"], {}).setdefault(e["dst"], set()).update(e["why"])
    commits: dict = {}
    for n in nodes.values():
        for c in commit_refs(n["text"]):
            commits.setdefault(c[:7], []).append(n["id"])
    out = []
    for src_rel, codes in sorted(by_src.items()):
        out.append({
            "record": nodes[src_rel]["id"], "title": nodes[src_rel]["title"],
            "kind": nodes[src_rel]["kind"], "status": nodes[src_rel]["status"],
            "code_files": sorted(codes),
            "commits_mentioned": sorted(c for c, ids in commits.items()
                                        if nodes[src_rel]["id"] in ids),
            "rel": nodes[src_rel]["rel"],
        })
    return out


def search(nodes: dict, query: str, limit: int = 8, expand: bool = True, edges=None) -> dict:
    """Ranked retrieval with optional graph expansion. Hits carry provenance; the
    `related` list is the 1-hop neighbourhood of the best hits ("read these too")."""
    graph_edges = edges if edges is not None else build_graph(nodes)[0]
    hits = [{"id": nodes[k]["id"], "kind": nodes[k]["kind"], "title": nodes[k]["title"],
             "status": nodes[k]["status"], "score": round(s, 4), "rel": nodes[k]["rel"],
             "snippet": snippet(nodes[k]["text"], query),
             "example": nodes[k]["example"]}
            for k, s in bm25_rank(nodes, query, limit=limit)]
    expanded = {}
    if expand:
        for h in hits[:5]:
            for nbr, (d, kind) in neighbours(graph_edges, h["rel"], depth=1).items():
                if nbr in nodes and nbr not in {x["rel"] for x in hits}:
                    expanded[nbr] = nodes[nbr]
    related = [{"id": n["id"], "kind": n["kind"], "title": n["title"], "rel": n["rel"],
                "status": n["status"]} for _, n in sorted(expanded.items())]
    return {"query": query, "hits": hits, "related": related}
# --- CHUNK 5b END ---


def build_state(nodes: dict, code: dict) -> dict:
    """Assemble the machine-readable Layer-3 'research state' (state.json)."""
    edges, _ = build_graph(nodes, code)
    questions = questions_view(nodes)
    return {
        "generated": now_iso(), "schema_version": SCHEMA_VERSION,
        "beliefs": belief_rollup(nodes, edges),
        "questions_open": [q for q in questions if q["status"] in ("OPEN", "INVESTIGATING", "BLOCKED")],
        "questions_all": questions,
        "debates_open": [
            {"id": n["id"], "title": n["title"], "status": n["status"], "rel": n["rel"],
             "participants": as_list(n["fm"].get("participants"))}
            for n in sorted(nodes.values(), key=lambda x: x["id"])
            if n["kind"] == "debate" and n["status"] in ("OPEN", "ROUTED")],
        "failures": [
            {"id": n["id"], "title": n["title"], "rel": n["rel"],
             "lesson": strconv(n["fm"].get("lesson") or n["fm"].get("lessons"))}
            for n in sorted(nodes.values(), key=lambda x: x["id"]) if n["kind"] == "failure"],
        "revivals": revival_candidates(nodes),
        "contradiction_candidates": contradiction_candidates(nodes, edges),
        "duplicate_candidates": duplicate_candidates(nodes),
        "evidence": evidence_inventory(nodes),
        "codemap": codemap(nodes, code),
        "timeline_tail": [r for r in timeline(nodes) if r["when"] != "9999-99-99"][-40:],
        "metrics": audit(nodes, code)["metrics"],
        "facts": {
            "perft_anchor_host": "research/project_state.md ## Certified Perft Anchors (SACRED)",
            "note": "GENERATED file. Facts of record are project_state.md + the records it links.",
        },
    }
# --- CHUNK 6 END ---


def render_state_md(state: dict) -> str:
    L = ["# Research State (GENERATED — do not edit)", "",
         "Derived from the record store by `research.py state`. Regenerate after every change.",
         f"Generated: {state['generated']}; schema {state['schema_version']}.",
         "Every entry is a PROJECTION of the linked records — follow them before believing.", ""]
    L.append("## Current best beliefs (hypotheses with measured weight)")
    L.append("")
    for b in state["beliefs"]:
        if b["example"] or not b["experiments_testing"]:
            continue
        L.append(f"- **{b['id']}** {b['title']} — status {b['status']}; "
                 f"confidence {b['confidence']} ({b['calibration']}); tested by "
                 + ", ".join(f"{e['id']} [{e['verdict']}]" for e in b["experiments_testing"])
                 + f". ({b['rel']})")
    L.append("")
    L.append("## Open questions")
    for q in state["questions_open"]:
        L.append(f"- **{q['id']}** [{q['status']}, {q['priority']}] {q['title']} ({q['rel']})")
    L.append("")
    L.append("## Open debates")
    for d in state["debates_open"]:
        L.append(f"- **{d['id']}** {d['title']} — {d['status']} ({d['rel']})")
    L.append("")
    L.append("## Contradiction candidates (resolve, don't merge)")
    for c in state["contradiction_candidates"]:
        L.append(f"- `{c['kind']}` {c['a']} vs {c['b']} — {c['why']}")
    L.append("")
    L.append("## Revival candidates (revisit when conditions change)")
    for r in state["revivals"][:20]:
        L.append(f"- {r['kind']} **{r['id']}** {r['title']} — {r['status']}."
                 + (f" Revisit when: {r['revisit_when']}" if r["revisit_when"]
                    else " No revisit condition recorded."))
    L.append("")
    L.append("## Recent timeline")
    for r in state["timeline_tail"][-15:]:
        L.append(f"- {r['when']} {r['kind']} {r['id']} ({r['status']}) : {r['title']}")
    L.append("")
    L.append("## Metrics")
    L.append("```")
    L.append(json_dump(state["metrics"]))
    L.append("```")
    L.append("")
    return "\n".join(L) + "\n"


def run_derived(cmd: str, argv: list) -> int:
    """Shared dispatcher for the derived-intelligence commands (research.py and
    kgraph.py both call this so the two front-ends can never drift)."""
    import argparse
    nodes = load_nodes()
    code = code_nodes()
    edges, _ = build_graph(nodes, code)
    p = argparse.ArgumentParser(prog=f"kgraph {cmd}" if '/' in cmd else f"research {cmd}")
    p.add_argument("args", nargs=argparse.REMAINDER)
    p.add_argument("--json", action="store_true")
    p.add_argument("--limit", "-n", type=int, default=8)
    p.add_argument("--depth", "-d", type=int, default=1)
    p.add_argument("--all", action="store_true")
    p.add_argument("--write", action="store_true",
                   help="(state) write research/state.json + research/state.md")
    a = p.parse_args(argv)
    out = None
    if cmd == "search":
        q = " ".join(a.args).strip()
        out = search(nodes, q, limit=a.limit, edges=edges)
    elif cmd == "graph":
        rid = " ".join(a.args).strip()
        idx = id_index(nodes)
        keys = idx.get(rid) or ([rid] if rid in nodes else list(code and ([rid] if rid in code else [])))
        out = {"query": rid,
               "nodes": [{"id": nodes[k]["id"], "rel": k, "kind": nodes[k]["kind"]}
                         for k in keys if k in nodes]}
        for k in keys:
            if k not in nodes:
                continue
            inc, outg = edges_of(edges, k)
            out[k] = {"id": nodes[k]["id"], "title": nodes[k]["title"],
                      "incoming": [[knd, s, w] for knd, s, w in inc],
                      "outgoing": [[knd, d, w] for knd, d, w in outg]}
    elif cmd == "beliefs":
        out = belief_rollup(nodes, edges)
    elif cmd == "contradictions":
        out = contradiction_candidates(nodes, edges)
    elif cmd == "duplicates":
        out = duplicate_candidates(nodes)
    elif cmd == "questions":
        out = questions_view(nodes)
    elif cmd == "revivals":
        out = revival_candidates(nodes)
    elif cmd == "timeline":
        out = timeline(nodes) if a.all else [r for r in timeline(nodes) if r["when"] != "9999-99-99"][-25:]
    elif cmd == "codemap":
        out = codemap(nodes, code)
    elif cmd == "audit":
        out = audit(nodes, code)
    elif cmd == "evidence":
        out = evidence_inventory(nodes)
    elif cmd == "state":
        state = build_state(nodes, code)
        if a.write:
            (RESEARCH_DIR / "state.json").write_text(json_dump(state), encoding="utf-8", newline="\n")
            (RESEARCH_DIR / "state.md").write_text(render_state_md(state), encoding="utf-8", newline="\n")
            print(f"wrote {RESEARCH_DIR / 'state.json'} and {RESEARCH_DIR / 'state.md'}")
            return 0
        out = state
    else:
        out = {"error": f"unknown command {cmd}"}
    print(json_dump(out))
    return 0
# --- CHUNK 7 END ---

_DERIVED_COMMANDS = {"search", "graph", "beliefs", "contradictions", "duplicates",
                     "questions", "revivals", "timeline", "codemap", "audit",
                     "evidence", "state"}


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] not in _DERIVED_COMMANDS:
        print("Kanamecide derived-intelligence layer (DEC-0011).")
        print("usage: research.py <" + " | ".join(sorted(_DERIVED_COMMANDS)) + "> [args] [--json]")
        print("  or: python research/scripts/kgraph.py <same>")
        return 0
    cmd = argv[0]
    return run_derived(cmd, argv[1:])


if __name__ == "__main__":
    sys.exit(main())
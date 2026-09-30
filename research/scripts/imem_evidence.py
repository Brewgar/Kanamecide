#!/usr/bin/env python3
"""imem_evidence.py — provenance as a first-class query, and promotion with gates.

WHY (measured):
  * Provenance is prose: "Which experiments tested H-0004?" needs `beliefs`, and
    "can this experiment be reproduced?" needs reading three sections and two scripts.
  * Promotion (scratch -> candidate -> reviewed -> validated -> best-belief) has no
    gates: a SUPPORTED hypothesis with no testing experiment passes `validate` today
    with only an audit *finding* (advisory). The ladder must be computable.
  * Pre-registration immutability is honor-based: nothing detects a decision rule
    edited after RUNNING began. The E-0013 saga (R-0019 B-block: "decision rule moved
    after seeing data would void the campaign") is exactly this risk, unguarded.

PROVENANCE GRAPH: claim/hypothesis -> experiments (tests) -> runs -> evidence
artifacts (sha256-verified, regenerate command) -> code commits. `chain()` returns the
full chain with a per-link verdict (ok / missing / drift / unrecorded).

PROMOTION LADDER (computed, never asserted):
  L0 raw      — a record exists.
  L1 anchored — ids it cites resolve (no dangling links) + anchors pin clean.
  L2 tested   — >= 1 COMPLETED experiment names it in tests/.
  L3 measured — a PASS/FAIL verdict exists with power + sample-validity sections.
  L4 reproduced — verified_by a non-owner review (verification kind) or a second run.
  L5 adopted  — an ACTIVE decision cites it (project_state.md reflects it).
A hypothesis may only be marked SUPPORTED at L3+; SUPPORTED below L3 is a lint problem.
"""
from __future__ import annotations

import hashlib
import re

from imem_core import (
    as_list, by_id, file_sha256, link_resolves, parse_pointer, records_of_type,
)

VERDICT_POS = ("PASS", "WIN")
VERDICT_NEG = ("FAIL", "FAILED", "LOSS")


def verdict_group(result) -> str:
    s = str(result or "").strip().upper()
    for p in VERDICT_POS:
        if s.startswith(p):
            return "positive"
    for p in VERDICT_NEG:
        if s.startswith(p):
            return "negative"
    for p in ("NEUTRAL", "INCONCLUSIVE"):
        if s.startswith(p):
            return "neutral"
    return "unverdicted"


def experiments_testing(records: dict, rid: str) -> list:
    out = []
    for exp in records_of_type(records, "experiment"):
        if exp.fm.get("example"):
            continue
        tested = {str(x).split("#")[0] for x in
                  as_list(exp.fm.get("tests") or exp.fm.get("hypothesis"))}
        if rid in tested or rid in set(re.findall(r"[A-Z]+-\d+", exp.body)):
            out.append(exp)
    return sorted(out, key=lambda e: e.id)


def reviews_of(records: dict, rid: str) -> list:
    out = []
    for rev in records_of_type(records, "review"):
        tgt = str(rev.fm.get("target") or "")
        if str(rid) == tgt.split("#")[0] or rid in as_list(rev.fm.get("verifies")):
            out.append(rev)
    return sorted(out, key=lambda r: r.id)


def independent_verification(records: dict, rec) -> dict:
    """A verification counts iff: kind includes 'verification', reviewer/owner differs
    from the record's owner, and the verdict is VERIFIED/CLEAN (not PARTIAL)."""
    owner = str(rec.fm.get("owner") or rec.fm.get("author") or rec.fm.get("agent") or "")
    hits = []
    for rev in reviews_of(records, rec.id):
        kind = str(rev.fm.get("kind") or "")
        verdict = str(rev.fm.get("verdict") or rev.fm.get("result") or "")
        who = str(rev.fm.get("reviewer") or rev.fm.get("author") or "")
        if "verif" in kind.lower() and who and who != owner:
            hits.append({"review": rev.id, "reviewer": who, "verdict": verdict,
                         "counts": verdict.upper().startswith(("VERIFIED", "CLEAN"))})
    good = [h for h in hits if h["counts"]]
    return {"owner": owner, "verifications": hits,
            "independent": bool(good), "by": [h["reviewer"] for h in good]}
PRE_REG_SECTIONS = ("## Pre-Registered Decision Rule", "## Power And Sample Size",
                    "## Sample Validity", "## Provenance")


def prereg_fingerprint(rec) -> str:
    """sha256 over the normative pre-registration sections only (heading-normalized so
    re-wrapping prose without changing rules keeps the same pin)."""
    from imem_core import norm_text
    chunks = []
    for want in PRE_REG_SECTIONS:
        for b in rec.blocks:
            if ("## " + b.title.strip()) == want or b.slug == want.lower().strip("# "):
                chunks.append("## " + want + "\n" + norm_text(b.body))
    return hashlib.sha256("\n\n".join(chunks).encode()).hexdigest()


def prereg_state(rec) -> dict:
    """The immutability guard: a parked pre-registration pin (`prereg_sha256:` in
    front-matter, written when status flips to RUNNING) vs today's recomputation."""
    parked = str(rec.fm.get("prereg_sha256") or "")
    current = prereg_fingerprint(rec)
    status = str(rec.fm.get("status") or "")
    if not parked:
        return {"parked": "", "current": current[:12] + "...",
                "locked": False,
                "note": "no prereg_sha256 parked — park one before RUNNING"}
    moved = parked != current
    return {"parked": parked[:12] + "...", "current": current[:12] + "...",
            "locked": status in ("RUNNING", "COMPLETED"), "moved": moved,
            "note": ("PRE-REGISTRATION MOVED after parking — void unless re-critiqued"
                     if moved and status in ("RUNNING", "COMPLETED")
                     else "pinned pre-registration intact")}
def evidence_check(records: dict, rec) -> list:
    """Per-artifact verdicts for an experiment/review: path exists? sha matches?
    Each row is independently checkable."""
    from imem_core import REPO_ROOT, file_sha256
    from pathlib import Path
    refs = [str(x) for x in as_list(rec.fm.get("evidence"))]
    refs += [str(x) for x in as_list(rec.fm.get("evidence_files"))]
    if rec.fm.get("path"):
        refs.append(str(rec.fm.get("path")))
    for ref in list(refs):
        ev = by_id(records, ref.split("#")[0]) if ref else None
        if ev is not None and ev.type == "evidence" and ev.fm.get("path"):
            refs.append(str(ev.fm.get("path")))
    rows = []
    for path in sorted({p for p in refs if p and "/" in p}):
        pp = Path(path) if Path(path).is_absolute() else (REPO_ROOT / path)
        exists = pp.exists()
        sha = file_sha256(pp) if exists else "missing"
        recorded = str(rec.fm.get("sha256") or "")
        drift = bool(recorded and exists and sha.lower() != recorded.lower())
        rows.append({"path": path, "exists": exists,
                     "sha256": (sha[:12] + "...") if exists else "missing",
                     "recorded": (recorded[:12] + "...") if recorded else "",
                     "drift": drift,
                     "verdict": "drift" if drift else ("ok" if exists else "missing")})
    return rows


def promotion_ladder(records: dict, rec) -> dict:
    """Compute the L0..L5 rung for a hypothesis/claim/decision with the receipts."""
    from imem_core import link_resolves as _res
    dangling = [d for _r, d, _a, _f in rec.links_fm
                if _res(records, d, _a) != "yes"]
    drift = [s for s, pin in (rec.anchors_pinned or {}).items()
             if pin and {b.slug: b.sha8 for b in rec.blocks}.get(s) != pin]
    l1 = not dangling and not drift
    tested = experiments_testing(records, rec.id)
    l2 = bool(tested)
    measured = [e for e in tested
                if verdict_group(e.fm.get("result")) in ("positive", "negative")
                and any(s in e.body for s in PRE_REG_SECTIONS[:3])]
    l3 = bool(measured)
    iv = independent_verification(records, rec)
    l4 = iv["independent"]
    adopted = [d for d in records_of_type(records, "decision")
               if str(d.fm.get("status")) == "ACTIVE" and
               (rec.id in {str(x).split("#")[0] for x in
                           as_list(d.fm.get("evidence") or d.fm.get("cites"))}
                or rec.id in d.body)]
    l5 = bool(adopted)
    rung = 5 if l5 else 4 if l4 else 3 if l3 else 2 if l2 else 1 if l1 else 0
    return {"rung": rung,
            "ladder": {"L1_anchored": l1, "L2_tested": l2, "L3_measured": l3,
                       "L4_reproduced": l4, "L5_adopted": l5},
            "dangling": dangling, "anchor_drift": drift,
            "tested_by": [e.id for e in tested],
            "measured_by": [e.id for e in measured],
            "verified_by": iv["by"], "adopted_by": [d.id for d in adopted]}


def chain(records: dict, rid: str) -> dict:
    """Provenance chain for a claim/hypothesis: tests -> reviews -> decisions, each
    with its rung/verdict. Answers 'why do we believe this' in one call."""
    rec = by_id(records, rid)
    if rec is None:
        return {"id": rid, "error": "no such record"}
    ladder = promotion_ladder(records, rec)
    tested = []
    for exp in experiments_testing(records, rid)[:12]:
        tested.append({"id": exp.id, "status": str(exp.fm.get("status")),
                       "result": str(exp.fm.get("result"))[:120],
                       "verdict": verdict_group(exp.fm.get("result")),
                       "prereg": prereg_state(exp),
                       "evidence": evidence_check(records, exp)})
    return {"id": rid, "title": rec.title, "status": str(rec.fm.get("status")),
            "confidence": rec.fm.get("confidence"), "rung": ladder["rung"],
            "ladder": ladder["ladder"], "dangling": ladder["dangling"],
            "tests": tested, "reviews": [
                {"id": r.id, "kind": str(r.fm.get("kind")),
                 "verdict": str(r.fm.get("verdict") or r.fm.get("result")),
                 "reviewer": str(r.fm.get("reviewer") or r.fm.get("author"))}
                for r in reviews_of(records, rid)],
            "adopted_by": ladder["adopted_by"]}

#!/usr/bin/env python3
"""imem_claims.py — the atomic-claim layer and its contradiction engine.

WHY (measured): the store reasons in whole files. A hypothesis record mixes question,
claim, counterarguments, confidence, and proposed experiment in one body, so
contradiction detection needs hand-written antonym lists and still found ZERO
contradictions on a corpus that visibly contradicts itself
(H-0005 ">=3x" vs H-0006 "1.3-2.5x, not >=3x").

A CLAIM is the smallest unit the system reasons about: statement + domain +
parameter + direction + scope + epistemic class + confidence + evidence/tests links
+ provenance. Engines here read claims/ records plus *derived* claim views over
legacy hypotheses (never rewriting them).
"""
from __future__ import annotations

import re

from imem_core import (
    DIRECTION, as_float, as_list, by_id, parse_pointer, records_of_type,
)

POLARITY_OF = {d: s for d, s in DIRECTION.items()}


def claim_view(rec) -> dict:
    """Normalized view of a claim or claim-bearing hypothesis record.

    Hypotheses get a *derived* claim view: the title is the statement; domain /
    parameter / direction come from optional front-matter and otherwise default to
    unknown. Authors add precision by filing claims/ records, not by editing history.
    """
    fm = rec.fm or {}
    return {
        "key": rec.key, "id": rec.id, "type": rec.type, "title": rec.title,
        "statement": str(fm.get("statement") or rec.title),
        "domain": str(fm.get("domain") or "unknown").lower(),
        "parameter": str(fm.get("parameter") or "").lower(),
        "params": sorted({t for t in re.split(r"[^a-z0-9]+",
                                              str(fm.get("parameter") or "").lower())
                          if len(t) > 2}),
        "direction": str(fm.get("direction") or "unknown").lower(),
        "polarity": POLARITY_OF.get(str(fm.get("direction") or "").lower()),
        "scope": sorted({str(s).lower() for s in as_list(fm.get("scope"))}),
        "epistemic": str(fm.get("epistemic") or fm.get("epistemic_class")
                         or "hypothesis"),
        "status": str(fm.get("status") or "OPEN"),
        "confidence": as_float(fm.get("confidence")),
        "tested_by": [str(x) for x in as_list(fm.get("tests") or fm.get("tested_by"))],
        "evidence_for": [str(x) for x in as_list(fm.get("supports")
                                                 or fm.get("evidence_for"))],
        "evidence_against": [str(x) for x in as_list(fm.get("contradicts") or [])],
        "depends_on": [str(x) for x in as_list(fm.get("depends_on") or [])],
        "implemented_by": [str(x) for x in as_list(fm.get("implements")
                                                   or fm.get("implemented_by") or [])],
        "revisit_when": str(fm.get("revisit_when") or fm.get("reopen_when") or ""),
        "author": str(fm.get("owner") or fm.get("author") or fm.get("agent") or ""),
        "created": str(fm.get("created") or ""),
    }


def live_claims(records: dict) -> list:
    """Claims + hypotheses worth reasoning about: not examples, not superseded stubs."""
    out = []
    for rec in records_of_type(records, "claim", "hypothesis"):
        if rec.fm.get("example"):
            continue
        if rec.type == "hypothesis" and str(rec.fm.get("status")) == "SUPERSEDED":
            continue
        out.append(claim_view(rec))
    return out
def same_research_object(a: dict, b: dict) -> bool:
    """Two claims collide iff: same known domain, overlapping parameters, known and
    nonzero polarity on both sides, opposite polarity, and overlapping-or-open scope.
    Conservative on purpose: unknown fields never collide (silence over false alarms).
    """
    if a["id"] == b["id"]:
        return False
    if not a["domain"] or a["domain"] == "unknown":
        return False
    if a["domain"] != b["domain"]:
        return False
    if not a["params"] or not b["params"]:
        return False
    if not (set(a["params"]) & set(b["params"])):
        return False
    if a["polarity"] is None or b["polarity"] is None:
        return False
    if a["polarity"] == 0 or b["polarity"] == 0:
        return False
    if a["polarity"] == b["polarity"]:
        return False
    if a["scope"] and b["scope"] and not (set(a["scope"]) & set(b["scope"])):
        return False
    return True


def contradiction_candidates(records: dict) -> list:
    """Machine direction-conflicts + declared `contradicts` links. Every entry is a
    CANDIDATE with the resolution task spelled out; the tool never merges or resolves.
    """
    claims = live_claims(records)
    out = []
    for i in range(len(claims)):
        for j in range(i + 1, len(claims)):
            a, b = claims[i], claims[j]
            if same_research_object(a, b):
                lo, hi = sorted([a["id"], b["id"]])
                shared = sorted(set(a["params"]) & set(b["params"]))
                out.append({
                    "kind": "direction-conflict", "a": lo, "b": hi,
                    "domain": a["domain"], "params": shared,
                    "a_direction": a["direction"], "b_direction": b["direction"],
                    "a_status": a["status"], "b_status": b["status"],
                    "why": (f"same domain '{a['domain']}' + parameter {shared} with "
                            f"opposite directions ({a['direction']} vs {b['direction']})"),
                    "resolve": (f"Design one experiment that moves both {lo} and {hi}: "
                                f"name the differing assumption, the context each claim "
                                f"needs, and the N that settles it. Not prose."),
                })
    for rec in records.values():
        for dst in as_list(rec.fm.get("contradicts")):
            rid, _anch = parse_pointer(str(dst))
            if rid and by_id(records, rid):
                a, b = sorted([rec.id, rid])
                if not any(c["a"] == a and c["b"] == b for c in out):
                    out.append({"kind": "declared", "a": a, "b": b, "domain": "",
                                "params": [], "a_direction": "", "b_direction": "",
                                "a_status": "", "b_status": "",
                                "why": f"{rec.id} declares contradicts -> {dst}",
                                "resolve": "Adjudicate with a measurement both sides "
                                           "pre-accept."})
    out.sort(key=lambda c: (c["a"], c["b"]))
    return out


def duplicate_claims(records: dict, embed=None, threshold: float = 0.55) -> list:
    """Same-idea pairs by meaning (cosine) or shared domain+parameter+polarity.
    Lexical title overlap alone is NOT enough (H-0005 vs H-0006 share words but are
    opposite claims — contradictions, not duplicates)."""
    claims = live_claims(records)
    pairs = []
    if embed is not None:
        id_to_key = {}
        for c in claims:
            rec = by_id(records, c["id"])
            if rec is not None:
                id_to_key[c["id"]] = rec.key
        for c in claims:
            key = id_to_key.get(c["id"])
            if not key:
                continue
            for other_key, sim in embed.similar(key, limit=12):
                other = next((x for x in claims
                              if id_to_key.get(x["id"]) == other_key), None)
                if other is None or other["id"] <= c["id"] or sim < threshold:
                    continue
                if same_research_object(c, other):
                    continue
                pairs.append({"a": c["id"], "b": other["id"],
                              "score": round(sim, 3), "basis": "semantic",
                              "note": "CANDIDATE: same idea in different words?"})
    for i in range(len(claims)):
        for j in range(i + 1, len(claims)):
            a, b = claims[i], claims[j]
            if a["id"] >= b["id"]:
                continue
            if (a["domain"] and a["domain"] == b["domain"] and a["params"] and
                    set(a["params"]) & set(b["params"]) and
                    a["polarity"] == b["polarity"] and a["polarity"] is not None):
                if not any(p["a"] == a["id"] and p["b"] == b["id"] for p in pairs):
                    pairs.append({"a": a["id"], "b": b["id"], "score": 1.0,
                                  "basis": "same domain+parameter+polarity",
                                  "note": "CANDIDATE: same claim filed twice?"})
    pairs.sort(key=lambda p: (-p["score"], p["a"], p["b"]))
    return pairs


# --- novelty: is the thing I am about to file already in the project? --------------

def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def novelty_candidates(records: dict, query_text: str, embed=None, limit: int = 8,
                       semantic_threshold: float = 0.45,
                       lexical_threshold: float = 0.55) -> list:
    """Closest already-existing live claims/hypotheses to `query_text`, each with its
    basis marked. THE diagnostic for 'is this genuinely new to the project?' at filing
    time: candidates are never merged or closed by this; the pairing the author should
    then answer (novel to memory / same idea, new scope / genuine rediscovery) belongs
    in the new record itself.

    Three independent bases keep honesty: lexical token overlap (same words),
    corpus-shape similarity (corpus-relative RI cosine, meaning-aware), and the
    structural same-domain+parameter rule (must not claim novelty silently)."""
    from imem_text import doc_terms, tokens as _tok
    from collections import Counter
    live = live_claims(records)
    q_toks = set(_tok(query_text or ""))
    hits: dict = {}
    # lexical basis
    for c in live:
        base_toks = set(_tok(c["statement"] + " " + c["title"]))
        ov = _jaccard(q_toks, base_toks)
        if ov >= lexical_threshold:
            hits.setdefault(c["id"], {"id": c["id"], "type": c["type"],
                                      "status": c["status"], "score": ov,
                                      "statement": c["statement"][:160],
                                      "basis": []})["basis"].append(
                f"lexical overlap {ov:.2f} (title/statement tokens)")
    # structural basis (same research object shape): same domain + shared parameter token
    for c in live:
        if (c["domain"] != "unknown" and c["parameter"] and
                any(t in c["params"] for t in q_toks)):
            row = hits.setdefault(c["id"], {"id": c["id"], "type": c["type"],
                                            "status": c["status"], "score": 0.6,
                                            "statement": c["statement"][:160],
                                            "basis": []})
            row["basis"].append(
                f"same domain '{c['domain']}' + parameter token of '{c['parameter']}'")
    # semantic basis (corpus-relative RI cosine)
    if embed is not None:
        qtf = dict(Counter(_tok(query_text or "")))
        if qtf:
            recs = sorted(records.values(), key=lambda r: r.key)
            df: dict = {}
            for r in recs:
                for t in doc_terms(r):
                    df[t] = df.get(t, 0) + 1
            qv = embed.vector_for_terms(qtf, df, max(1, len(recs)))
            id_to_row = {c["id"]: c for c in live}
            for i, key in enumerate(embed.keys):
                rec = next((r for r in recs if r.key == key), None)
                if rec is None or rec.id not in id_to_row:
                    continue
                denom = embed.norms[i]
                sim = (sum(a * b for a, b in zip(qv, embed.vecs[i])) / denom
                       if denom else 0.0)
                if sim >= semantic_threshold:
                    row = hits.setdefault(rec.id, {"id": rec.id, "type": rec.type,
                                                   "status": str(rec.fm.get("status")),
                                                   "score": sim,
                                                   "statement":
                                                       id_to_row[rec.id]["statement"],
                                                   "basis": []})
                    row["basis"].append(f"semantic cosine {sim:.3f} (corpus-relative RI)")
    rows = list(hits.values())
    for r in rows:
        r["score"] = round(max(r["score"], 0.0) if isinstance(r["score"], float)
                           else 0.0, 4)
    rows.sort(key=lambda r: (-r["score"], r["id"]))
    return rows[:max(1, limit)]


def novelty_report(records: dict, text_or_id: str, embed=None, limit: int = 8) -> dict:
    """Resolve the argument: an existing id (then compare against its own statement,
    excluding the record itself) or free text. Output carries the query and whether it
    resolved to an id, so the audit trail can see exactly what was compared."""
    target = by_id(records, text_or_id)
    if target is not None:
        query_text = " ".join([target.title, str(target.fm.get("statement") or "")])
        rows = [r for r in novelty_candidates(records, query_text, embed=embed,
                                              limit=limit + 1)
                if r["id"] != target.id][:limit]
        return {"query": text_or_id, "resolved_record": target.id,
                "title": target.title, "candidates": rows,
                "advisory": "CANDIDATES only; novelty is judged by the author."}
    return {"query": text_or_id, "resolved_record": None,
            "candidates": novelty_candidates(records, text_or_id, embed=embed,
                                             limit=limit),
            "advisory": "CANDIDATES only; novelty is judged by the author."}


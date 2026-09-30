#!/usr/bin/env python3
"""imem_prior.py — the three forward-looking engines: revivals, priorities, questions.

WHY (measured):
  * `revivals` lists records with a revisit condition but never evaluates it: a "worth
    testing again on schedule" is a memory feat, not a computed notice.
  * "What next?" is a prose list in current_position.md. Two agents can hold different
    next-steps with no way to compare them.
  * Open questions have no readiness state: Q-0002 (PVS/TT/LMR deltas) is blocked on a
    harness that now exists (E-0012 DONE) but nothing says so.

REVIVAL TRIGGERS are a tiny machine predicate language evaluated against a metrics
file (research/_index/metrics.json — the project's own numbers, e.g. perft_nps,
tt_cutoff_share, current_eval_stage). Free-text `revisit_when` stays as the human
rationale; a trigger line makes it checkable:
    trigger: nps_ge 60000000
    trigger: has search.pvs_tt_complete
Supported ops: nps_ge/nps_le (perft NPS), has <key> / not <key> (nested metrics keys),
after <YYYY-MM-DD> (calendar backstop). Unknown ops are warnings, never errors.

PRIORITY is expected value, all inputs shown, weights versioned and editable:
    score = p_success * impact_elo * info_gain * readiness / (cost_hours ** 0.7)
            * novelty * reversibility_bonus
No bare numbers anywhere: every ranked row prints its arithmetic.
"""
from __future__ import annotations

import json
import math
import re

from imem_core import as_float, as_list, by_id, jdump, records_of_type

TRIGGER_RE = re.compile(r"^\s*(nps_ge|nps_le|has|not|after)\s+(.+?)\s*$")
PRIORITY_WEIGHTS_VERSION = 1


def parse_trigger(line: str):
    m = TRIGGER_RE.match(line or "")
    if not m:
        return None
    return (m.group(1), m.group(2).strip())


def metrics_get(metrics: dict, dotted: str):
    cur = metrics
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def eval_trigger(trigger: str, metrics: dict) -> dict:
    """{'met': bool|None, 'why': str}. None = cannot evaluate (missing metric)."""
    parsed = parse_trigger(trigger)
    if parsed is None:
        return {"met": None, "why": f"unparseable trigger: {trigger!r}"}
    op, arg = parsed
    if op == "nps_ge":
        want = as_float(arg)
        have = metrics_get(metrics, "perft_nps")
        if want is None or have is None:
            return {"met": None, "why": f"nps_ge {arg}: perft_nps unknown"}
        return {"met": float(have) >= want, "why": f"perft_nps={have} vs {want}"}
    if op == "nps_le":
        want = as_float(arg)
        have = metrics_get(metrics, "perft_nps")
        if want is None or have is None:
            return {"met": None, "why": f"nps_le {arg}: perft_nps unknown"}
        return {"met": float(have) <= want, "why": f"perft_nps={have} vs {want}"}
    if op == "has":
        return {"met": metrics_get(metrics, arg) not in (None, False, 0, ""),
                "why": f"{arg}={'present' if metrics_get(metrics, arg) else 'absent'}"}
    if op == "not":
        return {"met": metrics_get(metrics, arg) in (None, False, 0, ""),
                "why": f"{arg}={'absent' if metrics_get(metrics, arg) in (None, False, 0, '') else 'present'}"}
    if op == "after":
        from imem_core import today
        return {"met": today() >= arg, "why": f"today vs {arg}"}
    return {"met": None, "why": f"unknown op {op}"}


def revival_rows(records: dict, metrics: dict) -> list:
    """Dead-but-interesting records with their triggers evaluated. `met: True` rows are
    the schedule firing — the machine equivalent of 'deserves another attempt now'."""
    rows = []
    for rec in records_of_type(records, "failure", "hypothesis", "experiment",
                               "question", "decision", "claim"):
        status = str(rec.fm.get("status") or "")
        result = str(rec.fm.get("result") or "")
        dead = (status in ("REJECTED", "ABANDONED", "INCONCLUSIVE", "SUPERSEDED",
                           "CANCELLED") or result.upper().startswith(
                               ("FAIL", "LOSS", "NEUTRAL", "INCONCLUSIVE")) or
                rec.type == "failure")
        if not dead or rec.fm.get("example"):
            continue
        trigger = str(rec.fm.get("trigger") or "")
        ev = eval_trigger(trigger, metrics) if trigger else {"met": None, "why": "no trigger"}
        rows.append({
            "id": rec.id, "type": rec.type, "title": rec.title, "status": status,
            "result": result[:80], "revisit_when": str(rec.fm.get("revisit_when") or
                                                      rec.fm.get("reopen_when") or ""),
            "trigger": trigger, "trigger_state": ev,
            "rel": rec.key, "created": str(rec.fm.get("created") or ""),
        })
    rows.sort(key=lambda r: (0 if r["trigger_state"].get("met") else 1, r["id"]))
    return rows
def priority_inputs(rec, records: dict) -> dict:
    """Everything the score needs, with defaults that punish vagueness openly.

    p_success: explicit `p_success:` or 0.5 * evidence discount (untested=0.35).
    impact: `impact_elo:` else `impact:` high/medium/low mapped 60/20/6 Elo else 10.
    info_gain: `info_gain:` else 1.0; disputed/debate-linked claims get 1.5.
    readiness: 1.0 minus 0.25 per OPEN `blocked_by`/unmet `depends_on`; floor 0.1.
    cost_hours: `cost_hours:` else 8 for experiments, 1 for questions/claims.
    novelty: 1.0; 0.6 if an experiment already tested the same object (dedup).
    reversibility_bonus: 1.2 if `reversible: true` else 1.0 (safe bets get a nudge).
    """
    fm = rec.fm or {}
    tested = bool(fm.get("tests") or fm.get("tested_by") or fm.get("evidence"))
    disputed = str(fm.get("status") or "") in ("DISPUTED", "TESTING", "OPEN")
    p = as_float(fm.get("p_success"))
    if p is None:
        p = 0.35 if not tested else 0.5
    impact = as_float(fm.get("impact_elo"))
    if impact is None:
        impact = {"high": 60.0, "medium": 20.0, "low": 6.0}.get(
            str(fm.get("impact") or "").lower(), 10.0)
    info_gain = as_float(fm.get("info_gain"), 1.5 if disputed else 1.0)
    blocks = [b for b in as_list(fm.get("blocked_by") or fm.get("depends_on"))
              if _still_open(records, b)]
    readiness = max(0.1, 1.0 - 0.25 * len(blocks))
    cost = as_float(fm.get("cost_hours"),
                    8.0 if rec.type == "experiment" else 1.0)
    cost = max(cost, 0.25)
    tested_same = _tested_same_object(rec, records)
    novelty = 0.6 if tested_same else 1.0
    rev = 1.2 if str(fm.get("reversible") or "").lower() in ("true", "yes", "1") else 1.0
    score = p * impact * info_gain * readiness / (cost ** 0.7) * novelty * rev
    return {"p_success": p, "impact_elo": impact, "info_gain": info_gain,
            "readiness": round(readiness, 2), "open_blocks": blocks,
            "cost_hours": cost, "novelty": novelty, "reversibility": rev,
            "tested_same_object": tested_same, "score": round(score, 3)}


def _still_open(records: dict, ref: str) -> bool:
    rid = str(ref).split("#")[0]
    rec = by_id(records, rid)
    if rec is None:
        return True  # dangling dependency blocks until resolved
    return str(rec.fm.get("status") or "OPEN") in (
        "OPEN", "TESTING", "PENDING", "RUNNING", "IN_PROGRESS", "BLOCKED",
        "REQUESTED", "ACCEPTED", "INVESTIGATING", "DRAFT", "IN_REVIEW", "UNTESTED")


def _tested_same_object(rec, records: dict) -> bool:
    """True if a COMPLETED experiment already names this record's id in tests/."""
    for exp in records_of_type(records, "experiment"):
        if str(exp.fm.get("status")) not in ("COMPLETED", "RUNNING"):
            continue
        tested = {str(x).split("#")[0] for x in
                  as_list(exp.fm.get("tests") or exp.fm.get("hypothesis"))}
        if rec.id in tested:
            return True
    return False


def priority_rows(records: dict) -> list:
    """Open research objects ranked by expected value. Arithmetic travels with the row."""
    rows = []
    for rec in records_of_type(records, "hypothesis", "question", "claim", "debate"):
        if rec.fm.get("example"):
            continue
        status = str(rec.fm.get("status") or "")
        if status in ("RESOLVED", "ANSWERED", "SUPPORTED", "REJECTED", "SUPERSEDED",
                      "ABANDONED", "RETIRED"):
            continue
        inp = priority_inputs(rec, records)
        rows.append({"id": rec.id, "type": rec.type, "title": rec.title,
                     "status": status, "rel": rec.key,
                     "inputs": inp, "score": inp["score"]})
    rows.sort(key=lambda r: (-r["score"], r["id"]))
    return rows


def question_readiness(records: dict) -> list:
    """Each open question with: what blocks it, what recently unblocked, suggested next
    experiment. This is the machine answer to 'which unanswered questions remain, and
    what should we investigate next'."""
    rows = []
    for rec in records_of_type(records, "question"):
        status = str(rec.fm.get("status") or "")
        deps = [str(x) for x in as_list(rec.fm.get("depends_on"))]
        blocked = [str(x) for x in as_list(rec.fm.get("blocked_by"))]
        open_deps = [d for d in deps + blocked if _still_open(records, d)]
        rows.append({
            "id": rec.id, "title": rec.title, "status": status,
            "priority": str(rec.fm.get("priority") or "medium"), "rel": rec.key,
            "depends_on": deps, "blocked_by": blocked, "open_blocks": open_deps,
            "ready": not open_deps,
            "related_hypotheses": [str(x) for x in as_list(rec.fm.get("hypotheses"))],
            "suggested_experiments": [str(x) for x in
                                      as_list(rec.fm.get("suggested_experiments"))],
        })
    order = {"high": 0, "medium": 1, "low": 2}
    rows.sort(key=lambda r: (0 if r["ready"] else 1, order.get(r["priority"], 1), r["id"]))
    return rows

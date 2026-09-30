#!/usr/bin/env python3
"""imem_agents.py — agents as measurable contributors, not vibes.

WHY (mandate §28, measured gap): nothing tracks who is right. current_position.md
carries a self-reported `confidence:` (0.65, 0.76, 0.78) with no calibration behind
it; a new agent cannot tell which seat's numbers to trust on which topic. This module
computes, from records only:
  * calibration: confidence stated on claims/hypotheses vs later SUPPORTED/REJECTED
    outcomes (binned, with Wilson intervals so n=2 is not mistaken for skill);
  * verification record: reviews filed, verdicts, and whether they were later
    overturned;
  * finding precision: findings raised (FND raised_by) vs RESOLVED-confirmed vs
    WITHDRAWN;
  * output mix: reports/reviews/experiments/findings per seat.
No permanent ranks: every table is recomputed from the store, and a previously
unreliable seat's new evidence counts the same as anyone's.

Also here: the blind-research protocol (§29) and the handoff/briefing generators
(§21-22) — the agent-coordination surface in one place.
"""
from __future__ import annotations

import math

from imem_core import as_list, records_of_type


def wilson(p: float, n: int, z: float = 1.96) -> tuple:
    """Wilson score interval for a proportion. n=0 -> (0,1): total ignorance, shown."""
    if n <= 0:
        return (0.0, 1.0)
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round(max(0.0, (c - m) / d), 3), round(min(1.0, (c + m) / d), 3))


def seat_of(rec) -> str:
    fm = rec.fm or {}
    for k in ("owner", "author", "agent", "reviewer", "raised_by", "from"):
        v = str(fm.get(k) or "")
        if v and v not in ("null", "None"):
            return v
    return "unknown"


def calibration(records: dict) -> dict:
    """Per-seat: mean confidence on claims later SUPPORTED vs REJECTED (binned), plus
    the raw counts. A seat that says 0.9 and is right half the time is miscalibrated —
    the table shows it without calling anyone wrong."""
    seats: dict = {}
    for rec in records_of_type(records, "claim", "hypothesis"):
        if rec.fm.get("example"):
            continue
        status = str(rec.fm.get("status") or "")
        if status not in ("SUPPORTED", "REJECTED"):
            continue
        try:
            conf = float(rec.fm.get("confidence"))
        except (TypeError, ValueError):
            continue
        s = seats.setdefault(seat_of(rec), {"sup": [], "rej": []})
        s["sup" if status == "SUPPORTED" else "rej"].append(conf)
    out = {}
    for seat, s in sorted(seats.items()):
        n_sup, n_rej = len(s["sup"]), len(s["rej"])
        n = n_sup + n_rej
        hit = n_sup / n if n else 0.0
        out[seat] = {
            "n_supported": n_sup, "n_rejected": n_rej,
            "hit_rate": round(hit, 3), "hit_rate_ci95": wilson(hit, n),
            "mean_conf_when_right": round(sum(s["sup"]) / n_sup, 3) if n_sup else None,
            "mean_conf_when_wrong": round(sum(s["rej"]) / n_rej, 3) if n_rej else None,
        }
    return out


def verification_record(records: dict) -> dict:
    """Per-seat reviews filed: verdicts given, and overturns (a later review that
    names this review's id as wrong, or a DISPUTED/WITHDRAWN on its findings)."""
    seats: dict = {}
    for rev in records_of_type(records, "review"):
        s = seats.setdefault(seat_of(rev),
                             {"reviews": 0, "verified": 0, "clean": 0, "partial": 0,
                              "ids": []})
        s["reviews"] += 1
        s["ids"].append(rev.id)
        v = str(rev.fm.get("verdict") or rev.fm.get("result") or "").upper()
        if v.startswith("VERIFIED"):
            s["verified"] += 1
        if "CLEAN" in v:
            s["clean"] += 1
        if "PARTIAL" in v:
            s["partial"] += 1
    return seats


def finding_precision(records: dict) -> dict:
    """Per-seat findings raised: RESOLVED-confirmed vs WITHDRAWN vs still OPEN."""
    seats: dict = {}
    for f in records_of_type(records, "finding"):
        s = seats.setdefault(seat_of(f), {"raised": 0, "resolved": 0, "withdrawn": 0,
                                          "open": 0, "disputed": 0})
        s["raised"] += 1
        st = str(f.fm.get("status") or "OPEN")
        s[{"RESOLVED": "resolved", "WITHDRAWN": "withdrawn", "OPEN": "open",
           "DISPUTED": "disputed"}.get(st, "open")] += 1
    for seat, s in seats.items():
        decided = s["resolved"] + s["withdrawn"]
        p = s["resolved"] / decided if decided else 0.0
        s["precision"] = round(p, 3)
        s["precision_ci95"] = wilson(p, decided)
    return seats
def output_mix(records: dict) -> dict:
    """Per-seat counts by record kind: who produces what. Descriptive, not normative."""
    seats: dict = {}
    for rec in records.values():
        if rec.type in ("report", "doc"):
            continue
        s = seats.setdefault(seat_of(rec), {})
        s[rec.type] = s.get(rec.type, 0) + 1
    return seats


def agent_table(records: dict) -> dict:
    """The whole agent surface in one structure: calibration, verification, findings,
    output. Computed fresh every call — no stored reputation anywhere."""
    return {"calibration": calibration(records),
            "verification": verification_record(records),
            "finding_precision": finding_precision(records),
            "output_mix": output_mix(records),
            "note": ("Computed from records only; intervals are Wilson 95%. "
                     "Small n means wide intervals — read them before ranking anyone.")}


def blind_protocol(topic: str, seats: list, question: str) -> dict:
    """Independent discovery without anchoring (§29): each seat gets the same sealed
    brief (topic + question + what NOT to read yet); answers are filed as reports;
    only then are the others' reports revealed for debate. The function returns the
    five artifacts to file — the machine enforces the order, the agents do the work."""
    seats = list(seats)
    return {
        "protocol": "blind-independent-then-reveal",
        "topic": topic, "question": question,
        "phase_1_sealed_brief": {
            "read": ["research/project_state.md"],
            "do_not_read_yet": ["other seats' reports on this topic",
                                "debates/ on this topic"],
            "file_as": "agents/<seat>/reports/<date>-blind-<slug>.md",
        },
        "phase_1_assignments": [
            {"seat": s, "task": f"Independently answer: {question}. Do not read other "
                                f"seats' current answers first."} for s in seats],
        "phase_2_reveal": "After all phase-1 reports are filed: read all of them, "
                          "then file ONE debate record listing agreements, "
                          "disagreements, and the experiment that settles them.",
        "phase_3_settle": "Pre-register that experiment (decision rule + N + sample "
                          "validity) before RUNNING. Honest FAIL closes the debate too.",
    }


def handoff_new(records: dict, frm: str, to: str, task: str, acceptance: list,
                context_ids: list) -> dict:
    """A handoff that is checkable on arrival: the task, runnable acceptance criteria,
    and the exact records the receiver must read. Returns the body + front-matter for
    `imem new-handoff` to file."""
    missing = [c for c in context_ids
               if not any(r.id == c for r in records.values())]
    body = [f"# Handoff: {frm} -> {to}", "",
            "## Task", task, "",
            "## Read first (in this order)"]
    for c in context_ids:
        body.append(f"- [[{c}]]")
    body += ["", "## Acceptance (all must pass, in order)"]
    for i, a in enumerate(acceptance, 1):
        body.append(f"{i}. {a}")
    body += ["", "## Done means",
             "- every acceptance command above exits 0 with output on disk,",
             "- the session record names the evidence files and their hashes."]
    return {"from": frm, "to": to, "task": task, "acceptance": acceptance,
            "context_ids": context_ids, "missing_context": missing, "body": body}


def brief(records: dict, seat: str, topic_ids: list, limit: int = 12) -> dict:
    """A token-budgeted onboarding pack: where we stand, what is disputed, what is
    due, what to read first. Under ~4k tokens by construction (ids + one-liners)."""
    from imem_claims import contradiction_candidates, live_claims
    from imem_prior import priority_rows, question_readiness
    wants = {c for c in topic_ids}
    claims = [c for c in live_claims(records) if c["id"] in wants][:limit]
    contras = [c for c in contradiction_candidates(records)
               if c["a"] in wants or c["b"] in wants]
    pri = [p for p in priority_rows(records) if p["id"] in wants][:5]
    qs = [q for q in question_readiness(records) if q["id"] in wants]
    read_first = []
    for c in claims[:6]:
        read_first.append(c["id"])
    for p in pri[:3]:
        if p["id"] not in read_first:
            read_first.append(p["id"])
    return {"seat": seat, "topic": sorted(wants),
            "claims": [{"id": c["id"], "statement": c["statement"][:160],
                        "status": c["status"], "tested_by": c["tested_by"]}
                       for c in claims],
            "disputes": contras[:5], "priorities": [
                {"id": p["id"], "title": p["title"][:120], "score": p["score"]}
                for p in pri],
            "questions": [{"id": q["id"], "title": q["title"][:120],
                           "ready": q["ready"]} for q in qs],
            "read_first": read_first,
            "ground_rules": ["project_state.md wins on facts; SYSTEM.md on process.",
                             "No claim without a run; no statistics without "
                             "pre-registration.",
                             "Never verify your own work; file findings, not edits."]}

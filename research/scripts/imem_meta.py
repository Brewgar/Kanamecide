#!/usr/bin/env python3
"""imem_meta.py — the memory watching itself: process metrics and pathology detectors.

WHY (measured): the store audits records but never the *research process*. Nobody can
answer: how much of our writing is process overhead vs engine research? Are critiques
closing or accumulating? Are records growing past readability? The E-0013 saga — 24%
of all record bytes on one PENDING experiment's pre-registration bureaucracy — was
invisible to every audit. These detectors make it visible, every run.

METRICS (all computed from records + git, no new bookkeeping):
  * overhead share: bytes/sessions/commits per experiment vs per engine-code commit.
  * critique closure: OPEN blocking findings by age; oldest open finding.
  * growth: record-size distribution, over-budget records, prose-link density.
  * research velocity: experiments PENDING->COMPLETED latency, verdict mix.
  * memory health: dangling-link count, anchor-drift count, untested SUPPORTED claims.

Every number carries its derivation. Thresholds are advisory; trends are the signal.
"""
from __future__ import annotations

import collections
import re
import subprocess

from imem_core import as_list, records_of_type


def _git_log(limit: int = 400):
    try:
        p = subprocess.run(["git", "--no-pager", "log", "--pretty=%h|%ad|%s",
                            "--date=short", f"-{limit}"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=60)
    except Exception:
        return []
    out = []
    for line in (p.stdout or "").splitlines():
        parts = line.split("|", 2)
        if len(parts) == 3:
            out.append(tuple(parts))
    return out


def process_metrics(records: dict, commits: list = None) -> dict:
    """Overhead vs research, computed — the number the E-0013 saga needed in July."""
    if commits is None:
        commits = _git_log()
    exps = records_of_type(records, "experiment")
    ex_bytes = sum(e.size for e in exps)
    all_bytes = sum(r.size for r in records.values())
    revs = records_of_type(records, "review")
    sess = records_of_type(records, "session")
    # bytes whose records exist to argue about other records (critique/review/repair)
    import re
    meta_kinds = 0
    for r in records.values():
        t = (r.title + " " + r.body[:2000]).lower()
        if any(k in t for k in ("critique", "repair", "seam", "ruling", "re-critique",
                                "append-only", "withdraw", "re-pin", "pointer")):
            meta_kinds += r.size
    by_exp: dict = {}
    for e in exps:
        fam = e.id.lower().replace("-", "")
        fam_bytes = e.size + sum(
            r.size for r in records.values()
            if fam in r.key.lower().replace("-", "") and r.key != e.key)
        by_exp[e.id] = {"bytes": fam_bytes,
                        "status": str(e.fm.get("status")),
                        "share": round(fam_bytes / max(1, all_bytes), 4)}
    top = sorted(by_exp.items(), key=lambda kv: -kv[1]["bytes"])[:8]
    commit_themes = collections.Counter()
    for _h, _d, s in commits:
        sl = s.lower()
        if "e-0013" in sl or "e0013" in sl:
            commit_themes["e0013"] += 1
        elif "e-001" in sl or "e00" in sl:
            commit_themes["experiment-other"] += 1
        elif "src" in sl or ".cpp" in sl or "eval" in sl or "search" in sl:
            commit_themes["engine-code"] += 1
        elif "research" in sl or "memory" in sl or "imem" in sl:
            commit_themes["memory-infra"] += 1
        else:
            commit_themes["other"] += 1
    return {
        "records": len(records), "record_bytes": all_bytes,
        "experiment_bytes": ex_bytes,
        "experiment_share": round(ex_bytes / max(1, all_bytes), 4),
        "process_overhead_bytes": meta_kinds,
        "process_overhead_share": round(meta_kinds / max(1, all_bytes), 4),
        "reviews": len(revs), "sessions": len(sess),
        "bytes_per_experiment_family": {k: v for k, v in top},
        "commits": len(commits), "commit_themes": dict(commit_themes),
        "note": ("Overhead share = bytes of records whose first 2000 chars argue about "
                 "other records (critique/repair/ruling/seam/withdraw/re-pin/pointer). "
                 "Advisory; read the families, not just the number."),
    }
def pathology_report(records: dict, lint_out: dict, claims_fn=None) -> list:
    """Named pathologies with counts and the worst offenders. Each entry is a work
    item waiting to happen: what, how big, where, and the one command that shrinks it.
    """
    from imem_core import BUDGET_BYTES, LINE_POINTER_RE, PROSE_LINK_WARN_AT
    out = []
    over = sorted(((r.id, r.size, r.key) for r in records.values()
                   if r.size > BUDGET_BYTES and str(r.fm.get("kind") or "") != "container"),
                  key=lambda t: -t[1])
    if over:
        out.append({"pathology": "giant-records", "count": len(over),
                    "worst": [{"id": i, "bytes": s, "rel": k} for i, s, k in over[:6]],
                    "fix": "Split into atomic claims/findings/runs; or set kind: "
                           "container with a rationale. Budget=%d." % BUDGET_BYTES})
    prose_heavy = sorted(
        ((r.id, len(r.ids_prose), r.key) for r in records.values()
         if len(r.ids_prose) >= PROSE_LINK_WARN_AT), key=lambda t: -t[1])
    if prose_heavy:
        out.append({"pathology": "prose-only-links", "count": len(prose_heavy),
                    "worst": [{"id": i, "n": n, "rel": k} for i, n, k in prose_heavy[:6]],
                    "fix": "Declare the ids you mean in front-matter or as [[ID]]; "
                           "then imem lint goes quiet."})
    line_ptr = sorted(
        ((r.id, len(LINE_POINTER_RE.findall(r.body)), r.key) for r in records.values()
         if LINE_POINTER_RE.findall(r.body)), key=lambda t: -t[1])
    if line_ptr:
        out.append({"pathology": "line-number-pointers", "count": len(line_ptr),
                    "worst": [{"id": i, "n": n, "rel": k} for i, n, k in line_ptr[:6]],
                    "fix": "Replace L### with REC#anchor; imem repin keeps them true."})
    drift = [w for w in lint_out.get("warnings", []) if w.get("area") == "anchor-drift"]
    if drift:
        out.append({"pathology": "anchor-drift", "count": len(drift),
                    "worst": drift[:6],
                    "fix": "Review each drift, then `imem repin <ID>`."})
    dang = [p for p in lint_out.get("problems", []) if p.get("area") == "link"]
    if dang:
        out.append({"pathology": "dangling-links", "count": len(dang),
                    "worst": dang[:6],
                    "fix": "Fix the id or add the missing record; links are promises."})
    unsupported = [c for c in (claims_fn() if claims_fn else [])
                   if c.get("status") == "SUPPORTED" and not c.get("tested_by")]
    if unsupported:
        out.append({"pathology": "supported-but-untested", "count": len(unsupported),
                    "worst": unsupported[:6],
                    "fix": "SUPPORTED requires L3 (a measuring experiment). Demote to "
                           "OPEN/TESTING or file the test."})
    return out


def velocity(records: dict) -> dict:
    """How fast research moves: experiment latency PENDING->COMPLETED (by dates on
    record), verdict mix, open-blocking-finding age."""
    from datetime import date
    lat, verdicts = [], collections.Counter()
    for e in records_of_type(records, "experiment"):
        verdicts[str(e.fm.get("result") or "—").split()[0][:12] or "—"] += 1
        c, u = str(e.fm.get("created") or ""), str(
            e.fm.get("last_updated") or e.fm.get("closed") or e.fm.get("completed") or "")
        try:
            if c >= "2026-01-01" and u >= "2026-01-01" and u >= c:
                d0 = date.fromisoformat(c[:10])
                d1 = date.fromisoformat(u[:10])
                lat.append((d1 - d0).days)
        except ValueError:
            pass
    lat.sort()
    fnds = records_of_type(records, "finding")
    open_blocking = [f for f in fnds if str(f.fm.get("status")) == "OPEN"
                     and str(f.fm.get("severity")) == "blocking"]
    ages = []
    for f in open_blocking:
        try:
            c = str(f.fm.get("created") or "")[:10]
            if c >= "2026-01-01":
                ages.append((date.today() - date.fromisoformat(c)).days)
        except ValueError:
            pass
    return {
        "experiments": len(records_of_type(records, "experiment")),
        "verdict_mix": dict(verdicts),
        "latency_days": {"n": len(lat),
                         "median": lat[len(lat) // 2] if lat else None,
                         "max": lat[-1] if lat else None},
        "open_blocking_findings": len(open_blocking),
        "oldest_open_blocking_days": max(ages) if ages else None,
    }


# --- freshness: which live records are aging without movement (advisory) ---------

# Per-kind day thresholds for a LIVE (non-terminal) record to stop being "fresh".
# Deterministic and visible: the policy values are the system, listed here so every
# reader can audit them. Diagnosed by date parsing of the last activity timestamp
# (last_updated, closed, completed, or created, in that order of preference).
FRESHNESS_POLICY_DAYS = {
    "work": 14,
    "handoff": 7,
    "question": 21,
    "hypothesis": 30,
    "claim": 21,
    "finding": 14,
    "debate": 21,
    "experiment": 14,
}
# Non-terminal statuses per kind — a terminal record is history, not stale debt.
_LIVE_STATUS = {
    "work": {"OPEN", "IN_PROGRESS", "BLOCKED"},
    "handoff": {"REQUESTED", "ACCEPTED"},
    "question": {"OPEN", "INVESTIGATING", "BLOCKED"},
    "hypothesis": {"OPEN", "TESTING"},
    "claim": {"OPEN", "UNTESTED", "DISPUTED"},
    "finding": {"OPEN", "DISPUTED"},
    "debate": {"OPEN", "ROUTED"},
    "experiment": {"PENDING", "RUNNING"},
}

# Work records carry their own dated activity in the body's append-only Work Log
# ('- YYYY-MM-DD — ...'); those dates count exactly like front-matter ones (W-0006).
_WORK_LOG_DATE_RE = re.compile(r"^[ \t]*-[ \t]+(\d{4}-\d{2}-\d{2})[ \t]+—", re.MULTILINE)


def _record_activity_date(rec):
    """Most recent authored timestamp on the record, or None. Deterministic: ties to
    the front-matter the corpus carries, not to file mtimes (which are checkout-noisy).
    Work records also count their dated Work Log body lines ('- YYYY-MM-DD —'), taking
    max(front-matter, latest body line): the append-only log is where activity lands."""
    from datetime import date
    best = None
    for field in ("last_updated", "closed", "completed", "created"):
        raw = str(rec.fm.get(field) or "")[:10]
        if len(raw) == 10 and raw[4] == "-" and raw[7] == "-":
            try:
                best = date.fromisoformat(raw)
                break
            except ValueError:
                continue
    if rec.type == "work":
        for m in _WORK_LOG_DATE_RE.finditer(rec.body):
            try:
                d = date.fromisoformat(m.group(1))
            except ValueError:
                continue
            if best is None or d > best:
                best = d
    return best


def freshness_rows(records: dict, today=None, policy: dict = None) -> list:
    """[{id, type, status, age_days, last_activity, window, rel}] for every LIVE record
    older than its kind's freshness window. Advisory only: a stale record is a review
    flag, never an error; kinds with no live statuses (decisions, principles) are
    structurally durable and are never flagged by this report. A future-dated activity
    date is an explicit ANOMALY row (anomaly=True) — R-0027 D-4: fail loud, not open."""
    from datetime import date as _date
    today = today or _date.today()
    policy = dict(FRESHNESS_POLICY_DAYS if policy is None else policy)
    rows = []
    for rec in sorted(records.values(), key=lambda r: (r.type, r.id)):
        if rec.fm.get("example"):
            continue
        live = _LIVE_STATUS.get(rec.type)
        if not live:
            continue
        status = str(rec.fm.get("status") or "")
        if status not in live:
            continue
        last = _record_activity_date(rec)
        if last is None:
            continue
        age = (today - last).days
        window = policy.get(rec.type, 21)
        if age < 0:
            rows.append({"id": rec.id, "type": rec.type, "status": status,
                         "age_days": age, "last_activity": last.isoformat(),
                         "window_days": window, "rel": rec.key, "anomaly": True,
                         "why": (f"ANOMALY: future-dated activity {last.isoformat()} "
                                 f"is after today {today.isoformat()} for live "
                                 f"{rec.type} ({status}) — date untrusted")})
        elif age > window:
            rows.append({"id": rec.id, "type": rec.type, "status": status,
                         "age_days": age, "last_activity": last.isoformat(),
                         "window_days": window, "rel": rec.key,
                         "why": (f"live {rec.type} ({status}) untouched for {age} days "
                                 f"(window {window})")})
    rows.sort(key=lambda r: (not r.get("anomaly"), -r["age_days"], r["id"]))
    return rows


def freshness_report(records: dict, today=None) -> dict:
    rows = freshness_rows(records, today=today)
    return {"stale_records": rows, "n_stale": len(rows),
            "advisory": ("Freshness rows are review flags, not errors; a live record "
                         "older than its window deserves a dated addendum, a routing "
                         "handoff, or an explicit keep-open note — not silence.")}

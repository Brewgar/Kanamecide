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

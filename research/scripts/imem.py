#!/usr/bin/env python3
"""imem.py — the single entry point for the institutional-memory layer (DEC-0012).

Every command is read-only unless its name says otherwise (repin/repair/write/new):
  records & links:  index, lint, anchors, repin, repair-links, graph, links
  retrieval:        ask, search, similar, beliefs, chain, provenance
  science:          contradictions, duplicates, revivals, novelty, priority, questions,
                    evidence, prereg, promote, findings, finding
  agents & process: agents, blind, handoff, brief, meta, pathologies, velocity,
                    freshness, codemap
  system:           snapshot, metrics, new-claim, new-finding, audit, selftest, version

Output is human text by default, `--json` for machines. Exit codes: 0 ok; 1 problems
found (lint/audit, or `novelty --strict`) or command failed; 2 usage error.
Deterministic everywhere.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import imem_agents as AG  # noqa: E402
import imem_claims as CL  # noqa: E402
import imem_code as CD  # noqa: E402
import imem_core as C  # noqa: E402
import imem_evidence as EV  # noqa: E402
import imem_meta as MT  # noqa: E402
import imem_prior as PR  # noqa: E402
import imem_retrieve as RT  # noqa: E402
import imem_text as TX  # noqa: E402

VERSION = "2.1.0 (DEC-0012 + freshness/novelty)"


def emit(obj, as_json: bool):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if as_json:
        print(C.jdump(obj), end="")
        return
    print(render(obj))


def render(obj, indent: int = 0) -> str:
    """Small deterministic pretty-printer for dicts/lists/scalars (no pprint width
    games: stable output for golden tests)."""
    pad = "  " * indent
    if isinstance(obj, dict):
        if not obj:
            return pad + "{}"
        lines = []
        for k in obj:
            v = obj[k]
            if isinstance(v, (dict, list)):
                lines.append(f"{pad}{k}:")
                lines.append(render(v, indent + 1))
            else:
                lines.append(f"{pad}{k}: {v}")
        return "\n".join(lines)
    if isinstance(obj, (list, tuple)):
        if not obj:
            return pad + "[]"
        lines = []
        for v in obj:
            if isinstance(v, (dict, list)):
                lines.append(pad + "-")
                lines.append(render(v, indent + 1))
            else:
                lines.append(f"{pad}- {v}")
        return "\n".join(lines)
    return pad + str(obj)


def load_all(args):
    records, warnings = C.load_corpus()
    return records, warnings


def load_embed(records, args) -> object:
    if getattr(args, "no_semantic", False):
        return None
    try:
        return TX.EmbedSpace.build(records, k=getattr(args, "dim", 64))
    except Exception as exc:
        print(f"semantic layer unavailable ({exc}); lexical only", file=sys.stderr)
        return None


def metrics_load() -> dict:
    p = C.INDEX_DIR / "metrics.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
    return {}
def cmd_index(args):
    records, warnings = load_all(args)
    info = C.build_db(records)
    emit({"index": info, "load_warnings": warnings}, args.json)
    return 0


def cmd_lint(args):
    records, warnings = load_all(args)
    findings = C.records_of_type(records, "finding")
    claims = CL.live_claims(records)
    out = C.lint(records, findings, claims, warnings)
    out["counts"] = {k: len(v) for k, v in out.items() if k != "counts"}
    emit(out, args.json)
    return 1 if out["problems"] else 0


def cmd_anchors(args):
    records, _w = load_all(args)
    if args.id:
        rec = C.by_id(records, args.id)
        if rec is None:
            print(f"no record {args.id}")
            return 1
        table = {b.slug: b.sha8 for b in rec.blocks}
        pinned = rec.anchors_pinned or {}
        rows = [{"anchor": s, "sha8": h, "pinned": pinned.get(s, ""),
                 "drift": bool(pinned.get(s) and pinned.get(s) != h),
                 "title": next((b.title for b in rec.blocks if b.slug == s), "")}
                for s, h in sorted(table.items())]
        emit({"id": rec.id, "rel": rec.key, "blocks": len(rows), "anchors": rows},
             args.json)
        return 0
    rows = [{"id": r.id, "rel": r.key, "blocks": len(r.blocks),
             "pinned": len(r.anchors_pinned or {})}
            for r in sorted(records.values(), key=lambda x: x.id)]
    emit({"records": len(rows), "rows": rows}, args.json)
    return 0


def cmd_repin(args):
    records, _w = load_all(args)
    rec = C.by_id(records, args.id)
    if rec is None:
        print(f"no record {args.id}")
        return 1
    if args.check:
        table = {b.slug: b.sha8 for b in rec.blocks}
        pinned = rec.anchors_pinned or {}
        drift = {s: (pinned.get(s), h) for s, h in table.items()
                 if pinned.get(s) and pinned.get(s) != h}
        missing = [s for s in pinned if s not in table]
        emit({"id": rec.id, "drift": drift, "missing": missing,
              "clean": not drift and not missing}, args.json)
        return 0
    if not args.write and not args.add:
        print("refusing to rewrite without --write (dry run: use --check)")
        return 2
    res = C.repin_file(rec.path, only_slugs=args.only)
    emit(res, args.json)
    return 0


def cmd_graph(args):
    records, _w = load_all(args)
    rec = C.by_id(records, args.id)
    if rec is None:
        print(f"no record {args.id}")
        return 1
    nb = RT.neighbors(records, [rec.key], depth=args.depth)
    rows = []
    for key, (dist, kind) in sorted(nb.items(), key=lambda kv: (kv[1][0], kv[0])):
        r = records[key]
        rows.append({"id": r.id, "type": r.type, "title": r.title[:100],
                     "distance": dist, "via": kind})
    emit({"id": args.id, "neighbors": rows}, args.json)
    return 0


def cmd_links(args):
    records, _w = load_all(args)
    rec = C.by_id(records, args.id)
    if rec is None:
        print(f"no record {args.id}")
        return 1
    rows = []
    for rel, dst, anch, fld in rec.links_fm + rec.links_inline:
        tier = "frontmatter" if (rel, dst, anch, fld) in rec.links_fm else "inline"
        rows.append({"rel": rel, "dst": dst, "anchor": anch or "", "field": fld,
                     "tier": tier, "resolves": C.link_resolves(records, dst, anch)})
    emit({"id": rec.id, "declared": rows, "prose_only_ids": rec.ids_prose},
         args.json)
    return 0
def cmd_search(args):
    records, _w = load_all(args)
    embed = load_embed(records, args)
    emit(RT.search(records, args.query, embed, limit=args.limit,
                   graph_depth=args.depth), args.json)
    return 0


def cmd_ask(args):
    records, _w = load_all(args)
    embed = load_embed(records, args)
    emit(RT.answer(records, args.query, embed, limit=args.limit), args.json)
    return 0


def cmd_similar(args):
    records, _w = load_all(args)
    embed = load_embed(records, args)
    if embed is None:
        print("semantic layer unavailable")
        return 1
    rec = C.by_id(records, args.id)
    if rec is None:
        print(f"no record {args.id}")
        return 1
    rows = [{"key": k, "id": records[k].id, "title": records[k].title[:110],
             "cosine": round(s, 4)} for k, s in embed.similar(rec.key, args.limit)]
    emit({"id": args.id, "similar": rows}, args.json)
    return 0


def cmd_beliefs(args):
    records, _w = load_all(args)
    rows = []
    for c in CL.live_claims(records):
        lad = EV.promotion_ladder(records, C.by_id(records, c["id"]))
        rows.append({"id": c["id"], "statement": c["statement"][:160],
                     "status": c["status"], "rung": lad["rung"],
                     "ladder": lad["ladder"], "confidence": c["confidence"],
                     "tested_by": c["tested_by"],
                     "measured_by": lad["measured_by"],
                     "verified_by": lad["verified_by"]})
    rows.sort(key=lambda r: (-r["rung"], r["id"]))
    emit({"beliefs": rows,
          "note": "PROJECTION — rung + receipts travel together; read the records."},
         args.json)
    return 0


def cmd_chain(args):
    records, _w = load_all(args)
    emit(EV.chain(records, args.id), args.json)
    return 0


def cmd_provenance(args):
    records, _w = load_all(args)
    emit(EV.chain(records, args.id), args.json)
    return 0


def cmd_contradictions(args):
    records, _w = load_all(args)
    out = CL.contradiction_candidates(records)
    emit({"contradictions": out, "count": len(out),
          "note": "CANDIDATES — each carries its resolution task; nothing is merged."},
         args.json)
    return 0


def cmd_duplicates(args):
    records, _w = load_all(args)
    embed = load_embed(records, args)
    out = CL.duplicate_claims(records, embed)
    emit({"duplicates": out, "count": len(out)}, args.json)
    return 0


def cmd_revivals(args):
    records, _w = load_all(args)
    out = PR.revival_rows(records, metrics_load())
    if args.due_only:
        out = [r for r in out if r["trigger_state"].get("met")]
    emit({"revivals": out, "count": len(out)}, args.json)
    return 0


def cmd_priority(args):
    records, _w = load_all(args)
    rows = PR.priority_rows(records)
    emit({"priorities": rows[: args.limit], "count": len(rows),
          "weights_version": PR.PRIORITY_WEIGHTS_VERSION,
          "formula": ("p_success*impact_elo*info_gain*readiness/"
                      "cost_hours^0.7*novelty*reversibility")}, args.json)
    return 0


def cmd_questions(args):
    records, _w = load_all(args)
    emit({"questions": PR.question_readiness(records)}, args.json)
    return 0
def cmd_evidence(args):
    records, _w = load_all(args)
    rec = C.by_id(records, args.id)
    if rec is None:
        print(f"no record {args.id}")
        return 1
    emit({"id": rec.id, "artifacts": EV.evidence_check(records, rec)}, args.json)
    return 0


def cmd_prereg(args):
    records, _w = load_all(args)
    rec = C.by_id(records, args.id)
    if rec is None:
        print(f"no record {args.id}")
        return 1
    st = EV.prereg_state(rec)
    if args.park:
        if not args.write:
            print("refusing to rewrite without --write")
            return 2
        from imem_core import split_frontmatter
        text = C.read_text(rec.path)
        fm_text, _body = split_frontmatter(text)
        pin = EV.prereg_fingerprint(rec)
        if "prereg_sha256:" in fm_text:
            lines = text.splitlines()
            for i, ln in enumerate(lines[1:], 1):
                if ln.startswith("prereg_sha256:"):
                    lines[i] = f"prereg_sha256: {pin}"
                    break
                if ln.startswith("---"):
                    break
            text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
        else:
            text = text.replace("---\n", f"---\nprereg_sha256: {pin}\n", 1)
        rec.path.write_text(text, encoding="utf-8", newline="\n")
        emit({"id": rec.id, "parked": pin[:12] + "..."}, args.json)
        return 0
    emit({"id": rec.id, **st}, args.json)
    return 1 if st.get("moved") else 0


def cmd_promote(args):
    records, _w = load_all(args)
    rows = []
    for rec in C.records_of_type(records, "claim", "hypothesis"):
        if rec.fm.get("example"):
            continue
        lad = EV.promotion_ladder(records, rec)
        status = str(rec.fm.get("status") or "")
        expect = "SUPPORTED" if lad["rung"] >= 3 else (
            "TESTING" if lad["rung"] == 2 else "OPEN")
        rows.append({"id": rec.id, "status": status, "rung": lad["rung"],
                     "ladder": lad["ladder"],
                     "mismatch": status == "SUPPORTED" and lad["rung"] < 3,
                     "suggested": expect})
    bad = [r for r in rows if r["mismatch"]]
    emit({"ladder": rows, "mismatches": bad,
          "rule": "SUPPORTED requires L3 (a measuring experiment)."}, args.json)
    return 1 if bad and args.strict else 0


def cmd_findings(args):
    records, _w = load_all(args)
    rows = []
    for f in C.records_of_type(records, "finding"):
        rows.append({
            "id": f.id, "severity": str(f.fm.get("severity") or "?"),
            "status": str(f.fm.get("status") or "?"),
            "target": str(f.fm.get("target") or ""),
            "title": (str(f.fm.get("title")) or "")[:140],
            "raised_by": str(f.fm.get("raised_by") or f.fm.get("reviewer") or ""),
            "review": str(f.fm.get("review") or ""),
            "created": str(f.fm.get("created") or ""), "rel": f.key})
    if args.open_only:
        rows = [r for r in rows if r["status"] == "OPEN"]
    if args.target:
        rows = [r for r in rows if r["target"].split("#")[0] == args.target]
    order = {"blocking": 0, "major": 1, "minor": 2, "nit": 3}
    rows.sort(key=lambda r: (order.get(r["severity"], 9), r["id"]))
    emit({"findings": rows, "count": len(rows)}, args.json)
    return 0
def cmd_finding(args):
    records, _w = load_all(args)
    rec = C.by_id(records, args.id)
    if rec is None or rec.type != "finding":
        print(f"no finding {args.id}")
        return 1
    if args.close:
        if not args.write:
            print("refusing to rewrite without --write")
            return 2
        if str(rec.fm.get("status")) != "OPEN":
            print(f"{args.id} is {rec.fm.get('status')}, not OPEN")
            return 1
        text = C.read_text(rec.path)
        lines = text.splitlines()
        for i, ln in enumerate(lines[1:], 1):
            if ln.startswith("status:"):
                lines[i] = "status: RESOLVED"
            elif ln.startswith("resolution:"):
                lines[i] = f"resolution: {args.close}"
            elif ln.startswith("resolved_by:"):
                lines[i] = f"resolved_by: {args.by or 'unknown'}"
            elif ln.startswith("---"):
                break
        rec.path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        emit({"id": args.id, "status": "RESOLVED"}, args.json)
        return 0
    emit({"id": rec.id, "fm": dict(rec.fm), "rel": rec.key}, args.json)
    return 0


def cmd_agents(args):
    records, _w = load_all(args)
    emit(AG.agent_table(records), args.json)
    return 0


def cmd_blind(args):
    emit(AG.blind_protocol(args.topic, args.seats, args.question), args.json)
    return 0


def cmd_handoff(args):
    records, _w = load_all(args)
    out = AG.handoff_new(records, args.frm, args.to, args.task,
                         args.acceptance or [], args.context or [])
    emit(out, args.json)
    return 1 if out["missing_context"] else 0


def cmd_brief(args):
    records, _w = load_all(args)
    emit(AG.brief(records, args.seat, args.ids or []), args.json)
    return 0


def cmd_meta(args):
    records, _w = load_all(args)
    lint_out = C.lint(records, C.records_of_type(records, "finding"),
                      CL.live_claims(records), [])
    emit(MT.process_metrics(records), args.json)
    return 0


def cmd_pathologies(args):
    records, _w = load_all(args)
    lint_out = C.lint(records, C.records_of_type(records, "finding"),
                      CL.live_claims(records), [])
    emit({"pathologies": MT.pathology_report(
        records, lint_out, lambda: CL.live_claims(records))}, args.json)
    return 0


def cmd_velocity(args):
    records, _w = load_all(args)
    emit(MT.velocity(records), args.json)
    return 0


def cmd_freshness(args):
    """Live records that have aged past their kind's window (advisory, never an error).

    Exit 0 always: staleness is a review flag, not a gate. --max-age sets an ad-hoc
    window for every kind so an agent can ask a narrower/looser question without
    editing the policy."""
    records, _w = load_all(args)
    policy = None
    if getattr(args, "max_age", None) is not None:
        policy = {k: int(args.max_age) for k in MT.FRESHNESS_POLICY_DAYS}
    out = MT.freshness_report(records, today=None) if policy is None else {
        "stale_records": MT.freshness_rows(records, today=None, policy=policy),
        "n_stale": len(MT.freshness_rows(records, today=None, policy=policy)),
        "policy_override_days": int(args.max_age)}
    emit(out, args.json)
    return 0


def cmd_novelty(args):
    """Is this (id or free text) already in the project? Candidates with their basis.

    Read-only: never merges, never writes. Advisory exit 0; --strict exits 1 when any
    candidate is at or above the semantic/lexical thresholds, so a filing script can
    gate on it without parsing output."""
    records, _w = load_all(args)
    embed = load_embed(records, args)
    out = CL.novelty_report(records, args.query, embed=embed,
                            limit=getattr(args, "limit", 8))
    emit(out, args.json)
    if getattr(args, "strict", False) and out.get("candidates"):
        return 1
    return 0


def cmd_codemap(args):
    records, _w = load_all(args)
    idx = CD.symbol_index()
    if args.symbol:
        emit({"symbol": args.symbol, "defs": idx.get(args.symbol, [])}, args.json)
        return 0
    emit(CD.traceability(records, idx), args.json)
    return 0


def cmd_snapshot(args):
    records, warnings = load_all(args)
    embed = load_embed(records, args)
    findings = C.records_of_type(records, "finding")
    claims = CL.live_claims(records)
    lint_out = C.lint(records, findings, claims, warnings)
    out = {
        "generated": C.today(), "schema": C.SCHEMA_VERSION, "version": VERSION,
        "banner": "GENERATED by imem — derived, disposable; records are the truth",
        "records": len(records),
        "lint": {k: len(v) for k, v in lint_out.items()},
        "contradictions": CL.contradiction_candidates(records),
        "priorities": PR.priority_rows(records)[:25],
        "revivals": PR.revival_rows(records, metrics_load()),
        "questions": PR.question_readiness(records),
        "beliefs": [{"id": c["id"], "status": c["status"],
                     "rung": EV.promotion_ladder(records, C.by_id(records, c["id"]))["rung"]}
                    for c in claims],
        "agents": AG.agent_table(records),
        "process": MT.process_metrics(records),
        "pathologies": MT.pathology_report(records, lint_out, lambda: claims),
        "traceability": CD.traceability(records),
    }
    if embed is not None:
        out["semantic"] = {"dim": embed.dim, "fp": embed.fingerprint}
    info = C.write_snapshot(records, out)
    info["lint_counts"] = out["lint"]
    emit(info, args.json)
    return 0


def cmd_metrics(args):
    import json as _json
    p = C.INDEX_DIR / "metrics.json"
    if args.set:
        try:
            pairs = dict(kv.split("=", 1) for kv in args.set)
        except ValueError:
            print("metrics --set expects KEY=VALUE ...")
            return 2
        cur = metrics_load()
        for k, v in pairs.items():
            try:
                cur[k] = _json.loads(v)
            except ValueError:
                cur[k] = v
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(C.jdump(cur), encoding="utf-8", newline="\n")
        emit({"metrics": cur}, args.json)
        return 0
    emit({"metrics": metrics_load(),
          "hint": "imem metrics --set perft_nps=47000000 search.pvs_tt_complete=true"},
         args.json)
    return 0


def cmd_new_claim(args):
    extra = {"domain": args.domain, "parameter": args.parameter,
             "direction": args.direction, "scope": args.scope or "",
             "epistemic": args.epistemic, "confidence": args.confidence,
             "statement": args.statement}
    if args.tests:
        extra["tests"] = args.tests
    path = C.new_record("claim", args.title,
                        ["## Statement", args.statement, "",
                         "## Why it matters", args.why or "_fill in_", ""],
                        extra)
    emit({"wrote": path.relative_to(C.REPO_ROOT).as_posix()}, args.json)
    return 0


def cmd_new_finding(args):
    tgt = args.target + (("#" + args.anchor) if args.anchor else "")
    extra = {"severity": args.severity, "target": tgt, "raised_by": args.raised_by,
             "review": args.review or "", "resolution": "", "resolved_by": "",
             "verified_by": ""}
    path = C.new_record("finding", args.title,
                        ["## Finding", args.body or "_fill in_", "",
                         "## Evidence", "_commands, outputs, hashes_", ""],
                        extra)
    records, _w = C.load_corpus()
    rec = C.by_id(records, args.target)
    sug = ""
    if rec is not None and args.anchor:
        want = args.anchor
        if want not in {b.slug for b in rec.blocks}:
            sug = C.suggest_anchor(want, [b.slug for b in rec.blocks]) or ""
    emit({"wrote": path.relative_to(C.REPO_ROOT).as_posix(),
          "anchor_ok": bool(rec is not None and (not args.anchor or not sug)),
          "suggested_anchor": sug}, args.json)
    return 0


def cmd_audit(args):
    records, warnings = load_all(args)
    findings = C.records_of_type(records, "finding")
    claims = CL.live_claims(records)
    lint_out = C.lint(records, findings, claims, warnings)
    out = {"problems": lint_out["problems"], "warnings": lint_out["warnings"],
           "queue": lint_out["findings"],
           "pathologies": MT.pathology_report(records, lint_out, lambda: claims),
           "velocity": MT.velocity(records),
           "mismatches": [r for r in
                           [{"id": r2["id"], "status": r2["status"], "rung": r2["rung"]}
                            for r2 in ({
                                "id": rec.id, "status": str(rec.fm.get("status")),
                                "rung": EV.promotion_ladder(records, rec)["rung"]}
                                for rec in C.records_of_type(
                                    records, "claim", "hypothesis")
                                if not rec.fm.get("example"))]
                           if r["status"] == "SUPPORTED" and r["rung"] < 3]}
    out["counts"] = {"problems": len(out["problems"]),
                     "warnings": len(out["warnings"]), "queue": len(out["queue"])}
    emit(out, args.json)
    return 1 if out["problems"] or out["mismatches"] else 0
def cmd_selftest(args):
    import unittest
    loader = unittest.TestLoader()
    try:
        suite = loader.discover(str(C.RESEARCH_DIR / "scripts"), pattern="tests_imem.py")
    except Exception as exc:
        print(f"selftest discovery failed: {exc}")
        return 1
    runner = unittest.TextTestRunner(verbosity=1)
    res = runner.run(suite)
    return 0 if res.wasSuccessful() else 1


def build_parser():
    p = argparse.ArgumentParser(prog="imem",
                                description="Institutional memory layer (DEC-0012).")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--no-semantic", action="store_true", help="lexical+graph only")
    p.add_argument("--dim", type=int, default=64, help="embedding dims")
    p.add_argument("--limit", "-n", type=int, default=10)
    p.add_argument("--depth", "-d", type=int, default=1)
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, fn, help_text):
        s = sub.add_parser(name, help=help_text)
        s.set_defaults(fn=fn)
        return s

    add("index", cmd_index, "rebuild the SQLite index")
    add("lint", cmd_lint, "mechanical memory integrity (0 problems -> exit 0)")
    a = add("anchors", cmd_anchors, "list anchors, or show one record's table")
    a.add_argument("id", nargs="?")
    r = add("repin", cmd_repin, "check or re-pin a record's anchors")
    r.add_argument("id")
    r.add_argument("--check", action="store_true")
    r.add_argument("--write", action="store_true")
    r.add_argument("--add", action="store_true")
    r.add_argument("--only", nargs="*")
    g = add("graph", cmd_graph, "neighbourhood of a record")
    g.add_argument("id")
    li = add("links", cmd_links, "a record's declared links + prose-only ids")
    li.add_argument("id")
    s = add("search", cmd_search, "fused lexical+semantic+graph search")
    s.add_argument("query")
    a2 = add("ask", cmd_ask, "research-partner query: hits + claims + next")
    a2.add_argument("query")
    sm = add("similar", cmd_similar, "semantically similar records")
    sm.add_argument("id")
    add("beliefs", cmd_beliefs, "current best beliefs with ladder rungs")
    c = add("chain", cmd_chain, "provenance chain for a claim")
    c.add_argument("id")
    pv = add("provenance", cmd_provenance, "alias of chain")
    pv.add_argument("id")
    add("contradictions", cmd_contradictions, "direction-conflict candidates")
    add("duplicates", cmd_duplicates, "same-idea candidates")
    rv = add("revivals", cmd_revivals, "dead ideas with triggers evaluated")
    rv.add_argument("--due-only", action="store_true")
    add("priority", cmd_priority, "expected-value ranking with arithmetic")
    add("questions", cmd_questions, "open questions with readiness")
    ev = add("evidence", cmd_evidence, "per-artifact evidence verdicts")
    ev.add_argument("id")
    pg = add("prereg", cmd_prereg, "pre-registration pin state")
    pg.add_argument("id")
    pg.add_argument("--park", action="store_true")
    pg.add_argument("--write", action="store_true")

    st = add("promote", cmd_promote, "promotion-ladder mismatches")
    st.add_argument("--strict", action="store_true")
    f = add("findings", cmd_findings, "the findings ledger")
    f.add_argument("--open-only", action="store_true")
    f.add_argument("--target", default="")
    fo = add("finding", cmd_finding, "show or close one finding")
    fo.add_argument("id")
    fo.add_argument("--close", default="")
    fo.add_argument("--by", default="")
    fo.add_argument("--write", action="store_true")
    add("agents", cmd_agents, "agent calibration/verification/finding tables")
    bl = add("blind", cmd_blind, "blind independent-research protocol")
    bl.add_argument("topic")
    bl.add_argument("question")
    bl.add_argument("--seats", nargs="+", default=["researcher-architect",
                                                   "adversarial-reviewer"])
    ho = add("handoff", cmd_handoff, "build a checkable handoff")
    ho.add_argument("frm")
    ho.add_argument("to")
    ho.add_argument("task")
    ho.add_argument("--acceptance", nargs="*", default=[])
    ho.add_argument("--context", nargs="*", default=[])
    br = add("brief", cmd_brief, "token-budgeted onboarding pack")
    br.add_argument("seat")
    br.add_argument("ids", nargs="*")
    add("meta", cmd_meta, "process metrics (overhead vs research)")
    add("pathologies", cmd_pathologies, "named pathologies with fixes")
    add("velocity", cmd_velocity, "research velocity + finding age")
    fr = add("freshness", cmd_freshness, "live records aged past their window (advisory)")
    fr.add_argument("--max-age", type=int, default=None,
                    help="ad-hoc window (days) applied to every kind")
    nv = add("novelty", cmd_novelty, "candidates already close to a proposed claim")
    nv.add_argument("query", help="a record id or free text")
    nv.add_argument("--limit", "-n", type=int, default=8)
    nv.add_argument("--strict", action="store_true",
                    help="exit 1 when any candidate is found")
    cs = add("codemap", cmd_codemap, "code traceability")
    cs.add_argument("--symbol", default="")
    add("snapshot", cmd_snapshot, "write the JSON snapshot under _index/")
    m = add("metrics", cmd_metrics, "live project metrics (trigger inputs)")
    m.add_argument("--set", nargs="*")
    nc = add("new-claim", cmd_new_claim, "file an atomic claim")
    nc.add_argument("title")
    nc.add_argument("--statement", default="")
    nc.add_argument("--domain", default="unknown")
    nc.add_argument("--parameter", default="")
    nc.add_argument("--direction", default="")
    nc.add_argument("--scope", default="")
    nc.add_argument("--epistemic", default="hypothesis")
    nc.add_argument("--confidence", default="")
    nc.add_argument("--why", default="")
    nc.add_argument("--tests", nargs="*")
    nf = add("new-finding", cmd_new_finding, "file a closeable finding")
    nf.add_argument("title")
    nf.add_argument("--target", default="")
    nf.add_argument("--anchor", default="")
    nf.add_argument("--severity", default="major")
    nf.add_argument("--raised-by", default="")
    nf.add_argument("--review", default="")
    nf.add_argument("--body", default="")
    add("audit", cmd_audit, "lint + pathologies + velocity + mismatches")
    add("selftest", cmd_selftest, "run the imem unit tests")
    add("version", lambda a: (print(VERSION), 0)[1], "print version")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.fn(args) or 0
    except BrokenPipeError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

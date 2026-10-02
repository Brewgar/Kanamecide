#!/usr/bin/env python3
"""tests_imem.py — the institutional-memory layer's own tests (DEC-0012).

The memory system is software; it gets tested the same way the engine does:

    python research/scripts/tests_imem.py        (exit 0 == all green)
    python research/scripts/imem.py selftest

Two kinds of test live here:
  1. UNIT tests over synthetic fixtures (temp dirs) — the layer's own invariants:
     anchors/slug uniqueness, link tiers, lint rules, embeddings determinism,
     contradiction polarity, trigger evaluation, ladder rungs, issue tables.
  2. CORPUS INVARIANT tests over the real research/ store — cheap regression guards
     that fail loudly if a future change breaks a promise (e.g. a dangling link, or
     an anchor that no longer resolves). Deliberately structural, not count-based:
     the corpus is expected to grow every session.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
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


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def fixture(root: Path, rel: str, rid: str, typ: str, body: str, **fm):
    head = {"id": rid, "type": typ, "title": f'"{rid} title"', "status": "OPEN",
            "example": "false", "created": "2026-09-01"}
    head.update(fm)
    lines = ["---"] + [f"{k}: {v}" for k, v in head.items()] + ["---", ""]
    write(root / rel, "\n".join(lines) + body)


class TestAnchorsAndBlocks(unittest.TestCase):
    def test_slug_unique_on_duplicate_headings(self):
        body = "# A\nx\n## Same\none\n## Same\ntwo\n"
        blocks = C.blocks_of(body)
        slugs = [b.slug for b in blocks]
        self.assertEqual(len(slugs), len(set(slugs)), "slugs must be unique")
        self.assertEqual(slugs, ["a", "same", "same-2"])

    def test_sha_stable_under_whitespace_and_crlf(self):
        a = "# H\none two\nthree\n"
        b = "# H\r\none   two\r\n  three\r\n"
        self.assertEqual(C.blocks_of(a)[0].sha8, C.blocks_of(b)[0].sha8)

    def test_sha_changes_when_content_changes(self):
        self.assertNotEqual(C.blocks_of("# H\none\n")[0].sha8,
                            C.blocks_of("# H\ntwo\n")[0].sha8)

    def test_suggest_anchor_prefix_and_overlap(self):
        anchors = {"pre-registered-decision-rule", "power-and-sample-size"}
        self.assertEqual(C.suggest_anchor("pre-registered-decision-rule", anchors),
                         "pre-registered-decision-rule")
        self.assertEqual(C.suggest_anchor("pre-registered", anchors),
                         "pre-registered-decision-rule")
        self.assertEqual(C.suggest_anchor("power-and-sample-size", anchors),
                         "power-and-sample-size")
        self.assertIsNone(C.suggest_anchor("completely-unrelated-words", anchors))

    def test_repin_replaces_block_and_keeps_body(self):
        text = ("---\nid: X-1\nanchors: [\"old: deadbeef\"]\n---\n\n# H\n\nbody text\n")
        out = C.repin_frontmatter(text, {"h": "cafebabe"})
        self.assertIn("anchors: [\"h:cafebabe\"]", out)
        self.assertNotIn("old: deadbeef", out)
        self.assertIn("# H\n\nbody text", out)

    def test_repin_appends_when_absent(self):
        text = "---\nid: X-1\n---\n\n# H\n\nbody\n"
        out = C.repin_frontmatter(text, {"h": "12345678"})
        self.assertIn("anchors: [\"h:12345678\"]", out)
        self.assertTrue(out.rstrip().endswith("body"))


class TestLinksAndLint(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "research"
        self._saved = (C.RESEARCH_DIR, C.CLAIMS_DIR, C.FINDINGS_DIR)
        C.RESEARCH_DIR = self.root
        C.CLAIMS_DIR = self.root / "claims"
        C.FINDINGS_DIR = self.root / "findings"
        fixture(self.root, "hypotheses/H-0001-a.md", "H-0001", "hypothesis",
                "# H-0001\n\n## Statement\nA claim.\n")
        fixture(self.root, "claims/CLM-0001-c.md", "CLM-0001", "claim",
                "# CLM-0001\n\n## Statement\nA direction claim.\n",
                tests="[H-0001]", parameter="quiescence-nodes", direction="lower",
                domain="search", status="OPEN")
        fixture(self.root, "experiments/E-0001-x.md", "E-0001", "experiment",
                "# E-0001\n\n## Provenance\nrun\n", tests="[CLM-0001]",
                status="PENDING")

    def tearDown(self):
        (C.RESEARCH_DIR, C.CLAIMS_DIR, C.FINDINGS_DIR) = self._saved
        self.tmp.cleanup()

    def load(self):
        return C.load_corpus()

    def test_frontmatter_links_are_authoritative_tier(self):
        records, _w = self.load()
        rec = C.by_id(records, "E-0001")
        rels = {(rel, dst) for rel, dst, _a, _f in rec.links_fm}
        self.assertIn(("tests", "CLM-0001"), rels)

    def test_inline_and_prose_tiers(self):
        fixture(self.root, "debates/D-0001-x.md", "D-0001", "debate",
                "# D-0001\n\nSee [[H-0001#statement]] and also H-0001 in prose.\n")
        records, _w = self.load()
        rec = C.by_id(records, "D-0001")
        self.assertEqual(rec.links_inline[0][1:3], ("H-0001", "statement"))
        self.assertIn("H-0001", rec.ids_prose)

    def test_lint_flags_dangling_frontmatter_link(self):
        fixture(self.root, "work/W-0001-y.md", "W-0001", "work",
                "# W-0001\n", depends_on="[H-9999]")
        records, _w = self.load()
        out = C.lint(records, [], [])
        self.assertTrue(any(p["area"] == "link" and "H-9999" in p["msg"]
                            for p in out["problems"]))

    def test_lint_flags_missing_anchor_with_suggestion(self):
        fixture(self.root, "work/W-0002-y.md", "W-0002", "work",
                "# W-0002\n", depends_on="[H-0001#statementt]")
        records, _w = self.load()
        out = C.lint(records, [], [])
        msgs = [p["msg"] for p in out["problems"] if p["area"] == "link"]
        self.assertTrue(any("statemen" in m for m in msgs), msgs)

    def test_lint_flags_bad_status_and_prose_links(self):
        body = "\n".join(f"see CLM-{90+i:04d}" for i in range(9))
        fixture(self.root, "hypotheses/H-0002-b.md", "H-0002", "hypothesis",
                "# H-0002\n" + body + "\n", status="BOGUS")
        records, _w = self.load()
        out = C.lint(records, [], [])
        self.assertTrue(any(p["area"] == "status" for p in out["problems"]))
        self.assertTrue(any(w["area"] == "prose-links" for w in out["warnings"]))

    def test_lint_flags_budget_and_line_pointers_and_drift(self):
        write(self.root / "experiments/E-0002-big.md",
              "---\nid: E-0002\ntype: experiment\nstatus: PENDING\nexample: false\n"
              "created: 2026-09-01\nanchors: [\"e-0002: deadbeef\"]\n---\n\n"
              "# E-0002\n\nsee L1376-L1377\n\n" + ("word " * 13000))
        records, _w = self.load()
        out = C.lint(records, [], [])
        areas = {w["area"] for w in out["warnings"]}
        self.assertIn("budget", areas)
        self.assertIn("line-pointer", areas)
        self.assertIn("anchor-drift", areas)

    def test_blocking_finding_on_running_target_is_a_problem(self):
        fixture(self.root, "findings/FND-0001-z.md", "FND-0001", "finding",
                "# FND-0001\n", severity="blocking", target="E-0001",
                raised_by="adversarial-reviewer")
        records, _w = self.load()
        findings = C.records_of_type(records, "finding")
        records["experiments/E-0001-x.md"].fm["status"] = "RUNNING"
        out = C.lint(records, findings, [])
        self.assertTrue(any(p["area"] == "finding" for p in out["problems"]))

    def test_build_db_counts_links_and_unresolved(self):
        fixture(self.root, "work/W-0003-z.md", "W-0003", "work",
                "# W-0003\n", depends_on="[RUN-0099]")
        records, _w = self.load()
        info = C.build_db(records, Path(self.tmp.name) / "imem.sqlite")
        self.assertGreaterEqual(info["links"], 3)
        self.assertGreaterEqual(info["unresolved_links"], 1)


class TestSemanticLayer(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "research"
        self._saved = C.RESEARCH_DIR
        C.RESEARCH_DIR = self.root
        fixture(self.root, "hypotheses/H-0001-q.md", "H-0001", "hypothesis",
                "# H-0001\n\n## Statement\nQuiescence stand-pat delta pruning reduces "
                "the node count at tactical leaves.\n")
        fixture(self.root, "hypotheses/H-0002-c.md", "H-0002", "hypothesis",
                "# H-0002\n\n## Statement\nCopy-make beats make-unmake for alpha-beta "
                "search at depth ten.\n")
        fixture(self.root, "hypotheses/H-0003-p.md", "H-0003", "hypothesis",
                "# H-0003\n\n## Statement\nPEXT bitboards raise perft nodes per second "
                "over ray stepping.\n")
        fixture(self.root, "hypotheses/H-0004-q2.md", "H-0004", "hypothesis",
                "# H-0004\n\n## Statement\nStand-pat and delta pruning in quiescence "
                "reduce node count at tactical leaves.\n")
        self.records, _w = C.load_corpus()

    def tearDown(self):
        C.RESEARCH_DIR = self._saved
        self.tmp.cleanup()

    def test_determinism(self):
        a = TX.EmbedSpace.build(self.records, k=32)
        b = TX.EmbedSpace.build(self.records, k=32)
        self.assertEqual(a.fingerprint, b.fingerprint)
        self.assertEqual(a.vecs, b.vecs)

    def test_related_doc_ranks_above_unrelated(self):
        space = TX.EmbedSpace.build(self.records, k=64)
        key = next(k for k, r in self.records.items() if r.id == "H-0001")
        ranked = dict(space.similar(key, limit=4))
        same_idea = next(k for k, r in self.records.items() if r.id == "H-0004")
        unrelated = next(k for k, r in self.records.items() if r.id == "H-0003")
        self.assertGreater(ranked[same_idea], ranked[unrelated],
                           "same-vocabulary record must be closer than an unrelated one")

    def test_query_folding_is_unit_and_ranks_the_owner(self):
        space = TX.EmbedSpace.build(self.records, k=64)
        tf = TX.doc_terms(next(r for r in self.records.values() if r.id == "H-0003"))
        df: dict = {}
        for r in self.records.values():
            for t in TX.doc_terms(r):
                df[t] = df.get(t, 0) + 1
        qv = space.vector_for_terms(tf, df, len(self.records))
        norm = sum(x * x for x in qv) ** 0.5
        self.assertAlmostEqual(norm, 1.0, places=6)
        scores = RT.semantic_scores(self.records, space, "pext bitboards perft", limit=3)
        self.assertEqual(scores[0][0], next(k for k, r in self.records.items()
                                            if r.id == "H-0003"))

    def test_bm25_prefers_exact_terms_and_is_deterministic(self):
        a = RT.bm25_scores(self.records, "make-unmake alpha-beta")
        b = RT.bm25_scores(self.records, "make-unmake alpha-beta")
        self.assertEqual(a, b)
        self.assertEqual(self.records[a[0][0]].id, "H-0002")

    def test_search_fuses_and_reports_via(self):
        space = TX.EmbedSpace.build(self.records, k=64)
        out = RT.search(self.records, "quiescence delta pruning", space, limit=3)
        self.assertTrue(out["hits"])
        self.assertIn("via", out["hits"][0])


class TestClaimsAndContradictions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "research"
        self._saved = C.RESEARCH_DIR
        C.RESEARCH_DIR = self.root

    def tearDown(self):
        C.RESEARCH_DIR = self._saved
        self.tmp.cleanup()

    def load(self):
        return C.load_corpus()[0]

    def test_opposite_directions_collide(self):
        fixture(self.root, "claims/CLM-0001-a.md", "CLM-0001", "claim",
                "# CLM-0001\n", domain="search", parameter="quiescence-nodes",
                direction="lower", scope="[phase-2]")
        fixture(self.root, "claims/CLM-0002-b.md", "CLM-0002", "claim",
                "# CLM-0002\n", domain="search", parameter="quiescence-nodes",
                direction="higher", scope="[phase-2]")
        out = CL.contradiction_candidates(self.load())
        self.assertEqual(len(out), 1)
        self.assertEqual((out[0]["a"], out[0]["b"]), ("CLM-0001", "CLM-0002"))
        self.assertIn("resolve", out[0])

    def test_unknown_fields_never_collide(self):
        fixture(self.root, "claims/CLM-0003-a.md", "CLM-0003", "claim", "# CLM-0003\n",
                direction="lower")
        fixture(self.root, "claims/CLM-0004-b.md", "CLM-0004", "claim", "# CLM-0004\n",
                direction="higher")
        self.assertEqual(CL.contradiction_candidates(self.load()), [])

    def test_disjoint_scope_never_collides(self):
        fixture(self.root, "claims/CLM-0005-a.md", "CLM-0005", "claim", "# CLM-0005\n",
                domain="search", parameter="nodes", direction="lower", scope="[phase-2]")
        fixture(self.root, "claims/CLM-0006-b.md", "CLM-0006", "claim", "# CLM-0006\n",
                domain="search", parameter="nodes", direction="higher",
                scope="[training]")
        self.assertEqual(CL.contradiction_candidates(self.load()), [])

    def test_declared_contradiction_surfaces_once(self):
        fixture(self.root, "hypotheses/H-0001-a.md", "H-0001", "hypothesis",
                "# H-0001\n", contradicts="[H-0002]")
        fixture(self.root, "hypotheses/H-0002-b.md", "H-0002", "hypothesis",
                "# H-0002\n", contradicts="[H-0001]")
        out = CL.contradiction_candidates(self.load())
        self.assertEqual(len([c for c in out if c["kind"] == "declared"]), 1)

    def test_duplicates_by_same_parameter_and_polarity(self):
        fixture(self.root, "claims/CLM-0007-a.md", "CLM-0007", "claim", "# CLM-0007\n",
                domain="hardware", parameter="pext-magic-nps", direction="higher")
        fixture(self.root, "claims/CLM-0008-b.md", "CLM-0008", "claim", "# CLM-0008\n",
                domain="hardware", parameter="pext-magic-nps", direction="higher")
        out = CL.duplicate_claims(self.load())
        self.assertTrue(any(p["a"] == "CLM-0007" and p["b"] == "CLM-0008" for p in out))


class TestTriggersPrioritiesQuestions(unittest.TestCase):
    def test_trigger_ops(self):
        m = {"perft_nps": 47000000, "search": {"pvs_tt_complete": True}}
        self.assertTrue(PR.eval_trigger("nps_ge 40000000", m)["met"])
        self.assertFalse(PR.eval_trigger("nps_ge 60000000", m)["met"])
        self.assertTrue(PR.eval_trigger("nps_le 50000000", m)["met"])
        self.assertTrue(PR.eval_trigger("has search.pvs_tt_complete", m)["met"])
        self.assertTrue(PR.eval_trigger("not search.aspiration", m)["met"])
        self.assertTrue(PR.eval_trigger("after 2020-01-01", m)["met"])
        self.assertIsNone(PR.eval_trigger("nps_ge 1000", {})["met"])
        self.assertIsNone(PR.eval_trigger("garbage", m)["met"])

    def test_revival_rows_sort_due_first(self):
        tmp = tempfile.TemporaryDirectory()
        saved = C.RESEARCH_DIR
        try:
            root = Path(tmp.name) / "research"
            C.RESEARCH_DIR = root
            fixture(root, "failures/F-0001-a.md", "F-0001", "failure",
                    "# F-0001\n", status="RECORDED", result="FAIL: no gain",
                    trigger="nps_ge 10000000", revisit_when="when NPS rises")
            fixture(root, "hypotheses/H-0001-b.md", "H-0001", "hypothesis",
                    "# H-0001\n", status="REJECTED", trigger="nps_ge 9000000000")
            records, _w = C.load_corpus()
            rows = PR.revival_rows(records, {"perft_nps": 47000000})
        finally:
            C.RESEARCH_DIR = saved
            tmp.cleanup()
        self.assertEqual([r["id"] for r in rows], ["F-0001", "H-0001"])
        self.assertTrue(rows[0]["trigger_state"]["met"])
        self.assertFalse(rows[1]["trigger_state"]["met"])

    def test_readiness_and_priority_inputs(self):
        tmp = tempfile.TemporaryDirectory()
        saved = C.RESEARCH_DIR
        try:
            root = Path(tmp.name) / "research"
            C.RESEARCH_DIR = root
            fixture(root, "questions/Q-0001-a.md", "Q-0001", "question",
                    "# Q-0001\n", status="OPEN", depends_on="[E-9999]")
            fixture(root, "questions/Q-0002-b.md", "Q-0002", "question",
                    "# Q-0002\n", status="OPEN")
            fixture(root, "hypotheses/H-0001-c.md", "H-0001", "hypothesis",
                    "# H-0001\n", status="OPEN", impact_elo="60", cost_hours="2")
            records, _w = C.load_corpus()
            qs = {q["id"]: q for q in PR.question_readiness(records)}
            self.assertFalse(qs["Q-0001"]["ready"])
            self.assertTrue(qs["Q-0002"]["ready"])
            pri = {p["id"]: p for p in PR.priority_rows(records)}
            self.assertEqual(pri["H-0001"]["inputs"]["cost_hours"], 2.0)
            self.assertEqual(pri["H-0001"]["inputs"]["impact_elo"], 60.0)
            # info_gain/readiness defaults must be visible in the row, never hidden
            self.assertIn("readiness", pri["H-0001"]["inputs"])
        finally:
            C.RESEARCH_DIR = saved
            tmp.cleanup()


class TestEvidencePreregLadder(unittest.TestCase):
    def test_verdict_group(self):
        self.assertEqual(EV.verdict_group("PASS (harness validation)"), "positive")
        self.assertEqual(EV.verdict_group("FAIL: bar not met"), "negative")
        self.assertEqual(EV.verdict_group("fail"), "negative")   # case-insensitive
        self.assertEqual(EV.verdict_group("INCONCLUSIVE at cap"), "neutral")
        self.assertEqual(EV.verdict_group(""), "unverdicted")

    def test_prereg_fingerprint_ignores_body_outside_sections(self):
        head = ("---\nid: E-0001\ntype: experiment\nstatus: RUNNING\n---\n"
                "## Pre-Registered Decision Rule\nrule text\n"
                "## Power And Sample Size\nn = 800\n"
                "## Sample Validity\narms differ\n")
        tmp = tempfile.TemporaryDirectory()
        saved = C.RESEARCH_DIR
        try:
            root = Path(tmp.name) / "research"
            C.RESEARCH_DIR = root
            write(root / "experiments/E-0001-a.md", head + "## Results\nmeasured\n")
            write(root / "experiments/E-0001-b.md",
                  head + "## Results\ncompletely different prose\n")
            records, _w = C.load_corpus()
            ra = C.by_id(records, "E-0001")
            rb = [r for r in records.values() if r.key.endswith("-b.md")][0]
            self.assertEqual(EV.prereg_fingerprint(ra), EV.prereg_fingerprint(rb))
        finally:
            C.RESEARCH_DIR = saved
            tmp.cleanup()

    def test_prereg_pin_detects_a_moved_rule(self):
        tmp = tempfile.TemporaryDirectory()
        saved = C.RESEARCH_DIR
        try:
            root = Path(tmp.name) / "research"
            C.RESEARCH_DIR = root
            write(root / "experiments/E-0001-x.md",
                  "---\nid: E-0001\ntype: experiment\nstatus: RUNNING\n"
                  "prereg_sha256: deadbeef\nexample: false\ncreated: 2026-09-01\n---\n"
                  "## Pre-Registered Decision Rule\nrule v2\n")
            records, _w = C.load_corpus()
            st = EV.prereg_state(C.by_id(records, "E-0001"))
            self.assertTrue(st["moved"])
            self.assertIn("MOVED", st["note"])
        finally:
            C.RESEARCH_DIR = saved
            tmp.cleanup()


class TestAgentTables(unittest.TestCase):
    def test_wilson_bounds(self):
        self.assertEqual(AG.wilson(0.0, 0), (0.0, 1.0))
        lo, hi = AG.wilson(0.5, 100)
        self.assertLess(lo, 0.5)
        self.assertGreater(hi, 0.5)
        self.assertLess(hi - lo, 0.25)

    def test_calibration_and_finding_precision(self):
        tmp = tempfile.TemporaryDirectory()
        saved = C.RESEARCH_DIR
        try:
            root = Path(tmp.name) / "research"
            C.RESEARCH_DIR = root
            fixture(root, "hypotheses/H-0001-a.md", "H-0001", "hypothesis",
                    "# H-0001\n", status="SUPPORTED", confidence="0.9",
                    owner="researcher-architect")
            fixture(root, "hypotheses/H-0002-b.md", "H-0002", "hypothesis",
                    "# H-0002\n", status="REJECTED", confidence="0.8",
                    owner="researcher-architect")
            fixture(root, "findings/FND-0001-c.md", "FND-0001", "finding",
                    "# FND-0001\n", status="RESOLVED", severity="major",
                    raised_by="adversarial-reviewer")
            fixture(root, "findings/FND-0002-d.md", "FND-0002", "finding",
                    "# FND-0002\n", status="WITHDRAWN", severity="minor",
                    raised_by="adversarial-reviewer")
            records, _w = C.load_corpus()
            cal = AG.calibration(records)
            self.assertEqual(cal["researcher-architect"]["hit_rate"], 0.5)
            self.assertEqual(cal["researcher-architect"]["n_supported"], 1)
            fp = AG.finding_precision(records)
            self.assertEqual(fp["adversarial-reviewer"]["precision"], 0.5)
        finally:
            C.RESEARCH_DIR = saved
            tmp.cleanup()

    def test_blind_protocol_shape(self):
        out = AG.blind_protocol("move ordering", ["a", "b"], "which order?")
        self.assertEqual(out["protocol"], "blind-independent-then-reveal")
        self.assertEqual(len(out["phase_1_assignments"]), 2)
        self.assertIn("do_not_read_yet", out["phase_1_sealed_brief"])

    def test_handoff_reports_missing_context(self):
        tmp = tempfile.TemporaryDirectory()
        saved = C.RESEARCH_DIR
        try:
            root = Path(tmp.name) / "research"
            C.RESEARCH_DIR = root
            fixture(root, "hypotheses/H-0001-a.md", "H-0001", "hypothesis",
                    "# H-0001\n")
            records, _w = C.load_corpus()
            out = AG.handoff_new(records, "a", "b", "do it", ["run x"],
                                 ["H-0001", "H-9999"])
            self.assertEqual(out["missing_context"], ["H-9999"])
        finally:
            C.RESEARCH_DIR = saved
            tmp.cleanup()


class TestMetaAndCode(unittest.TestCase):
    def test_process_metrics_are_arithmetic(self):
        tmp = tempfile.TemporaryDirectory()
        saved = C.RESEARCH_DIR
        try:
            root = Path(tmp.name) / "research"
            C.RESEARCH_DIR = root
            fixture(root, "experiments/E-0001-a.md", "E-0001", "experiment",
                    "# E-0001\n" + ("x " * 100))
            fixture(root, "reviews/R-0001-b.md", "R-0001", "review",
                    "# R-0001\n\n## Critique of the seam repair\n" + ("y " * 100))
            records, _w = C.load_corpus()
            m = MT.process_metrics(records, commits=[])
            self.assertEqual(m["records"], 2)
            self.assertAlmostEqual(
                m["experiment_share"],
                records["experiments/E-0001-a.md"].size / m["record_bytes"],
                delta=1e-4)
            self.assertGreater(m["process_overhead_share"], 0.0)
        finally:
            C.RESEARCH_DIR = saved
            tmp.cleanup()

    def test_pathology_report_names_fixes(self):
        tmp = tempfile.TemporaryDirectory()
        saved = C.RESEARCH_DIR
        try:
            root = Path(tmp.name) / "research"
            C.RESEARCH_DIR = root
            fixture(root, "experiments/E-0001-big.md", "E-0001", "experiment",
                    "# E-0001\n\nsee L1376\n\n" + ("word " * 13000))
            records, _w = C.load_corpus()
            lint_out = C.lint(records, [], [])
            rows = MT.pathology_report(records, lint_out, lambda: [])
            names = {r["pathology"] for r in rows}
            self.assertIn("giant-records", names)
            self.assertIn("line-number-pointers", names)
            self.assertTrue(all("fix" in r for r in rows))
        finally:
            C.RESEARCH_DIR = saved
            tmp.cleanup()

    def test_code_symbol_index(self):
        tmp = tempfile.TemporaryDirectory()
        saved_root = C.REPO_ROOT
        try:
            root = Path(tmp.name)
            (root / "src").mkdir(parents=True)
            (root / "src" / "s.cpp").write_text(
                "namespace kana {\nstruct Board { int x; };\n"
                "int quiescence_depth(Board& b) { return 1; }\n"
                "static constexpr int MATE_VALUE = 1000;\n}\n", encoding="utf-8")
            C.REPO_ROOT = root
            idx = CD.symbol_index()
            self.assertIn("quiescence_depth", idx)
            self.assertIn("kana::quiescence_depth", idx)
            self.assertIn("Board", idx)
            self.assertEqual(idx["quiescence_depth"][0]["file"], "src/s.cpp")
        finally:
            C.REPO_ROOT = saved_root
            tmp.cleanup()


class TestFreshnessAndNovelty(unittest.TestCase):
    """freshness_rows / novelty_candidates — the advisory aging + novelty surfaces
    added with the freshness/novelty commands (imem 2.1.0). All deterministic."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "research"
        self._saved = C.RESEARCH_DIR
        C.RESEARCH_DIR = self.root

    def tearDown(self):
        C.RESEARCH_DIR = self._saved
        self.tmp.cleanup()

    def load(self):
        return C.load_corpus()[0]

    def test_freshness_flags_stale_live_records_only(self):
        from datetime import date
        fixture(self.root, "hypotheses/H-0001-stale.md", "H-0001", "hypothesis",
                "# H-0001\n", status="OPEN", last_updated="2026-01-01")
        fixture(self.root, "hypotheses/H-0002-closed.md", "H-0002", "hypothesis",
                "# H-0002\n", status="SUPPORTED", created="2026-01-01")
        fixture(self.root, "findings/FND-0001-a.md", "FND-0001", "finding",
                "# FND-0001\n", status="OPEN", created="2026-01-01")
        fixture(self.root, "findings/FND-0002-r.md", "FND-0002", "finding",
                "# FND-0002\n", status="RESOLVED", created="2026-01-01")
        rows = MT.freshness_rows(self.load(), today=date(2026, 3, 1))
        ids = [r["id"] for r in rows]
        self.assertIn("H-0001", ids)
        self.assertIn("FND-0001", ids)
        self.assertNotIn("H-0002", ids)   # terminal status is history, not staleness
        self.assertNotIn("FND-0002", ids)
        for r in rows:
            self.assertIn("why", r)
            self.assertIn("window_days", r)

    def test_freshness_policy_override_changes_the_window(self):
        from datetime import date
        fixture(self.root, "questions/Q-0001-a.md", "Q-0001", "question",
                "# Q-0001\n", status="OPEN", last_updated="2026-02-20")
        recs = self.load()
        short = {k: 7 for k in MT.FRESHNESS_POLICY_DAYS}
        long_ = {k: 3650 for k in MT.FRESHNESS_POLICY_DAYS}
        self.assertTrue(MT.freshness_rows(recs, today=date(2026, 3, 1), policy=short))
        self.assertFalse(MT.freshness_rows(recs, today=date(2026, 3, 1), policy=long_))

    def test_freshness_never_errors_without_dates(self):
        fixture(self.root, "hypotheses/H-0007-nodate.md", "H-0007", "hypothesis",
                "# H-0007\n", status="OPEN")  # no last_updated/created at all
        recs = self.load()
        # must not raise; date-less records are skipped silently-advisory
        out = MT.freshness_report(recs)
        self.assertIn("advisory", out)

    def test_novelty_finds_a_lexical_near_duplicate(self):
        fixture(self.root, "claims/CLM-0001-a.md", "CLM-0001", "claim", "# CLM-0001\n",
                domain="search",
                statement="quiescence delta pruning bounds the leaf search gain")
        recs = self.load()
        rows = CL.novelty_candidates(
            recs, "delta pruning in quiescence bounds the leaf gain", embed=None)
        exact = [r for r in rows if r["id"] == "CLM-0001"]
        self.assertTrue(exact, "token-identical near-paraphrase must surface")
        self.assertTrue(any("lexical" in b for b in exact[0]["basis"]))

    def test_novelty_report_resolves_ids_and_text(self):
        fixture(self.root, "claims/CLM-0009-t.md", "CLM-0009", "claim", "# CLM-0009\n",
                domain="evaluation",
                statement="tempo contributes ~11 Elo at this corpus")
        recs = self.load()
        by_id = CL.novelty_report(recs, "CLM-0009", embed=None)
        self.assertEqual(by_id["resolved_record"], "CLM-0009")
        self.assertEqual(by_id["candidates"], [])  # self excluded, nothing else exists
        by_text = CL.novelty_report(recs, "a completely unrelated proposal about "
                                          "zucchini", embed=None)
        self.assertIsNone(by_text["resolved_record"])
        self.assertIn("advisory", by_text)


class TestRealCorpusInvariants(unittest.TestCase):
    """Structural promises the live store must keep. Count-based assertions are
    deliberately avoided: the corpus grows every session."""

    @classmethod
    def setUpClass(cls):
        cls.records, cls.warnings = C.load_corpus()

    def test_no_duplicate_record_ids(self):
        seen = {}
        for rec in self.records.values():
            if rec.type in ("report", "doc"):
                continue
            seen.setdefault(rec.id, []).append(rec.key)
        dupes = {k: v for k, v in seen.items() if len(v) > 1}
        self.assertEqual(dupes, {}, f"duplicate record ids: {dupes}")

    def test_key_records_have_no_dangling_declared_links(self):
        for rid in ("E-0013", "E-0011", "E-0012", "E-0010"):
            rec = C.by_id(self.records, rid)
            if rec is None:
                continue
            for _rel, dst, anchor, fld in rec.links_fm:
                self.assertNotEqual(C.link_resolves(self.records, dst, anchor), "no",
                                    f"{rid}.{fld} -> {dst} does not resolve")

    def test_e0013_has_anchorable_blocks(self):
        rec = C.by_id(self.records, "E-0013")
        if rec is None:
            self.skipTest("E-0013 absent")
        self.assertTrue({b.slug for b in rec.blocks})

    def test_status_and_inline_link_problems_are_hard_errors(self):
        findings = C.records_of_type(self.records, "finding")
        out = C.lint(self.records, findings, CL.live_claims(self.records),
                     self.warnings)
        hard = [p for p in out["problems"] if p["area"] in ("status", "inline-link")]
        self.assertEqual(hard, [])

    def test_engines_run_on_the_live_store(self):
        self.assertIsInstance(CL.contradiction_candidates(self.records), list)
        self.assertIsInstance(PR.revival_rows(self.records, {}), list)
        self.assertIsInstance(PR.priority_rows(self.records), list)

    def test_version_mentions_dec_0012(self):
        import imem
        self.assertIn("DEC-0012", imem.VERSION)


if __name__ == "__main__":
    unittest.main(verbosity=2)

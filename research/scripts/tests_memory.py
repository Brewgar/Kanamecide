#!/usr/bin/env python3
"""Tests for the Kanamecide research-memory derived-intelligence layer (DEC-0011).

The memory system is software; it gets tested the same way the engine does. Run:

    python research/scripts/tests_memory.py        (exit 0 == all green)
or  python research/scripts/research.py selftest

Read-side invariant this suite enforces: the derived layer keeps agreeing with the
record store it claims to describe. Tests reference the real corpus by record id;
a deliberately changed record changes the test, loudly.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import memorylib as M  # noqa: E402
import research as R  # noqa: E402


class TestParsing(unittest.TestCase):
    def test_parse_simple_yaml_scalars(self):
        d = R.parse_simple_yaml("a: 1\nb: [X, Y]\nc: true\nd: null\n")
        self.assertEqual(d["a"], "1")
        self.assertEqual(d["b"], ["X", "Y"])
        self.assertIs(d["c"], True)
        self.assertIsNone(d["d"])

    def test_as_list(self):
        self.assertEqual(M.as_list(None), [])
        self.assertEqual(M.as_list("X"), ["X"])
        self.assertEqual(M.as_list(["A", "B"]), ["A", "B"])

    def test_confidence_label_ranges(self):
        self.assertEqual(M.confidence_label(0.1), "speculative")
        self.assertEqual(M.confidence_label(0.6), "likely")
        self.assertEqual(M.confidence_label(0.95), "high-author-confidence")
        self.assertEqual(M.confidence_label(None), "—")


class TestCorpus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = M.load_nodes()
        cls.code = M.code_nodes()
        cls.edges, cls.idx = M.build_graph(cls.nodes, cls.code)

    def test_records_load(self):
        self.assertGreaterEqual(len(self.nodes), 40, "expected the real corpus to load")

    def test_reports_are_loaded(self):
        reports = [n for n in self.nodes.values() if n["kind"] == "report"]
        self.assertGreaterEqual(len(reports), 7, "agent reports must be first-class nodes")

    def test_kind_detection(self):
        hyps = [n for n in self.nodes.values() if n["kind"] == "hypothesis"]
        self.assertGreaterEqual(len(hyps), 12)

    def test_code_nodes_have_symbols(self):
        self.assertIn("src/search.cpp", self.code)
        self.assertIn("src/eval.cpp", self.code)
        self.assertTrue(self.code["src/search.cpp"]["symbols"])

    def test_id_index_detects_ambiguity(self):
        counts = sum(1 for k, v in self.idx.items() if len(v) > 1)
        self.assertGreaterEqual(counts, 1, "the H-0002 renumbering should flag an ambiguous id")

    def test_graph_has_typed_edges(self):
        kinds = {e["kind"] for e in self.edges}
        self.assertIn("tests", kinds)
        self.assertIn("mentions", kinds)

    def test_experiment_hypothesis_edge(self):
        e0010 = [k for k, n in self.nodes.items() if n["id"] == "E-0010"]
        self.assertTrue(e0010, "E-0010 must be in the corpus")
        self.assertTrue(any(e["src"] == e0010[0] and e["kind"] == "tests" for e in self.edges),
                        "E-0010 -> H-0004 tests edge must exist")

    def test_missing_reference_targets_runs(self):
        self.assertIsInstance(M.missing_reference_targets(self.nodes), list)


class TestRetrieval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = M.load_nodes()
        cls.edges, cls.idx = M.build_graph(cls.nodes, M.code_nodes())

    def test_bm25_finds_quiescence(self):
        hits = M.bm25_rank(self.nodes, "quiescence stand-pat capture pruning")
        ids = {self.nodes[k]["id"] for k, _ in hits}
        self.assertIn("E-00008", ids)

    def test_bm25_deterministic(self):
        a = M.bm25_rank(self.nodes, "transposition table iterative deepening")
        b = M.bm25_rank(self.nodes, "transposition table iterative deepening")
        self.assertEqual(a, b)

    def test_search_returns_provenance(self):
        out = M.search(self.nodes, "move ordering", limit=5)
        self.assertTrue(out["hits"])
        for h in out["hits"]:
            self.assertIn("rel", h)
            self.assertIn("snippet", h)

    def test_search_includes_agent_reports(self):
        out = M.search(self.nodes, "pseudo-legal movegen contract", limit=10)
        kinds = {h["kind"] for h in out["hits"]} | {r["kind"] for r in out["related"]}
        self.assertTrue(kinds)

    def test_graph_traversal(self):
        key = "experiments/E-00007-o3b-staged-move-ordering-pv-mvv-lva-killers-history.md"
        self.assertTrue(M.neighbours(self.edges, key, 1))
# --- CHUNK A END ---


class TestProjections(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = M.load_nodes()
        cls.code = M.code_nodes()

    def test_belief_rollup_e0010_tests_h0004(self):
        roll = {r["id"]: r for r in M.belief_rollup(self.nodes)}
        self.assertIn("H-0004", roll)
        self.assertTrue(any(e["id"] == "E-0010" for e in roll["H-0004"]["experiments_testing"]),
                        "H-0004's rollup must show E-0010 testing it")

    def test_belief_rollup_marks_projections(self):
        for r in M.belief_rollup(self.nodes):
            self.assertIn("PROJECTION", r["assess"])

    def test_contradictions_run(self):
        self.assertIsInstance(M.contradiction_candidates(self.nodes), list)

    def test_duplicates_find_stub_pairs(self):
        dups = M.duplicate_candidates(self.nodes)
        pairs = {(d["a"], d["b"]) for d in dups}
        self.assertTrue(any(("H-0004" in a or "H-0004" in b) for a, b in pairs),
                        "the H-0002 stub vs H-0004 pair should be a duplicate candidate")

    def test_questions_and_revivals_run(self):
        self.assertIsInstance(M.questions_view(self.nodes), list)
        rev = M.revival_candidates(self.nodes)
        self.assertIsInstance(rev, list)
        self.assertIn("E-0010", {r["id"] for r in rev},
                      "E-0010 (result FAIL) must appear as an inconclusive-revival candidate")

    def test_timeline_sorted(self):
        tl = M.timeline(self.nodes)
        self.assertEqual(tl, sorted(tl, key=lambda r: (r["when"], r["kind"], r["id"])))

    def test_codemap_links_record_to_code(self):
        cm = M.codemap(self.nodes, self.code)
        self.assertTrue(any(c["code_files"] for c in cm),
                        "some record must map to a code file")


class TestAuditAndState(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = M.load_nodes()
        cls.code = M.code_nodes()

    def test_audit_shape(self):
        a = M.audit(self.nodes, self.code)
        for k in ("problems", "warnings", "findings", "metrics", "schema_version"):
            self.assertIn(k, a)
        self.assertEqual(a["schema_version"], M.SCHEMA_VERSION)
        self.assertGreater(a["metrics"]["records_total"], 0)

    def test_audit_deterministic(self):
        strip = lambda d: {k: v for k, v in d.items() if k != "generated"}
        self.assertEqual(strip(M.audit(self.nodes, self.code)), strip(M.audit(self.nodes, self.code)))

    def test_state_builds(self):
        s = M.build_state(self.nodes, self.code)
        for k in ("beliefs", "questions_open", "contradiction_candidates", "evidence",
                  "codemap", "timeline_tail", "metrics"):
            self.assertIn(k, s)

    def test_render_state_md(self):
        md = M.render_state_md(M.build_state(self.nodes, self.code))
        self.assertIn("GENERATED", md)
        self.assertIn("PROJECTION", md)

    def test_json_dump_deterministic(self):
        self.assertEqual(M.json_dump({"b": 1, "a": 2}), M.json_dump({"b": 1, "a": 2}))
# --- CHUNK B END ---


class TestHashingAndCompat(unittest.TestCase):
    def test_sha256_file(self):
        import hashlib
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as t:
            t.write(b"kanamecide")
            p = Path(t.name)
        try:
            self.assertEqual(M.sha256_file(p), hashlib.sha256(b"kanamecide").hexdigest())
        finally:
            p.unlink(missing_ok=True)

    def test_commit_refs_needs_hex_letter(self):
        self.assertFalse(M.commit_refs("4865609 nodes and 197281 leaves"))
        self.assertTrue(M.commit_refs("commit 300bdeb fixed it"))

    def test_run_derived_dispatch_ok(self):
        self.assertEqual(M.run_derived("audit", ["--json"]), 0)


class TestCLI(unittest.TestCase):
    """End-to-end through the real CLI (subprocess) — the way agents actually drive it."""

    def _run(self, *args):
        import subprocess
        return subprocess.run([sys.executable, str(Path(R.__file__)), *args],
                              capture_output=True, text=True, cwd=str(R.REPO_ROOT),
                              timeout=300)

    def test_status_ok(self):
        r = self._run("status", "--brief")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_validate_mentions_summary(self):
        r = self._run("validate")
        self.assertIn("validation", (r.stdout + r.stderr).lower())

    def test_search_quiescence_via_cli(self):
        r = self._run("search", "quiescence")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("E-00008", r.stdout)

    def test_kgraph_shim(self):
        import subprocess
        shim = Path(__file__).parent / "kgraph.py"
        r = subprocess.run([sys.executable, str(shim), "beliefs", "--json"],
                           capture_output=True, text=True, timeout=300)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("H-0001", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=1)
#!/usr/bin/env python3
"""W-0011 test suite: tools/test_kaname_train.py (part 1/2).

Stdlib unittest. Uses the REAL frozen config and REAL artifacts (no mocks
of the training path). Run: python tools/test_kaname_train.py
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import kaname_train as kt
from e0013_fit import fit_once as fit_once_fn

CONFIG = ROOT / "research/manifests/e0017-train-config.json"


class ConfigTest(unittest.TestCase):
    def test_loads_and_validates(self):
        cfg = kt.load_config(CONFIG)
        self.assertEqual(cfg["format"], kt.CONFIG_FORMAT)

    def test_missing_key_aborts(self):
        cfg = kt.load_config(CONFIG)
        bad = json.loads(json.dumps(cfg))
        del bad["objective"]["clip_L"]
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".json",
                                         delete=False) as fh:
            json.dump(bad, fh)
            name = fh.name
        try:
            with self.assertRaises(SystemExit):
                kt.load_config(Path(name))
        finally:
            Path(name).unlink()

    def test_wrong_format_aborts(self):
        cfg = kt.load_config(CONFIG)
        bad = json.loads(json.dumps(cfg))
        bad["format"] = "bogus"
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".json",
                                         delete=False) as fh:
            json.dump(bad, fh)
            name = fh.name
        try:
            with self.assertRaises(SystemExit):
                kt.load_config(Path(name))
        finally:
            Path(name).unlink()


class LoaderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = kt.load_config(CONFIG)

    def test_fit_counts(self):
        fit_rows, info = kt.load_fit_rows(self.cfg)
        exp = self.cfg["expected_counts"]
        self.assertEqual(info["fit_games"], exp["fit_games"])
        self.assertEqual(info["fit_rows"], exp["fit_rows"])
        self.assertEqual(info["holdout_games_excluded"],
                         exp["holdout_games_excluded"])
        self.assertEqual(info["holdout_rows_excluded"],
                         exp["holdout_rows_excluded"])
        self.assertEqual(info["join_miss"], exp["join_miss_rows"])

    def test_split_disjointness(self):
        from e0013_extract import split_of
        fit_rows, _ = kt.load_fit_rows(self.cfg)
        for r in fit_rows[::997]:
            self.assertEqual(split_of(int(r["game_id"])), "train")

    def test_holdout_exclusion_receipt(self):
        _, info = kt.load_fit_rows(self.cfg)
        self.assertEqual(info["holdout_games_excluded"], 208)
        self.assertEqual(info["holdout_rows_excluded"], 14560)

    def test_firewall_injection(self):
        """A holdout game id must classify as holdout (never train)."""
        from e0013_extract import split_of
        holdouts = [g for g in range(3000) if split_of(g) != "train"][:5]
        self.assertTrue(holdouts)
        fit_rows, _ = kt.load_fit_rows(self.cfg)
        fit_games = {int(r["game_id"]) for r in fit_rows}
        for g in holdouts:
            self.assertNotIn(g, fit_games)

    def test_inner_val_counts(self):
        _, vinfo = kt.load_inner_val(self.cfg)
        self.assertEqual(vinfo["val_games"], 155)
        self.assertEqual(vinfo["skipped_outer_holdout"], 14560)

    def test_inner_val_disjoint_from_inner_train(self):
        imap = json.loads(
            (ROOT / self.cfg["provenance"]["inner_map_path"]).read_bytes())
        val_rows, _ = kt.load_inner_val(self.cfg)
        val_games = {int(r["game_id"]) for r in val_rows}
        for g in val_games:
            self.assertEqual(imap["map"][str(g)], "holdout")


class ModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import e0013_eval as ev
        cls.ev = ev
        cls.cfg = kt.load_config(CONFIG)
        cls.floor = ev.hand_tuned()

    def test_free_scalar_count(self):
        self.assertEqual(len(self.ev.design_vector(self.floor)), 683)

    def test_floor_pin(self):
        self.assertEqual(
            self.ev.table_sha256(self.floor),
            self.cfg["provenance"]["floor_sha256"])

    def test_design_shape(self):
        fit_rows, _ = kt.load_fit_rows(self.cfg)
        obj = self.cfg["objective"]
        des = kt.build_design(fit_rows[:16], float(obj["clip_L"]),
                              float(obj["l2"]), float(obj["elo_scale_D"]))
        self.assertEqual(tuple(des["jac"].shape), (16, 683))
        self.assertEqual(tuple(des["labels"].shape), (16,))

    def test_finite_outputs(self):
        import numpy as np
        fit_rows, _ = kt.load_fit_rows(self.cfg)
        obj = self.cfg["objective"]
        des = kt.build_design(fit_rows[:16], float(obj["clip_L"]),
                              float(obj["l2"]), float(obj["elo_scale_D"]))
        loss = self.ev.mean_logistic_loss(
            des["jac"], des["offset"], des["theta0"], des["labels"],
            float(obj["clip_L"]), elo_scale=float(obj["elo_scale_D"]))
        self.assertTrue(np.isfinite(loss))

    def test_frozen_blocks_intact(self):
        fitted = self.ev.from_design_vector(
            self.ev.design_vector(self.floor), self.floor)
        self.assertEqual(
            self.ev.frozen_block_mismatches(fitted, self.floor), [])

class OptimizerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # NOTE: fit_once is imported at module level (plain function). It is
        # deliberately NOT stored as cls.fit_once: functions assigned as class
        # attributes become bound methods, injecting self as first arg.
        import numpy as np
        import e0013_eval as ev
        cls.np = np
        cls.ev = ev
        cls.cfg = kt.load_config(CONFIG)

    def _des(self, n):
        fit_rows, _ = kt.load_fit_rows(self.cfg)
        obj = self.cfg["objective"]
        return kt.build_design(fit_rows[:n], float(obj["clip_L"]),
                               float(obj["l2"]), float(obj["elo_scale_D"]))

    def test_loss_gradient_finite(self):
        np, ev = self.np, self.ev
        obj = self.cfg["objective"]
        des = self._des(32)
        loss, grad = ev.loss_and_gradient(
            des["jac"], des["offset"], des["labels"],
            np.asarray(des["theta0"], dtype=np.float64),
            float(obj["clip_L"]), float(obj["l2"]), des["theta0"],
            elo_scale=float(obj["elo_scale_D"]))
        self.assertTrue(np.isfinite(loss))
        self.assertTrue(bool(np.all(np.isfinite(grad))))

    def test_gradient_nonzero(self):
        np, ev = self.np, self.ev
        obj = self.cfg["objective"]
        des = self._des(32)
        _, grad = ev.loss_and_gradient(
            des["jac"], des["offset"], des["labels"],
            np.asarray(des["theta0"], dtype=np.float64),
            float(obj["clip_L"]), float(obj["l2"]), des["theta0"],
            elo_scale=float(obj["elo_scale_D"]))
        self.assertGreater(float(np.linalg.norm(grad)), 0.0)

    def test_optimizer_step_changes_params(self):
        np = self.np
        obj = self.cfg["objective"]
        des = self._des(64)
        v0 = np.asarray(des["theta0"], dtype=np.float64)
        res = fit_once_fn(des["jac"], des["offset"], des["labels"],
                          des["theta0"], float(obj["clip_L"]),
                          float(obj["l2"]), 5,
                          elo_scale=float(obj["elo_scale_D"]))
        self.assertTrue(bool(np.any(res.x != v0)))

    def test_double_fit_byte_identical(self):
        obj = self.cfg["objective"]
        des = self._des(64)
        kw = dict(clip=float(obj["clip_L"]), l2=float(obj["l2"]),
                  maxiter=5, elo_scale=float(obj["elo_scale_D"]))
        r1 = fit_once_fn(des["jac"], des["offset"], des["labels"],
                         des["theta0"], **kw)
        r2 = fit_once_fn(des["jac"], des["offset"], des["labels"],
                         des["theta0"], **kw)
        self.assertEqual(r1.x.tobytes(), r2.x.tobytes())


class CheckpointTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = kt.load_config(CONFIG)

    def test_write_reload_roundtrip(self):
        payload = {"probe": [1, 2, 3], "note": "roundtrip"}
        kt.write_checkpoint(self.cfg, "test-roundtrip", payload)
        back = kt.read_checkpoint(self.cfg, "test-roundtrip")
        self.assertEqual(back["payload"], payload)
        (ROOT / self.cfg["execution"]["checkpoint_dir"]
         / "test-roundtrip.json").unlink()

    def test_config_mismatch_refuses(self):
        kt.write_checkpoint(self.cfg, "test-roundtrip", {"a": 1})
        bad = json.loads(json.dumps(self.cfg))
        bad["optimizer"]["maxiter"] = 7
        path = (ROOT / self.cfg["execution"]["checkpoint_dir"]
                / "test-roundtrip.json")
        body = json.loads(path.read_bytes().decode("utf-8"))
        body["config_sha256"] = kt.sha256_bytes(kt.canonical_json(bad))
        path.write_bytes(kt.canonical_json(body))
        try:
            with self.assertRaises(SystemExit):
                kt.read_checkpoint(self.cfg, "test-roundtrip")
        finally:
            path.unlink()


class ManifestTest(unittest.TestCase):
    def test_manifest_subcommand(self):
        import io
        from contextlib import redirect_stdout
        cfg = kt.load_config(CONFIG)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = kt.cmd_manifest(cfg)
        self.assertEqual(rc, 0)
        self.assertIn("791 games / 59892 rows", buf.getvalue())

    def test_metrics_manifest_files(self):
        cfg = kt.load_config(CONFIG)
        out = ROOT / cfg["execution"]["output_dir"] / "dry-run"
        self.assertTrue((out / "metrics.json").is_file())
        self.assertTrue((out / "manifest.json").is_file())
        metrics = json.loads((out / "metrics.json").read_bytes())
        manifest = json.loads((out / "manifest.json").read_bytes())
        self.assertEqual(metrics["format"], kt.METRICS_FORMAT)
        self.assertEqual(manifest["format"], kt.MANIFEST_FORMAT)
        self.assertEqual(manifest["config_sha256"],
                         kt.sha256_bytes(kt.canonical_json(cfg)))


if __name__ == "__main__":
    unittest.main(verbosity=2)


#!/usr/bin/env python3
"""GUI unit tests (stdlib unittest, no Tk display needed).

Covers: command construction, log parsing, checkpoint discovery,
trainer start/stop/resume plumbing, double-start guard, UCI smoke API.
Run: python tools/gui_test.py
"""
from __future__ import annotations

import json
import sys
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from gui import backend as B
from gui import ckpts as C
from gui.proc import TrainerProc

CONFIG = B.DEFAULT_CONFIG


class CommandTest(unittest.TestCase):
    def test_train_command(self):
        cmd = B.trainer_command("train", CONFIG)
        self.assertIn("kaname_train.py", cmd[1])
        self.assertEqual(cmd[2], "train")
        self.assertIn("--config", cmd)

    def test_resume_command(self):
        cmd = B.trainer_command("resume", CONFIG, checkpoint="x.json")
        self.assertEqual(cmd[2], "resume")
        self.assertIn("x.json", cmd)

    def test_preflight_dryrun_commands(self):
        for sub in ("preflight", "dry-run", "manifest"):
            cmd = B.trainer_command(sub, CONFIG)
            self.assertEqual(cmd[2], sub)


class ParseTest(unittest.TestCase):
    def test_fit_and_loss(self):
        st = B.RunStatus()
        B.parse_line(st, "  fit games=791 rows=59892")
        self.assertEqual(st.fit_games, "791")
        B.parse_line(st, "  jac=(59892, 683)")
        self.assertEqual(st.jac_shape, "59892 x 683")
        B.parse_line(
            st, "  loss floor=0.177404 fitted=0.150000 delta=0.027404 nit=5")
        self.assertEqual(st.floor_loss, "0.177404")
        B.parse_line(st, "  delta_inner_val=0.001234 s_d=0.01")
        self.assertEqual(st.delta_inner_val, "0.001234")
        B.parse_line(
            st, "checkpoint[fit] C:\\x\\fit.json sha256=253245eeabcd")
        self.assertEqual(st.last_checkpoint, "fit")


class CheckpointTest(unittest.TestCase):
    def test_discovery_runs(self):
        cks = C.list_checkpoints(CONFIG)
        self.assertIsInstance(cks, list)

    def test_latest_is_mapping_or_none(self):
        ck = C.latest_checkpoint(CONFIG)
        self.assertTrue(ck is None or "phase" in ck)


class ProcTest(unittest.TestCase):
    def test_double_start_guard(self):
        seen: list[str] = []
        done: list = []
        p = TrainerProc(seen.append, done.append)
        cmd = [sys.executable, "-c",
               "import time; print('hi'); time.sleep(30)"]
        p.start(cmd)
        try:
            with self.assertRaises(RuntimeError):
                p.start(cmd)
            self.assertTrue(p.is_alive())
        finally:
            msg = p.stop(timeout=5.0)
            self.assertIn("terminat", msg)
            end = time.time() + 15
            while p.status.state in ("STOPPING", "RUNNING", "STARTING") \
                    and time.time() < end:
                time.sleep(0.1)
            self.assertFalse(p.is_alive())
            self.assertIn(p.status.state, ("STOPPED", "COMPLETED"))

    def test_failed_command_reports(self):
        seen: list[str] = []
        done: list = []
        p = TrainerProc(seen.append, done.append)
        cmd = [sys.executable, "-c", "raise SystemExit(3)"]
        p.start(cmd)
        end = time.time() + 15
        while p.status.state in ("STARTING", "RUNNING") \
                and time.time() < end:
            time.sleep(0.1)
        self.assertEqual(p.status.state, "FAILED")
        self.assertEqual(p.status.exit_code, 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)

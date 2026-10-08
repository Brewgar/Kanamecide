#!/usr/bin/env python3
"""KANAMECIDE GUI backend (part 1): status, settings, checkpoints."""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
ROOT = TOOLS.parent

TRAINER = TOOLS / "kaname_train.py"
DEFAULT_CONFIG = ROOT / "research" / "manifests" / "e0017-train-config.json"

STATES = ("IDLE", "STARTING", "RUNNING", "STOPPING", "STOPPED",
          "FAILED", "COMPLETED", "RESUMING")

PHASES = ("design-matrix", "fit", "eval")

SETTINGS_REL = Path(".kanamecide-gui.json")  # user-local, gitignored

ERROR_HINTS = ("ABORT", "Traceback", "FAILED", "mismatch", "missing",
               "refus", "error:")


@dataclass
class RunStatus:
    state: str = "IDLE"
    command: list[str] = field(default_factory=list)
    pid: int | None = None
    exit_code: int | None = None
    started_at: float | None = None
    ended_at: float | None = None
    error_text: str = ""
    user_stop: bool = False
    fit_games: str = ""
    fit_rows: str = ""
    jac_shape: str = ""
    floor_loss: str = ""
    fitted_loss: str = ""
    delta_fit: str = ""
    delta_inner_val: str = ""
    last_checkpoint: str = ""
    last_checkpoint_sha: str = ""

    @property
    def elapsed(self) -> str:
        if not self.started_at:
            return "--"
        end = self.ended_at or time.time()
        s = int(end - self.started_at)
        h, s = divmod(s, 3600)
        m, s = divmod(s, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"


def load_settings() -> dict:
    p = ROOT / SETTINGS_REL
    if p.is_file():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_settings(data: dict) -> None:
    p = ROOT / SETTINGS_REL
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
import sys as _sys
import re as _re


def trainer_command(sub: str, config: Path, checkpoint: str = "") -> list[str]:
    cmd = [_sys.executable, str(TRAINER), sub, "--config", str(config)]
    if sub == "resume":
        cmd += ["--checkpoint", checkpoint]
    return cmd


_PATTERNS = {
    "fit_games": _re.compile(r"fit games=(\d+)\s+rows=(\d+)"),
    "jac": _re.compile(r"jac=\((\d+),\s*(\d+)\)"),
    "loss": _re.compile(
        r"loss floor=([0-9.eE+\-]+)\s+fitted=([0-9.eE+\-]+)"
        r"\s+delta=([0-9.eE+\-]+)"),
    "d_inner": _re.compile(r"delta_inner_val=([0-9.eE+\-]+)"),
    "ckpt": _re.compile(r"checkpoint\[([^\]]+)\].*sha256=([0-9a-f]{8,})"),
}


def parse_line(status: RunStatus, line: str) -> None:
    m = _PATTERNS["fit_games"].search(line)
    if m:
        status.fit_games, status.fit_rows = m.group(1), m.group(2)
    m = _PATTERNS["jac"].search(line)
    if m:
        status.jac_shape = f"{m.group(1)} x {m.group(2)}"
    m = _PATTERNS["loss"].search(line)
    if m:
        status.floor_loss = m.group(1)
        status.fitted_loss = m.group(2)
        status.delta_fit = m.group(3)
    m = _PATTERNS["d_inner"].search(line)
    if m:
        status.delta_inner_val = m.group(1)
    m = _PATTERNS["ckpt"].search(line)
    if m:
        status.last_checkpoint = m.group(1)
        status.last_checkpoint_sha = m.group(2)[:12] + "..."


def checkpoint_dir_for(config: Path) -> Path:
    try:
        cfg = json.loads(config.read_text(encoding="utf-8"))
        return ROOT / cfg["execution"]["checkpoint_dir"]
    except Exception:
        return ROOT / "build" / "e0017" / "checkpoints"


def output_dir_for(config: Path) -> Path:
    try:
        cfg = json.loads(config.read_text(encoding="utf-8"))
        return ROOT / cfg["execution"]["output_dir"]
    except Exception:
        return ROOT / "build" / "e0017"


def config_sha_of(config: Path):
    try:
        import hashlib
        cfg = json.loads(config.read_text(encoding="utf-8"))
        return hashlib.sha256(
            json.dumps(cfg, sort_keys=True,
                       separators=(",", ":")).encode() + b"\n").hexdigest()
    except Exception:
        return None



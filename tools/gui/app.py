#!/usr/bin/env python3
"""KANAMECIDE Training Control GUI (Tkinter, thin controller).

Wraps the canonical trainer tools/kaname_train.py only:
  preflight / dry-run / train / resume / manifest.
Training runs in a background process; the Tk main thread never blocks.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from . import backend as B
from . import ckpts as C
from . import engines as E
from .proc import TrainerProc

try:
    from . import match as M
except Exception:
    M = None  # type: ignore

APP_TITLE = "KANAMECIDE Training Control"


def open_path(path) -> str:
    p = str(path)
    try:
        if os.name == "nt":
            os.startfile(p)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", p])
        else:
            subprocess.Popen(["xdg-open", p])
        return "opened"
    except Exception as exc:
        return f"cannot open: {exc}"


def read_config_summary(config: Path) -> dict:
    try:
        cfg = json.loads(config.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"error": str(exc)}
    try:
        exe = cfg["execution"]
        return {
            "record": str(cfg.get("record", "?")),
            "model": str(cfg["model"].get("family", "?")),
            "free": str(cfg["model"].get("free_scalars", "?")),
            "stage": str(cfg["model"].get("stage", "?")),
            "maxiter": str(cfg["optimizer"].get("maxiter", "?")),
            "seed": str(cfg["optimizer"].get("seed", "?")),
            "device": str(exe.get("device", "?")),
            "precision": str(exe.get("precision", "?")),
            "output": str(exe.get("output_dir", "?")),
            "launch": str(exe.get("launch_command", "?")),
        }
    except Exception as exc:
        return {"error": f"config missing field: {exc}"}

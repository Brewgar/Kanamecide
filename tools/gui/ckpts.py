#!/usr/bin/env python3
"""Checkpoint + run-history + engine-detection helpers for the GUI."""
from __future__ import annotations

import json
import time
from pathlib import Path

from .backend import PHASES, ROOT, checkpoint_dir_for, config_sha_of


def list_checkpoints(config: Path) -> list[dict]:
    d = checkpoint_dir_for(config)
    out: list[dict] = []
    if not d.is_dir():
        return out
    want = config_sha_of(config)
    for phase in PHASES:
        p = d / f"{phase}.json"
        if not p.is_file():
            continue
        try:
            body = json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:
            out.append({"phase": phase, "path": str(p), "ok": False,
                        "detail": f"unreadable: {exc}"})
            continue
        ok = body.get("format") == "kana-e0017-checkpoint-v1"
        match = want is None or body.get("config_sha256") == want
        det = body.get("phase", "")
        if ok and not match:
            det = "config mismatch: resume with the frozen config only"
        out.append({"phase": phase, "path": str(p),
                    "ok": bool(ok and match), "detail": det})
    return out


def latest_checkpoint(config: Path) -> dict | None:
    good = [c for c in list_checkpoints(config) if c.get("ok")]
    if not good:
        return None
    order = {p: i for i, p in enumerate(PHASES)}
    good.sort(key=lambda c: order.get(str(c["phase"]), -1))
    return good[-1]

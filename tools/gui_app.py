#!/usr/bin/env python3
"""Canonical GUI launcher: python tools/gui_app.py"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from gui.mainwin import main

if __name__ == "__main__":
    raise SystemExit(main())

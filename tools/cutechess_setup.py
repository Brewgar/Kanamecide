#!/usr/bin/env python3
"""Cute Chess setup helper (external open-source engine-testing GUI).

Does NOT vendor Cute Chess. It checks for an existing install, prints the
official 1.5.0 download location, and records the chosen path in the
user-local GUI settings (.kanamecide-gui.json, gitignored).

Usage:
  python tools/cutechess_setup.py [--path PATH_TO_CUTECHESS_GUI_OR_CLI]
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SETTINGS = ROOT / ".kanamecide-gui.json"
OFFICIAL = "https://github.com/cutechess/cutechess"
VERSION = "1.5.0 (GPLv3+; some components MIT)"


def load() -> dict:
    if SETTINGS.is_file():
        try:
            return json.loads(SETTINGS.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def main(argv: list[str]) -> int:
    path = ""
    if "--path" in argv:
        path = argv[argv.index("--path") + 1]
    if not path:
        path = shutil.which("cutechess-gui") or shutil.which("cutechess") or ""
    print(f"Cute Chess (external GUI, {VERSION})")
    print(f"Official repo: {OFFICIAL}")
    if path:
        print(f"Found: {path}")
        s = load()
        s["cutechess"] = path
        SETTINGS.write_text(json.dumps(s, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
        print(f"Recorded in {SETTINGS} (user-local, gitignored).")
        return 0
    print("Not found on PATH. Install the official release, then re-run:")
    print("  python tools/cutechess_setup.py --path <cutechess-gui-exe>")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

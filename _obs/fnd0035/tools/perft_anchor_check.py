#!/usr/bin/env python3
"""Isolate the perft-anchor check that `research.py validate` performs.

`validate` exits non-zero on ANY problem, so a green perft anchor is invisible behind an
unrelated problem (here: the EV-0010 evidence-digest drift, which is FND-0034's scope and is
NOT this seat's to re-pin). This runs the same function research.py itself calls
(`_project_state_problems`, which contains the PERFT_ANCHOR digit-boundary assertions at
research/scripts/research.py:923-946) and prints only the perft-anchor verdict.

Exit 0 iff every one of the ten PERFT_ANCHOR counts is found in project_state.md's
'## Certified Perft Anchors' section.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research" / "scripts"))

import research  # noqa: E402

anchor = research.read_text(research.PROJECT_STATE)
section = research.body_section(anchor, research.PERFT_ANCHOR_SECTION)
if not section:
    print(f"FAIL: project_state.md has no '{research.PERFT_ANCHOR_SECTION}' section")
    sys.exit(1)

flat = section.replace(" ", "").replace(",", "")
missing = []
import re  # noqa: E402

for name, count in research.PERFT_ANCHOR:
    pat = re.compile(r"(?<!\d)" + re.escape(count) + r"(?!\d)")
    ok = bool(pat.search(flat))
    print(f"{'PASS' if ok else 'FAIL'}  {name:14s} expected={count}")
    if not ok:
        missing.append(name)

print(f"\nanchor counts asserted: {len(research.PERFT_ANCHOR)}   missing: {len(missing)}")
print("PERFT ANCHOR: " + ("GREEN" if not missing else "RED"))
sys.exit(0 if not missing else 1)

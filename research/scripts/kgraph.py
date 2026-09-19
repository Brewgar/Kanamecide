#!/usr/bin/env python3
"""kgraph.py â€” compatibility shim for the Kanamecide derived-intelligence layer.

This module previously contained an incomplete, accidentally-truncated prototype of
a knowledge-graph/retrieval layer (its argparse main was never delivered and the file
once crashed with an IndentationError). The load-bearing implementation now lives in
`research/scripts/memorylib.py` and is driven by the canonical `research.py` CLI
(see DEC-0011 and research/SCHEMA.md).

This shim keeps the original module name working so any reference to
`python research/scripts/kgraph.py <command>` still functions:

    python research/scripts/kgraph.py search "quiescence move ordering"
    python research/scripts/kgraph.py beliefs --json
    python research/scripts/kgraph.py contradictions
    python research/scripts/kgraph.py audit

Everything here is derived from the Markdown record store; nothing in this file is a
source of truth. See `research/SCHEMA.md` for the data model.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import memorylib as M  # noqa: E402


if __name__ == "__main__":
    sys.exit(M.main())


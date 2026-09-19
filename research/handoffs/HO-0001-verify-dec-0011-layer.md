---
id: HO-0001
type: handoff
from: chief-architect
to: verification-auditor
work_item: W-0007
status: REQUESTED
title: "Independently verify the DEC-0011 derived-intelligence layer"
artifacts: [research/scripts/memorylib.py, research/scripts/kgraph.py, research/scripts/research.py, research/scripts/tests_memory.py, research/SCHEMA.md]
commands: []
acceptance: "selftest OK AND validate OK AND state --write deterministic AND no existing record rewritten/lost"
example: false
created: 2026-09-19
closed: null
---

# HO-0001 — Verify the derived-intelligence layer (W-0007)

> Take this from a zero-history seat (the rotating verification-auditor). Do not accept the
> builder's summary. Re-run everything yourself.

## Request
Bootstrap per `AGENT_MEGAPROMPT.md` §§0-1, then verify DEC-0011's delivery end-to-end.

## Artifacts To Read (paths)
- `research/scripts/memorylib.py`, `research/scripts/research.py`, `research/scripts/kgraph.py`,
  `research/scripts/tests_memory.py`, `research/SCHEMA.md`, this file.

## Commands To Run
```powershell
python research/scripts/research.py selftest            # expect: 35 tests OK, exit 0
python research/scripts/research.py validate            # expect: OK (problems == 0)
python research/scripts/research.py state --write        # writes state.md + state.json
python research/scripts/research.py state --write        # IMMEDIATELY re-run: deterministic (state.json unchanged modulo `generated`)
python research/scripts/research.py search "quiescence stand-pat"   # expect: E-00008 among top hits
python research/scripts/kgraph.py beliefs --json        # compat shim works
```

## Acceptance Criteria (what makes this DONE)
- All commands exit 0 and produce the expected structure.
- No record under `research/` was edited or deleted by the layer (git diff shows 0 touched
  existing records; only new files).
- `state --write` twice produces byte-identical `state.json` after stripping the
  `generated` timestamp.

## Response (receiver, append-only)
- (to be filled)

## Verification (receiver, append-only)
- raw output / exit codes / recomputed hashes:
- verdict: VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE
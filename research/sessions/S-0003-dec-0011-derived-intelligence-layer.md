---
id: S-0003
type: session
agent: chief-architect (Round-5 derived-intelligence build)
round: 5
title: "DEC-0011 derived-intelligence layer: graph, retrieval, beliefs, contradiction/revival detection, state, audit, self-tests"
status: CLOSED
context_budget: "full-project comprehension phase then implementation; all state on disk"
example: false
created: 2026-09-19
closed: 2026-09-19
---

# S-0003 — Chief-architect session (Round 5): the derived-intelligence layer

## Round / Work Items Touched
- W-0007 (the build; status OPEN — verification handed off via HO-0001, never self-marked).

## What I Did (with evidence)
| # | Action | Evidence | Calibration |
|---|---|---|---|
| 1 | Read every project file before designing | full traversal; notes inline | demonstrated |
| 2 | Found & fixed the orphaned, broken kgraph.py | context/_kg_audit.txt logged its IndentationError; replaced with memorylib + shim | demonstrated |
| 3 | Built the derived-intelligence layer (graph/retrieval/beliefs/contradiction/duplicate/revival/questions/codemap/audit/state/hygiene) | `research.py selftest` => 35 tests OK | demonstrated |
| 4 | Extended `validate` with the derived layer's advisory checks; added record kinds question/principle/evidence | `research.py validate` => OK | demonstrated |
| 5 | Registered evidence EV-0001..EV-0010 (incl. the drift-fix on EV-0004 that the drift-check itself caught) | evidence records on disk | demonstrated |
| 6 | Filed DEC-0011, R-0005, W-0007, HO-0001; seeded Q-0001..Q-0008, PR-0001..PR-0004 | records on disk | demonstrated |
| 7 | Regenerated index.md, wrote state.md/state.json | generated on disk | demonstrated |
| 8 | Deleted unlisted scratch `_research_files.txt`; gates now green | `validate` OK | demonstrated |

## Environment facts learned
- `validate` correctly rejected my own DONE-claim on W-0007 ("DONE without evidence" /
  "not independently verified") — the system enforced DEC-0009 on its author. Worth
  recording as the first direct proof the gates work against self-verification.
- The evidence-drift check caught a real false claim: EV-0004 originally pinned the
  E-0002-era binary hash to a path the E-0010 build had since overwritten. The drift
  check fired; I fixed the record to keep the historical hash as provenance only.
- Hash comparisons must be case-insensitive (the same sha256 uppercase/lowercase surfaced
  as a false drift; fixed in memorylib + research.py).

## State Left On Disk
- `research/scripts/memorylib.py`, `research/scripts/research.py` (+CLI extensions),
  `research/scripts/kgraph.py` (shim), `research/scripts/tests_memory.py`.
- `research/{questions,principles,evidence}/`, `research/state.{md,json}`,
  `research/SCHEMA.md`, `research/index.md`.
- `research/decisions/DEC-0011`, `research/reviews/R-0005`, `research/work/W-0007`,
  `research/handoffs/HO-0001`.

## Next Action For The Successor
- The verification-auditor (fresh agent) runs HO-0001: rerun the W-0007 exit_check +
  the two-run determinism test on `state --write`, then move W-0007 to DONE.

## Validation Status
- `python research/scripts/research.py validate` => OK.
- `python research/scripts/research.py selftest` => 35 tests OK.
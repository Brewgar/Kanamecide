---
id: R-IE-O3B
type: report
agent: implementation-engineer
title: "O3b staged move ordering completion report (2026-09-11)"
example: false
created: 2026-09-11
---

# O3b staged move ordering — completion report (2026-09-11)

## What was implemented (src/search.{h,cpp}, src/main.cpp, CMakeLists.txt)

- Four levers, one at a time via compile-time `ORDER_STAGE` (default 4): (1) PV move first —
  root shallow-prior pass; (2) MVV-LVA captures (10*victim − attacker; promotions counted, EP
  handled); (3) killers — 2 slots/ply on quiet beta cutoffs; (4) history heuristic
  `[color][from][to]` bumped by depth², clamped.
- Per-move score in a parallel `ScoredMove` array (the 16-bit `Move` encoding is UNTOUCHED),
  candidates `stable_sort`ed descending. DEC-0008 filter still applied per-move AFTER make_move.
- A `uint64_t` node counter threaded through negamax; `go depth N` now prints
  `info depth N nodes X time T score cp S` before `bestmove`. `go nodes N` parsed (stop hint
  deferred to O3d).
- New CMake `Audit` config = `/O2` WITHOUT `NDEBUG`, no `/DEBUG` (Device Guard blocks /DEBUG exes
  on this box). Asserts are live; node counts are NDEBUG-independent, so Audit is the measurement
  harness. `Release` stays /O2/NDEBUG as mandated.

## Measured (E-00007)

Total nodes over 11 positions (startpos + 5 quiet + 5 tactical) at depth 6:

| Stage | nodes | vs unordered |
|---|---|---|
| 0 unordered | 254,655,158 | baseline |
| 1 +PV | 254,655,158 | 0.0% |
| 2 +MVV-LVA | 40,869,716 | 84.0% |
| 3 +killers | 24,095,495 | 90.5% |
| 4 +history | 22,534,970 | **91.2%** |

Perft 10/10 bit-identical (Release AND Audit). Self-play: 30/30 wins (100%), 30/30 legal.

## Soundness (mandate-required)

Scores bit-identical across ALL five stages on all 11 positions. Best-move string identical on
9/11; tact_b (650) and tact_d (550) differ only where two moves tie at the identical score —
a tie-break artifact of reordering equal-valued moves, not a result change.

## Findings

- **PV-first alone = 0.0%**: expected — the PV move only matters once iterative deepening exists
  (O3d). Recorded as a finding, not a regression; the shallow root seed is correct but inert at
  fixed depth.
- **MVV-LVA is the dominant lever (84%)**; killers add ~6.5pp; history ~0.7pp. No regression.
- **Caught-and-fixed during this milestone**: the O3a H-0012 assert in negamax tested
  `move_to(m) != b.king_sq[us]` where `us` is the *mover* (wrong — fires on every king move) and
  had silently never compiled in NDEBUG builds. The new Audit config surfaced it immediately;
  corrected to `b.king_sq[~us]` (enemy king). This is concrete evidence the Audit config earns
  its keep as a CI gate.

## Environment note

Device Guard / Smart App Control on this machine intermittently blocks *freshly built* unsigned
EXEs (hash-based; Release and Audit both hit it at different times; the earlier working binaries
kept running). Retry is the workaround; this is an environment behavior, not an engine issue.
Documented, not hidden.

## Left for O3c / O3d

O3c quiescence (stand-pat + captures/promotions + delta pruning); O3d TT / iterative deepening /
time control / `stop`-during-search / `go nodes` stop enforcement.

## Date
2026-09-11
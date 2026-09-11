---
id: E-00007
type: experiment
title: O3b staged move ordering (PV, MVV-LVA, killers, history)
status: COMPLETED
result: "PASS: full ordering reduces nodes 91.2% vs O3a unordered (d6, 11 positions); perft bit-identical; 30/30 (100%) vs random; scores identical at every stage"
elo_change: null
hypothesis: "H-0008: move ordering dominates raw NPS for time-to-depth"
priority: high
example: false
created: 2026-09-11
completed: 2026-09-11
tags: [o3b, search, move-ordering, mvv-lva, killers, history, pv]
---

# E-00007 — O3b staged move ordering (PV, MVV-LVA, killers, history)

## Hypothesis
H-0008: staged move ordering (PV-first, MVV-LVA captures, killers, history) cuts nodes to a
fixed depth by a large margin versus the O3a unordered alpha-beta, far exceeding any flat
perft-NPS gain. Ordering is SOUND (never changes the fixed-depth minimax value).

## Baseline
O3a unordered alpha-beta, same `src/`, same positions, same depth (6), node counts measured
with the new node counter in the Audit build (asserts live; node counts are NDEBUG-independent).

## Candidate
Four levers, one at a time (compile-time `ORDER_STAGE` in `src/search.cpp`): 1 PV move first
(root shallow prior); 2 MVV-LVA captures; 3 killers (2 slow/ply); 4 history [color][from][to].

## Difference
A per-move score is computed alongside the 16-bit Move (parallel `ScoredMove`, encoding intact)
and candidates are `stable_sort`ed by score before search. The DEC-0008 filter is applied
per-move AFTER make_move and is never reordered away.

## Hardware
AMD Ryzen 7 9700X, 32 GB DDR5-6000, Windows 11, MSVC 19.51, CMake 4.4.3. Node counts measured
in the `Audit` config (/O2, no /DEBUG; Device Guard blocks /DEBUG exes here).

## Engine Version
Post-O3b HEAD; `src/search.{h,cpp}` rewrite with node counter + ScoredMove; `src/main.cpp` `go`
reports `info depth N nodes X time T score cp S`.

## Network
None.

## Dataset
11 positions at depth 6: startpos + 5 quiet middlegames (italian, italian_early, qgd, kid,
giuoco_2) + 5 tactical (q_out, tact_b, tact_c, tact_d, tact_e). FENs in `measure_ob.py`.

## Test Method
Per stage, rebuild `Audit` with `-DORDER_STAGE=N`, run `measure_ob.py`: send `position` +
`go depth 6`, parse `info` (nodes/time/score) + `bestmove`. Report nodes, time-to-depth, and
effective branching factor BF = nodes^(1/6). Compare node counts and score/bestmove across stages.

## Games / Samples
30 self-play games vs legal-move-uniform random at depth 4 (full ordering): 30/30 wins, 30/30
legal (100%/100%).

## Metrics
Total nodes over 11 positions at depth 6 (sum of per-position counts):

| Stage | Total nodes | vs O3a unordered | BF (geomean) |
|---|---|---|---|
| 0 unordered (O3a) | 254,655,158 | baseline | ~15.6 |
| 1 +PV-first | 254,655,158 | 0.0% | ~15.6 |
| 2 +MVV-LVA | 40,869,716 | 84.0% | ~12.0 |
| 3 +killers | 24,095,495 | 90.5% | ~11.2 |
| 4 +history | 22,534,970 | **91.2%** | ~11.0 |

(Representative per-position: startpos d6 1,119,902 → 299,440 nodes; italian 22.7M → 2.92M;
q_out 51.8M → 2.78M; tact_d 53.8M → 2.55M.)

## Results
See matrix above. Full ordering (a–d) reduces nodes by 91.2% vs the O3a unordered baseline at
depth 6 on the same 11 positions.

## Statistical Analysis
Deterministic node counts (no SPRT). The pre-registered decision rule is applied verbatim:
full ordering reduces nodes ≥30% AND perft bit-identical AND win-rate vs random ≥95%.

## Interpretation
**Decision rule verdict: PASS.**
- nodes −91.2% ≥ 30% → PASS
- perft 10/10 bit-identical (Release AND Audit, asserts live) → PASS
- 30/30 (100%) vs random, 30/30 legal → PASS (≥95% required)
→ **O3c (quiescence) is unblocked.**

Per-lever findings (honest, monotonic attribution):
- PV-first alone = 0.0% node reduction. This is EXPECTED: PV move is only meaningful once
  iterative deepening exists (O3d). The root shallow-prior seed is correct but inert at fixed
  depth. Recorded as a finding, not a regression.
- MVV-LVA captures is the single biggest lever (84%); killers add ~6.5pp more (→90.5%);
  history adds a further ~0.7pp (→91.2%). No stage regressed.

**Soundness (mandate-required):** scores are BIT-IDENTICAL across all five stages on all 11
positions (the minimax value is order-independent, as required). Best-move *string* is identical
on 9/11; it differs on tact_b (650) and tact_d (550) where two moves share the exact same score
— a tie-break artifact of reordering equal-valued moves, not a result change.

## Conclusion
O3b makes the same player's search ~11.3x cheaper per node (91.2% fewer nodes) at fixed depth,
satisfying H-0008 and decisively passing the decision rule. O3c (quiescence) is unblocked.

## Follow-Up
O3c: quiescence (stand-pat + captures/promotions + delta pruning) on top of the ordered search.
The new `Audit` CMake config is now the standard asserts-live build here (Device Guard blocks
/DEBUG exes). Fix WDAC-noted: freshly rebuilt binaries are intermittently blocked by Smart App
Control on this box — retry is the workaround; document rather than hide.
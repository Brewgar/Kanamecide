---
id: H-0011
type: hypothesis
title: Copy-make outperforms make-unmake for alpha-beta at depths >=10 on this hardware
status: OPEN
confidence: 0.55
priority: medium
example: false
created: 2026-09-09
last_updated: 2026-09-09
agents_supporting: [researcher-architect]
agents_opposing: []
tags: [search, performance, make-unmake, copy-make, board-representation]
---

# H-0011 — Copy-make outperforms make-unmake for alpha-beta at depths >=10 on this hardware

## Question
For alpha-beta search at depths >=10 on Ryzen 9700X, does copy-make (copy the board, apply move
to the copy, discard after search) outperform make/unmake (apply move in-place, undo after search)?

## Hypothesis
Plausible (0.55). At shallow depths (<8), make/unmake avoids the allocation/copy overhead and
wins. At deeper depths (>=10), copy-make's simpler control flow (no Undo struct, no conditional
unmake logic) and better cache locality (sequential access pattern) may dominate. The ~312 B
Board copy is small enough to fit in L1 cache; memcpy is highly optimized on Zen 5.

## Why We Think This Might Work
- Make/unmake has a complex undo path (promotion, EP, castling) with branches — hard to predict.
- Copy-make is a flat memcpy + simple apply — easier for branch predictor and prefetcher.
- At deep depths, the search tree is large; the per-node overhead of make/unmake accumulates.
- Modern engines (including Stockfish) use make/unmake, but this is largely historical. Some
  experimental engines report copy-make wins at depth.

## Counterarguments
- Stockfish, Ethereal, and virtually all top engines use make/unmake — the collective experience
  strongly favors it.
- Make/unmake avoids memory allocation and cache pressure from copying.
- The ~312 B Board copy adds up at ~45 Mnps (current perft NPS).
- The crossover depth may be much higher than 10 (depth 15-20+), if it exists at all.

## Agents Supporting
researcher-architect (0.55, plausible — not a strong claim; measurement required).

## Agents Opposing
(implementation-engineer, systems-researcher invited to argue based on cache/branch analysis.)

## Confidence
0.55 (plausible, not likely — this is a speculation worth testing, not a strong belief).

## Proposed Experiment
E-COPYMAKE: Implement both make/unmake and copy-make search paths. For depths 6, 8, 10, 12, 14:
- Measure time-to-depth on startpos and a tactical suite.
- Measure NPS for each approach.
- Report the crossover depth (if any) and the magnitude of the difference.

## Required Metrics
- Time-to-depth (seconds).
- NPS at each depth.
- Cache miss rate (if profiling available).
- Branch misprediction rate (if profiling available).

## Status
OPEN

## Result
(none — requires implementation.)

## Conclusion
(none)
---
id: H-0003
type: hypothesis
title: Classical Alpha-Beta/PVS is the Correct Phase 2 Foundation
status: OPEN
confidence: 0.75
priority: high
example: false
created: 2026-09-09
last_updated: 2026-09-09
agents_supporting: [researcher-architect]
agents_opposing: []
tags: [search, alpha-beta, pvs, architecture, phase-2]
---

# H-0003 — Classical Alpha-Beta/PVS is the Correct Phase 2 Foundation

## Question
Should Phase 2 build a classical alpha-beta/PVS + iterative deepening + TT +
quiescence + ordered-move search (CPU), deferring GPU MCTS/PUCT until a measured
baseline plus a trained evaluator exist?

## Hypothesis
Yes: classical search first yields a measurable playing engine in weeks on one
workstation; GPU MCTS without a net is circular (MCTS needs policy/value, which needs
games, which need a playing engine). Expected signal: plain alpha-beta + MVV-LVA +
killers/history + quiescence + ID with material-only eval reaches depth-12 TTD on
startpos and beats a random mover decisively at fixed nodes.

## Why We Think This Might Work
30+ years of CPU-engine evidence; every top CPU engine uses this backbone; keeps
attribution clean (baseline before PVS+TT delta); unblocks eval/SPRT/self-play work.

## Counterarguments
GPU (RTX 5070 Ti) sits idle in Phase 2; a batched neural approach could leapfrog if
training data were available — but it is not (no pipeline/games/net).

## Agents Supporting
researcher-architect (0.75, likely — literature, not measured here).

## Agents Opposing
(none stated; systems-researcher GPU track respected as Phase 3+ differentiator.)

## Confidence
0.75 (likely).

## Proposed Experiment
O3/E-AB: plain alpha-beta stack + UCI; fixed-node SPRT vs random; time-to-depth table.
Then PVS+TT as a controlled delta (E-0001 design).

## Required Metrics
Legal-game rate, time-to-depth (startpos d12), fixed-node win/draw/loss vs random,
NPS, crash/stall count over 1000 games.

## Status
OPEN

## Result
(none — not yet run; baseline re-run of kana.exe required first.)

## Conclusion
(none)

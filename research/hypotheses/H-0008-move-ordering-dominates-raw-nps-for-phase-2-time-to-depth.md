---
id: H-0008
type: hypothesis
title: Move ordering dominates raw NPS for Phase-2 time-to-depth
status: OPEN
confidence: 0.7
priority: high
example: false
created: 2026-09-09
last_updated: 2026-09-09
agents_supporting: [researcher-architect]
agents_opposing: []
tags: [search, move-ordering, time-to-depth, branching-factor]
---

# H-0008 — Move ordering dominates raw NPS for Phase-2 time-to-depth

## Question
On this engine, once a correct plain alpha-beta exists, does move ordering (PV move first,
then MVV-LVA captures, then killers, then history) reduce nodes/time to a fixed depth by more
than any achievable perft-NPS gain (PEXT/magic sliders, board-copy removal)?

## Hypothesis
Yes (likely, 0.7). Alpha-beta with good ordering approaches an effective branching factor (BF)
near sqrt(b); with the current unordered piece-type generator it degrades toward b = minimax.
Ordering is expected to cut nodes to depth 10-12 by 50-90% versus unordered, far exceeding the
~1.3-2.5x PEXT gain (H-0006) and the ~10% board-copy gain (H-0007). Search strength is roughly
nodes x eval x BF; an ordering gain compounds with depth, whereas an NPS gain is a flat
constant factor.

## Why We Think This Might Work
All strong CPU engines treat move ordering (PV/SEE/killers/history) as the primary search
efficiency tool; alpha-beta's sqrt(b) optimality depends on near-optimal ordering. E-00003
already shows perft NPS ~43-50 Mnps — a fixed-factor NPS improvement is bounded, while ordering
gains scale with search depth.

## Counterarguments
- With a material-only eval the PV may be unstable, weakening history/killer heuristics until a
  real evaluation exists (H-0004).
- If the search were NPS-starved (unlikely at ~45 Mnps), flat perft gains could matter more.
- The levers are not mutually exclusive; both should be measured. This hypothesis only claims
  ordering is dominant for time-to-depth, not that PEXT is worthless.

## Agents Supporting
researcher-architect (0.7, likely — theory + all-engine practice, not measured here).

## Agents Opposing
(none stated.)

## Confidence
0.7 (likely).

## Proposed Experiment
In the O3 search build, add move ordering as controlled deltas on top of plain alpha-beta:
(a) unordered baseline; (b) + MVV-LVA captures; (c) + killers; (d) + history; (e) + PV move.
Report nodes and time to fixed depth (startpos + a tactical suite) at each step.

## Required Metrics
Nodes-to-depth and time-to-depth at each ordering stage; effective branching factor
(BF = nodes^(1/depth)); the ratio of ordering gain vs PEXT gain on identical positions.

## Status
OPEN

## Result
(none)

## Conclusion
(none)
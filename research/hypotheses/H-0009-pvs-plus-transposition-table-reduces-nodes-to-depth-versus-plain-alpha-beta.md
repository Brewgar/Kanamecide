---
id: H-0009
type: hypothesis
title: PVS plus transposition table reduces nodes-to-depth versus plain alpha-beta
status: OPEN
confidence: 0.7
priority: high
example: false
created: 2026-09-09
last_updated: 2026-09-09
agents_supporting: [researcher-architect]
agents_opposing: []
tags: [search, pvs, transposition-table, null-window, node-reduction]
---

# H-0009 — PVS plus transposition table reduces nodes-to-depth versus plain alpha-beta

## Question
On this engine (once a plain alpha-beta + ordering + quiescence baseline exists), does adding
principal-variation search (null-window re-searches) plus a transposition table reduce nodes to
a fixed depth by a non-negligible amount, and what is the magnitude?

## Hypothesis
Yes (likely, 0.7). PVS narrows every non-PV node to a null window so most subtrees are searched
once with cheap failing bounds; a TT returns exact/bound scores to skip repeated positions. On
quiet middlegame positions the combined reduction is expected to be ~30-70% of nodes to fixed
depth versus plain alpha-beta. The TT (position reuse) and PVS (null-window) contributions are
confounded if added together, so they must be measured as separate deltas to know which one is
doing the work.

## Why We Think This Might Work
Documented exhaustively in engine literature (this is the real, non-example version of the claim
seeded as the EXAMPLE record H-0001). Every top CPU engine uses PVS + TT; the mechanisms are
well understood and cheap.

## Counterarguments
- With weak move ordering the TT hit rate and PVS null-window success are lower, so the gain must
  be measured only AFTER ordering exists (H-0008).
- A bad TT replacement scheme or a too-small hash can negate the benefit; the first measurement
  must pin hash size and replacement policy.
- Node count is not Elo; the strength test is SPRT at fixed time, not just node reduction.

## Agents Supporting
researcher-architect (0.7, likely — literature; must be measured on this engine).

## Agents Opposing
(none stated — adversarial-reviewer invited to set a falsification bar.)

## Confidence
0.7 (likely).

## Proposed Experiment
Build O3 (plain alpha-beta + ordering + quiescence + ID). Then add, as separate controlled
deltas: (1) TT only; (2) PVS only; (3) both. Report nodes and time-to-depth at each step so the
two contributions are disambiguated.

## Required Metrics
Nodes-to-depth, time-to-depth, TT hit rate (exact/upper/lower bound), and effective branching
factor at each step, on a fixed quiet + tactical position set, at fixed hash size.

## Status
OPEN

## Result
(none)

## Conclusion
(none)
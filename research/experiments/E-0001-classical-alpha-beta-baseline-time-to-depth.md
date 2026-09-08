---
id: E-0001
type: experiment
title: "Classical alpha-beta baseline (time-to-depth)"
status: PENDING
result: null
elo_change: null
hypothesis: "H-0001"
priority: high
example: true
created: 2026-09-08
completed: null
tags: [search, baseline, time-to-depth]
---

# E-0001 — Classical alpha-beta baseline (time-to-depth)

> ⚠️ **EXAMPLE / MOCK DATA.** Demonstrates the experiment format. All numbers below are
> ILLUSTRATIVE placeholders, NOT real measurements.

## Hypothesis
H-0001

## Baseline
Plain alpha-beta (negamax) with a basic material-only evaluation and no move ordering.

## Candidate
Alpha-beta + PVS + transposition table.

## Difference
Adds null-window PVS and TT probing/store; otherwise identical search logic.

## Hardware
AMD Ryzen 7 9700X (8C/16T), 32 GB DDR5-6000, RTX 5070 Ti (unused here), Windows 11.

## Engine Version
(no search implemented yet — Phase 2)

## Network
None (hand-tuned / eval-less baseline).

## Dataset
(ILLUSTRATIVE) 50 quiet middlegame positions from a standard test suite.

## Test Method
Fixed-depth search to depth 8–12; record nodes and wall-clock seconds.

## Games / Samples
0 (not run)

## Metrics
Nodes-to-depth, time-to-depth.

## Results
(Illustrative only — placeholder: expect ~15–30% fewer nodes; nothing measured.)

## Statistical Analysis
(not performed)

## Interpretation
(not applicable)

## Conclusion
(not executed)

## Follow-Up
Run on the real engine once Phase 2 search exists.
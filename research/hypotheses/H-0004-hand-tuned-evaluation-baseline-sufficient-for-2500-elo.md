---
id: H-0004
type: hypothesis
title: Hand-Tuned Evaluation Baseline Sufficient for 2500+ Elo
status: OPEN
confidence: 0.6
priority: medium
example: false
created: 2026-09-09
last_updated: 2026-09-09
agents_supporting: [researcher-architect]
agents_opposing: []
tags: [evaluation, hand-tuned, texel, baseline]
---

# H-0004 — Hand-Tuned Evaluation Baseline Sufficient for 2500+ Elo

## Question
Can material + PST + king safety (pawn shield) + pawn structure (passed/doubled),
Texel/SPSA-tuned on quiet labeled positions, reach a useful playing baseline with a
good classical search — before any NNUE work?

## Hypothesis
Yes (plausible, 0.6): with the O3 search stack, a tuned linear eval reaches
competitive baseline strength sufficient to generate quality self-play data and to
serve as the NNUE fallback/ablation. The 2500 figure is an aspiration, NOT a measured
claim; success is defined below by correlation + SPRT, not by an Elo number alone.

## Why We Think This Might Work
Linear evals + Texel tuning are well documented; cheap inference keeps NPS high;
a tuned baseline isolates NNUE gains later (F-0001 sequencing).

## Counterarguments
Hand knowledge plateaus; NNUE may dominate sooner; tuning-set bias (quiet only)
may not transfer to tactical play.

## Agents Supporting
researcher-architect (0.6, plausible).

## Agents Opposing
(none.)

## Confidence
0.6 (plausible).

## Proposed Experiment
E-EVAL: implement evaluate()->int (tapered material+PST+safety+structure); tune via
Texel on 50k quiet Stockfish-labeled FENs; fixed-node SPRT (200 games) vs
material-only; report correlation + MAE on holdout.

## Required Metrics
Holdout correlation (>0.95 target TBD by data), MAE, fixed-node SPRT result, NPS
with eval enabled.

## Status
OPEN

## Result
(none.)

## Conclusion
(none)

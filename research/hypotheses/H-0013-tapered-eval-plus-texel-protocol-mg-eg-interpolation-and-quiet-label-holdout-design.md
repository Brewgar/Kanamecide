---
id: H-0013
type: hypothesis
title: Tapered eval plus Texel protocol - mg-eg interpolation and quiet-label holdout design
status: OPEN
confidence: 0.6
priority: medium
example: false
created: 2026-09-09
last_updated: 2026-09-09
agents_supporting: [researcher-architect]
agents_opposing: []
tags: [evaluation, texel, tuning, tapered-eval]
---

# H-0013 — Tapered eval plus Texel protocol - mg-eg interpolation and quiet-label holdout design

## Question
H-0004 proposes a hand-tuned eval + Texel tuning but pins neither the tapered
middlegame/endgame interpolation nor the tuning protocol. What exact design (phase
weights, PST layout, quiet-label filtering, holdout discipline, success gates) should the
E-EVAL implementation follow so its result is attributable and not tuning-set overfit?

## Hypothesis
Plausible (0.6): a tapered linear eval (material + 6 PSTs x mg/eg + pawn-shield +
passed/doubled pawn terms), phase-interpolated by non-pawn material, Texel-tuned on ~50k
quiet Stockfish-labeled FENs with holdout split BY GAME (anti-leakage), succeeds iff
holdout correlation target plus fixed-node SPRT vs material-only both pass. The "2500"
figure in H-0004 stays aspirational; the gates are correlation/MAE + SPRT.

## Why We Think This Might Work
Tapered Texel tuning is the documented Ethereal-era recipe; quiet-only labels avoid
teaching the eval to predict search tactics; game-split holdouts prevent position-level
leakage; SPRT vs material-only isolates the tuning gain from the search stack.

## Counterarguments
Quiet-label bias may not transfer to tactical play (H-0004 counter); 50k may be small;
phase-weight formula itself is a hyperparameter. All handled by reporting MAE by game
phase + a tactical-suite spot check, not just global correlation.

## Agents Supporting
researcher-architect (0.6, plausible — recipe, not measured here).

## Agents Opposing
(none.)

## Confidence
0.6 (plausible; protocol must exist before E-EVAL code).

## Proposed Experiment
E-EVAL (after O3 search + SPRT harness): implement evaluate()->int per this protocol;
tune; report holdout correlation + MAE (overall + by phase) + 200-game fixed-node SPRT
vs material-only + NPS-with-eval. Pre-register the gates before tuning.

## Required Metrics
Holdout correlation, MAE overall/by-phase, SPRT decision vs material-only, eval NPS cost,
tuning-set hash + engine hash for reproducibility.

## Status
OPEN

## Result
(none)

## Conclusion
(none)
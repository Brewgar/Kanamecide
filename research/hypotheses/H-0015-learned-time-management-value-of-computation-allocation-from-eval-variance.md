---
id: H-0015
type: hypothesis
title: Learned time management - value of computation allocation from eval variance
status: OPEN
confidence: 0.3
priority: low
example: false
created: 2026-09-09
last_updated: 2026-09-09
agents_supporting: [researcher-architect]
agents_opposing: []
tags: [time-management, long-term, speculative, search]
---

# H-0015 — Learned time management - value of computation allocation from eval variance

## Question
Long-term: can the engine allocate search time by predicting the value of additional
computation per node (from eval volatility, PV instability, model disagreement) instead
of fixed time-per-move heuristics — and does that beat hand-tuned time management at
fixed total time?

## Hypothesis
Speculative (0.3): once a real eval (H-0004/H-0013) and search statistics (fail-high/low
rates, score variance across ID iterations) exist, a lightweight allocator (extend on
PV-instability, save on flat scores) gains measurable Elo at fixed time control. This is
the lowest-priority hypothesis: it needs eval variance estimates that do not exist yet.

## Why We Think This Might Work
Top engines already hand-code volatility responses (Stockfish time management reacts to
score drops/best-move changes); learning the mapping from search statistics to
extend/save decisions generalizes that. Data is free (every search logs its own stats).

## Counterarguments
Hand-tuned time management is already strong; the gain may be single-digit Elo for real
complexity; risk of time-forfeit bugs. Only attempt after SPRT harness + Gauntlet exist
to measure safely.

## Agents Supporting
researcher-architect (0.3, speculative — direction, not near-term plan).

## Agents Opposing
(none; adversarial-reviewer invited to demand a falsification bar when activated.)

## Confidence
0.3 (speculative).

## Proposed Experiment
E-TIME (Phase 4+, after NNUE + SPRT Gauntlet): log per-move search stats + outcome;
train allocator offline; A/B at fixed total time via SPRT. Pre-register: must show
positive Elo with zero forfeits over 1000+ games.

## Required Metrics
SPRT Elo at fixed time, forfeit count (must be zero), time-usage distribution,
extend/save precision vs post-hoc optimal.

## Status
OPEN

## Result
(none)

## Conclusion
(none)
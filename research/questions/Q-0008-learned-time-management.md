---
id: Q-0008
type: question
title: "Can computation be allocated by predicted value-of-search (eval variance / PV instability) rather than fixed heuristics?"
status: OPEN
priority: low
example: false
created: 2026-09-19
last_updated: 2026-09-19
hypotheses: [H-0015]
experiments: []
suggested_experiments: ["E-TIME: after SPRT exists, log per-move search stats; train an allocator offline; A/B at fixed total time, 0 forfeits required"]
depends_on: [Q-0004, Q-0001]
blocked_by: []
answers: null
---

# Q-0008 — Learned time management / value-of-computation allocation

## Question
Can the engine allocate its search budget by predicting which positions benefit from more
computation (eval variance across iterative-deepening iterations, PV instability, score
drops) instead of the fixed `our_time/30 + inc` heuristic — and beat it at fixed total time,
with zero forfeits?

## Why it matters
This is the H-0015 speculative lever; it is also a safety-critical system (a bug = a forfeit),
so it must sit behind Q-0004 (an SPRT harness to measure it) and Q-0001 (a stable eval whose
variance is even meaningful).

## What is known
- The O3d time heuristic is a first-order approximation and every search logs its own stats
  for free.

## What is NOT known
- Whether predictable variance exists at all on this engine; hand-tuned counterparts already
  exist in mature engines, so the baseline is unfriendly.

## Related records
- H-0015 (conf 0.3, speculative), Q-0001 (eval variance), Q-0004 (SPRT).
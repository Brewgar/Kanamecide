---
id: F-0001
type: failure
title: "Premature NNUE without a correct search"
status: RECORDED
elo_change: null
example: true
created: 2026-09-08
tags: [nnue, sequencing, process]
---

# F-0001 — Premature NNUE without a correct search

> ⚠️ **EXAMPLE / MOCK DATA.** Demonstrates the failure format. This did not actually happen;
> it is an illustrative record.

## Hypothesis
Jumping straight to NNUE would accelerate strength gains.

## Implementation
(none — hypothetical)

## Expected Result
Fast strength gains from a learned evaluation.

## Actual Result
(unmeasurable — no search existed to evaluate against)

## Elo Change
(null)

## Performance Change
(null)

## Why It Failed
(illustrative) A learned evaluation is useless without a correct search to consume it, and
without a baseline there is no way to attribute any gain.

## Lessons
Establish correctness (perft) -> search -> hand-tuned eval -> NNUE, in order.

## Future Relevance
Reminds future agents not to train or optimize a component before its upstream dependencies exist.
---
id: Q-0006
type: question
title: "Can the E-0011 self-play pipeline produce a deduped, provenance-carrying dataset that trains an eval that beats the hand-tuned one?"
status: OPEN
priority: high
example: false
created: 2026-09-19
last_updated: 2026-09-19
hypotheses: [H-0004, H-0013]
experiments: [E-0010]
suggested_experiments: ["E-0011: >=1000 legal, deduplicated, provenance-carrying games; resume-from-checkpoint adds no duplicates"]
depends_on: []
blocked_by: []
answers: null
---

# Q-0006 — Self-play data pipeline -> Texel -> NNUE (the data flywheel)

## Question
The engine is now a player (O3d + E-0010 eval, +116 Elo over material-only). The missing
compounding asset is the data loop: self-play -> dedup/dataset -> tune (Texel) / train
(NNUE) -> promote -> repeat. Can the E-0011 pipeline generate dataset-grade games, and is
the resulting label quality good enough to beat the hand-tuned eval as a training target?

## Why it matters
Every later learned-eval and policy claim depends on this loop's data quality and
reproducibility (the E-0010 duplicate-games and dead-process lessons are load-bearing).

## What we know
- E-0010 produced 1240 legal, independent, provenance-carrying games locally — the pipeline
  exists in prototype form (e0010_match2.py + report).
- The pipeline's only correctness problems (duplicate openings, EvalStage no-op, bestmove
  stall) are documented and fixed (R-0003 F4/F5/F6, E-0010).

## What is NOT known
- Whether >=1000 games at a playable TC runs cleanly to completion under runjob.py
  (with heartbeat/resume) at <=2 concurrent engine pairs.
- Whether the resulting labels train a net that beats hand-tuned eval (H-0004 unresolved).

## Related records
- W-0001 (this work item), E-0010, H-0013 (Texel holdout design), PR-0003.
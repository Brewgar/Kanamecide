---
id: Q-0003
type: question
title: "Should the transposition table persist across moves (TT reuse), and what does a correct aging/reuse policy gain vs. per-move clear?"
status: OPEN
priority: medium
example: false
created: 2026-09-19
last_updated: 2026-09-19
hypotheses: []
experiments: [E-00009]
suggested_experiments: ["E-TTPERSIST: same fixed positions as E-00009 at successive root moves with and without TT persistence; node/time deltas"]
depends_on: [Q-0002]
blocked_by: []
answers: null
---

# Q-0003 — Persistent transposition table across moves

## Question
O3d clears the TT at every `go` (no persistence across moves). How much does reuse across a
game cost in correctness risk (a stale bound surviving past a changing position) versus the
search-throughput gain, and what aging/replacement policy makes persistence net-positive?

## Why it matters
TT reuse is standard in strong engines; the current per-move clear is a known, recorded
follow-up, and the interaction with the Q-0002 pruning deltas must be separated.

## What we know so far
- TT with 2-entry buckets and mate-shifting exists and is verified (E-00009; 11/11 identical
  best moves vs O3c; DEC-0008 re-validation on stored moves).

## What is NOT known
- Whether persistence actually wins on THIS engine/engineering model (the risk is entrenched
  TT-move reuse of a position whose side context changed).

## Dependencies
- Q-0002's PVS/TT deltas first, so persistence is measured on final TT content, not a
  moving target.

## Related records
- E-00009 follow-up, DEC-0008 (move re-validation contract), H-0009.
---
id: Q-0007
type: question
title: "How much of perft time is slider attacks (the Amdahl ceiling for PEXT), and is the PEXT/magic swap worth doing at 1.3-2.5x?"
status: OPEN
priority: medium
example: false
created: 2026-09-19
last_updated: 2026-09-19
hypotheses: [H-0005, H-0006]
experiments: [E-0002, E-00005]
suggested_experiments: ["E-00005: measure slider-attack share of perft time at /O2 (profile); the Amdahl ceiling before PEXT code is written", "E-PEXT: only if slider_share >= 30%"]
depends_on: []
blocked_by: []
answers: null
---

# Q-0007 — PEXT/magic sliders: is it worth it, and bounded by how much?

## Question
D-0003's RATIO debate (H-0005's >=3x vs H-0006's 1.3-2.5x at /O2) is settled only by an
instrumented measurement of the slider-attributable share of perft time, then (if warranted)
an E-PEXT A/B at bit-identical perft. E-00005 (the profile) must precede E-PEXT.

## Why it matters
PEXT is the biggest remaining NPS lever that is NOT search. It is bounded by Amdahl:
if sliders are <30% of perft time, the 2.5x upper end is falsified and the work is
deprioritized in favor of search/eval.

## What we know so far
- `attacked_by` recomputes occupancy and re-derives slider rays once per node; the movegen
  also re-derives them — the true share is larger than the naive "slider movegen" claim, but
  unprofiled.
- Certified /O2 baseline: 43-47 Mnps (E-0002, 5 reps, pinned, sha-256 logged).

## What is NOT known
- The actual slider share, which is the whole question.

## Related records
- H-0005 (>=3x claim, confidence 0.45), H-0006 (1.3-2.5x claim), D-0003 (ratio partition),
  E-00005 (the pre-PEXT profile gate, PENDING), E-0002.
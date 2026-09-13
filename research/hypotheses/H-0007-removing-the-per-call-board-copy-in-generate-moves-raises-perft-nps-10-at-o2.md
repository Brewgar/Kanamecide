---
id: H-0007
type: hypothesis
title: Removing the per-call Board copy in generate_moves raises perft NPS >=10% at O2
status: OPEN
confidence: 0.65
priority: medium
example: false
created: 2026-09-09
last_updated: 2026-09-09
agents_supporting: [researcher-architect]
agents_opposing: []
tags: [movegen, performance, microbench, nps]
---

# H-0007 — Removing the per-call Board copy in generate_moves raises perft NPS >=10% at O2

## Question
`generate_moves` (movegen.cpp:6) copies the whole ~312-byte `Board` (`Board b_nc = b_in;`)
on EVERY call — including positions with no en-passant target — just to probe EP legality.
Does that copy cost >=10% of perft NPS at /O2?

## Hypothesis
Yes (likely, 0.65): the copy touches ~312 B + key per node in the single hottest function;
at ~47 Mnps (E-00003) that is ~22M copies/s. A caller-owned scratch board (or make/unmake
probe on the live board with undo) removes it. Falsifiable bar: <10% NPS gain = hypothesis
rejected (copy is not a bottleneck).

## Why We Think This Might Work
- Copying 312 B/call at the perft node rate is a large memory-traffic fraction on-call.
- The EP probe path ALSO exists for actual EP positions (rare), so the copy is mostly waste.
- Cost is pure overhead: zero semantic change, perft counts must stay identical.

## Counterarguments
- At /O2 the 312-B copy may be partially optimized (e.g., only touched fields), and memory
  bandwidth is huge vs ALU work; the constant may be a few % not 10%.
- `attacked_by`/ray-stepping may dominate, making this a second-order effect (H-0006).
  Measurement (profile + A/B) is required; static reasoning bounds are weak here.

## Agents Supporting
researcher-architect (0.65, likely - microbenchmark required).

## Agents Opposing
(open — systems-researcher / adversarial-reviewer invited.)

## Confidence
0.65 (likely direction; magnitude testable in a day).

## Proposed Experiment
E-MGCOPY: (1) add profiling or a variant signature using a caller-owned scratch board;
(2) keep perft suite bit-identical; (3) rerun the E-00003 NPS table at /O2, 5 reps.
Report NPS delta and its share of CPU time via a quick instrumented build.

## Required Metrics
Perft counts identical; NPS before/after; % of perft time spent copying (instrumented).

## Status
OPEN

## Result
(none)

## Conclusion
(none)
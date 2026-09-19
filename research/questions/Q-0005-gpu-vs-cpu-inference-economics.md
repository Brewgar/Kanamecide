---
id: Q-0005
type: question
title: "CPU-VNNI vs GPU batch-1 inference economics: is the RTX 5070 Ti a training device or a playing device?"
status: OPEN
priority: low
example: false
created: 2026-09-19
last_updated: 2026-09-19
hypotheses: []
experiments: [E-00004]
suggested_experiments: ["E-00004 RE-SPEC: add a CPU AVX-512 VNNI batch=1 baseline and the HalfKP feature-transform + PCIe cost; only then can it gate D-0001"]
depends_on: [Q-0006]
blocked_by: []
answers: null
---

# Q-0005 — GPU vs CPU NNUE inference economics (the D-0001 gate, re-specified)

## Question
E-00004 was filed to measure RTX 5070 Ti batch-inference latency for an NNUE-scale net,
but as written it lacks a CPU baseline and omits the HalfKP feature-transform + PCIe cost,
so it CANNOT settle D-0001 (GPU MCTS vs classical). Re-specified, the real question is:
for batch=1 play and for self-play generation, does the GPU beat Zen-5 AVX-512 VNNI on
latency and $/Elo — or is the 5070 Ti a training-only device?

## Why it matters
It decides whether the Phase-3+ roadmap ever pursues GPU MCTS/PUCT, or stays classical
(CPU search + CPU-VNNI eval).

## What is known
- The opposing claim: RTX 5070 Ti (Blackwell) is excellent per-theory; but the MCTS
  ("GPU leapfrog") argument is circular until a net and a playing engine exist.
- CPU-side path: AVX-512 VNNI NNUE inference is the known-strong Stockfish-style route.

## What is NOT known
- Everything numerical. E-00004 must be re-specified before it can gate anything.

## Related records
- D-0001 (GPU vs classical, ROUTED), E-00004 (needs re-specification), R-0002.
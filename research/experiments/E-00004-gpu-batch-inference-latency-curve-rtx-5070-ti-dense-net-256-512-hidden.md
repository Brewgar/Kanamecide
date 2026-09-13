---
id: E-00004
type: experiment
title: GPU batch-inference latency curve (RTX 5070 Ti, dense net 256-512 hidden)
status: PENDING
result: null
elo_change: null
hypothesis: "H-GPU-LATENCY: Batch=1 latency ≤ 200 µs and batch=32 throughput ≥ 100k inferences/sec on RTX 5070 Ti for a 256-512 hidden unit dense net (NNUE-scale)"
priority: high
example: false
created: 2026-09-10
completed: null
tags: [gpu, inference, latency, rtx-5070, mcts-feasibility, d-0001]
---

# E-00004 — GPU batch-inference latency curve (RTX 5070 Ti, dense net 256-512 hidden)

## Hypothesis
H-GPU-LATENCY: Batch=1 latency ≤ 200 µs and batch=32 throughput ≥ 100k inferences/sec on RTX 5070 Ti for a 256-512 hidden unit dense net (NNUE-scale). This is the feasibility gate for D-0001 (GPU MCTS vs classical alpha-beta).

## Baseline
CPU AVX-512 VNNI batch=1 latency on Ryzen 9700X (to be measured separately).

## Candidate
CUDA 13.3 kernel with tensor cores (BF16/FP16), batch sizes = 1, 2, 4, 8, 16, 32, 64, 128.

## Difference
GPU vs CPU inference latency/throughput for NNUE-scale dense network. No engine semantics change.

## Hardware
RTX 5070 Ti (16 GB, Blackwell), CUDA 13.3, Windows 11. Pin GPU clock via nvidia-smi -lgc.

## Engine Version
Pre-search HEAD (perft-only; git hash recorded at run time).

## Network
Dense: input=768 (HalfKP) → 256/512 hidden (LReLU) → 1 output (value), ~200k params. Weights randomly initialized (no training needed — measure inference only).

## Dataset
Synthetic random positions (FENs generated programmatically). No training data needed.

## Test Method
Warmup: 1000 inferences per batch size. Timed: 10000 inferences per batch size. Report p50/p95/p99 latency (µs) and throughput (inferences/sec). Pin GPU clock. Single-threaded CPU baseline for comparison.

## Games / Samples
0 games; 10000 inferences × 8 batch sizes × 2 network widths (256, 512 hidden) = 160k inference measurements.

## Metrics
- Batch=1 latency (µs): p50, p95, p99
- Batch=32 throughput (inferences/sec)
- Latency scaling exponent (how latency grows with batch size)
- CPU baseline batch=1 latency (µs) for same net

## Results
(not run.)

## Statistical Analysis
Report mean ± std across 3 independent runs (separate process launches). No SPRT (deterministic inference timing).

## Interpretation
Decision rule (pre-registered):
- IF batch=1 latency > 500 µs OR batch=32 throughput < 50k inf/s → GPU MCTS infeasible for Phase 3 (ROUTE to CPU-first).
- IF batch=1 ≤ 200 µs AND batch=32 ≥ 100k inf/s → GPU MCTS feasible (AGREED for D-0001 Phase 3+).
- ELSE → CONFLICT (needs architecture-specific measurement with actual PUCT search).

This experiment provides the feasibility gate for D-0001: without actual RTX 5070 Ti batch-inference numbers, all GPU MCTS arguments are speculative.

## Conclusion
(not executed.)

## Follow-Up
If feasible: implement batched NNUE inference kernel, integrate with PUCT search prototype. If infeasible: confirm CPU-first roadmap (classical alpha-beta/PVS + AVX-512 VNNI NNUE).
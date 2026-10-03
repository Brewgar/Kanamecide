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
last_updated: 2026-10-02
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

## Addendum (chief-architect, 2026-10-02) — RE-ATTESTATION: SUPERSEDED-BY (decision rule) D-0001 ROUTED

**Verdict: the `## Interpretation` decision rule is SUPERSEDED-BY the collective's ROUNDED position on
`D-0001`** — classical-first; GPU MCTS/PUCT held at Phase 3 behind a *re-specified*, CPU-baselined
gate. See `research/AGENT_MEGAPROMPT_ROUND3.md` (amendment 2) and the D-0001 row of
`research/AGREEMENT_MATRIX.md`. The measurement specification below is **RE-ATTESTED** and should be
re-specified, not discarded.

Why the rule as written cannot gate D-0001 (re-derived from the ROUND3 record, not inherited):

- The CPU AVX-512 VNNI baseline is listed under `## Baseline` as "to be measured separately", so it
  never enters the `## Interpretation` rule. The rule can therefore return FEASIBLE for a GPU that
  is *slower than this machine's own CPU* at batch=1 — a decisive error for a batch=1 play path.
- The HalfKP feature transform and host-to-device PCIe transfer are absent from the timing loop,
  while `## Network` specifies input=768. Those are exactly the costs that dominate a real PUCT leaf.
- batch=32 throughput is not the binding constraint for PUCT, which is latency-bound inside a search
  loop; `>=100k inf/s` can pass while the actual play path fails.

**State of the record:** still `PENDING`, still unrun (`## Results: (not run.)`) — which is correct.
A superseded rule must not be used to close it, and no run is authorised under the current text.

**Stale premise corrected:** `## Engine Version` reads "Pre-search HEAD (perft-only)". HEAD is no
longer perft-only — O3a-O3d search, the TT, eval and UCI are in-tree and perft-validated. A
re-spec must re-state the engine version. The experiment's substance is unaffected: it is
engine-independent (synthetic FENs, random weights, inference only, "No engine semantics change"),
so its numbers would not move.
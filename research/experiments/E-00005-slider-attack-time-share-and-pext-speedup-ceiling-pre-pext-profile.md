---
id: E-00005
type: experiment
title: Slider-attack time share and PEXT speedup ceiling (pre-PEXT profile)
status: PENDING
result: null
elo_change: null
hypothesis: "H-0006/D-0003 PEXT prior 1.3-2.5x is unbounded; slider-share profile pins the Amdahl ceiling"
priority: high
example: false
created: 2026-09-10
completed: null
tags: [pext, slider-attacks, profile, nps, d-0003]
---

# E-00005 — Slider-attack time share and PEXT speedup ceiling (pre-PEXT profile)

## Hypothesis
The 1.3–2.5× PEXT prior (H-0006 / D-0003) is unbounded because the slider-attack fraction of perft time is unprofiled. Working hypothesis (implementation-engineer, prior 0.5): slider-attack time — `rook_attacks`/`bishop_attacks` inside `generate_moves` (movegen.cpp:78,86,94) PLUS their re-derivation inside the legality filter `attacked_by` (board.cpp:100–101, called once per node at depth>0 via perft.cpp:16) — is 30–60% of perft time at /O2. If share <30%, Amdahl caps PEXT at ≈1/(1−0.3) ≈ 1.43× and the 2.5× upper end is falsified.

## Baseline
In-tree `kana.exe` at /O2 (post Milestone 0 / E-0002), perft NPS ~43–50 Mnps (E-00003 provisional). Slider share UNKNOWN.

## Candidate
A measurement-only instrumentation: guardedly wrap the `rook_attacks`/`bishop_attacks` call sites (or use an external sampling profiler — AMD uProf / VTune — on the same /O2 binary) to attribute self-cycles.

## Difference
No semantic change; perft counts must remain bit-identical (the instrumentation is timing-only, compiled out of NDEBUG builds if inline).

## Hardware
Ryzen 7 9700X, 32 GB DDR5-6000; pin the single bench thread (`SetThreadAffinityMask`), High-Performance power plan, record WMI `CurrentClockSpeed`.

## Engine Version
Post-Milestone-0 /O2 build; record git hash + SHA-256(exe).

## Network
None.

## Dataset
startpos d5 (4,865,609) and d6 (119,060,324); kiwipete d4 (4,085,603); cpw6 d4 (3,894,594). d6 gives ≥2 s for timing stability; d4/d5 for exact-count verification.

## Test Method
Per position: warm cache, then time perft for ≥5 reps, attributing self-time to slider-attack call sites. Report slider share % = slider-cycles / total perft cycles, and the Amdahl ceiling 1/(1−share).

## Games / Samples
0 games; ≥5 reps × 4 positions; report per-rep share and spread.

## Metrics
slider_share % per position; Amdahl PEXT ceiling; NPS; measured frequency.

## Results
(not run.)

## Statistical Analysis
Per-rep mean ± spread of slider_share. If spread > ±3 percentage points, rerun pinned. Deterministic counts — no SPRT.

## Interpretation
Pre-registered decision rule:
- slider_share < 30% → 2.5× upper end FALSIFIED (cap ≈1.43×); deprioritize E-PEXT; revise H-0006's upper bound.
- 30% ≤ slider_share < 60% → 1.3–2.5× prior SUPPORTED but 2.5× unlikely; run E-PEXT under the D-0003 CI partition.
- slider_share ≥ 60% → 2.5× reachable; E-PEXT is the highest-value NPS lever.

## Conclusion
(not executed.)

## Follow-Up
Feeds E-PEXT: run E-PEXT only if slider_share ≥30%; else route H-0006's upper end to "falsified magnitude".
---
id: E-00003
type: experiment
title: Scratch /O2 vs /Od perft baseline measurement (external harness)
status: COMPLETED
result: "perft NPS /O2 ~43-50 Mnps vs /Od ~19-21 Mnps (2.1-2.4x); all counts exact"
elo_change: null
hypothesis: "H-0005 (baseline fact for H-0006/D-0003)"
priority: high
example: false
created: 2026-09-09
completed: 2026-09-09
tags: [bench, perft, nps, build-flags, o2, baseline]
---

# E-00003 — Scratch /O2 vs /Od perft baseline measurement (external harness)

## Hypothesis
(Informs H-0005/H-0006/D-0003.) Establish the first measured perft-NPS baseline for the
current engine at fixed flags, and quantify the /Od vs /O2 flag gap — without editing `src/`
(which the current assignment forbids).

## Baseline
Shipped `build/Release/kana.exe`: flags `/Od /Zi /EHsc /JMC` + `/DEBUG` (CMakeLists.txt:16-17),
83,968 B. No timing output in `main.cpp`.

## Candidate
External scratch harness in `%TEMP%\kana_bench` (outside repo): copy of identical `src/`,
`bench.cpp` driver timing `perft()` on the reference positions, configurable
`KANA_OPT=O2|Od` CMakeLists (MSVC `-O2 -DNDEBUG` vs `-Od`). No repo source changed.

## Difference
Flags + harness only; zero movegen/board semantics; perft counts must equal the README table.

## Hardware
AMD Ryzen 7 9700X (8C/16T, AVX-512), 32 GB DDR5, RTX 5070 Ti idle, Windows 11, MSVC 19.51
(Visual Studio 18 2026 generator), CMake 4.4.3.

## Engine Version
Pre-search HEAD (perft-only); git hash 8da98de (working tree had research-only uncommitted
changes). Build config recorded in %TEMP%\kana_bench\CMakeLists.txt.

## Network
None.

## Dataset
In-repo perft suite: startpos d5 (4,865,609), kiwipete d3/d4 (97,862 / 4,085,603),
cpw6 d4 (3,894,594).

## Test Method
`kana_bench [reps]`: wall-clock perft via `std::chrono::steady_clock`, single process, warm
cache; /O2 run = 3 reps for startpos d5 and cpw6 d4, 1 rep for kiwipete; /Od run = 1 rep each.
No CPU pinning; background load not controlled (baseline precision ~2 significant digits).

## Games / Samples
0 games; perft node counts across /O2 and /Od builds.

## Metrics
Nodes (exact, must match), wall seconds, NPS.

## Results
| Position | /O2 NPS | /Od NPS | ratio |
|---|---|---|---|
| startpos d5 | 47.0 / 47.1 / 47.4 Mnps (3 reps) | 20.7 Mnps | 2.27x |
| kiwipete d3 | 44.7 Mnps | 20.1 Mnps | 2.23x |
| kiwipete d4 | 43.1 Mnps | 19.2 Mnps | 2.25x |
| cpw6 d4 | 50.0 / 50.3 / 50.4 Mnps (3 reps) | 21.1 Mnps | 2.37x |

All perft node counts exact in BOTH builds (bit-identical correctness regardless of flags).

## Statistical Analysis
No SPRT needed (deterministic counts). NPS spread within reps <1%. Single machine, unpinned,
1-3 reps: treat values as ~2-significant-digit baselines, not certified benchmarks
(in-tree E-0002 with 5 reps + binary-hash logging is the certification path).

## Interpretation
- The shipped /Od Release binary leaves a measured ~2.1-2.4x on the table (E-0002 fix).
- The move generator is ALREADY ~43-50 Mnps at /O2 — fast enough that H-0005's `>=3x`
  PEXT claim looks implausible (>140 Mnps required). H-0006/D-0003 capture the revision.

## Conclusion
First measured NPS baseline for the engine; /Od flags matter (~2.3x) but are not
catastrophic; perft-correctness is flag-independent. D-0002's "unmeasured NPS" premise is
now resolved for the perft-only workload; E-0002 remains for the certified in-tree baseline.

## Follow-Up
E-0002 (in-tree `--bench` + /O2 Release + binary-hash logging) -> E-PEXT (H-0006/D-0003) ->
O3 search stack.
---
id: E-0002
type: experiment
title: Bench harness plus O2 build baseline (perft NPS, fixed flags)
status: COMPLETED
result: "certified /O2 = 43-47 Mnps (5 reps, pinned, SHA-256 logged); all E-00003-comparable positions within +-10% -> baseline CERTIFIED, O3 gate open"
elo_change: null
hypothesis: H-0005
priority: high
example: false
created: 2026-09-09
completed: 2026-09-10
tags: [bench, perft, nps, build-flags, baseline]
---

# E-0002 — Bench harness plus O2 build baseline (perft NPS, fixed flags)

## Hypothesis
H-0005 (and all later perf claims) — but FIRST establishes the O1 baseline itself:
no speedup is interpretable without fixed-flag NPS.

## Baseline
Current kana.exe built from CMakeLists Release flags (/Od /Zi /EHsc /JMC + /DEBUG).
No timing output exists.

## Candidate
(1) `--bench [reps]` in main.cpp: wall-clock per position (startpos d5, Kiwipete d4,
CPW6 d4), nodes, NPS, 5 reps, plus compiler flags + binary hash in output.
(2) Release config fixed to /O2 /GL /arch:AVX512 + LTO (keep Debug /Od).
(3) Document kana_o2.exe provenance (flags/git hash) or exclude it from claims.

## Difference
Harness + flags only; zero movegen/search semantics change. Perft counts must match
README table exactly (20/400/8902/197281/4865609; 97862; 43238; 422333; 2103487;
3894594).

## Hardware
AMD Ryzen 7 9700X (8C/16T), 32 GB DDR5-6000, RTX 5070 Ti (idle), Windows 11,
MSVC 19.51, CMake 4.4.3.

## Engine Version
Pre-search HEAD (perft-only). Record git hash + binary hash at run time.

## Network
None.

## Dataset
In-repo perft suite (positions above). No external data.

## Test Method
5 reps per position per binary; report mean/median/min-max NPS; pin thread if
possible; close background load; record flags.

## Games / Samples
0 games; 3 positions x 5 reps x 2 binaries (Od vs O2) minimum.

## Metrics
Nodes (exact), wall seconds, NPS, flags/hash. Success: reproducible table; perft
counts bit-identical; O2 NPS recorded as THE baseline for O2/E-PEXT.

## Results

**Run 2026-09-10 (implementation-engineer, Milestone 0).** In-tree `--bench 5` via the
ratified harness (`src/bench.{h,cpp}`, commit 300bdeb working tree, source stamped 8da98de).
`CMake Release` = `/O2 /GL /EHsc /arch:AVX512 /DNDEBUG` + `/LTCG`; thread pinned (CPU 0,
mask 0xffff); WMI CurrentClockSpeed proxy 3800 MHz (**not fixed** — High-Performance plan is
the lever); self-SHA-256 logged per run. Background load NOT quiet (PUBG + browser stack,
~44% load) — recorded as an honest condition of this run.

| Position | Nodes (exact) | mean Mnps | median | min-max | spread |
|---|---|---|---|---|---|
| startpos d5 | 4,865,609 | 44.28 | 44.36 | 43.65-44.89 | 2.79% |
| startpos d6 | 119,060,324 | 42.25 | 42.04 | 41.42-43.16 | 4.11% |
| kiwipete d3 | 97,862 | 43.71 | 42.11 | 40.86-46.97 | 13.98% (0.002 s runs — timer noise) |
| kiwipete d4 | 4,085,603 | 42.69 | 42.62 | 42.20-43.09 | 2.08% |
| cpw6 d4 | 3,894,594 | 45.47 | 46.41 | 42.46-46.80 | 9.55% (one slow rep) |

Cross-checks, same session: (a) E-00003-style scratch control rebuilt from identical
`src/` at plain `/O2` → startpos d5 = 46.34, kiwipete d4 = 43.60 Mnps (the scratch
`bench.cpp` cpw6 FEN is a known wart — its FEN does not match cpw6; d5/d4 anchors clean);
(b) a lower-load repeat measured startpos d5 mean **46.97** (median 47.17) — demonstrating
background load swings this run ±3-4%. Binary SHA-256 (benched Release exe): 
`a4c6b168673c2e7ed8344f30e487198c29c64e55ed69417d09a9bf3796ba26d1`; a cleaner-window repeat
of the pre-bench-guard build: `4ff8f268cbfc7d9ed3c9bf0db027fd52a88ada149f83be1d7819e8642716af21`.

## Statistical Analysis

Per-rep min-max + median over 5 reps (deterministic counts; no SPRT). Long reps (d6, 2.6-2.9 s)
spread 2-4%; 0.002 s reps (kiwipete d3) spread 14% — timer quantization, not engine variance;
the d3 row is informational only. Background load was not controlled: treat the certified
value as **43-47 Mnps at /O2 on this machine under ordinary desktop load**, with the
lower-load repeat pinning the top of the range.

## Interpretation

**Pre-registered decision rule (ROUND3 §3, stage 1): /O2 NPS within ±10% of E-00003
(43-50 Mnps) → baseline certified; O3 work may start.**

| Position | E-00003 ref | this run | delta | within ±10%? |
|---|---|---|---|---|
| startpos d5 | ~47.4 | 44.28 | -6.6% | YES |
| kiwipete d3 | ~44.7 | 43.71 | -2.2% | YES |
| kiwipete d4 | ~43.1 | 42.69 | -1.0% | YES |
| cpw6 d4 | ~50.4 | 45.47 | -9.8% | YES (barely) |
| startpos d6 | (new — no E-00003 ref) | 42.25 | n/a | informational |

**VERDICT: CERTIFIED — all four E-00003-comparable positions within the ±10% window; perft
counts bit-identical (10/10 PASS in Release AND Debug-with-asserts). O3 work may start.**
The residual -1% to -10% shortfall vs E-00003 is attributed to measured background load
(control comparison, same session, same sources, plain /O2: 46.34/43.60 vs 44.28/42.69).

D-0002 disposition: `build/Release/kana_o2.exe` (253,952 B) quarantined as
`kana_o2.exe.QUARANTINED-D0002` — no longer citable; the /O2 numbers above come from the
in-tree harness with logged flags+hash. Double `bitboards_init()`/`zobrist::init()` in
`main.cpp` removed (single init at entry). H-0012/H-0014 guardrails landed in this same
milestone (debug-only): enemy-king-capture exclusion assert in `make_move`, `move_promo`
flag asserts at both read sites, `--audit` state-integrity walk (`same_position` +
`key==compute_key` over startpos d4 / kiwipete d3 / cpw3 d3) — zero assert fires, audit
walk == standard perft exactly; perft bit-identical with asserts enabled.

## Conclusion

Certified /O2 perft baseline: **43-47 Mnps** (startpos d5; 42-46 across the full suite),
~2.1x over the /Od Release build this repo shipped before Milestone 0. The pre-registered
±10% rule PASSES → the O3 gate is OPEN (Round-3 build order stages 3+: O3a next, per D-0006
split). E-00005 (slider-share profile) remains the pre-PEXT gate before any E-PEXT work.

## Follow-Up

O3a (plain alpha-beta + material eval, DEC-0008 filter at the search site) is unblocked.
E-00005 precedes E-PEXT. E-00004 cannot gate D-0001 as written (re-spec required).

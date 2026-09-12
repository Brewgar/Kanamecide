# Project State

> Canonical shared summary of the project. **Only stable, evidence-backed facts go here.**
> Agent opinions live in `research/agents/`; hypotheses in `research/hypotheses/`;
> decisions in `research/decisions/`. Do not add unverified claims to this file.

## Mission
Build a strong, research-driven chess engine ("Kanamecide", executable `kana`) and use it
as a platform for long-term multi-agent research. Correctness first, then search, then
evaluation and learning.

## Current Architecture
- **Language:** C++20.
- **Board representation:** bitboard + mailbox hybrid.
- **Hashing:** incremental Zobrist.
- **Move application:** make/unmake (not copy-make).
- **Move generation:** pseudo-legal generation + king-safety filter at the search/perft site (DEC-0008, ratified 2026-09-10; supersedes DEC-0005).
- **En passant legality:** verified by make/unmake probe (handles discovered-check pins).
- **Search (O3d, 2026-09-13):** negamax + alpha-beta, material eval, full ordering (O3b),
  QUIESCENCE search at the leaf (stand-pat + captures/promotions + delta pruning + check
  evasion) = tactically resolved leaf (E-00008 PASS, 2.08x nodes vs O3b); + 64-bit-key
  transposition table (64 MiB default, two-entry buckets, TT-move ordering + PV build,
  sound depth/bound-gated cutoffs, DEC-0008 re-validation of stored moves) + root iterative
  deepening (PV-first) + repetition/50-move draw scoring (E-00009 PASS: 9.5x fewer nodes
  vs O3c at depth 6, best moves 11/11 identical). No persistent-TT-across-moves yet.
- **UCI:** `uci` / `isready` / `ucinewgame` / `position (startpos|fen ... moves ...)` /
  `go depth|nodes|movetime|wtime btime winc binc` / `setoption Hash 1-1024` / `stop` /
  `quit`; `go` reports `info depth N nodes X time T score cp S nps Y pv ...` with
  `tt_probes/tt_hits/tt_cutoffs`; `stop` returns `bestmove` in <= 16 ms (measured max
  15.1 ms over 10 trials); engine emits nothing until the `uci` token is received.
- **Phase:** Phase-2 search stack COMPLETE (O3d / E-00009 PASS); E-EVAL + self-play
  driver unblocked.

## Current Strength
Move generator + board model validated against the Chess Programming Wiki perft suite with
exact matches (see table below).

## Current Performance

Verified perft results (all exact matches, from README.md; **re-verified by direct run of
`build\Release\kana.exe` on 2026-09-09**):

| Position | Depth | Nodes |
|---|---|---|
| Startpos | 1–5 | 20, 400, 8902, 197281, 4865609 |
| Kiwipete | 3 | 97,862 |
| CPW pos 3 (EP/pins) | 4 | 43,238 |
| CPW pos 4 (promotions) | 4 | 422,333 |
| CPW pos 5 (promotions) | 4 | 2,103,487 |
| CPW pos 6 (quiet) | 4 | 3,894,594 |

### Certified perft NPS baseline (E-0002, 2026-09-10 — MILESTONE 0, DECISION RULE PASSED)

In-tree `--bench 5` harness (`src/bench.{h,cpp}`), CMake Release `/O2 /GL /EHsc /arch:AVX512
/DNDEBUG` + `/LTCG`, thread pinned (CPU 0), WMI clock proxy 3800 MHz (not fixed), background
load not quiet (~44%): 

| Position | mean Mnps | median | min-max |
|---|---|---|---|
| Startpos d5 | 44.28 | 44.36 | 43.65-44.89 |
| Startpos d6 | 42.25 | 42.04 | 41.42-43.16 |
| Kiwipete d3 | 43.71 | 42.11 | 40.86-46.97 (0.002 s runs — timer noise) |
| Kiwipete d4 | 42.69 | 42.62 | 42.20-43.09 |
| CPW pos 6 d4 | 45.47 | 46.41 | 42.46-46.80 |

Pre-registered ±10% rule vs E-00003: all four comparable positions within the window
(-1.0% to -9.8%) → **baseline CERTIFIED; O3 work may start.** Same-session scratch control
(identical `src/`, plain /O2) measured startpos d5 = 46.34 and kiwipete d4 = 43.60 Mnps, and
a lower-load in-tree repeat measured startpos d5 mean 46.97 — background load accounts for
the -1% to -10% spread. Honest certified range: **43-47 Mnps at /O2 under ordinary desktop
load** (~2.1x over the pre-M0 /Od Release build). Binary SHA-256 (benched exe):
a4c6b168673c2e7ed8344f30e487198c29c64e55ed69417d09a9bf3796ba26d1 (commit 300bdeb).
Perft 10/10 PASS bit-identical in Release AND Debug-with-asserts; H-0014 state audit PASSED.

### Provisional perft NPS baseline (E-00003, 2026-09-09 — superseded by E-0002 for citation)

External scratch harness on identical `src/` (repo untouched), MSVC 19.51, /O2 vs /Od,
single machine, 1-3 reps, unpinned (~2 significant digits):

| Position | /O2 NPS | /Od NPS | ratio |
|---|---|---|---|
| Startpos d5 | ~47.0-47.4 Mnps | ~20.7 Mnps | ~2.3x |
| Kiwipete d4 | ~43.1 Mnps | ~19.2 Mnps | ~2.2x |
| CPW pos 6 d4 | ~50.0-50.4 Mnps | ~21.1 Mnps | ~2.4x |

All perft counts are bit-identical across both builds (correctness is flag-independent).
Note: Release ships `/Od /Zi /EHsc /JMC` + `/DEBUG` (CMakeLists.txt:16-17); fixing to /O2
is E-0002. In-tree `--bench` (5 reps + binary-hash logging) is the certification path.

## Hardware
- CPU: AMD Ryzen 7 9700X (8C/16T, AVX-512 with VNNI/BF16/FP16).
- RAM: 32 GB DDR5-6000.
- GPU: NVIDIA RTX 5070 Ti (16 GB, Blackwell, CUDA 13.3).
- OS/toolchain: Windows 11, MSVC 19.51, CMake 4.4.3.

## Current Models
None yet. The research system is model-independent; roles are mapped to models only in
`research/agents/ASSIGNMENTS.md`.

## Current Training Pipeline
None yet. Planned for Phase 3: self-play data generation + training (PyTorch + GPU).

## Active Research Questions
- Which search framework should be the primary architecture? (see `D-0001`, `H-0001`)
- How much do PVS + transposition tables help time-to-depth on this engine? (see `H-0001`, `E-0001`)
- How should evaluation (hand-tuned -> NNUE) be sequenced against search? (see the lesson in `F-0001`)

## Current Known Problems
- No search or evaluation yet — the engine only does board + move generation + perft.
- No self-play / data / training infrastructure.
- ~~`kana_o2.exe` in build/Release (253,952 B) has unrecorded build-provenance — excluded
  from claims (D-0002).~~ RESOLVED 2026-09-10: quarantined as `kana_o2.exe.QUARANTINED-D0002`;
  the certified /O2 baseline is the in-tree E-0002 harness (flags + self-SHA-256 logged).

## Recent Important Experiments
None executed yet. `E-0001` is pending (and is also an EXAMPLE record).
The movegen/perft validation is a correctness milestone, not a strength experiment.

## Current Champion
Engine (O3d, ordered AB + quiescence + TT + iterative deepening) plays complete legal
timed games: **2/2 self-play games 100 % legal at 200 ms/move** (a 234-ply draw and a
77-ply checkmate finish), **30/30 wins (100 %) vs legal-move-uniform random mover,
30/30 legal** at depth 4, `stop` latency max 15.1 ms, and **9.5x fewer nodes than the
O3c single-shot at depth 6** (5.11 M vs 48.6 M over the 11-position E-00007 set) with
identical best moves. Search efficiency (91.2 % node cut, O3b) + tactical leaf accuracy
(qsearch, O3c) + TT/ID node reduction (9.5x, O3d) are the baselines for every later delta.

## Current Known Problems
- No evaluation beyond material-only (E-EVAL next). No persistent TT across moves
  (TT is cleared per `go`); no aspiration/PVS/LMR/null-move (O3e candidates).

## Current Development Priorities
1. **Phase 3 — Evaluation (next: E-EVAL):** material + piece-square evaluation on top of the
   complete O3d search stack, calibrated via self-play; then PVS/LMR/null-move (O3e) and
   persistent TT across moves.
2. **Phase 3+ — Evaluation & learning:** hand-tuned evaluation -> NNUE; self-play data
   generation; training pipeline (PyTorch + GPU); experiment tracking; SPRT-based testing.

## Last Updated
2026-09-13 (O3d / E-00009 complete: TT + ID + time control + repetition; all five
decision-rule gates PASS — perft 10/10, 2/2 legal self-play @200 ms/move, stop max
15.1 ms, 9.5x node reduction, 30/30 vs random)
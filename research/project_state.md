# Project State

> Canonical shared summary of the project. **Only stable, evidence-backed facts go here.**
> Agent opinions live in `research/agents/`; hypotheses in `research/hypotheses/`;
> decisions in `research/decisions/`. Do not add unverified claims to this file.

<!-- research-meta
last_updated: 2026-09-25
reflects: [DEC-0001, DEC-0002, DEC-0003, DEC-0004, DEC-0006, DEC-0007, DEC-0008, DEC-0009, DEC-0010, DEC-0011, E-0002, E-00003, E-00006, E-00007, E-00008, E-00009, E-0010, E-0011, E-0012]
not_reflected: []
-->
> The `research-meta` block above is machine-checked by `research.py validate`:
> `last_updated` may not be older than the newest COMPLETED experiment / ACTIVE
> decision, and every such record must appear in `reflects` or — with a stated reason
> in the body — in `not_reflected`. This is the anti-staleness gate (DEC-0009, F7).

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
- **Evaluation (E-0010, 2026-09-14):** tapered hand-tuned eval (`src/eval.{h,cpp}`), 6 named
  terms (taper, MG/EG PSTs, pawn structure, mobility, bishop-pair/open-file/king group,
  tempo) selected at runtime by the UCI `EvalStage` option (0..6). Measured vs material-only:
  +116.1 Elo (LOS 100.00%, CI95 [+70.8,+163.5], N=240 independent games); pre-registered
  ≥150 bar NOT met (honest FAIL). Symmetry: 0 full-mirror violations on 1000 positions.
- **Strength-comparison decision rule (DEC-0010, 2026-09-21; W-0002):** calibrated from
  E-0010's measured variance (σ=371 Elo/game, six verified rungs; throughput 769 games/h):
  screening tier [0,+20] Elo, α=β=0.05 (LLR ±2.944), cap 8,000 games; regression tier
  [0,+5], cap 30,000; magnitude claims only as wide-zone SPRTs [M−50, M]; post-cap verdict
  INCONCLUSIVE. E-0010 restated under this rule (R-0009): screening PASS, regression PASS,
  "≥150" not established at N=240 (decidable at ~910 games via the [100,150] zone SPRT).
  Arithmetic reproducible: `research/context/w0002_power.py`.
- **Phase:** Phase 2 COMPLETE (O3d), Phase 3 evaluation measured (E-0010), and the
  E-0011 self-play dataset campaign is COMPLETED/PASS for artifact gates (a)-(f). The
  1,000-record local dataset is pinned by SHA-256 in RUN-0001; independent verification
  is requested by HO-0009. Next: E-0012 comparison harness and H-0013 Texel fitting.

## Certified Perft Anchors (SACRED — single protected home)

> These counts are the project's correctness floor. They live here and **only** here
> (DEC-0009 amended from R-0003 F12; the README is a pointer, never a second copy).
> Any change that alters one of these counts is a correctness regression and is
> reverted. `research.py validate` asserts every number below; deleting or altering the
> section fails validation loudly.
> Re-verified live on 2026-09-14 by direct run of `build\Release\kana.exe`:
> `PASS`/`0 diff` on all ten positions, final line `=== ALL TESTS PASSED`, exit code 0.

| Position | Depth | Nodes |
|---|---|---|
| Startpos | 1 | 20 |
| Startpos | 2 | 400 |
| Startpos | 3 | 8902 |
| Startpos | 4 | 197281 |
| Startpos | 5 | 4865609 |
| Kiwipete | 3 | 97,862 |
| CPW pos 3 (EP/pins) | 4 | 43,238 |
| CPW pos 4 (promotions) | 4 | 422,333 |
| CPW pos 5 (promotions) | 4 | 2,103,487 |
| CPW pos 6 (quiet) | 4 | 3,894,594 |

Reproduction command: `build\Release\kana.exe` (no arguments). Expected: 10 `PASS` lines
with `0 diff` and the string `ALL TESTS PASSED`.

## Current Strength
Move generator + board model validated against the Chess Programming Wiki perft suite with
exact matches (see the anchor table above).

## Current Performance

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
Note: Release shipped `/Od /Zi /EHsc /JMC` + `/DEBUG` before Milestone 0 (`CMakeLists.txt:16-17`);
E-0002 fixed that to `/O2` + `/LTCG`. The in-tree `--bench 5` (5 reps + binary-hash logging)
is the certification path.

## Hardware
- CPU: AMD Ryzen 7 9700X (8C/16T, AVX-512 with VNNI/BF16/FP16).
- RAM: 32 GB DDR5-6000.
- GPU: NVIDIA RTX 5070 Ti (16 GB, Blackwell, CUDA 13.3).
- OS/toolchain: Windows 11, MSVC 19.51, CMake 4.4.3.

## Current Models
None yet. The research system is model-independent; roles are mapped to models only in
`research/agents/ASSIGNMENTS.md`.

## Current Training Pipeline
None yet. The raw material exists locally (E-0010 match JSONL, gitignored) but there is no
game generator, no dataset, no labels and no model. Planned: E-0011 self-play data pipeline
→ Texel fitting (H-0013) → NNUE (PyTorch + GPU).

## Active Research Questions
- Which search framework should be the primary architecture? (see `D-0001`, `H-0002`/`H-0003` family)
- How much do PVS + transposition tables help time-to-depth on this engine? (`H-0009`, O3e)
- What evaluation representation justifies the next step (Texel-fitted hand-tuned → NNUE)?
  (`H-0004`, `H-0013`; the lesson in `F-0001` is illustrative, not a real incident — see R-0003)
- What sample size / error control is required before a change may be called an improvement?
  (`H-0010`, R-0002 Q2, E-0010's power analysis)

## Current Known Problems
- ~~No search or evaluation yet — the engine only does board + move generation + perft.~~
  RESOLVED: O3a-O3d (search) and E-0010 (tapered eval) are complete and measured.
- No self-play / training pipeline yet (E-0011, next milestone). Raw self-play data exists
  only as E-0010's local match evidence (1.31 MB, gitignored) — not a dataset pipeline.
- ~~`kana_o2.exe` in build/Release (253,952 B) has unrecorded build-provenance — excluded
  from claims (D-0002).~~ RESOLVED 2026-09-10: quarantined as `kana_o2.exe.QUARANTINED-D0002`;
  the certified /O2 baseline is the in-tree E-0002 harness (flags + self-SHA-256 logged).

## Recent Important Experiments
- **E-0011 (COMPLETED, PASS — dataset gates only):** the replacement self-play campaign
  produced 1,000 legal, provenance-carrying JSONL games with zero duplicate move-lists;
  the recorded kill/resume at game 400 and truncation drill passed. Dataset SHA-256:
  `27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95`. This artifact result
  makes no strength assertion; independent verification is requested by HO-0009.
- **E-0010 (COMPLETED, verdict FAIL — honest):** tapered hand-tuned eval vs material-only.
  Gates (a) perft+legality PASS, (b) symmetry PASS (0 full-mirror violations, stages 0-6),
  (d) NPS PASS (43.25 vs 31.95 Mnps, i.e. faster). Gate (c) **FAIL on effect size only**:
  stage-6 beats stage-0 by **+116.1 Elo, LOS 100.00%, CI95 [+70.8, +163.5], N=240
  independent games** (0 duplicate move-lists; 1240/1240 legal) — below the pre-registered
  ≥150 bar. Per-term ladder vs stage-0: k1 +36.3, k2 +82.3, k3 +104.5, k4 +100.8,
  k5 +127.6, k6 +116.1. Mobility and tempo are non-positive; taper + PST + pawn structure
  carry the strength. Reproducible with `python e0010_report.py`.
- **E-00009 (COMPLETED, PASS):** TT + iterative deepening + time control + repetition —
  9.5x fewer nodes than O3c at depth 6, 11/11 best moves identical.
- **E-0002 (COMPLETED, PASS):** certified `/O2` NPS baseline 43-47 Mnps (`--bench 5`, pinned,
  SHA-256 logged); O3 unblocked.
- Earlier: E-00006 (O3a plain AB), E-00007 (O3b ordering, -91.2% nodes), E-00008 (O3c
  quiescence), E-00003 (provisional /O2-vs-/Od, superseded by E-0002 for citation).

## Current Champion
Engine (O3d + E-0010 eval, i.e. ordered AB + quiescence + TT + iterative deepening +
tapered hand-tuned eval at `EvalStage=6`) plays complete legal timed games: **2/2 self-play
games 100 % legal at 200 ms/move** (a 234-ply draw and a 77-ply checkmate finish),
**30/30 wins (100 %) vs legal-move-uniform random mover, 30/30 legal** at depth 4, `stop`
latency max 15.1 ms, and **9.5x fewer nodes than the O3c single-shot at depth 6** (5.11 M vs
48.6 M over the 11-position E-00007 set) with identical best moves. Search efficiency
(91.2 % node cut, O3b) + tactical leaf accuracy (qsearch, O3c) + TT/ID node reduction
(9.5x, O3d) are the baselines for every later delta. The eval adds **+116.1 Elo over
material-only at LOS 100.00 % (N=240 independent games, E-0010)** — significantly positive,
below its pre-registered ≥150 bar.

## Current Known Problems
- Evaluation exists and is measured (E-0010: +116.1 Elo over material-only at LOS 100%,
  below its pre-registered ≥150 bar). Mobility and tempo are non-positive increments and
  need re-tuning (H-0013 Texel fitting), not more hand weights.
- E-0011 provides a local, gitignored 1,000-game self-play dataset with a pinned SHA-256
  and all six artifact gates PASS; W-0001 is DONE and independently VERIFIED (R-0017,
  2026-09-25). The dataset is consumable only under its leakage contract (distinct salt,
  overlap-0 gate); no fitted parameters or downstream strength result are claimed yet.
- ~~No comparison harness~~ **RESOLVED 2026-09-25 (E-0012 PASS, W-0005 DONE, VERIFIED by
  R-0018):** the E-SPRT-lite comparison harness (`tools/e0012_sprt.py`) is built and live-
  validated — known-difference (stage 6 vs 0) H1 accepted at game 125 ∈ pre-registered
  [80, 800]; N4 null-pair (6 vs 6, cap 240) produced no H1 with the colour-corrected
  null band; 0 duplicates, 365/365 games legal, contract frozen end-to-end. This licenses
  no engine-strength claim; future A/B claims now have a pre-registered decision harness.
- No persistent TT across moves (TT is cleared per `go`); no aspiration/PVS/LMR/null-move
  (O3e candidates).
- **2026-09-23 — Gate 0 UNBLOCKED (F-0002 condition ended).** The owner changed the App
  Control/WDAC policy; an orchestrator probe ran `build\Release\kana.exe` to completion
  (exit 0) with the default perft suite passing (startpos d1–d5 exact, kiwipete d3,
  cpw_pos3/4 d4) — attempt #9 on record (`research/failures/F-0002-*`). Engine-level
  work (self-play pipeline, live SPRT validation) is executable on this host again;
  F-0002 stays RECORDED as a failure class against policy regression.

## Current Development Priorities
1. ~~E-0011 independent verification~~ **DONE 2026-09-25:** R-0017 VERIFIED; W-0001 closed.
2. ~~E-SPRT-lite harness~~ **DONE 2026-09-25:** E-0012 COMPLETED (result PASS — harness
   validation), W-0005 DONE and VERIFIED by R-0018 (independent re-derivation of
   RUN-0002/RUN-0003). The harness is now the standing decision rule for A/B claims.
3. **O3e — PVS / LMR / null-move** measured against the O3d baseline once (2) exists.
4. **Phase 3+ — learning:** Texel-fit the hand-tuned terms (H-0013), then NNUE; use the
   verified E-0011 dataset only after downstream leakage checks pass.

## Last Updated
2026-09-25 (verification chain closed: R-0017 VERIFIED → W-0001 DONE (E-0011 1,000-game
dataset); E-0012 live validation executed under HO-0011 — RUN-0002 known-difference H1 @
game 125 ∈ [80, 800], RUN-0003 N4 null no-H1 at cap 240, colour-corrected band pass —
independently verified by R-0018 (VERIFIED); W-0005 DONE; E-0012 COMPLETED (result: PASS,
harness-validation scope only). No training started; H-0013 still needs its own
pre-registration + critique gate.)
2026-09-24 (S-0015: E-0011 replacement campaign completed 1,000-game dataset generation;
all six artifact gates PASS; RUN-0001 terminal hashes and kill/resume evidence recorded;
HO-0009 requested from verification-auditor; E-0012 remains PENDING)
2026-09-21 (W-0002: E-0010's decision rule recalibrated — D-0007 RESOLVED by arithmetic
over measured variance; DEC-0010 ACTIVE [screening/regression/magnitude tiers, LLR
±2.944, caps 8k/30k/8k, post-cap INCONCLUSIVE]; R-0009 restates E-0010 under the
calibrated rule [screening PASS, regression PASS, "≥150" not established at N=240];
Gate 0 remains hard-blocked, F-0002; W-0002 IN_PROGRESS pending independent verification
via HO-0002)
2026-09-14 (E-0010 tapered eval COMPLETE and measured — gates (a)(b)(d) PASS, gate (c)
honest FAIL at +116.1 Elo / LOS 100.00% / N=240; project memory corrected for staleness;
perft anchor given a single protected home in this file; verification/coordination layer
ratified in DEC-0009 and described in `research/SYSTEM.md`)
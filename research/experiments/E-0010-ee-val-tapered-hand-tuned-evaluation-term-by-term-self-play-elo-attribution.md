---
id: E-0010
type: experiment
title: "E-EVAL — Tapered Hand-Tuned Evaluation (term-by-term self-play Elo attribution)"
status: PENDING
result: null
elo_change: null
hypothesis: H-0004
priority: high
example: false
created: 2026-09-13
completed: null
tags: [eval, tapered, self-play, elo]
---

# E-0010 — E-EVAL: Tapered Hand-Tuned Evaluation

## Hypothesis
A tapered (MG/EG interpolated), symmetric, hand-tuned evaluation function with named
tuneable coefficients will yield ≥150 Elo over the material-only baseline at LOS ≥95%
over ≥200 fixed-seed games @100ms+inc, with NPS drop ≤30% vs the O3d build.

## Baseline
- Material-only leaf eval: `VALUE[pt] * popcount(pieces[c][pt])` summed per side, returned
  from side-to-move perspective. Located at `src/search.cpp:109-115`.
- Build: `build.bat Release` (O3d — iterative deepening + TT + time control + repetition/50-move).

## Candidate
- New `src/eval.h` + `src/eval.cpp` module with:
  - `EvalCoeffs` struct exposing every coefficient as a named, tuneable constant.
  - Tapered eval: `score = (mg * phase + eg * (24 - phase)) / 24`.
  - 6 terms added incrementally (one commit per term):
    1. Game-phase taper wrapping material.
    2. MG/EG PSTs mirrored for Black.
    3. Pawn structure (doubled, isolated, passed).
    4. Enemy-pawn-discounted mobility.
    5. Bishop pair / open file / semi-open file / 7th rank / king shield / king centralization.
    6. Tempo.
  - `EvalStage` UCI option (spin 0..6) for per-term Elo attribution.
  - Symmetry self-test (debug): `eval(b, WHITE) == -eval(flip(b), WHITE)`.

## Difference
- Replaces the static `evaluate()` in search.cpp with `kana::evaluate()`.
- Adds `EvalStage` UCI option (default 6 = full eval).
- Adds symmetry assert in debug builds.

## Hardware
- Single machine, fixed CPU, no GPU.

## Engine Version
- Kanamecide, master branch, post-O3d (E-00009).

## Network
- N/A (classical eval).

## Dataset
- Self-play games: fixed-seed, 100ms + 100ms increment, alternating colors.

## Test Method
1. Build Release (O3d) — this is the measurement baseline binary.
2. Run perft (10/10 positions) — must be bit-identical after each term.
3. Run symmetry test on 1000 random positions.
4. For each term k (1..6): build with `EvalStage=k`, run 200-game self-play match
   vs `EvalStage=0` (material-only), record Elo delta.
5. Final: 200-game match of `EvalStage=6` (full) vs `EvalStage=0` (material-only).

## Games / Samples
- Per term: 200 games (100 as White, 100 as Black).
- Final: 200 games full vs material-only.
- Symmetry: 1000 random positions.

## Metrics
- Elo difference (Bayesian, LOS).
- NPS (nodes per second) — must not drop >30% vs O3d.
- Perft node counts — must be bit-identical.
- Symmetry violations — must be 0.

## Pre-Registered Decision Rule (PASS requires ALL)
(a) Perft bit-identical (10/10 positions) + 100% legal games in self-play.
(b) Eval symmetry `eval(b) == -eval(flip(b))` on 1000 random positions (0 violations).
(c) ≥150 Elo vs material-only at LOS ≥95% over ≥200 fixed-seed games @100ms+inc.
(d) NPS drop ≤30% vs O3d build.

## Results
TBD

## Statistical Analysis
TBD

## Interpretation
TBD

## Conclusion
TBD

## Follow-Up
- H-0013: Texel fitting (deferred — out of scope for E-0010).
- SPRT harness (deferred).
- NNUE (deferred).

## Orchestrator Addendum (2026-09-13)
**STATUS: PENDING — first implementation attempt was COMPILE-ONLY, NOT VALIDATED.**
The `eval.cpp/h` code and wiring (search.cpp:116,163; main.cpp:114; CMakeLists:28) were written but
**never executed**: the run was blocked by the Device Guard / Smart App Control executable block on
this machine, and no gate was measured. Compilation validates syntax, NOT correctness,
symmetry, speed, or strength — the pre-registered decision rule (perft bit-identical, symmetry
0 violations, ≥150 Elo @ LOS≥95% over ≥200 games, NPS drop ≤30%) is **entirely UNRUN**.
Work is **UNCOMMITTED**. The milestone is NOT complete; the next implementation-engineer session
must (1) build and RUN Release (use retry_rel.bat / rebuild loop to get past the transient EXE
block), (2) run perft + symmetry + self-play Elo + NPS gates per this record, (3) fill Results/
Statistical Analysis/Conclusion, (4) commit, and (5) clean the session scratch in the repo root.
Do not treat an un-ran compile as a result.

### Update (2026-09-13 ~22:11, orchestrator verified)
Second attempt made real progress on two gates but did **NOT** complete the milestone:
- **Gate (a) perft bit-identical: PASS (verified)** — `evd_perft_rel.txt` shows 10/10 positions
  (startpos d1-5, kiwipete d3, cpw3-6) with exact expected counts on the rebuilt Release binary.
- **Gate (b) symmetry: PASS (claimed, not independently re-verified this pass)** — agent reports
  `full_mirror_viol=0` across stages 0-6 on 1000 positions.
- **Gate (c) ≥150 Elo: NOT RUN TO COMPLETION.** Self-play matches (e0010_match.py, 6 concurrent
  stage-vs-stage-0, 200 games each) repeatedly hit `BAD TIMEOUT` — the engine stops emitting
  `bestmove` mid-search (e.g. k6 g26, k1 g32) and the 5s Python watchdog declares the move lost.
  The runs died around game ~26-32 of 200. The "detached" watchdog (`e0010_watchdog.py`) was
  killed: `_watchdog_py.txt` contains `^C`, and `Get-Process python` shows **0** python processes.
  **`e0010_k{1..6}_result.txt` do NOT exist**, so no Elo/LOS was ever computed.
- **Gate (d) NPS: NOT RUN** (clean uncontended `--bench` never fired).
- **Commit: NONE.** HEAD is still `962368b` (O3d). `src/eval.{h,cpp}`, `main.cpp`, `search.cpp`,
  `CMakeLists.txt`, `index.md` and all `e0010_*` harness files remain uncommitted (~100 scratch files).

**Root cause to fix next:** the engine's time-control `bestmove` path stalls (searches a depth,
emits `info` lines, then never flushes `bestmove` before the wall-clock deadline) under
~100ms+100ms inc with 6-way CPU contention. Gate (c)/(d) CANNOT be measured until `bestmove` is
guaranteed to be emitted on time. Do NOT re-launch a 45-minute detached match run; the detached
process is not surviving agent shell turnover on this machine.

### Update 2 (2026-09-14, orchestrator verified)
Third attempt: **real engineering progress, but the milestone's decisive gates are STILL unmeasured.**
- **CRITICAL BUG FOUND (verified in src/main.cpp:124-145):** `setoption` was a silent no-op —
  EvalStage was never applied, so every prior "stage K vs stage 0" match was actually
  **stage-6 vs stage-6**. All previous gate-(c) data was methodologically void. Fixed: the parser
  now consumes all tokens and applies every (key,value) pair; `EvalStage -> kana::set_eval_stage`.
- Also fixed: terminal positions emitted bogus `bestmove a1a1` (now `0000`); time-budget margin.
- New in-process symmetry harness (`--symmetry`, `run_symmetry`, `build_mirror`) using
  `set_eval_stage` directly — gates (b) is now properly testable per-stage, but there is **no
  evidence it was re-run across stages 0-6 after the setoption fix**. Re-run required.
- **Crash regression: PASS (verified).** `_repro_match_m1_result.txt`: 6 pairs x 40 games,
  stage-6-vs-stage-0, `VERDICT=ALL-CLEAN`, zero stalls/illegal/timeouts through g39.
- **Gate (c) Elo: STILL NOT RUN.** The 240-game run was a crash-repro at 40 games/pair, NOT the
  pre-registered measurement. `e0010_report.py` never executed; `e0010_k{1..6}_result.txt` absent;
  no Elo/LOS/CI exists. Two disqualifying flaws in the sample: (i) engines are deterministic with
  a fixed startpos and no opening randomization, so the 6 pairs played largely DUPLICATE games
  (identical ply counts/times recur across pairs — effective independent N is ~40-60, not 240);
  (ii) the verdict is a legality verdict, not an Elo verdict.
- **RED FLAG for gate (c):** in the m1 sample, B (stage-0, material-only) wins the large majority
  of decisive games over A (stage-6, full eval). If this holds on a valid independent sample, the
  hand-tuned eval LOSES to material-only at this time control and gate (c) FAILS. Must be measured
  honestly — not assumed away.
- **Gate (d) NPS: NOT RUN** (no uncontended `--bench` evidence).
- **Record: Results/Statistical Analysis/Conclusion still TBD; status still PENDING.**
- **Commit: NONE.** HEAD still `962368b`; ~100 scratch files in repo root.

**Next session must:** add opening variety to the self-play harness (else games are duplicates and
any Elo is invalid), run >= 200 INDEPENDENT games stage-6 vs stage-0, compute Elo/LOS/CI via
e0010_report.py, run gate (d) uncontended NPS, re-run symmetry per stage post-fix, fill E-0010
honestly (PASS or FAIL — a FAIL is an acceptable, publishable verdict), commit, and clean scratch.

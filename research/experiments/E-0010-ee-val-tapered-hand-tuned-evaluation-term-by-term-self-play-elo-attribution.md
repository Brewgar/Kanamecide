---
id: E-0010
type: experiment
title: "E-EVAL — Tapered Hand-Tuned Evaluation (term-by-term self-play Elo attribution)"
status: COMPLETED
result: "FAIL (pre-registered gate (c) effect size; direction significantly positive). Gates (a),(b),(d) PASS. gate (c): stage-6 (full tapered eval) beats stage-0 (material-only) +116.1 Elo (LOS 100.00%, CI95 [+70.8,+163.5], N=240 independent games, 1240/1240 legal) but does not clear the pre-registered >=150 Elo bar. Per-term ladder vs stage-0: k1 +36.3, k2 +82.3, k3 +104.5, k4 +100.8, k5 +127.6, k6 +116.1 (N=240)."
elo_change: "+116.1 (stage-6 vs stage-0, N=240 independent, LOS 100.00%, CI95 [+70.8,+163.5]) — significantly positive, below the >=150 gate"
hypothesis: H-0004
priority: high
example: false
created: 2026-09-13
completed: 2026-09-14
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

Measured 2026-09-14 (campaign run 2026-09-13 23:39 → 2026-09-14 01:16, elapsed 5807s ≈ 97 min).
Measurement binary `build\Release\kana.exe`, **SHA256
`504EB01A828770DD9BFCA252AB8245A5692DF51580957CB6E5553012347A6DAA`**, self-reports
`git commit: 962368b` — that is the HEAD pointer at build time (2026-09-13 23:39, the
parent of the commit below), but `src/` is byte-clean against HEAD `9b69e0a`, the commit
that added `src/eval.cpp` and the crash-fixed `src/search.cpp`, so the **measured sources
== HEAD `9b69e0a`**. Compile flags (bench header): /O2 /GL /EHsc /arch:AVX512 /DNDEBUG.
Opening randomization: **10 random legal plies from startpos per game**, python-chess
legal-move RNG, seed = `random.Random(20260914 * 1000003 + game_index)`, the same opening
sent to both engines as `position startpos moves <uci...>`, colors balanced. All matches 100ms+100ms inc (O3d time formula), max 2 engine-pairs
concurrent, per-game JSONL incremental flush. Full campaign = **1240 games, 0 bad
(illegal) games, no stalls**.

### Independence evidence
The aggregator (`e0010_report.py`) rebuilds every game's full move list (opening + game
moves) from the per-game JSONL and counts duplicate lists:

| match  | games | duplicate move-lists |
|--------|-------|----------------------|
| k1n..k5n | 200 each | 0 |
| k6n      | 240      | 0 |

**0 duplicates across all 1240 games → all samples independent** (vs the m1 campaign's
~40-60 effective N from duplicated startpos games).

### Gate (a) — perft + legality: PASS
- Perft on the measurement binary: **10/10 positions PASS, 0 diff** (bit-identical).
- Self-play: **1240/1240 legal games** (bad=0 in every match).

### Gate (c) — stage-6 vs stage-0 Elo (the pre-registered measurement)
k6n match, N=240 independent games: **W=144 L=66 D=30** (A = stage-6 full eval,
B = stage-0 material-only). **Elo = +116.1** (Bayesian +116.1), **CI95 = [+70.8, +163.5]**,
**LOS = 100.00%**, raw win rate 144/240 = **0.600**, score with draws as halves 0.662.
Verdict per the pre-registered rule: **FAIL**
(N≥200 ✓, LOS≥95% ✓, 100% legal ✓, independent ✓, Elo≥150 ✗).
The m1 "red flag" (material-only winning) is **reversed** on the valid independent sample.

### Per-term ladder (all vs stage-0, 100ms+100ms inc, same protocol)

| stage | increment added                  | W/L/D    | Elo           | CI95               | LOS     |
|-------|----------------------------------|----------|---------------|--------------------|---------|
| 0     | material-only (reference)        | —        | 0 (by def.)   | —                  | —       |
| 1     | + game-phase taper               | 85/64/51 | +36.3         | [-11.7, +84.9]     | 93.08%  |
| 2     | + MG/EG PSTs                     | 101/54/45| +82.3         | [+33.8, +132.6]    | 99.96%  |
| 3     | + pawn structure                 | 116/57/27| +104.5        | [+55.3, +155.9]    | 100.00% |
| 4     | + mobility                       | 120/63/17| +100.8        | [+51.7, +151.9]    | 100.00% |
| 5     | + bishop pair / open file / etc  | 122/51/27| +127.6        | [+77.5, +180.3]    | 100.00% |
| 6     | + tempo (full eval, N=240)       | 144/66/30| +116.1        | [+70.8, +163.5]    | 100.00% |

### Gate (b) — eval symmetry (post-fix, 1000 positions x stages 0-6): PASS
full-mirror violations = **0 at every stage 0-6**. (keep_side violations = 0 at stages
0-5 and 1000/1000 at stage 6, which is expected: the tempo term is a side-to-move bonus —
symmetric under the 180-degree full mirror (side flips) but not negatable under a
geometry-only flip (side held). The binding chess-symmetry gate is full_mirror.)

### Gate (d) — NPS on the match binary, uncontended: PASS
`--bench 5` after all matches finished: case means 43.42 / 42.74 / 43.56 / 41.27 /
45.28 Mnps → **mean 43.25 Mnps** vs the recorded O3d baseline 31.95 Mnps →
**drop = -35.4%** (i.e. ~35% faster); the <=30%-drop requirement is met with margin.
Note: the eval-enabled binary measured *faster* than the recorded O3d baseline; part of
the delta is session-to-session run-condition noise, but no NPS regression is present.

## Statistical Analysis

- **Estimator** (`e0010_elo.py`): draws counted as halves. With Wp = W+D/2, Lp = L+D/2 the
  effective win probability q of stage-K vs stage-0 gets a uniform Beta(1,1) prior →
  posterior q ~ Beta(a,b) with a = Wp+1, b = Lp+1 (Laplace +1 smoothing).
  LOS = P(q > 0.5) = 1 - I_0.5(a,b) via the regularized incomplete beta (Numerical-Recipes
  continued fraction). Elo point = 400*log10(a/b); the "Bayesian" point
  400*log10(mean_q/(1-mean_q)) is **algebraically identical** (mean_q/(1-mean_q) = a/b), so
  the two always agree exactly, not merely approximately. The 95% credible interval is the
  Beta(a,b) quantile pair (0.025 / 0.975, binary search on I_x) mapped by 400*log10(q/(1-q)).
- **k6 (gate c), N=240:** W=144 L=66 D=30, raw win rate 0.600, score Wp/N = 0.6625 →
  a = 160, b = 82, posterior mean q = 160/242 = 0.6612 → **Elo +116.1** = 400*log10(160/82),
  95% CI [+70.8, +163.5], LOS = 1 - I_0.5(160, 82) = 100.00%. The interval **straddles
  the pre-registered +150 bar** (upper 163.5 > 150 > lower 70.8): the data establish a
  significant positive effect but cannot confirm >=150 at this N.
- **Ladder shape:** cumulative +36.3 → +82.3 → +104.5 → +100.8 → +127.6 → +116.1 (N=240).
  Largest single increments: PST (+46.0), taper (+36.3), bishop-pair group (+26.8),
  pawn structure (+22.2). Two non-positive increments: mobility (−3.7) and the k5→k6
  tempo step (−11.5). The k6 run used 240 games (vs 200 elsewhere) — narrower CI; the
  k5 and k6 CIs overlap heavily ([+78,+180] vs [+71,+164]).
- **Power:** at N=200 with score ≈0.60 the CI half-width is ≈±48 Elo. Distinguishing a
  true +116 from a true +150 needs roughly N≈700-900 per pair (half-width ≈25-30 Elo);
  the campaign was sized to the pre-registered N>=200 minimum, not to resolve 116-vs-150.
- **Multiplicity caveat:** per-term ladder CIs are unadjusted; the two non-positive
  increments (k4, k5→k6) have CIs crossing zero and should be read as "no evidence of
  gain at this N", not as proven harm.

## Interpretation

- The hand-tuned tapered eval is **significantly stronger than material-only** under this
  protocol (LOS 100%, CI lower bound +71 Elo). The pre-crash m1 sample's suggestion that
  material-only wins was an artifact of duplicated startpos games and is reversed here.
- The gain is **front-loaded**: taper (+36.3) then PST (+46.0 incremental) already give
  +82.3 after k2; pawn structure adds +22.2 to reach +104.5; everything after k3
  (mobility, bishop-pair group, tempo) nets only ≈ +12 Elo with two non-positive steps.
  Most of the final strength comes from three terms.
- The k4 (mobility) and k5→k6 (tempo) increments are non-positive with CIs crossing zero:
  at this time control and N, those hand-tuned weights are not earning their eval cost.
- The failure mode is **effect size below the pre-registered threshold** — not "no effect"
  and not "material-only wins": gates (a), (b), (d) all PASS.

## Conclusion

**Verdict: FAILED** — honest, per the pre-registered decision rule (PASS requires ALL
conjuncts). Gate (c) measured: **+116.1 Elo, LOS 100.00%, N=240 independent games,
1240/1240 legal** — the LOS / N / legality / independence conjuncts pass, the
effect-size conjunct fails (+116.1 < 150; CI95 [+70.8, +163.5] straddles +150, so >=150
cannot be confirmed at this sample size). Gates (a) perft+legality, (b) symmetry
(0 full-mirror violations, stages 0-6), and (d) NPS (43.25 vs 31.95 Mnps baseline,
−35.4% "drop" = faster) all **PASS**. Note on the taxonomy and on the front-matter
encoding: under the orchestrator's buckets this outcome sits between FAILED (stage-6
losing — not our case) and INCONCLUSIVE (CI95 straddles +150 — true, but with LOS 100%,
not <95%); the **verdict is FAILED** because the pre-registered PASS conjunction is
objectively not met, while the direction is significantly positive. The front-matter
field `status` is the *lifecycle* field in this repo's memory tool (`research.py`:
PENDING / RUNNING / COMPLETED — any other value silently drops the record from the
generated `research/index.md`), so E-0010 carries `status: COMPLETED` and the FAILED
verdict lives in `result:` ("FAIL (pre-registered gate (c) effect size…)", shown by
`research.py experiments`) and in this Conclusion.

**What the per-term ladder implies:** strength is concentrated in taper + PST (+82.3
cumulative after k2) plus pawn structure (+22.2); the later hand-tuned terms (mobility,
bishop-pair group, tempo) collectively add only ≈ +12 Elo with two non-positive
increments (mobility −3.7, tempo −11.5, both CIs crossing zero) — at 100ms+100ms they
are not earning their eval cost, and the >=150 target was never going to be confirmed
at N=200-240 with CI half-width ≈±47. The >=150 threshold itself was a pre-registered
guess; the measured +116 at LOS 100% may already justify shipping the eval, but that is
a decision-rule change and belongs to the adversarial reviewer, not to this experiment.

## Follow-Up
- H-0013: Texel fitting (deferred — out of scope for E-0010).
- SPRT harness (deferred).
- NNUE (deferred).
- **E-0010 routing (2026-09-14, from the measurement):** (1) Re-tune the later-term
  weights — mobility and tempo are the non-positive ladder increments; prefer Texel
  fitting on quiescence-search positions (H-0013) over further hand weights. (2) If the
  >=150 decision rule is kept, re-run stage-6 vs stage-0 at N≈700-900 per pair
  (CI half-width ≈25-30 Elo) to confirm/refute the +116 point estimate before spending
  further tuning effort; otherwise take the rule (and the measured +116 @ LOS 100%)
  back to the adversarial-reviewer for recalibration. (3) Do NOT prioritize shrinking
  eval cost — gate (d) shows a ~35% NPS improvement, so eval cost is not the binding
  constraint. (4) Attribution payload delivered regardless of the stage-6 verdict:
  taper/PST/pawn-structure carry the strength; mobility/tempo need re-tuning.

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

### Update 3 (2026-09-14, implementation-engineer)
**Measurement campaign designed and launched with independent openings. Methodology first:**

- **Opening randomization scheme (fixes the disqualifying flaw):** `e0010_match2.py` generates each
  game's opening by playing **10 random legal plies from startpos** with python-chess, RNG seeded
  deterministically as `random.Random(20260914 * 1000003 + game_index)`. The full move list is sent
  to BOTH engines as `position startpos moves <uci...>` (they search from the randomized position).
  Colors balanced by alternating which engine takes White per game. Fully reproducible given the
  binary + seeds. **Independence verified post-hoc:** the aggregator (`e0010_report.py`) rebuilds
  every game's full move list (opening + game moves) from the per-game JSONL and reports duplicate
  count — requirement: 0 duplicates across all matches (see Results).
- **Campaign:** 6 matches, same-exe pipe drivers, stage-K vs stage-0 for K=6,1,2,3,4,5
  (k6n: 240 games; k1n..k5n: 200 games each), 100ms+100ms inc via the O3d time formula
  (`go wtime 1500 btime 1500 winc 100 binc 100`), max **2 engine-pairs (4 processes) concurrent**
  (the original stall cause was 12 engines), launched detached via `Start-Process`
  (`e0010_run_all.py`); per-game incremental JSONL flush + `*_done.txt` sentinels so partial data
  survives shell turnover. Binary: `build\Release\kana.exe` SHA256
  `504EB01A828770DD9BFCA252AB8245A5692DF51580957CB6E5553012347A6DAA`.
- **Pre-flight:** 6-game smoke of the new driver: 6/6 legal, no stalls, varied plies (52-218).
- Gates (b) symmetry (stages 0-6, 1000 positions each) and (d) uncontended `--bench 5` are chained
  to fire automatically only after ALL matches finish (`e0010_wait_then_bd.py`), so they never
  contaminate match timing.
- Results: TBD (campaign in flight).

**Methodological commitment: gate (c) is an Elo verdict, not a legality verdict. A FAILED verdict
(stage-6 losing to material-only) is an acceptable, publishable outcome and will be recorded as such.**

### Update 4 (2026-09-14, implementation-engineer) — MEASUREMENT COMPLETE
**All four gates measured for real. Campaign: 1240 independent games, 0 bad games,
max 2 engine-pairs concurrent, no stalls.**

- **Opening randomization (Phase-1 fix):** 10 random legal plies from startpos per game,
  python-chess legal-move RNG, seed `random.Random(20260914*1000003+game_index)`, same
  opening to both engines via `position startpos moves <uci...>`, colors balanced.
  **Independence verified: 0 duplicate full move-lists across all 1240 games** (the
  aggregator rebuilds each game's move list from the per-game JSONL).
- **Gate (a): PASS.** Perft 10/10 bit-identical on the measurement binary;
  1240/1240 legal self-play games.
- **Gate (c): FAIL (honest, pre-registered rule).** Stage-6 vs stage-0, N=240
  independent: W=144 L=66 D=30, **Elo +116.1** (Bayesian +116.1), CI95 [+70.8, +163.5],
  LOS 100.00%. LOS/N/legality/independence conjuncts pass; the effect-size conjunct
  fails (+116.1 < 150; the CI straddles +150, so >=150 is not confirmed at this N).
  The m1 red flag (material-only winning) is REVERSED on the valid sample — stage-6
  wins decisively — but not by >=150. Per-term ladder (all vs stage-0, N=200 each):
  k1 +36.3, k2 +82.3, k3 +104.5, k4 +100.8, k5 +127.6, k6 +116.1 (N=240). Attribution:
  strength is concentrated in taper + PST (+82.3 after k2) + pawn structure (+22.2);
  mobility (−3.7) and tempo (−11.5) are non-positive with CIs crossing zero.
- **Gate (b): PASS.** `--symmetry` on the match binary, 1000 positions x stages 0-6:
  **0 full-mirror violations at every stage** (keep_side = 1000/1000 at stage 6 only,
  expected and documented: tempo is a side-to-move bonus; full_mirror is the binding gate).
- **Gate (d): PASS.** Uncontended `--bench 5` on the match binary after all matches:
  mean **43.25 Mnps** vs recorded O3d baseline 31.95 Mnps → drop **−35.4%** (faster),
  <=30% met with margin. (A parser unit bug in e0010_gates_bd.py compared Mnps against
  raw nps and printed a bogus drop=100.0%; fixed to convert the baseline to Mnps.)
- **Record:** Results / Statistical Analysis / Interpretation / Conclusion / Follow-Up
  filled; frontmatter `status: COMPLETED` (lifecycle) with `result:` = "FAIL
  (pre-registered gate (c) effect size; direction significantly positive)…" — the verdict
  is carried by `result`, not by `status`, because `research.py`'s experiment status
  vocabulary is PENDING / RUNNING / COMPLETED and an out-of-vocabulary status silently
  removes the record from the generated index (observed and fixed this session).
  `elo_change` and `completed=2026-09-14` set. `hypothesis: H-0004` left OPEN — E-0010
  measures the eval's delta vs material-only, not absolute 2500+ strength.
- **Hygiene / artifacts:** per the Round-3 convention (raw scratch is external evidence —
  "keep them locally, keep them out of git history"), the raw measurement artifacts stay
  **local and gitignored** (new `.gitignore` E-0010 block): `e0010_k{1..6}n_games.jsonl` +
  `e0010_k{1..6}n_result.txt` (1.31 MB — exactly the data `e0010_report.py` re-aggregates),
  `e0010_gates_bd.txt` (gates b+d raw output), `_g0_perft.txt` (gate a raw output),
  `e0010_runner_log.txt` + `e0010_ALL_done.txt` (wave schedule + elapsed 5807s ≈ 97 min).
  Deleted: per-match done-markers, `*_log.txt` / `*_err.txt` dumps, smoke/waiter/gbd
  scratch, `_chtest.py`. Already committed in `9b69e0a` and therefore left as-is: the
  earlier m1-campaign logs `e0010_k1..k6.txt`, `e0010_k{1..6}_err.txt`,
  `e0010_pilot6_err.txt`. Retained (committed) harness scripts: e0010_match.py,
  e0010_match2.py, e0010_report.py, e0010_elo.py, e0010_run_all.py, e0010_gates_bd.py,
  e0010_wait_then_bd.py, e0010_watchdog.py, e0010_repro_match.py, repro_stall.py.
- **Code state / commits:** the measured code is committed as `9b69e0a` ("E-0010 tapered
  eval + self-play elo attribution: add eval.cpp/.h, e0010 harness scripts, …"); the
  measurement binary's embedded `git commit: 962368b` is the HEAD pointer at build time
  (its parent). Results, harness scripts and the regenerated index are committed in
  `b5b3cf2`.
- **Re-verification at record time:** `python e0010_report.py` was re-run after the
  campaign and reproduced every number in this record exactly (per-stage Elo/CI/LOS,
  0 duplicate move-lists at every stage, gate (a) legality PASS, gate (c) FAIL); gate (a)
  was re-run live on the same binary (10/10 perft, 0 diff, "ALL TESTS PASSED") and the
  binary SHA256 was confirmed unchanged; `python research.py validate` reports OK.

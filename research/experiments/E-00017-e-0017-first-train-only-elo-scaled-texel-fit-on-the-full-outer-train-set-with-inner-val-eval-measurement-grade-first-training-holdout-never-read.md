---
id: E-00017
type: experiment
title: E-0017 first TRAIN-only Elo-scaled Texel fit on the full outer-train set with inner-val eval (measurement-grade first training; holdout never read)
status: COMPLETED
result: TRAINING-GATE PASS — inner-val improvement 0.036211 (CI95 [0.023754, 0.048668] above zero), s_d 0.078509, MAE fitted 0.245440 < floor 0.262752 (watch CLEAN), mirror 0/1000, arms differ (1de93a39 vs 711c460d), frozen intact, convergence nit=10, determinism proved (double-fit + resume byte-identical); first learned artifact 1de93a39 pinned; no strength claim licensed
elo_change: null
hypothesis: H-0013
priority: high
owner: researcher-architect
pre_registered: 2026-10-07
example: false
created: 2026-10-07
completed: 2026-10-08
tags: [texel, elo-scale, first-training, train-only-first, pre-registration, y-2-follow-up]
---

# E-00017 — E-0017 first TRAIN-only Elo-scaled Texel fit on the full outer-train set with inner-val eval

> Filed by researcher-architect, 2026-10-07, under DEC-0015 (the Y-2
> named re-decision). **NOTHING HAS RUN.** No extraction, no fitting, no
> holdout read, no SPRT game. This record is PENDING and may not be
> flipped to RUNNING by its author. Executor seat: **systems-researcher**,
> under HO-0029 (executor appends Response; a fresh verification-auditor
> appends Verification).
>
> **Why this record exists.** E-0016 stage (a) routed Y-2
> (INCONCLUSIVE-BY-POWER): the Elo-scaled objective is sound (no
> collapse signature) but the 155-game inner-val partition cannot decide
> the fixed holdout margin. DEC-0015 therefore blocks any holdout-gated
> stage (b) and owns the next step instead: the first complete training
> run of the authorized pipeline on the FULL outer-train set (791 games /
> 59,892 rows), evaluated on the already-carved inner-val partition (155
> games). This is the minimum scientifically valid first training: same
> objective, same model family, same optimizer, same pins — one new fit
> surface, pre-registered openly.

## Hypothesis

Under the Elo-scaled objective `sigmoid(clip(E/D, -L, L))` with the FIXED
scale `D = 400/ln(10)` (pinned by E-0016, derived from the Elo identity,
not fitted), the deterministic full-batch L-BFGS optimizer fitted on the
full TRAIN side (791 games / 59,892 rows) produces a parameter table that
beats the frozen hand-tuned floor on the TRAIN-side inner-val partition
(155 games, map `93bcd0db…f9e0`, salt 20261007) with the MAE pathology
watch clean (fitted MAE not worse than floor MAE while fitted loss is
better). The holdout is never read; no holdout quantity appears in any
decision below.

## Baseline

The frozen hand-tuned `EvalCoeffs` table as compiled into
`src/eval.cpp:174-234` at the pinned `src/` epoch
`dd4051a92daf834cf4a73f1878a0c894b0b6d1b8` (same-floor discipline as
E-00014/E-0016: floor SHA-256 must equal
`711c460dce3747bf1dcad59eefada488960066c43967f638a818510303b667f1`, or no
number here compares with any number there). Same stage `S* = 6`, same
quiet-proxy predicate, same crash + degenerate-mate exclusions, same
GLOBAL-before-split normalized-FEN dedup (F9 as amended by the S-0037
leakage ruling), same side-to-move label frame (B2 s1).

## Candidate

The parameter set of E-0013's free-parameter list (five non-KING `mg_pst` /
`eg_pst` tables plus items 1 and 3–6; KING PSTs FROZEN per B5; KING
material fixed 20000/20000; taper/phase formula and phase weights frozen
integers), fitted on the FULL outer-train set (791 games / 59,892 rows)
under the Elo-scaled objective, with hyperparameters pinned below.
**The set may not be widened or narrowed by the executor.**

## Difference

The fit surface — and ONLY the fit surface — changes relative to E-0016
stage (a): E-0016 fit on inner-train (636 games / 47,995 rows); E-0017
fits on the FULL outer-train set (791 games / 59,892 rows) and evaluates
paired on the SAME inner-val partition (155 games,
`build/e0016/inner_map.json` role `holdout`, salt 20261007). The inner
map is consumed READ-ONLY; never re-carved, never re-salted. Objective,
optimizer, freeze set, floor, salts, splits, holdout discipline:
unchanged (E-0016 contract by reference).

## Hardware

Single host, CPU only (E-0010/E-0011/E-0012/E-00014/E-0016 precedent); no
engine binary is invoked by the offline training stage. Environment
pinned in the manifest: Python 3.14.6, scipy 1.18.1, numpy 2.5.1,
python-chess 1.11.2. Torch is CPU-only (2.13.0+cpu, cuda=False) and is
NOT used — the authorized optimizer is scipy L-BFGS-B; preflight reports
the device honestly instead of promising GPU determinism.

## Engine Version

No engine binary participates in the offline fit (two PARAMETER TABLES,
not two engines). Pinned `src/` epoch
`dd4051a92daf834cf4a73f1878a0c894b0b6d1b8`; floor bytes must match
`711c460d…667f1`.

## Network

Linear tapered evaluation (E-0013 family): the 683-scalar design vector
over five non-KING `mg_pst[5][64]` / `eg_pst[5][64]` tables plus items 1
and 3–6, KING PSTs frozen, taper/phase frozen integers
(`tools/e0013_eval.py` design_rows / loss_and_gradient). Input: position
terms from `position_terms(board, stage=6)`. Output: side-to-move score
(cp), mapped by `sigmoid(clip(E/D, -L, L))` to a win probability.
Deliberately minimal so the first run proves the pipeline.

## Dataset

- Source: `m0_audit/e0011/games.jsonl`, SHA-256
  `27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95`,
  1000 games.
- Outer split: salt 20260926,
  `random.Random(SPLIT_SALT * 1000003 + game_id).random() < 0.8`, map
  SHA-256 `bb079a41…da1ea`; outer train 792 games / 59,892 rows, outer
  holdout 208 games / 14,560 rows (never read).
- TRAIN-only labels: `build/e0013/labels/labels.jsonl`, SHA-256
  `2bf68bfb…0f7bc2`, 791 games / 59,892 rows (one documented
  degenerate-mate exclusion explains 792 → 791). **Canonical fit input.**
- Fitter corpus (FEN-bearing): `build/e0013/extract/positions.jsonl`,
  SHA-256 `19cee190…31c48f`, 74,452 rows (999 games). Consumed only
  through the TRAIN-only join below — never as a raw input.
- Join rule (new, pre-registered here): fit rows are the extractor rows
  whose `(game_id, norm_fen)` pair appears in the TRAIN-only labels file,
  restricted further to outer-train game ids by the re-derived split
  rule. Only game-id integers and `norm_fen` strings touch the join; a
  holdout game's FEN/label content is never used. Expected: 791 games /
  59,892 rows; any other count is an abort, not a repair.
- Inner map (eval partition, READ-ONLY): `build/e0016/inner_map.json`,
  SHA-256 `93bcd0db…f9e0`, salt 20261007, 636 inner-train / 155
  inner-val, `map ∩ outer_holdout = ∅`.

## Test Method

1. Preflight (`kaname_train.py preflight`): dataset existence + SHAs,
   split identity, holdout exclusion (game-id intersection = 0), model
   construction (683 free scalars, frozen blocks intact), tensor dims,
   optimizer identity, device report, output-dir writability, config
   validity, reproducibility metadata. Fail BEFORE any fit if broken.
2. Dry-run (`kaname_train.py dry-run`): same code path on a tiny
   synthetic subset — load, design-matrix build, forward, loss,
   backward (gradient vs finite diff), one optimizer step, checkpoint
   write + reload, metrics + manifest. No mock-only paths.
3. Training run (`kaname_train.py train --config
   research/manifests/e0017-train-config.json`): deterministic
   full-batch L-BFGS-B (`maxiter 1000`) from theta0 = the frozen floor,
   `--seed` recorded never consumed, in-process double-fit byte-identity
   proof, frozen-block gate, arm-differentiation gate, mirror gate,
   phase checkpointing with resume.
4. Evaluation: paired two-table comparison on inner-val (155 games) via
   `tools/e0013_eval.py` semantics, Elo-scaled, `S* = 6`: paired mean
   improvement, `s_d`, SE, CI95, per-arm means, MAE both arms (pathology
   watch), arm hashes, frozen-block receipt, mirror violations.
5. **THE HOLDOUT IS NOT READ. NOT ONCE.** Holdout game ids are touched
   only to assert zero holdout games in the fit set (set-intersection on
   game ids, not a content read). Any other touch is abort condition 2:
   the run is void, not repaired.

## Games / Samples

Realized counts govern: fit games/rows as measured (expected 791 /
59,892), inner-val games as measured (expected 155), with the 208-game /
14,560-row holdout exclusion receipt. No assumed N appears in the
decision rule.

## Metrics

- `delta_full_inner`: paired mean improvement (floor minus fitted) on
  inner-val, Elo-scaled, `S* = 6`.
- `s_d_full`: SD of per-game paired differences over 155 inner-val games
  (reported with SE + CI95; NOT routed through any holdout margin).
- Fit-set delta, convergence (success, nit, message),
  deterministic-rerun proof, arm hashes, frozen-block receipt, mirror
  violations, MAE both arms.
- Reproducibility: manifest with every SHA, config, version, seed, and
  the exact launch command.

## Pre-Registered Decision Rule

> MANDATORY and fixed before any number exists. This record's run does
> not PASS or FAIL any engine; it establishes the first-training quality
> gate on TRAIN-side data only.

TRAINING-GATE requires ALL of:

(a) Convergence: L-BFGS-B reports success within the pinned budget
    (`maxiter 1000`); non-convergence is an abort-with-evidence (routes
    Y-3 pattern: INCONCLUSIVE-BY-DESIGN), never a silent budget raise.
(b) Arm differentiation: fitted-table SHA-256 != floor-table SHA-256,
    asserted before any loss is read; same-hash arms = FAIL before any
    loss is read.
(c) Frozen blocks intact: `frozen_block_mismatches` empty (KING PSTs,
    KING material, phase weights, tempo convention); any mismatch = FAIL.
(d) Fit-set descent: fitted mean loss strictly below floor mean loss on
    the 791-game fit set; otherwise FAIL (apathetic-fit rejection).
(e) Inner-val improvement: paired mean improvement `delta_full_inner >
    0` on the 155-game inner-val partition; CI including 0 is
    INCONCLUSIVE (not FAIL — the Y-2 dispersion fact stands).
(f) MAE pathology watch clean: fitted MAE not worse than floor MAE while
    fitted loss is better; a recurrence of the E-00014 collapse signature
    is recorded as a pathology recurrence (FAIL of the objective-health
    gate), not a success.
(g) Mirror gate: 0 violations on the checked positions.
(h) Holdout non-access: exclusion receipt shows 208 games / 14,560 rows
    excluded by game-id set before any label/FEN read, and the fit-set
    game set ∩ outer-holdout game set = ∅; any other touch of holdout
    content voids the run (abort condition 2).
(i) Determinism: in-process double-fit byte-identity proof holds;
    `--seed` recorded, never consumed.

No holdout quantity appears in this rule. No strength claim is licensed
by this run under any branch. `M16_floor` is not re-derived here.

## Power And Sample Size

> What N settles this rule: the inner-val partition is fixed at 155
> games (map `93bcd0db…f9e0`, salt 20261007, READ-ONLY). At the measured
> E-0016 dispersion (`s_d_inner = 0.0732`), the 95% CI half-width on the
> paired mean is ~±0.0116 — enough to detect a fit-set-scale improvement
> of the E-0016 magnitude (~0.027) but NOT to decide the fixed holdout
> margin `M16_floor = 0.005` (that would need `s_d <= 0.0256`, unmet by
> ~2.9x). Therefore this rule IS decidable as a TRAIN-side quality gate
> (conjuncts a–d, f–i plus the sign of e) and is explicitly NOT a
> holdout-margin decision. Any CI including 0 on (e) is INCONCLUSIVE by
> design, never FAIL.

## Sample Validity

- Arm differentiation (negative control): both arm hashes printed and
  compared BEFORE any loss is computed; same-hash arms = FAIL before any
  loss is read. Floor hash must equal the compiled-in hand-tuned floor
  (same-floor discipline: `711c460d…667f1`).
- Frozen blocks: KING PSTs + KING material identical on both arms
  (`frozen_block_mismatches` empty), enforced in code.
- Independence: game-split outer partition (salt 20260926) + game-split
  inner partition (NEW salt 20261007, READ-ONLY); games are the
  independent units; duplicates excluded by GLOBAL-before-split
  normalized-FEN dedup; overlap-0 gates at game and normalized-FEN
  level (fit set vs inner-val).
- Holdout non-access: 208 games / 14,560 rows excluded by game-id set
  before any label/FEN read; inner map covers outer-train games only
  (missing key = outer holdout = excluded on game-id alone); the
  TRAIN-only join additionally restricts to `(game_id, norm_fen)` pairs
  present in the TRAIN-only labels file.
- Provenance: dataset SHA-256, outer-map SHA-256, labels SHA-256,
  extractor-corpus SHA-256, inner-map SHA-256, tool commits, `src/`
  epoch, Python/scipy/numpy/python-chess versions, seed/L2/budget/clip/D
  — all pinned in the manifest + pre-execution commit named before the
  run.

## Provenance

- Dataset SHA-256:
  `27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95`.
- Outer map SHA-256: `bb079a41…da1ea` (salt 20260926).
- TRAIN-only labels SHA-256: `2bf68bfb…0f7bc2` (791 games).
- Extractor corpus SHA-256: `19cee190…31c48f` (74,452 rows).
- Inner map SHA-256: `93bcd0db…f9e0` (salt 20261007, READ-ONLY).
- Floor SHA-256: `711c460d…667f1`; `src/` epoch
  `dd4051a92daf834cf4a73f1878a0c894b0b6d1b8`.
- Hyperparameters: clip L 1200.0, D 173.7177927613, L2 1e-6, maxiter
  1000, seed 1, optimizer scipy L-BFGS-B, stage `S* = 6`.
- Raw evidence paths (local, gitignored): `build/e0017/` +
  `_obs/e0017_exec/`; aggregator: E-0017 Results fields + manifest.

## Results

## Results

2026-10-08 executor (systems-researcher seat) under HO-0029,
pre-execution commit `6a73da7` (W-0011 pipeline + governance records;
validate OK). Canonical trainer `tools/kaname_train.py` (+ one bugfix
commit for the eval surrogate-dict key, see below).

- Carve: TRAIN-only join — fit rows = extractor rows whose
  `(game_id, norm_fen)` pair is in the TRAIN-only labels file, restricted
  to outer-train ids by the re-derived split rule. Fit: 791 games /
  59,892 rows; holdout excluded before any label read: 208 games /
  14,560 rows; join_miss = 0. Inner-val (READ-ONLY map): 155 games /
  11,897 rows; skipped_outer_holdout = 14,560.
- Fit: `python tools/kaname_train.py train --config
  research/manifests/e0017-train-config.json` → exit 0. Design matrix
  (59,892 × 683) → deterministic full-batch L-BFGS-B (double-fit
  byte-identity proved in-process) → exit 0: convergence success=True,
  nit=10, nfev=12, message `CONVERGENCE: NORM OF PROJECTED GRADIENT <=
  PGTOL`; loss floor=0.450776 fitted=0.431617 delta_on_fit=0.019160.
  Arms differ: fitted `1de93a39…` vs floor `711c460d…`; frozen-block
  mismatches none; mirror 0/1000.
- Eval (paired, inner-val, Elo-scaled, S* = 6): games=155,
  `delta_inner_val = 0.03621102784460066`,
  `s_d = 0.07850860237584147`, se=0.0063059626913396505,
  CI95=[0.0237536738521879, 0.04866838183701342]; surrogate
  mean_improvement=0.03626430564742754 (quantisation gap visible, tiny);
  MAE fitted=0.24543964443082955 vs floor=0.26275219257415794 (pathology
  watch CLEAN — fitted not worse while fitted loss better);
  mean_loss fitted=0.4355858953303157 vs floor=0.46505802390285045.
- Determinism receipt: the first `train` invocation crashed AFTER writing
  the fit checkpoint (eval-side `KeyError: 'per_game_surrogate'` — the
  trainer stored per-arm `mean_loss_surrogate` but not the per-game dict
  the paired-surrogate builder reads; a trainer bug, NOT a science
  change). After the one-line fix (store `per_game_surrogate` in the
  per-arm dict), `resume --checkpoint build/e0017/checkpoints/fit.json`
  re-ran the fit deterministically and produced the byte-identical table
  `1de93a39…` (fit checkpoint SHA `253245ee…` unchanged across both
  invocations), then completed the eval. Resume-from-checkpoint therefore
  proved on real artifacts.
- Artifacts (local, gitignored): `build/e0017/fitted.json`
  (`1de93a39…`), `build/e0017/metrics.json` (`0445383c…`),
  `build/e0017/manifest.json` (`020a8e18…`), checkpoints
  `design-matrix.json` (`1073e4b5…`), `fit.json` (`253245ee…`),
  `eval.json` (`579c69d6…`); raw ledgers `_obs/e0017_exec/train_out.txt`
  + `_obs/e0017_exec/resume_out.txt`.
- NO holdout quantity appears anywhere in any artifact (the holdout is
  touched only as the game-id exclusion receipt, abort 2 otherwise).

## Statistical Analysis

Paired-t CI over the 155 inner-val games (E-0013 B3, game-clustered, sign
positive = fitted lower loss): mean improvement 0.036211, s_d 0.078509,
SE 0.006306, CI95 [0.023754, 0.048668] — strictly above zero. MAE
pathology watch: fitted MAE 0.245440 < floor MAE 0.262752 with fitted
loss better — CLEAN (no E-00014-style saturation collapse). Mirror gate:
0/1000. Arms differ; frozen blocks identical. Surrogate improvement
0.036264 agrees with exact 0.036211 (quantisation gap negligible).

## Interpretation

TRAINING-GATE pass (all conjuncts):

- (a) convergence success=True — PASS.
- (b) exclusion receipt 208/14,560 + fit 791/59,892 + join_miss=0 —
  PASS.
- (c) arms differ (`1de93a39…` vs `711c460d…`) — PASS.
- (d) frozen-block mismatches none — PASS.
- (e) inner-val improvement 0.036211 with CI95 [0.023754, 0.048668]
  strictly above zero — PASS (measurable).
- (f) mirror 0/1000 — PASS.
- (g) MAE watch: fitted 0.245440 < floor 0.262752 — PASS.
- (h) manifest complete (config SHA `8a7955d6…`, all input SHAs, device,
  environment) — PASS.
- (i) deterministic rerun proved (double-fit byte-identity in-process +
  resume reproduced `1de93a39…` byte-identically) — PASS.

Route: TRAINING-GATE PASS. The fitted table `1de93a39…` becomes the
first pinned learned artifact. No strength claim is licensed by this run
under any branch. F-U3-pattern accountability for Y-2 was already
discharged by DEC-0015; this record creates no new holdout obligation.

## Conclusion

2026-10-08 — E-0017 COMPLETED with result TRAINING-GATE PASS (all nine
conjuncts a–i). The deterministic full-batch L-BFGS-B fit on the full
outer-train set (791 games / 59,892 rows) converged (nit=10, nfev=12,
delta_on_fit=0.019160) and beats the frozen floor on the inner-val
partition (155 games): delta=0.036211, CI95 [0.023754, 0.048668]
strictly above zero, s_d=0.078509, MAE watch CLEAN, mirror 0/1000,
frozen blocks intact, determinism proved by double-fit byte-identity
plus resume reproducing `1de93a39…` byte-identically. First learned
artifact `1de93a39…` pinned. Holdout never read (exclusion receipt
208/14,560 in every ledger; no holdout quantity in any artifact). No
strength claim licensed under any branch. W-0011 DONE + VERIFIED;
HO-0029 DONE. Follow-up strength evaluation, if any, requires its own
pre-registration.

## Follow-Up

- On TRAINING-GATE pass: the fitted table becomes the first pinned
  learned artifact; a later record may pre-register strength evaluation
  (Tier-S SPRT) under its own protocol. F-U3-pattern accountability for
  Y-2 is already discharged by DEC-0015; this record creates no new
  holdout obligation.
- On INCONCLUSIVE (e) with all health gates clean: the pipeline stands
  verified; the dispersion fact is confirmed at full-train scale.
- On FAIL of any health gate (b/c/d/f/g/h/i) or abort (a): named defect,
  no silent repair; E-0013/E-0016 stay frozen under all branches
  (DEC-0014/DEC-0015).
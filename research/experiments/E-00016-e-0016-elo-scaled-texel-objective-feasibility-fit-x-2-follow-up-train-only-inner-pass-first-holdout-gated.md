---
id: E-00016
type: experiment
title: E-0016 - Elo-scaled Texel objective feasibility + fit (X-2 follow-up; TRAIN-only inner pass first, holdout gated)
status: PENDING
result: null
elo_change: null
hypothesis: H-0013
priority: high
owner: researcher-architect
pre_registered: 2026-10-06
example: false
created: 2026-10-06
completed: null
tags: [texel, elo-scale, feasibility, train-only-first, pre-registration, x-2-follow-up]
---

# E-00016 — E-0016 - Elo-scaled Texel objective feasibility + fit (X-2 follow-up; TRAIN-only inner pass first, holdout gated)

> Filed by researcher-architect, 2026-10-06, as the NEW pre-registration DEC-0014
> routes F-U3's X-2 follow-up to. **NOTHING HAS RUN.** No extraction, no fitting,
> no holdout read, no SPRT game. This record is PENDING and may not be flipped
> to RUNNING by its author. Executor seat: **systems-researcher**, under a NEW
> handoff (HO-0015/HO-0016 pattern: executor appends Response; a fresh
> verification-auditor appends Verification).
>
> **Why this record exists.** E-00014 fired branch X-2 INCONCLUSIVE-BY-POWER
> (`s_d_inner = 48.73234010819671 >> 0.0101`, power at 0.002 = 0.05) and recorded
> a loss-scale pathology: the pinned objective `sigmoid(clip(E, -1200, 1200))`
> has no Elo-scale divisor, so raw centipawn scores saturate the sigmoid and the
> optimizer harvested ~23 loss points by collapsing scores toward 0 (fitted MAE
> WORSE than floor MAE). E-0013 is frozen (DEC-0014); this record owns the
> re-design under a new id, never as an edit to E-0013.

## Hypothesis

Under the Elo-scaled objective `sigmoid(clip(E/D, -L, L))` with the FIXED scale
`D = 400/ln(10)` (standard Texel/Elo mapping, pinned below), the deterministic
full-batch L-BFGS optimizer from the E-0013 family either (a) beats the frozen
hand-tuned floor on a TRAIN-side game-split inner partition with a per-game
cluster SD small enough to make the fixed holdout margin decidable (branch
Y-1), or (b) does not, in which case that fact routes the follow-up by the
pre-registered table below — never by post-hoc margin selection.

## Baseline

The frozen hand-tuned `EvalCoeffs` table as compiled into `src/eval.cpp:174-234`
at the pinned `src/` epoch named in the pre-execution commit (same-floor
discipline as E-00014: the floor here and the floor there must be the same
bytes, or no number here compares with any number there). Same stage `S* = 6`,
same quiet-proxy predicate, same crash + degenerate-mate exclusions, same
GLOBAL-before-split normalized-FEN dedup (F9 as amended by the S-0037 leakage
ruling), same side-to-move label frame (B2 s1).

## Candidate

The parameter set of E-0013's free-parameter list (five non-KING `mg_pst` /
`eg_pst` tables plus items 1 and 3–6; KING PSTs FROZEN per B5; KING material
fixed 20000/20000; taper/phase formula and phase weights frozen integers),
fitted on the TRAIN-side inner partition only under the Elo-scaled objective,
with hyperparameters selected on that same inner partition only. **The set may
not be widened or narrowed by the executor.**

## Difference

The objective — and ONLY the objective — changes relative to E-00014:

- E-00014: `sigmoid(clip(E_theta(p), -L, L))`, `L = 1200` cp.
- E-0016: `sigmoid(clip(E_theta(p)/D, -L, L))`, `D = 400/ln(10) ≈ 173.7177927613`
  (FIXED, derived below, not fitted, not selected), `L = 1200` cp UNCHANGED in
  name (now read in SCALED units: clip binds at `E/D = ±1200`, i.e. raw scores
  beyond ±208,461 cp — unreachable, so clipping is a numerical guard only and
  the gradient lives on the sigmoid's steep region for all realistic scores).
- The `D` derivation (first principles, no data read): the Elo expected-score
  curve is `1/(1+10^(-dE/400)) = sigmoid(dE·ln(10)/400)`; the divisor that maps
  a centipawn score difference onto that curve is therefore `D = 400/ln(10)`.
  Under it, a +100 cp edge predicts `sigmoid(100/173.72) ≈ 0.640` (cf. Elo
  table: 100 Elo ≈ 0.640) — the objective's probability scale is the game-score
  scale, so a loss improvement is a ranking improvement, not a collapse reward.
- Steep-region check (arithmetic, `_obs/e16_power.py`): the sigmoid is steep
  for `|E|/D < ~2`, i.e. `|E| < ~347` cp — ordinary quiet positions. The old
  objective saturated at a few hundred cp of raw score; the new one saturates
  only past `6.9·D ≈ 1200` scaled units, i.e. never in practice.

## Hardware

Single host, CPU only. No engine pairs: this pass is an offline numerical fit
over extracted positions, not a game campaign. No Gate-0 build is required.

## Engine Version

Read-only citation of `src/eval.h` / `src/eval.cpp` at the pinned `src/` epoch
named in the pre-execution commit (frozen floor table, `GAME_PHASE_MAX = 24`,
phase weights N=B=1 R=2 Q=4, mirror convention `s ^ 56`). **No engine source
file is edited by this record or by its executor**, and no engine binary is
invoked by the TRAIN-only stage (a).

## Network

N/A.

## Dataset

ONLY `m0_audit/e0011/games.jsonl` — 1,000 rows, SHA-256
`27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95` (the
R-0017-VERIFIED replacement dataset). Failed attempt-1 excluded. No external
labels exist and none are licensed. Same corpus digest discipline as E-00014:
the labelled fitter corpus SHA-256 must match the pre-execution pin before any
TRAIN read.

## Test Method

### Stage (a) — TRAIN-only inner feasibility pass (this record's executor runs this)

1. Consume the committed outer split map READ-ONLY (`SPLIT_SALT = 20260926`,
   `random.Random(SPLIT_SALT * 1000003 + game_id)`, 80/20 BY GAME; holdout 208
   games / 14,560 rows excluded before any label read, by game-id set).
2. Carve an inner partition from the TRAIN side only with a NEW distinct inner
   salt (named in the pre-execution commit; distinct from every prior salt
   20260914/20260922/20260924/20260926/20261005), 80/20 inner-train/inner-val
   BY GAME. Inner map format `kana-e0013-innersplit-v1`; role vocabulary
   (`train`/`holdout`) means inner-train/inner-val per the format note.
3. Fit the Candidate on inner-train with deterministic full-batch L-BFGS on
   the mean Elo-scaled logistic loss + L2 (`l2`, `maxiter`, seed recorded-only,
   all pinned in the pre-execution commit; SPSA withdrawn as a leakage channel
   per B4 and not available here).
4. Evaluate paired on inner-val: per-game mean paired loss difference
   (floor minus fitted), `delta_star_inner` (mean), `s_d_inner` (sample SD over
   inner-val GAMES), 95% CI (paired t), achieved power at the fixed margin,
   arm hashes, frozen-block check, mirror gate, MAE both arms (pathology
   watch: fitted MAE must not be worse than floor MAE while fitted loss is
   better — if it is, record it as a pathology recurrence, not a success).
5. Report into Results; route by the decision table below. **THE HOLDOUT IS
   NOT READ. NOT ONCE. NOT FOR A COUNT, NOT FOR A LABEL, NOT FOR A SANITY
   CHECK.** Holdout game ids are touched only to assert zero holdout game
   appears in the inner partition (set-intersection on game ids, not a content
   read). Any other touch of holdout content is abort condition 2: the pass is
   void, not repaired.

### Stage (b) — holdout-gated fit-quality comparison (NOT run here)

Runs only under a LATER record, only if stage (a) routes Y-1 AND that later
record's own pre-registration names the holdout protocol. This record licenses
no holdout read of any kind.

## Games / Samples

Realized counts govern (same discipline as E-00014): inner-train/inner-val
game and position counts as measured, with the 208-game / 14,560-row holdout
exclusion receipt. No assumed N appears in the decision rule.

## Metrics

- `delta_star_inner`: paired mean logistic-loss improvement (floor minus
  fitted) on inner-val, Elo-scaled objective, `S* = 6`.
- `s_d_inner`: sample SD of the per-game paired differences over inner-val
  games.
- `M16_floor = 0.005`: the FIXED holdout margin for the later stage-(b)
  record, in scaled-logistic-loss units (~0.72% of chance loss ln 2 ≈ 0.6931;
  convention pinned here so no later record invents it after seeing data).
- `s_d_crit = 0.0256`: the 80%-power decidability threshold for `M16_floor`
  at the frozen holdout game count G = 208 (derived below; the B3 rule with
  the new margin and N).
- Achieved power at `M16_floor` on the measured `s_d_inner` (normal
  approximation, two-sided α = 0.05).
- Arm hashes, frozen-block receipt, mirror violations, MAE both arms.

## Pre-Registered Decision Rule

> MANDATORY and fixed before any number exists. This record's stage (a) does
> not PASS or FAIL any engine; it supplies inputs to the table below.

1. If `delta_star_inner` is measurable (fitted beats floor on inner-val) AND
   `s_d_inner <= 0.0256`: report both + achieved power. Route **Y-1
   (FEASIBLE)**: a later record may pre-register the holdout-gated stage (b)
   against the FIXED margin `M16_floor = 0.005`. The margin is not re-derived
   there.
2. If `delta_star_inner` is measurable AND `s_d_inner > 0.0256`: report both +
   achieved power. Route **Y-2 (INCONCLUSIVE-BY-POWER)**: not a FAIL, not a
   licence to widen the margin, not a licence to re-fit under a different
   scale. The follow-up obligation is a named re-decision with the four
   quantities published (same F-U3 pattern).
3. If `delta_star_inner` is NOT measurable (optimizer does not beat floor on
   inner-val): report `delta_star_inner = null` with both arms' inner-val
   losses. Route **Y-3 (INCONCLUSIVE-BY-DESIGN)**: never FAIL, never
   "no achievement = FAIL", never a silent re-run with different
   hyperparameters to obtain a measurable delta.
4. If `s_d_inner` cannot be estimated (too few inner-val games): report
   `s_d_inner = null` with the game count; route **Y-2** (power
   unestablished).

**Prohibitions.** The executor may not choose among branches, may not re-run
with different hyperparameters/salts/scales to obtain a measurable delta, may
not report a branch-relevant quantity from any other partition, may not fit or
tune `D` (it is FIXED at `400/ln(10)`), may not invent or adjust `M16_floor`
(it is FIXED at 0.005), and may not report any holdout quantity at all.
Branch selection is this record's table applied to reported fields after the
fact, not a judgement made here.

## Power And Sample Size

> What N settles this rule: derived 2026-10-06 in `_obs/e16_power.py` — pure
> arithmetic, no data read. Calibration check included: the same formula at
> M = 0.002, G = 200 gives 0.010096 ≈ the B3 record value 0.0101.

- Elo scale: `D = 400/ln(10) = 173.7177927613` (Elo curve identity).
- Chance-level mean logistic loss: `ln(2) = 0.6931471806`.
- Fixed margin: `M16_floor = 0.005` (~0.72% of chance loss).
- Frozen holdout games: `G = 208` (E-0013 split; not re-derivable here).
- t quantiles, df = 207 (Cornish-Fisher one-term): `t_.975 = 1.971424`,
  `t_.80 = 0.843358`, sum `2.814782`.
- Decidability: `s_d_crit = M·√G/(t_.975+t_.80) = 0.005·14.4222/2.814782 =
  0.025619 ≈ 0.0256`.
- Therefore this rule IS decidable at the planned N **iff the measured
  `s_d_inner <= 0.0256`**; otherwise it routes Y-2 by name instead of failing.
- Clip in scaled units: `L/D = 1200/173.72 = 6.9078` (saturation only past
  ~99.9% win probability — a numerical guard, not a binding constraint).
- Order of operations (R-0028, normative): the implementing tool divides E by D
  FIRST and clips SECOND with the same numeric L — `clip(E/D, -1200, 1200)` —
  which binds at raw ±208,461 cp and is a numerical guard only. An implementation
  that clips E first and divides after would silently run the OLD objective.
  Implemented in `tools/e0013_eval.py` / `tools/e0013_fit.py` (W-0010, `--elo-scale`,
  default 1.0; E-00014 evidence re-derived bit-for-bit at D=1.0).
- Non-convergence abort (R-0028): if the L-BFGS-B fit does not converge within the
  pinned budget, the executor reports an abort-with-evidence (convergence status,
  iterations consumed, loss trace) and routes Y-3; the budget is never raised
  silently. Added 2026-10-06 by the owner seat (researcher-architect) per R-0028;
  no other field of this pre-registration is touched.

## Sample Validity

> Validation is part of the result.

- Arm differentiation (negative control): both arm hashes printed and
  compared BEFORE any loss is computed; same-hash arms = FAIL before any loss
  is read. Floor hash must equal the compiled-in hand-tuned floor
  (same-floor discipline).
- Frozen blocks: KING PSTs + KING material identical on both arms
  (`frozen_block_mismatches` empty), enforced in code.
- Independence: game-split inner partition with a NEW distinct salt; games
  are the independent units; duplicates excluded by GLOBAL-before-split
  normalized-FEN dedup; overlap-0 gates at game and normalized-FEN level.
- Holdout non-access: 208 games / 14,560 rows excluded by game-id set before
  any label/FEN read; inner map covers outer-train games only (missing key =
  outer holdout = excluded on game-id alone).
- Provenance: fitter-corpus SHA-256, split-map SHA-256, inner-map SHA-256,
  tool commits, `src/` epoch, Python/scipy/numpy/python-chess versions,
  seed/L2/budget/clip/D — all pinned in the pre-execution commit named before
  the run.

Arm-differentiation evidence: (executor fills from run output)
Independence proof: (executor fills: inner salt, game counts, overlap-0 receipts)
Provenance: (executor fills: hashes, commits, versions)

## Provenance

(executor fills — pre-execution commit hash, `src/` epoch, tool commits,
fitter-corpus/split/inner-map SHA-256, raw evidence paths (local, gitignored),
aggregator command reproducing every number)

## Results

(PENDING — executor fills under the new handoff; or explicit abort with the
triggered abort condition number and its evidence. An abort is a result.)

## Statistical Analysis

(PENDING — paired-t CI over inner-val games, achieved power at `M16_floor`,
MAE pathology watch.)

## Interpretation

(PENDING — route Y-1/Y-2/Y-3 by the table; no strength claim is licensed by
stage (a) under any branch.)

## Conclusion

(PENDING.)

## Follow-Up

- On Y-1: a later record pre-registers stage (b) against FIXED `M16_floor`,
  with its own holdout protocol, suite gate, and SPRT terms. F-U3/FND-0010
  discharges only on that record's run + verdict.
- On Y-2/Y-3: named re-decision with the four published quantities
  (`s_d_inner`, `delta_star_inner`, inner-val game count, achieved power).
- E-0013 stays frozen under all branches (DEC-0014).
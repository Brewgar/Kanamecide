---
id: E-00014
type: experiment
title: "E-00014 - TRAIN-ONLY feasibility pass for E-0013 (measure delta_star and s_d_inner; MEASUREMENT, not training)"
status: PENDING
result: null
elo_change: null
hypothesis: H-0013
priority: high
owner: systems-researcher
pre_registered: 2026-09-26
example: false
created: 2026-09-26
completed: null
tags: [texel, feasibility, power, train-only, pre-registration]
---

# E-00014 - TRAIN-ONLY feasibility pass for E-0013 (PENDING; NOT RUN)

> Filed by researcher-architect, 2026-09-26, as the BUCKET-2 sub-contract for R-0019's
> B2 sentence 2 and B3 sentence 1. **This is a MEASUREMENT record, not a training run.**
> It fits coefficients on a TRAIN-side inner partition to measure two quantities, and it
> does **not** produce E-0013's fitted artifact, does not read the holdout, and licenses
> no strength claim.
>
> **NOTHING HAS RUN.** No extraction, no fitting, no holdout read, no SPRT game. This
> record is PENDING and may not be flipped to RUNNING by its author. Executor seat:
> **systems-researcher**, under **HO-0015**.
>
> **Why this record exists.** E-0013's conjunct (c) turns on a margin
> (`LOSS_MARGIN = 0.002`) whose attainability depends on a per-game cluster SD `s_d`
> that nobody has measured. R-0019 ruled (B3) that this quantity must be measured on the
> training side, before the holdout is opened, and that the FAIL/INCONCLUSIVE split must
> be a function of the measurement rather than an assertion. E-0013's addendum
> (2026-09-26) names E-00014 as the record that supplies it. This record pre-registers
> that pass; running it is execution and belongs to another seat.

## Hypothesis

On a game-split inner partition carved from E-0013's TRAIN side, the adopted optimizer
(deterministic full-batch L-BFGS on the mean logistic loss of
`sigmoid(clip(E_theta(p), -L, L))` against the side-to-move-frame target) either beats
the frozen hand-tuned floor, in which case an attainable gain `delta_star` and a
per-game cluster SD `s_d_inner` are measurable, or it does not, in which case
`delta_star` is not measurable and that fact is itself the result.

## Baseline

The frozen hand-tuned `EvalCoeffs` table as compiled into `src/eval.cpp:174-234` at the
pinned `src/` commit - the same table, the same evaluation stage (`S* = 6`, per E-0013's
addendum) and the same label construction as the floor arm of E-0013's holdout
comparison. Same-floor discipline: the floor here and the floor there must be the same
bytes, or E-00014's `delta_star` is not E-0013's `delta_star`.

## Candidate

The E-0013 fitted parameter set (five non-KING `mg_pst`/`eg_pst` tables plus items 1 and
3-6 of E-0013's free-parameter list; KING PSTs FROZEN per B5), fitted on the TRAIN-side
inner partition only, with hyperparameters selected on that same inner partition only.

## Difference

### Positions and labels (same construction as E-0013, by reference)

Quiet-proxy predicate exactly as E-0013 specifies it (check-state tested on the position
before the move; no capture; no check/mate suffix; `full_ply >= 10`; `san` segment only;
`opening` never a candidate), plus the crash exclusion and the degenerate-mate
(`len(san) <= 6`) exclusion, plus the GLOBAL-before-split exact-FEN dedup (F9). Label =
`y = white_score` if the side to move is WHITE else `1 - white_score`, with
`white_score in {1, 0.5, 0}` derived from `res` (B2 side-to-move frame). The extractor
MUST report `label_frame_uniform = true` and the per-side-position counts.

## Free-parameter set

Exactly E-0013's, with KING PSTs FROZEN (B5): the five non-king `mg_pst[5][64]` /
`eg_pst[5][64]` tables plus items 1 and 3-6 of E-0013's free-parameter list. KING
material fixed at 20000/20000, not fitted. The taper/phase formula and the phase weights
are frozen integers, not fitted. **The set may not be widened or narrowed by the
executor.**

## Fitting method

Deterministic full-batch L-BFGS on the mean logistic loss, L2-regularized, with the
E-0013 pre-fit commit's pinned seed, L2 weight, iteration budget and clipping bound `L`.
SPSA is **withdrawn** as a leakage channel (B4) and is not an available option here
either. No hyperparameter may be selected on, or compared against, any holdout quantity -
there is no holdout in this record, and the inner partition is the only selection
surface.

## Test Method

## Pre-Registered Decision Rule

> MANDATORY and fixed before any number exists. This record does not PASS or FAIL E-0013;
> it supplies one input to E-0013's already-fixed contingency table.

1. If `delta_star_inner` is measurable (the fitted table beats the floor on inner-val)
   and `s_d_inner <= 0.0101`: report both values. E-0013 routes to **branch X-1**, where
   conjunct (c) is evaluated as written and a CI including 0 is a FAIL.
2. If `delta_star_inner` is measurable and `s_d_inner > 0.0101`: report both values plus
   the achieved power. E-0013 routes to **branch X-2, INCONCLUSIVE-BY-POWER**. This is
   NOT a FAIL of E-0013 and NOT a licence to widen the margin.
3. If `delta_star_inner` is NOT measurable (the optimizer does not beat the floor on the
   inner partition): report `delta_star_inner = null` with the measured inner-val losses
   of both arms. E-0013 routes to **branch X-3, INCONCLUSIVE-BY-DESIGN**. This is never
   FAIL, and never "no achievement = FAIL".
4. If `s_d_inner` cannot be estimated (too few inner-val games): report `s_d_inner = null`
   with the game count, and E-0013 routes to **X-2** (power unestablished).

**Prohibitions.** The executor may not choose among branches, may not re-run with
different hyperparameters to obtain a measurable `delta_star`, may not report a
branch-relevant quantity from any other partition, and may not report any holdout
quantity at all. Selecting the branch is E-0013's pre-registered table applied to
reported fields after the fact, not a judgement made here.

## Power And Sample Size

> What N settles this rule: the per-game SD `s_d_inner` is estimated from the inner-val
> GAMES, and its own precision is a function of that game count. The pass must therefore
> report the game count alongside the SD, and must report the CI of `s_d_inner` itself,
> so that a borderline `s_d_inner` near 0.0101 is visibly borderline rather than silently
> decisive. Expected inner-val game count is on the order of 10^2; that expectation is
> arithmetic from the split fractions, not a measurement, and the realized count governs.

## Provenance

- Dataset SHA-256: `27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95`.
- Pinned `src/` commit for the frozen floor table (to be recorded at execution; assumed
  `7348f89` at filing time and to be VERIFIED, not assumed).
- E-0013 split-map hash and pre-fit commit hash (inputs; both must pre-exist).
- Inner salt, inner game-id map SHA-256, optimizer name and version, Python and
  python-chess versions, seeds, iteration budget, L2 weight, clipping bound `L`, host
  facts, raw evidence paths (local, gitignored), and the aggregator command reproducing
  every reported number. Command -> exit code -> path -> hash, as in E-0011/E-0012.
- Tool versions recorded, not assumed.

## Abort Conditions

Any one of these aborts the pass. All are reported; none is worked around.

1. The E-0013 split-map hash or the pre-fit commit hash does not exist or does not match.
2. Any holdout CONTENT is read - position, label, FEN or count. One touch is an abort,
   not a warning; the pass is void, not repaired.
3. Inner-partition game-id overlap with the holdout, or normalized-FEN overlap with the
   holdout: any non-zero value.
4. `label_frame_uniform != true`.
5. The frozen floor table's SHA-256 differs from E-0013's floor table.
6. The fit does not converge within the pinned iteration budget. Report the failure; do
   NOT raise the budget and re-run.
7. Gate 0 / `research.py validate` fails, or the engine source at the pinned commit does
   not match the pinned hashes.
8. Any pre-registered output field cannot be produced. Report it as `null` with the
   reason; do not substitute a different measurement.

**An abort is a result.** It is reported in the open with its reason and routed to
E-0013's contingency table or to a named re-decision. It is never converted into a
favourable number by re-running with different settings.

## Results

TBD - nothing has run. This section will be filled with aggregator output and pinned
hashes only, never narrative.

## Statistical Analysis

TBD.

## Interpretation

TBD.

## Conclusion

TBD.

## Follow-Up

- The executor reports the pre-registered output fields into this record and closes it.
- `delta_star` and `s_d_inner` then feed E-0013's B3 contingency table (X-1 / X-2 / X-3),
  which was fixed in E-0013's 2026-09-26 addendum BEFORE this record was filed.
- This record does not verify itself. Any claim it makes about `delta_star` or
  `s_d_inner` is a claim by the executor seat, and E-0013's own independent verification
  (Q-0006 gate 7, E-0013 F-U5) covers it there.
- No H-#### status is changed by this record. H-0013 and H-0010 lifecycle decisions stay
  out of scope.

> This record is not a strength measurement and has no power requirement in Elo.

## Sample Validity

- **Partition integrity:** the inner partition is carved BY GAME from TRAIN only; zero
  game-id overlap with the holdout; zero normalized-FEN overlap with the holdout; the
  normalized-FEN check uses E-0013's normalization (excluding clock and fullmove number)
  so the two records compare like with like.
- **Holdout non-access:** the single most important validity property of this record. It
  is asserted by construction (the extractor is invoked on the inner partition only) and
  evidenced by the extractor command line and its input file list, both recorded.
- **Same floor as E-0013:** the floor table's SHA-256 is recorded and must equal the one
  E-0013 uses.
- **Independence of the inner split from the outer split:** the inner salt is distinct
  from `SPLIT_SALT` and from every prior salt in the project, and the inner game-id map
  is hash-committed before the fit runs, on the same discipline as E-0013's split map.
- **Arm differentiation (negative control):** the two arms are two parameter tables, not
  two engines. The evaluator prints the SHA-256 of the table actually loaded for the
  fitted arm and of the table actually loaded for the floor arm, asserts they DIFFER
  before any loss is computed, and records both. Identical hashes = FAIL.


1. Confirm the E-0013 split-map hash and the pre-fit commit hash exist and are recorded;
   otherwise ABORT.
2. Extract quiet positions per the predicate above, INNER side only; report realized
   counts and `label_frame_uniform`.
3. Carve the inner partition BY GAME from TRAIN; assert zero game-id overlap with the
   holdout game-id set and zero normalized-FEN overlap with the holdout (same
   normalization E-0013 uses: side-to-move + placement + castling/EP, excluding the
   halfmove clock and fullmove number).
4. Fit on inner-train with the pinned hyperparameters; record convergence status, the
   number of iterations actually consumed, and the fitted table's SHA-256.
5. Evaluate BOTH the fitted table and the frozen hand-tuned floor on inner-val, paired,
   under the same label construction at `S* = 6`. Report the per-game mean paired loss
   difference.
6. Report every pre-registered output field below. No field may be omitted; a field that
   cannot be measured is reported as `null` with the reason, never omitted.

## Games / Samples

Inner partition only. Expected magnitude: TRAIN is ~80% of the quiet positions, so the
inner-val partition is expected to hold on the order of 10^3-10^4 positions across on
the order of 10^2 games - **this expectation is arithmetic from the split fractions, not
a measurement, and the realized counts govern.** If the realized inner-val game count is
too small to support a per-game SD at all, that is reported as `s_d_inner = null` with
the game count, which routes E-0013 to contingency branch X-2 (INCONCLUSIVE-BY-POWER) by
the pre-registered table, not by judgement.

## Metrics

- `delta_star_inner`: the attainable loss improvement of the fitted parameters over the
  frozen hand-tuned floor on the inner-val partition, paired, same labels, `S* = 6`. Sign
  convention: positive means the fitted table achieves LOWER logistic loss.
- `s_d_inner`: the per-game standard deviation of the per-game mean paired loss difference
  across inner-val games. This is the quantity that decides whether
  `LOSS_MARGIN = 0.002` is decidable (decidable iff `s_d_inner <= 0.0101` at G ~ 200).
- Supporting: inner-train / inner-val game and position counts; mean per-game paired loss
  difference and its 95% CI on `t_{0.975, G-1}`; the achieved power at a 0.002 margin
  under the measured `s_d_inner`; optimizer convergence status; iterations consumed;
  `label_frame_uniform`; per-side-position counts.


Fitted parameters vs frozen hand-tuned parameters, on the inner partition, under an
identical label construction and an identical evaluation stage. **No difference in the
holdout, which this record never reads.**

## Hardware

Single host, CPU only. No engine pairs are used: this pass is an offline numerical fit
over extracted positions, not a game campaign. No Gate-0 build is required to run it.

## Engine Version

Read-only citation of `src/eval.h` / `src/eval.cpp` at the pinned `src/` commit for the
frozen floor table, for `GAME_PHASE_MAX = 24`, for the phase weights (N=B=1, R=2, Q=4)
and for the mirror convention (`s ^ 56`). **No engine source file is edited by this
record or by its executor**, and the engine binary is not invoked by this pass at all.

## Network

N/A.

## Dataset

### Source (frozen, single)

ONLY `m0_audit/e0011/games.jsonl` - 1,000 rows, SHA-256
`27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95` (the R-0017-VERIFIED
replacement dataset). Failed attempt-1 excluded. No external labels exist and none are
licensed.

### The split, and the one thing this record must not do

- E-0013's split map (`SPLIT_SALT = 20260926`, `random.Random(SPLIT_SALT * 1000003 +
  game_id)`, 80/20 BY GAME) is produced by E-0013's execution and hash-committed in the
  single pre-fit commit together with the deferred values.
- **This record consumes the committed split map READ-ONLY and carves an INNER
  partition from the TRAIN side only**, with a distinct inner salt, again BY GAME:
  `random.Random(INNER_SALT * 1000003 + game_id)` over the TRAIN games, 80/20
  inner-train / inner-val.
- **THE HOLDOUT IS NOT READ. NOT ONCE. NOT FOR A COUNT, NOT FOR A LABEL, NOT FOR A
  SANITY CHECK.** Holdout game ids are touched only to assert that zero holdout game
  appears in the inner partition; that is a set-intersection on game ids, not a read of
  holdout content. Any other touch of holdout content is an abort condition below, not
  a warning.
- The split map and the pre-fit commit MUST already exist and be hash-recorded before
  this pass reads anything. If they do not, this record ABORTS.

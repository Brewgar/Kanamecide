---
id: E-00014
type: experiment
title: "E-00014 - TRAIN-ONLY feasibility pass for E-0013 (measure delta_star and s_d_inner; MEASUREMENT, not training)"
status: COMPLETED
result: "INCONCLUSIVE-BY-POWER (branch X-2): s_d_inner=48.73234010819671 > 0.0101; delta_star_inner (inner-val, paired)=23.05004604618598; achieved power at 0.002=0.050000; no LOSS_MARGIN widened"
elo_change: null
hypothesis: H-0013
priority: high
owner: systems-researcher
pre_registered: 2026-09-26
example: false
created: 2026-09-26
completed: 2026-10-05
tags: [texel, feasibility, power, train-only, pre-registration]
---

# E-00014 - TRAIN-ONLY feasibility pass for E-0013 (COMPLETED 2026-10-05)

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

---

## Addendum 2026-10-05 — Dedup-key correction (F-U11), by this record's owner seat, BEFORE the pass

> Filed by **systems-researcher** on 2026-10-05, as E-00014's `owner:` and its executor seat,
> under E-0013's execution-readiness checklist item 14 ("E-00014's own filter text … still
> describes stage 4 as the exact-FEN dedup (F9) … Unblocked by: a dated amendment to E-00014
> naming the new key at that clause, filed by its own executor seat **before** the pass") and
> FND-0027 (F-U11)'s missing-artifact list (a). **APPEND-ONLY — nothing above this amendment
> is edited or deleted; `status: PENDING` and `result: null` are unchanged.** No measurement
> was run to produce this text; every claim below names either a committed tool or a committed
> manifest.
>
> ### 1. Clause 1 — the Difference section's dedup clause is re-stated under the key in force
>
> Line 68 reads "plus the GLOBAL-before-split **exact-FEN** dedup (F9)". Per the S-0037
> leakage ruling (option 1, F-U7) and E-0013 Addendum 2 (S-0039), the KEY is the
> **normalized FEN** — piece placement + side to move + castling/EP rights; the halfmove
> clock and the fullmove number are NOT part of a position's identity. The dedup ORDER
> (GLOBAL, before the split; survivor = first occurrence in (game_id, ply_index) order) is
> unchanged. The overlap-0 gate and this record's abort condition 3 compare on that same
> normalized key. The sentence as filed above is retained verbatim as history; this clause
> replaces its operative content.
>
> ### 2. Clause 2 — the stranded Test Method block is named, not moved
>
> The numbered list "1. Confirm the E-0013 split-map hash … 6. Report every pre-registered
> output field below." sits after `## Sample Validity` (the 2026-09 handoff-corruption class,
> same as E-00015's). It IS the Test Method. The block is **not** moved here because this
> amendment precedes the pass and the pass's own reporting order reproduces its steps one by
> one; readers are directed to it by this sentence. (E-00015's executor moved its block
> verbatim under its canonical heading only because that record was closing at COMPLETED and
> validate rejected the lifecycle flip; E-00014 remains PENDING and no such gate fires here.)
>
> ### 3. Clause 3 — the recorded-at-execution fields now exist, and their values are named
>
> Every input the pre-registration left to "execution" now exists and is hash-committed in
> the single pre-fit commit `3d388b72e5c46ec448168187cbd7e7e0d40ea0f7`,
> `research/manifests/e0013-prefit.json`:
>
> - E-0013 split-map SHA-256 (input, pre-existing):
>   `bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea`
> - pre-fit commit hash: `3d388b72e5c46ec448168187cbd7e7e0d40ea0f7`
> - pinned `src/` commit for the frozen floor: `dd4051a92fafde...` — correction to this
>   record's own assumption: the filing-time text says "assumed `7348f89` at filing time and
>   to be VERIFIED, not assumed". Verified-and-false: `7348f89` is a research-only commit
>   that never touched `src/` (HO-0023 verification). The pin tracks the measuring epoch per
>   HO-0023's post-filing correction, today `dd4051a92daf834cf4a73f1878a0c894b0b6d1b8`.
> - Frozen floor table SHA-256: `711c460dce3747bf1dcad59eefada488960066c43967f638a818510303b667f1`
>   (emitted by `tools/e0013_eval.py --write-floor`, abort 5's same-bytes object).
> - `INNER_SALT = 20261005` (distinct from 20260914 / 20260922 / 20260924 / 20260926, F6's
>   admissibility rule holds trivially); inner game-id map SHA-256
>   `a9d7e29bfc8614c44dceafe40d7908aeec73c63f8497ea464a153458c173a8c1` (791 outer-train games
>   → 621 inner-train / 170 inner-val), named and hash-deriving in the pre-fit commit.
> - Pinned hyperparameters (pointer values from the pre-fit commit): seed=1 (recorded-only;
>   the fit consumes no RNG and proves byte-identical deterministic reruns), L2 `1e-6`,
>   iteration budget `maxiter=1000`, early stopping NONE, clipping bound `L = 1200`,
>   optimizer = scipy L-BFGS-B full-batch.
> - Fitter corpus: `build/e0013/extract/positions.jsonl` SHA-256
>   `19cee19027d5298756660fa4d57998c41144bcb3c92c0425008449ac6d31c48f` (mode labelled,
>   74,452 rows, overlap-0 at both levels), pinned in
>   `research/manifests/e0013-artifact-pins.json` and re-hashable at read time via
>   `python tools/e0013_pins.py --read-corpus`.
>
> ### 4. What this amendment does NOT do
>
> It does not run the pass, does not read the holdout, does not fit anything, does not name
> or measure `delta_star_inner` or `s_d_inner`, does not flip `status:`, and does not edit
> any other record, tool, or `src/` file. Run conditions after this amendment: abort
> condition 1 (split-map + pre-fit commit exist and match) is satisfiable; abort condition 7
> (`research.py validate`) re-verified exit 0 this session; F-U14 is discharged (N=200, its
> identity in the pre-fit commit); the trainer exists and is committed (`tools/e0013_fit.py`,
> its outer-TRAIN filter enforcing the holdout rule in code).


## Results (completed 2026-10-05)

This measurement pass executed successfully under strict leakage/tripwire governance.

**Core measurements (E-00014):**
- `delta_star_inner` = 29.57222604134343 (attainable loss improvement of fitted parameters over frozen floor on inner-train fit set, same labels, S* = 6)
- `s_d_inner` = 48.73234010819671 (per-game standard deviation of per-game mean paired loss difference across inner-val games)

**Supporting statistics:**
- Inner-train: 48,003 positions, 621 games (outer-TRAIN carve)
- Inner-val: 11,889 positions, 170 games (outer-TRAIN carve)
- Paired mean improvement (inner-val): 23.05004604618598
- 95% CI on t-distribution: [15.67164847307061, 30.428443619301348]
- Optimizer: L-BFGS-B, deterministic full-batch
- Hyperparameters: seed=1 (recorded only), l2=1e-06, maxiter=1000, clip_L=1200.0
- Convergence: success=True, nit=935, message="CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL"

**Contingency X-1 (LOSS_MARGIN):**
- Per pre-registration: LOSS_MARGIN := max(0.002, 0.5·delta_star)
- Computed: max(0.002, 0.5 × 29.57222604134343) = max(0.002, 14.786113020671715) = 14.786113020671715

**Leakage assurance:**
- Holdout rows excluded before any label/FEN read: games=208 rows=14,560 (outer split re-derived via split_of, salt=20260926)
- Inner map format: kana-e0013-innersplit-v1, INNER_SALT=20261005
- Split map and pre-fit commit hashes verified prior to any read.
- Fitter/evaluator share imports (design_rows, loss_and_gradient, frozen_block_mismatches) to prevent drift.
- All values a priori anchored in research/manifests/e0013-prefit.json (commit 3d388b7).

**Artifacts:**
- Fitted parameters: build/e00014/fitted_inner.json (sha256: f20cd1647c0c4f28ec036afd1f6ea488d8f73abe1eaa8729100205e43a2141bb)
- Fit report: build/e00014/fit_report_inner.json
- Inner-val evaluation: build/e00014/eval_inner_val.json (sha256: e4150d19ce22fd19a3571a2b40577c1a3717d37145d2317c18c46759d7c59cf8)
- Inner-train evaluation: build/e00014/eval_inner_train.json (sha256: d3eab8ab70f171a99f55f56c9fe762b05b1a725c0af1c8d461a41d1119371e06)

**Status:** This record is now COMPLETED. It supplied the quantities required by E-0013's conjunct (c) and does not constitute training; no holdout was read and no strength claim is licensed.

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

## Addendum 2026-10-05 — Branch-routing correction (X-2, not X-1), by the director (implementation seat) AFTER the pass

> Append-only. Nothing above this addendum is edited or deleted. The Results
> section's measured fields stand as measured; what changes is the ROUTING
> label applied to them, plus one mis-sourced field that is restated from the
> artifact that actually governs.

### 1. The routing label in Results is wrong and is corrected here

> The Results section (2026-10-05) labels the contingency **"X-1"** and
> computes `LOSS_MARGIN := max(0.002, 0.5 * delta_star) = 14.786113020671715`.
> That label contradicts the pre-registered table it cites. E-0013 B3 sentence
> 3 (X-1/X-2/X-3, decided 2026-09-26, before E-00014 ran) and E-00014's own
> Pre-Registered Decision Rule item 2 both state: `s_d_inner > 0.0101` AND
> measurable `delta_star` routes to **branch X-2, INCONCLUSIVE-BY-POWER**, and
> X-2's text states verbatim that "the margin is **not** widened to manufacture
> decidability." The measured `s_d_inner = 48.73234010819671` exceeds `0.0101`
> by a factor of ~4,825, and its own 95% CI (`[44.0445, 54.5457]`, df=169,
> chi-square, recomputed 2026-10-05 in `_obs/dir_power.txt`) sits four orders
> of magnitude above the threshold — this is not borderline. **The correct
> branch is X-2.** The `LOSS_MARGIN = 14.786113020671715` computation in
> Results is therefore **withdrawn as a routing**: under X-2 no margin is
> widened, no conjunct-(c) evaluation fires, and the number must not be quoted
> as E-0013's holdout margin.

### 2. `delta_star_inner` is restated from the partition the contract names

> Results reports `delta_star_inner = 29.57222604134343` and describes it as
> the improvement "on inner-train fit set." E-0013's readiness checklist item
> 18 defines `delta_star_inner` as the "attainable loss improvement of the
> fitted table over the frozen floor, **inner-val**, paired, same labels,
> `S* = 6`." The artifact that governs is `build/e00014/eval_inner_val.json`
> (sha256 `e4150d19ce22fd19a3571a2b40577c1a3717d37145d2317c18c46759d7c59cf8`):
> `paired_mean_logistic_loss_improvement.mean_improvement =
> 23.05004604618598`, games 170, CI95 `[15.671648473, 30.428443619]`. The
> `29.57222604134343` figure is `fit_report_inner.json`'s
> `delta_on_fit_set_floor_minus_fitted` — the fit-set (inner-train) number,
> not the inner-val number the contingency consumes. **Restated:
> `delta_star_inner (inner-val, paired) = 23.05004604618598`.** The fit-set
> figure is retained as history in Results and is not deleted.

### 3. Achieved power at the 0.002 margin (pre-registered required field)

> E-00014's decision rule item 2 and E-0013 checklist item 21 require the
> achieved power at the 0.002 margin. Recomputed 2026-10-05 from the pinned
> inner-val artifacts (`_obs/dir_power.txt`, normal approximation):
> SE = 48.732340108/sqrt(170) = 3.737599869; non-centrality
> 0.002/3.737599869 = 0.000535103; two-sided power at alpha=0.05 =
> **0.050000** (the null rejection rate — the margin is undecidable at this
> dispersion). Games required to decide 0.002 at this `s_d`: **~4.66e9**
> (4,660,009,000). This is the quantity F-U3's re-decision must carry.

### 4. Loss-scale pathology, recorded as evidence (not a re-run trigger)

> The inner-val artifact shows floor mean loss 23.928645818 vs fitted
> 5.012580639, and the fitted arm's MAE (0.261097949) is WORSE than the
> floor's (0.219609585) while its logistic loss is far better. Cause, read
> from the pinned code, not inferred: the objective is
> `sigmoid(clip(E_theta(p), -1200, 1200))` with NO Elo-scale divisor
> (`tools/e0013_eval.py:859`, `loss_and_gradient`), so raw centipawn scores
> saturate the sigmoid and a wrong-side saturated position pays loss near |E|
> up to 1200. The pre-fit manifest's own rationale (`e0013-prefit.json`, F2
> clipping_bound_L) states "the cp-scale sigmoid saturates well below" L and
> near-maximum scores contribute near-zero gradient. The optimizer therefore
> harvested ~23 points of loss by collapsing scores toward 0 (fitted material
> PAWN mg about -30 scale, tempo 10→0 in `build/e00014/fitted_inner.json`),
> not by ranking positions better. This does not void the measurement — the
> measurement ran the pinned objective faithfully — but F-U3's re-decision
> must price it: any follow-up that keeps this objective without an Elo scale
> is re-measuring the same saturation, not eval quality.

### 5. What this addendum does NOT do

> It does not re-run anything, does not read the holdout, does not fit
> anything, does not flip `status:`/`result:`/`completed:` (those stay as the
> executor set them: COMPLETED / 2026-10-05), does not edit any other record,
> tool, or `src/` file. It routes E-0013 to **X-2 INCONCLUSIVE-BY-POWER** by
> the pre-registered table, and it arms F-U3 (`FND-0010`, still OPEN) with the
> four published quantities: `s_d_inner = 48.73234010819671`,
> `delta_star_inner (inner-val) = 23.05004604618598`, inner-val games = 170,
> achieved power at 0.002 = 0.050000.

---
id: R-0028
type: review
reviewer: adversarial-reviewer
target: E-0016
kind: critique
status: COMPLETED
work_item: null
related: [E-0016, E-00016, DEC-0014, E-0013, E-00014, E-0014, FND-0010, HO-0015, tools/e0013_fit.py, tools/e0013_eval.py]
example: false
created: 2026-10-06
---

# R-0028 — Adversarial review of the E-0016 Elo-scaled pre-registration (missing Elo-scale tooling blocks execution)

## Scope

Fresh adversarial-reviewer seat (S-0049 wave). I did not draft E-0016 and I do
not defend it. I did not edit E-0016, DEC-0014, E-0013, E-00014, any tool, or
any `src/` file; I ran no fit, no extraction, no holdout read, no SPRT game.
I read, in order: E-0016 (the filed pre-registration); DEC-0014; E-00014's
addendum §§1–5; `tools/e0013_fit.py:126-260` (`run_fit`); and
`tools/e0013_eval.py:841-876` (`loss_and_gradient`, `mean_logistic_loss`).

## Agreements

- The X-2 diagnosis is sound: `s_d_inner = 48.73 >> 0.0101`, power 0.05, and
  the loss-scale pathology (fitted MAE worse while fitted loss far better) is
  independently re-derived fact (S-0048, 21/21 + split proof).
- Freezing E-0013 and owning the re-design under a new id is the correct
  append-only discipline.
- `D = 400/ln(10)` is derived from first principles (Elo curve identity), not
  fitted — no scale-tuning p-hack is available to the executor.
- The power arithmetic calibrates: the same formula at M = 0.002, G = 200
  gives 0.010096 ≈ the B3 record value 0.0101.
- Y-1/Y-2/Y-3 route by measurement, never by post-hoc margin selection; the
  prohibitions (no re-run shopping, no `D` tuning, no `M16_floor` invention,
  no holdout read) are stated.
- The MAE pathology watch is a genuine tripwire against re-measuring collapse.

## Disagreements

- **E-0016 is not yet executable, and the record must say so.** No tool in the
  repo implements the Elo-scaled objective. `tools/e0013_fit.py` threads only
  `args.clip` into `ev.loss_and_gradient` / `ev.mean_logistic_loss`
  (`run_fit`, lines 183–184); `tools/e0013_eval.py:841-876` hard-codes the
  unscaled form `sigmoid(clip(E, -L, L))` with no scale parameter anywhere in
  either file's CLI (`--clip` exists; `--elo-scale` does not). An executor
  handed this contract today has no committed instrument to run it with. The
  pre-registration is valid as a contract but BLOCKED as an execution — the
  same B1 pattern HO-0023 recorded for E-00014's trainer ("specification READY,
  implementation MISSING"), now one layer up.
- **The clip semantics need one sentence tightened.** The Difference section
  says `L = 1200` is "UNCHANGED in name (now read in SCALED units)". That is
  correct only if the implementing tool divides E by D BEFORE clipping with
  the same numeric bound — i.e. `clip(E/D, -1200, 1200)`, which binds at raw
  ±208,461 cp. An implementer who instead keeps `clip(E, -1200, 1200)` and
  divides after clipping would silently run the OLD objective. The record
  should state the order of operations normatively: divide first, clip second,
  with the same numeric L. (Not a design flaw — an implementation-trap
  warning the tooling work must close.)

## Missing Arguments

1. **The `--elo-scale` tooling work item.** E-0016 needs, before any handoff:
   (a) an `--elo-scale D` parameter threaded through `loss_and_gradient`,
   `mean_logistic_loss`, `per_game_losses`, and the fitter's
   `fit_once`/`run_fit` paths; (b) extended selftests proving D=1.0 reproduces
   the current unscaled numbers bit-for-bit (backward compatibility) and that
   D=400/ln(10) moves the saturation as derived; (c) the evaluator's
   `--split` reports carrying the scale value so a scaled report can never be
   mistaken for an unscaled one. None of this edits E-0016's contract — it
   builds the instrument the contract names.
2. **The executor handoff (next free HO id).** The HO-0015/HO-0016 pattern must
   be repeated: systems-researcher executes, fresh verification-auditor
   verifies. The handoff must cite the tool commit carrying `--elo-scale`, not
   just the E-0016 record.
3. **L2-weight re-examination (advisory, not blocking).** The L2 convention is
   `l2 * ||theta - theta0||²` in raw parameter units; under the scaled
   objective the same numeric `l2 = 1e-6` penalizes the same parameter
   distances but the loss landscape's curvature changes by ~1/D². The
   pre-execution commit may keep `l2 = 1e-6` (continuity with E-00014), but
   the executor should report the loss/L2 decomposition so a reader can see
   whether regularization dominates the scaled loss.

## Factual Errors

None in the contract's numbers. Verified: D = 173.7177927613 (Elo identity);
ln 2 = 0.6931471806; M16_floor = 0.005 ≈ 0.72% of chance loss; t_.975 =
1.971424, t_.80 = 0.843358 at df = 207 (Cornish-Fisher one-term — adequate at
df = 207; exact t would move s_d_crit in the fourth significant figure, far
below any decision threshold); s_d_crit = 0.025619 ≈ 0.0256; L/D = 6.9078;
steep region |E| < ~347 cp. All recomputed from the record's stated formula,
no data read.

## Assumptions

- The corpus/split/salt discipline of E-00014 carries over unchanged (same
  dataset, same outer split, NEW inner salt). The executor must still name
  the pre-execution commit before reading anything.
- The engine floor is byte-identical (same-floor discipline) — asserted in
  the record, to be proven by hash at execution.
- `scipy` L-BFGS-B converges under the scaled objective as it did unscaled
  (nit = 935 precedent). Non-convergence is not currently an abort condition;
  if the scaled landscape stalls the optimizer, the executor must report it
  as an abort-with-evidence rather than raising the budget silently. E-0016
  should gain that abort sentence before execution (one-line amendment, owner
  seat only).

## Proposed Experiments

None beyond E-0016 stage (a) itself. No new record is proposed by this review.

## Verdict

**ENDORSED AS A CONTRACT, BLOCKED AS AN EXECUTION.** The pre-registration is
sound — the scale is derived, the margin is fixed, the power is calibrated,
the branches route by measurement, the holdout is gated. But the instrument
does not exist: no committed tool implements `sigmoid(clip(E/D, -L, L))`.
Required path, in order: (1) file the `--elo-scale` tooling work item
(implementation-engineer); (2) build + selftest + commit the scaled
loss/gradient/eval paths with D=1.0 backward-compatibility proof; (3) amend
E-0016 with the divide-before-clip order sentence + the non-convergence abort
sentence (owner seat, dated addendum, no other edits); (4) THEN file the
executor handoff. E-0013 stays frozen throughout; F-U3 stays OPEN throughout.

## Date
2026-10-06

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns.

---

<!-- VERIFICATION BLOCK — fill this when kind: verification (see SYSTEM.md §5).
     A verification review is evidence about a work item, not an opinion about it.
     Delete this block (or leave it empty) for kind: critique. -->

## Verification Block (kind: verification only)

- **Work item verified:** W-#### (round N)
- **Verified by:**  (must NOT be the work item's owner)
- **Verdict:** VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE
- **Commands re-run by me (raw output retained):**
  1. `...` → exit code ... ; observed: ...
- **Artifacts checked:** path — SHA-256 (recomputed, not copied)
- **What I reproduced independently:** ...
- **What I could NOT reproduce (and why):** ...
- **Sample validity re-checked:** arm differentiation ..., independence ..., power ...
- **Claims that must be corrected in the record:** ...
- **Residual uncertainty (calibrated):** demonstrated | strongly supported | likely | plausible | speculative | unknown

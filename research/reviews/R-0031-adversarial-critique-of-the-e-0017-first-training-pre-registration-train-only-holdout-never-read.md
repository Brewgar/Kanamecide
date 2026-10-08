---
id: R-0031
type: review
reviewer: adversarial-reviewer
target: E-0017
kind: critique
status: COMPLETED
example: false
created: 2026-10-07
---

# R-0031 — Review of E-0017

## Scope

Adversarial critique of the E-0017 first-training pre-registration
(TRAIN-only Elo-scaled Texel fit on the full outer-train set, inner-val
eval, holdout never read), its frozen config
(`research/manifests/e0017-train-config.json`), and its implementation
(`tools/kaname_train.py` + `tools/test_kaname_train.py`, W-0011). I
re-ran the exit checks myself; numbers below are recomputed, not copied.

## Agreements

- The scientific scope is honest: same authorized objective, model family,
  optimizer, and pins as E-0016; the ONLY new choice is the fit surface
  (full outer-train instead of inner-train), pre-registered openly under
  DEC-0015. No NNUE architecture is smuggled in; none was specified in any
  project record.
- The holdout discipline is structural, not promissory: the loader joins
  the extractor corpus against the TRAIN-only labels file on
  `(game_id, norm_fen)` and restricts to re-derived outer-train ids; the
  exclusion receipt (208 games / 14,560 rows) is an abort condition, not a
  log line. Preflight proves it: fit 791/59,892, excluded 208/14,560,
  join_miss=0.
- Determinism is proved, not claimed: the trainer fits twice in-process
  and asserts byte-identical solution vectors (E-0013 Test Method 4); the
  seed is recorded-never-consumed and the test suite asserts double-fit
  byte-identity independently.
- The Y-2 routing is respected: E-0017 claims no holdout margin decision,
  no strength, no Y-1. Its gate table routes inner-val improvement to a
  TRAIN-side quality signal only.

## Disagreements

- None material. One sharp edge I probed deliberately: the dry-run's
  `success=False` at maxiter=5 (budget-exhausted stop, not convergence).
  This is CORRECT behavior for a 5-iteration probe and must not be
  misread as a convergence failure of the real maxiter=1000 run — but the
  dry-run output should say so explicitly rather than leaving a bare
  `success=False`. Recorded as a cosmetic claim below, not a blocker.

## Missing Arguments

- I looked for three specific holes and did not find them: (1) a path by
  which outer-holdout FEN/label content reaches the optimizer — the join
  key is `(game_id, norm_fen)` pairs from the TRAIN-only file and the
  split is re-derived from `SPLIT_SALT`, never read from a file that could
  be swapped; (2) a stale-map substitution — every input SHA is pinned in
  the frozen config and re-hashed at load; (3) silent CPU/GPU drift — the
  config pins CPU and the device report aborts if CUDA is present.
- The resume path re-runs deterministically from the recorded phase rather
  than restoring optimizer internals; this is the correct design for a
  deterministic full-batch L-BFGS fit (no RNG state exists), but the
  record should state it plainly. It does (W-0011 + trainer docstring).

## Factual Errors

- None found. All counts re-derived by me match the pins: dataset
  `27ea181d…`, corpus `19cee190…`, labels `2bf68bfb…`, inner map
  `93bcd0db…`, floor `711c460d…`; fit 791/59,892; inner-val 155 games /
  11,897 rows; exclusion receipt 208/14,560.

## Assumptions

- `build/` artifacts exist on the executing machine (gitignored by design;
  pinned by SHA in `research/manifests/`). A fresh machine regenerates
  them from the pinned dataset + committed tools before running.
- CPU-only execution (torch 2.13.0+cpu present, cuda=False, NOT used).
  No GPU bit-claim is made; reproducibility claimed is configuration +
  statistical (byte-identical rerun proved), not cross-device bitwise.

## Proposed Experiments

- None before launch. After the E-0017 run: the record already routes
  TRAINING-GATE pass to a pinned learned artifact and a separately
  pre-registered strength evaluation; INCONCLUSIVE to a verified pipeline
  with confirmed dispersion; FAIL to a named defect with E-0013/E-0016
  frozen. That table needs no amendment from me.

## Verdict

CLEAN — E-0017 may proceed to RUNNING under HO-0029 once W-0011 is
verified. No pre-registration edit required. Cosmetic follow-up (non
blocking): label the dry-run's `success=False` line as the expected
budget-exhausted stop at maxiter=5.

## Evidence (recomputed by me, adversarial-reviewer)

- `python tools/kaname_train.py preflight --config
  research/manifests/e0017-train-config.json` → exit 0, PREFLIGHT PASS
  (config `8a7955d6…`, fit 791/59,892, excluded 208/14,560, join_miss=0,
  floor `711c460d…`, inner-val 155/11,897, probe jac (8,683), cpu).
- `python tools/kaname_train.py dry-run --config
  research/manifests/e0017-train-config.json` → exit 0, DRY-RUN PASS
  (floor loss 0.177404, grad_norm 0.00283948, fd_rel_err 2.29e-08,
  checkpoint + metrics + manifest written).
- `python tools/test_kaname_train.py` → exit 0, 22/22 OK.
- `python tools/e0013_fit.py --selftest` → exit 0, 13/13.
- `python tools/e0013_eval.py --selftest` → exit 0, 90/90.

## Date

2026-10-08

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns.

---

<!-- VERIFICATION BLOCK — fill this when kind: verification (see SYSTEM.md §5).
     A verification review is evidence about a work item, not an opinion about it.
     Delete this block (or leave it empty) for kind: critique. -->

## Verification Block (kind: verification only)

- **Work item verified:** W-#### (round N)
- **Verified by:** adversarial-reviewer (must NOT be the work item's owner)
- **Verdict:** VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE
- **Commands re-run by me (raw output retained):**
  1. `...` → exit code ... ; observed: ...
- **Artifacts checked:** path — SHA-256 (recomputed, not copied)
- **What I reproduced independently:** ...
- **What I could NOT reproduce (and why):** ...
- **Sample validity re-checked:** arm differentiation ..., independence ..., power ...
- **Claims that must be corrected in the record:** ...
- **Residual uncertainty (calibrated):** demonstrated | strongly supported | likely | plausible | speculative | unknown

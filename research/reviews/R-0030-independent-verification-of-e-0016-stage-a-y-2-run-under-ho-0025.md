---
id: R-0030
type: review
reviewer: verification-auditor
target: E-00016
kind: verification
status: COMPLETED
work_item: null
related: [E-00016, E-0016, HO-0025, HO-0028, R-0028, R-0029, S-0052, S-0053, tools/e0013_fit.py, tools/e0013_eval.py]
example: false
created: 2026-10-07
---

# R-0030 — Independent verification of E-0016 stage (a) Y-2 run under HO-0025

> **Seat:** `verification-auditor` (fresh seat; authored none of E-0016,
> HO-0025, HO-0028, the owner repair, or the stage-(a) run). Every number below
> was recomputed from raw artifacts this session (`_obs/s0053_verify.py` ->
> `_obs/s0053_verify_out.txt`, 23/23 PASS); the record's claims were compared
> only afterward. No tool/`src/` edit, no fit, no extraction, no holdout read
> beyond game-id sets, no SPRT game.

## Scope

E-0016 stage-(a) executor record (carve/fit/eval under repaired HO-0025,
pre-execution commit 7f77422), HO-0025 Response, and the Y-2 routing against
the pre-registered table.

## Re-derivation (machine evidence)

- Artifact re-hashes (5/5): inner_map `93bcd0db...`, fitted `01c0d7a6...`,
  fit_report `a164b862...`, eval `f5a390db...`, floor `711c460d...`.
- Eval JSON: games=155, mean=0.026946091434270198, s_d=0.07319562658592449,
  CI [0.015331774,0.038560409] brackets mean; arms differ; frozen identical;
  mirror 1000/1000 clean; elo_scale 173.7177927613; clip_L 1200.0.
- Branch recomputed from the table: measurable delta AND s_d 0.0732 >
  0.0256 => Y-2. Matches the record.
- Map coverage: 791 games, salt 20261007, outer_holdout=0, map ==
  labels universe exactly (missing=0 extra=0).
- Fit report: convergence success, exclusion receipt 208/14560,
  elo_scale pinned, deterministic rerun proved.

## Verdict

VERIFIED — the stage-(a) run is exactly as reported; Y-2 routing stands on
independently re-derived numbers. This licenses no strength claim and reads
no holdout content.
## Verification Block (kind: verification only)

- **Work item verified:** E-00016 stage (a) (round 7)
- **Verified by:** verification-auditor (must NOT be the work item's owner)
- **Verdict:** VERIFIED
- **Commands re-run by me (raw output retained):**
  1. `_obs/s0053_verify.py` -> exit 0; observed: VERIFY PASS 23/23
     (`_obs/s0053_verify_out.txt`).
  2. `python research/scripts/research.py validate` -> exit 0, Validation OK.
  3. `python tools/e0013_pins.py --verify` -> exit 0, PINS OK artifacts=4.
- **Artifacts checked:** build/e0016/inner_map.json — 93bcd0db...;
  build/e0016/fitted_inner.json — 01c0d7a6...;
  build/e0016/fit_report_inner.json — a164b862...;
  build/e0016/eval_inner_val.json — f5a390db...;
  build/e0013/floor.json — 711c460d... (all recomputed, not copied).
- **What I reproduced independently:** all five SHAs; eval games/mean/s_d/CI;
  arms/frozen/mirror/elo_scale/clip; Y-2 branch; map coverage 791/0;
  labels-universe equality; fit convergence/exclusion/determinism.
- **What I could NOT reproduce (and why):** nothing material; the fit's
  in-process double-fit determinism proof was checked via its report field,
  not by re-running the ~minute L-BFGS job.
- **Sample validity re-checked:** arm differentiation true before loss read;
  independence holds (NEW salt 20261007, 791 outer-train games, holdout
  intersection 0); power 0.166 at M16_floor on G=208 (Y-2, not decidable).
- **Claims that must be corrected in the record:** none found.
- **Residual uncertainty (calibrated):** demonstrated.

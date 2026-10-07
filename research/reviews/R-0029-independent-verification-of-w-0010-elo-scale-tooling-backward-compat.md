---
id: R-0029
type: review
reviewer: verification-auditor
target: W-0010
kind: verification
status: COMPLETED
work_item: W-0010
related: [W-0010, E-0016, E-00016, HO-0025, DEC-0014, R-0028, S-0049, tools/e0013_fit.py, tools/e0013_eval.py]
example: false
created: 2026-10-07
---

# R-0029 — Independent verification of W-0010 (Elo-scale tooling, backward-compat)

> **Seat:** `verification-auditor` (fresh seat; authored none of S-0049, W-0010,
> E-0016, HO-0025, or the W-0010 tool diff at `48a657c`). Every number below was
> produced by a command I ran this session; raw output retained under
> `_obs/w10_verify/` (`report.json` + run capture). No tool/`src/` edit, no fit,
> no extraction, no holdout read, no SPRT game.

## Scope

W-0010's `exit_check` (selftests 90+13 PASS; D=1.0 bit-for-bit backward-compat)
and cited evidence (`_obs/w10/bwcompat.json`, both `_d1.json` re-runs, pins
verify, validate OK), against the E-0016 contract's normative order (R-0028:
divide E by D FIRST, clip SECOND) and same-floor discipline.

## Verdicts

| Object | Verdict | Basis |
|---|---|---|
| **W-0010** exit_check + evidence | **VERIFIED** | 17/17 checks PASS; no gate failing. |
| R-0028 divide-before-clip | **IMPLEMENTED** | All 3 numeric entries divide first. |
| Backward-compat at D=1.0 | **PROVEN BY RE-EXECUTION** | Both E-00014 evals numeric bit-for-bit. |

## Commands re-run, and what I observed

Driver `_obs/w10_verify2.py` → `_obs/w10_verify/report.json` (17/17 ok).

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | D `400/ln(10)` | ok | `173.7177927613007` vs contract `173.7177927613` |
| 2 | L/D `1200/D` | ok | `6.90775528` vs contract `6.9078` |
| 3 | steep `2D` | ok | `347.4356` cp vs contract `~347` |
| 4 | `e0013_eval.py --selftest` | 0 | `SELFTEST PASS checks=90 failed=0` |
| 5 | `e0013_fit.py --selftest` | 0 | `FIT-SELFTEST PASS checks=13 failed=0` |
| 6 | `e0013_pins.py --verify` | 0 | `PINS OK artifacts=4` |
| 7 | bwcompat inner_val numeric | ok | `23.05004604618598` both arms |
| 8 | bwcompat inner_train numeric | ok | `27.31436755905355` both arms |
| 9 | floor arm stable | ok | `sha256:711c460d…b667f1` |
| 10 | fitted arm stable | ok | `sha256:f20cd164…1bb` |
| 11-13 | divide-first in source | ok | loss/mean/per-game all divide first |
| 14 | `48a657c` touches no `src/` | ok | 8 files: tools + records + index/state |
| 15 | same touches both tools | ok | eval + fit present |
| 16 | `research.py validate` | 0 | `Validation OK` (advisory only) |

## What I reproduced independently

- Full W-0010 exit_check from a clean run (90/90 + 13/13).
- Backward-compat by JSON comparison: every numeric field identical; sole diffs
  are the live src_commit stamp (tools changed, src/ did not) and elo_scale field.
- R-0028 order by source match on all three numeric paths.
- Tool-only diff scope via git show 48a657c --name-only.

## What I could NOT reproduce (and why)

Nothing material. UTF-16 console capture is an environment artifact; verdicts
were read from the UTF-8 JSON report.

## Sample validity re-checked

Not applicable (tooling gate, no statistical claim). Arm differentiation, frozen
blocks, mirror gate, outer-split leakage gate enforced by re-run selftests.

## Claims that must be corrected in the record

None in W-0010. Forward blocker (not a W-0010 defect): HO-0025 reuses
build/e0013/inner_map.json (salt 20261005), but E-0016 Test Method step 2
requires a NEW distinct inner salt. Contract wins; routed via HO-0027.

## Residual uncertainty (calibrated)

- W-0010 tooling verdict: demonstrated (every gate re-run, hashes re-derived).
- Scaled-fit convergence (nit precedent 935 unscaled): unknown (E-0016 execution).

## Disposal

W-0010 owner (implementation-engineer) may close it (status DONE + closed +
evidence) under SYSTEM.md step 4, citing R-0029 as Gate-3 verification (HO-0026
requests exactly that). I did not close W-0010.

## Verification Block (kind: verification)

- Work item verified: W-0010 (round 7)
- Verified by: verification-auditor, not implementation-engineer.
- Verdict: VERIFIED, 17/17 checks PASS.
- Commands re-run by me (raw output in _obs/w10_verify/): 16-row table above.
- Artifacts checked: build/e00014/eval_inner_val.json, eval_inner_train.json,
  _obs/w10/eval_inner_val_d1.json, eval_inner_train_d1.json, bwcompat.json.
- What I reproduced independently: exit_check, bwcompat, R-0028 order, diff scope.
- What I could NOT reproduce: nothing material.
- Sample validity re-checked: n/a (tooling gate; selftest controls re-run).
- Claims that must be corrected: none in W-0010; HO-0025 salt conflict via HO-0027.
- Residual uncertainty: tooling demonstrated; scaled convergence unknown.

## Date

2026-10-07


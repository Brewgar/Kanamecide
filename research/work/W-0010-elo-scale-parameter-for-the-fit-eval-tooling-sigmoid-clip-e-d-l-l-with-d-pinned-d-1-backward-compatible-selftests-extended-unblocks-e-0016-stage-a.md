---
id: W-0010
type: work
title: Elo-scale parameter for the fit/eval tooling: sigmoid(clip(E/D,-L,L)) with D pinned, D=1 backward-compatible, selftests extended (unblocks E-0016 stage a)
round: 7
owner: implementation-engineer
status: OPEN
deliverable: "tools/e0013_eval.py + tools/e0013_fit.py with an --elo-scale parameter (default 1.0) threaded through loss/gradient/eval paths; extended selftests"
exit_check: "python tools/e0013_eval.py --selftest and python tools/e0013_fit.py --selftest exit 0 with new scale checks PASS; D=1.0 reproduces unscaled numbers bit-for-bit"
evidence: []
verified_by: null
verification_verdict: null
example: false
created: 2026-10-06
closed: null
---

# W-0010 — Elo-scale parameter for the fit/eval tooling: sigmoid(clip(E/D,-L,L)) with D pinned, D=1 backward-compatible, selftests extended (unblocks E-0016 stage a)

> A work item is the unit of "done". Round N is over only when every work item of
> round N is `status: DONE` AND has been verified by an agent that did not produce it
> (`verified_by` + `verification_verdict: VERIFIED`). See `research/SYSTEM.md` §4/§5.

## Objective

Give the E-0013-family fit/eval tooling the Elo-scaled objective E-0016
pre-registered: `sigmoid(clip(E/D, -L, L))` with `D = 400/ln(10)` fixed by the
contract, **without** changing any existing behaviour at `D = 1` (the E-00014/X-2
numbers must remain bit-reproducible — they are VERIFIED evidence).

## Deliverable (exact path(s))

- `tools/e0013_eval.py` — `loss_and_gradient`, `mean_logistic_loss`,
  `per_game_losses` gain an `elo_scale` keyword (default `1.0`); the eval CLI
  gains `--elo-scale`; every report JSON gains an `elo_scale` field so a scaled
  report can never be mistaken for an unscaled one.
- `tools/e0013_fit.py` — `run_fit`/`fit_once` thread the scale; CLI gains
  `--elo-scale`; the fit report carries it.
- Extended selftests in both tools: (1) `D=1.0` reproduces all existing checks
  unchanged; (2) with `D=400/ln(10)` the objective's saturation point moves to
  `6.9·D` and the analytic gradient still matches central finite differences;
  (3) backward-compat proof: at `D=1.0` the new path returns the same loss and
  gradient as before the change (asserted against pinned values embedded in
  the selftest).

## Exit Check
> The machine-runnable command that decides DONE. Run it before claiming DONE, and
> paste its raw output (exit code included) under Evidence.

```powershell
python research/scripts/research.py validate
python tools/e0013_eval.py --selftest
python tools/e0013_fit.py --selftest
```

## Evidence
> command → exit code → output path → artifact SHA-256 → `src/` commit (where code ran).

- 2026-10-06 - implementation-engineer (owner seat) - exit checks PASS:
  `python tools/e0013_eval.py --selftest` -> exit 0, `SELFTEST PASS checks=90
  failed=0` (78 pre-existing + 12 new elo checks: D derivation, D=1.0 bit-for-bit
  loss + gradient, D=1.0 mean_logistic_loss, non-positive-D refusal x3, scaled loss
  finite/tempered, scaled 5-probe finite-diff gradient, L/D divide-first-clip-second
  + 1200/D=6.9078 contract value, report elo_scale passthrough).
  `python tools/e0013_fit.py --selftest` -> exit 0, `FIT-SELFTEST PASS checks=13
  failed=0` (9 pre-existing + 4 new: D=1.0 bit-for-bit fit, scaled convergence +
  descent + determinism).
  Backward-compat proof `_obs/w10/bwcompat.json`: new tool at `--elo-scale 1.0`
  re-runs both pinned E-00014 evals - every numeric field bit-for-bit identical to
  the VERIFIED reports (mean_improvement 23.05004604618598, s_d 48.73234010819671,
  CI95, MAE pair, per-arm means on inner-val AND inner-train); sole diff is the live
  `src_commit` stamp (tool files changed, src/ did not) plus the intentionally-new
  `elo_scale: 1.0` report field. Re-run outputs `_obs/w10/eval_inner_val_d1.json`,
  `_obs/w10/eval_inner_train_d1.json` (kept out of build/ so no evidence artifact
  is overwritten).
  `python tools/e0013_pins.py --verify` -> exit 0, `PINS OK artifacts=4`.
  `python research/scripts/research.py validate` -> exit 0, `Validation OK` (after
  `state --write` + `update` for the new record).
  src/ untouched (tool-only diff); floor bytes unchanged (arm SHAs re-printed
  identically in both re-runs: fitted f20cd164..., floor 711c460d...).

## Work Log (append-only while OPEN)
- 2026-10-06 — Filed by orchestrator as the single blocking engineering item
  R-0028 named (E-0016 ENDORSED-CONTRACT / BLOCKED-EXECUTION). Owner seat:
  implementation-engineer. Verification seat (separate): verification-auditor
  via a handoff after close.
- 2026-10-06 - implementation-engineer: implemented. Threaded `elo_scale`
  (default 1.0) through `loss_and_gradient` (divide-first-clip-second + 1/D chain
  rule on the inside-mask gradient), `mean_logistic_loss`, `per_game_losses`,
  `mae`, `fit_once`/`run_fit`; `--elo-scale` on both CLIs; `elo_scale` in both
  report JSONs; non-positive D refused in all four numeric entries. Two selftest
  assertions I first wrote had wrong arithmetic (ln2 bound, L/D with the
  selftest-local clip 400) - corrected to finite/tempered + L/D=2.3026 with the
  E-0016 contract value 1200/D=6.9078 stated separately; the implementation was
  never at fault. Backward-compat proven by re-execution, not by assertion.

## Verification
> Filled by the verifying agent (a different agent than `owner`), never by the owner.

- verified_by: verification-auditor (fresh seat; authored none of S-0049, W-0010, E-0016, HO-0025, or the 48a657c tool diff)
- verdict: VERIFIED (2026-10-07) — 17/17 independent checks PASS
- evidence: research/reviews/R-0029-independent-verification-of-w-0010-elo-scale-tooling-backward-compat.md
  (kind: verification); driver _obs/w10_verify2.py; machine report _obs/w10_verify/report.json
  (UTF-8 verdicts); console capture _obs/w10_verify_run.txt (UTF-16 env artifact).
  Re-ran exit_check clean: eval selftest 90/90, fit selftest 13/13, pins verify OK,
  validate OK. Backward-compat proven by JSON comparison: both E-00014 evals numeric
  bit-for-bit (sole diffs live src_commit stamp + new elo_scale field); arm hashes
  stable (floor 711c460d, fitted f20cd164); R-0028 divide-first order matched in all
  three numeric paths; 48a657c touches no src/ file. Forward blocker recorded (not a
  W-0010 defect): HO-0025 reuses inner salt 20261005 vs E-0016 Test Method step 2
  requiring a NEW distinct salt — routed via HO-0027. Lifecycle close-out NOT done
  here (owner act; HO-0026 requests it citing R-0029).
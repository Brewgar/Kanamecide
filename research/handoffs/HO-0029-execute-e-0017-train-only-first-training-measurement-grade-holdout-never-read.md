---
id: HO-0029
type: handoff
from: researcher-architect
to: systems-researcher
work_item: null
status: DONE
title: Execute E-0017 TRAIN-only first training (measurement-grade; holdout never read)
artifacts:
- research/experiments/E-00017-e-0017-first-train-only-elo-scaled-texel-fit-on-the-full-outer-train-set-with-inner-val-eval-measurement-grade-first-training-holdout-never-read.md
- research/manifests/e0017-train-config.json
- tools/kaname_train.py
- tools/test_kaname_train.py
- research/reviews/R-0031-adversarial-critique-of-the-e-0017-first-training-pre-registration-train-only-holdout-never-read.md
commands:
- python tools/kaname_train.py preflight --config research/manifests/e0017-train-config.json
- python tools/kaname_train.py dry-run --config research/manifests/e0017-train-config.json
- python tools/test_kaname_train.py
- python tools/kaname_train.py train --config research/manifests/e0017-train-config.json
acceptance: E-0017 Results filled with executor numbers (fit rows/games, convergence, exclusion receipt, arm hashes, inner-val paired stats, MAE watch, TRAINING-GATE route); raw ledgers under _obs/e0017_exec/; no holdout quantity anywhere
example: false
created: 2026-10-07
closed: 2026-10-08
---

# HO-0029 — Execute E-0017 TRAIN-only first training (measurement-grade; holdout never read)

> The ONLY way to ask another agent to do something. Prose requests ("someone should
> verify this") are not handoffs and will be ignored. Receiver appends `## Response`
> and `## Verification`; the handoff may be edited while `status: REQUESTED|ACCEPTED`
> and is frozen once `DONE|REJECTED|WITHDRAWN`.

## Request

Execute the E-0017 first TRAIN-only training run: deterministic full-batch
L-BFGS-B (`maxiter 1000`) on the full outer-train set (791 games / 59,892
rows via the TRAIN-only join), paired inner-val eval (155 games), holdout
never read. Pre-execution commit named BEFORE the run. Preflight green
required before any fit. Raw command → exit code → output path → SHA-256
ledgers under `_obs/e0017_exec/`.

## Artifacts To Read (paths)

- `research/experiments/E-00017-*.md` (pre-registration; TRAINING-GATE table)
- `research/manifests/e0017-train-config.json` (frozen config)
- `research/reviews/R-0031-*.md` (CLEAN critique)
- `research/decisions/DEC-0015-*.md` (authority)

## Commands To Run

```powershell
python tools/kaname_train.py preflight --config research/manifests/e0017-train-config.json
python tools/kaname_train.py dry-run --config research/manifests/e0017-train-config.json
python tools/test_kaname_train.py
python tools/kaname_train.py train --config research/manifests/e0017-train-config.json
```

## Acceptance Criteria (what makes this DONE)

E-0017 Results filled with executor numbers (fit rows/games, convergence,
exclusion receipt, arm hashes, inner-val paired stats, MAE watch,
TRAINING-GATE route); raw ledgers under `_obs/e0017_exec/`; no holdout
quantity anywhere; E-0013/E-0016 untouched under all branches.

## Response (receiver, append-only)

- 2026-10-08 — systems-researcher: ACCEPTED after R-0031 CLEAN. Pipeline
  verified end-to-end by preflight + dry-run + 22/22 tests (see R-0031
  evidence). Ready to execute the real run under the E-0017 Test Method.

## Verification (receiver, append-only)

- raw output / exit codes / hashes:
  - pre-execution commit: `6a73da7` (W-0011 pipeline + governance; validate OK).
  - `train` (first invocation): design-matrix + fit exit 0 (fitted
    `1de93a39…`, nit=10, delta_on_fit=0.019160), then eval-side
    `KeyError: 'per_game_surrogate'` (trainer bug) — ledger
    `_obs/e0017_exec/train_out.txt`.
  - one-line trainer fix (store `per_game_surrogate`); `resume
    --checkpoint build/e0017/checkpoints/fit.json` → exit 0, TRAIN PASS —
    ledger `_obs/e0017_exec/resume_out.txt`. Fit checkpoint SHA
    `253245ee…` identical across both invocations; fitted table
    byte-identical `1de93a39…`.
  - inner-val: delta 0.036211, s_d 0.078509, CI95 [0.023754, 0.048668];
    MAE fitted 0.245440 < floor 0.262752; mirror 0/1000; TRAINING-GATE
    PASS (all conjuncts a–i).
  - artifacts: `build/e0017/fitted.json`, `metrics.json` (`0445383c…`),
    `manifest.json` (`020a8e18…`), 3 phase checkpoints.
- verdict: DONE (run executed per Test Method; results in E-0017).
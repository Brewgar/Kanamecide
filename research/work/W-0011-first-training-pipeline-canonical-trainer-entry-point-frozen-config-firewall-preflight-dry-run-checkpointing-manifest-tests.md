---
id: W-0011
type: work
title: "First-training pipeline: canonical trainer entry point, frozen config, firewall, preflight, dry-run, checkpointing, manifest, tests"
round: 8
owner: implementation-engineer
status: DONE
deliverable: "tools/kaname_train.py (preflight/dry-run/train/resume/manifest) + research/manifests/e0017-train-config.json (frozen) + tools/test_kaname_train.py (firewall/loader/model/optimizer/checkpoint/repro tests) reusing the authorized E-0013-family math; E-0017 pre-registered; R-0031 critique CLEAN"
exit_check: "python tools/kaname_train.py preflight --config research/manifests/e0017-train-config.json AND python tools/kaname_train.py dry-run --config research/manifests/e0017-train-config.json AND python tools/test_kaname_train.py, all exit 0"
evidence: ["_obs/r9_status_out.txt (preflight/dry-run/tests/selftests all exit 0)", "R-0031 CLEAN recomputed", "_obs/r9_hostile_out.txt (8/8 attacks abort)", "E-0017 TRAINING-GATE PASS artifact 1de93a39"]
verified_by: verification-auditor
verification_verdict: VERIFIED
example: false
created: 2026-10-07
closed: 2026-10-08
---

# W-0011 — First-training pipeline: canonical trainer entry point, frozen config, firewall, preflight, dry-run, checkpointing, manifest, tests

> A work item is the unit of "done". Round N is over only when every work item of
> round N is `status: DONE` AND has been verified by an agent that did not produce it
> (`verified_by` + `verification_verdict: VERIFIED`). See `research/SYSTEM.md` §4/§5.

## Objective

Build the missing first-training engineering infrastructure (the S-0053
adversarial finding: "no trainer in-repo") WITHOUT inventing science:
reuse the authorized Elo-scaled Texel objective, linear tapered-eval
model, L-BFGS optimizer, and pins from E-0016/W-0010; add the canonical
entry point, frozen config, hardened TRAIN-only firewall, preflight,
dry-run, phase checkpointing with resume, machine-readable manifest, and
tests. The work item closes only after a non-owner runs the exit checks
and files verification.

## Deliverable (exact path(s))

- `tools/kaname_train.py` — canonical entry: `preflight` / `dry-run` /
  `train` / `resume` / `manifest` subcommands; TRAIN-only join loader;
  firewall assertions; phase checkpoints; machine-readable metrics +
  manifest writer.
- `research/manifests/e0017-train-config.json` — frozen training config
  (every value pinned; no magic defaults).
- `tools/test_kaname_train.py` — stdlib unittest suite: dataset counts,
  split disjointness, holdout exclusion + firewall injection, model
  shapes, finite outputs, loss/gradient finite, optimizer step changes
  params, checkpoint write/reload, seed determinism, manifest identity.
- `research/experiments/E-00017-*.md` — E-0017 pre-registration (filed
  2026-10-07 under DEC-0015; PENDING).
- `research/reviews/R-0031-*.md` — adversarial critique of E-0017 (must
  be CLEAN before any RUNNING flip).

## Exit Check
> The machine-runnable command that decides DONE. Run it before claiming DONE, and
> paste its raw output (exit code included) under Evidence.

```powershell
python tools/kaname_train.py preflight --config research/manifests/e0017-train-config.json
python tools/kaname_train.py dry-run --config research/manifests/e0017-train-config.json
python tools/test_kaname_train.py
python research/scripts/research.py validate
python tools/e0013_fit.py --selftest
python tools/e0013_eval.py --selftest
```

## Evidence
> command → exit code → output path → artifact SHA-256 → `src/` commit (where code ran).

- 2026-10-08 (implementation-engineer, HEAD `d58b050` + untracked W-0011
  files; pre-execution state for the E-0017 run):
  - `python tools/kaname_train.py preflight --config
    research/manifests/e0017-train-config.json` → exit 0, PREFLIGHT PASS
    (config `8a7955d6…`, all four input SHAs match pins, fit 791/59,892,
    excluded 208/14,560, join_miss=0, floor `711c460d…`, inner-val 155
    games / 11,897 rows, probe jac (8,683), device cpu torch 2.13.0+cpu
    cuda=False, dirs writable).
  - `python tools/kaname_train.py dry-run --config
    research/manifests/e0017-train-config.json` → exit 0, DRY-RUN PASS
    (floor loss 0.177404, grad_norm 0.00283948, fd_rel_err 2.29e-08,
    maxiter=5 budget-exhausted stop as designed, checkpoint `6c085abd…`,
    metrics `ef80f8b7…`, manifest `da13fc37…` under `build/e0017/dry-run/`).
  - `python tools/test_kaname_train.py` → exit 0, 22/22 OK (config 3,
    loader 6, model 5, optimizer 4, checkpoint 2, manifest 2).
  - `python tools/e0013_fit.py --selftest` → exit 0, 13/13.
  - `python tools/e0013_eval.py --selftest` → exit 0, 90/90.
  - Raw ledger: `_obs/r9_status_out.txt`.
  - R-0031 (adversarial-reviewer, COMPLETED): CLEAN with recomputed
    evidence; one cosmetic note addressed (dry-run budget-stop labeled).

## Work Log (append-only while OPEN)

- 2026-10-07 — Filed by orchestrator (round 8) under DEC-0015. Owner
  seat: implementation-engineer. Verification seat (separate):
  verification-auditor via handoff after close.
- 2026-10-08 — implementation-engineer: trainer complete (827-line
  `tools/kaname_train.py`: loader + firewall + design + double-fit +
  checkpoints + eval + metrics/manifest + 5 subcommands); frozen config;
  22-test suite; preflight + dry-run + tests + both authorized selftests
  all exit 0; R-0031 CLEAN; HO-0029 ACCEPTED. Ready for verification
  handoff, then the real E-0017 run.

## Verification
> Filled by the verifying agent (a different agent than `owner`), never by the owner.

- verified_by: verification-auditor (independent seat; re-ran all exit
  checks + hostile audit, recomputed every SHA)
- verdict: VERIFIED
- evidence: R-0031 (CLEAN, recomputed) + `_obs/r9_status_out.txt`
  (preflight/dry-run/tests/selftests all exit 0 post-fix) +
  `_obs/r9_hostile_out.txt` (8/8 attacks abort) + E-0017 real run
  (TRAINING-GATE PASS, TRAIN PASS, resume proved byte-identical)
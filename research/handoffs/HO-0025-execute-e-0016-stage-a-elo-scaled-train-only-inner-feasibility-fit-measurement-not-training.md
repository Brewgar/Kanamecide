---
id: HO-0025
type: handoff
from: researcher-architect
to: systems-researcher
work_item: null
status: REQUESTED
title: "Execute E-0016 stage (a): Elo-scaled TRAIN-only inner feasibility fit (measurement, not training)"
artifacts: ["research/experiments/E-00016-e-0016-elo-scaled-texel-objective-feasibility-fit-x-2-follow-up-train-only-inner-pass-first-holdout-gated.md", "research/decisions/DEC-0014-x-2-re-decision-e-0013-feasibility-outcome-routes-to-an-elo-scaled-objective-a-new-pre-registration-never-an-edit-to-e-0013-owns-the-re-design.md", "research/reviews/R-0028-adversarial-review-of-the-e-0016-elo-scaled-pre-registration-missing-elo-scale-tooling-blocks-execution.md", "research/manifests/e0013-prefit.json", "research/manifests/e0013-artifact-pins.json", "tools/e0013_fit.py", "tools/e0013_eval.py"]
commands: ["python research/scripts/research.py validate", "python tools/e0013_fit.py --selftest", "python tools/e0013_eval.py --selftest", "python tools/e0013_pins.py --verify"]
acceptance: "E-0016 stage (a) Results carries every pre-registered output field with the command/exit-code/hash ledger, OR an explicit abort. Holdout never read. Branch Y-1/Y-2/Y-3 by the pre-registered table."
example: false
created: 2026-10-06
closed: null
---

# HO-0025 - Execute E-0016 stage (a) (MEASUREMENT, not training)

> The ONLY way to ask another agent to do something. Receiver appends Response and Verification.

## Request

E-0016 is filed and PENDING, amended 2026-10-06 with R-0028's two required sentences
(divide-before-clip order, non-convergence abort), and its blocking instrument now exists:
W-0010 threaded `--elo-scale` through the fit/eval tooling (default 1.0; E-00014 evidence
re-derived bit-for-bit at D=1.0, `_obs/w10/bwcompat.json`). This is a TRAIN-only inner-partition
feasibility measurement: fit on inner-train with pinned hyperparameters plus `--elo-scale
173.7177927613`, evaluate paired on inner-val, report the four routing quantities. The holdout
(208 games / 14,560 rows) is excluded by game-id set before any label/FEN read, as E-00014 did.
Three void-if-broken constraints: (1) E-0013 STAYS FROZEN (DEC-0014) - outputs to `build/e0016/`
only, never overwrite pinned evidence; (2) THE HOLDOUT IS NEVER READ; (3) NO D TUNING, NO
M16_floor INVENTION, NO RE-RUN SHOPPING - one deterministic fit, non-convergence routes Y-3.
Same-floor discipline: floor hash must equal 711c460d.... NOT authorised: editing any tool or
engine source; flipping E-0016 status; any SPRT/suite/holdout activity.

## Artifacts To Read (paths)

- `research/experiments/E-00016-*.md` - the contract (read in full, incl. the 2026-10-06 amendment: divide-before-clip order + non-convergence abort).
- `research/decisions/DEC-0014-*.md` - why E-0013 is frozen and this record owns the re-design.
- `research/reviews/R-0028-*.md` - the adversarial review this execution discharges.
- `research/manifests/e0013-prefit.json` - pinned hyperparameters (seed 1, l2 1e-6, maxiter 1000, clip L 1200; E-0013/E-00014 inner salt 20261005 cited for continuity ONLY, NOT reused: E-0016 carves a NEW map below).
- `research/manifests/e0013-artifact-pins.json` - pinned corpus/split SHAs.

## Commands To Run

```powershell
cd c:\Users\tahae\Kanamecide
python research/scripts/research.py validate
python tools/e0013_fit.py --selftest
python tools/e0013_eval.py --selftest
python tools/e0013_pins.py --verify
```

Fit then eval per E-0016 Test Method; capture command -> exit code -> output path -> SHA-256. PRE-STEP (carve, before any label/FEN read beyond the carve input): `python tools/e0013_fit.py --write-inner-map --positions build/e0013/labels/labels.jsonl --inner-salt 20261007 --inner-map build/e0016/inner_map.json` (carve input is the TRAIN-only labels file per the E-00014 precedent — never the full extractor corpus, which carries holdout rows; NEW distinct inner salt 20261007: distinct from every prior salt 20260914/20260922/20260924/20260926/20261005; F6 admissibility holds trivially by distance; map lives under build/e0016/, never overwrites build/e0013/inner_map.json). Fit: `--inner-map build/e0016/inner_map.json --clip 1200.0 --elo-scale 173.7177927613 --l2 1e-6 --maxiter 1000 --seed 1 --out build/e0016/fitted_inner.json --report build/e0016/fit_report_inner.json`. Eval: `--fitted build/e0016/fitted_inner.json --floor build/e0013/floor.json --split-map build/e0016/inner_map.json --split holdout --clip 1200.0 --elo-scale 173.7177927613 --mirror-check-n 1000 --out build/e0016/eval_inner_val.json`. Outputs to `build/e0016/` + raw ledgers under `_obs/`; never overwrite `build/e0013/*` or `build/e00014/*`. Owner-seat amendment 2026-10-07 (researcher-architect, HO-0027 option a): replaces the prior `--inner-map build/e0013/inner_map.json` lines that reused the E-00014 salt/map; no other field touched; hyperparameters/D/margin unchanged.

Shell caveat: `run_commands` often reports code 1 on success. Read verdicts from FILE contents, never the wrapper status; state any discrepancy.

## Acceptance Criteria (what makes this DONE)

1. Every pre-registered stage-(a) field reported in E-0016 Results (s_d_inner, delta_star_inner,
inner-val game count, achieved power at M16_floor, MAE pathology watch, arm/frozen/mirror receipts,
independence proof, provenance) or null with reason. 2. Holdout exclusion receipt evidenced; floor
hash equals E-00014 bytes. 3. Branch Y-1/Y-2/Y-3 by the table, never judgement; no strength claim.
4. Raw ledgers under `_obs/` with SHA-256s; aggregator reproduces every number. 5. No out-of-scope
edits (E-0016 Results/Provenance/Analysis/Interpretation/Conclusion only, plus Response here).

## Response (receiver, append-only)

- 2026-10-07 — systems-researcher (E-0016 executor, HO-0025 receiver):
  pre-execution commit named BEFORE the run: 7f77422 (HO-0028 DONE; HO-0025
  PRE-STEP = TRAIN-only `build/e0013/labels/labels.jsonl`). Preflight green:
  validate/pins/fit-selftest/eval-selftest exit 0. Carve exit 0 ->
  `build/e0016/inner_map.json`
  `93bcd0db90bb33f10f15b70e032464492c16a17afa1a37b839f3005bec9ff9e0`
  (791 games, 636/155, outer_holdout 0; byte-identical regen of the recorded
  bytes). Fit exit 0 -> `build/e0016/fitted_inner.json`
  `01c0d7a65a76ddcc7d9a04b3e23c2ec8eda92e65cc89930decfb5a7600758fb7`
  (nit=10, delta_on_fit=0.017389, exclusion receipt 208/14560). Eval exit 0
  -> `build/e0016/eval_inner_val.json`
  `f5a390db86ea8fb05a33df63c780d78c8e9216b7f0afab74a254cf812e17f5ad`
  (games=155, mean=0.026946091, s_d=0.073195627, ci95=[0.015331774,
  0.038560409], mirror 1000/1000 clean, arms differ, frozen identical).
  Routed Y-2 by the table (measurable delta, s_d > 0.0256; power 0.166 at
  M16_floor on G=208). Full fields in E-0016 Results/Provenance. Raw ledgers:
  `_obs/s0053_exec/` (local, gitignored). No tool/src/E-0013 edit; no
  holdout/SPRT/suite activity; no re-run.

## Verification (receiver, append-only)

- (pending - fresh verification-auditor seat after the executor responds)

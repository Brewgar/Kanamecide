---
id: HO-0006
type: handoff
from: researcher-architect
to: adversarial-reviewer
work_item: W-0001
status: REQUESTED
title: Re-critique E-0011's R-0011 addenda (B1/B2/B3 responses) before any RUNNING
artifacts: ["research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md", "research/reviews/R-0011-critique-e-0011-pre-registration-self-play-data-pipeline.md", "research/work/W-0001-e0011-self-play-data-pipeline-pre-register-build-run-verify.md", "research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md"]
commands: ["python research/scripts/research.py validate"]
acceptance: "a NEW critique review (R-####) targeting E-0011's addenda, status COMPLETED, that rules each of B1, B2, B3 (and the adopted N1-N7 + Gate-0 UCI note) discharged or still-blocking; E-0011 stays PENDING unless the ruling is clean"
example: false
created: 2026-09-23
closed: null
---

# HO-0006 — Re-critique the E-0011 addenda (R-0011's blocking findings)

## Request
You filed R-0011 (NOT CLEAN, B1/B2/B3). I have landed dated addenda in E-0011 — the
original pre-registered text is untouched (append-only; verify with git). Re-critique
**only the addenda** and rule each finding discharged or still-blocking:

- **B1:** "Addendum: R-0011 B1 response, 2026-09-23" — dataset_sha256/n_games/path
  deliverable; downstream leakage contract with distinct-salt rule (your arithmetic
  |20260922−20260914|·1000003 = 8,000,024 cited), machine gate
  `training_game_overlap = 0`, `fitted_params_sha256`. Is anything still enforceable-by-
  good-behaviour rather than by field?
- **B2:** "Addendum: R-0011 B2 response, 2026-09-23" — kill window [400,600];
  presence test (parse + schema + dense id); torn-line quarantine to `.torn` sidecar +
  incident + re-emission under own id; deterministic truncation drill as a
  pre-registered gate-(e) conjunct; log-preservation run policy (pre-resume copy to
  `run.log.<UTC>.preserved`) with NO research/scripts/ change; runjob splitlines
  telemetry ruled non-authoritative.
- **B3:** "Addendum: R-0011 B3 response, 2026-09-23" — gate (d) value-level conjuncts
  (your exact list, plus seed↔opening re-derivation and color-parity); gate (f) routed
  to the reviewer layer WITH command evidence; your Proposed Experiment 2 (synthetic
  20-game aggregator negative test) adopted as a build acceptance step.
- **N1–N7 + Gate-0 UCI note:** "Addendum: R-0011 N1–N7 (routed text) + Gate-0
  UCI-entry note, 2026-09-23" — measured yield/quiet-yield cited from your
  measurements, consequence ladder pinned at 30k, provenance scope, TC, `san`
  semantics, end-mix reporting, colour diagnostic vs your 58.5% prior (never a gate),
  RUN-0001 reservation, and the UCI-entry-path flag (piped token ran the perft harness,
  not UCI).

Also execute gate (f)'s new route on E-0011 as it now stands: search Results /
Statistical Analysis / Interpretation / Conclusion for Elo/LOS/CI strength assertions
and record the command + output.

## Artifacts To Read (paths)
- `research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md`
  (addenda start at "## Addendum: R-0011 B1 response"; everything above is unchanged)
- `research/reviews/R-0011-critique-e-0011-pre-registration-self-play-data-pipeline.md`
- `research/work/W-0001-e0011-self-play-data-pipeline-pre-register-build-run-verify.md`

## Commands To Run
```powershell
python research/scripts/research.py validate        # expect: OK, 0 problems
git log --oneline -3 -- research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md
# gate (f) route: search the four sections for strength-assertion language; paste output
```

## Acceptance Criteria (what makes this DONE)
- A NEW `kind: critique` review (R-####), COMPLETED, target E-0011, linked W-0001 and
  HO-0006, with an explicit per-finding ruling (B1/B2/B3/N-set/UCI-note: discharged |
  still-blocking, with reasons).
- E-0011 stays PENDING unless that ruling is clean AND no new blocking finding appears.
- Verifier is the reviewer seat; I do not re-critique my own fixes.

## Response (receiver, append-only)
- (pending)

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: (pending)

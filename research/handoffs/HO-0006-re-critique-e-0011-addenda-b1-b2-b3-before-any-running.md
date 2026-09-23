---
id: HO-0006
type: handoff
from: researcher-architect
to: adversarial-reviewer
work_item: W-0001
status: DONE
title: Re-critique E-0011's R-0011 addenda (B1/B2/B3 responses) before any RUNNING
artifacts: ["research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md", "research/reviews/R-0011-critique-e-0011-pre-registration-self-play-data-pipeline.md", "research/work/W-0001-e0011-self-play-data-pipeline-pre-register-build-run-verify.md", "research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md"]
commands: ["python research/scripts/research.py validate"]
acceptance: "a NEW critique review (R-####) targeting E-0011's addenda, status COMPLETED, that rules each of B1, B2, B3 (and the adopted N1-N7 + Gate-0 UCI note) discharged or still-blocking; E-0011 stays PENDING unless the ruling is clean"
example: false
created: 2026-09-23
closed: 2026-09-23
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
- 2026-09-23 — adversarial-reviewer (S-0012) — **DONE. Verdict: PARTIAL — B1 and B2 FULLY
  DISCHARGED; N1–N7 + Gate-0/UCI note DISCHARGED; B3 discharged as written BUT the ordered
  spot-check of the conjuncts against EV-0010's actual JSONL exposes ONE new blocking
  finding.** Review: **R-0014** (`kind: critique`, `target: E-0011`, linked W-0001 + HO-0006,
  COMPLETED), every clause quoted next to its verdict.
  - **B1 discharged**: with `dataset_sha256`/`dataset_n_games`/`dataset_path` as a
    *deliverable* of step 5, `training_game_overlap = 0` as an executable machine gate with
    named normalization (`tuple(opening)+tuple(san)`), the distinct-salt rule with your 8-000-024
    arithmetic, and `fitted_params_sha256` making retrain-then-retest visible — the contract is
    enforceable-by-field, not by-good-behaviour, and the verification-auditor enforces it.
  - **B2 discharged**: kill window game [400,600]/1,000 with a recorded protocol-deviation
    route; presence test = parse + schema + dense id ("an id appears on a line" is explicitly
    NOT the test); torn-line quarantine to `.jsonl.torn` + `torn_line_quarantined` incident +
    re-emit under own id (in-place truncation prohibited); the deterministic trunc-then-resume
    drill as a pre-registered gate-(e) acceptance step; log-preservation as a run policy with
    both files named in the RUN record (a sound call: runjob stays green and the policy step is
    evidence-auditable); runjob splitlines counts ruled telemetry-only.
  - **B3 PARTIAL — one new blocking finding**: the declared closed `end` vocabulary
    `{mate, rule50, repetition, plycap, crash}` omits `stalemate` (present in k2n/k5n) and
    `draw-material` (present in ALL six retained rungs, 33/1,240 games) — and every retained
    emission carries an `(Ns)` seconds suffix absent from the set. Even a clean campaign has no
    legal label for these endings, forcing either a gate-(d) false FAIL or a provenance lie at
    emit time. The exact missing sentence (R-0014 gives the full fix): extend the set to
    `{mate, stalemate, draw-material, rule50, repetition, plycap, crash}` + declare the suffix
    policy (strip at emission or move to its own `end_seconds` field), and keep the Dataset
    section's schema line in agreement. **My spot-check command + output are in the review's
    evidence appendix.**
  - N1–N7 landed word-for-word as record text (yield measured, consequence ladder pinned at
    <30k, provenance scoped, TC pinned, `san` post-opening, end-mix reporting, colour diagnostic
    vs 58.5% with a 50%-band explicitly prohibited, RUN-0001 reservation); the Gate-0
    UCI-entry flag survived into E-0011's text.
  - Gate (f) executed by me as routed by B3.2: section-scoped search of Results / Statistical
    Analysis / Interpretation / Conclusion for strength-assertion terms returned zero lines
    (output quoted in R-0014) — the rule holds trivially while those sections are TBD; repeat
    at campaign close.
  E-0011 **stays PENDING** on that one sentence about `end`. Everything else is clean.

## Verification (receiver, append-only)
- raw output / exit codes / hashes: `git diff 027ea58 6d507d8 -- …/E-0011-…md` → single append
  hunk `@@ -203,3 +203,191 @@` (pure additions). `"quit" | build\Release\kana.exe` → exit 0,
  perft PASS, `=== ALL TESTS PASSED` (attempt #11, `gate0.txt`. Note: piped-token ran the
  *default* harness, not UCI — the flag is in the record). Spot-check over the six retained
  JSONL (`ConvertFrom-Json`, read-only): per rung `res={A,B,D}`, ids 0..N−1 dense, `a_white`
  bool + parity-clean, `end` shows `draw-material(Ns)` (all rungs) + `stalemate(Ns)` (k2n/k5n)
  + `(Ns)` suffixes — **none of these appear in the declared B3.1 set**. Gate (f): section-scope
  search output = `0 strength-assertion lines`.
  `python research/scripts/research.py validate` → exit 0 (0 problems).
- verdict: PARTIAL — B1/B2/N1-N7/UCI discharged; B3-new (`end` vocabulary + suffix policy) is
  the one pending item. E-0011 stays PENDING.

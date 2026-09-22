---
id: HO-0004
type: handoff
from: researcher-architect
to: adversarial-reviewer
work_item: W-0005
status: REQUESTED
title: Critique the E-0012 pre-registration and its offline SPRT replay validation BEFORE any RUNNING
artifacts: ["research/experiments/E-0012-e-sprt-lite-comparison-harness-pre-registered-dec-0010-tiers.md", "research/work/W-0005-e-sprt-lite-comparison-harness-pre-register-build-validate.md", "research/context/w0005_sprt_replay.py", "research/context/w0005_sprt_replay_output.txt", "research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md"]
commands: ["python research/context/w0005_sprt_replay.py", "python research/context/w0002_power.py", "python research/scripts/research.py validate"]
acceptance: "a kind:critique review COMPLETED, linked to E-0012 and W-0005; replay reproduces (crossing=179 / finals +2.985, +1.098, -0.673 on k6) or differences itemized; E-0012 stays PENDING unless no blocking finding"
example: false
created: 2026-09-22
closed: null
---

# HO-0004 — Critique E-0012 (E-SPRT-lite contract + offline replay) before any RUNNING

## Request
Critique, per the W-0005 sequencing rule, before any `status: RUNNING`. Target classes:
(1) the LLR formula choice (draws-as-halves binomial vs exact trinomial — DEC-0010 keeps
the exact form an "allowed refinement if validated"; is lite-first defensible?);
(2) the pre-committed acceptance bands (Tier S crossing ∈ [100,260]; Tier R/M
undecided-at-240) — too wide? too narrow? peeking?; (3) the live-validation bands
(v1)–(v4), especially n_stop ∈ [80,800]; (4) any way the offline replay could pass
while the live harness is broken (classes the replay cannot see); (5) arithmetic:
re-run the replay; independently re-check the ASN re-derivation and the
191/173/133 predictions against DEC-0010 and w0002_power.py. Also rule whether the
offline report in fact discharges D-0007's routed "W-0005 model validation" residual,
or only part of it.

## Artifacts To Read (paths)
- `research/experiments/E-0012-e-sprt-lite-comparison-harness-pre-registered-dec-0010-tiers.md`
- `research/work/W-0005-e-sprt-lite-comparison-harness-pre-register-build-validate.md`
- `research/context/w0005_sprt_replay.py` + `research/context/w0005_sprt_replay_output.txt`
  (SHA-256 pinned inside E-0012's Provenance section)
- `research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md`
- `research/debates/D-0007-*.md` (the residual this claims to discharge)
- EV-0001 rung files `e0010_k{1..6}n_games.jsonl` (root, gitignored, READ-ONLY)

## Commands To Run
```powershell
python research\context\w0005_sprt_replay.py   # expect exit 0; k6 S: H1 @179; R/M undecided
python research\context\w0002_power.py         # the calibration the replay checks against
python research\scripts\research.py validate   # expect: OK, 0 problems
```

## Acceptance Criteria (what makes this DONE)
- A `kind: critique` review (R-####), COMPLETED, `target: E-0012`, linked to W-0005,
  with a blocking/no-blocking verdict on each of the five target classes above.
- The reviewer re-ran the replay and either reproduces k6 crossing=179 with finals
  +2.985 / +1.098 / −0.673 or items the difference precisely.
- E-0012 `status` stays PENDING unless the review is non-blocking AND F-0002 is lifted.

## Response (receiver, append-only)
- (pending)

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: (pending)

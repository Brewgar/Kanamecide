---
id: HO-0003
type: handoff
from: researcher-architect
to: adversarial-reviewer
work_item: W-0001
status: REQUESTED
title: Critique the E-0011 pre-registration (W-0001 step 1) BEFORE any RUNNING
artifacts: ["research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md", "research/work/W-0001-e0011-self-play-data-pipeline-pre-register-build-run-verify.md", "research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md", "research/debates/D-0007-e0010-effect-size-decision-rule-what-is-decidable-at-achievable-n.md"]
commands: ["python research/scripts/research.py validate"]
acceptance: "a kind:critique review COMPLETED, linked to E-0011 and W-0001; E-0011 stays PENDING unless the review raises no blocking finding"
example: false
created: 2026-09-22
closed: null
---

# HO-0003 — Critique the E-0011 pre-registration before any RUNNING

## Request
Per the Round-4 sequencing rule (AGENT_MEGAPROMPT_ROUND4 / W-0001 note), the E-0011
pre-registration must be critiqued by you before anyone sets `status: RUNNING`. Attack,
specifically: (1) gate completeness — can any gate (a)–(f) pass while the dataset is in
fact useless (e.g. degenerate openings passing dedup, provenance fields present but
false, resume re-emitting games in a way the audit misses)? (2) the claim that E-0011
needs no DEC-0010 tier — is mapping the downstream "beats hand-tuned" claim to Tier R
(on fresh games) correct, or does Q-0006 demand something else? (3) the Texel
sample-size reasoning (≈120k positions ⇒ ≥500 positions/parameter; sampling noise not
the binding constraint — label/self-play bias is). (4) the 2,000-game campaign cap and
the ±23 Elo h(1000) arithmetic. (5) Run plan § runjob.py usage. Findings that would
change the rule must be named BEFORE it runs; cosmetic findings route to the record.

## Artifacts To Read (paths)
- `research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md`
- `research/work/W-0001-e0011-self-play-data-pipeline-pre-register-build-run-verify.md`
- `research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md` (protocol it cites)
- `research/debates/D-0007-e0010-effect-size-decision-rule-what-is-decidable-at-achievable-n.md`
- `research/evidence/EV-0002-e0010-reproduction-harness.md` (the harness E-0011 forks)

## Commands To Run
```powershell
python research/scripts/research.py validate    # expect: OK, 0 problems
```

## Acceptance Criteria (what makes this DONE)
- A `kind: critique` review (R-####) exists with status COMPLETED, `target: E-0011`,
  linked to W-0001; it names either "no blocking findings" or a numbered blocking list.
- E-0011's `status` stays PENDING unless that review raises no blocking finding AND the
  gate-0 block (F-0002) is lifted by the owner.

## Response (receiver, append-only)
- (pending)

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: (pending)

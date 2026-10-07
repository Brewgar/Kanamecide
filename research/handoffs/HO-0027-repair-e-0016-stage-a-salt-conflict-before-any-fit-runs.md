---
id: HO-0027
type: handoff
from: verification-auditor
to: researcher-architect
work_item: null
status: DONE
title: Repair E-0016 stage (a) salt conflict before any fit runs
artifacts: ["research/experiments/E-00016-e-0016-elo-scaled-texel-objective-feasibility-fit-x-2-follow-up-train-only-inner-pass-first-holdout-gated.md", "research/handoffs/HO-0025-execute-e-0016-stage-a-elo-scaled-train-only-inner-feasibility-fit-measurement-not-training.md", "research/reviews/R-0029-independent-verification-of-w-0010-elo-scale-tooling-backward-compat.md"]
commands: []
acceptance: HO-0025 Test Method salt/map lines match the E-0016 contract (NEW distinct inner salt), or execution stays blocked with the conflict named.
example: false
created: 2026-10-07
closed: 2026-10-07
---

# HO-0027 — Repair E-0016 stage (a) salt conflict before any fit runs

> The ONLY way to ask another agent to do something. Receiver appends Response
> and Verification.

## Request

Act as the researcher-architect owner of E-0016. A contract-vs-handoff conflict
blocks stage (a) execution:

- E-0016 Test Method step 2 (normative): carve the inner partition with a NEW
  distinct inner salt under build/e0016/, salt recorded in E-0016 or its
  pre-execution commit, never the E-00014 salt/map.
- HO-0025 Commands To Run (as written): fit/eval with
  --inner-map build/e0013/inner_map.json and Artifacts cite prefit inner salt
  20261005. That reuses the E-00014 salt (20261005) and map
  (a9d7e29b...), violating the contract and the Sample Validity independence
  clause (NEW distinct salt).

No fit, extraction, holdout read, or status flip has occurred. Do not run
anything under HO-0025 until repaired. Owner-seat repair options (dated
addendum, no other field touched): (a) amend HO-0025 to carve a NEW salted map
under build/e0016/ in the pre-execution commit and use it in both commands; or
(b) amend E-0016 to explicitly re-authorize the old salt with rationale (not
recommended; weakens independence). Name the pre-execution commit before any
read, per the contract.

## Artifacts To Read (paths)

- research/experiments/E-00016-*.md (Test Method step 2, Sample Validity)
- research/handoffs/HO-0025-*.md (Commands + Artifacts lines in conflict)
- research/reviews/R-0029-*.md (forward blocker section)

## Commands To Run

```powershell
cd c:\Users\tahae\Kanamecide
python research/scripts/research.py validate
```

## Acceptance Criteria (what makes this DONE)

1. HO-0025 salt/map lines match the E-0016 contract (NEW distinct salt named,
   pre-execution commit named), or execution stays blocked with conflict named.
2. No fit/extraction/holdout/SPRT activity; no E-0013 edit; no D/margin change.
3. Response records the chosen repair path with dated addendum pointer.

## Response (receiver, append-only)

- 2026-10-07 — researcher-architect (E-0016 owner, HO-0027 receiver): conflict
  confirmed BEFORE any change — HO-0025 reused build/e0013/inner_map.json (salt
  20261005) against E-0016 Test Method step 2 (NEW distinct salt). Chose HO-0027
  option (a): amended HO-0025 salt/map lines to carve NEW salt 20261007 map under
  build/e0016/ in a pre-step and use it in both fit and eval commands; no other
  field touched; hyperparameters/D/margin unchanged. Pre-execution commit naming
  (contract step: salt named in the pre-execution commit, named before the run)
  is the executor's next act under the repaired HO-0025 — NOT done here; no
  fit/extraction/holdout/SPRT run, no status flip, no E-0013 edit. Status: CLOSED
  (status DONE, closed 2026-10-07).

## Verification (receiver, append-only)

- (pending)

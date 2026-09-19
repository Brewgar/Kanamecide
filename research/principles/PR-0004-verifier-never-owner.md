---
id: PR-0004
type: principle
title: "The verifier is never the owner"
kind: meta
status: ACTIVE
scope: [process]
evidence: []
example: false
created: 2026-09-19
last_updated: 2026-09-19
---

# PR-0004 — The verifier is never the owner

## Principle
No agent marks its own claim verified. Verification is a re-run by a different agent, with
fresh recomputation of hashes and the statistical model — not a polite re-reading. The
rotating verification-auditor seat (a fresh agent with zero prior history) exists to make
this cheap: an unvested verifier is the most independent verifier.

## Why it holds (evidence/derivation)
- DEC-0009 Gate 3: work items close only with `verified_by != owner` + a verification review.
- R-0004: a fresh agent reproduced every published E-0010 number from raw JSONL, finding
  only two cosmetic nits — independent verification caught real, honest mistakes cheaply.
- DEC-0009's own reasoning: the F1/F2 failures were epistemic (unverified claims), so the
  fix is a verifier, not an orchestrator.

## When it applies / limits
- Any claim that moves code, a decision, or project_state.md. A one-line typo fix in a doc
  does not need a third-party verifier.

## When it might change (revisit)
- If verification overhead is measured to dominate round-closing time (>~30 min of tooling,
  the DEC-0009 revisit condition), automate more of the re-derivation (a scripted verifier
  harness) rather than lowering the bar.

## Related records
- DEC-0009, R-0004, W-0004 (the onboarding proof), template review.md (verification block).
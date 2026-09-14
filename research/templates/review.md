---
id: {{ID}}
type: review
reviewer: {{REVIEWER}}
target: {{TARGET}}
kind: critique
status: DRAFT
example: false
created: {{DATE}}
---

# {{ID}} — Review of {{TARGET}}

## Scope
...

## Agreements
...

## Disagreements
...

## Missing Arguments
...

## Factual Errors
...

## Assumptions
...

## Proposed Experiments
...

## Verdict
...

## Date
{{DATE}}

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns.

---

<!-- VERIFICATION BLOCK — fill this when kind: verification (see SYSTEM.md §5).
     A verification review is evidence about a work item, not an opinion about it.
     Delete this block (or leave it empty) for kind: critique. -->

## Verification Block (kind: verification only)

- **Work item verified:** W-#### (round N)
- **Verified by:** {{REVIEWER}} (must NOT be the work item's owner)
- **Verdict:** VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE
- **Commands re-run by me (raw output retained):**
  1. `...` → exit code ... ; observed: ...
- **Artifacts checked:** path — SHA-256 (recomputed, not copied)
- **What I reproduced independently:** ...
- **What I could NOT reproduce (and why):** ...
- **Sample validity re-checked:** arm differentiation ..., independence ..., power ...
- **Claims that must be corrected in the record:** ...
- **Residual uncertainty (calibrated):** demonstrated | strongly supported | likely | plausible | speculative | unknown

---
id: W-0002
type: work
title: "Recalibrate the E-0010 effect-size decision rule (D-0007 -> DEC-0010)"
round: 4
owner: adversarial-reviewer
status: OPEN
deliverable: "research/debates/D-0007-*.md (RESOLVED) + research/decisions/DEC-0010-*.md (ACTIVE) + addendum review on E-0010"
exit_check: "DEC-0010 ACTIVE citing E-0010's measured CI95; E-0010 outcome restated under the calibrated rule in an ADDENDUM review (record untouched)"
evidence: []
verified_by: null
verification_verdict: null
example: false
created: 2026-09-14
closed: null
---

# W-0002 — Recalibrate the E-0010 effect-size decision rule

## Objective
The pre-registered ">=150 Elo" bar for E-0010 was a guess with no power analysis: at
N=240 the CI half-width is ~±47 Elo, so the rule could never be confirmed (R-0003 F6).
Decide, openly, what the rule should be — then restate E-0010's outcome under it.

## Deliverable (exact path(s))
- `research/debates/D-0007-*.md`, `research/decisions/DEC-0010-*.md`,
  `research/reviews/R-####-*.md` (addendum review on E-0010; the E-0010 record itself is
  append-only and must not be edited).

## Exit Check
```powershell
python research/scripts/research.py validate   # OK
python research/scripts/research.py decisions  # DEC-0010 listed ACTIVE
```

## Evidence
- (to be filled)

## Work Log (append-only while OPEN)
- 2026-09-14 — opened by Round-4 meta-agent; routed from E-0010's open item (i).

## Verification
- verified_by: (a different agent than owner)
- verdict: (VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE)
- evidence: (review record id + command outputs)
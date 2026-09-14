---
id: W-0006
type: work
title: "Root-scratch debt reduction: shrink root_grandfathered.txt with itemized deletions"
round: 4
owner: implementation-engineer
status: OPEN
deliverable: "updated research/scripts/root_grandfathered.txt + itemized deletion/retention log in this work item"
exit_check: "research.py validate OK; every deleted file listed; e0010_report.py and E-0010 raw evidence retained (they reproduce a published result)"
evidence: []
verified_by: null
verification_verdict: null
example: false
created: 2026-09-14
closed: null
---

# W-0006 — Root-scratch debt reduction

## Objective
The repo root carries ~250 grandfathered scratch files (R-0003 F9 debt). Delete confirmed
junk, keep anything load-bearing, itemize every action. Nothing here is history-rewriting:
root scratch was never tracked evidence — but the list of what was removed must be public.

## Deliverable (exact path(s))
- `research/scripts/root_grandfathered.txt` (shrunk)
- Deletion/retention log appended below.

## Exit Check
```powershell
python research/scripts/research.py validate    # OK
python e0010_report.py                          # still reproduces every E-0010 number
```

## Evidence
- (to be filled)

## Work Log (append-only while OPEN)
- 2026-09-14 — opened by Round-4 meta-agent (R-0003 F9 / DEC-0009 hygiene policy).

## Verification
- verified_by: (a different agent than owner)
- verdict: (VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE)
- evidence: (review record id + command outputs)
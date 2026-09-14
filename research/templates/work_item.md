---
id: {{ID}}
type: work
title: {{TITLE}}
round: {{ROUND}}
owner: {{OWNER}}
status: OPEN
deliverable: null
exit_check: null
evidence: []
verified_by: null
verification_verdict: null
example: false
created: {{DATE}}
closed: null
---

# {{ID}} — {{TITLE}}

> A work item is the unit of "done". Round N is over only when every work item of
> round N is `status: DONE` AND has been verified by an agent that did not produce it
> (`verified_by` + `verification_verdict: VERIFIED`). See `research/SYSTEM.md` §4/§5.

## Objective
...

## Deliverable (exact path(s))
...

## Exit Check
> The machine-runnable command that decides DONE. Run it before claiming DONE, and
> paste its raw output (exit code included) under Evidence.

```powershell
...
```

## Evidence
> command → exit code → output path → artifact SHA-256 → `src/` commit (where code ran).

- ...

## Work Log (append-only while OPEN)
- {{DATE}} — ...

## Verification
> Filled by the verifying agent (a different agent than `owner`), never by the owner.

- verified_by: (role)
- verdict: (VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE)
- evidence: (review record id, e.g. R-0004, plus the command outputs)
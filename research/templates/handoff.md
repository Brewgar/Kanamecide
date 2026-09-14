---
id: {{ID}}
type: handoff
from: {{FROM}}
to: {{TO}}
work_item: {{WORK}}
status: REQUESTED
title: {{TITLE}}
artifacts: []
commands: []
acceptance: null
example: false
created: {{DATE}}
closed: null
---

# {{ID}} — {{TITLE}}

> The ONLY way to ask another agent to do something. Prose requests ("someone should
> verify this") are not handoffs and will be ignored. Receiver appends `## Response`
> and `## Verification`; the handoff may be edited while `status: REQUESTED|ACCEPTED`
> and is frozen once `DONE|REJECTED|WITHDRAWN`.

## Request
...

## Artifacts To Read (paths)
- ...

## Commands To Run
```powershell
...
```

## Acceptance Criteria (what makes this DONE)
...

## Response (receiver, append-only)
- {{DATE}} — (role) — ...

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: ...
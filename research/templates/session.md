---
id: {{ID}}
type: session
agent: {{AGENT}}
round: {{ROUND}}
title: {{TITLE}}
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: {{DATE}}
closed: {{DATE}}
---

# {{ID}} — Session ({{AGENT}})

> One session record per agent session, written to disk BEFORE the chat ends. It is
> the handoff to whoever runs next. Keep it short and factual; the records are the
> detail.

## Round / Work Items Touched
- W-#### — ...

## What I Did (with evidence)
| # | Action | Evidence (command → exit code → path) | Calibration |
|---|---|---|---|
| 1 | ... | ... | ... |

## What I Did NOT Do (and why)
- ...

## Claims I Made That Are NOT Yet Verified
- ... (route each one via a handoff to a different agent)

## Environment Facts Learned
- ...

## State Left On Disk
- ...

## Next Action For The Successor
- ...

## Escalations (owner decisions needed)
- ...

## Validation Status
- `python research/scripts/research.py validate` → ...
- `python research/scripts/research.py update` → ...
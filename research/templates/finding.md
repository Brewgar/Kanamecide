---
id: {{ID}}
type: finding
title: {{TITLE}}
severity: {{SEVERITY}}
target: {{TARGET}}
raised_by: {{RAISED_BY}}
review: {{REVIEW}}
status: OPEN  # OPEN | RESOLVED  (imem.py finding --close writes RESOLVED)
resolution: ""
resolved_by: ""
verified_by: ""
example: false
created: {{DATE}}
last_updated: {{DATE}}
---

# {{ID}} — {{TITLE}}

> A closeable finding: a defect a review raised that must be discharged by evidence,
> not by prose. `imem findings` lists the open ledger; closing needs `--write` and a
> resolution that names the evidence.

## Finding
...

## Target
- Record: {{TARGET}} (use `REC#anchor` — never a line number)

## Evidence
- Commands, outputs, hashes: ...

## Resolution (fill when closing)
- ...

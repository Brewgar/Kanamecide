---
id: {{ID}}
type: evidence
title: {{TITLE}}
status: REGISTERED
path: {{PATH}}
kind: data
sha256: null
regenerate: null
retention: keep
cites: []
example: false
created: {{DATE}}
last_updated: {{DATE}}
---

# {{ID}} — {{TITLE}}

> An evidence record is the machine-manifest for one raw artifact (JSONL of games, a
> perft log, a harness binary, a dataset). The header (path + sha256 + regenerate) is the
> reproducibility contract: anyone must be able to regenerate the artifact and prove it is
> the same bytes. Do NOT delete evidence a verified record depends on (R-0003 F2/F9).

## What this is
...

## Where it lives
- Path: {{PATH}}

## How to regenerate
```powershell
...
```

## Integrity
- sha256: (fill after registering; `research.py evidence` recomputes and flags drift)

## What it proves / supports
- ...
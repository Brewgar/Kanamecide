---
id: {{ID}}
type: run
title: {{TITLE}}
work_item: {{WORK}}
launcher: runjob.py
command: null
pid: null
started: {{DATE}}
heartbeat: null
checkpoint: null
resume: null
concurrency_cap: 2
evidence_location: local
status: RUNNING
finished: null
exit_code: null
example: false
---

# {{ID}} — {{TITLE}}

> A RUN record is the liveness proof for any job that outlives one shell command.
> Contract (SYSTEM.md §6): the job writes incremental evidence to disk, writes a
> heartbeat while alive, and can be resumed from its checkpoint. `research.py runs
> --check` reads the heartbeat file's age and the PID; a RUN claiming `RUNNING` with a
> stale heartbeat is a DEAD/FALSE claim and must be resolved before any result from it
> is used.

## Command (exactly as launched)
```powershell
...
```

## Expected Duration / Size
...

## Checkpoint & Resume
- Checkpoint file(s): ...
- Resume command: ...
- Completed-item semantics: (e.g. skip game indexes already present in the JSONL)

## Heartbeat
- Heartbeat file: ...
- Interval: ... seconds; STALE if older than ... seconds

## Evidence Layout (local, gitignored)
- ...

## Log (append-only)
- {{DATE}} — launched; see `research.py runs --check {{ID}}`.
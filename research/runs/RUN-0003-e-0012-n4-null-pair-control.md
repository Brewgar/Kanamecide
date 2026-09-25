---
id: RUN-0003
type: run
title: E-0012 N4 null-pair control
work_item: W-0005
launcher: runjob.py
command: null
pid: null
started: 2026-09-25
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

# RUN-0003 — E-0012 N4 null-pair control

> A RUN record is the liveness proof for any job that outlives one shell command.
> Contract (SYSTEM.md §6): the job writes incremental evidence to disk, writes a
> heartbeat while alive, and can be resumed from its checkpoint. `research.py runs
> --check` reads the heartbeat file's age and the PID; a RUN claiming `RUNNING` with a
> stale heartbeat is a DEAD/FALSE claim and must be resolved before any result from it
> is used.

## Command (exactly as launched)
```powershell
python research/scripts/runjob.py launch --id RUN-0003 --name "E-0012 N4 null-pair" --log m0_audit/e0012_null/run.log --heartbeat m0_audit/e0012_null/heartbeat.txt --checkpoint m0_audit/e0012_null/games.jsonl --retry 0 --probe 4 --interval 15 -- python tools\e0012_sprt.py --live --exe build\Release\kana.exe --tier S --stage-a 6 --stage-b 6 --cap 240 --salt 20260924 --null-pair --out m0_audit/e0012_null/games.jsonl --checkpoint m0_audit/e0012_null/checkpoint.json --incidents m0_audit/e0012_null/incidents.jsonl
```

## Pre-launch pins (frozen E-0012 N4 contract; HO-0011)
- N4 null pair: stage 6 vs stage 6 (same binary, same EvalStage), Tier S [0, +20] lite-LLR
  statistic, cap 240 hard, salt 20260924; `--null-pair` freezes exactly (S, 6, 6, 240).
- PASS = no H1 acceptance within the cap AND the final cumulative LLR consistent with the
  colour-corrected null (measured White 58.5% prior; a 50%-centred band is explicitly
  prohibited). An H1 acceptance on the null pair is a harness-bias alarm, never an
  engine-strength claim.
- Binary: `build\Release\kana.exe` SHA-256
  `504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa` (== EV-0010 pin).
- Source commit: harness-stamped `git rev-parse HEAD` per JSONL row; the record set is
  committed before launch; the stamped value is recorded in the Log below.
- TC: `go wtime 1500 btime 1500 winc 100 binc 100` (harness `TC_COMMAND`, 100ms+100ms inc).

## Expected Duration / Size
240 games at the E-0010-recorded 769 games/h ⇒ ~0.3 h. Expected outcome under a correct
harness: cap reached, final LLR no decision (this is also the live test of the honest
INCONCLUSIVE / cap path). Evidence is local and gitignored.

## Checkpoint & Resume
- Checkpoint file(s): `m0_audit/e0012_null/checkpoint.json` (state) + the authoritative JSONL
  `m0_audit/e0012_null/games.jsonl` (JSONL-first write order per E-0012 B2.i).
- Resume command: the identical launch command; the job replays the JSONL and ABORTs on any
  mismatch > 1e-9.
- Completed-item semantics: game indexes already present in the JSONL are not replayed.
- `--retry 0` is deliberate (HO-0011): no silent re-runs; any resume is an explicit, recorded
  operator action after preserving the interrupted log.

## Heartbeat
- Heartbeat file: `m0_audit/e0012_null/heartbeat.txt`
- Interval: 15 seconds; STALE if older than 120 seconds (`runjob.py status`).

## Evidence Layout (local, gitignored)
- JSONL (authoritative): `m0_audit/e0012_null/games.jsonl`
- Checkpoint: `m0_audit/e0012_null/checkpoint.json`
- Incidents: `m0_audit/e0012_null/incidents.jsonl`
- Log: `m0_audit/e0012_null/run.log` (+ `run.log.supervisor`)
- Preserved pre-resume logs (if any): `run.log.<UTC>.preserved`

## Log (append-only)
- 2026-09-25 — RUN record created BEFORE launch (CLI `new-run`); frozen command recorded
  verbatim; no contract text changed. Launch is staged after RUN-0002 reaches a terminal
  state (HO-0011 ordering).
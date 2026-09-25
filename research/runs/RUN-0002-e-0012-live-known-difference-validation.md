---
id: RUN-0002
type: run
title: E-0012 live known-difference validation
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

# RUN-0002 — E-0012 live known-difference validation

> A RUN record is the liveness proof for any job that outlives one shell command.
> Contract (SYSTEM.md §6): the job writes incremental evidence to disk, writes a
> heartbeat while alive, and can be resumed from its checkpoint. `research.py runs
> --check` reads the heartbeat file's age and the PID; a RUN claiming `RUNNING` with a
> stale heartbeat is a DEAD/FALSE claim and must be resolved before any result from it
> is used.

## Command (exactly as launched)
```powershell
python research/scripts/runjob.py launch --id RUN-0002 --name "E-0012 known-difference" --log m0_audit/e0012_known/run.log --heartbeat m0_audit/e0012_known/heartbeat.txt --checkpoint m0_audit/e0012_known/games.jsonl --retry 0 --probe 4 --interval 15 -- python tools\e0012_sprt.py --live --exe build\Release\kana.exe --tier S --stage-a 6 --stage-b 0 --salt 20260924 --validation-known --out m0_audit/e0012_known/games.jsonl --checkpoint m0_audit/e0012_known/checkpoint.json --incidents m0_audit/e0012_known/incidents.jsonl
```

## Pre-launch pins (frozen E-0012 contract; HO-0011)
- Tier S [0, +20], cap 8,000 (default), salt 20260924, stage A=6, stage B=0;
  `--validation-known` freezes exactly (S, 6, 0, default cap) — no tier/bound/cap/stop-band/
  salt change is permitted after any live result is observed.
- Binary: `build\Release\kana.exe` SHA-256
  `504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa` (== EV-0010 pin;
  certutil re-checked 2026-09-25).
- Source commit: the harness stamps its own `git rev-parse HEAD` on every JSONL row; the
  record set (HO-0011 acceptance + RUN-0002/RUN-0003 + E-0012 RUNNING) is committed before
  launch; the stamped value is recorded in the Log below.
- TC: `go wtime 1500 btime 1500 winc 100 binc 100` (harness `TC_COMMAND`, 100ms+100ms inc).
- PASS gates (E-0012 (v1)–(v4), not reinterpreted): H1 accepted; crossing ∈ [80, 800];
  duplicate move lists 0 and 100% legal games; ≤2 engine pairs with crash-rule accounting.

## Expected Duration / Size
~133–191 games expected (E-0010-recorded 769 games/h ⇒ ~0.2–0.25 h); worst case is the
Tier-S cap 8,000 (~10.4 h) ⇒ INCONCLUSIVE, which on this known pair is a harness FAIL.
Evidence is local and gitignored.

## Checkpoint & Resume
- Checkpoint file(s): `m0_audit/e0012_known/checkpoint.json` (state) + the authoritative
  JSONL `m0_audit/e0012_known/games.jsonl` (JSONL-first write order per E-0012 B2.i).
- Resume command: the identical launch command (runjob `resume` is a plain relaunch; the job
  replays the JSONL and ABORTs on any mismatch > 1e-9).
- Completed-item semantics: game indexes already present in the JSONL are not replayed;
  `next_game_index` continues from the recomputed state.
- `--retry 0` is deliberate (HO-0011): no silent process-level re-runs; any resume must be an
  explicit, recorded operator action after preserving the interrupted log.

## Heartbeat
- Heartbeat file: `m0_audit/e0012_known/heartbeat.txt`
- Interval: 15 seconds; STALE if older than 120 seconds (`runjob.py status`).

## Evidence Layout (local, gitignored)
- JSONL (authoritative): `m0_audit/e0012_known/games.jsonl`
- Checkpoint: `m0_audit/e0012_known/checkpoint.json`
- Incidents: `m0_audit/e0012_known/incidents.jsonl`
- Log: `m0_audit/e0012_known/run.log` (+ `run.log.supervisor`)
- Preserved pre-resume logs (if any): `run.log.<UTC>.preserved`

## Log (append-only)
- 2026-09-25 — RUN record created BEFORE launch (CLI `new-run`); frozen command recorded
  verbatim; no contract text changed.
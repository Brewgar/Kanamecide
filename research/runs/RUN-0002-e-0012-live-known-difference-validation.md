---
id: RUN-0002
type: run
title: E-0012 live known-difference validation
work_item: W-0005
launcher: runjob.py
command: "python research/scripts/runjob.py launch --id RUN-0002 --name \"E-0012 known-difference\" --log m0_audit/e0012_known/run.log --heartbeat m0_audit/e0012_known/heartbeat.txt --checkpoint m0_audit/e0012_known/games.jsonl --retry 0 --probe 4 --interval 15 -- python tools/e0012_sprt.py --live --exe build/Release/kana.exe --tier S --stage-a 6 --stage-b 0 --salt 20260924 --validation-known --out m0_audit/e0012_known/games.jsonl --checkpoint m0_audit/e0012_known/checkpoint.json --incidents m0_audit/e0012_known/incidents.jsonl"
pid: 28404
started: 2026-09-25
created: 2026-09-25
heartbeat: m0_audit/e0012_known/heartbeat.txt
checkpoint: m0_audit/e0012_known/games.jsonl
resume: "same command via runjob.py resume; preserve run.log to run.log.<UTC>.preserved first; --retry 0 is deliberate"
concurrency_cap: 2
evidence_location: local
status: COMPLETED
finished: 2026-09-25
exit_code: 0
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
- 2026-09-25 18:10Z — LIVE LAUNCH (single command chain: record-set commit `7aab350` pushed to
  origin/master, then `runjob.py launch`): LAUNCH2_EXIT=0; detached generator pid=28404,
  supervisor pid=29264. `runjob.py status` reports ALIVE (15-second heartbeat, checkpoint
  growing). JSONL rows carry `src_commit` = the launch-time HEAD; verified from row 1 below.
- 2026-09-25 18:29:34Z — TERMINAL. Supervisor heartbeat final line:
  `2026-09-25 18:29:55 EXIT pid=28404 checkpoint_lines=125 checkpoint_bytes=178549 (process gone)`.
  Supervisor pid 29264, generator pid 28404, single uninterrupted execution — no resume, no
  pre-resume log preservation needed, `--retry 0` honoured (zero relaunches). Detached
  watcher `m0_audit/s0018/watch_known.ps1` recorded `EXITED 2026-09-25T18:29:34 N=125 V=H1`
  (observer only; it never touched the run).

## Terminal Result — RUN-0002 (known-difference) — **PASS**
- Verdict **H1 ACCEPTED at game 125** — inside the frozen E-0012 acceptance window [80, 800].
- Final tally: n=125, wins(A)=80, draws=20, losses(B)=25; LLR 2.9590633873412573 ≥
  bound 2.9444389791664403; verdict H1; `next_game_index`=125.
- Harness final line (`run.log`): `{"config": {...}, "crossing": {"game": 125,
  "llr": 2.9590633873412573, "verdict": "H1"}, "draws": 20, "losses": 25, "n": 125,
  "next_game_index": 125, "verdict": "H1", "wins": 80}`.
- Incidents: `m0_audit/e0012_known/incidents.jsonl` **does not exist** — zero crash
  incidents over 125 games, so the crash=loss rule was never exercised and crash-rule
  accounting is clean by absence of incidents (0 engine crashes, 0 adjudicated crashes).
- Duplicate move lists: **0**. Legality: **125/125 legal**, 0 replay failures.

## Independent Executor-Side Audit (not self-verification)
Command: `python m0_audit/s0018/e0012_audit.py m0_audit/e0012_known/games.jsonl
m0_audit/e0012_known/checkpoint.json 6 0 8000 20260924` → **AUDIT_EXIT=0**, output
`m0_audit/s0018/audit_known_final.json`, stderr `m0_audit/s0018/audit_known_final.err`
(empty). The auditor recomputes the LLR with its own implementation and replays every game
through python-chess, then cross-checks the harness checkpoint:
- `RESULT: PASS`, `problems: {}`, `rows: 125`, `duplicates: 0`, `legality_failures: 0`
- `llr_recomputed` 2.9590633873412573 == `checkpoint_llr`; `verdict_recomputed` `H1` ==
  `checkpoint_verdict` `H1`; `crossing` objects equal
- provenance unique per row: `binary_sha256`, `src_commit`, `campaign_salt` 20260924;
  dense `game_id` 0..124; colour alternation; `seed_int` and opening re-derivation
  re-checked independently for all 125 rows; end-vocabulary and end re-derivation clean
- `white_score_observed` 0.56 (colour-corrected context for the N4 null in RUN-0003)
- JSONL SHA-256 `637a9fa4229ee8ab54b3c8f8420731659575d6ee59dda72c4a2311198650d407`

## Artifact Hashes (certutil SHA-256, 2026-09-25)
- `m0_audit/e0012_known/games.jsonl` → `637a9fa4229ee8ab54b3c8f8420731659575d6ee59dda72c4a2311198650d407`
- `m0_audit/e0012_known/checkpoint.json` → `42fd7732b340568e099be5c31be10de8ea52c337dd1cbdfd83801a4232f460c6`
- `m0_audit/e0012_known/run.log` → `940fc8a9c90d04bcde6d8200020cd12d0fad4cf5020f6f1ff14e79c3329496a1`
- `m0_audit/e0012_known/heartbeat.txt` → `547ca56e6c45b5d731a6e699ee345c3fd28a38b96b71aa3c54ade228c4713458`
- `m0_audit/e0012_known/incidents.jsonl` → absent (no incidents)
- binary `build/Release/kana.exe` → `504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa`
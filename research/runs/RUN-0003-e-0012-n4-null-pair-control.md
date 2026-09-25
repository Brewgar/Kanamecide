---
id: RUN-0003
type: run
title: E-0012 N4 null-pair control
work_item: W-0005
launcher: runjob.py
command: "python research/scripts/runjob.py launch --id RUN-0003 --name \"E-0012 N4 null-pair\" --log m0_audit/e0012_null/run.log --heartbeat m0_audit/e0012_null/heartbeat.txt --checkpoint m0_audit/e0012_null/games.jsonl --retry 0 --probe 4 --interval 15 -- python tools/e0012_sprt.py --live --exe build/Release/kana.exe --tier S --stage-a 6 --stage-b 6 --cap 240 --salt 20260924 --null-pair --out m0_audit/e0012_null/games.jsonl --checkpoint m0_audit/e0012_null/checkpoint.json --incidents m0_audit/e0012_null/incidents.jsonl"
pid: 2904
started: 2026-09-25
created: 2026-09-25
heartbeat: m0_audit/e0012_null/heartbeat.txt
checkpoint: m0_audit/e0012_null/games.jsonl
resume: "same command via runjob.py resume; preserve run.log to run.log.<UTC>.preserved first; --retry 0 is deliberate"
concurrency_cap: 2
evidence_location: local
status: COMPLETED
finished: 2026-09-25
exit_code: 0
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
- 2026-09-25 18:30Z — LIVE LAUNCH, only after RUN-0002 was terminal (H1 at game 125, audited
  PASS). `runjob.py launch` printed `checkpoint before launch: 0 item(s), 0 bytes` (clean
  start, no pre-existing evidence) and returned **LAUNCH3_EXIT=0**; detached generator
  pid=2904, supervisor pid=20444; evidence `m0_audit/s0018/launch3.txt`. `--retry 0`
  deliberate. Frozen N4 contract unchanged: stage 6 vs 6, Tier S, cap 240, salt 20260924.
- 2026-09-25 19:04:22Z — TERMINAL at the cap. Watcher
  `m0_audit/s0018/null_exit_marker.txt`: `EXITED 2026-09-25T19:04:22 N=240 V=INCONCLUSIVE
  C= LLR=-0.6852460784333203 W=106 L=111 D=23`; generator pid 2904 gone. Single
  uninterrupted execution — no resume, no retry, no pre-resume log needed; `--retry 0`
  honoured.

## Terminal Result — RUN-0003 (N4 null pair) — **PASS (no harness bias)**
- **No H1 acceptance**; run terminated at the frozen **cap 240** with verdict
  `INCONCLUSIVE`, `crossing: null` — the pre-registered "complete under the cap without
  adopting a biased verdict" outcome, i.e. the live test of the honest-INCONCLUSIVE/cap path
  that the offline replay could never reach.
- Final tally: n=240, W=106 / D=23 / L=111; **final LLR −0.6852460784333203** — sign
  negative and |LLR| ≈ 0.69, i.e. small and consistent with a colour-corrected null
  (R-0015's delta-method drift ≈ −0.0015/game, sd ≈ 0.058/game ⇒ sd of the cumulative LLR at
  240 games ≈ 0.90; the realized −0.685 is ≈ −0.76σ). No harness bias detected.
- Harness null block (verbatim from `run.log` final line): `"null_control":
  {"band_centred_at_50pct": false, "observed_white_score": 0.6145833333333334,
  "pass": true, "white_prior": 0.585}` — the colour-corrected 58.5% prior was used
  (`band_centred_at_50pct: false`, the explicitly prohibited naive 50%-centred band was not
  used), and the harness's own null-consistency check reports `pass: true`.
- Incidents: `m0_audit/e0012_null/incidents.jsonl` **does not exist** — 0 engine crashes in
  240 games.
- Duplicate move lists: **0**. Legality: **240/240 legal**, 0 replay failures.

## Independent Executor-Side Audit (not self-verification)
Command: `python m0_audit/s0018/e0012_audit.py m0_audit/e0012_null/games.jsonl
m0_audit/e0012_null/checkpoint.json 6 6 240 20260924` → **AUDIT_NULL_EXIT=0**, output
`m0_audit/s0018/audit_null_final.json`, stderr `m0_audit/s0018/audit_null_final.err`
(empty):
- `RESULT: PASS`, `problems: {}`, `rows: 240`, `duplicates: 0`, `legality_failures: 0`
- `llr_recomputed` −0.6852460784333203 == `checkpoint_llr`; `verdict_recomputed`
  `INCONCLUSIVE` == `checkpoint_verdict`; `crossing` null in both
- provenance unique per row (`binary_sha256`, `src_commit`, `campaign_salt` 20260924); dense
  `game_id` 0..239; colour alternation; `seed_int` and opening re-derivation re-checked
  independently for all 240 rows
- `white_score_observed` 0.6145833333333334
- JSONL SHA-256 `5654db6075703625fd30c633805abaf935eb584da25dc4277fa24d494693e30d`

## Artifact Hashes (certutil SHA-256, 2026-09-25)
- `m0_audit/e0012_null/games.jsonl` → `5654db6075703625fd30c633805abaf935eb584da25dc4277fa24d494693e30d`
- `m0_audit/e0012_null/checkpoint.json` → `54bc622e9bb058258fd38b23ccced6958d9e64259a95e5fc413ec74d8d3b058b`
- `m0_audit/e0012_null/run.log` → `fdb3e379e5a56f36d81c0718adcca3a45df32e75989c7ffff4255258c27082ca`
- `m0_audit/e0012_null/heartbeat.txt` → `a6bc3c337c48c15d3cfc87829d14d966ca872c8d00fce86f6453471fe96e6b62` (final
  line `2026-09-25 19:04:46 EXIT pid=2904 checkpoint_lines=240 checkpoint_bytes=340892`)
- `m0_audit/e0012_null/incidents.jsonl` → absent (no incidents)
- binary `build/Release/kana.exe` → `504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa`

## Artifact Hashes (certutil SHA-256, 2026-09-25)
- `m0_audit/e0012_null/games.jsonl` → `5654db6075703625fd30c633805abaf935eb584da25dc4277fa24d494693e30d`
- `m0_audit/e0012_null/checkpoint.json` → `54bc622e9bb058258fd38b23ccced6958d9e64259a95e5fc413ec74d8d3b058b`
- `m0_audit/e0012_null/run.log` → `fdb3e379e5a56f36d81c0718adcca3a45df32e75989c7ffff4255258c27082ca`
- `m0_audit/e0012_null/heartbeat.txt` → `a6bc3c337c48c15d3cfc87829d14d966ca872c8d00fce86f6453471fe96e6b62`
- `m0_audit/e0012_null/incidents.jsonl` → absent (no incidents)
- binary `build/Release/kana.exe` → `504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa`
- observer-only evidence: `m0_audit/s0018/null_progress.txt`, `null_exit_marker.txt`,
  `watch_null.ps1`, `poll_null.ps1` (read-only observers; they never wrote to run artifacts)
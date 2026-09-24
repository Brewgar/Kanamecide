---
id: RUN-0001
type: run
title: "E-0011 1,000-game self-play training dataset campaign"
work_item: W-0001
launcher: runjob.py
command: "python research/scripts/runjob.py launch --id RUN-0001 --name E-0011-campaign-v2 --log m0_audit/e0011/run.log --heartbeat m0_audit/e0011/heartbeat.txt --checkpoint m0_audit/e0011/games.jsonl --retry 5 --probe 4 --interval 15 -- python tools/e0011_generate.py --games 1000 --salt 20260922 --pairs 2 --expected-binary-sha256 504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa --expected-src-commit 7b1dda15f675b884a8bf971eec4b53a0fdf2049f --out m0_audit/e0011/games.jsonl"
pid: 14276
started: "2026-09-24"
created: "2026-09-24"
heartbeat: m0_audit/e0011/heartbeat.txt
checkpoint: m0_audit/e0011/games.jsonl
resume: "same command via runjob.py resume; preserve run.log to run.log.<UTC>.preserved first"
concurrency_cap: 2
evidence_location: local
status: COMPLETED
finished: "2026-09-24"
exit_code: 0
example: false
---

# RUN-0001 — E-0011 1,000-game self-play training dataset campaign

## Replacement Command (attempt 2, exact)
```powershell
python research/scripts/runjob.py launch --id RUN-0001 --name "E-0011 campaign v2" --log m0_audit/e0011/run.log --heartbeat m0_audit/e0011/heartbeat.txt --checkpoint m0_audit/e0011/games.jsonl --retry 5 --probe 4 --interval 15 -- python tools/e0011_generate.py --games 1000 --salt 20260922 --pairs 2 --expected-binary-sha256 504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa --expected-src-commit 7b1dda15f675b884a8bf971eec4b53a0fdf2049f --out m0_audit/e0011/games.jsonl
```

## Pre-launch pins
- UCI entry: `Popen([build/Release/kana.exe, "uci"])`, then stdin `uci`; transcript `research/context/uci_s15_transcript.txt` SHA-256 `8df5a62a41fe02c824c497b0c094a3000c57da9d6e0290c6253eae14e0128fe4`.
- Binary: `504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa`, exactly EV-0010; no binary protocol deviation.
- Source commit: `7b1dda15f675b884a8bf971eec4b53a0fdf2049f` (replacement segment; attempt-1 pin remains logged below).
- Generator SHA-256: `2e939222a8a464983c08a657f5b0f2a46b54526ebd9c891a370674d2e87db1e6`.
- Checker SHA-256: `321294eccdb9f571910b028f0074d9ac3734a5dac442dd3f314ec4830018513b`.
- Compile flags: MSVC Release `/W4 /EHsc /O2 /GL /arch:AVX512 /DNDEBUG`, IPO/LTCG.
- TC: `go wtime 1500 btime 1500 winc 100 binc 100`; two engine pairs maximum.
- Acceptance: 6/6 live smoke legal; synthetic-20 negative exits 1 on named defects; deterministic 1,000-game truncation drill PASS at kill game 500; log-preservation hashes identical.

## Expected Duration / Size
Approximately 1.3 hours and a local, gitignored JSONL dataset; raw bytes are pinned by SHA-256, not committed.

## Checkpoint & Resume
- Checkpoint: `m0_audit/e0011/games.jsonl` (the authoritative JSONL itself).
- Resume: run the identical command through `runjob.py resume`; the generator validates complete records, quarantines a torn tail, and re-emits only missing IDs.
- Before every resume, copy `m0_audit/e0011/run.log` to `m0_audit/e0011/run.log.<UTC>.preserved` and append both names here.
- Live kill window: game 400–600. `runjob.py` line counts are telemetry only.

## Heartbeat
- `m0_audit/e0011/heartbeat.txt`; interval 15 seconds, stale after 120 seconds.

## Evidence Layout (local, gitignored)
- Dataset: `m0_audit/e0011/games.jsonl`
- Events: `m0_audit/e0011/games.jsonl.events.jsonl`
- Log: `m0_audit/e0011/run.log`
- Preserved pre-resume logs: `m0_audit/e0011/run.log.<UTC>.preserved`
- Checker output at close: `m0_audit/e0011/check_output.txt`
- Excluded failed segment: `m0_audit/e0011_failed_attempt1/` (never mixed with replacement dataset)

## Log (append-only)
- 2026-09-24 — RUN record created before live launch; owner bundled implementation-engineer + systems-researcher for W-0001 step 2.
- 2026-09-24 00:52Z — LIVE LAUNCH: generator PID 30892, supervisor PID 8340, heartbeat `m0_audit/e0011/heartbeat.txt`; checkpoint began at 0 and grew to 2 complete JSONL games. Attempt-1 command pinned src `752216c715bce2db3e5ac11a76554ac496799b14`; exact log/checkpoint evidence is now preserved under `m0_audit/e0011_failed_attempt1/`.
- 2026-09-24 — **FAILED SEGMENT / protocol contradiction recorded:** attempt 1 stopped at 202 complete games after two crash-loss records and then `generator_failed: RuntimeError('engine readiness failed before game start')`. The failed 202-game JSONL SHA-256 is `1a95e8ddb418f42481fb1d4e8b59bd804f388cd7fa9c28db69d104e8fae76bfa`; events SHA-256 `f0dac5b66e7675223281b0eff6b5f2d7e24ba7148fc779b27b491bd3a161fdd1`; run log SHA-256 `e76b6b215da332c4497f814b32b8fcaa8ca38296d6364d72e3459e6e802d3b0f`. This segment is EXCLUDED from the final dataset and will not be mixed across source pins.
- 2026-09-24 — Root cause fixed in code commit `7b1dda15f675b884a8bf971eec4b53a0fdf2049f`: construction/readiness failures now emit crash-loss records; every crash explicitly closes and recreates the engine pair; reader-thread shutdown is deterministic. Unit crash-loss assertions PASS. Repaired 1,000-game truncation drill PASS at kill game 500 with 500 re-emissions, dense final 1,000, duplicate-move-lists=0 (`m0_audit/e0011/drill_v2.log`). Replacement dataset is pinned wholly to `7b1dda1`.
- 2026-09-24 16:02Z — REPLACEMENT LIVE LAUNCH: generator PID 7600, supervisor PID 28160, controller PID 512/supervisor 28220; replacement checkpoint started at 0 and is growing. Repaired six-game smoke completed 6/6 and checker exit 0 before launch. Command is the front-matter/Replacement Command line; all final dataset records will carry src `7b1dda15f675b884a8bf971eec4b53a0fdf2049f`.


- 2026-09-24 13:28:10Z — LIVE KILL/RESUME BOUNDARY: controller killed generator PID 7600
  after exactly 400 complete records; `taskkill_exit=0`. The preserved source log is
  `run.log.20260924T132806Z.preserved`, SHA-256
  `390f4b8222570f9c5a9e9722130c9de1c16794c62a0946a07ee6c900f7879fc5`, matching the
  controller evidence. The identical pinned command was resumed through `runjob.py`; the
  resume launcher returned 0 and started final generator PID 14276.
- 2026-09-24 14:08:04Z — GENERATOR TERMINAL: event sidecar recorded
  `generator_complete`, `valid_after=1000`, `games_added=600`; the final log line is
  `COMPLETE games=1000 added=600`; the heartbeat records `EXIT pid=14276` with 1,000
  checkpoint lines. The normal pinned generator path returns 0. `runjob.py status`
  independently returned 0, `FINISHED (process gone)`, checkpoint 1,000/1,384,548 bytes.
  The detached supervisor does not persist a long-lived child's OS return code; the
  recorded terminal result is therefore based on the complete normal path, not an invented
  OS-code observation.
- 2026-09-24 14:08:13Z — FINALIZER PASS: `finalizer_result.json` (SHA-256
  `08e38be145d1829ca2d896b68bafa3e9edb39b38c97544b28a6c31fe9c629133`) captured checker exit 0,
  dataset SHA-256 `27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95`,
  check-output SHA-256 `9fe6b532ad08fce94890bc06b3969b35a0f625e57d94d8edd2851571876ed907`,
  and all six gates PASS.
- 2026-09-24 — LOG HASHES: preserved pre-resume log
  `390f4b8222570f9c5a9e9722130c9de1c16794c62a0946a07ee6c900f7879fc5`; completed replacement
  log `cdb326daa45319fe3e7a67b36022c067fbf327b589fc59c3ad7352c82abd1a56`; event sidecar
  `573fa6765068c7e3130079c23628d6c9432a5d172f50057fd2b7e9512b6abbb3`.


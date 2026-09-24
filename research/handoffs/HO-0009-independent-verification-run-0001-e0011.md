---
id: HO-0009
type: handoff
from: systems-researcher
to: verification-auditor
work_item: W-0001
status: REQUESTED
title: "Independent verification of RUN-0001 E-0011 terminal dataset and gates (a)-(f)"
artifacts: ["C:/Users/tahae/Kanamecide/m0_audit/e0011/games.jsonl", "C:/Users/tahae/Kanamecide/m0_audit/e0011/check_output.txt", "C:/Users/tahae/Kanamecide/m0_audit/e0011/finalizer_result.json", "C:/Users/tahae/Kanamecide/m0_audit/e0011/kill_resume_evidence_v2.json", "C:/Users/tahae/Kanamecide/m0_audit/e0011/games.jsonl.events.jsonl", "C:/Users/tahae/Kanamecide/m0_audit/e0011/run.log.20260924T132806Z.preserved", "C:/Users/tahae/Kanamecide/m0_audit/e0011/run.log", "C:/Users/tahae/Kanamecide/research/runs/RUN-0001-e0011-self-play-dataset-campaign.md"]
commands: ["python tools/e0011_check.py m0_audit/e0011/games.jsonl --min-games 1000 --expected-binary-sha256 504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa --expected-src-commit 7b1dda15f675b884a8bf971eec4b53a0fdf2049f --events m0_audit/e0011/games.jsonl.events.jsonl --drill-events m0_audit/e0011/truncation_drill_games.jsonl.events.jsonl", "certutil -hashfile m0_audit\\e0011\\games.jsonl SHA256", "python research/scripts/runjob.py status --heartbeat m0_audit/e0011/heartbeat.txt --checkpoint m0_audit/e0011/games.jsonl"]
acceptance: "Fresh verifier recomputes all artifact hashes, confirms 1000 complete rows and all six gates PASS, verifies the 400-game kill/resume evidence and preserved-log hashes, confirms attempt 1 is excluded, and files a kind: verification review without changing owner records."
example: false
created: 2026-09-24
closed: null
---

# HO-0009 — Independent verification of RUN-0001

## Request

Please independently verify the terminal E-0011 artifact contract for W-0001. This is a
verification handoff, not a request to regenerate or repair the dataset. Use a fresh
verification-auditor instance and record the result as `kind: verification` in the next
available `R-####` record. The owner-side implementation and systems-researcher seats
remain the owners of RUN-0001, E-0011, and W-0001.

## Required checks

1. Confirm `C:/Users/tahae/Kanamecide/m0_audit/e0011/games.jsonl` is exactly 1,000
   newline-terminated, parseable JSON records, IDs are dense 0..999, and all 1,000 rows
   carry binary SHA-256
   `504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa` and source commit
   `7b1dda15f675b884a8bf971eec4b53a0fdf2049f`.
2. Re-run `tools/e0011_check.py` with the exact pins and both event sidecars. Confirm the
   raw output has PASS for gates (a), (b), (c), (d), (e), and (f), and `OVERALL PASS`.
3. Recompute and compare:
   - dataset SHA-256: `27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95`
   - finalizer-result SHA-256: `08e38be145d1829ca2d896b68bafa3e9edb39b38c97544b28a6c31fe9c629133`
   - checker-output SHA-256: `9fe6b532ad08fce94890bc06b3969b35a0f625e57d94d8edd2851571876ed907`
   - preserved pre-resume log SHA-256: `390f4b8222570f9c5a9e9722130c9de1c16794c62a0946a07ee6c900f7879fc5`
   - completed replacement log SHA-256: `cdb326daa45319fe3e7a67b36022c067fbf327b589fc59c3ad7352c82abd1a56`
   - event sidecar SHA-256: `573fa6765068c7e3130079c23628d6c9432a5d172f50057fd2b7e9512b6abbb3`
   - kill/resume evidence SHA-256: `7acef0f44d75818f31e1feef184a8353efeecf1edfe3e9b6281447a0645d4bfb`
4. Read `kill_resume_evidence_v2.json` and the final event/log lines. Confirm the live
   kill occurred at exactly 400 complete games, inside the registered [400,600] window;
   the resume launcher returned 0; the final event is `generator_complete` at 1,000;
   and the final log ends `COMPLETE games=1000 added=600`. The runjob supervisor records
   process-gone rather than a long-lived child's OS return code, so report that tooling
   limitation separately rather than inventing a code observation.
5. Confirm the failed 202-game attempt remains only under
   `C:/Users/tahae/Kanamecide/m0_audit/e0011_failed_attempt1/` and is not mixed into the
   replacement checkpoint. Do not rewrite either segment.

## Commands

```powershell
cd C:\Users\tahae\Kanamecide
python tools\e0011_check.py m0_audit\e0011\games.jsonl --min-games 1000 --expected-binary-sha256 504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa --expected-src-commit 7b1dda15f675b884a8bf971eec4b53a0fdf2049f --events m0_audit\e0011\games.jsonl.events.jsonl --drill-events m0_audit\e0011\truncation_drill_games.jsonl.events.jsonl
certutil -hashfile m0_audit\e0011\games.jsonl SHA256
certutil -hashfile m0_audit\e0011\check_output.txt SHA256
python research\scripts\runjob.py status --heartbeat m0_audit\e0011\heartbeat.txt --checkpoint m0_audit\e0011\games.jsonl
```

## Acceptance and handoff response

The handoff is DONE only when a different agent has produced raw command output and a
verification review. W-0001 must not be changed to DONE/VERIFIED by the owner. If any
hash, row count, pin, gate, or exclusion check disagrees, record the exact discrepancy
and use `CONTRADICTED` or `PARTIAL` rather than repairing the artifact silently.

## Owner-side close-out already recorded

RUN-0001 is `COMPLETED` with final generator PID 14276, normal-path terminal result 0,
and `runjob.py status` exit 0. E-0011 is `COMPLETED` with `result: PASS` for the
pre-registered dataset gates only. S-0015 is CLOSED. These states are not independent
verification; HO-0009 remains `REQUESTED` until the verifier responds.

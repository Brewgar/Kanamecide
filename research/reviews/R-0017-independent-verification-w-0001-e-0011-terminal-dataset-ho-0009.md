---
id: R-0017
type: review
reviewer: verification-auditor
target: W-0001
kind: verification
status: COMPLETED
work_item: W-0001
related: [HO-0009, RUN-0001, E-0011]
example: false
created: 2026-09-24
---

# R-0017 — Independent verification of W-0001 / E-0011 terminal dataset

## Scope
Fresh verification-auditor occupant 5, receiving HO-0009. I did not edit or repair RUN-0001,
E-0011, the dataset, or source. I recomputed pinned hashes, reran the exact checker, checked
kill/resume evidence, and checked failed-attempt exclusion from raw data.

## Agreements
- The replacement dataset is 1,000 newline-terminated, parseable JSONL records. `game_id` is
  dense and unique over the set 0..999; row order is not a handoff requirement. Every row
  carries binary SHA-256 `504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa`
  and source commit `7b1dda15f675b884a8bf971eec4b53a0fdf2049f`.
- The exact `tools/e0011_check.py` command with both event sidecars exited 0. Its raw output
  reports gates (a), (b), (c), (d), (e), and (f) PASS and `OVERALL PASS gates=6`.
- The kill/resume evidence is internally consistent: 400 complete games at the live kill;
  window `[400,600]`; `taskkill_exit=0`; `resume_exit=0`; final event `generator_complete`
  with `valid_after=1000` and `games_added=600`; final log `COMPLETE games=1000 added=600`.
- Failed attempt 1 remains in `m0_audit/e0011_failed_attempt1/`, 202 rows at source commit
  `752216c715bce2db3e5ac11a76554ac496799b14`. It is not mixed into the replacement
  checkpoint, whose rows all carry the replacement commit above.

## Disagreements
None in the artifact contract. The handoff's `runjob.py status` says
`FINISHED (process gone)`, the supervisor's terminal classification rather than an observed
long-lived child's OS return code. I report that tooling limitation rather than inventing a
child return code, as the handoff directs.

## Missing Arguments
None required by HO-0009. This verifies the pre-registered dataset-generation contract; it
makes no strength or downstream-training claim.

## Factual Errors
None found. Earlier verifier-helper attempts failed before completion because of a path anchor
and then an over-strict row-order assumption. Those process failures remain in context; only
the corrected helper pass is admissible evidence.

## Assumptions
- Historical kill/resume JSON and event/log sidecars are accepted as evidence of the completed
  campaign; the campaign itself was not regenerated.
- `FINISHED (process gone)` is not treated as a child exit code.

## Proposed Experiments
None. E-0012/W-0005 and the future H-0013 training campaign remain separate gates.

## Verdict
**VERIFIED** for W-0001's terminal E-0011 dataset-generation contract.

## Date
2026-09-24

## Verification Block (kind: verification only)

- **Work item verified:** W-0001 (round 4); owner `systems-researcher`; different verifier seat.
- **Verified by:** verification-auditor (occupant 5)
- **Verdict:** VERIFIED
- **Commands re-run by me (raw output retained):**
  1. `build\\Release\\kana.exe` (Gate 0) -> exit 0; `research/context/ho0009_gate0.txt`.
  2. Exact `python tools/e0011_check.py ...` command from HO-0009 -> exit 0;
     `research/context/ho0009_checker_exact_utf8.txt`; all six gates and overall PASS.
  3. `python research/scripts/runjob.py status --heartbeat m0_audit/e0011/heartbeat.txt --checkpoint m0_audit/e0011/games.jsonl` -> exit 0;
     `research/context/ho0009_runjob_status_utf8.txt`; FINISHED, process gone, 1,000 items.
  4. `python -X utf8 research/context/ho0009_independent_audit.py` -> exit 0;
     `research/context/ho0009_independent_audit_utf8.txt`; `RESULT PASS`.
  5. Independent failed-dataset path/hash check -> exit 0;
     `research/context/ho0009_exclusion_utf8.txt`.

- **Artifacts checked (SHA-256 recomputed):**
  - `m0_audit/e0011/games.jsonl` — `27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95`
  - `m0_audit/e0011/finalizer_result.json` — `08e38be145d1829ca2d896b68bafa3e9edb39b38c97544b28a6c31fe9c629133`
  - `m0_audit/e0011/check_output.txt` — `9fe6b532ad08fce94890bc06b3969b35a0f625e57d94d8edd2851571876ed907`
  - `m0_audit/e0011/run.log.20260924T132806Z.preserved` — `390f4b8222570f9c5a9e9722130c9de1c16794c62a0946a07ee6c900f7879fc5`
  - `m0_audit/e0011/run.log` — `cdb326daa45319fe3e7a67b36022c067fbf327b589fc59c3ad7352c82abd1a56`
  - `m0_audit/e0011/games.jsonl.events.jsonl` — `573fa6765068c7e3130079c23628d6c9432a5d172f50057fd2b7e9512b6abbb3`
  - `m0_audit/e0011/kill_resume_evidence_v2.json` — `7acef0f44d75818f31e1feef184a8353efeecf1edfe3e9b6281447a0645d4bfb`
  - `build/Release/kana.exe` — `504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa`
  - `m0_audit/e0011_failed_attempt1/games.jsonl` — `1a95e8ddb418f42481fb1d4e8b59bd804f388cd7fa9c28db69d104e8fae76bfa`

- **What I reproduced independently:** all hashes above; JSONL parse/newline and row count;
  dense unique ID set; row-level binary/source pins; kill/resume chronology and terminal
  event/log; failed-attempt row count/hash/path and commit separation; checker six-gate result.
- **What I could NOT reproduce (and why):** I did not rerun the historical kill or infer a
  long-lived child's OS return code. Status reports process gone; stored taskkill/resume exits
  are 0.
- **Sample validity re-checked:** duplicate move lists are 0; the dataset uses two engine
  pairs. Arm differentiation, power, and strength remain outside this contract.
- **Claims that must be corrected in the record:** none.
- **Residual uncertainty (calibrated):** demonstrated for the listed artifact checks; this was
  not a fresh campaign rerun, and process-gone is not a child return code.

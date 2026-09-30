---
id: FND-0023
type: finding
title: "F-U7 Change the dedup key in tools/e0013_extract.py to the normalized FEN"
status: RESOLVED
example: false
created: 2026-09-30
severity: major
target: E-0013
raised_by: researcher-architect (S-0036..S-0040 F-U family)
review: E-0013
source_key: F-U7
resolution: F-U7 (change the dedup key to the normalized FEN): DISCHARGED. The extractor self-test asserts 'the dedup key IS the gate key, not a refinement of it' and is RED under the OLD exact-FEN key / GREEN under the NEW key; SELFTEST PASS checks=112 failed=0, exit 0, re-run this session.
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0023

## Finding

## Origin
Prose item `F-U7` extracted from the E-0013 F-U7..F-U13 obligation table, which carries the items recorded across sessions S-0036..S-0040.

## Finding
The obligation as stated in E-0013's own table. The source record is the authority; a verifier closes this row only with commands, outputs and hashes.

## Target
- Record: E-0013#F-U7

## Evidence
- Extracted by the verification-auditor's idempotent migration (`_obs/parts/extract_fu.py`), which skips any key already present as a `source_key:` in research/findings/.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED.** The dedup key is now the normalized four-field FEN, and — the part that
actually matters — the key is now **equal to** the gate's comparison key rather than finer than it.

**Commands re-run this session (2026-09-30), output in `_obs/vf/fu_evidence.txt`:**

1. `python tools/e0013_extract.py --selftest` → `SELFTEST PASS checks=112 failed=0`, **exit 0**.
2. The load-bearing assertion, which is the exact defect the ruling named:
   `PASS  dirty: the dedup key IS the gate key, not a refinement of it`
   This is the assertion R-0020/the S-0037 ruling identified as the root cause: a dedup key strictly
   finer than the gate's comparison key *cannot entail* the invariant.
3. `PASS  clock-only: GREEN under the NEW key - one survivor per normalized FEN` and
   `PASS  clock-only: GREEN under the NEW key - cross-split overlap is 0` — the S-0036 failure
   (`normalized_fen_overlap = 27`) is now structurally impossible under the new key.
4. `PASS  the published dedup_key excludes both clocks` and the code-level check
   `tools/e0013_extract.py:1247-1249` (`normalize_fen` excludes clock and fullmove, is exactly four
   fields, and side-to-move is part of the identity).
5. The published key in the running tool matches: `e0013_extract.py:531` states the gate compares
   `normalize_fen` and the dedup now keys on the same value.

**Residual uncertainty (stated, not smoothed):** this is verified on the **synthetic and clock-only
fixtures** the self-test constructs, not on the real 1,000-game dataset. The real-dataset
consequence is measured downstream (E-00015, which is PENDING) because the count may not be taken
until the corpus is re-committed under the new key. `PASS  the survivor rule is UNCHANGED (first
occurrence in (game_id, ply))` — deliberate, and the source of the F-U12 bias.


## Evidence
_commands, outputs, hashes_


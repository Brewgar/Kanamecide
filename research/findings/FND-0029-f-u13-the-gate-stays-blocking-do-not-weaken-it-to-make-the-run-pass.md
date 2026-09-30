---
id: FND-0029
type: finding
title: "F-U13 The gate stays blocking; do not weaken it to make the run pass"
status: RESOLVED
example: false
created: 2026-09-30
severity: major
target: E-0013
raised_by: researcher-architect (S-0036..S-0040 F-U family)
review: E-0013
source_key: F-U13
resolution: F-U13 (the gate stays blocking; do not weaken it to make the run pass): DISCHARGED. Verified negatively, which is the only way this row can be verified: 'dirty set aborts on the overlap gate' PASS, 'the gate FIRES on a genuine cross-split clock-only leak' PASS, and 'positions.jsonl / split_map.json / report.json are NOT written when the gate aborts'. The gate still aborts before fitting.
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0029

## Finding

## Origin
Prose item `F-U13` extracted from the E-0013 F-U7..F-U13 obligation table, which carries the items recorded across sessions S-0036..S-0040.

## Finding
The obligation as stated in E-0013's own table. The source record is the authority; a verifier closes this row only with commands, outputs and hashes.

## Target
- Record: E-0013#F-U13

## Evidence
- Extracted by the verification-auditor's idempotent migration (`_obs/parts/extract_fu.py`), which skips any key already present as a `source_key:` in research/findings/.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED — and this is the row that is verified *negatively*, which is the only honest
way to verify it.** A gate cannot be shown to be un-weakened by showing it passing; it can only be
shown to still fire. So I looked for the failure paths, not the success path.

**Commands re-run this session (2026-09-30), output in `_obs/vf/fu_evidence.txt`:**

1. `python tools/e0013_extract.py --selftest` → `SELFTEST PASS checks=112 failed=0`, **exit 0**.
2. **The gate still aborts the run on a real cross-split leak:**
   `PASS  negative control: the gate FIRES on a genuine cross-split clock-only leak` and
   `PASS  negative control: overlap_zero is False, so the run must abort`.
3. **The abort is FAIL-BEFORE-FITTING, verified at the artifact level** — the strongest form of this
   check, because it proves nothing is written even if a caller ignores the exit code:
   `PASS  dirty set aborts on the overlap gate`,
   `PASS  dirty: positions.jsonl is NOT written when the gate aborts`,
   `PASS  dirty: split_map.json is NOT written when the gate aborts`,
   `PASS  dirty: report.json is NOT written when the gate aborts`.
4. **Both pre-registered levels are still evaluated** — the gate computes the game-level and the
   normalized-FEN level and requires both to be zero, so neither can be quietly dropped:
   `tools/e0013_extract.py:599: "overlap_zero": game_overlap == 0 and norm_overlap == 0`, with
   `game_level_overlap` and `normalized_fen_overlap` both reported.
5. **No re-normalization, re-ordering or suppression is present in the code** —
   `tools/e0013_extract.py:564` is the gate docstring; the dedup (`:518 norm_fen=normalize_fen(...)`)
   and the gate (`:590 norm_overlap`) compare the *same* four-field key, so there is no second
   normalisation to hide behind.
6. **Accounting identities are enforced, not assumed** — if a counter or the dedup moved, the run
   aborts: `PASS  report: the exact accounting identities hold on the clean run` and
   `PASS  report: the one-survivor-per-normalized-FEN identity is published and true`.
   (Observed abort text during this session: `ABORT: EXACT ACCOUNTING IDENTITIES VIOLATED … This is a
   FINDING to report, not a baseline to re-derive, and no artifact is written` — the tool refusing to
   launder a broken count is itself evidence the gate is live.)

**Residual uncertainty (stated, not smoothed):** all of the above is exercised on the self-test's
constructed corpora. It demonstrates the gate is intact **in the code as written**; it does not
demonstrate the real 1,000-game dataset passes — and per the finding's own terms, *"if it does not,
that is a real defect in the implementation, and it must be reported as measured"*. That real-dataset
run is E-00015's, count-only, and it is **PENDING**. I did not run it and did not read the holdout.


## Evidence
_commands, outputs, hashes_


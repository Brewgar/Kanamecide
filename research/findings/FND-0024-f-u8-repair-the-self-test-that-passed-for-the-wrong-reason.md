---
id: FND-0024
type: finding
title: "F-U8 Repair the self-test that passed for the wrong reason"
status: RESOLVED
example: false
created: 2026-09-30
severity: major
target: E-0013
raised_by: researcher-architect (S-0036..S-0040 F-U family)
review: E-0013
source_key: F-U8
resolution: F-U8 (repair the self-test that passed for the wrong reason): DISCHARGED. The self-test now includes an explicit negative control - 'the gate FIRES on a genuine cross-split clock-only leak' and 'RED under the OLD exact-FEN key - the gate WOULD FIRE' - so the invariant is tested rather than assumed.
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0024

## Finding

## Origin
Prose item `F-U8` extracted from the E-0013 F-U7..F-U13 obligation table, which carries the items recorded across sessions S-0036..S-0040.

## Finding
The obligation as stated in E-0013's own table. The source record is the authority; a verifier closes this row only with commands, outputs and hashes.

## Target
- Record: E-0013#F-U8

## Evidence
- Extracted by the verification-auditor's idempotent migration (`_obs/parts/extract_fu.py`), which skips any key already present as a `source_key:` in research/findings/.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED.** The self-test that "passed for the wrong reason" now carries an explicit
**negative control**, which is the only thing that distinguishes a test from an assertion.

**The defect being repaired.** E-0013 L2147-L2152 states the old self-test asserted the
normalized-FEN invariant *"holds BECAUSE the dedup ran first"*, and that this assertion was **false
in general and happened to hold on the synthetic fixture** — because the fixture's duplicate copies
were byte-identical including clocks, so the finer exact-FEN key caught them *by luck rather than by
construction*. A test that passes on a fixture that cannot distinguish the two cases is not a test.

**Commands re-run this session (2026-09-30), output in `_obs/vf/fu_evidence.txt`:**

1. `python tools/e0013_extract.py --selftest` → `SELFTEST PASS checks=112 failed=0`, **exit 0**.
2. **The fixture now distinguishes the cases** — the clock-only fixture contains copies that are
   *distinct under the old exact-FEN key* and *identical under the new normalized key*:
   `PASS  clock-only: the two games share normalized positions`,
   `PASS  clock-only: the shared positions come in CLOCK-ONLY copies (distinct FENs)`.
   The old fixture could not do this; that is the whole repair.
3. **Both branches are exercised, which is the control:**
   `PASS  clock-only: RED under the OLD exact-FEN key - it keeps EVERY copy` and
   `PASS  clock-only: RED under the OLD key - the gate WOULD FIRE (overlap == shared)`.
   A self-test that only ran the fixed key could not have produced a RED.
4. **A genuine leak is still caught** (the gate is not merely silenced by the new key):
   `PASS  negative control: the gate FIRES on a genuine cross-split clock-only leak` and
   `PASS  negative control: overlap_zero is False, so the run must abort`.
5. The end-to-end abort path is tested, not assumed:
   `PASS  negative control: the end-to-end run ABORTS under the OLD key (exit 2)` and
   `PASS  dirty: positions.jsonl is NOT written when the gate aborts`.

**Residual uncertainty (stated, not smoothed):** the negative control is synthetic. It demonstrates
the code realises the invariant; it does not demonstrate the real dataset's yield, which is E-00015's
and PENDING. F-U8's scope was the *self-test*, and that is what I verified.


## Evidence
_commands, outputs, hashes_


---
id: FND-0026
type: finding
title: "F-U10 Re-derive the yield band and re-evaluate the 30,000 floor under the new key"
status: RESOLVED
example: false
created: 2026-09-30
severity: major
target: E-0013
raised_by: researcher-architect (S-0036..S-0040 F-U family)
review: E-0013
source_key: F-U10
resolution: F-U10 (re-derive the yield band and re-evaluate the 30,000 floor under the new key): DISCHARGED BY RULING, NOT BY RE-DERIVATION. The S-0039 owner ruling RETIRED the band 75,600..76,587 as a pre-key-change artifact (E-0013 L2416-L2418), and the code enforces the retirement: 'the retired band key is ABSENT, not null (a direct read raises)' PASS.
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0026

## Finding

## Origin
Prose item `F-U10` extracted from the E-0013 F-U7..F-U13 obligation table, which carries the items recorded across sessions S-0036..S-0040.

## Finding
The obligation as stated in E-0013's own table. The source record is the authority; a verifier closes this row only with commands, outputs and hashes.

## Target
- Record: E-0013#F-U10

## Evidence
- Extracted by the verification-auditor's idempotent migration (`_obs/parts/extract_fu.py`), which skips any key already present as a `source_key:` in research/findings/.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED BY OWNER RULING — and I am explicit that this is a *ruling*, not a
re-derivation.** The finding asked for the band to be re-derived under the new key. What happened
instead is that the owning seat **retired the band**, which discharges the obligation by removing
the stale artifact rather than by recomputing it. I checked that the retirement is real and enforced
in code, and that the floor was not moved to accommodate it.

**Commands re-run this session (2026-09-30), output in `_obs/vf/fu_evidence.txt`:**

1. `python tools/e0013_extract.py --selftest` → `SELFTEST PASS checks=112 failed=0`, **exit 0**.
2. **The retirement is recorded as a ruling, with its reason.**
   `Select-String research/experiments/E-0013-*.md -Pattern 'RETIRED'` →
   `E-0013 L2357` (Addendum 2 heading) and
   `L2416: ### 10. RULING 1 (F-U10) - the band is RETIRED, as a pre-key-change artifact` with
   `L2418: **The band 75,600..76,587 is RETIRED. Not re-derived, not kept-frozen.**`
3. **The retirement is enforced, not merely annotated** — a retired key that merely went `null` would
   still be readable and could still be cited:
   `PASS  report: the retired band key is ABSENT, not null (a direct read raises)` and
   `PASS  report: the retirement is recorded as a tombstone with is_live False`.
4. **The 30,000 floor was NOT renegotiated to make the problem go away** — this is the part that
   could have been done quietly, so I checked it directly.
   `Select-String tools/e0013_extract.py -Pattern 'SCOPE_FLOOR\s*='` → `L142: SCOPE_FLOOR = 30000`,
   and the self-test pins it: `PASS  floor: the pinned constant is still 30,000 after both branches
   ran` and `PASS  report: the scope floor is published, at 30,000, with its headroom` /
   `PASS  report: the scope floor says it is not the retired band`.
   E-0013 L2672 concurs: *"| L235-244 rules 1-2 | the 30,000 floor on the TRAIN count | **UNCHANGED**;
   the value is not renegotiable and the new count satisfies it |"*.
5. The tool reports the branch rather than deciding it (separation of duties preserved):
   `scope_floor={"applied_by": "E-0013's owner seat; this tool reports the branch, it does not decide", …}`.

**Residual uncertainty (stated, not smoothed):** retiring the band discharges *this* obligation, but
the question the band was asking — the realized yield under the new key, and whether it clears
30,000 — is **not answered**. It is E-00015's to measure, on a record that is `PENDING` and that the
S-0037 ruling put under a hold (*"E-00015 may not run until the new dedup key is implemented and the
re-derivation under F-U7 is complete"*). I did not run it, did not read the holdout, and fitted
nothing. **A retired band is not a measured one**, and this row must not be read as "the yield is
known".


## Evidence
_commands, outputs, hashes_


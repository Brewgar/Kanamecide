---
id: FND-0002
type: finding
title: "B2 Q-LABEL: the fit target's colour frame, and the label's attainable gai"
status: RESOLVED
example: false
created: 2026-09-29
target: E-0013
severity: blocking
raised_by: chief-architect (extraction; original raisers in source)
review: E-0013-h-0013-texel-fit-on-verified-e-0011-datas
resolution: "B2 Q-LABEL (colour frame + attainable gain): DISCHARGED (text); the measurement half is pre-registered to E-00014 and NOT RUN. Colour frame pinned to the side-to-move frame with a FAIL consequence for the White-frame error."
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0002

## Origin
Prose item `B2` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> Q-LABEL: the fit target's colour frame, and the label's attainable gain

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `
### B2 - Q-LABEL: the fit target's colour frame, and the label's attainable gain

**B2 sentence 1 (the colour frame - the sharp edge), verbatim per R-0019:**`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED (text); the measurement half is a named, pre-registered, NOT-RUN delegation.**
B2 has two halves and they are discharged differently. The *text* half is discharged by text; the
*measurement* half (attainable gain, `delta_star`) was what B2 itself asked to be MEASURED, so
routing it to a pre-registered train-only pass is the finding's own instruction, not an evasion.

**Commands re-run this session (2026-09-30), output in `_obs/vf/`:**

1. Discharge text present — `Select-String research/experiments/E-0013-*.md -Pattern '\*\*B2\*\*'` →
   `E-0013 L966: | **B2** | **DISCHARGED (text); measurement half PRE-REGISTERED as E-00014, NOT RUN** | ...`,
   with the residual column stating the `delta_star` / `s_d` numbers "are not in this record and
   are not in any record yet; they are E-00014's, run by another seat under HO-0015, train-only."
2. **The delegation is honest, and I checked the thing that could have made it a dodge** —
   the text half must NOT be delegated. R-0020 L576-L593 tests exactly this ("Is delegation used to
   discharge a finding that only addendum text could discharge?") and rules **HONEST**: for B2 the
   *text* half "is discharged by text (L557-L566)" and only the *measurement* half is delegated.
3. **Delegated obligation is genuinely unstarted, not silently absorbed** —
   `Select-String -Path research/experiments/E-0013-*.md -Pattern 'S-0036'` and the E-0013 addendum
   both confirm E-00014/E-00015 are not run. Independently, `python tools/e0013_extract.py --selftest`
   → `SELFTEST PASS checks=112 failed=0` (exit 0) and the S-0037 addendum L2289 records the binding
   hold: *"E-00015 may not run until the new dedup key is implemented and the re-derivation under
   F-U7 is complete. It waits."*
4. Target integrity — `_obs/vf/hb.py` → `H_body sha256 = c7ebe54c…bea7` over `22196` bytes,
   **identical to the pinned value**; the protected contract text B2 critiques is unmodified.

**Residual uncertainty (stated, not smoothed):** the *attainable gain* has never been measured.
`delta_star` and `s_d` do not exist in any record. That is the pre-registered state, not a defect,
but it does mean B2's measurement half is discharged *by delegation only* — E-00014 must still run
under HO-0015 before the margin's attainability is a fact. **E-00015 stays PENDING** and I did not
run, read, or fit anything.


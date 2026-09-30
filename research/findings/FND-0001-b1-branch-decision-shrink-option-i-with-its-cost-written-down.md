---
id: FND-0001
type: finding
title: "B1 BRANCH DECISION: **SHRINK** (option (i)), with its cost written down"
status: RESOLVED
example: false
created: 2026-09-29
target: E-0013
severity: blocking
raised_by: chief-architect (extraction; original raisers in source)
review: E-0013-h-0013-texel-fit-on-verified-e-0011-datas
resolution: "B1 BRANCH DECISION (SHRINK): discharged as a branch decision with its cost written down. Discharge text verified present at E-0013 L965 by grep this session; independent re-verification R-0022 L319-L520."
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0001

## Origin
Prose item `B1` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> BRANCH DECISION: **SHRINK** (option (i)), with its cost written down

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `
### B1 - BRANCH DECISION: **SHRINK** (option (i)), with its cost written down

**The problem, in the record's own words.** Three existing sentences are mutually`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED.** B1 is the branch decision (SHRINK, option (i)) with its cost written
down. The discharge is textual and its text is present in the target record; the run is not
required (and is forbidden) to be re-executed to confirm a *disposition*.

**Commands re-run this session (2026-09-30), with output kept in `_obs/vf/`:**

1. Discharge text present at the cited location —
   `Select-String research/experiments/E-0013-*.md -Pattern '\| \*\*B[1-7]\*\*'` →
   `E-0013 L965: | **B1** | **DISCHARGED as a BRANCH DECISION (SHRINK), cost written** | ...`
   The row states the disposition verbatim, names the three-column structure
   (Disposition / What physically happened / Residual), and records the residuals
   (H-0013 limb (b) UNANSWERED; the one-`--exe` wall DEFERRED to F-U2).
2. Independent re-verification exists and is a *different seat* —
   `Select-String research/reviews/R-0022-*.md -Pattern 're-verified'` →
   `R-0022 L319: ## 6. THE SUBSTANCE — re-verified, not accepted` and
   `L520: "Every one of R-0021's four required repairs is applied and verified, the substance
   is sound, B3/B4/B5 are all ..."` (R-0022, reviewer `adversarial-reviewer`).
3. The lifecycle flip this row's residuals hang off was independently audited with no revert —
   `Select-String research/reviews/R-0025-*.md -Pattern 'NO REVERT'` →
   `R-0025 L48: **NO REVERT IS REQUIRED. C1–C7 and C9 all hold on recomputation.**`
4. Target integrity — the protected range is untouched by this closure, so the row closes
   against the *same* contract text R-0019 critiqued:
   `_obs/vf/hb.py` (byte-level) → `H_body sha256 = c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7`
   over `H_body bytes = 22196` (lines 1..428 minus 5,6,7,10,14) — **matches the pinned value exactly.**
5. Ledger/record integrity — `python research/scripts/research.py selftest` → `Ran 47 tests ... OK` (exit 0);
   `python research/scripts/imem.py selftest` → `Ran 43 tests ... OK`, `VERSION = "2.0.0 (DEC-0012)"` (exit 0).

**Residual uncertainty (stated, not smoothed):** B1's residuals are *by design* not closed here —
H-0013 limb (b) is UNANSWERED and the `--exe` wall is DEFERRED to **F-U2** (FND-0009, which stays
OPEN as a `major` row and does not gate lint). Closing B1 discharges the *finding that a branch
decision had to be made and costed*; it does not assert that the deferred items are done.

**Note on the extractor finding (my own, filed separately as FND-0023):** the same `E-0013` file
carries **severed sentences inside the S-0037 addendum** (L2092, L2124, L2152) — the X1 defect
class recurring in a *later* addendum. That defect is real and is filed as its own OPEN blocking
row. It does **not** retract B1, because B1's disposition text (L965) is intact and is not one of
the severed lines; but it is the reason this ledger must not be read as "E-0013's addenda are
structurally clean."


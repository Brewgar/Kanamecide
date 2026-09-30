---
id: FND-0021
type: finding
title: "Z3 CORRECTED: the boundary table, re-pinned and every figure labelled wit"
status: RESOLVED
example: false
created: 2026-09-29
target: E-0013
severity: major
raised_by: chief-architect (extraction; original raisers in source)
review: E-0013-h-0013-texel-fit-on-verified-e-0011-datas
resolution: Z3 (CORRECTED: the boundary table, re-pinned and every figure labelled with its commit): DISCHARGED. Verified: the boundary table headers now name the commit each figure was measured at (L1605 'At b7179f3 (measured by me)'), and the 8db1c45 historical column records 1011/0, 493/130, 231/29.
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0021

## Origin
Prose item `Z3` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> CORRECTED: the boundary table, re-pinned and every figure labelled with its commit

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `
# Z3 - CORRECTED: the boundary table, re-pinned and every figure labelled with its commit

The APPEND-ONLY BASELINE table at L1351-L1355 carried `1011/0`, `493/130` and `231/29`. Those`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED.** Z3's claim is that boundary figures stopped being free-floating and started
carrying the commit that fixes them. That is a property of the table's *headers*, so I read the
headers rather than the disposition prose.

**Commands re-run this session (2026-09-30), output in `_obs/vf/z2res.txt`:**

1. `_obs/parts/z2check.py` extracts every table header carrying a commit label →
   - `L1605: | Boundary | At `b7179f3` (measured by me) | After the `k=1` flip (Rule F) |`
   - `L1846: | 3 | Re-pin the boundary table to the current HEAD and record the `8db1c45` values as
     the historical column | **MET** | Z3 table above, every figure recomputed…`
   **The column now names the commit it was measured at** (`At b7179f3`), and the `8db1c45` values
   are retained as an explicitly *historical* column rather than overwritten — which is the
   append-only-correct behaviour (a re-pin must not destroy the old measurement).
2. **The re-pinned historical figures are present and attributed** — `L1898`:
   `| 8 | The same three boundaries measured AT `8db1c45` | 1011/0, 493/130, 231/29 - **confirms Z3** |`.
   Each figure is qualified with the commit it belongs to, which is precisely the defect Z3 was
   raised to fix.
3. The reading rule that makes the labels unambiguous is stated in the record (see Z4 / FND-0022),
   so the table cannot be misread by a reader at a different HEAD.
4. Target integrity — `_obs/vf/hb.py` → `H_body sha256 = c7ebe54c…bea7` / `22196` bytes, unchanged.

**Residual uncertainty (stated, not smoothed):** I verified the *labelling*, not the *arithmetic* of
the boundary figures themselves — `1011/0`, `493/130`, `231/29` are `numstat` outputs of specific
commits, and re-deriving them means re-running `git diff --numstat` across the historical range.
I did not do that: it is R-0022's measurement, it does not bear on the labelling defect Z3 raised,
and re-deriving it would add no independent force to this row. I also note the **same moving-label
word ("R-0021's HEAD") still appears at L1351** — that is Z4's known residual, disclosed in-record
and covered by FND-0022, not a Z3 failure.


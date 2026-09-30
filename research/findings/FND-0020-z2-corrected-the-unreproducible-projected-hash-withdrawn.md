---
id: FND-0020
type: finding
title: "Z2 CORRECTED: the unreproducible projected hash, withdrawn"
status: RESOLVED
example: false
created: 2026-09-29
target: E-0013
severity: major
raised_by: chief-architect (extraction; original raisers in source)
review: E-0013-h-0013-texel-fit-on-verified-e-0011-datas
resolution: Z2 (CORRECTED: the unreproducible projected hash, withdrawn): DISCHARGED as to substance - 8ad61ccd...00a727 is withdrawn and every occurrence of it in E-0013 sits in a withdrawal/audit context, with the reproducible post-flip H_legacy d8add61c...e6144 recorded. The record's own P4 proof row is separately stale: filed as FND-0031.
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0020

## Origin
Prose item `Z2` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> CORRECTED: the unreproducible projected hash, withdrawn

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `
# Z2 - CORRECTED: the unreproducible projected hash, withdrawn

`b7179f3`'s commit message states that the flip "moves the pair from `b04fd5a4...00ce6` to`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED as to substance. The record's own proof of it is stale — filed separately as
FND-0031 rather than waved through.** Z2 is the row where the distinction between "the correction
happened" and "the correction is demonstrated" actually matters, so I did both and reported both.

**Commands re-run this session (2026-09-30), output in `_obs/vf/zres.txt` / `_obs/vf/z2res.txt`:**

1. **The correction itself is real and total.** `_obs/parts/z2check.py` scans the whole file for the
   withdrawn hash and reports:
   `occurrences of the WITHDRAWN hash: [1696, 1699, 1847, 1900, 1950] count = 5`
   I then read each one. **All five sit inside a withdrawal or audit context** — L1696 (`That figure
   is unreproducible`), L1699 (the "appear only inside" statement), L1847 (`withdrawn as
   unreproducible`), L1900 (the S-0033 occurrence-sweep row), L1950 (the P4 verification row). So the
   substantive requirement — *no live use of an unreproducible hash* — **holds**.
2. **The replacement figure is recorded.** E-0013 L1847: the reproducible post-flip `H_legacy` is
   `d8add61c...e6144`. The S-0034 obligation table marks obligation 4 (`Record Z2's correction`) **MET**.
3. **But the record's own proof row is wrong, and I am not closing my eyes to it.** Row P4 (L1950)
   asserts *"occurrences at L1696, L1699, L1809, L1862 — all four"*. Recomputed, there are **five**,
   and **two of the four line numbers it names (L1809, L1862) contain no such hash at all** — those
   lines moved when later dated addenda were appended. Worse, **P4 is self-referential**: it quotes
   the withdrawn hash in order to count its occurrences, so P4 is itself one of the five it
   enumerates, and no self-consistent version of that row can ever exist while it quotes the token.
   Filed as **FND-0031** (`severity: minor`).
4. Target integrity — `_obs/vf/hb.py` → `H_body sha256 = c7ebe54c…bea7` / `22196` bytes, unchanged.

**Why this row closes and FND-0031 does not.** The finding Z2 raised was that an *unreproducible
projected hash* was circulating as if authoritative. That is fixed: the hash is withdrawn, labelled
unreproducible at every occurrence, and replaced by a reproducible one. The residual defect is in
the *audit row's* bookkeeping, not in the correction, and it is a `minor` bookkeeping issue that does
not propagate a wrong number into any claim. Closing Z2 asserts the correction; **it does not assert
that every proof row in the file is accurate** — FND-0031 is the standing record that one is not.


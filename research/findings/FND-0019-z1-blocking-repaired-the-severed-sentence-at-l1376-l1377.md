---
id: FND-0019
type: finding
title: "Z1 BLOCKING, REPAIRED: the severed sentence at L1376-L1377"
status: RESOLVED
example: false
created: 2026-09-29
target: E-0013
severity: major
raised_by: chief-architect (extraction; original raisers in source)
review: E-0013-h-0013-texel-fit-on-verified-e-0011-datas
resolution: Z1 (BLOCKING, REPAIRED: the severed sentence at L1376-L1377): DISCHARGED. Verified mechanically this session - L1376 ends 'are NOT' and L1377 opens 'shifted.', one contiguous sentence, with zero lines starting with the orphan head.
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0019

## Origin
Prose item `Z1` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> BLOCKING, REPAIRED: the severed sentence at L1376-L1377

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `
# Z1 - BLOCKING, REPAIRED: the severed sentence at L1376-L1377

`b7179f3` replaced L1377-L1386 to qualify two over-broad "have been re-derived" claims, and`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED.** This row has a crisp, falsifiable, two-line claim, so I tested exactly that
claim rather than the disposition prose around it.

**Commands re-run this session (2026-09-30), output in `_obs/vf/zres.txt`:**

1. `_obs/parts/zcheck.py` reads the two lines directly and prints their edges:
   - `Z1 L1376 tail : ...`, are a different numbering and are NOT`
   - `Z1 L1377 head : shifted. The cross-references written *b...`
   - `Z1 CONTIGUOUS : L1376 ends 'are NOT' -> True | L1377 opens 'shifted.' -> True`
   **Both halves of the record's own P3 criterion are TRUE**, so the sentence at L1376-L1377 is one
   contiguous sentence again. The severed head `shifted.` is back where the sentence needs it.
2. The orphan cannot survive anywhere else in the file — the same script that found the X4 orphan
   (`_obs/parts/x45.py`) reports **zero** lines beginning `move it, and per R-0020`, i.e. the X1-class
   orphan-head pattern is absent from the file.
3. Target integrity — `_obs/vf/hb.py` → `H_body sha256 = c7ebe54c…bea7` over `22196` bytes,
   **unchanged**: the repair sits at L1376-L1377, far below the protected range L1-L428.

**Residual uncertainty (stated, not smoothed):** the record's own audit also asserts a *method*
claim — that the word was recovered from the pre-edit blob rather than from memory
(`git show b7179f3~1:<path>` L1377), and that the diff is 1 hunk / 1 removed / 1 added line. I
verified the **end state** (contiguity) directly; I did **not** re-derive the word's provenance from
the historical blob, because that is R-0022/S-0032's provenance chain and re-deriving it would mean
trusting a reconstruction rather than the current file. The end state is what the finding asked for.


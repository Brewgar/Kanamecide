---
id: FND-0006
type: finding
title: "B6 The yield: the "measured" label was applied to a number measured for a"
status: RESOLVED
example: false
created: 2026-09-29
target: E-0013
severity: blocking
raised_by: chief-architect (extraction; original raisers in source)
review: E-0013-h-0013-texel-fit-on-verified-e-0011-datas
resolution: B6 (the yield: a measured label was applied to a number measured for a different filter): DISCHARGED (rule text); 76,593 relabelled a PER-PLY count for a DIFFERENT (bare) predicate, the ~997 projection is withdrawn, and the honest band 75,600-76,587 is recorded as a BAND.
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0006

## Origin
Prose item `B6` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> The yield: the "measured" label was applied to a number measured for a different filter

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `
### B6 - The yield: the "measured" label was applied to a number measured for a different filter

**B6 sentence 1 (the count pass rule and the relabelling; the count itself is BUCKET 2 -`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED (rule text); the COUNT itself is pre-registered to E-00015 and NOT RUN.**
B6 is the row where the defect was an *epistemic* one: a number measured under one filter was
labelled as if measured under another. The discharge is that the label is corrected, the false
precision is withdrawn, and an honest BAND replaces the point estimate.

**Commands re-run this session (2026-09-30), output in `_obs/vf/`:**

1. **The false label is corrected in terms, in the record** —
   `Select-String research/experiments/E-0013-*.md -Pattern '76,593'` → `E-0013 L866`:
   the "'measured, not assumed' phrase" is **superseded**, because *"76,593 is measured for the BARE
   predicate over the …"* — i.e. the record now says which filter the number belongs to, which is
   exactly the correction B6 demanded.
2. **The projection is withdrawn, not quietly kept** — `E-0013 L868-L871`: the `~997` figure is
   labelled `UNMEASURED PREDICTION`, and the honest band *"recorded as a BAND and not as a point"* is
   `75,600 <= realized usable yield <= 76,587`, with its upper bound *"76,593 minus at most 6
   positions from the single degenerate game and zero crash games"* and its lower bound *"76,593 minus
   ~997 projected cross-game FEN duplicates, from the measured …"*.
3. **I recomputed the band's arithmetic myself** — `_obs/parts/b56math.py` →
   `76,593 - 76,587 = 6` ✔ (the stated degenerate-game bound);
   `1.302% of 76,593 = 997` ✔ (the stated projection, from the measured `1705/130930` rate);
   `75,600 / 30,000 = 2.52x` ✔ (the record's "2.5x headroom").
   **All three reproduce.** The band is also *conservative*: `76,593 - 997 = 75,596`, so the printed
   lower bound 75,600 is 4 positions tighter than the projection — rounding in the safe direction.
4. **The scope-changing consequence of the refuted ~27k figure is named, not dropped** —
   `E-0013 L880`: *"27,000 sits BELOW"* the 30,000 floor, and I confirmed the comparison is real:
   `27,000 < 30,000 -> True`. Had 27k been accepted it would have armed the fallback scope.
5. **The count is routed, pre-registered and still unrun** — `E-0013 L844` records the band against
   the 30,000 floor; the count itself is E-00015's, count-only, before any fitter. I did not run it.
6. Target integrity — `_obs/vf/hb.py` → `H_body sha256 = c7ebe54c…bea7` / `22196` bytes, unchanged.

**Residual uncertainty (stated, not smoothed):** the realized count **does not exist yet**. The
`~997` figure is a projection from a 1.302% exact-FEN rate, and the S-0037 ruling (L2326-L2334) later
found that projection **does not carry over** to the new normalized-FEN key, because clock-only
duplicates are invisible to an exact-FEN rate — so this band is now **superseded pending
re-derivation** and the band was subsequently **RETIRED** outright by the S-0039 owner ruling
(F-U10). What is discharged here is the *rule* ("a measured label may not be applied to a number
measured for a different filter"), not the yield. **E-00015 stays PENDING**; I read no holdout, read
no label field, and fitted nothing.


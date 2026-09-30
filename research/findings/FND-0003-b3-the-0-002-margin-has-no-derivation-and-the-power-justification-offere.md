---
id: FND-0003
type: finding
title: "B3 The 0.002 margin has no derivation, and the power justification offere"
status: RESOLVED
example: false
created: 2026-09-29
target: E-0013
severity: blocking
raised_by: chief-architect (extraction; original raisers in source)
review: E-0013-h-0013-texel-fit-on-verified-e-0011-datas
resolution: "B3 (0.002 margin underived, power justification false): DISCHARGED (text), including the contingency decided in advance. R-0020's PARTIALLY-DISCHARGED condition was verified satisfied this session: the X-1/X-2/X-3 table now sits directly under B3 sentence 3 at E-0013 L677-L692."
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0003

## Origin
Prose item `B3` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> The 0.002 margin has no derivation, and the power justification offered for it is false

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `
### B3 - The 0.002 margin has no derivation, and the power justification offered for it is false

**B3 sentence 1 (effective N, and what the margin is actually conditional on), verbatim`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED (text), including the contingency decided in advance.**
This is the row where "trust the addendum" would have been the wrong method: R-0020 ruled B3
**PARTIALLY DISCHARGED**, not discharged. I therefore verified R-0020's own stated condition
instead of reading the disposition table.

**Why B3 was only partial, and what discharged it.** R-0020 L383-L405 found **"B3 sentence 3
announces a table that is not there"**: the X-1/X-2/X-3 contingency table — the thing that must not
be chosen after `s_d_inner` is known — sat ~340 lines away from the sentence announcing it, under
the B4 region. A table that has drifted away from its announcement is no longer pre-registration.

**Commands re-run this session (2026-09-30), output in `_obs/vf/`:**

1. The condition R-0020 set, checked directly —
   `Select-String research/experiments/E-0013-*.md -Pattern 'Three mutually'` →
   `E-0013 L678: part that must not be chosen after 's_d_inner' is known. Three mutually exclusive`.
   I then read the contiguous block: **L677-L692** is the announcement (L677 `**B3 sentence 3 - THE
   CONTINGENCY, DECIDED NOW, BEFORE ANY NUMBER EXISTS.**`) immediately followed by the
   `Contingency table … DECIDED HERE, 2026-09-26, BEFORE E-00014 RUNS` block and branch
   **(X-1) `s_d_inner <= 0.0101` AND `delta_star` measurable** (L687-L691). **The table is now
   adjacent to its announcement. R-0020's condition is SATISFIED.**
2. R-0020's condition named exactly this, and its closure clause named the outcome —
   `Select-String research/reviews/R-0020-*.md -Pattern 'B3|B4'` →
   `L777: "Every seam in the X1 list is joined, the X-1/X-2/X-3 table sits under B3 sentence 3, the …"`
   and `L784: "… B3 DISCHARGED, B4 DISCHARGED, B5 DISCHARGED, B6 DISCHARGED, B7 …"`.
   I am not accepting L784 on its word — item 1 above is the independent check, and L784 is the
   standard it is measured against.
3. The severity of the finding itself is discharged: the false power justification is superseded.
   `Select-String research/experiments/E-0013-*.md -Pattern 'LOSS_MARGIN'` →
   `L661: '> LOSS_MARGIN = 0.002 is decidable at the planned N **iff 's_d…'` — the decidability
   CONDITION is now stated, which is what "no derivation" demanded.
4. The severed `LOSS_MARGIN` rule that R-0020 listed as seam 5 is now ONE sentence —
   `Select-String … -Pattern 'LOSS_MARGIN'` → `L1173: '| 5 | L588 '...over the' | L1011-L1020 |
   L639-L649 | **the LOSS_MARGIN rule is one sentence** |'` (the record's own repair table).
5. Target integrity — `_obs/vf/hb.py` → `H_body sha256 = c7ebe54c…bea7` / `22196` bytes, unchanged.

**Residual uncertainty (stated, not smoothed):** the contingency is decided but its INPUT
(`s_d_inner`, `delta_star`) is E-00014's and does not exist yet. Branch X-2 routes to **F-U3**
(FND-0010, `major`, legitimately OPEN). Closing B3 asserts the branches were fixed *in advance* —
it does not assert which branch will fire. **E-00015 stays PENDING**; I read no holdout and fitted
nothing.


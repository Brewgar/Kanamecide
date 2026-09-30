---
id: FND-0028
type: finding
title: "F-U12 Route the new corpus limitation into Sample Validity"
status: OPEN
example: false
created: 2026-09-30
severity: major
target: E-0013
raised_by: researcher-architect (S-0036..S-0040 F-U family)
review: E-0013
source_key: F-U12
resolution: 
resolved_by: 
verified_by: 
---

# FND-0028

## Finding

## Origin
Prose item `F-U12` extracted from the E-0013 F-U7..F-U13 obligation table, which carries the items recorded across sessions S-0036..S-0040.

## Finding
The obligation as stated in E-0013's own table. The source record is the authority; a verifier closes this row only with commands, outputs and hashes.

## Target
- Record: E-0013#F-U12

## Evidence
- Extracted by the verification-auditor's idempotent migration (`_obs/parts/extract_fu.py`), which skips any key already present as a `source_key:` in research/findings/.

## Resolution (fill when closing)
- ...

## Addendum 2026-09-30 — verification-auditor (Gate 3 seat) — **NOT DISCHARGED; row stays OPEN**

**This row is NOT closed.** The limitation it asks to be routed into Sample Validity has been
*named* in E-0013's addendum but has **not** been carried into the `## Sample Validity` section,
and no record constrains any claim on it. Naming a bias is not the same as routing it.

**What the finding asks.** The low-`game_id` survivor bias (E-0013 section 3.2) is a named
limitation of the dataset and must appear in E-0013's Sample Validity and constrain every claim the
fit licenses. (E-0013 F-U12 table row, L2225.)

**The bias itself is real, and I confirmed the record is right about it** —
`Select-String research/experiments/E-0013-*.md -Pattern 'biased toward'` →
`E-0013 L2153-L2159`: *"A position deduplicated away is a datum that no longer exists … The survivor
rule (first occurrence in `(game_id, ply_index)` order) means the surviving copy is the one from the
lowest-numbered game, so the corpus is now **biased toward low-numbered games** in exactly the regions
where collisions occur. That bias is a **new, named limitation** of the dataset and must be carried
into E-0013's Sample Validity …"*.
I also confirmed the mechanism is unchanged rather than silently altered: the self-test asserts
*"the survivor rule is UNCHANGED (first occurrence in (game_id, ply))"* — PASS. So the bias is a
consequence of a *deliberately preserved* rule, and it will persist until that rule is revisited.

**Why it is not discharged — what I checked and did not find.**

1. `Select-String research/experiments/E-0013-*.md -Pattern 'Sample Validity'` in the post-S-0037
   region returns only the L2671 row: *"| L169-171 Sample Validity | dedup key normalization |
   **STILL CORRECT**, and now load-bearing twice over |"* — a re-affirmation of the **dedup-key**
   clause. There is **no** entry anywhere in the addenda recording the low-`game_id` survivor bias
   inside Sample Validity, and **no** clause constraining the claims the fit licenses.
2. The obligation is still listed as outstanding in E-0013's own F-U table (L2225), i.e. the owning
   seat has not marked it done.
3. The most recent implementation session did not do it —
   `Select-String research/sessions/S-0040-*.md -Pattern 'F-U12|Sample Validity|bias'` returns no
   completion claim for F-U12 (only the binding `L74: Did NOT read the holdout, fit anything …`).

**Exactly what is missing to discharge this row.**
(a) an entry in E-0013's `## Sample Validity` naming the low-`game_id` survivor bias as a dataset
    limitation (append-only: a dated addendum, never an in-place edit of the protected range);
(b) an explicit constraint clause stating how the bias bounds every claim a fit may license;
(c) a decision on whether the survivor rule stays as-is (in which case the bias is permanent and
    must be priced into the claims) or is revisited — currently the self-test pins it as UNCHANGED.

**Residual uncertainty, stated plainly:** I did not and could not assess how large the bias is in
positions-per-`game_id` terms, because quantifying it requires the re-derived corpus and E-00014's
pass — both of which are forbidden to me here. **I did not read the holdout, read any label field,
or fit anything, and E-00014/E-00015 stay PENDING.**


## Evidence
_commands, outputs, hashes_


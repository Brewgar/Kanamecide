---
id: HO-0017
type: handoff
from: researcher-architect
to: verification-auditor
work_item: W-0003
status: REQUESTED
title: "Independently verify the E-0013 L5-only lifecycle flip (R-0024 Q1-Q8)"
artifacts: ["research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "research/reviews/R-0024-confirmation-of-the-contract-repair-and-the-flip-authorisation-part-6-is-unsatisfiable-as-written-and-is-re-specified.md", "research/experiments/E-00014-e-0014-train-only-feasibility-pass-for-e-0013-delta-star-and-s-d-inner-measurement-not-training.md", "research/experiments/E-00015-e-0015-count-only-realized-usable-quiet-yield-pass-for-e-0013-measurement-not-training.md"]
commands: ["git show 6a6eb0a --numstat -- research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "git show 6a6eb0a -U0 -- research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "git diff --numstat 4478c3a..6a6eb0a -- research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "python research/scripts/research.py validate"]
acceptance: "Q1-Q8 in R-0024's Ruling 4 are recomputed from the repository, not read from the author's addendum, and each is given a verdict. Recompute H_body and H_legacy on BOTH the ce845c5 blob and the post-flip file, splitting on 0x0A only and deleting lines {5,6,7,10,14} BY LINE NUMBER. H_body MUST read 22,196 bytes, not 22,270: 22,270 would mean L5 was edited outside the five-field exclusion. git show 6a6eb0a --numstat must read exactly 1 1; git show 6a6eb0a -U0 must show exactly one @@ -5 +5 @@ hunk whose added line is exactly 'status: RUNNING'; all 13 remaining 'status: PENDING' occurrences must be byte-identical to f86801a; H_legacy must read d8add61c...e6144 over 22,270 bytes; 4478c3a..6a6eb0a must read 1441/1; git diff --check must be empty; and no file other than E-0013 may appear in 6a6eb0a. Write a review of kind: verification, verified_by must NOT be researcher-architect. If any of Q1-Q6 fails, say so plainly: the flip is reversed by the same line-anchored procedure, E-0013 returns to status: PENDING, and the failure is recorded in a dated addendum naming the clause that failed. Do NOT proceed to any build, fit, extraction, counting, feasibility pass or SPRT generation, and do NOT read the holdout: no seat may do so while any of Q1-Q6 is unverified."
example: false
created: 2026-09-27
closed: null
---

# HO-0017 — Independently verify the E-0013 L5-only lifecycle flip (R-0024 Q1–Q8)

> The ONLY way to ask another agent to do something. Prose requests ("someone should
> verify this") are not handoffs and will be ignored. Receiver appends `## Response`
> and `## Verification`; the handoff may be edited while `status: REQUESTED|ACCEPTED`
> and is frozen once `DONE|REJECTED|WITHDRAWN`.

## Request

**E-0013 was flipped `PENDING` → `RUNNING` on 2026-09-27 in commit `6a6eb0a`, by the owner
seat, under R-0024's authorisation. I am the seat that made the flip, so I cannot verify
it.** SYSTEM.md §1 forbids the owner verifying its own proposal; R-0024 applied the same
rule to itself; and **a condition cannot be discharged by the seat that performed the act.**

**R-0024's Q1–Q8 are binding on you and on no one else. I have written no verdict on any of
them.** What follows is the author's account of what was done — evidence about the act, and
**not** the verification of it. Recompute everything from the repository.

The flip was one line: L5 of E-0013, `status: PENDING` → `status: RUNNING`, 15 bytes to 15
bytes, committed alone in `6a6eb0a` (1 file, 1 insertion, 1 deletion). It is authorised by
R-0024's **pre-condition P1–P5**, not by any future audit. R-0024 separately ruled
R-0023's condition part 6 unsatisfiable as written and re-specified it.

## Artifacts To Read (paths)
- `research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`
  — the flipped record. Read its **S-0034 addendum** for the author's claim, and read the
  **front matter and the R-0023 contract clause** yourself rather than trusting either.
- `research/reviews/R-0024-confirmation-of-the-contract-repair-and-the-flip-authorisation-part-6-is-unsatisfiable-as-written-and-is-re-specified.md`
  — Ruling 4, steps 1–6, and the Q1–Q8 table. **This defines the assertions, not their outcome.**
- E-00014 / E-00015 — the two PENDING measurement sub-contracts. **Neither ran. Confirm that yourself.**

## Commands To Run
```powershell
$e13 = "research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md"

# Q2, Q3, Q8 - the commit must be one file, one line, L5
git show 6a6eb0a --numstat -- $e13
git show 6a6eb0a -U0 -- $e13
git show 6a6eb0a --stat
git diff --check 6a6eb0a^ 6a6eb0a

# Q4 - the 13 other occurrences must be byte-identical to the pre-flip commit
git show f86801a:$e13 > $env:TEMP\e13_pre.md
git show 6a6eb0a:$e13 > $env:TEMP\e13_post.md
# then locate every 'status: PENDING' in both and diff the 13 non-L5 lines

# Q1, Q5 - recompute from raw bytes; split on 0x0A only; drop {5,6,7,10,14} BY LINE NUMBER
git cat-file blob ce845c5:$e13 > $env:TEMP\e13_base.md
# H_body    = sha256 of lines 1..428 minus lines 5,6,7,10,14, each re-terminated with one 0x0A
#            expect c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7 / 22196 bytes, BOTH sides
# H_legacy  = sha256 of lines 1..428, each re-terminated with one 0x0A
#            pre-flip expect b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6 / 22270
#            post-flip expect d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144 / 22270

# Q6 - the boundary, file-scoped
git diff --numstat 4478c3a..6a6eb0a -- $e13      # expect 1441 / 1
git diff --numstat 4478c3a..f86801a -- $e13     # the pre-flip baseline, for contrast: 1440 / 0

python research/scripts/research.py validate
```

**Q1's byte count is the load-bearing one.** If the post-flip `H_body` reads **22,270**
rather than **22,196**, then L5 was edited *outside* the five-field exclusion and the
contract was violated. `H_body` is the only quantity in that record that is invariant under
exactly the legal transitions and sensitive to exactly the illegal ones.

**On Q6, know what you are checking before you call it a failure.** The author's brief
anticipated "deletions remain 0". The measured value is **1441 / 1**. Replacing L5 *is* one
deletion at that boundary, because L5 is itself inside the compared range; no line-anchored
edit of L5 could yield 0 deletions. R-0024's Q6 itself states **1441 / 1**. Judge the claim
against the contract and the ruling, not against the tidier number.

## Acceptance Criteria (what makes this DONE)

1. **Q1–Q8 each carry a verdict**, each backed by a command you ran and output you kept.
   Nothing is accepted "per the addendum".
2. A review record with `kind: verification`, whose `verified_by` is **not**
   `researcher-architect` (Gate 3; `validate` rejects `verified_by == owner`).
3. Hashes **recomputed, not copied**. State any figure you could not reproduce, and why —
   R-0024 did exactly that on two of its own items and that is the standard, not a failure.
4. **If any of Q1–Q6 fails: say so plainly and do not soften it.** The flip is then reversed
   by the same line-anchored procedure (L5 only, `RUNNING` → `PENDING`), E-0013 returns to
   `status: PENDING`, and the failure is recorded in a dated addendum **naming the clause
   that failed**. A flip that has not been audited may not be relied on, but it is not
   thereby unauthorised — do not treat a failure as grounds to proceed.
5. **Do not proceed** to the build, the extractor, the trainer or the parameter-table
   evaluator, and **do not read the holdout**, while any of Q1–Q6 is unverified.

## Response (receiver, append-only)
- 2026-09-27 — (role) — ...

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: ...

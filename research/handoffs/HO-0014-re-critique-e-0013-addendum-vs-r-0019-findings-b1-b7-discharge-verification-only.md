---
id: HO-0014
type: handoff
from: researcher-architect
to: adversarial-reviewer
work_item: null
status: REQUESTED
title: "Re-critique E-0013 addendum vs R-0019 findings B1-B7 (discharge verification only)"
artifacts: ["research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "research/reviews/R-0019-e-0013-pre-registration-critique-h-0013-texel-fit-contract-ho-0013-six-question-ruling.md", "research/experiments/E-00014-e-0014-train-only-feasibility-pass-for-e-0013-delta-star-and-s-d-inner-measurement-not-training.md", "research/experiments/E-00015-e-0015-count-only-realized-usable-quiet-yield-pass-for-e-0013-measurement-not-training.md", "research/handoffs/HO-0013-critique-e-0013-pre-registration-h-0013-texel-fit-contract-before-any-running.md", "research/questions/Q-0006-self-play-data-pipeline.md", "research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md", "research/experiments/E-0010-ee-val-tapered-hand-tuned-evaluation-term-by-term-self-play-elo-attribution.md", "tools/e0012_sprt.py", "tools/e0011_check.py", "src/eval.cpp", "src/eval.h", "src/main.cpp"]
commands: ["git --no-pager diff --numstat HEAD -- research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "python research/scripts/research.py validate"]
acceptance: "a new review record (CLI-assigned id) that, for EACH of B1-B7 and for the F1-F12 freeze-audit gap, rules DISCHARGED / PARTIALLY DISCHARGED / NOT DISCHARGED with cited evidence, and rules separately on the three integrity properties: (i) the original pre-addendum E-0013 text is unaltered, (ii) the BUCKET-3 decision removed the unexecutable mandate rather than re-pointing it, and (iii) nothing was measured, fitted, counted or run. E-0013 may leave PENDING only on a ruling that every finding is DISCHARGED or honestly converted."
example: false
created: 2026-09-26
closed: null
---

# HO-0014 - Re-critique E-0013 addendum vs R-0019 findings B1-B7 (discharge verification only)

> The ONLY way to ask another agent to do something. Prose requests ("someone should
> verify this") are not handoffs and will be ignored. Receiver appends `## Response`
> and `## Verification`; the handoff may be edited while `status: REQUESTED|ACCEPTED`
> and is frozen once `DONE|REJECTED|WITHDRAWN`.

## Request

E-0013 has received a single dated, pure-additions addendum (2026-09-26) in response to
your R-0019. **Your scope is DISCHARGE VERIFICATION ONLY.** You are not being asked
whether you like the design, and you are not being asked to re-open any ruling you
already made.

**What you are checking, and nothing else:**

1. **For each of B1, B2, B3, B4, B5, B6, B7:** is the finding now closed, or honestly
   converted into something else? A finding counts as closed only if the record now
   contains text that discharges it. A finding counts as "honestly converted" only if it
   was converted into a NAMED, OWNED, DATED obligation and the addendum says plainly
   that it is not discharged. **Anything else - a finding quietly narrowed, a threshold
   quietly widened, a measurement quietly promised without an owner - is a
   NOT-DISCHARGED ruling.** Say so where you find it.
2. **The freeze-audit gap (R-0019's F1-F12):** every one is either closed with a value or
   closed with an explicit "derived from <pinned input>" pointer. Check each of the
   twelve individually.
3. **The three integrity properties**, ruled separately and explicitly:
   - **(i) ORIGINAL TEXT INTACT.** The pre-addendum E-0013 text must be unaltered -
     append-only, no rewrite, no deletion, supersession by quotation and name only. The
     `git diff --numstat` above should show additions and ZERO deletions; verify it
     yourself rather than trusting the number I report.
   - **(ii) THE BUCKET-3 DECISION REMOVED THE UNEXECUTABLE MANDATE.** R-0019's B1 held
     that the record mandated a Tier-S result it had also prohibited the means of
     obtaining. The addendum takes a branch decision on that. Your check is narrow and
     mechanical: **does the decision remove the unexecutable mandate, or does it merely
     re-point it at a different instrument?** In particular, check that the old sentence
     requiring an "A != B by handshake-hash dump" is not still standing anywhere beside a
     different decision, and that whatever replaced it is ACHIEVABLE with the surface
     that actually exists. **You are not asked whether the chosen branch is the better
     engineering choice** - that call was the owner's to make and its cost is written into
     the record. You are asked whether that branch actually discharges the defect the way

**What you are NOT being asked to do, and should decline to do:**

- Do not re-litigate design taste. R-0019's rulings (P1 adopted / P0 deferred, Q-LABEL
  result-only, Q-FIT deterministic L-BFGS with SPSA withdrawn, Q-SCOPE all-terms with
  KING PSTs frozen, Q-SUITE independent suite with the substitution path closed,
  per-game cap NONE) are SETTLED. If the addendum implements them faithfully, that is
  what you check; if you think one of them was the wrong call, that is out of scope here
  and belongs in a new record, not in this re-critique.
- Do not run any training, fitting, extraction, counting, feasibility pass, or SPRT game
  generation. Read-only inspection and arithmetic are in scope; measurement is not.
- Do not edit E-0013, E-00014, E-00015, or any other record. The review lives in
  `reviews/`.
- Do not flip E-0013 to RUNNING, do not open or close HO-0005/W-0003, and do not change
  any H-#### status.

**You are not being told the answer.** This handoff does not assert that the addendum
discharges anything. It asserts only what was written and where. If the discharge is
partial, silent, or cosmetic, the correct verdict is NOT DISCHARGED and the addendum
stays unlanded. An honest NOT-CLEAN here costs the project one more cycle; a false CLEAN
costs it the experiment.

## Artifacts To Read (paths)

- `research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`
  - the original contract (UNCHANGED) and the dated addendum (from the
  `## Addendum: R-0019 discharge ...` heading onward). Read both; the addendum's claims
  are claims about the original.
- `research/reviews/R-0019-e-0013-pre-registration-critique-h-0013-texel-fit-contract-ho-0013-six-question-ruling.md`
  - your own prior ruling: B1-B7 verbatim, the F1-F12 table, DN1-DN10, and the arithmetic
  the pass already contains (yield band, the `s_d <= 0.0101` derivation).
- `research/experiments/E-00014-*.md` and `research/experiments/E-00015-*.md` - the two
  PENDING measurement sub-contracts; confirm each is PENDING, unrun and owned, and that
  the addendum does not claim their outputs.
- `research/handoffs/HO-0013-*.md` - the request that produced R-0019 (read-only).
- `research/questions/Q-0006-self-play-data-pipeline.md` - readiness gate 7, quoted into
  the addendum by B7.
- `research/experiments/E-0011-*.md` (N1's consequence ladder, the mis-citation B5 records
  a correction note about) and `research/experiments/E-0010-*.md:341-344` (the ladder and
  its attribution) - to check the backwards-citation claim arithmetically. **Neither is
  edited by this work and neither may be edited by you.**
- `tools/e0012_sprt.py` (lines 293-345, 471-490) and `tools/e0011_check.py` (lines

## Commands To Run

```powershell
cd c:\Users\tahae\Kanamecide
git --no-pager diff --numstat HEAD -- 'research/experiments/E-0013*'
# expect: additions, and 0 deletions. Zero deletions is the append-only proof.
git --no-pager log --oneline -3
python research/scripts/research.py validate
python research/scripts/research.py experiments
# E-0013 must read PENDING; E-00014 and E-00015 must read PENDING.
python research/scripts/research.py hypotheses
# confirm no H-#### status changed as a side effect of this work.
```

**Shell caveat in this environment, stated so it does not waste your time:** `run_commands`
routinely reports `Command exited with code 1` on commands that plainly succeeded, and
PowerShell's `>` writes UTF-16. Redirect with `| Out-File -Encoding utf8 <file>` and read
the FILE; treat the file as authoritative over the reported status, and say so if they
disagree.

**Read-only arithmetic you may want to redo yourself rather than inherit:** the yield band
(76,593; 1705/130930 = 1.302 %; 75,600-76,587); the power condition
(0.002 / (2.8016 / sqrt(200)) = 0.0101); the salt distance
(|20260926 - 20260924| x 1,000,003 = 2,000,006 > 1,999); the E-0010 attribution deltas
(k4-k3 = -3.7, k6-k5 = -11.5); and the fitted-parameter count against the ">= 500
positions/parameter" standard.

## Acceptance Criteria (what makes this DONE)

1. A new review record (CLI-assigned id, `kind: critique`, `target: E-0013`) that rules
   **each of B1, B2, B3, B4, B5, B6, B7** individually: DISCHARGED / PARTIALLY
   DISCHARGED / NOT DISCHARGED, with cited evidence for each.
2. A ruling on the **F1-F12** freeze-audit gap, item by item (twelve items).
3. Three separate explicit rulings: (i) original text intact; (ii) the BUCKET-3 decision
   removed the unexecutable mandate rather than re-pointing it; (iii) nothing was
   measured, fitted, counted or run, and no status was flipped.
4. A ruling on the **BUCKET-2 conversion** (E-00014, E-00015): honest delegation, or not.
5. A DN1-DN10 disposition check: no nit silently dropped.
6. An explicit statement of what E-0013's status should be next, and on what condition it
   may leave PENDING.
7. If any finding is NOT DISCHARGED, the exact missing sentence, so the next cycle is
   mechanical rather than interpretive.

**Explicitly NOT an acceptance criterion:** agreeing with the branch decision, agreeing
with the pinned `SUITE_TOLERANCE = 0.02`, or finding the design attractive. A reviewer
who likes this addendum and a reviewer who does not should both be able to sign it.

## Response (receiver, append-only)
- 2026-09-26 - (role) - ...

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: ...

  371-398) - to check the B1 mechanism and the B6 per-ply-count claim against the actual
  surface. **Cited read-only; no seat may edit them.**
- `src/eval.cpp` (`eval_init` 174-234; the `stage>=6` tempo line at 356), `src/eval.h`
  (the `EvalCoeffs` struct), `src/main.cpp` (103-114 UCI options, 124-147 the `setoption`
  parser) - to check the B1 mechanism is achievable and the `S* = 6` claim.
- `research/work/W-0001-*.md` and `research/reviews/R-0017-*.md` - the VERIFIED records
  the B5 correction note deliberately does not touch.

     it claims to.
   - **(iii) NOTHING WAS MEASURED, FITTED, COUNTED OR RUN.** No training, no fitting, no
     extraction, no counting, no feasibility pass, no SPRT game generation. No holdout
     read. E-0013 must still be `status: PENDING`; no H-#### status may have changed;
     no CLOSED/VERIFIED record may have been edited.
4. **The BUCKET-2 conversion, specifically:** the addendum delegates two MEASUREMENTS to
   two PENDING records (E-00014, E-00015). Check that the delegation is honest - that
   the addendum does not claim those numbers, does not let the holdout be read to obtain
   them, and does not use the delegation as a way to discharge a finding that only
   addendum text could have discharged. A finding discharged by "someone will measure it
   later" is NOT DISCHARGED unless the measurement is what the finding actually asked for.

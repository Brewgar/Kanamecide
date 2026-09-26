---
id: HO-0015
type: handoff
from: researcher-architect
to: systems-researcher
work_item: null
status: REQUESTED
title: "Execute E-00014: TRAIN-ONLY feasibility pass (measurement, not training)"
artifacts: ["research/experiments/E-00014-e-0014-train-only-feasibility-pass-for-e-0013-delta-star-and-s-d-inner-measurement-not-training.md", "research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "research/reviews/R-0019-e-0013-pre-registration-critique-h-0013-texel-fit-contract-ho-0013-six-question-ruling.md", "m0_audit/e0011/check_output.txt"]
commands: ["python research/scripts/research.py validate"]
acceptance: "E-00014's Results section carries every pre-registered output field (delta_star_inner, s_d_inner, and each supporting field) with the command/exit-code/hash ledger, OR an explicit abort with the triggered abort condition and its evidence. The holdout is never read. No fitted artifact for E-0013 is produced, no E-0013 status is flipped by this work, and no engine source file or tools/e0012_sprt.py is edited."
example: false
created: 2026-09-26
closed: null
---

# HO-0015 - Execute E-00014: the TRAIN-ONLY feasibility pass (MEASUREMENT, not training)

> The ONLY way to ask another agent to do something. Prose requests are not handoffs and
> will be ignored. Receiver appends `## Response` and `## Verification`.

## Request

E-00014 is filed and PENDING. It is the BUCKET-2 measurement sub-contract for R-0019's
B2 and B3: the train-only pass that measures `delta_star` (the attainable loss
improvement of the adopted optimizer over the frozen hand-tuned floor) and `s_d_inner`
(the per-game cluster SD of the paired loss difference), on an inner partition carved
from E-0013's TRAIN side.

**This is a MEASUREMENT, not a training run.** It fits coefficients on a train-side inner
partition in order to measure two quantities. It does **not** produce E-0013's fitted
artifact, does **not** read the holdout, and licenses **no** strength claim of any kind.

**The single hardest constraint, stated first because breaking it voids the pass:**

> **THE HOLDOUT IS NOT READ. NOT ONCE. NOT FOR A COUNT, NOT FOR A LABEL, NOT FOR A
> SANITY CHECK.** Holdout game ids may be touched only to assert that zero holdout game
> appears in the inner partition. Any other read of holdout content is abort condition 2:
> the pass is void, not repaired.

E-0013's split map and pre-fit commit must already exist and be hash-recorded before you
read anything. If they do not, that is abort condition 1.

Read E-00014 in full first. Its Test Method, its eight Abort Conditions and its four
decision branches are pre-registered; your job is to execute them and report, not to
choose among them. Choosing the branch is E-0013's pre-registered contingency table
(X-1 / X-2 / X-3), applied to the fields you report.

## Artifacts To Read (paths)

- `research/experiments/E-00014-*.md` - the contract. Read it in full before running.
- `research/experiments/E-0013-*.md` - the parent contract, for the predicate, the label
  construction, the fitted set, and the B3 contingency table this feeds.
- `research/reviews/R-0019-*.md` - sections B2 and B3, for what the pass must produce and
  why the quantity must come from the training side.
- `m0_audit/e0011/check_output.txt` - the terminal diagnostic (read-only), for the
  already-measured baseline figures E-00014 cites.
- `tools/e0011_check.py:371-398` - the quiet-proxy predicate and the position-dedup
  instrument, cited read-only. **Not to be edited;** if you need a different tool, write
  a new one.

## Commands To Run

```powershell
cd c:\Users\tahae\Kanamecide
python research/scripts/research.py validate
# then the counting / fitting / evaluation commands you wrote, each captured as
#   command -> exit code -> output path -> SHA-256
```

Shell caveat in this environment: `run_commands` often reports `Command exited with code 1`
on commands that succeeded, and PowerShell `>` writes UTF-16. Use
`| Out-File -Encoding utf8 <file>` and read the FILE; take every verdict from file
contents, and state the discrepancy in your response if the file and the status disagree.

## Acceptance Criteria (what makes this DONE)

1. **Every** pre-registered output field in E-00014's Metrics and Test Method is reported,
   including the supporting per-stage fields - or reported as `null` with the reason. No
   field silently omitted.
2. The command/exit-code/path/hash ledger reproduces every reported number.
3. An explicit statement that the holdout was not read, with the extractor command line
   and its input file list as evidence.
4. The four decision branches are NOT chosen by you; you report the fields and state
   which branch E-0013's pre-registered table selects, citing it.
5. Any abort is reported as an abort, with the triggered condition number and its
   evidence. An abort is a result.
6. The inner salt, inner game-id map SHA-256, optimizer name and version, Python and
   python-chess versions, seeds, iteration budget, L2 weight, clipping bound `L`, and
   the floor table's SHA-256 are all recorded.
7. Nothing outside E-00014's Results/Provenance sections is edited. No engine source, no
   `tools/e0012_sprt.py`, no `tools/e0011_check.py`, no other record.

**Explicitly NOT an acceptance criterion:** a large `delta_star`, a small `s_d_inner`, or
any verdict that flatters E-0013. The honest null is worth more than a lucky number, and
branch X-3 (the optimizer does not beat the floor) is a perfectly good outcome to report.

## Response (receiver, append-only)
- 2026-09-26 - (role) - ...

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: ...


**Specifically NOT authorised:**
- Running the holdout evaluation. That is E-0013's own run, later, under its own
  pre-registration.
- Re-running with different hyperparameters to obtain a measurable `delta_star`.
- Raising the iteration budget on non-convergence.
- Editing `tools/e0011_check.py`, `tools/e0012_sprt.py`, or any engine source file.
- Flipping E-00014 or E-0013 to RUNNING, or changing any H-#### status. E-00014's status
  is flipped by the owner seat when the pre-conditions are met, not by the executor.
- Any game generation, engine pair, or SPRT activity.

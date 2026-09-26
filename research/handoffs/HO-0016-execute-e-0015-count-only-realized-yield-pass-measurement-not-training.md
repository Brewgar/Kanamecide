---
id: HO-0016
type: handoff
from: researcher-architect
to: systems-researcher
work_item: null
status: REQUESTED
title: "Execute E-00015: count-only realized usable quiet yield pass (measurement, not training)"
artifacts: ["research/experiments/E-00015-e-0015-count-only-realized-usable-quiet-yield-pass-for-e-0013-measurement-not-training.md", "research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "research/reviews/R-0019-e-0013-pre-registration-critique-h-0013-texel-fit-contract-ho-0013-six-question-ruling.md", "m0_audit/e0011/check_output.txt", "tools/e0011_check.py"]
commands: ["python research/scripts/research.py validate"]
acceptance: "E-00015's Results section carries every pre-registered count field (count_bare_ply, count_after_crash_excl, count_after_degenerate_excl, count_usable_distinct, count_usable_distinct_train, count_usable_distinct_holdout, and the game/dedup counts) with the command/exit-code/hash ledger, OR an explicit abort with the triggered abort condition. No label is read, no fitting occurs, no filter, band, floor or split is changed after the count is seen, and the band comparison is reported as-is."
example: false
created: 2026-09-26
closed: null
---

# HO-0016 - Execute E-00015: the count-only realized-yield pass (MEASUREMENT, not training)

> The ONLY way to ask another agent to do something. Prose requests are not handoffs and
> will be ignored. Receiver appends `## Response` and `## Verification`.

## Request

E-00015 is filed and PENDING. It is the BUCKET-2 measurement sub-contract for R-0019's
B6: the count-only pass that measures E-0013's **realized usable quiet yield** under
E-0013's own filter - the number that arms or disarms the 30,000 scope floor.

**This is a COUNT, not a training run and not a fit.** It replays recorded SAN move lists
through `python-chess` and counts positions. It fits nothing, evaluates nothing, builds
nothing, and licenses no claim beyond the count.

**The two hardest constraints, stated first because breaking either voids the pass:**

> **1. NO LABEL IS READ.** The pass is label-free by construction. It must not touch `res`
> or anything derived from it, and must not compute a loss, a correlation, or a
> per-side-position label distribution. This is what makes a whole-dataset count
> acceptable here at all. Reading a label is abort condition 3.

> **2. THE FILTER, THE DEDUP ORDER, THE SPLIT, THE FLOOR AND THE BAND ARE FIXED BEFORE
> YOU SEE THE COUNT.** They are pre-registered in E-00015. If your realized
> `count_usable_distinct` lands outside the pre-registered band
> `75,600 <= count <= 76,587`, you report it as-is, name which arithmetic assumption it
> breaks, and route it. You do **not** re-run with a modified filter, you do **not** widen
> the band, and you do **not** move the 30,000 floor. A count that lands badly is a
> result, not a retry.

E-0013's split map must already exist and be hash-recorded before you run. If it does
not, that is abort condition 2.

Read E-00015 in full first. Its four decision branches and seven abort conditions are
pre-registered. Your job is to execute and report; the branch is selected by E-00015's
fixed rule applied to the counts you report, and the all-terms / reduced-scope question
belongs to E-0013, not to you.

**If branch 2 fires (TRAIN-side count below 30,000),** the reduced scope is explicitly
**NOT** the mobility/tempo subset. E-0013's B5 correction note records that E-0010:344

## Artifacts To Read (paths)

- `research/experiments/E-00015-*.md` - the contract. Read it in full before running.
- `research/experiments/E-0013-*.md` - the parent contract: the QUIET predicate spec, the
  exclusions, the split discipline, and the F9 global-before-split dedup rule.
- `research/reviews/R-0019-*.md` - section B6, and the arithmetic section that derives the
  band and identifies 76,593 as a per-ply count for a different filter.
- `m0_audit/e0011/check_output.txt` - the terminal diagnostic (read-only), the source of
  the already-measured figures E-00015 cites. Do not recompute them and do not present
  them as this pass's output.
- `tools/e0011_check.py:371-398` - the quiet-proxy predicate and the position-dedup
  instrument, cited read-only. **Not to be edited;** the checker is a VERIFIED artifact.

## Commands To Run

```powershell
cd c:\Users\tahae\Kanamecide
python research/scripts/research.py validate
# then the counting command you wrote, captured as
#   command -> exit code -> output path -> SHA-256
```

Shell caveat in this environment: `run_commands` often reports `Command exited with code 1`
on commands that succeeded, and PowerShell `>` writes UTF-16. Use
`| Out-File -Encoding utf8 <file>` and read the FILE; take every verdict from file
contents, and state the discrepancy in your response if the file and the status disagree.

## Acceptance Criteria (what makes this DONE)

1. **Every** pre-registered count field is reported: `plies_san_total`, `count_bare_ply`,
   `count_after_crash_excl`, `count_after_degenerate_excl`, `count_usable_distinct`,
   `count_usable_distinct_train`, `count_usable_distinct_holdout`, `games_used`,
   `games_excluded_crash`, `games_excluded_degenerate`, `duplicates_removed_by_dedup` -
   or reported as `null` with the reason. No field silently omitted.
2. The headline count is recomputable from the stage-by-stage counts by a reader.
3. The band comparison against `75,600..76,587` is reported explicitly, as-is.
4. Train/holdout overlap counts are reported at BOTH the game level
   (`tuple(opening) + tuple(san)`) and the normalized-FEN level, so the overlap-0
   invariant is checkable rather than asserted.
5. An explicit statement that no label field was read, with the counting code as evidence.
6. The dataset SHA-256, E-0013 split-map hash, python-chess and Python versions, the
   exact counting command with exit code, the raw evidence path, and the aggregator
   command reproducing every number are all recorded.
7. Any abort is reported as an abort, with the triggered condition number and evidence.
8. Nothing outside E-00015's Results/Provenance sections is edited.

**Explicitly NOT an acceptance criterion:** a count inside the band, or a count above
30,000. A count below the floor is a legitimate and useful result: it converts a latent
trap into a known state, and E-0013's rule already says what happens then.

## Response (receiver, append-only)
- 2026-09-26 - (role) - ...

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: ...

attributes the two WORST marginal contributions (mobility -3.7 Elo, tempo -11.5 Elo) to
exactly those terms, so the ladder's fallback citation is backwards. A reduced scope must
be re-derived and re-registered under its own critique. Report the count; do not choose a
replacement scope.

**Specifically NOT authorised:**
- Reading any label field.
- Changing the predicate, the dedup order (global-before-split, per F9), the split salt,
  the split map, the 30,000 floor, or the band after seeing the count.
- Any fitting, any game generation, any engine pair, any SPRT activity.
- Editing `tools/e0011_check.py`, `tools/e0012_sprt.py`, or any engine source file. If
  you need a counting tool, write a new one; do not modify the verified checker.
- Flipping E-00015 or E-0013 to RUNNING, or changing any H-#### status.

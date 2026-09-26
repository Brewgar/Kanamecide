---
id: S-0027
type: session
agent: adversarial-reviewer
title: "HO-0014 re-critique of the E-0013 addendum vs R-0019 B1-B7 - NOT CLEAN on two new blocking findings (X1 truncated/interleaved addendum, X2 false parameter-count rationale); all three integrity properties HOLD"
title: "HO-0014 re-critique of the E-0013 addendum vs R-0019 B1-B7 - NOT CLEAN on two new blocking findings (X1 truncated/interleaved addendum, X2 false parameter-count rationale); all three integrity properties HOLD"
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-26
closed: 2026-09-26
---

# S-0027 - Session (adversarial-reviewer)

> One session record per agent session, written to disk BEFORE the chat ends. It is
> the handoff to whoever runs next. Keep it short and factual; the records are the
> detail.

## Round / Work Items Touched
- HO-0014 (received, now DONE) - re-critique of the E-0013 addendum against R-0019 B1-B7, discharge verification only.
- R-0020 (filed) - the review itself. E-0013, E-00014, E-00015 read only; none edited.

## What I Did (with evidence)

| # | Action | Evidence (command -> exit code -> path) | Calibration |
|---|---|---|---|
| 1 | Confirmed a clean start at the expected commit | `git pull --ff-only` -> up to date; `git rev-parse HEAD` / `origin/master` -> both `8759ed31`; `git status -sb` -> clean | demonstrated |
| 2 | Ruled HO-0014's own integrity CLEAN (no cut sentence, nothing below the Response/Verification template, no unrequested acceptance criterion) | read all 172 lines from a numbered disk dump | demonstrated |
| 3 | Proved append-only myself rather than accepting the reported numstat. HO-0014's suggested command returns EMPTY on a clean tree; the correct baseline is the pre-addendum commit `4478c3a` | `git diff --numstat 4478c3a HEAD -- research/experiments/E-0013-*.md` -> `648  0  <file>`; shortstat -> `1 file changed, 648 insertions(+)` | demonstrated |
| 4 | Ruled the three integrity properties separately: (i) original text unaltered HOLDS; (ii) SHRINK REMOVED the unexecutable mandate rather than re-pointing it HOLDS; (iii) nothing measured/fitted/counted/run, no holdout read, no status flipped HOLDS | S-1 quoted at L473-474 and superseded by name at L517-519; `git show --name-only ce845c5` -> 10 paths, all `research/*.md`; `git diff 4478c3a HEAD -- research/hypotheses/` -> empty; every `m0_audit/e0011/` mtime still 2026-09-24 | demonstrated |
| 5 | Verified the B1 replacement is achievable against the real surface, not by assertion | read `tools/e0012_sprt.py:297-303, 320-330, 470-492`; `src/main.cpp:103-114, 133-147`; `src/eval.cpp:352-358`; `src/_write_eval.py:1-32`; `src/eval.h` in full. Every citation in the addendum is exact | demonstrated |
| 6 | Verified B6's central claim against code: 76,593 is a per-`san`-ply count for the bare predicate, a DIFFERENT filter from E-0013's own | `tools/e0011_check.py:371-383` (distinct-FEN Counter) vs `:384-395` (per-ply `quiet_proxy`); `m0_audit/e0011/check_output.txt` | demonstrated |
| 7 | Ruled B1 DISCHARGED, B2 DISCHARGED (text)/honestly converted (measurement), B3/B4/B5 PARTIALLY DISCHARGED, B6 DISCHARGED, B7 DISCHARGED | R-0020, each with cited line numbers | demonstrated |
| 8 | Ruled all twelve F1-F12 closed (8 by VALUE, 3 by explicit POINTER, F4 by value+pointer) | R-0020 F-table | demonstrated |
| 9 | Ruled DN1-DN10 complete: 5 discharged, 4 recorded/routed, 1 recorded-and-carried; no silent drop | E-0013 L736-L747 | demonstrated |
| 10 | Ruled the BUCKET-2 delegation HONEST on all three of HO-0014's tests | E-00014/E-00015 both PENDING, `result: null`; HO-0015 acceptance states "The holdout is never read"; E-00014 is TRAIN-ONLY | demonstrated |
| 11 | Redid all handed arithmetic. Everything reproduces EXCEPT the parameter count, which is 4.46x short of the standard the record claims to meet | 1705/130930 = 1.3022 %; 0.01302 x 76593 = 997.2; band 75,600-76,587; 0.002/0.198103 = 0.0100964; salt 2,000,006 > 1,999; k4-k3 = -3.7; k6-k5 = -11.5; **683 params / 76,587 = 112.1 per param vs 500 required = 4.46x short** | demonstrated |
| 12 | Filed two new blocking findings the addendum's own disposition table is silent about (X1, X2) and gave exact repair text | R-0020 "What must change": 9 seam joins by line number, 1 relocation, 1 termination, 1 author-supplied sentence with 3 stated conditions, 1 replacement clause, 2 `owner:` fields | demonstrated |
| 13 | Filed S-0027 (this record) and closed HO-0014 with its Response + Verification blocks | HO-0014 `status: DONE`, `closed: 2026-09-26` | demonstrated |

## What I Did NOT Do (and why)
- Did not re-litigate any R-0019 ruling: P1-adopted/P0-deferred, Q-LABEL result-only, Q-FIT deterministic full-batch L-BFGS with SPSA withdrawn, Q-SCOPE all-terms with KING PSTs frozen, Q-SUITE independent suite with substitution closed, per-game cap NONE. All SETTLED per HO-0014.
- Did not rule on whether SHRINK was the better engineering call, nor on the pinned `SUITE_TOLERANCE = 0.02`. Both explicitly out of scope.
- Ran no training, fitting, extraction, counting, feasibility pass, build or SPRT game generation; read no holdout; did not run `tools/e0012_sprt.py` in any mode.
- Did not edit E-0013, E-00014, E-00015, HO-0014's Request section, R-0019, any CLOSED/VERIFIED record, `tools/e0012_sprt.py`, or any engine source.
- Did not flip E-0013 to RUNNING; did not open or close HO-0005/W-0003; changed no H-#### status.
- Did not add a second conformance-hold finding beyond X1/X2, and did not demand any decision be re-opened.

## Claims I Made That Are NOT Yet Verified
- **The offline-evaluator / compiled-scorer equivalence** (R-0020, "Residual risk"). B1 differentiates two parameter tables by SHA-256 inside an offline evaluator, while the pinned floor is the compiled-in table at `src/eval.cpp:174-234`. Nothing in the addendum pins that the offline evaluator's scoring is identical to the compiled scorer's. I flagged this as a residual for the execution seat rather than inventing a requirement; it is calibration **unknown** and should be confirmed before stage (a) produces a number.
- **That the text missing at E-0013 L707 is absent rather than merely unlocated.** I verified it has no candidate tail anywhere in the file; I cannot rule out that the author holds it elsewhere. Calibration **strongly supported**.

## Environment Facts Learned
- `run_commands` reported `Command exited with code 1` on commands that plainly succeeded, throughout, as HO-0014 warned. Every capture was taken with `| Out-File -Encoding utf8` and read from the FILE, which I treated as authoritative over the reported status.
- **Material disagreement found and chased down:** `research.py validate` first returned **exit 1** with 60 problems. All 60 were caused by my own `_t_*.txt` scratch files in the repo root tripping the DEC-0009 hygiene check. I moved them to `%TEMP%\kaname_rev` and re-ran: **exit 0**. The failure was mine, not the record's - stated here rather than hidden, and it is why the first `validate` number in my own evidence block is annotated.
- `read_files` returned stale/conflicting content for chunk reads of the E-0013 addendum, exactly as warned. Two conflicting reads (of E-0013 L823 and L828) were discarded before any line number was cited. **Every line number in R-0020 comes from a numbered dump written to disk.**
- `git diff --numstat HEAD -- <file>` is **useless as an append-only check on a clean tree** - it returns empty, indistinguishable from "nothing changed". The baseline commit must be named explicitly (`4478c3a` here). This is a trap for any future reviewer told to "verify the numstat yourself".
- `git diff --check` emits LF->CRLF warnings on Windows for these files; those are line-ending notices, not whitespace errors (0 trailing-whitespace / space-before-tab / blank-line-at-EOF findings).
- `python research/scripts/research.py` has no close-handoff subcommand; a handoff is closed by editing its front-matter `status:`/`closed:` directly while it is still `REQUESTED|ACCEPTED`.
- **PowerShell `Set-Content -Encoding utf8` writes a UTF-8 BOM, and that BOM breaks the record front-matter parser.** It cost me three validate cycles on S-0027 ("missing/invalid front-matter", then `status='' not in the session vocabulary`, then a self-referential dangling-id warning). Every pre-existing record starts `2D 2D 2D 0A` (`---` + LF) with **no** BOM. To rewrite a record's bytes without one: `[System.IO.File]::WriteAllText($path, $txt, (New-Object System.Text.UTF8Encoding($false)))`. Note this is the opposite failure from the `>` -> UTF-16 trap HO-0014 warned about: both are encoding problems, in opposite directions. **Read the file's first bytes when a front-matter parse fails** - the visible text is identical either way.
- While confirming the CLI-assigned id I re-ran `new-review` and created a stray stub, which I deleted. Naming that stub's id in R-0020 produced a dangling-id validate warning, so the note deliberately does not repeat the id - the same self-inflicted warning class the previous session had to fix.

## State Left On Disk
- `research/reviews/R-0020-*.md` - the ruling. NOT CLEAN; E-0013 stays PENDING.
- `research/handoffs/HO-0014-*.md` - `status: DONE`, `closed: 2026-09-26`, with my Response and Verification appended.
- `research/sessions/S-0027-*.md` - this record.
- `research/index.md`, `research/state.md`, `research/state.json` - regenerated by `update` and `state --write`.
- E-0013, E-00014, E-00015, R-0019, all H-#### and all CLOSED/VERIFIED records: **untouched**.

## Next Action For The Successor
- **researcher-architect**: re-issue the E-0013 addendum per R-0020 "What must change". All of it is mechanical: join the ten seams by the line numbers given, move the X-1/X-2/X-3 table to sit under B3 sentence 3, re-join the F-U1..F-U6 obligations list, terminate the file with a complete sentence, supply the one author-only sentence (X1-a) against the three stated conditions, replace the X2 clause with the supplied arithmetic sentence (and change "240" to "128"), and set `owner:` on E-00014 and E-00015. **No decision is re-opened**: SHRINK, the freeze, `SUITE_TOLERANCE = 0.02`, the NONE cap and the X-1/X-2/X-3 branches all stand.
- Then a **fresh re-critique** of the corrected addendum before E-0013 may move PENDING -> RUNNING. I am deliberately not pre-authorising that flip.
- **E-00014 and E-00015 may proceed in parallel** under HO-0015/HO-0016: they are separate PENDING records, they do not read the holdout, and they do not depend on E-0013 leaving PENDING. E-00014's numbers feed the X-1/X-2/X-3 branch decision, so running them now is the cheapest way to shorten the remaining cycle.

## Escalations (owner decisions needed)
- **Whether the offline-evaluator equivalence check becomes a pre-registered requirement.** I flagged it as a residual (calibration unknown) rather than ruling on it, because it is a new requirement and not a discharge of any R-0019 finding. If the owner wants it binding, it should be added as an addendum clause and critiqued - not smuggled in as a reviewer preference.
- **Whether the X2 correction should also be made to R-0019.** The false ">= 500 positions/parameter" rationale and the "240" figure both originate in **R-0019's own B5 text** (R-0019:81-83) and were faithfully copied into the addendum. R-0019 is a COMPLETED review and I did not edit it. If the project wants the error corrected at source rather than only downstream, that is an owner's call.

## Validation Status
- `python research/scripts/research.py update` -> **exit 0**
- `python research/scripts/research.py state --write` -> **exit 0**
- `python research/scripts/research.py validate` -> **exit 0**, "Validation OK - statuses are in-vocabulary; the perft anchor and project_state.md consistency are verified; repo-root hygiene is respected." Only grandfathered/advisory warnings remain, and no new warning class was introduced.
- `git diff --check` -> **exit 0** (0 trailing-whitespace / space-before-tab / blank-line-at-EOF findings; LF->CRLF notices only).

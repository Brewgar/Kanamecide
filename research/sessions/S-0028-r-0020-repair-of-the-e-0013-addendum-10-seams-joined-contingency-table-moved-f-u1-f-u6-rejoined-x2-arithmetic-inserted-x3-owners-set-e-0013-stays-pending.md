---
id: S-0028
type: session
agent: researcher-architect
round: 4
title: R-0020 repair of the E-0013 addendum: 10 seams joined, contingency table moved, F-U1..F-U6 rejoined, X2 arithmetic inserted, X3 owners set; E-0013 stays PENDING
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-26
closed: 2026-09-26
---

# S-0028 — Session (researcher-architect)

> One session record per agent session, written to disk BEFORE the chat ends. It is
> the handoff to whoever runs next. Keep it short and factual; the records are the
> detail.

## Round / Work Items Touched
- Round 4, seat `researcher-architect` (OWNER). No `W-####` item; this is the owner-side repair
  of the E-0013 addendum that adversarial-reviewer found NOT CLEAN in **R-0020** (HO-0014).
  Records read in full: `research/SYSTEM.md`, R-0020 (all 902 lines), and the E-0013 addendum
  (L429+) from a numbered dump. Records written: E-0013 (addendum only), E-00014, E-00015, this
  session. Nothing else was edited.

## What I Did (with evidence)

| # | Action | Evidence (command → exit code → path) | Calibration |
|---|---|---|---|
| 1 | Derived every seam line number from a numbered dump rather than trusting R-0020's or my own memory, then joined by CONTENT | `python` num-dump of E-0013 → 0 → `$TEMP/kana_scratch_s0028/e0013_numbered.txt`; all 10 heads and 10 continuations located and asserted before any edit | demonstrated |
| 2 | **Proved the append-only contract by hash.** Lines 1-428 of E-0013, from `git show ce845c5:<path>` and from the working file | `python` SHA-256 over lines 1..428 (UTF-8, with terminators, 22,270 bytes) → 0 → both `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`; equal | demonstrated |
| 3 | Joined the ten severed sentences as contiguous text in their own sections, moving each continuation byte-for-byte (no retyping, nothing deleted) | repair script `repair1.py` → 0 → E-0013; after-ranges L471-475, L515-517, L542-543, L593-598, L639-649, L743-747, L765-774, L834-848, L871-875, L899-L903 | demonstrated |
| 4 | Seam 8 (X1-a), the one absent continuation: **adopted R-0020's conforming template VERBATIM** (R-0020:696-701) | E-0013 L835-L840, leading into the existing tail at L841-L848; it names E-00015, makes DISARMED provisional, says the band is NOT a measurement of this record's own filter, and ends `(mobility/tempo scope; B6)` | demonstrated |
| 5 | Moved the X-1/X-2/X-3 contingency table (old L960-L995) to sit under B3 sentence 3's announcement, no wording change | E-0013: announcement L677-L680, table L682-L717 | demonstrated |
| 6 | Re-joined F-U1..F-U6, including F-U3's stranded `Owner:/Due:` line | E-0013 L909-L944, one contiguous list; F-U3's owner line at L931 | demonstrated |
| 7 | Restored B1's cost item 4 to items 1-3, and the BUCKET-1/2/3 list to one place; completed BUCKET 3's promised cost in the bullet's own words | E-0013 L544-L548, L471-L487 | demonstrated |
| 8 | Terminated the addendum's narrative on a complete sentence | E-0013 L1106-L1114; the old L1073 bullet had no continuation of any kind | demonstrated |
| 9 | **X2**: deleted the false parameter-count clause, inserted R-0020's replacement verbatim, changed 240 → 128, and added a dated editorial note naming the old wording | E-0013 L788, L791-L807, L809 | demonstrated (R-0020's arithmetic) |
| 10 | **X3**: `owner: systems-researcher` on E-00014 and E-00015, the seat HO-0015/HO-0016 dispatch to | one front-matter line each; both records still `status: PENDING`, `result: null` | demonstrated |
| 11 | **N1** as a binding text note (coefficient regeneration substitutes the block ONLY; never re-run a stage generator) at E-0013 L572-L581; **N2** F-U4's owner seat named literally at L934-L935; **N3** disposition-table rows for X1 and X2 | E-0013 L572-L581, L934-L935, and the two new rows in the addendum-to-addendum table | demonstrated |
| 12 | Added the dated repair section to E-0013, including the L1-428 hash pair and the explicit ORIGINAL-vs-ADDENDUM append-only distinction | E-0013 L1116-L1234 | demonstrated |
| 13 | `research.py update`, `state --write`, `validate`, `git diff --check` | exit codes 0 / 0 / 0 / 0; `validate` prints "Validation OK" | demonstrated |
| 14 | Committed and pushed; HEAD == origin/master; tree clean | `git push origin master` → 0; `git rev-parse HEAD` == `git rev-parse origin/master` | demonstrated |

## What I Did NOT Do (and why)
- **Did not flip E-0013 to RUNNING** and set no `result:`. I am not authorised to, and per R-0020
  the move PENDING → RUNNING requires a fresh re-critique to confirm. E-0013 ends this session
  at `status: PENDING`.
- Did not re-open any decision. SHRINK, the KING-PST freeze, `SUITE_TOLERANCE = 0.02`, the NONE
  per-game cap and the X-1/X-2/X-3 branches are exactly as ruled.
- Did not re-derive or "improve" R-0020's arithmetic. Its 683 / 76,587 / ~112 / ~4.5x figures are
  inserted verbatim, and the freeze rationale now records the shortfall as a STATED LIMITATION.
- Did not edit R-0019, R-0020, HO-0013, HO-0014, or any CLOSED/VERIFIED record (E-0011, E-0012,
  W-0001, W-0005, RUN-0002/0003, R-0017/R-0018), and did not touch any H-#### text or status.
- Did not touch `tools/` or `src/`. N1 is a text note about `write_eval_p5.py`, not a change to
  it, and `write_eval_p5.py` / `src/eval.cpp` are cited and not edited.
- Did not open or close HO-0005 / W-0003, and did not run `research.py round`.
- Ran no training, fitting, extraction, counting, feasibility pass or SPRT generation, and read
  no holdout. The only numbers I produced are SHA-256 hashes of text I had already written.
- Did not correct the "(240 params)" in the F3 row of the F1-F12 table: that is R-0019's own
  item label, quoted, and editing quoted text is the thing the append-only rule forbids.

## Claims I Made That Are NOT Yet Verified
- **That the repair is complete and correct.** I have shown the ten seams are contiguous, the
  table is under its announcement, the obligations are one list, the file ends on a complete
  sentence, and the false clause is gone. Whether a re-critique agrees is not mine to certify -
  R-0020 asked for a re-critique, and this repair is the input to it, not a substitute for it.
- **That R-0020's own arithmetic is right** (683 free scalars, 76,587 positions, ~112/~89 per
  parameter, ~4.46x short). It is inserted verbatim on R-0020's authority. I did not re-count
  `EvalCoeffs` member by member, because that is the reviewer's instrument and it is recorded as
  its finding, not as mine. An adversarial-reviewer re-check is the natural place for it.
- The historical `648 additions / 0 deletions` numstat over `ce845c5..HEAD` no longer holds and
  will not hold again. That is intended, and the record says so; it is not a claim awaiting proof.

## Environment Facts Learned
- `run_commands` reported `Command exited with code 1` on **every** command in this session,
  including ones that plainly succeeded. Every verdict in this record is taken from a file's
  contents, and the four exit codes were captured with `$LASTEXITCODE` explicitly.
- PowerShell `>` writes UTF-16: `git show ... > file` produced a 73,719-byte file as 147,438
  bytes with a `FF FE` BOM, which then failed to decode as UTF-8. Redirecting through
  `Out-File -Encoding utf8` still writes a BOM, which silently breaks record front-matter
  parsing. I did all record I/O through `python` with explicit `encoding='utf-8'` and
  `newline='\n'`, and every file written that way is BOM-free and LF-only, matching the
  pre-existing bytes.
- `read_files` returns STALE content for line-range requests on large files, as warned. Every
  line number I acted on came from a numbered dump written to disk and re-read. Two early chunk
  reads of the addendum disagreed with the dump; the dump won.
- `git diff --check` emits `LF will be replaced by CRLF` warnings for every touched file
  (`core.autocrlf=true`) and still exits 0. Those warnings are not whitespace errors.
- `research.py new-session` allocates a five-digit id (S-0028). Scratch scripts were kept in
  `%TEMP%\kana_scratch_s0028`, **outside** the repository, so nothing new appeared under the
  repo root or under `research/`.
- `git diff --numstat HEAD -- <path>` returns **empty** on a clean tree and cannot distinguish
  "add-only" from "nothing changed". Always name a baseline commit: `ce845c5` for the pre-repair
  addendum, `4478c3a` for the pre-addendum file.

## State Left On Disk
- `research/experiments/E-0013-...md` — addendum repaired in place; L1-L428 byte-identical to
  `ce845c5` (SHA-256 `b04fd5a4...00ce6` on both sides); dated repair section at L1116-L1234.
  `status: PENDING`, `result: null`, `completed: null` - unchanged.
- `research/experiments/E-00014-...md`, `E-00015-...md` — `owner: systems-researcher`. Both still
  `status: PENDING`; neither was run.
- `research/state.md`, `research/state.json`, `research/index.md` — regenerated by the CLI.
- No `src/`, `tools/`, `m0_audit/` or build artifact was touched. No new measurement exists,
  because none was taken.

## Next Action For The Successor
- **adversarial-reviewer**: a fresh re-critique of the repaired E-0013 addendum against R-0020's
  four conditions (all seams joined + table under B3 s3 + obligations contiguous + complete
  terminal sentence; X1-a supplied; X2 replaced and 240 → 128; owners set on E-00014/E-00015).
  Only on that ruling may E-0013 move PENDING → RUNNING. R-0020 explicitly did not pre-authorise
  the flip.
- **systems-researcher**: E-00014 and E-00015 are runnable now under HO-0015 / HO-0016. Both have
  a named owner for the first time. Neither depends on E-0013 leaving PENDING, neither reads the
  holdout, and E-00015's count is what the pre-registered 30,000 scope floor and the ladder's
  DISARMED status wait on.
- **researcher-architect (next round)**: F-U1..F-U6 remain open and dated to E-0013 close-out;
  F-U4 still requires a correction to E-0011 filed *by the seat that owns E-0011*
  (`systems-researcher`), not by this seat.

## Escalations (owner decisions needed)
- One, and it is not a decision I was asked to make: **whether B5's all-terms scope should
  survive a 4.46x shortfall against E-0011 N1's identifiability standard.** R-0020 ruled the
  *text* discharged by recording the shortfall honestly and left the *decision* alone, and I
  have left it alone. If the next reviewer wants the scope revisited, that is a new ruling in a
  new record, not an edit to this one.
- Not an escalation, recorded so it is not lost: "B5 sentence 2 (the ladder's citation,
  corrected)" at E-0013 L811 announces quoted text that lives far away under B6 sentence 1. It
  is a dangling pointer, not a severed sentence, and R-0020 did not enumerate it; I left it
  exactly as found and flagged it in the record rather than moving text on my own judgement.

## Validation Status
- `python research/scripts/research.py update` → **exit 0** ("updated: research/index.md").
- `python research/scripts/research.py state --write` → **exit 0** ("wrote research/state.json and
  research/state.md").
- `python research/scripts/research.py validate` → **exit 0**, "Validation OK - statuses are
  in-vocabulary; the perft anchor and project_state.md consistency are verified; repo-root
  hygiene is respected." The warnings printed alongside are pre-existing and grandfathered
  (legacy E-0000x records, dangling ids from retired names, ambiguous `beliefs.md` /
  `current_position.md`); none of them names a file this session touched.
- `git diff --check` → **exit 0**.
- `git status -sb` after commit → `## master...origin/master`, clean tree.

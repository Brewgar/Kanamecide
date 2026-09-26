---
id: S-0033
type: session
agent: researcher-architect
round: 4
title: Two stale evidence lines in E-0013 REVISED in place (Z2 prose + condition row 10) - the withdrawn figure 8ad61ccd/00a727 occurs 4x, all inside the Z2 withdrawal record, in NO live claim; orchestrator count; seam 22, 0 new; E-0013 stays PENDING
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-26
closed: 2026-09-26
---

# S-0033 — Session (researcher-architect)

> One session record per agent session, written to disk BEFORE the chat ends. It is
> the handoff to whoever runs next. Keep it short and factual; the records are the
> detail.

## Round / Work Items Touched
- E-0013 — two **stale evidence lines revised in place**. No other line changed.
- No work item opened or closed. HO-0005 / W-0003 untouched.

## The defect, and why it was mine
S-0032 wrote Z2's withdrawal into this record. The withdrawal is the correct disposition and
**stands unchanged**. But writing the withdrawn figure into the record made two of my own
evidence lines false *by that very edit*:

1. Z2 prose (was L1698-L1702): "`8ad61ccd` and `00a727` appear in `research/` only inside
   R-0023" — false, because the withdrawal put them in E-0013.
2. Condition table row 10: "present in **R-0023 only**; never in this file" — false, and
   **self-denying**: row 10 is itself one of the occurrences.

Both were true at `f03613e` and went stale at `dc8f9fc`. This is the **self-invalidating
evidence line** hazard: a withdrawal that must name the figure to withdraw it necessarily
creates a new occurrence of the string it is withdrawing. The fix is to revise the claim, not
to delete the line and not to withdraw differently.

## The repair — attribution
**The orchestrator's independent count** found the four occurrences (L1696, L1699, L1809,
L1862); I confirmed it with `git grep` and adopted its number. This is **not a fresh defect of
mine** — it is the expected consequence of a correct earlier edit. Both lines are rewritten,
**not deleted**, and each now says on its face that the earlier "never in this file" search
result was true at `f03613e`, was **made stale by the Z2 withdrawal itself**, and names the
corrected reading.

## What I Did (with evidence)

| # | Action | Evidence (command → result → path) | Calibration |
|---|---|---|---|
| 1 | Repo state at session start | `git pull --ff-only` 0 "Already up to date"; `git status -sb` clean; HEAD == origin/master == `ffb6d9e` | demonstrated |
| 2 | Orchestrator's count of 4 occurrences **independently confirmed** | `git grep -n 8ad61ccd` → L1696, L1699, L1809, L1862 in E-0013 | demonstrated |
| 3 | Each occurrence labelled withdrawal-record vs live-claim | L1696 Z2 body (withdrawal); L1699 Z2 body (withdrawal, this repair); L1809 condition row 4 = the Z2 discharge row (withdrawal); L1862 condition row 10 (withdrawal, this repair). **Live claims: 0** | demonstrated |
| 4 | Z2 prose revised in place, line count held at 5 | `git diff -U0` hunk 1, `-5/+5`; L1698-L1702 | demonstrated |
| 5 | Condition row 10 revised in place, still one table row | `git diff -U0` hunk 2, `-1/+1` at L1862 | demonstrated |
| 6 | Whole-file line count unchanged by this repair | 1,865 lines before and after; numstat **6/6** | demonstrated |
| 7 | **Cited line numbers are self-consistent** — the repair cites its own post-edit positions | after editing, `git grep` → 1696, 1699, 1809, 1862, exactly the four cited | demonstrated |
| 8 | `H_body` recomputed on **BOTH sides** (`ce845c5` blob and working file), lines 1-428 minus {5,6,7,10,14} | `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7`, **22,196 bytes** on both — **pair equal** | demonstrated |
| 9 | `4478c3a..HEAD` numstat with commit label | `4478c3a` "R-0019 critique of the E-0013 Texel pre-registration - NOT CLEAN…"; **1440 insertions / 0 deletions** | demonstrated |
| 10 | Per-hunk paren audit, `git diff -U0` | 2 hunks; hunk 1 `+0/-0`, hunk 2 `+0/-0`; **total delta 0** | demonstrated |
| 11 | **Seam instrument rebuilt and re-run** | see below | demonstrated |
| 12 | Terminal-punctuation/seam check over exactly the lines edited | the 6 edited lines introduce **0** new seams; no edited line ends on a dangling token | demonstrated |
| 13 | File hygiene | no BOM, **0 CR bytes**, single trailing newline, LF-only, 1,865 lines | demonstrated |
| 14 | E-0013 front matter | L5 `status: PENDING`, L6 `result: null`, L7 `elo_change: null`, L10 `owner: null`, L14 `completed: null` — **PENDING, not flipped** | demonstrated |
| 15 | `update`, `state --write`, `validate`, `git diff --check` | all **exit 0**; validate → "Validation OK" | demonstrated |

## The seam instrument — rebuilt, because S-0032's was not saved
S-0032 ran the seam check ad hoc and **did not commit the script**, so I could not re-run it
as written. I reconstructed it from the recorded definition and **calibrated it against the
two numbers S-0032 published**, rather than asserting it:

| Anchor | S-0032 recorded | Rebuilt instrument |
|---|---|---|
| `b7179f3` (pre-Z1) | 19 | **19** — and it **captures Z1 at L1376**, the one true positive |
| `8c30f32` (post-Z1) | 18 | **18** |
| `ffb6d9e` (HEAD) | — | 22 |
| worktree after this repair | — | **22 — 0 new** |

Both recorded anchors reproduce exactly, including the discriminating case, so the
reconstruction is faithful on the evidence that matters. Definition used: line N opens on a
capitalised/identifier token while line N-1 ends on a **dangling function token** (one that
cannot terminate a sentence) and carries no sentence boundary, skipping structure (headings,
list items, table rows, fences) and the frozen L1-428 block.

**Honest caveat, stated rather than hidden.** The instrument reports **22** at HEAD, not 18.
The 18 was measured at `8c30f32`, which reproduces exactly. The +4 all sit in the S-0032
addendum (L1530, L1645, L1662, L1838) and are surface-indistinguishable from the 18 counted
as legitimate — L1662 opens on `L1377`, a ledger pointer of exactly the kind counted at
L677-L680. **I could not find a surface rule that separates them, and I did not invent one to
make the number come out.** The load-bearing claim for this session is the delta: **0 new
seams**, which is robust to this ambiguity. The 22-vs-18 gap is a calibration question for
whoever turns this into tooling, and I flag it rather than paper over it.

## What I Did NOT Do (and why)
- **DID NOT FLIP E-0013 to RUNNING.** R-0023's condition part 6 still requires a **fresh
  adversarial-reviewer critique**; this seat may not self-verify its own proposal
  (SYSTEM.md §1). `status:` remains `PENDING` at L5.
- **DID NOT DELETE either evidence line.** A record that deletes the evidence line is doing
  the opposite of what is wanted; both were rewritten so the claim is checkable.
- **DID NOT weaken the disposition.** The figure remains **WITHDRAWN, not asserted**, and
  `d8add61c...e6144` remains the recorded correct projection. All four occurrences sit inside
  the withdrawal record; **no live claim** carries the figure.
- **DID NOT edit S-0032 L38**, which carries the same stale "only inside R-0023, never in
  E-0013" wording. It is a **CLOSED, append-only session record**; the stale line is
  superseded by this record rather than rewritten. Flagged, not silently touched.
- Did not touch lines 1-428 (H_body pair equal on both sides). Did not edit R-0019 to R-0023,
  `tools/`, or `src/`. No H-#### text or status edited. HO-0005 and W-0003 untouched.
- Did not re-run R-0023's 30-scheme brute force. I did not attempt to reconstruct the scheme
  behind `8ad61ccd...00a727`; the withdrawal is accepted on R-0023's negative result.
- Did not run training, fitting, extraction, counting or SPRT generation. Did not read the
  holdout. Did not set any `result:`.

## Claims I Made That Are NOT Yet Verified
- **The seam instrument's 22-vs-18 gap at HEAD is unresolved.** My reconstruction reproduces
  both published anchors (19 at `b7179f3` including the Z1 true positive, 18 at `8c30f32`) but
  finds 4 extra seams in the S-0032 addendum. Either S-0032's ad-hoc script had a filter I
  could not recover, or it undercounted. **Unresolved — it is a calibration question, not a
  finding about the file.** Whoever builds the text-integrity tooling must settle it against a
  committed script, and should commit the script this time.
- The rebuilt instrument is **n=1 calibrated against two anchors**, not validated. Its
  discriminating power rests on S-0032's single true positive, which I did not re-derive.
- I did not independently re-verify R-0023's brute-force negative; I accepted the withdrawal,
  which is the conservative direction.

## Environment Facts Learned
- The S-0032 seam instrument was **never committed**, so "re-run your own seam instrument" means
  re-derive it. Calibrating a reconstructed instrument against its published anchors is the
  only honest way to claim continuity — assert nothing you did not reproduce.
- `research.py new-session` derives the filename from `--title`, so a long title **silently
  produces a path over MAX_PATH**: the generated S-0033 name was **285 chars** and had to be
  renamed to 143. Keep titles short; the body carries the detail.
- `run_commands` reports `Command exited with code 1` even on success. Verdicts were taken
  from file contents with `$LASTEXITCODE` captured explicitly.
- `core.autocrlf=true`: git prints "LF will be replaced by CRLF…" on add/diff. Checkout-time
  warning only; the stored blob stays LF and the file has 0 CR bytes.

## State Left On Disk
- E-0013: two evidence lines revised in place; **1,865 lines unchanged**, numstat 6/6,
  `status: PENDING`, lines 1-428 byte-identical to `ce845c5` by `H_body`.
- This session record, S-0033.

## Next Action For The Successor
1. **An adversarial-reviewer must still run a fresh critique of E-0013** confirming (v-a)
   `H_body` = `c7ebe54c...f883bea7` on both sides over 22,196 bytes. Only then does R-0023's
   condition part 6 close, and only then is the flip authorised. The flip remains a **separate
   L5-only commit**, line-anchored, never by string replace.
2. When this becomes tooling: **commit the seam instrument** and settle the 22-vs-18
   calibration first, so the gate is reproducible by the next seat.

## Escalations (owner decisions needed)
- **S-0032 L38 carries the same stale claim** ("only inside R-0023, never in E-0013"). It is
  append-only and I did not edit it. If the owner wants historical records corrected in place
  rather than superseded, that is a policy call affecting every closed session record.
- The 22-vs-18 seam calibration gap, if the tooling work item needs a fixed threshold.

## Validation Status
- `python research/scripts/research.py update` → **exit 0**
- `python research/scripts/research.py state --write` → **exit 0**
- `python research/scripts/research.py validate` → **exit 0**, "Validation OK — statuses are
  in-vocabulary; the perft anchor and project_state.md consistency are verified; repo-root
  hygiene is respected." (`audit` warnings are pre-existing and advisory.)
- `git diff --check` → **exit 0**
- `H_body` pair equal on both sides; `4478c3a..HEAD` = 1440/0; paren delta 0; seams 22, 0 new.
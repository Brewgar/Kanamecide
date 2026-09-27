---
id: S-0037
type: session
agent: researcher-architect
round: 4
title: e0013-leakage-ruling-normalized-fen-dedup-key
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-27
closed: 2026-09-27
---

# S-0037 — Session (researcher-architect)

> One session record per agent session, written to disk BEFORE the chat ends. It is
> the handoff to whoever runs next. Keep it short and factual; the records are the
> detail.

## Round / Work Items Touched
- Round 4. E-0013 only. W-0003 remains untouched and is not claimed. No work item is
  closed here.

## The RULING, in one line
**Option (1): strengthen the dedup KEY to the normalized four-field FEN.** Not (2) re-split,
not (3) INCONCLUSIVE-BY-SCOPE. Full reasoning, costs, and the supersession of E-00015's
band are in E-0013's S-0037 addendum (below L2067). The one-line reason: F9 required the
normalized-FEN gate to be *entailed by construction*, and a dedup key **strictly finer**
than the gate's comparison key cannot entail it — so the gate firing is evidence about the
key, not about the data. Option (2) is rejected because a salt adopted after a known-failing
gate is selection on the leakage check, which L309-310's own p-hacking tripwire forbids.

## What I Did NOT Do (and why)
- **Did not edit `tools/e0013_extract.py`, `tools/e0013_eval.py`, or anything under `src/`.**
  The remedy is the engineer's; I own the contract and I rule the scope.
- **Did not re-run the extractor, fit anything, read the holdout, or read any label field.**
- **Did not change E-0013's `status:` (still `RUNNING`) or any `result:`.** No lifecycle
  transition was made or authorised.
- **Did not edit R-0019..R-0025, any S-00xx, E-0011, E-0012, W-0001, W-0005, RUN-0002/RUN-0003,
  R-0017/R-0018.** Did not change any H-#### text or status. Did not open or close HO-0005/W-0003.
- **Did not adopt a new split salt and did not authorize a salt search.**
- **Did not weaken, re-order, re-normalize or suppress the overlap-0 gate.**
- **Did not edit E-00015** — its supersession is recorded in E-0013 as obligation F-U10,
  because E-0013 owns the key and E-00015 has its own executor seat.
- **Did not re-count or re-derive the 27.** They are carried forward exactly as S-0036 measured.

## Claims I Made That Are NOT Yet Verified
- **The ruling itself is a contract change and is not self-certifying.** It goes to
  verification-auditor with: the F-U7 key change, the E-00015 supersession, the
  `split_map_sha256` invariance assertion, and the `H_body` invariance proof. **A handoff for
  this is owed and has not yet been filed** — see Escalations.
- **The predicted new realized yield is UNKNOWN and I did not estimate it.** It falls; by how
  much is the engineer's measurement (F-U7/F-U10), not my claim.
- **The claim that the new key makes the gate pass is a proof, not a measurement.** It holds

## State Left On Disk
- E-0013: ruling appended below L2067, **append-only**. L1-428 untouched; `H_body` unchanged at
  `c7ebe54c…bea7` / 22,196 B. `status: RUNNING`, no `result:`.
- E-00015: **still PENDING and unrun.** Must WAIT for the new key. Its band lower bound and the
  `~997` exact-FEN projection are **SUPERSEDED**; the 30,000 floor's value is unchanged and is
  not renegotiable.
- E-00014: still PENDING; its inner partition and `s_d_inner`/`delta_star` figures are superseded.
- **Extraction remains BLOCKED.** Nothing fitted, no holdout read, no artifact written.
- `research/state.md` + `state.json` regenerated via `state --write` (never hand-edited).

## Next Action For The Successor
The **implementation-engineer**, under a handoff, implements F-U7..F-U9:
1. **F-U7** — key the dedup `seen` set on `pos.norm_fen`, not `pos.fen`
   (`e0013_extract.py:326-331`); update the published `dedup_key` string at L442.
2. **F-U8** — repair the self-test at L835-839 and add a **clock-only-difference** regression
   case; keep the existing clock-only gate case at L750-752 passing.
3. **F-U9** — re-derive and re-commit split map + `positions.jsonl` + report; assert
   `split_map_sha256` is **UNCHANGED** (a moved digest is a finding, not a new baseline).
4. Then **F-U10** (re-derive the band + re-evaluate the 30,000 floor), **F-U11** (re-derive
   E-00014's inner partition), **F-U12** (route the low-`game_id` survivor bias into Sample
   Validity), **F-U13** (gate stays blocking; if it fires, report as measured).
5. Only then may E-00015 and E-00014 run, and only then may any fit read the data.

**If F-U7 cannot be implemented, the ruling converts IN ADVANCE to option (3)** —
E-0013 ends `INCONCLUSIVE-BY-SCOPE`. That contingency is pre-registered in the addendum so it
cannot later be read as a rationalisation. It is **not** a licence to fall back to (2).

## Escalations (owner decisions needed)
- **A handoff to implementation-engineer for F-U7..F-U13 is owed and is NOT yet filed.** I did
  not file it this session (HO-0005/W-0003 must not be opened or closed, and no new handoff id
  was allocated). **The next seat should file it before any extractor work begins.**
- **A handoff to verification-auditor for this ruling is owed and is NOT yet filed**, carrying
  the key change, the E-00015 supersession, the `split_map_sha256` invariance assertion, and the
  `H_body` proof.
- **No H-#### status was changed and none should be** until a fit is verified.

## Validation Status
- `python research/scripts/research.py validate` → exit 0, `Validation OK` (remaining lines are
  pre-existing grandfathered/advisory warnings, not failures).
- `python research/scripts/research.py update` → exit 0, `updated: research/index.md`.
- `python research/scripts/research.py state --write` → exit 0, wrote `state.md` + `state.json`.
- `git diff --check` → exit 0, empty.
- Repo floor `build\Release\kana.exe` not re-run this session (no `src/` change; S-0036 verified
  it, and this seat changed no code).

  by construction; whether the *implementation* realises it is F-U13's job to check on real data.

## Environment Facts Learned
- `run_commands` reports **exit 1 on success** (shell integration quirk); verdicts must be
  read from `$LASTEXITCODE` and from file contents, never from the command's own "success" field.
- `git checkout -- <file>` re-applies CRLF here; files must be written as UTF-8 **without BOM**
  and LF-only, or `H_body` moves. A trailing blank line at EOF trips `git diff --check` (exit 2).
- PowerShell `>` writes UTF-16 and `Set-Content -Encoding utf8` writes a BOM — both wrong for
  these records; use `[System.IO.File]::WriteAllBytes` for byte-exact work.
- The extractor's self-test at `e0013_extract.py:835-839` asserted the normalized-FEN invariant
  "holds BECAUSE the dedup ran first". **That assertion is false in general** — it held only
  because the synthetic fixture's duplicate copies were byte-identical *including clocks*. This
  is the defect in one sentence, and it is why the 27 were invisible to the self-test.


## What I Did (with evidence)
| # | Action | Evidence (command → exit code → result) | Calibration |
|---|---|---|---|
| 1 | Pushed the 3 unpushed commits before starting | `git push origin master` → `aba0fa3..320aa25 master -> master`, exit 0 | demonstrated |
| 2 | Appended the dated ruling to E-0013 (review-licensed side only) | `H_body` recomputed post-edit → `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7`, **22,196 bytes** — unchanged | demonstrated |
| 3 | Verified the file is still LF-only, BOM-free after the append | `CR_count=0`, first bytes `45,45,45` (`---`) | demonstrated |
| 4 | **Corrected a false premise in the referral** | the referral said the key change moves the split map's SHA-256. It does not: `split_map()` is a pure function of `(SPLIT_SALT, game_id)` (`e0013_extract.py:163-164`, `156-160`), computed at L532 over dataset rows, and the hashed object `{format, split_salt, train_fraction, rule, map}` (L575-582) contains **no dedup-derived quantity**. Recomputed the map digest independently to confirm invariance | demonstrated |
| 5 | Fixed a `git diff --check` failure my own append caused | trailing blank line at EOF → trimmed; `git diff --check` exit 0 | demonstrated |
| 6 | Memory layer green | `update` → 0; `state --write` → 0; `validate` → 0, file contains `Validation OK` | demonstrated |

## Round / Work Items Touched
- W-#### — ...

## What I Did (with evidence)
| # | Action | Evidence (command → exit code → path) | Calibration |
|---|---|---|---|
| 1 | ... | ... | ... |

## What I Did NOT Do (and why)
- ...

## Claims I Made That Are NOT Yet Verified
- ... (route each one via a handoff to a different agent)

## Environment Facts Learned
- ...

## State Left On Disk
- ...

## Next Action For The Successor
- ...

## Escalations (owner decisions needed)
- ...

## Validation Status
- `python research/scripts/research.py validate` → ...
- `python research/scripts/research.py update` → ...
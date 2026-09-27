---
id: S-0036
type: session
agent: implementation-engineer
round: 4
title: e0013-parameter-table-evaluator-built-and-transcription-verified-overlap-0-gate-fails-27-on-the-real-dataset
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-27
closed: 2026-09-27
---

# S-0036 — Session (implementation-engineer)

> One session record per agent session, written to disk BEFORE the chat ends. It is
> the handoff to whoever runs next. Keep it short and factual; the records are
> the detail.

## Round / Work Items Touched
- Round 4. Continued the E-0013 build started in the previous session. W-0003 remains
  `IN_PROGRESS`; it is **not** claimed done here and nothing about it was closed.
- Two commits: `1a2dff7` (extractor, previous session) and `e8e2159` (this one).

## What I Did (with evidence)
| # | Action | Evidence (command → exit code → result) | Calibration |
|---|---|---|---|
| 1 | Built `tools/e0013_eval.py`, the offline parameter-table evaluator | `python tools/e0013_eval.py --selftest` → rc 0 → `SELFTEST PASS checks=78 failed=0` | demonstrated |
| 2 | Verified the whole `src/eval.cpp` transcription against the C++ source | 768 PST literals (6 pieces × mg/eg × 64), every scalar, both passed-pawn arrays, `FLAT_VALUE` → **zero mismatches** | demonstrated |
| 3 | Fixed 5 failing self-test expectations in the evaluator | all 5 were wrong *expectations*, not wrong code: a mis-hand-counted phase (14 not 16), three half-site tests that ignored the taper, and an L2 check that compared gradients at two different points | demonstrated |
| 4 | Found and fixed a **gate-ordering defect** in the extractor | the overlap-0 gate aborted at L613 but artifacts were written at L589-592; a blocking gate that leaves `positions.jsonl` on disk is not a gate | demonstrated |
| 5 | Extended the extractor self-test to pin that fix | `--selftest` → rc 0 → `SELFTEST PASS checks=59 failed=0`, incl. "NOT written when the gate aborts" | demonstrated |
| 6 | Confirmed the repo floor is intact | `build\Release\kana.exe` → rc 0 → `=== ALL TESTS PASSED` | demonstrated |
| 7 | Confirmed the memory layer validates | `research.py validate` → `Validation OK` (remaining lines are pre-existing advisory warnings) | demonstrated |

## The finding that matters: the overlap-0 gate FAILS on the real dataset

`python tools/e0013_extract.py --out-dir m0_audit/e0013_real` → **rc 2**, aborting with
`normalized_fen_overlap=27`, `game_level_overlap=0`. The out-dir was **not created** — the
gate now withholds the data, which is the whole point of it.

These 27 are **genuine cross-split leaks**, not a normalization artifact. Each is an identical
4-field FEN with an **identical label** present in both sides, differing only in the halfmove and
fullmove clocks. Examples, all `K+R vs K` endgames:

| normalized FEN | train | holdout | labels |
|---|---|---|---|
| `8/1R6/8/8/8/2K5/8/k7 w - -` | game 152, ply 234 | game 262, ply 278 | 1.0 / 1.0 |
| `8/1R6/8/8/8/2K5/k7/8 b - -` | game 152, ply 233 | game 262, ply 277 | 0.0 / 0.0 |
| `8/6r1/8/5k2/7K/8/8/8 w - -` | game 929, ply 236 | game 657, ply 276 | 0.0 / 0.0 |

Every colliding train side holds **exactly one** position, so this is not a dedup survivor
artifact. The cause is mechanical: a `K+R vs K` endgame has a small reachable-position space, so
independently generated games reach the same handful of positions, and the **exact-FEN dedup
(clock included) cannot see it** while the **normalized gate can**. E-0013 F9 anticipated exactly
this: the normalized gate "verifies that invariant". It does not verify — it fires.

**This is not mine to decide.** A pass/fail on a blocking leakage gate belongs to the owning
seat, and every fix is scope-changing: re-splitting, deduping on normalized FEN, or excluding
the endgame region each re-opens a decision that is pre-registered. I did not silently pick one.

## What I did NOT do
- Did **not** flip, weaken, re-order, re-normalize or suppress the overlap-0 gate to make the run
  pass. Reported as measured.
- Did **not** read the holdout, fit anything, run the feasibility pass, or set any `result:`.
- Did **not** edit `src/`, any E-00xx record, or any `status:` line. E-0013 stays `RUNNING`;
  E-00014 and E-00015 stay `PENDING`.
- Did **not** run E-00015's count-only pass (it is a separate seat's execution under HO-0016).
- Did **not** write a session/project_state claim that the extraction is unblocked. It is not.

## Next action (owning seat / verification-auditor)
The extraction is **blocked**, so E-00014, E-00015 and the fit cannot proceed until the 27
collisions are adjudicated. Whoever owns E-0013 must rule on the leakage contract. My
recommendation is to file this as a finding against E-0013's conjunct (d) and take a ruling
before any fitting; the honest default if no ruling is affordable is that E-0013 ends
INCONCLUSIVE-BY-SCOPE rather than proceeding on a split that leaks 27 labelled positions.

## Environment facts
- `python` + `chess` + `numpy` present; PowerShell only. The engine exposes no per-FEN
  `evaluate()` dump, so the C++ cross-check was done by parsing `src/eval.cpp` rather than by
  querying the binary.

---
id: S-0039
type: session
agent: researcher-architect
round: 4
title: e0013-band-retired-artifacts-pinned-ruling-correction
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-27
closed: 2026-09-27
---

# S-0039 — Session (researcher-architect)

> One session record per agent session, written to disk BEFORE the chat ends. It is
> the handoff to whoever runs next. Keep it short and factual; the records are the
> detail.

## The three rulings, in one line each
1. **F-U10 — the band `75,600..76,587` is RETIRED**, as a pre-key-change artifact. Not
   re-derived, not kept-frozen. It was a **yield-plausibility cross-check on the pipeline**,
   not a quality threshold; the quality rule is the unchanged 30,000 floor, which holds at
   59,892. Retired **before** E-00015/E-00014 run and before the floor is evaluated on any
   number that arms a scope claim. Full reasoning and costs in E-0013's Addendum 2, L2354+.
2. **F-U9 — the artifacts are hash-pinned in `research/`, NOT committed.** The 13 MB
   `positions.jsonl` is derived, regenerable, and would cost 13 MB again on every future key
   change; it also contradicts this repo's own E-0010 precedent. The manifest is the
   engineer's to write; the `.gitignore` change is not mine to make.
3. **CORRECTION to my own S-0037 ruling**: **no committed split map has ever existed.** The
   premise came from the ORCHESTRATOR's instruction and was false; I repeated it. Annotated,
   not edited. The invariance claim is unaffected and the pin is now *stronger*.

## Round / Work Items Touched
- Round 4. E-0013 only (review-licensed append at L2354+). W-0003 untouched and not claimed.
  HO-0005 not opened or closed. No work item closed here.

## What I Did (with evidence)
| # | Action | Evidence (command → result) | Calibration |
|---|---|---|---|
| 1 | Re-derived every S-0038 figure from the artifact bytes rather than inheriting it | parsed all 74,452 rows: **74,452 distinct `norm_fen`, 0 with >1 row**; `positions.jsonl` 13,004,718 B / 74,452 lines / `ac8c92f0...`; gates `0/0`, `overlap_zero true`; 59,892+14,560 = 74,452 | demonstrated |
| 2 | Recomputed `split_map.json`'s digest from its own 14,463 bytes | `bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea` = the tool's `SPLIT_MAP_SHA256_EXPECTED`, and = the old-key baseline's digest | demonstrated |
| 3 | Diffed both captured self-test name sets | 59 → 79; removed **exactly 1** (`dirty: the normalized-FEN invariant holds BECAUSE the dedup ran first`), added 21, kept 58 | demonstrated |
| 4 | Verified the "committed split map" premise is false | `1a2dff7` → only `tools/e0013_extract.py`; `git ls-files` matches nothing; `git log --all --name-only -- '*split_map*' '*positions.jsonl'` → **empty** | demonstrated |
| 5 | Found the band was **already out of band under the OLD key** | old-key run 76,593 vs `hi` 76,587, `comparison: "above"` — no measurement of this corpus has ever landed inside the band | demonstrated |
| 6 | **NEW FINDING**: the report's `src_commit` is `9f6574c`, the **parent** of `da93d9c` | the run predates the commit of its own code change; provenance field is stale | demonstrated |
| 7 | Verified the tactical suite against conjunct (f) | `tactics_set.py` `POSITIONS` = **73** entries (< N≥200), gitignored (`.gitignore:73`), EV-0006 `sha256: null` | demonstrated |
| 8 | Appended Addendum 2 to E-0013 | spliced onto the **HEAD blob** (the working copy had CRLF re-applied by `git checkout --`); `H_body` after = `c7ebe54c…bea7` / **22,196 B**; L1-2353 byte-identical to HEAD; CR=0; no BOM; `git diff --check` exit 0 | demonstrated |

## What I Did NOT Do (and why)
- Did **not** edit `tools/e0013_extract.py`, `tools/e0013_eval.py`, or anything under `src/`.
  So the band constants at L574-576 and self-test L930-932 are **still live and now known
  to be meaningless** — the engineer's edit, and I say so in the addendum.
- Did **not** run the extractor in any mode, including `--selftest`. Did not run E-00014 or
  E-00015. Did not fit anything, read the holdout, or read any label field.
- Did **not** change `SPLIT_SALT`, the dedup order, the survivor rule, the 30,000 floor, or
  the band.
- Did **not** edit E-0013's `status:` (still `RUNNING`) or any `result:` (still `null`), any
  H-####, any R-00xx, any CLOSED/VERIFIED record, HO-0005, or W-0003.
- Did **not** edit E-00014 or E-00015. Their required dated amendments are named in the
  addendum and are their executor seats' to file; I do not edit another seat's record to
  deliver my own ruling.
- Did **not** edit `.gitignore`, un-ignore any path, create a manifest, or commit any artifact.
- Did **not** edit the S-0037 addendum's text. Section 12 annotates it; nothing in it moved.

## Claims I Made That Are NOT Yet Verified
- **All three rulings are not self-certifying.** They go to **HO-0019** (verification-auditor,
  `REQUESTED`, undischarged) with S-0038's implementation. Neither this addendum nor
  S-0038 discharges Gate 3.
- The **F-U14 obligation** (build + hash-pin an N≥200 independent tactical suite) is newly
  named by me and has not been seen by any other seat.
- The section 9 `src_commit` staleness is my finding from reading the artifact; the engineer
  who owns the tool has not confirmed it.

## State Left On Disk
- E-0013: Addendum 2 appended at L2354+; `status: RUNNING`; no `result:`;
  `H_body` unchanged at `c7ebe54c…bea7` / 22,196 B.
- `tools/e0013_extract.py` untouched (`da93d9c`). Artifacts under `build/s41/extract_new/`
  untouched and **still uncommitted** — deliberately, per Ruling 2.
- E-00014, E-00015: both still `PENDING`, both still blocked. Nothing fitted, no holdout read.

## Next Action For The Successor
- **implementation-engineer**, under a handoff: (a) remove the band constants + self-test
  band checks, or mark the band retired in the report; (b) write the `research/` manifest
  pinning `positions_sha256`, `split_map_sha256` and `report.json`, and make the
  **full-mode** artifact at a clean commit; (c) narrow `.gitignore` if a commit is wanted;
  (d) F-U11 inner partition; (e) F-U12 survivor bias into Sample Validity.
- **systems-researcher**: file the dated amendments to E-00015 (band retired, rule 3
  replaced, stage 4 restated) and to E-00014 (L68 key), each **before** its pass.
- **F-U14, unowned**: the N≥200 independent suite. This blocks the pre-fit commit.

## Escalations (owner decisions needed)
- None blocking this seat's own work. Two items need another seat's decision: whether the
  extractor re-emits full-mode positions at a clean commit before any fitter reads it, and
  who owns F-U14.

## Environment Facts Learned
- `run_commands` reports **exit 1 on success**; take verdicts from `$LASTEXITCODE` and file
  contents. Confirmed again this session, repeatedly.
- PowerShell one-liners with nested `python -c` quoting are a reliable way to lose a session
  to a `SyntaxError` that the editor's auto-close parens introduced. Write a scratch `.py`
  under `build/s41/` with the editor and run it; the scratch is gitignored.
- E-0013 at `f12f1ce` ends with **no trailing newline** (`ends_with_newline False`, 2353
  split parts), so an append must supply its own leading `\n`. `git diff --check` wants no
  trailing blank line.

## Validation Status
- `H_body` recomputed **after** the edit: `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` / 22,196 B — equals the expected value and equals the same construction from `git show ce845c5:`.
- `python research/scripts/research.py validate` → exit 0, file contains `Validation OK`.
- `python research/scripts/research.py update` → exit 0, `updated: research/index.md`.
- `python research/scripts/research.py state --write` → exit 0, wrote `state.md` + `state.json`.
- `git diff --check` → exit 0, empty.
- Repo floor `build\Release\kana.exe` **not** re-run: no `src/` change and this seat changed
  no code. S-0038 verified it at `da93d9c`.
---
id: S-0035
type: session
agent: verification-auditor
round: 4
title: ho-0017-independent-audit-of-the-e-0013-l5-flip-r-0025-verified-q1-q8-no-revert
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-27
closed: 2026-09-27
---

# S-0035 — Session (verification-auditor)

> One session record per agent session, written to disk BEFORE the chat ends. It is
> the handoff to whoever runs next. Keep it short and factual; the records are the
> detail.

## Round / Work Items Touched
- Round 4. Took handoff **HO-0017** (audit the E-0013 L5-only flip, R-0024 Q1–Q8). Filed
  **R-0025** (`kind: verification`, reviewer `verification-auditor`) and this record, **S-0035**.
- **No work item was claimed or closed.** W-0003 stays `IN_PROGRESS` with `verified_by: null`;
  that obligation is unrelated to this handoff and remains unmet.

## What I Did (with evidence)
| # | Action | Evidence (command → exit code → result) | Calibration |
|---|---|---|---|
| 1 | Recomputed `H_body` on **five** revisions from raw bytes | `git cat-file blob <rev>:<E-0013>` → rc 0; all five = `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` / **22,196 B** | demonstrated |
| 2 | Recomputed `H_legacy` pre and post | `b04fd5a4…00ce6`/22,270 → `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144`/22,270; both statuses 15 B, so length invariant | demonstrated |
| 3 | Proved the flip is one line in one file at L5 | `git diff --numstat 6a6eb0a~1..6a6eb0a` → rc 0, `1 1 <path>`; `git diff -U0` → one `@@ -5 +5 @@`, `-status: PENDING` / `+status: RUNNING` | demonstrated |
| 4 | Checked the five front-matter fields | L5 `status: RUNNING`; L6/L7/L10/L14 byte-identical to `6a6eb0a~1` | demonstrated |
| 5 | Verified the `4478c3a..HEAD` boundary | `git diff --numstat` → rc 0, **1643/1**; `git diff -U0` → removed lines = **1**, exactly `-status: PENDING` | demonstrated |
| 6 | Swept all 11 commits touching E-0013 in range for L1–L428 hunks | only `6a6eb0a` edits inside the block; `f2b627c` lowest old-side line = **1729** | demonstrated |
| 7 | Census of `status: PENDING` at six revisions | `6a6eb0a~1`=14 → `6a6eb0a`=**13** (delta −1); HEAD(`8a92457`)=**23**; all 13 byte-identical across the flip | demonstrated |
| 8 | Governance sweep (C9) | E-00014/E-00015 both `PENDING`/`result: null`; 14 OPEN + 3 SUPERSEDED hypotheses; HO-0005 `REQUESTED`; `tools/`+`src/` = **0** commits in range; R-0019…R-0024 each touched only by their own authoring commit | demonstrated |
| 9 | Byte hygiene on every revision read | CR=0, trailing 0x0A, no BOM on all five + worktree; worktree byte-equal to HEAD blob | demonstrated |

**Verdict: C1–C7 and C9 all PASS. NO REVERT. The flip at `6a6eb0a` is VERIFIED** (Q1–Q8 all
VERIFIED). E-0013 legitimately remains `RUNNING`; it is not `COMPLETED` and nothing was measured.

## What I Did NOT Do (and why)
- **Did not edit E-0013 at all** — the audit passed, and a clean audit is not a licence to touch
  the thing audited. In particular I did **not** "fix" the stale `| 13 |` row: `8a92457` had
  already superseded it in place, correctly and outside 1–428.
- **Did not revert the flip.** Not required; no criterion failed.
- **Did not read the holdout**, and ran no training, fitting, extraction, counting, feasibility
  pass or SPRT generation. Set no `result:`. Changed no H-#### status.
- **Did not edit HO-0017**, so its stale embedded count of 24 stands; correcting another seat's
  handoff is the owner's action. I pinned the true figure to a commit in R-0025 instead.
- **Did not edit R-0019…R-0024**, any handoff, W-0003, HO-0005, `tools/`, `src/`,
  `state.md` or `state.json` (GENERATED — only via `state --write`).
- **Did not run the Gate 0 engine build** (`kana.exe`). Nothing in this handoff touched `src/`,
  so the floor is unaffected; I make no claim to have re-verified it.


## Claims I Made That Are NOT Yet Verified
- **None of my own.** Every figure in R-0025 is a recomputation, and each is re-derivable by any
  seat from the commands recorded in its Verification block. My one unreproducible *input* - the
  handoff's `status: PENDING` count of 24 - is reported as **not mine to fix** (measured 23).
- **R-0025 itself is a verification record, not a verified one.** It certifies the flip, not
  itself. If the project wants R-0025 independently re-checked, that is a fresh handoff.

## Environment Facts Learned
- This runner **reports exit 1 on commands that SUCCEED**, and its shell-integration capture is
  unreliable: during this session one batched call echoed the *same* output text for three
  different commands. Mitigation used throughout: redirect to a file with
  `| Out-File -Encoding utf8` and read the FILE.
- **Never let shell redirection touch a byte under test.** PowerShell `>` writes UTF-16 and
  `Set-Content -Encoding utf8` writes a BOM; each would silently destroy `H_body`/`H_legacy` and
  still *look* right. All hashing was done in Python reading `git cat-file blob` as raw bytes.
- Python's stdout on this machine is **cp1254**; `print()` of an em-dash or a BOM character
  raises `UnicodeEncodeError` and kills the script mid-run. Fixed by writing results with
  `io.open(..., encoding="utf-8")` and printing only ASCII.
- `git diff -U0` and `--numstat` **together** make git print the numstat line *and* the patch. My
  first C1 check parsed that combined output and wrongly reported "not 1 1". Reported in R-0025
  rather than quietly fixed: the raw output is part of the evidence.
- A hunk whose old-side count is **0** is a pure insertion, not a modification. A hunk-range screen
  that ignores this flags `ce845c5` (which *created* the L1-L428 block) as a body edit.

## State Left On Disk
- `research/reviews/R-0025-...-ho-0017.md` - the audit, `kind: verification`, COMPLETED,
  ~278 lines, CR=0, no BOM, trailing 0x0A, all template placeholders replaced.
- `research/sessions/S-0035-....md` - this record.
- Scratch scripts went to `$env:TEMP` only, never to the repo root (root is policy-checked).

## Next Action For The Successor
- **Nothing downstream is authorised by R-0025.** The lifecycle transition is verified; the
  *measurement* is not. E-0013 is `RUNNING` with no data. The build, extractor, trainer,
  parameter-table evaluator, feasibility pass and holdout read each still need a **separate,
  named authorisation** before any seat may begin. If the owner wants that, file it as a
  machine-readable handoff with runnable acceptance criteria, per HO-0017's own closing note.
- Optionally: the owner may wish to correct HO-0017's embedded count 24 -> 23 (pinned at `8a92457`).

## Escalations (owner decisions needed)
1. **HO-0017 carries a stale embedded figure** (`status: PENDING` = 24; true value 23 at
   `8a92457`). Owner action - I may not edit another seat's handoff.
2. **W-0003 remains `IN_PROGRESS` with `verified_by: null`.** It was out of scope here and I
   deliberately did not touch it. It will block `research.py round --round 4` until separately
   verified by a seat that is not its owner (`adversarial-reviewer`).
3. **The earlier Q6 criterion is formally withdrawn** as unsatisfiable; R-0025 is filed against
   the corrected criteria. No further action needed, but the withdrawal should be noted wherever
   the old wording is quoted.

## Validation Status
- `python research/scripts/research.py validate` -> PASS (warnings only, all pre-existing)
- `python research/scripts/research.py update` -> regenerates `research/index.md`
- `python research/scripts/research.py state --write` -> regenerates `state.md` + `state.json`
- `git diff --check` -> rc 0, empty (no whitespace damage)

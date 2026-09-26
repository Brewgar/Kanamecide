---
id: R-0025
type: review
reviewer: verification-auditor
target: E-0013
kind: verification
status: COMPLETED
example: false
created: 2026-09-27
---

# R-0025 — Independent audit of the E-0013 L5-only lifecycle flip (R-0024 Q1–Q8), under HO-0017

## Scope and standing

**Fresh seat, nothing inherited.** I occupy `verification-auditor`. The flip at `6a6eb0a` was
made by the `researcher-architect` seat. SYSTEM.md §1 forbids the owner verifying its own claim;
HO-0017 says the same; and **a condition cannot be discharged by the seat that performed the
act.** I therefore recompute every figure from the repository's own bytes and accept nothing
from the handoff's account — including its numbers.

I ran **no** training, fitting, extraction, counting, feasibility pass or SPRT generation. I read
**no** holdout. I set **no** `result:`. I changed **no** H-#### status. I did not open or close
HO-0005 or W-0003. I did not edit R-0019…R-0024, E-0013, or any handoff. I touched no `tools/`
or `src/` file. **E-0013 was not edited at all** — it did not need it, and a clean audit is not
a licence to touch the thing audited.

**Method.** All hashing was done by a Python script I wrote, reading `git cat-file blob` output
as **raw bytes** and splitting on `0x0A` only, with no normalisation, no newline translation and
no text-mode read. This is deliberate: the environment hazards in this repository (PowerShell
`>` emitting UTF-16, `Set-Content -Encoding utf8` emitting a BOM) would each silently destroy
the very bytes under test, so no shell redirection was allowed anywhere near the measurement.

## Verdict — Q1 through Q8, and the corrected criteria C1–C9

| # | Criterion | Expected | **My recomputed measurement** | Verdict |
|---|---|---|---|---|
| C1 | one line, one file, and that line is L5 | `1 1`, single `@@ -5 +5 @@` | `1 1 <path>`, 1 file, 1 hunk `(5,1)`, `-status: PENDING` / `+status: RUNNING` | **PASS** |
| C2 | L5 = `status: RUNNING`; L6/L7/L10/L14 untouched | five exact values | L5 `b'status: RUNNING'`; L6 `result: null`, L7 `elo_change: null`, L10 `owner: null`, L14 `completed: null`, all byte-identical to `6a6eb0a~1` | **PASS** |
| C3 | **`H_body` UNCHANGED**, 22,196 B, not 22,270 | `c7ebe54c…bea7` / 22,196 | `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` / **22,196 B** on **all five** revisions `ce845c5`, `6a6eb0a~1`, `6a6eb0a`, `f2b627c`, `HEAD` | **PASS** |
| C4 | `H_legacy` moved, length invariant | `d8add61c…e6144` / 22,270 | pre `b04fd5a4…00ce6`/22,270 → post `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144`/**22,270**; delta 0 | **PASS** |
| C5 | `4478c3a..HEAD` deletions == 1, and it is `-status: PENDING` | exactly one, identified | removed lines = **1**, and it is exactly `-status: PENDING`; insertions 1,643 (not a criterion) | **PASS** |
| C6 | pre-write assertion **evidenced** | L5 was `status: PENDING` | `6a6eb0a~1` L5 = `b'status: PENDING'`, 15 B, blob 145,308 B; post blob also 145,308 B | **PASS** |
| C7 | no other commit smuggled an L1–L428 body edit | only the flip | 11 commits touch E-0013 in range; only `6a6eb0a` edits inside 1–428 (see the `ce845c5` note below) | **PASS** |
| C8 | `status: PENDING` fell by exactly 1 across `6a6eb0a`; survivors intact | −1 | **14 → 13**, delta −1; all 13 byte-identical across the flip | **PASS** (with an observation, below) |
| C9 | nothing ran; no holdout; no `result:`; governance untouched | all null | `result: null`, `completed: null`; E-00014/E-00015 both `PENDING`/`null`; 14 OPEN + 3 SUPERSEDED hypotheses; HO-0005 `REQUESTED`; W-0003 `IN_PROGRESS`; `tools/` and `src/` have **zero** commits in range | **PASS** |

**NO REVERT IS REQUIRED. C1–C7 and C9 all hold on recomputation.** The flip stands, and it
stands on evidence I produced rather than on the author's account of it.

**Q1–Q8 mapping.** R-0024's Q1 = C3, Q2 = C1, Q3 = C1 (hunk line number), Q4 = C8, Q5 = C4,
Q6 = C5, Q7 = C1 (`git diff --check`, rc 0, empty), Q8 = C1 (no other file in the commit).
Each carries the verdict in the table above. **All eight: VERIFIED.**

## The load-bearing invariant, and why its byte count is the whole audit

`H_body` is the only quantity in this record that is **invariant under exactly the legal
transitions and sensitive to exactly the illegal ones.** I recomputed it five times, from raw
bytes, on both sides of the flip and at HEAD:

```
ce845c5   H_body = c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7 / 22196 B
6a6eb0a~1 H_body = c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7 / 22196 B
6a6eb0a   H_body = c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7 / 22196 B
f2b627c   H_body = c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7 / 22196 B
HEAD      H_body = c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7 / 22196 B
```

**It reads 22,196 bytes and not 22,270.** That is the positive proof, and it is the only figure
in this audit that carries the argument by itself: 22,196 means the write fell **inside** the
five-field exclusion `{5,6,7,10,14}`; had L5 been edited outside the exclusion the protected
range would have moved and the digest with it. The distinction is arithmetic, not editorial:
deleting five lines from a 22,270-byte block whose contents are 15, 12, 16, 11 and 15 bytes plus
five terminators (74 bytes) yields exactly 22,196, and that is what I measured.

`H_legacy` I derived rather than accepted, and the **length invariant** is what makes C4
meaningful: `status: PENDING` and `status: RUNNING` are **both 15 bytes**, so replacing L5 moves
the digest and provably cannot move the length. Pre `b04fd5a4…00ce6`/22,270 → post
`d8add61c…e6144`/22,270. The digest moved; the byte count did not. Exactly as projected.

## Byte hygiene (this repository's known corruption vector)

Checked on every revision I read, because a restore once re-applied CRLF here and silently
corrupted LF-protected bytes:

| Revision | bytes | CR count | ends 0x0A | BOM |
|---|---|---|---|---|
| `ce845c5` | 73,719 | **0** | yes | no |
| `6a6eb0a~1` | 145,308 | **0** | yes | no |
| `6a6eb0a` | 145,308 | **0** | yes | no |
| `f2b627c` | 147,636 | **0** | yes | no |
| `HEAD` | 159,338 | **0** | yes | no |
| worktree | 159,338 | **0** | yes | no |

**worktree bytes == HEAD blob bytes: True.** No restore was needed, so none was performed.

## Observations — reported, not failed

**1. The orchestrator's earlier Q6 wording was UNSATISFIABLE; this audit is filed against the
corrected criteria.** The withdrawn draft said insertions rise by 1 and "deletions remain zero".
That cannot hold: L5 lies *inside* the compared range, so replacing it is **one deletion at that
boundary by construction**, and no line-anchored edit of L5 could ever yield 0 deletions. I
measured **1,643 insertions / 1 deletion** at `8a92457` and **1,441 / 1** at `6a6eb0a` itself.
R-0023's Rule F already framed this as a bounded exception of exactly one deletion, and R-0024's
own Q6 states 1441/1. Judged against the contract and the ruling rather than the tidier number,
the correct form is the one the record already adopted: the zero-deletion property survives as a
**bounded exception of exactly one deletion, and that deletion is the flip itself**. I checked
that the exception is *exactly* bounded: across the whole `4478c3a..HEAD` range the removed-line
set has cardinality **1**, and its single member is `-status: PENDING`. No other line of the
addendum was deleted anywhere in the range.

**2. C8's raw count is a MOVING TARGET and the embedded figure is STALE — pinned here.**
Measured, not inherited: `ce845c5`=3, `4478c3a`=2, `6a6eb0a~1`=**14**, `6a6eb0a`=**13**,
`f2b627c`=**13**, `8a92457`(HEAD)=**23**. The handoff's embedded **24** does **not** reproduce;
the real figure at HEAD is **23**, so the embedded count is stale by 1 and I record it as such.
This is **an observation, not a failure**, for the reason the record itself already gave
correctly at its §4: a document that reports a count of a string **creates occurrences of the
string it counts**. The invariant that actually matters is the positional one, and that one
holds — **all 13 quoted occurrences are byte-identical across the flip**, at L20, 435, 456,
1132, 1270, 1363, 1394, 1435, 1557, 1565, 1574, 1576, 1865. **Pinned to `8a92457`: 23.**
One of those rows, the `| 13 | E-0013 front matter |` line, was later revised **in place** by
`8a92457` (now L1903, marked **SUPERSEDED (S-0034)**) because it had gone stale on the flip.
That is a correction by a later commit at a line **outside 1–428**, it is disclosed in the diff,
and it is the opposite of a covert edit. **I did not edit the handoff to fix its count**; I
report the measured figure and pin it here.

**3. `ce845c5` intersects lines 1–428 but did not edit the block — it created it.** My first
sweep flagged `ce845c5` for a hunk starting at old-line 425. I chased it rather than waving it
through, and the resolution matters: the hunk is `@@ -425,0 +426,648 @@`, a **pure insertion of
648 lines** into a file that was **426 lines long**. The L1–L428 block **did not exist before
`ce845c5`** — `ce845c5` is the *pinned baseline* the hash is defined against, not a body edit.
Across the range, the only commit that edits inside the established 1–428 block is `6a6eb0a`, at
L5. I report the flag because a hunk-range screen that ignores insertion-vs-modification would
produce a false positive here, and the next seat should not be misled by it.

**4. `f2b627c` (Z4) is clean, as required.** Its two hunks are `@@ -1729 +1729 @@` (the Z3
column header) and `@@ -1762,0 +1763,38 @@` (the appended Z4 section). **The lowest old-side
line it touches is 1729, far outside 1–428.** No body edit.

**5. Byte hygiene note for whoever touches this file next.** I did **not** restore any file, so
the CRLF re-application hazard did not fire and `H_body` needed no post-restore recomputation.
I flag the standing hazard rather than leaving it implicit: a `git checkout -- <E-0013>` on this
path would re-apply CRLF, and the result would still *look* correct while silently breaking
every hash above. If a future seat must restore this record, re-verify 0 CR + trailing 0x0A and
**recompute `H_body` afterwards** — do not assume the tables above survive a restore.

## Authorisations — what this audit does and does not permit

- **C1–C7 and C9 pass. No revert. The flip at `6a6eb0a` is VERIFIED**, and the flip is now
  *evidenced*, which is what HO-0017's acceptance criterion 1 asked for.
- **The authorisation for the flip was never mine to grant.** It rests on R-0024's P1–P5
  pre-condition, which that review recomputed for itself. This audit **evidences** the
  authorisation; it does not extend it.
- **Nothing downstream is authorised by this record.** No seat may read "the flip verified" as
  "the measurement may begin". Q1–Q8 covered the lifecycle transition and nothing else. The
  build, the extractor, the trainer, the parameter-table evaluator, the feasibility pass and the
  holdout read each remain **unauthorised** until a separate, named authorisation says so.
- **E-0013 remains `RUNNING`, and it is not `COMPLETED`, and nothing has been measured.** No
  `result:` was set, no fitted artifact exists, and no H-#### status moved.

## What I could NOT reproduce, and why

Only one figure, and it is reported above as an observation rather than buried: the **embedded
`status: PENDING` count of 24** in HO-0017's account. I measure **23** at `8a92457`. The cause is
identified rather than mysterious — the count is self-invalidating, and the record's own §4
already explains the mechanism correctly. Per HO-0017's acceptance criterion 3, stating a figure
I could not reproduce *with its cause* is the standard to follow here, not a failure of the audit.

---

## Verification Block (kind: verification only)

- **Work item verified:** HO-0017 / the E-0013 lifecycle flip at `6a6eb0a` (round 4). Note: this
  is **not** a claim on W-0003, which I did not open or close and whose `verified_by` remains
  `null`; W-0003's own verification is a separate, still-unmet obligation.
- **Verified by:** `verification-auditor` (a different seat from `researcher-architect`, the
  author of the flip — Gate 3 satisfied; `verified_by != owner`).
- **Verdict:** **VERIFIED** (Q1–Q8 all pass; C1–C7 and C9 all pass; no revert)
- **Audit seat ran at:** HEAD = `8a92457` (== `origin/master` at audit time), clean tree, and
  `git pull --ff-only` reported "Already up to date." **Environment note:** this runner reports
  exit 1 on commands that SUCCEED, so no exit code below is taken from the wrapper; each is the
  value captured inside the script from the child process itself.
- **Commands re-run by me (raw output retained):**
  1. `git pull --ff-only` → **rc 0**; observed: `Already up to date.`
  2. `git status -sb` → **rc 0**; observed: `## master...origin/master` (no ahead/behind, no
     dirty entries).
  3. `git diff --numstat 6a6eb0a~1..6a6eb0a` → **rc 0**; observed:
     `1<TAB>1<TAB>research/experiments/E-0013-h-0013-…-stage-5.md`. Fields = 3, insertions
     `1`, deletions `1`. *(C1. My first attempt combined `--numstat` with `-U0`, which makes git
     print the numstat line **and** the patch; that produced a false "not 1 1" and I re-ran it
     clean. The raw output is reported here, including my own mis-parse.)*
  4. `git show 6a6eb0a --numstat --format=` → **rc 0**; observed: `1\t1\t<path>`.
  5. `git diff -U0 6a6eb0a~1..6a6eb0a` → **rc 0**; observed, whole commit:
     `diff --git a/…E-0013….md b/…E-0013….md` / `index fd2fa24..9e328ad 100644` /
     `@@ -5 +5 @@ title: "E-0013 — H-0013 Texel fit …"` / `-status: PENDING` /
     `+status: RUNNING`. **1 hunk, range (5,1), 1 file.**
  6. `git show 6a6eb0a --name-only --format=` → **rc 0**; observed: exactly
     `['research/experiments/E-0013-h-0013-…-stage-5.md']` — **no other file** (Q8).
  7. `git diff --check 6a6eb0a~1..6a6eb0a` → **rc 0**, output `''` (Q7).
  8. `git diff --numstat 4478c3a..HEAD -- <E-0013>` → **rc 0**; observed: **`1643 / 1`**.
     Also measured: `4478c3a..6a6eb0a~1` = `1440/0`, `4478c3a..6a6eb0a` = `1441/1`,
     `4478c3a..f2b627c` = `1479/1`. The whole-tree `4478c3a..HEAD` listing is **not
     comparable**; E-0013's own line within it is `1643 / 1`.
  9. `git diff -U0 4478c3a..HEAD -- <E-0013>` → **rc 0**; observed **removed lines = 1**, the
     single member being exactly `-status: PENDING`; added lines = 1,643; 2 hunks (C5).
  10. `git log --format=%h --reverse 4478c3a..HEAD -- <E-0013>` → **rc 0**; 11 commits:
     `ce845c5 f450976 fce355c c23803f b7179f3 8c30f32 dc8f9fc 049c81d 6a6eb0a f2b627c
     8a92457`. Per-commit `git show <c> -U0 --format= -- <E-0013>` hunk ranges vs lines 1–428:
     `ce845c5 (425,0)` [pure insertion — Observation 3], `f450976` 0, `fce355c` 0, `c23803f` 0,
     `b7179f3` 0, `8c30f32` 0, `dc8f9fc` 0, `049c81d` 0, **`6a6eb0a` (5,1)**, `f2b627c` 0
     (its ranges are `(1729,1)` and `(1762,0)`), `8a92457` 0 (C7).
  11. `git show f2b627c -U0 --format= -- <E-0013>` → **rc 0**; hunks `@@ -1729 +1729 @@` and
     `@@ -1762,0 +1763,38 @@`; lowest old-side line **1729** (C7).
  12. `git cat-file blob <rev>:<E-0013>` for `ce845c5`, `6a6eb0a~1`, `6a6eb0a`, `f2b627c`, `HEAD`
     → **rc 0** each; raw bytes hashed as described (C3/C4/C6/C8, and hygiene).
  13. `git log --format=%h 4478c3a..HEAD -- tools/` and `… -- src/` → **rc 0** each; observed:
     **empty, no commits** (C9).
  14. `git log -1 --format=%h 4478c3a..HEAD -- <each of R-0019…R-0024>` → R-0019 **none**;
     R-0020 `a6394f5`, R-0021 `d3ce887`, R-0022 `8db1c45`, R-0023 `f03613e`, R-0024 `f86801a`
     — each is that record's **own authoring commit**, so each was written once and never edited
     again. **No R-0019…R-0024 record was modified by any later commit** (C9).

- **Artifacts checked (recomputed from raw bytes, not copied):**
  - `research/experiments/E-0013-…-stage-5.md` at `ce845c5` — 73,719 B, CR=0, trailing 0x0A, no BOM
  - same at `6a6eb0a~1` — 145,308 B, CR=0, trailing 0x0A, no BOM
  - same at `6a6eb0a` — 145,308 B, CR=0, trailing 0x0A, no BOM
  - same at `f2b627c` — 147,636 B, CR=0, trailing 0x0A, no BOM
  - same at `HEAD` / worktree — 159,338 B, CR=0, trailing 0x0A, no BOM, **byte-equal**
  - `H_body` (L1–L428 minus L{5,6,7,10,14}, re-terminated 0x0A, split on 0x0A only) —
    **SHA-256 `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` / 22,196 B**,
    identical on all five revisions
  - `H_legacy` (L1–L428, re-terminated 0x0A) — pre-flip SHA-256
    `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6` / 22,270 B;
    post-flip SHA-256 `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144` /
    22,270 B
- **What I reproduced independently:** every figure above. In particular, both hash pairs on both
  sides, from raw bytes with the byte counts; the exclusion arithmetic; the length-invariance
  proof; the `1 1` numstat and the single `@@ -5 +5 @@` hunk; the identity of the one removed
  line across the whole `4478c3a..HEAD` range; the per-commit hunk sweep against lines 1–428;
  the `status: PENDING` census at six revisions; the front-matter field census; and the
  governance cells (sub-contract statuses, hypothesis statuses, HO-0005, W-0003, the
  R-0019…R-0024 edit history, `tools/`, `src/`).
- **What I could NOT reproduce (and why):** the handoff's embedded `status: PENDING` count of
  **24**; I measure **23** at `8a92457`, pinned above. Cause identified, not mysterious: the
  count is self-invalidating, since documenting a count of a string adds occurrences of it. I did
  not edit HO-0017 (not my write authority); the true figure is pinned to a commit in this record.
- **Sample validity re-checked:** **not applicable, and deliberately not performed.** This audit
  concerns a lifecycle metadata transition, not a measurement: no sample was drawn, no arm
  exists, no statistic was computed, and the holdout was **not** read. There is nothing to check
  for arm differentiation, independence or power, and manufacturing such a check would be
  theatre. I record the non-applicability explicitly rather than leaving the field silently blank.
- **Claims that must be corrected in the record:**
  1. **The earlier Q6 criterion is unsatisfiable as written** and is withdrawn — "insertions +1
     and deletions remain 0" cannot hold for a line-anchored edit of a line lying inside the
     compared range. Correct form, measured: **1 deletion, and that deletion is
     `-status: PENDING`.**
  2. **HO-0017's embedded `status: PENDING` count of 24 is stale**; the true figure is **23** at
     `8a92457`. Correcting the handoff is the owner's action, not mine.
  3. **No correction is owed to E-0013.** Its §5/§6 figures reproduced exactly (`1441/1`,
     `d8add61c…e6144`/22,270, `c7ebe54c…bea7`/22,196), and its own §4 already flagged the
     self-invalidating-count trap correctly. The one row that went stale on the flip was already
     corrected in place and labelled **SUPERSEDED (S-0034)** by `8a92457`.
- **Residual uncertainty (calibrated):** **demonstrated** for C1–C7 and C9 — each is a
  deterministic byte-level or commit-graph fact, recomputed from the repository, and any future
  seat can re-derive them with the same few lines of Python. The single soft item is C8's raw
  count, and there the residual uncertainty is not in the *method* but in the fact that **any**
  count of a self-referential string is stale the moment it is written. That is a property of the
  instrument, is already documented by the record, and is precisely why I verified the
  **positional** invariant and merely pinned the raw count.

## Date
2026-09-27


---
id: S-0004
type: session
agent: verification-auditor
round: 5
title: HO-0001: verification of the DEC-0011 derived-intelligence layer (PARTIAL - 4 named gaps)
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-19
closed: 2026-09-19
---

# S-0004 — Session (verification-auditor)

> One session record per agent session, written to disk BEFORE the chat ends. It is
> the handoff to whoever runs next. Keep it short and factual; the records are the
> detail.

## Round / Work Items Touched
- **W-0007** (round 5, owner: chief-architect) — independent verification via **HO-0001**.
  Verdict: **PARTIAL** (see `reviews/R-0006-…`); W-0007 stays OPEN.
- Note: this file's name says "3-named-gaps" because it was scaffolded before the fourth gap
  (G5, the block-style-YAML gate defect) was found; the front-matter title above is current.
  The file is not renamed: a rename would show up as a git delete+add, and the record id
  (S-0004) is what the links use.

## What I Did (with evidence)
| # | Action | Evidence (command → exit code → path) | Calibration |
|---|---|---|---|
| 1 | Bootstrap per SYSTEM.md §11 with zero chat history | `status --brief` / `next` / `validate` → exit 0 (`context/_bootstrap_*.txt`) | demonstrated |
| 2 | Ran HO-0001's exit checks myself | `selftest` 0 (35 tests); `validate` 0 (0 problems, 18 warnings); `state --write` ×2 → byte-identical `state.json`; `search "quiescence stand-pat"` → E-00008 rank 0; `kgraph.py beliefs --json` → exit 0 (`context/_ho0001_report2.txt`) | demonstrated |
| 3 | Recomputed artifact hashes rather than copying them | `Get-FileHash build\Release\kana.exe` = `504EB01A…A6DAA` = EV-0010 (`context/_ho0001_kana_sha.txt`) | demonstrated |
| 4 | Tested that the gates still bite, by adversarial mutation on a sandbox copy (real corpus untouched) | 6 designed gates exit 1; 4 anchor mutations exit 0 (`context/_ho0001_report{3,4,5}.txt`) | demonstrated |
| 5 | Found G1: `PERFT_ANCHOR` row 1 leaves the five startpos counts unasserted | 4 mutations of the certified table → `validate` exit 0 (`context/_ho0001_report4.txt`) | demonstrated |
| 6 | Found G2: committed `state.{md,json}` were stale at commit | `git diff -U0 research/state.md` vs the corpus → records 118→119, session 2→3, edges 852→866 | demonstrated |
| 7 | Found G3: `audit`'s `problems` is orphaned from `validate`; message mislabels the kind | `audit --json` → problems=1 vs `validate` exit 0; probe6 names the record (`context/_ho0001_report6.txt`) | demonstrated |
| 8 | Checked the no-rewrite acceptance clause at byte level | `git diff --name-status 7162357 4dbb89e` → 5 M / 37 A / 0 D; 0 M in record dirs (`context/_ho0001_fullnm.txt`, `_ho0001_recdel*.txt`) | demonstrated |
| 9 | Filed the review, filled HO-0001's Response + Verification, set W-0007's verification fields | `reviews/R-0006-…`, `handoffs/HO-0001-…`, `work/W-0007-…` | demonstrated |
| 10 | Found G5 (Round-5 blocker) after the first pass: a block-style `evidence:` list is invisible to `parse_simple_yaml`, so gate 1 falsely rejects a correct DONE | sandbox cases B vs C: DONE+VERIFIED with block evidence → validate exit 1 / `round` PASS; with inline evidence → validate exit 0 (`context/_ho0001_report{7,8,9}.txt`) | demonstrated |
| 11 | Verified the layer polices new artifacts too: my own review draft created a dangling-id warning, which I then removed | `validate` warning `dangling id … referenced by ['reviews/R-0006-…']`, gone after rewording | demonstrated |

## What I Did NOT Do (and why)
- **No Gate 0.** Every `kana.exe` run (Release, Audit, a copy outside `build/`, and via
  `runjob.py launch --retry 8`) returned exit 4551 — Device Guard. No engine count, NPS value
  or test result was produced by me; I did not substitute the inherited numbers for a run.
- **Did not fix G1/G5/G2/G3.** `src/` and `research/scripts/` are outside my write authority, and
  G5's one-line fix is inside W-0007 — *another agent's record body* (I may write only its
  `## Verification` section). The fixes belong to the owner/tooling agent. I regenerated only
  `research/state.{md,json}`, which the handoff itself required me to run (`state --write`), and
  which fixes G2's artifact on disk.
- **Did not mark W-0007 DONE** and did not touch `project_state.md`, `SYSTEM.md`, `SCHEMA.md`
  or any other agent's record body (profile.md write authority).
- **Did not test `contradictions` firing on R-0005 F16's motivating case** — it returns 0
  candidates today, so the detector's positive case is untested (proposed as experiment 4).

## Claims I Made That Are NOT Yet Verified
- G1's severity claim ("five of ten certified counts can be altered undetected") is verified
  for those five numbers in a sandbox copy; that the same hole lets a *differently worded* edit
  through is **likely**, not tested.
- My reading that R-0005 F16's motivating conflicts became moot after the 2026-09-09 renumbering
  is **speculative** — untested; needs the H-0005/H-0006/D-0003 record history.
- I did not independently re-run `build.bat`, so I cannot say whether a fresh build would also
  be Device-Guard-blocked (the copy of the existing binary was, which suggests a content/policy
  match rather than a path rule).

## Environment Facts Learned
- **`kana.exe` cannot be executed in this environment.** Every invocation returned
  **exit 4551** — `'…\build\Release\kana.exe' was blocked by your organization's Device Guard
  policy`. 20 consecutive attempts through the documented retry loop (`g0_perft.bat`-style
  `cmd /c` + `findstr` pattern), `build\Audit\kana.exe`, a copy at
  `research/context/_kana_copy.exe`, and `runjob.py launch --retry 8 --retry-delay 3 --probe 2`
  (which raises `OSError: [WinError 4551]` inside `subprocess`/`CreateProcess`) — **all
  blocked**. So the documented "intermittently blocks freshly built unsigned exes" hazard is
  currently a hard block, and the documented workarounds do not work. A copy of the binary is
  blocked too, which points at a content/hash-based policy rather than a path rule (**likely**,
  not tested with a fresh build).
- Shell realities (as documented in AGENT_MEGAPROMPT §4) confirmed again: PowerShell `>`
  redirects write **UTF-16LE**, which mangles the em dash in the layer's output. Capture JSON
  through `subprocess` with `encoding="utf-8"` (my probes) or `cmd /c`, not through `>`.
  Foreground command output capture through the tool is unreliable; always read the file.
- `runjob launch` refuses (WinError 4551) *before* any RUN record is useful here — the launch
  aborts, so no RUN record was filed for the Gate 0 attempts (they are logged in
  `context/_gate0_auditor_attempts.txt`).

## State Left On Disk
- `research/reviews/R-0006-independent-verification-of-the-dec-0011-derived-intelligence-layer-ho-0001-w-0007.md`
  (new; `kind: verification`, COMPLETED, verdict PARTIAL).
- `research/handoffs/HO-0001-verify-dec-0011-layer.md` — status REQUESTED → **DONE**, with the
  receiver's Response + Verification sections filled (raw exit codes, hashes, verdict).
- `research/work/W-0007-derived-intelligence-layer.md` — `verified_by` /
  `verification_verdict: PARTIAL` set and the `## Verification` section filled; **status left
  OPEN** (the owner's call; gate 3 forbids DONE on a PARTIAL verdict).
- `research/sessions/S-0004-…md` (this record).
- `research/state.{md,json}` — **regenerated** by my required `state --write` runs and now
  current with the corpus (this is G2's fix on disk; it needs a commit).
- Gitignored scratch (not records): `research/context/_ho0001_probe{,2,3,4,5,6}.py`,
  `_ho0001_report{,2,3,4,5,6}.txt`, `_v2_*`, `_gate0_auditor*`, `_ho0001_*` captures.
  No new files in the repo root; the hygiene gate stays green.
- Note for the reader: my session record takes the next free id **S-0004**, which coincidentally
  matches a pre-existing *dangling* reference `S-0004` in `experiments/E-00009-…md:145`
  ("S-0004/mandes …"). That warning will disappear from `validate` now, but it is a **false
  resolution**: E-00009's `S-0004` is some other, never-written record, not this session.

## Next Action For The Successor
1. **Fix G5 first — it is the actual Round-5 blocker, and it is one line.** Rewrite W-0007's
   `evidence:` block sequence as an inline list (same content), so DEC-0009 gate 1 can see it;
   without this, a DONE+VERIFIED W-0007 makes `validate` exit 1. (`templates/work_item.md`
   already emits inline lists; the record was hand-written in block style.) Better still, teach
   `parse_simple_yaml` block sequences and add a `validate` warning for unparsed list fields.
2. **Fix G1** (same class, also small): split `PERFT_ANCHOR` row 1 into one row per startpos
   count (or assert `|4865609|`-style stripped cells), then add the mutation test to
   `tests_memory.py` so the hole cannot come back. `project_state.md` advertises the guarantee
   the code does not provide.
3. Decide G3 (wire `M.audit()['problems']` into `validate`, or demote the channel and fix the
   message text), and consider the stale-state warning proposed as experiment 3 in R-0006.
4. Commit the regenerated `research/state.{md,json}` (G2) together with the new records.
5. Then request a re-verification of W-0007 by a *different* fresh agent (the seat is rotating —
   I must not re-verify my own review).
6. Independently: remediate Gate 0 (owner) so the next agent can prove the floor.

## Escalations (owner decisions needed)
1. **Gate 0 is unrunnable on this machine** (exit 4551 on every `kana.exe`, including a copy and
   `build\Audit\kana.exe`). Per AGENT_MEGAPROMPT §5 this is a stop-and-escalate condition: the
   correctness floor cannot be proven, and no engine claim can be verified from this environment.
   Needs an allow-list or a different host. Until then, only artifact *identity* (hashes) can be
   checked here — not behaviour.
2. **Round 5 cannot close on the current artifacts.** `round --round 5` exits 1 by design
   (W-0007 OPEN/PARTIAL), and even after the substantive gaps are fixed, G5 would make
   `validate` reject W-0007's DONE claim while `round` passes it. The owner should fix G5 (or
   the parser) before setting W-0007 DONE.
3. **`project_state.md` lines 53-55 overstate the anchor gate** (G1). Either make the text true
   by fixing `PERFT_ANCHOR`, or soften the text. The project should not advertise a guarantee it
   does not have on 5 of its 10 sacred counts.
4. **`research/scripts/` is outside the verification-auditor's write authority**, so I could not
   land the small fixes I verified. Someone with tooling authority must.
5. Optional: `agents/researcher-architect/reports/2026-09-09-placeholder.md` is a mis-typed
   placeholder (`type: hypothesis`, no `status`) that produces the lone `audit` problem; it is
   also a dangling-id source. It is another agent's record — needs that agent's decision.

## Validation Status
- `python research/scripts/research.py validate` → **exit 0, `Validation OK`** (0 problems;
  18 advisory warnings: 9 grandfathered legacy pre-registration, 9 dangling-id).
- `python research/scripts/research.py selftest` → exit 0, `Ran 35 tests … OK`.
- `python research/scripts/research.py update` → index.md regenerated (exit 0).
- `python research/scripts/research.py state --write` → `state.{md,json}` rewritten (exit 0);
  unchanged-since-verification besides the new records' timestamps.
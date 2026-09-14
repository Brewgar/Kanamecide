---
id: ROUND4
type: round_megaprompt
title: "Round 4 — data pipeline + E-0010 resolution + reviewer onboarding"
status: ACTIVE
created: 2026-09-14
example: false
---

# AGENT MEGAPROMPT — ROUND 4 (operational; any agent can execute it)

> You are running a Round-4 session. Standing prompt first (`AGENT_MEGAPROMPT.md`), then
> this file, then your role's `profile.md`. Round exit criterion:
> `python research/scripts/research.py round --round 4` exits 0.

## Round goal
One sentence: **stand up the self-play data pipeline (E-0011) under the new verification
system, resolve E-0010's two open items, and prove the fresh-reviewer path works.**

## Work items (already opened; `research.py work` to list)

- **W-0001 — E-0011 self-play data pipeline** (owner: systems-researcher; code:
  implementation-engineer).
  Step 1: researcher-architect files E-0011 (PENDING) with pre-registered decision rule,
  power ("what N settles it"), and sample-validity plan; adversarial-reviewer critiques
  it before `status: RUNNING`. Step 2: implementation. Step 3: run under `runjob.py`
  (RUN record, heartbeat, checkpoint, resume; ≤ 2 engine pairs).
  Exit check: generator produces ≥ 1,000 legal, deduplicated, provenance-carrying games
  (JSONL, legal-move-flushed); `duplicate-move-lists=0`; a fresh agent resumes the job
  from checkpoint and the game count only grows.
- **W-0002 — recalibrate the E-0010 effect-size rule** (owner: adversarial-reviewer).
  Open D-0007 on what the decision rule for eval-strength deltas should have been at
  N=240 (CI95 half-width ~±47 ⇒ ≥150 was unwinnable); file DEC-0010 with the calibrated
  rule (screening vs confirmatory bars, power analysis). The E-0010 record itself is NOT
  edited; its resolution is an addendum review + the new decision.
  Exit check: DEC-0010 ACTIVE, cites E-0010's measured CI; E-0010 outcome re-stated
  (PASS/FAIL/INCONCLUSIVE) under the calibrated rule in the addendum, not by rewrite.
- **W-0003 — Round-2 AGREEMENT_MATRIX backfill** (owner: adversarial-reviewer).
  The reviewer's matrix column was left empty in Round 2. Close it as a new review
  record (R-#### addendum) covering the Round-2 items the column should have addressed;
  the matrix file itself stays untouched as a historical artifact.
  Exit check: review record COMPLETED, names the Round-2 artifacts reviewed.
- **W-0004 — fresh-reviewer onboarding proof** (owner: verification-auditor seat ×2).
  Two brand-new agents bootstrap from the repo alone (research/README.md →
  AGENT_MEGAPROMPT.md → profile → `status --brief` → Gate 0) and each delivers one
  `kind: verification` review of E-0010: re-run `python e0010_report.py`, recompute the
  ladder numbers, check `duplicate-move-lists=0`.
  Exit check: two verification reviews COMPLETED with verdicts; each lists any number
  that did NOT reproduce.
- **W-0005 — E-SPRT-lite comparison harness pre-registration** (owner: researcher-architect;
  build: systems-researcher). Two-tier error control (screening δ≈20 Elo; regression
  δ=5; LLR ±2.944; game cap → INCONCLUSIVE), implemented as a resumable runjob job.
  Exit check: harness decides a known-difference pair (stage-6 vs stage-0) within its
  pre-registered bounds, and its decision matches the E-0010 measurement's sign.
- **W-0006 — root-scratch debt reduction** (owner: implementation-engineer).
  Shrink `research/scripts/root_grandfathered.txt`: delete confirmed-junk scratch,
  move anything worth keeping into `research/` or `tools/`, keep `e0010_report.py` and
  raw E-0010 evidence (they reproduce a published result). Log every deletion.
  Exit check: validate OK; grandfathered list updated; deletions itemized in the work item.

## Ordering and verification
- W-0004's verifiers must not be W-0001/W-0002 owners. Every work item closes with
  `verified_by ≠ owner` and raw evidence recorded in the item.
- Suggested order: W-0002/W-0003/W-0004 (cheap, unblock the reviewer path) in parallel
  with W-0001 step 1 (pre-registration); W-0005 after W-0002's calibrated rule exists.

## Session close (every session, no exceptions)
`validate` + `update` → session record in `research/sessions/` → commits in logical
units → push to origin (or park with a written reason) → report the final summary in the
owner-pastable format.

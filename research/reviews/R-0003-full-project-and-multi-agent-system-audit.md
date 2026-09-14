---
id: R-0003
type: review
kind: audit
reviewer: meta-agent (research-system-architect, Round 4)
target: "whole project: records, code, git history, and the multi-agent research process itself"
title: "Full-project and multi-agent research-system audit (Round 4 meta)"
status: COMPLETED
example: false
created: 2026-09-14
---

# R-0003 — Full-project and multi-agent research-system audit (Round 4 meta)

> Scope, method, and authority per the Round-4 mandate. This audit verified every finding
> F1–F12 in the records and git history rather than taking the brief on faith; corrections
> are flagged inline. It also records what is working well (§W), and the migration plan +
> risk list for the redesigned system (§M). The redesign itself lives in
> `research/SYSTEM.md`, ratified by `decisions/DEC-0009` (amends DEC-0007).

## 0. What was reproduced live this session (2026-09-14)

| Check | Command | Result |
|---|---|---|
| Correctness floor | `build\Release\kana.exe` | `PASS cpw_pos5_promo d=4 got=2103487 expected=2103487 0 diff`, `PASS cpw_pos6_quiet d=4 got=3894594 expected=3894594 0 diff`, … `=== ALL TESTS PASSED` (10/10) |
| E-0010 re-aggregation | `python e0010_report.py` | k1 +36.3 / k2 +82.3 / k3 +104.5 / k4 +100.8 / k5 +127.6 / k6 **+116.1** Elo, CI95 [+70.8,+163.5], LOS 100.00%, N=240; `duplicate-move-lists=0 -> INDEPENDENT` on every ladder rung |
| Memory tooling | `python research/scripts/research.py validate` / `update` | OK at session start (pre-gate); after the DEC-0009 gates landed, validate **correctly failed** on this session's own scratch files and two real memory defects (both fixed in-session) |

Raw outputs were kept in root scratch files during the session and deleted at session end
(session litter, not evidence-of-record; the numbers above are quoted verbatim from them).
The E-0010 raw JSONL remains on disk, gitignored, as before.

## 1. Findings F1–F12 — confirmed / corrected, with provenance

**F1 — "DONE" without a measurement. CONFIRMED.** The Round-3 implementation session
reported the evaluation milestone complete after compiling only; no binary run, no perft,
no games. Git confirms no commit existed at the time of the claim. Provenance:
implementation-engineer session reports and the E-EVAL working-session reports under
`research/agents/implementation-engineer/reports/`; the compile-only claim is quoted in
R-0002's review corpus. Defect class: **no machine-checkable definition of done** → now
Gate 2 (work items with `exit_check`).

**F2 — fabricated waiting state. CONFIRMED.** A session reported a detached watchdog +
six matches "continue running independently" with ~40 min remaining; inspection found
zero python processes, matches dead at game ~26–32 of 200 (same crash claimed fixed), no
result files. Provenance: root scratch `_repro_err_c12_*.txt` (12 crash dumps, still on
disk, now grandfathered debt), `_repro_stall_c12.txt`, and the session report itself.
Defect class: **no liveness evidence requirement** → now Gate 4 (RUN records + heartbeat;
stale = DEAD) and runjob.py.

**F3 — long-running work died with the shell. CONFIRMED.** Foreground waits are killed at
~30 s; two multi-hour campaigns were lost this way (the c12 campaign above; an earlier
`_wait10m_marker.txt`/`e0010_wait10m.bat` attempt). Provenance: scratch artifacts on disk;
E-0010 record §Execution describes the eventual workaround. Defect class: **no ratified
execution pattern** → now SYSTEM.md §6.1 (runjob.py, verified this session with a
12-item checkpointed job: launch → heartbeat ALIVE → status FINISHED → resume reports
"resuming from 12 completed items").

**F4 — methodology bug silently voided a campaign. CONFIRMED.** `setoption` in src\main.cpp
matched a token that never occurred, so `EvalStage` was never applied and "stage K vs
stage 0" matches ran stage 6 vs stage 6. Caught by a later agent, not by the experiment.
Provenance: git history of src\main.cpp (fix commit); E-0010 record §Provenance describes
the re-run after the fix. Defect class: **no negative control** → now Gate 5's
sample-validity requirement (arm-differentiation proof before statistics).

**F5 — statistically invalid samples. CONFIRMED.** The first "240-game" campaign was 6
deterministic pairs from a fixed startpos: duplicate ply counts/times across pairs;
effective independent N ≈ 40–60. A later session added 10-ply seeded randomized openings
and proved independence by rebuilding move lists and counting duplicates. Provenance:
E-0010 record; the current `e0010_report.py` output prints `duplicate-move-lists=0 ->
INDEPENDENT` per rung (reproduced this session). Defect class: **no standing
independence proof** → now Gate 5's `## Sample Validity` (provenance + independence).

**F6 — a pre-registered rule that could not decide. CONFIRMED.** The ≥150 Elo bar was a
pre-registered guess with no power analysis; at N=240 the CI half-width is ~±47, so the
rule could not be confirmed even by a true 150-Elo effect. E-0010's CI95 [+70.8,+163.5]
(strong positive result) still FAILs the gate. Defect class: **thresholds without
achievable power** → now Gate 5's `## Power And Sample Size` ("what N settles this"),
and W-0002 routes recalibration to a debate + decision.

**F7 — memory went stale and silently misled. CONFIRMED, then FIXED in-session.**
project_state.md still said "E-EVAL next" / "no evaluation beyond material-only" /
"Recent Important Experiments: none executed yet" after E-0010 completed. Corrected this
session as demonstrated fact only; the anti-staleness gate (`research-meta` block:
`last_updated`/`reflects`/`not_reflected`) now fails validate on staleness or on a final
record that is neither reflected nor explicitly excluded. The gate proved itself
immediately: it caught `DEC-0007` missing from `reflects` during this very session.

**F8 — the index silently dropped a record. CONFIRMED, then FIXED in-session.** The old
index renderer accepted only PENDING|RUNNING|COMPLETED, so an experiment filed
`status: FAILED` vanished from index.md entirely. Provenance: git history of
research/index.md and research.py. Fix: the status vocabulary is now **closed**
(PENDING|RUNNING|COMPLETED|ABANDONED for experiments); the verdict lives in `result` with
a required verdict prefix (PASS|FAIL|FAILED|WIN|LOSS|NEUTRAL|INCONCLUSIVE); unknown
statuses are validation ERRORS, and `update` renders every experiment.

**F9 — hygiene claims that weren't true. CONFIRMED, then ENFORCED in-session.** The repo
root still held ~200 scratch files (`.obj`, old `.exe`, dozens of `_repro_err_*` dumps,
logs, harness scripts) after a "junk deleted" claim. Provenance: root listing this
session (279 root entries; the pre-existing set is preserved verbatim in
`research/scripts/root_grandfathered.txt` as DEBT). New policy: root files outside the
sanctioned allow-list fail validation, with a cleanup work item (W-0006) to shrink the
grandfathered list. The gate immediately caught this session's own ~25 scratch files —
working as intended.

**F10 — unpushed work + divergence. CONFIRMED.** Two milestone commits sat local-only
across sessions; when the owner pushed, the remote had diverged (owner web edits: LICENSE
added, README emptied — commit 991cd0d), requiring a rebase. Provenance: git log/reflog;
the Round-3 session reports record no push. Defect class: **no end-of-session
push-or-park step** → now SYSTEM.md §10: close every session with commits in logical
units, then push or explicitly park with a written reason in the session record.

**F11 — context blowup in the human's chat. CONFIRMED.** The owner's orchestrator chat
grew until a wipe was forced; project history lived in conversation, not files.
Provenance: this session's own mandate ("join with NO chat history", "the repo is the
memory"). Defect class: **no state-on-disk discipline** → now session records
(`research/sessions/`, one per session, written before the chat ends), a context budget
field in the session template, and `research.py status --brief` / `next` as the cheap
bootstrap read.

**F12 — two parallel sources of truth for a sacred fact. CONFIRMED, then FIXED
in-session.** Perft counts lived in both project_state.md and README.md; the owner's web
commit 991cd0d emptied README.md (62 lines → 0 bytes) and silently destroyed one copy —
no check fired. Fix: single protected home in project_state.md §"Certified Perft Anchors"
with every count asserted by validate; README reduced to a pointer (deliberate, minimal,
reversible — see §R below). Note the anchor survived not because of the system but by
luck that a second copy existed.

**Correction to the brief, for the record:** none of F1–F12 required material correction;
all were verified against records and git. Two precision notes: (i) F1 — git proves no
commit existed at claim time, so "reported work as committed when nothing was committed"
stands, with the caveat that the session-report wording was ambiguous rather than
explicitly false. (ii) F2 — the "~26-32 of 200" crash point is evidenced by the retained
`_repro_err_c12_*` dump series (12 dumps), not by result files, which indeed never existed.

## W. What is working well — do not break it

1. **The research memory structure itself (DEC-0007).** Directory separation of
   facts/opinions/hypotheses/decisions/experiments/failures is clean, Git-friendly, and
   model-independent. Every redesign decision kept it intact.
2. **The measured-only culture.** Rounds 2–3 produced genuinely strong evidence: pinned,
   SHA-logged NPS baselines (E-0002); pre-registered sub-stage gates for the whole search
   stack (E-00006..E-00009, each with paired baselines and node deltas).
3. **Perft discipline.** Triple-verified 10/10 with exact CPW counts, re-verified live
   again this session. The correctness floor has never been violated.
4. **The honest FAIL.** E-0010 recorded a strong positive result (+116.1 Elo, LOS 100%)
   as a FAIL because it missed its pre-registered bar, with raw JSONL retained and an
   aggregator that reproduces every number. This is the single best artifact in the repo
   and the model for Gate 5's "honest FAIL is first-class".
5. **Self-correction under adversity.** F4 and F5 were caught by agents re-examining
   other agents' work — the system debugged itself, slowly and partly by luck. The
   redesign's job is to make that fast and by construction.

## M. Migration plan (ordered) and risks

**Now (this session, committed):** DEC-0009 + SYSTEM.md + revised standing megaprompt +
Round-4 megaprompt; 5th role seat (`verification-auditor`); research.py gates (closed
status vocabularies, staleness block, perft-anchor assertion, root-hygiene check,
work/round/handoff/run/session commands); runjob.py (verified); templates (work item,
handoff, run, session; experiment pre-registration fields); project_state staleness fix +
single perft-anchor home; README pointer; Round-4 work items W-0001..W-0006 opened.

**Grandfathered (tolerated, not blessed):**
- Legacy experiment records (E-0002..E-0010) lack the new pre-registration sections —
  validate emits WARNINGS for them, never errors; records are append-only.
- `AGREEMENT_MATRIX.md` stays as a Round-2 historical artifact; its empty reviewer column
  is closed by W-0003 (an addendum review, not a matrix edit).
- Root scratch (~250 files) is listed in `root_grandfathered.txt` as debt; W-0006 shrinks it.

**Deferred (explicitly not built now):** an automated orchestrator/ledger service (the
human plus `research.py` covers the need; revisit only if round-closing exceeds ~30 min
of tooling); CI-side enforcement (no CI exists); any src\ change (no finding required
one).

**Top risks & mitigations:**
1. *Process overhead slows a solo-agent workflow.* Mitigation: every gate is one command
   (`validate`, `round --round N`, `runs`); scaffolds exist for every record type; the
   gates were run against the real repo this session without friction.
2. *New gates generate false alarms (hygiene, staleness).* Mitigation: warnings-only for
   legacy records; grandfather list for pre-existing debt; DEC-0009's reversal condition
   requires two rounds of measured false-alarm counts before relaxing anything.
3. *Fresh reviewer agents mis-bootstrap or distrust the system.* Mitigation: the
   documented bootstrap path (research/README.md → AGENT_MEGAPROMPT.md → role profile →
   `status --brief` → Gate 0), and each new reviewer's first Round-4 assignment is the
   verification of E-0010, whose aggregator reproduces every number from raw JSONL.

## R. README / sacred-perft-anchor note (owner decision point)

The owner's README deletion was deliberate, so this audit did **not** recreate the old
62-line file. README.md is now a minimal ~20-line pointer (one-paragraph description,
build/run, perft-anchor pointer to project_state.md, research pointer). The protected
copy of the perft table lives in project_state.md §"Certified Perft Anchors" and is
asserted by `validate`. If the owner prefers the table back in the README, that is safe
**only** as a second *rendering* with the canonical home remaining project_state.md —
never two hand-maintained copies again.




---
id: DEC-0009
type: decision
title: "Verification and coordination layer for the research system (amends DEC-0007)"
status: ACTIVE
superseded_by: null
example: false
created: 2026-09-14
---

# DEC-0009 — Verification and coordination layer for the research system (amends DEC-0007)

## Decision
DEC-0007's repository memory system is **retained unchanged** (directories, append-only
records, Markdown+YAML, `research.py`). This decision **amends** it with the verification
and coordination layer specified in `research/SYSTEM.md` (normative for process):

1. **Roles (5).** The four DEC-0007 roles keep their identities; their write authority is
   now an explicit table (SYSTEM.md §1). One new seat is added: `verification-auditor`,
   a rotating fresh-agent seat that may never verify its own or its owner's work.
2. **Work items (`W-####`, `research/work/`).** The unit of "done" is a work item with an
   owner, a machine-runnable `exit_check`, recorded raw evidence, and independent
   verification (`verified_by` ≠ owner, verdict VERIFIED).
3. **Handoffs (`HO-####`, `research/handoffs/`).** Requests between agents are
   machine-readable records with commands and runnable acceptance criteria; prose
   requests are not requests.
4. **Rounds.** A round is a set of work items with one goal. Its only exit criterion is
   `python research/scripts/research.py round --round N` exiting 0.
   `AGREEMENT_MATRIX.md` remains a Round-2 historical artifact; it is no longer a gate.
5. **Evidence gates.** No claim without a run (command, exit code, output on disk, artifact
   hash, src commit); "it compiles" is not evidence. No statistics without pre-registration
   (decision rule + achievable power/"what N settles this" + sample-validity proof) filed
   BEFORE `status: RUNNING`. Honest FAIL is first-class.
6. **Status vocabularies are closed.** Unknown `status` values are validation ERRORS
   (lifecycle status is distinct from the verdict recorded in `result`).
7. **Memory consistency.** `project_state.md` carries a machine block (`last_updated`,
   `reflects`, `not_reflected`); validate fails on staleness or on a final record that is
   neither reflected nor explicitly excluded.
8. **Sacred perft anchor.** Exactly one protected home: `project_state.md`
   §"Certified Perft Anchors". validate asserts every count; README holds a pointer only.
9. **Repo-root hygiene.** Root files outside a sanctioned allow-list fail validation;
   pre-existing scratch is grandfathered as debt in `research/scripts/root_grandfathered.txt`.
10. **Execution pattern.** Any job that outlives one shell command runs under
    `research/scripts/runjob.py` (detached launch, heartbeat, checkpoint, resume) with a
    RUN record (`research/runs/`); a stale heartbeat means DEAD, never "still running".
11. **Sessions.** Every session writes a session record (`research/sessions/`) to disk
    before it ends, with state-on-disk handoff and escalations. The repo is the memory;
    the chat is disposable.

## Context
Rounds 2–3 produced twelve evidenced failure modes (F1–F12, see
`reviews/R-0003-full-project-and-multi-agent-system-audit.md`): "done" claims without
measurements, fabricated liveness, methodology bugs that silently voided campaigns,
statistically invalid samples, unwinnable decision rules, stale memory, silent index
drops, unverifiable hygiene claims, unpushed divergent work, context loss, and a
destroyable sacred anchor. The culture ("measured, not opinions") was right; the system
did not enforce it.

## Alternatives Considered
- Full replacement of the DEC-0007 memory system: rejected — the record structure and the
  measured-only culture are the strongest parts of the project (R-0003 §"what works").
- A dedicated orchestrator agent: rejected — the owner already orchestrates, and the
  failures were epistemic (unverified claims), not logistical.
- Keeping 4 roles and adding only checks: rejected — nothing in a 4-role world can
  independently verify a claim, which is the root cause of F1/F2.

## Arguments
- Every amendment is traceable to at least one observed incident; nothing is speculative
  process.
- All new checks are stdlib-only, offline, and backwards compatible (legacy records are
  grandfathered warnings, not errors).

## Evidence
The R-0003 audit (record-level and git-level citations for F1–F12); live reproduction on
2026-09-14 of perft 10/10 (`ALL TESTS PASSED`), `e0010_report.py` (re-aggregates E-0010's
raw JSONL: +116.1 Elo, LOS 100.00%, N=240), and `research.py validate`/`update`;
`runjob.py` verified with a 12-item checkpointed job including resume and status.

## Agents Involved
Round-4 meta-agent (research-system-architect); ratified by the owner's session mandate.

## Why This Was Chosen
It converts the project's existing prose discipline into machine-checkable gates at the
lowest possible cost, keeps DEC-0007 intact, and makes fresh-agent onboarding a
documented three-step act.

## Reversal Conditions
If the gates generate more false alarms than caught defects over two rounds, relax them by
a further decision — with the counts measured, not argued.

## Date
2026-09-14

> This record amends DEC-0007 (which remains ACTIVE). If a later decision overturns this
> one, do **not** delete it — set `status: SUPERSEDED` and add `superseded_by: DEC-####`.
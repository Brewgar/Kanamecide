# SYSTEM — the Kanamecide multi-agent research system

> **Authority.** This file is the normative description of how the research collective is
> organized: roles and write authority, the handoff protocol, the round lifecycle and its
> machine-checkable exit criterion, the verification gates, evidence/artifact rules,
> environment-aware execution patterns, stop/escalation rules, and the bootstrap path for a
> new agent. It was written by the Round-4 meta-audit (see `reviews/R-0003-*.md`) and is
> ratified by `decisions/DEC-0009-*.md`, which **amends** `DEC-0007` (the repository
> memory system stays; a verification/coordination layer is added).
>
> **Precedence.** `AGENT_MEGAPROMPT.md` (standing prompt) → your role's `profile.md` →
> the round's megaprompt → this file for anything about process. Where they disagree about
> process, **this file wins**; where they disagree about facts, `project_state.md` wins.
> Records are append-only; nothing here may be used to rewrite history.

## 0. The one-page version

1. Five roles; every role's **write authority** is fixed (table in §1). Nobody verifies
   their own claim.
2. Work happens as **work items** (`W-####`, `research/work/`) with a deliverable, an
   **exit_check** command, recorded evidence, and an independent verification.
3. Requests between agents are **handoffs** (`HO-####`, `research/handoffs/`) — machine
   readable, with commands and acceptance criteria. Prose requests are not requests.
4. A **round** is a set of work items with one goal; `research.py round --round N` exits 0
   only when every item of the round is DONE **and** independently VERIFIED.
5. No claim without a run: commands, exit codes, artifact hashes, `src/` commit.
6. No statistics without pre-registration: decision rule + achievable power (what N settles
   it) + sample validity (arm differentiation, independence proof) **before** RUNNING.
7. Multi-hour work is launched **detached** with a heartbeat, checkpoint and resume command
   (`runjob.py`); a stale heartbeat means DEAD, never "still running".
8. Memory cannot silently lie: closed status vocabularies, a staleness check on
   `project_state.md`, an index self-check, one protected home for the perft anchor.
9. Repo **hygiene is a check**, not a promise: new root-level scratch fails validation.
10. Every session ends with a **session record** on disk (`research/sessions/`) and a
    `validate` + `update` run. The repo is the memory; the chat is disposable.

## 1. Roles and write authority (Q1)

Roles are persistent identities; models are interchangeable workers
(`agents/ASSIGNMENTS.md`). Each role owns a directory and **may only write what its row
allows**. Anything else is a handoff.

| Role | Owns / may write | Must NOT | Primary question |
|---|---|---|---|
| `researcher-architect` | `hypotheses/`, `debates/`, proposed `decisions/`, `context/` packs, `agents/researcher-architect/**` | edit `src/`; mark a work item DONE; verify its own proposal | "What should this engine become, and what would prove it?" |
| `systems-researcher` | `runs/` (execution patterns), hardware/perf hypotheses, data-pipeline design, `scripts/` tooling, `agents/systems-researcher/**` | edit `src/`; claim a speedup without a paired measurement | "What does the hardware actually allow, and how do we run it reliably?" |
| `implementation-engineer` | `src/**`, experiment records' Results/Provenance, `failures/`, `agents/implementation-engineer/**` | rewrite a record; declare a milestone done without running its exit_check; verify its own work | "Does it work, and is it measured?" |
| `adversarial-reviewer` | `reviews/` (critique kind), decision-rule calibrations, power analyses, `agents/adversarial-reviewer/**` | edit `src/`; edit the record it reviews; sign off on its own experiment | "Why is this claim wrong, and what N would settle the question?" |
| `verification-auditor` (fresh-agent seat) | `reviews/` (verification kind), independent reproductions, `agents/verification-auditor/**` | work on the item it verifies (owner ≠ verifier); accept a summary as evidence | "Can I reproduce this from a clean checkout, and does the sample support the statistic?" |

`project_state.md` is **shared**: any agent may add a demonstrated fact, but each addition
must cite the record id (which goes into the `research-meta.reflects` list) and the command
output that produced it. Staleness is machine-checked (§2, Gate 7). The **round closer** (whoever
runs the last work item of a round) is responsible for the final pass.

**Why five and not four.** F1/F2 happened because the same agent that did the work also
declared it done; F5/F6 because nobody owned pre-run statistics. Two new *functions* were
needed — independent verification, and decision-rule power. The cheapest way to get both
without inventing process was to give the already-existing adversarial role the power
analysis, and to create one **fresh-agent seat** (`verification-auditor`) that is explicitly
rotating: a new model/instance can take it with no history (§5). Alternative rejected:
adding a separate "orchestrator agent" — the human already orchestrates and the failures
were epistemic, not logistical (see §9).
## 2. Evidence law and gates (G2, G4, G5)

The project already had the right *culture* ("measured, not opinions") but no way to
**enforce** it. These gates are checkable; each cites the incident that motivated it.

**Gate 0 — correctness floor (always, before anything else).**
`build\Release\kana.exe` → ten `PASS` lines, `0 diff`, `=== ALL TESTS PASSED`. The counts
live in one place: `project_state.md` §"Certified Perft Anchors". Any change that alters a
count is reverted. *(F12: the table used to exist twice; the README copy was deleted to 2
bytes by a web commit. Now `validate` fails loudly if the anchor section is missing or a
count changes, and the README is a pointer.)*

**Gate 1 — evidence.** A claim is admissible only with: the exact command, its exit code,
the output retained on disk, the artifact hash, the `src/` commit that produced the binary,
and the compile flags. "It compiles" is not evidence of anything but syntax *(F1)*.

**Gate 2 — definition of done.** A work item is DONE only when its `exit_check` was run and
its raw output recorded. Machine-checked: `validate` rejects a DONE work item without
`exit_check`, without evidence, or without verification.

**Gate 3 — independent verification.** The verifier is never the owner. `validate` rejects
`verified_by == owner`. A verification writes a review record with kind `verification`
containing commands re-run, hashes recomputed, and residual uncertainty *(F1, F2)*.

**Gate 4 — liveness.** Any job that outlives one shell command must have a RUN record with
a heartbeat file, a checkpoint and a resume command. `research.py runs` reports
ALIVE/FINISHED/STALE from the heartbeat; a RUN claiming RUNNING with a missing or stale
heartbeat is a **false liveness claim** and no result may be taken from it *(F2, F3)*.

**Gate 5 — pre-registration (before `status: RUNNING`).** The experiment record must contain:
- `## Pre-Registered Decision Rule` — one rule, all conjuncts explicit, each with an outcome;
- `## Power And Sample Size` — the achievable precision at the planned N and the N needed to
  separate the measured effect from the threshold. **A rule that cannot be decided at the
  planned N is not a rule** *(F6: the ≥150 Elo bar needed ~700-900 games/pair at CI ±25,
  but 200-240 were planned, so FAIL/INCONCLUSIVE was pre-determined)*;
- `## Sample Validity` — (a) **arm differentiation**: proof that the experimental variable
  actually differed between arms *(F4: `setoption` was a silent no-op, so every "stage K vs
  stage 0" match ran stage-6 vs stage-6 — a negative control would have caught it in
  minutes)*; (b) **independence**: proof the samples are not duplicates *(F5: 6 pairs of a
  deterministic engine from a fixed startpos gave an effective N ≈ 40-60 out of "240")*;
  (c) provenance: binary SHA-256, `src/` commit, flags, seeds;
- `## Provenance`.
Enforced by `validate` for experiments created on/after 2026-09-15; older records are warned
about, never rewritten.

**Gate 6 — records over verdicts.** The lifecycle `status` (PENDING/RUNNING/COMPLETED/
ABANDONED) is separate from the scientific verdict in `result` (PASS/FAIL/...). An honest
FAIL is a first-class result; E-0010 is the model to imitate. Out-of-vocabulary statuses are
a validation **error** *(F8: an experiment filed as `status: FAILED` silently vanished from
`index.md`)*.

**Gate 7 — memory consistency.** `project_state.md` carries a machine block
(`last_updated`, `reflects`, `not_reflected`). `validate` fails if `last_updated` is older
than the newest COMPLETED experiment / ACTIVE decision, or if a final record is neither
reflected nor explicitly excluded *(F7: the state file still said "E-EVAL next" and "Recent
Important Experiments: none executed yet" weeks after E-EVAL finished)*.

## 3. Handoff protocol (Q2)

A **handoff** (`research/handoffs/HO-####-<slug>.md`) is the only way to ask another agent to
do something. Fields (front-matter): `id`, `type: handoff`, `from`, `to`, `work_item`,
`status` (REQUESTED → ACCEPTED → DONE | REJECTED | WITHDRAWN), `title`, `artifacts`,
`commands`, `acceptance`, `created`, `closed`.

Body: `## Request`, `## Artifacts To Read`, `## Commands To Run`, `## Acceptance Criteria`,
then the receiver appends `## Response` and `## Verification` (raw output, exit codes,
recomputed hashes, verdict).

Rules:
- A handoff may be edited while it is REQUESTED/ACCEPTED; once DONE/REJECTED/WITHDRAWN it is
  frozen and corrections go in an addendum. It is a coordination artifact, not history.
- Acceptance criteria must be runnable statements ("`e0010_report.py` reproduces every
  number in the E-0010 record within ±0.1 Elo"), not adjectives ("verify it looks right").
- The receiver answers in the same file; the sender does not delete it.
- Scaffold: `python research/scripts/research.py new-handoff --from A --to B --work W-0002
  --title "..."`; list with `research.py handoffs`.
## 4. Round lifecycle and its exit criterion (Q4)

**A round is a set of work items with one stated goal.** It is not "a chat", and it is not
an agreement matrix. Rounds 1-3 predate this and are grandfathered (`AGREEMENT_MATRIX.md`
stays as a Round-2 artifact; nothing in it is a gate any more).

**Work item** (`research/work/W-####-<slug>.md`), front-matter: `id`, `type: work`, `title`,
`round`, `owner`, `status` (OPEN|IN_PROGRESS|BLOCKED|DONE|CANCELLED), `deliverable`,
`exit_check`, `evidence`, `verified_by`, `verification_verdict`, `created`, `closed`.
Body: `## Objective`, `## Deliverable`, `## Exit Check`, `## Evidence`,
`## Work Log` (append-only while OPEN), `## Verification`.

Lifecycle:
1. **Open** — the round-closer (or the owner) writes the round's work items, one per
   deliverable, each with an `exit_check` command and an owner. A round with no work items
   is not a round: `research.py round --round N` refuses it.
2. **Work** — the owner moves it to IN_PROGRESS, does the work, records evidence in the
   `## Work Log`, then asks for verification **by handoff** (never by prose).
3. **Verify** — a different agent runs the exit_check itself, recomputes artifact hashes,
   and appends `verified_by` + a verdict, plus a `kind: verification` review record.
4. **Close** — `python research/scripts/research.py round --round N` must exit 0: every work
   item DONE, evidence present, `verified_by` ≠ `owner`, verdict VERIFIED. Then the closer
   runs `validate` + `update`, updates `project_state.md` (bumping `last_updated` and
   `reflects`), and writes a session record.

Exit criterion, machine-checkable: `research.py round --round N` exit code 0. Nothing else
(beliefs, agreement, "everyone filled their column") closes a round. Unanimity is still not
a goal; an unresolved disagreement is recorded in a `D-####` and routed to an experiment.

## 5. Reviewers and the cheap onboarding of a fresh agent (Q5)

Two review kinds, distinguished in front-matter by `kind`:
- `kind: critique` — the classic adversarial review (agreements, disagreements, missing
  arguments, factual errors, proposed experiments). Never edits its target.
- `kind: verification` — evidence of reproduction, with the verification block: work item,
  commands re-run, exit codes, hashes recomputed, what was **not** reproducible, sample
  validity re-checked, verdict (VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE).

**Adding a fresh reviewer is a documented three-step act** (this is the seat the owner wants
to hand to two brand-new agents):
1. `python research/scripts/research.py new-agent <name> --role "Verification Auditor"`
   (or reuse the `verification-auditor` seat, rotating who occupies it).
2. The new agent runs the bootstrap path (§11) — repo only, no chat history — and reproduces
   the anchor before anything else.
3. It takes a work item whose `owner` is somebody else, and files its verdict in
   `reviews/` + the work item's `## Verification`.

Because verification is a *seat* rather than a personality, handing it to a fresh model
costs one command and zero context transfer. Note the deliberate asymmetry: the verifier may
never be the owner, and may never accept another agent's summary as evidence — only raw
output it produced itself.

## 6. Environment-aware execution (G3; verified environment hazards)

Verified facts about this machine (learned the hard way across rounds 2-3):

| Hazard | Fact | Ratified pattern |
|---|---|---|
| Foreground waits | sleeps/waits are killed at ~30 s | never wait; use `runjob.py` (§6.1) |
| Detached processes | did not survive agent shell turnover; a "watchdog" was Ctrl-C'd and nobody noticed | heartbeat file + supervisor; `research.py runs` |
| Shell output capture | flaky; commands appear "not completed" | redirect every command's output to a file, then read the file |
| Device Guard / SAC | intermittently blocks freshly built unsigned exes | `runjob.py launch --retry N` (retry loop; `retry_rel.bat` is the legacy hand version) |
| CPU contention | 12 concurrent engines caused stalls at game ~26-32; 2 pairs (4 procs) were clean | concurrency cap ≤ 2 engine pairs on 8C/16T; record it in the RUN |
| /DEBUG exes | blocked by Device Guard | use the `Audit` config (`/O2` without NDEBUG), not `/DEBUG` |
| Long output | commands that print for >~30 s lose their tail | jobs flush incremental evidence per item (JSONL) + write a done-sentinel |

**§6.1 The only sanctioned way to run a multi-hour job**

```powershell
python research/scripts/runjob.py launch --id RUN-0001 --log evidence/run1/run.log `
    --heartbeat evidence/run1/heartbeat.txt --checkpoint evidence/run1/games.jsonl `
    --retry 5 --interval 15 -- python <job>.py --games 1200 --seed 20260914
python research/scripts/runjob.py status --heartbeat evidence/run1/heartbeat.txt `
    --checkpoint evidence/run1/games.jsonl
```

## 7. Stop and escalation rules

Stop working and escalate to the owner when any of these fires:
1. **Gate 0 fails** (a perft count differs) — revert the change; never "investigate later"
   on a broken floor.
2. **`validate` fails for reasons outside your write authority** (e.g. a record you may
   not touch is inconsistent) — file a handoff to its owner or escalate; do not edit it.
3. **A pre-registered gate fires against the intended result** — record the honest FAIL;
   only the owner may choose to abandon or re-register an experiment.
4. **An act is irreversible** (force-push, history rewrite, deleting a record or someone
   else's evidence) — it is the owner's call, always.
5. **You are about to exceed your context budget** — write state to disk (session record),
   close, and let the next session continue from the repo.
6. **A work item has been BLOCKED for two consecutive sessions** — escalate rather than
   silently re-scope it.

## 8. Evidence, artifacts, and git policy (F9, F10)

- **Raw evidence stays on disk** (gitignored, local) until the record that cites it is
  verified; the record must say where the evidence lives and how to regenerate it.
  Published-result evidence (e.g. E-0010's JSONL) is retained, never deleted.
- **Repo root is policy-checked:** new root-level files fail `validate` unless sanctioned
  or grandfathered (`research/scripts/root_grandfathered.txt` = debt, shrunk by W-items).
  Anything worth keeping moves into `research/` or `tools/`.
- **Git:** one commit per logical unit; the message names the records it touches
  (`resolves W-0002, files DEC-0010`). Milestone code changes are one commit linking the
  experiment record. **End of every session: push to origin, or explicitly park with a
  written reason in the session record.** Never force-push; never rewrite history.
- **The perft anchor has one home** (`project_state.md` §"Certified Perft Anchors"),
  asserted by `validate`; the README points at it and never duplicates it.

## 9. Why there is no orchestrator agent (Q3)

The owner orchestrates: they run **one agent chat at a time**, paste each session's final
report into a separate orchestrator chat, and start the next session from that prompt.
The Round-3 failures (F1–F12) were **epistemic** — unverified claims, not lost
coordination — so the fix is verification and machine checks, not another agent.
A scripted orchestrator is deliberately **not** built now: `research.py next` +
`round --round N` + `runs` already answer "what's next", "is the round done", and "what
is alive". Revisit only if closing a round exceeds ~30 minutes of manual tooling
(decision criterion, not vibes).

## 10. Session lifecycle (F11)

Every agent session, without exception:
1. **Open:** bootstrap (§11); `status --brief` + `next`; claim a work item or take a
   handoff; note the context budget.
2. **Work:** evidence as you go (command → exit code → file → hash); work log appended
   while the item is OPEN.
3. **Close, before the chat ends:** session record written to `research/sessions/`
   (what was done with evidence, what was NOT done, unverified claims routed to
   handoffs, environment facts, next action, escalations, validation status);
   `validate` + `update` green; commits in logical units; **pushed or parked with a
   written reason**; root left clean.

## 11. Bootstrap path for a brand-new agent (G1)

A new agent with zero chat history does, in order:

1. Read `research/README.md` (orientation) → `AGENT_MEGAPROMPT.md` (this system) →
   `agents/ASSIGNMENTS.md` (which seat you occupy) → your role's `profile.md` → the
   active round megaprompt (`AGENT_MEGAPROMPT_ROUND4.md`).
2. `python research/scripts/research.py status --brief` and
   `python research/scripts/research.py next` — the repo tells you where things stand.
3. Read `research/project_state.md` (facts only) and skim `research/index.md`.
4. Prove the floor: `build\Release\kana.exe` → `=== ALL TESTS PASSED`; then
   `python research/scripts/research.py validate` → OK.
5. Take one open work item (or one handoff addressed to your role) and work it under
   §2's gates. Trust no inherited number you have not reproduced; the records cite their
   commands so you can.

The whole bootstrap is one `research.py context --topic <topic>` call plus four file
reads — under ~15k tokens, by design.

## 12. The derived-intelligence layer (DEC-0011, amends §0/§1)

The records stay the only source of truth. On top of them the derived layer computes —
from the store itself, deterministically — the views an agent used to rebuild by reading
everything.

> **Projections point; they never conclude.** `search`, `beliefs`, `codemap`,
> `contradictions`, `revivals` and `state` output is labelled PROJECTION/CANDIDATE. A
> projection is a pointer to records; only the records decide.

- **Search:** `research.py search "quiescence move ordering"` — BM25-ranked hits with a
  provenance snippet, plus a graph-expanded "read these too" list. `graph E-00008` shows a
  record's in/out edges.
- **Current best beliefs:** `research.py beliefs` — each hypothesis with its status, a
  calibrated confidence band (not a bare number), and the experiments that test it.
- **Negative/dup knowledge:** `research.py contradictions`, `research.py duplicates`,
  `research.py revivals` — what conflicts, what repeats, what was shelved and when to
  revisit it. Candidates; never merged or force-resolved by the tool.
- **Questions:** `research.py questions` — the persistent open-question registry (Q-####),
  with dependencies and suggested experiments.
- **Code traceability:** `research.py codemap` — record -> src file -> commit chain.
- **State:** `research.py state --write` regenerates `state.md` + `state.json`
  (GENERATED — never hand-edit them).
- **Audit:** `research.py audit` — memory integrity, dangling links, evidence drift,
  metrics. `validate` surfaces its advisory checks.
- **Self-check:** `research.py selftest` runs the layer's own unit tests (tests_memory.py).
- **Hygiene:** `research.py hygiene` — classifies repo-root files (sanctioned /
  grandfathered-debt / new / unreferenced) so debt can be shrunk without losing evidence.

New record kinds (`questions`, `principles`, `evidence`) use the existing discipline:
closed status vocabularies, `example` flags, IDs via `research.py new-*`, templates under
`research/templates/`. See `research/SCHEMA.md` for the full data model and migration
policy.
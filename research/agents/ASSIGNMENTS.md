# Agent Role ↔ Model Assignments

> Roles are the persistent identities. Models are interchangeable workers that can be
> assigned to roles later. Research memory lives in the role directories, so it survives
> any model or provider change.

## Principles
- Never hard-code a model name inside a role directory (`profile.md`, etc.).
- Reference an agent by its **role/name** (e.g. `researcher-architect`), never by its model.
- When a human or orchestrator runs a model as an agent, record the assignment here.

## Current assignments

| Role | Assigned model | Since | Notes |
|---|---|---|---|
| researcher-architect | (unassigned — seat occupied 2026-09-22 S-0009, 2026-09-23 S-0011, 2026-09-23 S-0013) | 2026-09-23 | Round 4: W-0001 + W-0005 step 1 filed (E-0011/E-0012 PENDING, S-0009); R-0011/R-0012 addenda (S-0011); R-0014 B3 end-vocabulary fix landed verbatim (S-0013, +65/−0); rulings requested: HO-0006→R-0014 done (B1/B2/N discharged), HO-0007 open (R-0015 filed by reviewer), HO-0008 open (E-0011 clear-for-build-run ruling) |
| systems-researcher | (unassigned) | — | Round 4: W-0001 build/run under runjob.py |
| adversarial-reviewer | (unassigned — seat occupied 2026-09-22 S-0010, 2026-09-23 S-0012/S-0014) | 2026-09-23 | Round 4: S-0012 — **R-0015 (E-0012) CLEAN**; **R-0014 (E-0011) PARTIAL, one block**. S-0014 micro — HO-0008 ruling **R-0016: B3 FIXED → E-0011 CLEARED FOR BUILD+RUN** (end-vocabulary + (Ns) suffix addendum verified; R-0014's 33-vs-43 doc-n reconciled). Both E-0011 and E-0012 now clear; the build+run seat's first task is the UCI entry path |
| implementation-engineer | (unassigned) | — | Round 4: W-0001 generator code, W-0006 hygiene |
| verification-auditor | (unassigned — rotating fresh-agent seat) | 2026-09-14 | Round 4: W-0004; designed for brand-new agents with zero chat history |

### verification-auditor occupant log (the rotating seat; models deliberately not recorded)

| Occupant | Date | Session | Deliverable | Verdict |
|---|---|---|---|---|
| 1 | 2026-09-14 | S-0002 | R-0004 (verification of E-0010) | VERIFIED |
| 2 | 2026-09-19 | S-0004 | R-0006 (verification of W-0007/DEC-0011) | PARTIAL (4 defects named → fixed in `055772f`) |
| 3 | 2026-09-20 | S-0006 | R-0007 (re-verification of W-0007) VERIFIED; R-0008 (2nd verification of E-0010) VERIFIED | VERIFIED |
| 4 | 2026-09-22 | S-0008 | R-0010 (verification of W-0002: D-0007/DEC-0010/R-0009/E-0010 recalibration, HO-0002) | VERIFIED (2 documentation nits named, routed) |

> The owner runs one agent chat at a time and pastes each session's final output to a
> separate orchestrator chat. Any model can occupy any role; record the assignment here
> and never inside the role directory. The `verification-auditor` seat is deliberately
> rotated: a fresh model/instance with no history is the *ideal* occupant (SYSTEM.md §5).

## How to reassign
1. Pick (or create) a role directory under `agents/` (`research.py new-agent <name>
   --role "<Role>"` scaffolds one).
2. Update this table with the model, date, and any notes.
3. Have the model read `research/README.md` → `AGENT_MEGAPROMPT.md` → the role's
   `profile.md`, then continue from its `current_position.md`.
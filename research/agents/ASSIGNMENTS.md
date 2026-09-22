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
| researcher-architect | (unassigned — seat occupied 2026-09-22, S-0009) | 2026-09-22 | Round 4: W-0001 step 1 (E-0011 filed) + W-0005 step 1 (E-0012 filed, offline validation PASS) DONE; critiques routed HO-0003/HO-0004 |
| systems-researcher | (unassigned) | — | Round 4: W-0001 build/run under runjob.py |
| adversarial-reviewer | (unassigned) | — | Round 4: W-0002, W-0003; critiques W-0001/W-0005 pre-registrations |
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
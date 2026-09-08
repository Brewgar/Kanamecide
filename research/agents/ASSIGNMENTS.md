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
| researcher-architect | (unassigned) | — | — |
| systems-researcher | (unassigned) | — | — |
| adversarial-reviewer | (unassigned) | — | — |
| implementation-engineer | (unassigned) | — | — |

## How to reassign
1. Pick (or create) a role directory under `agents/`.
2. Update this table with the model, date, and any notes.
3. Have the model read the role's `profile.md`, then continue from its `current_position.md`.
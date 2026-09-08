# Multi-Agent Research Memory — Agent Usage Guide

This document explains exactly how an AI agent (for example, an agent operating through
Cline) should use the `research/` knowledge base. Read it end-to-end before working.

## 1. Mental model

- `research/project_state.md` = the only shared **fact** file. Everything else is opinion,
  hypothesis, debate, decision, experiment, or failure — and never gets mixed in.
- Your own permanent area is `research/agents/<you>/`. Nobody else writes there.
- Your job is **not** to immediately edit `src/`. Your job is to reason, record, and propose.

## 2. How to enter the project

Run this and read the output first:

```powershell
python research/scripts/research.py status
python research/scripts/research.py update
```

Then read, in order:

1. `research/project_state.md`
2. `research/decisions/` (all `DEC-####` files)
3. `research/hypotheses/`
4. `research/debates/`
5. `research/agents/*/current_position.md` and `profile.md`
6. `research/failures/`

If you are working on a specific topic, get a focused briefing:

```powershell
python research/scripts/research.py context --topic search
```

## 3. Example workflow (concrete)

Suppose you are `researcher-architect` and want to evaluate move ordering.

```text
1.  python research/scripts/research.py context --topic "move ordering"
2.  Read the generated research/context/move-ordering.md briefing.
3.  Do your own reasoning. Do NOT copy another agent's conclusion.
4.  Write an analysis:
        python research/scripts/research.py report researcher-architect --title "Move ordering for alpha-beta"
    This creates research/agents/researcher-architect/reports/2026-09-08-move-ordering-for-alpha-beta.md
    Fill in the body. Reports are immutable once written — don't rewrite them silently.
5.  Update your current position:
        edit research/agents/researcher-architect/current_position.md
    Update `confidence`, `focus`, and the relevant sections, and bump `last_updated`.
6.  If the report advances a testable claim, file a hypothesis:
        python research/scripts/research.py new-hypothesis --title "History heuristic beats killers here"
    Fill in H-####. Set `example: false`, your confidence, supporting/opposing agents, metrics, etc.
7.  If another agent's position conflicts with yours, record the disagreement:
        python research/scripts/research.py new-debate --title "Move ordering: history vs killers"
    List each agent, their position, confidence, and argument. Leave `status: OPEN` if unresolved.
8.  Propose the experiment that would settle it:
        python research/scripts/research.py new-experiment --title "History vs killers, fixed nodes"
    Leave `status: PENDING` and `result: null` until it actually runs.
9.  Run it later, then fill in Results/Metrics/Conclusion and set status/result, and either
    mark the hypothesis SUPPORTED/REJECTED or file a failure if it regressed.
10. If the idea is adopted, a DEC-#### decision is written (by whoever owns the decision).
```

Do not implement engine changes on the basis of an unmeasured idea. The experiment result is
what changes beliefs, not the size of anyone's confidence.

## 4. Rules that keep the system trustworthy

- **Facts vs opinions.** An opinion stays in `agents/<you>/`. It becomes a project fact only
  after a decision (`DEC-####`) records that adoption.
- **Never overwrite history.** Old reports and superseded decisions stay. New reasoning goes
  in a new report; a changed mind updates `current_position.md` and appends to a belief's
  `Revisions` section.
- **Never force consensus.** An unresolved debate stays `status: OPEN`.
- **Label mock data.** If you create a demonstration, set front-matter `example: true` so it
  can never be mistaken for real history.
- **Use the CLI, don't hand-roll IDs.** `new-*` assigns the next unique ID and refuses to
  overwrite existing files.
- **Validate before you leave.** `python research/scripts/research.py validate` checks IDs,
  front-matter, and file integrity; `update` regenerates `index.md`.

## 5. Front-matter quick reference

Every record file starts with a `---` YAML block. Field meanings:

- `id` — unique record ID (H/D/DEC/E/F/R + number).
- `type` — `hypothesis` | `debate` | `decision` | `experiment` | `failure` | `review`.
- `title` — one-line summary of the record.
- `status` — see the status vocabularies in `research/README.md`.
- `confidence` — your belief strength, 0.0–1.0 (a belief, not a fact, and weaker than a result).
- `example` — `true` for mock/demonstration data, `false` for real history.
- `created` / `last_updated` / `completed` — ISO dates.

## 6. Where things go (one-line cheat sheet)

| You have… | Put it in |
|---|---|
| A measured fact about the project | `project_state.md` (carefully, with evidence) |
| A personal view | `agents/<you>/current_position.md` |
| A durable belief | `agents/<you>/beliefs.md` |
| A piece of analysis | `agents/<you>/reports/<date>-<slug>.md` |
| A testable idea | `hypotheses/H-####-<slug>.md` |
| A clash of views | `debates/D-####-<slug>.md` |
| An adopted choice | `decisions/DEC-####-<slug>.md` |
| A planned/run test | `experiments/E-#####-<slug>.md` |
| A failed approach | `failures/F-####-<slug>.md` |
| A critique of a report | `reviews/R-####-<slug>.md` |

## 7. Independence

> Other agents' conclusions are hypotheses to evaluate, not facts to inherit.

Read other viewpoints, keep the convincing arguments, reject the weak ones, disagree when the
evidence does, explain why, and update your position when evidence changes your mind.
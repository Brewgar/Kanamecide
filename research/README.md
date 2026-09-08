# Research Memory System

The multi-agent knowledge base for the Kanamecide chess-engine project. It is a plain
Markdown + YAML repository (no databases, no web app) so that humans and Cline agents can
read and edit it directly, and Git can version every change.

## Why it exists

Multiple independent AI agents work on this project over months. A brand-new agent must be
able to reconstruct: what is being built, why decisions were made, what each agent believes,
where they disagree, what was tested, what failed, what succeeded, and what remains unclear.

## The cardinal rule (read this first)

> **An agent's opinion is NOT a project fact.**
> **An experiment result is stronger evidence than an agent's confidence.**

Keep these categories strictly separate:

| What | Where | Meaning |
|---|---|---|
| FACTS | `research/project_state.md` | Evidence-backed (code, benchmarks, tests, docs). |
| AGENT BELIEFS | `research/agents/<agent>/` | What one agent currently believes. |
| HYPOTHESES | `research/hypotheses/` | Might be true; not yet established. |
| DISAGREEMENTS | `research/debates/` | Material differences between agents. |
| DECISIONS | `research/decisions/` | What the project has adopted (immutable). |
| EXPERIMENTS | `research/experiments/` | Controlled tests and measured results. |
| FAILURES | `research/failures/` | Failed approaches and lessons. |
| REVIEWS | `research/reviews/` | A second/third-agent critique of a report or record. |

Never write "Kimi thinks X" into `project_state.md`; only after the project adopts it via a
`DEC-####` decision does it become the project architecture.

## Directory structure

```text
research/
├── README.md            # this file — index + instructions
├── index.md             # auto-generated index (run `research update`)
├── project_state.md     # shared, evidence-backed project summary
│
├── agents/              # one role per directory (model-independent)
│   ├── ASSIGNMENTS.md   # maps models -> roles (survives provider changes)
│   ├── researcher-architect/{profile.md, current_position.md, beliefs.md, reports/}
│   ├── systems-researcher/{...}
│   ├── adversarial-reviewer/{...}
│   └── implementation-engineer/{...}
│
├── hypotheses/          # H-#### records
├── debates/             # D-#### records
├── decisions/           # DEC-#### records (immutable history)
├── experiments/         # E-##### records
├── failures/            # F-#### records
├── reviews/             # R-#### records
├── templates/           # reusable scaffolds used by `research new-*`
├── context/             # generated context packs (derived; gitignored)
└── scripts/research.py  # the CLI (stdlib-only Python)
```

## The fact/opinion labels

Every record carries a `type` in its YAML front-matter, and every *record* also carries an
`example` flag (`true` = mock/demonstration data, `false` = real history). Key statuses:

- **Hypothesis:** `OPEN`, `TESTING`, `SUPPORTED`, `REJECTED`, `INCONCLUSIVE`, `SUPERSEDED`.
- **Debate:** `OPEN` (unresolved) or `RESOLVED` (never force a false consensus).
- **Decision:** `ACTIVE` or `SUPERSEDED` (set `superseded_by: DEC-####`; never delete).
- **Experiment:** `PENDING`, `RUNNING`, `COMPLETED`, `ABANDONED`; plus `result`
  (`WIN` / `LOSS` / `NEUTRAL` / `INCONCLUSIVE`).
- **Failure:** `RECORDED`.

## Minimum onboarding reading for a new agent

In this order:

1. `research/project_state.md` — what we are building and its current facts.
2. `research/decisions/` — why the current architecture is what it is.
3. `research/hypotheses/` — open questions and their proposed tests.
4. `research/debates/` — where agents disagree and why.
5. `research/agents/` — each agent's `profile.md` and `current_position.md`.
6. `research/failures/` — mistakes to avoid repeating.

For a one-command overview, run `python research/scripts/research.py status`.

## Agent workflow

```text
enter project
   ↓
read project_state.md + index.md
   ↓
read relevant decisions, hypotheses, debates, agent positions
   ↓
perform independent reasoning
   ↓
write an immutable report under agents/<you>/reports/
   ↓
update agents/<you>/current_position.md
   ↓
create/update a belief (agents/<you>/beliefs.md) or hypothesis if warranted
   ↓
record a disagreement (debates/) if warranted
   ↓
propose an experiment (experiments/)
```

An idea does **not** become code. Ideas become hypotheses first; experiments (not opinions)
decide them; decisions codify what is adopted.

Independence is mandatory: other agents' conclusions are hypotheses to evaluate, not facts
to inherit. Read them, find the strong and weak arguments, disagree when warranted, explain
why, and change your own position when evidence actually changes your mind.

## Commands

From the repo root (PowerShell/Windows):

```powershell
python research/scripts/research.py status         # project research summary
python research/scripts/research.py agents         # list agents + confidence/focus
python research/scripts/research.py hypotheses     # list hypotheses
python research/scripts/research.py debates        # list disagreements
python research/scripts/research.py decisions      # list decisions
python research/scripts/research.py experiments    # list experiments
python research/scripts/research.py failures       # list failures
python research/scripts/research.py update         # regenerate index.md
python research/scripts/research.py validate       # check record integrity
python research/scripts/research.py context --topic search   # focused briefing
python research/scripts/research.py new-hypothesis --title "..."   # scaffold (next ID)
python research/scripts/research.py new-debate --title "..."
python research/scripts/research.py new-decision --title "..."
python research/scripts/research.py new-experiment --title "..."
python research/scripts/research.py new-failure --title "..."
python research/scripts/research.py new-review --reviewer X --target H-0001
python research/scripts/research.py new-agent NAME --role "Role Title"
python research/scripts/research.py report AGENT --title "..."
```

A convenience wrapper `research.bat` exists at the repo root, so `.\research.bat status`
also works. The Python form is the canonical, portable one.

## ID scheme

`H-####` hypotheses · `D-####` debates · `DEC-####` decisions · `E-#####` experiments ·
`F-####` failures · `R-####` reviews. The `new-*` commands auto-assign the next ID.

## Record formats

See `research/templates/` for the canonical scaffold of every record type. Every
hypothesis/debate/decision/experiment/failure/review file begins with YAML front-matter
and follows with a fixed set of Markdown headings. Keep the front-matter fields — the CLI
reads them.

## Cross-review flow

```text
Agent A report  →  Agent B reviews  →  Agent C reviews  →  debate  →  experiment
```

A review identifies agreements, disagreements, missing arguments, factual errors, hidden
assumptions, and proposed experiments. **A review never edits the original report** — it lives
in `reviews/` and is linked to its target.

## Model independence

Agents are identified by **role**, never by model: `researcher-architect`, `systems-researcher`,
`adversarial-reviewer`, `implementation-engineer`. A model can be assigned to a role later;
the model↔role mapping lives in `research/agents/ASSIGNMENTS.md`. This keeps research memory
valid if a model or provider changes.

## Git

All research documents are plain text and are committed normally. Link experiments to engine
commits, decisions to implementation commits, and record engine versions. Don't commit large
datasets. Derived `research/context/` packs are gitignored and regenerated on demand.

## Seeded example data

`H-0001`, `D-0001`, `E-0001`, `F-0001`, and `R-0001` are **mock examples** (front-matter
`example: true`) that demonstrate the formats. They are NOT real research. `DEC-0001` …
`DEC-0007` are real decision records reconstructed from the project's `README.md` and the
creation of this system.
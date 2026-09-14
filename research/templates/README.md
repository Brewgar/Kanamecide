# Templates

Reusable scaffolds for every record type. The `research` CLI (`new-*` commands) reads
these templates and fills in the `{{ID}}`, `{{TITLE}}`, `{{AGENT}}`, `{{ROLE}}`, and
`{{DATE}}` placeholders.

## Epistemic records (what we know)

| Template | Used by | Lives in |
|---|---|---|
| hypothesis.md | `new-hypothesis` | `research/hypotheses/` |
| debate.md | `new-debate` | `research/debates/` |
| decision.md | `new-decision` | `research/decisions/` |
| experiment.md | `new-experiment` | `research/experiments/` |
| failure.md | `new-failure` | `research/failures/` |
| review.md | `new-review` | `research/reviews/` |
| report.md | `report` | `research/agents/<role>/reports/` |

## Coordination records (what we are doing, and proof it happened)

| Template | Used by | Lives in |
|---|---|---|
| work_item.md | `new-work` | `research/work/` |
| handoff.md | `new-handoff` | `research/handoffs/` |
| run.md | `new-run` / `runjob.py` | `research/runs/` |
| session.md | `new-session` | `research/sessions/` |
| agent_profile.md | `new-agent` | `research/agents/<role>/profile.md` |
| current_position.md | `new-agent` | `research/agents/<role>/current_position.md` |
| beliefs.md | `new-agent` | `research/agents/<role>/beliefs.md` |

Keep front-matter fields intact — the CLI and `validate` rely on them. Every *record*
must carry `id` (where applicable), `type`, `title`, `status`, `created`, and `example`
(`true` = mock/demonstration data, `false` = real history). Status values are closed
vocabularies enforced by `validate` — an unknown status is a loud error, never a
silently dropped record (see `research/SYSTEM.md` §2).

The `experiment.md` template carries four sections that are enforced for experiments
created on/after 2026-09-15: **Pre-Registered Decision Rule**, **Power And Sample
Size**, **Sample Validity**, and **Provenance**. They exist because the project was
burned by a rule that could not be decided at its planned N, by an arm that never
differed, and by a sample that was 80% duplicate games.

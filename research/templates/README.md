# Templates

Reusable scaffolds for every record type. The `research` CLI (`new-*` commands) reads
these templates and fills in the `{{ID}}`, `{{TITLE}}`, `{{AGENT}}`, `{{ROLE}}`, and
`{{DATE}}` placeholders.

| Template | Used by |
|---|---|
| agent_profile.md | `new-agent` |
| current_position.md | `new-agent` |
| beliefs.md | `new-agent` |
| hypothesis.md | `new-hypothesis` |
| debate.md | `new-debate` |
| decision.md | `new-decision` |
| experiment.md | `new-experiment` |
| failure.md | `new-failure` |
| review.md | `new-review` |
| report.md | `report` |

Keep front-matter fields intact — the CLI and `validate` rely on them. Every *record*
(hypothesis / debate / decision / experiment / failure / review) must carry these
front-matter fields: `id`, `type`, `title`, `status`, `created`, and `example`
(`true` = mock/demonstration data, `false` = real history).
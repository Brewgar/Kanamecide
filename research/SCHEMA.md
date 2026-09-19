# SCHEMA — the Kanamecide research-memory data model (DEC-0011)

> This file is the normative reference for the derived-intelligence layer's schema.
> The records are the truth; this file describes the shape a reader may rely on.

## 0. Principles

1. **Append-only, Git-versioned Markdown is the canonical store** (DEC-0007, DEC-0009).
2. **Everything derived is recomputable and disposable.** `state.md`, `state.json`,
   `research/context/*`, the graph — delete them and re-run `research.py state --write`.
3. **Projections point; they never conclude.** A rollup labels its sources and never
   merges, rewrites, or claims. Output says PROJECTION/CANDIDATE, not fact.
4. **Stdlib only, offline, deterministic.** Same repo, byte-identical output.
5. **Backwards compatible.** Legacy records parse with documented defaults and show as
   warnings, not errors (records are never rewritten to satisfy a new field).

## 1. Memory layers

| Layer | Home | What it is |
|---|---|---|
| L0 raw evidence | `research/evidence/` (EV-####) | Manifest for a raw artifact: `path`, `sha256`, `regenerate` command, retention, `cites`. |
| L1 events | existing: `experiments/`, `work/`, `handoffs/`, `runs/`, `sessions/` | Something that happened, with exit code + evidence. |
| L2 knowledge | existing: `hypotheses/`, `debates/`, `decisions/`, `reviews/`, `failures/` | A claim, an argument, a verdict. |
| L3 current state | `state.md` + `state.json` (GENERATED) + `questions/` (Q-####) | What's currently believed, open, disputed. |
| L4 strategic+meta | `principles/` (PR-####) | Durable lessons (`kind: strategic` or `meta`) that outlive a round. |
| L5 agent memory | `agents/<role>/` | What one agent believes/owns. |
| L6 meta-memory | `audit` metrics + `principles/`(`kind: meta`) | Knowledge about how the project itself learns. |

## 2. Record kinds + status vocabularies (closed)

| Kind | Dir | Status vocabulary |
|---|---|---|
| hypothesis | hypotheses/ | OPEN TESTING SUPPORTED REJECTED INCONCLUSIVE SUPERSEDED |
| debate | debates/ | OPEN ROUTED RESOLVED SUPERSEDED |
| decision | decisions/ | ACTIVE SUPERSEDED PROPOSED |
| experiment | experiments/ | PENDING RUNNING COMPLETED ABANDONED (+ verdict in `result`: PASS/FAIL/WIN/LOSS/NEUTRAL/INCONCLUSIVE) |
| failure | failures/ | RECORDED |
| review | reviews/ | DRAFT IN_REVIEW COMPLETED |
| work | work/ | OPEN IN_PROGRESS BLOCKED DONE CANCELLED |
| handoff | handoffs/ | REQUESTED ACCEPTED DONE REJECTED WITHDRAWN |
| run | runs/ | PLANNED RUNNING COMPLETED FAILED ABANDONED |
| session | sessions/ | OPEN CLOSED |
| question | questions/ | OPEN INVESTIGATING ANSWERED BLOCKED ABANDONED SUPERSEDED |
| principle | principles/ | ACTIVE REVISED RETIRED |
| evidence | evidence/ | REGISTERED SUPERSEDED LOST |
| report (agent) | agents/<r>/reports/ | (informed; not lifecycle-gated) |

Unknown statuses fail `validate` loudly.

## 3. The knowledge graph (typed edges)

Edges are read from record front-matter and prose. A record links to another via its id.

Relation fields an agent may set in front-matter (a subset fires edges):

`tests`, `supports`, `contradicts`, `depends_on`, `supersedes`, `superseded_by`,
`verifies`, `derived_from`, `implements`, `falsified_by`, `revisit_when`, `answers`,
`blocked_by`, `resolved_by`, `evidence` (EV-####), `cites`, `related`.

Actor fields (`owner`, `author`, `agent`, `reviewer`, `from`, `to`, `verified_by`) become
actor edges. `src/…` and `tools/…` paths and commit hashes in a record's body become
code/provenance edges. `touches-code` links an idea to the code that embodies it.

## 4. Epistemic status and confidence

A record's `confidence` is a **belief, never evidence**. The layer maps it to a band:

| Confidence | Label (calibrated) |
|---|---|
| < 0.3 | speculative |
| >= 0.3 | plausible |
| >= 0.55 | likely |
| >= 0.75 | strongly supported |
| >= 0.9 | high-author-confidence (still not "fact") |

A claim may be additionally marked post-experiment by the rollup (a hypothesis is upgraded
only by a PASSing experiment, never by confidence).

Epistemic classes a record may self-tag: `observation | fact | hypothesis | heuristic |
implementation-detail | causal | correlational | proof | rejected | decision`. Use `status`
for lifecycle, `result` for verdict, and the calibrated band for belief strength.

## 5. Negative knowledge + revival

A failure, rejected hypothesis, inconclusive experiment, or superseded decision carries
`revisit_when:` — the condition under which the failure result might change (new hardware,
new architecture, new training data). `research.py revivals` lists records with this
condition set so a "we decided not to" can become a "worth testing again" on schedule.

## 6. Migration policy

To evolve the schema: bump `SCHEMA_VERSION` in `memorylib.py`, document the new field here,
and teach the parser to supply a default for old records (they are never rewritten). A
changing field definition ships with a record that says so. `research.py schema --check`
reports which records lack which declared fields.

## 7. Observability

`research.py audit` reports: counts by kind/status, dangling ids, evidence drift, completed
experiments without Provenance, hypotheses marked SUPPORTED but untested, contradiction and
duplicate candidates, open-question count, revival count. These are the memory's own
vital signs; a rising contradiction-count is a research queue, not a bug.

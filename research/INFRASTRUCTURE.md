# INFRASTRUCTURE — the Kanamecide institutional-memory layer (normative)

> **Authority.** This file is the normative description of the institutional-memory
> primitives that `research/scripts/imem*.py` compute over the canonical Markdown store.
> It exists so that the *infrastructure itself* is not rediscovered from prose in code
> comments. `research/SYSTEM.md` owns roles and process; `research/SCHEMA.md` owns the
> DEC-0011 data/record model this layer extends; `research/project_state.md` owns facts.
> Where they disagree: `SYSTEM.md` for process, `project_state.md` for facts, and this
> file for the derived-intelligence layer's machinery. The Markdown records are the
> truth; every derived view here is recomputable and disposable.

## 0. The one-page invariant

1. **Canonical store = Git-versioned Markdown records.** The only source of truth is
   `research/<kind>/<ID>-....md` (with YAML front-matter). Derived state lives in
   `research/_index/` (`imem.sqlite`, `imem.json`, `metrics.json`) and must not be read
   as evidence. Every derived artifact is deterministic, `stdlib`-only, and offline.
   An existing record is *addended* — never rewritten; a superseded record is
   *marked* (`status: SUPERSEDED`) — never deleted.
2. **The layer's job is retrieval and gates, not conclusions.** Search, beliefs,
   contradictions, duplicates, revivals, provenance, promotion ladders: every derived
   stance is labelled PROJECTION or CANDIDATE and points at record ids; the records
   decide. A finding is never closed by a projection.
3. **Governance is deterministic where determinism is possible.** Anchors pin block
   hashes; links pin ids and record anchors; findings pin a target and a severity; work
   items pin an exit check; evidence pins a sha256. Prose-only ids and line-number
   pointers (`L1376`) are the known historical harms (the R-0021/S-0032 seam path) and
   are flagged by lint, never trusted as structure.

## 1. Primitive vocabulary

| Primitive | Where it lives | Written by | Meaning |
|---|---|---|---|
| `anchors:` front-matter | `<record>.md` | `imem.py repin` / the store's authors | `slug: sha8` pairs; machine-proof that a block was not silently re-pinned to different content |
| `[[ID#anchor]]` | prose | a record's author | inline link, machine-checked but advisory (the `#anchor` accessor makes it stable) |
| typed front-matter edges | `<record>.md` | the record's author | graph of `tests`, `supports`, `contradicts`, `depends_on`, `supersedes`, `derived_from`, `implements`, ... (see `imem_core.EDGE_FIELDS`) |
| `evidence:` | `research/evidence/EV-####` | an evidence record's author | artifact manifest — path + sha256 + regenerate + cites — with a read-time re-hash check |
| `claim` | `research/claims/CLM-####` | `new-claim` | atomic, typed, direction-bearing statement the contradiction/priority engines reason over |
| `finding` | `research/findings/FND-####` | `new-finding` / review tools | closeable defect raised by a review; severity `blocking|major|minor|nit` with attributable `raised_by`/`resolved_by`/`verified_by` |
| `question` | `research/questions/Q-####` | `new-question` | persistent open-questions registry with `depends_on` / `suggested_experiments` / `blocked_by` |

Ids that occur only in prose are `prose ids`: the graph captures them as provenance, the
lint warns when a record carries many, and any id whose weight matters is declared in
front-matter or as an inline `[[ID]]` anchor.

## 2. Record layering

`layer_of(kind)` (`research/scripts/memorylib.py` `LAYERS`) is canonical:

- **L0 — Raw evidence** — pinned artifacts: `research/evidence/EV-####` manifests; engine binaries and raw JSONL under gitignored paths.
- **L1 — Events (workflow)** — `experiments/`, `work/`, `handoffs/`, `runs/`, `sessions/`: something that happened or is due, with exit evidence and a heartbeat where a long-running job is involved (see `SYSTEM.md` §6 and `runjob.py`).
- **L2 — Knowledge / arguments** — `hypotheses/`, `debates/`, `decisions/`, `reviews/`, `failures/`: what we believe (how well), each with falsifiers.
- **L3 — Current state** — `research/state.md` + `state.json` (GENERATED), `questions/`, `principles/`.
- **L4 — Strategic + meta** — durable lessons.
- **L5 — Agent memory** — `agents/<role>/`.
- **L6 — Meta memory** — `meta`, `pathologies`, `velocity`, `agents`, `promote` outputs.

A record may move on these layers *by evidence only*: superseded, promoted by L5 adoption, demoted by falsifying experiments. The promotion ladder in
`imem_evidence.py` implements the rung computation: **L0** raw → **L1** anchored →
**L2** tested → **L3** measured → **L4** reproduced → **L5** adopted. A hypothesis marked
SUPPORTED requires an L3-measured rung; `promote --strict` (or the corpus-level invariant) reports any SUPPORTED at L0/L1/L2 as a mismatch; the current-state rollups (state.md / state.json) re-derive it by running the same inputs; an author's confidence is a belief lever, not evidence.

Claims carry `direction` from the closed vocabulary in `imem_core.DIRECTION`, so
contradiction detection is structural (`claim A direction-higher vs claim B direction-lower on the same domain/parameter overlapping scope`) rather than a hand-written antonym list — which is how the H-0005/H-0006 pair was found by hand a round late in December, and what DEC-0012's closed `direction` field makes structural.

## 3. The retrieval contract

Answer a reader's query in this order:

1. **Lexical** — `research.py search` (BM25) / `imem.py search` for exact anchors and
   front-matter; the knowledge graph (`imem.py graph`).
2. **Semantic** — `imem.py search/ask/similar` (Random Indexing: a Sahlgren-style
   ternary-signature space built from the live corpus; same corpus → same ranking;
   deterministic, offline, stdlib-only; switchable off with `--no-semantic`).
3. **Graph** — `imem.py graph` / `chain` / `provenance` for links, actor edges and
   code-touchpoint edges.

Every projection is labelled and keeps its columns tied to record ids; the id is the
object of truth, not the ranking itself. At scale the derived store is a cache:
`imem.py index` rebuilds `_index/imem.sqlite` (+ `_index/imem.json`) and nothing is lost
if it is deleted.

## 4. Findings and the claim-ledger gates

A **finding** is a defect-of-record targeting some other record (or a core record's
live state). It is filed with a `severity` and attributable `raised_by`, reviewed by a
separate seat, and closed only by resolution evidence (`resolved_by`, `verified_by`, and
the `## Resolution` addendum) plus a `closed:` date. `imem.py lint` escalates a
hard `PROBLEM` when an `OPEN` + `blocking` finding targets a RUNNING/COMPLETED target,
and closes otherwise as advisory warnings. That is the deterministic shape of
"reviewers never edit the record": a defect cannot block forever, and its closure
itself is a ledger entry (the reviewer does not get to bless its own defect away).

A **claim** is an atomic typed statement: `domain`, `parameter`, `direction`, `scope`,
`epistemic`, plus whether the evidence supports it for (`supports`), against it
(`contradicts`), or by whom and what unblocks it (`tests` / `depends_on`)
(research/scripts/imem_claims.py). Contradiction candidates (direction-opposing claims on
the same domain + shared parameter, wedge between two sessions' texts) and duplicate
candidates (same parameter + polarity, or semantic similarity using `EmbedSpace` cosine)
are emitted; agents decide whether a candidate is a true conflict or a merge target.
Revival triggers (`revisit_when:` lines with a compute trigger) are evaluated against
`research/_index/metrics.json`; the current-state `revivals` list, with the trigger
code's state, is the instrument that lets a "we decided not to" become a "worth another
attempt."

## 5. Promotion, novelty, and freshness gates

- **Promotion ladder** (`imem.py promote`, `imem_evidence.py`): **L0** raw → **L1**
  anchored → **L2** tested → **L3** measured → **L4** reproduced → **L5** adopted.
  A hypothesis may only be SUPPORTED at L3+; `promote --strict` reports mismatches.
- **Novelty** (`imem.py novelty <id|text>`): the pre-file diagnostic. Given free text or
  a record id, it returns the closest existing claims/hypotheses with the comparison's
  *basis* (lexical token overlap / corpus-relative semantic cosine / same
  domain+parameter), never merging. A claim is genuinely new to the project as *judged
  by its author against the candidates shown*, with an *exit* flag on `--strict` for
  filing scripts. Not editing history to prove scarcity.
- **Freshness** (`imem.py freshness`): live (non-terminal) records older than their
  kind's window are surfaced with the rule's number (`window_days`) and the *last
  authored date* (never file mtimes, which are checkout-noisy), so a live record that
  has gone quiet is a review flag rather than silent drift. Advisory only, never an
  error; `--max-age` widens/narrows without touching the policy. Terminal records are
  history, not stale debt.

## 6. Authority, gates, and the seat model

- Decisions are immutable history: only a newer decision supersedes (`status:
  SUPERSEDED` + `superseded_by:`); no deletion.
- The verifier is never the owner (SYSTEM.md Gate 3; PR-0004): a record's `verified_by`
  must point at the function that recomputed the evidence, not at the function that
  wrote the conclusion. Self-closure followed by a separate reviewer is the pattern
  (see FND-0032 and HO-0021).
- An evidence manifest is only as good as its read-time guard (`imem.py evidence`
  compares pinned `sha256` with the bytes on disk). Assertion drift is a finding, not
  an emergent claim.
- `project_state.md` carries a machine block (`research-meta`: `last_updated`,
  `reflects`, `not_reflected`) that `research.py validate` enforces: stale summaries
  fail loudly, dated.

## 7. Constraints baked into the environment

- This host is Windows/PowerShell; harnesses may report a false "exit 1" on success and
  shell-redirection re-encodes text (UTF-16 `>`, BOM on `Set-Content -Encoding utf8`).
  Every gate's verdict comes from redirected file contents under `_obs/` (or
  `research/context/`), never from a harness's own report; binary-sensitive records are
  hashed byte-wise in Python from `git cat-file blob`, never by redirecting shell text.
  (S-0034/S-0036/R-0025 environment notes carry the incidents.)
- Jobs that outlive a shell command run under `research/scripts/runjob.py` (detached
  launch, heartbeat, checkpoint, resume). A stale heartbeat means DEAD — never report
  "still running"without a fresh heartbeat you read this session.
- Concurrency cap on this 8C/16T host: ≤ 2 concurrent engine matches; 12 concurrent
  engines stalled at game ~26–32 in Round 3 (project precedent).

## 8. Known limits and open directions

1. Semantic retrieval is an offline, deterministic *approximation* (Random Indexing):
   it catches jargon-matched meaning across authors in a corpus of this size; a much
   larger corpus would justify a measured upgrade, and any such upgrade lands through
   this doc's own migration rule, never silently.
2. `research.py search` is lexical + graph (BM25); `imem.py` adds the fused
   lexical+semantic+graph projection (`ask`). Both label outputs PROJECTION; readers do
   not need to prefer one — the ids they name are the system of record.
3. `contradictions` / `duplicates` / `revivals` / `priority` / `freshness` / `novelty`
   emit candidates; only an agent decides a candidate is a true conflict, duplicate,
   revival candidate, or priority — and the merge/ruling lands as addenda on records,
   never tool-side.
4. `core_schema.py` declares epistemic classes not yet populated by present record
   kinds (platform, meta); their vocabulary rolls into `SCHEMA.md` §6–§7 as the schema
   grows, with documented defaults for old records (records are never rewritten).
5. Raw session captures inside `research/context/`, `_obs/`, `build/`, or `m0_audit/`
   are gitignored scratch/evidence: a reader lifts what a session left, but the durable
   record store — and this file's contract — applies only to `research/*` and to a
   manifest's pinned artifacts.

## 9. Performance and scale notes (measured here)

- `_index/imem.sqlite` ≈ 3.7 MB for ~248 records, rebuilt in place by `imem.py
  index`; deleting it loses nothing (the cache property).
- `imem.py lint` runs in well under a second at this corpus size; the heaviest read is
  the EmbedSpace build, which is linear in corpus tokens (RI, not SVD — the SVD path is
  reserved for long batch runs; see `imem_text.EmbedSpace.build(method=`)`).

## 10. Migration policy

1. Bump `SCHEMA_VERSION` in `memorylib.py`; document the new field in `SCHEMA.md`; teach
   parsers to supply a documented default for old records (records are never rewritten).
2. Rebuild the derived store (`imem.py index`; `research.py state --write`) after any
   change; every migration is a small commit whose evidence is the diff and the tests.
3. Pruning the store out of policy only ever happens as deliberate moves (to `_obs/`
   or a versioned path), logged and attributably committed — never force-deleting
   history.

## Appendix A — where each engine lives

- `research/scripts/research.py` — canonical CLI + validators: `status`/`next`/
  `context`, `new-*` scaffolds, `work`/`runs`/`handoffs`, `round`, `validate`,
  `selftest`, `hygiene`, `audit`, `update`, `state --write`.
- `research/scripts/memorylib.py` — derived-intelligence store algorithms:
  `load_nodes`, `code_nodes`, `build_graph`, BM25 search, belief rollup,
  contradiction/duplicate/revival candidates, timeline, `evidence_inventory`,
  `audit`, `state`.
- `research/scripts/kgraph.py` — compatibility shim exposing those commands through
  the older name (pre-DEC-0011 surface).
- `research/scripts/imem*.py` — the DEC-0012 institutional layer: anchors, links,
  claims/findings ledgers, `lint`, fused retrieval (`search`/`ask`/`similar`/`brief`/
  `chain`/`provenance`/`codemap`), `contradictions`, `duplicates`, `promote`,
  `priority`, `questions`, `evidence`, `prereg`, `agents`, `handoff`, `meta`,
  `pathologies`, `velocity`, `freshness`, `novelty`, `audit`, `snapshot`, `metrics`,
  `new-claim`/`new-finding` writers; its own unit/corpus suite
  `research/scripts/tests_imem.py`; long-running execution in
  `research/scripts/runjob.py`.

## Appendix B — governance lineage

DEC-0007 (Markdown store) → DEC-0009 (verification/coordination + SYSTEM.md) →
DEC-0011 (derived-intelligence layer; memorylib + kgraph shim) → DEC-0012 (claim/finding
ledger + the deterministic lint gate; the v2 imem suite) → today's additions (v2.1:
freshness + novelty surfaces). Decisions supersede, they never disappear.



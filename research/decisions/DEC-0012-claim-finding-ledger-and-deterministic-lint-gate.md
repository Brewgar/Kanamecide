---
id: DEC-0012
type: decision
title: "Claim/finding ledger (CLM/FND record kinds) with a deterministic severity-vocabulary lint gate, built as a derived intelligence layer"
status: ACTIVE
superseded_by: null
amends: [DEC-0011]
evidence: []
example: false
created: 2026-09-30
---

# DEC-0012 — Claim/finding ledger and deterministic lint gate

## Decision
DEC-0011's derived-intelligence layer is **extended, not amended in behaviour**: the
existing graph/retrieval/audit machinery is retained unchanged. This decision adds a
ledger substrate for two things the original record types expressed badly:

1. **Two new record kinds** with closed vocabularies: `claims/` (CLM-####,
   `status: OPEN|DISCHARGED|WITHDRAWN`) and `findings/` (FND-####,
   `status: OPEN|CLOSED`, `severity: blocking|major|minor`, `raised_by` must name the
   author + context, and closers must state the same in `--by`).
2. **A derived institutional-memory layer** (`research/scripts/imem.py`, built on
   `memorylib.py` + `core_schema.py`/`fixtures_core.py`): markdown stays canonical
   (DEC-0007), storage (`research/_index/imem.sqlite3` + `_obs/`) is derived and
   disposable (git-ignored, regenerable with `imem.py index`), all commands are
   deterministic/stdlib-only/offline, 31 subcommands (index, lint, anchors, repin,
   graph, links, search, ask, similar, beliefs, chain, provenance, contradictions,
   duplicates, revivals, priority, questions, evidence, prereg, promote, findings,
   finding, agents, blind, handoff, brief, meta, pathologies, velocity, codemap,
   snapshot, metrics, selftest, version).
3. **Two new gates** and one interlock: `findings_lint` (extends `audit`) checks the
   FND/CLM vocabulary and yields `problems`/`warnings` (blocking-only strictness:
   open `blocking` findings are `problems`, everything else advisory); `validate`
   declares a problem when a RUNNING/PAUSED target carries OPEN blocking findings;
   and both rules are locked into `tests_imem.py` so the gates cannot erode quietly.

## Context
The R-0019 critique of E-0013 produced ledger objects — claims (B1..B7) and findings
(F-U1..F-U13, X1-X4, Z1-Z4) — that lived only as rows inside session and review prose:
grep-able, but not queryable, not status-tracked, and invisible to any gate. The 2026-09-30
session (S-0041's precursor sessions) built the layer and **migrated the E-0013 corpus into
FND-0001..0022 + CLM-0001..0003, filed OPEN by design** so the discharge of each row is an
explicit, attributable act; the same session added four standing questions (Q-0001..0004)
and six research principles (RULES_OF_ENGAGEMENT). Enactment: `74aed25` (tooling) +
`a8a902a` (migration), both under this decision's banner; this record was authored after
the build to close the governance gap (the decision was referenced by version stamp and
commit messages before it had a record). **Recorded retroactively; states intent, does not
redefine the enacted system.**

## Alternatives Considered
- Folding the ledger into `research.py`: rejected — `research.py` guards the canonical
  store; imem is a sworn-derived layer, which keeps DEC-0007's "Markdown is canonical"
  load-bearing and makes the whole layer recoverable by reindex.
- Free-text severities (high/low, critical): rejected — closed vocabularies are what
  make the lint gate deterministic; open vocabularies turned the old gates into prose.
- Severity-strength lint (all severities block): rejected — majors/minors blocking the
  gate would incentivise silent severity downgrades; only `blocking` findings gate.

## Arguments
- **Disposable by construction**: `imem.py index` rebuilds everything from the markdown;
  `rm research/_index/imem.sqlite3` loses nothing.
- **Institutional memory**: a finding filed, migrated, repaired, and re-found can be
  recalled five sessions later (`imem.py findings`, `recall`, cross-agent review) —
  the failure mode the layer exists to prevent is *finding the same bug twice*.
- The corpus migrations are **idempotent** (`created=0` on re-run), so reruns are safe
  and the ledger is auditable.

## Evidence
- `research/scripts/imem.py` header (VERSION `2.0.0 (DEC-0012)`) + commits `74aed25`,
  `a8a902a`; self-test `imem.py selftest` (43/43 at enactment).
- This record itself resolves the two `unresolvable link` lint problems produced when
  R-0026 and S-0041 linked `related: DEC-0012` before the record existed.

## Agents Involved
Chief-architect agent (decision and build mandate), verification-auditor (ledger
closure round; flagged the missing record by linking it).

## Why This Was Chosen
Claims and findings are the natural unit of a research critique, and only a gated
ledger makes "we fixed the reviewer vector" a *checkable* statement instead of a
session-log assertion.

## Reversal Conditions
If two rounds of use show the FND/CLM gates produce busywork without catching real
defects, demote the lint to advisory and mark this SUPERSEDED; the records remain.

## Date
2026-09-30

> This record amends DEC-0011 (which remains ACTIVE). The ledger layer never rewrites a
> record; closures/dispositions are attributable acts recorded in the rows themselves,
> and independently verified per Gate 3 (R-0026). See `research/templates/claim.md`,
> `research/templates/finding.md`, `research/SYSTEM.md` §12.

## Addendum 2026-09-30 — erratum: status vocabularies are implementation-defined (FND-0032)

Item 1 of the Decision section states the findings status vocabulary as `OPEN|CLOSED`.
That token is **stale**: the vocabulary of record is the implementation —
`research/scripts/imem_core.py` `STATUS_VOCAB_EXTRA["finding"]` =
`{OPEN, RESOLVED, DISPUTED, WITHDRAWN, SUPERSEDED}`, and
`research/scripts/imem.py` `finding --close` writes `status: RESOLVED` (L395).
`research/templates/finding.md` was annotated to match (7ff12b9). The Decision line
stands verbatim as the record of what was written; the implementation line governs.
The same rule applies to the `claims/` line: for both kinds, the implementation —
not this record's prose — is the vocabulary of record. Raised by the
verification-auditor as FND-0032 (round-5 ledger-tail premise check); corrected by
the record author. DEC-0012 remains ACTIVE and is otherwise unchanged.

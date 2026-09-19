---
id: R-0005
type: review
reviewer: chief-architect (research-systems, Round-5 seat)
target: "the DEC-0007/DEC-0009 memory system as a whole (this session's re-audit)"
kind: audit
work_item: W-0007
status: COMPLETED
example: false
created: 2026-09-19
---

# R-0005 — Audit of the memory system itself, and what DEC-0011 adds

## Scope
Every file in the repository was read or inspected (code, records, logs, harness scripts,
history) before any change. DEC-0011 was then designed against the observed gaps only.

## What the prior system got right (kept, not broken)
- DEC-0007 directory truth-separation and append-only records.
- DEC-0009 gates: closed status vocabularies, work-item exit checks, the perft anchor home,
  root-hygiene gate, runjob.py. All retained; extended, not replaced.

## New findings (F13–F25) and their fixes in DEC-0011
- **F13 — agent reports invisible.** The 115 KB+ of deepest analysis (`agents/*/reports/`)
  was never in `index.md`, never validated, never searchable. FIX: reports are first-class
  nodes; `search` retrieves them.
- **F14 — a broken artifact posed as a tool.** `kgraph.py` was an orphaned prototype (no CLI,
  crashed with an `IndentationError` per `context/_kg_audit.txt`, untracked in git). FIX:
  the layer it promised is delivered in `memorylib.py`; `kgraph.py` is a working shim.
- **F15 — no code/provenance traceability.** Ideas could not be traced to code/commits.
  FIX: `codemap` + `touches-code` edges + commit-hash extraction (with a false-positive
  guard for numeric perft counts).
- **F16 — no contradiction / duplicate / revival detection.** The H-0005 backwards bound and
  the H-0006-vs-D-0003 bound conflict were found a round late by hand; the duplicate H-0002
  stubs sat undetected. FIX: `contradictions` / `duplicates` / `revivals` (all CANDIDATES).
- **F17 — hypotheses lacked a falsifier field.** "When would this be wrong?" is now a schema
  field. FIX: rolled into the belief rollup + template guidance.
- **F18 — confidence was a bare number.** FIX: a calibrated ladder (PROJECTION labels +
  `calibrated` bands) so a number is never silently treated as evidence.
- **F19 — evidence was unregistered.** Root-level measurement artifacts existed with no
  manifest, no hashes, no regeneration commands. FIX: `evidence/` records + integrity checks.
- **F20 — no open-questions registry.** FIX: `questions/` (Q-####) with dependencies and
  suggested experiments, so a question survives its author.
- **F21 — no machine-readable current state.** Hand-maintained `project_state.md` + a
  regenerated `index.md` + per-agent position files risked drifting apart. FIX: generated
  `state.md` (human) + `state.json` (machine), never hand-edited.
- **F22 — the memory system had no tests.** FIX: `tests_memory.py` + `research.py selftest`
  (35 tests this session, green).
- **F23 — the hygiene gate found junk but did not classify it.** FIX: `hygiene` splits
  sanctioned / grandfathered-debt / unsanctioned / unreferenced vs referenced-by-records,
  so W-0006 deletion is evidence-driven, not guesswork.
- **F24 — dangling record ids.** `DEC-0010`, `D-0007` are referenced but do not exist
  (W-0002 work) — now surfaced as a `validate` warning rather than silently allowed.
- **F25 — validation never checked reports.** `type: report` had no required-field /
  status enforcement at all. FIX: reports load as records; the corpus completeness check
  now includes them.

## What this changes
- One command (`research.py state --write`) regenerates the Layer-3 view; the same layer
  drives retrieval, contradiction detection, questions, and the audit — all derived.
- Answers the mission's core questions: "show every experiment supporting/contradicting
  H-0009" → `research.py search`/`beliefs`; "why did X fail and when revisit it" →
  `revivals`/evidence; "what implements H-0009" → `codemap`.

## Residual limits (honest)
- The engines' true research value is proven only by future rounds using it; the layer is
  a map, not the territory. Retrieval is BM25+graph, not embeddings (stdlib-only by design).
- `validate` still cannot judge prose quality; it can only guarantee structure and links.
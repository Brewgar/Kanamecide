---
id: DEC-0011
type: decision
title: "Derived-intelligence layer for the research memory (graph, retrieval, state, audit, questions, evidence, principles)"
status: ACTIVE
superseded_by: null
amends: [DEC-0007, DEC-0009]
evidence: []
example: false
created: 2026-09-19
---

# DEC-0011 — Derived-intelligence layer for the research memory

## Decision
DEC-0007's Markdown record store and DEC-0009's verification/coordination gates are
**retained unchanged**. This decision **adds** a read-only, fully-derived intelligence
layer on top, implemented in `research/scripts/memorylib.py` (+ a `kgraph.py` compat
shim) and exposed through the single `research.py` CLI:

1. **A typed knowledge graph** (populated from front-matter relations, prose id
   references, actor fields, `src/` paths and commit hashes) with BFS neighbourhood
   expansion (`graph` / `search` commands).
2. **Ranked retrieval** (BM25, deterministic) with graph-expanded "read these too"
   (`search`).
3. **A computed current-best-belief projection** per hypothesis with its evidence
   rollup (`beliefs`), plus contradiction candidates (`contradictions`), duplicate
   candidates (`duplicates`), a revival/passive-negative registry (`revivals`), and a
   timeline (`timeline`). All outputs are labelled PROJECTIONS or CANDIDATES — they
   point at records, they never conclude or merge.
4. **Three new record kinds** with closed status vocabularies: `questions/` (Q-####,
   persistent open questions), `principles/` (PR-####, strategic + meta memory),
   `evidence/` (EV-####, sha256-manifested raw artifacts with regeneration commands).
5. **A generated Layer-3 state** (`research/state.md` + `research/state.json`, written
   by `research.py state --write`, never hand-edited) and a **codemap** linking records
   to code.
6. **A memory-integrity audit** (`audit`) feeding `validate` advisory checks, plus a
   **hygiene classifier** (`hygiene`) and a **schema registry** (`schema`).
7. **Self-tests** (`tests_memory.py`, run by `research.py selftest`): the memory layer
   is software and must prove itself like the engine does.

## Context
R-0005 (this session's audit) catalogued what the DEC-0007/DEC-0009 system could not
answer: which experiments bear on a hypothesis, which records contradict, which failed
idea deserves a second look, what code implements an idea, and whether the store itself
is consistent. The orphaned `kgraph.py` prototype (line-409 IndentationError, never
wired into the CLI) is evidence this need existed but was never delivered.

## Alternatives Considered
- A database (SQLite/graph DB): rejected (DEC-0007 already weighed it; Markdown stays
  the human/Git source of truth, and the derived layer is trivially recomputable).
- Writing projections back into records: rejected — verbatim records are append-only;
  a derived projection must never masquerade as a concluded fact.
- Embedding-based semantic search: not now (stdlib-only constraint, brittle deps);
  BM25 + graph expansion covers the deterministic, offline need.

## Arguments
- The layer is **derived and disposable**: delete `state.json` and re-run `state
  --write`; nothing is lost. Memory corruption is therefore recoverable by construction.
- Every command is deterministic and offline; tests make the layer itself provable.
- New record kinds follow the existing closed-vocabulary/append-only discipline exactly.

## Evidence
- Self-test suite green (`research.py selftest`, 35 tests) on the real corpus.
- `search`, `beliefs`, `contradictions`, `codemap`, `audit`, `hygiene`, `state`,
  `schema`` demonstrated against the live repository in this session.

## Agents Involved
Chief-architect agent (this session's mandate), respecting DEC-0009 gates.

## Why This Was Chosen
It makes the project's existing collective memory *queryable by meaning, structure and
provenance*, self-auditing, and self-testing — without touching a single existing record.

## Reversal Conditions
If two rounds of measured use find the derived layer misleads more than it informs,
retire it (set this SUPERSEDED) and return to DEC-0009 alone.

## Date
2026-09-19

> This record amends DEC-0007 and DEC-0009 (both remain ACTIVE). The derived layer never
> rewrites a record; `research/SYSTEM.md` §12 is the normative description.

---
id: DEC-0004
type: decision
title: "Make/unmake move application"
status: ACTIVE
superseded_by: null
example: false
created: 2026-09-08
---

# DEC-0004 — Make/unmake move application

## Decision
Moves are applied with make/unmake, not copy-make.

## Context
Search will make and unmake millions of moves; the per-move cost and memory footprint matter.

## Alternatives Considered
(Not formally archived; reconstructed from README.md.) Copy-make (copying the whole board per move).

## Arguments
- Make/unmake avoids per-move board copies.
- The state delta (incl. Zobrist) is cheap to track with a small undo record.

## Evidence
Documented in README.md ("Make/unmake move application (not copy-make)").

## Agents Involved
Pre-dates the agent system; recorded from README.md.

## Why This Was Chosen
Lower allocation and memory traffic in the hot path.

## Reversal Conditions
If a different model (e.g. copy-make on a specialized SIMD board) measured faster with
acceptable memory cost.

## Date
2026-09-08
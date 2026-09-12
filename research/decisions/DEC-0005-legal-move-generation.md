---
id: DEC-0005
type: decision
title: "Legal move generation"
status: SUPERSEDED
superseded_by: DEC-0008
example: false
created: 2026-09-08
---

# DEC-0005 — Legal move generation

## Decision
The engine generates legal moves directly, not pseudo-legal moves + a legality filter.

## Context
Phase 1 correctness depended on never emitting an illegal move (including king-safety cases).

## Alternatives Considered
(Not formally archived; reconstructed from README.md.) Pseudo-legal generation + filter at make time.

## Arguments
- Generating only legal moves guarantees correctness invariants for search.
- Suitable as a rock-solid reference even if a faster pseudo-legal path is added later in the hot loop.

## Evidence
Documented in README.md ("Legal move generation (not pseudo-legal + filter)").
Validated against the Chess Programming Wiki perft suite (exact matches).

## Agents Involved
Pre-dates the agent system; recorded from README.md.

## Why This Was Chosen
Correctness first; performance can be layered on later without changing correctness.

## Reversal Conditions
Likely superseded in the search hot path by a pseudo-legal + fast-legal branch, if
benchmarks justify it — the correctness reference generator would be retained.

## Date
2026-09-08

## Supersession Addendum (researcher-architect, 2026-09-10)

Superseded by **DEC-0008 — Pseudo-legal move generation + king-safety filter at the search/perft
site**, which corrects this record's stated contract to match the actual code and the D-0004
runtime repro (16 pseudo-legal vs 9 legal on `7k/8/8/8/8/8/8/r3R2K w - - 0 1`). The old wording
("generates legal moves directly") did not match `generate_moves` (pseudo-legal except en passant
and castling). This record is retained for provenance and is not deleted.
---
id: DEC-0005
type: decision
title: "Legal move generation"
status: ACTIVE
superseded_by: null
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
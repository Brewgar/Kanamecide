---
id: DEC-0003
type: decision
title: "Incremental Zobrist hashing"
status: ACTIVE
superseded_by: null
example: false
created: 2026-09-08
---

# DEC-0003 — Incremental Zobrist hashing

## Decision
Position keys are produced with incremental Zobrist hashing.

## Context
A fast, collision-resistant position key is required for future transposition tables
and repetition detection.

## Alternatives Considered
(Not formally archived; reconstructed from README.md.) Recomputing keys from scratch per position.

## Arguments
- Incremental updates are O(1) per move (xor-in / xor-out) vs O(n) recomputation.
- Standard practice in strong engines and well understood.

## Evidence
Documented in README.md ("Incremental Zobrist hashing"). Implemented in `src/zobrist.*`.

## Agents Involved
Pre-dates the agent system; recorded from README.md.

## Why This Was Chosen
It is the industry-standard, low-risk approach that directly supports the roadmap.

## Reversal Conditions
Only if benchmarks showed incremental hashing was a bottleneck (very unlikely).

## Date
2026-09-08
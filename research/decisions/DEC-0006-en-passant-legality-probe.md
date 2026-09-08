---
id: DEC-0006
type: decision
title: "En passant legality via make/unmake probe"
status: ACTIVE
superseded_by: null
example: false
created: 2026-09-08
---

# DEC-0006 — En passant legality via make/unmake probe

## Decision
En passant legality is verified with a make/unmake probe, which correctly handles
discovered-check pins on the capturer.

## Context
En passant is the classic source of perft divergence: the capture can expose a sliding
check/pin, making a naive en-passant move illegal.

## Alternatives Considered
(Not formally archived; reconstructed from README.md.) Direct geometric pin analysis.

## Arguments
- The make/unmake probe reuses the exact same legality logic the search will use.
- It guarantees correctness for the subtler pin cases without special-casing.

## Evidence
Documented in README.md; verified by exact perft matches on CPW positions 3/4/5 (EP/pins).

## Agents Involved
Pre-dates the agent system; recorded from README.md.

## Why This Was Chosen
Correctness of the foundational move generator is non-negotiable.

## Reversal Conditions
Only if a faster method is proven correct across the full perft suite AND adds real speed.

## Date
2026-09-08
---
id: CLM-0003
type: claim
title: "Fresh-game overlap must be zero before a fitted artifact is consumed"
status: OPEN
example: false
created: 2026-09-29
domain: data
parameter: training-game-overlap
direction: no_effect
scope: [phase-3]
epistemic: decision
confidence: 0.9
statement: No downstream game may share a normalized-FEN dedup key with the training set before a fitted artifact is consumed.
tested_by: [E-0011, E-0013]
---

# CLM-0003

## Statement
No downstream game may share a normalized-FEN dedup key with the training set before a fitted artifact is consumed.

## Direction and scope
- Domain: data
- Parameter: training-game-overlap
- Direction: no_effect
- Scope: [phase-3]

## Evidence
- See the E-0013 family records.

## What would falsify this
- A pre-registered E-0012-protocol measurement.

## Status
OPEN


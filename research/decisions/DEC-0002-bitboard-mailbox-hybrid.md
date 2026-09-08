---
id: DEC-0002
type: decision
title: "Bitboard + mailbox hybrid board representation"
status: ACTIVE
superseded_by: null
example: false
created: 2026-09-08
---

# DEC-0002 — Bitboard + mailbox hybrid board representation

## Decision
The board representation is a bitboard + mailbox hybrid.

## Context
Correct move generation and board state management were the Phase 1 foundation.
Both representations have complementary strengths (fast occupancy/masks vs. easy
piece/color iteration).

## Alternatives Considered
(Not formally archived; reconstructed from README.md.) Pure bitboard, pure mailbox/0x88.

## Arguments
- Bitboards give cheap attack/occupancy operations.
- The mailbox side keeps per-square logic simple and correct.

## Evidence
Documented in README.md ("Bitboard + mailbox hybrid representation").
Implemented in `src/bitboard.*` and `src/board.*`.

## Agents Involved
Pre-dates the agent system; recorded from README.md.

## Why This Was Chosen
A pragmatic blend of correctness (mailbox) and speed (bitboards).

## Reversal Conditions
If a pure representation proved materially faster without correctness risk.

## Date
2026-09-08
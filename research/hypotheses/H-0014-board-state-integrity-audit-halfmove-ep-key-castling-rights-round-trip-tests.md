---
id: H-0014
type: hypothesis
title: Board state integrity audit - halfmove EP-key castling-rights round-trip tests
status: OPEN
confidence: 0.6
priority: medium
example: false
created: 2026-09-09
last_updated: 2026-09-09
agents_supporting: [researcher-architect]
agents_opposing: []
tags: [correctness, testing, board, zobrist]
---

# H-0014 — Board state integrity audit - halfmove EP-key castling-rights round-trip tests

## Question
Perft counts moves, not clocks or keys: the halfmove reset path (board.cpp:157), the EP
key XOR maintenance (:152-155), and the corner-square castling-rights clearing (:141-144)
are exercised by perft but never asserted on directly. Does a round-trip audit
(make/unmake asserting `same_position` + `key==compute_key`) over a perft walk pass, and
should it become a permanent debug harness?

## Hypothesis
Plausible (0.6): the code is correct by inspection, but these three paths are the classic
sources of search-time corruption (wrong 50-move adjudication, TT key aliasing, illegal
castling out of search). A debug-only audit walk (assert after every make/unmake in a
depth-4 traversal of startpos + kiwipete + cpw3) passes and stays as a regression gate.

## Why We Think This Might Work
`same_position()` (board.cpp:204-213) already compares every field incl. key; wiring it
into a debug traversal is <50 lines. compute_key() gives an independent from-scratch
oracle for the incremental key path.

## Counterarguments
Perft exact-matches already cover move legality end-to-end; clocks/keys do not affect
perft counts, so the audit tests "new" surface with unknown bug probability — could find
nothing (still worth it as a gate for Phase 2, where keys feed the TT).

## Agents Supporting
researcher-architect (0.6, plausible — cheap insurance before TT lands).

## Agents Opposing
(none; adversarial-reviewer invited to extend the audit list.)

## Confidence
0.6 (plausible; outcome unknown until run).

## Proposed Experiment
E-STATEAUDIT (with E-0002): debug traversal asserting after every unmake that
`same_position(before,after)` holds and `key==compute_key`; plus a rights-transition
table test (16 rights states x move/capture events on corner squares) and an EP clock
sequence test. Gate: zero fires across the suite.

## Required Metrics
Audit traversal completes with zero assert fires; rights-table 100% pass; key oracle
agreement on every node visited.

## Status
OPEN

## Result
(none)

## Conclusion
(none)
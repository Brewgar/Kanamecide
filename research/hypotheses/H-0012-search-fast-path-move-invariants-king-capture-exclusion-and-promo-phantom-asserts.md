---
id: H-0012
type: hypothesis
title: Search fast-path move invariants - king-capture exclusion and promo-phantom asserts
status: OPEN
confidence: 0.7
priority: high
example: false
created: 2026-09-09
last_updated: 2026-09-09
agents_supporting: [researcher-architect]
agents_opposing: []
tags: [correctness, search, movegen, invariants]
---

# H-0012 — Search fast-path move invariants - king-capture exclusion and promo-phantom asserts

## Question
`generate_moves` masks destinations with `& ~own` only (movegen.cpp:70-103) — it never
excludes the enemy king square — and `move_promo()` returns a phantom piece on any
non-promotion Move (defs.h:52). Before any search fast path (captures-only gen, SEE,
staging) is built, are both invariants documented and debug-asserted?

## Hypothesis
Yes, required (likely, 0.7): (1) search must exclude captures of the enemy king square at
generation or filter post-make — a king capture is not a legal move, it is a checkmate
detection bug waiting to happen; (2) every `move_promo` call site must assert
`move_flag(m)==PROMOTION` first. In-filtered legal positions the enemy king is never en
prise (every ply is own-king filtered), so perft is unaffected — the risk is future fast
paths plus arbitrary-FEN robustness (`--fen` accepts any FEN today).

## Why We Think This Might Work
Direct inspection: all leaper/slider branches apply only `& ~b.occ[us]`; no branch tests
the destination against the enemy king square. defs.h:52 computes
`KNIGHT+((m>>12)&3)` unconditionally. Cheap asserts close the hole permanently.

## Counterarguments
Filtered play never exposes the case, so asserts are "dead code" until a bug exists —
but that is exactly what asserts are for; cost is zero in Release (NDEBUG).

## Agents Supporting
researcher-architect (0.7, likely — inspection, not yet a failing test).

## Agents Opposing
(none; implementation-engineer invited to confirm assert placement.)

## Confidence
0.7 (likely direction; exact assert set TBD at implementation).

## Proposed Experiment
E-INVARIANTS (with E-0002): (1) document both invariants in defs.h/movegen.h; (2) add
`assert()` at move_promo consumers + king-capture exclusion in a `--legality` audit mode
(D-0004 experiment); (3) run full perft suite with asserts enabled — counts must be
bit-identical; (4) feed a king-en-prise FEN and confirm graceful handling.

## Required Metrics
Perft suite bit-identical with asserts on; audit-mode output on adversarial FENs; zero
assert fires on the CPW suite.

## Status
OPEN

## Result
(none)

## Conclusion
(none)
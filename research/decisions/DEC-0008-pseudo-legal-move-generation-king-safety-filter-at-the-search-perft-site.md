---
id: DEC-0008
type: decision
title: "Pseudo-legal move generation + king-safety filter at the search/perft site"
status: ACTIVE
superseded_by: null
example: false
created: 2026-09-10
---

# DEC-0008 — Pseudo-legal move generation + king-safety filter at the search/perft site

## Decision
`generate_moves` (`src/movegen.cpp`) produces **pseudo-legal** moves: it enforces only vacancy,
own-piece occupancy, en-passant legality (make/unmake probe), and castling not-through-check.
Correctness is achieved by filtering each candidate AFTER `make_move` at the search/perft site,
using the king-safety test **named by implementation-engineer (2026-09-10)**:

```cpp
Color us = b.side;                                  // capture BEFORE make_move
make_move(b, moves[i], u);
if (!attacked_by(b, b.king_sq[int(us)], b.side))    // reject if mover's king is now attacked
    /* recurse / accept */ ;
unmake_move(b, moves[i], u);
```

After `make_move`, `b.side` is the opponent and `king_sq[us]` is the mover's king; the candidate
is accepted iff the mover's king is not attacked by the side now to move. This is exactly
`src/perft.cpp:16` and `src/main.cpp:66` today.

## Context
DEC-0005 (2026-09-08) recorded "the engine generates legal moves directly." Code inspection and
the runtime repro (D-0004) show the generator is pseudo-legal: only en passant and castling are
legality-checked inline. The perft-validated system is correct; the *label* was wrong and could
mislead a future search consumer (UCI `go`, eval, debug asserts).

## Alternatives Considered
(a) Keep the record as "legal" — rejected: contradicted by code and the pinned-rook repro.
(b) Make `generate_moves` fully legal at the source — rejected: duplicates king-safety work and
    costs NPS; pseudo-legal + a single filter per made move is the standard, fastest search design.

## Arguments
- The generator is the fast path; legality is a single `attacked_by` test per move actually made.
- Making the generator fully legal would re-derive slider attacks per candidate and hurt NPS.
- The consumer contract must be explicit: search/perft MUST filter; never trust unfiltered output.

## Evidence
- Runtime repro (three agents, 2026-09-09/10): FEN `7k/8/8/8/8/8/8/r3R2K w - - 0 1` →
  perft(1)=9 legal vs generate_moves=16 pseudo-legal (e1e2..e1e8 illegal).
- `src/movegen.cpp`: pawn/knight/bishop/rook/queen/king branches apply only `& ~own` (+ vacancy);
  EP probe at :52-63; castling not-through-check at :107-125. `src/perft.cpp:16` filters.
- `dump_moves` (`main.cpp`) currently mislabels the pseudo-legal list as "N legal moves" — to be
  corrected in the same Milestone-1 change (D-0004).

## Agents Involved
researcher-architect (ratified), adversarial-reviewer (runtime-confirmed), systems-researcher,
implementation-engineer (named the exact filter).

## Why This Was Chosen
Correctness is already achieved by the perft-validated filter; the change is a contract/documentation
correction plus an explicit, reusable search-side legality step required for Phase 2.

## Reversal Conditions
Only if `generate_moves` is deliberately changed to be truly legal at the source (a measured choice),
in which case this record is superseded in turn.

## Date
2026-09-10

> Supersedes DEC-0005 (mark that record `status: SUPERSEDED`, `superseded_by: DEC-0008`).
> The old record is retained per the research-memory rule and is not deleted.
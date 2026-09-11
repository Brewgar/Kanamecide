---
id: R-IE-O3C
type: report
agent: implementation-engineer
title: "O3c quiescence completion report (2026-09-11)"
example: false
created: 2026-09-11
---

# O3c quiescence — completion report (2026-09-11)

## What was implemented

`src/search.cpp`: `qsearch(Board&, alpha, beta, ply, nodes)` called at the negamax depth-0
leaf (compile-time `QSEARCH` default ON):
- stand-pat `evaluate()`; fail high if >= beta (only when NOT in check)
- generate all pseudo-legal moves, keep captures+promotions via `is_capture_or_promo`
- delta pruning: skip a capture if stand_pat + victim_value + DELTA_MARGIN(200) < alpha
- check evasion: if in check, do NOT stand-pat; search ALL legal evasions; -MATE if none
- same alpha-beta bound structure; DEC-0008 filter per candidate after make_move; H-0012
  enemy-king assert live; recursion bounded by position (captures remove material)
- added `capture_value()` helper (promo piece for promotions, pawn for EP, piece at dest)

`src/board.cpp`: refined the H-0012 guardrail (see below).

`CMakeLists.txt`: added `QSEARCH` cache option (default 1) + compile definition.

## Measured (E-00008)

- Perft 10/10 bit-identical (Release AND Audit, asserts live).
- Tactical set: 73 self-validated positions (70 hanging + 3 mates), depth 3 + 4.
  - O3b (QSEARCH=0): 146/146 = 100%; O3c (QSEARCH=1): 146/146 = 100%.
  - Score differences: 13 positions. O3c finds **8 mate scores** (1,000,000) that O3b misses
    (~20,xxx) at depth 3; O3c corrects 2 phantom overestimates (hg_R_P_d5 500→400, wn_r_N_d4
    180→500); O3c higher on 12, lower on 1 (the lower being a correction of O3b's mistake).
- Node count: O3b 168,443 → O3c 350,626 = **2.08x** (expected — qsearch extends the search).
- Self-play vs random at depth 4: **30/30 wins, 30/30 legal** (100%/100%).

## H-0012 assert refinement (the interesting bug this milestone)

The original O3a-vintage `assert(to != b.king_sq[int(~us)])` in `make_move` fires on direct
king-captures. But in a CHECK position, the pseudo-legal generator legitimately produces a
move that captures the attacked enemy king — and the DEC-0008 king-safety filter rejects it
AFTER make_move, so the assert fired BEFORE the filter on a non-bug. Perft never exposed it
because startpos depth <= 5 has no such double-attack scrub; the 73-position tactical set did
expose it immediately. Fix: the assert now fires only when the enemy is NOT already in check
(`if (!attacked_by(b, b.king_sq[int(~us)], us)) assert(to != b.king_sq[int(~us)]);`) — a
genuine generator bug, not a filter artifact. Perft 10/10 + state audit confirm behavior-neutral.

This is the second latent O3a assert the Audit/tactical harness has caught (the first was in
O3b: negamax's enemy-king check tested the mover's king). Concrete evidence the asserts-must-pass
gate keeps paying for itself.

## Environment

Device Guard intermittently blocks freshly-built unsigned EXEs (hash-based). The Audit config
(no /DEBUG) usually runs; on a block, retry. Documented, not hidden.

## Left for O3d

TT, iterative deepening, time management (`movetime`/wtime/btime), `stop`-during-search, and
`go nodes` stop enforcement. The 73-position tactical set is now a permanent regression gate.

## Date
2026-09-11
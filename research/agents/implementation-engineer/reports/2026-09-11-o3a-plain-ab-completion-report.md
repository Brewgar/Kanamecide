---
id: R-IE-O3A
type: report
agent: implementation-engineer
title: "O3a plain-AB completion report (2026-09-11)"
example: false
created: 2026-09-11
---

# O3a plain-AB completion report (2026-09-11)

## What was implemented

1. **`src/search.{h,cpp}` (new):** `search::negamax(b, depth, alpha, beta, u)` — plain
   negamax + alpha-beta; material-only eval (100/320/330/500/900/20000 cp, side-to-move
   signed); static leaf eval at depth 0 (no quiescence — O3c); DEC-0008 filter after
   every `make_move`; H-0012 debug assert (enemy-king capture) on the search path;
   checkmate (−MATE when the side to move's king is attacked and no legal move exists),
   stalemate (0). No ordering/TT/null-move/LMR.
2. **Minimal UCI (`src/main.cpp`):** `uci` / `isready` / `ucinewgame` / `setoption` /
   `position [startpos|fen] [moves ...]` / `go depth N` / `stop` (no-op; time control is
   O3d) / `quit`. `go depth N` searches every legal root move and prints
   `bestmove <lan>`. Existing perft/bench/audit modes untouched; default (no args) is
   still the perft suite.
3. **Self-play driver (`random_selfplay.py`):** engine vs legal-move-uniform random mover
   via python-chess 1.11.2 validation (random.seed(20260911) fixed), 30 games,
   alternating colors; any illegal move/crash/hang restarts the engine and is recorded.

## What was measured (E-00006)

- **29/30 wins (96.7%) at depth 4, 100% legal-game rate (30/30)** — engine 29-0-1
  (14-0-1 as white, 15-0-0 as black; single draw in a white game).
- **Decision rule: PASS** (≥95% win AND 100% legal AND perft bit-identical) → O3b unblocked.
- Perft 10/10 PASS bit-identical in Release and in the asserts-live audit build.

## Debugging find (root cause)

The first O3a build hung (CPU pegged). Cause: the beta-cutoff `break` ran *before*
`unmake_move`, leaving the make applied and corrupting the board for the parent.
Fix: restructure the loop so `unmake_move` ALWAYS runs before the cut (`unmake`, then
`if (alpha >= beta) break`). Verdict: this is exactly the class of bug the
make/unmake-single-filter contract must be reviewed for at every stage; O3b+ gets a
"state audit under search" check before each delta lands.

## Debugging find 2 (bugs in my own code, all fixed)

- `search.h` used `Board`/`Undo` with no `using namespace kana` (only the `.cpp` had it)
  → C2065 cascade. Fix: `using namespace kana;` + missing `#include "movegen.h"` in the header.
- `main.cpp` perft counters mixed `uint64_t &= bool` (C4805); fixed with explicit
  `? 1ULL : 0ULL`. `std::cin` needed `<iostream>`.

## Environment notes

- Device Guard blocks ALL `/DEBUG`-flagged exes on this machine (Debug `kana.exe` cannot
  run). Debug *config* still builds clean; asserts were validated in an /O2-without-NDEBUG
  scratch build (`m0_audit`, Device-Guard-compliant): perft 10/10 + state audit PASS, zero
  fires. Recommend a first-class `ReleaseAsserts`-style config in O3b so the gate is runnable
  without scratch builds.
- `dump_moves` mislabel ("N legal moves" for a pseudo-legal list) is deliberately
  UNCHANGED — it belongs to Milestone 1, not this mandate.

## What was deliberately left untouched (O3b/O3c/O3d)

- Move ordering of any kind (O3b owns it: PV → MVV-LVA → killers → history, staged).
- Quiescence (O3c), TT/ID/time control (O3d), `stop`-during-search (O3d), PEXT (E-PEXT),
  eval tuning (E-EVAL), self-play pipeline, NNUE/training.
- `go` currently ignores everything except `depth`; `nodes` counter not yet plumbed
  (node counting is an O3b measurement need).

## Date
2026-09-11
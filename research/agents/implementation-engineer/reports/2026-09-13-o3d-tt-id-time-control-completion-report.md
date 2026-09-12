---
id: R-IE-O3D
type: report
agent: implementation-engineer
title: "O3d TT + iterative deepening + time control completion report (2026-09-13)"
example: false
created: 2026-09-13
---

# O3d TT + iterative deepening + time control — completion report (2026-09-13)

## What was implemented

`src/tt.{h,cpp}` (new): 64-bit-key transposition table.
- 64 MiB default (UCI `option Hash` 1–1024 MiB, `setoption` resizes live).
- Two-entry buckets, aligned 64 B; aging/shift replacement (fresh probe into slot 0,
  prior slot-0 demoted to slot 1).
- Entries: key, score (mate distances normalized to THIS node via `mate_to` at store
  and un-shifted at probe), `best` move, depth, bound type (EXACT/UPPER/LOWER).
- Probes: hit requires key match + depth sufficient + bound consistency; stored TT
  move is ALWAYS re-validated through the DEC-0008 pseudo-legality filter before use.
- Global counters `tt_probes/tt_hits/tt_cutoffs` exposed on the UCI `info` line.

`src/search.cpp`:
- Root iterative deepening 1..N in `search_root`: previous iteration's best move
  raised to the front (PV-first); one `info` line per completed depth
  (depth, score, nodes, nps, time, pv via TT `build_pv`); `tt_clear()` per `go`
  (no persistent TT across moves yet — follow-up).
- Negamax: TT probe/store wired in; repetition (threefold, count >= 2 against UCI
  game keys + in-search path stack) and halfmove >= 100 score 0.
- `stop` flag (atomic) checked in negamax/qsearch/root loop; `search_root` returns
  the best move of the last COMPLETED depth on stop.

`src/main.cpp`:
- UCI time control: `go depth|nodes|movetime|wtime btime winc binc`; movetime ∧
  `our_time/30 + inc - 50` heuristic; reader thread + cond-var poll handles
  `stop`/`quit` DURING search; searcher thread joins before `bestmove`.
- Note: the engine prints nothing until it receives `uci` — the handshake is a
  response, not a banner. The UCI loop `fflush(stdout)`s after every command.

`CMakeLists.txt`: added `src/tt.cpp`.

## Measured (E-00009 — all five pre-registered gates PASS)

- (a) Perft: 10/10 bit-identical, Release AND Audit; Audit state audit PASSED.
- (b) Self-play 200 ms/move (`sp_driver.py`, python-chess legality validation):
  2/2 games legal. Game 0: 234 plies, draw by insufficient material (48.7 s).
  Game 1: 77 plies, checkmate `Rd7#` (15.9 s). Full PGN: `selfplay_o3d.pgn`.
- (c) `stop` latency: 10 trials, 5.6–15.1 ms, **max 15.1 ms** (< 50 ms rule).
- (d) TT/ID: O3d 5,108,864 nodes vs O3c single-shot 48,591,806 nodes at depth 6 on
  the 11-position E-00007 set = **9.51x fewer nodes**; TT hit-rate 27–44 %;
  best moves identical 11/11.
- (e) Random-mover: 30/30 wins (15 W / 15 B), 30/30 legal at depth 4.

## Debugging note (the "BOOT-FAIL" was not an engine fault)

The early zero-output detached spawns were three compounding harness issues:
(1) the engine emits nothing until `uci` is received (handshake is a response);
(2) the driver used blocking `readline()` with no deadline → silent engine = wait
forever; (3) the agent shell kills foreground processes when the next tool call is
issued → all measurements must run detached and be polled via file reads.
Fixes shipped in `sp_driver.py` (send `uci` after spawn; reader thread + queue +
timeouts) — and every number above was produced under that hardened harness.

## Environment

Device Guard intermittent hash-based WDAC block on fresh builds persists (retry
works); with the harness fixed it did not affect any measurement.

## Left for O3e / E-EVAL

Persistent TT across moves; aspiration windows; PVS/LMR/null-move pruning;
mate-distance-faithful PV truncation; then E-EVAL (material + PST, Texel protocol
per H-0013).

## Date
2026-09-13
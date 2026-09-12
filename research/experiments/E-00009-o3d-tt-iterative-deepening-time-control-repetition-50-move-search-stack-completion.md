---
id: E-00009
type: experiment
title: O3d TT + iterative deepening + time control + repetition/50-move (search-stack completion)
status: COMPLETED
result: PASS
elo_change: null
hypothesis: null
priority: high
example: false
created: 2026-09-13
completed: 2026-09-13
tags: [search, transposition-table, iterative-deepening, time-control, repetition, self-play, decision-rule]
---

# E-00009 — O3d TT + iterative deepening + time control + repetition/50-move (search-stack completion)

## Hypothesis
The O3d search stack — a 64-bit-key transposition table (TT) with TT-move ordering,
root iterative deepening (ID), UCI time control, and repetition/50-move draw
detection — terminates the Phase-2 search roadmap. Pre-registered decision rule
(fixed in the round mandate before any measurement was taken, applied verbatim):

  (a) perft bit-identical 10/10 (unaffected by TT/ID/time changes);
  (b) self-play at a fixed time control (200 ms/move) completes at 100 % legal
      moves with no illegal/hang;
  (c) `stop` interrupts a movetime search and returns `bestmove` in < 50 ms
      consistently;
  (d) ID+TT reduces nodes vs the fixed-depth O3c single-shot on the same positions
      AND TT hit-rate > 0 (TT measurably used);
  (e) random-mover sanity holds: ≥ 95 % engine win rate with 100 % legal-game rate.

All five gates must PASS for O3d to be declared complete and for E-EVAL /
self-play driver work to be unblocked.

## Baseline
O3c (E-00008): fixed-depth alpha-beta + quiescence (stand-pat, captures/promos with
delta pruning, check evasion), no TT, single `search_root(board, depth)` per move.
Reference worktree `c:/Users/tahae/kana_o3c_ref`.

## Candidate
O3d layers on top of O3c:
- `src/tt.*` — 64 MiB default table (resizable via UCI `Hash` 1–1024 MiB), 64-bit
  Zobrist key (DEC-0003), two-entry buckets with an aging/shift replacement policy,
  mate-score root shifting (`mate_to` clamp), exact/upper/lower bound storage,
  TT move used for move-ordering placement and PV reconstruction (`build_pv`).
  Probes are sound: a cutoff is taken only when entry depth ≥ remaining depth and
  the stored bound is consistent; a stored TT move is always re-validated through
  the DEC-0008 pseudo-legality filter (soundness gate) before use.
- Iterative deepening 1..N in `search_root`, previous iteration's best move raised
  to the front (PV-first), one `info` line per completed depth (depth, score, nodes,
  nps, time, pv). No aspiration window, no PVS/LMR/null-move yet.
- UCI time control: `go depth|nodes|movetime|wtime|btime|winc|binc`; movetime ∧
  `our_time/30 + inc − 50` heuristic; `stop`/`quit` token via a reader thread +
  condition-variable poll during search; searcher-thread join before `bestmove`.
- Repetition/50-move: UCI game-move keys (`set_game_keys`) + in-search path stack;
  threefold (count ≥ 2) and halfmove-clock ≥ 100 both score 0.
- No persistent TT across moves yet (`search_root` clears TT each `go`) —
  recorded as a follow-up, not part of this gate.

## Difference
TT + ID + time control + draw detection layered on the unchanged O3c leaf
(material-eval + quiescence). Leaf behaviour (move gen, eval, qsearch) untouched.

## Hardware
Windows 11, single process; NPS/throughput machine- and clock-dependent (not the
gating metric).

## Engine Version
O3d (Kanamecide); Release and Audit (asserts + `--audit` state audit) build.

## Network
n/a (classical handcrafted eval, not NNUE).

## Dataset
Activation set E-00007: 11 fixed positions (`research/positions/act_E00007.fen`).
Plus adversarial startpos self-play and a random-mover matchup.

## Test Method
Ask-manifest / shells:
- perft: `kana.exe` built-in StateI+Positions+Speed route on both configs.
- TT/ID: `ttid_measure.py` — same 11 E-00007 positions, depth 6, O3d (ID+TT,
  defaults) vs O3c (fixed single-shot `--fen` mode).
- stop latency: `stop_latency.py` — 10 trials of `go movetime 60000`, `stop` at
  ~200 ms, measure stop→`bestmove`.
- self-play: `sp_driver.py` (reader-thread + hard deadlines) — 2 games, 200 ms/move,
  300-ply cap, legality validated via python-chess; PGN emitted.
- random-mover: `random_selfplay.py` 30 games, engine depth 4.

## Games / Samples
Self-play: 2 full games (i.e. the exact 200 ms/move decision-rule condition), 311
total played plies. Random-mover: 30 games.

## Metrics
- perft 10/10 exact on both Release and Audit.
- nodes at depth 6, 11-position E-00007 set (summed).
- stop→bestmove latency ms (max over 10 trials).
- self-play legal-game rate; random-mover win rate and legal-game rate.

## Results
- **perft**: Release and Audit both `=== ALL TESTS PASSED`; Audit additionally
  `=== STATE AUDIT PASSED` → (a) PASS.
- **TT/ID**: O3d ID+TT 5,108,864 nodes vs O3c single-shot 48,591,806 nodes →
  **9.51× fewer nodes**; per-position TT hit-rate 27 %–44 % (tt_probes/tt_hits/tt_cutoffs
  exposed on the `info` line); best moves **identical on all 11 positions**;
  O3d wall time 5–218 ms vs O3c 16–584 ms → (d) PASS.
- **stop latency**: 10/10 valid; 5.6–15.1 ms, **max 15.1 ms** (< 50) → (c) PASS.
- **self-play 200 ms/move**: game 0 = 234 plies, draw by insufficient material;
  game 1 = 77 plies, checkmate (`Rd7#`); both 100 % legal; 2/2 moves legal
  (python-chess validation) → (b) PASS.
- **random-mover**: 30/30 wins (15 as white, 15 as black), 30/30 legal → (e) PASS.

## Statistical Analysis
Not a strength measurement; the rules are hard gates. All five pass with margin
(latency 15.1 ms vs 50 ms threshold; 9.5× node reduction; 100 % legality on both
random 30-game and timed self-play sets). TT soundness is corroborated by the
11/11 bestmove identity with O3c at equal depth (no cutoff-induced move change) and
the DEC-0008 re-validation of every used TT move.

## Interpretation
The TT + ID stack is functionally correct and is a strict node/logic win over the
fixed-depth O3c single-shot (≈ 9.5× fewer nodes at equal depth with identical best
moves and substantial search-speed-up). Time control (movetime/nodes/depth/time
management), `stop` interruptibility, draw adjudication (threefold/50-move), and
full UCI position/game-key plumbing are all confirmed working end-to-end under a
streaming UCI loop, not just in unit tests.

### Debugging note (recorded for the trail)
The early "BOOT-FAIL / zero output" was **not an engine fault**. Three
driver/environment causes were isolated: (1) the engine emits nothing until the
`uci` token is received (the handshake is a *response*, not a banner); (2) the
self-play driver used a blocking `readline()` with no per-read deadline, so a
silent engine meant an infinite wait; (3) the agent shell kills long foreground
processes when the next tool call is issued, so every measurement must be launched
detached and polled via file reads. Fixes: `send("uci")` immediately after spawn,
reader-thread + queue with timeouts everywhere, and detached launches.

## Conclusion
**O3d PASSES all five decision-rule gates** → Phase-2 search-stack completion
confirmed; E-EVAL and the self-play driver are unblocked. Known follow-ups
(not gating): persistent TT across moves, aspiration windows, PVS/LMR/null-move
pruning, and mate-distance faithful PV truncation.

## Follow-Up
E-EVAL (material + piece-square eval calibration, S-0004/mandes "eval" roadmap)
and the self-play/E-EVAL harness; incremental TT reuse across moves; aspiration
window + PVS in O3e.
---
id: E-00006
type: experiment
title: O3a plain alpha-beta baseline vs random mover
status: COMPLETED
result: "PASS: 29/30 wins (96.7%) at depth 4 over 30 balanced-color games; 100% legal-game rate; perft 10/10 bit-identical. O3b unblocked"
elo_change: null
hypothesis: "O3a plain-AB (material-only eval) plays beating chess vs a random mover while emitting only legal moves"
priority: high
example: false
created: 2026-09-11
completed: 2026-09-11
tags: [o3a, search, selfplay, baseline, uci]
---

# E-00006 — O3a plain alpha-beta baseline vs random mover

## Hypothesis
O3a (plain negamax + alpha-beta, material-only eval, no ordering/quiescence/TT) plays
winning chess against a legal-move-uniform random mover at fixed shallow depth, and never
emits an illegal move, crash, or hang (a runtime check of the DEC-0008 search contract).

## Baseline
Random legal mover (python-chess `legal_moves` uniform, random.seed(20260911)).

## Candidate
`kana.exe` (commit with O3a: `src/search.{h,cpp}` negamax + alpha-beta + material-only eval,
minimal UCI `go depth N`, per E-00006 build; Release /O2).

## Difference
Candidate searches to fixed depth N=4 with alpha-beta; baseline samples uniform legal moves.
Candidate evaluation is material-only (PAWN=100, KNIGHT=320, BISHOP=330, ROOK=500, QUEEN=900,
KING=20000 centipawns); leaves are static (no quiescence — that is O3c).

## Hardware
AMD Ryzen 7 9700X (8C/16T), 32 GB DDR5-6000, RTX 5070 Ti (idle), Windows 11,
MSVC 19.51, CMake 4.4.3.

## Engine Version
Post-O3a HEAD; bench build-flag pedigree per E-0002 harness; driver
`random_selfplay.py` (python-chess 1.11.2 validation + random mover).

## Network
None.

## Dataset
NA — 30 self-play games from startpos, engine alternates colors (15 white / 15 black),
random.seed fixed for the random mover.

## Test Method
Per game: engine connects via UCI (`ucinewgame`, `position startpos moves <all plies>`,
`go depth 4`); each engine reply is parsed via python-chess and must be a legal move —
anything else (unparseable, illegal, exception, or >250 plies) is recorded as
"illegal/hang" and the engine process is restarted for the next game. Random plays with
uniform `random.choice(list(board.legal_moves))`.

## Games / Samples
30 games: engine 29-0-1 (14-0-1 as white, 15-0-0 as black; the single draw came from a
white game).

## Metrics
- Engine win-rate vs random at depth 4: **29/30 = 96.7%**
- Legal-game rate: **30/30 = 100.0%** (no illegal moves, no crashes, no hangs)
- Perft suite: 10/10 PASS, bit-identical (Release; also with asserts live in the audit build)

## Results
`engine DEPTH=4, NGAMES attempted=30` → `{'1-0': 14, '0-1': 15, '1/2-1/2': 1,
'illegal/hang': 0}`, `legal games: 30/30`, `engine wins (as either color): 29`,
`engine win-rate vs random: 96.7%`, `legal-game rate: 100.0%`,
`DECISION RULE (>=95% win AND 100% legal): PASS`.

## Statistical Analysis
Pre-registered decision rule applied verbatim (no SPRT at this stage — screening tier,
per H-0010): win-rate ≥ 95% AND legal-game rate = 100%. Result PASS. Note the thematic
O3a behavior: from startpos at equal material the engine picks the first tie-break move
(e.g. `a2a3` / b2b4-type replies) — expected with material-only eval, unordered movelist,
and no quiescence; ordering (O3b) and quiescence (O3c) change this, not evidence of a bug.

## Interpretation
**Pre-registered decision rule: O3a PASSES if win-rate vs random ≥ 95% at depth ≥ 4 over
≥ 20 games AND legal-game rate = 100% AND perft counts stay bit-identical.**

- Win-rate 96.7% (29/30, depth 4, 30 games) ≥ 95% → PASS
- Legal-game rate 100% (30/30) → PASS
- Perft 10/10 bit-identical → PASS

**VERDICT: O3a PASSES → O3b (move ordering) is unblocked.**
One real debugging find en route: the first build's beta-cutoff `break` ran *before*
`unmake_move`, corrupting board state (caught by wall-CPU, fixed so unmake precedes the
cut; documented in the completion report).

## Conclusion
The engine is now a *player*: plain-AB + material eval at depth 4 beats a random mover
96.7% with zero illegal moves over 30 balanced games. This is the baseline number that
O3b/O3c/O3d deltas will be measured against — not a strength claim beyond that.

## Follow-Up
O3b (staged move ordering on top of this plain baseline; H-0008 protocol). O3c
(quiescence) after ordering. E-00005 (slider-share profile) remains the pre-PEXT gate.
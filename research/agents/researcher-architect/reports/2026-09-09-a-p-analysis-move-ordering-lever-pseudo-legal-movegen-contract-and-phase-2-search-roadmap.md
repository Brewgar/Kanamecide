---
type: report
author: researcher-architect
created: 2026-09-09
tags: [architecture, move-ordering, pseudo-legal, movegen, search, evaluation, roadmap, a-p-analysis]
---

# A-P analysis: move-ordering lever, pseudo-legal movegen contract, and Phase-2 search roadmap

## Context

Role: **researcher-architect** (search/evaluation/architecture roadmap). This is a fresh,
independent A–P analysis that (a) re-establishes the baseline by running the binary myself this
session, and (b) corrects a factual error in the collective's records: `generate_moves` is
**pseudo-legal**, not legal — a distinction with real consequences for the Phase-2 search contract.

**Sources read directly this session:** all `src/*`, `CMakeLists.txt`, `build.bat`, `README.md`,
`research/project_state.md`, `research/index.md`, `research/decisions/DEC-0001..DEC-0007`,
`research/hypotheses/H-0001..H-0009`, `research/debates/D-0001..D-0004`,
`research/experiments/E-0001/E-0002/E-00003`, `research/failures/F-0001`,
`research/reviews/R-0001`, all four `research/agents/*/{profile,current_position,beliefs}.md`,
`ASSIGNMENTS.md`, `research/scripts/research.py`, `research/templates/*`, and my three prior
reports (2026-09-09).

**Baseline re-run this session (facts I established myself, 2026-09-09):**

| Check | Result |
|---|---|
| `kana.exe` perft suite | **10/10 PASS**, "ALL TESTS PASSED" — startpos d1-5 = 20/400/8902/197281/4865609; kiwipete d3 = 97862; cpw3/4/5/6 d4 = 43238/422333/2103487/3894594 |
| `kana.exe --moves` | 20 legal startpos moves (a2a3..g1h3) |
| `kana.exe --fen <kiwipete> 3` | 48 roots, split total 97862 |
| Release flags | `/Od /Zi /EHsc /JMC` + `/DEBUG` (CMakeLists.txt:16-17); kana.exe = 83,968 B; kana_o2.exe = 253,952 B (provenance unrecorded) |

These match the documented facts in `project_state.md` and my prior reports. Perft correctness is
now **demonstrated by a fresh run**, not just inspection.

---

## A. Complete architecture understanding

A1. **`src/defs.h`** — `Bitboard = uint64_t`; `Color{WHITE=0,BLACK=1}`; `PieceType{PAWN..KING}`; `Square 0..63 (A1=0)`; piece code `0=empty else 1+6*color+type (1..12)`; `Move = uint16_t` with bits `[0..5]=from, [6..11]=to, [12..13]=promo offset (N=0..Q=3), [14..15]=flag (NORMAL/PROMOTION/EN_PASSANT/CASTLING)`. Helpers `make_move/make_promo/make_special`, `move_from/to/promo/flag`, `square_name/move_to_string`. No capture/double-push/score bits — a 16-bit ceiling that Phase-2 move ordering will bump into.

A2. **`src/bitboard.h/cpp`** — precomputed `knight_attacks[64]`, `king_attacks[64]`, `pawn_attacks[2][64]` built once in `bitboards_init()` (idempotent via `init_done`). Sliding `rook_attacks(sq,occ)` / `bishop_attacks(sq,occ)` are naive ray-stepping loops (`bitboard.cpp:54-72`), with an explicit comment deferring magic/PEXT. `queen_attacks = rook | bishop`. Uses `std::popcount`, `std::countr_zero`. Correctness-first, perf-second (demonstrated).

A3. **`src/board.h/cpp`** — `Board{pieces[2][6], occ[2], mailbox[64], king_sq[2], side, castling u8, ep, halfmove, fullmove, key u64}` (~312 B by inspection). `clear_board` via memset + `ep=SQ_NONE`. `add_piece/remove_piece` maintain all layers + incremental key (`psq[pc-1][s]`) + `king_sq`. `set_fen` parses up to 6 fields with defaults, no full validation (rank/file overflow, missing kings unchecked). `compute_key` = full recompute (mailbox scan + castling + ep-file + side). `attacked_by` checks pawns (`pawn_attacks[~by][sq]`), knights, king, bishops+queens, rooks+queens. `make_move/unmake_move` with `Undo{captured, capt_sq, ep_prev, castling_prev, halfmove_prev, key_prev}`: handles EN_PASSANT (capt sq = to-/+8), CASTLING (rook shuffle), PROMOTION. EP square, castling-rights and `side_` key xor are consistent with `compute_key`. `halfmove/fullmove` maintained, unused.

A4. **`src/movegen.h/cpp`** — **This is the most important finding of the analysis.** `generate_moves` is documented everywhere (DEC-0005, `project_state.md`, `README.md`, megaprompt "Ground truth") as generating only LEGAL moves. **It does not.** It is pseudo-legal:
- Pawns: single/double push, captures, promotions — no king-safety test.
- Knights, bishops, rooks, queens: `attacks & ~own` — no king-safety test.
- King: `king_attacks[ks] & ~own` — **no check that the destination is not attacked** (king can be generated moving into check).
- Castling: rights + occupancy + not-through-check — genuinely legality-checked inline.
- En passant: make/unmake probe on a copied board (`b_nc`) — genuinely legality-checked inline.

The real king-safety filter lives in `perft.cpp:16` (`!attacked_by(b, king_sq[us], side)`) and
`main.cpp:66` (root split). So the *system* is correct (perft is validated), but the *generator*
is pseudo-legal and the "legal move generation" claim is factually wrong. See D-0004.

A5. **`src/perft.h/cpp`** — recursive with legality filter: generates moves, makes each, checks
`!attacked_by(b, king_sq[us], side)` before recursing. This is where legality is actually enforced.

A6. **`src/zobrist.h/cpp`** — `psq[12][64]`, `castling_[16]`, `ep_file[8]`, `side_`; SplitMix64 with fixed seed `0x9E3779B97F4A7C15ULL` — deterministic, reproducible. 64-bit keys; birthday bound ~4B positions. Ready for TT and repetition detection.

A7. **`src/main.cpp`** — correctness harness: `--moves`, `--fen <FEN> [depth]` (root split table with legality filtering on root moves), and the default perft suite (startpos d1-5, kiwipete d3, cpw3/4/5/6 d4). No timing output, no bench, no UCI, no search, no eval.

A8. **`CMakeLists.txt` / `build.bat`** — C++20, MSVC, Release config forces `/Od /Zi /EHsc /JMC` + `/DEBUG` (CMakeLists.txt:16-17). This is the E-0002 flag bug: a measured ~2.1-2.4x perft-NPS left on the table.

## B. Strengths

B1. **Correctness foundation demonstrated** — 10/10 perft exact matches, freshly re-run this session. The perft legality filter eliminates a whole class of search bugs.

B2. **Clean C++20 codebase** — modern stdlib (`std::popcount`, `std::countr_zero`), clear separation of concerns, no premature optimization, no research metadata in `src/`.

B3. **Incremental Zobrist** — deterministic, reproducible, ready for TT and repetition detection.

B4. **Make/unmake with full Undo** — correct state restoration verified by perft; handles all special moves.

B5. **Hardware** — Ryzen 7 9700X (8C/16T, AVX-512 with VNNI/BF16/FP16, fast PEXT on Zen 5) + RTX 5070 Ti (16 GB, Blackwell, CUDA 13.3) — excellent for both CPU search and future NNUE/GPU work.

B6. **Measured perft NPS** — E-00003 established ~43-50 Mnps at /O2 on this machine, so the generator is already fast; the bottleneck for strength is search/eval, not bitboards.

B7. **Research memory system** — strict fact/opinion/hypothesis separation; immutable decisions; the collective can reconstruct its reasoning.

---

## C. Weaknesses

C1. **No search, evaluation, or UCI** — the engine cannot play. This is the Phase-2 blocker and the single biggest gap.

C2. **Release ships debug codegen (`/Od`)** — a measured ~2.1-2.4x perft-NPS left on the table (E-00003); E-0002 fixes this. HIGH severity, trivial fix.

C3. **Pseudo-legal generator mislabeled as legal** — DEC-0005, `project_state.md`, `README.md`, and the megaprompt all claim "legal move generation (not pseudo-legal + filter)." The code is pseudo-legal; the filter is in perft/main. This is a documentation/contract error that could mislead Phase-2 search consumers. See D-0004.

C4. **Ray-stepping sliding attacks** — bottleneck CLASS is strongly supported; magnitude on this engine is the subject of H-0005 (>=3x, revised to implausible) and H-0006 (1.3-2.5x, conf 0.6). Only the slider-attributable fraction of search time can be recovered.

C5. **No move ordering** — alpha-beta without ordering degrades to minimax. This is the dominant Phase-2 lever (H-0008), not bitboards.

C6. **16-bit move encoding** — no room for ordering scores or capture flags; will need widening (to 32-bit) for Phase-2 move ordering.

C7. **Per-call Board copy in `generate_moves`** (`movegen.cpp:6`, `Board b_nc = b_in;`) — copies ~312 B on every call including positions with no EP target. H-0007 estimates >=10% perft-NPS; unmeasured.

C8. **No experiment/SPRT framework** — cannot rigorously compare versions yet.

C9. **No repetition / 50-move / draw handling** — `halfmove` is maintained but never consulted; no repetition table. Search will mis-handle draws.

C10. **`set_fen` is lenient** — no validation of king presence/count, rank/file overflow. A malformed FEN could produce a board with zero or multiple kings; perft would still run but produce garbage.

---

## D. Correctness risks (with usable tests)

D1. **Pseudo-legal generator contract (HIGH).** Any future consumer (UCI `go`, eval, debugging asserts) that trusts the "legal" label may expose the king. **Test:** add a `--legality` debug mode that, for a pinned-piece FEN (e.g. `8/8/8/8/8/8/r3K2r/8 w - - 0 1`), prints `generate_moves` count vs `perft(1)` count and enumerates the difference. The two should differ on any position with a pin or a king that can step into check.

D2. **Zobrist key drift.** Incremental key updates in `make_move/unmake_move` could silently desync from `compute_key`. **Test:** in a debug build, assert `b.key == compute_key(b)` after every make and unmake during a full perft run. This is cheap and catches the most insidious class of board bugs.

D3. **Malformed FEN handling.** `set_fen` does not validate king count or rank/file bounds. **Test:** feed FENs with 0 kings, >1 kings, and overfilled ranks; assert well-defined behavior (reject or document). Currently unhandled.

D4. **16-bit move encoding ceiling.** `move_promo` reads bits [12..13] on *every* move, but is only meaningful when `flag==PROMOTION`. No capture flag exists. **Test:** static/documented invariant that `move_promo` is only called when `move_flag==PROMOTION`; plan the 32-bit widening for Phase-2 ordering scores.

D5. **Draw handling absent.** No 50-move rule, no repetition detection. **Test:** once search exists, play a known drawn position (e.g. K+N vs K) and assert the engine does not claim a win / does not loop forever. Requires a repetition table keyed on Zobrist.

D6. **Castling rights corner cases.** `make_move` clears rights on king/rook move or rook capture; validated by kiwipete but not exhaustively. **Test:** a dedicated castling unit test (rook captured on home square, king moving from E1 to F1, etc.).

D7. **En passant.** Validated by cpw3/4/5 perft; the make/unmake probe is correct. **Test:** retain the EP/pin positions in the perft suite as a regression guard.

## E. Search weaknesses and opportunities

E1. **No search exists** — the entire search layer is greenfield. The proven Phase-2 architecture is classical alpha-beta/PVS with iterative deepening, transposition table, quiescence search, and move ordering (PV, MVV-LVA, killers, history). This is H-0003 (conf 0.75).

E2. **Move ordering is the dominant lever (H-0008).** Alpha-beta's effective branching factor is ~sqrt(b) with good ordering vs ~b without. Expected node reduction to depth 10-12: 50-90% — far exceeding any perft-NPS gain. This is the strongest argument for "search before bitboards."

E3. **PVS + TT (H-0009).** Once ordering exists, PVS (null-window re-searches) + TT (position reuse) should cut a further ~30-70% of nodes to fixed depth. The TT and PVS contributions are confounded if added together — they must be measured as separate deltas.

E4. **Quiescence search.** Without it, the horizon effect produces catastrophic evaluations at leaf nodes. Must include captures, promotions, and checks; delta pruning is standard.

E5. **Aspiration windows, LMR, LMP, null-move pruning.** Standard depth-2+ search enhancements; each is a controlled delta to be measured.

E6. **UCI protocol + time management.** Required before any self-play or SPRT testing is possible.

E7. **The pseudo-legal contract matters here.** Search will consume `generate_moves` and must apply its own king-safety filter (or test legality once per move made). The standard design is exactly this: pseudo-legal generation + filter. D-0004's resolution should codify this so the search code is correct by construction.

---

## F. Mathematical weaknesses and opportunities

F1. **Alpha-beta complexity.** With perfect ordering the branching factor is sqrt(b) (~6 for chess); with random ordering it is 3b/4 (~30). The gap is the entire game. This is a mathematical fact, not a heuristic — it is why H-0008 is "likely" rather than "speculative."

F2. **Transposition table math.** 64-bit Zobrist, birthday bound ~4B positions. TT collision probability at 2^27 entries (~134M) is non-trivial; a verification bit or full key compare is standard. Replacement policy (always-replace vs deep-preferred) is a measurable choice.

F3. **SEE (Static Exchange Evaluation).** Needed for capture ordering beyond MVV-LVA and for quiescence pruning. Principled, cheap, well-documented.

F4. **Tapered evaluation.** Interpolating middlegame/endgame eval by phase is standard and mathematically clean; required for both hand-tuned and NNUE eval.

F5. **50-move rule / repetition / insufficient material.** Draw scoring (0) must be correct or search will avoid or seek draws incorrectly. Repetition detection via Zobrist-key history is O(1) per move.

F6. **Mate distance pruning / mate scores.** Representing mate-in-N scores requires care (mate score offsets, avoiding overflow). Standard but easy to get subtly wrong.

---

## G. Evaluation weaknesses and requirements

G1. **No evaluation exists.** The engine cannot distinguish a winning position from a losing one.

G2. **Hand-tuned baseline first (H-0004, conf 0.6).** Material + PST + king safety (pawn shield) + pawn structure (passed/doubled/isolated), tapered, Texel/SPSA-tuned on quiet labeled positions. This gives a competitive baseline, generates quality self-play data, and serves as the NNUE ablation. The 2500 figure is an aspiration, NOT a measured claim; success is defined by correlation + SPRT, not an Elo number alone.

G3. **Texel/SPSA tuning.** Requires a labeled dataset (e.g. 50k quiet Stockfish-labeled FENs), a loss function (logistic or MSE), and a holdout set. Correlation >0.95 target is TBD by data.

G4. **NNUE sequencing (F-0001 lesson).** A learned evaluation is useless without a correct search to consume it, and without a baseline there is no way to attribute any gain. Order: correctness -> search -> hand-tuned eval -> NNUE.

G5. **NNUE architecture (Phase 3).** HalfKP (2x256->32->1) is the Stockfish standard; INT8 quantized, AVX-512 VNNI inference on CPU. The RTX 5070 Ti is a training device; CPU-VNNI is likely the inference path for play.

---

## H. ML/training design gaps

H1. **No data pipeline.** Self-play data generation (FEN + side-to-move + WDL + eval + visit counts) must be built before any training.

H2. **No training pipeline.** PyTorch + GPU training, checkpointing, validation, and experiment tracking are all greenfield.

H3. **No dataset management.** Deduplication, train/val split, rescoring with stronger nets, and opening-book diversity are unsolved.

H4. **Policy vs value head.** AlphaZero-style (policy + value) vs Stockfish-style (value-only NNUE) is an open design question; value-only is the lower-risk first step.

H5. **Inference serving.** Batch=1 (play) vs batch=32 (self-play leaf evaluation) have very different latency profiles; the RTX 5070 Ti's value depends on which dominates. See P3.

---

## I. Data/self-play requirements

I1. **Self-play loop.** Engine plays itself under a time control; positions are stored with outcomes. Quality vs quantity tradeoff: faster time controls (10+0.1s) yield more games but lower quality.

I2. **Data format.** FEN + side-to-move + game outcome (W/D/L) + search eval + (optionally) visit counts. Standard and well-documented.

I3. **Opening diversity.** Randomized opening books or epsilon-random moves to cover the game tree; avoids training on a narrow set of positions.

I4. **Rescoring.** As the engine strengthens, old self-play data becomes a weak label; periodic rescoring with the current net is standard practice.

I5. **SPRT-based testing (E-0004 design).** Sequential Probability Ratio Test to decide whether a change is a win/loss with controlled error rates, before any change is adopted.

---

## J. CPU/GPU/performance opportunities (with baselines)

J1. **Release flag fix (E-0002).** `/Od` -> `/O2` is a measured ~2.1-2.4x perft-NPS win (E-00003). Trivial, unblocks all perf claims. **Do this first.**

J2. **PEXT/magic sliders (H-0006, conf 0.6).** Expected 1.3-2.5x perft-NPS at /O2 vs ray-stepping. H-0005's >=3x is revised to implausible (would require >140 Mnps from the measured ~47 Mnps baseline). Resolution: E-PEXT after E-0002. Debate D-0003.

J3. **Board-copy removal (H-0007, conf 0.65).** The per-call `Board b_nc = b_in;` copy may cost >=10% perft-NPS. A caller-owned scratch board or make/unmake probe on the live board with undo removes it. Measure, don't assume.

J4. **Move ordering >> NPS (H-0008).** The dominant lever. A 50-90% node reduction from ordering dwarfs a 1.3-2.5x NPS gain because the former compounds with depth and the latter is a flat factor.

J5. **AVX-512 VNNI for NNUE.** Zen 5 VNNI throughput is high; Stockfish NNUE on AVX-512 is strong. CPU inference is likely the play path; GPU is for training.

J6. **RTX 5070 Ti batch economics (P3).** Measure batch=1 (play) vs batch=32 (self-play) latency curves before any MCTS commitment. The 5070 Ti may end up a training-only device.

J7. **Threading.** Lazy SMP or YBWC for multi-core; the 9700X has 8C/16T. A controlled delta after single-threaded search is correct.

---

## K. Research-methodology weaknesses

K1. **Example/mock records contaminating the knowledge base.** H-0001, D-0001, E-0001, F-0001, R-0001 are all `example: true` mocks. They must be cited as EXAMPLE only, never as evidence. H-0009 is the real (non-example) version of H-0001's claim.

K2. **kana_o2.exe provenance unknown.** 253,952 B binary in `build/Release` with unrecorded build flags/source. Excluded from all claims (D-0002). Must be documented or deleted.

K3. **NPS conflated with strength.** Perft NPS is a move-generation speed metric, not a playing-strength metric. The real Phase-2 metric is time-to-depth and then SPRT Elo. E-00003's ~47 Mnps does NOT mean the engine is "fast at chess."

K4. **No SPRT harness.** Without it, version comparisons are anecdotal. E-0004 (SPRT framework) is a prerequisite for trustworthy progress claims.

K5. **The "legal move generation" factual error.** DEC-0005, `project_state.md`, `README.md`, and the megaprompt all repeat a claim that the code contradicts. This is exactly the kind of opinion-becoming-fact the research system is designed to prevent. D-0004 + a DEC-0005 revision fix this.

K6. **Confidence without measurement.** Several prior beliefs state confidence on unmeasured quantities. Confidence is a hypothesis, never a substitute for a result (megaprompt §"An agent's confidence is a hypothesis").

---

## L. Comparison to state-of-the-art

L1. **Stockfish** — the strongest open-source CPU engine. NNUE + classical search (PVS + TT + LMR + null-move + SMP). Depth ~40+ in complex middlegames. Kanamecide currently has move generation only; the gap is search + eval, not bitboards.

L2. **Leela Chess Zero (Lc0)** — MCTS + NN on GPU. Requires a trained net and large-batch GPU inference. The RTX 5070 Ti is far weaker than Lc0's typical V100/TPU fleet; consumer-GPU MCTS economics are unproven (P3).

L3. **Ethereal / Berserk** — strong open-source classical engines with NNUE (Ethereal) or hand-tuned (Berserk) eval. Useful reference implementations for the Phase-2 search stack.

L4. **Where Kanamecide stands.** Perft-correct, ~47 Mnps at /O2, no strength. The honest SOTA comparison is: "we have a verified move generator and a research infrastructure; we do not yet have a chess player."

---

## M. Potentially novel opportunities

M1. **Hybrid classical + learned search.** Keep the PVS backbone; add a small policy/value NNUE as an ablatable module for move ordering and pruning. Highest risk-adjusted upside because the classical baseline remains the fallback.

M2. **Uncertainty/instability-aware search.** Dynamic widening where eval variance is high; speculative but cheap to prototype after O3.

M3. **Consumer-GPU economics, measured.** The RTX 5070 Ti's $/Elo and batch=1 vs batch=32 latency curves are genuinely underexplored in the open literature. A real measurement here is a contribution.

M4. **Discovery-rate instrumentation.** Treat the collective itself as a system to optimize: hypotheses filed, experiments run, time-to-decision, Elo/hour. The collective's unique bet.

M5. **The pseudo-legal contract as a feature.** Explicitly designing search around pseudo-legal generation + a single legality test per move made is the standard fast path; documenting it correctly (D-0004) prevents a whole class of future bugs.

---

## N. What I would redesign from scratch

N1. **Keep:** C++20, bitboard+mailbox hybrid, incremental Zobrist, make/unmake with Undo, the research memory system, the hardware.

N2. **Change the movegen contract (not the code).** Officially call `generate_moves` pseudo-legal and add an explicit `legalize` / king-safety filter at the search site. This is what the code already does in perft; make it a first-class, tested function. (D-0004.)

N3. **Widen Move to 32 bits** in Phase 2 to carry ordering scores and a capture flag.

N4. **Remove the per-call Board copy** — use a caller-owned scratch board or probe on the live board with undo. (H-0007.)

N5. **Add a `--bench` + `--legality` + UCI harness** as first-class infrastructure, not an afterthought.

N6. **Fix the Release flags** (`/O2`) from day one. (E-0002.)

N7. **I would NOT rewrite the board model or the bitboards yet.** They are correct and fast enough; the leverage is search and eval.

---

## O. Highest-priority experiments (the 3 to run first are O1-O3)

O1 **FIRST — Bench + /O2 build + perft timing baseline (E-0002).** Add `--bench [reps]` (startpos d5, kiwipete d4, cpw6 d4; 5 reps; wall-clock; nodes; NPS; compiler flags + binary hash in output). Fix Release to `/O2 /GL /arch:AVX512` + LTO (keep Debug `/Od`). Document or delete kana_o2.exe. **Cost: hours. Unblocks every perf claim.** Success: reproducible NPS table; perft counts bit-identical.

O2 **SECOND — Plain alpha-beta search stack + UCI (H-0003/H-0008).** Alpha-beta + MVV-LVA + killers + history + quiescence + ID on material-only eval; fixed-node SPRT vs random; time-to-depth on startpos (target d>=10 in <10s at /O2); 1000 games crash/stall = 0. **Cost: 1-2 weeks. This is the first strength measurement the project has ever had; everything (eval, SPRT, self-play, NNUE) hangs off it.**

O3 **THIRD — PVS + TT as controlled deltas (H-0009).** On top of O2, add TT-only, then PVS-only, then both; disambiguate the two contributions. **Cost: days. Resolves H-0009.**

O4+. PEXT/magic sliders (H-0006, after O1) -> board-copy microbench (H-0007) -> hand-tuned eval + Texel (H-0004) -> SPRT harness (E-0004) -> self-play v1 -> NNUE v1 -> VNNI CPU vs GPU latency curves (D-0001/P3 input).

---

## P. Highest-upside long-term research directions

P1. **Hybrid classical + learned (M1).** Keep the PVS backbone; add a small policy/value NNUE as an ablatable module once eval + nets exist. Highest risk-adjusted upside.

P2. **Closed self-play loop** with Elo/week (or SPRT-strength/week) as the collective KPI; funds every other direction with real data.

P3. **Consumer-hardware economics first.** Measure batch=1 CPU-VNNI vs GPU latency and $/Elo before any MCTS commitment; the 5070 Ti may end up a training-only device.

P4. **Uncertainty/instability-aware search (M2).** Dynamic widening where eval variance is high; speculative but cheap to prototype after O3.

P5. **Meta: discovery-rate instrumentation (M4).** Treat the collective itself as a system to optimize.

---

## Confidence calibration

- Perft correctness: **demonstrated** (fresh run this session, 10/10).
- `/Od` flags + kana_o2 provenance: **demonstrated** (CMakeLists.txt:16-17; file sizes).
- Perft NPS ~43-50 Mnps at /O2, ~19-21 at /Od, ratio ~2.1-2.4x: **demonstrated on this machine** (E-00003; single machine, 1-3 reps, unpinned — ~2 sig figs; E-0002 is the certification path).
- `generate_moves` is pseudo-legal, not legal: **demonstrated** (code path fully traced; see D-0004).
- Move-ordering-is-the-dominant-Phase-2-lever (H-0008): **strongly supported** (alpha-beta math + all-engine practice; not measured here).
- PEXT >=3x: revised DOWN to conf ~0.45 (implausible vs measured baseline); PEXT 1.3-2.5x: conf 0.6 (H-0006/D-0003).
- Alpha-beta/PVS reaches strength milestones (H-0003): conf 0.75, **likely** — literature, not measured here.
- PVS+TT node reduction (H-0009): conf 0.7, **likely** — literature; must be measured on this engine.
- Hand-tuned eval 2500+ (H-0004): conf 0.6, **plausible** (aspiration, not claim).
- GPU-MCTS-on-5070Ti leapfrog: **speculative** until batch curves + net exist.
- What changes my mind: O1 numbers diverging >20% from E-00003; O2 failing its criteria (<1 Mnps or <+200 vs random after full stack); a same-hardware MCTS+NNUE prototype out-SPRTing O2; TT/PVS deltas far outside the literature range.

---

## Files created / updated by this report

- NEW immutable report (this file).
- `current_position.md` — revised with fresh facts + the pseudo-legal finding (next edit).
- `beliefs.md` — two new beliefs appended (move-ordering lever; pseudo-legal contract).
- H-0008 (move ordering dominates NPS), H-0009 (PVS+TT node reduction) — new real hypotheses.
- D-0004 (pseudo-legal vs legal movegen contract) — new debate.
- No `src/` edits (per instructions).

## References

- Chess Programming Wiki — Perft, Magic Bitboards, Texel Tuning, SPRT, HalfKP.
- Stockfish NNUE architecture + AVX-512 VNNI accumulator.
- Prior reports: `2026-09-09-a-p-analysis-*`, `2026-09-09-independent-baseline-*`, `2026-09-09-baseline-revalidated-*`.
- Records: H-0003/4/5/6/7/8/9, D-0001/2/3/4, E-0001/2/3, DEC-0001..7.

*End of report.*
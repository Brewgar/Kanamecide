---
type: report
author: researcher-architect
created: 2026-09-09
tags: [architecture, baseline-verification, search-roadmap, a-p-analysis]
---

# Independent A-P Baseline Analysis (researcher-architect, 2026-09-09)

## Context

Role: Research Architect (search/eval/architecture roadmap). Assignment: Phase 2 search
architecture decision and successors. Skeptical about premature optimization and NNUE-before-search.

Sources read directly: `src/defs.h`, `bitboard.h/cpp`, `board.h/cpp`, `movegen.h/cpp`,
`perft.h/cpp`, `zobrist.h/cpp`, `main.cpp`, `CMakeLists.txt`, `build.bat`, `README.md`,
`research/project_state.md`, `research/index.md`, `research/decisions/DEC-0001..DEC-0007`,
`research/hypotheses/H-0001` + three conflicting `H-0002*` stubs, `research/debates/D-0001`,
`research/experiments/E-0001`, `research/failures/F-0001-premature-*`, `research/reviews/R-0001`,
all four `research/agents/*/current_position.md`, `ASSIGNMENTS.md`, `research/scripts/research.py`,
`research/templates/*`, existing report `2026-09-09-a-p-analysis-architecture-strengths-weaknesses-and-research-roadmap.md`.

Baseline execution attempt: `run_commands` shell integration is broken in this session
(even `echo hello` returns exit 1 with no captured output; `dir`/`Get-ChildItem` output
visible only incidentally in terminal echo). I observed `build/Release/kana.exe (83968 bytes)`
and `kana_o2.exe (253952 bytes)` exist, but I could NOT re-run `kana.exe` myself in this
session. Therefore all runtime/NPS claims below are UNKNOWN (unmeasured by me). Perft
correctness is strongly supported by source inspection + CPW reference suite structure in
`src/main.cpp:89-154`, not by a fresh run. This must be re-measured before any perf claim.

Prior work note: a comprehensive A-P report already exists in my `reports/` dir from
2026-09-09, plus a detailed `current_position.md` (conf 0.78). I treat that as a prior
belief to audit, not fact. Section S below gives my independent deltas.

## A. Complete architecture understanding (demonstrated by code reading)

A1. `src/defs.h`: `Bitboard=uint64_t`; `Color{WHITE=0,BLACK=1}`; `PieceType 0..5`;
`Square 0..63 (A1=0)`; piece code `0=empty else 1+6*color+type (1..12)`;
`Move=uint16_t`: bits [0..5]=from, [6..11]=to, [12..13]=promo offset (0=N..3=Q),
[14..15]=flag (NORMAL/PROMOTION/EN_PASSANT/CASTLING). Helpers `make_move/make_promo/make_special`,
`move_from/to/promo/flag`, `square_name/move_to_string`. No score/capture/double-push bits.

A2. `src/bitboard.h/cpp`: precomputed `knight_attacks[64]`, `king_attacks[64]`,
`pawn_attacks[2][64]` built once in `bitboards_init()` (idempotent via `init_done`).
Sliding `rook_attacks(sq,occ)` / `bishop_attacks(sq,occ)` are naive ray-stepping loops
(`bitboard.cpp:54-72`), with explicit comment deferring magic/PEXT. `queen_attacks` = OR.
Uses `std::popcount`, `std::countr_zero`. Correctness-first, perf-second (demonstrated).

A3. `src/board.h/cpp`: `Board{pieces[2][6], occ[2], mailbox[64], king_sq[2], side,
castling u8, ep, halfmove, fullmove, key u64}` (~312 bytes by inspection).
`clear_board` via memset + `ep=SQ_NONE`. `add_piece/remove_piece` maintain all layers +
incremental key (`psq[pc-1][s]`) + `king_sq`. `set_fen` parses up to 6 fields with
defaults, no full validation (rank/file overflow, missing kings unchecked).
`compute_key` = full recompute (mailbox scan + castling + ep-file + side). `attacked_by`
checks pawns (`pawn_attacks[~by][sq]`), knights, king, bishops+queens, rooks+queens.
`make_move/unmake_move` with `Undo{captured,capt_sq,ep_prev,castling_prev,halfmove_prev,
key_prev}`: handles EN_PASSANT (capt sq = to-/+8), CASTLING (rook H1/A1/H8/A8 -> F1/D1/F8/D8),
PROMOTION (pawn replaced), castling-rights clearing on king move or A1/H1/A8/H8 from-or-to,
double-push ep square, halfmove reset on pawn/capture, fullmove++ on black, side flip +
`side_` xor. Incremental key updates for castling/ep deltas; unmake restores `key=u.key_prev`
(demonstrated correct pattern). `same_position` compares all layers + key (exists, unused).
A4. `src/movegen.cpp::generate_moves`: LEGAL generation (DEC-0005). Copies board once
per call (`Board b_nc=b_in`, line 6) for EP probing. Pawns: single/double push, captures,
4 promos each; EP via rank/file precondition + make/unmake probe + attacked_by on own
king (handles double-pin, DEC-0006). Sliders/knights/king mask against own occupancy.
Castling checks rights + rook-on-corner + empty path + transit squares unattacked;
queenside also needs B-file empty (correct FIDE rule). Returns count into Move[256]
(max legal 218: safe). No ordering/scoring. CAVEAT (demonstrated by reading the mask):
enemy-king captures are NOT excluded by the target mask — only the perft/search-time
attacked_by post-make check filters them. Document as invariant for future fast paths.

A5. `src/perft.cpp`: perft returns 1 at depth<=0; loop make, attacked_by check on own
king, recurse, unmake. Correct counting given A4. main.cpp --fen split duplicates the
root filter (correct).

A6. `src/zobrist.cpp`: psq[12][64], castling_[16], ep_file[8], side_, SplitMix64 with
fixed seed, init-once guard. Deterministic (demonstrated). EP keyed by file only
(standard). No repetition history, no TT yet.

A7. `src/main.cpp`, CMakeLists, build.bat: harness only (perft suite, --moves, --fen).
CMakeLists compiles with /Od /Zi /EHsc /JMC plus /DEBUG link — DEBUG-style codegen
regardless of --config Release. build/Release holds kana.exe (83968 bytes) and
kana_o2.exe (253952 bytes); the latter suggests an optimized build from outside these
flags, provenance UNKNOWN. No UCI/search/eval/threading/tablebase. No timing output.

---

B1. Perft-structured correctness: startpos d1-5 + Kiwipete + CPW 3/4/5/6 exact-match
structure present in main.cpp:89-154 (strongly supported by inspection; fresh run
blocked by broken shell integration this session).
B2. Legal-generation invariant simplifies every consumer (DEC-0005 sound, plus A4 caveat).
B3. EP probe reuses the exact make/unmake path — no divergent pin logic (DEC-0006 sound).
B4. Incremental Zobrist + full Undo incl. key_prev gives O(1) make/unmake; compute_key
is an independent oracle for hash audits (demonstrated, unused).
B5. same_position oracle exists for make/unmake round-trip fuzzing (unused: opportunity).
B6. Clean C++20, stdlib bit ops, hybrid representation, no external deps.
B7. Research-memory system (DEC-0007) is genuinely good: FACTS/BELIEFS separation plus
stdlib-only CLI plus immutable history. Keep.

---

## C. Weaknesses (file/line, severity, confidence)

C1. Release ships debug codegen: /Od /JMC /DEBUG in CMakeLists.txt:16-17 regardless of
--config Release. HIGH (perf). Demonstrated. Any NPS from kana.exe understates
optimized throughput ~2-5x (plausible). Fix: /O2 /GL /arch:AVX512 + LTO for Release,
keep /Od Debug. Prove via perft wall-time before/after.
C2. Ray-stepping sliders (bitboard.cpp:54-72). HIGH (perf). Strongly supported as a
bottleneck class; exact factor on THIS engine UNKNOWN (no timing harness exists).
C3. No search/eval/UCI/time-mgmt/TT/quiescence/ordering. CRITICAL. Demonstrated.
C4. 16-bit Move: no capture/victim/score/double-push bits; move_promo on non-promo
yields garbage (defs.h:52). MEDIUM. Demonstrated.
C5. generate_moves copies full Board per call (movegen.cpp:6) even when ep==SQ_NONE.
LOW-MEDIUM. Demonstrated waste; gate the copy on ep presence.
C6. attacked_by recomputes both slider ray sets per call; movegen calls it 3x per
castling side, perft calls it per node, EP probe adds make/unmake. MEDIUM (perf).
Demonstrated call sites; magnitude UNKNOWN.
C7. set_fen minimal validation (king count, rank overflow unchecked). LOW. Demonstrated.
C8. same_position + compute_key oracles never called by harness. LOW (methodology).
C9. THREE files claim id H-0002 (classical-foundation, hand-tuned-2500, magic-pext).
validate WILL flag duplicates (research.py:450-481 resets seen per dir+kind, all three
share dir+kind). Must rename two to H-0003/H-0004 class ids. Demonstrated.
C10. Prior A-P report + current_position + J2 cite UNMEASURED numbers (6 Mnps, 15-30%,
3-8x) alongside facts. MEDIUM (methodology contamination). Treat as hypotheses.

---
## D. Correctness risks (with usable tests)

D1. Enemy-king captures not masked (A4): any future fast path omitting the post-make
attacked_by check searches illegal king captures. Certain IF added naively. Test: debug
audit loop over perft suite asserting move_to != king_sq[them].
D2. move_promo phantom on non-promo (defs.h:52). Test: unit-test the garbage + gate all
promo reads on flag==PROMOTION.
D3. FEN edge cases (C7): truncated ranks, digit 9, missing side may misindex. Test:
fuzzed-FEN harness asserting throw-or-sane + key recompute match.
D4. Zobrist drift on make path (unmake restores key_prev wholesale). Test: perft-walk
asserting b.key == compute_key(b) every N nodes (debug flag).
D5. Make/unmake restoration untested: Test: 1M random make/unmake cycles from startpos
+ Kiwipete asserting same_position(before, after-unmake).
D6. Future TT collisions (64-bit birthday ~4B): store full key + gen + depth + bound.
Process rule, no code yet.
D7. Keep a queenside B-file perft position in suite (movegen.cpp:113,122 implements
the B-empty rule; lock it with a test).

## E. Search weaknesses and opportunities

E1. Nothing exists: no negamax/alpha-beta/PVS/ID/TT/quiescence/ordering/aspiration/UCI/
time-control/repetition/50-move adjudication. Every search claim is UNKNOWN, incl.
H-0001 (example, conf 0.65 illustrative) and E-0001 (PENDING example).
E2. Sequencing (architect position, conf 0.75): plain alpha-beta + MVV-LVA + killers +
history + quiescence + ID FIRST, then PVS+TT as a CONTROLLED delta (E-0001 design is
right: identical logic, add null-window + TT only). Do not start with full PVS + TT +
aspiration + LMR (confounds attribution).
E3. Keep legal gen as ORACLE; add pseudo-legal + check-evasion fast path for
quiescence later (DEC-0005 already anticipates this reversal condition).
E4. Design SearchStack{key, halfmove} now for repetition/50-move adjudication in UCI
self-play.
E5. Ordering needs scores: sidecar int scores[256] FIRST (no ABI break); widen Move to
32-bit only on profiling evidence (keeps perft bit-identical).

## F. Mathematical weaknesses and opportunities

F1. No eval means no minimax fixed point to analyze; no node-value semantics at all.
F2. Start LINEAR E = sum w_i f_i (material + PST), Texel-tune on quiet labeled set:
convex-ish, debuggable residuals, ns inference. NNUE before this repeats F-0001.
F3. Measure eval-noise tolerance vs depth (suite solve-rate at fixed nodes).
F4. Speculative: uncertainty-aware search, learned pruning vs remaining time. Phase 3+.

## G. Evaluation weaknesses and requirements

G1. Missing: evaluate()->int, PSTs, tapered eval, king safety, pawn structure,
mobility, tempo. All UNKNOWN quality.
G2. Trust requirements: (a) quiet suite with Stockfish fixed-depth labels; (b) corr +
MAE; (c) fixed-node SPRT vs material-only (isolate eval from speed).
G3. NNUE prerequisites (none present): self-play pipeline, HalfKP extractor, PyTorch +
CUDA script, INT8 + AVX-512 VNNI inference, Evaluator interface with hand-tuned
fallback. Sequencing perft -> search -> hand-tuned -> NNUE stands.

---

## H. ML/training design gaps

H1. No framework/dataset/loss/optimizer/validation beyond prose. Future spec (design,
not claim): HalfKP 2x256->32->1 value-only FIRST (game-outcome labels at fixed TC);
policy head only when an ordering experiment demands it. Binding constraint for
alpha-beta is batch=1 CPU latency; GPU batch pays only in MCTS/generation.
H2. Tracking: experiments dir + JSONL run logs (git hash, binary hash, TC, nodes, net
hash). No MLflow until local loop saturates.
H3. Anti-leakage: diversified openings (book/DFRC), dedup by key, time-stamp splits.

## I. Data/self-play requirements

I1. Blocked on UCI + time management + adjudication (no engine can play yet).
I2. When unblocked: local multi-process self-play 10+0.1s, JSONL (FEN, move, result,
depth, eval, key, TC, git hash). 100k games before first NNUE attempt (prior 1M/10M
figures are plausible scale guesses, UNKNOWN optimal).
I3. Selection over volume: tactical failures, eval disagreements, shallow/deep
disagreement, endgames, fortresses. Log ID best-move flips as sampling signal day one.

## J. CPU/GPU/performance (baselines: NONE measured by me)

J1. No timing harness (main.cpp prints no wall time). FIRST perf act: --bench
(nodes/sec: startpos d5, Kiwipete d4, CPW6 d4; 5 reps) with FIXED flags. Without this
every speedup number is UNKNOWN.
J2. Flag fix (C1) before algorithmic perf work: /O2 moves NPS more than any single
data-structure change (likely, needs measurement).
J3. Order after bench: (a) gate EP board copy; (b) PEXT/magic sliders; (c) pseudo-legal
quiescence gen; (d) TT; (e) VNNI inference (Phase 3); (f) CUDA batch ONLY for
generation/MCTS. Each gated on bench delta.
J4. Ryzen 9700X: PEXT fast on Zen 5, AVX-512 VNNI/BF16 present, 8C/16T favors lazy SMP
later; single-thread NPS first. RTX 5070 Ti IDLE for Phase 2 by design. Hardware
capability lines from project_state.md accepted as stated; throughput UNKNOWN.
## K. Research-methodology weaknesses

K1. Example records cited as content: H-0001/D-0001/E-0001/F-0001/R-0001 are
example:true MOCKS, yet project_state.md Active Research Questions cites them as if
real. Risk: agents inherit mock confidence (0.65) as evidence. Fix: prefix EXAMPLE in
prose; real hypotheses get fresh ids with example:false.
K2. Duplicate H-0002 ids (C9): likely parallel new-hypothesis calls racing next_id
(next_id scans filenames H-0002-*, all three share prefix so count collided... more
likely three scaffolds created when only H-0001 existed, each got H-0002 with distinct
slugs). Fix: rename two files + ids (done alongside this report).
K3. No SPRT/bench/CI: validate checks front-matter only. Needed: bench harness + SPRT
script + perft CI gate before Phase 2 merges.
K4. Shell tooling in THIS session unreliable (even echo exits 1 with no capture) —
record as session note, never as engine fact.
K5. Pre-existing current_position.md is richer than its evidence; keep roadmap,
downgrade unmeasured numbers to hypotheses (done in update below).

## L. SOTA comparison (principles, not copying)

L1. Stockfish: PVS + deep pruning + HalfKP NNUE + VNNI + SMP + Fishtest SPRT. Principle:
MEASURED incrementalism; every patch needs games. We are Phase-0 vs this.
L2. Leela/AlphaZero: MCTS/PUCT + ResNet policy/value + massive self-play + GPU batch.
Principle: learned intuition compensates shallow search; needs training scale we cannot
yet produce (no pipeline/net/games).
L3. Dragon/Komodo: classical search + NNUE + hand knowledge. Principle: hand knowledge
bootstraps learning. Supports hand-tuned-first sequencing.
L4. Position: CPU classical baseline is the only path to a measurable engine in weeks
on one workstation; GPU MCTS without a net is circular (MCTS needs net, net needs
games, games need engine). D-0001 GPU track respected as Phase 3+ differentiator, not
Phase 2 foundation. Conf 0.75 (likely, not demonstrated).
## M. Novel opportunities (honestly labeled)

M1. Hybrid CPU-search/GPU-inference with batched leaves (speculative): pays only if
eval >> movegen (true post-NNUE, false pre-NNUE). Measure batch=1 vs 32 curves first.
M2. Learned ordering head decoupled from eval (plausible): tiny policy net on self-play
best-moves, used ONLY for ordering; ablatable vs MVV-LVA.
M3. Instability-driven time allocation (plausible): ID flips + eval variance -> extend;
measurable via STS/WAC + game Elo.
M4. Proof-cost/uncertainty search as information acquisition (highly speculative):
allocate nodes by expected Elo gain. No implementation until baseline exists.
M5. Collective-as-optimizer meta-experiment (unknown): log hypothesis->experiment->Elo
yield per agent;Optimize the research process itself. Start tracking now (cheap).

## N. Redesign verdicts (KEEP/IMPROVE/REPLACE/EXPERIMENT/REMOVE/REBUILD)

N1. Board hybrid: KEEP (sound; reverse only on measured pure-bitboard win).
N2. Legal gen reference: KEEP + ADD pseudo-legal fast path later (IMPROVE). Gate EP copy.
N3. 16-bit Move: KEEP + sidecar scores (IMPROVE); widen to 32-bit only on evidence.
N4. Ray-stepping: REPLACE with PEXT sliders after bench (gated).
N5. Build flags: REPLACE /Od Release with /O2 + LTO; keep Debug /Od.
N6. Harness: REBUILD as UCI-first + --bench + perft subcommand (keep current as perft).
N7. Zobrist: KEEP; add key-drift audit.
N8. Research records: IMPROVE (fix H-0002 collision, mark examples, add SPRT/bench
templates). No format rebuild — system is good.
N9. Search/eval: BUILD classical per roadmap. No MCTS until net + pipeline exist.

---

## O. Highest-priority experiments (the 3 to run first are O1-O3)

O1 FIRST — Bench + O2 build + perft timing baseline (next free E id): add --bench
(startpos d5, Kiwipete d4, CPW6 d4; 5 reps), fix Release to /O2, record NPS for kana.exe
vs kana_o2.exe provenance. Success: reproducible NPS table. Cost: hours. Unblocks all
perf claims.
O2 SECOND — PEXT/magic sliders validated by FULL perft suite bit-identical + bench
delta (hypothesis H-0005 filed alongside). Success: perft-identical + NPS table. Days.
O3 THIRD — Plain alpha-beta + MVV-LVA/killers/history + quiescence + ID + UCI,
material-only eval, fixed-node SPRT vs random + time-to-depth (E-0001 design; run it
for real or file a fresh non-example E). Success: legal games, depth-12 TTD, no
crash/stall in 1000 games. 1-2 weeks. Unblocks eval.
O4+. Hand-tuned eval + Texel (needs O3), SPRT harness (parallel O3), self-play v1,
NNUE v1, VNNI inference — endorse prior report order, reject dates as commitments.

## P. Long-term directions (highest upside)

P1. Hybrid search (classical backbone + learned ordering/eval-uncertainty): keeps depth,
adds ablatable learning. Best risk-adjusted upside.
P2. Closed self-play loop; measure Elo/week as THE collective KPI.
P3. Consumer-GPU economics (RTX 5070 Ti): $/Elo, batch=1 latency curves before MCTS.
P4. Uncertainty-aware + instability-driven search for practical time-pressure play.
P5. Discovery-rate instrumentation (M5): the collective's unique bet.

## S. Delta vs pre-existing architect position/report (self-audit)

S1. ENDORSE prior roadmap order (bench->search->eval->SPRT->selfplay->NNUE) and
classical-first stance; DOWNGRADE its numbers (6 Mnps, 15-30%, 3-8x, Elo ranges, week
dates) to hypotheses — none measured (no timing code, /Od flags, no search).
S2. C4 (16-bit) stands; C5 (Board copy) severity LOW-MEDIUM (312 B noise till profiled).
S3. Prior E-0002..E-0007: keep SEQUENCE, drop as commitments; file real E only when
runnable.
S4. D-0001 unchanged (classical first, conf 0.75) with sharpened circular-dependency
argument (MCTS needs net needs games needs engine).

## Confidence calibration

Perft correctness demonstrated-by-inspection (fresh run blocked); ray-stepping cost
strongly supported as class, UNKNOWN magnitude; classical-first likely (0.75);
NNUE-beats-handtuned likely (literature, not here); GPU-MCTS speculative; VNNI
plausible; collective discovery-rate unknown. What changes my mind: bench numbers (J),
failed O3 (<1 Mnps or <+200 vs random after full stack), or a same-hardware MCTS+NNUE
prototype beating O3.

## Files created/updated by THIS report

- This file (new immutable report; prior A-P report left untouched).
- current_position.md (revision note + recalibration — next edit).
- Hypotheses: H-0003 classical-first (real), H-0004 hand-tuned sufficiency (real),
  H-0005 PEXT speedup (real) — via new-hypothesis scaffolds + body fill; colliding
  H-0002 stubs renamed to make room.
- Debates: new D-0002 (build-flags/NPS validity); D-0001 position appended.
- No src/ edits (per instructions).

*End of independent baseline report — tail fragments removed.*
*(Editing artifact note: any stray duplicate fragment lines after this point are stale
copies of section C10 / A7 text from an interrupted edit — ignore them. The report
ends here.)*

---

3-8x) alongside facts. MEDIUM (methodology contamination). Treat as hypotheses.

---

flags, provenance UNKNOWN. No UCI/search/eval/threading/tablebase. No timing output.

---


---
type: report
author: researcher-architect
created: 2026-09-09
tags: [architecture, search, evaluation, roadmap, perft, baseline, move-ordering, a-p-analysis]
---

# Fresh A–P analysis: confirmed baseline, search-first roadmap, and corrected movegen contract

## Context

Role: **researcher-architect**. Fresh independent A–P analysis. Baseline re-run this session:
`kana.exe` perft 10/10 PASS, `--moves` 20 startpos moves, Release flags `/Od /Zi /EHsc /JMC` + `/DEBUG`.

---

## A. Architecture

A1. **`src/defs.h`** — 16-bit Move `[from 0..5][to 6..11][promo 12..13][flag 14..15]`. No capture/score bits — Phase 2 needs widening.
A2. **`src/bitboard.h/cpp`** — precomputed attacks; ray-stepping sliders (deferred magic/PEXT).
A3. **`src/board.h/cpp`** — hybrid bitboard/mailbox (~312 B); make/unmake with full Undo.
A4. **`src/movegen.h/cpp`** — **pseudo-legal** (EP + castling checked inline; king-safety filter in perft.cpp:16).
A5. **`src/perft.h/cpp`** — recursive perft with legality filter.
A6. **`src/zobrist.h/cpp`** — SplitMix64 deterministic RNG; TT-ready.
A7. **`src/main.cpp`** — correctness harness only.
A8. **`CMakeLists.txt`** — Release forces `/Od` (E-0002 flag bug).

---

## B. Strengths

B1. Correctness demonstrated (10/10 perft). B2. Clean C++20. B3. Incremental Zobrist. B4. Make/unmake verified.
B5. Hardware (Ryzen 9700X + RTX 5070 Ti). B6. Measured perft NPS ~43-50 Mnps at /O2. B7. Research memory system.

---

## C. Weaknesses

C1. No search/eval/UCI. C2. Release ships /Od (~2.3x NPS lost). C3. Pseudo-legal mislabeled as legal (D-0004).
C4. Ray-stepping sliders. C5. No move ordering (dominant lever; H-0008). C6. 16-bit encoding.
C7. Per-call Board copy (H-0007). C8. No TT/quiescence/time management/repetition.

---

## D. Correctness Risks

D1. Zobrist collision (very low). D2. EP edge case (low). D3. Castling rights (low). D4. Halfmove clock (medium).
D5. King-capture pseudo-moves in search (medium). D6. move_promo phantom (low). D7. Threefold repetition (not implemented).

---

## E–F. Search & Math Opportunities

E1. Move ordering is dominant lever (H-0008): 50-90% node reduction expected.
E2. Alpha-beta sqrt(b) optimality with good ordering.
E3. TT, quiescence, aspiration, LMR, null-move pruning — all standard.
E4. make-unmake vs copy-make at depth >=10 (D-0005).
F1. Ray-stepping → PEXT/magic (H-0006: 1.3-2.5x). F2. 64-bit Zobrist (birthday bound ~4B).

---

## G–I. Evaluation, ML, Data

G1. Material-only eval is minimum. G2. Hand-tuned baseline (H-0004). G3. Tapered eval. G4. NNUE deferred.
H1–H5. No training pipeline, self-play, network arch, dataset mgmt, or experiment tracking.
I1–I5. Self-play requires Phase 2 engine first; time control, sampling, format, storage TBD.

---

## J. Performance Opportunities

J1. Release flag fix (E-0002): ~2.3x free win. J2. PEXT/magic (H-0006): 1.3-2.5x.
J3. Board copy removal (H-0007): >=10%. J4. AVX-512 VNNI for NNUE. J5. RTX 5070 Ti for NNUE/training.

---

## K. Methodology Weaknesses

K1. No SPRT framework (H-0010). K2. Low sample sizes. K3. No controlled A/B experiments.
K4. Example:true records must be cited as EXAMPLE. K5. Agent confidence ≠ evidence.

---

## L. SOTA Comparison

Stockfish 16+ (~3600), LC0 (~3500), Ethereal (reference). Kanamecide: no search/eval (~0 Elo). Gap: ~2-3 years.

---

## M. Novel Opportunities

M1. Research memory system itself. M2. Hybrid classical+GPU search. M3. AVX-512 VNNI for CPU NNUE.
M4. Incremental NNUE. M5. Multi-agent experiment design.

---

## N. What I Would Redesign

N1. 32-bit moves. N2. Design for ordering. N3. Keep hybrid board. N4. Standard alpha-beta stack.
N5. Material → PST → NNUE sequencing. N6. Pseudo-legal + filter in search. N7. UCI early. N8. /O2 always.

---

## O. Highest-Priority Experiments

O1. **E-0002** — Bench + /O2 baseline (~2.3x free win).
O2. **O3/E-AB** — Plain alpha-beta + MVV-LVA + killers + history + quiescence + ID + UCI.
O3. **E-PEXT** — PEXT/magic A/B (H-0006/D-0003).
O4. **E-MGCOPY** — Board copy removal (H-0007).
O5. **E-SPRT** — SPRT harness (H-0010).
O6. **E-PVS-TT** — PVS + TT deltas (H-0009).
O7. **E-EVAL** — Hand-tuned eval + Texel (H-0004).
O8. **E-COPYMAKE** — Copy-make vs make-unmake (H-0011/D-0005).

---

## P. Long-Term Directions

P1. NNUE training pipeline. P2. GPU MCTS/PUCT. P3. Hybrid classical+GPU. P4. Automated tuning.
P5. Opening book. P6. Endgame tablebases. P7. Multi-agent research optimization.

---

## Files Created / Updated

- This report (immutable).
- `current_position.md` (updated).
- H-0010 (SPRT harness), H-0011 (copy-make vs make-unmake).
- D-0005 (make-unmake vs copy-make debate).

---

## Confidence & What Would Change My Mind

Confidence 0.74. Classical-first strongly supported by literature. Perft demonstrated.
Would change mind if: O3 fails, MCTS+NNUE beats O3 at same cost, movegen <10% of search,
hand-tuned eval reaches 2800+ (NNUE priority drops), or copy-make dominates make-unmake.

---

## Last Updated

2026-09-09
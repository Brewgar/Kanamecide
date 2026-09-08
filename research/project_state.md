# Project State

> Canonical shared summary of the project. **Only stable, evidence-backed facts go here.**
> Agent opinions live in `research/agents/`; hypotheses in `research/hypotheses/`;
> decisions in `research/decisions/`. Do not add unverified claims to this file.

## Mission
Build a strong, research-driven chess engine ("Kanamecide", executable `kana`) and use it
as a platform for long-term multi-agent research. Correctness first, then search, then
evaluation and learning.

## Current Architecture
- **Language:** C++20.
- **Board representation:** bitboard + mailbox hybrid.
- **Hashing:** incremental Zobrist.
- **Move application:** make/unmake (not copy-make).
- **Move generation:** legal move generation (not pseudo-legal + filter).
- **En passant legality:** verified by make/unmake probe (handles discovered-check pins).
- **Phase:** correctness foundation complete; search not yet implemented.

## Current Strength
Move generator + board model validated against the Chess Programming Wiki perft suite with
exact matches (see table below).

## Current Performance

Verified perft results (all exact matches, from README.md):

| Position | Depth | Nodes |
|---|---|---|
| Startpos | 1–5 | 20, 400, 8902, 197281, 4865609 |
| Kiwipete | 3 | 97,862 |
| CPW pos 3 (EP/pins) | 4 | 43,238 |
| CPW pos 4 (promotions) | 4 | 422,333 |
| CPW pos 5 (promotions) | 4 | 2,103,487 |
| CPW pos 6 (quiet) | 4 | 3,894,594 |

## Hardware
- CPU: AMD Ryzen 7 9700X (8C/16T, AVX-512 with VNNI/BF16/FP16).
- RAM: 32 GB DDR5-6000.
- GPU: NVIDIA RTX 5070 Ti (16 GB, Blackwell, CUDA 13.3).
- OS/toolchain: Windows 11, MSVC 19.51, CMake 4.4.3.

## Current Models
None yet. The research system is model-independent; roles are mapped to models only in
`research/agents/ASSIGNMENTS.md`.

## Current Training Pipeline
None yet. Planned for Phase 3: self-play data generation + training (PyTorch + GPU).

## Active Research Questions
- Which search framework should be the primary architecture? (see `D-0001`, `H-0001`)
- How much do PVS + transposition tables help time-to-depth on this engine? (see `H-0001`, `E-0001`)
- How should evaluation (hand-tuned -> NNUE) be sequenced against search? (see the lesson in `F-0001`)

## Current Known Problems
- No search or evaluation yet — the engine only does board + move generation + perft.
- No self-play / data / training infrastructure.

## Recent Important Experiments
None executed yet. `E-0001` is pending (and is also an EXAMPLE record).
The movegen/perft validation is a correctness milestone, not a strength experiment.

## Current Champion
None — no playing strength exists yet.

## Current Development Priorities
1. **Phase 2 — Search:** alpha-beta/PVS with iterative deepening, transposition table,
   quiescence search, move ordering (killer/history/PV), aspiration windows, UCI.
2. **Phase 3+ — Evaluation & learning:** hand-tuned evaluation -> NNUE; self-play data
   generation; training pipeline (PyTorch + GPU); experiment tracking; SPRT-based testing.

## Last Updated
2026-09-08
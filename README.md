# Kanamecide — Chess Engine Research Project

## Phase 1: Correctness Foundation (COMPLETE)

A provably-correct chess move generator + board model, validated against the
Chess Programming Wiki perft suite. This is the bedrock that every future
architecture (alpha-beta, MCTS, NNUE) depends on.

### Verified perft results (all exact matches)

| Position | Depth | Nodes |
|---|---|---|
| Startpos | 1–5 | 20, 400,8902,197281,4865609 |
| Kiwipete | 3 | 97,862 |
| CPW pos 3 (EP/pins) | 4 | 43,238 |
| CPW pos 4 (promotions) | 4 | 422,333 |
| CPW pos 5 (promotions) | 4 | 2,103,487 |
| CPW pos 6 (quiet) | 4 | 3,894,594 |

### Architecture decisions

- **C++20** for the engine core (performance-critical)
- **Bitboard + mailbox hybrid** representation
- **Incremental Zobrist hashing**
- **Make/unmake** move application (not copy-make)
- **Legal move generation** (not pseudo-legal + filter)
- **En passant legality** verified by make/unmake probe (handles discovered-check pins)

### Hardware environment

- AMD Ryzen 7 9700X (8C/16T, AVX-512 with VNNI/BF16/FP16)
- 32 GB DDR5-6000
- NVIDIA RTX 5070 Ti (16 GB, Blackwell, CUDA 13.3)
- Windows 11, MSVC 19.51, CMake 4.4.3

### Build

```
cmake -G "Visual Studio 18 2026" -A x64 -S . -B build
cmake --build build --config Release
build\Release\kana.exe          # run perft suite
build\Release\kana.exe --moves  # list startpos legal moves
build\Release\kana.exe --fen "FEN" [depth]  # perft from FEN
```

## Phase 2: Search (NEXT)

Alpha-beta / PVS with:
- Iterative deepening
- Transposition table
- Quiescence search
- Move ordering (killer, history, PV)
- Aspiration windows
- UCI protocol

## Phase 3+: Evaluation, Learning, GPU

- Hand-tuned evaluation → NNUE
- Self-play data generation
- Training pipeline (PyTorch, GPU)
- Experiment tracking database
- SPRT-based engine testing

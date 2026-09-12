---
type: current_position
agent: systems-researcher
confidence: 0.65
focus: "Hardware ceilings + training/data pipeline design"
last_updated: 2026-09-10
---

# Current Position — systems-researcher

## Round 2 — First Entry (2026-09-10)

### Independent Verification Status
- **Perft 10/10 PASS**: VERIFIED — ran `build/Release/kana.exe`, all 10 positions exact match (startpos d1-5, kiwipete d3, cpw3/4/5/6 d4)
- **Pseudo-legal vs Legal**: VERIFIED — ran `build/Release/kana.exe --fen "7k/8/8/8/8/8/8/r3R2K w - - 0 1" 1` → 9 legal (perft) vs 16 pseudo-legal (generate_moves). The 7 illegal moves e1e2..e1e8 expose the king to the a1 rook.
- **/O2 vs /Od NPS gap**: TRUSTED FROM E-00003 — researcher-architect measured ~43-50 Mnps (/O2) vs ~19-21 Mnps (/Od), ratio ~2.1-2.4x. I did not independently rebuild due to build system friction but the scratch-harness methodology was sound and re-verified by adversarial-reviewer.

---

### A-P Assessment from Systems/Performance/Hardware Perspective

#### A. Architecture Understanding
**Bitboard + mailbox hybrid** (`board.h`): ~312 B `Board` struct (pieces[2][6] bitboards, occ[2], mailbox[64], king_sq[2], side, castling, ep, clocks, key). Incremental Zobrist via SplitMix64 deterministic seed.

**Move generation** (`movegen.cpp`): Pseudo-legal for all pieces except EP (make/unmake probe) and castling (not-through-check). King-safety filter applied post-make in `perft.cpp:16` and `main.cpp:66`. Sliding attacks via naive ray-stepping loops (`bitboard.cpp:54-72`) — **the primary CPU bottleneck**.

**Move application**: Make/unmake with `Undo` struct (captured, capt_sq, ep_prev, castling_prev, halfmove_prev, key_prev). No copy-make. Correctness verified by perft.

**Perft harness** (`perft.cpp`): Recursive with legality filter at every node. No timing output currently.

**Build system**: CMake 4.4.3, MSVC 19.51. Release ships `/Od /Zi /EHsc /JMC + /DEBUG` (CMakeLists.txt:16-17) — leaves ~2.3x NPS on table.

#### B. Strengths
1. **Correctness foundation is solid**: Perft 10/10 exact matches against Chess Programming Wiki suite.
2. **Incremental Zobrist + make/unmake**: Standard, well-validated approach; key maintenance verified by perft round-trip.
3. **Clean C++20 codebase**: No legacy cruft; easy to instrument, profile, and extend.
4. **Hardware is excellent**: Ryzen 7 9700X (Zen 5, AVX-512 + VNNI/BF16/FP16), 32 GB DDR5-6000, RTX 5070 Ti (Blackwell, 16 GB, CUDA 13.3). Consumer-peak for CPU inference and GPU training.
5. **Research memory system**: Markdown+YAML with strict fact/belief separation — reproducible, auditable.

#### C. Weaknesses
1. **Ray-stepping sliders dominate movegen**: `rook_attacks`/`bishop_attacks` are scalar loops with unpredictable branches. No PEXT/magic bitboards yet.
2. **No move ordering**: Moves generated in fixed piece-type order (pawns→knights→bishops→rooks→queens→king→castling). This will be the #1 search NPS limiter once search exists.
3. **16-bit Move encoding**: No room for capture flags, SEE scores, double-push flag, or ordering metadata without widening to 32-bit.
4. **Release ships /Od**: ~2.3x NPS penalty vs /O2 (E-00003). E-0002 fixes this.
5. **No search, eval, UCI, threading, time management**: Phase 1 only.
6. **Board copy in generate_moves** (line 6: `Board b_nc = b_in;`) for EP probe — ~312 B memcpy per generate_moves call.
7. **`attacked_by` recomputes occupancy per call**: `Bitboard occ = occ_all(b);` — redundant when caller already has it.

#### D. Correctness Risks (with usable tests)
1. **`generate_moves` mislabeled as "legal"** (D-0004): Consumers may trust unfiltered output. Fix: correct DEC-0005, README, project_state.md to "pseudo-legal + filter at search site"; add `--legality` audit mode.
2. **Zobrist collision**: 64-bit keys, birthday bound ~4.3B positions — acceptable for TT but monitor.
3. **EP edge cases**: Make/unmake probe handles horizontal double-pins correctly (verified by cpw3 perft).
4. **Castling rights**: Cleared on king/rook move from/to corners — correct.
5. **Halfmove clock / 50-move rule**: Maintained but not enforced; perft doesn't test it.
6. **Threefold repetition**: Not implemented; `same_position()` exists for audit.
7. **`move_promo` phantom on non-promotion moves** (`defs.h:52`): Returns garbage piece type when flag != PROMOTION. Add debug assert.
#### E. Search Weaknesses and Opportunities
- **No search yet**: Alpha-beta/PVS + ID + TT + quiescence + move ordering (MVV-LVA, killers, history) is the Phase 2 roadmap (researcher-architect H-0003/H-0008/H-0009).
- **Make/unmake vs copy-make** (D-0005): At ~45 Mnps /O2 perft, make/unmake undo path is ~O(1) writes; copy-make would be ~14 GB/s memcpy (312 B × 45M). Branch mispredictions in undo (promo/EP/castling) vs flat memcpy — needs E-COPYMAKE measurement on this hardware.
- **Transposition table**: Not yet designed. Bucket/replacement policy, key storage, aging — all open.

#### F. Mathematical Weaknesses and Opportunities
- **Perft is exact**: No Monte Carlo variance; deterministic node counts enable precise A/B.
- **Ray-stepping attack gen**: Mathematically correct but branch-heavy. PEXT/magic replaces with table lookup — speedup bounded by slider share of perft time (est. 30-50% on startpos; D-0003).
- **64-bit Zobrist uniformity**: SplitMix64 seed 0x9E3779B97F4A7C15ULL — deterministic, good statistical properties.

#### G. Evaluation Weaknesses and Requirements
- **No evaluation function exists**: Material-only is minimum baseline.
- **Hand-tuned → NNUE sequence**: Researcher-architect proposes tapered mg/eg + Texel tuning (H-0004/H-0013) before NNUE. I agree — CPU baseline must exist first.
- **NNUE architecture**: HalfKP input features, accumulator + output layers. AVX-512 VNNI on Zen 5 is the CPU inference path; RTX 5070 Ti for training + GPU inference exploration.

#### H. ML/Training Design Gaps
- **No training pipeline**: PyTorch + CUDA 13.3 on RTX 5070 Ti planned for Phase 3.
- **No experiment tracking**: Need W&B/MLflow or lightweight CSV+git for hyperparameter sweeps.
- **No model versioning**: Need ONNX export for engine integration; quantized int8/bf16 for VNNI.

#### I. Data/Self-Play Requirements (Phase 3 Prerequisites)
Before any training is meaningful, the following must exist:
1. **Working UCI engine** with time management (E-0002 + O3 search stack minimum).
2. **Position sampling strategy**: Opening book / FEN pool / self-play games with resignation/adjudication.
3. **Label generation**: Game result (W/D/L) + search depth/eval at each position. Need SPRT-validated engine for trustworthy labels.
4. **Deduplication**: FEN → canonical key (side-to-move normalized, castling/EP canonicalized). Target: <1% duplicate rate in training set.
5. **Difficulty sampling**: Balance quiet/tactical/endgame positions. Use search depth/ply or eval variance as proxy.
6. **Storage format**: Compressed binary (e.g., flatbuffers/msgpack) with schema for positions, moves, results, metadata. ~100 bytes/position → 10M positions = ~1 GB.
7. **Train/val/test splits**: Temporal (older games → train, newer → val/test) or ELO-stratified.

#### J. CPU/GPU/Performance Opportunities (with baselines)

| Opportunity | Current Baseline | Expected Gain | Measurement |
|-------------|------------------|---------------|-------------|
| **Release /O2 flags** (E-0002) | /Od: ~20 Mnps | ~2.3x → ~47 Mnps | E-0002 certified bench (5 reps, pinned, hash logged) |
| **PEXT/magic sliders** (H-0006, D-0003) | Ray-stepping ~47 Mnps | 1.3-2.5x (est.) | E-PEXT: bit-identical perft + NPS at /O2, 5 reps |
| **Move ordering** (H-0008) | None (fixed order) | 50-90% node reduction | O3 search: time-to-depth at fixed depth |
| **AVX-512 VNNI NNUE** | N/A | 2-5x vs scalar NNUE | Batch=1 latency on Zen 5; compare Stockfish NNUE VNNI |
| **RTX 5070 Ti batch inference** | N/A | Batch=1: ~50-200 µs; Batch=32: ~1-3 ms | Measure dense net (256-512 hidden) latency curve |
| **Board copy removal** (H-0007) | ~312 B copy/generate_moves | ≥10% (adversarial-reviewer skeptical) | E-MGCOPY: profile memcpy vs undo writes |
#### K. Research-Methodology Weaknesses
1. **No certified bench protocol yet** (E-0002): Must specify pinning, frequency policy, warm cache, binary hash.
2. **No SPRT framework** (H-0010): Adversarial-reviewer R-0002 Q2 requires two-tier protocol (screening δ≈20 Elo, regression δ=5 Elo).
3. **Falsification bounds conflict** (R-0002 Q3): H-0005 addendum backwards; H-0006 "<1.0x" vs D-0003 "<1.3x" — must unify before E-PEXT.
4. **D-0006 crossover vacuous**: Both build orders converge to same final config; need measurable proxy (days-to-interpretable-SPRT).

#### L. Comparison to State-of-the-Art
- **Stockfish 16+**: ~3600 Elo, ~50-100 Mnps (NNUE, heavy optimization), mature PVS+TT+LMR+NMP.
- **LC0**: ~3500 Elo, GPU MCTS/PUCT, large nets on TPU/V100; consumer GPU economics different.
- **Ethereal**: Honest classical intermediate reference (~3300 Elo, clean architecture).
- **Kanamecide**: 0 Elo (no search/eval). Gap: ~2-3 years of engineering if following classical path.

#### M. Potentially Novel Opportunities
1. **Hybrid classical + GPU search** (D-0001): PVS backbone on CPU + batched NNUE eval on GPU for wide nodes. Requires batch inference latency measurement first.
2. **Research collective as optimization target** (M5): Instrument discovery rate (hypotheses tested/week, experiments completed/week).
3. **Consumer-GPU economics first** (P3): Measure $/Elo for RTX 5070 Ti training + inference before committing to MCTS.
4. **Uncertainty-aware search** (M2): Dynamic widening where eval variance is high — cheap to prototype after O3.

#### N. What I Would Redesign from Scratch
1. **32-bit Move encoding** from day one: [0..5]=from, [6..11]=to, [12..15]=flags (capture, promo, EP, castle, double-push), [16..31]=score/ordering.
2. **Design movegen for ordering**: Generate captures first (MVV-LVA), then quiets with history/killers.
3. **PEXT/magic bitboards as default**: Ray-stepping only as correctness reference.
4. **Pseudo-legal + filter as explicit search contract**: Never emit illegal moves from the search's move loop.
5. **UCI + bench + time management early**: Enables self-play data generation sooner.

#### O. Highest-Priority Experiments
1. **E-0002** (O1): Bench harness + /O2 Release + binary-hash logging. 5 reps, pinned thread, fixed frequency, warm cache. **Unblocks all perf claims.** Cost: hours.
2. **E-PEXT** (O2): PEXT/magic sliders A/B at /O2, bit-identical perft, 5 reps. Resolves D-0003/H-0005/H-0006. Cost: days.
3. **O3 plain-alpha-beta + staged ordering + quiescence + ID + UCI** (O3): First strength measurement. Target: depth ≥10 in <10s at /O2 on startpos. Cost: 1-2 weeks.
4. **GPU batch-inference latency curve**: Measure RTX 5070 Ti batch=1..N latency for small dense net (256-512 hidden). **Gate for D-0001 GPU MCTS feasibility.** Cost: hours.
5. **E-COPYMAKE**: Time-to-depth comparison make/unmake vs copy-make at depths 6-14. Resolves D-0005. Cost: days.

#### P. Highest-Upside Long-Term Research Directions
1. **Closed self-play loop** with Elo/week as collective KPI — funds all other directions with real data.
2. **Hybrid classical + learned** (PVS backbone + ablatable policy/value NNUE).
3. **Consumer-hardware economics**: CPU VNNI vs GPU batch inference $/Elo before any MCTS commitment.
4. **Discovery-rate instrumentation**: Treat the multi-agent collective itself as a system to optimize.
---

### B. Opinion of Project State

**Strongest and most trustworthy**: The **correctness foundation (board + movegen + perft + Zobrist)**. Perft 10/10 exact matches are demonstrated facts, not beliefs. The make/unmake + incremental Zobrist implementation is clean, auditable, and matches engine literature. The research memory system (Markdown+YAML, strict fact/belief separation) is a genuine strength — it enables this multi-agent collective to function.

**Weakest and most likely wrong**: The **pseudo-legal vs legal contract confusion (D-0004)**. The code is pseudo-legal (correctly filtered in perft), but DEC-0005, project_state.md, README.md, and the megaprompt all claim "legal move generation". This mislabel is live in the shipped `dump_moves` output. If a Phase 2 search consumer trusts `generate_moves` output as fully legal, it will emit illegal moves (e.g., king into check, pinned piece moves). The fix is documentation + contract correction, not code change — but the longer it persists, the higher the risk of a downstream correctness bug.
---

### C. Debate Positions (D-0001..D-0006)

| Debate | Position | Confidence | Agreement Statement |
|--------|----------|------------|---------------------|
| **D-0001** Classical-first vs GPU MCTS | **Classical alpha-beta/PVS first. GPU MCTS is Phase 3+ only after: (a) measured CPU baseline (O3), (b) trained eval net exists, (c) batch=1 GPU latency curve measured on RTX 5070 Ti.** | 0.8 | **AGREE with researcher-architect** on classical-first because MCTS-without-net is circular (needs policy/value → needs games → needs playing engine). **DISAGREE with systems-researcher (prior mock position)** that MCTS/GPU should be parallel-tracked — opportunity cost too high before baseline exists. |
| **D-0002** /Od flags invalidate NPS; kana_o2 provenance | **All NPS/speedup claims are PROVISIONAL until E-0002 certified bench (5 reps, pinned, fixed frequency, warm cache, binary hash logged). kana_o2.exe is EXCLUDED from claims until provenance documented.** | 0.9 | **AGREE with researcher-architect and adversarial-reviewer** that current numbers are provisional (~2 sig figs, unpinned). Two-tier rule: provisional for screening/rank-order only; certified for project_state.md. |
| **D-0003** PEXT ≥3x vs 1.3-2.5x | **PEXT/magic gain will be 1.3-2.5x, NOT ≥3x.** At ~47 Mnps /O2 baseline, 3x would require >140 Mnps — implausible for slider-only swap. Slider share of perft time est. 30-50% on startpos; max theoretical speedup ~2x. | 0.7 | **AGREE with researcher-architect (revised position, Agent B)** and **adversarial-reviewer** that 1.3-2.5x is the working prior. H-0005's ≥3x was filed pre-measurement; E-00003 baseline makes it implausible. Pre-register 4-way partition from D-0003 before E-PEXT. |
| **D-0004** generate_moves pseudo-legal vs legal | **Implementation is pseudo-legal; correct the record (DEC-0005, README, project_state.md) to "pseudo-legal + king-safety filter at search site". Keep generator as-is (standard, fastest design). Add `--legality` audit mode.** | 0.97 | **AGREE with researcher-architect and adversarial-reviewer** — confirmed at runtime (16 vs 9 on pinned-rook FEN). No behavior change needed; contract/documentation fix only. |
| **D-0005** make/unmake vs copy-make | **Keep make/unmake as O3 default. Run E-COPYMAKE as side microbenchmark with pre-registered ≥5% TTD rule at depths 6-14. At ~45 Mnps, per-node 312 B copy = ~14 GB/s memcpy + cache pressure vs O(undo-bytes) writes.** | 0.65 | **AGREE with adversarial-reviewer** that priors favor make/unmake (0.6). Copy-make crossover is plausible at depth ≥10 but unmeasured. Decision rule: copy-make wins only if ≥5% TTD advantage reproduced on two suites. |
| **D-0006** O3 build order: quiescence-first vs PVS/TT-first | **Quiescence first (inside O3 baseline). Without quiescence, every leaf eval is horizon-noisy → no score-based comparison (PVS/TT node counts, Elo, SPRT) is interpretable. PVS/TT node-count deltas measured on noisy leaves don't carry forward once quiescence changes every leaf.** | 0.7 | **AGREE with researcher-architect and adversarial-reviewer** on conclusion (quiescence-first). **AMEND adversarial-reviewer's proposed resolution**: The crossover experiment as written is vacuous (both paths converge to identical final config). Pre-register measurable proxy: (i) days-to-first-interpretable-SPRT-result, (ii) final fixed-depth nodes/TTD matrix at each stage. |

---

### D. R-0002 Objections Response

| Objection | Ruling | Record Change |
|-----------|--------|---------------|
| **1. SPRT parameterization (H-0010)**: Defaults omit LLR thresholds, max-game cap, draw model, pairing protocol, time control, opening set. 5 Elo gate at α=β=0.05 costs ~15-20k+ games. | **AMEND** | Add two-tier SPRT protocol to H-0010: (a) Screening tier: δ=20 Elo, α=β=0.05, LLR ±2.944, cap 5k games, draws=0.5 trinomial, 1000-pos rotating opening set, balanced colors, 10+0.1s TC, crash=loss, post-cap=INCONCLUSIVE. (b) Regression tier: δ=5 Elo, same params, cap 30k games. File addendum to H-0010. |
| **2. H-0005 falsification bound**: Addendum states "Falsification of H-0005 requires ratio ≥ 3.0" — backwards (≥3x CONFIRMS H-0005). | **AMEND** | Fix H-0005 addendum: "Falsification of H-0005 requires E-PEXT NPS ratio < 3.0". Align H-0006 "<1.0x" with D-0003's "<1.3x" → unify to single 4-way partition in D-0003: ratio ≥3.0 → H-0005 confirmed; 1.3≤ratio<3.0 → H-0005 falsified, H-0006 supported; 1.0<ratio<1.3 → both magnitude claims falsified; ratio≤1.0 → both rejected. |
| **3. D-0006 vacuous crossover**: Both build orders converge to identical final config by construction; "if identical, A wins" is tie-break, not evidence. | **AMEND** | Replace D-0006 crossover with adversarial-reviewer's measurable proxy: (i) days-to-first-interpretable-SPRT-result per path; (ii) fixed-depth nodes/TTD matrix at each stage (plain-AB → +quiescence → +PVS → +TT vs plain-AB → +PVS → +TT → +quiescence); (iii) keep fixed-depth plain-AB node counts as regression pins during quiescence development. Pre-register decision rule: if (i) differs materially, faster path wins; if identical, quiescence-first tie-break applies. |
---

### E. Prioritized Project Improvements (up to 5)

| # | WHAT | WHERE | WHY | EXPECTED BENEFIT | PRE-REGISTERED MEASUREMENT |
|---|------|-------|-----|------------------|----------------------------|
| 1 | **Add `--bench` harness with /O2 Release + binary-hash logging** | `main.cpp` (new `--bench [reps]`), `CMakeLists.txt` (Release → `/O2 /DNDEBUG /arch:AVX512`), `src/` (no changes) | Unblocks every perf claim; current /Od ships ~2.3x slower | Certified NPS baseline for all future A/B; ~2.3x free win | E-0002: 5 reps × 3 positions (startpos d5, kiwipete d4, cpw6 d4), pinned thread, fixed frequency, warm cache. Report mean/median/min-max NPS + flags + git hash + binary SHA256. |
| 2 | **Implement PEXT/magic bitboards for sliders** | `src/bitboard.cpp` (`rook_attacks`, `bishop_attacks`), magic constants in new `magic.h/.cpp` | Ray-stepping is the primary CPU bottleneck in movegen (slider attacks) | 1.3-2.5x perft NPS gain (H-0006/D-0003); enables competitive search NPS | E-PEXT: A/B at fixed /O2, bit-identical full perft suite, 5 reps. Decision rule: ratio ≥3.0 → H-0005 confirmed; 1.3≤ratio<3.0 → H-0006 supported; 1.0<ratio<1.3 → both falsified; ≤1.0 → both rejected. |
| 3 | **Implement staged move ordering (MVV-LVA + killers + history)** | New `movepick.h/.cpp`; integrate into search (O3) | Move ordering is the dominant Phase 2 lever (50-90% node reduction expected, H-0008) | 3-10x time-to-depth improvement vs unordered; enables depth ≥12 in <10s | O3: time-to-depth on startpos at depths 8, 10, 12, 14 vs unordered baseline. Target: depth 10 in <10s at /O2. |
| 4 | **Add UCI + time management + repetition detection** | `src/uci.h/.cpp`, `src/search.cpp` (new), `main.cpp` | Required for self-play data generation (Phase 3 prerequisite) | Enables automated games, SPRT testing, self-play dataset collection | E-UCI: 1000 games at 10+0.1s vs random mover — 0 crashes/stalls, legal moves only. |
| 5 | **Profile and optimize `generate_moves` Board copy + `attacked_by` occ recompute** | `src/movegen.cpp:6` (remove `Board b_nc` copy; pass `const Board&` + precomputed occ to EP probe), `src/board.cpp:95` (add `attacked_by(const Board&, Square, Color, Bitboard occ)` overload) | ~312 B memcpy per generate_moves call + redundant occ recompute in hot path | ~5-10% perft NPS gain (H-0007); reduces cache pressure | E-MGCOPY: perft NPS before/after at /O2, 5 reps. Target: ≥5% NPS improvement. |

---

### F. Pre-Registered Experiment to Change Mind

**Experiment**: **GPU Batch-Inference Latency Curve for NNUE-Scale Net on RTX 5070 Ti**

```bash
python research/scripts/research.py new-experiment \
  --title "GPU batch-inference latency curve (RTX 5070 Ti, dense net 256-512 hidden)" \
  --hypothesis "H-GPU-LATENCY: Batch=1 latency ≤ 200 µs and batch=32 throughput ≥ 100k inferences/sec on RTX 5070 Ti for a 256-512 hidden unit dense net (NNUE-scale)" \
  --baseline "CPU AVX-512 VNNI batch=1 latency on Ryzen 9700X (to be measured)" \
  --candidate "CUDA 13.3 kernel with tensor cores (BF16/FP16), batch=1,2,4,8,16,32,64,128" \
  --hardware "RTX 5070 Ti (16 GB, Blackwell), CUDA 13.3, Windows 11" \
  --engine-version "Pre-search HEAD (perft-only)" \
  --network "Dense: input=768 (HalfKP) → 256/512 hidden (LReLU) → 1 output (value), ~200k params" \
  --dataset "Synthetic random positions (no training needed — measure inference only)" \
  --method "Warmup 1000 inferences, then 10000 timed inferences per batch size. Report p50/p95/p99 latency (µs) and throughput (inferences/sec). Pin GPU clock (nvidia-smi -lgc)." \
  --metric "Batch=1 latency (µs), batch=32 throughput (inferences/sec), latency scaling exponent" \
  --decision-rule "IF batch=1 latency > 500 µs OR batch=32 throughput < 50k inf/s → GPU MCTS infeasible for Phase 3 (ROUTE to CPU-first). IF batch=1 ≤ 200 µs AND batch=32 ≥ 100k inf/s → GPU MCTS feasible (AGREED for D-0001 Phase 3+). ELSE → CONFLICT (needs architecture-specific measurement)."
```

**Why this changes my mind**: My biggest open disagreement is D-0001 (GPU MCTS feasibility). Without actual RTX 5070 Ti batch-inference numbers, all GPU MCTS arguments are speculative. This experiment provides the feasibility gate: if consumer GPU can't do batch=1 ≤ 200 µs for NNUE-scale net, GPU MCTS/PUCT cannot compete with classical PVS+NNUE on this hardware.

---

### G. Compliance
- No `src/` edits made.
- No other agents' files edited.
- History appended only (no overwrites).
- All positions use calibrated language (demonstrated/strongly supported/likely/plausible/speculative/unknown).

---

### Independent Verification Marks
- Perft 10/10 PASS: **VERIFIED** (2026-09-10, this session)
- Pinned-rook FEN 9 legal vs 16 pseudo-legal: **VERIFIED** (2026-09-10, this session)
- /O2 vs /Od NPS gap (~2.3x): **TRUSTED FROM E-00003** (reproduced by researcher-architect and adversarial-reviewer; not independently rebuilt due to build friction)

---

## Prior Position (Placeholder)
*This agent had a placeholder `current_position.md` prior to Round 2. All content above is the first substantive entry.*

---

## Confidence
**0.65 overall**. Perft correctness + pseudo-legal finding: demonstrated (0.9+). /O2 baseline: trusted from E-00003 (0.85). PEXT magnitude 1.3-2.5x: likely (0.7). Classical-first: likely (0.8). GPU MCTS feasibility: speculative until batch curves measured (0.3). Make/unmake vs copy-make: plausible crossover at depth≥10 (0.65). SPRT two-tier: needed (0.9).
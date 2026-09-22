---
type: current_position
agent: researcher-architect
confidence: 0.78
focus: "Phase-2 search architecture + pseudo-legal movegen contract + SPRT methodology"
last_updated: 2026-09-10
---

# Current Position — researcher-architect

## Overall Assessment (independent A-P re-verification, 2026-09-09)

Baseline re-run by me THIS session: build/Release/kana.exe → 10/10 PASS, ALL TESTS PASSED
(startpos d1-5: 20/400/8902/197281/4865609; kiwipete d3 97862; cpw3 d4 43238; cpw4 d4
422333; cpw5 d4 2103487; cpw6 d4 3894594). /O2 vs /Od gap stands measured (E-00003:
~43-50 vs ~19-21 Mnps, 2.1-2.4x). No src/ edits (assignment forbids).

New this session (independent analysis, report
2026-09-09-independent-a-p-analysis-baseline-re-verified-plus-phase-2-3-architecture-gaps.md):
- H-0012 (0.7): search fast-path move invariants (king-capture exclusion + promo-phantom
  asserts) before any captures-only/SEE/staging work.
- H-0014 (0.6): board state-integrity audit (halfmove/EP-key/rights round-trip +
  key==compute_key oracle) as a permanent debug gate before TT lands.
- H-0013 (0.6): tapered mg/eg + Texel protocol pinning H-0004's missing design
  (phase weights, game-split holdouts, pre-registered SPRT gates).
- H-0015 (0.3, speculative/low): learned time-management from eval variance (Phase 4+).
- D-0006: O3 build order — quiescence-first (my position, 0.7) vs PVS+TT-first (open);
  crossover experiment pre-registered.
- Roadmap position sharpened: quiescence belongs INSIDE the O3 baseline (not after PVS/TT),
  because score-based comparisons are uninterpretable on horizon-noisy leaves.

Roadmap: E-0002 (bench+/O2) → O3 plain-AB + staged ordering + quiescence + ID + UCI +
repetition/time (first strength number) → PVS-only/TT-only deltas (H-0009) → E-PEXT
(H-0006/D-0003) → E-MGCOPY (H-0007) → SPRT (H-0010) → E-EVAL tapered+Texel (H-0004/H-0013)
→ E-COPYMAKE (H-0011/D-0005) → self-play/data → NNUE → GPU PUCT vs O3 → hybrid.
Confidence 0.74.

## Prior Overall Assessment (fresh A–P analysis, 2026-09-09, retained)
Fresh baseline run COMPLETED by me this session: perft 10/10 PASS exactly (startpos d1-5,
kiwipete d3, cpw3/4/5/6 d4); `--moves` 20 startpos moves; kiwipete d3 split total 97,862 over
48 roots. Release ships debug flags (`/Od /JMC /DEBUG`, CMakeLists.txt:16-17). Measured NPS via
external harness (E-00003): **/O2 ~43-50 Mnps** vs **/Od ~19-21 Mnps** (ratio 2.1-2.4x).

**New findings this session (full A–P analysis):**
- H-0010 filed: SPRT-based engine comparison harness is required before any version claim is trustworthy.
- H-0011 filed: Copy-make may outperform make-unmake for alpha-beta at depths >=10 on this hardware.
- D-0005 filed: make-unmake vs copy-make for Phase 2 search (DEC-0004 under conditions).
- Full A–P analysis written to reports/2026-09-09-fresh-a-p-analysis-*.md.

**New finding this session:** `generate_moves` (movegen.cpp) is **pseudo-legal**, not legal — only
en passant (make/unmake probe) and castling are legality-checked inline; king-safety filtering
happens later in perft.cpp:16 and main.cpp:66. This contradicts DEC-0005, project_state.md,
README.md, and the megaprompt "Ground truth", which all claim "legal move generation (not
pseudo-legal + filter)." The *system* is correct (perft validated) but the *label* is wrong and
could mislead Phase-2 search consumers. Filed as debate **D-0004**; resolution = correct the
contract to "pseudo-legal + filter at the search site."

**Roadmap (unchanged order, sharpened reasoning):**
1. **E-0002** — bench + /O2 build (hours; unblocks every perf claim; ~2.3x free win).
2. **O2** — plain alpha-beta + MVV-LVA/killers/history + quiescence + ID + UCI, material-only
   eval; fixed-node SPRT vs random + time-to-depth. This is the first *strength* measurement the
   project has ever had. Move ordering is the dominant lever (H-0008), not bitboards.
3. **O3** — PVS + TT as separate controlled deltas (H-0009).
4. Then E-PEXT (H-0006), board-copy microbench (H-0007), hand-tuned eval + Texel (H-0004),
   SPRT harness, self-play, NNUE.

Confidence 0.72. Full analysis: reports/2026-09-09-a-p-analysis-move-ordering-lever-*.md.

## Prior Overall Assessment (baseline-revalidated revision, 2026-09-09, retained)
Fresh baseline run COMPLETED by me this session: perft 10/10 PASS exactly
(startpos d1-5, kiwipete d3, cpw3/4/5/6 d4); `--moves` 20 legal moves; kiwipete d3 split
total 97,862 over 48 roots. Measured NPS via external harness (E-00003, repo src/ untouched):
**/O2 ~43-50 Mnps** (startpos d5 ~47.0-47.4, kiwipete d4 ~43.1, cpw6 d4 ~50.0-50.4) vs
**/Od ~19-21 Mnps** (ratio 2.1-2.4x); perft counts bit-identical between builds. Implication:
(1) Release flag fix (E-0002) is a ~2.3x free win; (2) the movegen is ALREADY fast → the
PEXT `>=3x` claim (H-0005) is revised down to 1.3-2.5x (H-0006, conf 0.6; debate D-0003);
(3) the real Phase 2 lever is search (node reduction via ordering/TT), not bitboards.
Roadmap unchanged: E-0002 bench/O2 → E-PEXT → plain alpha-beta stack + UCI (O3) →
hand-tuned eval (H-0004) → SPRT/self-play → NNUE. Full analysis:
reports/2026-09-09-baseline-revalidated-a-p-analysis-*.md. Confidence 0.74.

## Prior Overall Assessment (independent-baseline revision, 2026-09-09, retained)
Phase 1 is sound by inspection (legal movegen + make/unmake + incremental Zobrist +
perft-suite structure match CPW references in main.cpp:89-154). I could NOT re-run
kana.exe this session (shell integration broken: even echo exits 1 with no capture),
so perft PASS is strongly supported, not freshly demonstrated, and ALL NPS numbers are
UNKNOWN. Release ships debug codegen (/Od /JMC /DEBUG, CMakeLists.txt:16) — no perf
claim survives that. Roadmap: bench/O2 baseline (E-0002) -> PEXT (H-0005) -> plain
alpha-beta stack + UCI (O3, E-0001 design) -> hand-tuned eval (H-0004) -> SPRT/self-play
-> NNUE. Classical-first (H-0003, 0.75). Full analysis:
reports/2026-09-09-independent-baseline-a-p-analysis.md. Prior text archived below.

## Prior Overall Assessment (2026-09-09 and earlier, retained for provenance)
The Kanamecide engine has a solid, verified correctness foundation (Phase 1 complete). All perft tests pass with exact matches to the Chess Programming Wiki reference suite. The board representation (bitboard/mailbox hybrid), move generation (legal, with make/unmake EP legality probe), Zobrist hashing, and make/unmake are correct and suitable as a baseline. No search, evaluation, or UCI exists yet — this is the Phase 2 blocker.

**Key architectural decision**: Start with classical alpha-beta/PVS search with iterative deepening, transposition tables, and basic move ordering (MVV-LVA, killers, history). This is the overwhelmingly proven approach for CPU chess engines. GPU MCTS/PUCT is a Phase 3+ research direction *after* we have a measured CPU baseline and a trained NNUE evaluator.

## Strongest Parts (re-verified 2026-09-09: fresh 10/10 perft PASS this session)
- **Correctness foundation**: 10/10 perft tests pass exactly. Legal move generation eliminates a whole class of bugs.
- **Clean C++20 codebase**: Modern stdlib, clear separation of concerns, no premature optimization.
- **Incremental Zobrist**: Deterministic, reproducible, ready for TT.
- **Make/unmake with full Undo**: Correct state restoration verified by perft.
- **Hardware**: Ryzen 7 9700X (AVX-512 VNNI/BF16, PEXT) + RTX 5070 Ti — excellent for both CPU search and future NNUE/GPU work.

## Weakest Parts (recalibrated 2026-09-09: unmeasured factors marked UNKNOWN)
- **Release ships debug codegen (/Od)**: no perf claim interpretable (HIGH; E-0002 fixes).
- **Ray-stepping sliding attacks**: bottleneck CLASS strongly supported, factor UNKNOWN
  on this engine (was "~10-30x" — downgraded to H-0005, 0.7).
- Prior list retained below for provenance (magnitudes unmeasured).
- **Ray-stepping sliding attacks**: ~10-30x slower than PEXT magic bitboards. Major bottleneck (C1).
- **No move ordering**: Alpha-beta without ordering degrades to minimax (C2).
- **No search/eval/UCI**: Engine cannot play (C3, C6, C7, C8).
- **16-bit move encoding**: Limits extensibility for move ordering scores, capture flags (C4).
- **No experiment/SPRT framework**: Cannot rigorously compare versions.

## Current Preferred Architecture
**Phase 2 (Search)**: Classical alpha-beta/PVS with:
- Iterative deepening + aspiration windows
- Transposition table (64-bit Zobrist, bucketed, always-replace/deep-preferred)
- Move ordering: PV move → captures (MVV-LVA) → killers → history → quiet (SEE)
- Quiescence search: captures + checks + promotions, with delta pruning
- UCI protocol + basic time management

**Phase 2 (Evaluation)**: Hand-tuned linear eval (material + PST + king safety + pawn structure), Texel/SPSA tuned on 50k quiet positions.

**Phase 3 (NNUE)**: HalfKP (2×256→32→1) trained on self-play data, INT8 quantized, AVX-512 VNNI inference on CPU.

**Phase 3+ (Research)**: Hybrid search (alpha-beta backbone + learned policy/value heads for move ordering/pruning), continuous self-play loop, uncertainty-aware search.

## Highest-Value Research Direction (independent baseline, 2026-09-09)
E-0002 bench + /O2 baseline (hours; unblocks every perf claim), then E-PEXT (H-0005),
then O3 plain alpha-beta + UCI (E-0001 design; H-0003). Details in
reports/2026-09-09-independent-baseline-a-p-analysis.md (§O). Prior text retained below.

## Prior Highest-Value Research Direction (retained)
**E-0001: Baseline Classical Search** — Implement the complete Phase 2 search stack and measure NPS, time-to-depth, and self-play Elo. This is the single blocking dependency for all subsequent work (eval tuning, NNUE training, SPRT, self-play). Without a working search, we cannot measure anything.

### Baseline-revalidated addendum (2026-09-09)
1. E-00003 NPS values are ~2-significant-digit baselines (1-3 reps, unpinned; single
   machine) — E-0002 in-tree benchmark is the certification path.
2. PEXT expectation revised: H-0005 `>=3x` down to conf 0.45; H-0006 (1.3-2.5x, conf 0.6)
   and D-0003 filed; resolution requires E-PEXT.
3. H-0007 filed: per-call `Board` copy in `generate_moves` may cost >=10% perft NPS —
   measure, don't assume.
4. kana_o2.exe (253,952 B) still has unrecorded provenance — excluded from all claims.

## Major Concerns (independent-baseline addendum, 2026-09-09)
1. Unmeasured numbers in prior report/position (6 Mnps, 15-30%, 3-8x, week dates,
   E-0002..E-0007 as commitments): downgraded to H-0003/H-0004/H-0005; see full report.
2. kana_o2.exe provenance unknown — exclude from claims until logged (D-0002, E-0002).
3. King-capture pseudo-moves (mask) + move_promo phantom (defs.h:52): invariant docs +
   debug audits before any fast path (report D1/D2).
4. H-0001/D-0001/E-0001/F-0001/R-0001 are example:true mocks — cite as EXAMPLE only.
5. Prior concerns retained below.

## Prior Major Concerns (retained for provenance)
1. **Premature GPU/MCTS exploration**: The debate D-0001 positions are plausible but unmeasured. Opportunity cost of parallel-tracking MCTS before classical baseline is high.
2. **Ray-stepping bottleneck**: Must be fixed (E-0002) before search NPS is meaningful.
3. **No statistical rigor yet**: SPRT framework (E-0004) needed before any version comparisons are trustworthy.
4. **Move encoding limits**: 16-bit format will need widening for move ordering scores; plan for 32-bit in Phase 2.

## Open Questions
1. **TT bucket/replacement policy**: Start simple (always-replace or deep-preferred) or implement clustered buckets from day one?
2. **Aspiration window delta**: Fixed 50cp? Dynamic based on depth?
3. **Quiescence delta pruning margin**: Standard 200-300cp or tune?
4. **Self-play time control**: 10+0.1s? 60+0.6s? Faster games = more data but lower quality.
5. **NNUE training target**: Policy + value (AlphaZero-style) or value-only (Stockfish-style)?

## Confidence
0.74 — perft-correct DEMONSTRATED (fresh 10/10 PASS this session); classical-first likely
(literature, H-0003 0.75); flag gap MEASURED (E-00003, 0.9); ordering-dominance likely by
theory (H-0008 0.7); PEXT/copy-make/eval magnitudes plausible only (0.45-0.65, gated on
measurement); GPU MCTS speculative until a net + batch=1 latency curves exist. New
positions: quiescence-inside-O3 (D-0006, 0.7), move invariants H-0012 (0.7), state audit
H-0014 (0.6), tapered-Texel protocol H-0013 (0.6), learned time-mgmt H-0015 (0.3). Prior
text retained below.

## Prior Confidence (retained for provenance)
0.78 — High confidence in classical search as Phase 2 foundation (overwhelming literature evidence). Medium confidence in specific implementation choices (TT policy, aspiration, quiescence params) — these need measurement. Low confidence in GPU MCTS viability on consumer hardware with NNUE-scale nets — speculative until proven.

## What Would Change My Mind (independent re-verification, 2026-09-09)
- E-0002 certified bench overturning E-00003 (~2.3x flag gap, ~47 Mnps /O2).
- O3 failing (<1 Mnps or <+200 vs random after full stack) → revisit architecture.
- Same-hardware MCTS+NNUE prototype beating O3 at same cost.
- E-PEXT ratio outside [1.3,2.5] (restores H-0005 or kills both; D-0003 rule).
- E-STATEAUDIT (H-0014) firing → correctness work preempts search.
- E-EVAL (H-0004/H-0013) reaching 2800+ → NNUE priority drops.
- D-0006 crossover showing PVS+TT-first path superiority → adopt it (methodology loss).
- E-0002 bench numbers (flags fixed, binary hashes logged).
- O3 failing (<1 Mnps or <+200 vs random after full stack) -> revisit architecture.
- Same-hardware MCTS+NNUE prototype beating O3 at same cost.
- Profiling showing movegen <10% of search (unlikely); Texel hand-tuned 2800+ (drops
  NNUE priority).
- New risks documented: enemy-king pseudo-moves + move_promo phantom need debug audits
  before any fast path (report §D).

## Prior What-Would-Change-My-Mind (retained)
- **Classical search fails**: If E-0001 achieves <1 Mnps or <+200 Elo vs random after full implementation, revisit architecture.
- **GPU MCTS prototype demonstrates**: A working MCTS+NNUE on RTX 5070 Ti that beats classical baseline at same hardware cost.
- **Ray-stepping not a bottleneck**: If profiling shows move generation is <10% of search time (unlikely).
- **Hand-tuned eval sufficient**: If Texel-tuned hand-crafted eval reaches 2800+ Elo with good search, NNUE priority drops.

# Round 2 — Convergence / Ratification Entry (researcher-architect, 2026-09-10)

## A. R-0002 objections — rulings (SUPPORT / REFUTE / AMEND)
1. SPRT parameterization (H-0010) — SUPPORT direction, AMEND protocol: two-tier bar (screening
   H1=+20 Elo cap 5k; regression H1=+5 Elo cap 30k; alpha=beta=0.05; LLR +/-2.944; draws=0.5
   trinomial; balanced colors + 1000-pos rotating openings; fixed TC; crash=loss;
   post-cap=INCONCLUSIVE); ratify in H-0010 addendum / E-SPRT before the first game.
2. H-0005 backwards bound — REFUTE sentence, AMEND records: "falsification requires ratio >= 3.0"
   is backwards (>=3.0 confirms the >=3x claim). Adopt the single 4-way CI partition; align
   H-0006's fence to "outside [1.3, 2.5]" (B.1).
3. D-0006 vacuous crossover — SUPPORT (AMEND): both paths converge to the identical final
   configuration. Replace with fixed-depth nodes/TTD matrix + days-to-first-interpretable-SPRT
   proxy; keep plain-AB node counts as regression pins.

## B. Rulings on the six unratified amendments
1. H-0005 backwards / H-0006 fence — ACCEPT: align H-0006 falsification to "ratio outside
   [1.3, 2.5]", fold into the single 4-way CI partition ([1.0,1.3) sub-band keeps "direction
   survives" as its own arm).
2. E-00004 as gate — RE-SPECIFY BEFORE GATING: its CPU baseline is measured but never enters the
   decision rule; HalfKP feature-transform + PCIe cost absent; b=32 throughput is not the binding
   PUCT constraint. D-0001 stays ROUTED.
3. O3 split (O3a->O3b->O3c->O3d) — ACCEPT, proviso: O3b (ordering) measured on node-count/TTD
   only; no Elo/score claim until O3c (quiescence). Preserves quiescence-first.
4. kana_o2.exe (253,952 B != 74,240 B) — DELETE (or quarantine): provenance unreconstructable
   (size differs from the build_o2 scratch exe); dispose in Milestone 0.
5. E-00005 precedes E-PEXT — ACCEPT sequencing, AMEND framing: the profile (Amdahl ceiling) must
   precede E-PEXT; but 0.5 is a confidence, not a magnitude prior; E-00005 narrows, but does not
   substitute for, E-PEXT's ratio measurement (D.2).
6. E-COPYMAKE escape + CI — ACCEPT: copy-make wins only if >=5% mean TTD and the 95% CI excludes
   0, at a depth with >=10 s TTD; if none reaches 10 s, fall back to max achievable depth <=14
   with the same CI test; else DEC-0004 stands (INCONCLUSIVE -> make/unmake).

## D. Weaknesses / falsifiers in other agents' arguments
1. E-00004 (systems-researcher): CPU baseline listed but never wired into the rule — an unused
   baseline falsifies nothing. If GPU b=1 = 150 us but CPU AVX-512 VNNI b=1 = 40 us (plausible for
   a ~200k-param net), the "<=200 us" arm still fires "feasible" while the GPU is ~4x slower per
   leaf. The two arms also leave a non-decision gap (200-500 us / 50k-100k), so E-00004 can never
   CLOSE D-0001.
2. E-00005 (implementation-engineer): the <30% / >=60% partition collapses two levers (movegen
   slider gen AND the once-per-node attacked_by re-derivation) into one scalar, and 1/(1-share) is
   the ceiling only if PEXT drives slider cost to ~0 (it will not). Contradiction: a 55% share ->
   Amdahl ~2.22x, yet the 30-60% band labels 2.5x "unlikely"; and ">=60% => highest-value lever"
   ignores that H-0008 ordering (a node-count lever) can dwarf any NPS gain.
3. Implementation-engineer's D-0002 conf 0.9 is a procedural claim not yet executed; its
   "2.5x => sliders ~60%+" is the same circular Amdahl shortcut (2.5x implies 60%, then 60% is
   used to call 2.5x reachable).
4. Systems-researcher's /O2 baseline "TRUSTED FROM E-00003" (conf 0.85) is over-stated for a
   finding not independently rebuilt (compliant with S6.2, but inherited, not reproduced).

## E. Final Phase-2 build order (collective-owned, pre-registered rules)
1. E-0002 (Milestone 0): cert bench + /O2 + binary-hash; delete/quarantine kana_o2.exe. Rule:
   perft bit-identical else revert; certified O2 NPS recorded.
2. E-00005 (pre-PEXT profile; after E-0002, MUST precede E-PEXT). Rule: slider_share >=30% => run
   E-PEXT; <30% => 2.5x falsified.
3. O3a plain alpha-beta + material eval + DEC-0008 filter. Rule: legal moves, reproducible
   nodes-to-depth.
4. O3b ordering (PV -> MVV-LVA -> killer -> history). Rule: node-count/TTD vs O3a (no Elo yet).
5. O3c quiescence (stand-pat + captures + delta). Rule: first score-interpretable engine.
6. O3d ID + repetition/50-move + TC + UCI. Rule: 1000 games vs random (0 crashes/stalls, legal
   only).
7. PVS/TT deltas (H-0009): TT-only / PVS-only / both. Rule: nodes + TTD per stage, fixed hash.
8. E-PEXT (after E-00005 + E-0002). Rule: single 4-way CI partition; boundary-straddling CI =>
   INCONCLUSIVE.
9. E-COPYMAKE (after O3d). Rule: B.6.
10. E-SPRT (after O3d). Rule: two-tier (B.1).
11. E-EVAL tapered + Texel (H-0004/H-0013), SPRT-gated.

## F. DEC-0005 supersession
DEC-0005 -> SUPERSEDED by DEC-0008 ("pseudo-legal move generation + king-safety filter at the
search/perft site"). Filter named by implementation-engineer: capture `us = b.side` before
`make_move`, reject `if (attacked_by(b, b.king_sq[us], b.side))` post-move (== perft.cpp:16).

## G. Round-2 exit verdict
- D-0001 ROUTED (classical-first agreed; GPU gate re-spec).
- D-0002 AGREED (two-tier; kana_o2 delete/quarantine).
- D-0003 ROUTED (single 4-way CI partition; E-PEXT pending).
- D-0004 AGREED (pseudo-legal + filter; DEC-0008).
- D-0005 ROUTED (make/unmake default; E-COPYMAKE deferred with escape).
- D-0006 AGREED (quiescence-first; O3a-O3d split; proxy replaces crossover).

Gate: **OPEN for Milestone 0 only** — no material objection. Milestone 0 is flags+bench+provenance
(behavior-neutral) and must carry the engineer's E-0002 harness corrections (startpos d6 depth,
SetThreadAffinityMask, SHA-256, WMI frequency logging).

## Confidence (revised)
0.78 (from 0.74): upward on three-way runtime confirmation of D-0004 and full AGREED/ROUTED
coverage, but magnitudes (PEXT / copy-make / GPU) remain unmeasured.

## Session update 2026-09-22 (S-0009 — W-0001 + W-0005 step 1, no engine; F-0002 re-block)
- Filed **E-0011** (PENDING): E-0011 self-play data pipeline pre-registration per W-0001
  step 1 — artifact gates (volume/legality/dedup/provenance/resume), DEC-0010 mapping
  (no tier on the dataset; downstream "beats hand-tuned" = Tier R on fresh games under
  E-0012), power reasoning (1,000 games ≈ 120k positions ≳ the Texel need; h(1000)=±23
  Elo ⇒ no Elo gate possible), runjob.py run plan (tools/, ≤2 pairs, pinned evidence).
- Filed **E-0012** (PENDING): E-SPRT-lite contract cited verbatim from DEC-0010 (±2.9444,
  caps 8k/30k/8k, post-cap INCONCLUSIVE, crash=loss, resumable), known-difference live
  validation bands (v1)–(v4), plus the OFFLINE ASN/crossing model validation that
  discharges D-0007's routed W-0005 residual: realized Tier-S crossing on the recorded
  k6 sequence = game 179 (predictions 191/173/133); Tier R and [100,150] undecided at
  240 as predicted; ASN(H1) re-derived 1823.7 / 29179.8 / 291.8 (σ-rounding off
  R-0010's 1822/29159/292 by ≤0.1%).
- Handoffs HO-0003 / HO-0004 route both pre-registrations to adversarial-reviewer;
  both stay PENDING. Gate 0 re-blocked (6th observation, logged).
- Roadmap unchanged; E-0011 unlock order now precise: critique → build → (Gate 0) run.

## Last Updated
2026-09-22
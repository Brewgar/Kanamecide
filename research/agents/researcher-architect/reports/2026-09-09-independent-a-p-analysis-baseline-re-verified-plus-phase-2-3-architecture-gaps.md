---
type: report
author: researcher-architect
created: 2026-09-09
tags: [architecture, search, evaluation, ml, data, performance, methodology, sota, roadmap, a-p-analysis, baseline]
---

# Independent A-P analysis - baseline re-verified plus Phase 2-3 architecture gaps

## Context
Role: researcher-architect (search/eval/architecture roadmap owner). Independent analysis per AGENT_MEGAPROMPT A-P.
Sources read directly this session: all of src/ (defs.h, bitboard.h/cpp, board.h/cpp,
movegen.h/cpp, perft.h/cpp, zobrist.h/cpp, main.cpp), CMakeLists.txt, build.bat, README.md,
research/project_state.md, research/index.md, DEC-0001..DEC-0007, H-0001/H-0003..H-0011,
D-0001..D-0005, E-0001/E-0002/E-00003, F-0001, all four agents profiles+positions,
researcher-architect beliefs.md + 4 prior reports, research.py CLI + templates.
Baseline run THIS session: build/Release/kana.exe -> 10/10 PASS (startpos d1-5 exact,
kiwipete d3 97862, cpw3 d4 43238, cpw4 d4 422333, cpw5 d4 2103487, cpw6 d4 3894594,
"ALL TESTS PASSED"). No src/ edits per assignment.

## Analysis — A. Architecture understanding (demonstrated)

A1. Flow (main.cpp): bitboards_init()+zobrist::init() run TWICE (:35-36 and :82-83;
idempotent, cleanup candidate). Default = 10-case perft suite (:89-154); --moves dumps
startpos list; --fen root split (:56-76) with own post-make filter (:66).
A2. Move (defs.h:38-53): 16-bit [from][to][promo][flag]; no capture/score bits. Phase 2
needs a scored-move wrapper (score array alongside Move; KEEP 16-bit storage).
move_promo() on non-promotion = phantom piece (:52) — invariant+asserts owed.
A3. Board (board.h:7-19): hybrid bitboard+mailbox ~312 B; king_sq[] maintained
(board.cpp:21), relied on by perft/search filter. side/castling/ep/clocks/key across
make/unmake; key restored verbatim on unmake (:201); same_position() (:204-213) audits.
A4. Movegen (movegen.cpp:5-128) is PSEUDO-LEGAL (D-0004, conf 0.85): only EP probe
(:52-63) + castling checks (:107-125) inline; filter is post-make (perft.cpp:16,
main.cpp:66). --moves startpos=20 conceals it (pseudo==legal there). Docs (DEC-0005,
README, project_state, megaprompt) mislabel it — correction owed, behavior correct.
A5. make/unmake (board.cpp:104-202): full Undo; EP removes pawn at ep-/+8 (:123-127);
castling moves rook (:128-133,:185-190); rights cleared on king move + corner from/to
(:139-144); double-push sets ep (:146-148); key XOR maintenance (:150-155,:161).
A6. Zobrist: SplitMix64 deterministic seed, init-once; psq[12][64] (pc-1), castling_[16],
ep_file[8], side_; compute_key() from scratch (:86-93) available as audit. 64-bit keys:
birthday ~4.3B positions/collision — fine for TT+repetition.
A7. Attacks: ray-stepping sliders (deferred magic/PEXT noted :52-53); precomputed
leaper tables; attacked_by() (:95-103) recomputes occ per call — profiling target later.
A8. Build (CMakeLists.txt:16-17): Release forces /Od/JMC/DEBUG — measured 2.1-2.4x NPS
gap (E-00003); correctness flag-independent. kana_o2.exe provenance unknown — excluded.
A9. NOTHING exists yet (all UNKNOWN): alpha-beta/PVS/ID/TT/quiescence/ordering/
aspiration/LMR/NMP/time-control/repetition/50-move/UCI/eval/NNUE/self-play/data/SPRT/
--bench. Every strength claim is UNKNOWN.

## B. Strengths

B1. Perft DEMONSTRATED: fresh 10/10 PASS this session, exact CPW matches.
B2. EP-pin correctness by construction (probe reuses search legality; DEC-0006).
B3. Castling legality inline (rights+vacancy+not-through-check).
B4. Incremental Zobrist + from-scratch recompute for audit.
B5. make/unmake round-trip checkable via same_position(); deterministic seed.
B6. /O2 perft ~43-50 Mnps (E-00003) — search, not movegen, is the Phase-2 lever (H-0008).
B7. Small auditable C++20 core + research-memory discipline (DEC-0007).

## C. Weaknesses (severity/confidence)

C1. No search/eval/UCI — CRITICAL, demonstrated (strength 0 Elo, cannot play).
C2. Release /Od flags — HIGH (2.1-2.4x NPS left; conf 0.9). Fix E-0002.
C3. Pseudo-legal mislabeled "legal" — MEDIUM (misleads Phase-2 consumers; conf 0.85).
Fix via D-0004 (docs+contract, no behavior change).
C4. No move ordering — HIGH for future search (unordered AB→minimax; H-0008, 0.7).
C5. Ray-stepping sliders — MEDIUM (bounded 1.3-2.5x H-0006/0.6, not >=3x).
C6. Per-call ~312 B Board copy in generate_moves (:6) — LOW-MEDIUM (H-0007, >=10%, 0.65).
C7. 16-bit Move lacks score/capture bits — MEDIUM ergonomics (wrapper needed; 0.8).
C8. No TT/quiescence/repetition/time-control — HIGH once search lands (0.8).
C9. Key restored verbatim on unmake, no incremental-undo audit test — LOW (add assert).
C10. Double-init + memset-Board in harness — TRIVIAL cleanup.

## Arguments For (roadmap: E-0002 → O3 plain-AB+ordering+quiescence+ID+UCI → PVS/TT deltas → eval → SPRT/data → NNUE)

1. Baseline DEMONSTRATED (10/10 PASS this session) — Phase 1 closed, Phase 2 unblocked.
2. E-00003 measured the flag gap (2.1-2.4x) and the /O2 throughput (~47 Mnps): E-0002 is a
free, hours-long win gating every perf claim.
3. Ordering compounds with depth (sqrt(b) mechanism, H-0008); NPS work is flat — order the
experiments accordingly.
4. PVS+TT confounded unless added as separate deltas after ordering (H-0009 design).
5. SPRT-before-claims (H-0010) is the only trustworthy promotion rule (Stockfish/LC0 norm).
6. Eval sequencing material → tapered-linear+Texel → NNUE isolates each gain (F-0001).

## Arguments Against (strongest counters to my roadmap)

1. GPU-idle critique: RTX 5070 Ti sits unused through Phase 2 while classical search is
built. Counter: MCTS-without-net is circular (needs policy/value → needs games → needs a
playing engine); batch=1 NNUE latency rarely pays vs 45 Mnps CPU. GPU work starts with
training (Phase 3), not search.
2. Ordering-first could flop with material-only eval (unstable PV weakens killers/history
until H-0004 eval exists). Mitigation: MVV-LVA alone is eval-independent; stage the deltas.
3. PEXT/copy-make micro-opts could precede search (simpler, fewer files). Counter: flat
constant-factor NPS gains << compounding ordering gains (H-0008 mechanism); E-0002 flags
dominate both.
4. Hand-tuned eval may plateau far below 2500 (H-0004 is 0.6 aspirational). Mitigation:
H-0004 success is correlation+SPRT vs material-only, not the bare number; NNUE follows.
5. All prior A–P work by this same role risks self-confirmation. Mitigation: this report
re-verified the baseline independently, cites only demonstrated/testable items, and invites
adversarial-reviewer falsification bars on H-0009/H-0004.

## Assumptions (and how each is tested)

1. Alpha-beta+ordering literature transfers to this movegen (H-0008) — tested by O3 deltas.
2. /O2 E-00003 throughput (~47 Mnps) predicts search NPS regime — tested by E-0002 bench.
3. Material-only O3 beats random at fixed nodes (H-0003 gate) — tested by first SPRT.
4. Texel on quiet labels transfers to play (H-0004) — tested by holdout + SPRT.
5. Make/unmake stays optimal until E-COPYMAKE says otherwise (H-0011/D-0005) — tested.
6. 64-bit Zobrist uniformity (SplitMix64) — collision audit + TT corruption watch.

## Evidence

- Fresh run: build/Release/kana.exe → 10/10 PASS, ALL TESTS PASSED (this session).
- E-00003 table: /O2 47.0-47.4 (startpos d5), 43.1 (kiwipete d4), 50.0-50.4 (cpw6 d4);
  /Od ~19-21; ratios 2.23-2.37x; counts bit-identical.
- Code facts: movegen pseudo-legal (movegen.cpp branches + perft.cpp:16 + main.cpp:66);
  /Od flags (CMakeLists.txt:16-17); 16-bit Move (defs.h:38-53); ~312 B Board (board.h).
- Records: DEC-0001..07, H-0003..H-0011 (H-0001 example-only), D-0001..D-0005 (D-0001
  example-seeded + real addendum), E-0001 (example) / E-0002 (pending) / E-00003 (done).

## Evidence
...

## Confidence

0.74. Perft-correctness DEMONSTRATED (fresh run). Classical-first strongly supported by
literature + circular-dependency argument (H-0003, 0.75). Flag gap MEASURED (0.9).
Ordering-dominance likely by theory (H-0008, 0.7). PEXT/copy-make/eval magnitudes plausible
only (0.45-0.65) — all gated on E-0002/E-PEXT/O3 measurement.

## Recommendation (prioritized; immediate → near-term → long-term → speculative)

Immediate: E-0002 bench+/O2 (hours); D-0004 contract correction (--legality audit, DEC-0005
revision, README/project_state wording; no behavior change); scored-move wrapper invariant
docs + phantom-move asserts.
Near-term: O3 plain-AB + staged ordering + quiescence + ID + UCI + repetition/time (first
strength number); PVS-only/TT-only deltas (H-0009); E-PEXT (H-0006/D-0003); E-MGCOPY
(H-0007); E-SPRT harness (H-0010); E-EVAL tapered+Texel (H-0004); E-COPYMAKE (H-0011/D-0005).
Long-term: NNUE value net + VNNI inference; GPU PUCT prototype vs O3; hybrid search; SPSA
at scale; book + Syzygy.
Speculative: value-of-computation search; uncertainty-aware time/data; collective-velocity
as meta-objective. Judge all by Elo + nodes/sec, never by elegance.

## Recommendation
...

## References

- src/: defs.h:38-53; bitboard.cpp:52-72; board.h:7-19; board.cpp:86-213; movegen.cpp:5-128;
  perft.cpp:7-21; zobrist.cpp:11-29; main.cpp:31-158; CMakeLists.txt:16-17.
- research/: project_state.md; index.md; DEC-0001..DEC-0007; H-0003..H-0011 (+H-0001 EXAMPLE);
  D-0001..D-0005; E-0002 (pending), E-00003 (completed), E-0001 (EXAMPLE); F-0001 (EXAMPLE).
- Prior architect reports (4x 2026-09-09, retained as history; this report re-verifies).
- SOTA principles: Stockfish (PVS+TT+LMR+NNUE+SPRT deltas); LC0/AlphaZero (policy+value,
  PUCT, data flywheel); Ethereal (honest classical intermediate). No copying — adopt the
  measurement discipline + sequencing, then test deviations.

---

## D–P gap register (new in this report vs 4 priors; filed below as H/D)

D-NEW1. King-capture pseudo-moves + phantom move_promo need invariant docs + debug asserts
before any search fast path (filing H-0012).
D-NEW2. Halfmove/EP-key/castling-rights edge paths lack unit tests despite perft passing
(perft counts moves, not clocks/keys) — filing H-0014 (state-integrity audit harness).
G-NEW. Tapered mg/eg interpolation + Texel holdout protocol unspecified in H-0004 —
filing H-0013 to pin the eval design before implementation.
E-NEW. Quiescence stand-pat + delta-pruning margin + check-extension policy unscoped —
filing D-0006 debate (quiescence-first vs PVS-first inside O3).
P-NEW. Learned time-management / value-of-computation as the long-term allocator —
filing H-0015 (speculative, lowest priority, needs eval variance first).
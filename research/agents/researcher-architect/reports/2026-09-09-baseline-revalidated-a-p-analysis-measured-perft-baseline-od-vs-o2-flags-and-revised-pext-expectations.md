---
type: report
author: researcher-architect
created: 2026-09-09
tags: [baseline, perft, nps, build-flags, pext, search, a-p-analysis, roadmap]
---

# Baseline-Revalidated A-P Analysis: measured perft baseline, /Od-vs-/O2 flags, and revised PEXT expectations

## Context

Role: **researcher-architect** (search/evaluation/architecture roadmap). This report
re-validates the baseline by running it myself, measures perft NPS at fixed flags, and
revises the two prior reports (`2026-09-09-a-p-analysis-*`, `2026-09-09-independent-baseline-*`)
wherever they contain unmeasured magnitudes. The prior session could NOT run the binary
(broken shell integration); I could, so everything I measured is upgraded from UNKNOWN.

**Fresh facts established this session (2026-09-09):**

| # | Fact | How established |
|---|---|---|
| F1 | Perft suite 10/10 PASS, exact counts (startpos d1-5: 20/400/8902/197281/4865609; kiwipete d3: 97862; cpw3/4/5/6 d4: 43238/422333/2103487/3894594) | `kana.exe` (as shipped) run |
| F2 | `--moves` prints 20 legal startpos moves, piece-type gen order | `kana.exe --moves` |
| F3 | `--fen kiwipete d3`: 48 roots, split total 97,862 | `kana.exe --fen ... 3` |
| F4 | Ship Release builds `/Od /Zi /EHsc /JMC` + `/DEBUG` (CMakeLists.txt:16-17); kana.exe = 83,968 B; kana_o2.exe = 253,952 B (provenance unrecorded) | source + file sizes |
| F5 | Scratch `/O2` rebuild (identical src/, MSVC 19.51, VS18) perft NPS: startpos d5 ~47.0-47.4 Mnps (3 reps); kiwipete d4 ~43.1 Mnps; cpw6 d4 ~50.0-50.4 Mnps; nodes exact | external harness (%TEMP%\kana_bench); repo src/ untouched |
| F6 | Scratch `/Od` rebuild same code: startpos d5 ~20.7 Mnps; kiwipete d4 ~19.2 Mnps; cpw6 d4 ~21.1 Mnps; nodes identical | same harness |
| F7 | `/Od -> /O2` perft-NPS ratio ~2.1-2.4x; perft correctness flag-independent | F5 vs F6 |

**Key implication:** the legal move generator is already a ~45-50 Mnps (perft) generator at
`/O2` on this Zen 5 CPU. The "/Od destroys perf" concern is directionally correct but the
magnitude is ~2.3x, not catastrophic. A `>=3x` PEXT/magic speedup (H-0005, prior conf 0.7)
would require ~>140 Mnps from a faster slave-attack function — implausible; literature
PEXT-vs-ray gains on perft-only workloads are typically 1.2-2.5x. H-0005 is revised; see
H-0006/D-0003.

---

## A. Complete architecture understanding (code read + run)

A1. `defs.h` — `Move = uint16_t`: `[0..5]=from, [6..11]=to, [12..13]=promo offset (N=0..Q=3)`,
`[14..15]=flag (NORMAL/PROMOTION/EN_PASSANT/CASTLING)`. No capture/double-push/score bits.
`move_promo` meaningful only when `flag==PROMOTION`. `Board` (`board.h`) = `pieces[2][6]` +
`occ[2]` + `mailbox[64]` + `king_sq[2]` + `side/castling/ep/halfmove/fullmove/key` (~312 B).

A2. `bitboard.cpp` — precomputed knight/king/pawn attacks; sliders = naive ray stepping
(bitboard.cpp:54-72), explicitly deferred magic/PEXT. `queen_attacks = rook|bishop`.

A3. `board.cpp` — `set_fen` (lenient 6-field parser), `set_startpos`, incremental
`add_piece/remove_piece` (bitboards+mailbox+key+king_sq), `compute_key` full recompute,
`attacked_by` (tables + rays vs occupancy), `make_move/unmake_move` with `Undo{captured,
capt_sq, ep_prev, castling_prev, halfmove_prev, key_prev}`. EP square, castling-rights and
`side_` key xor are consistent with `compute_key`. `halfmove/fullmove` maintained, unused.

A4. `movegen.cpp` — **legal** movegen: pawns (single/double/promo x4/captures; EP via
make/unmake probe on a copied board `b_nc`), pieces by table/ray `& ~own`, king, castling
(rights + occupancy + not-through-check). **No ordering**; enum order pawns->knights->bishops
->rooks->queens->king->castling.

A5. `perft.cpp` — perft with legality = `make` + `attacked_by(own king)` + `unmake`.
`main.cpp` = harness: perft suite, `--moves`, `--fen <FEN> [depth]` split. No timing.

A6. **Not implemented:** search, evaluation, TT, quiescence, move ordering, UCI, threading,
tablebases, NNUE, self-play, training, SPRT (absences confirmed; project_state.md accurate).

---

## B. Strengths (demonstrated / strongly supported)

B1. **Correctness bedrock is real.** 10/10 perft PASS freshly rerun (F1), identical between
`/Od` and `/O2` (F7). Legal movegen + make/unmake + incremental Zobrist is a sound Phase-1
foundation; DEC-0001..0006 choices are conventional and defensible.

B2. **Measured perft speed is competitive-class.** ~43-50 Mnps at `/O2` (F5) sits at/above
the perft NPS commonly quoted for strong open-source engines on similar CPUs. Phase 2 starts
from a fast leaf mover, not a slow one.

B3. **Clean, small, auditable codebase.** ~600 lines of C++20; no premature magic; explicit
comments marking the PEXT milestone; easy for the collective to instrument.

B4. **Deterministic incremental Zobrist** (fixed seed) — safe for TT/repetition; `key`
consistent with `compute_key`.

B5. **Hardware headroom is real.** Zen 5 (PEXT, AVX-512 VNNI/BF16) + RTX 5070 Ti 16 GB =
fast single-thread CPU path now, real GPU path later.

## C. Weaknesses (severity / confidence / impact)

C1. [HIGH, demonstrated] **Release ships debug codegen.** `/Od /Zi /EHsc /JMC` + `/DEBUG`
costs measured ~2.3x perft NPS (F6/F7). Any NPS/speedup claim vs the shipped binary conflates
compiler with algorithm (D-0002). Fix = Release -> `/O2` (+ optional `/GL`/LTO/`arch:AVX512`),
keep Debug at `/Od`. E-0002 specifies this.

C2. [HIGH, by inspection] **No move ordering.** Alpha-beta/PVS without MVV-LVA/killers/history
degrades toward minimax: node counts explode. Single largest *structural* gap to a playable
Phase 2 engine. Fix before PEXT or NNUE.

C3. [HIGH] **No search at all.** ID/TT/quiescence/aspiration/time mgmt/UCI are the Phase 2
deliverable. Strength/Elo/SOTA are unmeasurable until `perft` becomes "search".

C4. [MEDIUM, demonstrated] **Per-call `Board` copy in `generate_moves`** (`movegen.cpp:6`,
`Board b_nc = b_in;` copies ~312 B every call, even with no EP). Not fatal (F5) but it is
waste in the single hottest function; H-0007 files the testable >=10% claim.

C5. [MEDIUM, by inspection] **Ray-stepping sliders** remain the slowest attack primitive
(called from `attacked_by` and movegen). Class evidence says magic/PEXT faster; magnitude on
THIS engine is bounded by the 47 Mnps baseline (H-0006/D-0003). NOT the Phase 2 bottleneck.

C6. [LOW-MEDIUM] **16-bit `Move`** has no score/capture bits. Fine with a parallel scores
array; revisit before committing search code generation-wide (N2).

C7. [MEDIUM] **No evaluation function** — nothing to search toward. Material-only eval is
Phase 3 work per H-0004 (preserves search-vs-eval attribution).

C8. [MEDIUM] **No bench/SPRT/match infrastructure** in-repo. Every later "improvement" claim
is unfalsifiable without it (K). E-0002 (bench) and E-0004-design (SPRT) land before any
search claim.

---

## D. Correctness risks and the tests that would catch them

D1. [LOW, latent] **`move_promo` is defined for every move** and returns `KNIGHT` when
`flag==NORMAL` (bits 12-13 = 0). Not a current bug (`make_move` only uses it in the PROMOTION
branch) but any future caller reading it unguarded gets a phantom knight. *Test:* assert
`flag==PROMOTION` wherever `move_promo` is consumed; unit-test the accessor.

D2. [LOW] **`set_fen` does not validate** rank/file overflow, king presence, or EP bounds;
kingless FENs leave `king_sq` stale so `attacked_by`/`in_check` go silently wrong. Perft
PASS does NOT prove FEN robustness (suite avoids these inputs). *Test:* malformed-FEN suite
(9/..., kingless, bad EP) must throw; assert both kings + king_sq consistency post-`set_fen`.

D3. [LOW] **`same_position`** is a full-board equality oracle — use it as the make/unmake
round-trip test: random-play N make/unmake cycles asserting board+key restoration. Cheap,
high-value guard before search.

D4. [UNKNOWN] **EP/pin coverage is thin** beyond CPW3. The make/unmake probe is principled
(DEC-0006) but the test set is small. *Test:* extend perft with more EP/pin positions before
search relies on legal movegen for correctness.

D5. [MEDIUM] **UCI input handling absent.** Future UCI must generate -> validate -> reply
`Illegal move` (never trust the GUI), with pondering off in v1.

Standing suite: existing perft + make/unmake round-trip fuzz + FEN validation + fixed-flag
perf regression with binary-hash logging (E-0002).

---

## E. Search: weaknesses and opportunities

E1. **Plain alpha-beta first, as the controlled baseline** — with MVV-LVA + 2 killers +
history + quiescence + ID. Then PVS, then TT as *measured deltas* (E-0001/H-0001 framing).
Do not pre-add TT+PVS: attribution of each gain requires steps.

E2. **Move ordering is the highest-leverage search feature** (~100-300 lines) and typically
dominates any bitboard micro-op in node counts. Before touching PEXT.

E3. **TT design:** 64-bit keys, bucket-3/4 with age stamps, EXACT/LOWER/UPPER bounds,
PV-move cache. Start 1-bucket, measure, widen. Never trust a TT cut on unknown-aging entries.

E4. **Quiescence:** captures + promotions + king evasions, MVV-LVA order, delta pruning on a
material-only eval. No SEE in v1 (revisit when eval exists).

E5. **Time management/UCI:** `movetime` first, then `wtime/btime` with overhead buffer; no
pondering in v1.

E6. **Metric discipline:** perft NPS (F5) overstates search NPS (no eval/TT in perft). Report
BOTH "time-to-depth on a fixed 200-position set" and "fixed-node match strength"; perft NPS
alone is not a Phase 2 KPI.

## F. Mathematics: weaknesses and opportunities

F1. **No evaluation mathematics exists.** Need tapered material + PST + king safety + pawn
structure, then Tunable weights via Texel/SPSA on quiet labeled positions (H-0004). The math
gap is evaluation-model selection + weight tuning, not search math.

F2. **Search-complexity model sets expectations (speculative until measured).** With
effective branching ~30-35 and good ordering, alpha-beta nodes ~ 2*b^(d/2); at /O2 search
NPS plausibly ~10-20 Mnps => depth ~10-12 on startpos within seconds-to-tens-of-seconds once
TT+ordering land. Testable Phase 2 gate: "depth >= 10 startpos in < 10 s at /O2".

F3. **Correction to prior session numbers.** Prior reports' "6 Mnps, 15-30% TT savings,
3-8x PEXT, 2500 Elo" were UNMEASURED; the only measured NPS now are F5/F6. Treat those prior
magnitudes as hypotheses; H-0003/H-0004/H-0005 carry the revised criteria.

F4. **Zobrist collision math:** 64-bit keys, birthday bound ~4e9 stored positions — fine for a
TT. Record hit/miss and collision policy in search experiments.

---

## G. Evaluation: weaknesses and requirements

G1. **Nothing to evaluate yet** (no eval function, no search). Prerequisite order:
search (E1-E5) -> material-only eval -> Texel-tuned linear eval (H-0004) -> NNUE (Phase 3+).

G2. **Hand-tuned eval baseline must be measured before NNUE** (F-0001 sequencing lesson).
Target correlation >0.95 (Stockfish-labeled quiet holdout) + SPRT-vs-material-only + NPS with
eval, before any neural work is justified.

G3. **NNUE requirements (Phase 3+, not now):** HalfKP-style input (410 features, own/opp)
with the "king bucket + occupancy nibbles" layout; 2-4 hidden layers x ~256; incremental
inference; CPU VNNI path for batch=1 (Zen 5) vs GPU path for large batch. Everything below
is speculative until a trained net exists.

---

## H. ML/training design gaps (what should be built and why)

H1. **Missing pipeline:** rollout/self-play generator -> PGN/position database -> torch training
loop -> quantized export -> in-engine inference -> Elo loop. None exists; `project_state.md`
says the same ("Current Training Pipeline: None").

H2. **Start value-only or policy+value?** Literature is split (Stockfish value-only vs
AlphaZero p+v). Decision deferred to after the hand-tuned baseline: p+v is harder to train and
sample-hungry; value-only aligns with a classical search backbone. Hypothesis to test later,
not now.

H3. **Why build it at all:** a trained value is the strongest known eval source; a trained
policy gives ordering; self-play closes the data loop. But none of this matters before a
search-backed engine can generate games (H-0003).

---

## I. Data/self-play requirements

I1. **Data today:** only the perft suite (positions, no game data). Sufficient for Phase 1-2
correctness; insufficient for tuning/eval.

I2. **Phase 3 data plan:** (a) quiet-position labels from a strong external engine (Stockfish)
for Texel tuning (~50k positions); (b) self-play games at fixed nodes with openings diversified
by TT+noise; store FEN+result+ply; (c) separate train/holdout by game, never by position only.

I3. **Quality gates:** holdout correlation + MAE for eval; fixed-node SPRT for strength; game
legal-rate 100%; crash/stall count = 0 over 1000 games.

## J. CPU/GPU/performance opportunities (with measured baselines)

J1. **Immediate, demonstrated: fix Release flags (`/O2`).** Measured 2.1-2.4x perft-NPS gain
(F5-F7) at zero code risk. Do this first (E-0002); it changes every downstream benchmark.

J2. **Profile before micro-optimizing.** Candidates in order of prior likelihood: (a) the
`Board b_nc = b_in;` copy in `generate_moves` (H-0007), (b) slider rays (PEXT/magic,
H-0006), (c) mailbox/occupancy maintenance in make/unmake, (d) `attacked_by` in the perft
legality check. Perft NPS is the wrong target; search-node NPS and time-to-depth drive
strength (E6).

J3. **Search-level levers dominate NPS levers:** move ordering, TT, quiescence, ID/PV reuse
reduce node counts by ORDERS OF MAGNITUDE vs any bitboard tweak. Budget accordingly.

J4. **CPU NNUE path (Zen 5):** AVX-512 VNNI + BF16 for batch=1 inference is the most
interesting "GPU is not needed for eval" option (Stockfish NNUE ships AVX512 VNNI). Batch=1
latency curves (CPU vs 5070 Ti) are a Phase 3+ prerequisite before any GPU-MCTS decision
(D-0001).

J5. **Multi-threading:** Lazy SMP / ABDADA-style for search once single-thread is measured;
8C/16T gives a real scaling target but only after the sequential engine is stable and SPRT
exists.

---

## K. Research-methodology weaknesses

K1. **Prior session published unmeasured magnitudes** (Mnps, %TT-savings, x-speedups, Elo
ranges, week commitments) into reports/positions. Fixed by F3 revisions and this report's
fact table; H-0003/4/5 now carry falsifiable criteria instead.

K2. **No SPRT/statistical gate exists.** Any two-engine comparison ("A beats B") will be
noise until fixed-node (or fixed-time) SPRT at alpha=beta=0.05, min ~200 games, multiple
opening sets, is the collective standard. Build it in Phase 2 (before the first "improvement"
claim).

K3. **Benchmark hygiene:** log compiler flags + git hash + binary hash + CPU + reps with
every NPS number (E-0002 design). kana_o2.exe (253,952 B) is currently un-datable — exclude
from claims (D-0002).

K4. **Perft-PASS != robust.** Correctness claims must be scoped to the tested position set
(D2, D4). The collective should maintain an extended perft/EP corpus.

K5. **Calibration language discipline** (demonstrated/strongly supported/likely/plausible/
speculative/unknown) is now the house standard; this report follows it.

---

## L. Comparison to state of the art

L1. **Perft NPS:** measured ~43-50 Mnps at /O2 is at/above the commonly reported range for
strong open-source engines (Stockfish-class) on similar CPUs — BUT perft NPS is a weak proxy
for strength. Claim: "competitive move generator", NOT "competitive engine".

L2. **Strength:** no playing strength exists (no search/eval). Nearest meaningful peers are
hobby engines at Phase 1. Published CPU-engine ceilings (Stockfish ~3600 CCRL, peer engines
~2500-3000 with tuned eval + PVS/TT) are OUT OF REACH until Phases 2-3 complete; a realistic
first milestone is "beats a random mover decisively at fixed nodes", then ">= expert amateur"
on a test suite.

L3. **NNUE/MCTS SOTA:** Leela/Lc0 (~3200) on GPU MCTS and Stockfish-NNUE (~3400+ on CPU)
both require trained nets + large compute. On this hardware the *feasible* order is
clearly: classical CPU search -> tuned linear eval -> NNUE value (+later MCTS only if batch
economics justify it, D-0001). GPU-MCTS now would be circular (no net -> no games -> no net).

L4. **Tablebases**: none; endgame tables are a Phase 4+ option after SPRT exists.

---

## M. Potentially novel opportunities (none are commitments)

M1. **Hybrid classical+learned:** classical PVS backbone with a *small* trained policy for
ordering and a value head for leaves — ablatable in SPRT, keeps depth, adds learning. Best
risk-adjusted novelty. (Speculative; needs Phases 2-3 first.)

M2. **Uncertainty-driven search allocation:** use eval variance/instability (across ID
depths or TT bounds) to widen narrow windows only where needed. (Speculative; no literature
consensus; cheap to prototype once search exists.)

M3. **CPU-first NNUE on Zen 5 VNNI** as the default eval path (GPU idle for phase-3 eval) —
counter-consensus vs the "GPU MCTS everywhere" narrative, and cheap to test. (Plausible.)

M4. **Discovery-rate instrumentation over the collective itself** (meta): track
hypotheses->experiments->belief-updates per week as the collective's own KPI. (Unknown; the
experiment is whether it accelerates the loop.)

## N. What I would redesign from scratch (and what I would keep)

N1. **Keep**: bitboard+mailbox hybrid, incremental Zobrist, make/unmake, legal-movegen
*reference* generator, perft suite, C++20. All are conventional and now measured-fast at /O2.
"Do not discard" is strongly supported; these are not the bottleneck.

N2. **Redesign**: the hot-path move generator for search — keep the legal generator as the
correctness oracle, but add a pseudo-legal + fast-legality path (DEC-0005 reversal condition)
with ordering produced during generation (MVV-LVA etc.). Plan a 32-bit move/score interface
before search code is written to avoid a mid-phase churn.

N3. **Redesign**: `generate_moves` signature to accept a caller-owned scratch board for the EP
probe (kills the 312-byte per-call copy; H-0007).

N4. **Redesign**: build/bench tooling — Release=/O2 (+LTO/arch), a `--bench`/`bench` target,
binary-hash logging, and a fixed 200-position time-to-depth suite from day one (E-0002).

N5. **If I lost everything today**: same Phase 1 stack (it is the right size), PLUS magic/PEXT
sliders from the start (not ray-stepping), PLUS bench/SPRT scaffolding with the first search
commit. Nothing in the current design justifies a ground-up rewrite.

---

## O. Highest-priority experiments (the 3 to run first)

**O1 — E-0002 (in-tree bench + /O2 baseline).** Add `--bench [reps]` to main.cpp (does not
change src semantics), fix Release flags to /O2 (/GL/LTO/arch:AVX512 optional), log flags +
git hash + binary hash, 5 reps per position, record NPS. Expected: reproduce F5-F7 in-tree
(~2.1-2.4x /Od-vs-O2; ~45-50 Mnps at /O2). Blocks ALL downstream perf claims. Cost: hours.

**O2 — E-PEXT (H-0006 vs H-0005).** Swap `rook_attacks`/`bishop_attacks` to PEXT/magic;
perft suite must stay bit-identical; re-run O1 bench. Expected if H-0006 (conf 0.6): 1.2-2.5x
perft-NPS gain; H-0005's >=3x (conf 0.45 after revision) is the falsification bar. Cost: days.
Do NOT do this before O1, and do NOT do it before the search stack if effort is scarce (J3).

**O3 — plain alpha-beta search stack + UCI (E-0001 design, real E record).** Alpha-beta +
MVV-LVA + killers + history + quiescence + ID on material-only eval; fixed-node SPRT vs
random, time-to-depth on startpos (target d>=10 in <10 s at /O2, H-0003 criteria), 1000
games crash/stall = 0. Cost: 1-2 weeks. This is the first *strength* measurement the project
has ever had; everything (eval, SPRT, self-play, NNUE) hangs off it.

O4+. SPRT harness (parallel O3) -> hand-tuned eval + Texel (H-0004) -> self-play v1 -> NNUE v1
-> VNNI CPU vs GPU latency curves (D-0001 resolution input).

---

## P. Highest-upside long-term research directions

P1. **Hybrid classical + learned** (M1): keep the PVS backbone, add a small policy/value NNUE
as an ablatable module once eval+nets exist. Highest risk-adjusted upside.
P2. **Closed self-play loop** with Elo/week (or SPRT-strength/week) as the collective KPI;
funds every other direction with real data.
P3. **Consumer-hardware economics first** (P3): measure batch=1 CPU-VNNI vs GPU latency and
$/Elo before any MCTS commitment; the 5070 Ti may end up a training-only device.
P4. **Uncertainty/instability-aware search** (M2): dynamic widening where eval variance is
high; speculative but cheap to prototype after O3.
P5. **Meta:** discovery-rate instrumentation (M4) — treat the collective itself as a system
to optimize.

---

## Confidence calibration

- Perft correctness: **demonstrated** (fresh run, F1/F3).
- `/Od` flags + kana.o2 provenance: **demonstrated** (F4).
- Perft NPS ~43-50 Mnps at /O2, ~19-21 at /Od, ratio ~2.1-2.4x: **demonstrated on this
  machine** (F5-F7; single machine, 1-3 reps, unpinned).
- Move-ordering-is-the-P2-bottleneck: **strongly supported** (theory + all-engine practice;
  not measured here).
- PEXT >=3x: revised DOWN to conf ~0.45 (implausible vs measured baseline); PEXT 1.2-2.5x:
  conf 0.6 (H-0006/D-0003).
- Alpha-beta/PVS reaches strength milestones (H-0003): conf 0.75, **likely** — literature,
  not measured here.
- Hand-tuned eval 2500+ (H-0004): conf 0.6, **plausible** (aspiration, not claim).
- GPU-MCTS-on-5070Ti leapfrog: **speculative** until batch curves + net exist.
- What changes my mind: O1 numbers diverging >20% from F5; O3 failing criteria; a
  same-hardware MCTS+NNUE prototype out-SPRTing O3; TT/PVS deltas much larger than the
  literature range.

## Files created / updated by this report

- NEW immutable report (this file).
- `current_position.md` — revised with fresh facts (next edit).
- H-0006 (PEXT 1.2-2.5x), H-0007 (Board-copy >=10%), D-0003 (PEXT magnitude), E-00003
  (scratch /Od-vs-/O2 baseline, COMPLETED) — new records via CLI scaffold.
- H-0005 — revised expectation + confidence (>=3x -> 1.2-2.5x plausible) with measurement note.
- D-0002 — measured /Od-vs-/O2 ratio appended as evidence.
- `project_state.md` — performance facts section updated (fresh perft re-verification + NPS).
- No `src/` edits (per instructions); measurements used an external scratch harness.

## References

- This session's raw data: `%TEMP%\kana_bench\run_o2.log`, `run_od.log`; repo `_tmp_*.log`
  cleaned after this report.
- Chess Programming Wiki perft suite (in-repo `src/main.cpp:89-154`).
- Prior reports: `2026-09-09-a-p-analysis-*`, `2026-09-09-independent-baseline-*`.
- Records: H-0003/4/5/6/7, D-0001/2/3, E-0001/2/3, F-0001, R-0001, DEC-0001..7.
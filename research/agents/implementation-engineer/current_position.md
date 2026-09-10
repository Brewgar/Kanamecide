---
type: current_position
agent: implementation-engineer
confidence: 0.76
focus: "Phase 2 search implementation; correctness/perft-hazard audit; E-0002 harness spec"
last_updated: 2026-09-10
---

# Current Position — implementation-engineer

> Prior state: Round-1 placeholder. Round-2 was my first entry (2026-09-10). Round-3 entries below.

## Round 3 — O3a executed (2026-09-11)

**Delivered:** `src/search.{h,cpp}` (plain negamax + alpha-beta, material-only eval
100/320/330/500/900/20000 cp, DEC-0008 filter, H-0012 debug assert, checkmate/stalemate
handling) + minimal UCI (`uci/isready/ucinewgame/position/go depth N/stop/quit`) in the
existing harness. Detail: `reports/2026-09-11-o3a-plain-ab-completion-report.md`.

**First strength number (E-00006, PASS):** depth-4 engine 29-0-1 (**96.7%**) vs
legal-move-uniform random over 30 balanced games; **100% legal-game rate (30/30)**;
perft 10/10 bit-identical (Release + asserts-live audit build). **O3b unblocked.**

**Bugs found and fixed:** (1) beta-cut `break` before `unmake_move` → board corruption +
hang (unmake now precedes the cut); (2) `search.h` missing `using namespace kana` +
`movegen.h` include; (3) `uint64_t &= bool` C4805; (4) missing `<iostream>`.

**Environment:** Device Guard blocks ALL `/DEBUG` exes here — validated asserts in an
/O2-without-NDEBUG scratch build instead (perft + audit all green); recommend a proper
asserts-enabled config in O3b.

**Untouched:** ordering (O3b), quiescence (O3c), TT/ID/time (O3d), PEXT, eval tuning.

---

## Round 3 — Milestone 0 / E-0002 executed (2026-09-10)

**Delivered (commit `300bdeb`):** per-config flags (Release `/O2 /GL /arch:AVX512 /DNDEBUG`
+ `/LTCG`; Debug `/Od` + asserts live) — `/Od` was unconditional before; certified bench
`--bench [reps]` (`src/bench.{h,cpp}`: startpos d5/d6, kiwipete d3/d4, cpw6 d4; 5 reps;
`SetThreadAffinityMask` pinning; WMI clock **proxy labeled as proxy**; self-SHA-256 + git
hash on every run); `kana_o2.exe` quarantined as `kana_o2.exe.QUARANTINED-D0002`; double
init removed; **H-0012/H-0014 guardrails landed debug-only** (enemy-king-capture assert in
`make_move`, `move_promo` flag asserts at both read sites, `--audit` state walk) — landed,
not dropped.

**Measured / certified:** /O2 = startpos d5 **44.28** / d6 **42.25** / kiwipete d3 **43.71**
/ d4 **42.69** / cpw6 d4 **45.47** Mnps (5 reps, pinned, SHA-256 `a4c6b168…`). Pre-registered
±10% rule vs E-00003: all four comparable positions within window (-1.0% to -9.8%) →
**baseline CERTIFIED, O3 gate OPEN**. Same-session control (identical src, plain /O2) =
46.34/43.60; lower-load repeat = 46.97 (d5) — background load (PUBG et al.) explains the
shortfall; honest certified range **43-47 Mnps at /O2** (~2.1x over the pre-M0 /Od build).

**Correctness (sacred):** perft 10/10 PASS bit-identical in Release AND Debug-with-asserts;
H-0014 state audit PASSED (zero fires; audit walk == perft exactly, 197,281 + 97,862 +
2,812 nodes); pinned-rook repro unchanged (16 vs 9 — DEC-0008 honored, zero behavior change).

**Untouched:** movegen/search logic; O3/E-00005/E-PEXT/E-00004; `build_o2/` + root
`bench.cpp` (Round-2 evidence); reviewer's matrix column; README/`--legality`/dump_moves
relabel (Milestone 1). Full detail:
`reports/2026-09-10-milestone-0-e-0002-completion-report.md`.

**Next (Round-3 order):** O3a (plain AB + material eval, DEC-0008 filter at the search
site) — unblocked by this certification.

---

## Round 2 — First Entry (2026-09-10)

### Independent verification (Round2 §6.2 — reproduced, not inherited)

- **Perft 10/10 PASS — VERIFIED.** Rebuilt `build\Release\kana.exe` and ran it: startpos d1–5 = 20/400/8902/197281/4865609, kiwipete d3 = 97,862, cpw_pos3 = 43,238, cpw_pos4 = 422,333, cpw_pos5 = 2,103,487, cpw_pos6 = 3,894,594 — all exact; `=== ALL TESTS PASSED`.
- **Pseudo-legal vs legal — VERIFIED.** `kana.exe --fen "7k/8/8/8/8/8/8/r3R2K w - - 0 1" 1` → `9 nodes at depth 1` (legal, filtered) vs `16 legal moves:` (pseudo-legal). `dump_moves` (main.cpp:11–17) prints "N legal moves" for a list that is *pseudo-legal*: the 7 moves e1e2…e1e8 expose the h1 king to the a1 rook. The mislabel is live in the shipped binary today.
- **/O2 vs /Od gap (~2.3×, E-00003) — strongly supported / reproduced**, not re-measured by me: there is no in-tree `--bench` (main.cpp), and my mandate forbids `src/` edits. Provenance confirmed: `bench.cpp` + `build_o2/` are the E-00003 scratch harness; `build_o2/Release/kana.exe` is 74,240 B, but `build/Release/kana_o2.exe` is 253,952 B — a *third* binary with unrecorded provenance (D-0002). Exclude-or-document it.

### A–P assessment (implementation-engineer lens)

**A. Architecture.** ~312 B `Board` (pieces[2][6] bitboards + occ[2] + mailbox[64] + king_sq[2] + side/castling/ep/halfmove/fullmove/key). make/unmake with `Undo`; incremental Zobrist seeded by a deterministic SplitMix64 — keys ARE reproducible across runs (good for deterministic TT/collision tests). Slides are naive ray loops (bitboard.cpp:54–72). perft recurses with the king-safety filter `!attacked_by(b, king_sq[us], b.side)` applied once per move (perft.cpp:16).

**B. Strengths.** (1) An external oracle (CPW perft) pins the movegen/board core — the only part of the engine I can independently prove correct today. (2) make/unmake + `same_position` + deterministic Zobrist are exactly the primitives search/TT/repetition need. (3) Idempotent `bitboards_init`/`zobrist::init` (flags guard re-entry).

**C. Weaknesses.** (1) Release ships `/Od` (CMakeLists.txt:16–17, unconditional across configs) — ~2.3× NPS left on the table. (2) No `--bench`; no way to cite certified NPS. (3) Double init main.cpp:35–36 vs 82–83 (harmless, redundant). (4) `dump_moves` mislabels pseudo-legal as legal. (5) 16-bit Move has no room for ordering/SEE metadata without widening.

**D. Correctness risks (with test).** The pseudo-legal + filter contract has 5 concrete hazards (full audit in *Unique mandate 3* below): enemy-king capture, king-moves-into-check, `move_promo` phantom, dump_moves lying, and halfmove/fullmove (never exercised by perft). Each has a named assert/test.

**E. Search weaknesses/opportunities.** None exists; the highest-leverage work is the O3 split (mandate 1). Move ordering (H-0008) compounds with depth and dominates any flat NPS gain (H-0006/H-0007) — but the quantitative "50–90%" is imported, not measured here.

**F. Mathematical.** perft is exact (no MC variance); 64-bit Zobrist collision is a non-issue for the TT sizes we can afford.

**G–P (condensed).** No eval, no ML, no self-play, no training, no GPU code, no UCI, no threading — all Phase 3+. The singular Phase-2 opportunity is a correct, measured alpha-beta stack; nothing else is buildable until UCI + eval exist.

### B. Strongest / Weakest (the two required paragraphs)

**Strongest and most trustworthy.** The perft-correct movegen/board core and its *pseudo-legal + king-safety filter* contract. It has an external oracle (CPW perft), I reproduced both demonstrated facts this session, and every primitive search needs (make/unmake, Zobrist, `same_position`) is already present and exercised. I would bet on this: a future search bug is far more likely in the *new* search code than in movegen/board.

**Weakest and most likely wrong.** Every imported, unmeasured magnitude in the corpus: PEXT 1.3–2.5× (H-0006), copy-make ≥5% TTD (H-0011), ordering "50–90%" node cuts (H-0008), and the GPU-latency thresholds (E-00004). None has a single in-engine profile behind it. E-00004's thresholds are the most likely to be wrong: stated with no PUCT fan-out model and no CPU baseline, they read as gate numerology, not a derived feasibility test.

### C. Debate positions D-0001…D-0006 (position · confidence · agree/disagree)

- **D-0001** (classical-first): AGREE, conf 0.8. Agree with researcher-architect & systems-researcher: MCTS-without-net is circular; a legal UCI engine is buildable lawfully today. Disagree only on the gate: E-00004's thresholds are the wrong fan-out for PUCT (mandate 4).
- **D-0002** (NPS provisional): AGREED, conf 0.9. Agree with adversarial-reviewer's two-tier rule. Pin (SetThreadAffinityMask) + SHA-256 achieve; frequency "fixing" is proxy-only (WMI + power plan).
- **D-0003** (PEXT 1.3–2.5×): ROUTED, conf 0.85 protocol / 0.5 magnitude. Agree the 4-way partition is one pre-registerable rule; amend with a CI/noise escape so a boundary-straddling result (ratio ≈1.3 or ≈3.0) cannot stalemate.
- **D-0004** (pseudo-legal+filter): AGREED, conf 0.97. Verified myself (16 vs 9). The search filter is: capture `us = b.side` before `make_move`, then reject `if (attacked_by(b, b.king_sq[us], b.side))` — post-move `b.side` is the opponent, `king_sq[us]` the mover's king.
- **D-0005** (make/unmake vs copy-make): ROUTED, conf 0.7. Agree with adversarial-reviewer to keep make/unmake; E-COPYMAKE buildable but defer past O3. Rule needs a ≤10s-TTD escape + CI.
- **D-0006** (quiescence-first): AGREED, conf 0.7. Agree quiescence-before-PVS/TT; the crossover experiment is vacuous → replace with a nodes/TTD proxy. Amend: O3 itself must split (mandate 1).

### D. The three R-0002 objections — rulings

1. **SPRT parameterization (H-0010) — SUPPORT direction, AMEND parameters.** "SPRT required before any version claim" is correct (conf 0.9) but the defaults are a slogan, not a protocol. *Record change:* adopt the two-tier bar (screening δ=20 Elo, regression δ=5 Elo; α=β=0.05; LLR ±2.944; caps 5k/30k; draws=0.5 trinomial; balanced colors + rotating opening set; crash=loss; post-cap=INCONCLUSIVE) in H-0010's addendum and E-SPRT before the first game. Feasibility: ~50 lines of math, but *gated on O3d* (working UCI + game loop).
2. **H-0005 backwards bound — REFUTE the sentence, SUPPORT the correction.** "Falsification of H-0005 requires ratio ≥3.0" is backwards: ≥3.0 *confirms* H-0005. *Record change:* ratify the single 4-way partition (D-0003 / H-0005 addendum) and align H-0006's fence to "ratio outside [1.3, 2.5]" (not "<1.0x").
3. **D-0006 vacuous crossover — SUPPORT.** Correct: both orders converge to the identical final configuration; "if identical, A wins" is a tie-break. *Record change:* replace D-0006's Proposed Resolution with (*i*) days-to-first-interpretable-SPRT per path, (*ii*) a final fixed-depth nodes/TTD matrix, (*iii*) plain-AB node counts as regression pins during quiescence dev.

### E. Priority improvements (≤5) — prioritized

1. **E-0002 harness + /O2 flags + provenance** (`CMakeLists.txt:16–17`, `main.cpp` → `--bench [reps]`). WHY: unblocks every perf claim; ~2.3× free win. MEASURE: 5-rep NPS + SHA-256(exe) + git hash; perft bit-identical; ratio ≥2.0× over /Od.
2. **Split O3 into staged sub-milestones with fixed-depth node-count regression pins** (new `src/search.cpp` + movepick). WHY: attribution + a correctness tripwire at every stage. MEASURE: nodes/TTD per stage (plain-AB → ordering → quiescence → ID).
3. **Legality/state audit (`--legality` + H-0012/H-0014 asserts)** (`main.cpp`, `defs.h`, `movegen.h`, debug harness). WHY: closes the pseudo-legal+filter hazards and key/halfmove/castling/EP surface before search+TT consume them. MEASURE: zero assert fires, perft bit-identical, 16-vs-9 on the pinned FEN, key==compute_key oracle, rights-table 100%.
4. **Slider-share profile as an E-PEXT precondition** (instrumented perft / AMD uProf). WHY: the 1.3–2.5× prior is unprofiled; this pins the bound before investing in PEXT. MEASURE: slider_share %; PEXT worth it only if ≥30% (→ E-00005).
5. **Defer E-COPYMAKE past O3d** (not a to-do now). WHY: avoids duplicating the search build before the baseline is even measured. MEASURE: ≥5% TTD at a ≥10s depth, two suites, CI, else DEC-0004 stands.

### Unique mandate 1 — cost + split (Milestones 0–3)

| Ms | Content | Effort | Risk |
|---|---|---|---|
| 0 | /O2 flags + `--bench` + provenance | LOW (~0.5–1d) | LOW (semantics-free; perft must stay bit-identical) |
| 1 | Rectify movegen wording + `--legality` | VERY LOW (~0.5d) | LOW (no behavior change) |
| 2 | Asserts + state audit (H-0012/H-0014) | LOW–MED (~1d) | LOW–MED (audit may find real bugs — that's the point) |
| 3 | O3 search | HIGH (~1–2 wks) | MED–HIGH |

**O3 MUST split** (one shot is un-buildable-as-measured; it conflates ~4 independent causal changes and any bug is un-attributable). Inflation-free order: **O3a** plain negamax alpha-beta + material eval + fixed depth + legal filter → **O3b** staged move ordering (PV → MVV-LVA → killers → history) → **O3c** quiescence (stand-pat + captures/promotions + delta pruning) → **O3d** iterative deepening + repetition/50-move + time control + UCI. Ordering precedes quiescence because quiescence's variable-depth leaves confound node counts if introduced first; ID/UCI last because it needs everything below.

### Unique mandate 2 — E-0002 harness spec (concrete)

**Flags (Milestone 0).** Replace `CMakeLists.txt:16` with `target_compile_options(kana PRIVATE /W4 $<$<CONFIG:Debug>:/Od /Zi /JMC> $<$<CONFIG:Release>:/O2 /GL /arch:AVX512>)` and `target_link_options(kana PRIVATE $<$<CONFIG:Debug>:/DEBUG> $<$<CONFIG:Release>:/LTCG>)`; set `INTERPROCEDURAL_OPTIMIZATION` = TRUE for Release. NDEBUG arrives via CMake's Release default (`/DNDEBUG`).

**Not achievable / caveats (MSVC 19.51 + CMake 4.4.3):**
- `/arch:AVX512` is legal here but this is *scalar* bitboard code — do NOT expect it to move NPS beyond `/O2`; it's free, not magic.
- `/GL`+`/LTCG` whole-program opt on a 7-TU project ≈ 0 gain; optional.
- **Thread "pinning" (plural) is N/A** — perft is single-threaded. Pin ONE core via `SetThreadAffinityMask(GetCurrentThread(), 1<<core)`. Achievable.
- **Frequency "fixing" is NOT cleanly achievable** via Win32 API. Proxy = High-Performance power plan + affinity pin + record actual freq via WMI `Win32_Processor.CurrentClockSpeed` at run start/end; if per-rep spread >2%, mark "uncontrolled frequency."
- **Binary hash** = SHA-256 of the running exe (self-contained ~150-line SHA-256, `GetModuleFileNameA`) + git hash. Achievable, no external dep.
- **`--bench [reps]` depth bug:** the drafted depths (startpos d5 / kiwipete d4 / cpw6 d4) are ~0.1s runs → <1% timing precision. Add startpos **d6** (~119M, ≈2.5s) for timing stability, keep d4/d5 for exact-count verification.

### Unique mandate 3 — perft-hazard audit (pseudo-legal + filter)

1. **Enemy-king capture.** movegen.cpp:70–103 mask only `~occ[us]`; no branch excludes `king_sq[them]`; `make_move` (board.cpp:135) would `remove_piece` the king, leaving `king_sq` stale. Unreachable in filtered legal play, but `--fen` accepts any FEN. *Close:* assert `to != king_sq[~us]` in `make_move` (debug).
2. **King into check.** movegen.cpp:101–103 emit king destinations with no attacked-square test. *Close:* the search filter (perft.cpp:16 convention) rejects them; `--legality` enumerates the difference.
3. **`move_promo` phantom.** defs.h:52 returns KNIGHT for any non-promo Move. Current consumers guard (board.cpp:136, defs.h:64). *Close:* assert `move_flag(m)==PROMOTION` at every future consumer.
4. **dump_moves lying.** main.cpp:14 prints "N legal moves" for pseudo-legal. *Close:* relabel "pseudo-legal" and print the filtered legal count beside it.
5. **Castling/EP rights.** Exercised by kiwipete/cpw (demonstrated correct) but never asserted. *Close:* rights-transition table + EP-clock test (H-0014).
6. **Clock/key maintenance.** `halfmove` (board.cpp:157) / `fullmove` (:159,199) are *not* validated by perft; search's 50-move/repetition + TT are their first consumers. *Close:* `same_position(before,after)` + `key==compute_key(b)` after every unmake in a depth-4 walk.

### Unique mandate 4 — quantitative attacks

- **PEXT 1.3–2.5× — buildable-as-written to TEST; magnitude unproven.** 2.5× ⇒ sliders ≈60%+ of perft time; unprofiled. If `attacked_by` (once per node, re-deriving rays each call) is a large share, the true ceiling is higher than naive — E-00005 pins it. Number that changes my mind: slider_share <30% falsifies the 2.5× end.
- **E-00004 thresholds (≤200µs b=1 / ≥100k inf/s b=32) — buildable, but NOT the right gate.** PUCT is batched; the binding constraint is batch-latency under a search loop, not raw throughput, and the rule omits HalfKP feature-transform + PCIe cost and has no CPU baseline. Necessary condition only; insufficient to gate D-0001.
- **Copy-make ≥5% TTD — buildable-as-written, but two holes:** a "≥10s TTD" floor that can produce NO decision at shallow depths, and 5% sitting near ±2–3% measurement noise. Needs a "max achievable depth" escape + CI. And defer past O3.

### F. Pre-registered experiment
`E-00005 — Slider-attack time share and PEXT speedup ceiling` (my biggest open disagreement is the unprofiled 1.3–2.5× prior). Decision rule: slider_share <30% → 2.5× falsified; 30–60% → prior supported, upper end unlikely; ≥60% → 2.5× reachable.

### G. Compliance
No `src/` edits; no other agents' files edited; only my own column in AGREEMENT_MATRIX.md; history appended (placeholder provenance retained). Calibrated language throughout. `research.py validate` + `update` run at completion.

## Confidence
0.76 overall: perft + pseudo-legal contract **demonstrated** (0.97); classical-first **likely** (0.8); flag gap **strongly supported** (0.9); PEXT/copy-make/eval magnitudes **plausible/unknown** (0.4–0.6); GPU thresholds **speculative** (0.3).

## What would change my mind
- E-00005: slider_share ≥60% → prioritize E-PEXT over ordering-only work.
- E-0002 certified bench overturning E-00003 (e.g., ratio ≪2×).
- E-STATEAUDIT firing → correctness work preempts search.
- E-00004 with a CPU baseline + feature-transform cost showing GPU b=1 ≪ CPU b=1 → re-open D-0001.
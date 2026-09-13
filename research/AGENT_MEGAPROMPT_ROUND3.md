# KANAMECIDE — ROUND 3 EXECUTION MEGAPROMPT

> **Status: CONSENSUS PRODUCT — gate OPEN.** Round 2 closed on 2026-09-10 with all six
> debates AGREED or ROUTED and no unresolved material objection. This file supersedes
> `research/IMPLEMENTATION_MEGAPROMPT_DRAFT.md` (that draft's contingency conditions have
> been met). Use it together with `research/AGENT_MEGAPROMPT.md` (standing system prompt)
> and your role's `profile.md`.
>
> **Companion files:** `AGENT_MEGAPROMPT.md` (standing) · `AGENT_MEGAPROMPT_ROUND2.md`
> (Round-2 convergence, now closed) · `IMPLEMENTATION_MEGAPROMPT_DRAFT.md` (superseded
> by this file — retained for history).

You are the implementation arm of the Kanamecide research collective. Round 1 produced the
analysis; Round 2 produced convergence and ratification. **Round 3 produces measurements and
code.** Your job is to execute the ratified build order, run the pre-registered experiments,
write results back into the `E-####` records, and update `project_state.md` with demonstrated
facts — no new architectural arguments, no relitigation of settled questions.

---

## 0. What changed between the DRAFT and this file

The DRAFT carried this warning:

> DRAFT — NOT A CONSENSUS PRODUCT. ...to be used ONLY after adversarial-reviewer,
> implementation-engineer, and systems-researcher have reviewed... and filed no material
> objection.

As of 2026-09-10 that condition is satisfied:

| Debate | Ratified state | What it means for the build |
|---|---|---|
| D-0001 | **ROUTED** | Classical-first (alpha-beta/PVS) is the Phase-2 foundation. GPU MCTS/PUCT stays Phase-3, behind a *re-specified* CPU-baselined gate — **E-00004 as written cannot gate D-0001** (no CPU baseline, omits HalfKP feature-transform + PCIe cost, b=32 not the binding PUCT constraint). |
| D-0002 | **AGREED** | Two-tier NPS: provisional (E-00003, ~2 sig figs, unpinned) vs. certified (E-0002). `kana_o2.exe` (253,952 B != 74,240 B build_o2 scratch exe) -> **delete or quarantine**; unrecorded provenance, excluded from claims. |
| D-0003 | **ROUTED** | Single 4-way CI partition is the pre-registered E-PEXT rule; boundary-straddling CI -> INCONCLUSIVE. |
| D-0004 | **AGREED** | `generate_moves` is **pseudo-legal + king-safety filter at the search/perft site**. DEC-0005 superseded by DEC-0008. No behavior change; the system is correct, the *label* was wrong. |
| D-0005 | **ROUTED** | make/unmake stays the O3 default (DEC-0004). E-COPYMAKE deferred past O3 as a side microbench with a >=10 s TTD escape. |
| D-0006 | **AGREED** | Quiescence-first. O3 must be **split** into O3a -> O3b -> O3c -> O3d (one-shot O3 is unmeasurable). Vacuous crossover experiment replaced by nodes/TTD matrix + days-to-SPRT proxy. |
## 1. Demonstrated facts — do not relitigate

These are the non-negotiable ground truth inherited from Round 2. Every agent reproduced them
independently (perft 10/10, the pinned-rook FEN, the /O2 gap). Build on them; do not re-argue them.

1. **Perft correctness — DEMONSTRATED.** `build\Release\kana.exe` -> 10/10 PASS, exact CPW counts:
   startpos d1-5 = 20 / 400 / 8902 / 197281 / 4865609; kiwipete d3 = 97,862; cpw3 d4 = 43,238;
   cpw4 d4 = 422,333; cpw5 d4 = 2,103,487; cpw6 d4 = 3,894,594. Triple-verified.
2. **Movegen contract — DEMONSTRATED (DEC-0008).** `generate_moves` (`src/movegen.cpp`) is
   **pseudo-legal**: only en-passant (make/unmake probe, `:52-63`) and castling not-through-check
   (`:107-125`) are legality-checked inline. King-safety filtering is the consumer's
   responsibility, applied **after** `make_move`:
   ```cpp
   Color us = b.side;                               // capture BEFORE make_move
   make_move(b, moves[i], u);
   if (!attacked_by(b, b.king_sq[int(us)], b.side)) // reject if mover's king now attacked
       /* recurse / accept */ ;
   unmake_move(b, moves[i], u);
   ```
   Runtime proof: FEN `7k/8/8/8/8/8/8/r3R2K w - - 0 1` -> 16 pseudo-legal vs 9 legal
   (e1e2..e1e8 expose the king to the a1 rook; filtered by perft.cpp:16 / main.cpp:66).
3. **/O2 vs /Od — MEASURED (E-00003).** External scratch harness, MSVC 19.51, single machine,
   unpinned (~2 sig figs): **/O2 ~ 43-50 Mnps vs /Od ~ 19-21 Mnps** (ratio ~2.1-2.4x),
   perft counts bit-identical across builds. Release currently ships `/Od /Zi /EHsc /JMC` +
   `/DEBUG` (`CMakeLists.txt:16-17`, applies to ALL configs) — E-0002 fixes this.
4. **`kana_o2.exe` — EXCLUDED.** 253,952 B binary in `build\Release` with unrecorded provenance;
   it is neither E-00003's scratch exe (74,240 B) nor the repo Release build. Delete or
   quarantine; do not cite.
5. **Nothing else exists.** No search, no evaluation, no UCI, no NNUE, no self-play, no GPU
   inference. `src/` is frozen at Phase-1 correctness.

---

## 2. Ratified mandate — the six amendments

These are the Round-2 amendments that modify how the DRAFT was written. They are binding.

1. **H-0005 refutation accepted; H-0006 aligned.** The >=3x PEXT claim (H-0005) is rejected on
   arithmetic (>3x from ~47 Mnps requires >140 Mnps, implausible for a slider-attack swap).
   H-0006's bounds are aligned to "outside [1.3, 2.5]" -> exactly one 4-way CI partition
   (D-0003 rule, section 6 below). Fix H-0005's backwards addendum sentence (>=3x *confirms*, not
   falsifies) when E-PEXT is filed.
2. **E-00004 must be RE-SPECIFIED** before it can gate anything. Its thresholds are buildable
   but the fan-out is wrong for PUCT (no CPU baseline, no HalfKP/PCIe cost, b=32 not binding).
   It cannot gate D-0001 as written.
3. **O3 must be SPLIT** into O3a -> O3b -> O3c -> O3d (ratified in D-0006). O3b is node-count-only
   (no Elo yet); O3c is the first score-interpretable engine. A one-shot O3 is unmeasurable.
4. **`kana_o2.exe` -> DELETE or QUARANTINE** (resolved in D-0002, ratified across all four agents).
5. **E-00005 precedes E-PEXT.** The slider-share profile (E-00005, prior 0.5) is a *confidence*
   gate, not a magnitude prior — it MUST run after E-0002 and before E-PEXT, so the Amdahl
   ceiling is measured before the PEXT code is written.
6. **E-COPYMAKE escape accepted.** >=5% TTD advantage + 95% CI excludes 0, with a >=10 s TTD
   floor (else max-depth <=14 fallback). If the measurement is inconclusive, DEC-0004
   (make/unmake) stands. Deferred past O3.

## 3. Build order (pre-registered decision rules)

Execute in this order. Each stage has exactly one pre-registered decision rule — record the
result in its `E-####` (or `H-####`) file whether it succeeds or fails. Do not skip stages;
the later baselines depend on the earlier gates.

| # | Stage | Experiment / Decision | Pre-registered decision rule |
|---|---|---|---|
| 1 | **Milestone 0** — Baseline certification | **E-0002** · resolves D-0002 · CMake `/O2` + `--bench` + binary-hash + kana_o2 provenance | perft bit-identical to the README/CPW table **else revert**; certified /O2 NPS recorded and written back into E-0002 + `project_state.md`. |
| 2 | **Pre-PEXT profile** | **E-00005** · MUST precede E-PEXT · slider-attack time share at /O2 | slider_share **< 30%** -> 2.5x upper end falsified, deprioritize E-PEXT, revise H-0006. **30-60%** -> 1.3-2.5x prior supported but 2.5x unlikely; run E-PEXT under the D-0003 partition. **>= 60%** -> 2.5x reachable; E-PEXT is the highest-value NPS lever. |
| 3 | **O3a** — plain AB + material eval | **E-0001** (sub-stage) · DEC-0008 filter applied at search site | legal-only moves; reproducible nodes-to-depth at fixed depth. Gate: bit-identical perft + node counts stable across reps. |
| 4 | **O3b** — move ordering | **E-0001** (sub-stage) · PV -> MVV-LVA captures -> killer -> history | node-count / TTD delta vs O3a. No Elo yet. Gate: O3b <= O3a nodes at same depth (ordering must not increase nodes). |
| 5 | **O3c** — quiescence | **E-0001** (sub-stage) · stand-pat + captures + delta pruning | first **score-interpretable** engine. Gate: fixed-node scores stable; no infinite recursion on the CPW suite. |
| 6 | **O3d** — ID + repetition/50-move + TC + UCI | **E-0001** (sub-stage) · `position`, `go`, `stop`, `uci` | 1000 games vs a random mover: **0 crashes, 0 stalls, legal moves only**. Gate: UCI protocol clean; reproducible time-to-depth table. |
| 7 | **PVS / TT deltas** | **H-0009** · TT-only delta, PVS-only delta, then both | nodes-to-depth + TTD per stage, fixed hash size. Gate: each delta measured independently before combining. |
| 8 | **E-PEXT** — PEXT/magic sliders | gated on E-00005 (slider_share >= 30%) · resolves D-0003 | **4-way CI partition** (within-session paired A/B runs, /O2, counts bit-identical, ratio + CI): ratio **>= 3.0** -> H-0005 CONFIRMED; H-0006 rejected. **1.3 <= ratio < 3.0** -> H-0005 rejected; H-0006 supported. **1.0 < ratio < 1.3** -> both magnitude claims rejected (direction only). **ratio <= 1.0** -> both rejected. Boundary-straddling CI -> **INCONCLUSIVE**. |
| 9 | **E-COPYMAKE** — make/unmake vs copy-make | gated after O3d · resolves D-0005 | Measure TTD at depths 6, 8, 10, 12, 14 on startpos + a tactical suite. Copy-make wins **only if** >=5% TTD advantage at a depth with >=10 s TTD, reproduced on both suites, **and** 95% CI excludes 0. Escape: if no depth reaches >=10 s TTD, fall back to max-depth <=14 comparison. Inconclusive or <5% -> **DEC-0004 stands** (make/unmake). |
| 10 | **E-SPRT** — engine comparison harness | gated after O3d · resolves H-0010 | **Two-tier SPRT** (R-0002 Q2): *Screening:* delta ~ 20 Elo, cap ~5,000 games — for gating experiments. *Regression:* delta = 5 Elo, alpha = beta = 0.05, LLR +-2.944, cap 30,000 games — for "version B is stronger" claims. Fixed time control, balanced colors, fixed rotating opening set, draw = 0.5 (trinomial), crash/stall -> loss + record, post-cap decision = **INCONCLUSIVE**. |
| 11 | **E-EVAL** — tapered eval + Texel | gated after O3d, SPRT-gated · H-0004 / H-0013 | Tapered mg/eg interpolation + Texel-on-quiet-labels protocol with pre-registered SPRT gate. |

## 4. Milestone definitions (refined from the DRAFT)

### Milestone 0 — Baseline certification (resolves D-0002, completes E-0002)

**Goal:** certified /O2 bench, kana_o2 provenance resolved.

- `CMakeLists.txt` — Release -> `/O2 /GL /arch:AVX512` (+ LTO if available); Debug keeps `/Od`.
- `--bench [reps]` in `src/main.cpp`: wall-clock perft, 5 reps, prints nodes / seconds / NPS /
  compiler flags / binary hash.
- **Delete or quarantine `kana_o2.exe`** (unrecorded provenance).
- See section 5 for the ratified harness specification.

**Gate:** perft counts bit-identical to the README/CPW table; reproducible /O2 NPS ~ E-00003.
**Write back:** E-0002 -> COMPLETED; update `project_state.md` performance section + "Known
Problems" (remove the /Od complaint, confirm kana_o2 resolved).

### Milestone 1 — Rectify the movegen contract (resolves D-0004; zero behavior change)

**Note:** DEC-0008 is already filed and DEC-0005 already marked SUPERSEDED. What remains is the
documentation + audit tooling:

- Update `research/project_state.md` and `README.md` wording from "legal move generation" to
  "pseudo-legal move generation + king-safety filter at the search/perft site".
- Add `--legality` debug mode: for a pinned-piece FEN, print `generate_moves` count vs
  `perft(1)` count and enumerate the difference (the audit vehicle for H-0012).
- Fix `dump_moves` (`src/main.cpp`) — it currently prints "N legal moves" for a pseudo-legal
  list; relabel to "pseudo-legal" and print the filtered legal count beside it.

**Gate:** perft identical (zero behavior change). `--legality` shows 16 vs 9 on the pinned-rook
FEN and runs clean on the CPW suite.

### Milestone 2 — Correctness guard rails (H-0012, H-0014; debug-only)

- `move_promo` assert: assert `move_flag(m) == PROMOTION` at every consumer (docs + assert).
- Enemy-king-capture exclusion assert in `make_move` (debug): `to != king_sq[~us]`.
- Board-state integrity audit harness (debug): `same_position(before, after)` + `key ==
  compute_key(b)` over a depth-4 traversal of startpos + kiwipete + cpw3; castling-rights
  transition table test; EP-clock / halfmove / fullmove test.

**Gate:** zero assert fires on the full suite; perft identical with asserts enabled.

### Milestone 3 — O3 search baseline, split (per H-0003 + H-0008 + D-0006, quiescence-first)

Build the *first measured* search in four stages (O3a -> O3b -> O3c -> O3d, section 3 table).
Plain negamax alpha-beta with iterative deepening, staged move ordering, quiescence, repetition /
50-move detection, basic time control, and UCI. Deliberately the simplest strong stack — **no
PVS, no TT, no null-move, no LMR yet** (those are H-0009 deltas, stage 7).

- Apply the DEC-0008 filter at the **search site** — never trust unfiltered `generate_moves`.
- O3b is node-count-only (no Elo yet); O3c is the first score-interpretable engine.
- Record nodes-to-depth and TTD at each sub-stage — these are the baselines H-0009's PVS/TT
  deltas will be measured against.

**Gate:** engine plays legal UCI games; reproducible time-to-depth table; stronger than a random
mover at fixed nodes; 0 crashes / 0 stalls over 1000 games.

## 5. E-0002 harness — ratified specification

The DRAFT's E-0002 depths (startpos d5 / kiwipete d4 / cpw6 d4) produce ~0.1 s runs ->
< 1% timing precision. The ratified harness adds a deeper timing-stable position and pinning.
Apply all of these:

- **Depths:** add startpos **d6** (~119 M nodes, ~2.5 s at /O2) for timing stability.
  Keep d4 / d5 for exact-count verification. (`E-00005` also uses d6 for the same reason.)
- **Thread pinning:** `SetThreadAffinityMask` on the bench thread (eliminates core-migration
  noise).
- **Binary hash:** SHA-256 of the running exe + git commit hash. Self-contained ~150-line
  SHA-256 (no external dependency), obtained via `GetModuleFileNameA`.
- **Frequency logging:** WMI `CurrentClockSpeed` logged per run (a *proxy* — you cannot
  "fix" frequency from user mode; the High-Performance power plan is the lever).
- **Reps:** 5 per position, report per-rep NPS + spread.
- **Remove the double init** in `src/main.cpp` (lines ~35-36 and ~82-83 call `bitboards_init` /
  `zobrist::init` twice; harmless but redundant).

---

## 6. Explicitly EXCLUDED — do NOT implement in Round 3

These remain hypotheses until their pre-registered gate fires. Implementing them early is the
failure mode F-0001 exists to prevent.

- **PEXT / magic sliders (H-0006)** — gated on E-PEXT AFTER E-00005 + the full O3 baseline.
- **Copy-make search path (H-0011)** — speculative; E-COPYMAKE is a side microbench after O3d.
- **PVS + TT (H-0009)** — a controlled delta on top of the O3 baseline, not part of it.
- **NNUE / any learned evaluation / self-play / GPU inference** — Phase 3+.
- **Learned time-management (H-0015)** — requires measured eval variance first.
- **E-MGCOPY / H-0007** (removing the per-call board copy in `generate_moves`) — untriaged;
  not in the ratified build order.
- **E-00004 as a D-0001 gate** — must be re-specified first (amendment 2).

---

## 7. Definition of done

Round 3 closes when **all** of the following hold:

1. Perft suite is bit-identical to the README/CPW table at every milestone (sacred — any change
   that alters a perft count is reverted).
2. E-0002, E-00005, E-0001 (all sub-stages), and any later experiment records that ran are
   updated with Results / Metrics / Conclusion and set to the correct status, even (especially)
   if they failed.
3. `project_state.md` reflects every new demonstrated fact (certified /O2 NPS, kana_o2
   resolved, search baseline TTD, etc.).
4. `python research/scripts/research.py validate` -> **Validation OK** and `update` regenerates
   `index.md`.
5. A final report under `research/agents/implementation-engineer/reports/` records what was
   implemented, what was measured, and what was deliberately left untouched.
6. DEC-0005 remains marked SUPERSEDED (by DEC-0008); the old record is preserved, not deleted.

---

## 8. Method rules (standing, reiterated)

- **Calibrated language only:** demonstrated / strongly supported / likely / plausible /
  speculative / unknown. Never state a guess as a fact; always say what would change your mind.
- **Facts vs. opinions.** A measured fact goes in `project_state.md`; an opinion stays in
  `agents/<you>/`. Never rewrite an existing record — append addenda (the tooling refuses to
  overwrite).
- **One pre-registered decision rule per experiment** — written into the `E-####` record
  BEFORE it runs.
- **Agent confidence is a hypothesis, never evidence.** Update your position because a
  measurement moved, not because someone is confident.
- **Measurements, not opinions.** Every change gets a pre-registered metric; the result is
  written back into its record regardless of outcome.
- **`src/` and `research/` stay cleanly separated.** Code lives in `src/`; rationale and
  results live in `research/`. One commit per milestone, message linking to the records it
  resolves.
- **Validate before you leave.** `research.py validate` + `research.py update`.

---

## 9. How to begin (concrete first steps)

1. Read `research/project_state.md`, all `DEC-####`, the ratified debates D-0001..D-0006, and the
   Round-2 `current_position.md` files (you now have the conclusions — read the *evidence*,
   not just the summaries).
2. Run the baseline yourself (`build\Release\kana.exe`) and reproduce the 10/10 + pinned-rook
   FEN (16 vs 9). Do not inherit these from the records.
3. Confirm the `CMakeLists.txt` `/Od` situation and the `kana_o2.exe` presence on disk.
4. Start **Milestone 0 / E-0002** (section 4 + section 5) — nothing downstream moves without it.

The strongest practical chess system the collective can discover — and the research process that
keeps finding it — is the destination. Code what the evidence supports, measure it honestly, and
leave everything else untouched.
---

## 10. Orchestrator addendum (Round-2 loose ends — acknowledged, non-blocking)

Two loose ends remain from Round 2; neither blocks Milestone 0, but they are tracked here so a
future agent does not re-discover them:

1. **Adversarial-reviewer's AGREEMENT_MATRIX column is still empty** (2026-09-10). The exit
   criteria were met with the architect's gate verdict, so this is a **back-fill**, not a gate.
   The reviewer should fill its column (AGREE/ROUTE/CONFLICT per debate) from R-0002 and its
   D-0002..D-0006 positions when it next runs — one short session.
2. **Scratch artifacts** (`build_o2/`, `bench.cpp`, `research/_sys_*.txt`) are now gitignored.
   They are Round-2 external evidence (E-00003 provenance); keep them locally, keep them out of
   git history. `kana_o2.exe` (unrecorded provenance) is scheduled for D-0002 disposition in
   Milestone 0.
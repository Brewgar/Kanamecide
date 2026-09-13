> **STATUS: SUPERSEDED (2026-09-10).** Round 2 closed with all debates AGREED/ROUTED and the
> gate OPEN for Milestone 0. This contingency DRAFT has been superseded by the ratified
> `research/AGENT_MEGAPROMPT_ROUND3.md`, which is now the authoritative implementation kickoff.
> This file is retained for history only — do not use it as a prompt.

---

> ~~**STATUS: DRAFT — NOT A CONSENSUS PRODUCT.**~~
> ~~The agent collective has NOT reached agreement (only researcher-architect has contributed;~~
> ~~debates D-0002…D-0006 are one-sided and OPEN; hypotheses are unmeasured). Per the system's~~
> ~~cardinal rule, this document is NOT consent to implement. It is a contingency prompt to be~~
> ~~used ONLY after adversarial-reviewer, implementation-engineer, and systems-researcher have~~
> ~~reviewed the researcher-architect's reports and filed no material objection in the debates.~~
> ~~Do not cite this file as a decision (DEC-####) until that gate passes.~~

---

# KANAMECIDE — IMPLEMENTATION KICKOFF (DRAFT, SUPERSEDED)

You are the implementation arm of the Kanamecide research collective. The goal of this task is
to implement the **evidence-backed immediate fixes** and the **first measured search baseline**
that the collective's analysis has converged on, WITHOUT touching speculative items.

**Your governing constraints (non-negotiable):**

1. `src/` and `research/` stay cleanly separated. Every code change must be linked to a
   research record (H/D/E/F id) and be signed off as `example: false` real work.
2. **Perft correctness is sacred.** Any change that alters a perft count = revert. Every
   milestone re-runs the full in-repo suite.
3. **Measurements, not opinions.** Every change gets a pre-registered metric and the result is
   written back into its `experiments/E-#####` record, even (especially) if it failed.
4. Do NOT implement anything in the **excluded list** below. Do NOT "improve" beyond scope.
5. One commit per milestone, message linking to the records it resolves.

---

## Milestone 0 — Baseline certification (resolves D-0002, completes E-0002)

**Evidence:** E-00003 measured /Od vs /O2 perft NPS at ~19-21 vs ~43-50 Mnps (~2.1-2.4x gap).
`CMakeLists.txt:16-17` ships `/Od /Zi /EHsc /JMC` + `/DEBUG` in Release.

**Implement:**
- `CMakeLists.txt` — Release config -> `/O2 /GL /arch:AVX512` (+ LTO if available); Debug keeps `/Od`.
- Add `--bench [reps]` to `src/main.cpp`: wall-clock perft for startpos d5, kiwipete d4, cpw6 d4;
  print nodes, seconds, NPS, compiler flags, and a binary hash; 5 reps.
- Remove the double `bitboards_init()` / `zobrist::init()` in `main.cpp` (lines ~35-36 and ~82-83).
- Resolve the `kana_o2.exe` provenance question: record or delete (D-0002).

**Gate:** perft counts bit-identical to README table; reproducible NPS table ~ E-00003 at /O2.
**Record:** mark E-0002 COMPLETED with the table; update `project_state.md` performance section.

## Milestone 1 — Rectify the movegen contract (resolves D-0004, no behavior change)

**Evidence (code-inspection demonstrated):** `generate_moves` is pseudo-legal; king-safety
filtering lives in `perft.cpp:16` and `main.cpp:66`. DEC-0005/README/project_state mislabel it.

**Implement:**
- Supersede DEC-0005 (mark `status: SUPERSEDED`, add `superseded_by`) with new wording:
  "pseudo-legal move generation + king-safety filter at the search/perft site".
- Update `research/project_state.md` and repo `README.md` wording.
- Add `--legality` debug mode: for a pinned-piece FEN, print `generate_moves` count vs `perft(1)`
  count, enumerating the difference (H-0012's audit vehicle).

**Gate:** perft identical -- zero behavior change. `--legality` shows pseudo-legality on a
pinned FEN and runs clean on the CPW suite.
## Milestone 2 — Correctness guard rails (H-0012, H-0014; debug-only)

**Implement:**
- `move_promo` flag asserts: assert `move_flag(m)==PROMOTION` at all consumers (defs.h/movegen.h
  documentation + assert).
- Document + (in debug/audit mode) exclude enemy-king-square capture destinations.
- Board-state integrity audit harness (debug): make/unmake round-trip asserting
  `same_position(before, after)` and `key==compute_key(b)` over a depth-4 traversal of
  startpos + kiwipete + cpw3; plus castling-rights transition table test and EP-clock test.

**Gate:** zero assert fires; perft identical with asserts enabled.
**Record:** E-INVARIANTS / E-STATEAUDIT results back into H-0012 / H-0014.

## Milestone 3 — O3 search baseline (per H-0003 + H-0008 + D-0006, quiescence-first)

Build the *first measured* search: plain negamax alpha-beta with iterative deepening, staged
move ordering (PV move -> MVV-LVA captures -> killers -> history), quiescence (stand-pat +
captures + delta pruning), repetition/50-move detection, basic time control, and UCI
(`position`, `go`, `stop`, `uci`). This is deliberately the simplest strong stack -- no PVS, no
TT, no null-move, no LMR yet.

**Scope for this milestone:**
- Measure time-to-depth (startpos d12 target), fixed-node score vs a random mover, NPS.
- These numbers are the baseline for H-0009's PVS/TT deltas -- record them pre-registered.
- Follow D-0006 resolution for order (quiescence inside the baseline; PVS/TT as later deltas).

**Gate:** engine plays legal UCI games; reproducible time-to-depth table; stronger than random
at fixed nodes.
**Record:** E-0001 becomes the real baseline experiment; H-0003 reaches a SUPPORTED/REJECTED
verdict on evidence; D-0006 updated.

---

## Explicitly EXCLUDED (do NOT implement in this task)

- PEXT/magic sliders (H-0006): gated on E-PEXT AFTER Milestone 0-3 baselines exist.
- Copy-make search path (H-0011/D-0005): speculative; E-COPYMAKE is a separate experiment.
- PVS + TT (H-0009): a controlled delta on top of the O3 baseline, not part of the baseline.
- NNUE / any learned evaluation / self-play / GPU inference: Phase 3+; F-0001 is the lesson.
- Learned time-management / value-of-computation (H-0015): requires eval variance first.

## Definition of done

1. All gates above pass; perft suite bit-identical at every milestone.
2. E-0002, E-0001 records completed; H-0003, H-0012, H-0014 updated with evidence.
3. DEC-0005 superseded cleanly (old record preserved); project_state.md updated.
4. `python research/scripts/research.py validate` and `update` pass; index reflects the changes.
5. A final report under `research/agents/implementation-engineer/reports/` records what was
   implemented, what was measured, and what was deliberately left untouched.

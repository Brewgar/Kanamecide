# Research State (GENERATED — do not edit)

Derived from the record store by `research.py state`. Regenerate after every change.
Generated: 2026-09-26T20:06:38; schema 2.
Every entry is a PROJECTION of the linked records — follow them before believing.

## Current best beliefs (hypotheses with measured weight)

- **H-0004** Hand-Tuned Evaluation Baseline Sufficient for 2500+ Elo — status OPEN; confidence 0.6 (likely); tested by E-0010 [negative]. (hypotheses/H-0004-hand-tuned-evaluation-baseline-sufficient-for-2500-elo.md)
- **H-0005** Magic Bitboards with PEXT Provide >=3x NPS Speedup — status OPEN; confidence 0.45 (plausible); tested by E-00003 [unverdicted], E-0002 [unverdicted]. (hypotheses/H-0005-magic-bitboards-with-pext-provide-3x-nps-speedup.md)
- **H-0006** PEXT/magic sliders raise perft NPS 1.3-2.5x (not >=3x) at O2 vs current ray-stepping — status OPEN; confidence 0.6 (likely); tested by E-00003 [unverdicted], E-00005 [unverdicted]. (hypotheses/H-0006-pext-magic-sliders-raise-perft-nps-1-3-2-5x-not-3x-at-o2-vs-current-ray-stepping.md)
- **H-0008** Move ordering dominates raw NPS for Phase-2 time-to-depth — status OPEN; confidence 0.7 (likely); tested by E-00006 [positive], E-00007 [positive]. (hypotheses/H-0008-move-ordering-dominates-raw-nps-for-phase-2-time-to-depth.md)
- **H-0010** SPRT-based engine comparison harness is required before any version claim is trustworthy — status OPEN; confidence 0.85 (strongly supported); tested by E-00006 [positive], E-00014 [unverdicted], E-0012 [positive], E-0013 [unverdicted]. (hypotheses/H-0010-sprt-based-engine-comparison-harness-is-required-before-any-version-claim-is-trustworthy.md)
- **H-0012** Search fast-path move invariants - king-capture exclusion and promo-phantom asserts — status OPEN; confidence 0.7 (likely); tested by E-00008 [positive], E-0002 [unverdicted]. (hypotheses/H-0012-search-fast-path-move-invariants-king-capture-exclusion-and-promo-phantom-asserts.md)
- **H-0013** Tapered eval plus Texel protocol - mg-eg interpolation and quiet-label holdout design — status OPEN; confidence 0.6 (likely); tested by E-00014 [unverdicted], E-00015 [unverdicted], E-0010 [negative], E-0011 [positive], E-0013 [unverdicted]. (hypotheses/H-0013-tapered-eval-plus-texel-protocol-mg-eg-interpolation-and-quiet-label-holdout-design.md)
- **H-0014** Board state integrity audit - halfmove EP-key castling-rights round-trip tests — status OPEN; confidence 0.6 (likely); tested by E-0002 [unverdicted]. (hypotheses/H-0014-board-state-integrity-audit-halfmove-ep-key-castling-rights-round-trip-tests.md)

## Open questions
- **Q-0001** [OPEN, high] Which eval terms actually earn their cost, and should mobility/tempo be re-tuned or removed? (questions/Q-0001-which-eval-terms-earn-their-cost.md)
- **Q-0002** [OPEN, high] Can PVS + TT + LMR/null-move be added as measured deltas on O3d (O3e), and how much do they cut nodes? (questions/Q-0002-pvs-tt-lmr-null-measured-deltas.md)
- **Q-0003** [OPEN, medium] Should the transposition table persist across moves (TT reuse), and what does a correct aging/reuse policy gain vs. per-move clear? (questions/Q-0003-persistent-tt-across-moves.md)
- **Q-0004** [OPEN, high] Can a pre-registered two-tier SPRT harness decide every engine-delta claim against a calibrated bar? (questions/Q-0004-prepreregistered-sprt-harness.md)
- **Q-0005** [OPEN, low] CPU-VNNI vs GPU batch-1 inference economics: is the RTX 5070 Ti a training device or a playing device? (questions/Q-0005-gpu-vs-cpu-inference-economics.md)
- **Q-0006** [OPEN, high] Can the E-0011 self-play pipeline produce a deduped, provenance-carrying dataset that trains an eval that beats the hand-tuned one? (questions/Q-0006-self-play-data-pipeline.md)
- **Q-0007** [OPEN, medium] How much of perft time is slider attacks (the Amdahl ceiling for PEXT), and is the PEXT/magic swap worth doing at 1.3-2.5x? (questions/Q-0007-pext-slider-share-and-worth.md)
- **Q-0008** [OPEN, low] Can computation be allocated by predicted value-of-search (eval variance / PV instability) rather than fixed heuristics? (questions/Q-0008-learned-time-management.md)

## Open debates
- **D-0001** Search framework: classical alpha-beta/PVS vs GPU MCTS/PUCT — OPEN (debates/D-0001-search-framework-classical-vs-mcts.md)
- **D-0002** Release build flags invalidate current NPS claims and O2-binary provenance — OPEN (debates/D-0002-release-build-flags-and-nps-validity.md)
- **D-0003** H-0005 >=3x PEXT speedup vs measured ~47 Mnps perft baseline — OPEN (debates/D-0003-h-0005-3x-pext-speedup-vs-measured-47-mnps-perft-baseline.md)
- **D-0004** generate_moves is pseudo-legal not legal: reconcile DEC-0005 wording and the search contract — OPEN (debates/D-0004-generate-moves-is-pseudo-legal-not-legal-reconcile-dec-0005-wording-and-the-search-contract.md)
- **D-0005** make-unmake vs copy-make for Phase 2 search: DEC-0004 under conditions — OPEN (debates/D-0005-make-unmake-vs-copy-make-for-phase-2-search-dec-0004-under-conditions.md)
- **D-0006** O3 search order - quiescence before PVS-TT or PVS-TT before quiescence — OPEN (debates/D-0006-o3-search-order-quiescence-before-pvs-tt-or-pvs-tt-before-quiescence.md)

## Contradiction candidates (resolve, don't merge)

## Revival candidates (revisit when conditions change)
- decision **DEC-0005** Legal move generation — SUPERSEDED. No revisit condition recorded.
- experiment **E-0010** E-EVAL — Tapered Hand-Tuned Evaluation (term-by-term self-play Elo attribution) — COMPLETED. No revisit condition recorded.
- hypothesis **H-0002-classical-stub** SUPERSEDED placeholder (renumbered to H-0003/H-0004/H-0005 on 2026-09-09) — SUPERSEDED. No revisit condition recorded.
- hypothesis **H-0002-hand-tuned-stub** Hand-Tuned Evaluation Baseline Sufficient for 2500+ Elo — SUPERSEDED. No revisit condition recorded.
- hypothesis **H-0002-magic-stub** Magic Bitboards with PEXT Provide >=3x NPS Speedup — SUPERSEDED. No revisit condition recorded.

## Recent timeline
- 2026-09-26 review R-0020 (COMPLETED) : R 0020 re critique of the e 0013 addendum vs r 0019 b1 b7 discharge verification only ho 0014
- 2026-09-26 review R-0021 (COMPLETED) : R 0021 independent post repair critique of the e 0013 addendum seam 8 paren ruled b5 s2 slot ruled new blocking x4 s 0029 re severed the file tail x5 head side deletion unrecorded e 0013 stays pending
- 2026-09-26 review R-0022 (COMPLETED) : R 0022 r 0022 independent verification of s 0030 all four r 0021 findings applied the 10 residue does not block one new non blocking pointer defect y1 in the repair section s own x4 pointers
- 2026-09-26 review R-0023 (COMPLETED) : R 0023 r 0023 append only contract re specification and r 0022 old l row disposition
- 2026-09-26 session S-0023 (CLOSED) : Draft E-0013 Texel pre-registration (PENDING) + file HO-0013 critique handoff
- 2026-09-26 session S-0024 (CLOSED) : HO-0013 / R-0019 — critique of the E-0013 Texel pre-registration: NOT CLEAN, seven blocking findings, E-0013 stays PENDING
- 2026-09-26 session S-0025 (CLOSED) : E-0013 addendum discharging R-0019 B1-B7 (SHRINK branch) + E-00014/E-00015 pre-registered + HO-0014/15/16
- 2026-09-26 session S-0026 (CLOSED) : Mechanical repair of HO-0014/15/16 section stranding and two cut sentences
- 2026-09-26 session S-0027 (CLOSED) : HO-0014 re-critique of the E-0013 addendum vs R-0019 B1-B7 - NOT CLEAN on two new blocking findings (X1 truncated/interleaved addendum, X2 false parameter-count rationale); all three integrity properties HOLD
- 2026-09-26 session S-0028 (CLOSED) : R-0020 repair of the E-0013 addendum: 10 seams joined, contingency table moved, F-U1..F-U6 rejoined, X2 arithmetic inserted, X3 owners set; E-0013 stays PENDING
- 2026-09-26 session S-0029 (CLOSED) : R-0020 repair second pass: seam 8 misjoin fixed (duplicate B6 citation removed), B5 s2 empty slot named and dispositioned, verification recorded; E-0013 stays PENDING
- 2026-09-26 session S-0030 (CLOSED) : R-0021 repair of the E-0013 addendum: X4 tail rejoined, seam-8 paren closed, B5 s2 heading withdrawn, X5 recorded, append-only baseline re-labelled; E-0013 stays PENDING
- 2026-09-26 session S-0031 (CLOSED) : Y1 fix (R-0022 four pointers) + bounded +10 pointer rewrite (7 in-band rows; 6 old-ref rows exempt) + RUNNING authorisation recorded but NOT executed (status is L5, inside the hash-proved L1-428 block)
- 2026-09-26 session S-0032 (CLOSED) : R-0023 adopted - Z1 repaired (one word), contract (a)-(e) verbatim, Z2 withdrawn, Z3 re-pinned, Ruling 2 recorded; FLIP NOT EXECUTED - condition part 6 unmet (fresh adversarial critique required, owner seat may not self-verify); E-0013 stays PENDING
- 2026-09-26 session S-0033 (CLOSED) : Two stale evidence lines in E-0013 REVISED in place (Z2 prose + condition row 10) - the withdrawn figure 8ad61ccd/00a727 occurs 4x, all inside the Z2 withdrawal record, in NO live claim; orchestrator count; seam 22, 0 new; E-0013 stays PENDING

## Metrics
```
{
  "by_kind": {
    "agent_profile": 1,
    "beliefs": 1,
    "current_position": 5,
    "debate": 7,
    "decision": 11,
    "doc": 14,
    "evidence": 8,
    "experiment": 15,
    "failure": 2,
    "handoff": 16,
    "hypothesis": 17,
    "principle": 4,
    "profile": 4,
    "question": 8,
    "report": 13,
    "review": 23,
    "round_megaprompt": 2,
    "session": 33,
    "work": 7
  },
  "by_status": {
    "ACTIVE": 14,
    "CLOSED": 33,
    "COMPLETED": 31,
    "DONE": 18,
    "DRAFT": 1,
    "IN_PROGRESS": 2,
    "OPEN": 28,
    "PENDING": 6,
    "RECORDED": 2,
    "REGISTERED": 8,
    "REQUESTED": 3,
    "RESOLVED": 1,
    "SUPERSEDED": 4
  },
  "code_files": 25,
  "contradiction_candidates": 0,
  "dangling_ids": 11,
  "duplicate_candidates": 2,
  "edges_total": 3355,
  "legacy_experiments_without_pre_registration": 6,
  "open_questions": 8,
  "records_total": 191,
  "revival_candidates": 5
}

```


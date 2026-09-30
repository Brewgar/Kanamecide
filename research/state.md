# Research State (GENERATED — do not edit)

Derived from the record store by `research.py state`. Regenerate after every change.
Generated: 2026-09-30T10:07:50; schema 2.
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
- 2026-09-29 finding FND-0008 (OPEN) : F-U1 P0 (deferred by R-0019, unchanged here).** The H-0013 dataset-discrepa
- 2026-09-29 finding FND-0009 (OPEN) : F-U2 the deferred strength contract (the cost of the B1 SHRINK decision).**
- 2026-09-29 finding FND-0010 (OPEN) : F-U3 contingency routing for B3 branch X-2 (INCONCLUSIVE-BY-POWER).** Route
- 2026-09-29 finding FND-0011 (OPEN) : F-U4 the E-0011 N1 backwards-citation correction (see B5 sentence 3).** Fil
- 2026-09-29 finding FND-0012 (OPEN) : F-U5 Q-0006 readiness gate 7 (see B7).** On any terminal verdict this recor
- 2026-09-29 finding FND-0013 (OPEN) : F-U6 DN6 routing.** Flag DEC-0010:186-187's stale "Pending: independent
- 2026-09-29 finding FND-0014 (OPEN) : X1 the addendum was a truncated, interleaved document.** Ten sentences we
- 2026-09-29 finding FND-0015 (OPEN) : X2 B5's freezing rationale was arithmetically false.** The claim that fre
- 2026-09-29 finding FND-0016 (OPEN) : X3 ownership.** `owner: systems-researcher` set on E-00014 and E-00015, t
- 2026-09-29 finding FND-0017 (OPEN) : X4 DISCHARGED.**
- 2026-09-29 finding FND-0018 (OPEN) : X5 DISCHARGED.**
- 2026-09-29 finding FND-0019 (OPEN) : Z1 BLOCKING, REPAIRED: the severed sentence at L1376-L1377
- 2026-09-29 finding FND-0020 (OPEN) : Z2 CORRECTED: the unreproducible projected hash, withdrawn
- 2026-09-29 finding FND-0021 (OPEN) : Z3 CORRECTED: the boundary table, re-pinned and every figure labelled wit
- 2026-09-29 finding FND-0022 (OPEN) : Z4 the HEAD inside a committed column header (CORRECTED, S-0034)

## Metrics
```
{
  "by_kind": {
    "agent_profile": 1,
    "beliefs": 1,
    "claim": 3,
    "current_position": 5,
    "debate": 7,
    "decision": 11,
    "doc": 15,
    "evidence": 8,
    "experiment": 15,
    "failure": 2,
    "finding": 22,
    "handoff": 19,
    "hypothesis": 17,
    "principle": 4,
    "profile": 4,
    "question": 8,
    "report": 13,
    "review": 25,
    "round_megaprompt": 2,
    "session": 40,
    "work": 7
  },
  "by_status": {
    "ACTIVE": 14,
    "CLOSED": 40,
    "COMPLETED": 33,
    "DONE": 18,
    "DRAFT": 1,
    "IN_PROGRESS": 2,
    "OPEN": 53,
    "PENDING": 5,
    "RECORDED": 2,
    "REGISTERED": 8,
    "REQUESTED": 6,
    "RESOLVED": 1,
    "RUNNING": 1,
    "SUPERSEDED": 4
  },
  "code_files": 29,
  "contradiction_candidates": 0,
  "dangling_ids": 12,
  "duplicate_candidates": 2,
  "edges_total": 3936,
  "legacy_experiments_without_pre_registration": 6,
  "open_questions": 8,
  "records_total": 229,
  "revival_candidates": 5
}

```


# Research State (GENERATED — do not edit)

Derived from the record store by `research.py state`. Regenerate after every change.
Generated: 2026-09-23T21:23:05; schema 2.
Every entry is a PROJECTION of the linked records — follow them before believing.

## Current best beliefs (hypotheses with measured weight)

- **H-0004** Hand-Tuned Evaluation Baseline Sufficient for 2500+ Elo — status OPEN; confidence 0.6 (likely); tested by E-0010 [negative]. (hypotheses/H-0004-hand-tuned-evaluation-baseline-sufficient-for-2500-elo.md)
- **H-0005** Magic Bitboards with PEXT Provide >=3x NPS Speedup — status OPEN; confidence 0.45 (plausible); tested by E-00003 [unverdicted], E-0002 [unverdicted]. (hypotheses/H-0005-magic-bitboards-with-pext-provide-3x-nps-speedup.md)
- **H-0006** PEXT/magic sliders raise perft NPS 1.3-2.5x (not >=3x) at O2 vs current ray-stepping — status OPEN; confidence 0.6 (likely); tested by E-00003 [unverdicted], E-00005 [unverdicted]. (hypotheses/H-0006-pext-magic-sliders-raise-perft-nps-1-3-2-5x-not-3x-at-o2-vs-current-ray-stepping.md)
- **H-0008** Move ordering dominates raw NPS for Phase-2 time-to-depth — status OPEN; confidence 0.7 (likely); tested by E-00006 [positive], E-00007 [positive]. (hypotheses/H-0008-move-ordering-dominates-raw-nps-for-phase-2-time-to-depth.md)
- **H-0010** SPRT-based engine comparison harness is required before any version claim is trustworthy — status OPEN; confidence 0.85 (strongly supported); tested by E-00006 [positive], E-0012 [unverdicted]. (hypotheses/H-0010-sprt-based-engine-comparison-harness-is-required-before-any-version-claim-is-trustworthy.md)
- **H-0012** Search fast-path move invariants - king-capture exclusion and promo-phantom asserts — status OPEN; confidence 0.7 (likely); tested by E-00008 [positive], E-0002 [unverdicted]. (hypotheses/H-0012-search-fast-path-move-invariants-king-capture-exclusion-and-promo-phantom-asserts.md)
- **H-0013** Tapered eval plus Texel protocol - mg-eg interpolation and quiet-label holdout design — status OPEN; confidence 0.6 (likely); tested by E-0010 [negative], E-0011 [unverdicted]. (hypotheses/H-0013-tapered-eval-plus-texel-protocol-mg-eg-interpolation-and-quiet-label-holdout-design.md)
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
- 2026-09-21 session S-0007 (CLOSED) : W-0002: E-0010 decision-rule recalibration (D-0007 solved by arithmetic; DEC-0010 ACTIVE; R-0009 addendum; HO-0002 to verification-auditor; Gate-0 re-block)
- 2026-09-22 experiment E-0011 (PENDING) : E-0011 — Self-play data pipeline: resumable, provenance-carrying, deduplicated game dataset for Texel fitting
- 2026-09-22 experiment E-0012 (PENDING) : E-0012 — E-SPRT-lite comparison harness (pre-registered, DEC-0010 tiers), offline-validated on retained E-0010 data
- 2026-09-22 handoff HO-0002 (DONE) : Independently verify W-0002: D-0007 + DEC-0010 + R-0009 (E-0010 decision-rule recalibration)
- 2026-09-22 handoff HO-0003 (DONE) : Critique the E-0011 pre-registration (W-0001 step 1) BEFORE any RUNNING
- 2026-09-22 handoff HO-0004 (DONE) : Critique the E-0012 pre-registration and its offline SPRT replay validation BEFORE any RUNNING
- 2026-09-22 handoff HO-0005 (REQUESTED) : Verify W-0003: R-0013 (Round-2 AGREEMENT_MATRIX backfill) and the untouched matrix
- 2026-09-22 review R-0010 (COMPLETED) : R 0010 independent verification w 0002 d 0007 dec 0010 r 0009 occupant 4
- 2026-09-22 review R-0011 (COMPLETED) : R 0011 critique e 0011 pre registration self play data pipeline
- 2026-09-22 review R-0012 (COMPLETED) : R 0012 critique e 0012 pre registration and offline sprt replay
- 2026-09-22 review R-0013 (COMPLETED) : R 0013 round2 agreement matrix backfill
- 2026-09-22 session S-0008 (CLOSED) : HO-0002: independent verification of W-0002 (D-0007/DEC-0010/R-0009) — VERIFIED — occupant 4; Gate-0 re-block
- 2026-09-22 session S-0009 (CLOSED) : W-0001/W-0005 step 1: E-0011 + E-0012 pre-registrations filed; offline SPRT replay PASS; HO-0003/HO-0004; Gate-0 re-block
- 2026-09-22 session S-0010 (CLOSED) : HO-0003/HO-0004 critiques (R-0011/R-0012: both NOT CLEAN) + W-0003 backfill (R-0013) + HO-0005
- 2026-09-22 work W-0002 (DONE) : Recalibrate the E-0010 effect-size decision rule (D-0007 -> DEC-0010)

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
    "experiment": 12,
    "failure": 2,
    "handoff": 5,
    "hypothesis": 17,
    "principle": 4,
    "profile": 4,
    "question": 8,
    "report": 13,
    "review": 13,
    "round_megaprompt": 1,
    "session": 10,
    "work": 7
  },
  "by_status": {
    "ACTIVE": 14,
    "CLOSED": 10,
    "COMPLETED": 19,
    "DONE": 7,
    "DRAFT": 1,
    "IN_PROGRESS": 2,
    "OPEN": 30,
    "PENDING": 5,
    "RECORDED": 2,
    "REGISTERED": 8,
    "REQUESTED": 1,
    "RESOLVED": 1,
    "SUPERSEDED": 4
  },
  "code_files": 21,
  "contradiction_candidates": 0,
  "dangling_ids": 7,
  "duplicate_candidates": 2,
  "edges_total": 1600,
  "legacy_experiments_without_pre_registration": 6,
  "open_questions": 8,
  "records_total": 143,
  "revival_candidates": 5
}

```


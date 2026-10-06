# Research State (GENERATED — do not edit)

Derived from the record store by `research.py state`. Regenerate after every change.
Generated: 2026-10-06T17:20:40; schema 2.
Every entry is a PROJECTION of the linked records — follow them before believing.

## Current best beliefs (hypotheses with measured weight)

- **H-0004** Hand-Tuned Evaluation Baseline Sufficient for 2500+ Elo — status OPEN; confidence 0.6 (likely); tested by E-0010 [negative]. (hypotheses/H-0004-hand-tuned-evaluation-baseline-sufficient-for-2500-elo.md)
- **H-0005** Magic Bitboards with PEXT Provide >=3x NPS Speedup — status OPEN; confidence 0.45 (plausible); tested by E-00003 [unverdicted], E-0002 [unverdicted]. (hypotheses/H-0005-magic-bitboards-with-pext-provide-3x-nps-speedup.md)
- **H-0006** PEXT/magic sliders raise perft NPS 1.3-2.5x (not >=3x) at O2 vs current ray-stepping — status OPEN; confidence 0.6 (likely); tested by E-00003 [unverdicted], E-00005 [unverdicted]. (hypotheses/H-0006-pext-magic-sliders-raise-perft-nps-1-3-2-5x-not-3x-at-o2-vs-current-ray-stepping.md)
- **H-0008** Move ordering dominates raw NPS for Phase-2 time-to-depth — status OPEN; confidence 0.7 (likely); tested by E-00006 [positive], E-00007 [positive]. (hypotheses/H-0008-move-ordering-dominates-raw-nps-for-phase-2-time-to-depth.md)
- **H-0010** SPRT-based engine comparison harness is required before any version claim is trustworthy — status OPEN; confidence 0.85 (strongly supported); tested by E-00006 [positive], E-00014 [neutral], E-0012 [positive], E-0013 [unverdicted]. (hypotheses/H-0010-sprt-based-engine-comparison-harness-is-required-before-any-version-claim-is-trustworthy.md)
- **H-0012** Search fast-path move invariants - king-capture exclusion and promo-phantom asserts — status OPEN; confidence 0.7 (likely); tested by E-00008 [positive], E-0002 [unverdicted]. (hypotheses/H-0012-search-fast-path-move-invariants-king-capture-exclusion-and-promo-phantom-asserts.md)
- **H-0013** Tapered eval plus Texel protocol - mg-eg interpolation and quiet-label holdout design — status OPEN; confidence 0.6 (likely); tested by E-00014 [neutral], E-00015 [positive], E-0010 [negative], E-0011 [positive], E-0013 [unverdicted]. (hypotheses/H-0013-tapered-eval-plus-texel-protocol-mg-eg-interpolation-and-quiet-label-holdout-design.md)
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
- experiment **E-00014** E-00014 - TRAIN-ONLY feasibility pass for E-0013 (measure delta_star and s_d_inner; MEASUREMENT, not training) — COMPLETED. No revisit condition recorded.
- experiment **E-0010** E-EVAL — Tapered Hand-Tuned Evaluation (term-by-term self-play Elo attribution) — COMPLETED. No revisit condition recorded.
- hypothesis **H-0002-classical-stub** SUPERSEDED placeholder (renumbered to H-0003/H-0004/H-0005 on 2026-09-09) — SUPERSEDED. No revisit condition recorded.
- hypothesis **H-0002-hand-tuned-stub** Hand-Tuned Evaluation Baseline Sufficient for 2500+ Elo — SUPERSEDED. No revisit condition recorded.
- hypothesis **H-0002-magic-stub** Magic Bitboards with PEXT Provide >=3x NPS Speedup — SUPERSEDED. No revisit condition recorded.

## Recent timeline
- 2026-10-03 finding FND-0035 (OPEN) : Q-0002 pre-eval census of src/search.cpp|tt.cpp: PVS/aspiration/LMR/null-move/futility are ALL absent; ordering+qsearch exist; ORDER_STAGE is one boolean so E-0007's per-lever attribution is NOT reproducible from current source
- 2026-10-03 handoff HO-0024 (REQUESTED) : HW-3: make the Release binary digest-stable (/Brepro or equivalent) so EV-00NN pins are reproducible
- 2026-10-03 session S-0044 (CLOSED) : Round-6 umbrella for the six seat sessions T-001..T-006 (W-0006 root-scratch clean-up, D-0002..D-0006 + E-00004/E-00005 re-attestation addenda, E-0013 gate-readiness, FND-0035 census, HO-0022/HO-0023) + the normalization commit
- 2026-10-03 work W-0008 (DONE) : imem 2.1 infrastructure: INFRASTRUCTURE.md normative doc + freshness/novelty advisory surfaces + chief-architect seat
- 2026-10-03 work W-0009 (OPEN) : Digest-stable Release build (/Brepro or equivalent) so an evidence binary pin is reproducible from source, not from a preserved copy
- 2026-10-04 experiment E-00015 (COMPLETED) : E-00015 - count-only realized usable quiet yield pass for E-0013 (MEASUREMENT, not training)
- 2026-10-04 handoff HO-0016 (DONE) : Execute E-00015: count-only realized usable quiet yield pass (measurement, not training)
- 2026-10-04 handoff HO-0022 (DONE) : Spot-check 10 random rows of MAN-W0006-ROOT-SCRATCH-001 (root-scratch debt reduction)
- 2026-10-04 handoff HO-0023 (DONE) : Blockers to GO on the E-0013 gate experiments E-00014 / E-00015, with a NO-GO on both and one unblocking amendment named for E-00015
- 2026-10-04 session S-0045 (CLOSED) : wave resume: land Sponsor rulings 1-4 post-inversion (FND-0034 disposition, EV-0010/EV-0011 re-pin under DEC-0013, W-0009/HO-0024 filed, HO-0022 owner verdict, HO-0023 blocker discharges)
- 2026-10-04 work W-0006 (DONE) : Root-scratch debt reduction: shrink root_grandfathered.txt with itemized deletions
- 2026-10-05 experiment E-00014 (COMPLETED) : E-00014 - TRAIN-ONLY feasibility pass for E-0013 (measure delta_star and s_d_inner; MEASUREMENT, not training)
- 2026-10-05 session S-0046 (CLOSED) : E-0014 branch-routing correction X-1 to X-2 INCONCLUSIVE-BY-POWER + project_state staleness repair + HO-0015 executor response
- 2026-10-06 decision DEC-0014 (ACTIVE) : X-2 re-decision: E-0013 feasibility outcome routes to an Elo-scaled objective; a new pre-registration (never an edit to E-0013) owns the re-design
- 2026-10-06 experiment E-00016 (PENDING) : E-0016 - Elo-scaled Texel objective feasibility + fit (X-2 follow-up; TRAIN-only inner pass first, holdout gated)

## Metrics
```
{
  "by_kind": {
    "agent_profile": 1,
    "beliefs": 1,
    "claim": 3,
    "current_position": 6,
    "debate": 7,
    "decision": 14,
    "doc": 18,
    "evidence": 9,
    "experiment": 16,
    "failure": 2,
    "finding": 35,
    "handoff": 24,
    "hypothesis": 17,
    "principle": 4,
    "profile": 5,
    "question": 8,
    "report": 13,
    "review": 27,
    "round_megaprompt": 2,
    "session": 46,
    "work": 9
  },
  "by_status": {
    "ACTIVE": 17,
    "CLOSED": 46,
    "COMPLETED": 37,
    "DONE": 26,
    "DRAFT": 1,
    "IN_PROGRESS": 1,
    "OPEN": 41,
    "PENDING": 4,
    "RECORDED": 2,
    "REGISTERED": 9,
    "REQUESTED": 5,
    "RESOLVED": 27,
    "RUNNING": 1,
    "SUPERSEDED": 4
  },
  "code_files": 31,
  "contradiction_candidates": 0,
  "dangling_ids": 18,
  "duplicate_candidates": 2,
  "edges_total": 4742,
  "legacy_experiments_without_pre_registration": 6,
  "open_questions": 8,
  "records_total": 267,
  "revival_candidates": 6
}

```


---
id: D-0006
type: debate
title: O3 search order - quiescence before PVS-TT or PVS-TT before quiescence
status: OPEN
participants: [researcher-architect, adversarial-reviewer]
example: false
created: 2026-09-09
last_updated: 2026-09-09
---

# D-0006 — O3 search order - quiescence before PVS-TT or PVS-TT before quiescence

## Question
Inside the O3 plain-alpha-beta build, which comes first: quiescence search (stand-pat +
captures/promotions + delta pruning) or the PVS + transposition-table deltas (H-0009)?
Both are needed; the order determines which measurements are interpretable.

## Agent A — researcher-architect (quiescence first)
Position: quiescence first, then PVS-only, then TT-only, then both.
Confidence: 0.7 (likely — methodology argument).
Argument: without quiescence every leaf eval is horizon-noisy, so NO Elo or score-based
comparison (including PVS/TT time-to-depth quality judgments and later SPRT games) is
interpretable. Node-count deltas for PVS/TT can still be measured after quiescence; the
reverse order (PVS/TT node counts on noisy leaves, then quiescence changing every leaf)
invalidates the earlier numbers. Quiescence also unblocks the first playable engine.

## Agent B — (open; implementation-engineer / adversarial-reviewer invited: PVS+TT first)
Position: (awaiting) PVS+TT node-reduction is measurable on fixed-depth node counts
without any quiescence, and quiescence confounds node counts (variable leaf expansion).
Confidence: —
Argument: (none yet; the plausible counter is that pure node-count attribution is
cleaner before quiescence adds variable-depth leaves.)

## Agent C — adversarial-reviewer (2026-09-09)
Position: Agree with A's CONCLUSION (quiescence first, conf 0.65) but not A's stated rationale
as the primary argument. The "no comparison is interpretable without quiescence" argument is
decisive for eval-delta and SPRT stages, NOT for the first-vs-random milestone (any search beats
random; leaf noise does not threaten +200 vs random). The decisive argument is B's own format:
PVS/TT deltas measured on a fixed-depth no-quiescence tree do not carry forward once quiescence
changes every leaf — you re-measure anyway, so B's order saves no work and delays the first
playable, score-interpretable engine.
Amendment to the proposed resolution: the "crossover" experiment as written is vacuous on its
own metric — both paths converge to the IDENTICAL final configuration by construction, so "if
identical, A wins on methodology" is a tie-break, not evidence. Pre-register a measurable proxy
instead: (i) days-to-first-interpretable-SPRT-result along each path; (ii) final fixed-depth
nodes/TTD matrix at each stage; (iii) keep fixed-depth plain-AB node counts as regression pins
WHILE quiescence is developed (quiescence bugs corrupt leaf counts silently). Razoring/delta-prune
margin must be scoped in the same record. If the two paths differ materially on (i), the faster
one wins; if identical, A's tie-break applies.
Confidence: 0.65 (quiescence-first ordering); 0.8 (fix the crossover decision rule).

## Points of Agreement
Both quiescence and PVS+TT are required in O3; staged deltas with nodes/time-to-depth at
each step; fixed position set + fixed hash size throughout.

## Points of Disagreement
Whether leaf-quality (A: quiescence first) or node-count purity (B: PVS+TT first) governs
the build order.

## Evidence Available
No search exists; H-0009 scopes the PVS/TT deltas; H-0008 scopes ordering deltas. Engine
literature builds quiescence into the baseline before measuring anything score-based.

## Evidence Missing
O3 plain-alpha-beta baseline itself; quiescence node-expansion profile on this movegen;
PVS null-window success rate with/without quiescence.

## Proposed Resolution Experiment
Crossover inside O3: plain-AB baseline → add quiescence → add PVS+TT (path 1) vs
plain-AB → add PVS+TT → add quiescence (path 2, scratch branch). Compare final
nodes/TTD/SPRT; if identical, order was cosmetic and A wins on methodology (playable
engine sooner). Decision rule pre-registered before building.

## Resolution
(unresolved — do not force consensus)

## Date
2026-09-09
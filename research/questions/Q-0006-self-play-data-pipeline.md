---
id: Q-0006
type: question
title: "Can the E-0011 self-play pipeline produce a deduped, provenance-carrying dataset that trains an eval that beats the hand-tuned one?"
status: OPEN
priority: high
example: false
created: 2026-09-19
last_updated: 2026-09-24
hypotheses: [H-0004, H-0013]
experiments: [E-0010, E-0011, E-0012]
suggested_experiments: ["E-0011: >=1000 legal, deduplicated, provenance-carrying games; resume-from-checkpoint adds no duplicates", "Next Texel fitting experiment (expected E-0013): use only the verified E-0011 dataset, game-split holdout, fitted_params_sha256, and fresh-game overlap=0 gate"]
depends_on: []
blocked_by: [W-0001, W-0005]
answers: null
---

# Q-0006 — Self-play data pipeline -> Texel -> NNUE (the data flywheel)

## Question
The engine is now a player (O3d + E-0010 eval, +116 Elo over material-only). The missing
compounding asset is the data loop: self-play -> dedup/dataset -> tune (Texel) / train
(NNUE) -> promote -> repeat. Can the E-0011 pipeline generate dataset-grade games, and is
the resulting label quality good enough to beat the hand-tuned eval as a training target?

## Why it matters
Every later learned-eval and policy claim depends on this loop's data quality and
reproducibility (the E-0010 duplicate-games and dead-process lessons are load-bearing).

## What we know
- E-0010 produced 1240 legal, independent, provenance-carrying games locally — the pipeline
  exists in prototype form (e0010_match2.py + report).
- The pipeline's only correctness problems (duplicate openings, EvalStage no-op, bestmove
  stall) are documented and fixed (R-0003 F4/F5/F6, E-0010).

## What is NOT known
- Whether >=1000 games at a playable TC runs cleanly to completion under runjob.py
  (with heartbeat/resume) at <=2 concurrent engine pairs.
- Whether the resulting labels train a net that beats hand-tuned eval (H-0004 unresolved).

## Related records
- W-0001 (this work item), E-0010, H-0013 (Texel holdout design), PR-0003.

## State addendum: first-training readiness (2026-09-24)

E-0011 now has a 1,000-game owner-side pinned artifact set and all six dataset gates PASS,
but W-0001 remains open solely for independent HO-0009 verification. E-0012 is a separate
pre-registered E-SPRT-lite harness validation; its live known-difference and null-control
campaigns remain open under W-0005. No H-0013 fitted parameters, fitted-parameter hash,
or downstream strength result exists. `PENDING_H-0013` in E-0011 is a dependency label,
not an experiment ID.

Q-0006 therefore remains OPEN and `blocked_by` W-0001/W-0005. The first training/fitting
experiment is a newly filed record (expected E-0013, CLI authoritative), not E-0012. The
prepared but inactive operating plan is
`research/AGENT_MEGAPROMPT_TRAINING_READINESS.md`.

### Official first-training readiness gates

1. Gate-0 engine tests and research `validate` pass.
2. HO-0009 yields a non-owner verification review and W-0001 is DONE/VERIFIED.
3. E-0012 live validation passes its pre-registered controls and W-0005 is independently VERIFIED.
4. A new H-0013 experiment is PENDING with extraction, labels, game-split holdout, deterministic
     seed, power, decision rules, provenance, and explicit failure outcomes.
5. Its adversarial critique is CLEAN or all blocking findings are discharged before RUNNING.
6. The fit consumes only the verified E-0011 dataset; its later fresh decision games use a
   distinct salt and report `training_game_overlap = 0` under the pinned normalization.
7. The fit produces and pins `fitted_params_sha256`, loads exactly that artifact into the
   candidate, and receives independent verification. No adoption or strength claim precedes it.

## History

- 2026-09-19 — opened after E-0010 established the prototype data/match loop.
- 2026-09-24 — E-0011 artifact generation closed owner-side; HO-0009 and W-0005 live validation
  remain gates. First-training readiness prompt prepared; E-0012/E-0013 routing clarified.

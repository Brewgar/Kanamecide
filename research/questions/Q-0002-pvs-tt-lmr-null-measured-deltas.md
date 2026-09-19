---
id: Q-0002
type: question
title: "Can PVS + TT + LMR/null-move be added as measured deltas on O3d (O3e), and how much do they cut nodes?"
status: OPEN
priority: high
example: false
created: 2026-09-19
last_updated: 2026-09-19
hypotheses: [H-0009]
experiments: []
suggested_experiments: ["E-PVS-TT: TT-only, PVS-only, both on the E-00007 11-position set; disambiguate the two contributions"]
depends_on: []
blocked_by: []
answers: null
---

# Q-0002 — O3e: measured PVS / LMR / null-move / aspiration deltas

## Question
Phase-2 search stopped at O3d (ordering + quiescence + TT + ID + time control). The
literature-standard selective heuristics (PVS null-window, LMR, null-move pruning,
aspiration windows) are deliberately absent. Which of them cut nodes-to-depth on THIS
engine, by how much, and do their contributions survive independent deltas (not the
confound that bites H-0009 if TT and PVS land together)?

## Why it matters
This is the next ordered strength lever after ordering (–91.2% nodes at O3b) and qsearch
(+mates, −phantoms at O3c). Ordering compounds with depth; pruning moves the constant.

## What we know so far
- TT/ID already give 9.51× fewer nodes vs the O3c single-shot on the same positions with
  identical best moves (E-00009); TT hit-rate 27–44%.
- MVV-LVA is the dominant ordering lever (84%), killers +6.5pp, history +0.7pp (E-00007).

## What is NOT known
- Whether PVS/LMR/NMP pay once ordering + qsearch + TT exist (they can interact).
- Whether a null-window bug risk is worth it before an SPRT harness can certify a real
  strength gain (H-0010).

## Dependencies
- H-0010 (E-SPRT-lite) should exist before any strength claim; node/TTD deltas can be
  measured first without strength claims.

## Related records
- H-0009, E-00006/7/8/9, D-0006 (build order).
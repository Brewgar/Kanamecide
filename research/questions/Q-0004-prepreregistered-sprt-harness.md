---
id: Q-0004
type: question
title: "Can a pre-registered two-tier SPRT harness decide every engine-delta claim against a calibrated bar?"
status: OPEN
priority: high
example: false
created: 2026-09-19
last_updated: 2026-09-19
hypotheses: [H-0010]
experiments: []
suggested_experiments: ["E-SPRT-lite: screening delta~20 Elo + regression delta=5, LLR +-2.944, cap 30000, crash=loss, post-cap INCONCLUSIVE"]
depends_on: []
blocked_by: []
answers: null
---

# Q-0004 — Standing pre-registered comparison harness (E-SPRT-lite)

## Question
Today every A/B strength claim still rides an ad-hoc harness. Can we stand up the ratified
two-tier SPRT harness (screening δ≈20 Elo; regression δ=5, α=β=0.05, LLR ±2.944, game cap
with post-cap INCONCLUSIVE, trinomial draws, balanced colors, crash=loss) so that every
future "B is stronger than A" claim is a decision, not an argument?

## Why it matters
This is the single most leveraged piece of measurement infrastructure left. It also decides
H-0010 (two-tier SPRT required before version claims are trusted).

## What we know so far
- E-0010's honest FAIL was only possible because a pre-registered bar existed; the harness is
  what raises every other experiment to that standard.
- The two-tier parameterization was argued in R-0002 Q2 and ratified in H-0010's addendum.

## What is NOT known
- Whether the regression tier (δ=5) is affordably decidable in wall-time on this machine
  (the reason for the ~30k cap), and whether the known-difference validation (stage-6 vs
  stage-0 must be called correctly) passes.

## Related records
- H-0010 (two-tier protocol), W-0005 (this work item), R-0002 Q2 (parameter derivation),
  E-0010 (the bar it must reproduce the sign of).
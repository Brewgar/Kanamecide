---
id: Q-0001
type: question
title: "Which eval terms actually earn their cost, and should mobility/tempo be re-tuned or removed?"
status: OPEN
priority: high
example: false
created: 2026-09-19
last_updated: 2026-09-19
hypotheses: [H-0004, H-0013]
experiments: [E-0010]
suggested_experiments: ["E-TEXEL: Texel-fit the tapered terms on qsearch-resolved positions; compare mobility/tempo refit vs drop"]
depends_on: [W-0002]
blocked_by: []
answers: null
---

# Q-0001 — Which eval terms actually earn their cost?

## Question
E-0010's per-term ladder shows the strength is front-loaded: taper + PST carry +82 of +116 Elo
by stage 2; pawn structure adds +22; mobility (−3.7) and tempo (−11.5) are NON-positive at
this time control with CIs crossing zero. Which terms are worth their cost, and does re-tuning
the weak terms (or removing them) beat adding more?

## Why it matters
The largest, cheapest known strength headroom is inside the current eval: re-fit its weak
terms before adding any machinery.

## What we know so far
- +116.1 Elo over material-only at LOS 100%, CI [+70.8, +163.5], N=240 (E-0010, honest FAIL
  of the ≥150 bar — direction is strongly positive).
- Mobility and tempo are non-positive increments (CIs cross zero) — "no evidence of gain",
  not proven harm.

## What is NOT known
- Whether the weak terms are mis-tuned (weights) or structurally unhelpful at this depth/TC.
- Whether Texel-on-qsearch positions (H-0013) fixes them.

## Dependencies
- W-0002 (recalibrated decision rule) should settle the screening bar first; E-0011 provides data.

## Related records
- E-0010 (measured ladder), H-0004 (eval-sufficiency hypothesis), H-0013 (Texel protocol).
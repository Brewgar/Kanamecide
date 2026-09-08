---
id: H-0001
type: hypothesis
title: "PVS + transposition table materially reduces time-to-depth vs plain alpha-beta"
status: OPEN
confidence: 0.65
priority: high
example: true
created: 2026-09-08
last_updated: 2026-09-08
agents_supporting: [researcher-architect, implementation-engineer]
agents_opposing: [adversarial-reviewer]
tags: [search, alpha-beta, pvs, transposition-table]
---

# H-0001 — PVS + transposition table materially reduces time-to-depth vs plain alpha-beta

> ⚠️ **EXAMPLE / MOCK DATA.** This file demonstrates the hypothesis format only.
> Nothing here is an established conclusion or real project history. Replace or delete it.

## Question
Does principal-variation search with a transposition table reach the same depth with
fewer nodes than a plain alpha-beta search on the Phase 2 engine?

## Hypothesis
PVS + TT cuts roughly 15–30% of nodes per fixed depth on quiet middlegame positions,
because TT cutoffs skip re-searches and PVS narrows every non-PV node to a null window.

## Why We Think This Might Work
Well documented in the literature and in most open-source engines; the Phase 2 roadmap
already plans a transposition table and PVS.

## Counterarguments
Move-ordering quality matters; with weak ordering the expected savings shrink.
(All figures are illustrative — not measured here.)

## Agents Supporting
researcher-architect, implementation-engineer

## Agents Opposing
adversarial-reviewer (insists on measuring before believing)

## Confidence
0.65

## Proposed Experiment
E-0001 — implement alpha-beta first, then add PVS + TT, and compare time-to-depth.

## Required Metrics
Nodes and wall-clock seconds to fixed depth, across a fixed position set.

## Status
OPEN

## Result
(none — not yet run)

## Conclusion
(none — this is example content)
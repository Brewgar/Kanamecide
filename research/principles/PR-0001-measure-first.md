---
id: PR-0001
type: principle
title: "Measure first; no claim without a run"
kind: meta
status: ACTIVE
scope: [process]
evidence: [E-0002, E-0010]
example: false
created: 2026-09-19
last_updated: 2026-09-19
---

# PR-0001 — Measure first; no claim without a run

## Principle
A claim about the engine (a speedup, a strength delta, an eval term's effect) is not a
fact until an experiment with a pre-registered decision rule, sufficient power, and a
valid sample has measured it. "It compiles" proves syntax only. Agent confidence is a
belief, never evidence.

## Why it holds (evidence/derivation)
- F1 (R-0003): "done" claimed after a compile with no run — the measurement did not exist.
- E-0010: the pre-registered >=150 Elo bar failed honestly (+116.1 at LOS 100%); the
  result, not the confidence, changed the record.
- R-0002/R-0003: measured-only discipline is the project's strongest asset.

## When it applies / limits
- Every strength/performance claim. Does NOT apply to knowledge claims provable by
  construction (a derivation, a correctness proof, a code inspection that names lines).

## When it might change (revisit)
- If a formal proof or a reproducible static analysis can substitute for a measurement
  (e.g. perft counts are proofs of legality, not measurements) — then the claim's
  epistemic class is Proof, not Experiment, and the record should say so.

## Related records
- R-0003 (F1), E-0010, SYSTEM.md Gate 2.
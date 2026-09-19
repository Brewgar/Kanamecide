---
id: PR-0002
type: principle
title: "One protected home for every sacred fact"
kind: meta
status: ACTIVE
scope: [memory]
evidence: []
example: false
created: 2026-09-19
last_updated: 2026-09-19
---

# PR-0002 — One protected home for every sacred fact

## Principle
A fact that everything else depends on (the certified perft counts, the measurement-cover
binary sha, a decision rule) lives in EXACTLY ONE place, and the tooling asserts it. A
second, hand-maintained copy is a corruption channel: when the owner's web edit emptied
README.md, the perft table survived only by luck (a second copy existed) — see R-0003 F12.

## Why it holds (evidence/derivation)
- R-0003 F12: two parallel perft tables (README + project_state) — one was silently destroyed.
- DEC-0009 #8: project_state.md §Certified Perft Anchors is the single protected home and
  `validate` asserts every number.

## When it applies / limits
- Facts of record (sacred anchors, measurement provenance). Does NOT forbid DERIVED
  renderings (state.md, index.md), which are recomputable and carry the GENERATED banner —
  a derived copy is a pointer, not a second truth.

## When it might change (revisit)
- If the store grows until one file becomes a merge-conflict hotspot at scale; then the
  single home moves to a canonical machine record everything derives from — the PRINCIPLE
  (one truth, everything derives) survives the mechanism change.

## Related records
- R-0003 (F12), DEC-0009, project_state.md.
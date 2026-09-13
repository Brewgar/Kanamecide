---
id: H-0006
type: hypothesis
title: PEXT/magic sliders raise perft NPS 1.3-2.5x (not >=3x) at O2 vs current ray-stepping
status: OPEN
confidence: 0.6
priority: high
example: false
created: 2026-09-09
last_updated: 2026-09-09
agents_supporting: [researcher-architect]
agents_opposing: []
tags: [bitboard, pext, magic, performance, movegen, nps]
---

# H-0006 — PEXT/magic sliders raise perft NPS 1.3-2.5x (not >=3x) at O2 vs current ray-stepping

## Question
How much perft NPS does replacing the ray-stepping sliders (`src/bitboard.cpp:54-72`) with
PEXT/magic lookups actually add, on THIS engine at /O2, given that the current generator is
already measured at ~43-50 Mnps (startpos d5 ~47 Mnps; E-00003)?

## Hypothesis
PEXT/magic sliders raise perft NPS by ~1.3-2.5x at /O2 — materially less than H-0005's
`>=3x` claim (which would require ~120-140 Mnps and is implausible vs both this measured
baseline and typical literature PEXT-vs-ray gains on perft-only workloads). Confidence 0.6
(plausible-to-likely). Falsifiable bounds: <1.0x = H-0006 wrong (rays as fast as PEXT here);
>=3x = H-0005 restored.

## Addendum (adversarial-reviewer, 2026-09-09) — falsification bound alignment

The "Falsifiable bounds: <1.0x" stated above conflicts with D-0003's decision rule
("falsification of H-0006 requires ratio < 1.3") and with H-0006's own claimed range of
1.3-2.5x. Since H-0006 claims a *range* (1.3-2.5x), the record-consistent falsification
bound is ratio < 1.3 (the lower edge of the claimed range) — NOT < 1.0x. Pre-register
exactly one partition before E-PEXT (adopted from D-0003 / R-0002 Q3); the <1.0x wording
here is superseded by that partition. Full review: R-0002.

## Why We Think This Might Work
PEXT/magic is classically faster than ray stepping, and `attacked_by` + movegen call slider
attacks per square. The bounds are tight because the baseline is already fast: only the
slider fraction of perft CPU time can be reduced, so 3x overall requires sliders to be
~75%+ of NPS attribution today.

## Counterarguments
- The EP probe's `Board b_nc` copy (H-0007) or mailbox maintenance may dominate, not rays.
- MSVC codegen at /O2 may already hoist ray loops well; PEXT is not a silver bullet on this
  toolchain. Actual magnitude is UNKNOWN until E-PEXT runs.

## Agents Supporting
researcher-architect (0.6, revised from H-0005's 0.7 on `>=3x`; measurement-informed).

## Agents Opposing
(open — H-0005's original >=3x claim is the opposing position, filed as D-0003.)

## Confidence
0.6 (direction likely; magnitude range plausible; both to be measured by E-PEXT).

## Proposed Experiment
E-PEXT (after E-0002 in-tree bench): swap `rook_attacks`/`bishop_attacks` to PEXT/magic,
require bit-identical full perft suite, then rerun the /O2 NPS table (startpos d5, kiwipete
d4, cpw6 d4; 5 reps). Compare vs E-00003 baseline.

## Required Metrics
Perft counts (must be identical), NPS at fixed flags/hash, ratio to E-00003 baseline, CPU
frequency/idle conditions recorded.

## Status
OPEN

## Result
(none)

## Conclusion
(none)
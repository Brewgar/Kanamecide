---
id: H-0005
type: hypothesis
title: Magic Bitboards with PEXT Provide >=3x NPS Speedup
status: OPEN
confidence: 0.45
priority: high
example: false
created: 2026-09-09
last_updated: 2026-09-09
agents_supporting: [researcher-architect]
agents_opposing: []
tags: [bitboard, pext, magic, performance, movegen]
---

# H-0005 — Magic Bitboards with PEXT Provide >=3x NPS Speedup

## Measurement Addendum (2026-09-09, researcher-architect)

E-00003 measured the baseline that was UNKNOWN when this hypothesis was filed: at /O2 the
current ray-stepping legal movegen sustains ~43-50 Mnps on this machine (startpos d5 ~47.0-
47.4 Mnps, kiwipete d4 ~43.1 Mnps, cpw6 d4 ~50.0-50.4 Mnps, 3 reps). A `>=3x` PEXT gain now
implies >~140 Mnps, which is implausible for a slave-attack swap (only the slider-attributable
fraction of perft time can be recovered). **Revised expectation: 1.3-2.5x** — filed as H-0006
(conf 0.6); this H-0005's `>=3x` bar is retained as the falsification upper bound and its
confidence is revised 0.7 -> 0.45. See D-0003. Falsification of H-0005 requires E-PEXT NPS
ratio >= 3.0 at identical flags; falsification of H-0006 requires ratio < 1.3.

## Question

Does replacing ray-stepping sliders (src/bitboard.cpp:54-72) with PEXT/magic
lookups materially raise perft NPS on this engine at identical node counts?

## Addendum (adversarial-reviewer, 2026-09-09) — falsification bound correction + full partition

The Measurement Addendum above contains a spec error: "Falsification of H-0005 requires E-PEXT
NPS ratio >= 3.0" has the direction backwards. H-0005 claims ">=3x", so a ratio >= 3.0 CONFIRMS
H-0005 (it is D-0003's restoration condition), and a ratio < 3.0 FALSIFIES the ">=3x" claim.
Correct, pre-registered partition for E-PEXT (at /O2, bit-identical perft counts, within-session
paired runs, ratio + CI):

- ratio >= 3.0 → H-0005 CONFIRMED; H-0006 rejected.
- 1.3 <= ratio < 3.0 → H-0005 falsified; H-0006 supported.
- 1.0 < ratio < 1.3 → both magnitude claims falsified (direction "PEXT >= ray" survives).
- ratio <= 1.0 → H-0005 and H-0006 both falsified.

Also note the conflict between H-0006's own text ("<1.0x = H-0006 wrong") and D-0003's
("falsification of H-0006 requires ratio < 1.3"): H-0006's stated range is 1.3-2.5x, so the
record-consistent bound is ratio < 1.3 (or > 2.5) for the range claim. Adopt exactly one rule.
Confidence: 0.85 (protocol requirement); 0.5 (1.3-2.5x magnitude). Full review: R-0002.

## Hypothesis
Yes (likely, 0.7): >=3x perft NPS on startpos/Kiwipete/CPW6 with BIT-IDENTICAL perft
counts across the full suite. PEXT is fast on Zen 5 (unlike older AMD); ray loops are
branch-heavy per square.

## Why We Think This Might Work
Documented engine literature + Zen 5 PEXT throughput; sliders dominate attacked_by +
movegen cost (call sites: movegen sliders, attacked_by rays, castling checks).

## Counterarguments
Current NPS is UNKNOWN (no bench, /Od flags); mailbox/bitboard maintenance may
dominate instead; init/table footprint costs; 3x threshold may not hold at /O2.

## Agents Supporting
researcher-architect (0.7, likely — class evidence, not measured here).

## Agents Opposing
(none.)

## Confidence
0.7 (likely).

## Proposed Experiment
O2/E-PEXT: (1) add --bench + fix /O2 baseline FIRST (O1); (2) swap sliders; (3) full
perft suite bit-compare; (4) 5-rep NPS table before/after on same binary flags.

## Required Metrics
Perft node counts (must match exactly), wall seconds, NPS, binary flags + hash.

## Status
OPEN

## Result
(none.)

## Conclusion
(none)

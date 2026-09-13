---
id: H-0002-magic-stub
type: hypothesis
title: Magic Bitboards with PEXT Provide >=3x NPS Speedup
status: SUPERSEDED
confidence: 0.7
priority: high
example: false
created: 2026-09-09
last_updated: 2026-09-09
agents_supporting: [researcher-architect]
agents_opposing: []
tags: [bitboard, pext, magic, performance, movegen]
---

# H-0002-magic STUB — SUPERSEDED (content moved to H-0005 on 2026-09-09)

Content moved to H-0005-magic-bitboards-with-pext-provide-3x-nps-speedup.md.
Retained for filename history only. Body archived below for provenance; do not cite.

---

# ARCHIVED BODY (moved to H-0005; status SUPERSEDED)

## Question
Does replacing ray-stepping sliders (src/bitboard.cpp:54-72) with PEXT/magic
lookups materially raise perft NPS on this engine at identical node counts?

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
SUPERSEDED (moved to H-0005; see stub header).

## Result
(none.)

## Conclusion
(none)
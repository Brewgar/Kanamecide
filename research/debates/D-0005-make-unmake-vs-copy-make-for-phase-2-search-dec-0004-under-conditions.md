---
id: D-0005
type: debate
title: make-unmake vs copy-make for Phase 2 search: DEC-0004 under conditions
status: OPEN
participants: [adversarial-reviewer, researcher-architect]
example: false
created: 2026-09-09
last_updated: 2026-09-09
---

# D-0005 — make-unmake vs copy-make for Phase 2 search: DEC-0004 under conditions

## Question
DEC-0004 chose make/unmake for move application. For Phase 2 alpha-beta search at depths >=10,
does copy-make outperform make-unmake on Ryzen 9700X? Should DEC-0004 be revisited for the
search hot path?

## Agent A — researcher-architect (open question)
Position: make/unmake is correct for perft and shallow search, but copy-make may win at depth >=10.
DEC-0004 should be revisited conditionally — keep make/unmake as the reference, allow copy-make
in the search hot path if measurement justifies it.
Confidence: 0.55 (plausible, not likely — measurement required).
Argument: At deep depths, copy-make's simpler control flow (memcpy + flat apply) and better
cache locality may dominate make/unmake's complex undo path (promotion/EP/castling branches).
The ~312 B Board copy fits in L1; memcpy is fast on Zen 5. Filed as H-0011.

## Agent B — DEC-0004 (existing decision)
Position: make/unmake is the project's chosen approach for all contexts.
Confidence: (decision, not a belief — but engine literature strongly favors make/unmake).
Argument: Stockfish, Ethereal, and virtually all top engines use make/unmake. It avoids memory
allocation and cache pressure. The ~312 B Board copy adds up at ~45 Mnps. The collective
experience overwhelmingly favors make/unmake.

## Agent C — adversarial-reviewer (2026-09-09)
Position: Keep make/unmake as the O3 default; run E-COPYMAKE as a SIDE microbenchmark, not a
blocking gate. H-0011's enabling argument ("~312 B fits in L1; memcpy is cheap") misses the
multiplier: at ~45 Mnps a per-node 312 B board copy is ~14 GB/s of memcpy traffic plus cache
line pressure, versus O(undo-bytes) writes for make/unmake. The crossover question is real but
the priors favor make/unmake (0.6); copy-make winning anywhere in depth 10-14: 0.4. Pre-register
the rule before measuring: copy-make wins only if >= 5% time-to-depth advantage at a depth with
>= 10 s TTD, reproduced on both suites; otherwise DEC-0004 stands. Both approaches agree on
search results (correctness is out of scope) — the debate is purely cost of attribution, so a
failing measurement must be allowed to settle it without drama.
Confidence: 0.6 (make/unmake stays better in 10-14); 0.4 (crossover exists in range).

## Points of Agreement
- Both approaches produce identical search results (correctness is not in question).
- The question is purely about performance (time-to-depth, NPS).
- Measurement on this specific hardware is required to resolve the debate.
- The reference perft generator should keep make/unmake (simplicity, correctness).

## Points of Disagreement
- Whether a crossover depth exists where copy-make wins.
- Whether the crossover depth (if it exists) is within the target search range (depth 10-14).
- Whether to implement both paths and measure, or to follow engine literature (make/unmake).

## Evidence Available
- DEC-0004 (make/unmake chosen).
- H-0011 (copy-make hypothesis, 0.55 confidence).
- Engine literature (overwhelmingly favors make/unmake).
- No measurements on this hardware exist.

## Evidence Missing
- E-COPYMAKE: time-to-depth and NPS for both approaches at depths 6, 8, 10, 12, 14 on Ryzen 9700X.
- Cache miss and branch misprediction rates for each approach.
- Profile of make/unmake undo path vs copy-make memcpy path.

## Proposed Resolution Experiment
E-COPYMAKE: Implement both make/unmake and copy-make search paths. Measure time-to-depth and
NPS at depths 6, 8, 10, 12, 14 on startpos and a tactical suite. Report the crossover depth
(if any). If copy-make wins at any target depth, revisit DEC-0004 for the search hot path
(make/unmake retained as reference).

## Resolution
(unresolved — measurement required)

## Date
2026-09-09
2026-09-09
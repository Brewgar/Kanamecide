---
id: D-0003
type: debate
title: H-0005 >=3x PEXT speedup vs measured ~47 Mnps perft baseline
status: OPEN
participants: [researcher-architect, adversarial-reviewer]
example: false
created: 2026-09-09
last_updated: 2026-09-09
---

# D-0003 — H-0005 >=3x PEXT speedup vs measured ~47 Mnps perft baseline

## Question
How much perft NPS does PEXT/magic actually add on this engine, now that the /O2 baseline is
measured (~43-50 Mnps; E-00003)? Does H-0005's `>=3x` claim remain credible?

## Agent A — researcher-architect (prior position, now revised)
Position: PEXT/magic sliders will give >=3x perft-NPS at identical node counts.
Confidence: 0.7 (as filed in H-0005, 2026-09-09 morning; pre-measurement).
Argument: documented engine literature + Zen 5 PEXT throughput; sliders dominate attacked_by
and movegen call sites; ray loops are branch-heavy per square.

## Agent B — researcher-architect (current position, measurement-informed)
Position: magnitude will be ~1.3-2.5x, NOT >=3x. A 3x gain would require ~>140 Mnps (from
the measured ~47 Mnps startpos d5 baseline), which is implausible for a slave-attack swap on
a perft workload; only the slider-attribute share of perft time can be recovered.
Confidence: 0.6 for the 1.3-2.5x range; 0.45 retained for the >=3x bound.
Argument: E-00003 demonstrates the premise (the generator is ALREADY fast); H-0005 was filed
while NPS was UNKNOWN, so its 3x bar was a guess, not a measurement. PEXT is table-lookup
(cheap) but the current rays are already short loops on mostly-open boards; the delta is
bounded by profiling before/after, not by canon.

## Agent C — (open; systems-researcher / adversarial-reviewer / implementation-engineer invited)
Position: (awaiting either defense of the 3x bar or independent profiling.)
Confidence: —
Argument: — (both A and B agree the resolution is empirical; the disagreement is the prior).

## Agent D — adversarial-reviewer (2026-09-09)
Position: Endorse Agent B's revision as the working prior (1.3-2.5x, conf 0.5 for me — the
slider-attributable share of perft time is unprofiled, so even the upper end is a guestimate;
the >=3x arithmetic is sound: it requires >~140 Mnps total, i.e. sliders ≈ 70%+ of time today).
The decision rule is INCOMPLETE and the records conflict. Pre-register exactly one partition
before E-PEXT, at /O2, counts bit-identical, within-session paired runs (alternate binaries in
one loop) reporting ratio + CI:
- ratio >= 3.0 → H-0005 CONFIRMED (>=3x); H-0006 rejected.
- 1.3 <= ratio < 3.0 → H-0005 falsified; H-0006 supported.
- 1.0 < ratio < 1.3 → both magnitude claims falsified (direction survives).
- ratio <= 1.0 → both hypotheses falsified.
E-00003's table is cross-session and unpinned (per-rep spread <1% but background load
uncontrolled); a point ratio near 1.3 or 3.0 is not a decision — report the CI.
Confidence: 0.5 (range), 0.85 (partition/protocol requirement).
Argument: The H-0005 addendum sentence "Falsification of H-0005 requires ratio >= 3.0" is
backwards (>=3x CONFIRMS H-0005, per this rule). H-0006's own "<1.0x" bound contradicts D-0003's
"<1.3". Fix both records before E-PEXT runs.

## Points of Agreement
- E-PEXT must first have a fixed-flag bench (E-0002) and require a bit-identical perft suite.
- The measured /O2 baseline (E-00003) is the correct comparison point; /Od numbers are
  compiler noise for this question (fixed by E-0002).

## Points of Disagreement
- The plausible gain interval: >=3x (A, prior) vs 1.3-2.5x (B, current). Static reasoning
  alone cannot settle it; only the A/B NPS delta at fixed flags can.

## Evidence Available
E-00003: /O2 perft NPS = startpos d5 ~47.0-47.4 Mnps (3 reps), kiwipete d4 ~43.1 Mnps,
cpw6 d4 ~50.0-50.4 Mnps; /Od ~19-21 Mnps (ratio 2.1-2.4x). H-0005 (prior claim), H-0006
(revised claim).

## Evidence Missing
An E-PEXT binary: bit-identical perft + NPS at /O2 (5 reps, fixed flags/hash). No profile
of slider share in perft time exists.

## Proposed Resolution Experiment
E-PEXT after E-0002: swap rook/bishop attacks to PEXT/magic, bit-compare full perft suite,
rerun E-00003 table. Decision rule: NPS ratio in [1.3, 2.5] -> H-0006 supported, H-0005's
3x falsified; ratio >= 3x -> H-0005 restored, revise H-0006.

## Resolution
(unresolved — do not force consensus)

## Date
2026-09-09
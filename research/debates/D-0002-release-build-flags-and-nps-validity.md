---
id: D-0002
type: debate
title: Release build flags invalidate current NPS claims and O2-binary provenance
status: OPEN
participants: [researcher-architect, adversarial-reviewer]
example: false
created: 2026-09-09
last_updated: 2026-09-09
---

# D-0002 — Release build flags invalidate current NPS claims and O2-binary provenance

## Question
Can any NPS or speedup number be trusted while CMakeLists.txt forces /Od /JMC /DEBUG
on Release, and while build/Release/kana_o2.exe (253952 bytes vs kana.exe 83968) has
unknown provenance?

## Agent A — researcher-architect
Position: No. All NPS/speedup figures are UNKNOWN until O1 (bench + /O2 baseline +
binary-hash logging) lands. The /Od Release flag is demonstrated (CMakeLists.txt:16).
kana_o2.exe exists but its flags/source are unrecorded — do not cite it as evidence.
Confidence: 0.9 (demonstrated premises, conservative conclusion).
Argument: Codegen dominates perft NPS; comparing unoptimized binaries measures the
compiler, not the algorithm. Fix flags first, then PEXT, then search deltas.

## Agent B — (open; implementation-engineer/systems-researcher invited)
Position: (awaiting counterargument: e.g. relative deltas at /Od still rank-order
optimizations.)
Confidence: —
Argument: (none yet.)

## Agent C — adversarial-reviewer (2026-09-09)
Position: The "trust vs distrust ALL NPS numbers" dichotomy is false. E-00003 established a
provisional /O2 baseline (~47 Mnps startpos d5) that I re-verified this session by re-running
the same harness fresh: /O2 = 46.6-50.5 Mnps, /Od = 18.9-21.0 Mnps, ratio ~2.3x, all counts
bit-identical. Two-tier rule: provisional numbers may be cited ONLY as provisional (~2 sig figs,
unpinned, single machine); any number that changes a roadmap or enters project_state.md must be
E-0002-certified (5 reps, logged flags + binary hash). /Od-relative deltas are screening-only,
for rank-order, on the untested assumption that codegen acts as a near-uniform multiplier.
kana_o2.exe stays excluded until its provenance is documented, or it is deleted from claims.
Confidence: 0.85 on the two-tier certification rule; 0.7 that /Od ranking transfers (assumption,
not demonstrated).
Argument: "No NPS claim is interpretable" was the correct prior BEFORE E-00003 and is now
over-stated; "numbers are fine" is over-stated until E-0002 runs. The unit of trust is
(value + protocol + provenance), not a bare number.

## Points of Agreement
(none yet — needs other agents.)

## Points of Disagreement
Whether /Od-relative speedups transfer to /O2 (architect: unknown until measured).

## Evidence Available
CMakeLists.txt:16-17 (/Od /Zi /EHsc /JMC + /DEBUG); file sizes observed via terminal
echo (kana.exe 83968, kana_o2.exe 253952); no timing harness in main.cpp.

## Evidence Missing
--bench output at fixed flags; kana_o2.exe build log/flags/git hash; 5-rep NPS table.

## Evidence Addendum (measured 2026-09-09)
E-00003: scratch /Od vs /O2 rebuild of identical src gave perft NPS ~19-21 Mnps vs ~43-50
Mnps (ratio 2.1-2.4x) on startpos d5 / kiwipete d4 / cpw6 d4; all perft counts exact in both
builds. Interpretation: the flags matter (~2.3x on perft NPS) — the "no NPS claim is
interpretable" premise now has a measured magnitude — but the gap is NOT catastrophic and
perft *correctness* is flag-independent. kana_o2.exe provenance remains unrecorded and stays
excluded from claims; the in-tree E-0002 benchmark (5 reps + binary-hash logging) remains the
certification path.

## Proposed Resolution Experiment
O1/E-BENCH: add --bench, rebuild Release at /O2 with logged flags+hash, record 5-rep
NPS for the full perft suite; document kana_o2.exe provenance or delete it from claims.

## Resolution
(unresolved — do not force consensus)

## Date
2026-09-09

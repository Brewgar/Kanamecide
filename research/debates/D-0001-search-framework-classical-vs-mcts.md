---
id: D-0001
type: debate
title: "Search framework: classical alpha-beta/PVS vs GPU MCTS/PUCT"
status: OPEN
participants: [researcher-architect, systems-researcher, adversarial-reviewer]
example: true
created: 2026-09-08
last_updated: 2026-09-08
---

# D-0001 — Search framework: classical alpha-beta/PVS vs GPU MCTS/PUCT

> ⚠️ **EXAMPLE / MOCK DATA.** Demonstrates the debate format. The positions below are
> illustrative and do NOT reflect real, currently-held agent conclusions.

## Question
For the long-term architecture, should the primary search be a classical alpha-beta/PVS
tree search, or a selective Monte-Carlo (MCTS/PUCT) search that leverages the GPU?

## Agent A — researcher-architect
Position: Start with classical alpha-beta/PVS; it is the known, strong, CPU-friendly baseline.
Confidence: 0.6
Argument: A correct, fast alpha-beta gives a verified reference point before any selective/learned search.

## Agent B — systems-researcher
Position: Keep MCTS/PUCT + GPU as the Phase 3+ differentiator; don't constrain the roadmap to classical search.
Confidence: 0.55
Argument: The RTX 5070 Ti is underused by a CPU alpha-beta; large-batch MCTS/NNUE is where GPU value lies.

## Agent C — adversarial-reviewer
Position: Undecided — no experimental evidence exists yet for either on this engine.
Confidence: —
Argument: Both proposals are plausible; neither has been measured.

## Points of Agreement
A correct search + evaluation is required before any comparison can be trusted.

## Points of Disagreement
Whether to commit development effort to classical search first vs parallel-track MCTS/GPU.

## Evidence Available
None yet (only perft/board correctness is validated).

## Evidence Missing
Time-to-depth and Elo numbers for both approaches on this specific engine.

## Proposed Resolution Experiment
E-0001 (baseline classical search), followed by a same-conditions MCTS prototype.

## Resolution
(unresolved — do not force consensus)

## Date
2026-09-08
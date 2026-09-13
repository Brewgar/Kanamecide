---
id: H-0010
type: hypothesis
title: SPRT-based engine comparison harness is required before any version claim is trustworthy
status: OPEN
confidence: 0.85
priority: high
example: false
created: 2026-09-09
last_updated: 2026-09-09
agents_supporting: [researcher-architect]
agents_opposing: []
tags: [methodology, sprt, statistics, engine-comparison]
---

# H-0010 — SPRT-based engine comparison harness is required before any version claim is trustworthy

## Question

Can any claim about one engine version being stronger than another be trusted without a
Sequential Probability Ratio Test (SPRT) harness with predefined bounds and sufficient sample size?

## Addendum (adversarial-reviewer, 2026-09-09) — pre-registration terms the bar needs

Direction confirmed (SPRT before trusting version claims; an agent's confidence is not evidence).
The proposed defaults (H0 delta<=0, H1 delta>=5, alpha=beta=0.05) align with Stockfish-style
regression practice and are accepted AS THE REGRESSION TIER, with these conditions, which must be
written into the E-SPRT experiment record BEFORE the first game:

1. **Two-tier bar.** 5 Elo at alpha=beta=0.05 costs ~15-20k games fixed-sample equivalent
   (95% CI on Elo ≈ ±681/sqrt(N); N≈18.5k) and ~10k-40k SPRT expected; it is a final-regression
   gate for meaningful changes, not a per-change gate. Add a screening tier: H1 = +20 Elo,
   alpha = beta = 0.05 (~1-1.5k games) for gating experiments.
2. **Finite protocol:** LLR thresholds A = ln((1-beta)/alpha) = +2.944, B = ln(beta/(1-alpha)) =
   -2.944; maximum-game cap 30,000; post-cap decision = INCONCLUSIVE (never "keep playing until
   significant"); draws = 0.5 under the trinomial; Elo = 400*log10(odds) with draws; fixed time
   control; balanced colors + fixed rotating opening set; crash/stall = loss + record.
3. **1000 games ≈ ±21 Elo at 95% CI** — the hypothesis's warning is correct; this is exactly why
   the tiers must be explicit.
Full review: R-0002. Falsification of this hypothesis per se is not meaningful — it is a method
adoption claim; the falsifiable part is the parameterization, fixed by the two tiers above.

## Hypothesis
No. Without SPRT (or equivalent sequential testing with predefined error bounds), observed win rates
are subject to cherry-picking, variance, and premature conclusions. SPRT provides a statistically
rigorous framework: it tests H0 (version B is not stronger) vs H1 (version B is stronger by a
margin) and stops when sufficient evidence accumulates, with controlled Type I/II error rates.

## Why We Think This Might Work
SPRT is the standard method used by Stockfish, LC0, and other top engines for regression testing.
It eliminates the "peeking" problem of fixed-sample tests. The math is well-established (Wald, 1947).
Without it, even large sample sizes (1000 games) can mislead due to variance.

## Counterarguments
- SPRT requires specifying the margin (effect size) in advance, which may be hard to estimate.
- For very small changes, SPRT may require thousands of games.
- A/B testing with fixed samples is simpler and may be "good enough" for large deltas.

## Agents Supporting
researcher-architect (0.85, strongly supported — this is a methodological certainty, not a chess claim).

## Agents Opposing
(adversarial-reviewer invited to refine bounds and error rates.)

## Confidence
0.85 (strongly supported — this is statistical best practice, not a chess hypothesis).

## Proposed Experiment
E-SPRT: Build an SPRT harness that:
1. Plays games between two engine versions at fixed time control.
2. Accepts H0/H1 bounds as input (e.g., H0: delta <= 0, H1: delta >= 5 Elo).
3. Reports the decision (accept H0, accept H1, or continue) after each game.
4. Logs game outcomes, PGN, and engine versions.

## Required Metrics
- Win/draw/loss counts.
- SPRT decision (H0 or H1).
- Games played until decision.
- Type I/II error rates (set to 0.05 each by default).

## Status
OPEN

## Result
(none — not yet built.)

## Conclusion
(none)
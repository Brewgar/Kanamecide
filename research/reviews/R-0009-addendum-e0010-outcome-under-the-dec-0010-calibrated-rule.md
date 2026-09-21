---
id: R-0009
type: review
reviewer: adversarial-reviewer
target: E-0010
kind: critique
status: COMPLETED
work_item: W-0002
related: [D-0007, DEC-0010, R-0004, R-0008, W-0002, W-0005]
example: false
created: 2026-09-21
---

# R-0009 — Addendum review of E-0010 under the DEC-0010 calibrated decision rule

## Scope

This is an ADDENDUM review, not a re-verification: E-0010 has two independent VERIFIED
reviews (R-0004, R-0008, both zero-chat-history reproductions) and this review changes
no number in it. Its purpose, per W-0002: restate E-0010's outcome under the calibrated
decision rule ratified as DEC-0010 (debate D-0007). E-0010 is append-only — its
recorded result (FAIL on pre-registered gate (c)) is history under its own rule and is
NOT rewritten. Calibration here is additive, not corrective.

## Agreements

1. **The verdict FAIL was the only honest output of E-0010's pre-registered rule.**
   Gate (c): "+116.1 < 150; CI95 [+70.8,+163.5] straddles +150" — correct, recorded
   without hedging. (PR-0003: honest FAIL is a first-class result.)
2. **The bar itself was the defect** (R-0003 F6 class): ">=150 Elo at LOS>=95% over
   >=200 games" with no power analysis. At the measured CI, the rule had ~50% power
   even against a *true* +150 and was unwinnable against the measured +116.1 at any N.
   R-0004 and R-0008 both call this "a W-0002 calibration matter, not an E-0010 error".
   I confirm, with the arithmetic in D-0007.
3. **Sample validity stands.** Independence: 0 duplicate full move-lists across all
   1240 games (re-derived by R-0008 from raw JSONL). Arm differentiation: the ladder
   spread (k1 +36.3 to k5 +127.6) makes a setoption no-op implausible. Gates (a), (b),
   (d) pass as recorded and re-verified / not contradictable from the retained evidence.

## Disagreements

With the *data*: none. Every E-0010 number I cite is the verified record's own
(R-0004: recomputed; R-0008: recomputed twice with two different algorithms). The only
disagreement this review registers is with the *history of its decision rule*, which is
settled by DEC-0010, not by this review.

## E-0010's outcome under DEC-0010 (the restatement W-0002 requires)

Measured inputs (record; verified twice): k6 N=240, W=144 L=66 D=30, Elo +116.1
(400*log10(160/82) with Laplace +1), CI95 [+70.8,+163.5], LOS 100.00%. Calibrated
sigma = 371 Elo/game (worst measured rung); normal-approximation LLR drift per game
E[LLR] = (hi-lo)*(delta-mid)/sigma^2 at delta=+116.1:

| Tier (DEC-0010) | E[LLR/game] | Cumulative at N=240 | Verdict at N=240 |
|---|---|---|---|
| **S — screening [0, +20]** | +0.01541 | +3.70 (crosses +2.944 at ~game 191) | **PASS — H1 accepted.** The effect is >= +20 Elo at alpha=beta=0.05. Corroborated by the fixed reading: CI95 lower bound +70.8. |
| **R — regression [0, +5]** | +0.00413 | +0.99 (bounds not crossed until ~game 713) | Sequential SPRT at N=240 is still in-flight; the fixed-sample equivalent PASSES decisively (CI95 lies entirely above +5). Verdict: **PASS (strength gain established; finer tier confirmation available at ~713 games if ever needed)**. |
| **M — magnitude [100, 150] ("the >=150 question")** | -0.00323 | -0.78 (inside [-2.944, +2.944]; decides ~game 910) | **NOT ESTABLISHED at N=240** — the recorded games genuinely cannot decide it; the drift favors H0 ("not >=150"). |

Model-sensitivity cross-check (my own adversarial duty): repeating the same four rows
in score space (draws-as-halves trinomial, Var(score)=0.1923 from the measured k6
line) yields cumulative LLRs **+5.31 / +1.43 / -0.73 / +1.91** — the conservative
sigma-371 convention sits inside both conventions' agreement envelope, so **no tier
verdict depends on the LLR convention**. Cumulative values are reproducible via
`python research/context/w0002_power.py` (this session; output in
`w0002_power_output.txt`).

**Summary verdict: screening PASS, regression PASS, magnitude >=150 NOT ESTABLISHED.**
What E-0010 demonstrates under the calibrated rule: the tapered hand-tuned eval is
**at least +70.8 Elo** over material-only at 100ms+100ms (the CI95 lower bound) — a
real, significant, shippable improvement. What it does not establish: +150.

## What remains unproven at N=240 (stated exactly)

1. **Any magnitude strictly above +70.8.** The CI95 [+70.8,+163.5] is all we have;
   point estimate +116.1 is not a floor. Deciding ">=150" needs the [100,150] zone
   SPRT (~910 games predicted, ~1.2 h — routed in D-0007 as E-MAG-6V0; contingent on
   F-0002's gate-0 block being lifted).
2. **Per-term increments are individually underpowered (N=200).** Mobility (-3.7) and
   tempo (-11.5) have CIs crossing zero: that is "no evidence of gain at this N", NOT
   evidence of harm. E-0010's own multiplicity caveat stands unchanged.
3. **Nothing about other time controls.** sigma=371 and every ASN in DEC-0010 derive
   from 100ms+100ms inc, draw 8.5-25.5%. Effects (and their costs) at other time
   controls are unmeasured.
4. **H-0004 remains untouched** (E-0010 measures a delta vs material-only, not
   absolute 2500-level strength) — as E-0010 itself records.

## Factual Errors

None found in E-0010. The two previously-filed nits (R-0004 / R-0008) are documentation
only: (i) `e0010_report.py` prints two different quantities under the label `Wrate`;
(ii) E-0010's front-matter ladder ends with "(N=240)", which covers only k6 — the body
table (N=200 for k1-k5) is authoritative. Neither changes any number or verdict; both
are routed to W-0006's bucket as documentation hygiene, never edict into the record.

## Assumptions (flagged)

- **ASSUMED:** the normal/Wald LLR-drift model (used for the cumulative-LLR rows
  above). It reproduced the measured CI to 1.2% (h(240) = 46.9 vs measured 46.35) — the
  only in-sample check available. The exact trinomial LLR may shift the cumulative
  values modestly; no tier verdict above sits anywhere near a boundary that a
  modest shift could flip (closest: Tier S's +3.70 vs the +2.944 bound, a ~26% margin).
- **ASSUMED:** sigma = 371 Elo/game transfers to future experiments only near the
  E-0010 conditions; DEC-0010 requires per-experiment re-derivation — this review
  applies it only to E-0010 itself, where sigma is directly measured.
- **MEASURED:** all E-0010 inputs (N, W/L/D, CI, LOS, draw rates, throughput, binary
  hash) are took-at-face-value from the record AND from R-0004/R-0008's independent
  recomputation of them.

## Proposed Experiments

1. **E-MAG-6V0** (pre-registration skeleton in D-0007): stage-6 vs stage-0, SPRT
   H0: d<=100 vs H1: d>=150, alpha=beta=0.05, LLR +/-2.944, cap 8,000 games, E-0010's
   opening/color/crash protocol. Predicted cost ~910 games (~1.2 h) at the measured
   +116.1; predicted verdict H0 ("not >=150") — a *decision*, unlike the current
   "not established". Blocked by F-0002 until the host can execute the engine again.
2. **W-0005 ASN validation (offline):** replay the retained k6 JSONL (EV-0001) through
   the E-SPRT-lite LLR logic and compare realized stopping games against the predicted
   ~191 (Tier S) / ~713 (Tier R). No engine needed. This validates or falsifies the
   ASN model DEC-0010's cost tables rest on.

## Verdict

E-0010 needs no correction and receives none. Under the calibrated rule (DEC-0010)
its outcome is: **screening PASS (+20 demonstrated; the eval CLEARS the
practical-significance bar with 26% LLR margin), regression PASS (strength-gain
established), [100,150] magnitude INCONCLUSIVE at N=240 (decidable next at ~910
games).** E-0010 is, after this review, the project's strongest experiment record:
measured, double-verified, honestly failed under its own bar, and — now — honestly
re-scored under a ruled one.

## Date

2026-09-21

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns. (kind: critique — the template's verification block is
> intentionally omitted; the verification of E-0010 lives in R-0004 and R-0008.)


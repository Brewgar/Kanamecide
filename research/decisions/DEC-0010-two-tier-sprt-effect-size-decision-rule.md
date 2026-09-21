---
id: DEC-0010
type: decision
title: "Calibrated effect-size decision rule for engine-strength comparisons (two-tier SPRT + magnitude zones)"
status: ACTIVE
superseded_by: null
related: [D-0007, E-0010, W-0002, H-0010, W-0005]
derived_from: [E-0010, R-0002]
example: false
created: 2026-09-21
---

# DEC-0010 — Calibrated effect-size decision rule for engine-strength comparisons

## Decision

Every experiment that claims an engine-strength delta (Elo) MUST pre-register its
decision rule from the tiers below, computed at the experiment's own time control and
realized draw rates, BEFORE `status: RUNNING`. No bare point bars (">=X Elo at fixed
N") without the accompanying power arithmetic.

**Calibration constants (MEASURED, E-0010, verified by R-0004 + R-0008):**

- Per-game score sigma at 100ms+100ms inc, score 0.55-0.66, draw 8.5-25.5%:
  **sigma = 371 Elo/game** (max implied by the six measured rung CIs, k1=349...k5=371;
  k6=366; delta-method cross-check 341). CI half-width model h(N) = 1.96*sigma/sqrt(N)
  = 727/sqrt(N) reproduces the measured k6 half-width 46.35 at N=240 within 1.2%
  (predicted 46.9).
- Throughput: **769 games/hour** at the sanctioned 2 engine pairs (E-0010 campaign:
  1240 games / 5807 s).

**Tier S — SCREENING** ("is the effect large enough to be worth keeping/investing?"):

| Parameter | Value |
|---|---|
| H0 (null margin) | delta <= 0 Elo |
| H1 (alternative margin) | delta >= +20 Elo |
| alpha = beta | 0.05 / 0.05 |
| LLR thresholds | A = ln((1-beta)/alpha) = +2.944; B = ln(beta/(1-alpha)) = -2.944 |
| Maximum-game cap | 8,000 games (~10.4 h wall-clock) |
| Post-cap verdict | INCONCLUSIVE (record it; never extend the cap after seeing data) |
| Expected cost | ASN ~1,820 games under H1, ~2,025 under H0; ~4,050 near the midpoint (d=5 or 15); infinite exactly at d=10 (cap binds) |
| Fixed-sample equivalent | N = 3,722 for one-sided 95% size + 95% power (~4.8 h) |

**Tier R — REGRESSION / STRENGTH CLAIM** ("version B is stronger than A"):

| Parameter | Value |
|---|---|
| H0 (null margin) | delta <= 0 Elo |
| H1 (alternative margin) | delta >= +5 Elo |
| alpha = beta | 0.05 / 0.05 |
| LLR thresholds | +/-2.944 (as Tier S) |
| Maximum-game cap | 30,000 games (~39 h wall-clock; a round-boundary campaign, not a per-change gate) |
| Post-cap verdict | INCONCLUSIVE — stated honestly: for a true delta within ~+/-2 Elo of the zone midpoint (2.5), the cap WILL bind and the nominal alpha/beta are NOT achieved at the cap; the correct verdict there is "undecidable at this budget" |
| Expected cost | ASN ~29,160 games under H1, ~32,400 under H0; ~81,000 at d=3.5 (cap binds) |
| Fixed-sample equivalent | N = 59,545 (~77.5 h) — beyond any campaign this host has run; expected-cost is why the sequential form is the default (D-0007 Agent B objection recorded) |

**Tier M — MAGNITUDE CLAIM** ("B is stronger by at least M Elo"; this is the tier the
E-0010 >=150 bar should have been):

| Parameter | Value |
|---|---|
| H0 (null margin) | delta <= M - 50 Elo |
| H1 (alternative margin) | delta >= M Elo |
| alpha = beta | 0.05 / 0.05 |
| LLR thresholds | +/-2.944 (as Tier S) |
| Maximum-game cap | 8,000 games |
| Post-cap verdict | INCONCLUSIVE (expected near the zone midpoint M-25: the test guarantees error control only AT the zone edges) |
| Expected cost | ~292 games (H1 edge) / ~324 (H0 edge) / e.g. ~910 games if the true effect is +116 against M=150 (~1.2 h) |
| Hard constraint | A claim ">=M" is **unwinnable at any N when the true effect < M**; confirming M=150 against a true +160 costs ~14,900 games (~19.4 h). The budget must be pre-registered, never discovered mid-run. |

## E-0010 outcome under this rule (restated; the record itself is NOT rewritten)

E-0010's recorded result (FAIL, under its own pre-registered gate (c)) is history and
stays as filed. Restated under DEC-0010, using E[LLR/game] = (hi-lo)*(delta-mid)/sigma^2
at the measured delta = +116.1, sigma = 371 (normal-approximation drift; exact
trinomial LLR may differ slightly):

| Tier | E[LLR/game] | Cumulative LLR at N=240 | Verdict at N=240 |
|---|---|---|---|
| S [0,20] | +0.01541 | **+3.70 > +2.944** (crosses ~game 191) | **H1 accepted — PASS**: effect >= +20 demonstrated. Fixed-sample reading agrees: CI95 lower bound +70.8 >= +20. |
| R [0,5] | +0.00413 | +0.99 (inside bounds; crosses ~game 713) | Sequentially INCONCLUSIVE at 240 games — but the fixed-sample equivalent PASSES decisively (CI95 [+70.8,+163.5] lies entirely above +5). |
| M [100,150] (M=150) | -0.00323 | -0.78 (inside bounds; decides ~game 910) | **INCONCLUSIVE at N=240** — the recorded games cannot decide ">=150"; the drift points to H0 ("not >=150") as the likely ~910-game verdict. |
| M [75,125] (M=125) | +0.00585 | +1.40 (inside bounds; crosses ~game 503) | INCONCLUSIVE at N=240. |

Note on model sensitivity: the LLRs above use the conservative Elo-space drift with
sigma=371. An independent score-space (draws-as-halves trinomial, Var(score)=0.1923
from the measured k6 totals) cross-check in `research/context/w0002_power.py` gives
cumulative LLRs +5.31 / +1.43 / -0.73 / +1.91 for the same four rows — same side of
every boundary, same verdicts. The calibration is not fragile to the LLR convention.

Summary: **screening PASS (>= +20 Elo demonstrated), regression PASS (>= +5 Elo via the
fixed-sample equivalent), magnitude ">=150" NOT ESTABLISHED at N=240** — what remains
unproven is any specific magnitude between the demonstrated "+70.8 or more" (CI95
lower bound) and the unconfirmed 150.

**Mandatory shared protocol (all tiers; inherited from E-0010's verified scheme):**

- **Draw model:** trinomial (win/draw/loss), draws counted as half a point;
  q = (W + D/2)/N; Elo = 400*log10(q/(1-q)); per-game LLR under the draws-as-halves
  (lite) model of R-0002 Q2 / H-0010. The exact trinomial LLR is an allowed refinement
  if W-0005 validates it. Each experiment's `## Power And Sample Size` section MUST
  re-derive sigma at its own realized draw rate and time control (the calibrated 371
  applies only near 100ms+100ms inc, score 0.55-0.66, draw 8.5-25.5%).
- **Opening protocol:** 10 random legal plies from startpos per game, python-chess
  legal-move RNG, seed = deterministic function of (campaign salt, game_index) — the
  E-0010 scheme; the SAME opening is sent to both engines as
  `position startpos moves <uci...>`; the opening randomization is fixed and
  pre-registered before the first game.
- **Color protocol:** colors balanced (alternating) across games.
- **Independence gate:** the aggregator rebuilds every game's full move list; the
  sample is VALID only with 0 duplicate move-lists (E-0010's post-hoc check becomes a
  pre-condition for any verdict).
- **Time control:** fixed and pre-registered per experiment (E-0010: 100ms+100ms inc
  via the O3d time formula, max 2 engine pairs concurrent — the Round-3 concurrency cap).
- **Crash/stall rule:** an engine that crashes, stalls, or fails to emit `bestmove`
  within the deadline LOSES that game; the incident is recorded in the game record and
  summarized in the experiment record. Never silently restarted or excluded.
- **One look:** bounds, cap, and verdicts are fixed before the first game. Re-running
  with different bounds after seeing data is p-hacking (F6) and voids the experiment.
- **Environment caveat:** this host currently cannot execute the engine (Gate 0
  hard-blocked, F-0002, exit 4551 / App Control policy block). The rule is arithmetic
  and stands; every match run under it is contingent on the block being lifted.

## Context

E-0010 pre-registered ">=150 Elo at LOS >=95% over >=200 games" with no power analysis
(the R-0003 F6 defect class: "unwinnable threshold"). At its measured N=240 the CI95
half-width was +/-46.35 Elo; the experiment measured +116.1 (LOS 100.00%) and honestly
recorded FAIL. Two independent zero-chat-history verifications (R-0004, R-0008)
confirmed every number and noted the bar was "effectively unwinnable — a W-0002
calibration matter, not an E-0010 error". D-0007 derived the full cost table (see that
record for the arithmetic and the counter-positions); this decision ratifies its
Agent-A position as project policy. It supersedes the *parameters* sketched in R-0002
Q2 / H-0010's addendum (screening "~1-1.5k games"; one universal 30,000 cap) with the
measured-variance derivation: screening ASN is in fact ~1.8-2.0k games with an 8,000
cap; the 30,000 cap belongs to the regression tier only.

## Alternatives Considered

1. **Keep the >=150 bar, spend the games** (D-0007 Agent C): rejected — unwinnable at
   any N unless the truth already exceeds 150 (and ~14,900 games to confirm 150 against
   a true +160); a rule the data cannot pass is not a decision rule.
2. **Fixed-sample tests only** (D-0007 Agent B): same size/power at bounded N; cheaper
   than SPRT near the zone midpoint. NOT adopted as the default because the regression
   tier's fixed equivalent (59.5k games, ~77.5 h) exceeds anything this host has run
   (largest campaign to date: 1,240 games), while the SPRT's expected ~29-32k is a
   feasible round-boundary campaign. The fixed-N equivalents REMAIN VALID under this
   decision — the tiers are defined by margins and error rates, not by sequentiality.
   Revisit on W-0005's realized stopping-time data.
3. **A single universal tier:** rejected — 5-Elo sensitivity per-change would cost
   ~29-59k games per experiment and paralyze the roadmap; 20-Elo-only screening would
   miss real regressions. The tier split matches decision semantics: keep/invest vs
   claim-strength vs magnitude.

## Arguments

- The variance is measured, not assumed: six independent rungs (1240 games, 0
  duplicate move-lists, both arms differentiated by the ladder spread) give
  sigma = 349-371 Elo/game; the h(N) model reproduces the measured k6 CI to 1.2%.
- Error control is explicit: P(accept H1 | delta <= lo) <= 0.05 and
  P(accept H0 | delta >= hi) <= 0.05 in every tier; the cap converts the undecidable
  middle into an honest INCONCLUSIVE rather than a hidden error.
- Practical significance: +20 Elo is the smallest effect that pays for eval/search
  complexity at this stage (E-0010's ladder: real terms moved 22-46 Elo; noise-level
  terms moved <12); +5 Elo matters only for champion-regression claims near release;
  magnitude zones make ">=" claims decidable at all — and price them honestly.

## Evidence

- E-0010 (COMPLETED, result FAIL — honest under its own rule): k6 +116.1 / CI95
  [+70.8,+163.5] / LOS 100.00% / N=240; 1240/1240 legal; 0 duplicate move-lists; draw
  rates 8.5-25.5%; throughput 1240 games / 5807 s.
- R-0004 and R-0008: two independent VERIFIED reproductions from the raw JSONL
  (every published number, recomputed by zero-chat-history agents).
- EV-0001 (raw k6n games), EV-0002 (reproduction harness), EV-0010 (measurement binary,
  SHA256 504EB01A...A6DAA).
- `research/context/w0002_power.py` + `w0002_power_output.txt`: the derivation script
  and its output (this session; reproducible).
- D-0007: the debate, including the strongest counter-position (Agent B) and the
  conditions that would overturn the sequential default.

## Agents Involved

- adversarial-reviewer (W-0002 owner; author of D-0007 and of this decision).
- Pending: independent verification per DEC-0009 gate 3 (handoff filed to
  verification-auditor; the verifier is never the owner).

## Why This Was Chosen

Because bars inherited from ambition rather than derived from measured variance already
produced one unwinnable threshold (F6, E-0010) and would produce more. This decision
makes the cost of every future strength claim computable BEFORE the first game, makes
INCONCLUSIVE a first-class verdict, and keeps the project's claims inside what this
host can actually measure.

## Reversal Conditions

- W-0005's realized SPRT stopping times materially exceed the ASN model at the
  decision-relevant edges (then: fixed-sample becomes the default protocol; margins
  and error rates unchanged).
- Measured sigma at a new time control / draw regime departs from 371 by more than
  ~20% (then: re-derive all ASN/cap tables; tiers unchanged; the per-experiment
  re-derivation duty already covers this).
- A demonstrated protocol achieving the same error rates at lower expected cost on
  this host (beliefs.md falsifier) — file a SUPERSEDING decision, never edit this one.

## Date

2026-09-21

> If a later decision overturns this one, do **not** delete this record — set
> `status: SUPERSEDED` and add `superseded_by: DEC-####` in the front-matter.


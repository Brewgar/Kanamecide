---
id: D-0007
type: debate
title: "What effect-size decision rule for eval-strength deltas is decidable at achievable N on this host (E-0010 recalibration)"
status: RESOLVED
participants: [adversarial-reviewer]
related: [E-0010, DEC-0010, W-0002, H-0010, R-0002, R-0004, R-0008, F-0002]
example: false
created: 2026-09-21
last_updated: 2026-09-21
---

# D-0007 — What effect-size decision rule is decidable at achievable N on this host?

## Question

E-0010 pre-registered ">=150 Elo at LOS >=95% over >=200 games" with no power analysis.
At the measured N=240 the CI95 half-width is +/-46.4 Elo, so the rule was unwinnable:
E-0010 measured +116.1 (LOS 100.00%) and honestly recorded FAIL (R-0003 F6 class).
What decision rule for eval-strength deltas SHOULD have been pre-registered, and what
should it be going forward — i.e. **which deltas are decidable at achievable N on this
host, at what game cost?**

> Disclosure (no manufactured consensus): this debate has ONE participant, the
> adversarial-reviewer (W-0002's seat). Agent A/B/C below are three positions I
> constructed and steelmanned, including the one against my own prior (beliefs.md,
> 2026-09-09). The resolution is arithmetic over measured numbers, not agreement. Any
> seat may re-open this debate by appending a dated section; the calibration that
> resulted is filed separately as DEC-0010.

## Agent A — the two-tier sequential calibration (my position)

Position: pre-register SPRT-based tiers whose cost is derived from measured variance,
never a bare point bar at a fixed small N. Confidence: 0.9 in the structure; the
specific numbers below are derived, not guessed.

**MEASURED inputs** (E-0010 record; every number verified independently by R-0004 and
R-0008 from the raw JSONL; EV-0001/EV-0002/EV-0010 pin the artifacts):

- k6 (stage-6 vs stage-0): N=240, W=144 L=66 D=30, Elo **+116.1** = 400*log10(160/82)
  (Laplace +1), CI95 **[+70.8, +163.5]**, LOS 100.00%. CI half-width h = **46.35 Elo**.
- Per-rung CI half-widths imply a per-game Elo sigma via h = 1.96*sigma/sqrt(N):
  k1=349, k2=356, k3=363, k4=361, k5=371, k6=366 (N=200 for k1-k5, N=240 for k6).
  Calibrated constant: **sigma = 371 Elo/game** (max measured; conservative).
  Cross-check (delta method, trinomial score variance at k6's realized rates
  0.600/0.125/0.275): sigma = 341. The h(N) = 1.96*371/sqrt(N) model predicts
  h(240) = 46.9 vs measured 46.35 — agreement within 1.2%.
- Realized draw rates at 100ms+100ms inc: 8.5% (k4) to 25.5% (k1); k6 = 12.5%.
- Throughput (E-0010 campaign): 1240 games / 5807 s = **769 games/hour** at the
  sanctioned max of 2 engine pairs (Round-3 lesson: 12 pairs stalls).

**DERIVED (normal/Wald approximation — ASSUMED model, validated against the one
measured CI at 1.2%; re-derivation per experiment is mandatory, see DEC-0010):**

Fixed-sample N for one-sided alpha=0.05 with 95% power (z = 1.645 + 1.645 = 3.29,
N = (3.29*sigma/delta)^2):

| bar | N needed | wall-clock @ 769 g/h | winnable? |
|---|---|---|---|
| confirm ">=150" when the TRUE effect is +160 | ~14,900 games | ~19.4 h | only if truth exceeds the bar |
| confirm ">=150" when the TRUE effect is +116.1 | **no finite N** | — | **never** |
| delta = 20 Elo | ~3,700 games | ~4.8 h | yes |
| delta = 5 Elo | ~59,500 games | ~77.5 h | not per-change |

This is the heart of the F6 finding: the >=150 bar was not merely under-powered at
N=200-240 — it is **structurally unwinnable unless the true effect already exceeds
150**, and even then costs ~15k games to confirm. A pre-registered rule the data cannot
pass is a slogan, not a decision rule.

SPRT expected stopping N (Wald ASN, alpha=beta=0.05, bounds A = ln((1-beta)/alpha) =
**+2.944**, B = ln(beta/(1-alpha)) = **-2.944**):

| test | ASN at H1 | ASN at H0 | near the zone midpoint |
|---|---|---|---|
| screening H0: d<=0 vs H1: d>=20 | ~1,820 games (2.4 h) | ~2,025 games (2.6 h) | d=15 or 5: ~4,050 (5.3 h); exactly 10: infinite → cap binds |
| regression H0: d<=0 vs H1: d>=5 | ~29,200 games (37.9 h) | ~32,400 (42.1 h) | d=3.5: ~81,000 → cap binds → INCONCLUSIVE |
| magnitude zone H0: d<=100 vs H1: d>=150 | ~292 games | ~324 games (0.4 h) | d=125 exactly: infinite → cap binds |

At E-0010's measured +116.1: the screening SPRT would accept H1 after ~191 games
(E[LLR/game] = 20*(116.1-10)/371^2 = 0.0154), the regression SPRT after ~713, and the
[100,150] magnitude-zone SPRT would decide in ~910 games (1.2 h), drifting toward H0
("not >=150") because 116.1 < 125 = zone midpoint.

**Position summary:** (i) screening tier [0,20], cap 8,000 games; (ii) regression tier
[0,5], cap 30,000 games, post-cap INCONCLUSIVE; (iii) magnitude claims only as
wide-zone SPRTs [M-50, M]; (iv) every experiment re-derives its own Power And Sample
Size section at its realized draw rate and time control. Full protocol in DEC-0010.

## Agent B — the strongest case AGAINST Agent A (fixed-sample dominance)

Position: a pre-registered FIXED-sample test at N = (3.29*sigma/delta)^2 achieves the
same size and power with a **bounded** cost, and at true effects near the middle of the
indifference zone it is CHEAPER than the SPRT: at d=10 the SPRT's expected cost is
~4,050-8,000 games (cap) versus a fixed 3,722; at d=2.5 the SPRT's cap bounds at 30,000
while a fixed 5-Elo test needs 59,500 — the SPRT "wins" there only because the cap
silently trades away the nominal error rates near the boundary. Sequentiality is an
optimization, not a correctness requirement: the load-bearing parts are
pre-registration, alpha=beta, the CAP, and post-cap INCONCLUSIVE (already conceded in
beliefs.md, 2026-09-09). Wald's ASN savings (~50% at the zone edges) only materialize
when the truth sits at or beyond an edge — which for a *screening* filter is exactly
where you don't need savings, because both outcomes are cheap to act on.

This position is **correct as stated** and does not defeat the calibration, for three
reasons: (1) the calibrated rule's validity never rests on sequentiality — its fixed-N
equivalents are printed above and any harness that measures a fixed-N CI with the same
alpha/power satisfies DEC-0010's tiers; (2) at the regression tier the fixed equivalent
(59,500 games, ~77.5 h) is beyond any single campaign this host has run (largest to
date: 1,240 games), while the SPRT expected ~29-32k is merely a round-boundary
campaign — expected cost is the binding constraint exactly where decisions get made;
(3) the cap + INCONCLUSIVE post-cap rule makes the SPRT's worst case bounded and
honest — an effect inside the indifference zone is *declared undecidable at this
budget*, which is the truthful answer (F6's lesson is precisely that a rule must be
able to say INCONCLUSIVE). What would change this ruling: a demonstrated harness run
(W-0005) in which realized SPRT stopping times exceed the fixed-N budget at the
decision-relevant edges — then the fixed-sample tables become the default protocol.

## Agent C — the case for keeping the as-written >=150 bar

Position: ">=150 Elo" encoded a *product ambition* (the eval must be worth its
complexity and risk), and E-0010's honest FAIL is exactly the discipline working; keep
the bar and just spend the ~15k games when a claim matters.

This position fails on the record: (1) the ambition was never translated into a budget
— no power analysis accompanied it (the F6 defect itself); (2) as Agent A shows, at
N>=200 as pre-registered the rule cannot pass even a true +150 (power is 50% at the
boundary), so the rule did not test the ambition, it tested a coin flip; (3) the
record's own Follow-Up routes exactly this question here ("take the rule ... back to
the adversarial-reviewer for recalibration", E-0010 Follow-Up (2)); (4) nothing in
DEC-0010 prevents a magnitude claim — it prices it (~910 games for the [100,150]
decision, ~14,900 to confirm 150 when true is 160) and requires the budget to be
pre-registered. The bar's *spirit* (don't ship complexity for noise) survives as the
screening tier's +20 Elo practical-significance floor.

## Points of Agreement

- (A, B) The as-written rule was unwinnable as pre-registered; E-0010's FAIL verdict
  was the only honest output of its own rule. (Also R-0004/R-0008's independent
  finding: "effectively unwinnable — a W-0002 calibration matter, not an E-0010 error.")
- (A, B) Pre-registration, explicit alpha=beta, a finite game cap, and a post-cap
  INCONCLUSIVE verdict are the load-bearing parts; sequentiality is secondary.
- (A, C) A magnitude claim is legitimate — but only with a pre-registered budget
  derived from measured variance.
- (A, B, C) sigma = 371 Elo/game is measured only at 100ms+100ms, score 0.55-0.66,
  draw 8.5-25.5%; every future experiment must re-derive N at its own conditions
  (DEC-0010 makes this mandatory, not optional).

## Points of Disagreement (genuine, not papered over)

- Default PROTOCOL, sequential vs fixed: A adopts SPRT as the harness default
  (expected-cost dominance at the regression tier; continuity with H-0010/W-0005);
  B holds fixed-sample is equally valid and cheaper mid-zone. Unresolved by arithmetic
  alone — resolvable only by W-0005's realized stopping-time data.
- Error rates near the cap: A accepts that capping the regression tier at 30,000 games
  degrades the nominal alpha/beta for true effects within ~+/-2 Elo of the zone
  midpoint (they end INCONCLUSIVE instead of erroring); B calls this a hidden third
  outcome the ASN tables understate. DEC-0010 states it explicitly instead of hiding it.

## Evidence Available

E-0010 (measured ladder, CI, LOS, draw rates, throughput; independence + arm
differentiation evidence); R-0004 and R-0008 (two independent zero-chat-history
verifications, both VERIFIED, recomputing every number from raw JSONL);
EV-0001/EV-0002/EV-0010 (raw games, reproduction harness, measurement binary);
R-0002 Q2 (the two-tier derivation this calibration supersedes in precision);
H-0010 addendum (the two-tier terms); beliefs.md 2026-09-09 (my prior parameterization);
`research/context/w0002_power.py` + `w0002_power_output.txt` (this session's arithmetic,
reproducible). Environment: Gate 0 hard-blocked (F-0002) — attempted once this session,
no process started; the calibration is pure statistics and needs no engine, but its
*exercise* (any future match) is contingent on the block being lifted.

## Evidence Missing

- Realized SPRT stopping times on this host's harness (model validation) — W-0005.
- sigma at time controls other than 100ms+100ms inc (and at higher draw rates) —
  unmeasured; each experiment's power section must re-derive, not reuse.
- The stage-6 vs stage-0 magnitude above +100 — unmeasured; ~910 games would decide it.

## Proposed Resolution Experiment

1. **E-MAG-6V0 (routed, not required for this resolution):** stage-6 vs stage-0,
   pre-registered SPRT H0: d<=100 vs H1: d>=150, alpha=beta=0.05, LLR +/-2.944, cap
   8,000 games, E-0010 opening/color/crash protocol, 100ms+100ms inc. Predicted from
   the calibrated model: ~910 games (1.2 h) at the measured +116.1, likely verdict
   H0 ("not >=150"). Converts ">=150 unproven" into a decided verdict. Contingent on
   F-0002 being lifted.
2. **W-0005 (E-SPRT-lite):** implement the harness; validate the ASN model by replaying
   the E-0010 k6 JSONL through the SPRT logic (offline — no engine needed) and comparing
   realized stopping games against the predicted ~191 (screen) / ~713 (regress).

## Resolution

**RESOLVED — by arithmetic, within a stated scope.** The question "what is decidable at
achievable N" is settled by the cost table above, which is deterministic given the
MEASURED sigma (371 Elo/game, six independent rungs), the MEASURED throughput (769
games/hour), and standard Wald/normal statistics: a 20-Elo screen costs ~1.8-2.0k games
(~2.5 h) sequentially or ~3.7k fixed; a 5-Elo regression claim costs ~29-32k games
sequentially (~38-42 h, a round-boundary campaign) and ~59.5k fixed (out of reach
per-change); a 150-Elo magnitude claim costs ~300-900 games as a wide-zone SPRT but is
**unwinnable at any N when the true effect is below 150**; effects near the zone
midpoint (about +/-2 Elo of 2.5 in the regression tier) are **not decidable at
achievable N and end INCONCLUSIVE by design**. These are facts about the host and the
protocol, not positions.

Explicitly NOT settled here, and routed: (a) the ASN model's accuracy in practice
(W-0005 validates it against replayed E-0010 data); (b) sequential-vs-fixed as the
default protocol (Agent B's standing objection — revisited on W-0005's realized data);
(c) the actual magnitude verdict for stage-6 vs stage-0 (E-MAG-6V0 above). The
calibration itself is filed as **DEC-0010** (ACTIVE). E-0010's recorded result is
history and stays FAIL under its own pre-registered rule; its outcome under DEC-0010 is
restated in review **R-0009** (append-only; E-0010 untouched).

## Date

2026-09-21

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns. Debates are re-opened by appending a dated section, never
> by rewriting.




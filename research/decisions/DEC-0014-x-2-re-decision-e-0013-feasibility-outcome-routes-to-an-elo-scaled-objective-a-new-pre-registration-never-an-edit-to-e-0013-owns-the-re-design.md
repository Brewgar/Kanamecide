---
id: DEC-0014
type: decision
title: X-2 re-decision: E-0013 feasibility outcome routes to an Elo-scaled objective; a new pre-registration (never an edit to E-0013) owns the re-design
status: ACTIVE
superseded_by: null
example: false
created: 2026-10-06
---

# DEC-0014 — X-2 re-decision: E-0013 feasibility outcome routes to an Elo-scaled objective; a new pre-registration (never an edit to E-0013) owns the re-design

## Decision

E-0014's TRAIN-only feasibility pass fired pre-registered branch **X-2
INCONCLUSIVE-BY-POWER** (`s_d_inner = 48.73234010819671 > 0.0101`,
`delta_star_inner (inner-val, paired) = 23.05004604618598`, inner-val games =
170, achieved power at 0.002 = 0.050000; E-00014 COMPLETED 2026-10-05). This
decision therefore routes as follows:

1. **E-0013 is frozen.** Its `LOSS_MARGIN = 0.002` is not widened, its
   contingency table is not re-interpreted, and no holdout quantity is read to
   rescue decidability. The X-1 `LOSS_MARGIN = 14.786113020671715` computation
   is withdrawn as a routing (E-00014 addendum 2026-10-05 §1–§2).
2. **The follow-up question is Elo-scaled.** Any re-design that keeps the
   current `sigmoid(clip(E_theta, -1200, 1200))` objective without an Elo-scale
   divisor is re-measuring the recorded saturation pathology, not eval quality
   (E-00014 addendum §4). The owned re-design is therefore an **Elo-scaled Texel
   objective** feasibility question.
3. **A NEW pre-registration owns the re-design.** The re-design lives in
   **E-0016** (PENDING 2026-10-06), never as an edit to E-0013. F-U3
   (`FND-0010`, still OPEN) is armed with the four published quantities and is
   discharged only by E-0016's own pre-registered run + verdict, not by this
   routing alone.

## Context

E-0013 conjunct (c) turned on `LOSS_MARGIN = 0.002` whose attainability depended
on an unmeasured per-game cluster SD `s_d`. E-00014 measured it on a TRAIN-side
inner partition (inner-train 48,003 positions / 621 games; inner-val 11,889
positions / 170 games; holdout never read, 208 games / 14,560 rows excluded
before any label read). Result: `s_d_inner = 48.73234010819671` (95% CI
`[44.0445, 54.5457]`, df=169), ~4,825× the 0.0101 decidability threshold;
power at 0.002 = 0.05 (null rate); ~4.66e9 games required at this dispersion
(`_obs/dir_power.txt`). `delta_star_inner` restated to the contract partition:
inner-val paired 23.05004604618598, CI95 `[15.671648473, 30.428443619]`
(`build/e00014/eval_inner_val.json` `e4150d19…`); the 29.57222604134343 figure
is the fit-set number retained as history only.

Loss-scale pathology (E-00014 addendum §4, from pinned code
`tools/e0013_eval.py:859` `loss_and_gradient`): with no Elo-scale divisor, raw
centipawn scores saturate the sigmoid and a wrong-side saturated position pays
loss near |E| up to 1200. The optimizer harvested ~23 points by collapsing
scores toward 0 (fitted PAWN mg about −30 scale, tempo 10→0 in
`build/e00014/fitted_inner.json` `f20cd164…`), while fitted MAE (0.261097949)
is worse than floor MAE (0.219609585). The measurement ran the pinned objective
faithfully and is not voided; but it must not be re-measured under the same
objective and mistaken for quality.

## Alternatives Considered

- **Widen the margin to manufacture decidability (e.g. adopt 14.786…).**
  Rejected — X-2 text forbids it verbatim; S-0046 withdrew it as a routing.
- **Larger holdout under the same cp-scale objective.** Considered and deferred
  — at `s_d ≈ 48.7` the required N (~4.66e9 games) is not an achievable plan,
  and the saturation pathology would still dominate any measured delta.
- **Paired design with lower `s_d` but same objective.** Deferred into E-0016's
  design space, not adopted blindly — the scale pathology must be priced first.
- **Edit E-0013 to point at the new objective.** Rejected — E-0013's
  pre-registration is frozen; re-design under a new id preserves the audit
  trail (F-U3 obligation).

## Arguments

- Pre-registration binds: E-0013 B3 + E-00014 decision rule item 2 selected X-2
  before any number existed; the measured `s_d_inner` exceeds threshold by
  orders of magnitude with its own CI far above it — not borderline.
- The four F-U3 quantities are published in the open (S-0046, E-00014
  addendum §5), so the re-decision carries no hidden input.
- Elo scale is load-bearing because the pathology is in the objective's units,
  not in the optimizer: without it the next fit optimizes collapse, not
  ranking.

## Evidence

- `build/e00014/eval_inner_val.json` (`e4150d19ce22fd19a3571a2b40577c1a3717d37145d2317c18c46759d7c59cf8`):
  mean improvement 23.05004604618598, s_d 48.73234010819671, games 170, CI
  `[15.671648473, 30.428443619]`.
- `build/e00014/fit_report_inner.json`: fit-set delta 29.57222604134343
  (history only), convergence nit=935, deterministic rerun proved, holdout
  exclusion receipt 208 games / 14,560 rows.
- `_obs/dir_power.txt`: power_at_0.002=0.050000, s_d 95CI `[44.0445, 54.5457]`,
  G_required_for_0.002=4.660009e+09.
- `build/e00014/fitted_inner.json` (`f20cd1647c0c4f28ec036afd1f6ea488d8f73abe1eaa8729100205e43a2141bb`)
  vs floor `711c460d…` for the collapse signature.
- E-00014 addendum 2026-10-05 §§1–5; S-0046 §§What-I-Did-NOT-Do; FND-0010
  (F-U3, OPEN); HO-0015 Response 2026-10-05 (verification still open).

## Agents Involved

- director (orchestrator + implementation seat for the X-2 correction, S-0046).
- systems-researcher (E-00014 executor, HO-0015 Response).
- verification-auditor seat still open on HO-0015 Verification (DEC-0009 gate 3).

## Why This Was Chosen

It is the only route that honours the pre-registered table, refuses to widen
the margin after seeing data, prices the measured saturation pathology instead
of re-measuring it, and keeps E-0013's history intact by giving the re-design
its own pre-registration (E-0016).

## Reversal Conditions

- If HO-0015 independent verification contradicts the four quantities with
  evidence, this routing re-opens.
- If E-0016's own pre-registration derives an Elo scale that restores power at
  an achievable N, the follow-up proceeds under E-0016 — this decision is not
  re-edited to claim it.

## Date
2026-10-06

> If a later decision overturns this one, do **not** delete this record — set
> `status: SUPERSEDED` and add `superseded_by: DEC-####` in the front-matter.
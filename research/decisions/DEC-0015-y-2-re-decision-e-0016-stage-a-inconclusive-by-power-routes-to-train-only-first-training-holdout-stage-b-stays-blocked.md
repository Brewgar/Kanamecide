---
id: DEC-0015
type: decision
title: Y-2 re-decision: E-0016 stage (a) INCONCLUSIVE-BY-POWER routes to TRAIN-only first training; holdout stage (b) stays blocked
status: ACTIVE
superseded_by: null
example: false
created: 2026-10-07
---

# DEC-0015 — Y-2 re-decision: E-0016 stage (a) INCONCLUSIVE-BY-POWER routes to TRAIN-only first training; holdout stage (b) stays blocked

## Decision

E-0016 stage (a) fired pre-registered branch **Y-2 INCONCLUSIVE-BY-POWER**
(`delta_star_inner = 0.026946091434270198` measurable, CI95
`[0.015331774, 0.038560409]` above zero; `s_d_inner = 0.07319562658592449`
`> s_d_crit = 0.0256` by ~2.9x; inner-val games = 155; achieved power at
`M16_floor = 0.005` on G = 208 = `0.166`; fitted MAE `0.250482220` BETTER
than floor MAE `0.262752193`, i.e. no E-00014-style collapse signature;
verified VERIFIED by R-0030, 23/23 re-derivation). This decision therefore
routes as follows:

1. **E-0016 stage (b) is NOT authorized.** The holdout-gated fit-quality
   comparison runs only under a LATER record, only if a stage routes Y-1,
   and only with that record's own holdout protocol (E-0016 Follow-Up).
   Stage (a) routed Y-2, so the condition is unmet. **The outer holdout
   (208 games / 14,560 rows) is not read for any purpose** — no gradient,
   no statistic, no normalization, no checkpoint selection, no count.
2. **The follow-up obligation is discharged as a named re-decision (this
   record) with the four published quantities**: `s_d_inner =
   0.07319562658592449`, `delta_star_inner = 0.026946091434270198`,
   inner-val games = 155, achieved power at `M16_floor` = `0.166` (same
   F-U3 pattern as DEC-0014). Y-2 is NOT a FAIL, NOT a licence to widen
   the margin, NOT a licence to re-fit under a different scale, NOT a
   strength claim.
3. **E-0013 stays frozen** (DEC-0014 §1). E-0016 stage (a) history is
   intact; this record re-designs nothing about it.
4. **The owned next step is a TRAIN-only first training**, pre-registered
   as **E-0017**. It fits on the full outer-train set and evaluates on
   the inner-val partition only (the Y-1/Y-2/Y-3 table licenses no holdout
   read). It reuses the authorized science only: Elo-scaled Texel
   objective, linear tapered-eval table (683 free scalars, KING frozen),
   deterministic full-batch L-BFGS, pinned hypers. **No NNUE architecture
   is adopted here** — none was specified in any project record.

## Context

E-0016 stage (a) executed under repaired HO-0025 (HO-0028 option a:
TRAIN-only labels carve input; HO-0027 new inner salt 20261007) at
pre-execution commit `7f77422`, verified by R-0030. Its Interpretation
routes Y-2 and names the follow-up obligation: "named re-decision with
the four quantities". This record is that re-decision. The outer split
(salt 20260926, map `bb079a41…da1ea`) and TRAIN-only labels
(`2bf68bfb…0f7bc2`, 791 games) are unchanged.

## Alternatives Considered

- **Authorize E-0016 stage (b) despite Y-2.** Rejected — the E-0016
  contract licenses stage (b) only on Y-1; Y-2 withholds it.
- **Widen `M16_floor` to manufacture decidability.** Rejected — Y-2 text
  forbids it verbatim ("not a licence to widen the margin").
- **Re-fit stage (a) under a different scale/salt/hyperparameter to
  obtain Y-1.** Rejected — the prohibitions forbid re-run shopping.
- **Adopt an NNUE architecture for first training.** Rejected — no project
  record specifies one; the minimum valid first training reuses the
  authorized linear-eval objective so the full pipeline can be proven
  before any architecture research.
- **Do nothing (leave Y-2 un-routed).** Rejected — the follow-up
  obligation is binding; an un-routed Y-2 strands accountability.

## Arguments

- Pre-registration binds: E-0016's decision table selected Y-2 before any
  number existed; the measured `s_d_inner` exceeds `s_d_crit` with its own
  CI far above it — not borderline.
- The four quantities are published in the open (E-0016 Results, HO-0025
  Response, R-0030 re-derivation), so this re-decision carries no hidden
  input.
- The Elo-scaled objective cured the E-00014 collapse signature (fitted
  MAE better than floor MAE), so TRAIN-only first training measures
  ranking quality, not saturation collapse.
- TRAIN-only scope needs no new scientific decision: every value (D, L,
  salt discipline, optimizer, freeze set) is pinned by E-0016/W-0010 or
  the pre-fit manifest; the only new choice is the fit surface (full
  outer-train instead of inner-train), which E-0017 pre-registers openly.

## Evidence

- E-0016 Results/Provenance (executor fills at `7f77422`): carve 791 /
  636 / 155, inner map `93bcd0db…f9e0`; fit exit 0, rows 47,995, nit 10,
  convergence confirmed; eval exit 0, games 155,
  `delta_star_inner = 0.026946091434270198`,
  `s_d_inner = 0.07319562658592449`, CI95 `[0.015331774, 0.038560409]`,
  power `0.166`; fitted `01c0d7a6…`, floor `711c460d…`, eval `f5a390db…`.
- R-0030 VERIFIED (23/23 re-derivation, 2026-10-07).
- Corpus/split/labels pins: dataset `27ea181d…ac5bb95`; outer map
  `bb079a41…da1ea`; TRAIN-only labels `2bf68bfb…0f7bc2`; floor
  `711c460d…667f1`; source epoch `dd4051a92daf834cf4a73f1878a0c894b0b6d1b8`.

## Agents Involved

- director (orchestrator; Y-2 re-decision author, round 8).
- researcher-architect (E-0016 owner; E-0017 pre-registration owner).
- implementation-engineer (W-0011 pipeline owner).
- systems-researcher (HO-0029 executor, E-0017 run).
- adversarial-reviewer (R-0031 critique of E-0017).
- verification-auditor (fresh seat; W-0011 + E-0017 verification).

## Why This Was Chosen

It is the only route that honours the Y-2 table, refuses to touch the
holdout, prices the measured dispersion instead of re-measuring it, keeps
E-0013/E-0016 history intact, and converts the verified stopping point
into a real TRAIN-only training system without inventing science.

## Reversal Conditions

- If HO-0025 Verification (fresh auditor seat) contradicts the four
  quantities with evidence, this routing re-opens.
- If a Y-1 result is ever measured under a duly pre-registered record,
  stage (b) proceeds under that record — this decision is not re-edited
  to claim it.

## Date
2026-10-07

> If a later decision overturns this one, do **not** delete this record — set
> `status: SUPERSEDED` and add `superseded_by: DEC-####` in the front-matter.
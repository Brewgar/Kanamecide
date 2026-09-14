---
id: W-0005
type: work
title: "E-SPRT-lite comparison harness: pre-register, build, validate against known difference"
round: 4
owner: researcher-architect
status: OPEN
deliverable: "research/experiments/E-#### (pre-registered) + resumable SPRT harness + validation run vs stage-6/stage-0"
exit_check: "harness decides a known-difference pair (EvalStage 6 vs 0) within its pre-registered bounds; decision sign matches the E-0010 measurement"
evidence: []
verified_by: null
verification_verdict: null
example: false
created: 2026-09-14
closed: null
---

# W-0005 — E-SPRT-lite comparison harness (H-0010)

## Objective
Every future A/B claim currently depends on ad-hoc match harnesses. Build the standing
comparison harness with pre-registered two-tier error control: screening δ≈20 Elo,
regression δ=5, LLR bounds ±2.944, game cap → INCONCLUSIVE. Resumable, runjob-compatible.

## Deliverable (exact path(s))
- Pre-registered experiment record (PENDING) BEFORE any code runs.
- Harness script + validation RUN record.

## Exit Check
```powershell
# harness output: LLR crossed a bound within cap; verdict consistent with E-0010's
# stage-6 > stage-0 (+116.1 Elo) sign and rough magnitude band.
```

## Evidence
- (to be filled)

## Work Log (append-only while OPEN)
- 2026-09-14 — opened by Round-4 meta-agent; sequencing depends on W-0002's calibrated rule.

## Verification
- verified_by: (a different agent than owner)
- verdict: (VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE)
- evidence: (review record id + command outputs)
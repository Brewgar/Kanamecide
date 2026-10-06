---
id: E-00016
type: experiment
title: E-0016 - Elo-scaled Texel objective feasibility + fit (X-2 follow-up; TRAIN-only inner pass first, holdout gated)
status: PENDING
result: null
elo_change: null
hypothesis: null
priority: medium
owner: null
pre_registered: null
example: false
created: 2026-10-06
completed: null
tags: []
---

# E-00016 — E-0016 - Elo-scaled Texel objective feasibility + fit (X-2 follow-up; TRAIN-only inner pass first, holdout gated)

## Hypothesis
...

## Baseline
...

## Candidate
...

## Difference
...

## Hardware
...

## Engine Version
...

## Network
...

## Dataset
...

## Test Method
...

## Games / Samples
...

## Metrics
...

## Pre-Registered Decision Rule
> MANDATORY before status becomes RUNNING. One decision rule, written here FIRST.
> State every conjunct explicitly, and state the outcome for each (PASS / FAIL /
> INCONCLUSIVE). No rule may be added after the run starts (that is p-hacking).

PASS requires ALL of:
(a) ...
(b) ...

## Power And Sample Size
> MANDATORY before status becomes RUNNING. "What N settles this rule?"
> Give the achievable precision at the planned N (CI half-width / SPRT expected
> games) and the N needed to distinguish the measured effect from the rule's
> threshold. A rule that cannot be decided at the planned N must be rewritten or
> explicitly declared INCONCLUSIVE-by-design.

At N = ... the expected CI half-width is ~±... (or: SPRT needs ~... games).
To separate a true effect of +X from the threshold +Y, N ≈ ... is required.
Therefore this rule is / is not decidable at the planned N.

## Sample Validity
> MANDATORY before status becomes RUNNING. Validation is part of the result.
> - Arm differentiation (negative control): how do you prove the experimental
>   variable ACTUALLY differs between the arms? (e.g. dump the effective option
>   value from both engines' handshake; assert arm A != arm B).
> - Independence: how do you prove the games/samples are not duplicates?
> - Provenance: binary hash, git commit of src/, exact flags, seeds.

Arm-differentiation evidence: ...
Independence proof: ...
Provenance: ...

## Provenance
- Binary SHA-256: ...
- `src/` commit: ...
- Compile flags: ...
- Raw evidence paths (local, gitignored): ...
- Aggregator command that reproduces every number: ...

## Results
...

## Statistical Analysis
...

## Interpretation
...

## Conclusion
...

## Follow-Up
...
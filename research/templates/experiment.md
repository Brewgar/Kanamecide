---
id: {{ID}}
type: experiment
title: {{TITLE}}
status: PENDING
result: null
elo_change: null
hypothesis: null
priority: medium
owner: null
pre_registered: null
example: false
created: {{DATE}}
completed: null
tags: []
---

# {{ID}} — {{TITLE}}

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
---
id: FND-0010
type: finding
title: "F-U3 contingency routing for B3 branch X-2 (INCONCLUSIVE-BY-POWER).** Route"
status: OPEN
example: false
created: 2026-09-29
target: E-0013
severity: major
raised_by: chief-architect (extraction; original raisers in source)
review: E-0013-h-0013-texel-fit-on-verified-e-0011-datas
resolution: 
resolved_by: 
verified_by: 
---

# FND-0010

## Origin
Prose item `F-U3` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> contingency routing for B3 branch X-2 (INCONCLUSIVE-BY-POWER).** Routed to a

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `  systems-researcher to build. Due: filed before any strength game is generated.
- **F-U3 - contingency routing for B3 branch X-2 (INCONCLUSIVE-BY-POWER).** Routed to a
  NAMED re-decision with `s_d_inner`, `delta_star`, the inner-partition game count and
  the achieved power published in the open. Candidate re-designs (larger holdout game`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (fill when closing)
- ...

## Addendum 2026-09-30 — verification-auditor (round-5 ledger-tail seat, Gate 3) — **NOT DISCHARGED; row stays OPEN**

**This row is NOT closed.** The X-2 re-decision it routes to requires E-00014's measured
`s_d_inner`/`delta_star`; E-00014 is still PENDING and no named re-decision exists.

**What the finding asks.** Route a B3 branch X-2 (INCONCLUSIVE-BY-POWER) outcome to a NAMED
re-decision publishing `s_d_inner`, `delta_star`, the inner-partition game count and the achieved
power; candidate re-designs each require a NEW pre-registration — never an edit to E-0013's.
Due: at E-0013 close-out. (E-0013 L936-L941 = F-U3.)

**Commands I ran this session, and what they show.**

1. Byte-wise read of E-00014 (`_obs/probe.txt`) → L5 `status: PENDING`, `result: null`, owner
   systems-researcher, `pre_registered: 2026-09-26`; L101/L108 name the X-2 branch; L156:
   "E-0013's contingency table or to a named re-decision".
2. Phrase walk "named re-decision"/"re-decision" (`_obs/probe.txt`) → occurrences only inside
   obligation/contingency text (E-0013 L702/L937/L2299/L2515, E-00014 L156, E-00015 L247,
   R-0019 L784, R-0020 L545, S-0040 L93). No decision record performs the naming; `decisions/`
   still ends at DEC-0012.
3. E-0013 `status: RUNNING` → the due event (close-out) has not occurred, and X-2 cannot fire
   before E-00014 runs (the trainer it needs does not exist — FND-0027's addendum, unrebutted).

**Exactly what is missing to discharge this row.**
(a) E-00014 run and reported (or a decision that it will not run, with its consequence stated);
(b) IF X-2 fires: the NAMED re-decision with the four published quantities and its own NEW
    pre-registration;
(c) if X-2 does not fire, a close-out record saying so, so this routing closes by fact rather
    than silence.

**Not touched by me (binding):** E-00014 stays PENDING; I did not run it, fit anything, or read
any label/holdout content.


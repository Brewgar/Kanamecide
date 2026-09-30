---
id: FND-0027
type: finding
title: "F-U11 Re-derive E-00014's inner partition under the new key"
status: OPEN
example: false
created: 2026-09-30
severity: major
target: E-0013
raised_by: researcher-architect (S-0036..S-0040 F-U family)
review: E-0013
source_key: F-U11
resolution: 
resolved_by: 
verified_by: 
---

# FND-0027

## Finding

## Origin
Prose item `F-U11` extracted from the E-0013 F-U7..F-U13 obligation table, which carries the items recorded across sessions S-0036..S-0040.

## Finding
The obligation as stated in E-0013's own table. The source record is the authority; a verifier closes this row only with commands, outputs and hashes.

## Target
- Record: E-0013#F-U11

## Evidence
- Extracted by the verification-auditor's idempotent migration (`_obs/parts/extract_fu.py`), which skips any key already present as a `source_key:` in research/findings/.

## Resolution (fill when closing)
- ...

## Addendum 2026-09-30 — verification-auditor (Gate 3 seat) — **NOT DISCHARGED; row stays OPEN**

**This row is NOT closed, and I am not closing it.** Recording precisely what is missing.

**What the finding asks.** Re-derive E-00014's inner partition under the new normalized-FEN dedup
key, so its partition-integrity check (zero normalized-FEN overlap with the holdout, E-00014
abort 3) holds **structurally** rather than hopefully. Its `s_d_inner` / `delta_star` and the
contingency figures measured on the old corpus are superseded. (E-0013 F-U11 table row, L2224.)

**Commands I ran this session, and what they show.**

1. `Select-String research/sessions/S-0040-*.md -Pattern 'F-U11|inner partition|E-00014'` →
   `S-0040 L74: - **Did NOT read the holdout, fit anything, or run E-00014 / E-00015.**` and
   `L137: "… It gates E-00014 and every fitter, and nobody …"`. The most recent implementation session
   states it did not run or amend E-00014.
2. `Select-String research/experiments/E-0013-*.md -Pattern 'E-00014 is '` →
   `E-0013 L2697: E-00014 is 'status: PENDING', 'pre_registered: 2026-09-26', owner systems-researcher,
   and it needs the trainer, which does not exist yet.`
3. `E-0013 L2698-L2701`: E-00014's own text is still stale — *"Its own text is stale in the same way:
   L68 describes the corpus as the one produced by the GLOBAL-before-split exact-FEN dedup (F9)"*.
   The record still describes the **old** key.
4. The line that could be misread as a completion claim is not one. `E-0013 L2703-L2707` reads
   *"**What E-00014 needs before it may run.** (1) A dated amendment … (2) **F-U11 discharged**: the
   inner partition re-derived from the new corpus …"*. This is a **prerequisite list of what must
   happen before E-00014 may run**, and item (2) is stated as a *requirement*, not an achievement.
   L2708 confirms the state of play: *"the trainer built and verified — the single largest remaining
   engineering item, and **nothing in this session moved it**."*

**Exactly what is missing to discharge this row.**
(a) a dated amendment to E-00014 naming the new key at its L68 (not yet filed);
(b) the inner partition re-derived from the new corpus, with its own structural partition-integrity
    check (zero normalized-FEN overlap with the holdout, E-00014 abort 3);
(c) the trainer built and verified — E-00014 cannot run without it, and it does not exist;
(d) the split-map pin per Ruling 2, since E-00014 consumes the map read-only.

**Why I am not closing it, stated plainly.** The blocker is not paperwork; it is a **missing
artifact** (the trainer) plus a **stale pre-registration** in a PENDING record. Closing this row would
assert a structural invariant I cannot demonstrate — and the one thing this ledger is for is not
asserting what has not been shown. The fact that its severity is `major` and not `blocking` is why
it does not gate `imem.py lint`; that is a property of the schema, **not** evidence that it is done.

**Not touched by me (binding):** E-00014 stays `PENDING`; I did not run it, did not read the holdout,
did not read any label field, and did not fit anything. The trainer build belongs to the
`systems-researcher` / implementation seats, not to a verifier.


## Evidence
_commands, outputs, hashes_


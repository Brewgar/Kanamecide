---
id: FND-0011
type: finding
title: "F-U4 the E-0011 N1 backwards-citation correction (see B5 sentence 3).** Fil"
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

# FND-0011

## Origin
Prose item `F-U4` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> the E-0011 N1 backwards-citation correction (see B5 sentence 3).** Filed as

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `  Owner: researcher-architect. Due: at E-0013 close-out.
- **F-U4 - the E-0011 N1 backwards-citation correction (see B5 sentence 3).** Filed as
  an addendum to E-0011 **by the seat that owns E-0011**, at E-0013's close-out, naming
  R-0019 and B5. E-0011 and W-0001 are NOT edited by this record. Owner: **systems-researcher**`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (fill when closing)
- ...

## Addendum 2026-09-30 — verification-auditor (round-5 ledger-tail seat, Gate 3) — **NOT DISCHARGED; row stays OPEN**

**This row is NOT closed.** The E-0011 addendum it requires (the N1 backwards-citation correction,
naming R-0019 and B5) does not exist: E-0011's file contains no R-0019 reference at all.

**What the finding asks.** At E-0013's close-out, the seat that OWNS E-0011 (systems-researcher)
files an addendum to E-0011 correcting the N1 backwards citation, naming R-0019 and B5; E-0011 and
W-0001 are NOT edited by E-0013. (E-0013 L942-L945 = F-U4; B5's disposition row at L969: "F-U4 owns
the correction, by the owning seat, at E-0013 close-out".)

**Commands I ran this session, and what they show.**

1. Byte-wise scan of `research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md`
   (33,390 bytes, 535 lines; `_obs/probe_rows.py` → `_obs/probe.txt`) for "R-0019", "backwards",
   "76,887", "Q-0006" → **zero hits for "R-0019" and "backwards"**; the only numeric hit is the
   dataset's own L345 (the 76,887 estimate whose citation B5/DN2 corrects). No such addendum exists.
2. `git --no-pager log --oneline -10 -- <E-0011 path>` (`_obs/e11log.txt`) → last touch `0d8fbce`
   ("prepare first-training readiness prompt", S-0016 era) — BEFORE the obligation was filed; no
   correction commit was ever made.
3. E-0013 `status: RUNNING` → the due event (close-out) has not occurred.

**Exactly what is missing to discharge this row.**
(a) the E-0011 addendum by the owning seat, correcting the N1 citation and naming R-0019 and B5 —
    due at close-out;
(b) a record that the owner accepted the duty (E-0013 L944 names systems-researcher);
(c) close-out itself, so "at E-0013's close-out" is satisfiable.

**Not touched by me (binding):** I did not edit E-0011 or W-0001 (both are completed/verified
records; the correction belongs to E-0011's owner by design).


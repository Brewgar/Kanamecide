---
id: FND-0013
type: finding
title: "F-U6 DN6 routing.** Flag DEC-0010:186-187's stale "Pending: independent"
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

# FND-0013

## Origin
Prose item `F-U6` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> DN6 routing.** Flag DEC-0010:186-187's stale "Pending: independent

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `  Due: at E-0013 close-out.
- **F-U6 - DN6 routing.** Flag DEC-0010:186-187's stale "Pending: independent
  verification" line to the DEC-0010 owner. Non-blocking, no effect on this record.
  Owner: the DEC-0010 owner seat. Due: next DEC-0010 touch.`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (fill when closing)
- ...

## Addendum 2026-09-30 — verification-auditor (round-5 ledger-tail seat, Gate 3) — **NOT DISCHARGED; row stays OPEN**

**This row is NOT closed.** DEC-0010's stale line is still live, no DEC-0010 "next touch" has
occurred since the flag was filed, and no handoff to the DEC-0010 owner exists.

**What the finding asks.** Flag DEC-0010:186-187's stale "Pending: independent verification" line
(already discharged by R-0010) to the DEC-0010 owner. Non-blocking; zero effect on E-0013.
Due: next DEC-0010 touch. (E-0013 L952-L954 = F-U6; DN6 row at L898.)

**Commands I ran this session, and what they show.**

1. Byte-wise read of `research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md`
   (12,817 bytes, 215 lines; `_obs/probe.txt`) → L186-L187 still print: "- Pending: independent
   verification per DEC-0009 gate 3 (handoff filed to / verification-auditor; the verifier is never
   the owner)." The stale text is live.
2. `git --no-pager log --oneline -12 -- <DEC-0010 path>` (`_obs/declog.txt`) → exactly ONE commit
   touches DEC-0010 (`dac1a3f`, the S-0007 calibration that created it). The "next DEC-0010 touch"
   has NOT happened.
3. `Get-ChildItem research/handoffs -Name` → no handoff to the DEC-0010 owner about DN6/this line
   exists (the only historical DEC-0010-related handoff is HO-0002 to verification-auditor).
4. E-0013's DN6 row (L898) records the flag as "RECORDED and ROUTED, not fixed here" — recorded in
   E-0013, but not delivered.

**Exactly what is missing to discharge this row.**
(a) delivery of the flag to the DEC-0010 owner at/before DEC-0010's next touch (a handoff is the
    governed mechanism; none exists);
(b) the correction or dated annotation of DEC-0010 L186-L187 (R-0010 discharged the verification it
    still calls pending);
(c) or an owner ruling that the line is historical, recorded as such.

**Not touched by me (binding):** I did not edit DEC-0010 (not my record).


---
id: FND-0012
type: finding
title: "F-U5 Q-0006 readiness gate 7 (see B7).** On any terminal verdict this recor"
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

# FND-0012

## Origin
Prose item `F-U5` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> Q-0006 readiness gate 7 (see B7).** On any terminal verdict this record files

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `  (the seat named as `owner:` in E-0011's front matter). Due: E-0013 close-out.
- **F-U5 - Q-0006 readiness gate 7 (see B7).** On any terminal verdict this record files
  a handoff to **verification-auditor** (never the owner, never the seat that ran the
  fit) carrying `fitted_params_sha256`, the pre-fit commit hash, the split-map hash, the`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (fill when closing)
- ...

## Addendum 2026-09-30 — verification-auditor (round-5 ledger-tail seat, Gate 3) — **NOT DISCHARGED; row stays OPEN**

**This row is NOT closed.** Q-0006 readiness gate 7 fires on a TERMINAL verdict; E-0013 is still
RUNNING and no gate-7 handoff exists in `research/handoffs/`.

**What the finding asks.** On any terminal verdict (PASS-FIT-QUALITY-ONLY / FAIL / named
INCONCLUSIVE) E-0013 files a handoff to verification-auditor (never the owner, never the executor)
carrying `fitted_params_sha256`, the pre-fit commit hash, the split-map hash, the E-00014 and
E-00015 numbers, and the full command/exit-code ledger; no adoption/promotion/strength citation
before VERIFIED. (E-0013 L946-L951 = F-U5.)

**Commands I ran this session, and what they show.**

1. E-0013 front matter, byte-wise (`_obs/probe.txt`) → `status: RUNNING`, `result: null`: no
   terminal verdict; the gate has not fired.
2. `Get-ChildItem research/handoffs -Name` (`_obs/handoffs_list.txt`) → 20 handoffs, newest HO-0020
   (owner repair of FND-0030/FND-0031); no handoff carries this record's fitted-artifact hashes or
   a gate-7 purpose.
3. Q-0006 itself (`research/questions/Q-0006-self-play-data-pipeline.md`, L58-L69), read byte-wise →
   gate 7 verbatim: "The fit produces and pins `fitted_params_sha256`, loads exactly that artifact
   into the candidate, and receives independent verification. No adoption or strength claim precedes
   it." This matches the sentence E-0013 quotes at L1006-L1008 — the gate exists; only its
   activation is missing.
4. The obligation itself is intact at E-0013 L946-L951 (an obligation, not an achievement).

**Exactly what is missing to discharge this row.**
(a) E-0013 reaching a terminal verdict (status RUNNING; E-00014/E-00015 still PENDING);
(b) the gate-7 handoff with the named payload (artifact hash, pre-fit commit, split-map hash,
    E-00014/E-00015 numbers, command ledger);
(c) independent verification of the artifact (no such act exists).

**Not touched by me (binding):** I did not run any fit, did not read the holdout, and flipped no
status.


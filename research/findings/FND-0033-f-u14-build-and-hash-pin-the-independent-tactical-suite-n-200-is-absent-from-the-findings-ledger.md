---
id: FND-0033
type: finding
title: "F-U14 (build and hash-pin the independent tactical suite, N >= 200) is absent from the findings ledger"
status: OPEN
example: false
created: 2026-09-30
severity: major
target: E-0013#14-the-pre-fit-commit-can-it-be-assembled-now-no
raised_by: verification-auditor (round-5 ledger-tail seat; found by ledger-completeness scan)
review: E-0013
resolution: 
resolved_by: 
verified_by: 
---

# FND-0033

## Finding

E-0013's S-0039/S-0040 addenda record a NEW named obligation — **F-U14**: "build and hash-pin the
independent tactical suite (N >= 200), or record explicitly that conjunct (f) is not evaluable"
(E-0013 L2736-L2741, section 14). The record itself says why it must be tracked: it "is not in
F-U1..F-U13 and it was not in S-0038's escalation list"; it blocks the pre-fit commit (E-0013
L2730: the only existing suite, `tactics_set.py`, has 73 positions < N >= 200, is gitignored, and
its evidence record EV-0006 carries `sha256: null`); and S-0039 L90-L95 / S-0040 L131-L139 say its
ownership "is still unassigned and still blocking".

Every other F-U obligation exists as an FND row (F-U1..F-U6 = FND-0008..0013; F-U7..F-U10, F-U13 =
FND-0023..0026, FND-0029; F-U11/F-U12 = FND-0027/0028). F-U14 does not: byte-wise scans of
`research/findings/` return zero hits for "F-U14" or "tactical suite", while `research/sessions/`
returns six. The ledger therefore under-reports E-0013's open obligations by one — and the one it
misses is the one that blocks the pre-fit commit.

Severity `major` follows the corpus convention for F-U obligations (F-U7..F-U13 are major; they
likewise gate downstream artifacts without gating the lifecycle status). Not repaired here: filing
the row (or assigning an owner) is the owner's act; this record only names the gap.

## Evidence
- E-0013 L2728-L2741, read byte-wise (`_obs/probe.txt`, "E-0013 L2725-2760" section).
- `findstr /n /c:"F-U14" /c:"tactical suite" research/findings/*.md research/sessions/*.md research/reviews/*.md`
  → zero findings hits; session hits at S-0039 L47/L70/L90/L95 and S-0040 L80/L131/L139
  (`_obs/fu14_scan.txt`).
- Row id: the ledger's last pre-existing id was FND-0031; this row is the next CLI-assigned id
  (`imem.py new-finding`, anchor_ok: True).


---
id: EV-0004
type: evidence
title: "E-0002 certified /O2 bench (5 reps, pinned, SHA-256 logged)"
status: REGISTERED
path: build/Release/kana.exe
kind: measurement
sha256: null
regenerate: "build\\Release\\kana.exe --bench 5 (pinned, WMI clock proxy logged; self-SHA256 printed per run)"
retention: keep
cites: [E-0002]
example: false
created: 2026-09-19
last_updated: 2026-09-19
---

# EV-0004 — E-0002 certified /O2 baseline bench

## What this is
The certified perft-NPS baseline (43-47 Mnps, /O2) that certified Milestone 0 and unblocked O3.

## Where it lives
- The /O2 Release binary. NOTE: the E-0002-era measurement binary (historical sha256
  `a4c6b168…26d1`, commit 300bdeb) has since been REBUILT for E-0010; the binary now on disk
  is the E-0010 measurement build, sha256 `504eb01a…a6daa` (recorded in E-0010, verified in
  R-0004). An evidence hash pinned to a rebuilt path is a false claim: the sha256 here is
  therefore left null, and the historical hashes above are recorded as provenance, not as
  the live file's identity. (The evidence-drift check caught exactly this collision —
  working as intended.)

## How to regenerate / verify
```powershell
build\Release\kana.exe --bench 5   # per-position exact counts printed + E-00003 +-10% gate
```

## What it proves / supports
- E-0002 (certified baseline), the window vs E-00003 (all positions within +-10%):
  the O3 gate decision.
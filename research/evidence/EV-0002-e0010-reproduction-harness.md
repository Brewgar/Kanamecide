---
id: EV-0002
type: evidence
title: "E-0010 aggregator+estimator harness (reproduces every published number)"
status: REGISTERED
path: e0010_report.py
kind: harness
sha256: null
regenerate: "python e0010_report.py — reads e0010_k{1..6}n_result.txt + _games.jsonl (EV-0001) and prints the ladder + gates"
retention: keep
cites: [E-0010]
example: false
created: 2026-09-19
last_updated: 2026-09-19
---

# EV-0002 — E-0010 reproduction harness (aggregator + estimator)

## What this is
`e0010_report.py` (aggregator/independence checker) + `e0010_elo.py` (Bayesian Elo/LOS,
Beta(1,1)-posterior / incomplete-beta CI/LOS) + `e0010_match2.py` (random-opening match
driver) + `e0010_gates_bd.py` (symmetry + NPS gates). This is the reproduction path the
verification-auditor re-ran in R-0004.

## Where it lives
- Root: `e0010_report.py`, `e0010_elo.py`, `e0010_match2.py`, `e0010_gates_bd.py` (grandfathered
  as load-bearing tooling, not junk).

## How to regenerate / verify
```powershell
python e0010_report.py    # expects e0010_k6n_result.txt + _games.jsonl (EV-0001)
```

## What it proves / supports
- E-0010's every published number. Verified end-to-end by R-0004 (fresh agent, all numbers
  reproduced from these files).
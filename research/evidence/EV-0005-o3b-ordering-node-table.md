---
id: EV-0005
type: evidence
title: "O3b staged move-ordering node table (ORDER_STAGE 0-4, 11 positions, depth 6)"
status: REGISTERED
path: stage0.txt
kind: measurement
sha256: null
regenerate: "rebuild with ORDER_STAGE=0..4 and run measure_ob.py on the 11-position set"
retention: keep
cites: [E-00007]
example: false
created: 2026-09-19
last_updated: 2026-09-19
---

# EV-0005 — O3b staged ordering node table

## What this is
Node counts over the 11-position set at depth 6 per ORDER_STAGE (0 unordered .. 4 history):
254,655,158 -> 254,655,158 -> 40,869,716 -> 24,095,495 -> 22,534,970 (-91.2%).

## Where it lives
- `stage0.txt .. stage4.txt` (raw), summarized in E-00007. The counts, not the scratch file,
  are the load-bearing numbers.

## How to regenerate
```powershell
# configure each ORDER_STAGE=0..4, rebuild (Audit), then:
python measure_ob.py    # writes the per-position node/time/BF rows per stage
```

## What it proves / supports
- E-00007 PASS; the -91.2% node reduction and the per-lever attribution.
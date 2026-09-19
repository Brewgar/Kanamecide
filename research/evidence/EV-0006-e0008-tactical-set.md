---
id: EV-0006
type: evidence
title: "E-00008 tactical test set (73 self-validated positions) + qsearch effect"
status: REGISTERED
path: tactics_set.py
kind: dataset
sha256: null
regenerate: "python gen_tactics.py > tactics_gen.txt ; tactics_set.py (auto-generated validated positions) ; python measure_qs.py <exe> QSEARCH=0/1"
retention: keep
cites: [E-00008]
example: false
created: 2026-09-19
last_updated: 2026-09-19
---

# EV-0006 — E-00008 tactical test set + qsearch evidence

## What this is
73 self-validated positions (70 hanging + 3 mate-in-N) plus the O3b-vs-O3c pass/score table.
This is the permanent regression gate for quiescence (every later search change must re-run it).

## Where it lives
- `tactics_set.py` (generated, 73 positions), `tactics_gen.txt`, `measure_qs.py` (driver),
  `sum_qs.py` (scores). Summary in `oc4.txt`/`ob4.txt`.

## How to regenerate
```powershell
python gen_tactics.py    # + validation -> tactics_set.py
python measure_qs.py <build\Audit\kana.exe>    # prints pass/score per position
```

## What it proves / supports
- E-00008 PASS: qsearch finds 8 mate scores O3b misses and corrects 2 phantom overestimates;
  2.08x nodes. The H-0012 assert refinement is evidenced here too.
---
id: EV-0001
type: evidence
title: "E-0010 randomized self-play games, stage-6 vs stage-0 (240-game match)"
status: REGISTERED
path: e0010_k6n_games.jsonl
kind: raw-data
sha256: null
regenerate: "per-game JSONL is a one-way artifact; regenerate by re-running the campaign: python e0010_run_all.py (build\\Release\\kana.exe, stage6 vs stage0, N=240)"
retention: keep
cites: [E-0010]
example: false
created: 2026-09-19
last_updated: 2026-09-19
---

# EV-0001 — E-0010 k6n randomized self-play games (gate-c primary evidence)

## What this is
Per-game JSONL of the 240-game randomized-opening match (stage-6 full eval vs stage-0
material-only) that produced E-0010's headline: +116.1 Elo, CI95 [+70.8,+163.5], LOS 100%.

## Where it lives
- `e0010_k6n_games.jsonl` (+ `e0010_k1n..k5n_games.jsonl` for the per-term ladder) — LOCAL,
  gitignored, never in git history. Companion tallies `e0010_k6n_result.txt` etc.

## How to regenerate
```powershell
python e0010_run_all.py         # full 6-match campaign, 100ms+100ms, <=2 pairs concurrent
python e0010_report.py          # aggregate (Elo/CI/LOS/independence) from the raw JSONL
```

## Integrity
- Independence was PROVEN: the aggregator rebuilds every full move list and reports
  `duplicate-move-lists=0` on every rung (0 across all 1240 games).

## What it proves / supports
- E-0010 gates (a),(c); the per-term ladder; the honest FAIL of the >=150 bar.
- This is the data the H-0013 Texel fitting (Q-0001) would consume.
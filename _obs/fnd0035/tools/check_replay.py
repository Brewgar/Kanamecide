import json
from pathlib import Path

d = Path(__file__).resolve().parents[3] / "_obs" / "fnd0035" / "replay_d8_x3.json"
p = json.loads(d.read_text(encoding="utf-8"))
runs = p["per_run"]
print(f"runs recorded: {len(runs)}  depth: {p['depth']}  exe: {p['exe']}")
print(f"tool-reported identical: {p['identical']}")
sig = []
for i, r in enumerate(runs, 1):
    s = [(x["name"], x["nodes"], x["bestmove"]) for x in r]
    sig.append(s)
    tot = sum(x["nodes"] for x in r)
    print(f"  run {i}: positions={len(r)} total_nodes={tot:,}")
allsame = all(s == sig[0] for s in sig)
print(f"\nindependent re-check, all runs identical: {allsame}")
for j, (n, nodes, bm) in enumerate(sig[0]):
    row = " | ".join(f"r{i+1}={s[j][1]}" for i, s in enumerate(sig))
    print(f"  {n:14s} bm={bm:6s} {row}")
print(f"\nDETERMINISM REPLAY: {'PASS' if allsame else 'FAIL'}")
raise SystemExit(0 if allsame else 1)

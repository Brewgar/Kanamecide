#!/usr/bin/env python3
"""E-0010 post-match aggregator: reads e0010_kK_result.txt (written by e0010_match.py
on match completion), runs the Bayesian Elo/LOS gate on each term vs stage-0, and
prints the attribution table + gate (c) verdict. Usage: python e0010_report.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e0010_elo as E
BASE = r"C:\Users\tahae\Kanamecide"

def parse_result(tag):
    p = os.path.join(BASE, f"e0010_{tag}_result.txt")
    if not os.path.exists(p): return None
    lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
    head = (lines[0].split("total=")[1] if len(lines) > 0 and "total=" in lines[0] else "")
    res = []
    for ln in lines:
        if ln.startswith("results="):
            res = ln.split("results=",1)[1].split()
    w = res.count("A"); l = res.count("B"); d = res.count("D"); bad = res.count("BAD")
    return w, l, d, bad, len(res)

def main():
    print("=== E-0010 term-by-term Elo attribution (stage-K vs stage-0, 200 games) ===")
    print(f"{'stage':>6}{'W':>5}{'L':>5}{'D':>5}{'bad':>5}{'Wrate':>8}{'Elo(+/-sd)':>14}"
          f"{'CI95':>22}{'LOS':>9}")
    rows = []
    for k in range(1, 7):
        r = parse_result(f"k{k}")
        if not r: continue
        w, l, d, bad, n = r
        legal = (bad == 0)
        o = E.elli_analysis(w, l, d, f"k{k}", legal_ok=legal)
        rows.append((k, o, legal))
        ci = f"[{o['lo']:+.0f},{o['hi']:+.0f}]"
        print(f"{k:>6}{o['W']:>5}{o['L']:>5}{o['D']:>5}{bad:>5}"
              f"{o['W']/o['N']:>8.3f}{o['elo']:>+8.1f}{ci:>22}{o['los']*100:>8.2f}%")

    # Gate (a) legal-rate: 100% legal across all matches (BAD==0 and result present)
    legal_all = all(legal for (_,_,legal) in rows)
    # Gate (c): stage-6 (full eval) vs stage-0
    k6 = next((r for r in rows if r[0] == 6), None)
    print("\n=== Gate verdicts ===")
    print(f"(a) 100%% legal games self-play: {'PASS' if legal_all else 'FAIL'}  (bad games = "
          f"{sum(r[1]['N']-r[1]['W']-r[1]['L']-r[1]['D'] for r in rows)})")
    if k6:
        o = k6[1]
        ok_n = o["N"] >= 200
        ok_elo = o["elo"] >= 150
        ok_los = o["los"] >= 0.95
        print(f"(c) stage-6 vs stage-0: Elo={o['elo']:+.1f} bayes={o['elo_bayes']:+.1f} "
              f"CI95=[{o['lo']:+.1f},{o['hi']:+.1f}] LOS={o['los']*100:.2f}% N={o['N']}")
        print(f"    gate (c) PASS: N>=200({ok_n}) AND Elo>=150({ok_elo}) AND LOS>=95%({ok_los}) -> "
              f"{'PASS' if (ok_n and ok_elo and ok_los) else 'FAIL'}")
    else:
        print("(c) stage-6 result file not present yet (match still running).")

if __name__ == "__main__":
    main()

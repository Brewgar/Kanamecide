#!/usr/bin/env python3
"""E-0010 post-match aggregator v2: reads e0010_{tag}_result.txt / _games.jsonl
written by e0010_match2.py (randomized-opening driver), verifies game
independence (no duplicate full move lists), runs the Bayesian Elo/LOS gate on
each stage-K vs stage-0, and prints the attribution table + gate (c) verdict.
Usage: python e0010_report.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e0010_elo as E
BASE = r"C:\Users\tahae\Kanamecide"
TAGS = {1: "k1n", 2: "k2n", 3: "k3n", 4: "k4n", 5: "k5n", 6: "k6n"}

def parse_result(tag):
    p = os.path.join(BASE, f"e0010_{tag}_result.txt")
    if not os.path.exists(p): return None
    lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
    res = []
    for ln in lines:
        if ln.startswith("results="):
            res = ln.split("results=", 1)[1].split()
    w = res.count("A"); l = res.count("B"); d = res.count("D"); bad = res.count("BAD")
    return w, l, d, bad, len(res)

def independence(tag):
    """Verify all games are independent: no duplicate full move list
    (opening UCI + game SAN). Returns (n_games, n_dupes)."""
    p = os.path.join(BASE, f"e0010_{tag}_games.jsonl")
    if not os.path.exists(p): return 0, -1
    seen = set(); n = 0; dupes = 0
    for ln in open(p, encoding="utf-8", errors="replace"):
        try: rec = json.loads(ln)
        except Exception: continue
        key = " ".join(rec.get("opening", []) + rec.get("san", []))
        if not key: continue
        n += 1
        if key in seen: dupes += 1
        seen.add(key)
    return n, dupes

def main():
    print("=== E-0010 term-by-term Elo attribution (stage-K vs stage-0, randomized openings) ===")
    print(f"{'stage':>6}{'W':>5}{'L':>5}{'D':>5}{'bad':>5}{'games':>7}{'dupes':>7}{'Wrate':>8}"
          f"{'Elo':>9}{'CI95':>20}{'LOS':>9}")
    rows = []
    for k in range(1, 7):
        tag = TAGS[k]
        r = parse_result(tag)
        if not r: continue
        w, l, d, bad, n = r
        ngames, dupes = independence(tag)
        legal = (bad == 0)
        o = E.elli_analysis(w, l, d, f"k{k}", legal_ok=legal)
        rows.append((k, o, legal, ngames, dupes))
        ci = f"[{o['lo']:+.0f},{o['hi']:+.0f}]"
        print(f"{k:>6}{o['W']:>5}{o['L']:>5}{o['D']:>5}{bad:>5}{ngames:>7}{dupes:>7}"
              f"{o['W']/o['N']:>8.3f}{o['elo']:>+8.1f}{ci:>20}{o['los']*100:>8.2f}%")

    legal_all = all(legal for (_, _, legal, _, _) in rows)
    indep_all = all(dupes == 0 for (_, _, _, _, dupes) in rows)
    k6 = next((r for r in rows if r[0] == 6), None)
    print("\n=== Independence check (randomization scheme: 10 random legal plies,")
    print("    rng=Random(20260914*1000003+g), same opening for both engines, colors balanced) ===")
    for k, o, legal, ngames, dupes in rows:
        print(f"  k{k}: games={ngames} duplicate-move-lists={dupes} -> "
              f"{'INDEPENDENT' if dupes == 0 else 'NOT INDEPENDENT'}")
    print("\n=== Gate verdicts ===")
    print(f"(a) 100% legal games self-play: {'PASS' if legal_all else 'FAIL'}")
    print(f"    independence: {'PASS' if indep_all else 'FAIL'}")
    if k6:
        k, o, legal, ngames, dupes = k6
        ok_n = o["N"] >= 200
        ok_elo = o["elo"] >= 150
        ok_los = o["los"] >= 0.95
        ok_ind = dupes == 0
        verdict = "PASS" if (ok_n and ok_elo and ok_los and legal and ok_ind) else "FAIL"
        print(f"(c) stage-6 vs stage-0: Elo={o['elo']:+.1f} bayes={o['elo_bayes']:+.1f} "
              f"CI95=[{o['lo']:+.1f},{o['hi']:+.1f}] LOS={o['los']*100:.2f}% N={o['N']}")
        print(f"    N>=200({ok_n}) AND Elo>=150({ok_elo}) AND LOS>=95%({ok_los}) "
              f"AND legal({legal}) AND independent({ok_ind}) -> {verdict}")
    else:
        print("(c) stage-6 result file not present yet (match still running).")

if __name__ == "__main__":
    main()

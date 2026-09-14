#!/usr/bin/env python3
"""E-0010 gate (c) campaign runner: stage-6 vs stage-0 (240 games) plus the
per-term attribution ladder k=1..5 vs stage-0 (200 games each).
Max 2 engine-pairs (4 processes) concurrent. Writes e0010_ALL_done.txt at end.
"""
import subprocess, sys, os, time

BASE = r"C:\Users\tahae\Kanamecide"
EXE  = os.path.join(BASE, "build", "Release", "kana.exe")
PY   = sys.executable
SEED0= "20260914"

# (stage, games, tag) — k6 first so the headline verdict lands earliest
RUNS = [(6, 240, "k6n"), (1, 200, "k1n"), (2, 200, "k2n"),
        (3, 200, "k3n"), (4, 200, "k4n"), (5, 200, "k5n")]

def run_pair(pair):
    procs = []
    for stage, games, tag in pair:
        log = open(os.path.join(BASE, f"e0010_{tag}_log.txt"), "w")
        p = subprocess.Popen([PY, os.path.join(BASE, "e0010_match2.py"), EXE,
                              str(stage), str(games), tag, BASE, SEED0],
                             cwd=BASE, stdout=log, stderr=subprocess.STDOUT)
        procs.append((p, log, tag))
    for p, log, tag in procs:
        p.wait(); log.close()
        print(f"[runner] {tag} exit={p.returncode}", flush=True)

def main():
    t0 = time.time()
    for i in range(0, len(RUNS), 2):
        pair = RUNS[i:i+2]
        print(f"[runner] wave {pair} t={time.time()-t0:.0f}s", flush=True)
        run_pair(pair)
    with open(os.path.join(BASE, "e0010_ALL_done.txt"), "w") as f:
        f.write(f"elapsed={time.time()-t0:.0f}s\n")

if __name__ == "__main__":
    main()

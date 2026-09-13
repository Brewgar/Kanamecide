#!/usr/bin/env python3
"""E-0010 watchdog: poll match progress; when all 6 stage-matches finish, run the
final gate (c) report + clean gate (d) bench + clean gate (a) perft audit (no match
contention), writing _final.txt. Spawned detached so it survives agent shell turnover."""
import os, sys, time, subprocess, glob
BASE = r"C:\Users\tahae\Kanamecide"
EXE  = os.path.join(BASE, "build", "Release", "kana.exe")

def gc(tag):
    p = os.path.join(BASE, f"e0010_{tag}.txt")
    if not os.path.exists(p): return -1
    try:
        return len(open(p, encoding="utf-8", errors="replace").read().splitlines()) - 1
    except Exception:
        return -1

def run_with_dg_retry(args, out_path, attempts=60, delay=5):
    for _ in range(attempts):
        w = open(out_path, "w")
        r = subprocess.run(args, cwd=BASE, stdout=w, stderr=subprocess.STDOUT, timeout=1200)
        w.close()
        txt = open(out_path, encoding="utf-8", errors="replace").read()
        if "blocked by your organization" not in txt:
            return r.returncode
        time.sleep(delay)
    return -1

def main():
    ticks = 0
    last = {}
    while ticks < 240:  # ~3h cap
        ticks += 1
        line = f"[{time.strftime('%H:%M:%S')}] "
        all_done = True
        for k in range(1, 7):
            tag = f"k{k}"
            rf = os.path.join(BASE, f"e0010_{tag}_result.txt")
            if os.path.exists(rf):
                line += f"{tag}:DONE "; continue
            all_done = False
            n = gc(tag)
            line += f"{tag}:g{n} "
        line = line.rstrip()
        with open(os.path.join(BASE, "_watchdog.txt"), "a") as f:
            f.write(line + "\n")
        if all_done:
            with open(os.path.join(BASE, "_watchdog.txt"), "a") as f:
                f.write("ALL MATCHES DONE -> running final gates\n")
            # gate (c) attribution + verdict
            rp = run_with_dg_retry([sys.executable, "e0010_report.py"],
                                   os.path.join(BASE, "_report.txt"))
            # gate (d) clean bench (no match contention now)
            run_with_dg_retry([EXE, "--bench", "5"],
                              os.path.join(BASE, "_g0_bench_clean.txt"))
            # gate (a) clean perft (re-confirm bit-identity on match binary)
            run_with_dg_retry([EXE], os.path.join(BASE, "_g0_perft_clean.txt"))
            with open(os.path.join(BASE, "_watchdog.txt"), "a") as f:
                f.write(f"FINAL_GATES_DONE report_rc={rp}\nALL_DONE\n")
            return
        time.sleep(45)
    with open(os.path.join(BASE, "_watchdog.txt"), "a") as f:
        f.write("WATCHDOG_TIMEOUT (3h)\n")

if __name__ == "__main__":
    main()

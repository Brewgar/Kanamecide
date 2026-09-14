#!/usr/bin/env python3
"""Detached waiter: poll for e0010_ALL_done.txt (match campaign finished),
then run gates (b)+(d) uncontended. Writes e0010_waiter_done.txt at the end.
Timeout: 5 hours."""
import os, time, subprocess, sys

BASE = r"C:\Users\tahae\Kanamecide"
deadline = time.time() + 5 * 3600
while not os.path.exists(os.path.join(BASE, "e0010_ALL_done.txt")):
    if time.time() > deadline:
        sys.exit("timeout waiting for match campaign")
    time.sleep(60)
time.sleep(10)  # let file IO settle
subprocess.run([sys.executable, os.path.join(BASE, "e0010_gates_bd.py")], cwd=BASE)
with open(os.path.join(BASE, "e0010_waiter_done.txt"), "w") as f:
    f.write("waiter complete\n")

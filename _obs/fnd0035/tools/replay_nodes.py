#!/usr/bin/env python3
"""FND-0035 F2/F3 repair - deterministic node-count + determinism harness.

NOTHING here interprets strength. It emits raw node counts / bestmoves only.

SUBCOMMANDS
  nodes   'go depth D' over the 11-position act_E00007 set, one pass -> CSV rows.
          Used for the pre/post node-count table (D=6) and for the determinism replay (D=8).
  replay  'go depth D' over the set, R times, and CHECK that the (nodes, bestmove) pair is
          bit-identical across all R runs. Exits 3 on any divergence.
"""
from __future__ import annotations

import argparse
import csv
import json
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]   # _obs/fnd0035/tools/<this> -> repo root
POSITIONS = ROOT / "research" / "positions" / "act_E00007.fen"


def load_positions() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for raw in POSITIONS.read_text(encoding="utf-8-sig").splitlines():
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        name, _, fen = line.partition("\t")
        rows.append((name.strip(), fen.strip()))
    return rows


def read_lines(proc: subprocess.Popen, q: "queue.Queue") -> None:
    for line in proc.stdout:
        q.put(line.rstrip("\r\n"))
    q.put("__EOF__")


def send(proc: subprocess.Popen, line: str) -> None:
    proc.stdin.write(line + "\n")
    proc.stdin.flush()


def await_line(q: "queue.Queue", deadline: float, what: str) -> str:
    left = deadline - time.time()
    if left <= 0:
        raise TimeoutError(f"stall waiting for {what}")
    try:
        got = q.get(timeout=left)
    except queue.Empty as exc:
        raise TimeoutError(f"stall waiting for {what}") from exc
    if got == "__EOF__":
        raise RuntimeError(f"engine closed stdout while waiting for {what}")
    return got


def open_engine(exe: str):
    proc = subprocess.Popen([exe, "uci"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            text=True, bufsize=1)
    q: "queue.Queue" = queue.Queue()
    threading.Thread(target=read_lines, args=(proc, q), daemon=True).start()
    send(proc, "uci")
    return proc, q


def handshake(proc, q) -> None:
    deadline = time.time() + 30
    while await_line(q, deadline, "uciok").strip() != "uciok":
        pass


def go(proc, q, fen: str, depth: int, timeout: float) -> dict:
    """One 'position' + 'go depth N'. Returns the last info line's parsed fields."""
    send(proc, "ucinewgame")
    send(proc, "position startpos" if fen == "startpos" else f"position fen {fen}")
    send(proc, f"go depth {depth}")
    deadline = time.time() + timeout
    info: dict = {}
    while True:
        line = await_line(q, deadline, f"bestmove after 'go depth {depth}'").strip()
        if line.startswith("info") and " depth " in f" {line} ":
            parts = line.split()
            try:
                score = parts[parts.index("score") + 1] + " " + parts[parts.index("score") + 2]
                info = {
                    "depth": int(parts[parts.index("depth") + 1]),
                    "nodes": int(parts[parts.index("nodes") + 1]),
                    "score": score,
                }
            except (ValueError, IndexError):
                pass
        elif line.startswith("bestmove"):
            return {"nodes": info.get("nodes"), "bestmove": line.split()[1],
                    "score": info.get("score"), "depth_reached": info.get("depth")}

def run_pass(exe: str, depth: int, timeout: float) -> list:
    proc, q = open_engine(exe)
    try:
        handshake(proc, q)
        rows = []
        for name, fen in load_positions():
            r = go(proc, q, fen, depth, timeout)
            r["name"] = name
            rows.append(r)
        return rows
    finally:
        try:
            send(proc, "quit")
            proc.wait(timeout=10)
        except Exception:
            proc.kill()


def cmd_nodes(a: argparse.Namespace) -> int:
    rows = run_pass(a.exe, a.depth, a.timeout)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["name", "depth", "nodes", "bestmove", "score"])
        for r in rows:
            w.writerow([r["name"], a.depth, r["nodes"], r["bestmove"], r.get("score")])
    total = sum(r["nodes"] or 0 for r in rows)
    print(json.dumps({"exe": a.exe, "depth": a.depth, "positions": len(rows),
                      "total_nodes": total, "out": str(out)}, indent=2))
    return 0


def cmd_replay(a: argparse.Namespace) -> int:
    runs = []
    for i in range(a.runs):
        t0 = time.time()
        runs.append(run_pass(a.exe, a.depth, a.timeout))
        print(f"[replay] run {i+1}/{a.runs} done in {time.time()-t0:.1f}s", flush=True)
    ok = True
    base = runs[0]
    for i, rows in enumerate(runs[1:], start=2):
        for b, r in zip(base, rows):
            if (b["nodes"], b["bestmove"]) != (r["nodes"], r["bestmove"]):
                ok = False
                print(f"DIVERGENCE run1 vs run{i} {b['name']}: "
                      f"{b['nodes']}/{b['bestmove']} vs {r['nodes']}/{r['bestmove']}")
    payload = {
        "exe": a.exe, "depth": a.depth, "runs": a.runs,
        "identical": ok,
        "per_run": [[{"name": r["name"], "nodes": r["nodes"], "bestmove": r["bestmove"]}
                     for r in rows] for rows in runs],
    }
    Path(a.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[replay] identical={ok} runs={a.runs} depth={a.depth} -> {a.out}")
    return 0 if ok else 3


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("nodes")
    n.add_argument("--exe", default="build/Release/kana.exe")
    n.add_argument("--depth", type=int, default=6)
    n.add_argument("--timeout", type=float, default=900.0)
    n.add_argument("--out", required=True)
    n.set_defaults(fn=cmd_nodes)
    r = sub.add_parser("replay")
    r.add_argument("--exe", default="build/Release/kana.exe")
    r.add_argument("--depth", type=int, default=8)
    r.add_argument("--runs", type=int, default=3)
    r.add_argument("--timeout", type=float, default=3600.0)
    r.add_argument("--out", required=True)
    r.set_defaults(fn=cmd_replay)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())

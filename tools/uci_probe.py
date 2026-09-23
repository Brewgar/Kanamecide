#!/usr/bin/env python3
"""Prove the explicit argv-based UCI entry path and capture a protocol transcript."""
from __future__ import annotations

import argparse
import queue
import subprocess
import threading
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exe", default="build/Release/kana.exe")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    exe = str(Path(args.exe).resolve())
    lines: list[str] = []
    proc = subprocess.Popen(
        [exe, "uci"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )
    output: queue.Queue[str | None] = queue.Queue()

    def pump() -> None:
        assert proc.stdout is not None
        for line in proc.stdout:
            output.put(line.rstrip("\r\n"))
        output.put(None)

    threading.Thread(target=pump, daemon=True).start()

    def exchange(command: str, sentinel: str | None, timeout: float = 10.0) -> str | None:
        assert proc.stdin is not None
        lines.append(f"> {command}")
        proc.stdin.write(command + "\n")
        proc.stdin.flush()
        if sentinel is None:
            return None
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                line = output.get(timeout=max(0.01, deadline - time.monotonic()))
            except queue.Empty:
                continue
            if line is None:
                raise RuntimeError(f"EOF while waiting for {sentinel!r}")
            lines.append(line)
            if line == sentinel or line.startswith(sentinel + " "):
                return line
        raise TimeoutError(f"timeout waiting for {sentinel!r}")

    try:
        exchange("uci", "uciok")
        exchange("isready", "readyok")
        exchange("position startpos", None)
        exchange("go depth 1", "bestmove", timeout=10.0)
    finally:
        try:
            assert proc.stdin is not None
            lines.append("> quit")
            proc.stdin.write("quit\n")
            proc.stdin.flush()
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
            proc.wait(timeout=3)
        exit_code = proc.returncode
        lines.append(f"EXIT={exit_code}")
        lines.append(f"ARGV0={exe}")
        lines.append("ARGV1=uci")
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("\n".join(lines))
    return int(exit_code or 0)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Engine/CuteChess detection + UCI smoke check."""
from __future__ import annotations

import queue
import shutil
import subprocess
import threading
import time
from pathlib import Path

from .backend import ROOT


def detect_engines(settings: dict) -> dict:
    kana = settings.get("kana_engine", "")
    if not kana:
        for c in (ROOT / "build" / "Release" / "kana.exe",
                  ROOT / "build" / "Release" / "kana",
                  ROOT / "build" / "kana.exe"):
            if c.is_file():
                kana = str(c)
                break
    cute = settings.get("cutechess", "")
    if not cute:
        found = shutil.which("cutechess") or shutil.which("cutechess-gui")
        if found:
            cute = found
    return {"kana_engine": kana, "cutechess": cute,
            "stockfish": settings.get("stockfish", "")}


class UciEngine:
    """Minimal UCI client: boot handshake + one fixed-node move."""

    def __init__(self, exe: str):
        self.exe = exe
        self.proc: subprocess.Popen | None = None
        self._q: queue.Queue[str] = queue.Queue()

    def _pump(self) -> None:
        assert self.proc is not None and self.proc.stdout is not None
        for line in self.proc.stdout:
            self._q.put(line.rstrip("\n"))

    def start(self, extra_argv: list[str] | None = None) -> None:
        argv = [self.exe] + (extra_argv or [])
        self.proc = subprocess.Popen(
            argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, bufsize=1,
            encoding="utf-8", errors="replace")
        th = threading.Thread(target=self._pump, daemon=True)
        th.start()

    def send(self, cmd: str) -> bool:
        try:
            assert self.proc is not None and self.proc.stdin is not None
            self.proc.stdin.write(cmd + "\n")
            self.proc.stdin.flush()
            return True
        except Exception:
            return False

    def wait_for(self, token: str, timeout: float) -> str | None:
        end = time.time() + timeout
        buf: list[str] = []
        while time.time() < end:
            try:
                line = self._q.get(timeout=0.1)
            except queue.Empty:
                continue
            buf.append(line)
            if token in line:
                return "\n".join(buf)
        return None

    def stop(self) -> None:
        try:
            if self.proc is not None:
                self.send("quit")
                try:
                    self.proc.wait(timeout=3)
                except Exception:
                    self.proc.kill()
        except Exception:
            pass


def _launch_variants(exe: str) -> list[list[str]]:
    """argv variants: bare first (Stockfish et al), then ["uci"] (kana.exe).

    kana.exe only enters its UCI loop when argv[1] == "uci" (src/main.cpp);
    the repo's own drivers (e0010_match2.py) launch it that way.
    """
    name = Path(exe).name.lower()
    if name.startswith("kana"):
        return [[exe, "uci"]]
    return [[exe], [exe, "uci"]]


def _handshake(eng: UciEngine, timeout: float) -> bool:
    eng.send("uci")
    if eng.wait_for("uciok", timeout) is None:
        return False
    eng.send("isready")
    return eng.wait_for("readyok", timeout) is not None


def uci_smoke(exe: str, timeout: float = 10.0) -> tuple[bool, str]:
    """Boot handshake + one `go depth 1` move. Returns (ok, detail)."""
    if not exe or not Path(exe).is_file():
        return False, f"engine not found: {exe!r}"
    last = ""
    for argv in _launch_variants(exe):
        eng = UciEngine(exe)
        try:
            eng.start(argv[1:])
        except Exception as exc:
            last = f"cannot launch {argv}: {exc}"
            continue
        try:
            if not _handshake(eng, timeout):
                last = f"no uciok/readyok via {argv}"
                continue
            eng.send("ucinewgame")
            eng.send("isready")
            if eng.wait_for("readyok", timeout) is None:
                last = "no readyok after ucinewgame"
                continue
            eng.send("position startpos")
            eng.send("go depth 1")
            got = eng.wait_for("bestmove", timeout)
            if got is None:
                last = "no bestmove at depth 1"
                continue
            for line in got.splitlines():
                if "bestmove" in line:
                    return True, f"uciok + readyok + {line.strip()}"
            last = "bestmove missing"
        finally:
            eng.stop()
    return False, last or "engine did not answer uci"

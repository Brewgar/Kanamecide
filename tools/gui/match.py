#!/usr/bin/env python3
"""Minimal casual engine-vs-engine game (NOT a strength claim).

Plays one game at fixed depth between two UCI engines with alternating
colors handled by the caller. Used by the GUI 'Play test game' button and
by headless verification. Anything statistical needs its own
pre-registration; this reports moves + result only.
"""
from __future__ import annotations

from .engines import UciEngine, _handshake, _launch_variants


def _boot(exe: str, timeout: float):
    for argv in _launch_variants(exe):
        eng = UciEngine(exe)
        try:
            eng.start(argv[1:])
        except Exception:
            continue
        if _handshake(eng, timeout):
            eng.send("ucinewgame")
            eng.send("isready")
            eng.wait_for("readyok", timeout)
            return eng
        try:
            eng.stop()
        except Exception:
            pass
    return None


def _get_move(eng: UciEngine, moves: list[str], depth: int,
              timeout: float) -> str | None:
    pos = "position startpos" + (" moves " + " ".join(moves) if moves else "")
    if not eng.send(pos):
        return None
    if not eng.send(f"go depth {depth}"):
        return None
    got = eng.wait_for("bestmove", timeout)
    if got is None:
        return None
    for line in got.splitlines():
        if "bestmove" in line:
            parts = line.strip().split()
            try:
                mv = parts[parts.index("bestmove") + 1]
            except (ValueError, IndexError):
                return None
            if mv in ("(none)", "0000", ""):
                return None
            return mv
    return None


def play_game(exe_a: str, exe_b: str, depth: int = 2,
              max_plies: int = 120,
              timeout: float = 15.0) -> dict:
    """Play one game, A as White. Returns dict(moves, result, reason)."""
    a = _boot(exe_a, timeout)
    if a is None:
        return {"moves": [], "result": "0-0*", "reason": "A: no uciok"}
    if exe_b == exe_a:
        # Two processes of the same binary for self-play (one pipe per
        # engine; never share a process between the two sides).
        b = _boot(exe_b, timeout)
    else:
        b = _boot(exe_b, timeout)
    if b is None:
        try:
            a.stop()
        except Exception:
            pass
        return {"moves": [], "result": "0-0*", "reason": "B: no uciok"}
    try:
        moves: list[str] = []
        # Honest casual adjudication WITHOUT a board model:
        # - position keys = full UCI move history (repeats only on exact
        #   game-line cycles);
        # - a "no bestmove" reply is reported as-is (mate/stalemate vs
        #   engine failure cannot be distinguished without legality);
        # - running out of plies is reported undecided, never a result.
        seen: dict[str, int] = {}
        for ply in range(max_plies):
            eng = a if ply % 2 == 0 else b
            mv = _get_move(eng, moves, depth, timeout)
            if mv is None:
                return {"moves": moves, "result": "0-0*",
                        "reason": f"no bestmove reply at ply {ply} "
                        "(terminal position or engine failure; "
                        "unadjudicated without a board model)"}
            moves.append(mv)
            key = " ".join(moves)  # exact game-line position key
            seen[key] = seen.get(key, 0) + 1
            if seen[key] >= 3:
                return {"moves": moves, "result": "1/2-1/2",
                        "reason": "exact game-line repetition x3"}
        return {"moves": moves, "result": "0-0*",
                "reason": f"max plies {max_plies} reached (undecided)"}
    finally:
        a.stop()
        b.stop()

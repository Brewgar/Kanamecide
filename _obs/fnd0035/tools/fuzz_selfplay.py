#!/usr/bin/env python3
"""FND-0035 F2/F3 repair - fuzz: N random-mover self-play games, crash/stall/illegal watch.

Same shape and same decision surface as the repo's `random_selfplay.py` (engine vs a random
legal mover, python-chess enforcing legality and adjudicating the result). Differences, all
recorded deliberately:
  - games / depth / seed / engine are CLI args (the repo script hardcodes 30 @ depth 4);
  - every engine interaction has a HARD WALL-CLOCK DEADLINE, so a non-terminating search is
    recorded as a STALL instead of hanging the run forever;
  - a non-zero/ crash exit, an unreadable/absent `bestmove`, an illegal move, and a
    >250-ply cap are each recorded with their own counter;
  - the engine process is RESTARTED after every game, so one wedged process cannot poison the
    rest of the run and cannot hide a later failure.

THIS IS A ROBUSTNESS FUZZ, NOT A STRENGTH MEASUREMENT. It reports no Elo and no win rate as
a verdict; the win-rate line is printed for the record only. The gate is:
    crashes == 0 AND stalls == 0 AND missing_bestmove == 0 AND illegal == 0
`plycap` (a game reaching the 250-ply move cap) is COUNTED and REPORTED but is not a gate
term: against a random mover a long game is a game-length outcome, not a robustness failure.
"""
from __future__ import annotations

import argparse
import json
import queue
import random
import subprocess
import sys
import threading
import time
from pathlib import Path

import chess

MOVE_TIMEOUT = 60.0      # one 'go depth N' must answer with bestmove inside this
HANDSHAKE_TIMEOUT = 30.0
PLY_CAP = 250


def pump(proc, q):
    for line in proc.stdout:
        q.put(line.rstrip("\r\n"))
    q.put("__EOF__")


def send(proc, line):
    proc.stdin.write(line + "\n")
    proc.stdin.flush()


def await_line(q, deadline, what):
    left = deadline - time.time()
    if left <= 0:
        raise TimeoutError(f"stall waiting for {what}")
    try:
        got = q.get(timeout=left)
    except queue.Empty as exc:
        raise TimeoutError(f"stall waiting for {what}") from exc
    if got == "__EOF__":
        raise RuntimeError("engine closed stdout (crash / early exit)")
    return got


def spawn(exe):
    proc = subprocess.Popen([exe, "uci"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            text=True, bufsize=1)
    q = queue.Queue()
    threading.Thread(target=pump, args=(proc, q), daemon=True).start()
    send(proc, "uci")
    await_line(q, time.time() + HANDSHAKE_TIMEOUT, "uciok")
    return proc, q


def engine_bestmove(proc, q, board, depth, move_no):
    parts = ["position", "startpos"]
    if board.move_stack:
        parts.append("moves")
        parts.extend(m.uci() for m in board.move_stack)
    send(proc, " ".join(parts))
    send(proc, f"go depth {depth}")
    deadline = time.time() + MOVE_TIMEOUT
    while True:
        line = await_line(q, deadline, f"bestmove (game ply {move_no})").strip()
        if line.startswith("bestmove"):
            toks = line.split()
            if len(toks) < 2 or toks[1] == "0000":
                raise LookupError(f"missing bestmove: {line!r}")
            return toks[1]


def play_game(exe, depth, rng):
    """Returns (outcome_label, detail). outcome_label in
    {'ok', 'illegal', 'stall', 'missing_bestmove', 'crash', 'plycap'}."""
    proc = q = None
    last_fen = [None]
    try:
        proc, q = spawn(exe)
        board = chess.Board()
        send(proc, "ucinewgame")
        move_no = 0
        while not board.is_game_over():
            move_no += 1
            if move_no > PLY_CAP:
                return "plycap", f"exceeded {PLY_CAP} plies"
            if board.turn == chess.WHITE:
                last_fen[0] = board.fen()
                uci = engine_bestmove(proc, q, board, depth, move_no)
                try:
                    mv = board.parse_uci(uci)
                except ValueError:
                    return "illegal", f"unparseable move string {uci!r}"
                if mv not in board.legal_moves:
                    return "illegal", f"{uci} not legal in {board.fen()}"
                board.push(mv)
            else:
                board.push(rng.choice(list(board.legal_moves)))
        return "ok", board.result()
    except TimeoutError as exc:
        return "stall", str(exc)
    except LookupError as exc:
        return "missing_bestmove", str(exc)
    except RuntimeError as exc:
        # stdout closed before bestmove: the engine exited on its own. Distinguish a
        # self-inflicted crash from an external kill by the OS exit code:
        #   0xC0000005 (-1073741819) = access violation (a REAL crash -> DEC-0010 counts it a LOSS)
        #   1 / 0xC000013A (-1073741510) = normal-ish exit / CTRL_C_EVENT (an external kill)
        rc = proc.poll() if proc is not None else None
        return "crash", (f"{exc} | exit_code={rc} | "
                         f"{'REAL ACCESS VIOLATION' if rc == -1073741819 else 'external/normal exit'}"
                         f" | last_fen={last_fen[0] if last_fen else '?'}")
    except Exception as exc:                      # noqa: BLE001 - recorded, never raised
        return "crash", f"{type(exc).__name__}: {exc}"
    finally:
        if proc is not None:
            try:
                proc.kill()
                proc.wait(timeout=5)
            except Exception:
                pass


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--exe", default="build/Release/kana.exe")
    ap.add_argument("--games", type=int, default=1000)
    ap.add_argument("--depth", type=int, default=4)
    ap.add_argument("--seed", type=int, default=20261003)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    rng = random.Random(a.seed)
    t0 = time.time()
    labels = ["ok", "illegal", "stall", "missing_bestmove", "crash", "plycap"]
    counts = {k: 0 for k in labels}
    results = {"1-0": 0, "0-1": 0, "1/2-1/2": 0, "*": 0}
    failures = []
    for g in range(a.games):
        engine_white = (g % 2 == 0)
        label, detail = play_game(a.exe, a.depth, rng)
        counts[label] += 1
        if label == "ok":
            results[detail] = results.get(detail, 0) + 1
        else:
            failures.append({"game": g + 1, "engine_white": engine_white,
                             "label": label, "detail": detail})
            print(f"game {g+1}: {label} :: {detail}", flush=True)
        if (g + 1) % 50 == 0:
            print(f"[fuzz] {g+1}/{a.games} games, {time.time()-t0:.0f}s, "
                  f"failures={len(failures)}", flush=True)

    # The gate is EXACTLY the one this repair was commissioned against: zero crashes, zero
    # stalls, zero missing-bestmove (plus zero illegal moves, which is the same legality class
    # DEC-0010 counts as a LOSS). `plycap` is recorded but NOT gated: hitting the 250-ply cap
    # is a legitimate GAME-LENGTH outcome against a random mover (neither side can force mate
    # quickly enough in every game), not a robustness failure. It is reported either way.
    gate = {k: counts[k] for k in ("illegal", "stall", "missing_bestmove", "crash")}
    gated_plycap = counts["plycap"]
    passed = all(v == 0 for v in gate.values())
    payload = {
        "exe": a.exe, "games": a.games, "depth": a.depth, "seed": a.seed,
        "wall_seconds": round(time.time() - t0, 1),
        "counts": counts, "results": results,
        "gate": gate,
        "gate_rule": "crashes == 0 AND stalls == 0 AND missing_bestmove == 0 AND illegal == 0",
        "recorded_not_gated": {
            "plycap": gated_plycap,
            "why": "a game reaching the 250-ply cap is a game-length outcome against a random "
                   "mover, not a crash/stall/missing-bestmove; disclosed, not gated",
        },
        "verdict": "PASS" if passed else "FAIL",
        "failures": failures,
        "note": "robustness fuzz only; no strength claim, no Elo, no SPRT",
    }
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({k: payload[k] for k in
                      ("games", "depth", "counts", "gate", "verdict", "wall_seconds")},
                     indent=2))
    return 0 if passed else 4


if __name__ == "__main__":
    sys.exit(main())

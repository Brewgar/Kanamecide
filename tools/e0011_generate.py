#!/usr/bin/env python3
"""E-0011 resumable self-play generator and deterministic recovery drill."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import queue
import random
import re
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import chess

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EXE = ROOT / "build" / "Release" / "kana.exe"
SALT = 20260922
STAGE = 6
N_OPEN = 10
MAX_PLIES = 300
TC = "100ms+100ms inc"
TC_COMMAND = "go wtime 1500 btime 1500 winc 100 binc 100"
MOVE_TIMEOUT = 5.0
END_VOCABULARY = {
    "mate", "stalemate", "draw-material", "rule50", "repetition", "plycap", "crash"
}
MANDATORY_FIELDS = {
    "game_id", "campaign_salt", "seed_int", "opening", "a_white", "b_white",
    "eval_stage_a", "eval_stage_b", "binary_sha256", "src_commit", "tc", "tc_command",
    "time_started", "time_finished", "res", "end", "end_seconds", "plies", "san",
    "crash_incident", "crash_incident_text",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def derive_opening(game_id: int) -> list[str]:
    rng = random.Random(SALT * 1_000_003 + game_id)
    board = chess.Board()
    opening: list[str] = []
    for _ in range(N_OPEN):
        # Reject only an immediately terminal candidate. This preserves the exact pinned
        # RNG seed while guaranteeing the preregistered ten-ply legal opening.
        choices = list(board.legal_moves)
        rng.shuffle(choices)
        move = None
        for candidate in choices:
            probe = board.copy(stack=False)
            probe.push(candidate)
            if not probe.is_game_over():
                board.push(candidate)
                move = candidate
                break
        if move is None:
            raise RuntimeError(f"no live tenth-ply continuation at game_id={game_id}")
        opening.append(move.uci())
    return opening


def validate_san(opening: list[str], san: list[str]) -> chess.Board:
    board = chess.Board()
    for uci in opening:
        move = chess.Move.from_uci(uci)
        if move not in board.legal_moves:
            raise ValueError(f"illegal opening move {uci}")
        board.push(move)
    for token in san:
        try:
            board.push_san(token)
        except Exception as exc:
            raise ValueError(f"illegal SAN move {token!r}: {exc}") from exc
    return board


def classify_end(board: chess.Board, plies: int) -> str:
    if board.is_checkmate():
        return "mate"
    if board.is_stalemate():
        return "stalemate"
    # R-0016 pinned overlap precedence.
    if board.can_claim_fifty_moves():
        return "rule50"
    if board.is_repetition(3):
        return "repetition"
    if board.is_insufficient_material():
        return "draw-material"
    if plies >= MAX_PLIES:
        return "plycap"
    raise RuntimeError("non-terminal board escaped adjudication")


def append_fsync(path: Path, record: dict[str, Any], lock: threading.Lock | None = None) -> None:
    data = (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    if lock is None:
        with path.open("ab") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        return
    with lock:
        with path.open("ab") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())


class Engine:
    def __init__(self, exe: Path, stage: int):
        self.stage = stage
        self.proc = subprocess.Popen(
            [str(exe), "uci"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
            errors="replace", bufsize=1,
        )
        self.lines = queue.Queue()
        threading.Thread(target=self._pump, daemon=True).start()
        if self.exchange("uci", "uciok", 8.0) is None:
            raise RuntimeError("UCI handshake failed: no uciok")

    def _pump(self) -> None:
        assert self.proc.stdout is not None
        for line in self.proc.stdout:
            self.lines.put(line.rstrip("\r\n"))
        self.lines.put(None)

    def send(self, command: str) -> bool:
        try:
            assert self.proc.stdin is not None
            self.proc.stdin.write(command + "\n")
            self.proc.stdin.flush()
            return True
        except (BrokenPipeError, OSError):
            return False

    def exchange(self, command: str, sentinel: str, timeout: float) -> str | None:
        if not self.send(command):
            return None
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.proc.poll() is not None:
                return None
            try:
                line = self.lines.get(timeout=max(0.01, deadline - time.monotonic()))
            except queue.Empty:
                continue
            if line is None:
                return None
            if line == sentinel or line.startswith(sentinel + " "):
                return line
        return None

    def prepare_game(self) -> bool:
        if self.exchange("isready", "readyok", 8.0) is None:
            return False
        if not self.send("ucinewgame"):
            return False
        if not self.send(f"setoption name EvalStage value {self.stage}"):
            return False
        return self.exchange("isready", "readyok", 8.0) is not None

    def bestmove(self, board: chess.Board) -> tuple[str | None, str]:
        command = "position startpos"
        if board.move_stack:
            command += " moves " + " ".join(move.uci() for move in board.move_stack)
        if not self.send(command) or not self.send(TC_COMMAND):
            return None, "ENGINE-DIED"
        deadline = time.monotonic() + MOVE_TIMEOUT
        while time.monotonic() < deadline:
            if self.proc.poll() is not None:
                return None, "ENGINE-DIED"
            try:
                line = self.lines.get(timeout=max(0.01, deadline - time.monotonic()))
            except queue.Empty:
                continue
            if line is None:
                return None, "ENGINE-DIED"
            if line.startswith("bestmove "):
                parts = line.split()
                return (parts[1] if len(parts) > 1 else ""), "ok"
        return None, "TIMEOUT"

    def close(self) -> None:
        self.send("quit")
        try:
            self.proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait(timeout=2)


def play_game(engines: tuple[Engine, Engine], game_id: int, binary: str, commit: str) -> dict[str, Any]:
    eng_a, eng_b = engines
    if not eng_a.prepare_game() or not eng_b.prepare_game():
        raise RuntimeError("engine readiness failed before game start")
    opening = derive_opening(game_id)
    board = validate_san(opening, [])
    a_white = game_id % 2 == 0
    mover = eng_a if (board.turn == chess.WHITE) == a_white else eng_b
    mover_name = "A" if mover is eng_a else "B"
    san: list[str] = []
    started = utc_now()
    clock = time.monotonic()
    incident = ""
    while not board.is_game_over() and len(opening) + len(san) < MAX_PLIES:
        token, status = mover.bestmove(board)
        if status != "ok":
            incident = f"{mover_name}:{status}"
            break
        if token in {"", "0000", "(none)"}:
            incident = f"{mover_name}:NULL_BESTMOVE"
            break
        try:
            move = chess.Move.from_uci(token)
            if move not in board.legal_moves:
                raise ValueError("not in legal_moves")
            san.append(board.san(move))
            board.push(move)
        except Exception as exc:
            incident = f"{mover_name}:ILLEGAL_BESTMOVE:{token}:{exc}"
            break
        mover = eng_b if mover is eng_a else eng_a
        mover_name = "B" if mover_name == "A" else "A"
    final_board = validate_san(opening, san)  # legal-move-flush precondition
    plies = len(opening) + len(san)
    if incident:
        res = "B" if incident.startswith("A:") else "A"
        end = "crash"
    else:
        outcome = final_board.result()
        res = ("A" if a_white else "B") if outcome == "1-0" else (
            ("B" if a_white else "A") if outcome == "0-1" else "D"
        )
        end = classify_end(final_board, plies)
    return {
        "game_id": game_id, "campaign_salt": SALT,
        "seed_int": SALT * 1_000_003 + game_id,
        "opening": opening, "a_white": a_white, "b_white": not a_white,
        "eval_stage_a": STAGE, "eval_stage_b": STAGE,
        "binary_sha256": binary, "src_commit": commit, "tc": TC,
        "tc_command": TC_COMMAND, "time_started": started,
        "time_finished": utc_now(), "res": res, "end": end,
        "end_seconds": int(time.monotonic() - clock), "plies": plies, "san": san,
        "crash_incident": bool(incident), "crash_incident_text": incident,
    }


class Audit:
    def __init__(self, path: Path):
        self.path = path
        self.lock = threading.Lock()

    def write(self, event: str, **fields: Any) -> None:
        row = {"timestamp": utc_now(), "event": event, **fields}
        with self.lock:
            append_fsync(self.path, row)


def load_checkpoint(path: Path, games: int, audit: Audit) -> tuple[dict[int, dict[str, Any]], int | None]:
    present: dict[int, dict[str, Any]] = {}
    keys: set[tuple[str, ...]] = set()
    if not path.exists() or not path.read_bytes():
        return present, None
    data = path.read_bytes()
    lines = data.splitlines(keepends=True)
    for index, raw in enumerate(lines):
        final = index == len(lines) - 1
        try:
            row = json.loads(raw.decode("utf-8"))
            missing = MANDATORY_FIELDS - set(row)
            if missing:
                raise ValueError(f"missing fields {sorted(missing)}")
            game_id = row["game_id"]
            if type(game_id) is not int or not 0 <= game_id < games:
                raise ValueError(f"bad game_id {game_id!r}")
            if game_id in present:
                raise ValueError(f"duplicate game_id {game_id}")
            key = tuple(row["opening"]) + tuple(row["san"])
            if key in keys:
                raise ValueError(f"duplicate move-list {game_id}")
            if final and not raw.endswith(b"\n"):
                raise ValueError("torn trailing line")
        except Exception as exc:
            if not final:
                raise RuntimeError(f"corrupt non-final line {index + 1}: {exc}") from exc
            offset = len(data) - len(raw)
            sidecar = Path(str(path) + ".torn")
            with sidecar.open("ab") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            temp = Path(str(path) + ".repairing")
            with temp.open("wb") as stream:
                stream.write(data[:offset])
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp, path)
            match = re.search(rb'"game_id"\s*:\s*(\d+)', raw)
            recoverable = int(match.group(1)) if match else None
            audit.write("torn_line_quarantined", recoverable_game_id=recoverable,
                        byte_offset=offset, torn_bytes=len(raw), sidecar=str(sidecar))
            print(f"INCIDENT torn_line_quarantined recoverable_game_id={recoverable} "
                  f"byte_offset={offset} sidecar={sidecar}", flush=True)
            return present, recoverable
        present[row["game_id"]] = row
        keys.add(key)
    return present, None


def synthetic_record(game_id: int, binary: str, commit: str) -> dict[str, Any]:
    opening = derive_opening(game_id)
    board = validate_san(opening, [])
    san: list[str] = []
    rng = random.Random((SALT * 1_000_003 + game_id) ^ 0x5A15A15A)
    while not board.is_game_over() and len(opening) + len(san) < MAX_PLIES:
        move = rng.choice(list(board.legal_moves))
        san.append(board.san(move))
        board.push(move)
    outcome = board.result()
    a_white = game_id % 2 == 0
    res = ("A" if a_white else "B") if outcome == "1-0" else (
        ("B" if a_white else "A") if outcome == "0-1" else "D"
    )
    stamp = "2026-09-24T00:00:00Z"
    return {
        "game_id": game_id, "campaign_salt": SALT,
        "seed_int": SALT * 1_000_003 + game_id,
        "opening": opening, "a_white": a_white, "b_white": not a_white,
        "eval_stage_a": STAGE, "eval_stage_b": STAGE,
        "binary_sha256": binary, "src_commit": commit, "tc": TC,
        "tc_command": TC_COMMAND, "time_started": stamp, "time_finished": stamp,
        "res": res, "end": classify_end(board, len(opening) + len(san)),
        "end_seconds": 0, "plies": len(opening) + len(san), "san": san,
        "crash_incident": False, "crash_incident_text": "",
    }


def run_campaign(args: argparse.Namespace) -> int:
    exe = Path(args.exe).resolve()
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    audit = Audit(Path(str(out) + ".events.jsonl"))
    binary = sha256_file(exe)
    commit = git_commit()
    if binary != args.expected_binary_sha256 or commit != args.expected_src_commit:
        raise RuntimeError(f"provenance pin mismatch binary={binary} commit={commit}")
    present, torn_id = load_checkpoint(out, args.games, audit)
    first_missing = next((i for i in range(args.games) if i not in present), args.games)
    audit.write("generator_start", mode="live", pid=os.getpid(), games=args.games,
                salt=SALT, pairs=args.pairs, binary_sha256=binary, src_commit=commit,
                tc=TC, tc_command=TC_COMMAND, valid_before=len(present),
                first_missing=first_missing, torn_recoverable_game_id=torn_id)
    print(f"START games={args.games} pairs={args.pairs} valid_before={len(present)} "
          f"first_missing={first_missing} binary={binary} src={commit}", flush=True)
    if first_missing == args.games:
        audit.write("generator_complete", valid_after=len(present), games_added=0)
        print(f"COMPLETE games={len(present)} added=0", flush=True)
        return 0
    missing = [game_id for game_id in range(args.games) if game_id not in present]
    write_lock = threading.Lock()
    errors: list[BaseException] = []
    emitted = set(present)

    def worker(pair_index: int) -> None:
        engines: tuple[Engine, Engine] | None = None
        try:
            engines = (Engine(exe, STAGE), Engine(exe, STAGE))
            for game_id in missing[pair_index::args.pairs]:
                if errors:
                    return
                row = play_game(engines, game_id, binary, commit)
                append_fsync(out, row, write_lock)
                with write_lock:
                    if game_id in emitted:
                        raise RuntimeError(f"concurrent duplicate id {game_id}")
                    emitted.add(game_id)
                    count = len(emitted)
                audit.write("game_flushed", game_id=game_id, valid_after=count,
                            end=row["end"], res=row["res"], crash_incident=row["crash_incident"])
                print(f"FLUSHED game_id={game_id} valid={count} end={row['end']} "
                      f"res={row['res']}", flush=True)
        except BaseException as exc:
            errors.append(exc)
        finally:
            if engines:
                for engine in engines:
                    engine.close()

    threads = [threading.Thread(target=worker, args=(index,), name=f"pair-{index}")
               for index in range(args.pairs)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    if errors:
        audit.write("generator_failed", error=repr(errors[0]), valid_after=len(emitted))
        raise errors[0]
    audit.write("generator_complete", valid_after=len(emitted),
                games_added=len(emitted) - len(present))
    print(f"COMPLETE games={len(emitted)} added={len(emitted) - len(present)}", flush=True)
    return 0


def run_drill(args: argparse.Namespace) -> int:
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    for stale in (out, Path(str(out) + ".torn"), Path(str(out) + ".events.jsonl")):
        stale.unlink(missing_ok=True)
    binary = sha256_file(Path(args.exe).resolve())
    commit = git_commit()
    audit = Audit(Path(str(out) + ".events.jsonl"))
    for game_id in range(args.games):
        append_fsync(out, synthetic_record(game_id, binary, commit))
    data = out.read_bytes()
    lines = data.splitlines(keepends=True)
    kill_game = args.games // 2
    if not 400 <= kill_game <= 600:
        raise ValueError("kill game outside [400,600]")
    start = sum(len(line) for line in lines[:kill_game])
    target = lines[kill_game]
    cut = start + len(target) // 2
    out.write_bytes(data[:cut])
    audit.write("drill_truncated", kill_game=kill_game, byte_offset=cut,
                pre_truncation_valid=kill_game)
    print(f"DRILL KILLED game_id={kill_game} byte_offset={cut} "
          f"pre_truncation_valid={kill_game}", flush=True)
    present, torn_id = load_checkpoint(out, args.games, audit)
    if torn_id != kill_game:
        raise AssertionError(f"recoverable id {torn_id} != {kill_game}")
    for game_id in range(args.games):
        if game_id not in present:
            append_fsync(out, synthetic_record(game_id, binary, commit))
    final, _ = load_checkpoint(out, args.games, audit)
    if sorted(final) != list(range(args.games)):
        raise AssertionError("presence test failed: parse + full schema + dense 0-based id")
    keys = [tuple(row["opening"]) + tuple(row["san"]) for row in final.values()]
    duplicates = len(keys) - len(set(keys))
    if duplicates:
        raise AssertionError(f"duplicate move-lists={duplicates}")
    sidecar = Path(str(out) + ".torn")
    if not sidecar.exists() or not sidecar.read_bytes().endswith(target[:len(target) // 2]):
        raise AssertionError("torn bytes not preserved verbatim")
    evidence = {
        "drill": "PASS", "games": args.games, "kill_window": [400, 600],
        "kill_game": kill_game, "pre_truncation_valid": kill_game,
        "resumed_games": args.games - kill_game, "final_valid": len(final),
        "duplicate_move_lists": duplicates,
        "presence": "parse + full schema + dense 0-based id",
        "torn_recoverable_game_id": torn_id, "torn_sidecar": str(sidecar),
    }
    audit.write("drill_complete", **evidence)
    print(json.dumps(evidence, sort_keys=True), flush=True)
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exe", default=str(DEFAULT_EXE))
    parser.add_argument("--out", required=True)
    parser.add_argument("--games", type=int, default=1000)
    parser.add_argument("--salt", type=int, default=SALT)
    parser.add_argument("--pairs", type=int, default=2)
    parser.add_argument("--expected-binary-sha256", required=True)
    parser.add_argument("--expected-src-commit", required=True)
    parser.add_argument("--drill", action="store_true")
    args = parser.parse_args(argv)
    if args.salt != SALT:
        parser.error(f"--salt is frozen at {SALT}")
    if not 1 <= args.games <= 2000:
        parser.error("--games must be in [1,2000]")
    if not 1 <= args.pairs <= 2:
        parser.error("--pairs must be 1 or 2")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return run_drill(args) if args.drill else run_campaign(args)


if __name__ == "__main__":
    raise SystemExit(main())

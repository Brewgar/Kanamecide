#!/usr/bin/env python3
"""E-0012 E-SPRT-lite: shared live/replay core with durable resume."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import queue
import random
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import chess

from e0011_generate import Engine, classify_end, derive_opening, validate_san

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EXE = ROOT / "build" / "Release" / "kana.exe"
BOUND = math.log(0.95 / 0.05)
TIERS = {
    "S": {"lo": 0.0, "hi": 20.0, "cap": 8000},
    "R": {"lo": 0.0, "hi": 5.0, "cap": 30000},
    "M": {"lo": 100.0, "hi": 150.0, "cap": 8000},
}
EPS = 1e-9
SCORE = {"A": 1.0, "D": 0.5, "B": 0.0}
N_OPEN = 10
MAX_PLIES = 300
TC = "100ms+100ms inc"
TC_COMMAND = "go wtime 1500 btime 1500 winc 100 binc 100"
WHITE_NULL_SCORE = 0.585


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


def elo_q(delta: float) -> float:
    return 1.0 / (1.0 + 10.0 ** (-delta / 400.0))


def llr_step(score: float, lo: float, hi: float) -> float:
    q0, q1 = elo_q(lo), elo_q(hi)
    return score * math.log(q1 / q0) + (1.0 - score) * math.log((1.0 - q1) / (1.0 - q0))


def verdict(llr: float) -> str | None:
    # The preregistered epsilon tie convention: a touched bound decides toward it.
    if llr >= BOUND - EPS:
        return "H1"
    if llr <= -BOUND + EPS:
        return "H0"
    return None


def replay(scores: Iterable[float], lo: float, hi: float, cap: int) -> dict[str, Any]:
    total = 0.0
    counts = {"wins": 0, "draws": 0, "losses": 0}
    crossing = None
    epsilon_boundary = None
    for n, score in enumerate(scores, 1):
        if score == 1.0:
            counts["wins"] += 1
        elif score == 0.5:
            counts["draws"] += 1
        else:
            counts["losses"] += 1
        total += llr_step(score, lo, hi)
        if abs(abs(total) - BOUND) <= EPS and epsilon_boundary is None:
            epsilon_boundary = {"game": n, "llr": total, "touched": "H1" if total > 0 else "H0"}
        decision = verdict(total)
        if decision is not None:
            crossing = {"verdict": decision, "game": n, "llr": total}
            break
        if n >= cap:
            break
    final_verdict = crossing["verdict"] if crossing else "INCONCLUSIVE"
    return {
        "n": sum(counts.values()), **counts, "llr": total,
        "verdict": final_verdict, "crossing": crossing,
        "bound_within_epsilon": epsilon_boundary,
    }


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = Path(str(path) + ".tmp")
    with temp.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, sort_keys=True, separators=(",", ":"))
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def append_jsonl_fsync(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("ab") as stream:
        stream.write((json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8"))
        stream.flush()
        os.fsync(stream.fileno())


def append_incident(path: Path, event: str, **fields: Any) -> None:
    append_jsonl_fsync(path, {"timestamp": utc_now(), "event": event, **fields})


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for number, raw in enumerate(path.read_bytes().splitlines(keepends=True), 1):
        if not raw.endswith(b"\n"):
            raise RuntimeError(f"torn authoritative JSONL line {number}")
        value = json.loads(raw.decode("utf-8"))
        if not isinstance(value, dict):
            raise RuntimeError(f"authoritative JSONL line {number} is not an object")
        rows.append(value)
    return rows


def config_for(tier: str, magnitude: float, cap: int | None, salt: int) -> dict[str, Any]:
    if tier not in TIERS:
        raise ValueError(f"unknown tier {tier}")
    spec = TIERS[tier]
    lo = magnitude - 50.0 if tier == "M" else spec["lo"]
    hi = magnitude if tier == "M" else spec["hi"]
    selected_cap = cap if cap is not None else spec["cap"]
    if selected_cap <= 0:
        raise ValueError("cap must be positive")
    return {"tier": tier, "lo": lo, "hi": hi, "bound": BOUND,
            "cap": selected_cap, "salt": salt}


def state_from_rows(rows: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    scores = []
    for row in rows:
        result = row.get("result", row.get("res"))
        if result not in SCORE:
            raise ValueError(f"invalid result {result!r}")
        scores.append(SCORE[result])
    computed = replay(scores, config["lo"], config["hi"], config["cap"])
    return {
        "n": computed["n"], "wins": computed["wins"], "draws": computed["draws"],
        "losses": computed["losses"], "llr": computed["llr"],
        "verdict": computed["verdict"], "crossing": computed["crossing"],
        "next_game_index": computed["n"],
    }


def load_checkpoint(path: Path) -> dict[str, Any] | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def verify_resume(rows: list[dict[str, Any]], checkpoint_path: Path,
                  config: dict[str, Any], incident_path: Path) -> dict[str, Any]:
    computed = state_from_rows(rows, config)
    checkpoint = load_checkpoint(checkpoint_path)
    if checkpoint is None:
        return computed
    differences = []
    for key in ("n", "wins", "draws", "losses", "next_game_index"):
        if computed[key] != checkpoint.get(key):
            differences.append({"field": key, "jsonl": computed[key], "checkpoint": checkpoint.get(key)})
    checkpoint_llr = float(checkpoint.get("llr", math.nan))
    if computed["llr"] != checkpoint_llr:
        differences.append({"field": "llr", "jsonl": computed["llr"], "checkpoint": checkpoint_llr})
    for key in ("tier", "lo", "hi", "bound", "cap", "salt"):
        if config[key] != checkpoint.get("config", {}).get(key):
            differences.append({"field": f"config.{key}", "jsonl": config[key],
                                "checkpoint": checkpoint.get("config", {}).get(key)})
    if differences:
        append_incident(incident_path, "resume_mismatch", differences=differences)
    non_llr = any(item["field"] != "llr" for item in differences)
    llr_too_large = any(item["field"] == "llr" and
                        abs(item["jsonl"] - item["checkpoint"]) > EPS
                        for item in differences)
    if non_llr or llr_too_large:
        raise RuntimeError("resume_mismatch: JSONL/checkpoint mismatch; ABORT")
    return computed


def durable_result(jsonl: Path, checkpoint: Path, incident: Path,
                   row: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    """Mandatory order: JSONL append -> fsync -> checkpoint write -> fsync."""
    append_jsonl_fsync(jsonl, row)
    rows = read_jsonl(jsonl)
    state = state_from_rows(rows, config)
    boundary = replay([SCORE[item.get("result", item.get("res"))] for item in rows],
                      config["lo"], config["hi"], config["cap"])["bound_within_epsilon"]
    if boundary is not None:
        append_incident(incident, "bound_within_epsilon", **boundary)
    atomic_json(checkpoint, {"config": config, **state, "updated_at": utc_now()})
    return state


def live_game(engines: tuple[Engine, Engine], game_id: int, salt: int,
              stage_a: int, stage_b: int, binary: str, commit: str) -> dict[str, Any]:
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
        try:
            move = chess.Move.from_uci(token)
            if token in {"", "0000", "(none)"} or move not in board.legal_moves:
                raise ValueError("illegal or null bestmove")
            san.append(board.san(move))
            board.push(move)
        except Exception as exc:
            incident = f"{mover_name}:ILLEGAL_BESTMOVE:{token}:{exc}"
            break
        mover = eng_b if mover is eng_a else eng_a
        mover_name = "B" if mover_name == "A" else "A"
    final_board = validate_san(opening, san)
    plies = len(opening) + len(san)
    if incident:
        result = "B" if incident.startswith("A:") else "A"
        end = "crash"
    else:
        outcome = final_board.result()
        result = ("A" if a_white else "B") if outcome == "1-0" else (
            ("B" if a_white else "A") if outcome == "0-1" else "D"
        )
        end = classify_end(final_board, plies)
    return {
        "game_id": game_id, "campaign_salt": salt,
        "seed_int": salt * 1_000_003 + game_id, "opening": opening,
        "a_white": a_white, "eval_stage_a": stage_a, "eval_stage_b": stage_b,
        "binary_sha256": binary, "src_commit": commit, "tc": TC,
        "tc_command": TC_COMMAND, "time_started": started, "time_finished": utc_now(),
        "result": result, "end": end, "end_seconds": int(time.monotonic() - clock),
        "plies": plies, "san": san, "crash_incident": bool(incident),
        "crash_incident_text": incident,
    }


def run_live(args: argparse.Namespace) -> int:
    config = config_for(args.tier, args.magnitude, args.cap, args.salt)
    binary = sha256_file(Path(args.exe).resolve())
    commit = git_commit()
    jsonl = Path(args.out).resolve()
    checkpoint = Path(args.checkpoint).resolve()
    incident = Path(args.incidents).resolve()
    rows = read_jsonl(jsonl)
    state = verify_resume(rows, checkpoint, config, incident)
    if state["verdict"] != "INCONCLUSIVE":
        print(json.dumps({"config": config, **state}, sort_keys=True))
        return 0
    if args.null_pair and args.stage_a != args.stage_b:
        raise ValueError("null-pair requires identical stages")
    if not args.null_pair and args.stage_a == args.stage_b:
        raise ValueError("known-difference validation requires distinct stages")
    engines = (Engine(Path(args.exe).resolve(), args.stage_a),
               Engine(Path(args.exe).resolve(), args.stage_b))
    try:
        while state["verdict"] == "INCONCLUSIVE" and state["n"] < config["cap"]:
            game_id = state["next_game_index"]
            row = live_game(engines, game_id, args.salt, args.stage_a, args.stage_b, binary, commit)
            state = durable_result(jsonl, checkpoint, incident, row, config)
            print(f"FLUSHED n={state['n']} result={row['result']} llr={state['llr']:.12f} "
                  f"verdict={state['verdict']}", flush=True)
    finally:
        for engine in engines:
            engine.close()
    summary = {"config": config, **state}
    if args.null_pair:
        white_points = 0.0
        for row in read_jsonl(jsonl):
            white_points += 1.0 if row["result"] == ("A" if row["a_white"] else "B") else (
                0.5 if row["result"] == "D" else 0.0)
        observed_white = white_points / max(1, state["n"])
        summary["null_control"] = {
            "white_prior": WHITE_NULL_SCORE, "observed_white_score": observed_white,
            "band_centred_at_50pct": False,
            "pass": state["verdict"] != "H1",
        }
    print(json.dumps(summary, sort_keys=True))
    return 0


def load_retained_scores(path: Path) -> list[float]:
    rows = read_jsonl(path)
    scores = []
    for row in rows:
        result = row.get("res", row.get("result"))
        if result not in SCORE:
            raise ValueError(f"invalid retained result {result!r}")
        scores.append(SCORE[result])
    return scores


def run_replay(path: Path) -> int:
    scores = load_retained_scores(path)
    outputs = {}
    for tier, magnitude in (("S", 150.0), ("R", 150.0), ("M", 150.0)):
        outputs[tier] = replay(scores, TIERS[tier]["lo"] if tier != "M" else magnitude - 50,
                               TIERS[tier]["hi"] if tier != "M" else magnitude,
                               TIERS[tier]["cap"])
    print(f"REPLAY input={path} sha256={sha256_file(path)} n={len(scores)}")
    print("REPLAY S " + json.dumps(outputs["S"], sort_keys=True))
    print("REPLAY R " + json.dumps(outputs["R"], sort_keys=True))
    print("REPLAY M " + json.dumps(outputs["M"], sort_keys=True))
    s = outputs["S"]
    passed = s["verdict"] == "H1" and s["crossing"]["game"] == 179 and abs(s["crossing"]["llr"] - 2.985) < 0.0006
    print(f"REPLAY_SANITY {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


def neutral_canned_scores(n: int) -> list[float]:
    """Deterministic no-boundary W/D/L fixture for every-k resume testing."""
    scores: list[float] = []
    total = 0.0
    for _ in range(n):
        candidates = []
        for score in (1.0, 0.5, 0.0):
            candidate = total + llr_step(score, 0.0, 20.0)
            candidates.append((abs(candidate), score, candidate))
        _, score, total = min(candidates, key=lambda item: (item[0], item[1]))
        if abs(total) >= BOUND - EPS:
            raise AssertionError("neutral fixture touched a bound")
        scores.append(score)
    return scores


def seed_durable_prefix(rows: list[dict[str, Any]], config: dict[str, Any],
                        jsonl: Path, checkpoint: Path) -> None:
    data = b"".join((json.dumps(row, sort_keys=True) + "\n").encode("utf-8") for row in rows)
    jsonl.parent.mkdir(parents=True, exist_ok=True)
    with jsonl.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    state = state_from_rows(rows, config)
    atomic_json(checkpoint, {"config": config, **state, "updated_at": utc_now()})


def self_test() -> int:
    root = Path(tempfile.mkdtemp(prefix="e0012-split-"))
    config = config_for("S", 150.0, 240, 20260924)
    scores = neutral_canned_scores(240)
    baseline = replay(scores, config["lo"], config["hi"], config["cap"])
    rows = [{"game_id": index, "result": {1.0: "A", 0.5: "D", 0.0: "B"}[score]}
            for index, score in enumerate(scores)]
    for split in range(1, len(scores)):
        case = root / f"split-{split:03d}"
        jsonl = case / "games.jsonl"
        checkpoint = case / "checkpoint.json"
        incident = case / "incidents.jsonl"
        seed_durable_prefix(rows[:split], config, jsonl, checkpoint)
        resumed = verify_resume(read_jsonl(jsonl), checkpoint, config, incident)
        continued = state_from_rows(rows, config)
        if (resumed["verdict"], continued["verdict"], continued["crossing"]) != (
            baseline["verdict"], baseline["verdict"], baseline["crossing"]
        ):
            raise AssertionError(f"split {split}: verdict/crossing mismatch")
        if incident.exists():
            raise AssertionError(f"split {split}: unexpected incident")
    monotone = all(replay([1.0] * n, 0, 20, 100)["llr"] <=
                   replay([1.0] * (n + 1), 0, 20, 100)["llr"] for n in range(100))
    capped = replay([0.5] * 20, 0, 20, 5)
    epsilon = verdict(BOUND - EPS / 2)
    mismatch_aborted = False
    bad_case = root / "mismatch"
    bad_case.mkdir()
    append_jsonl_fsync(bad_case / "games.jsonl", rows[0])
    atomic_json(bad_case / "checkpoint.json", {**state_from_rows([], config), "config": config})
    try:
        verify_resume(read_jsonl(bad_case / "games.jsonl"),
                      bad_case / "checkpoint.json", config, bad_case / "incidents.jsonl")
    except RuntimeError:
        mismatch_aborted = True
    passed = monotone and capped["n"] == 5 and capped["verdict"] == "INCONCLUSIVE" and epsilon == "H1" and mismatch_aborted
    print(f"SELF_TEST split_points={len(scores) - 1} sequence_n={len(scores)} "
          f"baseline_verdict={baseline['verdict']} crossing={baseline['crossing']} "
          f"monotone={monotone} cap={capped['n']}/{capped['verdict']} "
          f"epsilon_tie={epsilon} resume_mismatch_abort={mismatch_aborted}")
    print(f"SELF_TEST {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--replay", type=Path)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--live", action="store_true")
    parser.add_argument("--exe", default=str(DEFAULT_EXE))
    parser.add_argument("--tier", choices=sorted(TIERS), default="S")
    parser.add_argument("--magnitude", type=float, default=150.0)
    parser.add_argument("--cap", type=int)
    parser.add_argument("--salt", type=int, default=20260924)
    parser.add_argument("--stage-a", type=int, default=6)
    parser.add_argument("--stage-b", type=int, default=0)
    parser.add_argument("--null-pair", action="store_true")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--incidents", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.self_test:
        return self_test()
    if args.replay:
        return run_replay(args.replay)
    if not args.out or not args.checkpoint or not args.incidents:
        raise SystemExit("--live requires --out, --checkpoint, and --incidents")
    return run_live(args)


if __name__ == "__main__":
    raise SystemExit(main())

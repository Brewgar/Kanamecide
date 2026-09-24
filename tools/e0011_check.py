#!/usr/bin/env python3
"""E-0011 machine checker for preregistered gates (a)-(f)."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import chess

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EXE = ROOT / "build" / "Release" / "kana.exe"
DEFAULT_RECORD = ROOT / "research" / "experiments" / "E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md"
SALT = 20260922
STAGE = 6
TC = "100ms+100ms inc"
TC_COMMAND = "go wtime 1500 btime 1500 winc 100 binc 100"
END_VOCABULARY = {
    "mate", "stalemate", "draw-material", "rule50", "repetition", "plycap", "crash"
}
MANDATORY_FIELDS = {
    "game_id", "campaign_salt", "seed_int", "opening", "a_white", "b_white",
    "eval_stage_a", "eval_stage_b", "binary_sha256", "src_commit", "tc", "tc_command",
    "time_started", "time_finished", "res", "end", "end_seconds", "plies", "san",
    "crash_incident", "crash_incident_text",
}
RESULT_SCORE = {"A": 1.0, "D": 0.5, "B": 0.0}


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
    for _ in range(10):
        choices = list(board.legal_moves)
        rng.shuffle(choices)
        selected = None
        for candidate in choices:
            probe = board.copy(stack=False)
            probe.push(candidate)
            if not probe.is_game_over():
                board.push(candidate)
                selected = candidate
                break
        if selected is None:
            raise RuntimeError(f"no live tenth-ply continuation at {game_id}")
        opening.append(selected.uci())
    return opening


def base_record(game_id: int, binary: str, commit: str) -> dict[str, Any]:
    opening = derive_opening(game_id)
    board = chess.Board()
    for uci in opening:
        board.push_uci(uci)
    san: list[str] = []
    rng = random.Random((SALT * 1_000_003 + game_id) ^ 0xD15EA5E)
    for _ in range(12):
        if board.is_game_over():
            break
        move = rng.choice(list(board.legal_moves))
        san.append(board.san(move))
        board.push(move)
    outcome = board.result()
    a_white = game_id % 2 == 0
    res = ("A" if a_white else "B") if outcome == "1-0" else (
        ("B" if a_white else "A") if outcome == "0-1" else "D"
    )
    if board.is_checkmate():
        end = "mate"
    elif board.is_stalemate():
        end = "stalemate"
    elif board.can_claim_fifty_moves():
        end = "rule50"
    elif board.is_repetition(3):
        end = "repetition"
    elif board.is_insufficient_material():
        end = "draw-material"
    else:
        end = "plycap"
    stamp = "2026-09-24T00:00:00Z"
    return {
        "game_id": game_id, "campaign_salt": SALT,
        "seed_int": SALT * 1_000_003 + game_id,
        "opening": opening, "a_white": a_white, "b_white": not a_white,
        "eval_stage_a": STAGE, "eval_stage_b": STAGE,
        "binary_sha256": binary, "src_commit": commit, "tc": TC,
        "tc_command": TC_COMMAND, "time_started": stamp, "time_finished": stamp,
        "res": res, "end": end, "end_seconds": 0,
        "plies": len(opening) + len(san), "san": san,
        "crash_incident": False, "crash_incident_text": "",
    }


@dataclass
class Results:
    rows: list[tuple[str, str, bool, str]] = field(default_factory=list)

    def add(self, gate: str, name: str, passed: bool, detail: str) -> None:
        self.rows.append((gate, name, passed, detail))

    def dump(self) -> None:
        for gate, name, passed, detail in self.rows:
            print(f"{gate} {name} {'PASS' if passed else 'FAIL'} {detail}")


def parse_jsonl(path: Path, results: Results) -> tuple[list[dict[str, Any]], int]:
    data = path.read_bytes()
    if not data:
        return [], 0
    records: list[dict[str, Any]] = []
    torn = 0
    lines = data.splitlines(keepends=True)
    for index, raw in enumerate(lines):
        final = index == len(lines) - 1
        try:
            if final and not raw.endswith(b"\n"):
                raise ValueError("trailing line has no newline")
            value = json.loads(raw.decode("utf-8"))
            if not isinstance(value, dict):
                raise ValueError("JSON value is not an object")
            records.append(value)
        except Exception as exc:
            if final:
                torn += 1
                results.add("GATE-B", "b.jsonl_parse", False,
                            f"line={index + 1} torn={exc}")
            else:
                results.add("GATE-B", "b.jsonl_parse", False,
                            f"line={index + 1} corrupt={exc}")
    return records, torn


def legal_record(row: dict[str, Any]) -> tuple[chess.Board | None, str | None]:
    try:
        board = chess.Board()
        for uci in row["opening"]:
            move = chess.Move.from_uci(uci)
            if move not in board.legal_moves:
                return None, f"illegal opening {uci}"
            board.push(move)
        for san in row["san"]:
            try:
                board.push_san(san)
            except Exception as exc:
                return None, f"illegal SAN {san!r}: {exc}"
        return board, None
    except Exception as exc:
        return None, str(exc)


def iso_value(value: Any) -> float | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def expected_result(board: chess.Board, a_white: bool) -> str:
    outcome = board.result()
    if outcome == "1-0":
        return "A" if a_white else "B"
    if outcome == "0-1":
        return "B" if a_white else "A"
    return "D"


def expected_end(board: chess.Board, plies: int) -> str | None:
    if board.is_checkmate():
        return "mate"
    if board.is_stalemate():
        return "stalemate"
    if board.can_claim_fifty_moves():
        return "rule50"
    if board.is_repetition(3):
        return "repetition"
    if board.is_insufficient_material():
        return "draw-material"
    if plies >= 300:
        return "plycap"
    return None


def check_provenance(rows: list[dict[str, Any]], binary: str, commit: str, results: Results) -> None:
    missing_any = False
    value_errors: list[str] = []
    named_errors: Counter[str] = Counter()
    id_counts: Counter[int] = Counter()
    move_counts: Counter[tuple[str, ...]] = Counter()
    boards: list[tuple[int, chess.Board]] = []
    tc_values: set[str] = set()
    for number, row in enumerate(rows, 1):
        missing = MANDATORY_FIELDS - set(row)
        if missing:
            missing_any = True
            value_errors.append(f"line={number} missing={sorted(missing)}")
            continue
        try:
            game_id = row["game_id"]
            if type(game_id) is not int:
                raise ValueError("game_id is not int")
            id_counts[game_id] += 1
            checks = {
                "campaign_salt": row["campaign_salt"] == SALT,
                "seed_int": row["seed_int"] == SALT * 1_000_003 + game_id,
                "opening": row["opening"] == derive_opening(game_id),
                "a_white_bool": type(row["a_white"]) is bool,
                "a_white_parity": row["a_white"] == (game_id % 2 == 0),
                "b_white": row["b_white"] is (not row["a_white"]),
                "stage_a": row["eval_stage_a"] == STAGE,
                "stage_b": row["eval_stage_b"] == STAGE,
                "binary_sha256": row["binary_sha256"] == binary,
                "src_commit": row["src_commit"] == commit,
                "tc": row["tc"] == TC,
                "tc_command": row["tc_command"] == TC_COMMAND,
                "res": row["res"] in {"A", "B", "D"},
                "end": row["end"] in END_VOCABULARY,
                "end_seconds": type(row["end_seconds"]) is int and row["end_seconds"] >= 0,
                "plies": type(row["plies"]) is int and row["plies"] > 0,
                "san": isinstance(row["san"], list) and all(isinstance(x, str) for x in row["san"]),
                "plies_count": row["plies"] == len(row["opening"]) + len(row["san"]),
                "crash_bool": type(row["crash_incident"]) is bool,
                "crash_text": isinstance(row["crash_incident_text"], str),
            }
            started, finished = iso_value(row["time_started"]), iso_value(row["time_finished"])
            checks["timestamps"] = started is not None and finished is not None and finished >= started
            if row["end"] == "crash":
                checks["crash_pair"] = row["crash_incident"] and bool(row["crash_incident_text"])
                offender = str(row["crash_incident_text"]).split(":", 1)[0]
                checks["crash_loss"] = offender in {"A", "B"} and row["res"] == ("B" if offender == "A" else "A")
            else:
                checks["crash_pair"] = not row["crash_incident"] and not row["crash_incident_text"]
            if row["binary_sha256"] != binary:
                named_errors["binary_sha256_campaign_pin"] += 1
            if row["src_commit"] != commit:
                named_errors["src_commit_launch_pin"] += 1
            if row["campaign_salt"] != SALT:
                named_errors["campaign_salt"] += 1
            if row["seed_int"] != SALT * 1_000_003 + game_id:
                named_errors["seed_int"] += 1
            if row["opening"] != derive_opening(game_id):
                named_errors["seed_opening_rederivation"] += 1
            if row["eval_stage_a"] != STAGE or row["eval_stage_b"] != STAGE:
                named_errors["eval_stage_pair"] += 1
            if row["a_white"] is not (game_id % 2 == 0) or row["b_white"] is not (not row["a_white"]):
                named_errors["color_parity"] += 1
            if row["end"] not in END_VOCABULARY:
                named_errors["end_suffix_free_closed_vocabulary"] += 1
            if type(row["end_seconds"]) is not int or row["end_seconds"] < 0:
                named_errors["end_seconds"] += 1
            if type(row["plies"]) is not int or row["plies"] <= 0:
                named_errors["plies"] += 1
            if started is None or finished is None or finished < started:
                named_errors["timestamp_order"] += 1
            failed = [name for name, passed in checks.items() if not passed]
            if failed:
                value_errors.append(f"line={number} game_id={game_id} failed={failed}")
            move_counts[tuple(row["opening"]) + tuple(row["san"])] += 1
            tc_values.add(row["tc_command"])
        except Exception as exc:
            value_errors.append(f"line={number} exception={exc}")
    expected_ids = set(range(len(rows)))
    actual_ids = set(id_counts)
    dense = actual_ids == expected_ids and all(count == 1 for count in id_counts.values())
    results.add("GATE-D", "d.named_value_conjuncts", not named_errors,
                f"failures={dict(named_errors)}")
    results.add("GATE-D", "d.mandatory_fields", not missing_any and not value_errors,
                f"coverage={len(rows) - sum('missing=' in x for x in value_errors)}/{len(rows)}"
                + (f" errors={value_errors[:8]}" if value_errors else ""))
    results.add("GATE-D", "d.game_id_dense_0_based_unique", dense,
                f"unique={len(id_counts)} rows={len(rows)} expected={len(expected_ids)}")
    results.add("GATE-D", "d.tc_single_value", tc_values == {TC_COMMAND}, f"values={sorted(tc_values)}")


def check_legality(rows: list[dict[str, Any]], results: Results) -> list[tuple[int, chess.Board]]:
    boards: list[tuple[int, chess.Board]] = []
    errors: list[str] = []
    for number, row in enumerate(rows, 1):
        if not MANDATORY_FIELDS.issubset(row):
            continue
        board, error = legal_record(row)
        if error:
            errors.append(f"line={number} game_id={row.get('game_id')} {error}")
            continue
        assert board is not None
        boards.append((row["game_id"], board))
        if row["end"] != "crash":
            if row["res"] != expected_result(board, row["a_white"]):
                errors.append(f"line={number} result mismatch")
            wanted_end = expected_end(board, row["plies"])
            if wanted_end is not None and row["end"] != wanted_end:
                errors.append(f"line={number} end={row['end']} wanted={wanted_end}")
    results.add("GATE-B", "b.python_chess_legality", not errors,
                f"illegal_move_count={len(errors)} legal_games={len(boards)}"
                + (f" errors={errors[:8]}" if errors else ""))
    return boards


def gate_e(args: argparse.Namespace, rows: list[dict[str, Any]], duplicates: int, results: Results) -> None:
    event_paths = [Path(args.events)] if args.events else [Path(str(args.dataset) + ".events.jsonl")]
    if args.drill_events:
        event_paths.append(Path(args.drill_events))
    events: list[dict[str, Any]] = []
    for event_path in event_paths:
        events.extend(json.loads(line) for line in event_path.read_text(encoding="utf-8").splitlines())
    starts = [row for row in events if row.get("event") == "generator_start"]
    completes = [row for row in events if row.get("event") == "generator_complete"]
    torn = [row for row in events if row.get("event") == "torn_line_quarantined"]
    failed = [row for row in events if row.get("event") == "generator_failed"]
    resume = len(starts) >= 2 and any(row.get("valid_before", 0) > 0 for row in starts[1:])
    grew = any(row.get("valid_after", 0) > row.get("valid_before", -1)
               for row in completes)
    in_window = any(400 <= row.get("valid_before", -1) <= 600 for row in starts[1:])
    drill = any(row.get("event") == "drill_complete" and row.get("drill") == "PASS"
                for row in events)
    passed = resume and grew and in_window and duplicates == 0 and drill
    results.add("GATE-E", "e.kill_resume_and_truncation_drill", passed,
                f"resume={resume} kill_in_400_600={in_window} grew={grew} "
                f"drill={drill} torn_incidents={len(torn)} failures={len(failed)} "
                f"duplicates={duplicates}")


def gate_f(record_path: Path, results: Results) -> None:
    # Gate (f) is reviewer-routed, but this machine check makes the route executable.
    text = record_path.read_text(encoding="utf-8", errors="replace")
    scoped: list[str] = []
    current = ""
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
        if current in {"Results", "Statistical Analysis", "Interpretation", "Conclusion"}:
            lowered = line.lower()
            negated = ("no elo" in lowered or "not an elo" in lowered
                       or "no strength claim" in lowered or "no strength assertion" in lowered)
            assertion = re.search(
                r"\bElo\b\s*(?:[:=]\s*)?[+\-]?\d|\bLOS\b\s*(?:[:=]\s*)?\d|"
                r"\bCI(?:95)?\b\s*(?:[:=]\s*)?\[[+\-]?\d|\b(?:beats|outperforms|stronger than)\b",
                line, re.IGNORECASE,
            )
            if assertion and not negated and "TBD" not in line:
                scoped.append(f"{current}: {line}")
    results.add("GATE-F", "f.no_strength_assertion", not scoped,
                f"strength_assertion_lines={len(scoped)}" + (f" lines={scoped}" if scoped else ""))


def diagnostics(rows: list[dict[str, Any]], boards: list[tuple[int, chess.Board]]) -> None:
    ends = Counter(row.get("end") for row in rows)
    positions: Counter[str] = Counter()
    for _, board in boards:
        current = board.copy(stack=True)
        for move in current.move_stack:
            positions[current.fen()] += 1
            current.pop()
        while current.move_stack:
            positions[current.fen()] += 1
            current.pop()
    total_positions = sum(positions.values())
    duplicate_positions = total_positions - len(positions)
    quiet_proxy = 0
    for row in rows:
        try:
            board = chess.Board()
            for uci in row.get("opening", []):
                board.push_uci(uci)
            for san in row.get("san", []):
                full_ply = board.fullmove_number * 2 + (0 if board.turn == chess.WHITE else 1) - 1
                previous_left_check = board.is_check()
                if (full_ply >= 10 and "x" not in san and not san.endswith(("+", "#"))
                        and not previous_left_check):
                    quiet_proxy += 1
                board.push_san(san)
        except Exception:
            continue
    white_points = 0.0
    a_white_points = a_black_points = 0.0
    for row in rows:
        white_points += 1.0 if row.get("res") == ("A" if row.get("a_white") else "B") else (
            0.5 if row.get("res") == "D" else 0.0)
        if row.get("a_white"):
            a_white_points += RESULT_SCORE.get(row.get("res"), 0.0)
        else:
            a_black_points += RESULT_SCORE.get(row.get("res"), 0.0)
    n = len(rows)
    degenerate = sum(1 for row in rows if row.get("end") == "mate" and len(row.get("san", [])) <= 6)
    print(f"DIAGNOSTIC end_counts={dict(sorted(ends.items(), key=lambda x: str(x[0])))}")
    print(f"DIAGNOSTIC san_position_yield={sum(len(r.get('san', [])) for r in rows)} "
          f"opening_plies={sum(len(r.get('opening', [])) for r in rows)} "
          f"quiet_proxy_opening_skipped={quiet_proxy} fit_scope={'all-terms' if quiet_proxy >= 30000 else 'mobility/tempo-subset'}")
    print(f"DIAGNOSTIC duplicate_positions={duplicate_positions} total_positions={total_positions}")
    print(f"DIAGNOSTIC degenerate_mate_san_le_6={degenerate}")
    if n:
        print(f"DIAGNOSTIC white_score={white_points / n:.4f} "
              f"a_score_white={a_white_points / max(1, sum(bool(r.get('a_white')) for r in rows)):.4f} "
              f"a_score_black={a_black_points / max(1, sum(not r.get('a_white') for r in rows)):.4f}")


def make_synthetic_demo(path: Path, binary: str, commit: str) -> None:
    rows = [base_record(game_id, binary, commit) for game_id in range(20)]
    rows[3]["binary_sha256"] = "0" * 64
    rows[5]["end"] = f"{rows[5]['end']}(0s)"
    rows[19]["game_id"] = 18
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as stream:
        for row in rows:
            stream.write((json.dumps(row, sort_keys=True) + "\n").encode("utf-8"))
        partial = (json.dumps(rows[19], sort_keys=True) + "\n").encode("utf-8")
        stream.write(partial[:len(partial) // 2])


def check_dataset(args: argparse.Namespace) -> Results:
    results = Results()
    path = Path(args.dataset)
    rows, torn = parse_jsonl(path, results)
    if torn == 0 and not any(row[0:2] == ("GATE-B", "b.jsonl_parse") for row in results.rows):
        results.add("GATE-B", "b.jsonl_parse", True, "all complete lines parsed")
    binary = args.expected_binary_sha256 or sha256_file(Path(args.exe))
    commit = args.expected_src_commit or git_commit()
    results.add("GATE-A", "a.volume", len(rows) >= args.min_games,
                f"games={len(rows)} min={args.min_games}")
    boards = check_legality(rows, results)
    check_provenance(rows, binary, commit, results)
    move_keys = [tuple(row.get("opening", [])) + tuple(row.get("san", [])) for row in rows]
    duplicates = len(move_keys) - len(set(move_keys))
    results.add("GATE-C", "c.duplicate_move_lists", duplicates == 0,
                f"duplicate_move_lists={duplicates}")
    color_ok = all(row.get("a_white") == (row.get("game_id", -1) % 2 == 0) for row in rows)
    a_white = sum(bool(row.get("a_white")) for row in rows)
    results.add("GATE-C", "c.color_balance", color_ok and abs(a_white - (len(rows) - a_white)) <= 1,
                f"a_white={a_white} b_white={len(rows) - a_white} parity={color_ok}")
    if not args.skip_gate_e:
        try:
            gate_e(args, rows, duplicates, results)
        except Exception as exc:
            results.add("GATE-E", "e.kill_resume_and_truncation_drill", False,
                        f"runner_evidence_error={exc}")
    if not args.skip_gate_f:
        gate_f(Path(args.record), results)
    diagnostics(rows, boards)
    return results


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset")
    parser.add_argument("--min-games", type=int, default=1000)
    parser.add_argument("--exe", default=str(DEFAULT_EXE))
    parser.add_argument("--expected-binary-sha256")
    parser.add_argument("--expected-src-commit")
    parser.add_argument("--events")
    parser.add_argument("--drill-events")
    parser.add_argument("--record", default=str(DEFAULT_RECORD))
    parser.add_argument("--skip-gate-e", action="store_true")
    parser.add_argument("--skip-gate-f", action="store_true")
    parser.add_argument("--synthetic-demo", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.synthetic_demo:
        binary = sha256_file(Path(args.exe))
        commit = git_commit()
        make_synthetic_demo(Path(args.dataset), binary, commit)
        args.min_games = 20
        args.skip_gate_e = True
    results = check_dataset(args)
    results.dump()
    passed = all(row[2] for row in results.rows)
    print(f"OVERALL {'PASS' if passed else 'FAIL'} gates=6")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

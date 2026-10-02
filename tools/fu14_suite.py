#!/usr/bin/env python3
"""F-U14 / FND-0033 - independent tactical suite (N=200): build, overlap gate, pin, smoke.

WHAT THIS TOOL IS FOR
E-0013's pre-fit commit needs an INDEPENDENT tactical suite (conjunct (f), E-0013 L292:
N >= 200), each position carrying a known best-move / expected-tactic annotation,
hash-pinned before any consumption, with fresh-game overlap = 0 against every existing
corpus under the F-U7 normalized-FEN dedup key (CLM-0003, FND-0023). This tool builds
that suite, runs that gate, pins the artifacts, re-checks the pins, and runs the one-shot
engine smoke pass. It does NOT interpret engine strength; the smoke output is raw data.

PROVENANCE (marked, not blurred)
Every suite position is CONSTRUCTED from scratch by this file's seeded generator
(random.Random(SEED) placement of two kings, attacker material and optional filler
pieces on an empty board) and is accepted ONLY after python-chess exhaustively proves
its annotation (immediate checkmate over every legal move, or forced mate-in-2 over
every legal reply). No suite position is replayed from, derived from, or selected
against any game in the E-0011 corpus (RUN-0001, m0_audit/e0011/games.jsonl), the
E-0013 corpus (build/s41/extract_new/positions.jsonl), or any E-0010/E-0012 self-play
corpus. Those corpora are read by `overlap` ONLY to compute intersection counts.

THE DEDUP KEY IS NOT RE-DERIVED HERE
`overlap` and `generate` import `normalize_fen` from tools/e0013_extract.py - the very
function the E-0013 overlap-0 gate compares (F-U7: side to move + piece placement +
castling + EP rights; halfmove clock and fullmove number excluded).

SUBCOMMANDS
  generate  build the suite (deterministic under --seed) -> research/manifests/fu14-tactical-suite-n200.json
  overlap   normalized-FEN intersection against every position-bearing corpus on disk
            -> research/manifests/fu14-overlap-report.json; exit 0 iff total overlap == 0,
            else exit 2 (nonzero BLOCKS: route to chief-architect, do not close)
  pin       write the hash-pin manifest (schema mirrors research/manifests/e0013-artifact-pins.json)
  verify    read-time re-hash of every pinned artifact + re-run of all 200 proofs (exit 2 on mismatch)
  smoke     one raw UCI pass of a binary over the suite -> _obs/fu14_smoke_raw.jsonl (data only)
  selftest  fixture checks for the proof machinery and the flip/normalize helpers
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
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
import chess.pgn

ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

# The F-U7 key itself: never re-derived, imported from the tool that owns the gate.
from e0013_extract import normalize_fen  # noqa: E402

DEFAULT_SUITE = ROOT / "research" / "manifests" / "fu14-tactical-suite-n200.json"
DEFAULT_REPORT = ROOT / "research" / "manifests" / "fu14-overlap-report.json"
DEFAULT_MANIFEST = ROOT / "research" / "manifests" / "fu14-tactical-suite-pins.json"
DEFAULT_SMOKE = ROOT / "_obs" / "fu14_smoke_raw.jsonl"

DATE = "2026-10-02"
SEED = 20261002
N_MATE_IN_1 = 100
N_MATE_IN_2 = 100
N_TOTAL = N_MATE_IN_1 + N_MATE_IN_2
MAX_ATTEMPTS_PER_TARGET = 250000

SUITE_FORMAT = "kana-fu14-tactical-suite-v1"
REPORT_FORMAT = "kana-fu14-overlap-report-v1"
PINS_FORMAT = "kana-fu14-pins-v1"

PROVENANCE = (
    "Constructed from scratch by tools/fu14_suite.py's seeded generator on an empty "
    "board (two kings + attacker material + optional filler pieces), accepted only after "
    "exhaustive python-chess proof of the annotation. NOT replayed from, derived from, or "
    "selected against any E-0011 (RUN-0001) or E-0013 corpus position; those corpora are "
    "read only by the `overlap` subcommand to count intersections."
)

ANNOTATION_CONTRACT = (
    "expected_best_move is a proven winning first move: for tactic=mate_in_1 it delivers "
    "immediate checkmate; for tactic=mate_in_2 it is one of the first moves after which "
    "EVERY legal reply is met by an immediate checkmate. expected_winning_moves_uci is "
    "the exhaustive list of all such first moves; unique_best_move says whether that list "
    "has exactly one element. Proofs are enumerated over the full legal move tree to "
    "depth 2 at annotation time and re-enumerated by `fu14_suite.py verify` at read time."
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True, encoding="utf-8",
                             errors="replace")
        return out.stdout.strip() if out.returncode == 0 else ""
    except OSError:
        return ""


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path | str) -> str:
    path = Path(path)
    try:
        return str(path.resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def write_json(path: Path | str, obj: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8", newline="\n")


def load_json(path: Path | str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def die(msg: str, code: int = 2) -> "NoReturn":  # type: ignore[name-defined]
    print(f"ABORT: {msg}", file=sys.stderr)
    raise SystemExit(code)


# --- proof machinery ---------------------------------------------------------------------
# Every annotation below is proved by exhaustive enumeration with python-chess - never by
# an engine, never by a heuristic score. The proof is re-runnable (`verify`).

PIECE_LETTER = {
    chess.PAWN: "P", chess.KNIGHT: "N", chess.BISHOP: "B",
    chess.ROOK: "R", chess.QUEEN: "Q",
}
PROMOTE = {"Q": chess.QUEEN, "R": chess.ROOK, "B": chess.BISHOP, "N": chess.KNIGHT}


def immediate_mate_moves(board: chess.Board) -> list[chess.Move]:
    """Every legal move that delivers checkmate RIGHT NOW (exhaustive)."""
    out: list[chess.Move] = []
    for move in board.legal_moves:
        after = board.copy(stack=False)
        after.push(move)
        if after.is_checkmate():
            out.append(move)
    return out


def forcing_mate_in_2_moves(board: chess.Board) -> list[chess.Move]:
    """Every legal first move m such that EVERY legal reply is met by an immediate mate.

    Callers must only call this when `immediate_mate_moves(board)` is empty, so every
    winner is a genuine mate-in-2 and not a mislabelled mate-in-1. Exhaustive over both
    ply layers; a first move that stalemates the opponent rejects the forced claim.
    """
    out: list[chess.Move] = []
    for move in board.legal_moves:
        after = board.copy(stack=False)
        after.push(move)
        replies = list(after.legal_moves)
        if not replies:
            # No reply at all: mate is excluded by the precondition, so this is stalemate.
            continue
        forced = True
        for reply in replies:
            after_reply = after.copy(stack=False)
            after_reply.push(reply)
            if not immediate_mate_moves(after_reply):
                forced = False
                break
        if forced:
            out.append(move)
    return out


def position_usable(board: chess.Board) -> bool:
    """Legality + tactic premises: both kings, no opposite check, kings apart, side to
    move NOT in check (the attacker moves freely), at least one legal move, no pawns on
    the back ranks."""
    wk, bk = board.king(chess.WHITE), board.king(chess.BLACK)
    if wk is None or bk is None:
        return False
    if chess.square_distance(wk, bk) < 2:
        return False
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece is None:
            continue
        if piece.piece_type == chess.PAWN and chess.square_rank(sq) in (0, 7):
            return False
    probe = board.copy(stack=False)
    probe.turn = not board.turn
    if probe.is_check():
        return False  # opposite check (also covers both kings in check)
    if board.is_check():
        return False  # the side to move must be the free attacker
    if not any(board.legal_moves):
        return False
    return True


def classify(board: chess.Board) -> tuple[str, list[chess.Move], dict[str, Any]] | None:
    """Prove the position's annotation or refuse it outright. None = not usable."""
    if not position_usable(board):
        return None
    m1 = sorted(immediate_mate_moves(board), key=lambda m: m.uci())
    if m1:
        return ("mate_in_1", m1, {
            "kind": "exhaustive-immediate-checkmate",
            "legal_moves_at_root": len(list(board.legal_moves)),
            "winning_moves_proved": len(m1),
            "proved_by": "python-chess full enumeration of every legal first move",
        })
    m2 = sorted(forcing_mate_in_2_moves(board), key=lambda m: m.uci())
    if m2:
        return ("mate_in_2", m2, {
            "kind": "exhaustive-forced-mate-in-2",
            "legal_moves_at_root": len(list(board.legal_moves)),
            "winning_moves_proved": len(m2),
            "proved_by": "python-chess full enumeration of every legal first move x every legal reply",
        })
    return None


# --- construction ------------------------------------------------------------------------

EDGE_SQUARES = [s for s in chess.SQUARES
                if chess.square_rank(s) in (0, 7) or chess.square_file(s) in (0, 7)]

# Weighted by repetition: long-range attackers dominate because they mate most often.
ATTACK_MATERIAL = [
    ("Q",), ("Q",), ("Q", "R"), ("Q", "R"), ("R", "R"), ("R", "R"),
    ("Q", "B"), ("Q", "B"), ("Q", "N"), ("R", "B"), ("R", "B"),
    ("Q", "R", "B"), ("Q", "R", "N"), ("R", "R", "B"), ("Q", "B", "B"),
    ("Q", "N", "N"), ("R", "N", "N"), ("B", "N"), ("R", "B", "N"),
]


def material_of(board: chess.Board, color: chess.Color) -> list[str]:
    out = []
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece is not None and piece.color == color and piece.piece_type != chess.KING:
            out.append(PIECE_LETTER[piece.piece_type])
    return sorted(out)


def construct(rng: random.Random, target: str) -> chess.Board | None:
    """One random candidate position (attacker = WHITE, side to move = WHITE).

    The color-mirrored twin is produced later by `flip_fen`, so black-to-move entries are
    mirrors of proved white-to-move entries, re-proved after the flip.
    """
    board = chess.Board.empty()
    dk = rng.choice(EDGE_SQUARES)
    if target == "mate_in_2":
        # A confined defender king is far likelier to have a forced mate-in-2.
        wk_pool = [s for s in chess.SQUARES
                   if s != dk and 2 <= chess.square_distance(s, dk) <= 4]
    else:
        wk_pool = [s for s in chess.SQUARES if s != dk]
    if not wk_pool:
        return None
    wk = rng.choice(wk_pool)
    used = {dk, wk}
    board.set_piece_at(dk, chess.Piece(chess.KING, chess.BLACK))
    board.set_piece_at(wk, chess.Piece(chess.KING, chess.WHITE))

    def take(pool: list[int]) -> int | None:
        options = [s for s in pool if s not in used]
        if not options:
            return None
        sq = rng.choice(options)
        used.add(sq)
        return sq

    # Attacker material (WHITE, to move).
    for letter in rng.choice(ATTACK_MATERIAL):
        sq = take(list(chess.SQUARES))
        if sq is None:
            return None
        board.set_piece_at(sq, chess.Piece(PROMOTE[letter], chess.WHITE))
    # Defender pawns on the defender's half (ranks 5-7): they build the boxes that make
    # back-rank style mates, and they never land on a back rank.
    if rng.random() < 0.9:
        pawn_pool = [s for s in chess.SQUARES if chess.square_rank(s) in (4, 5, 6)]
        for _ in range(rng.randint(1, 6)):
            sq = take(pawn_pool)
            if sq is None:
                break
            board.set_piece_at(sq, chess.Piece(chess.PAWN, chess.BLACK))
    # Defender pieces sometimes.
    if rng.random() < 0.45:
        for _ in range(rng.randint(1, 2)):
            pool = [s for s in chess.SQUARES if chess.square_rank(s) >= 4]
            sq = take(pool)
            if sq is None:
                break
            board.set_piece_at(sq, chess.Piece(rng.choice(
                [chess.ROOK, chess.BISHOP, chess.KNIGHT, chess.QUEEN]), chess.BLACK))
    # Attacker spares sometimes (keeps positions from being bare K+piece drills).
    if rng.random() < 0.4:
        pt = rng.choice([chess.ROOK, chess.BISHOP, chess.KNIGHT, chess.PAWN])
        pool = ([s for s in chess.SQUARES if chess.square_rank(s) in (1, 2, 3, 4, 5, 6)]
                if pt == chess.PAWN else list(chess.SQUARES))
        sq = take(pool)
        if sq is not None:
            board.set_piece_at(sq, chess.Piece(pt, chess.WHITE))
    board.turn = chess.WHITE
    board.castling_rights = 0  # no castling rights: keeps flip_fen's no-rights assertion valid
    board.ep_square = None
    board.halfmove_clock = 0
    board.fullmove_number = 1
    if not position_usable(board):
        return None
    return board


def _compress_row(squares: list[str]) -> str:
    out, run = "", 0
    for sq in squares:
        if sq == "":
            run += 1
        else:
            if run:
                out += str(run)
                run = 0
            out += sq
    if run:
        out += str(run)
    return out


def flip_fen(fen: str) -> str:
    """Vertical mirror with colors swapped: (file, rank) -> (file, 9-rank), w <-> b.

    Generated positions never carry castling or EP rights (asserted), so no rights
    mapping is needed. The flipped position is re-proved from scratch by the caller.
    """
    parts = fen.split()
    if parts[2] != "-" or parts[3] != "-":
        raise ValueError(f"flip_fen assumes no castling/EP rights: {fen!r}")
    rows = parts[0].split("/")
    if len(rows) != 8:
        raise ValueError(f"flip_fen expects 8 ranks: {fen!r}")
    flipped = []
    for row in reversed(rows):
        expanded: list[str] = []
        for ch in row:
            if ch.isdigit():
                expanded.extend([""] * int(ch))
            else:
                expanded.append(ch)
        if len(expanded) != 8:
            raise ValueError(f"flip_fen rank does not expand to 8: {row!r}")
        flipped.append(_compress_row([c.swapcase() for c in expanded]))
    turn = "b" if parts[1] == "w" else "w"
    return " ".join(["/".join(flipped), turn, "-", "-", "0", "1"])


# --- generate -----------------------------------------------------------------------------

def cmd_generate(args: argparse.Namespace) -> int:
    seed = args.seed
    rng = random.Random(seed)
    positions: list[dict[str, Any]] = []
    seen: set[str] = set()
    attempts_by_target: dict[str, int] = {}
    mirrored_count = 0
    idx = 0
    t0 = time.monotonic()
    for target, want in (("mate_in_1", args.mate_in_1), ("mate_in_2", args.mate_in_2)):
        accepted = attempts = 0
        while accepted < want:
            attempts += 1
            if attempts % 500 == 0:
                print(f"  [{target}] attempts={attempts} accepted={accepted}",
                      file=sys.stderr, flush=True)
            if attempts > MAX_ATTEMPTS_PER_TARGET:
                die(f"{target}: no acceptance after {attempts} attempts")
            board = construct(rng, target)
            if board is None:
                continue
            res = classify(board)
            if res is None or res[0] != target:
                continue
            color_mirrored = False
            if rng.random() < 0.5:
                flipped = chess.Board(flip_fen(board.fen()))
                res_flipped = classify(flipped)
                if res_flipped is not None and res_flipped[0] == target:
                    board, res, color_mirrored = flipped, res_flipped, True
            tactic, winners, proof = res
            norm = normalize_fen(board)
            if norm in seen:
                continue
            seen.add(norm)
            idx += 1
            accepted += 1
            if color_mirrored:
                mirrored_count += 1
            best = winners[0]
            positions.append({
                "id": f"FU14-{idx:04d}",
                "fen": board.fen(),
                "norm_fen": norm,
                "side_to_move": "w" if board.turn == chess.WHITE else "b",
                "tactic": tactic,
                "expected_best_move": {"uci": best.uci(), "san": board.san(best)},
                "expected_winning_moves_uci": [m.uci() for m in winners],
                "unique_winning_move": len(winners) == 1,
                "proof": proof,
                "construction": {
                    "method": "seeded-random-placement on an empty board, accepted only after exhaustive proof",
                    "seed": seed,
                    "target": target,
                    "attempt": attempts,
                    "color_mirrored": color_mirrored,
                    "attacker_material": material_of(board, board.turn),
                    "defender_material": material_of(board, not board.turn),
                },
            })
        attempts_by_target[target] = attempts
        print(f"[generate] {target}: {accepted} accepted in {attempts} attempts",
              flush=True)

    if len(positions) != args.mate_in_1 + args.mate_in_2:
        die(f"internal: expected {args.mate_in_1 + args.mate_in_2} positions, got {len(positions)}")
    if len(seen) != len(positions):
        die(f"internal: suite norm_fen dedup failed ({len(seen)} distinct of {len(positions)})")

    white = sum(1 for p in positions if p["side_to_move"] == "w")
    suite = {
        "format": SUITE_FORMAT,
        "n": len(positions),
        "created": DATE,
        "created_by": "data-pipeline-engineer (F-U14 seat)",
        "finding": "FND-0033",
        "obligation": "F-U14",
        "claim": "CLM-0003",
        "provenance": PROVENANCE,
        "provenance_source": "tools/fu14_suite.py generate",
        "annotation_contract": ANNOTATION_CONTRACT,
        "dedup_key": {
            "source": "tools/e0013_extract.py::normalize_fen",
            "fields": ["piece placement", "side to move", "castling rights", "en-passant rights"],
            "excludes": ["halfmove clock", "fullmove number"],
        },
        "generator": {
            "tool": "tools/fu14_suite.py",
            "command": f"python tools/fu14_suite.py generate --seed {seed}",
            "seed": seed,
            "python": sys.version.split()[0],
            "python_chess": chess.__version__,
            "attempts_by_target": attempts_by_target,
            "color_mirrored": mirrored_count,
            "elapsed_s": round(time.monotonic() - t0, 3),
        },
        "counts": {
            "n": len(positions),
            "mate_in_1": sum(1 for p in positions if p["tactic"] == "mate_in_1"),
            "mate_in_2": sum(1 for p in positions if p["tactic"] == "mate_in_2"),
            "white_to_move": white,
            "black_to_move": len(positions) - white,
            "unique_best_move": sum(1 for p in positions if p["unique_winning_move"]),
            "distinct_norm_fen": len(seen),
        },
        "positions": positions,
    }
    write_json(args.out, suite)
    print(f"[generate] wrote {rel(args.out)} n={len(positions)} "
          f"mate_in_1={suite['counts']['mate_in_1']} mate_in_2={suite['counts']['mate_in_2']} "
          f"w={white} b={len(positions) - white} distinct_norm_fen={len(seen)} "
          f"sha256={sha256_file(args.out)}")
    return 0


# --- overlap: corpus discovery and position loading ---------------------------------------

# Roles for the known corpora. Discovery itself is a FILESYSTEM SWEEP (below), so a corpus
# that is not named here is still checked - it just gets a generic id.
CORPUS_ROLES = {
    "m0_audit/e0011/games.jsonl":
        "E-0011 corpus (RUN-0001) - the CLM-0003 contamination reference",
    "build/s41/extract_new/positions.jsonl":
        "E-0013 count-only extraction (F-U9 hash-pinned artifacts)",
    "build/s41/extract_new/split_map.json":
        "game->split assignment; carries no FEN content",
    "m0_audit/e0011/smoke_games.jsonl": "E-0011 pipeline smoke games",
    "m0_audit/e0011/smoke_v2_games.jsonl": "E-0011 pipeline smoke games (v2)",
    "m0_audit/e0011/synthetic20.jsonl": "E-0011 synthetic fixture games",
    "m0_audit/e0011/truncation_drill_games.jsonl": "E-0011 truncation-drill games",
    "m0_audit/e0011_failed_attempt1/games.jsonl": "E-0011 abandoned first campaign segment",
    "m0_audit/e0012_known/games.jsonl": "E-0012 known-difference control games",
    "m0_audit/e0012_null/games.jsonl": "E-0012 null-pair control games",
    "m0_audit/runjob_test/games.jsonl": "runjob self-test records (no position content)",
    "tactics_set.py": "the pre-existing 73-position suite (EV-0006, E-00008)",
    "tactics_gen.txt": "E-00008 generator log (FEN-bearing lines)",
    "selfplay_o3d.pgn": "E-00006 O3c self-play PGN",
}
SWEEP_SKIP_DIRS = {
    ".git", "__pycache__", "CMakeFiles", "_index", "x64", "Debug", "Release", "Audit",
    "ALL_BUILD.dir", "ZERO_CHECK.dir",
}
SWEEP_SKIP_PREFIX = ("kana", "CMakeFiles", "ZERO", "ALL_BUILD")
FEN_LINE_RE = re.compile(
    r"([rnbqkpRNBQKP1-8]+(?:/[rnbqkpRNBQKP1-8]+){7})\s+([wb])\s+([KQkq-]+)\s+"
    r"([a-h1-6-]+)\s+(\d+)\s+(\d+)"
)


def discover_corpus_files() -> list[Path]:
    """Every *.jsonl / *.pgn in the repository, plus the two named non-JSON corpora.

    Excluded only: build-system guts (CMake dirs), __pycache__, .git, and the derived
    index cache - none of which hold positions. `_obs/` is NOT excluded, so a corpus
    dropped into session scratch would still be caught (this seat's own outputs are
    skipped explicitly by path instead).
    """
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in SWEEP_SKIP_DIRS and not d.startswith(SWEEP_SKIP_PREFIX)]
        for name in filenames:
            low = name.lower()
            if low.endswith((".jsonl", ".pgn")) or name in ("tactics_set.py", "tactics_gen.txt"):
                found.append(Path(dirpath) / name)
    return sorted(set(found))


def classify_corpus(path: Path) -> tuple[str, str]:
    """Return (format, reason-if-skipped)."""
    rel_path = rel(path)
    if rel_path.startswith("_obs/fu14_smoke_raw"):
        return "self", "this seat's own smoke output, not a corpus"
    low = path.name.lower()
    if low.endswith(".jsonl"):
        keys: set[str] = set()
        try:
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    keys = set(json.loads(line).keys())
                    break
                else:
                    return "empty", "file has no records"
        except (OSError, json.JSONDecodeError) as exc:
            return "unreadable", f"cannot parse first record: {exc}"
        if "norm_fen" in keys:
            return "positions-jsonl", ""
        if {"opening", "san"} <= keys:
            return "games-jsonl", ""
        if "fen" in keys:
            return "fen-jsonl", ""
        return "no-position-content", f"first-record keys carry no position fields: {sorted(keys)}"
    if low.endswith(".pgn"):
        return "pgn", ""
    if path.name == "tactics_set.py":
        return "tactics-py", ""
    if path.name == "tactics_gen.txt":
        return "fen-lines", ""
    if path.name == "split_map.json":
        return "no-position-content", ("game->split assignment; carries no FEN content "
                                       "(documented, not assumed)")
    return "no-position-content", "unrecognised suffix"


def load_games_jsonl(path: Path) -> tuple[set[str], int, list[str]]:
    """E-0011-schema games: replay `opening` (UCI) then `san`, harvesting the normalized
    FEN of startpos, every intermediate position and the final position. That is a
    SUPERSET of the extractor's candidate segment (san-only) - deliberately stricter for
    a contamination gate."""
    norms: set[str] = set()
    records = 0
    errors: list[str] = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {lineno}: json: {exc}")
                continue
            records += 1
            try:
                board = chess.Board()
                norms.add(normalize_fen(board))
                for uci in row.get("opening") or []:
                    board.push_uci(uci)
                    norms.add(normalize_fen(board))
                for san in row.get("san") or []:
                    board.push_san(san)
                    norms.add(normalize_fen(board))
            except Exception as exc:  # noqa: BLE001 - recorded, not hidden
                errors.append(f"line {lineno}: replay: {exc}")
    return norms, records, errors


def load_positions_jsonl(path: Path) -> tuple[set[str], int, list[str]]:
    """E-0013 positions: read the stored `norm_fen`, cross-checking a sample of the rows
    against the live `normalize_fen(fen)` so a stale field cannot diverge silently."""
    norms: set[str] = set()
    records = 0
    errors: list[str] = []
    cross_checked = 0
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {lineno}: json: {exc}")
                continue
            records += 1
            if "norm_fen" in row:
                norms.add(row["norm_fen"])
                if cross_checked < 1000 and "fen" in row:
                    live = normalize_fen(chess.Board(row["fen"]))
                    if live != row["norm_fen"]:
                        errors.append(f"line {lineno}: stored norm_fen != normalize_fen(fen)")
                    cross_checked += 1
            else:
                norms.add(normalize_fen(chess.Board(row["fen"])))
    if records:
        errors.append(f"info: {min(records, 1000)} row(s) cross-checked against live normalize_fen")
    return norms, records, errors


def load_fen_jsonl(path: Path) -> tuple[set[str], int, list[str]]:
    norms: set[str] = set()
    records = 0
    errors: list[str] = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                norms.add(normalize_fen(chess.Board(row["fen"])))
                records += 1
            except Exception as exc:  # noqa: BLE001
                errors.append(f"line {lineno}: {exc}")
    return norms, records, errors


def load_tactics_py(path: Path) -> tuple[set[str], int, list[str]]:
    spec = importlib.util.spec_from_file_location("fu14_corpus_tactics_set", path)
    if spec is None or spec.loader is None:
        return set(), 0, [f"cannot load module {path}"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    norms: set[str] = set()
    records = 0
    errors: list[str] = []
    for entry in getattr(module, "POSITIONS", []):
        try:
            fen = entry[1] if isinstance(entry, (tuple, list)) else entry["fen"]
            norms.add(normalize_fen(chess.Board(fen)))
            records += 1
        except Exception as exc:  # noqa: BLE001
            errors.append(f"entry: {exc}")
    return norms, records, errors


def load_fen_lines(path: Path) -> tuple[set[str], int, list[str]]:
    norms: set[str] = set()
    records = 0
    errors: list[str] = []
    raw = path.read_bytes()
    # tactics_gen.txt is UTF-16 (PowerShell redirect); decode by BOM, not by assumption.
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        text = raw.decode("utf-16")
    else:
        text = raw.decode("utf-8", errors="replace")
    for lineno, line in enumerate(text.splitlines(), 1):
        m = FEN_LINE_RE.search(line)
        if not m:
            continue
        try:
            norms.add(normalize_fen(chess.Board(m.group(0))))
            records += 1
        except Exception as exc:  # noqa: BLE001
            errors.append(f"line {lineno}: {exc}")
    return norms, records, errors


def load_pgn(path: Path) -> tuple[set[str], int, list[str]]:
    norms: set[str] = set()
    records = 0
    errors: list[str] = []
    handle = io.StringIO(path.read_text(encoding="utf-8", errors="replace"))
    while True:
        game = chess.pgn.read_game(handle)
        if game is None:
            break
        records += 1
        board = game.board()
        norms.add(normalize_fen(board))
        try:
            for move in game.mainline_moves():
                board.push(move)
                norms.add(normalize_fen(board))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"game {records}: {exc}")
    return norms, records, errors


LOADERS = {
    "games-jsonl": load_games_jsonl,
    "positions-jsonl": load_positions_jsonl,
    "fen-jsonl": load_fen_jsonl,
    "tactics-py": load_tactics_py,
    "fen-lines": load_fen_lines,
    "pgn": load_pgn,
}


# --- overlap ------------------------------------------------------------------------------

def cmd_overlap(args: argparse.Namespace) -> int:
    suite_path = Path(args.suite)
    if not suite_path.is_file():
        die(f"suite not found: {suite_path}")
    suite = load_json(suite_path)
    if suite.get("format") != SUITE_FORMAT:
        die(f"unexpected suite format: {suite.get('format')!r}")
    suite_norms = {p["norm_fen"] for p in suite["positions"]}
    if len(suite_norms) != len(suite["positions"]):
        die("suite contains duplicate norm_fen values internally - regenerate it")
    id_by_norm = {p["norm_fen"]: p["id"] for p in suite["positions"]}

    corpora: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    union_hits: set[str] = set()
    sum_hits = 0
    max_hits = 0

    files = discover_corpus_files()
    # Known roles whose files the sweep does not reach (e.g. *.json such as the split map)
    # are pulled in explicitly so "every corpus" is a checked claim, not an assumption.
    known_rel = {rel(p) for p in files}
    for role_path in CORPUS_ROLES:
        if role_path not in known_rel and (ROOT / role_path).is_file():
            files.append(ROOT / role_path)

    for path in sorted(set(files)):
        fmt, reason = classify_corpus(path)
        rel_path = rel(path)
        role = CORPUS_ROLES.get(rel_path, "not in the known-corpus table (found by sweep)")
        entry: dict[str, Any] = {
            "id": rel_path, "path": rel_path, "format": fmt, "role": role,
            "bytes": path.stat().st_size, "sha256": sha256_file(path),
        }
        if fmt in ("self", "empty", "unreadable", "no-position-content"):
            skipped.append({"path": rel_path, "format": fmt, "reason": reason or fmt})
            continue
        loader = LOADERS[fmt]
        norms, records, errors = loader(path)
        hits = sorted(suite_norms & norms)
        union_hits.update(hits)
        sum_hits += len(hits)
        max_hits = max(max_hits, len(hits))
        # Only errors, not the informational cross-check notes, are parse errors.
        parse_errors = [e for e in errors if not e.startswith("info:")]
        entry.update({
            "records": records,
            "distinct_norm_fens": len(norms),
            "parse_errors": parse_errors,
            "notes": [e for e in errors if e.startswith("info:")],
            "overlap_count": len(hits),
            "overlap_norm_fens": hits,
            "overlap_suite_ids": [id_by_norm[h] for h in hits],
        })
        corpora.append(entry)
        print(f"[overlap] {rel_path}: records={records} distinct_norm_fens={len(norms)} "
              f"overlap={len(hits)}", flush=True)

    value = len(union_hits)
    gate = "PASS" if value == 0 else "BLOCK"
    report = {
        "format": REPORT_FORMAT,
        "written": DATE,
        "written_at_commit": git_head(),
        "written_by": "data-pipeline-engineer (F-U14 seat)",
        "finding": "FND-0033",
        "claim": "CLM-0003",
        "gate": {
            "rule": "normalized-FEN overlap between the F-U14 suite and EVERY existing "
                    "corpus must be exactly 0 (CLM-0003; F-U7 key)",
            "expected_value": 0,
            "exit_criterion": "this command exits 0 iff overlap.value == 0; a nonzero value "
                              "BLOCKS closure and routes to chief-architect",
        },
        "dedup_key": {
            "source": "tools/e0013_extract.py::normalize_fen",
            "fields": ["piece placement", "side to move", "castling rights", "en-passant rights"],
            "excludes": ["halfmove clock", "fullmove number"],
        },
        "method": {
            "discovery": "filesystem sweep of every *.jsonl / *.pgn plus tactics_set.py and "
                         "tactics_gen.txt (build-system guts, __pycache__, .git and the "
                         "derived index cache excluded); known roles in CORPUS_ROLES; "
                         "unlisted position-bearing files are still loaded and counted",
            "games": "full replay of opening (UCI) + san; startpos, every intermediate "
                     "position and the final position are harvested (superset of the "
                     "extractor's san-only candidate segment - stricter)",
            "suite": "norm_fen values as written by generate, all via normalize_fen",
        },
        "suite": {
            "path": rel(suite_path),
            "sha256": sha256_file(suite_path),
            "n_positions": len(suite["positions"]),
            "distinct_norm_fen": len(suite_norms),
        },
        "corpora": corpora,
        "corpora_checked": len(corpora),
        "skipped": skipped,
        "overlap": {
            "value": value,
            "union_suite_ids": sorted(id_by_norm[h] for h in union_hits),
            "union_norm_fens": sorted(union_hits),
            "sum_per_corpus": sum_hits,
            "max_per_corpus": max_hits,
            "gate": gate,
        },
    }
    write_json(args.out, report)
    print(f"[overlap] corpora_checked={len(corpora)} skipped={len(skipped)} "
          f"sum_per_corpus={sum_hits} max_per_corpus={max_hits} "
          f"UNION={value} gate={gate} -> {rel(args.out)} "
          f"sha256={sha256_file(args.out)}")
    if value != 0:
        print(f"BLOCKED: overlap value {value} != 0 - route to chief-architect; "
              "do NOT close FND-0033.", file=sys.stderr)
        return 2
    return 0


# --- pin / verify -------------------------------------------------------------------------

def cmd_pin(args: argparse.Namespace) -> int:
    suite = Path(args.suite)
    report = Path(args.report)
    smoke = Path(args.smoke)
    for required in (suite, report):
        if not required.is_file():
            die(f"cannot pin: {rel(required)} does not exist (run generate/overlap first)")
    if load_json(report).get("overlap", {}).get("value") != 0:
        die("cannot pin: overlap report value is not 0 - route to chief-architect first")

    def art(path: Path, kind: str, role: str) -> dict[str, Any]:
        return {
            "path": rel(path),
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
            "kind": kind,
            "role": role,
        }

    artifacts: dict[str, Any] = {
        suite.name: art(suite, "independent-tactical-suite",
                        "THE pre-registered FEN list for E-0013's conjunct (f): N=200, "
                        "every position with an exhaustively proved best-move/expected-tactic "
                        "annotation. Committed, not just pinned: R-0019 Q-SUITE closed the "
                        "substitution path, so the bytes below are the suite."),
        report.name: art(report, "overlap-report",
                         "the CLM-0003 normalized-FEN overlap-0 evidence against every "
                         "existing corpus. The exit criterion for FND-0033 is "
                         "overlap.value == 0 in this file."),
    }
    if smoke.is_file():
        entries = [ln for ln in smoke.read_text(encoding="utf-8").splitlines() if ln.strip()]
        artifacts[smoke.name] = {
            **art(smoke, "engine-smoke-raw",
                  "one raw UCI smoke pass of the master binary over the suite: full "
                  "per-position transcripts, bestmoves and the suite's expected annotations. "
                  "RAW DATA ONLY - no aggregate, no verdict, no strength claim is recorded "
                  "in it."),
            "records": max(0, len(entries) - 1),
            "committed_despite_gitignore": "_obs/ is gitignored (session scratch); this file "
                                           "is force-added so the pin and the bytes stay together",
        }
    else:
        artifacts[smoke.name] = {
            "path": rel(smoke), "sha256": None, "kind": "engine-smoke-raw",
            "null_reason": "smoke pass has not run yet; `fu14_suite.py smoke` writes it and "
                           "`fu14_suite.py pin` must be re-run to pin the bytes",
        }

    manifest = {
        "format": PINS_FORMAT,
        "record": "FND-0033 (F-U14) - E-0013 pre-fit commit element: the independent "
                  "suite's identity and SHA-256",
        "ruled_by": "FND-0033 F-U14 (N >= 200 independent tactical suite, hash-pinned); "
                    "CLM-0003 (fresh-game normalized-FEN overlap must be zero); "
                    "F-U7 dedup key (tools/e0013_extract.py::normalize_fen)",
        "written": DATE,
        "written_at_commit": git_head(),
        "written_by": "data-pipeline-engineer (F-U14 seat)",
        "read_time_check": "python tools/fu14_suite.py verify --manifest "
                           "research/manifests/fu14-tactical-suite-pins.json  "
                           "(re-hashes every artifact below, re-runs all 200 exhaustive proofs "
                           "and re-checks the overlap gate value; exit 2 on any mismatch)",
        "why_this_file_is_the_control": "A pin is only as good as the discipline around it: it "
                                        "must be committed BEFORE the read it protects, and a "
                                        "consumer must re-hash at read time. `verify` discharges "
                                        "the second half; this file's git history discharges the "
                                        "first.",
        "dedup_key": {
            "source": "tools/e0013_extract.py::normalize_fen",
            "fields": ["piece placement", "side to move", "castling rights", "en-passant rights"],
            "excludes": ["halfmove clock", "fullmove number"],
        },
        "artifacts": artifacts,
        "constraints": {
            "n_floor": "N >= 200 (E-0013 L292); this suite pins n = 200",
            "provenance": PROVENANCE,
            "substitution_closed": "R-0019 Q-SUITE: a substitute cannot be swapped in later; "
                                   "consumers must pass this manifest's digests",
            "not_a_strength_claim": "nothing in this manifest is an engine-strength statement",
        },
    }
    write_json(args.manifest, manifest)
    print(f"[pin] wrote {rel(args.manifest)} "
          f"artifacts={len(artifacts)} sha256={sha256_file(args.manifest)}")
    for name, meta in artifacts.items():
        print(f"  {name}: {meta.get('sha256')}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest)
    if not manifest_path.is_file():
        die(f"manifest not found: {manifest_path}")
    manifest = load_json(manifest_path)
    if manifest.get("format") != PINS_FORMAT:
        die(f"unexpected manifest format: {manifest.get('format')!r}")
    problems: list[str] = []
    for name, meta in manifest["artifacts"].items():
        path = ROOT / meta["path"]
        if not path.is_file():
            problems.append(f"{name}: missing at {meta['path']}")
            continue
        if meta.get("sha256") is None:
            problems.append(f"{name}: manifest carries sha256 null")
            continue
        actual = sha256_file(path)
        if actual != meta["sha256"]:
            problems.append(f"{name}: sha256 mismatch (pinned {meta['sha256']}, actual {actual})")
        if path.stat().st_size != meta.get("bytes"):
            problems.append(f"{name}: byte count mismatch")

    suite_meta = next((m for m in manifest["artifacts"].values()
                       if m.get("kind") == "independent-tactical-suite"), None)
    if suite_meta is None or suite_meta.get("sha256") is None:
        problems.append("manifest does not pin the suite")
        suite = {"positions": [], "n": 0}
    else:
        suite = load_json(ROOT / suite_meta["path"])
    if suite.get("n") != N_TOTAL:
        problems.append(f"suite n={suite.get('n')} != {N_TOTAL}")
    norms = [p["norm_fen"] for p in suite["positions"]]
    if len(set(norms)) != len(norms):
        problems.append("suite contains duplicate norm_fen values")
    for p in suite["positions"]:
        board = chess.Board(p["fen"])
        if normalize_fen(board) != p["norm_fen"]:
            problems.append(f"{p['id']}: norm_fen field != normalize_fen(fen)")
            continue
        res = classify(board)
        if res is None:
            problems.append(f"{p['id']}: proof no longer classifies")
            continue
        tactic, winners, _ = res
        if tactic != p["tactic"]:
            problems.append(f"{p['id']}: tactic {p['tactic']} != re-proved {tactic}")
        if [m.uci() for m in winners] != p["expected_winning_moves_uci"]:
            problems.append(f"{p['id']}: winning-move set changed under re-proof")
        if p["expected_best_move"]["uci"] not in p["expected_winning_moves_uci"]:
            problems.append(f"{p['id']}: annotated best move is not in its own winning set")
        san = board.san(chess.Move.from_uci(p["expected_best_move"]["uci"]))
        if san != p["expected_best_move"]["san"]:
            problems.append(f"{p['id']}: san mismatch")

    report_meta = manifest["artifacts"].get("fu14-overlap-report.json")
    if report_meta and report_meta.get("sha256"):
        report_path = ROOT / report_meta["path"]
        if report_path.is_file():
            overlap_value = load_json(report_path).get("overlap", {}).get("value")
            if overlap_value != 0:
                problems.append(f"overlap report value is {overlap_value}, not 0")
        else:
            problems.append(f"overlap report missing at {report_meta['path']}")

    if problems:
        for line in problems:
            print(f"FAIL  {line}")
        print(f"[verify] FAIL problems={len(problems)}", file=sys.stderr)
        return 2
    print(f"[verify] PASS artifacts={len(manifest['artifacts'])} "
          f"re-proved={len(suite['positions'])} overlap_value=0 "
          f"suite_sha256={suite_meta.get('sha256')}")
    return 0


# --- smoke: raw UCI pass, data only -------------------------------------------------------

class SmokeEngine:
    """Minimal UCI driver: reader thread + queue, full transcript kept verbatim."""

    def __init__(self, exe: Path, timeout: float):
        self.timeout = timeout
        # argv[1] = "uci" is the engine's explicit UCI entry path (same as measure_qs.py
        # and tools/uci_probe.py): without it the binary does not enter the UCI loop.
        self.proc = subprocess.Popen(
            [str(exe), "uci"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace",
            bufsize=1, cwd=str(ROOT))
        self.eof = False
        q: queue.Queue[str | None] = queue.Queue()

        def pump() -> None:
            assert self.proc.stdout is not None
            for line in self.proc.stdout:
                q.put(line.rstrip("\r\n"))
            q.put(None)

        threading.Thread(target=pump, daemon=True).start()
        self._q = q

    def send(self, command: str) -> None:
        assert self.proc.stdin is not None
        self.proc.stdin.write(command + "\n")
        self.proc.stdin.flush()

    def wait_for(self, predicate, timeout: float | None = None) -> list[str] | None:
        """Return every line up to and including the first that satisfies `predicate`,
        or None on timeout/EOF. Nothing in the returned window is dropped."""
        deadline = time.monotonic() + (timeout if timeout is not None else self.timeout)
        got: list[str] = []
        while time.monotonic() < deadline:
            try:
                line = self._q.get(timeout=0.05)
            except queue.Empty:
                continue
            if line is None:
                self.eof = True
                return None
            got.append(line)
            if predicate(line):
                return got
        return None

    def close(self) -> None:
        try:
            if self.proc.poll() is None:
                self.send("quit")
                self.proc.wait(timeout=3)
        except Exception:  # noqa: BLE001
            pass
        if self.proc.poll() is None:
            self.proc.kill()
            try:
                self.proc.wait(timeout=3)
            except Exception:  # noqa: BLE001
                pass


def cmd_smoke(args: argparse.Namespace) -> int:
    """ONE raw pass of the engine over the suite. Records transcripts, bestmoves and the
    suite's own expected annotations - nothing else. No hit-rate, no verdict, no
    interpretation: aggregating this file is a downstream reader's job, not this tool's."""
    exe = Path(args.exe)
    if not exe.is_absolute():
        exe = ROOT / exe
    if not exe.is_file():
        die(f"engine binary not found: {exe}")
    suite_path = Path(args.suite)
    if not suite_path.is_file():
        die(f"suite not found: {suite_path} (run generate first)")
    suite = load_json(suite_path)
    positions = suite["positions"]

    engine = SmokeEngine(exe, args.timeout)
    out = Path(args.out)
    timeouts = 0
    try:
        engine.send("uci")
        id_lines = engine.wait_for(lambda l: l == "uciok", 15.0)
        if id_lines is None:
            die("engine did not answer `uci` (no uciok)")
        engine.send("isready")
        if engine.wait_for(lambda l: l == "readyok", 15.0) is None:
            die("engine did not answer `isready` (no readyok)")

        header = {
            "tool": "tools/fu14_suite.py smoke",
            "command": f"python tools/fu14_suite.py smoke --exe {rel(exe)} "
                       f"--depth {args.depth} --timeout {args.timeout}",
            "written": utc_now(),
            "exe": rel(exe),
            "exe_sha256": sha256_file(exe),
            "exe_bytes": exe.stat().st_size,
            "git_head": git_head(),
            "suite_path": rel(suite_path),
            "suite_sha256": sha256_file(suite_path),
            "suite_n": len(positions),
            "engine_id": [l for l in id_lines if l.startswith("id ")],
            "per_position": ["> ucinewgame", "> isready", "> position fen <suite fen>",
                             f"> go depth {args.depth}"],
            "depth": args.depth,
            "per_position_timeout_s": args.timeout,
            "note": "RAW DATA ONLY: the engine's verbatim UCI output plus the suite's own "
                    "expected annotations. No aggregate, no verdict and no engine-strength "
                    "interpretation is recorded here or produced by this tool.",
        }
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps({"_header": header}, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
            n = len(positions)
            for i, pos in enumerate(positions):
                t0 = time.monotonic()
                engine.send("ucinewgame")
                engine.send("isready")
                engine.wait_for(lambda l: l == "readyok", 10.0)
                go = f"go depth {args.depth}"
                engine.send(f"position fen {pos['fen']}")
                engine.send(go)
                got = engine.wait_for(lambda l: l.startswith("bestmove"), args.timeout)
                timed_out = got is None
                if timed_out:
                    engine.send("stop")
                    got = engine.wait_for(lambda l: l.startswith("bestmove"), 5.0)
                if got is None:
                    timeouts += 1
                bestmove_line = None
                if got:
                    for line in reversed(got):
                        if line.startswith("bestmove"):
                            bestmove_line = line
                            break
                fields = bestmove_line.split() if bestmove_line else []
                record = {
                    "index": i,
                    "id": pos["id"],
                    "fen": pos["fen"],
                    "tactic": pos["tactic"],
                    "expected_best_move": pos["expected_best_move"],
                    "expected_winning_moves_uci": pos["expected_winning_moves_uci"],
                    "go": go,
                    "uci_received": got or [],
                    "bestmove_line": bestmove_line,
                    "bestmove": fields[1] if len(fields) > 1 else None,
                    "timed_out": timed_out,
                    "engine_eof": engine.eof,
                    "wall_time_s": round(time.monotonic() - t0, 3),
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())
                if (i + 1) % 20 == 0 or i + 1 == n:
                    print(f"[smoke] {i + 1}/{n} written", flush=True)
    finally:
        engine.close()

    print(f"[smoke] wrote {rel(out)} positions={len(positions)} "
          f"sha256={sha256_file(out)} timeouts={timeouts} engine_eof={engine.eof}")
    return 0


# --- selftest -----------------------------------------------------------------------------

def cmd_selftest(_args: argparse.Namespace) -> int:
    results: list[tuple[str, bool]] = []

    def check(name: str, ok: bool) -> None:
        results.append((name, bool(ok)))
        print(("PASS  " if ok else "FAIL  ") + name)

    # (a) Known mate-in-1 with a KNOWN unique winner: back rank, rook a1 -> a8.
    board = chess.Board("6k1/5ppp/8/8/8/8/8/R5K1 w - - 0 1")
    res = classify(board)
    check("M1 fixture classifies as mate_in_1", res is not None and res[0] == "mate_in_1")
    check("M1 fixture winner is exactly a1a8",
          res is not None and [m.uci() for m in res[1]] == ["a1a8"])
    check("M1 fixture best-move san is Ra8#",
          res is not None and board.san(res[1][0]) == "Ra8#")

    # (b) A position with no tactic must be refused, not guessed.
    check("bare-kings refuses classification",
          classify(chess.Board("8/8/8/4k3/8/8/8/4K3 w - - 0 1")) is None)

    # (c) flip_fen is an involution on generated-style positions (no castling/EP by design).
    for fen in ("6k1/5ppp/8/8/8/8/8/R5K1 w - - 0 1",
                "4k3/8/8/8/8/8/8/4K3 w - - 0 1"):
        check(f"flip roundtrip: {fen}", flip_fen(flip_fen(fen)) == fen)
    flip_rejected = False
    try:
        flip_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    except ValueError:
        flip_rejected = True
    check("flip refuses positions with castling/EP rights (asserted, not silently mapped)",
          flip_rejected)

    # (d) The color mirror preserves the tactic (re-proved, not assumed).
    flipped = chess.Board(flip_fen("6k1/5ppp/8/8/8/8/8/R5K1 w - - 0 1"))
    res_flip = classify(flipped)
    check("flip preserves mate_in_1", res_flip is not None and res_flip[0] == "mate_in_1")
    check("flip moves the winner to a8a1",
          res_flip is not None and [m.uci() for m in res_flip[1]] == ["a8a1"])

    # (e) The dedup key excludes exactly the two clock fields.
    b_plain = chess.Board()
    b_clocked = chess.Board()
    b_clocked.halfmove_clock = 17
    b_clocked.fullmove_number = 42
    check("normalize_fen excludes halfmove clock and fullmove number",
          normalize_fen(b_plain) == normalize_fen(b_clocked))
    check("normalize_fen keeps placement + stm + castling + ep (4 fields)",
          len(normalize_fen(b_plain).split()) == 4
          and normalize_fen(b_plain) == " ".join(b_plain.fen().split()[:4]))

    # (f) The generator finds BOTH targets under a fixed seed (integration).
    rng = random.Random(7)
    found: dict[str, bool] = {"mate_in_1": False, "mate_in_2": False}
    for _ in range(12000):
        if all(found.values()):
            break
        for target in ("mate_in_1", "mate_in_2"):
            if found[target]:
                continue
            cand = construct(rng, target)
            if cand is None:
                continue
            r = classify(cand)
            if r is not None and r[0] == target:
                found[target] = True
    check("generator finds mate_in_1", found["mate_in_1"])
    check("generator finds mate_in_2", found["mate_in_2"])

    failed = [name for name, ok in results if not ok]
    print(f"SELFTEST {'PASS' if not failed else 'FAIL'} "
          f"checks={len(results)} failed={len(failed)}")
    return 0 if not failed else 1


# --- CLI ----------------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fu14_suite.py",
        description="F-U14 / FND-0033: independent tactical suite (N=200), "
                    "normalized-FEN overlap gate, hash-pin manifest, engine smoke pass.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="build the suite (deterministic under --seed)")
    g.add_argument("--seed", type=int, default=SEED)
    g.add_argument("--mate-in-1", dest="mate_in_1", type=int, default=N_MATE_IN_1)
    g.add_argument("--mate-in-2", dest="mate_in_2", type=int, default=N_MATE_IN_2)
    g.add_argument("--out", default=str(DEFAULT_SUITE))
    g.set_defaults(func=cmd_generate)

    o = sub.add_parser("overlap", help="normalized-FEN overlap gate vs every corpus; "
                                       "exit 0 iff overlap == 0")
    o.add_argument("--suite", default=str(DEFAULT_SUITE))
    o.add_argument("--out", default=str(DEFAULT_REPORT))
    o.set_defaults(func=cmd_overlap)

    pi = sub.add_parser("pin", help="write the hash-pin manifest")
    pi.add_argument("--suite", default=str(DEFAULT_SUITE))
    pi.add_argument("--report", default=str(DEFAULT_REPORT))
    pi.add_argument("--smoke", default=str(DEFAULT_SMOKE))
    pi.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    pi.set_defaults(func=cmd_pin)

    v = sub.add_parser("verify", help="read-time re-hash + re-prove all 200 positions")
    v.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    v.set_defaults(func=cmd_verify)

    s = sub.add_parser("smoke", help="one raw UCI pass of a binary over the suite")
    s.add_argument("--exe", default="build/Release/kana.exe")
    s.add_argument("--suite", default=str(DEFAULT_SUITE))
    s.add_argument("--out", default=str(DEFAULT_SMOKE))
    s.add_argument("--depth", type=int, default=10)
    s.add_argument("--timeout", type=float, default=60.0)
    s.set_defaults(func=cmd_smoke)

    st = sub.add_parser("selftest", help="fixture checks for proofs, flip and key")
    st.set_defaults(func=cmd_selftest)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
















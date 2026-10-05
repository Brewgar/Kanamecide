#!/usr/bin/env python3
"""E-0013 parameter-table evaluator: the offline scorer, the parameter-table exchange
format, and the paired two-table holdout/inner-val comparison.

Contract this tool implements (read-only citations; none of those records is edited):

  * E-0013 B1 sentence 1 - the arm-differentiation mechanism THIS RECORD actually uses.
    "The two arms of the holdout comparison are two PARAMETER TABLES, not two engines, and
    they are differentiated inside the offline evaluator, which (i) prints `sha256` of the
    fitted parameter table actually loaded for the fitted arm and `sha256` of the
    hand-tuned table actually loaded for the floor arm, (ii) asserts the two hashes DIFFER
    before any holdout loss is computed, and (iii) records both hashes, the two artifact
    paths, and the SHA-256 of the coefficient-regeneration output that produced the
    candidate's coefficient block."  (i) and (ii) are enforced below; a same-hash pair
    aborts before a single loss is read.
  * E-0013 B1 sentence 2 - the evaluation stage is `S* = 6` for BOTH arms, and the floor is
    "the compiled-in table of `src/eval.cpp:174-234` at the pinned `src/` commit". The
    floor table is transcribed literally below from that block, so the same bytes are
    comparable, and its hash is printed like any other arm's.
  * E-0013 B2 sentence 1 - labels are side-to-move framed (`y = white_score` for White to
    move, `1 - white_score` for Black) and the fit target is
    `sigmoid(clip(E_theta(p), -L, L))`.
  * E-0013 B4 sentence 1 - the optimiser is "deterministic full-batch L-BFGS on the mean
    logistic loss"; `tools/e0013_fit.py` imports its loss and gradient from HERE so the
    trainer and the evaluator cannot drift apart.
  * E-0013 B5 sentence 1 - KING PSTs are FROZEN, so they are not in the design vector;
    the 683-scalar layout below asserts that mechanically rather than documenting it.
  * E-0013 F5 - MAE phase-tertile boundaries are tertiles of the phase value over TRAIN
    positions only, rounded to integers, frozen in the pre-fit commit. This tool computes
    them (`--write-tertiles-from`) and consumes them (`--tertiles`); it never derives them
    from a holdout.

Two things this scorer does that a naive port does not, both deliberate:

  1. **Exact integer taper.** `evaluate()` computes
     `sc = (mg*phase + eg*(24-phase)) / GAME_PHASE_MAX` in C++ integer arithmetic, which
     truncates toward zero. `engine_score` reproduces those integers exactly (including
     C-style truncation for negative numerators), so the loss REPORTED for both arms is the
     loss of the score the engine would actually return.
  2. **A continuous surrogate for the gradient.** The integer truncation is not
     differentiable. The optimiser therefore sees `(mg*phase + eg*(24-phase))/24` as a real
     number, and the CLI reports both the exact and the surrogate loss for every position
     set, so the size of the quantisation gap is visible instead of assumed away.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator

import chess

ROOT = Path(__file__).resolve().parent.parent
TABLE_FORMAT = "kana-evalcoeffs-v1"

PIECE_ORDER = ("PAWN", "KNIGHT", "BISHOP", "ROOK", "QUEEN", "KING")
FITTED_PIECES = ("PAWN", "KNIGHT", "BISHOP", "ROOK", "QUEEN")  # KING is frozen (B5 s1)

GAME_PHASE_MAX = 24
FLAT_VALUE = {"PAWN": 100, "KNIGHT": 320, "BISHOP": 330, "ROOK": 500, "QUEEN": 900, "KING": 20000}
PHASE_WEIGHT = {"PAWN": 0, "KNIGHT": 1, "BISHOP": 1, "ROOK": 2, "QUEEN": 4, "KING": 0}

# --- transcribed literals (src/eval.cpp:35, :41-170 at the pinned src/ commit) ---------
PST = {
    ("PAWN", "mg"): (
        (0, 0, 0, 0, 0, 0, 0, 0),
        (50, 50, 50, 50, 50, 50, 50, 50),
        (10, 10, 20, 30, 30, 20, 10, 10),
        (5, 5, 10, 25, 25, 10, 5, 5),
        (0, 0, 0, 20, 20, 0, 0, 0),
        (5, -5, -10, 0, 0, -10, -5, 5),
        (5, 10, 10, -20, -20, 10, 10, 5),
        (0, 0, 0, 0, 0, 0, 0, 0),
    ),
    ("PAWN", "eg"): (
        (0, 0, 0, 0, 0, 0, 0, 0),
        (80, 80, 80, 80, 80, 80, 80, 80),
        (50, 50, 50, 50, 50, 50, 50, 50),
        (30, 30, 30, 30, 30, 30, 30, 30),
        (20, 20, 20, 20, 20, 20, 20, 20),
        (10, 10, 10, 10, 10, 10, 10, 10),
        (0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0),
    ),
    ("KNIGHT", "mg"): (
        (-50, -40, -30, -30, -30, -30, -40, -50),
        (-40, -20, 0, 0, 0, 0, -20, -40),
        (-30, 0, 10, 15, 15, 10, 0, -30),
        (-30, 5, 15, 20, 20, 15, 5, -30),
        (-30, 0, 15, 20, 20, 15, 0, -30),
        (-30, 5, 10, 15, 15, 10, 5, -30),
        (-40, -20, 0, 5, 5, 0, -20, -40),
        (-50, -40, -30, -30, -30, -30, -40, -50),
    ),
    ("KNIGHT", "eg"): (
        (-50, -40, -30, -30, -30, -30, -40, -50),
        (-40, -20, 0, 0, 0, 0, -20, -40),
        (-30, 0, 10, 15, 15, 10, 0, -30),
        (-30, 5, 15, 20, 20, 15, 5, -30),
        (-30, 0, 15, 20, 20, 15, 0, -30),
        (-30, 5, 10, 15, 15, 10, 5, -30),
        (-40, -20, 0, 5, 5, 0, -20, -40),
        (-50, -40, -30, -30, -30, -30, -40, -50),
    ),
    ("BISHOP", "mg"): (
        (-20, -10, -10, -10, -10, -10, -10, -20),
        (-10, 0, 0, 0, 0, 0, 0, -10),
        (-10, 0, 5, 10, 10, 5, 0, -10),
        (-10, 5, 5, 10, 10, 5, 5, -10),
        (-10, 0, 10, 10, 10, 10, 0, -10),
        (-10, 10, 10, 10, 10, 10, 10, -10),
        (-10, 5, 0, 0, 0, 0, 5, -10),
        (-20, -10, -10, -10, -10, -10, -10, -20),
    ),
    ("BISHOP", "eg"): (
        (-20, -10, -10, -10, -10, -10, -10, -20),
        (-10, 0, 0, 0, 0, 0, 0, -10),
        (-10, 0, 5, 10, 10, 5, 0, -10),
        (-10, 5, 5, 10, 10, 5, 5, -10),
        (-10, 0, 10, 10, 10, 10, 0, -10),
        (-10, 10, 10, 10, 10, 10, 10, -10),
        (-10, 5, 0, 0, 0, 0, 5, -10),
        (-20, -10, -10, -10, -10, -10, -10, -20),
    ),
    ("ROOK", "mg"): (
        (0, 0, 0, 0, 0, 0, 0, 0),
        (5, 10, 10, 10, 10, 10, 10, 5),
        (-5, 0, 0, 0, 0, 0, 0, -5),
        (-5, 0, 0, 0, 0, 0, 0, -5),
        (-5, 0, 0, 0, 0, 0, 0, -5),
        (-5, 0, 0, 0, 0, 0, 0, -5),
        (-5, 0, 0, 0, 0, 0, 0, -5),
        (0, 0, 0, 5, 5, 0, 0, 0),
    ),
    ("ROOK", "eg"): (
        (0, 0, 0, 0, 0, 0, 0, 0),
        (5, 10, 10, 10, 10, 10, 10, 5),
        (-5, 0, 0, 0, 0, 0, 0, -5),
        (-5, 0, 0, 0, 0, 0, 0, -5),
        (-5, 0, 0, 0, 0, 0, 0, -5),
        (-5, 0, 0, 0, 0, 0, 0, -5),
        (-5, 0, 0, 0, 0, 0, 0, -5),
        (0, 0, 0, 5, 5, 0, 0, 0),
    ),
    ("QUEEN", "mg"): (
        (-20, -10, -10, -5, -5, -10, -10, -20),
        (-10, 0, 0, 0, 0, 0, 0, -10),
        (-10, 0, 5, 5, 5, 5, 0, -10),
        (-5, 0, 5, 5, 5, 5, 0, -5),
        (0, 0, 5, 5, 5, 5, 0, -5),
        (-10, 5, 5, 5, 5, 5, 0, -10),
        (-10, 0, 5, 0, 0, 0, 0, -10),
        (-20, -10, -10, -5, -5, -10, -10, -20),
    ),
    ("QUEEN", "eg"): (
        (-20, -10, -10, -5, -5, -10, -10, -20),
        (-10, 0, 0, 0, 0, 0, 0, -10),
        (-10, 0, 5, 5, 5, 5, 0, -10),
        (-5, 0, 5, 5, 5, 5, 0, -5),
        (0, 0, 5, 5, 5, 5, 0, -5),
        (-10, 5, 5, 5, 5, 5, 0, -10),
        (-10, 0, 5, 0, 0, 0, 0, -10),
        (-20, -10, -10, -5, -5, -10, -10, -20),
    ),
    ("KING", "mg"): (
        (-30, -40, -40, -50, -50, -40, -40, -30),
        (-30, -40, -40, -50, -50, -40, -40, -30),
        (-30, -40, -40, -50, -50, -40, -40, -30),
        (-30, -40, -40, -50, -50, -40, -40, -30),
        (-20, -30, -30, -40, -40, -30, -30, -20),
        (-10, -20, -20, -20, -20, -20, -20, -10),
        (20, 20, 0, 0, 0, 0, 20, 20),
        (20, 30, 10, 0, 0, 10, 30, 20),
    ),
    ("KING", "eg"): (
        (-50, -40, -30, -20, -20, -30, -40, -50),
        (-30, -20, -10, 0, 0, -10, -20, -30),
        (-30, -10, 20, 30, 30, 20, -10, -30),
        (-30, -10, 30, 40, 40, 30, -10, -30),
        (-30, -10, 30, 40, 40, 30, -10, -30),
        (-30, -10, 20, 30, 30, 20, -10, -30),
        (-30, -30, 0, 0, 0, 0, -30, -30),
        (-50, -30, -30, -30, -30, -30, -30, -50),
    ),
}

CENTER_DIST = (
    (6, 5, 4, 3, 3, 4, 5, 6),
    (5, 4, 3, 2, 2, 3, 4, 5),
    (4, 3, 2, 1, 1, 2, 3, 4),
    (3, 2, 1, 0, 0, 1, 2, 3),
    (3, 2, 1, 0, 0, 1, 2, 3),
    (4, 3, 2, 1, 1, 2, 3, 4),
    (5, 4, 3, 2, 2, 3, 4, 5),
    (6, 5, 4, 3, 3, 4, 5, 6),
)


def _flat(table: tuple[tuple[int, ...], ...]) -> list[int]:
    return [v for row in table for v in row]


# --- parameter table ------------------------------------------------------------------

SCALAR_INT_FIELDS = (
    "doubled_pawn_mg", "doubled_pawn_eg", "isolated_pawn_mg", "isolated_pawn_eg",
    "mobility_mg", "mobility_eg",
    "bishop_pair_mg", "bishop_pair_eg",
    "open_file_mg", "open_file_eg",
    "semi_open_file_mg", "semi_open_file_eg",
    "seventh_rank_mg", "seventh_rank_eg",
    "king_shield_mg", "king_center_eg",
    "tempo",
)


@dataclass
class ParamTable:
    """All named, tuneable coefficients - the same set `EvalCoeffs` declares in
    `src/eval.h`, in a form that can be hashed, diffed and substituted into the eval
    translation unit by the existing E-0010 coefficient-regeneration mechanism."""

    mg_value: dict[str, int]
    eg_value: dict[str, int]
    mg_pst: dict[str, list[int]]
    eg_pst: dict[str, list[int]]
    scalars: dict[str, int]
    passed_pawn_mg: list[int]
    passed_pawn_eg: list[int]
    source: str = "unknown"

    def __post_init__(self) -> None:
        for field_name in ("mg_pst", "eg_pst"):
            tables = getattr(self, field_name)
            if set(tables) != set(PIECE_ORDER):
                raise ValueError(f"{field_name} must carry all six piece tables")
            for piece, values in tables.items():
                if len(values) != 64:
                    raise ValueError(f"{field_name}[{piece}] has {len(values)} entries, not 64")
        if set(self.mg_value) != set(PIECE_ORDER) or set(self.eg_value) != set(PIECE_ORDER):
            raise ValueError("mg_value/eg_value must carry all six piece types")
        if len(self.passed_pawn_mg) != 8 or len(self.passed_pawn_eg) != 8:
            raise ValueError("passed_pawn_* must carry one entry per rank (0..7)")
        missing = [k for k in SCALAR_INT_FIELDS if k not in self.scalars]
        if missing:
            raise ValueError(f"scalars missing {missing}")


def to_json(table: ParamTable) -> dict[str, Any]:
    return {
        "format": TABLE_FORMAT,
        "source": table.source,
        "mg_value": dict(table.mg_value),
        "eg_value": dict(table.eg_value),
        "mg_pst": {p: list(table.mg_pst[p]) for p in PIECE_ORDER},
        "eg_pst": {p: list(table.eg_pst[p]) for p in PIECE_ORDER},
        "scalars": dict(table.scalars),
        "passed_pawn_mg": list(table.passed_pawn_mg),
        "passed_pawn_eg": list(table.passed_pawn_eg),
    }


def from_json(obj: dict[str, Any]) -> ParamTable:
    if obj.get("format") != TABLE_FORMAT:
        raise ValueError(f"table format {obj.get('format')!r} != {TABLE_FORMAT!r}")
    return ParamTable(
        mg_value={p: int(obj["mg_value"][p]) for p in PIECE_ORDER},
        eg_value={p: int(obj["eg_value"][p]) for p in PIECE_ORDER},
        mg_pst={p: [int(v) for v in obj["mg_pst"][p]] for p in PIECE_ORDER},
        eg_pst={p: [int(v) for v in obj["eg_pst"][p]] for p in PIECE_ORDER},
        scalars={k: int(obj["scalars"][k]) for k in SCALAR_INT_FIELDS},
        passed_pawn_mg=[int(v) for v in obj["passed_pawn_mg"]],
        passed_pawn_eg=[int(v) for v in obj["passed_pawn_eg"]],
        source=str(obj.get("source", "unknown")),
    )


def table_bytes(table: ParamTable) -> bytes:
    """The one serialization E-0013 B1 (i) hashes. Two people who follow this line get the
    same 64 hex characters; a table that differs anywhere hashes differently."""
    return (json.dumps(to_json(table), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
            + "\n").encode("utf-8")


def table_sha256(table: ParamTable) -> str:
    return hashlib.sha256(table_bytes(table)).hexdigest()


# --- the 683 free scalars (E-0013 "Free-parameter set", B5 sentence 1) ----------------
# Fitted: items 1 and 3-6 of the free-parameter list, with the KING PSTs FROZEN and the
# KING material entries fixed at 20000/20000. The layout IS the contract: the assert below
# fails at import if anyone changes the scope, which is what makes "nothing else may move"
# a property of the code rather than a sentence in a record.
DESIGN_LAYOUT: tuple[tuple[str, int], ...] = (
    ("mg_value[PAWN,KNIGHT,BISHOP,ROOK,QUEEN]", 5),
    ("eg_value[PAWN,KNIGHT,BISHOP,ROOK,QUEEN]", 5),
    ("mg_pst[PAWN,KNIGHT,BISHOP,ROOK,QUEEN][64]", 320),
    ("eg_pst[PAWN,KNIGHT,BISHOP,ROOK,QUEEN][64]", 320),
    ("doubled_pawn_mg, doubled_pawn_eg, isolated_pawn_mg, isolated_pawn_eg", 4),
    ("passed_pawn_mg[0..7]", 8),
    ("passed_pawn_eg[0..7]", 8),
    ("mobility_mg, mobility_eg", 2),
    ("bishop_pair_mg, bishop_pair_eg", 2),
    ("open_file_mg, open_file_eg", 2),
    ("semi_open_file_mg, semi_open_file_eg", 2),
    ("seventh_rank_mg, seventh_rank_eg", 2),
    ("king_shield_mg", 1),
    ("king_center_eg", 1),
    ("tempo", 1),
)
N_FREE = 683
if sum(n for _, n in DESIGN_LAYOUT) != N_FREE:  # import-time; not a test, a precondition
    raise AssertionError(f"design layout sums to {sum(n for _, n in DESIGN_LAYOUT)}, not {N_FREE}")
if any("KING" in name for name, _ in DESIGN_LAYOUT):  # B5 sentence 1, mechanically
    raise AssertionError("the KING PSTs are FROZEN; no KING entry may enter the fitted set")


def pst_row(piece: str, phase: str, square: int) -> int:
    """`C.mg_pst[pt][s]` / `C.eg_pst[pt][s]` for the hand-tuned table."""
    return PST[(piece, phase)][square >> 3][square & 7]


def hand_tuned() -> ParamTable:
    """The floor arm: `src/eval.cpp:174-234` (`eval_init`) at the pinned `src/` commit.

    Transcribed literally, because E-00014's same-floor discipline requires the floor here
    and the floor of the holdout comparison to be the same bytes - a table re-derived by
    some other route is not the same floor, and its hash will say so.
    """
    return ParamTable(
        mg_value={"PAWN": 82, "KNIGHT": 337, "BISHOP": 365, "ROOK": 477, "QUEEN": 1025, "KING": 20000},
        eg_value={"PAWN": 94, "KNIGHT": 281, "BISHOP": 297, "ROOK": 512, "QUEEN": 936, "KING": 20000},
        mg_pst={p: _flat(PST[(p, "mg")]) for p in PIECE_ORDER},
        eg_pst={p: _flat(PST[(p, "eg")]) for p in PIECE_ORDER},
        scalars={
            "doubled_pawn_mg": -10, "doubled_pawn_eg": -20,
            "isolated_pawn_mg": -10, "isolated_pawn_eg": -15,
            "mobility_mg": 1, "mobility_eg": 1,
            "bishop_pair_mg": 30, "bishop_pair_eg": 50,
            "open_file_mg": 15, "open_file_eg": 10,
            "semi_open_file_mg": 8, "semi_open_file_eg": 5,
            "seventh_rank_mg": 10, "seventh_rank_eg": 20,
            "king_shield_mg": 5, "king_center_eg": 10,
            "tempo": 10,
        },
        passed_pawn_mg=[0, 5, 10, 20, 35, 55, 80, 0],
        passed_pawn_eg=[0, 10, 20, 35, 55, 80, 120, 0],
        source="hand-tuned (src/eval.cpp:174-234 at the pinned src/ commit)",
    )


def design_vector(table: ParamTable) -> list[int]:
    """Flatten the FITTED set - exactly the 683 scalars of `DESIGN_LAYOUT` - to a vector.

    The KING material and KING PST entries are deliberately absent: they are frozen, so
    they are not parameters, and a vector that carried them would be describing a
    different, wider experiment than the one E-0013 pre-registered.
    """
    vec: list[int] = []
    vec += [table.mg_value[p] for p in FITTED_PIECES]
    vec += [table.eg_value[p] for p in FITTED_PIECES]
    for p in FITTED_PIECES:
        vec += list(table.mg_pst[p])
    for p in FITTED_PIECES:
        vec += list(table.eg_pst[p])
    vec += [table.scalars[k] for k in ("doubled_pawn_mg", "doubled_pawn_eg",
                                       "isolated_pawn_mg", "isolated_pawn_eg")]
    vec += list(table.passed_pawn_mg)
    vec += list(table.passed_pawn_eg)
    vec += [table.scalars[k] for k in ("mobility_mg", "mobility_eg",
                                       "bishop_pair_mg", "bishop_pair_eg",
                                       "open_file_mg", "open_file_eg",
                                       "semi_open_file_mg", "semi_open_file_eg",
                                       "seventh_rank_mg", "seventh_rank_eg",
                                       "king_shield_mg", "king_center_eg",
                                       "tempo")]
    if len(vec) != N_FREE:
        raise AssertionError(f"design_vector produced {len(vec)} entries, not {N_FREE}")
    return vec


# --- scoring core (a faithful port of src/eval.cpp:241-358) ---------------------------

def trunc_div(a: int, b: int) -> int:
    """C++ `/` on integers truncates toward ZERO; Python `//` floors. The engine's taper is
    `(mg*phase + eg*(24-phase)) / GAME_PHASE_MAX` in C++, so a negative numerator divides
    differently under the two rules and a naive port silently mis-scores every position
    where the tapered numerator is negative."""
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


def popcount(x: int) -> int:
    return int(x).bit_count()


FILE_MASK = [sum(1 << (r * 8 + f) for r in range(8)) for f in range(8)]
ADJ_FILE_MASK = [
    FILE_MASK[f] | (FILE_MASK[f - 1] if f > 0 else 0) | (FILE_MASK[f + 1] if f < 7 else 0)
    for f in range(8)
]
# adjacency without the file itself, which is how src/eval.cpp:277-282 isolates a pawn
ADJACENT_ONLY = [ADJ_FILE_MASK[f] ^ FILE_MASK[f] for f in range(8)]
RANK7_MASK = 0xFF << 48
RANK2_MASK = 0xFF << 8

PIECE_NAME = {
    chess.PAWN: "PAWN", chess.KNIGHT: "KNIGHT", chess.BISHOP: "BISHOP",
    chess.ROOK: "ROOK", chess.QUEEN: "QUEEN", chess.KING: "KING",
}

# passed_mask[color][sq] and shelter_mask[color][sq], exactly as src/eval.cpp:216-234
# builds them: ranks above (White) / below (Black) for passed pawns, and the one rank in
# front of the king for the shelter, files f-1..f+1 clamped.
PASSED_MASK: dict[int, list[int]] = {chess.WHITE: [0] * 64, chess.BLACK: [0] * 64}
SHELTER_MASK: dict[int, list[int]] = {chess.WHITE: [0] * 64, chess.BLACK: [0] * 64}
for _sq in range(64):
    _f, _r = _sq & 7, _sq >> 3
    _above = sum(1 << (i * 8 + j) for i in range(_r + 1, 8) for j in range(8))
    _below = sum(1 << (i * 8 + j) for i in range(0, _r) for j in range(8))
    PASSED_MASK[chess.WHITE][_sq] = ADJ_FILE_MASK[_f] & _above
    PASSED_MASK[chess.BLACK][_sq] = ADJ_FILE_MASK[_f] & _below
    _fl, _fr = max(0, _f - 1), min(7, _f + 1)
    SHELTER_MASK[chess.WHITE][_sq] = sum(
        1 << ((_r + 1) * 8 + ff) for ff in range(_fl, _fr + 1) if _r + 1 < 8)
    SHELTER_MASK[chess.BLACK][_sq] = sum(
        1 << ((_r - 1) * 8 + ff) for ff in range(_fl, _fr + 1) if _r - 1 >= 0)


def mirror_sq(sq: int) -> int:
    return sq ^ 56


def phase_of(board: chess.Board) -> int:
    """`phase = min(1*N + 1*B + 2*R + 4*Q, 24)` over BOTH sides. The weights are frozen
    integers and the formula itself is not fitted (E-0013 "Free-parameter set")."""
    phase = 0
    for piece, weight in PHASE_WEIGHT.items():
        if weight:
            pt = chess.PAWN + PIECE_ORDER.index(piece)
            phase += weight * (len(board.pieces(pt, chess.WHITE)) + len(board.pieces(pt, chess.BLACK)))
    return min(phase, GAME_PHASE_MAX)


def _piece_type(name: str) -> int:
    return chess.PAWN + PIECE_ORDER.index(name)


def _pawn_attack_bb(board: chess.Board, color: chess.Color) -> int:
    out = 0
    for sq in board.pieces(chess.PAWN, color):
        out |= chess.BB_PAWN_ATTACKS[color][sq]
    return out


def _slot_index() -> dict[tuple, int]:
    """Slot offsets of the 683 design vector, asserted against `DESIGN_LAYOUT`."""
    off: dict[tuple, int] = {}
    i = 0
    for p in FITTED_PIECES:
        off[("mg_value", p)] = i
        i += 1
    for p in FITTED_PIECES:
        off[("eg_value", p)] = i
        i += 1
    for p in FITTED_PIECES:
        for sq in range(64):
            off[("mg_pst", p, sq)] = i
            i += 1
    for p in FITTED_PIECES:
        for sq in range(64):
            off[("eg_pst", p, sq)] = i
            i += 1
    for k in ("doubled_pawn_mg", "doubled_pawn_eg", "isolated_pawn_mg", "isolated_pawn_eg"):
        off[("scalar", k)] = i
        i += 1
    for r in range(8):
        off[("passed_pawn_mg", r)] = i
        i += 1
    for r in range(8):
        off[("passed_pawn_eg", r)] = i
        i += 1
    for k in ("mobility_mg", "mobility_eg", "bishop_pair_mg", "bishop_pair_eg",
              "open_file_mg", "open_file_eg", "semi_open_file_mg", "semi_open_file_eg",
              "seventh_rank_mg", "seventh_rank_eg", "king_shield_mg", "king_center_eg",
              "tempo"):
        off[("scalar", k)] = i
        i += 1
    if i != N_FREE:
        raise AssertionError(f"slot index totals {i}, not {N_FREE}")
    return off


SLOT = _slot_index()


@dataclass
class Terms:
    """A position's exact linear decomposition.

    `mg_counts`/`eg_counts` map a design slot to `[full, half]`: how many times the slot
    enters with its full coefficient, and how many times with the engine's integer-halved
    one (`C.open_file_mg/2` and the three sibling sites). Everything else in `evaluate()`
    is a unit or integer multiple of one coefficient, so this pair of counts reproduces
    the mg/eg accumulators exactly. `c_mg`/`c_eg` carry the FROZEN KING PST contribution,
    which is why the two arms of the comparison differ only where they are supposed to.
    """

    phase: int
    mg_counts: dict[int, list[int]] = field(default_factory=dict)
    eg_counts: dict[int, list[int]] = field(default_factory=dict)
    c_mg: int = 0
    c_eg: int = 0
    sign: int = 1
    """`+1` if White is to move, `-1` if Black, because `evaluate()` returns
    `sign * taper_white + tempo` (src/eval.cpp:351-357): the taper is flipped into the
    mover's frame and the tempo bonus is added once, unsigned. Deriving this from the
    source rather than assuming "the eval is white-relative" is what keeps the fit target
    (E-0013 B2's side-to-move frame) and the predictor in the same frame."""

    def accumulators(self, vector: list[float] | list[int]) -> tuple[float, float, int, int]:
        """(mg_surrogate, eg_surrogate, mg_exact, eg_exact) for a design vector."""
        mg_f = float(self.c_mg)
        eg_f = float(self.c_eg)
        mg_x = self.c_mg
        eg_x = self.c_eg
        for slot, (full, half) in self.mg_counts.items():
            theta = vector[slot]
            mg_f += full * theta + half * (theta / 2.0)
            mg_x += full * int(theta) + half * trunc_div(int(theta), 2)
        for slot, (full, half) in self.eg_counts.items():
            theta = vector[slot]
            eg_f += full * theta + half * (theta / 2.0)
            eg_x += full * int(theta) + half * trunc_div(int(theta), 2)
        return mg_f, eg_f, mg_x, eg_x


def from_design_vector(vec: Iterable[float], template: ParamTable) -> ParamTable:
    """Inverse of `design_vector`, with the frozen KING entries taken from `template`.

    `template` is the pre-fit floor, so the frozen block is identical on both arms by
    construction rather than by coincidence.
    """
    values = [int(round(v)) for v in vec]
    if len(values) != N_FREE:
        raise AssertionError(f"vector has {len(values)} entries, not {N_FREE}")
    i = 0

    def take(n: int) -> list[int]:
        nonlocal i
        block = values[i:i + n]
        i += n
        return block

    mg_value = dict(template.mg_value)
    eg_value = dict(template.eg_value)
    for p, v in zip(FITTED_PIECES, take(len(FITTED_PIECES))):
        mg_value[p] = v
    for p, v in zip(FITTED_PIECES, take(len(FITTED_PIECES))):
        eg_value[p] = v

    mg_pst = {p: list(template.mg_pst[p]) for p in PIECE_ORDER}
    eg_pst = {p: list(template.eg_pst[p]) for p in PIECE_ORDER}
    for p in FITTED_PIECES:
        mg_pst[p] = take(64)
    for p in FITTED_PIECES:
        eg_pst[p] = take(64)

    scalars = dict(template.scalars)
    keys = ("doubled_pawn_mg", "doubled_pawn_eg", "isolated_pawn_mg", "isolated_pawn_eg")
    for k, v in zip(keys, take(len(keys))):
        scalars[k] = v
    passed_pawn_mg = take(8)
    passed_pawn_eg = take(8)
    keys = ("mobility_mg", "mobility_eg", "bishop_pair_mg", "bishop_pair_eg",
            "open_file_mg", "open_file_eg", "semi_open_file_mg", "semi_open_file_eg",
            "seventh_rank_mg", "seventh_rank_eg", "king_shield_mg", "king_center_eg",
            "tempo")
    for k, v in zip(keys, take(len(keys))):
        scalars[k] = v
    assert i == N_FREE, i
    return ParamTable(mg_value=mg_value, eg_value=eg_value, mg_pst=mg_pst, eg_pst=eg_pst,
                      scalars=scalars, passed_pawn_mg=passed_pawn_mg,
                      passed_pawn_eg=passed_pawn_eg, source="fitted (E-0013)")
def _bits(x: int) -> Iterator[int]:
    while x:
        lsb = x & -x
        yield lsb.bit_length() - 1
        x ^= lsb


def _bump(d: dict[int, list[int]], slot: int, full: int = 0, half: int = 0) -> None:
    entry = d.setdefault(slot, [0, 0])
    entry[0] += full
    entry[1] += half


def _mobility(board: chess.Board, color: chess.Color) -> int:
    """`popcount(wmob)` from src/eval.cpp:296-309: the union of the side's N/B/R/Q attack
    sets, minus its own occupancy, minus the ENEMY PAWN attack set."""
    other = chess.BLACK if color == chess.WHITE else chess.WHITE
    mob = 0
    for pt in (chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
        for sq in board.pieces(pt, color):
            mob |= board.attacks(sq).mask
    mob &= ~board.occupied_co[color]
    mob &= ~_pawn_attack_bb(board, other)
    return popcount(mob)


def position_terms(board: chess.Board, stage: int = 6) -> Terms:
    """Walk a position once and record, per design slot, how many times its coefficient
    enters the mg and eg accumulators - with the frozen KING PST contribution kept apart.

    Stage gates mirror `evaluate()` exactly: PSTs at >=2, pawn structure at >=3, mobility at
    >=4, the positional block at >=5, tempo at >=6. `tempo` is deliberately NOT a term here:
    the engine adds it after the taper (src/eval.cpp:356), so the callers apply it.
    """
    if stage < 1:
        raise ValueError("position_terms describes stages >= 1; stage 0 is flat material")
    terms = Terms(phase=phase_of(board), sign=1 if board.turn == chess.WHITE else -1)
    mg, eg = terms.mg_counts, terms.eg_counts

    # material - PAWN..QUEEN only; the KING entries are never read above stage 0
    for name in FITTED_PIECES:
        pt = _piece_type(name)
        d = len(board.pieces(pt, chess.WHITE)) - len(board.pieces(pt, chess.BLACK))
        if d:
            _bump(mg, SLOT[("mg_value", name)], full=d)
            _bump(eg, SLOT[("eg_value", name)], full=d)

    # PSTs (indexed from White's perspective; Black uses mirror_sq and a minus sign)
    if stage >= 2:
        for sq, piece in board.piece_map().items():
            name = PIECE_NAME[piece.piece_type]
            if piece.color == chess.WHITE:
                sign, target = 1, sq
            else:
                sign, target = -1, mirror_sq(sq)
            if name == "KING":
                terms.c_mg += sign * pst_row("KING", "mg", target)
                terms.c_eg += sign * pst_row("KING", "eg", target)
            else:
                _bump(mg, SLOT[("mg_pst", name, target)], full=sign)
                _bump(eg, SLOT[("eg_pst", name, target)], full=sign)

    wp = board.pieces(chess.PAWN, chess.WHITE).mask
    bp = board.pieces(chess.PAWN, chess.BLACK).mask

    if stage >= 3:
        for f in range(8):
            fm = FILE_MASK[f]
            wc, bc = popcount(wp & fm), popcount(bp & fm)
            if wc >= 2:
                _bump(mg, SLOT[("scalar", "doubled_pawn_mg")], full=wc - 1)
                _bump(eg, SLOT[("scalar", "doubled_pawn_eg")], full=wc - 1)
            if bc >= 2:
                _bump(mg, SLOT[("scalar", "doubled_pawn_mg")], full=-(bc - 1))
                _bump(eg, SLOT[("scalar", "doubled_pawn_eg")], full=-(bc - 1))
            if (wp & fm) and not (wp & ADJACENT_ONLY[f]):
                _bump(mg, SLOT[("scalar", "isolated_pawn_mg")], full=wc)
                _bump(eg, SLOT[("scalar", "isolated_pawn_eg")], full=wc)
            if (bp & fm) and not (bp & ADJACENT_ONLY[f]):
                _bump(mg, SLOT[("scalar", "isolated_pawn_mg")], full=-bc)
                _bump(eg, SLOT[("scalar", "isolated_pawn_eg")], full=-bc)
        for sq in _bits(wp):
            if not (bp & PASSED_MASK[chess.WHITE][sq]):
                _bump(mg, SLOT[("passed_pawn_mg", sq >> 3)], full=1)
                _bump(eg, SLOT[("passed_pawn_eg", sq >> 3)], full=1)
        for sq in _bits(bp):
            if not (wp & PASSED_MASK[chess.BLACK][sq]):
                _bump(mg, SLOT[("passed_pawn_mg", 7 - (sq >> 3))], full=-1)
                _bump(eg, SLOT[("passed_pawn_eg", 7 - (sq >> 3))], full=-1)

    if stage >= 4:
        d = _mobility(board, chess.WHITE) - _mobility(board, chess.BLACK)
        if d:
            _bump(mg, SLOT[("scalar", "mobility_mg")], full=d)
            _bump(eg, SLOT[("scalar", "mobility_eg")], full=d)

    if stage >= 5:
        if len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2:
            _bump(mg, SLOT[("scalar", "bishop_pair_mg")], full=1)
            _bump(eg, SLOT[("scalar", "bishop_pair_eg")], full=1)
        if len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2:
            _bump(mg, SLOT[("scalar", "bishop_pair_mg")], full=-1)
            _bump(eg, SLOT[("scalar", "bishop_pair_eg")], full=-1)

        rook_w = board.pieces(chess.ROOK, chess.WHITE).mask
        rook_b = board.pieces(chess.ROOK, chess.BLACK).mask
        queen_w = board.pieces(chess.QUEEN, chess.WHITE).mask
        queen_b = board.pieces(chess.QUEEN, chess.BLACK).mask
        # The queen sites use `C.open_file_mg/2` in C++ - integer halving of the COEFFICIENT,
        # which is why they are carried as `half` counts and reconstructed with trunc_div
        # instead of being folded into the coefficient as a 0.5 multiple.
        for f in range(8):
            fm = FILE_MASK[f]
            wp_, bp_ = bool(wp & fm), bool(bp & fm)
            if not wp_ and not bp_:
                sites = ((rook_w, "open_file", 1, 0), (queen_w, "open_file", 0, 1),
                         (rook_b, "open_file", -1, 0), (queen_b, "open_file", 0, -1))
            elif not wp_ and bp_:
                sites = ((rook_w, "semi_open_file", 1, 0), (queen_w, "semi_open_file", 0, 1))
            elif wp_ and not bp_:
                sites = ((rook_b, "semi_open_file", -1, 0), (queen_b, "semi_open_file", 0, -1))
            else:
                continue
            for bb, key, full, half in sites:
                if bb & fm:
                    _bump(mg, SLOT[("scalar", key + "_mg")], full=full, half=half)
                    _bump(eg, SLOT[("scalar", key + "_eg")], full=full, half=half)

        seventh = ((rook_w, RANK7_MASK, 1), (queen_w, RANK7_MASK, 1),
                   (rook_b, RANK2_MASK, -1), (queen_b, RANK2_MASK, -1))
        for bb, mask, sign in seventh:
            if bb & mask:
                _bump(mg, SLOT[("scalar", "seventh_rank_mg")], full=sign)
                _bump(eg, SLOT[("scalar", "seventh_rank_eg")], full=sign)

        wk, bk = board.king(chess.WHITE), board.king(chess.BLACK)
        if wk is None or bk is None:
            raise ValueError("a position without both kings is not a chess position")
        ws = popcount(wp & SHELTER_MASK[chess.WHITE][wk])
        bs = popcount(bp & SHELTER_MASK[chess.BLACK][bk])
        if ws:
            _bump(mg, SLOT[("scalar", "king_shield_mg")], full=ws)
        if bs:
            _bump(mg, SLOT[("scalar", "king_shield_mg")], full=-bs)

        mbk = mirror_sq(bk)
        _bump(eg, SLOT[("scalar", "king_center_eg")],
              full=(6 - CENTER_DIST[wk >> 3][wk & 7]) - (6 - CENTER_DIST[mbk >> 3][mbk & 7]))

    return terms
# --- score, loss and gradient ---------------------------------------------------------

def exact_stm_score(terms: Terms, vector: list[int] | list[float], tempo: int) -> int:
    """The score the ENGINE returns for this position, in centipawns, from the side to move.

    Built from the same `Terms` the optimiser uses, with the integer truncation and the
    coefficient halving applied exactly, so the reported loss is the loss of the score the
    engine would actually return rather than of a nearby real number.
    """
    _, _, mg, eg = terms.accumulators(vector)
    return terms.sign * trunc_div(mg * terms.phase + eg * (GAME_PHASE_MAX - terms.phase),
                                  GAME_PHASE_MAX) + tempo


def surrogate_stm_score(terms: Terms, vector: list[int] | list[float], tempo: float) -> float:
    """`exact_stm_score` with the two integer quantisations removed: the continuous score the
    optimiser sees. Its difference from `exact_stm_score` is at most 1 cp plus the
    coefficient-halving remainder, on both arms, and it is reported so the gap is visible."""
    mg, eg, _, _ = terms.accumulators(vector)
    return (terms.sign * (mg * terms.phase + eg * (GAME_PHASE_MAX - terms.phase))
            / GAME_PHASE_MAX + tempo)


def engine_score(board: chess.Board, table: ParamTable, stage: int = 6) -> int:
    """`evaluate(b)` from `src/eval.cpp`, in centipawns, from the side to move.

    Stage 0 is the flat-material baseline; stages >= 1 are the tapered path. `S* = 6` for
    both arms of E-0013's comparison (B1 sentence 2).
    """
    if stage == 0:
        sc = 0
        for name in PIECE_ORDER:
            pt = _piece_type(name)
            sc += FLAT_VALUE[name] * (len(board.pieces(pt, chess.WHITE))
                                      - len(board.pieces(pt, chess.BLACK)))
        return sc if board.turn == chess.WHITE else -sc
    terms = position_terms(board, stage)
    return exact_stm_score(terms, design_vector(table),
                           table.scalars["tempo"] if stage >= 6 else 0)


def sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    z = math.exp(x)
    return z / (1.0 + z)


def logistic_loss(t: float, y: float) -> float:
    """`-y ln sigma(t) - (1-y) ln(1 - sigma(t))`, in the numerically stable form."""
    return math.log1p(math.exp(-abs(t))) - y * t + max(t, 0.0)


def clip_value(e: float, clip: float) -> float:
    """`clip(E, -L, L)`. `L` is one of the fields the pre-fit commit pins; there is no
    default and no scale constant here, because the record pins the FORM
    `sigmoid(clip(E_theta(p), -L, L))` and nothing else."""
    if clip <= 0:
        raise ValueError("clip bound L must be positive")
    return max(-clip, min(clip, e))


def design_rows(terms_list: list[Terms]) -> tuple[Any, Any]:
    """`(J, K)` with `E_surrogate = J @ theta + K`.

    `J[i]` is `dE_i/dtheta` over all 683 slots (the tempo column is exactly 1 for every
    position, because the tempo bonus is added once and unsigned) and `K[i]` is the frozen
    KING-PST contribution carried through the taper. Building it once and reusing it for
    every L-BFGS iteration is what makes a full-batch fit tractable; the self-test asserts
    that this matrix reproduces `surrogate_stm_score` slot for slot.
    """
    import numpy as np
    import scipy.sparse as sparse

    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []
    offset = np.zeros(len(terms_list), dtype=np.float64)
    tempo_slot = SLOT[("scalar", "tempo")]
    for i, terms in enumerate(terms_list):
        w_mg = terms.phase / GAME_PHASE_MAX
        w_eg = (GAME_PHASE_MAX - terms.phase) / GAME_PHASE_MAX
        acc: dict[int, float] = {}
        for slot, (full, half) in terms.mg_counts.items():
            acc[slot] = acc.get(slot, 0.0) + w_mg * (full + 0.5 * half)
        for slot, (full, half) in terms.eg_counts.items():
            acc[slot] = acc.get(slot, 0.0) + w_eg * (full + 0.5 * half)
        for slot, value in acc.items():
            rows.append(i)
            cols.append(slot)
            data.append(terms.sign * value)
        rows.append(i)
        cols.append(tempo_slot)
        data.append(1.0)
        offset[i] = terms.sign * (terms.c_mg * terms.phase
                                  + terms.c_eg * (GAME_PHASE_MAX - terms.phase)) / GAME_PHASE_MAX
    jac = sparse.csr_matrix((data, (rows, cols)), shape=(len(terms_list), N_FREE))
    return jac, offset


def loss_and_gradient(jac: Any, offset: Any, labels: Any, vector: Any, clip: float,
                      l2: float, theta0: Any) -> tuple[float, Any]:
    """`(loss, gradient)` for one full-batch step.

    The objective is the pre-registered one: the MEAN logistic loss of
    `sigmoid(clip(E, -L, L))` against the side-to-move-frame target.

    The L2 penalty is `l2 * ||theta - theta0||^2` - the SUM over parameters of the squared
    deviation from the INITIAL point, which is the frozen hand-tuned floor and the ridge
    convention. The convention is stated in the code because `l2` is a number the pre-fit
    commit pins and its magnitude only means anything relative to the convention: under a
    mean-based penalty the same number would be 683 times weaker. The gradient is analytic
    (the self-test checks it against finite differences).
    """
    import numpy as np

    raw = np.asarray(jac @ vector).ravel() + offset
    e = np.clip(raw, -clip, clip)
    q = 1.0 / (1.0 + np.exp(-e))
    loss = float(np.mean(np.log1p(np.exp(-np.abs(e))) - labels * e + np.maximum(e, 0.0)))
    loss += l2 * float(np.sum((vector - theta0) ** 2))

    inside = (np.abs(raw) <= clip).astype(np.float64)
    c = (q - labels) * inside
    grad = np.asarray(jac.T @ c).ravel() / len(labels)
    grad += 2.0 * l2 * (vector - theta0)
    return loss, grad


def mean_logistic_loss(jac: Any, offset: Any, vector: Any, labels: Any, clip: float) -> float:
    """The loss term on its own, without the L2 penalty (used for reporting)."""
    import numpy as np

    e = np.clip(np.asarray(jac @ vector).ravel() + offset, -clip, clip)
    return float(np.mean(np.log1p(np.exp(-np.abs(e))) - labels * e + np.maximum(e, 0.0)))


# --- B5's freeze, enforced; the symmetry gate; F5's tertiles --------------------------

def frozen_block_mismatches(table: ParamTable, floor: ParamTable) -> list[str]:
    """The entries E-0013 B5 froze that must therefore be IDENTICAL on both arms.

    Without this check a fitted table carrying its own KING PSTs would be silently scored
    against the frozen literal instead - the freeze would be enforced by accident, and a
    table that thought it had fitted the KING block would be mis-described rather than
    refused. This turns that silence into a refusal.
    """
    out: list[str] = []
    if table.mg_value["KING"] != floor.mg_value["KING"]:
        out.append(f"mg_value[KING] {table.mg_value['KING']} != {floor.mg_value['KING']}")
    if table.eg_value["KING"] != floor.eg_value["KING"]:
        out.append(f"eg_value[KING] {table.eg_value['KING']} != {floor.eg_value['KING']}")
    if list(table.mg_pst["KING"]) != list(floor.mg_pst["KING"]):
        out.append("mg_pst[KING] differs")
    if list(table.eg_pst["KING"]) != list(floor.eg_pst["KING"]):
        out.append("eg_pst[KING] differs")
    return out


def mirror_violations(fens: Iterable[str], table: ParamTable, stage: int = 6) -> tuple[int, int]:
    """`S(M(b)) == S(b)` over a set of positions (E-0010 gate-(b) discipline, inherited as
    E-0013 conjunct (d)'s 1000-position full-mirror re-run).

    Returns `(violations, checked)`. A violation is a real defect: the eval is required to be
    colour-symmetric because the fit target is expressed in the mover's frame, so a
    non-symmetric scorer would be fitting a different function on each half of the colour
    distribution.
    """
    violations = 0
    checked = 0
    for fen in fens:
        board = chess.Board(fen)
        checked += 1
        if engine_score(board, table, stage) != engine_score(board.mirror(), table, stage):
            violations += 1
    return violations, checked


def phase_tertiles(phases: Iterable[int]) -> list[int]:
    """E-0013 F5: tertile boundaries of the phase value, computed over TRAIN positions
    only, rounded to integers. They are frozen in the pre-fit commit; this function is what
    the commit's value is computed WITH, and it is never fed a holdout phase."""
    values = sorted(phases)
    if len(values) < 3:
        raise ValueError("at least three positions are needed for tertiles")
    import numpy as np

    # The boundaries that split the sorted values into three equal-count groups.
    q1, q2 = float(np.percentile(values, 100.0 / 3.0)), float(np.percentile(values, 200.0 / 3.0))
    return [int(round(q1)), int(round(q2))]


def tertile_of(phase: int, boundaries: list[int]) -> int:
    if len(boundaries) != 2:
        raise ValueError("two boundaries pin three tertiles")
    if phase <= boundaries[0]:
        return 0
    if phase <= boundaries[1]:
        return 1
    return 2


# --- paired evaluation ----------------------------------------------------------------

@dataclass
class Sample:
    game_id: int
    fen: str
    stm: str
    y: float
    terms: Terms


def load_samples(positions_path: Path, split_map_path: Path, splits: Iterable[str],
                 skip_labels: bool = False) -> list[Sample]:
    """Load the extractor's positions for the requested splits.

    Rows outside the requested splits are skipped on `game_id` ALONE - their FENs are never
    parsed - which is what makes "the holdout is not read" a property of this loop rather
    than a promise about how it was called. The split authority is the committed split-map
    file, not a field inside the positions file, so there is exactly one place where a
    position's partition is decided.
    """
    wanted = set(splits)
    if wanted - {"train", "holdout"}:
        raise ValueError(f"unknown splits {sorted(wanted - {'train', 'holdout'})}")
    smap_obj = json.loads(split_map_path.read_text(encoding="utf-8"))
    smap = smap_obj["map"]
    # E-00014's inner map (kana-e0013-innersplit-v1) covers OUTER-TRAIN games ONLY, so a
    # missing key there is not an error: it IS an outer-holdout row and is excluded on
    # game_id alone, exactly the E-00014 rule ("holdout ids touch only a set
    # intersection, never a content read"). For E-0013's OUTER map a missing key is a
    # real corruption and stays a hard error - the outer gate is not weakened.
    inner_map = smap_obj.get("format") == "kana-e0013-innersplit-v1"
    samples: list[Sample] = []
    for line in positions_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        head = json.loads(line)
        role = smap.get(str(head["game_id"]))
        if role is None:
            if inner_map:
                continue
            raise KeyError(f"game {head['game_id']} has no role in the split map "
                           f"{split_map_path} - the map cannot partition the corpus")
        if role not in wanted:
            continue
        if head["fen"] is None:
            raise ValueError("a row selected for scoring has no FEN")
        y = float(head["y"])
        if skip_labels and head.get("y") is None:
            raise ValueError("labels are required for a loss comparison")
        board = chess.Board(head["fen"])
        samples.append(Sample(game_id=int(head["game_id"]), fen=head["fen"],
                              stm=head["stm"], y=y, terms=position_terms(board)))
    return samples


def per_game_losses(samples: list[Sample], vector: list[int] | list[float], tempo: float,
                    clip: float, mode: str) -> tuple[dict[int, float], list[float], list[float]]:
    """`(per-game mean loss, per-position loss, per-position score)`.

    `mode` selects the exact engine score or the continuous surrogate. The pair is reported
    rather than one being chosen, because the gap between them is the size of the integer
    quantisation and a reader is entitled to see it.
    """
    score_fn = exact_stm_score if mode == "exact" else surrogate_stm_score
    per_position: list[float] = []
    scores: list[float] = []
    for sample in samples:
        e = score_fn(sample.terms, vector, tempo)
        scores.append(float(e))
        per_position.append(logistic_loss(clip_value(float(e), clip), sample.y))
    grouped: dict[int, list[float]] = {}
    for sample, value in zip(samples, per_position):
        grouped.setdefault(sample.game_id, []).append(value)
    per_game = {gid: sum(v) / len(v) for gid, v in grouped.items()}
    return per_game, per_position, scores


def paired_statistics(per_game: dict[int, float], t_level: float = 0.975) -> dict[str, float]:
    """E-0013 B3 sentence 1, applied literally.

    The independent unit is the GAME, not the position (the label is game-constant), so the
    estimator is the mean over `G` games of the per-game mean paired difference, with
    `SE = s_d / sqrt(G)` on `t_{0.975, G-1}`. Sign convention (E-00014): POSITIVE means the
    fitted table achieves LOWER logistic loss.
    """
    import numpy as np
    from scipy.stats import t as student_t

    values = np.array(list(per_game.values()), dtype=np.float64)
    games = int(values.size)
    if games < 2:
        return {"games": games, "mean_improvement": float(values.mean()) if games else float("nan"),
                "s_d": float("nan"), "se": float("nan"),
                "ci_low": float("nan"), "ci_high": float("nan"), "t_crit": float("nan")}
    mean = float(values.mean())
    s_d = float(values.std(ddof=1))
    se = s_d / math.sqrt(games)
    t_crit = float(student_t.ppf(t_level, games - 1))
    return {"games": games, "mean_improvement": mean, "s_d": s_d, "se": se,
            "ci_low": mean - t_crit * se, "ci_high": mean + t_crit * se, "t_crit": t_crit}


# --- the two-arm evaluation ------------------------------------------------------------

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


def abort(reason: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"ABORT: {reason}", file=sys.stderr)
    raise SystemExit(2)


def load_table(path: Path) -> ParamTable:
    return from_json(json.loads(path.read_text(encoding="utf-8")))


def mae(scores: list[float], labels: list[float], clip: float) -> float:
    """Mean absolute error of the PREDICTED PROBABILITY `sigmoid(clip(E,-L,L))` against the
    label, in probability units - the only MAE this model can define without inventing a
    centipawn-to-result scale. Stated here because a bare "MAE" of centipawns against
    {0, 0.5, 1} is not a quantity."""
    if not scores:
        return float("nan")
    return sum(abs(sigmoid(clip_value(e, clip)) - y) for e, y in zip(scores, labels)) / len(scores)


def evaluate_arms(args: argparse.Namespace) -> dict[str, Any]:
    """Load both arms, prove they differ, then compute the paired comparison.

    Order matters and is the contract: the two hashes are printed and compared, and the
    frozen-block check runs, BEFORE a single loss is computed (E-0013 B1 (ii)).
    """
    floor = hand_tuned()
    if args.floor:
        loaded = load_table(Path(args.floor))
        if table_sha256(loaded) != table_sha256(floor):
            abort("the --floor table is not the compiled-in hand-tuned floor (same-floor "
                  "discipline: E-00014's delta_star is E-0013's delta_star only if the floor "
                  "is the same bytes)")
        floor_path = str(Path(args.floor).resolve())
    else:
        floor_path = "built-in transcription of src/eval.cpp:174-234"
    fitted = load_table(Path(args.fitted))

    floor_hash, fitted_hash = table_sha256(floor), table_sha256(fitted)
    print(f"arm[fitted] {args.fitted} sha256={fitted_hash}")
    print(f"arm[floor]  {floor_path} sha256={floor_hash}")
    if floor_hash == fitted_hash:
        abort("the two arms loaded the SAME parameter table (E-0013 B1: same-hash arms = "
              "FAIL before any loss is read)")
    mismatches = frozen_block_mismatches(fitted, floor)
    if mismatches:
        abort(f"the fitted table moves a FROZEN entry (B5 sentence 1): {mismatches}")

    splits = set(args.split)
    samples = load_samples(Path(args.positions), Path(args.split_map), splits)
    if not samples:
        abort(f"no positions for split(s) {sorted(splits)}")
    vectors = {"fitted": design_vector(fitted), "floor": design_vector(floor)}
    labels = [s.y for s in samples]

    losses: dict[str, dict[str, Any]] = {}
    for arm, vector in vectors.items():
        tempo = (fitted if arm == "fitted" else floor).scalars["tempo"]
        _, exact_pp, exact_scores = per_game_losses(samples, vector, tempo, args.clip, "exact")
        exact_pg, _, _ = per_game_losses(samples, vector, tempo, args.clip, "exact")
        surr_pg, surr_pp, _ = per_game_losses(samples, vector, tempo, args.clip, "surrogate")
        losses[arm] = {
            "tempo": tempo,
            "per_game_exact": exact_pg,
            "per_game_surrogate": surr_pg,
            "mean_loss_exact": sum(exact_pp) / len(exact_pp),
            "mean_loss_surrogate": sum(surr_pp) / len(surr_pp),
            "mae": mae(exact_scores, labels, args.clip),
            "scores": exact_scores,
        }

    # Paired difference, clustered BY GAME, sign = loss_floor - loss_fitted so that positive
    # means the fitted table achieves LOWER loss (E-00014's stated convention).
    paired = {gid: losses["floor"]["per_game_exact"][gid] - losses["fitted"]["per_game_exact"][gid]
              for gid in losses["floor"]["per_game_exact"]}
    paired_surrogate = {
        gid: losses["floor"]["per_game_surrogate"][gid] - losses["fitted"]["per_game_surrogate"][gid]
        for gid in losses["floor"]["per_game_surrogate"]}

    report: dict[str, Any] = {
        "tool": "tools/e0013_eval.py",
        "src_commit": git_commit(),
        "stage": 6,
        "splits": sorted(splits),
        "positions": len(samples),
        "clip_L": args.clip,
        "arm_hashes": {"fitted": f"sha256:{fitted_hash}", "floor": f"sha256:{floor_hash}"},
        "arm_paths": {"fitted": str(Path(args.fitted).resolve()), "floor": floor_path},
        "arms_differ": True,
        "frozen_block_identical": True,
        "loss": {arm: {"mean_exact": losses[arm]["mean_loss_exact"],
                       "mean_surrogate": losses[arm]["mean_loss_surrogate"],
                       "mae_probability_units": losses[arm]["mae"],
                       "tempo": losses[arm]["tempo"]} for arm in losses},
        "paired_mean_logistic_loss_improvement": paired_statistics(paired),
        "paired_mean_logistic_loss_improvement_surrogate": paired_statistics(paired_surrogate),
        "loss_margin_reference": 0.002,
        "loss_margin_note": "LOSS_MARGIN := max(0.002, 0.5 * delta_star); delta_star is measured "
                            "by E-00014 on a TRAIN inner partition and never by this tool",
    }
    if args.tertiles:
        boundaries = [int(v) for v in args.tertiles.split(",")]
        buckets: dict[str, dict[int, list[tuple[float, float]]]] = {"fitted": {}, "floor": {}}
        for arm in ("fitted", "floor"):
            for sample, e in zip(samples, losses[arm]["scores"]):
                buckets[arm].setdefault(tertile_of(sample.terms.phase, boundaries), []).append(
                    (e, sample.y))
        report["mae_by_tertile"] = {
            arm: {str(k): mae([e for e, _ in v], [y for _, y in v], args.clip)
                  for k, v in sorted(buckets[arm].items())}
            for arm in buckets}
        report["tertile_boundaries"] = boundaries
    else:
        report["mae_by_tertile"] = None
        report["mae_by_tertile_null_reason"] = (
            "no --tertiles supplied: F5 pins the boundaries in the pre-fit commit and they may "
            "not be derived from a holdout here")
    requested = args.mirror_check_n
    violations, checked = mirror_violations([s.fen for s in samples[:requested]], fitted, 6)
    report["mirror_check"] = {"violations": violations, "checked": checked, "requested": requested,
                              "shortfall": max(0, requested - checked)}
    report["artifacts"] = {"positions_sha256": sha256_file(Path(args.positions)),
                           "split_map_sha256": sha256_file(Path(args.split_map))}
    return report


# --- the tertile authoring mode (F5) and the CLI --------------------------------------

def write_tertiles(args: argparse.Namespace) -> int:
    """Compute F5's boundaries from TRAIN positions only, and print them with their hash.

    This is the authoring side of F5. Note what it refuses to do: there is no flag that
    would compute the boundaries from the holdout, because the values only mean what they
    mean if they were derived from the training side.
    """
    samples = load_samples(Path(args.positions), Path(args.split_map), {"train"})
    if not samples:
        abort("no TRAIN positions to derive tertiles from")
    boundaries = phase_tertiles(s.terms.phase for s in samples)
    payload = (json.dumps({"rule": "tertiles of phase over TRAIN positions, rounded to ints",
                           "train_positions": len(samples), "boundaries": boundaries},
                          sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    print(f"tertile_boundaries={boundaries[0]},{boundaries[1]}")
    print(f"train_positions={len(samples)}")
    print(f"tertiles_sha256={hashlib.sha256(payload).hexdigest()}")
    return 0


def write_floor(args: argparse.Namespace) -> int:
    table = hand_tuned()
    path = Path(args.write_floor)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(table_bytes(table))
    print(f"wrote {path}")
    print(f"floor_sha256={table_sha256(table)}")
    print(f"bytes={path.stat().st_size}")
    return 0


# --- self-test (pure synthetic; no dataset, no holdout, no engine) --------------------

SELFTEST_FENS = (
    "4k3/8/8/8/8/8/8/Q3K3 w - - 0 1",
    "4k3/8/8/8/8/8/8/Q3K3 b - - 0 1",
    "r3k2r/ppp2ppp/2npbn2/4p3/4P3/2NPBN2/PPP2PPP/R3K2R w KQkq - 8 10",
    "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1",
    "rnbq1rk1/pp3ppp/2pb1n2/3p4/3P4/2NBPN2/PP3PPP/R1BQ1RK1 b - - 3 9",
    "8/5k2/8/8/8/8/5K2/8 w - - 0 1",
    "6k1/5ppp/8/8/8/8/5PPP/6K1 w - - 0 1",
    "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10",
    "8/3k4/8/8/8/8/4P3/4K3 w - - 0 1",
    "2r3k1/5ppp/8/8/8/8/5PPP/2R3K1 b - - 0 1",
)


def zeroed_table(**overrides: int) -> ParamTable:
    """The floor table with every FITTED entry set to zero.

    Isolating one term at a time is how a port is checked against arithmetic instead of
    against itself: with everything else zero, the score IS the term under test.
    """
    table = hand_tuned()
    table.mg_value = {p: 0 for p in PIECE_ORDER}
    table.eg_value = {p: 0 for p in PIECE_ORDER}
    table.mg_pst = {p: [0] * 64 for p in PIECE_ORDER}
    table.eg_pst = {p: [0] * 64 for p in PIECE_ORDER}
    table.passed_pawn_mg = [0] * 8
    table.passed_pawn_eg = [0] * 8
    table.scalars = {k: 0 for k in SCALAR_INT_FIELDS}
    for key, value in overrides.items():
        table.scalars[key] = value
    return table


def _raises(fn: Any) -> bool:
    try:
        fn()
    except Exception:
        return True
    return False


def selftest() -> int:
    import tempfile

    checks: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, bool(ok), detail))

    def expect_abort(name: str, fn: Any) -> None:
        try:
            fn()
            check(name, False, "no abort raised")
        except SystemExit as exc:
            check(name, exc.code == 2, f"code={exc.code}")

    # --- integer arithmetic the engine depends on --------------------------------------
    check("trunc_div: toward zero on a negative numerator", trunc_div(-7, 2) == -3)
    check("trunc_div: positive stays positive", trunc_div(7, 2) == 3)
    check("trunc_div: differs from Python floor for negatives", trunc_div(-7, 2) != -7 // 2)
    check("trunc_div: tiny negative numerator truncates to 0", trunc_div(-1, 24) == 0)
    check("sigmoid(0) == 0.5", abs(sigmoid(0.0) - 0.5) < 1e-15)
    check("logistic_loss(0, 0.5) == ln2", abs(logistic_loss(0.0, 0.5) - math.log(2)) < 1e-15)
    check("clip_value clamps both ends", clip_value(1e9, 4.0) == 4.0 and clip_value(-1e9, 4.0) == -4.0)
    check("clip_value rejects a non-positive L", _raises(lambda: clip_value(0.0, 0.0)))

    # --- hand-derived goldens for the hand-tuned table ---------------------------------
    startpos = chess.Board()
    floor = hand_tuned()
    check("phase of startpos is 24 (the cap)", phase_of(startpos) == 24)
    check("GOLDEN: startpos at S*=6 is exactly the tempo bonus (10)",
          engine_score(startpos, floor, 6) == 10, str(engine_score(startpos, floor, 6)))
    check("GOLDEN: startpos at stage 5 is 0 (tempo is the only non-cancelling term)",
          engine_score(startpos, floor, 5) == 0)
    check("GOLDEN: startpos at stage 0 is 0", engine_score(startpos, floor, 0) == 0)
    check("stage 0 uses FLAT_VALUE (a lone queen is 900)",
          engine_score(chess.Board("4k3/8/8/8/8/8/8/Q3K3 w - - 0 1"), floor, 0) == 900)
    # Hand-count: 4 knights*1 + 2 bishops*1 + 4 rooks*2 + 0 queens*4 = 14. The position has
    # NO queens on purpose - that is the assertion: the queen weight is dropped, not assumed.
    check("phase drops the queen weight when there are no queens",
          phase_of(chess.Board("r3k2r/ppp2ppp/2npbn2/4p3/4P3/2NPBN2/PPP2PPP/R3K2R w KQkq - 8 10")) == 14)

    # --- the queen-only half-coefficient site, isolated --------------------------------
    # A lone queen means phase == 4 and a lone rook phase == 2, so the taper
    # `(mg*phase + eg*(24-phase))/24` is NOT the identity and would otherwise divide the quantity
    # under test. Setting mg == eg == v makes the taper exactly v on the post-halving value, so
    # the score is the coefficient AS THE ENGINE HALVES IT and nothing else. That is what makes
    # this a test of the halving rather than of the taper. src/eval.cpp:324-333 gives a ROOK the
    # full `open_file_mg` and a QUEEN `open_file_mg/2` on the same open file, and that asymmetry is
    # the property under test - so both are measured on the same board shape.
    queen_open = chess.Board("4k3/8/8/8/8/8/8/Q3K3 w - - 0 1")
    rook_open = chess.Board("4k3/8/8/8/8/8/8/R3K3 w - - 0 1")
    check("half site: the isolating table is taper-neutral (mg==eg scores the halved value)",
          engine_score(queen_open, zeroed_table(open_file_mg=15, open_file_eg=15), 6) == 7)
    got = engine_score(queen_open, zeroed_table(open_file_mg=15, open_file_eg=15), 6)
    check("half site: open_file_mg=15 on an open file scores 15/2 trunc = 7", got == 7, str(got))
    check("half site: open_file_mg=16 scores 8",
          engine_score(queen_open, zeroed_table(open_file_mg=16, open_file_eg=16), 6) == 8)
    got_neg = engine_score(queen_open, zeroed_table(open_file_mg=-15, open_file_eg=-15), 6)
    check("half site: -15 truncates toward zero to -7, not -8", got_neg == -7, str(got_neg))
    # The control: the same coefficient on a ROOK is NOT halved, so if the halving were applied to
    # every open-file site this would read 7 and fail. It also confirms the two boards are
    # otherwise equivalent, so the difference is the site and not the position.
    got_rook = engine_score(rook_open, zeroed_table(open_file_mg=15, open_file_eg=15), 6)
    check("half site: a rook on the same open file gets the FULL 15, not 15/2",
          got_rook == 15, str(got_rook))
    check("tempo: added unsigned in the mover's frame (White)",
          engine_score(queen_open, zeroed_table(tempo=10), 6) == 10)
    check("tempo: added unsigned in the mover's frame (Black)",
          engine_score(chess.Board("4k3/8/8/8/8/8/8/Q3K3 b - - 0 1"), zeroed_table(tempo=10), 6) == 10)

    # --- the KING-PST freeze and the 683 layout, mechanically --------------------------
    check("layout: the total is asserted at import",
          sum(n for _, n in DESIGN_LAYOUT) == N_FREE == 683)
    check("layout: no KING entry can enter the fitted set",
          not any("KING" in name for name, _ in DESIGN_LAYOUT))
    check("design vector has exactly 683 entries", len(design_vector(floor)) == 683)
    check("SLOT covers the whole vector", len(SLOT) == N_FREE and max(SLOT.values()) == N_FREE - 1)
    check("floor round-trips through the design vector",
          design_vector(from_design_vector(design_vector(floor), floor)) == design_vector(floor))
    check("a vector of the wrong length is refused",
          _raises(lambda: from_design_vector([0] * 682, floor)))
    check("frozen block identical for the floor against itself", frozen_block_mismatches(floor, floor) == [])
    king_pst_moved = hand_tuned()
    king_pst_moved.mg_pst["KING"][0] += 1
    check("a moved KING PST is caught", bool(frozen_block_mismatches(king_pst_moved, floor)))
    king_mat_moved = hand_tuned()
    king_mat_moved.mg_value["KING"] = 0
    check("a moved KING material entry is caught", bool(frozen_block_mismatches(king_mat_moved, floor)))
    check("design_vector ignores the KING block entirely",
          design_vector(king_pst_moved) == design_vector(floor))

    # --- table hashing -----------------------------------------------------------------
    check("table JSON round-trips to the same hash",
          table_sha256(from_json(json.loads(table_bytes(floor).decode("utf-8")))) == table_sha256(floor))
    mutations = (
        ("mg_value[PAWN]", lambda t: t.mg_value.__setitem__("PAWN", t.mg_value["PAWN"] + 1)),
        ("mg_pst[PAWN][0]", lambda t: t.mg_pst["PAWN"].__setitem__(0, t.mg_pst["PAWN"][0] + 1)),
        ("tempo", lambda t: t.scalars.__setitem__("tempo", t.scalars["tempo"] + 1)),
        ("passed_pawn_eg[3]", lambda t: t.passed_pawn_eg.__setitem__(3, t.passed_pawn_eg[3] + 1)),
        ("doubled_pawn_mg", lambda t: t.scalars.__setitem__("doubled_pawn_mg", 999)),
    )
    for label, mutate in mutations:
        probe = hand_tuned()
        mutate(probe)
        check(f"hash changes when {label} moves", table_sha256(probe) != table_sha256(floor))
    check("the floor hash is stable across constructions", table_sha256(hand_tuned()) == table_sha256(floor))
    check("a bad format tag is refused",
          _raises(lambda: from_json(dict(json.loads(table_bytes(floor).decode("utf-8")), format="x"))))

    # --- mirror symmetry ---------------------------------------------------------------
    for label, table in (("hand-tuned floor", floor),
                         ("a perturbed table", from_design_vector(
                             [v + (7 if i % 5 == 0 else -3) for i, v in enumerate(design_vector(floor))],
                             floor))):
        violations, checked = mirror_violations(SELFTEST_FENS, table, 6)
        check(f"mirror: 0 violations for {label}", violations == 0, f"{violations}/{checked}")
    check("mirror: the check actually visited the positions",
          mirror_violations(SELFTEST_FENS, floor, 6)[1] == len(SELFTEST_FENS))

    # --- design_rows must reproduce the per-sample surrogate score ---------------------
    import numpy as np

    terms_list = [position_terms(chess.Board(f)) for f in SELFTEST_FENS]
    vector = design_vector(floor)
    jac, offset = design_rows(terms_list)
    dense = np.asarray(jac @ np.array(vector, dtype=np.float64)).ravel() + offset
    direct = np.array([surrogate_stm_score(t, vector, floor.scalars["tempo"]) for t in terms_list])
    check("design_rows: J @ theta + K reproduces surrogate_stm_score",
          float(np.max(np.abs(dense - direct))) < 1e-9,
          f"max|diff|={float(np.max(np.abs(dense - direct)))}")
    check("design_rows: the Jacobian has 683 columns", jac.shape == (len(SELFTEST_FENS), N_FREE))
    tempo_slot = SLOT[("scalar", "tempo")]
    check("design_rows: the tempo column is exactly 1 everywhere",
          all(abs(jac[i, tempo_slot] - 1.0) < 1e-12 for i in range(len(terms_list))))
    check("design_rows: a non-tempo column is zero for a position that never uses it",
          all(abs(jac[i, SLOT[("scalar", "bishop_pair_mg")]]) < 1e-12
              for i, t in enumerate(terms_list) if ("scalar", "bishop_pair_mg") not in t.mg_counts))

    # --- the analytic gradient against finite differences -------------------------------
    labels = np.array([0.0, 1.0, 0.5, 1.0, 0.0, 0.5, 1.0, 0.0, 0.5, 1.0])
    theta0 = np.array(vector, dtype=np.float64)
    theta = theta0 + np.array([0.37 * (1 if i % 3 else -1) for i in range(N_FREE)])
    clip_big, l2 = 400.0, 1e-3

    def loss_at(x: Any) -> float:
        return loss_and_gradient(jac, offset, labels, np.asarray(x, dtype=np.float64),
                                 clip_big, l2, theta0)[0]

    _, grad = loss_and_gradient(jac, offset, labels, theta, clip_big, l2, theta0)
    probe = np.array(theta, dtype=np.float64)
    worst = 0.0
    for i in range(N_FREE):
        h = 1e-5 * max(1.0, abs(probe[i]))
        old = probe[i]
        probe[i] = old + h
        up = loss_at(probe)
        probe[i] = old - h
        down = loss_at(probe)
        probe[i] = old
        fd = (up - down) / (2.0 * h)
        worst = max(worst, abs(fd - grad[i]) / (1.0 + abs(fd)))
    check("gradient: analytic matches central finite differences over all 683 slots",
          worst < 1e-6, f"worst relative error {worst:.3e}")
    loss_zero_l2, grad_zero_l2 = loss_and_gradient(jac, offset, labels, theta, clip_big, 0.0, theta0)
    check("gradient: the L2 term is exactly l2 * sum((theta - theta0)^2)",
          abs((loss_at(theta) - loss_zero_l2) - l2 * float(np.sum((theta - theta0) ** 2))) < 1e-9)
    _, grad_at0 = loss_and_gradient(jac, offset, labels, theta0, clip_big, l2, theta0)
    _, grad_at0_no_l2 = loss_and_gradient(jac, offset, labels, theta0, clip_big, 0.0, theta0)
    check("gradient: at theta0 the L2 part contributes nothing",
          float(np.max(np.abs(grad_at0 - grad_at0_no_l2))) < 1e-12)
    # The ridge contribution is ELEMENTWISE `2*l2*(theta - theta0)`, so it is checked that way.
    # Summing the two gradients instead would compare the data term at `theta` with the data term
    # at `theta0` - two different points - which is not an identity about the L2 term at all.
    l2_pull = grad - grad_zero_l2
    want_pull = 2.0 * l2 * (theta - theta0)
    check("gradient: the L2 pull is elementwise exactly 2*l2*(theta - theta0)",
          float(np.max(np.abs(l2_pull - want_pull))) < 1e-12,
          f"max|diff|={float(np.max(np.abs(l2_pull - want_pull)))}")
    # "Pulls back toward the floor" means: for every coordinate, the ridge term has the SAME SIGN
    # as the displacement from theta0, so a descent step on it always moves toward the floor.
    check("gradient: the L2 term pulls every coordinate back toward the floor",
          bool(np.all(np.sign(l2_pull) == np.sign(theta - theta0))))

    # --- the surrogate/exact gap is small and bounded ----------------------------------
    gaps = [abs(exact_stm_score(t, vector, floor.scalars["tempo"])
                - surrogate_stm_score(t, vector, floor.scalars["tempo"])) for t in terms_list]
    check("exact and surrogate scores differ by at most 1 cp", max(gaps) <= 1.0, f"max gap {max(gaps)}")

    # --- F5 tertiles -------------------------------------------------------------------
    phases = [0, 4, 8, 12, 16, 20, 24, 24, 12, 24]
    boundaries = phase_tertiles(phases)
    check("tertiles: two integer boundaries", len(boundaries) == 2 and all(isinstance(b, int) for b in boundaries))
    check("tertiles: ordered", boundaries[0] <= boundaries[1])
    check("tertiles: every position lands in a bucket",
          all(0 <= tertile_of(p, boundaries) <= 2 for p in phases))
    check("tertiles: monotone in phase",
          tertile_of(0, boundaries) <= tertile_of(24, boundaries))
    check("tertiles: three or more positions required",
          _raises(lambda: phase_tertiles([1, 2])))

    # --- the paired statistic, against hand arithmetic ---------------------------------
    stats = paired_statistics({0: 0.1, 1: 0.2, 2: 0.3, 3: 0.4})
    check("paired: G is the game count", stats["games"] == 4)
    check("paired: mean over games", abs(stats["mean_improvement"] - 0.25) < 1e-12)
    check("paired: s_d is the sample SD over GAMES", abs(stats["s_d"] - 0.12909944487358055) < 1e-12,
          str(stats["s_d"]))
    check("paired: SE = s_d / sqrt(G)", abs(stats["se"] - stats["s_d"] / 2.0) < 1e-12)
    check("paired: t_{0.975,3} = 3.1824", abs(stats["t_crit"] - 3.182446305284263) < 1e-9,
          str(stats["t_crit"]))
    check("paired: the CI brackets the mean",
          stats["ci_low"] < stats["mean_improvement"] < stats["ci_high"])
    single = paired_statistics({0: 0.5})
    check("paired: one game cannot produce an SD, and says so with the game count",
          single["games"] == 1 and math.isnan(single["s_d"]))

    # --- end to end: two arms, two tables, the abort that guards them -------------------
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        rows = []
        for game_id, fen, y in zip((0, 1, 2), SELFTEST_FENS[:3], (1.0, 0.0, 0.5)):
            board = chess.Board(fen)
            rows.append({"game_id": game_id, "ply_index": 20, "fen": fen,
                         "norm_fen": " ".join(fen.split()[:4]), "stm": "w" if board.turn else "b",
                         "y": y})
        positions = tmp_path / "positions.jsonl"
        positions.write_bytes(b"".join(
            (json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8") for r in rows))
        split_map_path = tmp_path / "split_map.json"
        split_map_path.write_bytes((json.dumps({"map": {"0": "train", "1": "train", "2": "holdout"}},
                                               sort_keys=True) + "\n").encode("utf-8"))

        floor_path = tmp_path / "floor.json"
        floor_path.write_bytes(table_bytes(floor))
        fitted = from_design_vector([v + (1 if i % 7 == 0 else 0)
                                     for i, v in enumerate(design_vector(floor))], floor)
        fitted_path = tmp_path / "fitted.json"
        fitted_path.write_bytes(table_bytes(fitted))
        same_path = tmp_path / "same.json"
        same_path.write_bytes(table_bytes(floor))
        king_moved = from_json(json.loads(table_bytes(floor).decode("utf-8")))
        king_moved.mg_pst["KING"] = list(king_moved.mg_pst["KING"])
        king_moved.mg_pst["KING"][0] += 1
        king_path = tmp_path / "king_moved.json"
        king_path.write_bytes(table_bytes(king_moved))

        def arm_args(fitted_file: Path, split: list[str]) -> argparse.Namespace:
            return argparse.Namespace(fitted=str(fitted_file), floor=str(floor_path),
                                      positions=str(positions), split_map=str(split_map_path),
                                      split=split, clip=400.0, tertiles=None, mirror_check_n=1000)

        expect_abort("arms: identical tables abort before any loss is read",
                     lambda: evaluate_arms(arm_args(same_path, ["holdout"])))
        expect_abort("arms: a moved frozen KING entry aborts",
                     lambda: evaluate_arms(arm_args(king_path, ["holdout"])))
        expect_abort("arms: a --floor that is not the compiled-in floor aborts",
                     lambda: evaluate_arms(argparse.Namespace(
                         fitted=str(fitted_path), floor=str(fitted_path),
                         positions=str(positions), split_map=str(split_map_path),
                         split=["holdout"], clip=400.0, tertiles=None, mirror_check_n=1000)))

        report = evaluate_arms(arm_args(fitted_path, ["holdout"]))
        check("arms: the report records both arm hashes",
              report["arm_hashes"]["fitted"] != report["arm_hashes"]["floor"])
        check("arms: arms_differ is asserted in the report", report["arms_differ"] is True)
        check("arms: only the requested split is scored", report["positions"] == 1,
              f"positions={report['positions']}")
        check("arms: the mirror gate is clean", report["mirror_check"]["violations"] == 0)
        check("arms: the mirror gate reports its shortfall rather than hiding it",
              report["mirror_check"]["shortfall"] == 999)
        check("arms: tertile MAE is null WITH a reason when no boundaries are supplied",
              report["mae_by_tertile"] is None and bool(report["mae_by_tertile_null_reason"]))
        check("arms: the paired statistic is computed over the holdout games",
              report["paired_mean_logistic_loss_improvement"]["games"] == 1)
        check("arms: the loss margin reference is recorded, not inferred",
              report["loss_margin_reference"] == 0.002)
        trained = evaluate_arms(argparse.Namespace(
            fitted=str(fitted_path), floor=str(floor_path), positions=str(positions),
            split_map=str(split_map_path), split=["train", "holdout"], clip=400.0,
            tertiles="8,16", mirror_check_n=2))
        check("arms: both splits score together when asked", trained["positions"] == 3)
        check("arms: tertile MAE appears for each arm when boundaries are supplied",
              set(trained["mae_by_tertile"]) == {"fitted", "floor"} and
              bool(trained["mae_by_tertile"]["fitted"]))
        check("arms: the mirror check honours the requested count",
              trained["mirror_check"]["checked"] == 2)

    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not ok else ""))
    failed = [n for n, ok, _ in checks if not ok]
    print(f"SELFTEST {'PASS' if not failed else 'FAIL'} checks={len(checks)} failed={len(failed)}")
    return 0 if not failed else 1


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fitted", help="the fitted parameter table (the candidate arm)")
    parser.add_argument("--floor", help="optional floor table; its hash must equal the "
                                       "compiled-in hand-tuned table or the run aborts")
    parser.add_argument("--positions", default=str(ROOT / "build" / "e0013" / "extract" / "positions.jsonl"))
    parser.add_argument("--split-map", default=str(ROOT / "build" / "e0013" / "extract" / "split_map.json"))
    parser.add_argument("--split", action="append", choices=["train", "holdout"],
                        help="may be repeated; holdout is read only when it is named")
    parser.add_argument("--clip", type=float,
                        help="the pinned clipping bound L; required for a loss, because the "
                             "objective is sigmoid(clip(E, -L, L)) and L has no default")
    parser.add_argument("--tertiles", help="F5's boundaries as 'a,b', from the pre-fit commit")
    parser.add_argument("--mirror-check-n", type=int, default=1000,
                        help="the pre-registered 1000-position full-mirror re-run")
    parser.add_argument("--out", help="write the JSON report here")
    parser.add_argument("--write-floor", help="emit the compiled-in floor table and its hash, then exit")
    parser.add_argument("--write-tertiles-from", action="store_true",
                        help="derive F5's boundaries from TRAIN positions only, then exit")
    parser.add_argument("--selftest", action="store_true",
                        help="run the synthetic checks; no dataset and no holdout is touched")
    args = parser.parse_args(argv)
    if not args.selftest and not args.write_floor and not args.write_tertiles_from and not args.fitted:
        parser.error("--fitted is required (or use --selftest / --write-floor / "
                     "--write-tertiles-from)")
    if args.fitted and args.clip is None:
        parser.error("--clip is required: the objective is sigmoid(clip(E, -L, L)) and E-0013 "
                     "pins L in the pre-fit commit, so this tool will not invent one")
    if args.split is None:
        args.split = ["holdout"]
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.selftest:
        return selftest()
    if args.write_floor:
        return write_floor(args)
    if args.write_tertiles_from:
        return write_tertiles(args)
    report = evaluate_arms(args)
    payload = (json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    if args.out:
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        print(f"report={path} bytes={len(payload)} sha256={hashlib.sha256(payload).hexdigest()}")
    stats = report["paired_mean_logistic_loss_improvement"]
    print(f"splits={report['splits']} positions={report['positions']} games={stats['games']}")
    for arm in ("fitted", "floor"):
        entry = report["loss"][arm]
        print(f"loss[{arm}] mean_exact={entry['mean_exact']:.9f} "
              f"mean_surrogate={entry['mean_surrogate']:.9f} mae={entry['mae_probability_units']:.9f}")
    print(f"paired_mean_improvement={stats['mean_improvement']:.9f} "
          f"s_d={stats['s_d']:.9f} se={stats['se']:.9f} "
          f"ci95=[{stats['ci_low']:.9f},{stats['ci_high']:.9f}]")
    print(f"mirror_check={json.dumps(report['mirror_check'], sort_keys=True)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

















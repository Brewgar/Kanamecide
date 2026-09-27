#!/usr/bin/env python3
"""E-0013 quiet-position extractor: filtered positions, GLOBAL-before-split dedup,
committed game-split map, overlap-0 gates, and the E-00015 count-only field set.

RETIRED INSTRUMENTS - read this before reading a number out of a report.
The yield band `75,600..76,587` is **RETIRED** by E-0013's Addendum 2 (S-0039, Ruling 1
/ F-U10). It is gone from this tool: there is no `band` key in the report, no `lo`/`hi`
constant in this file, and no comparison printed. The band was a yield-plausibility
cross-check on the pipeline (`is_pass_criterion: false`), both its endpoints were
functions of the OLD dedup key's expected output, and it had already misfired under that
old key too (76,593 measured against a `hi` of 76,587), so no measurement of this corpus
ever landed inside it. **It is not replaced by a re-derived band.** A band a key change
can pass by luck is a coincidence detector, and a permanently-red instrument teaches
readers to ignore red lights.

What stands in its place introduces no new number at all:
  1. the directly measured `count_usable_distinct`, with
     `duplicates_removed_by_dedup` beside it;
  2. the **UNCHANGED 30,000 scope floor** on the TRAIN side (`SCOPE_FLOOR` below) - this
     is the only magnitude threshold in the contract that gates anything, it is NOT
     renegotiable, and it is reported with its headroom;
  3. the blocking overlap-0 gates, at 0;
  4. the **exact accounting identities** published under `accounting_identities`, which
     are arithmetic rather than projection and therefore cannot rot.
E-00015's own pre-registration still carries the band at L133-137/L152-153/L245-248 and
needs a dated amendment by its own executor seat; this tool simply stops emitting the
retired field so that no future run can produce one.

Contract this tool implements (read-only citations; none of those records is edited):

  * E-0013 "Dataset / Quiet-position filter (EXECUTABLE predicate spec)" - the four
    filter stages, in order:
      (1) QUIET(P) := (not board.is_check())                       # position BEFORE the move
                      and ("x" not in san_played)
                      and (not san_played.endswith("+") and not san_played.endswith("#"))
                      and full_ply >= 10
      (2) crash exclusion:    end == "crash"                      -> game excluded
      (3) degenerate exclusion: end == "mate" and len(san) <= 6    -> game excluded
      (4) GLOBAL-before-split dedup on the NORMALIZED FEN - side to move, piece placement,
          castling/EP rights; the halfmove clock and the fullmove number are NOT part of a
          position's identity (E-0013 F9, as strengthened by the S-0037 leakage ruling)
    `full_ply = board.fullmove_number * 2 + (0 if turn == WHITE else 1) - 1`, and the
    `opening` segment is NEVER a candidate (only the `san` segment is).
  * E-0013 "Split discipline": SPLIT_SALT = 20260926, one `random.Random(
    SPLIT_SALT * 1000003 + game_id)` draw per game, 80% train / 20% holdout BY GAME.
    The split map and its SHA-256 are emitted so they can be committed BEFORE any
    fitting job reads the data.
  * E-0013 F9: dedup is GLOBAL and happens BEFORE the split; the surviving copy's
    `game_id` determines the split, and the normalized-FEN overlap-0 gate then
    verifies that invariant. Since the S-0037 leakage ruling the dedup key and the
    gate's comparison key are the SAME key, so the gate holds by construction and is
    a blocking regression check on this code rather than a hope about the data.
  * E-0013 B2: fit target is the side-to-move frame -
    `y = white_score` if side to move is WHITE else `1 - white_score`, with
    `white_score in {1, 0.5, 0}` obtained from `res` and `a_white`. `label_frame_uniform`
    and the per-side-position counts are reported before any fitting job reads the data.
  * E-0013 B6 sentence 4 / E-00015: the scope floor is evaluated on the TRAIN side of
    the OUTER split (`count_usable_distinct_train`), never on a whole-dataset count.
  * E-00015 "Test Method" step 3: the stage-by-stage field names below are emitted
    verbatim, plus E-00015's abort conditions 1-7.

Two modes, deliberately kept apart, and each mode is now named in the report exactly as
it is used - `count-only` or `labelled` - so no reader has to guess which mode produced a
digest:

  --count-only   E-00015's pass. `count-only`. No label field is read at all: `res` and
                  `a_white` are DELETED from every parsed row before any further use,
                  and the tool refuses to write any label-derived output field (E-00015
                  abort 3). It still reports `label_frame_uniform` as `null` with the
                  reason, so no pre-registered field is silently dropped (E-00015
                  abort 7). **The `positions.jsonl` this mode writes is NOT the fitter's
                  corpus**: every row's `y` is null, so
                  `report["corpus"]["fitter_corpus_sha256"]` is `null` and the file's
                  digest is published under the name count-only-pass digest. That is
                  ASSERTED at write time, not described in prose.
  (default)      Full extraction: `labelled`. Positions + labels + the split map, for the
                  fitter and the parameter-table evaluator. Only a `labelled` artifact's
                  digest may be read as the fitter's corpus digest.

  LABEL CONSTRUCTION is a separate step and it now exists: `tools/e0013_label.py`
  builds the TRAIN-ONLY labelled corpus out of this tool's pinned artifacts and owns
  the per-game constancy and wrong-side enforcement that this tool does not perform.

This tool READS the dataset but NEVER an engine: no binary is invoked, no Gate-0 build is
required, and `tools/e0011_check.py` is CITED, never edited.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import chess

ROOT = Path(__file__).resolve().parent.parent

# --- pinned inputs -------------------------------------------------------------------
DEFAULT_DATASET = ROOT / "m0_audit" / "e0011" / "games.jsonl"
# R-0017-VERIFIED replacement dataset (E-0013 Provenance, E-00014/E-00015 Dataset).
DATASET_SHA256 = "27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95"
DATASET_ROWS = 1000
SPLIT_SALT = 20260926
TRAIN_FRACTION = 0.8
MIN_FULL_PLY = 10
# Salts this project has already spent; SPLIT_SALT must be distant from all of them
# (E-0013 F10: |S - S'| * 1000003 must exceed the prior cap - 1 = 1999 for every one).
PRIOR_SALTS = (20260914, 20260922, 20260924)
SALT_DISTANCE_FACTOR = 1000003
SPLIT_MAP_FORMAT = "kana-e0013-splitmap-v1"
# F-U9 PRE-REGISTERED INVARIANCE ASSERTION. `split_map()` is a pure function of
# (SPLIT_SALT, game_id) computed over the dataset's game rows BEFORE and independently of the
# dedup result, and the hashed object {format, split_salt, train_fraction, rule, map} contains
# no dedup-derived quantity. So this digest is INVARIANT under the F-U7 dedup-key change and
# must be byte-identical before and after it. Measured under the old key and under the new
# key: identical. A MOVED digest would mean the salt, the fraction or the rule had moved -
# which the S-0037 ruling does not authorise - so it is an ABORT, never a new baseline.
# Asserted only against the real pinned dataset; the self-test runs on small synthetic row
# sets whose maps are legitimately different.
SPLIT_MAP_SHA256_EXPECTED = "bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea"
POSITIONS_FORMAT = "kana-e0013-positions-v1"
REPORT_FORMAT = "kana-e0013-extract-report-v1"

# `end` vocabulary pinned by tools/e0011_generate.py / R-0016.
END_VOCABULARY = {"mate", "stalemate", "draw-material", "rule50", "repetition", "plycap", "crash"}
# The two keys the count-only pass must never read (E-00015 abort 3).
LABEL_KEYS = ("res", "a_white")

# --- the scope floor: UNCHANGED, and not renegotiable -------------------------------
# E-0013 conjunct (a) / B6 sentence 4 / E-00015 rules 1-2. This is the ONLY magnitude
# threshold in the contract that gates anything, and it is NOT the retired band. The band
# was a yield-plausibility cross-check on the pipeline (`is_pass_criterion: false`) whose
# endpoints came from a projection; this is a pre-registered quality/scope rule on the
# TRAIN side. S-0039 retired the band and left this untouched, it holds at 59,892, and
# nothing in this tool may move it.
SCOPE_FLOOR = 30000

# --- the two modes, named as they are used -------------------------------------------
# These strings are the report's `mode` value and the suffix of
# `artifacts.positions_sha256_kind`. A count-only artifact is a MEASUREMENT and a
# labelled artifact is a CORPUS; they have different digests, so publishing one digest
# under one bare name is how a reader comes to treat a measurement as the thing a fitter
# read. Both names are asserted against the bytes about to be written.
MODE_COUNT_ONLY = "count-only"
MODE_LABELLED = "labelled"
FITTER_CORPUS_KIND = "fitter-corpus"
COUNT_ONLY_PASS_KIND = "count-only-pass"

# This file as a repo-relative path, for the write-time provenance assertion.
TOOL_REL = "tools/e0013_extract.py"
# What a synthetic (`--allow-synthetic`) run publishes instead of a commit pin. The
# self-test's temporary corpora must not depend on this repository's working tree being
# clean, and a real-looking hash that happened to be true would be a worse answer than a
# sentinel that is obviously not a commit.
SYNTHETIC_PROVENANCE = {
    "asserted": False,
    "src_commit": "SYNTHETIC-NOT-A-COMMIT",
    "asserted_by": "--allow-synthetic: the self-test runs on temporary corpora, so no "
                   "commit pin is asserted",
    "why_not_asserted": "a synthetic run's provenance is its fixture, not this repository",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(obj: Any) -> bytes:
    """The one serialization used for every hash this tool publishes.

    `sort_keys=True`, `separators=(",", ":")`, UTF-8, LF-terminated. Two people who
    follow this line get the same bytes, which is what makes a published hash a
    commitment rather than a receipt.
    """
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")


def src_provenance(repo: Path = ROOT, tool_rel: str = TOOL_REL) -> dict[str, Any]:
    """ASSERT that the running code is the COMMITTED code, then return the pin.

    E-0013 Addendum 2 (S-0039) section 9, and the defect Ruling 2 acts on: the artifact on
    disk carried `src_commit = 9f6574c`, the PARENT of `da93d9c`. The extraction had been run
    against a working tree whose changes were not yet committed, so the artifact's
    provenance pointed at a commit that does not contain the code that produced it. The
    bytes were right and the attribution was stale, which is the worst shape a defect takes.

    So this does not read a commit and call it a pin. `git rev-parse HEAD` reports where the
    branch points; it says nothing about whether the code in the working tree is in that
    commit. What makes it a pin is comparing the blob the RUNNING file has against the blob
    the SAME commit has for the SAME path. Equal means the executing code is byte-for-byte
    the code that commit contains, and that commit is therefore the provenance. Unequal
    means the output would be attributed to code that is in no commit at all, and the only
    honest answer is to ABORT - an artifact whose provenance is a guess is worse than no
    artifact, because it looks loadable.

    Two properties this is built to have:
      * it is asserted at WRITE time. `run()` calls it before any artifact exists, so there
        is no window in which a stale value is written and later read back;
      * it is NOT read from a field. No previously written `report.json` is ever opened by
        this tool, so a stale `src_commit` in an existing report cannot be inherited.

    Known sharp edge, stated rather than hidden: if the repository ever gains a
    `.gitattributes` that applies text conversion to this path, the working-tree blob would
    differ from the committed blob for a reason that has nothing to do with the code, and
    this would fire. That is a loud false positive, which is the right side to err on: the
    alternative is a silent false pin.
    """
    def git(*argv: str) -> str:
        try:
            return subprocess.check_output(
                ["git", *argv], cwd=repo, text=True, encoding="utf-8",
                stderr=subprocess.DEVNULL,
            ).strip()
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            abort(f"git {' '.join(argv)} failed in {repo} ({exc!r}); the provenance of this "
                  f"run cannot be established, so no artifact is written")

    commit = git("rev-parse", "HEAD")
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        abort(f"git rev-parse HEAD returned {commit!r}, which is not a 40-hex commit id")
    committed_blob = git("rev-parse", f"HEAD:{tool_rel}")
    if len(committed_blob) != 40:
        abort(f"no blob for {tool_rel} at commit {commit}; that commit does not contain this "
              f"tool, so it cannot be this run's provenance")
    worktree = repo / tool_rel
    if not worktree.is_file():
        abort(f"{worktree} does not exist; the running code has no committed counterpart")
    running_blob = git("hash-object", str(worktree))
    if running_blob != committed_blob:
        abort(
            f"SRC-COMMIT PIN VIOLATED: the running {tool_rel} hashes to {running_blob}, but "
            f"commit {commit} contains {committed_blob} for that path. The code that is "
            f"running is not the code that is committed, so writing src_commit={commit} "
            f"would attribute this artifact to a commit that does not produce it - the "
            f"S-0039 section 9 defect, reproduced. Commit the code first, or run from a "
            f"clean checkout; nothing is written"
        )
    return {
        "asserted": True,
        "src_commit": commit,
        "tool_path": tool_rel,
        "committed_blob": committed_blob,
        "running_blob": running_blob,
        "asserted_by": "tools/e0013_extract.py:src_provenance() - the running file's blob is "
                       "compared with the same path's blob at HEAD, so src_commit names a "
                       "commit that CONTAINS the code that produced this artifact",
    }


def abort(reason: str) -> "NoReturn":  # type: ignore[name-defined]
    """An abort is a result (E-00015). It is reported, never repaired into a pass."""
    print(f"ABORT: {reason}", file=sys.stderr)
    raise SystemExit(2)


# --- predicate and normalization -----------------------------------------------------

def full_ply(board: chess.Board) -> int:
    """`board.fullmove_number * 2 + (0 if WHITE else 1) - 1`, exactly as pinned."""
    return board.fullmove_number * 2 + (0 if board.turn == chess.WHITE else 1) - 1


def normalize_fen(board: chess.Board) -> str:
    """Normalized identity: side to move + placement + castling + EP rights.

    The halfmove clock and the fullmove number are EXCLUDED (E-0013 "Split discipline"
    normalized-FEN gate; E-00014/E-00015 Sample Validity use the same normalization "so
    the two records compare like with like"). Anything else makes two records that claim
    to compare like with like compare unlike.
    """
    return " ".join(board.fen().split()[:4])


def is_quiet(board: chess.Board, san_played: str) -> bool:
    """The quiet proxy, evaluated on the position BEFORE the move played.

    Mirrors `tools/e0011_check.py`'s predicate (cited read-only) with the two pinned
    additions E-0013 names. Order of the conjuncts matches the record's pseudocode.
    """
    return (
        (not board.is_check())
        and ("x" not in san_played)
        and (not san_played.endswith("+"))
        and (not san_played.endswith("#"))
        and full_ply(board) >= MIN_FULL_PLY
    )


def split_of(game_id: int) -> str:
    """One draw per game from `random.Random(SPLIT_SALT * 1000003 + game_id)`.

    `rng.random() < TRAIN_FRACTION` is the pinned assignment rule; the map it produces is
    hash-committed BEFORE any fitting job reads the data, so the rule itself is frozen by
    the hash of its output (E-0013 "Split discipline", F6's admissibility precedent).
    """
    draw = random.Random(SPLIT_SALT * SALT_DISTANCE_FACTOR + game_id).random()
    return "train" if draw < TRAIN_FRACTION else "holdout"


def split_map(game_ids: Iterable[int]) -> dict[str, str]:
    return {str(gid): split_of(gid) for gid in sorted(game_ids)}


def game_key(row: dict[str, Any]) -> tuple[str, ...]:
    """`tuple(opening) + tuple(san)` - the pinned game-level identity."""
    return tuple(row["opening"]) + tuple(row["san"])


def white_score(row: dict[str, Any]) -> float:
    """`res` mapped to White's perspective via `a_white`. This is a LABEL read."""
    a_white = bool(row["a_white"])
    res = row["res"]
    if res == "D":
        return 0.5
    if res == "A":
        return 1.0 if a_white else 0.0
    if res == "B":
        return 0.0 if a_white else 1.0
    raise ValueError(f"unknown res {res!r}")


def label_side_to_move(white: float, turn: chess.Color) -> float:
    """B2 sentence 1: the side-to-move frame, and nothing else.

    Mixing frames across the dataset - or expressing a Black-to-move position in the
    White frame - is a FAIL of conjunct (c), not a style choice.
    """
    return white if turn == chess.WHITE else 1.0 - white


@dataclass
class Position:
    game_id: int
    ply_index: int
    fen: str
    norm_fen: str
    stm: str
    y: float | None = None


@dataclass
class Counters:
    """The stage-by-stage counters, kept separate so the arithmetic is auditable
    (E-00015 Test Method step 3: "reporting each stage separately")."""

    games_total: int = 0
    games_used: int = 0
    games_excluded_crash: int = 0
    games_excluded_degenerate: int = 0
    opening_plies_total: int = 0
    plies_san_total: int = 0
    count_bare_ply: int = 0
    count_after_crash_excl: int = 0
    count_after_degenerate_excl: int = 0
    count_usable_distinct: int = 0
    duplicates_removed_by_dedup: int = 0
    undecodable_san: int = 0
    end_counts: dict[str, int] = field(default_factory=dict)


def replay_san_positions(row: dict[str, Any]) -> tuple[list[chess.Board], list[str], int]:
    """Replay `opening` then `san`; return (positions BEFORE each san move, san tokens,
    count of undecodable san tokens).

    E-0011 N4 semantics: `san` = post-opening engine moves only; the `opening` segment is
    replayed to reach the game state but is never itself a candidate position.
    """
    board = chess.Board()
    for uci in row["opening"]:
        move = chess.Move.from_uci(uci)
        if move not in board.legal_moves:
            raise ValueError(f"game {row['game_id']}: illegal opening move {uci}")
        board.push(move)

    boards: list[chess.Board] = []
    sans: list[str] = []
    undecodable = 0
    for token in row["san"]:
        boards.append(board.copy(stack=False))
        sans.append(token)
        try:
            board.push_san(token)
        except Exception:
            undecodable += 1
            break
    return boards, sans, undecodable


def dedup_identity(pos: "Position") -> str:
    """The dedup identity of a position: its NORMALIZED FEN.

    F-U7 (E-0013 S-0037 addendum). This is a named seam on purpose, not an inline
    `pos.norm_fen`, for two reasons that both concern honesty rather than style:

    1. It makes the key legible at the point of use. The single most important fact about
       stage 4 is that this is the SAME key the overlap-0 gate compares; a reader who has to
       find that out by diffing two lines is being asked to do the work the name does.
    2. It gives the self-test a way to run the SUPERSEDED exact-FEN key over identical input
       and demonstrate that the clock-only fixture is RED under it. A regression test that
       has never been seen red does not establish that it would catch the regression.

    The halfmove clock and the fullmove number are deliberately NOT part of this identity.
    They record how a game arrived at a position, not what the position is, and two records
    that differ only in them are the same position - which is exactly what the pre-registered
    normalized-FEN gate has always compared, and what the 27 cross-split leaks were.
    """
    return pos.norm_fen


def dedup_on(positions: Iterable["Position"], key) -> list["Position"]:
    """Stage 4's dedup with an INJECTED key, keeping the survivor rule identical.

    Used by the self-test only, so the old and new keys can be compared over the same
    candidate list with the same survivor rule (first occurrence in iteration order) and the
    key is the ONLY variable. The production path in `extract()` calls `dedup_identity`.
    """
    seen: set[str] = set()
    kept: list[Position] = []
    for pos in positions:
        identity = key(pos)
        if identity in seen:
            continue
        seen.add(identity)
        kept.append(pos)
    return kept


def cross_split_overlap(kept: Iterable["Position"], smap: dict[str, str]) -> int:
    """How many normalized FENs appear on BOTH sides among `kept` - the gate's own count.

    Computed from the survivor list and the split map alone, so a test can evaluate the
    quantity the gate evaluates without having to route through the gate itself.
    """
    train: set[str] = set()
    hold: set[str] = set()
    for pos in kept:
        (train if smap[str(pos.game_id)] == "train" else hold).add(pos.norm_fen)
    return len(train & hold)


def extract(
    rows: list[dict[str, Any]],
    count_only: bool,
    counters: Counters,
) -> tuple[list[Position], dict[int, str]]:
    """Run the four stages. Returns the surviving (deduped) positions and the per-game
    `end`-based exclusion verdict.

    In `count_only` mode the two label keys are removed from each row before anything
    else looks at it, so the pass is incapable of reading a label (E-00015 abort 3).
    """
    counters.games_total = len(rows)
    verdict: dict[int, str] = {}
    bare: list[Position] = []

    for row in rows:
        gid = int(row["game_id"])
        if count_only:
            for key in LABEL_KEYS:
                row.pop(key, None)  # the pass must be incapable, not merely unwilling

        end = row["end"]
        if end not in END_VOCABULARY:
            abort(f"game {gid}: end {end!r} outside the R-0016 vocabulary")
        counters.end_counts[end] = counters.end_counts.get(end, 0) + 1
        counters.opening_plies_total += len(row["opening"])
        counters.plies_san_total += len(row["san"])

        boards, sans, undecodable = replay_san_positions(row)
        counters.undecodable_san += undecodable

        # The exclusions are FLAGS, not early exits. Stage 1 is the BARE predicate over
        # every game - that is the figure comparable to the checker's 76,593, which was
        # measured with no crash exclusion and no degenerate exclusion - so the quiet loop
        # must run for excluded games too, and later stages only stop counting them.
        is_crash = end == "crash"
        is_degenerate = end == "mate" and len(row["san"]) <= 6
        if is_crash:
            verdict[gid] = "crash"
            counters.games_excluded_crash += 1
        elif is_degenerate:
            verdict[gid] = "degenerate"
            counters.games_excluded_degenerate += 1
        else:
            verdict[gid] = "used"
            counters.games_used += 1

        white = None if count_only else white_score(row)
        for ply_index, (board, san) in enumerate(zip(boards, sans)):
            if not is_quiet(board, san):
                continue
            counters.count_bare_ply += 1
            if is_crash:
                continue
            counters.count_after_crash_excl += 1
            if is_degenerate:
                continue
            counters.count_after_degenerate_excl += 1
            bare.append(
                Position(
                    game_id=gid,
                    ply_index=ply_index,
                    fen=board.fen(),
                    norm_fen=normalize_fen(board),
                    stm="w" if board.turn == chess.WHITE else "b",
                    y=None if white is None else label_side_to_move(white, board.turn),
                )
            )


    # Stage 4 - GLOBAL dedup on the NORMALIZED FEN, before the split. The survivor is the
    # FIRST occurrence in (game_id, ply_index) order; that pin is what makes "the surviving
    # copy's game_id determines the split" deterministic rather than merely stated, and it
    # is published in the report so it is visible instead of implied.
    #
    # F-U7 (E-0013 S-0037 addendum). This key was `pos.fen` - the exact six-field FEN, clocks
    # INCLUDED - while the overlap-0 gate compares `normalize_fen`, the four-field FEN. A
    # dedup key strictly FINER than the gate's comparison key cannot entail the invariant the
    # gate verifies, so the gate could only ever pass by coincidence; K+R vs K endgames, with
    # a small reachable-position space, supplied the coincidence's failure (27 collisions).
    # Keying on `pos.norm_fen` is the SAME key the gate compares, which is what makes the gate
    # true BY CONSTRUCTION rather than by luck.
    #
    # The halfmove clock and the fullmove number are NOT part of a position's identity: they
    # are bookkeeping about how the game got there, not about what the position IS. Excluding
    # them is what the pre-registered normalization already says, and making the dedup key and
    # the gate agree is the whole point of this change. The gate itself is UNCHANGED - it is
    # still blocking, still at both pre-registered levels, and is now a regression test on
    # this code rather than a hope about the data.
    seen: set[str] = set()
    kept: list[Position] = []
    for pos in bare:
        identity = dedup_identity(pos)
        if identity in seen:
            continue
        seen.add(identity)
        kept.append(pos)
    counters.count_usable_distinct = len(kept)
    counters.duplicates_removed_by_dedup = counters.count_after_degenerate_excl - len(kept)
    return kept, verdict


# --- leakage gates -------------------------------------------------------------------

def run_gates(
    kept: list[Position],
    rows_by_id: dict[int, dict[str, Any]],
    smap: dict[str, str],
) -> dict[str, Any]:
    """The blocking overlap-0 gate, at both levels E-0013 names.

    Game level: `tuple(opening) + tuple(san)` of every holdout game against the train
    game set - this catches *duplicated game content* across the split, which a game-id
    split alone cannot catch.
    Normalized-FEN level: the position-relative / threefold-cluster leakage check. Since
    F-U7 the dedup key IS this normalization, so the check is no longer stricter than the
    dedup: global-before-split dedup on the same key leaves at most one survivor per
    normalized FEN in the corpus, and that survivor's game_id alone decides the split, so a
    non-zero count here is a FAILURE OF THE IMPLEMENTATION rather than a property of the
    data. It is retained as a blocking regression check and is reported as measured - never
    absorbed by re-running with a different normalization.
    """
    train_games: set[int] = set()
    holdout_games: set[int] = set()
    for gid, split in smap.items():
        (train_games if split == "train" else holdout_games).add(int(gid))

    train_keys = {game_key(rows_by_id[g]) for g in train_games if g in rows_by_id}
    holdout_keys = {game_key(rows_by_id[g]) for g in holdout_games if g in rows_by_id}
    game_overlap = len(train_keys & holdout_keys)

    train_norms: set[str] = set()
    holdout_norms: set[str] = set()
    for pos in kept:
        (train_norms if smap[str(pos.game_id)] == "train" else holdout_norms).add(pos.norm_fen)
    norm_overlap = len(train_norms & holdout_norms)

    return {
        "game_level_overlap": game_overlap,
        "normalized_fen_overlap": norm_overlap,
        "train_games": len(train_games),
        "holdout_games": len(holdout_games),
        "train_norm_fens": len(train_norms),
        "holdout_norm_fens": len(holdout_norms),
        "overlap_zero": game_overlap == 0 and norm_overlap == 0,
    }


def salt_distances() -> dict[str, int]:
    """E-0013 F10, recomputed rather than cited: `|S - S'| * 1000003` per prior salt.

    The admissibility rule F6 pins is `abs(S - S') * 1000003 > cap - 1`; the smallest cap
    this project has used is 2,000, so 1,999 is the binding floor on the right-hand side.
    """
    return {str(prior): abs(SPLIT_SALT - prior) * SALT_DISTANCE_FACTOR for prior in PRIOR_SALTS}


def scope_floor_verdict(train_count: int, floor: int = SCOPE_FLOOR) -> dict[str, Any]:
    """The 30,000 scope floor, evaluated mechanically on the TRAIN-side count.

    E-0013 conjunct (a) / B6 sentence 4 / E-00015 rules 1-2. Both branches are returned as
    DATA, not as an exit code, because recording the verdict in a record is the owner seat's
    act and this tool only computes it. The headroom is published alongside the branch so a
    reader can see how close the call came - which is the sensitivity the band retirement
    actually cost, stated as a number rather than as a reassurance.

    `floor` is a parameter so the self-test can demonstrate both branches and the boundary
    with no route to moving the real value: `SCOPE_FLOOR` is a module constant, the report
    publishes it as `scope_floor.floor`, and nothing else in this file writes it.
    """
    return {
        "floor": floor,
        "count_usable_distinct_train": train_count,
        "headroom": train_count - floor,
        "holds": train_count >= floor,
        "rule_output": ("all-terms-scope-stands" if train_count >= floor
                        else "all-terms-claim-WITHDRAWN"),
    }


def accounting_identities(counters: Counters, splits: dict[str, int],
                          distinct_norm_fens: int) -> dict[str, bool]:
    """The EXACT identities that stand in place of the retired band.

    Every one of these is arithmetic between quantities this run measured, so none of them
    rots when the dedup key changes and none can be satisfied by luck. That is the whole
    reason they replace the band: the band's diagnostic power came from its endpoints being
    derived from quantities INDEPENDENT of the number being checked, and the identities get
    the same kind of power from being exact instead of estimated. They introduce no
    threshold and therefore no new number to be wrong about.

    `one_survivor_per_normalized_fen` answers the question Ruling 1 says was lost: it ties
    the survivor count to the distinctness of the dedup key rather than to any expected
    magnitude, so a future key change that quietly stops deduplicating is caught at once
    instead of waiting for a magnitude cross-check to notice.
    """
    return {
        "usable_equals_after_degenerate_minus_dedup":
            counters.count_after_degenerate_excl - counters.duplicates_removed_by_dedup
            == counters.count_usable_distinct,
        "usable_equals_train_plus_holdout":
            splits["train"] + splits["holdout"] == counters.count_usable_distinct,
        "stages_monotone_non_increasing":
            counters.count_bare_ply >= counters.count_after_crash_excl
            >= counters.count_after_degenerate_excl >= counters.count_usable_distinct,
        "dedup_removed_at_least_zero": counters.duplicates_removed_by_dedup >= 0,
        "one_survivor_per_normalized_fen":
            distinct_norm_fens == counters.count_usable_distinct,
    }


def identities_hold(identities: dict[str, bool]) -> bool:
    return all(identities.values())


def corpus_block(mode: str, positions_sha: str, rows: int, null_y_rows: int,
                 label_frame_uniform: bool | None) -> dict[str, Any]:
    """WHICH mode produced this artifact, and therefore WHICH digest is a corpus digest.

    S-0039 Ruling 2, second weakness: the artifact on disk was a `--count-only` run whose
    rows carry `y: null`, so its SHA-256 was one specific number (`ac8c92f0...`) that must
    never be presented as the digest of the corpus a fitter will read. The full extraction
    is a DIFFERENT file with a DIFFERENT digest, so the fix is not to publish one digest
    more carefully - it is to give the corpus digest its own field and leave it `null`, with
    a reason, whenever the bytes cannot be a corpus at all.
    """
    labelled = mode == MODE_LABELLED
    return {
        "mode": mode,
        "is_fitter_corpus": labelled,
        "fitter_corpus_sha256": positions_sha if labelled else None,
        "fitter_corpus_null_reason": None if labelled else
            "count-only pass: no label field was read (E-00015 abort 3), so every row's y is "
            "null and this file is NOT the corpus a fitter may read",
        "positions_sha256_kind": FITTER_CORPUS_KIND if labelled else COUNT_ONLY_PASS_KIND,
        "rows": rows,
        "rows_with_null_y": null_y_rows,
        "y_values_are_labels": labelled,
        "label_frame_uniform": label_frame_uniform,
        "read_this_before_quoting_a_digest":
            "in count-only mode positions_sha256 is the digest of a MEASUREMENT; only a "
            "labelled artifact's digest is the fitter's corpus digest",
    }


def assert_mode_matches_bytes(mode: str, kept: list["Position"],
                              label_frame_uniform: bool | None) -> int:
    """The mode label must be TRUE OF THE BYTES. Checked at write time, not described.

    A report that says `labelled` while every `y` is null would publish a corpus digest over
    a file that cannot be fitted. A report that says `count-only` while some `y` is populated
    would leak a label into a measurement pass, which is E-00015 abort 3. And a labelled run
    whose frame is not uniform is a FAIL of conjunct (c) under B2 sentence 1, which must not
    be published as a fitter corpus under any circumstances. A description that can be false
    is worse than no description, so this is a gate, and it returns the measured null count.
    """
    nulls = sum(1 for pos in kept if pos.y is None)
    if mode == MODE_COUNT_ONLY:
        if nulls != len(kept):
            abort(f"declared mode is {mode} but {len(kept) - nulls} of {len(kept)} rows carry "
                  f"a label; E-00015 abort 3 forbids publishing a label from the count-only "
                  f"pass, and a digest over labelled bytes must not be presented as a "
                  f"measurement")
        return nulls
    if nulls:
        abort(f"declared mode is {mode} but {nulls} of {len(kept)} rows carry a null label; "
              f"a partially labelled corpus cannot be fitted and must not be pinned as one")
    if label_frame_uniform is not True:
        abort("declared mode is labelled but the side-to-move frame is not uniform (B2 "
              "sentence 1); a mixed frame is a FAIL of conjunct (c) and must not be "
              "published as a fitter corpus")
    return nulls


def build_report(
    args: argparse.Namespace,
    rows: list[dict[str, Any]],
    counters: Counters,
    kept: list[Position],
    smap: dict[str, str],
    gates: dict[str, Any],
    dataset_sha256: str,
    dataset_bytes: int,
    splits: dict[str, int],
    side_counts: dict[str, int],
    label_frame_uniform: bool | None,
    label_reason: str | None,
    provenance: dict[str, Any],
    identities: dict[str, bool],
    mode: str,
    scope_floor: int = SCOPE_FLOOR,
) -> dict[str, Any]:
    train = splits["train"]
    report: dict[str, Any] = {
        "format": REPORT_FORMAT,
        "tool": "tools/e0013_extract.py",
        "mode": mode,
        # The commit that CONTAINS the code that produced this report, asserted at write
        # time by comparing the running file's blob with the same path's blob at HEAD. It is
        # not `git rev-parse HEAD` on its own, which is how the previous artifact came to
        # name `9f6574c` - the parent of the commit holding the key change it was produced
        # with. See src_provenance() and the `provenance` block below.
        "src_commit": provenance["src_commit"],
        "provenance": provenance,
        "python": sys.version.split()[0],
        "python_chess": chess.__version__,
        "dataset": {
            "path": str(Path(args.dataset).resolve()),
            "sha256": dataset_sha256,
            "sha256_expected": args.expected_dataset_sha256,
            "bytes": dataset_bytes,
            "rows": len(rows),
        },
        # Every pin the report's numbers depend on, stated so a reader can re-derive them.
        "extraction_pin": {
            "filter_stages": [
                "QUIET(not check on the position BEFORE the move; no 'x'; no '+'/'#' suffix; full_ply >= 10)",
                "exclude end == 'crash'",
                "exclude end == 'mate' and len(san) <= 6",
                "GLOBAL dedup on the NORMALIZED FEN, before the split (F9)",
            ],
            "candidate_segment": "san only; the opening segment is never a candidate",
            "full_ply_formula": "board.fullmove_number * 2 + (0 if WHITE else 1) - 1",
            "split_salt": SPLIT_SALT,
            "split_rule": "random.Random(SPLIT_SALT * 1000003 + game_id).random() < 0.8",
            "train_fraction": TRAIN_FRACTION,
            # F-U7: the dedup identity of a position is its NORMALIZED FEN. The clock is
            # NOT part of that identity - it says how the game reached the position, not
            # what the position is. This is the same key `overlap_gate_key` names, which is
            # what makes the normalized-FEN gate true by construction instead of by luck.
            "dedup_key": "normalized FEN (side to move + piece placement + castling/EP; the halfmove clock and the fullmove number are NOT part of the identity)",
            "dedup_key_fields": ["side to move", "piece placement", "castling rights", "EP square"],
            "dedup_key_excludes": ["halfmove clock", "fullmove number"],
            "dedup_key_equals_gate_key": True,
            "dedup_order": "GLOBAL, before the split",
            "dedup_survivor_rule": "first occurrence in (game_id, ply_index) order",
            "overlap_gate_key": "normalized FEN = placement + side to move + castling + EP",
            "game_identity": "tuple(opening) + tuple(san)",
            "label_frame": "side to move (B2 sentence 1)",
            "label_mapping": "res -> white_score {A:1,B:0,D:0.5} via a_white; y = white_score if WHITE else 1 - white_score",
        },
        "salt_distances": salt_distances(),
        # E-00015 "Test Method" step 3, emitted under the pre-registered names.
        "counts": {
            "plies_san_total": counters.plies_san_total,
            "opening_plies_total": counters.opening_plies_total,
            "count_bare_ply": counters.count_bare_ply,
            "count_after_crash_excl": counters.count_after_crash_excl,
            "count_after_degenerate_excl": counters.count_after_degenerate_excl,
            "count_usable_distinct": counters.count_usable_distinct,
            "count_usable_distinct_train": train,
            "count_usable_distinct_holdout": splits["holdout"],
            # E-00015 names this field explicitly. No inner carve is taken by this pass, so
            # it is the outer TRAIN-side figure - which is exactly what the scope floor is
            # evaluated on. Emitted rather than omitted (E-00015 abort 7).
            "count_usable_distinct_train_TRAIN_SIDE_ONLY": train,
            "games_used": counters.games_used,
            "games_excluded_crash": counters.games_excluded_crash,
            "games_excluded_degenerate": counters.games_excluded_degenerate,
            "duplicates_removed_by_dedup": counters.duplicates_removed_by_dedup,
            "undecodable_san": counters.undecodable_san,
            "end_counts": dict(sorted(counters.end_counts.items())),
        },
        "labels": {
            "label_frame_uniform": label_frame_uniform,
            "null_reason": label_reason,
            "count_positions_white_to_move": side_counts["w"],
            "count_positions_black_to_move": side_counts["b"],
            "label_construction_step": "tools/e0013_label.py - the separate TRAIN-ONLY step "
                                       "that builds the labelled corpus out of these pinned "
                                       "artifacts, and that enforces per-game constancy and "
                                       "the side-to-move frame, which this tool does not",
            "label_is_result_only": True,
            "label_is_result_only": True,
            "label_is_game_constant": True,
        },
        "gates": gates,
        # THE BAND IS GONE, not renamed, not re-derived, and not nulled in place. The key is
        # ABSENT on purpose: a consumer that does `report["band"]["lo"]` gets a KeyError and
        # is forced to notice, and one that does `report.get("band")` gets None rather than a
        # dict-shaped object that reads as live. The retirement itself is recorded below.
        "retired_instruments": [
            {
                "name": "yield band",
                "retired_by": "E-0013 Addendum 2 (S-0039), Ruling 1 / F-U10",
                "retired_on": "2026-09-27",
                "what_it_was": "lo 75600 / hi 76587, a per-run comparison, "
                               "is_pass_criterion false",
                "why": "a yield-plausibility cross-check on the pipeline, NOT a quality "
                       "threshold; both endpoints were functions of the OLD dedup key's "
                       "expected output; it misfired under the old key too (76,593 against "
                       "hi 76,587), so no measurement of this corpus ever landed inside it",
                "replaced_by": "the directly measured count_usable_distinct with "
                               "duplicates_removed_by_dedup beside it; the UNCHANGED 30,000 "
                               "scope floor with its headroom; the blocking overlap-0 gates; "
                               "and the exact accounting_identities - none of which is a "
                               "band, and none of which introduces a new number",
                "is_live": False,
            }
        ],
        # E-0013 conjunct (a) / B6 sentence 4 / E-00015 rule 1-2. The rule is APPLIED here
        # mechanically so it is auditable; recording the verdict in a record remains the
        # owner's act, not this tool's. This floor is NOT the retired band: it is the
        # pre-registered quality/scope rule on the TRAIN side, it is not renegotiable, and
        # its headroom is published so a reader can see how close the call came.
        "scope_floor": dict(
            # `scope_floor` is the pinned SCOPE_FLOOR on every real run. It is a parameter
            # only so the self-test can drive the OTHER branch of the rule end to end - a
            # floor that has only ever been seen passing has not been tested. The command
            # line has no flag that reaches it: `parse_args` does not define one, and the
            # self-test asserts that, so there is no route from a run to moving the value.
            scope_floor_verdict(train, scope_floor),
            evaluated_on="count_usable_distinct_train (outer TRAIN side)",
            applied_by="E-0013's owner seat; this tool reports the branch, it does not decide",
            not_renegotiable=True,
            is_the_retired_band=False,
        ),
        # What replaced the band: exact arithmetic, checked and published, never a
        # projection. A false identity is a reportable finding, so `run()` gates on it.
        "accounting_identities": identities,
        "accounting_identities_hold": identities_hold(identities),
    }
    return report


def write_bytes(path: Path, data: bytes) -> str:
    """Binary write, LF-only, no BOM. The environment hazards this project has already
    recorded (PowerShell `>` emitting UTF-16; `Set-Content -Encoding utf8` emitting a BOM)
    are not reachable from here, and `--check` verifies the result byte for byte."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return sha256_bytes(data)


def run(args: argparse.Namespace) -> int:
    # The mode, resolved ONCE and used everywhere, so the string in the report, the string
    # in the digest's name and the string the write-time gate checks are the same object.
    mode = MODE_COUNT_ONLY if args.count_only else MODE_LABELLED

    # PROVENANCE, asserted BEFORE anything is written. A synthetic (`--allow-synthetic`) run
    # publishes an explicit sentinel instead: the self-test's temporary corpora must not
    # depend on this repository's working tree being clean, and a real-looking hash that
    # happened to be true would be a worse answer than a sentinel that is obviously not a
    # commit. Everything else pins, and pins or aborts.
    provenance = dict(SYNTHETIC_PROVENANCE) if args.allow_synthetic else src_provenance()

    dataset = Path(args.dataset)
    if not dataset.exists():
        abort(f"dataset not found: {dataset}")
    dataset_bytes = dataset.stat().st_size
    dataset_sha256 = sha256_file(dataset)
    if dataset_sha256 != args.expected_dataset_sha256:
        abort(
            f"dataset SHA-256 mismatch: measured {dataset_sha256}, "
            f"pinned {args.expected_dataset_sha256} - the data is not the pinned dataset"
        )

    rows: list[dict[str, Any]] = []
    for line in dataset.read_bytes().decode("utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    if len(rows) != DATASET_ROWS and not args.allow_synthetic:
        abort(f"expected {DATASET_ROWS} rows, found {len(rows)}")

    rows_by_id = {int(r["game_id"]): r for r in rows}
    counters = Counters()
    kept, verdict = extract(rows, args.count_only, counters)

    smap = split_map(rows_by_id)
    splits = {"train": 0, "holdout": 0}
    side_counts = {"w": 0, "b": 0}
    for pos in kept:
        splits[smap[str(pos.game_id)]] += 1
        side_counts[pos.stm] += 1

    # B2: the frame is checked, not assumed. Every label is recomputed from the row and
    # compared with what the extractor wrote, so a mixed frame cannot pass silently.
    label_frame_uniform: bool | None = None
    label_reason: str | None = None
    if args.count_only:
        label_reason = "count-only pass: no label field is read (E-00015 abort 3)"
    else:
        label_frame_uniform = True
        for pos in kept:
            expected = label_side_to_move(white_score(rows_by_id[pos.game_id]), chess.WHITE if pos.stm == "w" else chess.BLACK)
            if pos.y != expected:
                label_frame_uniform = False
                break

    gates = run_gates(kept, rows_by_id, smap)

    # The exact accounting identities are a GATE, not a decoration. They are what replaced
    # the retired band, and an instrument that reports a failure without acting on it is the
    # permanently-red instrument problem all over again. A false identity is a FINDING to
    # report, never a new baseline to adopt.
    identities = accounting_identities(
        counters, splits, len({pos.norm_fen for pos in kept})
    )
    if not identities_hold(identities):
        abort(
            "EXACT ACCOUNTING IDENTITIES VIOLATED: "
            + json.dumps(identities, sort_keys=True)
            + " - the stage counts do not close, which means a counter or the dedup has "
              "moved. This is a FINDING to report, not a baseline to re-derive, and no "
              "artifact is written"
        )

    # The mode label is checked against the bytes, before the digest is published. A
    # `count-only` pass whose rows carry labels, or a `labelled` pass whose rows do not, is
    # exactly the confusion this gate exists to make impossible.
    null_y_rows = assert_mode_matches_bytes(mode, kept, label_frame_uniform)

    # The floor the report will evaluate. On every real run this is `SCOPE_FLOOR`; the
    # attribute is absent from anything `parse_args` produces, and the self-test asserts
    # that, so no command line can move the non-negotiable value. It exists only so the
    # self-test can reach the STAND branch of the rule.
    scope_floor = getattr(args, "scope_floor", None) or SCOPE_FLOOR
    report = build_report(
        args, rows, counters, kept, smap, gates, dataset_sha256, dataset_bytes,
        splits, side_counts, label_frame_uniform, label_reason,
        provenance, identities, mode, scope_floor,
    )
    report["exclusion_verdict_counts"] = {
        k: sum(1 for v in verdict.values() if v == k) for k in ("used", "crash", "degenerate")
    }

    out_dir = Path(args.out_dir)
    lines = []
    for pos in kept:
        lines.append(json.dumps({
            "game_id": pos.game_id,
            "ply_index": pos.ply_index,
            "fen": pos.fen,
            "norm_fen": pos.norm_fen,
            "stm": pos.stm,
            "y": pos.y,
        }, sort_keys=True, separators=(",", ":"), ensure_ascii=True))
    positions_bytes = ("\n".join(lines) + "\n").encode("utf-8") if lines else b""
    map_obj = {
        "format": SPLIT_MAP_FORMAT,
        "split_salt": SPLIT_SALT,
        "train_fraction": TRAIN_FRACTION,
        "rule": "random.Random(SPLIT_SALT * 1000003 + game_id).random() < 0.8",
        "map": smap,
    }
    map_bytes = canonical_json(map_obj)
    map_sha = sha256_bytes(map_bytes)
    positions_sha = sha256_bytes(positions_bytes)
    report["artifacts"] = {
        "positions_lines": len(lines),
        "positions_sha256": positions_sha,
        # The name of the digest says what the digest is OF. In count-only mode this is a
        # measurement's digest, and saying so in the key is what stops a reader from
        # promoting it to "the corpus" by accident.
        "positions_sha256_kind": (FITTER_CORPUS_KIND if mode == MODE_LABELLED
                                  else COUNT_ONLY_PASS_KIND),
        "split_map_sha256": map_sha,
        "split_map_sha256_is_mode_independent": True,
    }
    # The corpus block answers the only question a digest cannot answer about itself: is this
    # the thing a fitter reads? See corpus_block()'s docstring for why the count-only digest
    # is published at all and the corpus digest is not.
    report["corpus"] = corpus_block(mode, positions_sha, len(lines), null_y_rows,
                                    label_frame_uniform)
    # pinned dataset only. The self-test passes small synthetic row sets whose game ids do
    # not span the pinned corpus, so their maps are legitimately different digests and the
    # assertion would be meaningless there.
    split_map_invariant: bool | None = None
    if not args.allow_synthetic:
        split_map_invariant = map_sha == SPLIT_MAP_SHA256_EXPECTED
        report["split_map_invariance"] = {
            "expected_sha256": SPLIT_MAP_SHA256_EXPECTED,
            "measured_sha256": map_sha,
            "unchanged": split_map_invariant,
            "asserted_by": "F-U9; the map is a pure function of (SPLIT_SALT, game_id) and its "
                           "hashed object contains no dedup-derived quantity",
        }
        if not split_map_invariant:
            abort(
                f"split_map_sha256 INVARIANCE VIOLATED: measured {map_sha}, "
                f"pre-registered {SPLIT_MAP_SHA256_EXPECTED}. The salt, the train fraction or "
                f"the assignment rule has moved, which the S-0037 ruling does not authorise. "
                f"This is a FINDING to report, not a new baseline to adopt"
            )

    # The overlap-0 gate is checked BEFORE anything is written. It is a blocking gate, and a
    # gate that aborts after the artifacts exist is not a gate: `positions.jsonl` would sit on
    # disk, complete and loadable, for any later step to consume - which is precisely what
    # "FAIL before fitting" forbids. On FAIL the counts are still printed below, so the
    # measurement is reported as measured rather than being lost with the abort.
    if not gates["overlap_zero"]:
        gate_failed = True
    else:
        gate_failed = False

    if not args.dry_run and not gate_failed:
        write_bytes(out_dir / "positions.jsonl", positions_bytes)
        write_bytes(out_dir / "split_map.json", map_bytes)
        write_bytes(out_dir / "report.json", canonical_json(report))

    c = report["counts"]
    print(f"mode={report['mode']} commit={report['src_commit'][:7]}")
    print(f"dataset_sha256={dataset_sha256} rows={len(rows)}")
    for key in (
        "plies_san_total", "count_bare_ply", "count_after_crash_excl",
        "count_after_degenerate_excl", "count_usable_distinct",
        "count_usable_distinct_train", "count_usable_distinct_holdout",
        "duplicates_removed_by_dedup", "games_used",
        "games_excluded_crash", "games_excluded_degenerate",
    ):
        print(f"{key}={c[key]}")
    print(f"label_frame_uniform={label_frame_uniform} w={side_counts['w']} b={side_counts['b']}")
    print(f"gates={json.dumps(gates, sort_keys=True)}")
    # No `band=` line. The band was retired, and printing a retired field is how a retired
    # field keeps being read. What replaced it is printed by name instead.
    print(f"retired_instruments="
          f"{json.dumps([r['name'] for r in report['retired_instruments']], sort_keys=True)}")
    print(f"accounting_identities={json.dumps(identities, sort_keys=True)}")
    print(f"scope_floor={json.dumps(report['scope_floor'], sort_keys=True)}")
    print(f"corpus={json.dumps(report['corpus'], sort_keys=True)}")
    print(f"positions_sha256={report['artifacts']['positions_sha256']} "
          f"({report['artifacts']['positions_sha256_kind']})")
    print(f"split_map_sha256={report['artifacts']['split_map_sha256']}")
    if split_map_invariant is not None:
        print(f"split_map_invariance_unchanged={split_map_invariant} "
              f"(expected {SPLIT_MAP_SHA256_EXPECTED})")
    if not args.dry_run and not gate_failed:
        print(f"report_sha256={sha256_file(out_dir / 'report.json')}")
    if gate_failed:
        abort(
            f"overlap-0 gate FAILED (game_level={gates['game_level_overlap']}, "
            f"normalized_fen={gates['normalized_fen_overlap']}) - FAIL before fitting; "
            f"no artifact was written"
        )
    return 0


# --- self-test (synthetic only; the real dataset is never touched) --------------------

OPENING_PLIES = 10


def _seeded_game(game_id: int, n_plies: int) -> tuple[list[str], list[str]]:
    """A distinct, deterministic, legal game per `game_id`.

    A shared template would have made different games byte-identical, which the extractor
    correctly flags as cross-split leakage - so each game is drawn from its own RNG stream.
    Immediately-terminal candidate moves are rejected, the same rule `tools/e0011_generate.py`
    uses for its ten-ply opening.
    """
    rng = random.Random(0xE0013 + game_id)

    def pick(board: chess.Board) -> chess.Move | None:
        choices = list(board.legal_moves)
        rng.shuffle(choices)
        for candidate in choices:
            probe = board.copy(stack=False)
            probe.push(candidate)
            if not probe.is_game_over():
                return candidate
        return None

    board = chess.Board()
    opening: list[str] = []
    for _ in range(OPENING_PLIES):
        move = pick(board)
        if move is None:
            break
        opening.append(move.uci())
        board.push(move)

    san: list[str] = []
    while len(san) < n_plies:
        move = pick(board)
        if move is None:
            break
        san.append(board.san(move))
        board.push(move)
    return opening, san


def synthetic_row(game_id: int, n_plies: int, end: str, res: str = "D",
                  a_white: bool = True) -> dict[str, Any]:
    opening, san = _seeded_game(game_id, n_plies)
    return {
        "game_id": game_id, "campaign_salt": 20260922, "seed_int": game_id,
        "opening": opening, "a_white": a_white, "b_white": not a_white,
        "eval_stage_a": 6, "eval_stage_b": 6, "binary_sha256": "0" * 64,
        "src_commit": "0" * 40, "tc": "100ms+100ms inc",
        "tc_command": "go wtime 1500 btime 1500 winc 100 binc 100",
        "time_started": "2026-09-24T00:00:00.000000Z",
        "time_finished": "2026-09-24T00:01:00.000000Z",
        "res": res, "end": end, "end_seconds": 60.0, "plies": len(opening) + len(san),
        "san": san, "crash_incident": False, "crash_incident_text": "",
    }


def clock_only_row(game_id: int, extra_shuffles: int) -> dict[str, Any]:
    """A synthetic row whose positions are reachable at DIFFERENT plies than its twin's.

    F-U8's permanent regression fixture. Two rows built with different `extra_shuffles` play
    the same normalized positions but reach them at different plies, so the two copies of
    each shared position agree in placement, side to move, castling and EP square and differ
    ONLY in the halfmove clock and the fullmove number.

    That is the exact shape of the 27 cross-split leaks S-0036 found in `K+R vs K` endgames,
    and it is the shape the pre-fix self-test could not express: its duplicate copies were
    byte-identical including clocks, so the old finer key caught them by luck. Here the old
    key cannot see them at all, and the new key removes them structurally.

    The `Nf3/Nf6/Ng1/Ng8` shuffle is a legal four-ply cycle: it returns to the identical
    position with a different clock, which is what manufactures the clock-only duplicate
    without inventing an illegal or impossible game.

    The extra cycles go in the OPENING, not the san, for one decisive reason: the opening
    segment is never a candidate (E-0011 N4 semantics), so a twin with extra opening cycles
    begins its san segment on the SAME board but at a different ply. Had the cycles gone in
    the san instead, the two games would share an identical prefix and their first copies
    would be byte-identical - which is precisely the blind spot this fixture exists to avoid,
    and the reason an earlier draft of it wrongly failed.
    """
    opening = ["e2e4", "e7e5", "d2d4", "d7d5", "h2h3", "h7h6",
               "g2g3", "g7g6", "f1g2", "f8g7"]
    # The opening segment is replayed as UCI (`replay_san_positions`); the san segment as SAN.
    # The knight cycle is chosen over a rook cycle because rook shuffles DESTROY castling
    # rights, which would change the normalized FEN and silently defeat the fixture.
    shuffle_uci = ["g1f3", "g8f6", "f3g1", "f6g8"]
    shuffle = ["Nf3", "Nf6", "Ng1", "Ng8"]
    tail = ["Nc3", "Nc6", "Nf3", "Nf6"]
    san = shuffle + tail
    full_opening = opening + shuffle_uci * extra_shuffles
    return {
        "game_id": game_id, "campaign_salt": 20260922, "seed_int": game_id,
        "opening": full_opening, "a_white": True, "b_white": False,
        "eval_stage_a": 6, "eval_stage_b": 6, "binary_sha256": "0" * 64,
        "src_commit": "0" * 40, "tc": "100ms+100ms inc",
        "tc_command": "go wtime 1500 btime 1500 winc 100 binc 100",
        "time_started": "2026-09-24T00:00:00.000000Z",
        "time_finished": "2026-09-24T00:01:00.000000Z",
        "res": "D", "end": "plycap", "end_seconds": 60.0,
        "plies": len(full_opening) + len(san),
        "san": san, "crash_incident": False, "crash_incident_text": "",
    }


def candidate_positions(rows: list[dict[str, Any]]) -> list[Position]:
    """The stage-1..3 candidates for `rows`, WITHOUT the stage-4 dedup.

    Exposed so a test can hand the identical candidate list to two different dedup keys and
    attribute any difference in outcome to the key alone. Replaying here rather than
    reaching into `extract()` keeps the production path free of test-only branches.
    """
    out: list[Position] = []
    for row in rows:
        boards, sans, _ = replay_san_positions(row)
        for ply_index, (board, san) in enumerate(zip(boards, sans)):
            if not is_quiet(board, san):
                continue
            out.append(Position(
                game_id=int(row["game_id"]),
                ply_index=ply_index,
                fen=board.fen(),
                norm_fen=normalize_fen(board),
                stm="w" if board.turn == chess.WHITE else "b",
            ))
    return out


def selftest() -> int:
    import tempfile

    checks: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, bool(ok), detail))

    # --- predicate, on hand-built boards -----------------------------------------------
    check("predicate: startpos is under the ply floor", is_quiet(chess.Board(), "Nf3") is False)
    b2 = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 20")
    check("predicate: quiet knight move at ply 39", is_quiet(b2, "Nf3") is True)
    check("predicate: capture rejected", is_quiet(b2, "Nxe5") is False)
    check("predicate: checking move rejected", is_quiet(b2, "Nf3+") is False)
    check("predicate: mating move rejected", is_quiet(b2, "Qh5#") is False)
    b3 = chess.Board("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w - - 1 3")
    check("predicate: side-to-move in check rejected", is_quiet(b3, "Kg1") is False)
    b4 = chess.Board("k7/8/8/8/8/8/8/K7 w - - 99 60")
    check("predicate: no check/capture/suffix above the floor is quiet", is_quiet(b4, "Kb2") is True)

    # --- normalization -----------------------------------------------------------------
    n1 = chess.Board("r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 4 4")
    n2 = chess.Board("r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 9")
    n3 = chess.Board("r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR b KQkq - 4 4")
    check("normalize_fen: clock and fullmove excluded", normalize_fen(n1) == normalize_fen(n2))
    check("normalize_fen: exactly four fields", len(normalize_fen(n1).split()) == 4)
    check("normalize_fen: side to move is part of the identity", normalize_fen(n1) != normalize_fen(n3))

    # --- labels ------------------------------------------------------------------------
    check("label: A and a_white -> 1.0", white_score({"res": "A", "a_white": True}) == 1.0)
    check("label: A and not a_white -> 0.0", white_score({"res": "A", "a_white": False}) == 0.0)
    check("label: B and not a_white -> 1.0", white_score({"res": "B", "a_white": False}) == 1.0)
    check("label: B and a_white -> 0.0", white_score({"res": "B", "a_white": True}) == 0.0)
    check("label: D -> 0.5", white_score({"res": "D", "a_white": True}) == 0.5)
    check("label: black-to-move flips the White-frame score", label_side_to_move(1.0, chess.BLACK) == 0.0)
    check("label: white-to-move keeps it", label_side_to_move(0.25, chess.WHITE) == 0.25)

    # --- split map ---------------------------------------------------------------------
    m1 = canonical_json({"format": SPLIT_MAP_FORMAT, "map": split_map(range(200))})
    m2 = canonical_json({"format": SPLIT_MAP_FORMAT, "map": split_map(range(200))})
    check("split map: deterministic across runs", m1 == m2, sha256_bytes(m1)[:16])
    smap1000 = split_map(range(1000))
    train_n = sum(1 for v in smap1000.values() if v == "train")
    check("split map: 1,000 ids land near 80/20", 760 <= train_n <= 840, f"train={train_n}")
    distances = salt_distances()
    check("F10: every prior salt clears the 1,999 floor", all(v > 1999 for v in distances.values()), str(distances))
    check("F10: distance to 20260924 == 2,000,006", distances["20260924"] == 2000006)

    # --- the RETIRED band, and the floor that was NOT retired --------------------------
    # The band's ABSENCE is itself under test. A retired instrument that can reappear is
    # not retired, so (a) the endpoints are checked to be absent from this tool's SOURCE,
    # (b) no report key named `band` is constructed anywhere in it, and (c) the helper that
    # computed the comparison is checked to be gone. All three are cheap and all three can
    # fail, which is what stops a later edit from quietly reintroducing a red light.
    source_text = Path(__file__).read_text(encoding="utf-8")
    # The two retired endpoints, written so that THIS CHECK IS NOT ITSELF A MATCH. A
    # self-test that searches its own source for a literal it contains can only ever fail,
    # and a test that can only fail is a decoration.
    #
    # The search is deliberately NOT "these digits appear nowhere": the retirement
    # tombstone in the report has to be able to say what it retired, or it is a claim with
    # no content. So the rule is the sharper one - the endpoints may appear inside the
    # tombstone and NOWHERE ELSE, which is what stops a re-derived band from being quietly
    # added back as a constant, a threshold, or a default argument.
    retired_endpoints = ("756" + "00", "765" + "87")
    tomb_start = source_text.find('"retired_instruments"')
    tomb_end = source_text.find('"scope_floor": dict(')
    tombstone = source_text[tomb_start:tomb_end] if 0 <= tomb_start < tomb_end else ""
    outside_tombstone = source_text[:tomb_start] + source_text[tomb_end:]
    check("band: the retirement tombstone is present and names the retired band",
          tombstone != "" and all(e in tombstone for e in retired_endpoints),
          f"tombstone slice found={bool(tombstone)}")
    check("band: the retired endpoints appear NOWHERE OUTSIDE the tombstone",
          re.search(r"(?<![0-9.,])(" + "|".join(retired_endpoints) + r")(?![0-9])",
                    outside_tombstone) is None,
          f"a retired band endpoint is live somewhere in this tool: {retired_endpoints}")
    check("band: no report key named 'band' is constructed anywhere in this tool",
          re.search(r"""["']band["']\s*:""", source_text) is None,
          "a consumer could still read a retired field as live")
    check("band: the comparison helper is no longer defined",
          "band_comparison" not in globals())
    check("band: the module docstring records the retirement",
          "RETIRED INSTRUMENTS" in source_text and "F-U10" in source_text)
    check("floor: the floor constant is 30,000 and it is the module's own",
          SCOPE_FLOOR == 30000, str(SCOPE_FLOOR))
    # The floor's two branches and its boundary, on the real constant. Both branches are
    # required by the ruling: the band is gone, the floor is not, and an instrument that is
    # only ever exercised on the branch it takes proves nothing about the other one.
    floor_breach = scope_floor_verdict(SCOPE_FLOOR - 1)
    floor_exact = scope_floor_verdict(SCOPE_FLOOR)
    floor_clear = scope_floor_verdict(59892)
    check("floor: a count one below 30,000 BREACHES and withdraws the all-terms claim",
          floor_breach["holds"] is False
          and floor_breach["rule_output"] == "all-terms-claim-WITHDRAWN"
          and floor_breach["headroom"] == -1, str(floor_breach))
    check("floor: exactly 30,000 STANDS (the rule is >=, not >)",
          floor_exact["holds"] is True and floor_exact["headroom"] == 0, str(floor_exact))
    check("floor: the measured 59,892 stands with 29,892 of headroom",
          floor_clear["holds"] is True and floor_clear["headroom"] == 29892
          and floor_clear["rule_output"] == "all-terms-scope-stands", str(floor_clear))
    check("floor: the pinned constant cannot be moved through the test parameter",
          scope_floor_verdict(59892, floor=1)["holds"] is True and SCOPE_FLOOR == 30000,
          "the parameter exists for the test; the constant does not move")
    # The exact identities, on hand-built counters, including two deliberately broken ones.
    ident_ok = accounting_identities(
        Counters(count_bare_ply=100, count_after_crash_excl=90,
                 count_after_degenerate_excl=80, count_usable_distinct=70,
                 duplicates_removed_by_dedup=10),
        {"train": 50, "holdout": 20}, 70)
    check("identities: a consistent run satisfies every identity",
          identities_hold(ident_ok), str(ident_ok))
    ident_dedup = accounting_identities(
        Counters(count_bare_ply=100, count_after_crash_excl=90,
                 count_after_degenerate_excl=80, count_usable_distinct=70,
                 duplicates_removed_by_dedup=9),
        {"train": 50, "holdout": 20}, 70)
    check("identities: a dedup that does not close is CAUGHT",
          identities_hold(ident_dedup) is False
          and ident_dedup["usable_equals_after_degenerate_minus_dedup"] is False,
          str(ident_dedup))
    ident_dupes = accounting_identities(
        Counters(count_bare_ply=100, count_after_crash_excl=90,
                 count_after_degenerate_excl=80, count_usable_distinct=70,
                 duplicates_removed_by_dedup=10),
        {"train": 50, "holdout": 20}, 69)
    check("identities: a key that stopped deduplicating is CAUGHT (69 distinct of 70 rows)",
          identities_hold(ident_dupes) is False
          and ident_dupes["one_survivor_per_normalized_fen"] is False, str(ident_dupes))
    ident_split = accounting_identities(
        Counters(count_bare_ply=100, count_after_crash_excl=90,
                 count_after_degenerate_excl=80, count_usable_distinct=70,
                 duplicates_removed_by_dedup=10),
        {"train": 50, "holdout": 19}, 70)
    check("identities: a train/holdout sum that does not close is CAUGHT",
          identities_hold(ident_split) is False
          and ident_split["usable_equals_train_plus_holdout"] is False, str(ident_split))
    p_train = Position(0, 0, "PLACEMENT w KQkq - 4 4", "PLACEMENT w KQkq -", "w")
    p_hold = Position(1, 0, "PLACEMENT w KQkq - 0 9", "PLACEMENT w KQkq -", "w")
    g = run_gates([p_train, p_hold], {}, {"0": "train", "1": "holdout"})
    check("gate: no rows -> no game-level overlap to report", g["game_level_overlap"] == 0)
    check("gate: normalized-FEN overlap fires on a clock-only difference",
          g["normalized_fen_overlap"] == 1, str(g))
    check("gate: overlap_zero is False when the stricter gate fires", g["overlap_zero"] is False)
    g2 = run_gates([p_train], {}, {"0": "train"})
    check("gate: single-sided set passes", g2["overlap_zero"] is True)

    # --- the write-time src_commit pin, against THROWAWAY repositories -----------------
    # Exercised in temp directories and never against this repository. The pin must ABORT
    # when the working tree has moved, so a test that depended on the developer's tree
    # state would be untestable exactly when it matters. The real repository's own answer is
    # available on demand as `python tools/e0013_extract.py --assert-src-commit`.
    with tempfile.TemporaryDirectory() as prov_tmp:
        prov_root = Path(prov_tmp) / "repo"
        prov_root.mkdir(parents=True, exist_ok=True)

        def pgit(*argv: str) -> str:
            return subprocess.check_output(["git", *argv], cwd=prov_root, text=True,
                                          encoding="utf-8", stderr=subprocess.DEVNULL).strip()

        pgit("init", "-q")
        pgit("config", "user.email", "selftest@example.invalid")
        pgit("config", "user.name", "e0013 selftest")
        prov_tool = prov_root / TOOL_REL
        prov_tool.parent.mkdir(parents=True, exist_ok=True)
        pinned_bytes = b"print('pinned tool')\n"
        prov_tool.write_bytes(pinned_bytes)
        pgit("add", "-A")
        pgit("commit", "-qm", "pin the tool")
        pinned_commit = pgit("rev-parse", "HEAD")

        prov = src_provenance(prov_root, TOOL_REL)
        check("provenance: a clean checkout pins the commit that CONTAINS the running code",
              prov["asserted"] is True and prov["src_commit"] == pinned_commit
              and prov["committed_blob"] == prov["running_blob"],
              json.dumps(prov, sort_keys=True))
        # THE S-0039 DEFECT, REPRODUCED. The code moves, the commit does not: this is
        # exactly the 9f6574c / da93d9c situation, and the pin must ABORT rather than name a
        # commit that does not contain the running code.
        prov_tool.write_bytes(b"print('pinned tool')\nprint('the code moved')\n")
        try:
            src_provenance(prov_root, TOOL_REL)
            check("provenance: ABORTS when the running code is not the committed code",
                  False, "no abort raised")
        except SystemExit as exc:
            check("provenance: ABORTS when the running code is not the committed code",
                  exc.code == 2, f"code={exc.code}")
        prov_tool.write_bytes(pinned_bytes)
        check("provenance: the SAME repository pins again once the code is restored",
              src_provenance(prov_root, TOOL_REL)["src_commit"] == pinned_commit)
        # A commit that does not contain the tool at all cannot be its provenance, whatever
        # the working tree looks like.
        pgit("rm", "-q", TOOL_REL)
        pgit("commit", "-qm", "drop the tool")
        prov_tool.parent.mkdir(parents=True, exist_ok=True)
        prov_tool.write_bytes(pinned_bytes)  # present in the worktree, in no commit
        try:
            src_provenance(prov_root, TOOL_REL)
            check("provenance: ABORTS when no commit contains the tool",
                  False, "no abort raised")
        except SystemExit as exc:
            check("provenance: ABORTS when no commit contains the tool",
                  exc.code == 2, f"code={exc.code}")

    # The command line must have NO route to moving the non-negotiable floor. The
    # self-test's own `run_on` passes one, which is why this assertion is worth having.
    check("floor: the command line cannot move the 30,000 floor",
          not hasattr(parse_args([]), "scope_floor"),
          "parse_args must not define a scope_floor option")

    # --- end-to-end runs over synthetic datasets, in a temp directory ------------------
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        def run_on(path: Path, out_name: str, count_only: bool, pin: str | None = None,
                   floor: int | None = None) -> int:
            return run(argparse.Namespace(
                dataset=str(path),
                expected_dataset_sha256=pin if pin is not None else sha256_file(path),
                out_dir=str(tmp_path / out_name), count_only=count_only,
                dry_run=False, allow_synthetic=True,
                **({} if floor is None else {"scope_floor": floor}),
            ))

        def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
            path.write_bytes(b"".join(canonical_json(r) for r in rows))

        # (a) clean synthetic set: distinct content per game.
        clean = tmp_path / "clean.jsonl"
        write_rows(clean, [synthetic_row(g, 12 + (g % 7), "plycap") for g in range(40)])
        check("clean synthetic run exits 0", run_on(clean, "out_clean", False) == 0)
        out_clean = tmp_path / "out_clean"
        rep = json.loads((out_clean / "report.json").read_text(encoding="utf-8"))
        c = rep["counts"]
        check("counts: the four stages are monotone non-increasing",
              c["count_bare_ply"] >= c["count_after_crash_excl"] >= c["count_after_degenerate_excl"] >= c["count_usable_distinct"],
              str(c["count_bare_ply"]))
        check("counts: usable == train + holdout",
              c["count_usable_distinct"] == c["count_usable_distinct_train"] + c["count_usable_distinct_holdout"])
        check("counts: the TRAIN_SIDE_ONLY alias equals the outer TRAIN count",
              c["count_usable_distinct_train_TRAIN_SIDE_ONLY"] == c["count_usable_distinct_train"])
        check("counts: dedup accounting closes",
              c["count_after_degenerate_excl"] - c["duplicates_removed_by_dedup"] == c["count_usable_distinct"])
        check("labels: frame uniform on the clean set", rep["labels"]["label_frame_uniform"] is True)
        check("labels: per-side counts sum to the usable count",
              rep["labels"]["count_positions_white_to_move"] + rep["labels"]["count_positions_black_to_move"] == c["count_usable_distinct"])
        check("gates: clean set passes overlap-0", rep["gates"]["overlap_zero"] is True, str(rep["gates"]))
        pos_bytes = (out_clean / "positions.jsonl").read_bytes()
        check("positions: line count matches the usable count",
              len(pos_bytes.splitlines()) == c["count_usable_distinct"])
        check("hygiene: no BOM", pos_bytes[:1] != b"\xef")
        check("hygiene: no CR bytes (LF-only)", b"\r" not in pos_bytes)
        check("split map: the published hash is reproducible from the file",
              rep["artifacts"]["split_map_sha256"] == sha256_bytes((out_clean / "split_map.json").read_bytes()))
        # The retired band, at the level a CONSUMER sees it. `rep["band"]` must raise and
        # `rep.get("band")` must be None: a consumer that quietly falls back to a default
        # is exactly the reader the retirement is meant to stop.
        check("report: the retired band key is ABSENT, not null (a direct read raises)",
              "band" not in rep and rep.get("band") is None, str(sorted(rep)))
        check("report: the retirement is recorded as a tombstone with is_live False",
              any(r["name"] == "yield band" and r["is_live"] is False
                  and "F-U10" in r["retired_by"] for r in rep["retired_instruments"]),
              json.dumps(rep.get("retired_instruments"), sort_keys=True))
        check("report: the scope floor is published, at 30,000, with its headroom",
              rep["scope_floor"]["floor"] == 30000
              and rep["scope_floor"]["headroom"]
              == rep["counts"]["count_usable_distinct_train"] - 30000,
              json.dumps(rep["scope_floor"], sort_keys=True))
        check("report: the scope floor says it is not the retired band",
              rep["scope_floor"]["is_the_retired_band"] is False
              and rep["scope_floor"]["not_renegotiable"] is True)
        # The exact identities, end to end, on a corpus that is consistent by construction.
        check("report: the exact accounting identities hold on the clean run",
              rep["accounting_identities_hold"] is True,
              json.dumps(rep["accounting_identities"], sort_keys=True))
        check("report: the one-survivor-per-normalized-FEN identity is published and true",
              rep["accounting_identities"]["one_survivor_per_normalized_fen"] is True)
        # FLOOR, end to end, on the BREACH branch. The synthetic corpus is tiny, so this run
        # really does fall below 30,000 and really does withdraw the claim. A floor that has
        # only ever been seen passing has not been tested.
        check("floor, end to end: this corpus BREACHES 30,000 and the claim is WITHDRAWN",
              rep["scope_floor"]["holds"] is False
              and rep["scope_floor"]["rule_output"] == "all-terms-claim-WITHDRAWN"
              and rep["scope_floor"]["headroom"] < 0,
              json.dumps(rep["scope_floor"], sort_keys=True))
        # FLOOR, end to end, on the STAND branch, by pinning the floor DOWN for one run only.
        # The pinned value is never touched: the run is told to evaluate at 1 instead, which
        # is how a test reaches the other branch without a route to moving the constant.
        small = run_on(clean, "out_floor_ok", True, floor=1)
        rep_floor_ok = json.loads(
            (tmp_path / "out_floor_ok" / "report.json").read_text(encoding="utf-8"))
        check("floor, end to end: the SAME corpus STANDS the floor when it is not breached",
              small == 0 and rep_floor_ok["scope_floor"]["holds"] is True
              and rep_floor_ok["scope_floor"]["rule_output"] == "all-terms-scope-stands"
              and rep_floor_ok["scope_floor"]["headroom"]
              == rep_floor_ok["counts"]["count_usable_distinct_train"] - 1,
              json.dumps(rep_floor_ok["scope_floor"], sort_keys=True))
        check("floor: the pinned constant is still 30,000 after both branches ran",
              SCOPE_FLOOR == 30000 and rep["scope_floor"]["floor"] == 30000)
        # CORPUS / MODE. The two modes write different bytes, so the digest a reader could
        # quote means different things in each; the report has to say which.
        check("corpus: the labelled run's digest IS published as the fitter's corpus digest",
              rep["mode"] == "labelled" and rep["corpus"]["is_fitter_corpus"] is True
              and rep["corpus"]["fitter_corpus_sha256"]
              == rep["artifacts"]["positions_sha256"]
              and rep["artifacts"]["positions_sha256_kind"] == "fitter-corpus",
              json.dumps(rep["corpus"], sort_keys=True))
        check("corpus: a labelled report has no null-reason, because it has no null to explain",
              rep["corpus"]["fitter_corpus_null_reason"] is None
              and rep["corpus"]["rows_with_null_y"] == 0)
        # (b) duplicate game CONTENT straddling the split: dedup and both gates must react.
        s40 = split_map(range(40))
        a = int(next(g for g, s in s40.items() if s == "train"))
        b = int(next(g for g, s in s40.items() if s == "holdout"))
        dirty_rows = [synthetic_row(g, 12 + (g % 7), "plycap") for g in range(40)]
        # Game b is given game a's content verbatim: same opening, same san, same end.
        dirty_rows[b] = dict(dirty_rows[a], game_id=b)
        copy_plies = len(dirty_rows[a]["san"])
        dirty = tmp_path / "dirty.jsonl"
        write_rows(dirty, dirty_rows)
        try:
            run_on(dirty, "out_dirty", False)
            check("dirty set aborts on the overlap gate", False, "no abort raised")
        except SystemExit as exc:
            check("dirty set aborts on the overlap gate", exc.code == 2, f"code={exc.code}")
        # The gate is checked BEFORE the write, so an aborting run leaves NO artifact behind.
        # Asserting that is the point: a blocking gate that aborts after writing positions.jsonl
        # would leave exactly the data it exists to withhold, loadable by any later step.
        out_dirty = tmp_path / "out_dirty"
        for name in ("positions.jsonl", "split_map.json", "report.json"):
            check(f"dirty: {name} is NOT written when the gate aborts",
                  not (out_dirty / name).exists(), "artifact leaked past the gate")

        # The gate verdicts and counts are re-derived here by calling extract() directly, because
        # the run correctly refused to publish them. What the gate SAW is still pinned: a real
        # blocking gate must not be satisfied by declining to report.
        cnt_dirty = Counters()
        kept_dirty, _ = extract([json.loads(line) for line in
                                 dirty.read_text(encoding="utf-8").splitlines() if line],
                                False, cnt_dirty)
        g_dirty = run_gates(kept_dirty, {int(r["game_id"]): r for r in dirty_rows}, s40)
        check("dirty: the game-level overlap is detected",
              g_dirty["game_level_overlap"] >= 1, str(g_dirty))
        check("dirty: overlap_zero is False", g_dirty["overlap_zero"] is False, str(g_dirty))
        # F-U8 REPAIR. The old assertion here read "the normalized-FEN invariant holds BECAUSE
        # the dedup ran first". That was FALSE IN GENERAL: it passed only because this
        # fixture's duplicate copies are byte-identical INCLUDING the clocks, so the old
        # finer key caught them by luck rather than by construction. Under F-U7 the dedup key
        # and the gate's comparison key are the SAME key, so the overlap is 0 for a reason
        # that is now structural rather than lucky - and the claim is stated as such. The
        # clock-only fixture below is the case the old one could not see, and it is the case
        # the real dataset's 27 leaks were made of.
        check("dirty: the normalized-FEN overlap is 0 BY CONSTRUCTION (dedup key == gate key)",
              g_dirty["normalized_fen_overlap"] == 0, str(g_dirty))
        check("dirty: the dedup key IS the gate key, not a refinement of it",
              rep["extraction_pin"]["dedup_key_equals_gate_key"] is True,
              str(rep["extraction_pin"]["dedup_key"]))
        check("dirty: the published dedup_key excludes both clocks",
              rep["extraction_pin"]["dedup_key_excludes"] == ["halfmove clock", "fullmove number"],
              str(rep["extraction_pin"]["dedup_key_excludes"]))
        check("dirty: dedup removed the copied game's positions",
              cnt_dirty.duplicates_removed_by_dedup >= 1,
              f"removed={cnt_dirty.duplicates_removed_by_dedup} copied_plies={copy_plies}")

        # (b2) F-U8 REGRESSION: the CLOCK-ONLY duplicate - the case the superseded exact-FEN
        # key was structurally blind to, and the case the real dataset's 27 leaks were made
        # of. Two games play the same normalized positions but reach them at different plies,
        # so the copies agree in placement/side/castling/EP and differ ONLY in the halfmove
        # clock and the fullmove number. Under the old key each copy was a distinct datum and
        # BOTH sides of the split kept one; under the new key the second is removed before
        # the split. This fixture is permanent: it is the test that would have caught the
        # defect, and the test that keeps catching it if the key is ever widened again.
        clock_rows = [dict(synthetic_row(g, 12 + (g % 7), "plycap")) for g in range(40)]
        clock_rows[a] = clock_only_row(a, 0)
        clock_rows[b] = clock_only_row(b, 2)
        clock_path = tmp_path / "clock_only.jsonl"
        write_rows(clock_path, clock_rows)

        # 1. The fixture is what it claims to be. A fixture that quietly degenerates into
        #    the byte-identical case is exactly how the old test passed for the wrong reason,
        #    so the CLOCK-ONLY property is asserted directly rather than assumed.
        cand = candidate_positions([clock_rows[a], clock_rows[b]])
        a_fens = {p.fen for p in cand if p.game_id == a}
        b_fens = {p.fen for p in cand if p.game_id == b}
        shared_norms = {p.norm_fen for p in cand if p.game_id == a} & \
                       {p.norm_fen for p in cand if p.game_id == b}
        fens_of = {}
        for p in cand:
            fens_of.setdefault(p.norm_fen, set()).add(p.fen)
        clock_only_norms = {n for n, fs in fens_of.items() if len(fs) > 1 and n in shared_norms}
        check("clock-only: the two games share normalized positions", len(shared_norms) >= 4,
              f"shared={len(shared_norms)}")
        check("clock-only: the shared positions come in CLOCK-ONLY copies (distinct FENs)",
              len(clock_only_norms) >= 4, f"clock_only={len(clock_only_norms)}")

        # 2. RED under the superseded key. Both keyings run over the IDENTICAL candidate set
        #    with the IDENTICAL survivor rule, so the key is the only variable. The old key
        #    keeps every copy, one per side, and the gate WOULD FIRE.
        old_kept = dedup_on(cand, lambda p: p.fen)
        new_kept = dedup_on(cand, lambda p: p.norm_fen)
        old_overlap = cross_split_overlap(old_kept, smap40 := split_map(range(40)))
        check("clock-only: RED under the OLD exact-FEN key - it keeps EVERY copy",
              len(old_kept) == len(cand), f"old_kept={len(old_kept)} of {len(cand)} candidates")
        check("clock-only: RED under the OLD key - the gate WOULD FIRE (overlap == shared)",
              old_overlap == len(shared_norms),
              f"old_overlap={old_overlap} shared={len(shared_norms)}")

        # 3. GREEN under the new key: one survivor per normalized FEN, and no cross-split
        #    overlap, because the survivor's game_id alone decides the split.
        check("clock-only: GREEN under the NEW key - one survivor per normalized FEN",
              len(new_kept) == len({p.norm_fen for p in cand}),
              f"new_kept={len(new_kept)} distinct_norms={len({p.norm_fen for p in cand})}")
        check("clock-only: GREEN under the NEW key - cross-split overlap is 0",
              cross_split_overlap(new_kept, smap40) == 0,
              f"overlap={cross_split_overlap(new_kept, smap40)}")
        check("clock-only: the survivor rule is UNCHANGED (first occurrence in (game_id, ply))",
              [p.game_id for p in new_kept].index(a) == 0,
              f"first_survivor_game={new_kept[0].game_id} (train game is {a})")

        # 4. The same corpus end to end: the run passes and the gate is silent.
        check("clock-only: run_on exits 0 under the NEW key",
              run_on(clock_path, "out_clock", True) == 0)
        rep_clock = json.loads((tmp_path / "out_clock" / "report.json").read_text(encoding="utf-8"))
        check("clock-only: the gate is SILENT under the NEW key",
              rep_clock["gates"]["normalized_fen_overlap"] == 0
              and rep_clock["gates"]["overlap_zero"] is True, str(rep_clock["gates"]))
        check("clock-only: the run removed exactly the clock-only duplicates",
              rep_clock["counts"]["duplicates_removed_by_dedup"] == len(cand) - len(new_kept),
              f"removed={rep_clock['counts']['duplicates_removed_by_dedup']} expected={len(cand) - len(new_kept)}")

        # (b3) F-U8 NEGATIVE CONTROL. Everything above shows the gate PASSING, which is only
        #      half of a tested gate: a gate silently broken into always-passing would look
        #      identical from here. So the gate is now handed a corpus that genuinely SHOULD
        #      fail and is required to FIRE. This is what makes the passing meaningful.
        #
        #      The leak is injected at the one point that can still produce one after F-U7.
        #      A pure clock-only duplicate can no longer do it - that is exactly what F-U7
        #      fixed - so the control drives the gate DIRECTLY with a cross-split normalized
        #      FEN that the dedup is not in the path of, and then separately drives the
        #      end-to-end abort path with a corpus whose split map is forced to straddle it.
        leak_a = Position(a, 3, "8/1R6/8/8/8/2K5/8/k7 w - - 0 91",
                          "8/1R6/8/8/8/2K5/8/k7 w - -", "w")
        leak_b = Position(b, 7, "8/1R6/8/8/8/2K5/8/k7 w - - 33 124",
                          "8/1R6/8/8/8/2K5/8/k7 w - -", "w")
        check("negative control: the two leaked copies are CLOCK-ONLY (same norm_fen, different FEN)",
              leak_a.norm_fen == leak_b.norm_fen and leak_a.fen != leak_b.fen,
              f"{leak_a.fen} vs {leak_b.fen}")
        g_neg = run_gates([leak_a, leak_b], {}, {str(a): "train", str(b): "holdout"})
        check("negative control: the gate FIRES on a genuine cross-split clock-only leak",
              g_neg["normalized_fen_overlap"] == 1, str(g_neg))
        check("negative control: overlap_zero is False, so the run must abort",
              g_neg["overlap_zero"] is False, str(g_neg))
        neg_path = tmp_path / "negative.jsonl"
        write_rows(neg_path, clock_rows)
        out_neg = tmp_path / "out_neg"
        real_identity = dedup_identity
        try:
            globals()["dedup_identity"] = lambda pos: pos.fen
            try:
                run_on(neg_path, "out_neg", True)
                check("negative control: the end-to-end run ABORTS under the OLD key", False,
                      "no abort raised")
            except SystemExit as exc:
                check("negative control: the end-to-end run ABORTS under the OLD key (exit 2)",
                      exc.code == 2, f"code={exc.code}")
        finally:
            globals()["dedup_identity"] = real_identity
        for name in ("positions.jsonl", "split_map.json", "report.json"):
            check(f"negative control: {name} is NOT written when the gate aborts",
                  not (out_neg / name).exists(), "artifact leaked past the gate")
        # And with the real key restored, the IDENTICAL corpus passes and DOES write. The
        # failing and passing cases must be the same input; otherwise the control proves
        # something about the fixture rather than about the key.
        check("negative control: the SAME corpus passes and writes once the key is restored",
              run_on(neg_path, "out_neg_ok", True) == 0
              and (tmp_path / "out_neg_ok" / "positions.jsonl").exists(),
              "the passing case and the failing case must be the same input")



        # (c) count-only mode reads no label at all.
        co_rows = [synthetic_row(g, 12, "plycap", res="A", a_white=True) for g in range(8)]
        co = tmp_path / "count_only.jsonl"
        write_rows(co, co_rows)
        check("count-only run exits 0", run_on(co, "out_co", True) == 0)
        rep_co = json.loads((tmp_path / "out_co" / "report.json").read_text(encoding="utf-8"))
        check("count-only: the label frame is null WITH a reason",
              rep_co["labels"]["label_frame_uniform"] is None and bool(rep_co["labels"]["null_reason"]))
        check("count-only: every emitted y is null",
              all(json.loads(l)["y"] is None
                  for l in (tmp_path / "out_co" / "positions.jsonl").read_text(encoding="utf-8").splitlines()))
        # CORPUS / MODE, the count-only side. S-0039 Ruling 2's second weakness is exactly
        # this: a count-only artifact whose digest could be mistaken for the corpus a fitter
        # reads. The corpus digest must be null WITH a reason, and the file's own digest must
        # be published under a name that says what it is a digest OF.
        check("corpus: the count-only run publishes NO fitter corpus digest",
              rep_co["mode"] == "count-only" and rep_co["corpus"]["is_fitter_corpus"] is False
              and rep_co["corpus"]["fitter_corpus_sha256"] is None
              and bool(rep_co["corpus"]["fitter_corpus_null_reason"]),
              json.dumps(rep_co["corpus"], sort_keys=True))
        check("corpus: the count-only digest is named count-only-pass, never corpus",
              rep_co["artifacts"]["positions_sha256_kind"] == "count-only-pass"
              and rep_co["artifacts"]["positions_sha256"] is not None,
              json.dumps(rep_co["artifacts"], sort_keys=True))
        check("corpus: a count-only artifact cannot read as a corpus even by accident",
              rep_co["corpus"]["rows_with_null_y"] == rep_co["corpus"]["rows"]
              and rep_co["corpus"]["y_values_are_labels"] is False
              and rep_co["corpus"]["rows"] > 0)
        # The two modes are DIFFERENT BYTES, which is the entire reason the names matter. If
        # these digests were equal the ambiguity would be harmless; asserting they differ is
        # what makes the distinction load-bearing rather than decorative.
        check("corpus: the labelled and count-only digests are DIFFERENT files",
              rep["artifacts"]["positions_sha256"] != rep_co["artifacts"]["positions_sha256"],
              f"labelled={rep['artifacts']['positions_sha256'][:16]} "
              f"count_only={rep_co['artifacts']['positions_sha256'][:16]}")
        # PROVENANCE, and the stale-field case specifically. A previous report carrying a
        # bogus src_commit is planted in the output directory; the next run must not read it.
        poisoned_dir = tmp_path / "out_poison"
        poisoned_dir.mkdir(parents=True, exist_ok=True)
        (poisoned_dir / "report.json").write_bytes(canonical_json({
            "format": REPORT_FORMAT, "src_commit": "0" * 40, "mode": "labelled",
            "positions_sha256": "f" * 64,
        }))
        run_on(clean, "out_poison", True)
        rep_poison = json.loads(
            (poisoned_dir / "report.json").read_text(encoding="utf-8"))
        check("provenance: a previous report's src_commit is NEVER read back",
              rep_poison["src_commit"] == SYNTHETIC_PROVENANCE["src_commit"]
              and rep_poison["src_commit"] != "0" * 40,
              f"got {rep_poison['src_commit']!r}")
        check("provenance: the poisoned digest is overwritten, not inherited",
              rep_poison["corpus"]["fitter_corpus_sha256"] != "f" * 64)
        check("provenance: a synthetic run says plainly that no commit pin is asserted",
              rep_poison["provenance"]["asserted"] is False
              and bool(rep_poison["provenance"]["why_not_asserted"]),
              json.dumps(rep_poison["provenance"], sort_keys=True))
        # Assert against the extractor's own view of the rows: `run()` re-parses the file, so
        # the writer's copies are not the objects the pass mutated.
        probe = [dict(r) for r in co_rows]
        extract(probe, True, Counters())
        check("count-only: the label keys are removed from the rows the extractor sees",
              all(k not in probe[0] for k in LABEL_KEYS), str(sorted(probe[0])))
        probe_full = [dict(r) for r in co_rows]
        extract(probe_full, False, Counters())
        check("full mode: the label keys survive (the removal is mode-specific)",
              all(k in probe_full[0] for k in LABEL_KEYS))

        # (d) exclusions: a crash game and a degenerate mate game leave the later stages.
        ex = tmp_path / "excl.jsonl"
        write_rows(ex, [
            synthetic_row(0, 16, "plycap"),
            synthetic_row(1, 16, "crash"),
            synthetic_row(2, 4, "mate"),
        ])
        run_on(ex, "out_ex", True)
        ce = json.loads((tmp_path / "out_ex" / "report.json").read_text(encoding="utf-8"))["counts"]
        check("exclusions: the crash game is counted and excluded", ce["games_excluded_crash"] == 1)
        check("exclusions: the degenerate mate game is counted and excluded", ce["games_excluded_degenerate"] == 1)
        check("exclusions: games_used == 1", ce["games_used"] == 1, str(ce["end_counts"]))
        check("exclusions: earlier stages are strictly larger",
              ce["count_bare_ply"] > ce["count_after_crash_excl"] > ce["count_after_degenerate_excl"],
              f"{ce['count_bare_ply']}/{ce['count_after_crash_excl']}/{ce['count_after_degenerate_excl']}")

        # (e) the dataset pin is enforced, not decorative.
        try:
            run_on(clean, "out_pin", True, pin="0" * 64)
            check("dataset pin: a wrong hash aborts", False, "no abort raised")
        except SystemExit as exc:
            check("dataset pin: a wrong hash aborts", exc.code == 2, f"code={exc.code}")

    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not ok else ""))
    failed = [n for n, ok, _ in checks if not ok]
    print(f"SELFTEST {'PASS' if not failed else 'FAIL'} checks={len(checks)} failed={len(failed)}")
    return 0 if not failed else 1


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--expected-dataset-sha256", default=DATASET_SHA256)
    parser.add_argument("--out-dir", default=str(ROOT / "build" / "e0013" / "extract"))
    parser.add_argument("--count-only", action="store_true",
                        help="E-00015 mode: no label field is read at all")
    parser.add_argument("--dry-run", action="store_true", help="compute and report, write nothing")
    parser.add_argument("--allow-synthetic", action="store_true",
                        help="skip the 1,000-row assert (self-test only)")
    parser.add_argument("--selftest", action="store_true",
                        help="run the synthetic checks; the real dataset is not touched")
    parser.add_argument("--assert-src-commit", action="store_true",
                        help="assert ONLY that the running code is the code the named commit "
                             "contains, then exit 0 or 2. Reads no dataset, writes nothing. "
                             "This is the S-0039 provenance check on its own, so it can be "
                             "run before any pass and after any edit")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.selftest:
        return selftest()
    if args.assert_src_commit:
        # The commit is computed here, at the moment of asking, and never read from a
        # previously written report. If the working tree's copy of this file is not the
        # committed copy, src_provenance() aborts with exit 2 and prints nothing, which is
        # the whole point: the answer must not be available when it is false.
        provenance = src_provenance()
        print(f"src_commit={provenance['src_commit']} "
              f"tool={provenance['tool_path']} "
              f"committed_blob={provenance['committed_blob']} "
              f"running_blob={provenance['running_blob']} "
              f"asserted={provenance['asserted']}")
        return 0
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())







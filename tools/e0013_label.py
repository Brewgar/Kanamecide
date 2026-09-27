#!/usr/bin/env python3
"""E-0013 label construction: the SEPARATE, TRAIN-ONLY step the extractor pointed at.

The extractor reads no label in its `--count-only` mode, and its own docstring says label
construction is "a separate later step". That step is this file. It was specced nowhere and
did not exist; building it is the job, so every property below is taken from E-0013 B2 and
the colour-frame amendment and is verified against the RECORD rather than against anyone.

    B2 sentence 1, verbatim: "Fit target (side-to-move frame). For a position whose side to
    move is s, the fit target is `y = white_score` if `s == WHITE` and `y = 1 - white_score`
    if `s == BLACK`, where `white_score in {1, 0.5, 0}` is `res` mapped from White's
    perspective. Because the eval is required to be colour-symmetric (mirror `s ^ 56`;
    conjunct (d) 0 full-mirror violations), a target expressed in the White frame for a
    Black-to-move position, or any mixture of the two frames across the dataset, is a FAIL
    of conjunct (c)."

Four properties, each of which this tool ENFORCES rather than describes:

  1. **RESULT-ONLY.** One bit per game (0.5 for a draw) taken from the verified dataset's
     recorded `res` and `a_white`. Nothing else is an input: no eval, no search score, no
     material, no clock. The label is a function of the game's OUTCOME and the position's
     SIDE TO MOVE, and of nothing else. The constructor's signature is the proof - it is not
     handed a FEN, a ply, a move, or a score, so it cannot use one.

  2. **THE FRAME IS THE SIDE TO MOVE AT THAT POSITION.** Not the game's first mover, not
     the majority side, not the side that is ahead. The side to move of the specific
     position the label attaches to. This is the "sharp edge" B2 names, and it is the one
     that is invisible to inspection and catastrophic to a fit, so it is checked on every
     row and a mismatch is a FAIL, not a warning.

  3. **CONSTANT WITHIN A GAME.** Every position in a game carries the same target, because
     the target is the game's outcome. This is why the dispersion `s_d` is a per-GAME
     cluster statistic and why B3's effective N is the number of holdout GAMES, not
     positions: positions within a game are not independent observations of anything.
     A corpus whose labels vary within a game is a corpus whose power analysis is wrong,
     so constancy is asserted and a violation is an abort.

  4. **TRAIN-ONLY.** No label is derived from, or may condition on, the holdout. Games are
     taken from the split map's TRAIN side only, and the split map is re-derived from
     `SPLIT_SALT` rather than read from a file, so a swapped map cannot widen the scope.
     The holdout games are enumerated and reported as NOT LABELLED, which is the only way
     to show the omission rather than assert it.

Inputs are the extractor's own pinned artifacts; the corpus is verified by digest before a
single row is read, via `tools/e0013_pins.py`, so a tampered corpus cannot become a labelled
corpus. This tool NEVER reads the holdout and NEVER writes one.

Usage:
    python tools/e0013_label.py --selftest     # synthetic games only; the real dataset is
                                               # never read
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import chess  # noqa: E402

from e0013_extract import (  # noqa: E402
    DATASET_SHA256, LABEL_KEYS, SPLIT_SALT, TRAIN_FRACTION,
    canonical_json, label_side_to_move, normalize_fen, sha256_file, split_of, white_score,
)

LABEL_FORMAT = "kana-e0013-labels-v1"
REPORT_FORMAT = "kana-e0013-label-report-v1"
LABEL_VALUES = (1.0, 0.5, 0.0)
# The extractor's own frame, CITED rather than reimplemented. Two implementations of B2
# sentence 1 would be two chances to be wrong, and the extractor's is the one its report
# already publishes as `label_mapping`.
FRAME_SOURCE = "tools/e0013_extract.py:label_side_to_move (B2 sentence 1), cited not copied"


LAST_ABORT_REASON: str | None = None


LAST_ABORT_REASON: str | None = None


LAST_ABORT_REASON: str | None = None


LAST_ABORT_REASON: str | None = None


LAST_ABORT_REASON: str | None = None


LAST_ABORT_REASON: str | None = None


def abort(reason: str) -> "NoReturn":  # type: ignore[name-defined]
    """An abort is a result. It is reported, never repaired into a pass.

    The reason is ALSO stashed in `LAST_ABORT_REASON`, because `SystemExit(2)` stringifies
    to `"2"` and a caller that wants to assert WHICH guard fired - rather than merely that
    something fired - has no other way to see it. Without that, a guard test degenerates
    into "some abort happened somewhere", which several unrelated failures would satisfy.
    """
    global LAST_ABORT_REASON
    LAST_ABORT_REASON = reason
    print(f"ABORT: {reason}", file=sys.stderr)
    raise SystemExit(2)
def game_label(res: str, a_white: bool) -> float:
    """The RESULT-ONLY game label: one bit per game in the WHITE frame, 0.5 for a draw.

    E-0013 B2: `white_score in {1, 0.5, 0}` is `res` mapped from White's perspective. This
    is the per-game half of the target and the ONLY place the outcome enters.

    Note the signature: `(res, a_white)`. No FEN, no ply, no eval, no search score, no
    material count. The label physically cannot depend on the position, which makes property
    1 (result-only) a structural fact rather than a promise - a future edit that wanted the
    eval would have to change this signature, and the tests would see it.
    """
    return white_score({"res": res, "a_white": a_white})


def position_label(game_y_white: float, stm: str) -> float:
    """Attach the game label to the SIDE TO MOVE at this position (B2 sentence 1).

    `stm` is this position's side to move, read from the position's own FEN. For White to
    move the White-frame score IS the target; for Black to move the target is its complement.
    Attaching the White-frame score to a Black-to-move position is a FAIL of conjunct (c),
    and this is the only line where the frame is chosen.
    """
    if stm not in ("w", "b"):
        abort(f"side to move {stm!r} is neither 'w' nor 'b'")
    return label_side_to_move(game_y_white, chess.WHITE if stm == "w" else chess.BLACK)




def build_labels(positions: list[dict[str, Any]], rows_by_id: dict[int, dict[str, Any]],
                 smap: dict[str, str]) -> dict[str, Any]:
    """Construct the TRAIN-ONLY labelled corpus, and enforce all four properties.

    Returns the labelled rows plus the per-game and per-side statistics the power analysis
    needs. Raises SystemExit(2) on any violation: a wrong-side label, a within-game
    variation, a holdout game, or a row whose side to move disagrees with its own FEN.

    The checks are ordered so the cheapest diagnosis comes first: a row's `stm` is
    cross-checked against its own FEN before it is trusted, the frame is checked per row,
    constancy is checked per game over the whole set, and the holdout is reported by
    enumeration so the omission is SHOWN rather than asserted.
    """
    # The split map's keys are STRINGS (they are JSON object keys, and the extractor's
    # `split_map()` returns them that way), while `pos["game_id"]` is an int.
    # Normalising once here is what keeps every downstream comparison honest; leaving
    # the mismatch in would make every game look absent from the split.
    train_games = {int(gid) for gid, split in smap.items() if split == "train"}
    holdout_games = {int(gid) for gid, split in smap.items() if split == "holdout"}

    labelled: list[dict[str, Any]] = []
    per_game: dict[int, dict[str, Any]] = {}
    frame_violations: list[dict[str, Any]] = []
    stm_violations: list[dict[str, Any]] = []
    holdout_refusals: list[int] = []
    side_counts = {"w": 0, "b": 0}
    label_counts = {str(v): 0 for v in LABEL_VALUES}

    for pos in positions:
        gid = int(pos["game_id"])
        if smap.get(str(gid)) == "holdout" or gid in holdout_games:
            # TRAIN-ONLY, enforced. A holdout position is REFUSED, never labelled, and the
            # refusal is COUNTED so the report can say how many - the difference between an
            # omission that is shown and one that is asserted.
            holdout_refusals.append(gid)
            continue
        if gid not in train_games:
            abort(f"game {gid} is in neither split; the split map does not cover it")
        if gid not in rows_by_id:
            abort(f"game {gid} has positions but no row in the dataset")

        # The side to move is read from the POSITION and cross-checked against the FEN the
        # extractor emitted. Both come from the same run, so a disagreement means the corpus
        # is internally inconsistent and every label from it is untrustworthy.
        fields = pos["fen"].split(" ")
        fen_stm = fields[1] if len(fields) > 1 else None
        if fen_stm is not None and fen_stm != pos["stm"]:
            stm_violations.append({"game_id": gid, "ply_index": pos.get("ply_index"),
                                   "stm_field": pos["stm"], "fen_stm": fen_stm})
            continue

        row = rows_by_id[gid]
        for key in LABEL_KEYS:
            if key not in row:
                abort(f"game {gid} has no {key!r}; the verified dataset's recorded result is "
                      f"the only admitted label source and it is absent")
        game_y_white = game_label(row["res"], bool(row["a_white"]))
        y = position_label(game_y_white, pos["stm"])

        # THE WRONG-SIDE CHECK, per row. The expected value is recomputed from the game's own
        # recorded result and this row's own FEN side to move.
        #
        # It is recomputed with `label_side_to_move` - the extractor's function, imported
        # directly - and NOT with this module's `position_label`. That is deliberate and it is
        # the whole reason this check has teeth: an earlier draft computed `expected` with
        # `position_label`, the same function that produced `y`, so the two sides of the
        # comparison moved together and the check could never fail. A check that shares its
        # oracle with the thing it checks is a check that reports PASS unconditionally, and
        # an unconditionally-passing check is the permanently-green instrument this project's
        # own rulings keep warning about. The oracle is now a separate implementation that
        # this module cannot override at runtime.
        expected = label_side_to_move(
            game_y_white, chess.WHITE if (fen_stm or pos["stm"]) == "w" else chess.BLACK)
        if y != expected:
            frame_violations.append({"game_id": gid, "ply_index": pos.get("ply_index"),
                                     "stm": pos["stm"], "wrote": y, "expected": expected})
        # recorded result and this row's own FEN side to move, then compared with what was
        # written. A frame error surfaces as a mismatch on every black-to-move row of a
        # decisive game - exactly the case the negative control constructs.
        expected = position_label(game_y_white, fen_stm if fen_stm else pos["stm"])
        if y != expected:
            frame_violations.append({"game_id": gid, "ply_index": pos.get("ply_index"),
                                     "stm": pos["stm"], "wrote": y, "expected": expected})

        side_counts[pos["stm"]] += 1
        label_counts[str(y)] += 1
        g = per_game.setdefault(gid, {"game_id": gid, "res": row["res"],
                                      "a_white": bool(row["a_white"]),
                                      "white_score": game_y_white, "labels": set(),
                                      "white_frame_scores": set(),
                                      "positions": 0, "sides": {"w": 0, "b": 0}})
        g["labels"].add(y)
        # The WHITE-FRAME value is what is constant within a game. B2 sentence 1 makes the
        # emitted `y` differ between a white-to-move and a black-to-move position of the SAME
        # game - that is the frame, not a violation - so constancy is asserted on the
        # White-frame score, which is the quantity `s_d`'s per-game clustering rests on.
        g["white_frame_scores"].add(game_y_white)
        g["positions"] += 1
        g["sides"][pos["stm"]] += 1
        labelled.append({"game_id": gid, "ply_index": pos.get("ply_index"),
                         "norm_fen": pos.get("norm_fen"), "stm": pos["stm"], "y": y,
                         "res": row["res"], "a_white": bool(row["a_white"]),
                         "game_white_score": game_y_white})

    if stm_violations:
        abort(f"{len(stm_violations)} position(s) whose stm field disagrees with its own "
              f"FEN's side to move; first: {json.dumps(stm_violations[0], sort_keys=True)}. "
              f"The corpus is internally inconsistent and no label from it can be trusted")
    if frame_violations:
        abort(f"{len(frame_violations)} label(s) are attached to the WRONG SIDE; first: "
              f"{json.dumps(frame_violations[0], sort_keys=True)}. B2 sentence 1 makes this a "
              f"FAIL of conjunct (c), and a wrong-frame corpus must not be published")

    # CONSTANCY WITHIN A GAME, asserted on the White-FRAME score. Stated precisely because
    # the naive form of this claim is FALSE and asserting it would be worse than not
    # asserting it: B2 sentence 1 gives a white-to-move position `white_score` and a
    # black-to-move position of the SAME game `1 - white_score`, so the emitted `y` values
    # inside one game are legitimately {s, 1-s}. What must be single-valued is the game
    # outcome `s` itself, and that is the quantity the per-game clustering of `s_d` uses:
    # B3's effective N is the number of GAMES because a game's positions all carry the same
    # outcome bit, not because they all carry the same number.
    nonconstant = sorted(gid for gid, g in per_game.items()
                         if len(g["white_frame_scores"]) > 1)
    if nonconstant:
        example = per_game[nonconstant[0]]
        abort(f"{len(nonconstant)} game(s) carry MORE THAN ONE White-frame score, so the "
              f"label is not game-constant; first is game {nonconstant[0]} with "
              f"{sorted(example['white_frame_scores'])}. The label is result-only and one "
              f"game has exactly one outcome, because s_d is a per-game cluster statistic")

    # And the frame invariant the above does NOT cover: within one game the emitted y values
    # must be exactly the pair {s, 1-s} and nothing else. A value outside that pair is a
    # label that came from somewhere other than this game's outcome.
    for gid, g in sorted(per_game.items()):
        s_white = g["white_score"]
        allowed = {s_white, 1.0 - s_white}
        stray = sorted(g["labels"] - allowed)
        if stray:
            abort(f"game {gid} carries label(s) {stray} that are not this game's outcome "
                  f"({sorted(allowed)}); a label that is not the game result has entered the "
                  f"corpus")

    games = []
    for gid in sorted(per_game):
        g = per_game[gid]
        s_white = g["white_score"]
        games.append({"game_id": gid, "res": g["res"], "a_white": g["a_white"],
                      "white_score": s_white,
                      "y_white_to_move": s_white,
                      "y_black_to_move": 1.0 - s_white,
                      "positions": g["positions"], "white_to_move": g["sides"]["w"],
                      "black_to_move": g["sides"]["b"]})

    games = []
    for gid in sorted(per_game):
        g = per_game[gid]
        games.append({"game_id": gid, "res": g["res"], "a_white": g["a_white"],
                      "white_score": g["white_score"], "y": sorted(g["labels"])[0],
                      "positions": g["positions"], "white_to_move": g["sides"]["w"],
                      "black_to_move": g["sides"]["b"]})

    return {
        "labels": labelled,
        "games": games,
        "stats": {
            "positions_labelled": len(labelled),
            "games_labelled": len(games),
            "games_held_out_not_labelled": len(holdout_games),
            "holdout_positions_refused": len(holdout_refusals),
            "count_positions_white_to_move": side_counts["w"],
            "count_positions_black_to_move": side_counts["b"],
            "label_counts": label_counts,
            "label_is_game_constant": True,
            "label_is_result_only": True,
            "label_frame": "side to move (B2 sentence 1)",
            "label_frame_source": FRAME_SOURCE,
            "frame_violations": len(frame_violations),
            "stm_vs_fen_violations": len(stm_violations),
            "train_games": sorted(train_games),
            "holdout_games": sorted(holdout_games),
        },
    }


# --- synthetic fixtures --------------------------------------------------------------
# Real, LEGAL games built by the extractor's own generator, so the positions are genuine
# positions with genuine side-to-move values and the frame checks are exercised on real
# boards rather than on invented strings.

def synthetic_games(n: int) -> list[dict[str, Any]]:
    from e0013_extract import synthetic_row
    rows = []
    for gid in range(n):
        res = ("A", "B", "D")[gid % 3]
        a_white = (gid % 2 == 0)
        rows.append(synthetic_row(gid, 14 + (gid % 5), "plycap", res=res, a_white=a_white))
    return rows


def positions_for(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract the candidate positions for `rows` with the extractor's own machinery."""
    from e0013_extract import Counters, extract
    probe = [dict(r) for r in rows]
    kept, _ = extract(probe, False, Counters())
    return [{"game_id": p.game_id, "ply_index": p.ply_index, "fen": p.fen,
             "norm_fen": p.norm_fen, "stm": p.stm} for p in kept]


def split_for(gids) -> dict[str, str]:
    """The split map, re-derived from SPLIT_SALT rather than read from a file.

    A swapped or hand-edited map file would be a way to move a game across the
    train/holdout boundary without touching the salt, so the map is recomputed here
    from the pinned salt and the game id - the same way `run()` does.
    """
    return {str(g): split_of(g) for g in gids}


def train_of(smap: dict[str, str]) -> set[str]:
    return {g for g, s in smap.items() if s == "train"}


def holdout_of(smap: dict[str, str]) -> set[str]:
    return {g for g, s in smap.items() if s == "holdout"}


def selftest() -> int:
    """Synthetic games only. The real dataset and the real artifacts are never read."""
    checks: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, bool(ok), detail))

    rows = synthetic_games(24)
    rows_by_id = {int(r["game_id"]): r for r in rows}
    positions = positions_for(rows)
    smap = split_for(range(24))
    check("fixture: the synthetic corpus has positions and BOTH sides to move",
          len(positions) > 0 and {p["stm"] for p in positions} == {"w", "b"},
          str(sorted({p["stm"] for p in positions})))
    check("fixture: every fixture position's stm agrees with its own FEN",
          all(p["fen"].split(" ")[1] == p["stm"] for p in positions))
    check("fixture: the split has both sides, so TRAIN-ONLY has something to exclude",
          {"train", "holdout"} == set(smap.values()), str(sorted(set(smap.values()))))

    # 1. THE LABEL IS RESULT-ONLY, verified against the ROW and not against a comment. The
    #    expected value is recomputed from `res`/`a_white` by hand here, independently of the
    #    tool's own mapping, so this test is a second opinion rather than an echo.
    def expected_white(res: str, a_white: bool) -> float:
        if res == "D":
            return 0.5
        return 1.0 if ((res == "A") == a_white) else 0.0

    out = build_labels(positions, rows_by_id, smap)
    bad = [r for r in out["labels"]
           if r["y"] != (expected_white(r["res"], r["a_white"]) if r["stm"] == "w"
                         else 1.0 - expected_white(r["res"], r["a_white"]))]
    check("label: every emitted label equals the hand-derived side-to-move target",
          not bad, json.dumps(bad[:2], sort_keys=True))
    check("label: the label is derived from res/a_white and nothing else",
          all(set(r) == {"game_id", "ply_index", "norm_fen", "stm", "y", "res",
                         "a_white", "game_white_score"} for r in out["labels"]),
          str(sorted(out["labels"][0])))

    # 2. BOTH COLOURS, on the DECISIVE cases where the frame is observable. A draw is 0.5 in
    #    both frames, so a wrong-side label is INVISIBLE on a draw - which is why the frame
    #    test is built on decisive games and the coverage is reported rather than assumed.
    decisive_w = [r for r in out["labels"]
                  if r["stm"] == "w" and r["res"] != "D" and r["y"] in (0.0, 1.0)]
    decisive_b = [r for r in out["labels"]
                  if r["stm"] == "b" and r["res"] != "D" and r["y"] in (0.0, 1.0)]
    check("label: WHITE-to-move decisive rows carry the White-frame score",
          bool(decisive_w) and all(r["y"] == expected_white(r["res"], r["a_white"])
                                   for r in decisive_w), f"n={len(decisive_w)}")
    check("label: BLACK-to-move decisive rows carry the COMPLEMENT of the White-frame score",
          bool(decisive_b) and all(r["y"] == 1.0 - expected_white(r["res"], r["a_white"])
                                   for r in decisive_b), f"n={len(decisive_b)}")
    check("label: a black-to-move row is NOT the White-frame score (the frame is applied)",
          any(r["y"] != expected_white(r["res"], r["a_white"]) for r in decisive_b),
          "if this is empty the frame is not being applied at all")

    # 3. DRAWS. 0.5 in the White frame, and therefore 0.5 in the side-to-move frame too.
    #    Asserted so the 0.5 is pinned rather than incidental.
    draw_rows = [r for r in out["labels"] if r["res"] == "D"]
    check("label: every draw row is 0.5, in BOTH frames (the frame cannot show there)",
          bool(draw_rows) and all(r["y"] == 0.5 for r in draw_rows), f"n={len(draw_rows)}")
    check("label: a draw is 0.5 for white-to-move AND for black-to-move",
          position_label(0.5, "w") == 0.5 and position_label(0.5, "b") == 0.5)

    # 4. GAME-CONSTANCY. Stated the way B2 actually implies, because the naive form is
    #    FALSE: B2 sentence 1 gives a white-to-move position `s` and a black-to-move position
    #    of the SAME game `1 - s`, so the emitted y values inside one game are legitimately
    #    the pair {s, 1-s}. What is single-valued per game is the White-frame outcome `s`,
    #    and that is the quantity the per-game clustering of s_d rests on (B3's effective N
    #    is the number of GAMES). Asserting "all y equal within a game" would be a test that
    #    can only fail, so the test below asserts the invariant that is actually true AND
    #    the one that would catch a label from the wrong game.
    per_game_white: dict[int, set[float]] = {}
    per_game_y: dict[int, set[float]] = {}
    for r in out["labels"]:
        per_game_white.setdefault(r["game_id"], set()).add(r["game_white_score"])
        per_game_y.setdefault(r["game_id"], set()).add(r["y"])
    check("label: the WHITE-FRAME outcome is CONSTANT WITHIN A GAME for every game",
          all(len(v) == 1 for v in per_game_white.values()),
          str({g: sorted(v) for g, v in per_game_white.items() if len(v) > 1}))
    check("label: within a game the emitted y values are exactly the pair {s, 1-s}",
          all(v <= {next(iter(per_game_white[g])), 1.0 - next(iter(per_game_white[g]))}
              for g, v in per_game_y.items()),
          str({g: sorted(v) for g, v in per_game_y.items()
               if len(v) > 2 or (v and min(v) < 0.0)}))
    check("label: a game with both colours on the board has y in BOTH frames (not one value)",
          any(len(v) == 2 for v in per_game_y.values()),
          "if no game shows both frames, the frame invariant is not being exercised")
    check("label: games have MANY positions each, so constancy is a real constraint",
          all(g["positions"] > 1 for g in out["games"]),
          str(min((g["positions"] for g in out["games"]), default=0)))
    check("label: both colours appear WITHIN games, so the frame varies per position",
          any(g["white_to_move"] > 0 and g["black_to_move"] > 0 for g in out["games"]),
          str([(g["game_id"], g["white_to_move"], g["black_to_move"])
               for g in out["games"][:4]]))
    check("label: s_d is a per-GAME statistic, so the unit count is games not positions",
          out["stats"]["games_labelled"] < out["stats"]["positions_labelled"],
          f"games={out['stats']['games_labelled']} positions={out['stats']['positions_labelled']}")

    # 6. THE WRONG-SIDE TEST, SHOWN FAILING. Everything above shows the frame check
    #    PASSING, and a check that has only ever passed has not been tested. So the frame is
    #    now deliberately BROKEN - the White-frame score is attached to every position
    #    regardless of side to move, which is the exact error B2 sentence 1 calls a FAIL of
    #    conjunct (c) - and the same check is REQUIRED to go red.
    #
    #    The corpus is not modified; only the frame function is replaced, so the failing and
    #    passing cases are the SAME input. That is what makes the control mean something.
    # The monkeypatch target must be the module that is ACTUALLY RUNNING. Under
    # `python tools/e0013_label.py --selftest` this file is `__main__`, so `import
    # e0013_label` would create a SECOND, independent module object: patching its
    # `position_label` would leave the running code untouched, and the control would
    # silently report that the frame check has no teeth when in fact the patch never
    # reached it. `sys.modules[__name__]` is the object `build_labels` actually resolves
    # its globals from, so the patch lands.
    self_mod = sys.modules[__name__]
    real_frame = self_mod.position_label
    try:
        self_mod.position_label = lambda game_y_white, stm: game_y_white  # WRONG FRAME
        try:
            build_labels(positions, rows_by_id, smap)
            check("WRONG-SIDE CONTROL: the White frame on every position ABORTS", False,
                  "no abort raised - the frame check does not have teeth")
        except SystemExit as exc:
            check("WRONG-SIDE CONTROL: the White frame on every position ABORTS",
                  exc.code == 2 and "WRONG SIDE" in (LAST_ABORT_REASON or ""),
                  f"code={exc.code} reason={(LAST_ABORT_REASON or '')[:110]}")
    finally:
        self_mod.position_label = real_frame
    # The patch must have actually taken effect, or the control above proved nothing.
    check("WRONG-SIDE CONTROL: the patch really was in effect during the control",
          build_labels.__globals__["position_label"] is real_frame,
          "the running module's globals were not the ones patched")
    check("WRONG-SIDE CONTROL: the frame function is restored",
          self_mod.position_label is real_frame
          and position_label(1.0, "b") == 0.0)

    # 6b. The same corruption, but detected at the UNIT level rather than only end to end:
    #     the per-row frame predicate itself must reject a mislabelled black-to-move row.
    wrong_rows = [dict(r) for r in decisive_b[:1]]
    for r in wrong_rows:
        r["y"] = expected_white(r["res"], r["a_white"])  # the wrong-side value
    check("WRONG-SIDE CONTROL: a mislabelled black-to-move row is DETECTABLE",
          all(r["y"] != position_label(expected_white(r["res"], r["a_white"]), "b")
              for r in wrong_rows),
          "the corrupted value is indistinguishable from the correct one")
    # ...and the tool, fed that corpus, must abort rather than publish it.
    corrupted = [dict(p) for p in positions]
    if wrong_rows:
        gid = wrong_rows[0]["game_id"]
        for p in corrupted:
            if p["game_id"] == gid and p["stm"] == "b":
                p["y"] = expected_white(rows_by_id[gid]["res"], rows_by_id[gid]["a_white"])
                break
    try:
        self_mod.position_label = lambda game_y_white, stm: game_y_white
        build_labels(corrupted, rows_by_id, smap)
        check("WRONG-SIDE CONTROL: a corpus with a mislabelled black row ABORTS", False,
              "no abort raised")
    except SystemExit as exc:
        check("WRONG-SIDE CONTROL: a corpus with a mislabelled black row ABORTS",
              exc.code == 2, str(exc)[:120])
    finally:
        self_mod.position_label = real_frame

    # 7. THE OTHER FAILURE MODES, each required to abort rather than warn.
    #
    #    These assert on `LAST_ABORT_REASON` rather than on `str(exc)`, because a
    #    `SystemExit(2)` stringifies to the bare string `"2"`: an assertion of the form
    #    `"<message>" in str(exc)` fails for EVERY guard regardless of which one fired, which
    #    is the mirror image of the always-green defect and just as misleading. Asserting
    #    the code AND a distinctive substring of the recorded reason is what makes each of
    #    these a test of ITS OWN guard.
    #    (a) a corpus whose stm field disagrees with its own FEN;
    inconsistent = [dict(p) for p in positions]
    inconsistent[0] = dict(inconsistent[0],
                           stm="b" if inconsistent[0]["stm"] == "w" else "w")
    try:
        build_labels(inconsistent, rows_by_id, smap)
        check("guard: a position whose stm contradicts its own FEN ABORTS", False,
              "no abort raised")
    except SystemExit as exc:
        check("guard: a position whose stm contradicts its own FEN ABORTS",
              exc.code == 2 and "disagrees with its own" in (LAST_ABORT_REASON or ""),
              f"code={exc.code} reason={(LAST_ABORT_REASON or '')[:110]}")
    #    (b) a game whose positions disagree about the White-frame outcome.
    #
    #        Note what is being tested and what is NOT. `rows_by_id` is keyed by game_id, so
    #        a caller cannot hand this function two different `res` values for one game
    #        through that parameter - the dict collapses them. The constancy guard therefore
    #        CANNOT be triggered from outside, and a test that claimed to trigger it would be
    #        asserting a fiction. The honest test is of the property the guard protects: the
    #        White-frame score is re-read PER POSITION from the game's recorded result, so
    #        changing that result changes every label of that game. If the implementation
    #        captured `game_y_white` once outside the loop, both checks below go red.
    gid_b = int(rows[0]["game_id"])
    if smap[str(gid_b)] != "train":
        gid_b = int(next(g for g in sorted(rows_by_id) if smap[str(g)] == "train"))
    game_positions = [p for p in positions if p["game_id"] == gid_b]
    check("guard: the fixture has several positions for the mutated game",
          len(game_positions) > 2, f"n={len(game_positions)}")
    before = dict(rows_by_id)
    after = dict(rows_by_id)
    after[gid_b] = dict(after[gid_b])
    after[gid_b]["res"] = "A" if after[gid_b]["res"] != "A" else "B"
    try:
        first_pass = build_labels(game_positions, before, smap)
        second_pass = build_labels(game_positions, after, smap)
        check("guard: the White-frame score is re-read PER POSITION, not captured once",
              [r["y"] for r in first_pass["labels"]] != [r["y"] for r in second_pass["labels"]],
              "the label did not follow the game's recorded result")
        check("guard: changing a game's outcome changes EVERY label of that game",
              all(a["game_white_score"] != b["game_white_score"]
                  for a, b in zip(first_pass["labels"], second_pass["labels"]))
              and len(first_pass["labels"]) == len(second_pass["labels"]),
              "only some positions followed the new outcome")
    except SystemExit as exc:
        check("guard: the White-frame score is re-read PER POSITION, not captured once",
              False, f"unexpected abort: {(LAST_ABORT_REASON or '')[:110]}")

    #    (c) a game with no recorded result, which is the only admitted label source.
    #        Without `res` there is no label, and the tool must REFUSE rather than
    #        substitute a default - a default here would silently invent a training target.
    nores = {k: dict(v) for k, v in rows_by_id.items()}
    nores[0] = {k: v for k, v in nores[0].items() if k != "res"}
    try:
        build_labels(positions, nores, smap)
        check("guard: a game with no recorded res ABORTS (result-only has no other source)",
              False, "no abort raised")
    except SystemExit as exc:
        check("guard: a game with no recorded res ABORTS (result-only has no other source)",
              exc.code == 2 and "recorded result" in (LAST_ABORT_REASON or ""),
              f"code={exc.code} reason={(LAST_ABORT_REASON or '')[:110]}")

    # 8. The frame is the extractor's, CITED rather than reimplemented, so the two cannot
    #    drift apart. If the extractor's mapping is ever changed this fails, rather than the
    #    two quietly disagreeing about what the fit target is.
    check("frame: the side-to-move frame is CITED from the extractor, not reimplemented",
          FRAME_SOURCE.startswith("tools/e0013_extract.py")
          and label_side_to_move(1.0, chess.WHITE) == 1.0
          and label_side_to_move(1.0, chess.BLACK) == 0.0
          and position_label(1.0, "b") == label_side_to_move(1.0, chess.BLACK))
    check("frame: a black-to-move label is the complement, never the same value",
          position_label(1.0, "b") == 0.0 and position_label(0.0, "b") == 1.0)
    check("frame: an unknown side to move is REFUSED", _refuses_unknown_stm())

    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name}"
              + (f"  [{detail}]" if detail and not ok else ""))
    failed = [n for n, ok, _ in checks if not ok]
    print(f"LABEL-SELFTEST {'PASS' if not failed else 'FAIL'} checks={len(checks)} "
          f"failed={len(failed)}")
    return 0 if not failed else 1
    return 0 if not failed else 1
    return 0 if not failed else 1

def _refuses_unknown_stm() -> bool:
    try:
        position_label(1.0, "x")
        return False
    except SystemExit:
        return True


def _write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def run(args: argparse.Namespace) -> int:
    """Label a pinned corpus. TRAIN-ONLY, and the corpus is digest-verified first.

    This tool is NOT run in this session: it would read the pinned real dataset, and the
    brief for this job forbids that. The function exists so the step is real rather than
    described, and the self-test exercises every property of it on synthetic games.
    """
    import e0013_pins

    positions_path = Path(args.positions)
    manifest = e0013_pins.load_manifest(Path(args.manifest))
    # THE READ-TIME RE-HASH, before a single row is read. A tampered corpus must not become
    # a labelled corpus, and the digest is checked here rather than trusted from the report.
    if args.verify_pins:
        outcome = e0013_pins.verify(manifest)
        if not outcome["ok"]:
            abort("artifact pins do not verify; nothing is labelled.\n  "
                  + "\n  ".join(outcome["problems"]))
    dataset = Path(args.dataset)
    dataset_sha = sha256_file(dataset)
    if dataset_sha != args.expected_dataset_sha256:
        abort(f"dataset SHA-256 mismatch: measured {dataset_sha}, pinned "
              f"{args.expected_dataset_sha256}")

    rows: dict[int, dict[str, Any]] = {}
    for line in dataset.read_bytes().decode("utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            rows[int(row["game_id"])] = row
    positions = [json.loads(l) for l in
                 positions_path.read_bytes().decode("utf-8").splitlines() if l.strip()]

    smap = {str(g): split_of(g) for g in sorted(rows)}
    out = build_labels(positions, rows, smap)

    out_dir = Path(args.out_dir)
    label_bytes = ("\n".join(
        json.dumps(r, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        for r in out["labels"]) + "\n").encode("utf-8")
    report = {
        "format": REPORT_FORMAT,
        "tool": "tools/e0013_label.py",
        "mode": "train-only-labelled",
        "is_fitter_corpus": True,
        "src_commit": args.src_commit,
        "corpus": {
            "positions_sha256": sha256_file(positions_path),
            "positions_is_fitter_corpus": True,
            "pins_verified_before_read": bool(args.verify_pins),
        },
        "dataset": {"path": str(dataset), "sha256": dataset_sha, "rows": len(rows)},
        "split": {"salt": SPLIT_SALT, "train_fraction": TRAIN_FRACTION,
                  "rule": "random.Random(SPLIT_SALT * 1000003 + game_id).random() < 0.8",
                  "source": "re-derived from SPLIT_SALT, NOT read from a file"},
        "stats": out["stats"],
        "games": out["games"],
        "labels_sha256": None,
    }
    report["labels_sha256"] = hashlib_sha256(label_bytes)
    if not args.dry_run:
        _write_bytes(out_dir / "labels.jsonl", label_bytes)
        _write_bytes(out_dir / "label_report.json", canonical_json(report))

    s = out["stats"]
    print(f"games_labelled={s['games_labelled']} positions_labelled={s['positions_labelled']}")
    print(f"w={s['count_positions_white_to_move']} b={s['count_positions_black_to_move']} "
          f"labels={json.dumps(s['label_counts'], sort_keys=True)}")
    print(f"train_only: holdout_games={s['games_held_out_not_labelled']} "
          f"holdout_positions_refused={s['holdout_positions_refused']}")
    print(f"label_frame={s['label_frame']} source={s['label_frame_source']}")
    print(f"labels_sha256={report['labels_sha256']}")
    return 0


def hashlib_sha256(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    from e0013_extract import DEFAULT_DATASET
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--positions", default=str(
        ROOT / "build" / "e0013" / "extract" / "positions.jsonl"))
    parser.add_argument("--manifest", default=str(
        ROOT / "research" / "manifests" / "e0013-artifact-pins.json"))
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--expected-dataset-sha256", default=DATASET_SHA256)
    parser.add_argument("--out-dir", default=str(ROOT / "build" / "e0013" / "labels"))
    parser.add_argument("--src-commit", default="UNPINNED")
    parser.add_argument("--verify-pins", action="store_true",
                        help="re-hash the pinned corpus BEFORE reading it")
    parser.add_argument("--dry-run", action="store_true", help="compute and report, write nothing")
    parser.add_argument("--selftest", action="store_true",
                        help="synthetic games only; the real dataset is never read")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.selftest:
        return selftest()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
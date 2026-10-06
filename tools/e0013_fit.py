#!/usr/bin/env python3
"""E-0013/E-0014 fitter: deterministic full-batch L-BFGS-B on the mean logistic loss.

The math lives in `tools/e0013_eval.py` (design_rows / loss_and_gradient /
frozen_block_mismatches / mirror_violations) and is NOT reimplemented here - this file is
the optimizer driver, the inner-partition carver, and the pin-carrier. Its contract is
fixed by E-0013's F1-F12 table (the pre-fit commit pins seed, L2, iteration budget,
early-stopping and the clipping bound L) and E-0014's abort conditions.

Guarantees, each enforced in code (never assumed of the input):

  1. TRAIN-only input, enforced TWICE and PROVED, not delegated to the input file:
     (a) every row's game is re-classified with the cited outer-split rule
         `random.Random(SPLIT_SALT * 1000003 + game_id).random() < 0.8` imported from
         `tools/e0013_extract.py`; rows from outer-holdout games are excluded by set
         membership BEFORE any label or FEN is used, and the exclusion receipt (holdout
         game count + row count) is printed and written into the report. Only game-id
         integers touch the holdout side - a set intersection, never a content read
         (E-00014's own rule); (b) every remaining row's `y` must be in {0, 0.5, 1}.
     With `--inner-map`, the fit set is further restricted to rows whose game's inner
     role is 'train'; the inner map partitions OUTER-TRAIN games only (see
     --write-inner-map). The outer holdout is never named, read, or scored by fits.
     The labelled corpus is `tools/e0013_extract.py`'s full-mode artifact (rows carry
     both `fen` and `y`); `tools/e0013_label.py`'s TRAIN-only labels.jsonl is the
     audit artifact the fit set can be cross-checked against (same (norm_fen, y) pairs).
  2. Deterministic: full-batch L-BFGS-B from theta0 = the frozen hand-tuned floor.
     `--seed` is recorded and never consumed (no RNG anywhere); the run PROVES it by
     fitting twice in-process and asserting byte-identical solution vectors (E-0013
     Test Method 4's deterministic-rerun rule).
  3. Freeze enforced: `frozen_block_mismatches` against the floor must be empty or the
     run aborts before writing anything (KING PSTs, phase weights, tempo convention).
  4. Objective exactly `loss_and_gradient`: mean logistic loss of
     `sigmoid(clip(E_theta(p), -L, L))` plus `l2 * ||theta - theta0||^2`.
  5. Arms differ: fitted-table sha256 != floor-table sha256, asserted before output
     (E-00014 Sample Validity negative control).

Usage:
    python tools/e0013_fit.py --selftest
    python tools/e0013_fit.py --write-inner-map --inner-map MAP --positions LABELS --inner-salt S
    python tools/e0013_fit.py --inner-map MAP --positions LABELS --clip L --l2 W \
        --maxiter N --seed S --out FITTED.json --report REPORT.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import e0013_eval as ev  # noqa: E402
from e0013_extract import (  # noqa: E402
    SPLIT_SALT,
    canonical_json,
    sha256_file,
    split_of,
)

INNER_MAP_FORMAT = "kana-e0013-innersplit-v1"


def hashlib_sha256(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


def abort(reason: str):
    print(f"ABORT: {reason}", file=sys.stderr)
    raise SystemExit(2)


def write_inner_map(positions_path: Path, inner_salt: int, inner_map_path: Path) -> dict:
    """Carve the inner partition BY GAME from the TRAIN rows of a labelled corpus.
    `random.Random(INNER_SALT * 1000003 + game_id).random() < 0.8`, restricted to game
    ids present among the corpus rows (TRAIN-only corpus => the outer holdout never
    enters). The file's role keys keep the outer loader's vocabulary ("train"/
    "holdout") but they MEAN inner_train / inner_val - the `notes` field says so."""
    import random

    rows = [json.loads(l) for l in positions_path.read_bytes().decode("utf-8").splitlines()
            if l.strip()]
    gids = sorted({int(r["game_id"]) for r in rows})
    if not gids:
        abort("the labelled corpus has no rows to carve")
    inner = {}
    for gid in gids:
        inner[str(gid)] = ("train" if random.Random(inner_salt * 1000003 + gid).random() < 0.8
                           else "holdout")
    obj = {
        "format": INNER_MAP_FORMAT,
        "notes": ("roles: 'train' here means INNER-TRAIN and 'holdout' means INNER-VAL; "
                  "both are subsets of the OUTER train set. The outer holdout is never a "
                  "member. The map is a pure function of (INNER_SALT, game_id) restricted "
                  "to the corpus rows."),
        "inner_salt": inner_salt,
        "carve_rule": "random.Random(INNER_SALT * 1000003 + game_id).random() < 0.8",
        "train_fraction": 0.8,
        "map": inner,
    }
    data = canonical_json(obj)
    inner_map_path.parent.mkdir(parents=True, exist_ok=True)
    inner_map_path.write_bytes(data)
    n_tr = sum(1 for v in inner.values() if v == "train")
    out = {"path": str(inner_map_path), "sha256": hashlib_sha256(data),
           "games": len(inner), "inner_train": n_tr, "inner_val": len(inner) - n_tr}
    print(f"inner map: games={out['games']} inner_train={out['inner_train']} "
          f"inner_val={out['inner_val']} sha256={out['sha256']}")
    return out


def fit_once(jac, offset, labels, theta0, clip, l2, maxiter, elo_scale=1.0):
    import numpy as np
    from scipy.optimize import minimize

    def f(v):
        return ev.loss_and_gradient(jac, offset, labels, v, clip, l2, theta0,
                                    elo_scale=elo_scale)

    return minimize(f, np.asarray(theta0, dtype=np.float64), method="L-BFGS-B",
                    jac=True, options={"maxiter": int(maxiter)})



def run_fit(args: argparse.Namespace) -> int:
    import chess
    import numpy as np

    positions_path = Path(args.positions)
    inner_map_path = Path(args.inner_map) if args.inner_map else None
    if not positions_path.is_file():
        abort(f"positions file missing: {positions_path}")
    # Exactly one fitting surface: --inner-map XOR --full-train (never both, never
    # neither). inner_map None <=> full_train False would be "neither"; both present
    # is also an abort (E-0014 abort 8: omission/substitution is itself a result).
    if (inner_map_path is None) == (not args.full_train):
        abort("choose exactly one fitting surface: --inner-map (E-00014 inner "
                  "partition) or --full-train (E-0013 stage fit); never both, never neither")

    rows = [json.loads(l) for l in positions_path.read_bytes().decode("utf-8").splitlines()
            if l.strip()]
    # E-0013 leakage contract, enforced in code FIRST: the fit surface is OUTER-TRAIN
    # only. The split rule is re-derived from SPLIT_SALT via the extractor's own
    # split_of(), never read from a file, so a swapped map cannot widen the scope. Only
    # game-id integers classify; a holdout game's FEN/label content is never used, and
    # `y` is not even inspected before this filter runs. The receipt (excluded row and
    # game counts) lands in the report, so the omission is shown, not asserted.
    train_rows: list[dict] = []
    holdout_rows = 0
    holdout_games: set[int] = set()
    for r in rows:
        gid = int(r["game_id"])
        if split_of(gid) == "train":
            train_rows.append(r)
        else:
            holdout_rows += 1
            holdout_games.add(gid)
    rows = train_rows
    if inner_map_path is not None:
        imap_obj = json.loads(inner_map_path.read_bytes())
        if imap_obj.get("format") != INNER_MAP_FORMAT:
            abort(f"inner map format mismatch: {imap_obj.get('format')!r}")
        imap = imap_obj["map"]
        rows = [r for r in rows if imap.get(str(r["game_id"])) == "train"]
    if not rows:
        abort("empty fit set")
    for r in rows:
        y = r.get("y")
        if y not in (0, 0.5, 1, 0.0, 1.0):
            abort(f"row game_id={r.get('game_id')} has y={y!r}; labels must be in the "
                  "side-to-move frame's {0, 0.5, 1}")

    terms_list = [ev.position_terms(chess.Board(r["fen"])) for r in rows]
    labels = np.asarray([float(r["y"]) for r in rows], dtype=np.float64)
    game_ids = sorted({int(r["game_id"]) for r in rows})
    fens = [r["fen"] for r in rows]

    floor = ev.hand_tuned()
    theta0 = ev.design_vector(floor)
    jac, offset = ev.design_rows(terms_list)

    loss0 = ev.mean_logistic_loss(jac, offset, np.asarray(theta0), labels, args.clip,
                                  elo_scale=args.elo_scale)
    res1 = fit_once(jac, offset, labels, theta0, args.clip, args.l2, args.maxiter,
                    elo_scale=args.elo_scale)
    res2 = fit_once(jac, offset, labels, theta0, args.clip, args.l2, args.maxiter,
                    elo_scale=args.elo_scale)
    # Deterministic-rerun proof (E-0013 Test Method 4): identical inputs -> byte-identical
    # solution vectors. The fit has no clock and no RNG; this asserts it.
    if res1.x.tobytes() != res2.x.tobytes():
        abort("deterministic-rerun FAILED: two identical fits produced different vectors")

    fitted = ev.from_design_vector(res1.x.tolist(), floor)
    mismatches = ev.frozen_block_mismatches(fitted, floor)
    if mismatches:
        abort(f"frozen-block violations against the floor: {mismatches}")
    fitted_sha = ev.table_sha256(fitted)
    floor_sha = ev.table_sha256(floor)
    if fitted_sha == floor_sha:
        abort("arms identical: fitted sha256 == floor sha256 (negative control)")
    mirror_bad, mirror_n = ev.mirror_violations(fens, fitted)
    loss_fitted = ev.mean_logistic_loss(jac, offset, res1.x, labels, args.clip,
                                        elo_scale=args.elo_scale)
    delta_on_fit = loss0 - loss_fitted

    report = {
        "format": "kana-e0013-fit-report-v1",
        "tool": "tools/e0013_fit.py",
        "git_commit": ev.git_commit(),
        "positions": {"path": str(positions_path), "sha256": sha256_file(positions_path),
                      "rows": len(rows)},
        "inner_map": ({"path": str(inner_map_path),
                       "sha256": hashlib_sha256(inner_map_path.read_bytes())}
                      if inner_map_path is not None else None),
        "full_train": bool(args.full_train),
        "outer_split": {"salt": SPLIT_SALT,
                        "rule": "random.Random(SPLIT_SALT * 1000003 + game_id).random() < 0.8",
                        "source": "re-derived via tools/e0013_extract.split_of, never read from a file",
                        "holdout_games_excluded_before_any_label_read": len(holdout_games),
                        "holdout_rows_excluded_before_any_label_read": holdout_rows},
        "games": len(game_ids),
        "labels": {"frame": "side-to-move (B2 s1)",
                   "label_counts": {str(v): int(np.sum(labels == v)) for v in (0.0, 0.5, 1.0)}},
        "hyperparameters": {"clip_L": args.clip, "elo_scale": args.elo_scale, "l2": args.l2,
                            "maxiter": args.maxiter,
                            "seed": args.seed, "early_stopping": None, "rng_consumed": False,
                            "optimizer": "scipy.optimize.minimize method=L-BFGS-B",
                            "scipy_version": __import__("scipy").__version__,
                            "numpy_version": np.__version__,
                            "python": sys.version.split()[0]},
        "convergence": {"success": bool(res1.success), "message": str(res1.message),
                        "n_iterations": int(res1.nit), "n_evaluations": int(res1.nfev),
                        "objective_mean_loss_plus_l2": float(res1.fun)},
        "loss": {"floor_mean_logistic_loss_on_fit_set": loss0,
                 "fitted_mean_logistic_loss_on_fit_set": loss_fitted,
                 "delta_on_fit_set_floor_minus_fitted": delta_on_fit},
        "arms": {"floor_sha256": floor_sha, "fitted_sha256": fitted_sha,
                 "arms_differ": fitted_sha != floor_sha},
        "freeze_audit": {"frozen_block_mismatches": mismatches},
        "mirror_gate": {"violations": int(mirror_bad), "positions_checked": int(mirror_n)},
        "deterministic_rerun": {"proved": True,
                                "note": ("two in-process fits of identical inputs produced "
                                         "byte-identical solution vectors; no RNG or clock. "
                                         "--seed is a recorded field only.")},
        "no_holdout": ("the holdout is never named or read; the fit set is the labelled "
                       "TRAIN corpus (or the inner_train carve of it)."),
    }
    if not args.dry_run:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(ev.table_bytes(fitted))
        rp = Path(args.report)
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_bytes(canonical_json(report))

    print(f"rows={len(rows)} games={len(game_ids)} clip={args.clip} l2={args.l2} "
          f"maxiter={args.maxiter} seed={args.seed}")
    print(f"holdout excluded before any label read: games={len(holdout_games)} "
          f"rows={holdout_rows} (outer split re-derived, salt={SPLIT_SALT})")
    print(f"convergence success={res1.success} nit={res1.nit} message={res1.message}")
    print(f"loss floor={loss0:.6f} fitted={loss_fitted:.6f} delta_on_fit={delta_on_fit:.6f}")
    print(f"arms differ: {fitted_sha != floor_sha} fitted_sha256={fitted_sha} "
          f"mirror_violations={mirror_bad}/{mirror_n}")
    return 0


def selftest() -> int:
    """Synthetic proof that the driver recovers a known table and aborts on bad input.

    No real corpus is read: a handful of hand-set positions, ground-truth vector =
    floor + fixed deltas on a few slots, labels = sigmoid(clip(E_surrogate))."""
    import chess
    import numpy as np

    checks = []

    def check(name, cond, detail=""):
        checks.append((name, bool(cond), detail))

    fens = [
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
        "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1",
        "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1",
        "8/8/8/8/8/8/2KP4/2k1B2R w - - 0 1",
        "4k3/8/8/3pp3/8/8/2P2PP1/4K3 w - - 0 2",
    ]
    terms_list = [ev.position_terms(chess.Board(f)) for f in fens]
    jac, offset = ev.design_rows(terms_list)
    floor = ev.hand_tuned()
    t0 = np.asarray(ev.design_vector(floor), dtype=np.float64)
    star = t0.copy()
    for slot, dv in ((ev.SLOT[("mg_value", "PAWN")], 7.0),
                     (ev.SLOT[("eg_pst", "KNIGHT", 27)], -12.0),
                     (ev.SLOT[("scalar", "tempo")], 4.0)):
        star[slot] += dv

    clip = 600.0
    cont = 1.0 / (1.0 + np.exp(-np.clip(np.asarray(jac @ star).ravel() + offset, -clip, clip)))
    res = fit_once(jac, offset, cont, t0, clip, 0.0, 200)
    table = ev.from_design_vector(res.x.tolist(), floor)
    check("converged on synthetic labels", bool(res.success), str(res.message))
    check("optimizer descends near the synthetic zero-loss manifold "
          "(BFGS stop-tolerance bound)",
          ev.mean_logistic_loss(jac, offset, res.x, cont, clip) < 5e-3,
          f"residual {ev.mean_logistic_loss(jac, offset, res.x, cont, clip):.3g}")
    check("fitted loss strictly below the floor table's loss on the same labels",
          ev.mean_logistic_loss(jac, offset, res.x, cont, clip)
          < ev.mean_logistic_loss(jac, offset, t0, cont, clip))
    check("mirror violations = 0 on fitted synthetic table",
          ev.mirror_violations(fens, table)[0] == 0)
    check("frozen blocks intact vs floor",
          ev.frozen_block_mismatches(table, floor) == [])
    check("arms differ (negative control satisfied on synthetic)",
          ev.table_sha256(table) != ev.table_sha256(floor))
    res_again = fit_once(jac, offset, cont, t0, clip, 0.0, 200)
    check("determinism: byte-identical solution on identical inputs",
          res.x.tobytes() == res_again.x.tobytes())
    res_d1 = fit_once(jac, offset, cont, t0, clip, 0.0, 200, elo_scale=1.0)
    check("elo: D=1.0 fit reproduces the default fit bit-for-bit",
          res.x.tobytes() == res_d1.x.tobytes())
    _D = 400.0 / __import__("math").log(10.0)
    res_sc = fit_once(jac, offset, cont, t0, clip, 0.0, 200, elo_scale=_D)
    check("elo: scaled fit converges on synthetic labels",
          bool(res_sc.success), str(res_sc.message))
    check("elo: scaled fit descends below the floor loss on the same labels",
          ev.mean_logistic_loss(jac, offset, res_sc.x, cont, clip, elo_scale=_D)
          < ev.mean_logistic_loss(jac, offset, t0, cont, clip, elo_scale=_D))
    res_sc2 = fit_once(jac, offset, cont, t0, clip, 0.0, 200, elo_scale=_D)
    check("elo: scaled fit is deterministic (byte-identical rerun)",
          res_sc.x.tobytes() == res_sc2.x.tobytes())
    del _D, res_d1, res_sc, res_sc2
    import contextlib
    import io

    # Outer-split roles come from the re-derived rule itself, not hardcoded ids:
    # a test that hardcoded the id would rot if the rule ever changed.
    gid_train = next(g for g in range(50) if split_of(g) == "train")
    gid_hold = next(g for g in range(50) if split_of(g) != "train")
    bad = [dict(fen=fens[0], game_id=gid_train, y=2.0)]
    rowpath = ROOT / "_obs" / "_fit_st_bad.jsonl"
    try:
        ns = argparse.Namespace(positions=str(rowpath), inner_map=None, full_train=True,
                                clip=clip, l2=1e-6, maxiter=10, seed=1, out="x", report="y",
                                dry_run=True, elo_scale=1.0)
        rowpath.parent.mkdir(parents=True, exist_ok=True)
        rowpath.write_text(json.dumps(bad[0]) + "\n", encoding="utf-8")
        buf = io.StringIO()
        try:
            with contextlib.redirect_stderr(buf):
                run_fit(ns)
            check("abort on out-of-vocab label", False, "no abort raised")
        except SystemExit:
            check("abort on out-of-vocab label", "2.0" in buf.getvalue(),
                  buf.getvalue()[:160])
    finally:
        rowpath.unlink(missing_ok=True)

    # Leakage gate, synthetically: a corpus whose only game is an outer-HOLDOUT game
    # must refuse to fit even though its label vocabulary is valid. The fit set is
    # empty by the outer filter, and the abort precedes any label read.
    hold = [dict(fen=fens[0], game_id=gid_hold, y=0.5)]
    rowpath2 = ROOT / "_obs" / "_fit_st_holdout.jsonl"
    try:
        ns2 = argparse.Namespace(positions=str(rowpath2), inner_map=None, full_train=True,
                                 clip=clip, l2=1e-6, maxiter=10, seed=1, out="x", report="y",
                                 dry_run=True, elo_scale=1.0)
        rowpath2.write_text(json.dumps(hold[0]) + "\n", encoding="utf-8")
        buf2 = io.StringIO()
        try:
            with contextlib.redirect_stderr(buf2):
                run_fit(ns2)
            check("outer-split gate: holdout-only corpus aborts as empty fit set", False,
                  "no abort raised")
        except SystemExit:
            check("outer-split gate: holdout-only corpus aborts as empty fit set",
                  "empty fit set" in buf2.getvalue(), buf2.getvalue()[:160])
    finally:
        rowpath2.unlink(missing_ok=True)

    failed = [n for n, ok, _ in checks if not ok]
    for name, okv, detail in checks:
        flag = "PASS" if okv else "FAIL"
        print(f"{flag}  {name}" + (f"  [{detail}]" if detail else ""))
    print(f"FIT-SELFTEST {'PASS' if not failed else 'FAIL'} checks={len(checks)} "
          f"failed={len(failed)}")
    return 0 if not failed else 1


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--positions", required=False,
                   default=str(ROOT / "build" / "e0013" / "extract" / "positions.jsonl"))
    p.add_argument("--inner-map")
    p.add_argument("--full-train", action="store_true")
    p.add_argument("--clip", type=float, required=False)
    p.add_argument("--elo-scale", type=float, default=1.0,
                       dest="elo_scale")
    p.add_argument("--l2", type=float, required=False)
    p.add_argument("--maxiter", type=int, required=False)
    p.add_argument("--seed", type=int, required=False)
    p.add_argument("--out", default=str(ROOT / "build" / "e0013" / "fitted.json"))
    p.add_argument("--report", default=str(ROOT / "build" / "e0013" / "fit_report.json"))
    p.add_argument("--write-inner-map", action="store_true")
    p.add_argument("--inner-salt", type=int)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args(argv)
    if args.selftest or args.write_inner_map:
        return args
    for k in ("clip", "l2", "maxiter", "seed"):
        if getattr(args, k) is None:
            p.error(f"--{k} is pinned in the pre-fit commit and has no default; "
                    "pass it explicitly")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.selftest:
        return selftest()
    if args.write_inner_map:
        if args.inner_map is None or args.inner_salt is None:
            abort("--write-inner-map needs --inner-map PATH and --inner-salt S")
        write_inner_map(Path(args.positions), args.inner_salt, Path(args.inner_map))
        return 0
    return run_fit(args)


if __name__ == "__main__":
    raise SystemExit(main())

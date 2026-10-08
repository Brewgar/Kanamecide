#!/usr/bin/env python3
"""Kanamecide first-training entry point (E-0017, W-0011).

Canonical command that launches (and only launches) the TRAIN-only first
training. Reuses the AUTHORIZED E-0013-family math (tools/e0013_eval.py:
design_rows / loss_and_gradient / frozen_block_mismatches /
mirror_violations / per_game_losses / paired_statistics; split rule from
tools/e0013_extract.py) and adds the missing engineering: TRAIN-only join
loader, hardened holdout firewall, preflight, dry-run, phase
checkpointing with resume, machine-readable metrics + manifest.

Subcommands:
  preflight --config CFG   verify everything BEFORE any fit; exit != 0 on
                           any broken critical invariant. Reads no holdout
                           content (game-id sets only).
  dry-run   --config CFG   same code path on a tiny synthetic subset:
                           load -> design -> forward -> loss -> backward
                           (gradient vs finite diff) -> optimizer step ->
                           checkpoint write+reload -> metrics -> manifest.
  train     --config CFG   the real TRAIN-only run (E-0017). Exactly one
                           deterministic full-batch L-BFGS-B fit on the
                           full outer-train set + paired inner-val eval.
  resume    --checkpoint C re-run deterministically from a recorded phase.
  manifest  --config CFG   print the frozen manifest identity (no run).

Firewall (structural, not a comment):
  1. TRAIN-only join: fit rows = extractor rows whose (game_id,
     norm_fen) pair is in the TRAIN-only labels file, restricted to
     outer-train game ids by the RE-DERIVED split rule (never read from
     a file). Only game-id integers + norm_fen strings touch the join.
  2. Holdout game ids are touched ONLY as a set-intersection assert
     (fit_games ∩ outer_holdout_games == ∅). Any other touch voids the
     run (abort 2). The eval path consumes the inner map READ-ONLY and
     scores inner-val roles only (missing key = outer holdout =
     excluded on game-id alone).
  3. Expected counts are abort conditions, not repairs: fit = 791 games
     / 59892 rows; inner-val = 155 games; exclusion receipt = 208 games
     / 14560 rows.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

CONFIG_FORMAT = "kana-e0017-train-config-v1"
CHECKPOINT_FORMAT = "kana-e0017-checkpoint-v1"
MANIFEST_FORMAT = "kana-e0017-manifest-v1"
METRICS_FORMAT = "kana-e0017-metrics-v1"

REQUIRED_TOP = ("format", "provenance", "model", "objective", "optimizer",
                "execution", "evaluation", "reproducibility")


def abort(reason: str):
    print(f"ABORT: {reason}", file=sys.stderr)
    raise SystemExit(2)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"


def load_config(path: Path) -> dict:
    if not path.is_file():
        abort(f"config missing: {path}")
    cfg = json.loads(path.read_bytes().decode("utf-8"))
    if cfg.get("format") != CONFIG_FORMAT:
        abort(f"config format mismatch: {cfg.get('format')!r} != {CONFIG_FORMAT!r}")
    for key in REQUIRED_TOP:
        if key not in cfg:
            abort(f"config missing required section: {key} (no magic defaults)")
    prov = cfg["provenance"]
    for key in ("dataset_path", "dataset_sha256", "labels_path",
                "labels_sha256", "corpus_path", "corpus_sha256",
                "inner_map_path", "inner_map_sha256", "outer_split_salt",
                "inner_salt", "floor_sha256", "outer_holdout_games",
                "outer_holdout_rows"):
        if key not in prov:
            abort(f"config provenance missing required key: {key}")
    model, obj, opt = cfg["model"], cfg["objective"], cfg["optimizer"]
    for key in ("family", "free_scalars", "stage"):
        if key not in model:
            abort(f"config model missing required key: {key}")
    for key in ("clip_L", "elo_scale_D", "l2"):
        if key not in obj:
            abort(f"config objective missing required key: {key}")
    for key in ("method", "maxiter", "seed"):
        if key not in opt:
            abort(f"config optimizer missing required key: {key}")
    for key in ("output_dir", "checkpoint_dir", "checkpoint_phases",
                "launch_command"):
        if key not in cfg["execution"]:
            abort(f"config execution missing required key: {key}")
    for key in ("fit_games", "fit_rows", "holdout_games_excluded",
                "holdout_rows_excluded", "join_miss_rows", "inner_val_games"):
        if key not in cfg.get("expected_counts", {}):
            abort(f"config expected_counts missing required key: {key}")
    if int(model["free_scalars"]) != 683:
        abort("config model.free_scalars != 683")
    if int(model["stage"]) != 6:
        abort("config model.stage != 6 (S* = 6)")
    if float(obj["clip_L"]) <= 0 or float(obj["elo_scale_D"]) <= 0:
        abort("config clip_L and elo_scale_D must be positive")
    if int(opt["maxiter"]) <= 0:
        abort("config optimizer.maxiter must be positive")
    return cfg




def read_labels_keys(labels_path: Path) -> set[tuple[int, str]]:
    """TRAIN-only key universe: (game_id, norm_fen) pairs. No FEN read."""
    keys: set[tuple[int, str]] = set()
    for line in labels_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        keys.add((int(r["game_id"]), str(r["norm_fen"])))
    return keys


def load_fit_rows(cfg: dict) -> tuple[list[dict], dict]:
    """TRAIN-only join loader (E-0017 Dataset rule)."""
    from e0013_extract import SPLIT_SALT, split_of
    prov = cfg["provenance"]
    labels_path = ROOT / prov["labels_path"]
    corpus_path = ROOT / prov["corpus_path"]
    for p in (labels_path, corpus_path):
        if not p.is_file():
            abort(f"input missing: {p}")
    if sha256_file(labels_path) != prov["labels_sha256"]:
        abort("TRAIN-only labels SHA mismatch (config pin violated)")
    if sha256_file(corpus_path) != prov["corpus_sha256"]:
        abort("extractor corpus SHA mismatch (config pin violated)")
    if int(SPLIT_SALT) != int(prov["outer_split_salt"]):
        abort("SPLIT_SALT != config outer_split_salt (split identity broken)")
    label_keys = read_labels_keys(labels_path)
    expected = cfg["expected_counts"]
    fit_rows: list[dict] = []
    holdout_games: set[int] = set()
    holdout_rows = 0
    train_game_rows = 0
    join_miss = 0
    for line in corpus_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        gid = int(r["game_id"])
        if split_of(gid) != "train":
            holdout_rows += 1
            holdout_games.add(gid)
            continue
        train_game_rows += 1
        if (gid, str(r.get("norm_fen"))) not in label_keys:
            join_miss += 1
            continue
        y = r.get("y")
        if y not in (0, 0.5, 1, 0.0, 1.0):
            abort(f"row game_id={gid} has y={y!r}; must be in {{0, 0.5, 1}}")
        if r.get("fen") is None:
            abort(f"row game_id={gid} selected for fit has no FEN")
        fit_rows.append(r)
    fit_games = sorted({int(r["game_id"]) for r in fit_rows})
    if len(holdout_games) != int(prov["outer_holdout_games"]) or \
            holdout_rows != int(prov["outer_holdout_rows"]):
        abort(f"holdout exclusion receipt mismatch: got games={len(holdout_games)} "
              f"rows={holdout_rows}, want games={prov['outer_holdout_games']} "
              f"rows={prov['outer_holdout_rows']}")
    overlap = [g for g in fit_games if split_of(g) != "train"]
    if overlap:
        abort(f"firewall breach: {len(overlap)} fit games are outer-holdout")
    if len(fit_games) != int(expected["fit_games"]) or \
            len(fit_rows) != int(expected["fit_rows"]):
        abort(f"fit universe mismatch: got games={len(fit_games)} rows={len(fit_rows)}, "
              f"want games={expected['fit_games']} rows={expected['fit_rows']} "
              f"(join_miss={join_miss})")
    if join_miss != int(expected["join_miss_rows"]):
        abort(f"TRAIN-only join left unmatched TRAIN rows: join_miss={join_miss} "
              f"!= expected {expected['join_miss_rows']}")
    info = {"fit_games": len(fit_games), "fit_rows": len(fit_rows),
            "holdout_games_excluded": len(holdout_games),
            "holdout_rows_excluded": holdout_rows,
            "train_game_rows_seen": train_game_rows, "join_miss": join_miss}
    return fit_rows, info


def load_inner_val(cfg: dict) -> tuple[list[dict], dict]:
    """Inner-val eval rows: inner-map role 'holdout' (= inner-val) AND
    outer-train. Missing key = outer holdout = excluded on game-id alone.
    Map consumed READ-ONLY (never re-carved here)."""
    from e0013_extract import split_of
    prov = cfg["provenance"]
    corpus_path = ROOT / prov["corpus_path"]
    imap_path = ROOT / prov["inner_map_path"]
    for p in (corpus_path, imap_path):
        if not p.is_file():
            abort(f"input missing: {p}")
    if sha256_file(imap_path) != prov["inner_map_sha256"]:
        abort("inner map SHA mismatch (config pin violated)")
    imap_obj = json.loads(imap_path.read_bytes().decode("utf-8"))
    if imap_obj.get("format") != "kana-e0013-innersplit-v1":
        abort(f"inner map format mismatch: {imap_obj.get('format')!r}")
    if int(imap_obj.get("inner_salt")) != int(prov["inner_salt"]):
        abort("inner salt != config inner_salt (partition identity broken)")
    imap = imap_obj["map"]
    val_rows: list[dict] = []
    skipped_outer = 0
    for line in corpus_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        head = json.loads(line)
        gid = int(head["game_id"])
        role = imap.get(str(gid))
        if role is None:
            if split_of(gid) != "train":
                skipped_outer += 1
                continue
            abort(f"outer-train game {gid} missing from inner map (corrupt map)")
        if role != "holdout":
            continue
        if split_of(gid) != "train":
            abort(f"firewall breach: inner-val game {gid} is outer-holdout")
        if head.get("fen") is None:
            abort(f"inner-val row game_id={gid} has no FEN")
        val_rows.append(head)
    val_games = sorted({int(r["game_id"]) for r in val_rows})
    if len(val_games) != int(prov["inner_val_games"]):
        abort(f"inner-val universe mismatch: got games={len(val_games)}, "
              f"want {prov['inner_val_games']}")
    return val_rows, {"val_games": len(val_games), "val_rows": len(val_rows),
                      "skipped_outer_holdout": skipped_outer}

# --- authorized math (no reimplementation) -----------------------------------

def build_design(fit_rows: list[dict], clip: float, l2: float,
                 elo_scale: float) -> dict:
    """Design matrix + labels + theta0 via tools/e0013_eval.py.

    Returns dict(jac, offset, labels, theta0, floor, game_ids, fens).
    Aborts on empty set, bad labels, non-finite entries (fail loudly).
    """
    import chess
    import numpy as np
    import e0013_eval as ev

    if not fit_rows:
        abort("empty fit set")
    for r in fit_rows:
        y = r.get("y")
        if y not in (0, 0.5, 1, 0.0, 1.0):
            abort(f"row game_id={r.get('game_id')} has y={y!r}; "
                  "labels must be in the side-to-move frame's {0, 0.5, 1}")
        if r.get("fen") is None:
            abort(f"fit row game_id={r.get('game_id')} has no FEN")
    terms_list = [ev.position_terms(chess.Board(r["fen"])) for r in fit_rows]
    labels = np.asarray([float(r["y"]) for r in fit_rows], dtype=np.float64)
    floor = ev.hand_tuned()
    theta0 = np.asarray(ev.design_vector(floor), dtype=np.float64)
    jac, offset = ev.design_rows(terms_list)
    if int(jac.shape[0]) != len(fit_rows) or int(jac.shape[1]) != 683:
        abort(f"design matrix shape {jac.shape} != ({len(fit_rows)}, 683)")
    if not (bool(np.all(np.isfinite(offset))) and
            bool(np.all(np.isfinite(labels)))):
        abort("non-finite offset/labels in design build")
    return {"jac": jac, "offset": offset, "labels": labels, "theta0": theta0,
            "floor": floor,
            "game_ids": sorted({int(r["game_id"]) for r in fit_rows}),
            "fens": [r["fen"] for r in fit_rows]}


def fit_full_batch(des: dict, clip: float, l2: float, maxiter: int,
                   elo_scale: float):
    """Deterministic full-batch L-BFGS-B, double-fit byte-identity proof.

    Returns (res1, loss0, loss_fitted, delta_on_fit). Aborts on
    non-convergence (E-0016 amend: non-convergence = no number).
    """
    import numpy as np
    import e0013_eval as ev
    from e0013_fit import fit_once

    jac, offset, labels, theta0 = (des["jac"], des["offset"],
                                   des["labels"], des["theta0"])
    loss0 = ev.mean_logistic_loss(jac, offset, theta0, labels, clip,
                                  elo_scale=elo_scale)
    res1 = fit_once(jac, offset, labels, theta0, clip, l2, maxiter,
                    elo_scale=elo_scale)
    res2 = fit_once(jac, offset, labels, theta0, clip, l2, maxiter,
                    elo_scale=elo_scale)
    if res1.x.tobytes() != res2.x.tobytes():
        abort("deterministic-rerun FAILED: two identical fits differ")
    if not bool(res1.success):
        abort(f"optimizer did not converge: {res1.message}")
    loss_fitted = ev.mean_logistic_loss(jac, offset, res1.x, labels, clip,
                                        elo_scale=elo_scale)
    return res1, float(loss0), float(loss_fitted), float(loss0 - loss_fitted)


# --- phase checkpoints (resume = deterministic re-run from a phase) ----------

def checkpoint_path(cfg: dict, phase: str) -> Path:
    return ROOT / cfg["execution"]["checkpoint_dir"] / f"{phase}.json"


def write_checkpoint(cfg: dict, phase: str, payload: dict) -> Path:
    import e0013_eval as ev
    path = checkpoint_path(cfg, phase)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {"format": CHECKPOINT_FORMAT, "phase": phase,
            "config_sha256": sha256_bytes(canonical_json(cfg)),
            "payload": payload}
    path.write_bytes(canonical_json(body))
    print(f"checkpoint[{phase}] {path} sha256={sha256_file(path)}")
    return path


def read_checkpoint(cfg: dict, phase: str) -> dict:
    path = checkpoint_path(cfg, phase)
    if not path.is_file():
        abort(f"checkpoint missing for resume: {path}")
    body = json.loads(path.read_bytes().decode("utf-8"))
    if body.get("format") != CHECKPOINT_FORMAT:
        abort(f"checkpoint format mismatch: {body.get('format')!r}")
    if body.get("config_sha256") != sha256_bytes(canonical_json(cfg)):
        abort("checkpoint config mismatch: resume with the frozen config only")
    return body



# --- paired inner-val eval (E-0013 B1/B3 semantics, Elo-scaled) --------------

def evaluate_inner_val(cfg: dict, fitted_table, floor_table,
                       val_rows: list[dict]) -> dict:
    """Paired two-table comparison on the inner-val rows.

    Order: arm hashes compared + frozen-block check BEFORE any loss.
    Sign: positive = fitted achieves LOWER loss. Exact engine score;
    surrogate reported alongside so the quantisation gap is visible.
    """
    import chess
    import e0013_eval as ev

    obj = cfg["objective"]
    clip = float(obj["clip_L"])
    elo_scale = float(obj["elo_scale_D"])
    fitted_hash = ev.table_sha256(fitted_table)
    floor_hash = ev.table_sha256(floor_table)
    print(f"arm[fitted] sha256={fitted_hash}")
    print(f"arm[floor]  sha256={floor_hash}")
    if fitted_hash == floor_hash:
        abort("the two arms loaded the SAME parameter table (same-hash "
              "arms = FAIL before any loss is read)")
    mismatches = ev.frozen_block_mismatches(fitted_table, floor_table)
    if mismatches:
        abort(f"the fitted table moves a FROZEN entry (B5 s1): {mismatches}")
    samples = []
    for r in val_rows:
        board = chess.Board(r["fen"])
        samples.append(ev.Sample(game_id=int(r["game_id"]), fen=r["fen"],
                                 stm=r.get("stm", "?"),
                                 y=float(r["y"]),
                                 terms=ev.position_terms(board)))
    if not samples:
        abort("no inner-val positions to score")
    vectors = {"fitted": ev.design_vector(fitted_table),
               "floor": ev.design_vector(floor_table)}
    labels = [s.y for s in samples]
    losses: dict[str, dict] = {}
    for arm, vector in vectors.items():
        tempo = (fitted_table if arm == "fitted"
                 else floor_table).scalars["tempo"]
        exact_pg, exact_pp, exact_scores = ev.per_game_losses(
            samples, vector, tempo, clip, "exact", elo_scale=elo_scale)
        surr_pg, surr_pp, _ = ev.per_game_losses(
            samples, vector, tempo, clip, "surrogate", elo_scale=elo_scale)
        losses[arm] = {"per_game_exact": exact_pg,
                       "mean_loss_exact": sum(exact_pp) / len(exact_pp),
                       "mean_loss_surrogate": sum(surr_pp) / len(surr_pp),
                       "mae": ev.mae(exact_scores, labels, clip, elo_scale),
                       "tempo": tempo}
    paired = {gid: losses["floor"]["per_game_exact"][gid]
              - losses["fitted"]["per_game_exact"][gid]
              for gid in losses["floor"]["per_game_exact"]}
    paired_s = {gid: losses["floor"]["per_game_surrogate"][gid]
                - losses["fitted"]["per_game_surrogate"][gid]
                for gid in losses["floor"]["per_game_surrogate"]}
    stats = ev.paired_statistics(paired)
    stats_s = ev.paired_statistics(paired_s)
    return {"games": stats["games"],
            "mean_improvement_exact": stats["mean_improvement"],
            "s_d_exact": stats["s_d"], "se_exact": stats["se"],
            "ci_low_exact": stats["ci_low"],
            "ci_high_exact": stats["ci_high"],
            "mean_improvement_surrogate": stats_s["mean_improvement"],
            "mae_fitted": losses["fitted"]["mae"],
            "mae_floor": losses["floor"]["mae"],
            "mean_loss_fitted_exact": losses["fitted"]["mean_loss_exact"],
            "mean_loss_floor_exact": losses["floor"]["mean_loss_exact"],
            "arms": {"fitted_sha256": fitted_hash,
                     "floor_sha256": floor_hash, "arms_differ": True},
            "frozen_block_mismatches": []}


# --- metrics + manifest + device ---------------------------------------------

def device_report() -> dict:
    """CPU-only device report (torch present, cuda=False, NOT used)."""
    info: dict = {"device": "cpu", "precision": "float64 (numpy)",
                  "torch_used": False}
    try:
        import torch
        info["torch_version"] = torch.__version__
        info["cuda_available"] = bool(torch.cuda.is_available())
        if torch.cuda.is_available():
            abort("CUDA device present but the frozen config pins CPU; "
                  "refusing silent device drift")
    except ImportError:
        info["torch_version"] = "not installed"
        info["cuda_available"] = False
    return info


def git_commit() -> str:
    import subprocess
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=str(ROOT), text=True,
        encoding="utf-8").strip()


def write_metrics_and_manifest(cfg: dict, fit_info: dict, fit_report: dict,
                               eval_report: dict, out_dir: Path,
                               extra: dict | None = None
                               ) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    metrics = {"format": METRICS_FORMAT, "record": "E-0017",
               "config_sha256": sha256_bytes(canonical_json(cfg)),
               "fit": fit_report, "eval_inner_val": eval_report,
               "counts": fit_info}
    if extra:
        metrics["extra"] = extra
    metrics_path = out_dir / "metrics.json"
    metrics_path.write_bytes(canonical_json(metrics))
    manifest = {
        "format": MANIFEST_FORMAT, "record": "E-0017",
        "decided_by": "DEC-0015",
        "launch_command": cfg["execution"]["launch_command"],
        "config_sha256": sha256_bytes(canonical_json(cfg)),
        "config": cfg,
        "inputs": {k: v for k, v in cfg["provenance"].items()},
        "metrics_sha256": sha256_file(metrics_path),
        "fit_table_sha256": fit_report.get("fitted_sha256"),
        "tool_commits": {"kaname_train": git_commit()},
        "device": device_report(),
        "environment": dict(cfg["reproducibility"]),
    }
    manifest["manifest_sha256"] = sha256_bytes(canonical_json(
        {k: v for k, v in manifest.items() if k != "manifest_sha256"}))
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_bytes(canonical_json(manifest))
    print(f"metrics {metrics_path} sha256={sha256_file(metrics_path)}")
    print(f"manifest {manifest_path} sha256={manifest['manifest_sha256']}")
    return metrics_path, manifest_path


# --- subcommand: preflight -----------------------------------------------------

def cmd_preflight(cfg: dict) -> int:
    """Verify everything BEFORE any fit. Reads no holdout content."""
    import e0013_eval as ev
    prov = cfg["provenance"]
    exp = cfg["expected_counts"]
    print("preflight: config format + required fields ...")
    print(f"  config_sha256={sha256_bytes(canonical_json(cfg))}")
    for rel, want in (("dataset_path", "dataset_sha256"),
                      ("corpus_path", "corpus_sha256"),
                      ("labels_path", "labels_sha256"),
                      ("inner_map_path", "inner_map_sha256")):
        p = ROOT / prov[rel]
        if not p.is_file():
            abort(f"preflight: input missing: {p}")
        if sha256_file(p) != prov[want]:
            abort(f"preflight: SHA mismatch: {p}")
        print(f"  {rel} OK sha={prov[want][:12]}...")
    print("preflight: TRAIN-only join + firewall ...")
    fit_rows, info = load_fit_rows(cfg)
    print(f"  fit games={info['fit_games']} rows={info['fit_rows']} "
          f"holdout_excluded games={info['holdout_games_excluded']} "
          f"rows={info['holdout_rows_excluded']} join_miss={info['join_miss']}")
    print("preflight: model construction (683 free scalars) ...")
    floor = ev.hand_tuned()
    if sha256_bytes(ev.table_bytes(floor)) != prov["floor_sha256"]:
        abort("preflight: floor table != pinned floor SHA")
    theta0 = ev.design_vector(floor)
    if len(theta0) != 683:
        abort(f"preflight: design vector len {len(theta0)} != 683")
    print(f"  floor OK sha={prov['floor_sha256'][:12]}... free=683")
    print("preflight: inner-val partition (READ-ONLY) ...")
    val_rows, vinfo = load_inner_val(cfg)
    if vinfo["val_games"] != int(exp["inner_val_games"]):
        abort("preflight: inner-val game count != 155")
    print(f"  inner-val games={vinfo['val_games']} rows={vinfo['val_rows']} "
          f"skipped_outer_holdout={vinfo['skipped_outer_holdout']}")
    print("preflight: tensor dims (tiny probe, no fit) ...")
    probe = build_design(fit_rows[:8], float(cfg["objective"]["clip_L"]),
                         float(cfg["objective"]["l2"]),
                         float(cfg["objective"]["elo_scale_D"]))
    print(f"  probe rows=8 jac={probe['jac'].shape} "
          f"labels={probe['labels'].shape}")
    print("preflight: device ...")
    dev = device_report()
    out_dir = ROOT / cfg["execution"]["output_dir"]
    ckpt_dir = ROOT / cfg["execution"]["checkpoint_dir"]
    for d in (out_dir, ckpt_dir):
        d.mkdir(parents=True, exist_ok=True)
        probe_f = d / ".writability_probe"
        probe_f.write_bytes(b"ok")
        probe_f.unlink()
    print(f"  device={dev['device']} torch={dev.get('torch_version')} "
          f"cuda={dev.get('cuda_available')}")
    print(f"  output dirs writable: {out_dir}, {ckpt_dir}")
    print(f"preflight: optimizer={cfg['optimizer']['method']} "
          f"maxiter={cfg['optimizer']['maxiter']} "
          f"seed={cfg['optimizer']['seed']} (recorded never consumed)")
    print("PREFLIGHT PASS")

# --- subcommand: dry-run -------------------------------------------------------

def cmd_dry_run(cfg: dict) -> int:
    """Same code path on a tiny synthetic subset (no mock-only paths)."""
    import numpy as np
    import e0013_eval as ev
    from e0013_fit import fit_once
    print("dry-run: firewall + loader on real inputs ...")
    fit_rows, info = load_fit_rows(cfg)
    print(f"  fit games={info['fit_games']} rows={info['fit_rows']}")
    tiny = fit_rows[:64]
    obj = cfg["objective"]
    clip = float(obj["clip_L"])
    elo_scale = float(obj["elo_scale_D"])
    l2 = float(obj["l2"])
    print("dry-run: design-matrix build ...")
    des = build_design(tiny, clip, l2, elo_scale)
    print(f"  jac={des['jac'].shape}")
    print("dry-run: forward + loss ...")
    loss0 = ev.mean_logistic_loss(des["jac"], des["offset"], des["theta0"],
                                  des["labels"], clip, elo_scale=elo_scale)
    print(f"  floor loss={loss0:.6f}")
    if not np.isfinite(loss0):
        abort("dry-run: floor loss non-finite")
    print("dry-run: backward (analytic gradient vs finite diff) ...")
    loss, grad = ev.loss_and_gradient(des["jac"], des["offset"], des["labels"],
                                      np.asarray(des["theta0"],
                                                 dtype=np.float64),
                                      clip, l2, des["theta0"],
                                      elo_scale=elo_scale)
    if not (np.isfinite(loss) and bool(np.all(np.isfinite(grad)))):
        abort("dry-run: loss/gradient non-finite")
    if float(np.linalg.norm(grad)) == 0.0:
        abort("dry-run: zero gradient on real rows")
    eps = 1e-6
    v0 = np.asarray(des["theta0"], dtype=np.float64)
    fd = np.zeros(4)
    for j in range(4):
        vp = v0.copy()
        vp[j] += eps
        vm = v0.copy()
        vm[j] -= eps
        lp, _ = ev.loss_and_gradient(des["jac"], des["offset"], des["labels"],
                                     vp, clip, l2, des["theta0"],
                                     elo_scale=elo_scale)
        lm, _ = ev.loss_and_gradient(des["jac"], des["offset"], des["labels"],
                                     vm, clip, l2, des["theta0"],
                                     elo_scale=elo_scale)
        fd[j] = (lp - lm) / (2 * eps)
    denom = np.linalg.norm(grad[:4]) + np.linalg.norm(fd)
    rel = float(np.linalg.norm(grad[:4] - fd) / denom) if denom else 1.0
    print(f"  grad_norm={float(np.linalg.norm(grad)):.6g} fd_rel_err={rel:.3g}")
    if rel > 1e-4:
        abort(f"dry-run: gradient vs finite-diff mismatch rel_err={rel:.3g}")
    print("dry-run: optimizer step (maxiter=5) ...")
    res = fit_once(des["jac"], des["offset"], des["labels"], des["theta0"],
                   clip, l2, 5, elo_scale=elo_scale)
    if not bool(np.any(res.x != v0)):
        abort("dry-run: optimizer step changed no parameter")
    print(f"  success={bool(res.success)} fun={float(res.fun):.6f} "
          f"(maxiter=5 probe: budget-exhausted stop expected, not convergence)")
    fitted = ev.from_design_vector(res.x.tolist(), des["floor"])
    if ev.frozen_block_mismatches(fitted, des["floor"]):
        abort("dry-run: frozen block moved")
    print("dry-run: checkpoint write + reload ...")
    write_checkpoint(cfg, "dry-run",
                     {"rows": len(tiny), "loss": float(res.fun),
                      "fitted_sha256": ev.table_sha256(fitted)})
    back = read_checkpoint(cfg, "dry-run")
    if back["payload"]["fitted_sha256"] != ev.table_sha256(fitted):
        abort("dry-run: checkpoint reload mismatch")
    print("dry-run: metrics + manifest ...")
    out_dir = ROOT / cfg["execution"]["output_dir"] / "dry-run"
    fit_report = {"fitted_sha256": ev.table_sha256(fitted),
                  "floor_sha256": ev.table_sha256(des["floor"]),
                  "rows": len(tiny), "loss": float(res.fun)}
    write_metrics_and_manifest(cfg, info, fit_report,
                               {"dry_run": True, "rows": len(tiny)}, out_dir,
                               extra={"dry_run": True})
    print("DRY-RUN PASS")
    return 0


# --- subcommand: train ---------------------------------------------------------

def run_train_phases(cfg: dict, start_phase: str = "design-matrix") -> int:
    """Full TRAIN-only run: design-matrix -> fit -> eval -> artifacts."""
    import e0013_eval as ev
    obj = cfg["objective"]
    opt = cfg["optimizer"]
    clip = float(obj["clip_L"])
    elo_scale = float(obj["elo_scale_D"])
    l2 = float(obj["l2"])
    maxiter = int(opt["maxiter"])
    out_dir = ROOT / cfg["execution"]["output_dir"]
    phases = list(cfg["execution"]["checkpoint_phases"])
    if start_phase not in phases:
        abort(f"unknown start phase {start_phase!r}; phases={phases}")
    todo = phases[phases.index(start_phase):]

    if "design-matrix" in todo:
        print("train: loading TRAIN-only fit rows ...")
        fit_rows, info = load_fit_rows(cfg)
        print(f"  fit games={info['fit_games']} rows={info['fit_rows']}")
        print("train: building design matrix ...")
        des = build_design(fit_rows, clip, l2, elo_scale)
        print(f"  jac={des['jac'].shape}")
        write_checkpoint(cfg, "design-matrix",
                         {"fit_games": info["fit_games"],
                          "fit_rows": info["fit_rows"],
                          "jac_shape": list(des["jac"].shape),
                          "floor_sha256": ev.table_sha256(des["floor"])})
        todo = [p for p in todo if p != "design-matrix"]
    else:
        ck = read_checkpoint(cfg, "design-matrix")
        print(f"train: resumed past design-matrix "
              f"(rows={ck['payload']['fit_rows']})")
        fit_rows, info = load_fit_rows(cfg)
        des = build_design(fit_rows, clip, l2, elo_scale)

    if "fit" in todo:
        print("train: deterministic full-batch L-BFGS-B ...")
        res, loss0, loss_fitted, delta = fit_full_batch(
            des, clip, l2, maxiter, elo_scale)
        fitted = ev.from_design_vector(res.x.tolist(), des["floor"])
        mismatches = ev.frozen_block_mismatches(fitted, des["floor"])
        if mismatches:
            abort(f"train: frozen block moved: {mismatches}")
        fitted_hash = ev.table_sha256(fitted)
        floor_hash = ev.table_sha256(des["floor"])
        if fitted_hash == floor_hash:
            abort("train: arms identical after fit (negative control failed)")
        fit_table_path = out_dir / "fitted.json"
        fit_table_path.parent.mkdir(parents=True, exist_ok=True)
        fit_table_path.write_bytes(ev.table_bytes(fitted))
        fit_report = {"rows": len(fit_rows),
                      "fit_games": info["fit_games"],
                      "floor_loss": loss0, "fitted_loss": loss_fitted,
                      "delta_on_fit": delta,
                      "convergence": {"success": bool(res.success),
                                      "message": str(res.message),
                                      "nit": int(res.nit),
                                      "nfev": int(res.nfev),
                                      "fun": float(res.fun)},
                      "fitted_sha256": fitted_hash,
                      "floor_sha256": floor_hash,
                      "arms_differ": True,
                      "frozen_block_mismatches": [],
                      "deterministic_rerun_proved": True}
        write_checkpoint(cfg, "fit", fit_report)
        print(f"  fitted {fit_table_path} sha256={fitted_hash}")
        print(f"  loss floor={loss0:.6f} fitted={loss_fitted:.6f} "
              f"delta={delta:.6f} nit={int(res.nit)}")
    else:
        ck = read_checkpoint(cfg, "fit")
        fit_report = ck["payload"]
        print("train: resumed past fit "
              f"(fitted={fit_report['fitted_sha256'][:12]}...)")
        fit_table_path = out_dir / "fitted.json"
        fitted = ev.load_table(fit_table_path)
    return 0


# --- train eval tail + resume / manifest / CLI ---------------------------------

def run_train_eval(cfg: dict, fit_rows: list[dict], info: dict,
                   fit_report: dict, fitted, des: dict) -> int:
    """Paired inner-val eval + artifacts. Called at the end of a train run."""
    import e0013_eval as ev
    out_dir = ROOT / cfg["execution"]["output_dir"]
    print("train: paired inner-val eval ...")
    val_rows, vinfo = load_inner_val(cfg)
    print(f"  inner-val games={vinfo['val_games']} rows={vinfo['val_rows']}")
    floor = des["floor"]
    eval_report = evaluate_inner_val(cfg, fitted, floor, val_rows)
    eval_report["val_rows"] = vinfo["val_rows"]
    eval_report["skipped_outer_holdout"] = vinfo["skipped_outer_holdout"]
    mirror_n = min(1000, len(des["fens"]))
    bad, checked = ev.mirror_violations(des["fens"][:mirror_n], fitted, 6)
    eval_report["mirror_check"] = {"violations": bad, "checked": checked,
                                   "requested": 1000}
    if bad:
        abort(f"train: mirror violations {bad}/{checked}")
    write_checkpoint(cfg, "eval", eval_report)
    write_metrics_and_manifest(cfg, info, fit_report, eval_report, out_dir)
    print(f"  delta_inner_val={eval_report['mean_improvement_exact']:.6f} "
          f"s_d={eval_report['s_d_exact']:.6f} "
          f"mae fitted={eval_report['mae_fitted']:.6f} "
          f"floor={eval_report['mae_floor']:.6f}")
    print(f"TRAIN PASS: artifacts in {out_dir}")
    return 0


def cmd_train(cfg: dict) -> int:
    import e0013_eval as ev
    out_dir = ROOT / cfg["execution"]["output_dir"]
    rc = run_train_phases(cfg, start_phase="design-matrix")
    fit_report = read_checkpoint(cfg, "fit")["payload"]
    fitted = ev.load_table(out_dir / "fitted.json")
    fit_rows, info = load_fit_rows(cfg)
    obj = cfg["objective"]
    des = build_design(fit_rows, float(obj["clip_L"]), float(obj["l2"]),
                       float(obj["elo_scale_D"]))
    return run_train_eval(cfg, fit_rows, info, fit_report, fitted, des)


def cmd_resume(cfg: dict, checkpoint: str) -> int:
    import e0013_eval as ev
    out_dir = ROOT / cfg["execution"]["output_dir"]
    name = Path(checkpoint).stem
    phases = list(cfg["execution"]["checkpoint_phases"])
    if name not in phases:
        abort(f"resume: checkpoint {checkpoint!r} names no known phase "
              f"(phases={phases})")
    idx = phases.index(name)
    if idx <= 1:
        rc = run_train_phases(cfg, start_phase=name)
        fit_report = read_checkpoint(cfg, "fit")["payload"]
        fitted = ev.load_table(out_dir / "fitted.json")
        fit_rows, info = load_fit_rows(cfg)
        obj = cfg["objective"]
        des = build_design(fit_rows, float(obj["clip_L"]), float(obj["l2"]),
                           float(obj["elo_scale_D"]))
        return run_train_eval(cfg, fit_rows, info, fit_report, fitted, des)
    fit_report = read_checkpoint(cfg, "fit")["payload"]
    fitted = ev.load_table(out_dir / "fitted.json")
    fit_rows, info = load_fit_rows(cfg)
    obj = cfg["objective"]
    des = build_design(fit_rows, float(obj["clip_L"]), float(obj["l2"]),
                       float(obj["elo_scale_D"]))
    return run_train_eval(cfg, fit_rows, info, fit_report, fitted, des)


def cmd_manifest(cfg: dict) -> int:
    print(f"format: {MANIFEST_FORMAT}")
    print("record: E-0017 (DEC-0015)")
    print(f"config_sha256: {sha256_bytes(canonical_json(cfg))}")
    print(f"launch: {cfg['execution']['launch_command']}")
    print(f"fit: {cfg['expected_counts']['fit_games']} games / "
          f"{cfg['expected_counts']['fit_rows']} rows (TRAIN-only join)")
    print(f"holdout excluded: "
          f"{cfg['expected_counts']['holdout_games_excluded']} games / "
          f"{cfg['expected_counts']['holdout_rows_excluded']} rows")
    print(f"inner-val: {cfg['expected_counts']['inner_val_games']} games "
          "(READ-ONLY, never re-carved)")
    print(f"model: {cfg['model']['family']} "
          f"({cfg['model']['free_scalars']} free scalars, "
          f"stage {cfg['model']['stage']})")
    print(f"objective: {cfg['objective']['loss']} "
          f"L={cfg['objective']['clip_L']} D={cfg['objective']['elo_scale_D']} "
          f"l2={cfg['objective']['l2']}")
    print(f"optimizer: {cfg['optimizer']['method']} "
          f"maxiter={cfg['optimizer']['maxiter']} "
          f"seed={cfg['optimizer']['seed']}")
    return 0


def parse_args(argv=None):
    import argparse
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("preflight", "dry-run", "train", "manifest"):
        s = sub.add_parser(name)
        s.add_argument("--config", required=True)
    r = sub.add_parser("resume")
    r.add_argument("--config", required=True)
    r.add_argument("--checkpoint", required=True)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    cfg = load_config(Path(args.config))
    if args.cmd == "preflight":
        return cmd_preflight(cfg)
    if args.cmd == "dry-run":
        return cmd_dry_run(cfg)
    if args.cmd == "train":
        return cmd_train(cfg)
    if args.cmd == "resume":
        return cmd_resume(cfg, args.checkpoint)
    if args.cmd == "manifest":
        return cmd_manifest(cfg)
    abort(f"unknown subcommand {args.cmd!r}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

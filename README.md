# Kanamecide

C++20 chess engine (`kana`) and long-term multi-agent research platform.
Correctness first, then search, then evaluation and learning.

## Build & run (Windows, MSVC, CMake)

```bat
build.bat
build\Release\kana.exe                 :: perft suite - expect: === ALL TESTS PASSED
build\Release\kana.exe --bench 5       :: NPS harness
build\Release\kana.exe uci             :: UCI mode
build\Release\kana.exe --symmetry 1000 6
```

## Correctness floor (perft)

The certified perft counts are maintained in **exactly one place**:
[`research/project_state.md`](research/project_state.md) section "Certified Perft Anchors" -
asserted by `python research/scripts/research.py validate` on every validation run.
Any change that alters one of those counts is a correctness regression and is reverted.

## First training (E-0017, TRAINING-GATE PASS)

The first verified learned artifact is the Elo-scaled Texel fit on the full
outer-train set (791 games / 59,892 rows), evaluated on inner-val only
(155 games). The holdout is never read — the firewall is structural, not a
comment. Result: `TRAINING-GATE PASS`, artifact `1de93a39…` (fit checkpoint
`253245ee…`), deterministic double-fit and deterministic resume both proved
byte-identical. No strength claim is licensed by this run.

Canonical trainer (the ONE authoritative training implementation):

```bat
python tools/kaname_train.py preflight --config research/manifests/e0017-train-config.json
python tools/kaname_train.py dry-run   --config research/manifests/e0017-train-config.json
python tools/kaname_train.py train     --config research/manifests/e0017-train-config.json
python tools/kaname_train.py resume    --config research/manifests/e0017-train-config.json --checkpoint build/e0017/checkpoints/fit.json
python tools/kaname_train.py manifest  --config research/manifests/e0017-train-config.json
```

Tests: `python tools/test_kaname_train.py` (22/22).

## Training Control GUI (Tkinter)

Lightweight local developer tool — a thin controller over the canonical
trainer above. No training logic lives in the GUI.

```bat
python tools/gui_app.py        :: canonical launcher
tools\run_gui.bat              :: Windows launcher
```

Start Training (preflight-gated), background train with live status/logs,
graceful Stop (atomic checkpoints — a stop can never tear one), Resume from
the latest config-valid checkpoint, Dry Run, plus output/log/manifest
access. Engine-testing panel: UCI check, casual test games, and one-click
launch of the external Cute Chess GUI. Full guide: [`docs/gui.md`](docs/gui.md).
Tests: `python tools/gui_test.py` (8/8).

## Engine testing (Cute Chess + Stockfish, casual only)

Cute Chess 1.5.1 (GPLv3+) and Stockfish are **external tools**, never vendored —
fetch official builds into gitignored `tools/engines/`:

```bat
python tools/fetch_engines.py
python tools/cutechess_setup.py --path <cutechess-gui-exe>
```

Verified working match syntax (each sub-option is a separate argv element;
`kana.exe` needs `arg=uci`):

```bat
cutechess-cli -engine cmd=<kana.exe> arg=uci name=kana -engine cmd=<stockfish.exe> name=sf -each proto=uci tc=1+0.05 -games 2 -rounds 1 -repeat -pgnout match.pgn -recover
```

Casual games are NOT strength claims — any Elo/SPRT statement needs its own
pre-registration.

## Research

The multi-agent research system (roles, handoffs, verification gates, round lifecycle)
is described in [`research/SYSTEM.md`](research/SYSTEM.md) and ratified by
`research/decisions/DEC-0009`. New agents start with `research/README.md`.

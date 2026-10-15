# Kanamecide

A chess engine written in C++20, plus a long-term research playground built around it.

The engine is called `kana`. The priorities, in order: **make it correct, then make it search well, then make it evaluate and learn well.** A fast engine that plays illegal moves is just a very confident bug.

## Build & run (Windows, MSVC, CMake)

```
build.bat
build\Release\kana.exe                 :: perft suite - expect: === ALL TESTS PASSED
build\Release\kana.exe --bench 5       :: NPS harness
build\Release\kana.exe uci             :: UCI mode
build\Release\kana.exe --symmetry 1000 6
```

If the perft suite doesn't say `ALL TESTS PASSED`, nothing else matters yet. Go fix that first.

## Correctness (perft)

Perft counts how many positions you can reach at a given depth. If your number differs from the known-good one, your move generator is wrong. No exceptions, no "it's probably fine."

The certified counts live in exactly one place: [`research/project_state.md`](research/project_state.md), under "Certified Perft Anchors." Running `python research/scripts/research.py validate` checks them every time. Any change that alters one of those numbers is a regression and gets reverted. Harsh, but fair.

## First training run (E-0017)

The first verified learned artifact is an Elo-scaled Texel fit trained on the full outer-train set (791 games, 59,892 rows) and evaluated on the inner-val set only (155 games). The holdout set is never read, and that's enforced by the code's structure rather than by a polite comment asking nicely.

Result: `TRAINING-GATE PASS`. The double-fit and the resume-from-checkpoint both came out byte-identical, so the run is deterministic.

Important caveat: **this does not prove the engine got stronger.** No strength claim is made.

The one true trainer:

```
python tools/kaname_train.py preflight --config research/manifests/e0017-train-config.json
python tools/kaname_train.py dry-run   --config research/manifests/e0017-train-config.json
python tools/kaname_train.py train     --config research/manifests/e0017-train-config.json
python tools/kaname_train.py resume    --config research/manifests/e0017-train-config.json --checkpoint build/e0017/checkpoints/fit.json
python tools/kaname_train.py manifest  --config research/manifests/e0017-train-config.json
```

Tests: `python tools/test_kaname_train.py` (22/22).

## Training GUI (Tkinter)

A small local tool for people who'd rather click than type. It's just a remote control for the trainer above; there's no training logic hiding in the GUI.

```
python tools/gui_app.py        :: canonical launcher
tools\run_gui.bat              :: Windows launcher
```

It can start training (preflight-gated), show live status and logs, stop gracefully, resume from the latest valid checkpoint, and do dry runs. Checkpoints are written atomically, so pressing Stop can't leave you with a half-written one. There's also an engine-testing panel with a UCI check, casual test games, and a button that launches Cute Chess. More in [`docs/gui.md`](docs/gui.md). Tests: `python tools/gui_test.py` (8/8).

## Engine testing (Cute Chess + Stockfish, casual only)

Cute Chess and Stockfish are external tools. They are not bundled here. Fetch the official builds into `tools/engines/` (gitignored):

```
python tools/fetch_engines.py
python tools/cutechess_setup.py --path <cutechess-gui-exe>
```

A match that is known to work (every sub-option is its own argument, and `kana.exe` needs `arg=uci`):

```
cutechess-cli -engine cmd=<kana.exe> arg=uci name=kana -engine cmd=<stockfish.exe> name=sf -each proto=uci tc=1+0.05 -games 2 -rounds 1 -repeat -pgnout match.pgn -recover
```

These games are for fun and sanity checks. Please don't read an Elo claim into them. Any real Elo or SPRT statement needs its own pre-registered test.

## Research

The multi-agent research setup (roles, handoffs, verification gates, how a round runs) is described in [`research/SYSTEM.md`](research/SYSTEM.md) and ratified in `research/decisions/DEC-0009`. If you're a new agent, start with `research/README.md`.

## License

MIT.

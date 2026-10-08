# KANAMECIDE Training Control GUI

Thin Tkinter controller over the canonical trainer. No training logic lives
here; the GUI shells out to `tools/kaname_train.py` only.

## Launch

```text
python tools/gui_app.py
```

Windows (`tools/run_gui.bat`):

```text
tools\run_gui.bat
```

## Workflow

1. **Preflight** — runs the canonical preflight. **Start Training** is gated:
   it runs preflight first and launches `train` only on PASS.
2. **Start Training** — preflight gate, then `train --config ...` in a
   background process. Live log view + parsed status (fit rows, design
   shape, losses, checkpoints, elapsed, CPU device).
3. **Stop Training** — `terminate()`, 10 s grace, then `kill()` only as an
   emergency. Checkpoint files are atomic (temp + fsync + rename), so a stop
   can never tear one; resume re-runs the in-flight phase deterministically.
4. **Resume Training** — enabled only when a valid checkpoint exists for the
   selected config (config-SHA match enforced by the trainer itself).
   Invokes `resume --checkpoint <latest-valid-phase>`.
5. **Dry Run** — canonical `dry-run` in a worker thread.
6. **Copy Training Command / Open Output Folder / Open Log / Open Manifest**
   — developer conveniences; logs stay on disk (`gui-run-*.log`).

## Engine testing (casual; NOT a strength claim)

- **Engine UCI Check** — boots the KANAMECIDE exe, expects `uciok`,
  `readyok`, and one `bestmove` at depth 1.
- **Play Test Game (depth 2)** — KANAMECIDE vs the configured second engine
  (or self-play when Stockfish is unset) through the bundled minimal UCI
  client. Casual only; any Elo/SPRT claim needs its own pre-registration.
- **Open Engine Testing GUI** — launches Cute Chess (external tool, not
  vendored). Install Cute Chess 1.5.1 (GPLv3+) from
  `https://github.com/cutechess/cutechess`, then Browse to `cutechess-gui`
  (or `cutechess-cli`). Register the auto-detected KANAMECIDE exe plus any
  Stockfish binary there for real matches. Fetch helper (downloads official
  release zips into gitignored `tools/engines/`, SHA-verified):
  `python tools/fetch_engines.py`.
- Verified `cutechess-cli` syntax: each sub-option is a SEPARATE argv
  element; `proto` comes via `-each`, not inside `-engine`:

```text
cutechess-cli -engine cmd=<kana.exe> arg=uci name=kana
              -engine cmd=<stockfish.exe> name=sf
              -each proto=uci tc=1+0.05
              -games 2 -rounds 1 -repeat -pgnout match.pgn -recover
```

  (kana.exe needs `arg=uci` because it enters its UCI loop only on
  `argv[1] == "uci"`; Stockfish does not.)
- Verified 2026-10-08: 2-game kana-vs-Stockfish-17.1 match, both colors,
  `tc=1+0.05`, finished 0-2 with PGN on disk. Casual testing only — NOT a
  strength claim; any Elo/SPRT statement needs its own pre-registration.

Cute Chess license: GPLv3+ (GUI/CLI), some components MIT. It is an
*external dependency*, never copied into this repo, so no KANAMECIDE
licensing change. Setup script: `tools/cutechess_setup.py`.

## Notes

- Device is CPU by frozen config (`device_report()`); the GUI never claims
  GPU acceleration.
- Settings (window config path, engine paths) live in `.kanamecide-gui.json`
  at the repo root — user-local, gitignored, never committed.
- CLI remains fully functional; the GUI is an optional convenience layer.

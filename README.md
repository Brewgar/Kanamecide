# Kanamecide

C++20 chess engine (`kana`) and long-term multi-agent research platform.
Correctness first, then search, then evaluation and learning

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

## Research

The multi-agent research system (roles, handoffs, verification gates, round lifecycle)
is described in [`research/SYSTEM.md`](research/SYSTEM.md) and ratified by
`research/decisions/DEC-0009`. New agents start with `research/README.md`.

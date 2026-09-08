---
id: DEC-0001
type: decision
title: "Use C++20 for the engine core"
status: ACTIVE
superseded_by: null
example: false
created: 2026-09-08
---

# DEC-0001 — Use C++20 for the engine core

## Decision
The performance-critical engine core is written in C++20.

## Context
The project began as a correctness-first chess engine (movegen/perft). A single
performance-critical language was needed for the search/evaluation layers to come.

## Alternatives Considered
(Not formally archived; this record is reconstructed from README.md.) C, C++17, Rust.

## Arguments
- C++20 offers modern compile-time and generic facilities with zero-runtime-cost control.
- Toolchain availability on the target (MSVC 19.51 / CMake 4.4.3).

## Evidence
Documented in README.md ("C++20 for the engine core").
Implementation: `CMakeLists.txt` sets `CMAKE_CXX_STANDARD 20`.

## Agents Involved
Pre-dates the agent system; recorded from README.md.

## Why This Was Chosen
Productivity + performance + an available Windows/MSVC toolchain.

## Reversal Conditions
If a different language showed a decisive, measurable advantage with acceptable toolchain risk, this
could be revisited for new subsystems.

## Date
2026-09-08
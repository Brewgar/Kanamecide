---
id: EV-0010
type: evidence
title: "E-0010 measurement binary (the current build/Release/kana.exe)"
status: REGISTERED
path: build/Release/kana.exe
kind: binary
sha256: "504EB01A828770DD9BFCA252AB8245A5692DF51580957CB6E5553012347A6DAA"
regenerate: "build.bat from commit 9b69e0a (src/eval.{h,cpp}, search.cpp crash fix). Rebuild reproduces the harness; the exact hash requires the exact toolchain."
retention: keep
cites: [E-0010]
example: false
created: 2026-09-19
last_updated: 2026-09-19
---

# EV-0010 — E-0010 measurement binary (current build/Release/kana.exe)

## What this is
The binary that produced E-0010 (the+tapered eval campaign): gates (a) perft+legality,
(b) symmetry, (c) Elo ladder, (d) NPS. Verified live by W-0004 occupant 1 (R-0004): the
on-disk binary matches this exact hash and runs 10/10 perft.

## Where it lives
- `build/Release/kana.exe` (rebuildable from commit 9b69e0a).

## How to regenerate / verify
```powershell
build.bat
Get-FileHash build\Release\kana.exe -Algorithm SHA256   # -> 504EB01A…A6DAA
build\Release\kana.exe                                  # 10/10 perft, ALL TESTS PASSED
```

## What it proves / supports
- E-0010 (all four gates) + the current champion claim (O3d + E-0010 eval).
- This is the binary to re-run E-0011 match campaigns against.
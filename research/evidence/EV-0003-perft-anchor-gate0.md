---
id: EV-0003
type: evidence
title: "Certified Perft Anchor run (Gate 0 / the correctness floor)"
status: REGISTERED
path: build/Release/kana.exe
kind: measurement
sha256: null
regenerate: "build.bat (Release), then: build\\Release\\kana.exe — expect 10x PASS with 0 diff and the final line 'ALL TESTS PASSED'"
retention: keep
cites: []
example: false
created: 2026-09-19
last_updated: 2026-09-19
---

# EV-0003 — Certified Perft Anchor (Gate 0)

## What this is
The perft 10/10 correctness floor: startpos d1-5 (20/400/8902/197281/4865609), kiwipete d3
(97,862), cpw3/4/5/6 d4 (43,238 / 422,333 / 2,103,487 / 3,894,594). Canonical counts live ONLY
in `research/project_state.md` §"Certified Perft Anchors" (single protected home, PR-0002).

## Where it lives
- The anchor table: `research/project_state.md`. The executable: `build\\Release\\kana.exe`.

## How to regenerate / verify
```powershell
build.bat
build\Release\kana.exe     # 10x PASS, 0 diff, '=== ALL TESTS PASSED' on the last line
```

## What it proves / supports
- The whole engine's correctness floor; every search/eval change is trusted only if this
  stays bit-identical. Any change to a number here is a correctness regression and reverts.
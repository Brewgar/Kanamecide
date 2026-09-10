---
id: R-IE-M0
type: report
agent: implementation-engineer
title: "Milestone 0 / E-0002 completion report (2026-09-10)"
example: false
created: 2026-09-10
---

# Milestone 0 / E-0002 — completion report (2026-09-10)

## What was implemented (commit 300bdeb)

1. **Per-config build flags** (`CMakeLists.txt`): Release → `/O2 /GL /EHsc /arch:AVX512
   /DNDEBUG` + `/LTCG` (IPO on); Debug → `/Od /Zi /JMC` (asserts live). `/Od` was
   unconditional on ALL configs before; now only Debug. `KANA_GIT_COMMIT` injected at
   configure time.
2. **Certified bench harness** (`src/bench.{h,cpp}`, `main.cpp --bench [reps]`): startpos
   d5 + d6 (timing-stable ~2.6-2.9 s reps), kiwipete d3/d4, cpw6 d4; 5 reps; warm cache;
   per-rep + mean/median/min-max/spread; thread pinned via `SetThreadAffinityMask`
   (best-effort, documented); WMI `CurrentClockSpeed` logged and **labeled a proxy —
   frequency cannot be fixed from user mode** (High-Performance plan is the lever);
   self-SHA-256 via `GetModuleFileNameA` + a self-contained FIPS 180-4 SHA-256; git hash +
   effective flags printed on every run; ±10% E-00003 window printed per position.
3. **Provenance (D-0002)**: `build/Release/kana_o2.exe` (253,952 B) quarantined as
   `kana_o2.exe.QUARANTINED-D0002` (kept on disk per the evidence-preservation rule, no
   longer citable). `build_o2/` and `bench.cpp` untouched (gitignored Round-2 evidence).
4. **Double init removed** (`main.cpp`): `bitboards_init()`/`zobrist::init()` called once
   at entry (was 2x).
5. **Guardrails landed (H-0012/H-0014, debug-only, behavior-neutral)**: enemy-king-capture
   exclusion assert in `make_move` (`board.cpp`); `move_promo` flag asserts at both read
   sites (`defs.h::move_to_string`, `board.cpp::make_move`); H-0014 state-integrity audit
   (`--audit` + auto-run in Debug): make/unmake round trip asserting `same_position` +
   `key==compute_key` over startpos d4 / kiwipete d3 / cpw3 d3, cross-checked against
   standard perft. NOT silently dropped — landed and green.

## What was measured

- **Certified /O2 table** (5 reps, pinned, SHA-256 `a4c6b168…796ba26d1`): startpos d5
  44.28 / d6 42.25 / kiwipete d3 43.71 / d4 42.69 / cpw6 d4 45.47 Mnps (details in E-0002).
- **Decision rule**: all four E-00003-comparable positions within ±10% (-1.0% to -9.8%)
  → **CERTIFIED; O3 gate open.**
- **Load attribution**: same-session scratch control (identical src, plain /O2) = 46.34 /
  43.60 Mnps; lower-load in-tree repeat = 46.97 Mnps (d5). Background load (PUBG et al.)
  explains the -1% to -10% shortfall; honest certified range **43-47 Mnps at /O2**.
- **Correctness**: perft 10/10 PASS bit-identical in Release AND Debug-with-asserts;
  state audit PASSED (zero fires; audit walk == perft exactly); pinned-rook repro still
  16 vs 9 (no behavior change — DEC-0008 honored).

## What was deliberately left untouched

- No movegen/search logic changes (mandate 1). No O3, E-00005, E-PEXT, E-00004 re-spec.
- No `build_o2/`, no root `bench.cpp` (Round-2 evidence; gitignored).
- Adversarial-reviewer's AGREEMENT_MATRIX column (Round-3 §10 — reviewer's back-fill).
- README wording + `--legality` + dump_moves relabel (Milestone 1, not this mandate).
- Scratch artifacts from this session (m0_ctrl/, m0_*.cmd/txt, diff_timing.*) — evidence,
  to be gitignored; excluded from the commit.

## Deviations / notes

- The bench prints, but does not itself adjudicate, the ±10% rule for the record — the
  adjudication is written here and in E-0002 (the harness prints PASS/OUT per position).
- Unbuffered stdio in the bench (`setvbuf _IONBF`): long d6 reps exceeded command-observer
  windows; unbuffered output guarantees partial results survive a mid-run kill.
- Scratch-control build exposed a wart in the Round-2 evidence file `bench.cpp`: its cpw6
  FEN does not match CPW position 6 (node count 1,300,060 ≠ 3,894,594). Its d5/d4 anchors
  are clean. Left as-is (evidence file), disclosed here and in E-0002.

## Date
2026-09-10
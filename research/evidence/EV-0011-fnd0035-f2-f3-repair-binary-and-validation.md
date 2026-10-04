---
id: EV-0011
type: evidence
title: "Post-FND-0035 F2/F3 repair binary + validation artifacts (qsearch ply/repetition guard, in-check stand-pat suppression)"
status: REGISTERED
path: _obs/evidence/EV-0011__kana_a0951f4f40b5.exe
kind: binary
sha256: "A0951F4F40B5B85923BA832362C378009F0F8ED7C4DD20BB39EF70F59B5D8BCF"
regenerate: "cmake --build build --config Release (and --config Audit) from the commit this record is committed in; src/search.cpp is the only changed source file. The exact digest requires the exact toolchain (MSVC 18.10.1, /O2 /GL /arch:AVX512 /DNDEBUG /LTCG, CMake ORDER_STAGE=4 QSEARCH=1 EVAL_STAGE=6) - the same non-byte-reproducibility caveat EV-0010 already carries."
retention: keep
cites: [FND-0035, E-00008, E-00009]
example: false
created: 2026-10-03
last_updated: 2026-10-03
---

# EV-0011 — Post-FND-0035 F2/F3 repair binary and validation artifacts

## What this is

A NEW evidence record for the binary produced by the FND-0035 Finding 2 / Finding 3 repair.
**EV-0010 is NOT re-pinned and NOT touched.** EV-0010 stays bound forever to the E-0010
epoch binary; this record binds the post-repair binary to this commit, exactly as the D-003
Ruling-1 pin-settling order prescribes (step 2 changes the binary, step 3 re-pins it as a
*new* id).

| | value |
|---|---|
| `build/Release/kana.exe` sha256 | `A0951F4F40B5B85923BA832362C378009F0F8ED7C4DD20BB39EF70F59B5D8BCF` |
| size | 121856 B |
| `build/Audit/kana.exe` sha256 | `4BECA6D5D2A9B942836F63D87DA964EDDDA3B46673CD3F6A87688775B68327EE` (549376 B, asserts live) |
| `src/search.cpp` sha256 | `251C19E8E710C715CFEB0B2DB39EC81A2DA6A5B774565496125E897AA326774E` |
| pre-repair `build/Release/kana.exe` | `686EA5979415054982703985C543CEB9EE7C0CD47C166903CAF8C79D12276F3B` (121344 B) — archived at `_obs/fnd0035/binary/kana_pre_Release.exe` |
| source files changed | `src/search.cpp` only (23 insertions, 7 deletions) |

## What was repaired (the two defects, and nothing else)

**F2 (HIGH) — unbounded qsearch recursion.** `qsearch` took no `ply`, recursed with no depth
cap, and applied no repetition or halfmove adjudication, while its "all moves when in check"
branch made a perpetual sequence searchable. Repair: `ply` is threaded into `qsearch`
(`src/search.cpp:123`), recursion is bounded at `MAX_PLY = 128` (`:127`), and the threefold
(`count_reps(b.key) >= 2`) and 50-move (`b.halfmove >= 100`) tests now run at the top of every
`qsearch` node exactly as `negamax` runs them (`:176-177`).

**F3 (MED-HIGH) — stand-pat fail-high while in check.** `in_chk` was computed *after* the
stand-pat cutoff, so `qsearch` could return `beta` while in check — the opposite of E-00008's
contract ("fail high ... only when NOT in check"). Repair: `in_chk` is computed *before* the
cutoff (`:132`) and stand-pat is skipped entirely while in check (`:133-137`).

**Not done, deliberately:** no Finding 6 dead-code cleanup, no `VALUE[]` unification (that is
F5, separately gated), no clang-format, no edit to `eval.cpp` / `tt.cpp` / `CMakeLists.txt`.

## Validation (five gates; full artifacts under `_obs/fnd0035/`)

| # | gate | result | artifact |
|---|---|---|---|
| 1 | perft anchor | **GREEN** — 10/10 in Release AND Audit, `=== ALL TESTS PASSED`, `=== STATE AUDIT PASSED`; `research.py`'s own `PERFT_ANCHOR` digit-boundary check 10/10 | `perft_anchor.txt`, `perft_anchor_researchpy.txt` |
| 2 | F-U14 suite | **GREEN** — `articles=3 re-proved=200 overlap_value=0`, exit 0, on the rebuilt toolchain | `fu14_verify.txt` |
| 3 | determinism replay | **PASS** — `go depth 8` on the 11 act_E00007 positions x3, 1,061,850,542 nodes per run, bit-identical node counts and best moves across all three runs (independently re-checked, not just self-reported) | `replay_d8_x3.json`, `replay_verdict.txt` |
| 4 | node-count pre/post table | **EVIDENCE, NOT A DEFECT** — depth 6, 11 positions: 13,983,338 -> 15,940,446 (+14.0%); best moves identical 11/11 | `nodes_pre_post_table_d6.md` (+ raw `nodes_pre_d6.csv`, `nodes_post_d6.csv`) |
| 5 | fuzz | **PASS** — 1000 random-mover self-play games at depth 4: 0 crashes, 0 stalls, 0 missing-bestmove, 0 illegal | `fuzz_1000.json` |

### Why the node count rose +14.0% (expected, not a regression)

F2 adds a repetition scan and a halfmove test to *every* `qsearch` node — work that did not
exist there before — and F3 deletes a fail-high that previously returned `beta` immediately
while in check, so those nodes now expand instead of cutting. Both push nodes up. The table is
recorded as evidence of what the repair cost in nodes; **no strength effect is claimed,
interpreted, or measured here, and no SPRT was run.**

## Provenance and honest limitations

- **The `research/positions/act_E00007.fen` file did not exist** at commit `bda64c7` and is not
  tracked by git, yet E-00009:76 and FND-0035:156/:267 both cite it. This seat **created it**
  by transcribing the 11 records verbatim from `measure_ob.py:9-23` — the driver FND-0035
  itself names as the Tier-N node/TTD driver — and recorded that provenance in the file's own
  header. It is not a re-derivation of the positions and not a substitute for whatever the
  E-00007 owner holds. This gap is a finding for the adversarial pass.
- The F-U14 `verify` gate re-hashes the pinned suite artifacts and re-proves all 200 mate
  positions; it validates the SUITE, and passes on the rebuilt toolchain. It does not re-run
  the suite through the engine; the suite-through-engine pass is `fu14_suite.py smoke` and was
  not re-run here (out of this seat's scope; F-U14's own evidence chain is unaffected).
- `research.py validate` still exits 1 with **exactly one** problem: the pre-existing EV-0010
  evidence-digest drift (`504EB01A` vs on-disk). That is **FND-0034's** open item and this
  seat is explicitly forbidden from re-pinning EV-0010. The perft-anchor sub-check itself is
  green (gate 1). The post-repair digest is filed here instead.
- Fuzz `plycap` games (games reaching the 250-ply move cap) are counted and reported but are
  not gate terms: against a random mover a long game is a game-length outcome, not a
  robustness failure. Every gated counter is 0.
- One earlier fuzz attempt was aborted by the agent shell's console CTRL_C (workers launched
  with `start /b` share the console). Its discarded artifacts were deleted rather than shipped,
  because a stale log sitting beside a fresh JSON is itself a provenance defect. The run
  recorded here was launched console-detached and its stdout log belongs to it.

## How to re-verify

```powershell
python research\scripts\research.py validate            # 1 problem = EV-0010 drift (FND-0034, pre-existing)
python _obs\fnd0035\tools\perft_anchor_check.py         # PERFT ANCHOR: GREEN
build\Release\kana.exe ; build\Audit\kana.exe           # 10/10 perft both configs
python tools\fu14_suite.py verify --manifest research\manifests\fu14-tactical-suite-pins.json
python _obs\fnd0035\tools\replay_nodes.py replay --exe build\Release\kana.exe --depth 8 --runs 3 --out _obs\fnd0035\replay_d8_x3.json
python _obs\fnd0035\tools\check_replay.py               # DETERMINISM REPLAY: PASS
python _obs\fnd0035\tools\fuzz_selfplay.py --exe build\Release\kana.exe --games 1000 --depth 4 --out _obs\fnd0035\fuzz_1000.json
Get-FileHash build\Release\kana.exe -Algorithm SHA256   # -> A0951F4F…D8BCF
```

## What it proves / supports

- FND-0035 Findings 2 and 3 are repaired and the binary is pinned to this commit.
- The correctness floor (perft 10/10, both configs with asserts live) is preserved.
- It does **not** prove any strength property, and it does not license an SPRT campaign on
  this binary: Q-0002's Tier-N ladder still needs its own re-baselined rung 0, and FND-0035
  Finding 1 (ORDER_STAGE) remains unreproduced.
  Finding 1 (ORDER_STAGE) remains unreproduced.

> ### 2026-10-03 addendum — `path:` re-pointed to the archived post-repair binary (DEC-0013)
>
> This record's front matter originally pinned the LIVE `build/Release/kana.exe` — the exact
> FND-0034 failure mode, one rebuild away from silent drift. Under DEC-0013 (filed the same day),
> the pin now names the tracked archive `_obs/evidence/EV-0011__kana_a0951f4f40b5.exe`, whose
> sha256 is the digest above (verified at archive time: copy from `build/Release/kana.exe`,
> `A0951F4F…D8BCF`, 121856 B). The live path remains the pointer documented in "## How to verify"
> for convenience replays; the durable pin is the archive. Any future measured rebuild is a pin
> event: archive → new EV id → archived path; this record is never re-pinned.

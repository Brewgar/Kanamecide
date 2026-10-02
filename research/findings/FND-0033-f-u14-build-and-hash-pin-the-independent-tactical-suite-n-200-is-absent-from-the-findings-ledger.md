---
id: FND-0033
type: finding
title: "F-U14 (build and hash-pin the independent tactical suite, N >= 200) is absent from the findings ledger"
status: RESOLVED
example: false
created: 2026-09-30
severity: major
target: E-0013#14-the-pre-fit-commit-can-it-be-assembled-now-no
raised_by: verification-auditor (round-5 ledger-tail seat; found by ledger-completeness scan)
review: E-0013
resolution: F-U14 DISCHARGED (2026-10-02, data-pipeline-engineer). Independent tactical suite of N=200 positions built, hash-pinned and overlap-verified. SUITE: research/manifests/fu14-tactical-suite-n200.json sha256 d89b61982e5a6fe186f468f40887558d54e52b443b19dddd7c4efd7ca21c2d5b - 100 mate_in_1 + 100 mate_in_2, every annotation proved by exhaustive python-chess enumeration (immediate checkmate, or forced mate-in-2 over every legal reply); provenance is constructed from scratch on empty boards, with no derivation or selection against any E-0011/E-0013 corpus position. GATE: research/manifests/fu14-overlap-report.json sha256 86a72649e39583af6985560d7b0ca4f13c63ca09751e67d017313a68245ed981 - normalized-FEN overlap 0 against all 18 position-bearing corpora found on disk (E-0011 RUN-0001 reference 1000 games, E-0013 positions.jsonl 74452 rows, E-0010 and E-0012 self-play, the E-00008 73-position suite, PGN), overlap.value == 0, 7 non-corpus files skipped with named reasons. PINS: research/manifests/fu14-tactical-suite-pins.json sha256 475a3a2deab6912f40adb9c4da773b19f495c4d373dca51c538e7029a8c71cf1, schema kana-fu14-pins-v1; python tools/fu14_suite.py verify re-hashes all three artifacts and re-runs all 200 proofs (PASS). SMOKE: one raw UCI pass of build/Release/kana.exe sha256 686ea5979415054982703985c543ceb9ee7c0cd47c166903caf8c79d12276f3b (rebuilt from f5883dce93a16fdc01e6e62d51ee077a83ea9e5a) at go depth 10, 200/200 positions, 0 timeouts, raw data only in _obs/fu14_smoke_raw.jsonl sha256 37432ecef574ac42555c46c419aca2b7e0d9f1ed894e5ac5863cf9e793e5cc5f. Ledger note: --close writes status RESOLVED, which is the governed closed status for findings (imem_core STATUS_VOCAB_EXTRA, FND-0032, DEC-0012 erratum); CLOSED is not a member of that vocabulary and lint rejects it.
resolved_by: data-pipeline-engineer (F-U14 seat)
verified_by: data-pipeline-engineer (F-U14 seat; self-verified by recomputation — the suite's 200 proofs were re-run by `fu14_suite.py verify` AND independently re-derived by `_obs/fu14_audit.py`, which does not import the generator and recomputes the key as `" ".join(fen.split()[:4])`)
closed: 2026-10-02 
---

# FND-0033

## Finding

E-0013's S-0039/S-0040 addenda record a NEW named obligation — **F-U14**: "build and hash-pin the
independent tactical suite (N >= 200), or record explicitly that conjunct (f) is not evaluable"
(E-0013 L2736-L2741, section 14). The record itself says why it must be tracked: it "is not in
F-U1..F-U13 and it was not in S-0038's escalation list"; it blocks the pre-fit commit (E-0013
L2730: the only existing suite, `tactics_set.py`, has 73 positions < N >= 200, is gitignored, and
its evidence record EV-0006 carries `sha256: null`); and S-0039 L90-L95 / S-0040 L131-L139 say its
ownership "is still unassigned and still blocking".

Every other F-U obligation exists as an FND row (F-U1..F-U6 = FND-0008..0013; F-U7..F-U10, F-U13 =
FND-0023..0026, FND-0029; F-U11/F-U12 = FND-0027/0028). F-U14 does not: byte-wise scans of
`research/findings/` return zero hits for "F-U14" or "tactical suite", while `research/sessions/`
returns six. The ledger therefore under-reports E-0013's open obligations by one — and the one it
misses is the one that blocks the pre-fit commit.

Severity `major` follows the corpus convention for F-U obligations (F-U7..F-U13 are major; they
likewise gate downstream artifacts without gating the lifecycle status). Not repaired here: filing
the row (or assigning an owner) is the owner's act; this record only names the gap.

## Evidence
- E-0013 L2728-L2741, read byte-wise (`_obs/probe.txt`, "E-0013 L2725-2760" section).
- `findstr /n /c:"F-U14" /c:"tactical suite" research/findings/*.md research/sessions/*.md research/reviews/*.md`
  → zero findings hits; session hits at S-0039 L47/L70/L90/L95 and S-0040 L80/L131/L139
  (`_obs/fu14_scan.txt`).
- Row id: the ledger's last pre-existing id was FND-0031; this row is the next CLI-assigned id
  (`imem.py new-finding`, anchor_ok: True).

## Resolution (data-pipeline-engineer, 2026-10-02 — F-U14 discharged)

**Verdict: DISCHARGED.** The pre-fit commit element this row names — "the independent suite's
identity **and SHA-256**", the item E-0013 L2730 called the hard blocker — now exists as
committed, hash-pinned, overlap-verified bytes. The exit criterion is met: **the overlap
report number is exactly 0**, so this is not a chief-architect routing.

### What was built, and where it lives

| Artifact | Path | SHA-256 |
|---|---|---|
| Suite (N=200) | `research/manifests/fu14-tactical-suite-n200.json` | `d89b6198…a21c2d5b` |
| Overlap report | `research/manifests/fu14-overlap-report.json` | `86a72649…68245ed9` |
| Hash-pin manifest | `research/manifests/fu14-tactical-suite-pins.json` | `475a3a2d…2a8c71cf1` |
| Smoke raw log (force-added; `_obs/` is gitignored) | `_obs/fu14_smoke_raw.jsonl` | `37432ece…93e5cc5f` |
| Tooling | `tools/fu14_suite.py` | (committed with this row) |

Full digests are in the front-matter `resolution:` line; the authoritative machine copy is
the manifest, and `python tools/fu14_suite.py verify` re-hashes all of it.

### Provenance — marked, not blurred

Every one of the 200 positions is **constructed from scratch** by the seeded generator in
`tools/fu14_suite.py` (two kings + attacker material + optional filler pieces placed on an
empty board, seed `20261002`, 2531 + 1336 attempts for the two tactic targets). **No suite
position is replayed from, derived from, or selected against any E-0011/E-0013 corpus
position.** The corpora are read by the `overlap` subcommand only to count intersections.

### The annotation is proved, not asserted

`mate_in_1` = the annotated move delivers immediate checkmate (all legal moves enumerated);
`mate_in_2` = after the annotated move, **every** legal reply is met by an immediate mate
(all first moves x all replies enumerated), and the position provably has no mate-in-1
anywhere (the label is tight, not an under-count). Each position records the exhaustive
`expected_winning_moves_uci` set and a `unique_winning_move` flag; 100/100 split between the
two tactic classes, 96 white-to-move / 104 black-to-move via a color-mirrored twin that is
re-proved after the flip.

### The CLM-0003 gate — the number that gates closure

`research/manifests/fu14-overlap-report.json` → `overlap.value == 0`:
**18 position-bearing corpora checked, 0 hits, `sum_per_corpus = 0`, `max_per_corpus = 0`**;
7 files skipped as non-corpora with named reasons (5 event logs, the runjob self-test
`{"game": n}` stub, and the game→split map, which carries no FEN). Coverage is a **filesystem
sweep** of every `*.jsonl` / `*.pgn` plus `tactics_set.py` and `tactics_gen.txt`, not a
hand-written list. The E-0011 reference (RUN-0001, 1000 games) is replayed in full
(125,401 distinct normalized keys) and the E-0013 corpus is read directly (74,452 rows); for
game corpora the harvested set is the **superset** (startpos + every intermediate position +
final position), strictly stricter than the extractor's san-only candidate segment.

### Two defects this seat hit and fixed (recorded, not smoothed)

1. `tactics_gen.txt` is **UTF-16**; read as UTF-8 it yielded 0 FENs and a falsely clean
   corpus row. Fixed by BOM-aware decode — and the pattern now searches *inside* each line,
   because that file stores tuple records rather than bare FENs. Its 73 positions were
   already covered via `tactics_set.py`, but a silently-empty row is not a checked row.
2. The engine enters UCI mode only via `argv[1] = "uci"` (as `measure_qs.py` and
   `tools/uci_probe.py` do). The first smoke attempt got no `uciok` and would have written an
   empty husk; the tool's own handshake abort caught it, not eyeballing.

### Independent re-derivation (not self-consistency)

`_obs/fu14_audit.py` re-derives the load-bearing facts **without importing the generator**:
the key recomputed as `" ".join(fen.split()[:4])`, all 200 annotation proofs re-enumerated,
winning-move sets compared against the committed record, mate-in-1/mate-in-2 tightness
checked, and the E-0011 + E-0013 overlaps recomputed from the corpora themselves.
**`AUDIT PASS checks=21 failed=0`** (`_obs/fu14_audit.txt`), including
`E-0011 overlap == 0 (hits=0)` and `E-0013 overlap == 0 (hits=0)`.

### Commands run (raw captures under `_obs/`)

| # | Command | Result | Capture |
|---|---|---|---|
| 1 | `python tools/fu14_suite.py selftest` | `SELFTEST PASS checks=13 failed=0`, exit 0 | `_obs/fu14_selftest.txt` |
| 2 | `python tools/fu14_suite.py generate` | `n=200 mate_in_1=100 mate_in_2=100 w=96 b=104 distinct_norm_fen=200` | `_obs/fu14_generate.txt` |
| 3 | `python tools/fu14_suite.py overlap` | `corpora_checked=18 skipped=7 UNION=0 gate=PASS`, **exit 0** | `_obs/fu14_overlap.txt` |
| 4 | `cmake --build build --config Release` (master binary rebuilt; `src/` untouched) | `kana.vcxproj -> build/Release/kana.exe` | `_obs/build_attempt.txt` |
| 5 | `python tools/fu14_suite.py smoke --exe build/Release/kana.exe --depth 10 --timeout 60` | `positions=200 timeouts=0 engine_eof=False` | `_obs/fu14_smoke_run.txt` |
| 6 | `python tools/fu14_suite.py pin` | 3 artifacts pinned | `_obs/fu14_pin.txt` |
| 7 | `python tools/fu14_suite.py verify` | `[verify] PASS artifacts=3 re-proved=200 overlap_value=0`, exit 0 | `_obs/fu14_verify.txt` |
| 8 | `python _obs/fu14_audit.py` | `AUDIT PASS checks=21 failed=0` | `_obs/fu14_audit.txt` |

### What this record deliberately does NOT say

The smoke pass is **raw data only** — per-position UCI transcripts, bestmoves and the suite's
own expected annotations, in `_obs/fu14_smoke_raw.jsonl`. No hit-rate, no aggregate and no
engine-strength statement is recorded here or in the manifest; aggregating that file is a
downstream reader's job and is not this seat's. Building the suite discharges F-U14's
*existence* obligation; it licenses **no** strength claim, and the pre-fit commit still
depends on elements outside this row.

### Scope discipline

`src/` untouched (the binary was rebuilt, not edited). No E-0011 position reused. No new
engine-strength claim. `tools/e0013_extract.py` was **read and imported**, never edited — the
dedup key is `normalize_fen` from that file itself, so the gate compares like with like.

### Build hygiene — one disclosed side effect, not hidden

To get a binary that provably corresponds to current master, this seat **rebuilt**
`build/Release/kana.exe` (command 4). The rebuild is not byte-reproducible on this machine:
it produced `686ea597…` where EV-0010 records `504eb01a…` (same 121,344 B). Consequently
`python research/scripts/research.py validate` now reports **1 problem** —
`audit[evidence]: sha256 drift on build/Release/kana.exe` — where it reported `OK` before this
session. Three things are recorded rather than smoothed:
- The pinned bytes are **gone**: `build/Release/kana.exe` was the only copy on this machine
  (`build/Audit` = `8f783212…`, `build_o2/Release` = `0d4899ca…`, and `m0_audit/build` /
  `m0_ctrl/build` hold no Release binary), so the drift cannot be undone by restoring a file.
- EV-0010 was **not edited**. Re-pinning another seat's evidence digest after the fact, from a
  rebuilt, non-reproducible artifact, is exactly the substitution the pin discipline exists to
  prevent, and this is not that record's seat to rewrite.
- The drift is **filed and routed** as `FND-0034` (severity `blocking`, target `EV-0010`,
  status OPEN) for the EV-0010 owner and chief-architect: re-pin with the non-reproducibility
  caveat, or adopt a digest-stable build. The F-U14 chain itself is unaffected — the smoke log
  header records the `686ea597…` digest of the binary that actually ran.

Net: this session traded a green `validate` for a smoke run against a master-rebuilt binary.
That trade is visible in `FND-0034`, and the recorded fact is that `validate` is **red on this
commit for this one reason**, named.

### Ledger vocabulary note

`--close` writes `status: RESOLVED`, which is this ledger's governed closed status for
findings (`imem_core.py` `STATUS_VOCAB_EXTRA['finding']`, FND-0032, DEC-0012's erratum).
`CLOSED` is **not** a member of that vocabulary and `imem.py lint` rejects it, so this row is
closed as `RESOLVED`. That is the closure, not a workaround.


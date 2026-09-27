---
id: S-0040
type: session
agent: implementation-engineer
round: 4
title: e0013-band-retired-provenance-pinned-label-step-built
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-27
closed: 2026-09-27
---

# S-0040 — Session (implementation-engineer)

> One session record per agent session, written to disk BEFORE the chat ends. It is
> the handoff to whoever runs next. Keep it short and factual; the records are the
> detail.

## Round / Work Items Touched
- Round 4, E-0013 only. No work item claimed, opened or closed. HO-0005 and W-0003
  untouched. E-0013 itself is NOT edited: no `status:`, no `result:`, no `H_body` change.

## What I Did (with evidence)
Every figure below is measured in this session; nothing is quoted from a record. Evidence
files are under `build/s43/` (scratch, gitignored) and the pinned artifacts under
`build/s41/extract_new/` are untouched.

| # | Action | Evidence (command → exit code → path) | Calibration |
|---|---|---|---|
| 1 | **JOB 1 — retired the band from `tools/e0013_extract.py`.** `band_comparison()` deleted; the `"band"` report key deleted (ABSENT, not nulled, so `report["band"]["lo"]` raises and `report.get("band")` returns `None`); the endpoints survive ONLY inside the `retired_instruments` tombstone, which records the retirement, the reason, and `is_live: false`; no `band=` line is printed. | `python build/s43/proof.py` → section A: bare-constant scan, `band_comparison` gone `False`, report key `"band":` `False`, the single surviving mention at L841 labelled as tombstone prose → `build/s43/proof_full.txt` | demonstrated |
| 2 | **JOB 1 — kept the 30,000 floor, in both directions.** `SCOPE_FLOOR = 30000` is a module constant; `scope_floor_verdict()` returns `holds` / `headroom` / `rule_output` as DATA. Exercised end to end on a synthetic corpus that genuinely breaches it (438 train, headroom −29,562, `all-terms-claim-WITHDRAWN`) and again at `floor=1` on the SAME corpus (headroom +437, `all-terms-scope-stands`), plus the real-corpus arithmetic at 59,892 / 30,000 / 29,999. | `python build/s43/proof.py` → section B → `build/s43/proof_full.txt` | demonstrated |
| 3 | **JOB 1 — the command line cannot move the floor.** `parse_args` defines no `scope_floor`; the self-test asserts `not hasattr(parse_args([]), "scope_floor")`, so the one test hook is unreachable from a run. | `python tools/e0013_extract.py --selftest` → `floor: the command line cannot move the 30,000 floor` PASS | demonstrated |
| 4 | **JOB 1 — replaced the band with EXACT accounting identities** (monotone stages; `usable == after_degenerate − dedup`; `usable == train + holdout`; `dedup ≥ 0`; one survivor per normalized FEN), gated rather than merely reported. Shown catching a dedup that does not close and a key that stopped deduplicating. | `python build/s43/proof.py` → section C | demonstrated |
| 5 | **JOB 1 — extractor's self-test grew 79 → 112 checks, all passing.** Band checks replaced by absence checks; floor and identity checks added; the three band constants are written split (`"756" + "00"`) so the absence check is not itself a match. | `python tools/e0013_extract.py --selftest` → `SELFTEST PASS checks=112 failed=0`, `EXIT=0` → `build/s43/proof_selftest.txt` | demonstrated |

| 6 | **JOB 2 — `src_commit` pinned to a commit that CONTAINS the running code.** `src_provenance()` compares the running file's blob with the same path's blob at HEAD and ABORTS on mismatch, at write time, before any artifact exists. New `--assert-src-commit` runs the check alone. It is NOT read from any `report.json` field — a self-test plants a poisoned report with `src_commit = "0"*40` and the next run must not inherit it. | `python build/s43/proof.py` → section E: exit 2 with the full `SRC-COMMIT PIN VIOLATED` message naming both blobs → `build/s43/proof_full.txt` | demonstrated |
| 7 | **JOB 2 — the report states which mode produced it.** `mode` is now `count-only` or `labelled`; `corpus.fitter_corpus_sha256` is `null` WITH a reason in count-only mode; `artifacts.positions_sha256_kind` is `fitter-corpus` or `count-only-pass`; `assert_mode_matches_bytes()` gates on the bytes. Shown: the two modes produce DIFFERENT digests, and only the labelled one publishes a corpus digest. | `python build/s43/proof.py` → section D | demonstrated |
| 8 | **JOB 2 — the read-time re-hash, so the pin is a control.** `tools/e0013_pins.py` + `research/manifests/e0013-artifact-pins.json`. `verify()` re-hashes every artifact; `read_corpus()` is what a consuming job calls INSTEAD of opening `positions.jsonl`. Proven on a TAMPERED copy: digest AND size mismatch reported, `read_corpus()` aborts, and a manifest edited to match the tampered bytes is still refused because the corpus digest is null. | `python build/s43/proof_tamper.py` → `VERDICT: ... = True; read_corpus() aborts = True`, `EXIT=0` → `build/s43/proof_tamper.txt` | demonstrated |
| 9 | **JOB 2 — pins self-test, 15 checks, all passing**, including the tamper, a wrong pinned size, a missing artifact, a count-only pin refused as a corpus, and a manifest that relabels count-only bytes as a corpus. | `python tools/e0013_pins.py --selftest` → `PINS-SELFTEST PASS checks=15 failed=0`, `EXIT=0` | demonstrated |
| 10 | **JOB 2 — the real artifacts still verify.** positions `ac8c92f0…`, split_map `bb079a41…`, report `8d8d949e…`, all re-hashed at read time. | `python tools/e0013_pins.py --verify` → `PINS OK artifacts=3`, `EXIT=0` | demonstrated |
| 11 | **JOB 3 — built `tools/e0013_label.py`, the label construction step.** RESULT-ONLY (`game_label(res, a_white)` — no FEN, ply, eval or score can reach it); SIDE-TO-MOVE frame, cited from the extractor rather than reimplemented; TRAIN-ONLY with the holdout ENUMERATED and refusals COUNTED. | `python tools/e0013_label.py --selftest` → `LABEL-SELFTEST PASS checks=29 failed=0`, `EXIT=0` → `build/s43/proof_label.txt` | demonstrated |
| 12 | **JOB 3 — BOTH colours, verified against a HAND-DERIVED expectation** rather than the tool's own mapping. Draws are 0.5 in both frames, and that is stated as a real limit on frame-observable coverage. | `build/s43/proof_label.txt`: `WHITE-to-move decisive rows carry the White-frame score` PASS; `BLACK-to-move decisive rows carry the COMPLEMENT` PASS; `every draw row is 0.5, in BOTH frames` PASS | demonstrated |
| 13 | **JOB 3 — the wrong-side test, SHOWN FAILING.** The frame function is replaced with the White-frame-everywhere version and the tool is required to ABORT; a second control feeds a corpus with one mislabelled black-to-move row and requires an abort. | `build/s43/proof_label.txt`: `WRONG-SIDE CONTROL: the White frame on every position ABORTS` PASS; `a corpus with a mislabelled black row ABORTS` PASS; stderr shows `98 label(s) are attached to the WRONG SIDE` | demonstrated |
| 14 | **JOB 3 — not run on the real dataset.** The step exists and is unit-tested on synthetic games only, as the brief requires. | no `run()` invocation; the self-test's fixtures come from `e0013_extract.synthetic_row` | demonstrated |

### Two findings worth the successor's attention

**(a) "the label is constant within a game" is FALSE as stated, and the naive test of it
aborts on correct data.** B2 sentence 1 gives a white-to-move position `s` and a
black-to-move position of the SAME game `1 − s`, so the emitted `y` values inside one game
are legitimately the pair `{s, 1 − s}`. What is single-valued per game is the WHITE-FRAME
outcome `s` — and that is the quantity the per-game clustering of `s_d` rests on, since B3's
effective N is the number of games. My first draft asserted "all `y` equal within a game" and
aborted on 14 correct games. The tool now asserts the true invariant (one `s` per game;
every `y` in `{s, 1 − s}`) plus a second check that a label from another game cannot enter.
**A reader who takes the naive form of this claim into the power analysis computes the wrong
`N`.**

**(b) My first wrong-side check shared its oracle with the thing it checked.** It computed
`expected` with `position_label` — the same function that produced `y` — so both sides moved
together and the check could not fail. The oracle is now the extractor's `label_side_to_move`,
which this module cannot override at runtime. A second defect of the same family: the control
patched `e0013_label.position_label` via `import e0013_label`, which under
`python tools/e0013_label.py` is a DIFFERENT module object from `__main__`, so the patch never
reached the running code and the control silently proved nothing. Both are now asserted, the
second with an explicit check that the patch was in effect.

## What I Did NOT Do (and why)
- **Did NOT run the extractor on the real dataset**, in any mode, so the full-mode (labelled)
  artifact is not re-emitted. That is a prohibition for this job and a separate seat's pass.
  The manifest records `fitter_corpus.sha256: null` with the reason, and `read_corpus()`
  REFUSES a corpus until it is filled — so the gap is a control, not a silent hole.
- **Did NOT read the holdout, fit anything, or run E-00014 / E-00015.**
- **Did NOT touch `src/`, `SPLIT_SALT`, the dedup key, the dedup order, the survivor rule, or
  the 30,000 floor.** The floor is a module constant with no CLI route, asserted by a test.
- **Did NOT edit** E-0013 (any `status:` / `result:` / `H_body`), any H-####, any R-00xx, any
  CLOSED/VERIFIED record, E-00014, E-00015, `tools/e0011_check.py`, `tools/e0012_sprt.py`,
  or `.gitignore`.
- **Did NOT author the tactical suite (F-U14).** That is Job 4 of a later session and must be
  authored independently of this project's records.
- **Did NOT open or close HO-0005 / W-0003.** S-0039 already names HO-0019 as the
  verification route for these three changes; I have not added to or closed it.

## Claims I Made That Are NOT Yet Verified
- **None of this discharges Gate 3.** The three changes are a contract implementation and go
  to HO-0019 (verification-auditor) with S-0038's work, exactly as S-0039 directs. Every
  "demonstrated" above is *this seat's own* demonstration.
- **The label step's `run()` path is unexercised on real data.** It is syntactically checked
  and its logic is unit-tested on synthetic games; its first real invocation is still ahead,
  and it should be treated as unproven until it has produced a labelled corpus.
- **E-00015 still carries the retired band** at L133-137 / L152-153 / L245-248 and its
  decision rule 3 still routes an out-of-band count to a re-decision. That is the E-00015
  executor's dated amendment, not mine, and E-00015 must not pass before it lands.

## Environment Facts Learned
- **`run_commands` reports exit 1 on success.** Verdicts come from `$LASTEXITCODE` and from
  file contents. Confirmed again throughout.
- **PowerShell strips double quotes from command-line arguments**, so an anchor containing
  `"` cannot be passed inline; anchors with quotes must arrive via a file (`build/s43/apply.py`
  reads `@path` anchors for this reason). This silently produced zero-match patches.
- **The editor cannot round-trip these files' CRLF line endings**, and its auto-indent
  rewrites the interior of multi-line string literals. Every edit to `tools/` therefore goes
  through `build/s43/patcher.py`, which normalises EOL, asserts a unique match, and writes back
  with the file's own convention.
- **Line-range replacement is not safe on its own.** A replacement whose end anchor is
  ambiguous truncates the following block, and the damage is silent because the file is a
  Python script that simply stops parsing later. Several rounds of damage in
  `tools/e0013_label.py` came from this; every fix since is verified by `ast.parse` AND by
  running the module, not by inspection.
- `pyflakes` is not installed; `ast.parse` plus a real run is the substitute.

## State Left On Disk
- `tools/e0013_extract.py` — band retired, floor kept, identities added, `src_commit` pinned,
  mode/corpus named, self-test 79 → 112 checks.
- `tools/e0013_pins.py` — NEW: the read-time re-hash and `read_corpus()`.
- `tools/e0013_label.py` — NEW: the label construction step, train-only, 29 checks.
- `research/manifests/e0013-artifact-pins.json` — NEW: the pin, with `fitter_corpus.sha256`
  honestly `null` and the reason recorded.
- `build/s41/extract_new/` — untouched. Its `report.json` still carries the stale
  `src_commit` 9f6574c and the retired `band` key; the manifest names both as superseded facts
  about those bytes rather than pretending otherwise.
- Scratch and all evidence under `build/s43/` (gitignored).

## Next Action For The Successor
- **Re-emit the full-mode artifact at a clean commit**, then fill `fitter_corpus.sha256` in the
  manifest. Until then no fitter may read TRAIN. `--assert-src-commit` must pass first, and it
  passes only when the tool is committed.
- **The owner seat's E-00015 and E-00014 dated amendments** (band retired, stage 4 restated as
  the normalized-FEN key, L68 corrected) must land before either record runs.
- **F-U14, the N ≥ 200 independent tactical suite**, is still unowned and still blocks the
  pre-fit commit.
- **HO-0019** for independent verification of all three jobs.

## Escalations (owner decisions needed)
- **Who re-emits the labelled corpus?** It requires running the extractor on the pinned real
  dataset, which this job was forbidden to do. It gates E-00014 and every fitter, and nobody
  currently owns it.
- **F-U14 ownership** is still unassigned and still blocking.

## Validation Status
- `python research/scripts/research.py update` → **exit 0**, `updated: research/index.md`
- `python research/scripts/research.py state --write` → **exit 0**, wrote `state.md` + `state.json`
- `python research/scripts/research.py validate` → **exit 0**, `Validation OK` (the warnings are
  pre-existing and grandfathered; none concern this session)
- `git diff --check` → **exit 0**, empty
- `python tools/e0013_extract.py --selftest` → **exit 0**, `SELFTEST PASS checks=112 failed=0`
- `python tools/e0013_pins.py --selftest` → **exit 0**, `PINS-SELFTEST PASS checks=15 failed=0`
- `python tools/e0013_label.py --selftest` → **exit 0**, `LABEL-SELFTEST PASS checks=29 failed=0`
- `python build/s43/proof.py` → **exit 0**; `python build/s43/proof_tamper.py` → **exit 0**
- The engine floor `build\Release\kana.exe` was **not** re-run: no `src/` change was made by
  this session. S-0038 verified it at `da93d9c`; the pre-fit commit must re-run it.

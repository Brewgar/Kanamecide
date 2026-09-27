---
id: S-0038
type: session
agent: implementation-engineer
round: 4
title: e0013-normalized-fen-dedup-key-f-u7-f-u13
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-27
closed: 2026-09-27
---

# S-0038 — Session (implementation-engineer)

> One session record per agent session, written to disk BEFORE the chat ends. It is
> the handoff to whoever runs next. Keep it short and factual; the records are the
> detail.

## Round / Work Items Touched
- Round 4. E-0013 only, under the S-0037 leakage ruling (obligations F-U7..F-U13).
- W-0003 remains untouched: not claimed, not closed. HO-0005 not opened or closed.
- Three commits: `ff56c41` (HO-0018), `9f6574c` (HO-0019), `da93d9c` (the code change).
  **The two handoffs are committed separately from the code, as required.**

## The one-line cause, in my own words
The dedup key was `pos.fen` — six fields, clocks included — while the overlap-0 gate compares
`normalize_fen` — four fields, clocks excluded. A key *strictly finer* than the key a gate
compares cannot **entail** the invariant that gate verifies, so the gate could never pass by
construction; it could only pass by coincidence. The `K+R vs K` endgames supplied the
coincidence's failure: 27 identical four-field FENs, one on each side, differing only in the
clocks. The gate did its job. The tool's key was under-specified.

## What I Did (with evidence)
| # | Action | Evidence (command → exit code → result) | Calibration |
|---|---|---|---|
| 1 | Filed the two handoffs S-0037 recorded as owed, with **CLI-allocated** IDs | `research.py new-handoff` ×2 → exit 0 → `HO-0018`, `HO-0019`; short slugs (MAX_PATH) | demonstrated |
| 2 | Captured the **old-key baseline** before touching code | `--count-only --dry-run` → **rc 2** (gate 27) → `build/s41/baseline_old_key.txt` | demonstrated |
| 3 | **F-U7** — changed the dedup KEY, not the gate | `tools/e0013_extract.py` `extract()` stage 4 + `build_report()` `dedup_key`; `run_gates()` **untouched** | demonstrated |
| 4 | **F-U8** — repaired the false-pass self-test, added the clock-only fixture and the negative control | `--selftest` → rc 0 → `SELFTEST PASS checks=79 failed=0` | demonstrated |
| 5 | **F-U9** — re-ran under the new key | `--count-only --out-dir build/s41/extract_new` → **rc 0**, gate `normalized_fen_overlap=0` | demonstrated |
| 6 | **The split-map digest prediction HELD** | old `bb079a41…d4ada1ea` → new `bb079a41…d4ada1ea`, **byte-identical**; `split_map_invariance_unchanged=True` | demonstrated |
| 7 | Proved the invariance **assertion itself** fires | `SPLIT_SALT=20260927` → **rc 2** `ABORT: split_map_sha256 INVARIANCE VIOLATED` | demonstrated |
| 8 | Confirmed Gate 0 intact | `build\Release\kana.exe` → rc 0 → `=== ALL TESTS PASSED` | demonstrated |

## The two code locations, before and after

**1. `extract()`, stage 4 — the dedup loop**
```python
- if pos.fen in seen:                 + if dedup_identity(pos) in seen:
      continue                             continue
- seen.add(pos.fen)                   + seen.add(dedup_identity(pos))
```
where `dedup_identity(pos) -> pos.norm_fen`. The key is now **the same key the gate compares**.

**2. `build_report()`, `extraction_pin` — the published key**
```python
- "dedup_key": "exact FEN (all six fields; the clock is part of the identity)"
+ "dedup_key": "normalized FEN (side to move + piece placement + castling/EP; the halfmove
+               clock and the fullmove number are NOT part of the identity)"
+ "dedup_key_excludes": ["halfmove clock", "fullmove number"]
+ "dedup_key_equals_gate_key": True
```

**The gate was NOT weakened.** `run_gates()` is unchanged in its logic. Weakening the gate to
match the key would have inverted the fix by deleting the instrument that found the defect.
Only its *docstring* changed, because it claimed to be "STRICTER than the dedup" and that is
no longer true — it is now the same key.

## The yield delta — MEASURED, not estimated

The owner explicitly declined to estimate this. It is a measurement:

| quantity | old key | new key | delta |
|---|---|---|---|
| `count_usable_distinct` | 76,593 | **74,452** | **−2,141** |
| `count_usable_distinct_train` | 61,598 | **59,892** | **−1,706** |
| `count_usable_distinct_holdout` | 14,995 | **14,560** | **−435** |
| `duplicates_removed_by_dedup` | 0 | **2,141** | +2,141 |
| `positions_sha256` | `07cff1ce1df3b148…` | **`ac8c92f05026646d…`** | changed |
| `split_map_sha256` | `bb079a41630161bc…` | **`bb079a41630161bc…`** | **UNCHANGED** |
| `normalized_fen_overlap` | **27** | **0** | −27 |

**The 30,000 floor is NOT breached: 59,892 ≥ 30,000**, so `rule_output=all-terms-scope-stands`
and **no stop condition was reached.** Nothing was re-split, the floor was not adjusted, and
the endgame region was not excluded.

## The pre-registered prediction: it HELD

`split_map_sha256` is a pure function of `(SPLIT_SALT, game_id)`, computed over the dataset's
game rows before and independently of the dedup, and its hashed object contains no
dedup-derived quantity. So it had to be byte-identical.

- **Old key:** `bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea`
- **New key:** `bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea`
- **Verdict: HELD — byte-identical.** A moved digest would have meant the salt, the fraction
  or the rule moved, which this ruling does not authorise.

I did not take this on trust. It is now a **machine assertion** (`SPLIT_MAP_SHA256_EXPECTED`)
that **aborts** rather than adopting a moved digest, and I **showed it firing** by perturbing
the salt in a scratch process (rc 2, `ABORT: split_map_sha256 INVARIANCE VIOLATED`). An
assertion nobody has seen fire is not tested.

**A correction to the record, which matters for F-U9:** the ruling refers to "the committed
split map" and its "committed SHA-256", but **no such file is committed.** Commit `1a2dff7`
added only `tools/e0013_extract.py`, and S-0036's run aborted before writing. `build/` and
`m0_audit/` are both gitignored. So there was no committed artifact to compare against; the
baseline I compared to is the one I measured under the old key minutes earlier. The
*invariance claim itself* is unaffected and is now properly pinned — but "the committed map"
describes something that does not exist.

## F-U8 — the false pass, and what I changed about it

The old check asserted the normalized-FEN invariant "holds BECAUSE the dedup ran first". That
was **false in general**; it held only because that fixture's duplicate copies were
byte-identical *including clocks*, so the finer key caught them by luck.

- **Removed exactly one pre-existing check** — the false assertion itself — and re-stated it
  as BY CONSTRUCTION. I diffed the check-name sets before and after: 59 → 79, one removed, 21
  added, **nothing else dropped or weakened**.
- **New permanent fixture** `clock_only_row()`: two games reaching the same positions at
  *different plies*, so every shared copy is a **clock-only** duplicate. Verified directly:
  8 shared normalized FENs, **16 distinct exact FENs, 0 byte-identical**.
- **RED under the old key:** it keeps every copy and the gate would fire on all 8.
- **GREEN under the new key:** one survivor each, cross-split overlap 0, end-to-end exit 0.
- **New negative control:** the production path is re-pointed at the superseded key → the run
  **aborts rc 2** and writes **no** artifact; the **identical** corpus passes and writes once
  the key is restored. The passing and failing cases are the same input, so the control
  proves something about the key, not about the fixture.

Two fixture bugs I hit and fixed (both recorded in the code so they are not re-introduced):
putting the shuffle in the **san** segment made the first copies byte-identical, defeating the
fixture; and a **rook** shuffle silently **destroys castling rights**, which changes the
normalized FEN and would have made the fixture lie.

## What I Did NOT Do (and why)
- **Did not weaken, re-order, re-normalize or suppress the gate.** It stays blocking at both
  pre-registered levels and still withholds every artifact on failure.
- **Did not run E-00015.** It stays `PENDING`; its pre-registration references the superseded
  key. I ran the extractor in **`--count-only`**, which reads no label field at all.
- **Did not read the holdout, did not read any label field, did not fit anything.**
- **Did not change** `SPLIT_SALT`, the dedup order, the survivor rule, the 30,000 floor, or
  the band. The band is still `75600..76587`; the new count lands **below** it
  (`band: below`), which is a **measurement to report, not a value to adjust**.
- **Did not touch `src/`**, `tools/e0011_check.py`, `tools/e0012_sprt.py`, E-0013's
  `status:`/`result:`, any H-####, any R-00xx/S-00xx, HO-0005, or W-0003.
- **Did not commit the extraction artifacts** — see Escalations.

## Claims I Made That Are NOT Yet Verified
- **The whole change is unverified by anyone but me.** Gate 3 forbids it. It is routed to
  **HO-0019** (the ruling) and to the F-U7..F-U13 implementation review.
- **The yield figures are my measurement**, reproducible from the commands in this record.
- **The claim that the new key makes the gate pass was a proof; it is now also a
  measurement** (`normalized_fen_overlap=0`, exit 0) on the real dataset.

## Environment Facts Learned
- `run_commands` reports **exit 1 on success**; take verdicts from `$LASTEXITCODE` and file
  contents. Confirmed again this session.
- The **opening** segment is replayed as **UCI**, the **san** segment as **SAN**. Putting SAN
  in `opening` raises `InvalidMoveError`.
- A rook shuffle **destroys castling rights** (`KQkq` → `Qq`), which changes the *normalized*
  FEN. A fixture meant to hold placement/side/castling/EP constant must not move a rook or king.
- `build/` and `m0_audit/` are **gitignored**, so extraction artifacts are un-committable
  without a policy decision.
- `git commit -m` with embedded double quotes breaks PowerShell parsing; use `-F <file>`.
- `git cat-file -p` piped through `>` is contaminated (PowerShell writes UTF-16 and converts
  line endings); read blobs with `python -c "subprocess.check_output(...)"` instead.

## State Left On Disk
- `tools/e0013_extract.py` — the key change, the assertion, the fixtures (commit `da93d9c`).
- Artifacts: `build/s41/extract_new/{positions.jsonl, split_map.json, report.json}` —
  `positions_sha256=ac8c92f05026646dc376deb9dbcc3205d0b324c815333d92d02bfba46040bf15`,
  `split_map_sha256=bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea`,
  report 3,573 B. **Not in git** (see Escalations).
- Evidence: `build/s41/{baseline_old_key.txt, run_new_key.txt, selftest_final.txt,
  assertion_fires.txt}` (gitignored scratch).
- E-0013 stays `RUNNING`; E-00014 and E-00015 stay `PENDING`. **No lifecycle transition.**

## Next Action For The Successor
- **verification-auditor: take HO-0019.** The ruling is not self-certifying, and neither is
  this implementation.
- **F-U10..F-U13 remain open**: re-derive E-00015's band (F-U10), re-derive E-00014's inner
  partition (F-U11), route the low-`game_id` survivor bias into Sample Validity (F-U12), and
  keep the gate blocking (F-U13).
- Only after F-U10 may **E-00015** run. **E-00014** still waits on F-U11. **No fit may read
  the holdout** until the ruling is independently verified.

## Escalations (owner decisions needed)
- **F-U10 needs a ruling I cannot make:** the band `75600..76587` is frozen, and the new
  measured yield **74,452 lands below it** (`comparison: "below"`, down from `"above"`).
  Re-deriving the band is the owner's act and is recorded as a dated amendment **to E-00015**,
  not to E-0013. I did not adjust it.
- **F-U9's "commit the artifacts" cannot be satisfied as written.** The artifacts live under
  `build/`, which is gitignored, and `m0_audit/` is too. Committing them needs a `.gitignore`
  decision that is not mine to make. They are on disk with their hashes above.
- **The survivor bias is a named limitation now** (F-U12): 2,141 data were **deleted**, and
  the survivor rule keeps the lowest-`game_id` copy, so the corpus is biased toward
  low-numbered games exactly where collisions occur.
- **W-0003 / HO-0005 untouched**, as instructed.

## Validation Status
- `python research/scripts/research.py validate` → exit 0, `Validation OK` (remaining lines
  are pre-existing grandfathered/advisory warnings, not failures).
- `python research/scripts/research.py update` → exit 0, `updated: research/index.md`.
- `python research/scripts/research.py state --write` → exit 0, wrote `state.md` + `state.json`.
- `git diff --check` → exit 0, empty.
- `python tools/e0013_extract.py --selftest` → exit 0, `SELFTEST PASS checks=79 failed=0`.
- `python tools/e0013_extract.py --count-only --out-dir build/s41/extract_new` → **exit 0**,
  `normalized_fen_overlap=0`, `split_map_invariance_unchanged=True`.
- `build\Release\kana.exe` → exit 0, `=== ALL TESTS PASSED` (no `src/` change, re-verified).

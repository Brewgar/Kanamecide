---
id: HO-0016
type: handoff
from: researcher-architect
to: systems-researcher
work_item: null
status: DONE
title: "Execute E-00015: count-only realized usable quiet yield pass (measurement, not training)"
artifacts: ["research/experiments/E-00015-e-0015-count-only-realized-usable-quiet-yield-pass-for-e-0013-measurement-not-training.md", "research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "research/reviews/R-0019-e-0013-pre-registration-critique-h-0013-texel-fit-contract-ho-0013-six-question-ruling.md", "m0_audit/e0011/check_output.txt", "tools/e0011_check.py"]
commands: ["python research/scripts/research.py validate"]
acceptance: "E-00015's Results section carries every pre-registered count field (count_bare_ply, count_after_crash_excl, count_after_degenerate_excl, count_usable_distinct, count_usable_distinct_train, count_usable_distinct_holdout, and the game/dedup counts) with the command/exit-code/hash ledger, OR an explicit abort with the triggered abort condition. No label is read, no fitting occurs, no filter, band, floor or split is changed after the count is seen, and the band comparison is reported as-is."
example: false
created: 2026-09-26
closed: 2026-10-04
---

# HO-0016 - Execute E-00015: the count-only realized-yield pass (MEASUREMENT, not training)

> The ONLY way to ask another agent to do something. Prose requests are not handoffs and
> will be ignored. Receiver appends `## Response` and `## Verification`.

## Request

E-00015 is filed and PENDING. It is the BUCKET-2 measurement sub-contract for R-0019's
B6: the count-only pass that measures E-0013's **realized usable quiet yield** under
E-0013's own filter - the number that arms or disarms the 30,000 scope floor.

**This is a COUNT, not a training run and not a fit.** It replays recorded SAN move lists
through `python-chess` and counts positions. It fits nothing, evaluates nothing, builds
nothing, and licenses no claim beyond the count.

**The two hardest constraints, stated first because breaking either voids the pass:**

> **1. NO LABEL IS READ.** The pass is label-free by construction. It must not touch `res`
> or anything derived from it, and must not compute a loss, a correlation, or a
> per-side-position label distribution. This is what makes a whole-dataset count
> acceptable here at all. Reading a label is abort condition 3.

> **2. THE FILTER, THE DEDUP ORDER, THE SPLIT, THE FLOOR AND THE BAND ARE FIXED BEFORE
> YOU SEE THE COUNT.** They are pre-registered in E-00015. If your realized
> `count_usable_distinct` lands outside the pre-registered band
> `75,600 <= count <= 76,587`, you report it as-is, name which arithmetic assumption it
> breaks, and route it. You do **not** re-run with a modified filter, you do **not** widen
> the band, and you do **not** move the 30,000 floor. A count that lands badly is a
> result, not a retry.

E-0013's split map must already exist and be hash-recorded before you run. If it does
not, that is abort condition 2.

Read E-00015 in full first. Its four decision branches and seven abort conditions are
pre-registered. Your job is to execute and report; the branch is selected by E-00015's
fixed rule applied to the counts you report, and the all-terms / reduced-scope question
belongs to E-0013, not to you.

**If branch 2 fires (TRAIN-side count below 30,000),** the reduced scope is explicitly
**NOT** the mobility/tempo subset. E-0013's B5 correction note records that E-0010:344
attributes the two WORST marginal contributions (mobility -3.7 Elo, tempo -11.5 Elo) to
exactly those terms, so the ladder's fallback citation is backwards. A reduced scope must
be re-derived and re-registered under its own critique. Report the count; do not choose a
replacement scope.

**Specifically NOT authorised:**
- Reading any label field.
- Changing the predicate, the dedup order (global-before-split, per F9), the split salt,
  the split map, the 30,000 floor, or the band after seeing the count.
- Any fitting, any game generation, any engine pair, any SPRT activity.
- Editing `tools/e0011_check.py`, `tools/e0012_sprt.py`, or any engine source file. If
  you need a counting tool, write a new one; do not modify the verified checker.
- Flipping E-00015 or E-0013 to RUNNING, or changing any H-#### status.

## Artifacts To Read (paths)

- `research/experiments/E-00015-*.md` - the contract. Read it in full before running.
- `research/experiments/E-0013-*.md` - the parent contract: the QUIET predicate spec, the
  exclusions, the split discipline, and the F9 global-before-split dedup rule.
- `research/reviews/R-0019-*.md` - section B6, and the arithmetic section that derives the
  band and identifies 76,593 as a per-ply count for a different filter.
- `m0_audit/e0011/check_output.txt` - the terminal diagnostic (read-only), the source of
  the already-measured figures E-00015 cites. Do not recompute them and do not present
  them as this pass's output.
- `tools/e0011_check.py:371-398` - the quiet-proxy predicate and the position-dedup
  instrument, cited read-only. **Not to be edited;** the checker is a VERIFIED artifact.

## Commands To Run

```powershell
cd c:\Users\tahae\Kanamecide
python research/scripts/research.py validate
# then the counting command you wrote, captured as
#   command -> exit code -> output path -> SHA-256
```

Shell caveat in this environment: `run_commands` often reports `Command exited with code 1`
on commands that succeeded, and PowerShell `>` writes UTF-16. Use
`| Out-File -Encoding utf8 <file>` and read the FILE; take every verdict from file
contents, and state the discrepancy in your response if the file and the status disagree.

## Acceptance Criteria (what makes this DONE)

1. **Every** pre-registered count field is reported: `plies_san_total`, `count_bare_ply`,
   `count_after_crash_excl`, `count_after_degenerate_excl`, `count_usable_distinct`,
   `count_usable_distinct_train`, `count_usable_distinct_holdout`, `games_used`,
   `games_excluded_crash`, `games_excluded_degenerate`, `duplicates_removed_by_dedup` -
   or reported as `null` with the reason. No field silently omitted.
2. The headline count is recomputable from the stage-by-stage counts by a reader.
3. The band comparison against `75,600..76,587` is reported explicitly, as-is.
4. Train/holdout overlap counts are reported at BOTH the game level
   (`tuple(opening) + tuple(san)`) and the normalized-FEN level, so the overlap-0
   invariant is checkable rather than asserted.
5. An explicit statement that no label field was read, with the counting code as evidence.
6. The dataset SHA-256, E-0013 split-map hash, python-chess and Python versions, the
   exact counting command with exit code, the raw evidence path, and the aggregator
   command reproducing every number are all recorded.
7. Any abort is reported as an abort, with the triggered condition number and evidence.
8. Nothing outside E-00015's Results/Provenance sections is edited.

**Explicitly NOT an acceptance criterion:** a count inside the band, or a count above
30,000. A count below the floor is a legitimate and useful result: it converts a latent
trap into a known state, and E-0013's rule already says what happens then.


## Response (receiver, append-only)
- 2026-09-26 - (role) - ...
- **2026-10-04 — systems-researcher (executor seat) — EXECUTED.** Pre-conditions: HO-0023's
  verification sign-off landed today (B6 was E-00015's last blocker; B4/B6 discharged). Preflight:
  `python tools/e0013_extract.py --selftest` → `SELFTEST PASS checks=112 failed=0`, exit 0;
  `python research/scripts/research.py validate` → exit 0, 0 problems. Then the ONE authorized
  count-only pass:

  ```
  python tools/e0013_extract.py --dataset m0_audit/e0011/games.jsonl \
    --expected-dataset-sha256 27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95 \
    --count-only --out-dir build/e00015/count_only
  -> exit 0 (RUN=0), transcript _obs/e0015/run_count_only2.txt
  ```

  One prior invocation aborted in pre-checks on hex-case spelling of the dataset pin (same bytes,
  `RUN=2`, nothing written; retained at `_obs/e0015/run_count_only.txt`). No amendment or
  instrument was touched; `tools/`, `src/`, E-0013, E-00014 are unmodified (`git status` attest
  at commit time).

  Headline: **`count_usable_distinct` = 74,452** (train 59,892 / holdout 14,560); all five
  accounting identities hold; overlap-0 at game and normalized-FEN levels; the 30,000 floor on
  the TRAIN side **HOLDS** (headroom 29,892) — the fixed rule selects the **all-terms-scope-stands**
  branch. Full stage table, identity table, abort-condition discharge and hashes are now in
  E-00015's Results/Provenance; E-00015 front matter is `status: COMPLETED`, `completed:
  2026-10-04`, `result: PASS - ...` — per this handoff's acceptance criterion 1 and the record's
  own Follow-Up ("the executor reports the counts and closes it").

  **Determinism receipt:** this run's `positions.jsonl` digest
  (`ac8c92f05026646dc376deb9dbcc3205d0b324c815333d92d02bfba46040bf15`) is byte-identical to the
  count-only-pass digest already pinned in `research/manifests/e0013-artifact-pins.json` — the
  same frozen dataset under the same tool reproduces the same bytes (an independent, unsolicited
  cross-check, not a requirement of this pass).

  Acceptance 1–8 self-check: 1 (all 11 count fields, non-null) ✓; 2 (headline recomputable:
  76.593k − 2,141 = 74,452 = 59,892 + 14,560) ✓; 3 (no band exists post-amendment; reported
  *as-retired*) ✓; 4 (overlap reported at both levels, both 0) ✓; 5 (no label read —
  `rows_with_null_y` = rows) ✓; 6 (dataset/split-map hashes, tool versions, command, exit code,
  raw paths recorded) ✓; 7 (no abort) ✓; 8 (edits confined to E-00015's Results/Provenance +
  its own lifecycle fields; untrue to say 'nothing else edited' — this Response and the E-00015
  status/result/completed fields are the authorized exceptions) ✓.
- **Verification remains open for a fresh verification-auditor seat** (re-run the pass into a
  scratch dir and/or independently recompute the counts from the produced artifacts before
  closing this handoff).

## Verification (receiver, append-only)
- **2026-10-04 — verification-auditor (fresh seat; authored none of this run).** Independent
  harness `_obs/e0015/verify_e0015.py` recomputes every headline number from the raw frozen
  dataset and the committed split map **without importing the extractor**, then does a
  byte-level determinism re-run into `_obs/e0015/scratch_rerun/`. Raw output:
  `_obs/e0015/verify_out.txt` — **29/29 PASS, OVERALL PASS, exit 0.** Recount reproduced
  `plies_san_total=120,930`, `count_bare_ply=76,593`, crash/degenerate stages, dedup
  (2,141), `count_usable_distinct=74,452`, train/holdout `59,892 / 14,560`; split map
  re-derived from `SPLIT_SALT=20260926` matches the committed map bit-for-bit; the executor's
  `positions.jsonl` re-aggregated independently (74,452 rows, y all null, norm_fen unique,
  train/holdout normalized-FEN overlap 0); scratch re-run bytes **identical** to the executor
  artifact (exit 0). Abort conditions re-inspected: dataset/split-map pins match; no label
  read; predicate fidelity — the record's `extraction_pin` block names the same four stages
  and normalized-FEN key this seat counted against, and the tool's selftest (112 checks)
  pinned the dedup key = gate key.
- One observation, recorded not repaired (not a defect of the pass, which was one authorized
  pre-amendment-state run already plus this fixing invocation): the tool's dataset-pin check
  compares hex strings case-sensitively; the executor's first invocation aborted on uppercase
  spelling of the same bytes. Disclosed openly in E-00015 Results; nothing was produced or
  seen.
- verdict: **VERIFIED** — the counts are the platform's numbers, reproducible bit-for-bit;
  the record's lifecycle edit (COMPLETED, `2026-10-04`) and Results/Provenance fill match the
  raw artifacts. This handoff is **DONE**, `closed: 2026-10-04`.
- verdict: ...

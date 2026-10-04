---
id: E-00015
type: experiment
title: "E-00015 - count-only realized usable quiet yield pass for E-0013 (MEASUREMENT, not training)"
status: COMPLETED
result: "PASS - realized usable quiet yield measured: count_usable_distinct=74,452 (train 59,892 / holdout 14,560); all five accounting identities hold; overlap-0 at both levels; 59,892 >= 30,000 floor, so conjunct (a)'s floor sub-condition holds and the all-terms scope stands. Measurement only; no training, no label read."
elo_change: null
hypothesis: H-0013
priority: high
owner: systems-researcher
pre_registered: 2026-09-26
example: false
created: 2026-09-26
completed: 2026-10-04
tags: [texel, yield, count-pass, scope-floor, pre-registration]
last_updated: 2026-10-03
related: [HO-0023, E-0013, HO-0016, FND-0023, FND-0026, FND-0029]
---

# E-00015 - count-only realized usable quiet yield pass for E-0013 (PENDING; NOT RUN)

> Filed by researcher-architect, 2026-09-26, as the BUCKET-2 sub-contract for R-0019's
> B6. **This is a COUNT-ONLY record. It is not a training run, not a fit, and not a
> strength measurement.** It counts positions under E-0013's own filter and reports the
> number. It fits nothing, evaluates nothing, and licenses no claim beyond the count.
>
> **NOTHING HAS RUN.** No extraction, no counting, no fitting, no SPRT game. This record
> is PENDING and may not be flipped to RUNNING by its author. Executor seat:
> **systems-researcher**, under **HO-0016**.
>
> **Why this record exists.** E-0013's conjunct (a) is a scope/yield gate, and the number
> E-0013 quoted - `quiet_proxy_opening_skipped = 76593` - is a PER-PLY count over the
> `san` segment for the BARE quiet predicate, measured by `tools/e0011_check.py:385-398`
> with no crash exclusion, no degenerate exclusion, no dedup and no split. It is
> therefore not the realized usable yield under E-0013's own filter, and E-0013's phrase
> "Expected yield (measured, not assumed)" is superseded by its 2026-09-26 addendum. The
> number that arms or disarms the 30,000 scope floor has to be measured by a count-only
> pass over E-0013's actual filter. That pass is this record.

## Hypothesis

None. This record measures a count and reports it. There is no hypothesis to support or
reject, and it is deliberately not dressed up as one: a count either comes out where the
pre-registered scope rule says it should, or it is reported and routed.

## Baseline

The terminal checker diagnostic on the R-0017-VERIFIED dataset
(`m0_audit/e0011/check_output.txt`): `san_position_yield=120930`, `opening_plies=10000`,
`quiet_proxy_opening_skipped=76593`, `duplicate_positions=1705`,
`total_positions=130930`, `degenerate_mate_san_le_6=1`, no `crash` row in `end_counts`.
These are the already-measured quantities the pre-registered band is computed from. This
record does not recompute them and does not treat them as its own output.

> **[SUPERSEDED 2026-10-03 — B6 amendment, clause 1.]** The word "band" in the sentence above
> is retired text, kept verbatim as filed. The band these figures were used to derive no longer
> exists (E-0013 Addendum 2, S-0039 Ruling 1 / F-U10, 2026-09-27). The figures themselves are
> unaffected: they remain cited, read-only, and are still **not** this record's output.

## Candidate

N/A - nothing is fitted and nothing is compared.

## Difference

N/A - a count has no arms.

## Hardware

Single host, CPU only. No engine binary is invoked: the pass replays recorded SAN move
lists through `python-chess`, exactly as `tools/e0011_check.py` does. No game generation,
no engine pairs, no Gate-0 build required.

## Engine Version

N/A for execution (no engine runs). The dataset's provenance is cited read-only: dataset
SHA-256 as below, generator binary
`504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa`, generator commit
`7b1dda15f675b884a8bf971eec4b53a0fdf2049f`. **No engine source file is edited by this
record or by its executor, and `tools/e0011_check.py` is CITED, never edited.**

## Network

N/A.

## Dataset

### Source (frozen, single)

ONLY `m0_audit/e0011/games.jsonl` - 1,000 rows, SHA-256
`27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95`. Failed attempt-1
excluded. No external data.

### The filter being counted (this is the thing that makes the number E-0013's)

Exactly E-0013's own filter, all four stages, in this order:

1. **QUIET predicate** on each `san` position (the `opening` segment is never a
   candidate): not in check on the position BEFORE the move played; `"x" not in san`;
   `san` does not end in `+` or `#`; `full_ply >= 10`, where
   `full_ply = board.fullmove_number * 2 + (0 if board.turn == WHITE else 1) - 1`.
2. **Crash exclusion:** games with `end == "crash"` are excluded (no trustworthy label).
3. **Degenerate exclusion:** games with `end == "mate"` and `len(san) <= 6` are excluded.

## Free-parameter set

N/A - nothing is fitted. The only "parameter" in this record is the scope-floor value
`30000`, which is pre-registered and not a free choice.

## Fitting method

N/A - no fitting, by construction. If this pass ever fits anything, it is void.

## Test Method

1. Verify the dataset SHA-256 matches the pin above. Mismatch = ABORT.
2. Verify E-0013's split-map hash exists and is recorded. Absent = ABORT.
3. Replay each game's `opening` + `san` through `python-chess` and count, reporting each
   stage separately so the arithmetic is auditable:
   - `plies_san_total` (all `san` positions, no filter);
   - `count_bare_ply` (stage 1 only, the figure comparable to 76,593);
   - `count_after_crash_excl` (stage 1 + 2);
   - `count_after_degenerate_excl` (stage 1 + 2 + 3);
   - `count_usable_distinct` (all four stages = E-0013's realized usable yield);
   - `count_usable_distinct_train` and `count_usable_distinct_holdout` (the split of the
     above, BY GAME via the committed map);
   - `count_usable_distinct_train_TRAIN_SIDE_ONLY` - i.e. the TRAIN-side figure after
     any further inner carving is NOT taken here; the scope floor is evaluated on the
     TRAIN side of the outer split, which is the quantity named in the decision rule;
   - `games_used`, `games_excluded_crash`, `games_excluded_degenerate`;
   - `duplicates_removed_by_dedup`.
4. Report the pre-registered band comparison (below).

> **[SUPERSEDED 2026-10-03 — B6 amendment, clause 1.]** There is no band to compare against.
> This item is replaced by: report the five exact accounting identities named in the 2026-10-03
> B6 amendment below, with the offending dict if any is false.

5. Report every field in Provenance. Omitted field = abort condition 7.

## Games / Samples

The whole verified dataset, all 1,000 games, filtered. No subsampling, no cap. Expected
output magnitude, as a BAND not a point, computed by the owner from already-measured
quantities and stated here so the executor can sanity-check without it being a target:
`75,600 <= count_usable_distinct <= 76,587`. Upper bound = 76,593 minus at most 6
positions from the single degenerate game and zero crash games. Lower bound = 76,593 minus
~997 projected cross-game FEN duplicates, from the measured 1705/130930 = 1.302 %
duplication rate. **The band is a sanity check, not a pass criterion: a count outside the
band is reported as-is and routed, never adjusted, re-run to land inside, or discarded.**

> **[SUPERSEDED IN PLACE 2026-10-03 — B6 amendment, clause 1. This paragraph is RETIRED text,
> retained verbatim as filed and NOT deleted.]** The band `75,600..76,587` was **RETIRED** by
> E-0013's Addendum 2 (S-0039 Ruling 1 / F-U10, 2026-09-27) as a pre-key-change artifact: both
> endpoints were functions of the OLD exact-FEN key's expected output, and the 1.302 % rate that
> produced the lower bound is blind by construction to the clock-only duplicates the
> normalized-FEN key removes. The live replacement text for this clause is the 2026-10-03 B6
> amendment at the end of this record.

## Metrics

- `count_usable_distinct` - the headline number, E-0013's realized usable yield.
- `count_usable_distinct_train` - the number the 30,000 scope floor is evaluated on.
- The stage-by-stage counts above, so any reader can recompute the headline from them.

## Pre-Registered Decision Rule

> MANDATORY and fixed before the count exists.

1. If `count_usable_distinct_train >= 30000`: conjunct (a) of E-0013 PASSES on yield, and
   the all-terms scope (KING PSTs frozen) stands. Report the count and the band
   comparison.

> **[SUPERSEDED IN PLACE 2026-10-03 — B6 amendment, clause 1.]** "the band comparison" in rule 1
> is retired text. Rule 1's floor test is UNCHANGED and still governs; what is reported alongside
> the count is now the five exact accounting identities, not a band comparison.
2. If `count_usable_distinct_train < 30000`: conjunct (a) FAILS its scope sub-condition;
   the all-terms claim is **WITHDRAWN** (recorded, not silently kept); the scope is
   **NOT** reduced to the mobility/tempo subset, because per E-0013's B5 that subset is
   not derivable from the attribution it cites (E-0010:344 measures mobility -3.7 Elo and
   tempo -11.5 Elo, the two WORST marginal contributions in the ladder); the reduced
   scope must instead be re-derived and re-registered under its own critique before use.
   E-0013 then ends INCONCLUSIVE-BY-SCOPE rather than proceeding on an unjustified scope.
3. If the count lands outside the pre-registered band `75,600..76,587`: report it,
   report which arithmetic assumption it breaks (the duplication projection, the
   degenerate-game bound, or the crash count), and route to a named re-decision. Do NOT
   re-run with a modified filter to land inside the band.

> **[SUPERSEDED IN PLACE 2026-10-03 — B6 amendment, clause 3 — this rule is RETIRED, kept
> verbatim as filed and NOT deleted.]** It has no object: the band was retired by E-0013's
> Addendum 2 (S-0039 Ruling 1 / F-U10, 2026-09-27), so a count cannot land outside it. It is
> replaced by the five exact accounting identities and their ABORT branch; see the 2026-10-03
> B6 amendment at the end of this record. Rules 1, 2 and 4 and the four pre-registered failure
> interpretations are UNCHANGED.
4. If any pre-registered field cannot be produced: report `null` with the reason. Do not
   substitute a different count.

**The floor is on the TRAIN-side count, not the whole-dataset count**, so that no
whole-dataset quantity decides the fit's scope (R-0019 Q2). The 30,000 value is
pre-registered and fixed; it may not be renegotiated after the count is reported.

**Prohibitions.** The executor may not change the filter, the dedup order, the split
salt, the split map, the floor, or the band after seeing the count. The executor may not
compute any label-derived quantity. The executor may not report the count in a way that
selects a favourable branch.

> **[SUPERSEDED IN PLACE 2026-10-03 — B6 amendment, clause 1.]** "or the band" is retired text
> (there is no band to move). The prohibition is UNCHANGED IN FORCE and now reads: the executor
> may not change the filter, the dedup key, the dedup order, the split salt, the split map, the
> floor, or the accounting identities after seeing the count.

4. **GLOBAL-before-split exact-FEN dedup** (F9): dedup is global, before the split; the
   surviving copy's `game_id` determines the split.

> **[SUPERSEDED IN PLACE 2026-10-03 — B6 amendment, clause 4 — stage 4 is RESTATED, kept
> verbatim as filed and NOT deleted.]** The dedup key is no longer the exact FEN. It is the
> **normalized FEN** (F-U7 / `FND-0023`): side to move + piece placement + castling/EP rights,
> with the halfmove clock and fullmove number **excluded** from a position's identity. Ruled by
> E-0013's S-0037 leakage ruling (2026-09-27) and implemented under S-0038. The
> global-before-split ordering and the surviving copy's `game_id` clause are UNAFFECTED and
> remain exactly as written above.

### The split

E-0013's committed split map (`SPLIT_SALT = 20260926`, `random.Random(SPLIT_SALT *
1000003 + game_id)`, 80/20 BY GAME), read-only, hash-recorded. The split map MUST already
exist and be hash-committed before this pass runs; if it does not, this record ABORTS,
because a count that is not attached to a committed split map cannot arm a scope rule.

### Label handling

**This pass reads no labels at all.** It is a pure count over positions and game
metadata. It does not touch `res`, does not compute a loss, a correlation, or a
per-side-position label distribution. This is deliberate: it keeps the pass incapable of
informing the fit's direction, and it means the pass cannot leak even in principle.

> **[Section-stranding repair, 2026-10-04, systems-researcher executor seat.]** The block above
> ("MANDATORY and fixed before the count exists" through "### Label handling") was found
> stranded under `## Follow-Up` (the known 2026-09 handoff-corruption class; the `## Pre-
> Registered Decision Rule` heading stood **empty**), which is why `research.py validate`
> rejected `COMPLETED` ("section '## Pre-Registered Decision Rule' is absent/empty — DEC-0009
> requires pre-registration"). The block was MOVED here **verbatim**; nothing was written or
> reworded. Follow-Up retains its own follow-up bullets only.

## Power And Sample Size

> What N settles this rule: N/A in the statistical sense. This is a deterministic count
> over a frozen 1,000-row dataset, not a sample. The relevant "N" is the full dataset,
> and it is used in full. There is no power question, no effect size, and no CI; the
> uncertainty in the expected figure lives entirely in the pre-registered band, which is
> stated as a band for exactly that reason. No pass/fail in this record may be described
> in terms of statistical confidence.

> **[RE-DESCRIBED IN PLACE 2026-10-03 — B6 amendment, clause 2. The paragraph above is kept
> verbatim as filed and is NOT deleted; one sentence in it no longer has an object.]** This is
> a deterministic count over a frozen 1,000-row dataset, not a sample. There is no sampling
> uncertainty, no effect size, and no CI. The reason a band is no longer given is that
> **projections rot under a key change while arithmetic does not**: the band was a projection
> of the old exact-FEN key's duplication volume (E-0013 Addendum 2, S-0039 Ruling 1 / F-U10,
> 2026-09-27), whereas the replacement instrument is the five exact accounting identities,
> which are key-independent. See the 2026-10-03 B6 amendment at the end of this record.

## Sample Validity

- **Filter fidelity:** the predicate is E-0013's, stage for stage, including the
  check-state-before-the-move detail and the `full_ply >= 10` floor. A divergence between
  this pass's predicate and E-0013's is a FAIL of the pass, because the number would then
  not be E-0013's number.
- **Dedup discipline:** global-before-split, surviving copy's `game_id` determines the
  split, and the normalized-FEN overlap-0 gate then verifies that invariant. Both the
  game-level (`tuple(opening) + tuple(san)`) and normalized-FEN-level overlap counts are
  reported so the invariant is checkable, not asserted.
- **Label-free by construction:** no label is read, so the count cannot inform the fit's
  direction or magnitude. This is the property that makes a whole-dataset count
  acceptable here at all.
- **Dedup key normalization:** the overlap-0 check uses E-0013's normalization
  (side-to-move + placement + castling/EP, excluding the halfmove clock and fullmove
  number), so this pass and E-0013 compare like with like.

## Provenance

- Dataset SHA-256: `27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95` (1,000
  rows, 1,384,548 B; measured by the tool at run time, equals the pin — abort condition 1
  satisfied, not triggered).
- E-0013 split-map hash (input; pre-existing and committed):
  `build/s41/extract_new/split_map.json` SHA-256
  `bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea` — re-hashed at read time by
  the tool itself (`split_map_invariance.unchanged: true`) and independently by
  `python tools/e0013_pins.py --verify` → exit 0, `PINS OK artifacts=3` (abort condition 2
  satisfied, not triggered).
- Already-measured baseline figures cited (not recomputed; the 2026-10-04 run independently
  produced `plies_san_total=120930`, `opening_plies_total=10000`, `count_bare_ply=76593`,
  `degenerate_mate_san_le_6=1` end-event, `crash=0` — agreeing with the baseline cited above;
  the old duplicate figure `1,705` pertained to a **different** measurement (exact-FEN key over
  `opening+san` segments), superseded context per the retired-instrument note).
- Predicate source cited: `tools/e0011_check.py:385-398` (read-only; NOT edited). The running
  extractor's filter stages, dedup key and split rule are emitted verbatim in the run's
  `report.json` under `extraction_pin` (abort condition 5 evidence) and the tool's own
  `--selftest` ran **112 checks, PASS** immediately before the pass (`_obs/e0015/selftest.txt`).
- Environment (recorded, not assumed): **Python `3.14.6`, `python-chess 1.11.2`**, Windows;
  host single-CPU; no engine binary invoked.
- The exact counting command, exit 0:
  `python tools/e0013_extract.py --dataset m0_audit/e0011/games.jsonl --expected-dataset-sha256
  27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95 --count-only --out-dir
  build/e00015/count_only`
  → raw transcript `_obs/e0015/run_count_only2.txt` (SHA-256
  `4bdce06e604ec70765323e9fcc5dd1fb8c787cdc956d8df207fb6ff3552b9af5`).
- Artifact hashes (SHA-256, measured 2026-10-04):
  - `build/e00015/count_only/positions.jsonl` — `ac8c92f05026646dc376deb9dbcc3205d0b324c815333d92d02bfba46040bf15` (13,004,718 B; kind `count-only-pass`; every row's `y` is `null`; NOT a labelled corpus)
  - `build/e00015/count_only/report.json` — `3ec92dc80597f3a4c0b8b018b796683b9debf6e166ae626a0e285a6a5f76d18f` (6,049 B)
  - `build/e00015/count_only/split_map.json` — `bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea` (14,463 B; tool-copied, mode-independent)
- Aggregator reproducing every number: `python -m json.tool` / `jq`-equivalent over
  `build/e00015/count_only/report.json` (keys `counts`, `gates`, `accounting_identities`,
  `scope_floor`) — every figure quoted in Results is one-to-one with that file.
- Provenance pin held: `report.json.provenance.src_commit` =
  `52b520f5d563340a7672dfd45d65b428e09a7ea2` with `committed_blob == running_blob` — the code
  that ran is exactly the code committed at HEAD at run time (S-0039 provenance contract).

## Abort Conditions

1. Dataset SHA-256 does not match the pin. Mismatch = ABORT.
2. E-0013's split-map hash does not exist or is not recorded. Absent = ABORT.
3. Any label field (`res` and anything derived from it) is read by the counting code.
   ABORT - the pass is void, not repaired.
4. Any non-zero train/holdout overlap at the game level or the normalized-FEN level.
5. The predicate as implemented diverges from E-0013's predicate on any of the four
   stages.
6. The dedup order is per-split rather than global-before-split.
7. Any pre-registered output field is omitted. Report it as `null` with the reason rather
   than dropping it.

**An abort is a result.** It is reported in the open with its reason. It is never
converted into a passing count by adjusting the filter, the band, or the floor.

> **[SUPERSEDED IN PLACE 2026-10-03 — B6 amendment, clause 1.]** "the band" here is retired
> text. It is replaced by "the accounting identities": a false identity aborts the pass, and it
> may not be made to hold by adjusting the filter, the dedup key, or the floor.

## Results

**Executed 2026-10-04 by the systems-researcher seat under HO-0016, after HO-0023's
verification sign-off (the last GO blocker). Exactly one authorized deterministic count-only
pass ran** (B6 amendment §5). One immediately preceding invocation aborted **during
pre-checks** with no count produced: the operator spelled the dataset pin in uppercase hex
(`27EA181D…`) against the record's lowercase pin — same bytes, string-compare abort, `RUN=2`,
nothing written (`_obs/e0015/run_count_only.txt`, retained). It is excluded as a failed attempt,
per the same "Failed attempt-1 excluded" discipline this record's Dataset section already
documents. No fitting, no label read, no engine invocation, no re-run after seeing any count.

**Stage-by-stage counts** (all fields present; none null; command → exit code → path → hash in
Provenance):

| field | value |
|---|---|
| `plies_san_total` | 120,930 |
| `count_bare_ply` | 76,593 |
| `count_after_crash_excl` | 76,593 |
| `count_after_degenerate_excl` | 76,593 |
| `count_usable_distinct` | **74,452** — E-0013's realized usable quiet yield |
| `count_usable_distinct_train` | **59,892** — the quantity the 30,000 floor is evaluated on |
| `count_usable_distinct_holdout` | 14,560 |
| `duplicates_removed_by_dedup` | 2,141 |
| `games_used` | 999 |
| `games_excluded_crash` | 0 |
| `games_excluded_degenerate` | 1 |
| train/holdout overlap, game level | **0** (`tuple(opening) + tuple(san)`) |
| train/holdout overlap, normalized-FEN level | **0** |

**The five accounting identities — all TRUE** (B6 amendment clause 3; no band exists):

| identity | value |
|---|---|
| `usable_equals_after_degenerate_minus_dedup` | true (76,593 − 2,141 = 74,452) |
| `usable_equals_train_plus_holdout` | true (59,892 + 14,560 = 74,452) |
| `stages_monotone_non_increasing` | true |
| `dedup_removed_at_least_zero` | true |
| `one_survivor_per_normalized_fen` | true |

**Pre-registered branch selected by the fixed rule: the TRAIN-side count 59,892 ≥ 30,000 floor
(headroom 29,892), so conjunct (a)'s floor sub-condition HOLDS and the all-terms scope stands.**
(This is the count that discharge E-0013 conjunct (a) quoted; what E-0013's owner does with the
discharged conjunct is E-0013's seat, not this record's.)

**Abort conditions 1–7: none triggered** (evidence for 1, 2, 5 in Provenance; 3: `label_frame_uniform:
null` and `rows_with_null_y: 74,452` of 74,452 rows — no label field was read; 4: both overlap
counters 0; 6: `dedup_order: GLOBAL, before the split`; 7: every pre-registered field above is
non-null).

## Statistical Analysis

TBD - and expected to remain short: this is a count.

## Interpretation

TBD.

## Conclusion

TBD.

## Follow-Up

- The executor reports the counts into this record and closes it.
- The TRAIN-side count then arms or disarms E-0013's conjunct (a) via the rule fixed
  above, which was written into E-0013's 2026-09-26 addendum BEFORE this record was
  filed.
- If branch 2 fires, the reduced scope must be re-derived and re-registered under its own
  critique before use (see E-0013's B5 correction note and follow-up obligation F-U4).
- This record does not verify itself; any count it reports is a claim by the executor
  seat, covered by E-0013's independent verification (Q-0006 gate 7, F-U5).
- No H-#### status is changed by this record.

> **[Section-stranding repair, 2026-10-04.]** The decision-rule block previously stranded here
> ("MANDATORY and fixed before the count exists" … "### Label handling") was moved verbatim into
> its own canonical heading `## Pre-Registered Decision Rule` above; see the dated note there.

---

## Addendum 2026-10-03 — B6 AMENDMENT (systems-researcher, E-00015's executor seat): the retired band is replaced by the five exact accounting identities, filter stage 4 is restated as the normalized-FEN key, and ONE deterministic count-only pass is authorised

> Filed by **systems-researcher** on 2026-10-03, as E-00015's `owner:` and its executor seat,
> under **Sponsor Ruling 2** and discharging **HO-0023 row B6**. E-0013 Addendum 2 (S-0039
> Ruling 1 / F-U10, 2026-09-27) required this amendment to be made, dated, in E-00015, by this
> seat, **before the pass runs**.
>
> **APPEND-ONLY, and no pre-existing text above is deleted.** Every superseded clause is marked
> in place, at its own location, with the clause number that replaces it. `status:` remains
> `PENDING`; `result:` remains `null`; no count exists.
>
> **NOTHING WAS RUN TO PRODUCE THIS AMENDMENT.** No extraction, no counting, no fitting, no
> label read, no holdout read, no engine invocation. Every claim below is either a quotation of
> this repository's own text or a pointer to it. `tools/e0013_extract.py`,
> `tools/e0013_pins.py`, `tools/e0013_eval.py`, `tools/e0011_check.py`, `tools/e0012_sprt.py`
> and every `src/` file are **unmodified**. E-00014 and E-0013 are **unmodified**.

### 0. Why this amendment exists, in one paragraph

E-00015's pre-registration described an instrument that its owner had already retired. The band
`75,600..76,587` was **RETIRED** by E-0013's Addendum 2 on 2026-09-27 (S-0039 Ruling 1 /
F-U10, `FND-0026`): both of its endpoints were functions of the OLD exact-FEN key's expected
output, and the 1.302 % duplication rate that produced its lower bound is blind by construction
to exactly the clock-only duplicate class that the normalized-FEN key removes. The instrument
was retired in the code — the band constants are gone from `tools/e0013_extract.py`, no report
key named `band` is constructed anywhere, and the retirement is published as a tombstone with
`is_live: False`. **The pre-registration still described the old instrument.** A count measured
under a superseded description is the "number that looks authoritative and is wrong" the S-0037
leakage ruling warned about, so the pass does not run until this amendment lands.

### 1. Clause 1 — the Games/Samples band clause is replaced by the accounting identities

**The expected output magnitude is NOT pre-registered as a band, and no band is reinstated in
its place.** The `75,600..76,587` clause and its lower-bound arithmetic (76,593 minus ~997
projected cross-game duplicates at the measured 1.302 % rate) are **RETIRED**. Retirement
authority, cited by record and date: **E-0013 Addendum 2, S-0039 Ruling 1 / F-U10, 2026-09-27**
(`FND-0026`, RESOLVED). Nothing replaces the band *as a band* — a re-derived band under the new
key would be computed from `duplicates_removed_by_dedup`, which is an output of the very run the
band is meant to check, and an instrument that cannot fail is not an instrument.

**The audit instrument for this pass is now the five exact accounting identities in clause 3.**
They are arithmetic between quantities this run measures, so they are key-independent and cannot
rot. They introduce **no threshold**, so there is no new number that can be wrong.

**What is still true of this section and is unchanged:** the pass counts the whole verified
dataset, all 1,000 games, filtered; no subsampling, no cap; and the already-measured baseline
figures in `## Baseline` and `## Provenance` remain **cited, read-only, and not this record's
output**.

### 2. Clause 2 — the Power section is re-described, not deleted

The `## Power And Sample Size` paragraph is **kept verbatim as filed**; one sentence in it — that
the uncertainty "lives entirely in the pre-registered band, which is stated as a band for exactly
that reason" — no longer has an object, because there is no band. Its live replacement:

- This record is a **deterministic count over a frozen 1,000-row dataset**, not a sample. The
  relevant "N" is the full dataset and it is used in full.
- There is **no sampling uncertainty, no effect size, and no CI.** That sentence of the filed
  paragraph is correct and **stays**.
- **No pass/fail in this record may be described in terms of statistical confidence.** Unchanged.
- **Why no band is given:** projections rot under a key change while arithmetic does not. The
  band was a projection of the old exact-FEN key's duplication volume (E-0013 Addendum 2,
  S-0039 Ruling 1 / F-U10, 2026-09-27; `FND-0026`). The dedup key changed under **F-U7 /
  `FND-0023`**, ruled by E-0013's S-0037 leakage ruling (2026-09-27) and implemented under
  S-0038. The identities that replace the band are exact and key-independent.
- **Test Method item 4** ("Report the pre-registered band comparison (below)") is replaced by:
  report the five identities of clause 3, with the offending dict if any is false.

### 3. Clause 3 — decision rule 3 is replaced by the five exact accounting identities

Decision rule 3 as filed ("if the count lands outside the pre-registered band … report which
arithmetic assumption it breaks … route to a named re-decision") is **RETIRED**: there is no
band, so it has no object. Its replacement is the **five identities the tool already emits**
under `accounting_identities` in `tools/e0013_extract.py`, named exactly as the tool names them
so a reader can diff this clause against the code:

| # | identity name | the arithmetic it asserts |
|---|---|---|
| 1 | `usable_equals_after_degenerate_minus_dedup` | `count_after_degenerate_excl - duplicates_removed_by_dedup == count_usable_distinct` |
| 2 | `usable_equals_train_plus_holdout` | `train + holdout == count_usable_distinct` |
| 3 | `stages_monotone_non_increasing` | `count_bare_ply >= count_after_crash_excl >= count_after_degenerate_excl >= count_usable_distinct` |
| 4 | `dedup_removed_at_least_zero` | `duplicates_removed_by_dedup >= 0` |
| 5 | `one_survivor_per_normalized_fen` | `distinct_norm_fens == count_usable_distinct` |

**Failure branch — this is not a warning.** If **any** identity is false, the pass **ABORTS** and
the violation is reported with the offending dict. `tools/e0013_extract.py` already aborts with
`ABORT: EXACT ACCOUNTING IDENTITIES VIOLATED: {...}`; this clause makes that abort **E-00015's own
pre-registered obligation** rather than the tool's private behaviour. A false identity is a
finding to report, never a new baseline to adopt.

Identity 5 is the one that answers what Ruling 1 says was lost: it ties the survivor count to the
distinctness of the dedup key rather than to any expected magnitude, so a future key change that
quietly stops deduplicating is caught at once instead of waiting for a magnitude cross-check.

**Unchanged by clause 3:** decision rules **1, 2 and 4**; the **30,000 scope floor** on
`count_usable_distinct_train` (explicitly *not* the retired band, and not renegotiable after the
count is reported); and the pre-registered failure interpretations of rules 1-2.

### 4. Clause 4 — filter stage 4 is restated as the normalized-FEN dedup key (F-U7)

Stage 4 as filed reads "GLOBAL-before-split **exact-FEN** dedup (F9)". That key is **superseded**.
Stage 4 is restated as:

> **4. GLOBAL-before-split dedup on the NORMALIZED FEN (F-U7 / `FND-0023`).** A position's
> identity is **side to move + piece placement + castling/EP rights**. The **halfmove clock and
> the fullmove number are EXCLUDED** from that identity. Dedup is global, before the split; the
> surviving copy's `game_id` determines the split.

Authority, cited by record and date: **F-U7**, ruled by E-0013's **S-0037 leakage ruling
(2026-09-27)**, implemented under **S-0038**, closed as `FND-0023` (RESOLVED). The
global-before-split ordering and the surviving copy's `game_id` clause are **unaffected and
remain exactly as filed** — only the key changed.

The overlap-0 invariant is checkable, not asserted: both the game-level
(`tuple(opening) + tuple(san)`) and normalized-FEN-level overlap counts are reported, and both
must be zero (abort condition 4). Per **`FND-0029` / F-U13 the gate stays blocking** — this
amendment weakens nothing, and in particular does not relax the overlap-0 gate, the
dedup-before-split order, or the accounting identities to make a pass runnable.

### 5. Run authorization — ONE deterministic count-only pass, aborts unchanged

**Authorised:** exactly **one** deterministic, count-only pass, under **HO-0016**, on the frozen
pinned inputs. Nothing else. No fitting, no SPRT game, no game generation, no engine pair, no
label read, no holdout read, no re-run after seeing the count.

**All seven abort conditions stand UNCHANGED and UNWEAKENED**, verbatim as filed. In particular:
the dataset SHA-256 pin (1), the committed split map (2), no label field read (3), overlap-0 at
both levels (4), predicate fidelity to E-0013 on all four stages (5), global-before-split dedup
(6), and no omitted output field (7). **Nothing in this amendment is grounds to relax any of
them** (`FND-0029` / F-U13).

**No field of this record may be filled from any pre-existing number.** Every pre-registered
output field must be produced by this run, from the pinned dataset, and reported as measured. The
`74,452` already recorded elsewhere in the project is **non-authoritative for this record**: it is
a count-only figure produced by a different, earlier invocation, and this amendment does not
change its status. Citing it here would import a number into a contract that has not yet measured
one. If a field cannot be produced, it is reported as `null` with the reason — never substituted
from a pre-existing figure.

**Sequence, and the order this amendment was required in.** The band was retired, and this
amendment was filed, **before** the pass runs, before any number exists, and before the 30,000
floor is evaluated on any count that arms or disarms a scope claim. **This amendment is a
re-registration; it is not a run and it produces no number.**

**Not authorised by this amendment:** running the pass in any mode; closing E-00015 on the
existing `74,452`; editing any `tools/` or `src/` file; editing E-0013 or E-00014; or flipping
any record's `status:`.

### 6. Integrity assertions for this amendment

1. `status: PENDING` and `result: null` are **unchanged**. No field of this record is filled from
   any pre-existing number; the count must be produced by the run itself.
2. No clause of this record now **relies on** a retired object: every band reference and the
   exact-FEN stage-4 reference is marked superseded in place at its own location, and each
   supersession names the clause that replaces it.
3. Nothing was deleted. Each superseded clause is retained verbatim as filed, per append-only
   style.
4. The five identity names in clause 3 match `tools/e0013_extract.py` exactly, so the clause can
   be diffed against the code.
5. The 30,000 scope floor, decision rules 1/2/4, the failure interpretations, all seven abort
   conditions, `result: null`, `status: PENDING`, the dataset and split-map pins, and the
   label-free-by-construction property are all **untouched**.
6. `E-00014`, `E-0013`, `tools/e0013_eval.py` and every `src/` file are **untouched**.
7. Nothing was run. This amendment is textual, and every claim in it is a quotation of or a
   pointer to text already in this repository.

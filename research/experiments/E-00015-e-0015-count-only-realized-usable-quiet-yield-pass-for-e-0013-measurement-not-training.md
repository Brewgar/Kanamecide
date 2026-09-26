---
id: E-00015
type: experiment
title: "E-00015 - count-only realized usable quiet yield pass for E-0013 (MEASUREMENT, not training)"
status: PENDING
result: null
elo_change: null
hypothesis: H-0013
priority: high
owner: systems-researcher
pre_registered: 2026-09-26
example: false
created: 2026-09-26
completed: null
tags: [texel, yield, count-pass, scope-floor, pre-registration]
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

## Metrics

- `count_usable_distinct` - the headline number, E-0013's realized usable yield.
- `count_usable_distinct_train` - the number the 30,000 scope floor is evaluated on.
- The stage-by-stage counts above, so any reader can recompute the headline from them.

## Pre-Registered Decision Rule

## Power And Sample Size

> What N settles this rule: N/A in the statistical sense. This is a deterministic count
> over a frozen 1,000-row dataset, not a sample. The relevant "N" is the full dataset,
> and it is used in full. There is no power question, no effect size, and no CI; the
> uncertainty in the expected figure lives entirely in the pre-registered band, which is
> stated as a band for exactly that reason. No pass/fail in this record may be described
> in terms of statistical confidence.

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

- Dataset SHA-256: `27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95`.
- E-0013 split-map hash (input; must pre-exist and be hash-recorded).
- Already-measured baseline figures cited (not recomputed): `san_position_yield=120930`,
  `opening_plies=10000`, `quiet_proxy_opening_skipped=76593`,
  `duplicate_positions=1705`, `total_positions=130930`, `degenerate_mate_san_le_6=1`, no
  `crash` row.
- Predicate source cited: `tools/e0011_check.py:385-398` (read-only; NOT edited).
- python-chess version, Python version, host facts, the exact counting command with exit
  code, the raw evidence path (local, gitignored), and the aggregator command reproducing
  every reported number. Command -> exit code -> path -> hash.
- Tool versions recorded, not assumed.

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

## Results

TBD - nothing has run. This section will be filled with the stage-by-stage counts and
pinned hashes only, never narrative.

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


> MANDATORY and fixed before the count exists.

1. If `count_usable_distinct_train >= 30000`: conjunct (a) of E-0013 PASSES on yield, and
   the all-terms scope (KING PSTs frozen) stands. Report the count and the band
   comparison.
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
4. If any pre-registered field cannot be produced: report `null` with the reason. Do not
   substitute a different count.

**The floor is on the TRAIN-side count, not the whole-dataset count**, so that no
whole-dataset quantity decides the fit's scope (R-0019 Q2). The 30,000 value is
pre-registered and fixed; it may not be renegotiated after the count is reported.

**Prohibitions.** The executor may not change the filter, the dedup order, the split
salt, the split map, the floor, or the band after seeing the count. The executor may not
compute any label-derived quantity. The executor may not report the count in a way that
selects a favourable branch.

4. **GLOBAL-before-split exact-FEN dedup** (F9): dedup is global, before the split; the
   surviving copy's `game_id` determines the split.

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

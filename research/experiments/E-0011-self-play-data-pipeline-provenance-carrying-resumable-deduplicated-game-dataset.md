---
id: E-0011
type: experiment
title: "E-0011 — Self-play data pipeline: resumable, provenance-carrying, deduplicated game dataset for Texel fitting"
status: PENDING
result: null
elo_change: null
hypothesis: H-0013
priority: high
owner: null
pre_registered: 2026-09-22
example: false
created: 2026-09-22
completed: null
tags: [self-play, data-pipeline, texel, pre-registration]
---

# E-0011 — Self-play data pipeline (W-0001 step 1 pre-registration)

> Filed by researcher-architect, 2026-09-22, as W-0001 step 1 per AGENT_MEGAPROMPT_ROUND4.
> **Not run. Gate 0 hard-blocked (F-0002, 6 observations through 2026-09-22); this record
> is a pre-registration only.** Adversarial-reviewer critique (HO-0003) precedes any
> `status: RUNNING`; build/run is implementation-engineer/systems-researcher per W-0001.

## Hypothesis
The E-0010 match harness (`e0010_match2.py`, EV-0002) can be grown into a generator that
produces ≥1,000 legal, deduplicated, provenance-carrying, resumable self-play games —
the dataset H-0013/Q-0006's Texel fit needs. **E-0011 claims an artifact, never an Elo
number.** (Q-0006.)

## Baseline
- Harness: `e0010_match2.py` (per-game JSONL incremental flush + fsync; python-chess
  legal-move opening RNG; ≤2 engine-pairs). Binary: EV-0010 (`build\Release\kana.exe`,
  SHA-256 `504EB01A…A6DAA`), the E-0010 champion configuration `EvalStage=6`.
- Measured throughput for cost estimates: **769 games/hour** at 2 pairs, 100ms+100ms inc
  (E-0010 campaign, 1240 games / 5807 s; verified R-0004/R-0008).

## Candidate
- `tools/e0011_generate.py` (NEW; fork of `e0010_match2.py` adding the provenance schema
  below, the crash/stall rule, and checkpoint-resume semantics).
- `tools/e0011_check.py` (NEW aggregator: legality re-verification, duplicate move-list
  count, provenance-field coverage, resume-consistency counts).
- Dataset at a gitignored local evidence path, one JSON object per completed game,
  appended + fsync'd per game ("legal-move-flushed": a game line is written only after
  its full move list was validated legal).

## Difference
Adds to the E-0010 harness: per-game provenance fields, a campaign checkpoint that is
the JSONL itself, deterministic resume (game seeds are a pure function of the campaign
salt and game index), and an aggregator that enforces the acceptance gates below.

## Hardware
Single host, CPU only, ≤2 engine pairs concurrent (Round-3 stall lesson; E-0010).

## Engine Version
`EvalStage=6` vs `EvalStage=6`, SAME binary as both engines (self-play for training
data; the strength relation between arms is not measured here — see Decision Rule).

## Network
N/A.

## Dataset (per-game JSONL schema — all fields MANDATORY, gate (d))
`game_id` (int, dense), `campaign_salt` (int), `seed_int` (the exact RNG seed integer),
`opening` (10-pli UCI list), `a_white`/`b_white` flags, `eval_stage_a`/`eval_stage_b`,
`binary_sha256`, `src_commit`, `tc` + `tc_command`, `time_started`, `time_finished`,
`res` (A/B/D), `end` (mate/rule50/repetition/plycap/crash), `plies`, `san` (full move
list), `crash_incident` (bool + text) whenever the crash rule fired.

## Test Method
1. Build/pin the binary; record SHA-256 (reuse EV-0010's unless rebuilt — a rebuilt binary
   gets its own hash recorded per game).
2. Pre-flight: ≥6-game smoke of the new driver; 6/6 legal, varied plies (E-0010 precedent).
3. Launch under `runjob.py` (see Run Plan). Target ≥1,000 games; new campaign salt
   (`20260922`, distinct from E-0010's `20260914`) so the datasets cannot silently mix.
4. Mid-campaign: kill the generator at an arbitrary point; `runjob.py resume`; confirm
   the game count only grows and no game_id is re-emitted (gate (e)).
5. Final: run the aggregator; fill Results. NO Elo computation is part of this experiment.

## Games / Samples
- Target: ≥1,000 completed games (≈1.3 h at the measured 769 games/h; hard campaign cap
  2,000 games, pre-registered, so an anomalous run cannot burn the round).
- Colors alternate per DEC-0010 (gate: `a_white` counts balanced within ±1).

## Metrics
games, legal_games, duplicate_move_lists, provenance_field_coverage, crash_incidents,
resume_added_games, campaign wall-clock vs the predicted 769 games/h. **NOT Elo.**

## Pre-Registered Decision Rule
> One rule, stated here FIRST. PASS requires ALL of (a)–(f). Any failure ⇒ FAIL with the
> failed conjuncts named; no conjunct may be relaxed after the first game is written.

(a) **Volume:** aggregator reports ≥1,000 games.
(b) **Legality:** aggregator re-validates every move of every game with python-chess:
    illegal_move_count = 0; engine crash/stall handled ONLY by the DEC-0010 crash rule
    (offender loses; incident recorded), never silently restarted or excluded.
(c) **Independence/dedup:** duplicate-move-lists = 0 over all games (full list = opening
    + moves; aggregator rebuilds and compares, as `e0010_report.py` does).
(d) **Provenance:** 100% of game records carry every Dataset field above.
(e) **Resumability:** the planned kill→resume leaves duplicate-move-lists = 0 AND final
    game count > game count at kill time (no re-emitted ids; aggregator resume audit).
(f) **No-strength-claim conjunct:** Results/Conclusion contain no engine-strength or Elo
    assertion (the deliverable is an artifact; the strength claim lives elsewhere — below).

### DEC-0010 tier mapping — which tier applies, and why the two MUST NOT be conflated
- **This experiment (E-0011): no tier.** Gates (a)–(f) are artifact counts with no
  statistical H0/H1; DEC-0010's tiers govern *engine-strength deltas*. There is nothing
  here for a tier to decide; attaching one would re-invent the F6/R-0003 defect.
- **The downstream claim** "the dataset trains an eval that BEATS the hand-tuned eval"
  (Q-0006) is a champion-replacement claim ⇒ **DEC-0010 Tier R** ("version B is stronger
  than A": H0 δ≤0 vs H1 δ≥+5, LLR ±2.9444, cap 30,000, post-cap INCONCLUSIVE), decided by
  a FUTURE experiment on FRESH measurement games under the E-SPRT-lite harness
  (E-0012/W-0005) — never on the training games (that would leak the fit into its own
  test). Tier S would under-claim a release decision (+20 is the "worth investigating"
  floor, not "replace the champion"); Tier M applies only to an explicit magnitude claim
  with a pre-registered [M−50, M] zone. Cited, not re-derived: DEC-0010 tier table,
  D-0007 (RESOLVED), verified by R-0010.

## Power And Sample Size
Two DIFFERENT N questions; the record must not conflate them.

1. **Is 1,000 games enough for the downstream Texel fit?** Yes for the intended use,
   and here is the honest reasoning (ASSUMED parts flagged):
   - E-0010 games ran 52–218 plies in pre-flight smoke with a 300-ply cap (E-0010 update 3);
     assume mean ≈ 120 plies ⇒ 1,000 games ≈ 120k positions; after the quiet-position
     filter and per-position dedup suitable for Texel labels, conservatively ≥50k usable
     (ASSUMED, flagged; the aggregator will MEASURE the realized position yield).
   - The fit targets the small hand-tuned coefficient set of E-0010's `EvalCoeffs`
     (6 term groups; O(10²) scalars even if all MG/EG tables were untied, and far fewer
     for the mobility/tempo re-tune E-0010's ladder motivates). ≥50k positions against
     O(10²) parameters is ≥500 positions/parameter — far above classical Texel fits that
     succeeded at O(10–100) positions/parameter. Sampling noise is NOT the binding
     constraint; the binding constraint is **label/systematic bias** (single-engine
     self-play, one time control), which is why the opening-diversity protocol and the
     holdout are the real power controls. An in-sample R² will NOT be reported as
     success evidence; the only legitimate downstream evidence is the Tier-R SPRT on
     fresh games (above).
   - What 1,000 games CANNOT do: support an Elo verdict. h(N) = 1.96·371/√1000 =
     ±23.0 Elo CI half-width (DEC-0010's calibrated sigma) — fine for a ±20-Elo screen,
     hopeless for the +5-Elo Tier-R claim (needs ~29,160 games sequentially). This is
     exactly why no Elo gate exists in E-0011.
2. **Cost feasibility of the campaign itself:** 1,000 games ≈ 1.3 h at the measured
   769 games/h; cap 2,000 games ≈ 2.6 h worst case. Decidable at the planned N by
   construction (gates are counts, not estimates).

## Sample Validity
- **Arm differentiation:** both engines are the same binary and EvalStage by design
  (self-play); the "negative control" is instead the seeded-arm check: the aggregator
  re-derives every game's opening from `(campaign_salt, game_id)` and asserts the
  recorded opening matches the recorded seed — catches silent RNG drift.
- **Opening diversity (DEC-0010 opening protocol, cited):** 10 random legal plies from
  startpos per game, python-chess legal-move RNG, seed a deterministic function
  `random.Random(salt * 1000003 + game_index)` (salt = 20260922), the SAME opening sent
  to both engines as `position startpos moves <uci...>`. Reported: distribution of game
  lengths and result mix, so the reviewer can see diversity, not just trust it.
- **Independence:** duplicate-move-lists = 0 as gate (c). Position-level dedup for the
  Texel export is a downstream concern of H-0013's fit protocol, recorded here as: the
  aggregator also reports duplicate-position counts so the fitter inherits a measured,
  not assumed, redundancy level.
- **Color balance:** alternating colors per DEC-0010; aggregator asserts balance ±1.
- **Provenance:** per-game fields above + campaign-level binary SHA-256, src commit,
  compile flags, host, salt, and the generator script's own SHA-256 in the RUN record.

## Run Plan (contingent on F-0002 being lifted; nothing runs today)
1. implementation-engineer builds `tools/e0011_generate.py` + `tools/e0011_check.py`
   per this record (`tools/` path per W-0001 deliverable).
2. Launch (detached, heartbeat, checkpoint = the games JSONL, resume-capable):
   ```powershell
   python research/scripts/runjob.py launch --id RUN-0001 --name "E-0011 campaign" `
     --log e0011/run.log --heartbeat e0011/heartbeat.txt `
     --checkpoint e0011/games.jsonl -- `
     python tools/e0011_generate.py --games 1000 --salt 20260922 --out e0011/games.jsonl
   ```
3. Mid-campaign kill→resume: `python research/scripts/runjob.py resume` with identical
   args; resume skips game_ids present in the checkpoint.
4. Heartbeat staleness ⇒ job is DEAD, never "still running" (SYSTEM.md §6; runjob.py).
5. Evidence pinning (per W-0001 exit check): command → exit code → output path →
   SHA-256 of the dataset + the aggregator + the log; RUN record in `research/runs/`.

## Provenance
- Binary SHA-256: EV-0010's `504EB01A…A6DAA` (if rebuilt: record the new hash; gate (d)
  pins it per game either way).
- `src/` commit: HEAD at run time, recorded per game (`src_commit`).
- Compile flags: as built (recorded in the RUN record).
- Raw evidence: gitignored local dataset path + aggregator outputs, hashed in the Results
  section once they exist. Aggregator command: `python tools/e0011_check.py e0011/games.jsonl`.

## Results
TBD — nothing has run; Gate 0 hard-blocked (F-0002). This section will be filled with
aggregator output + pinned hashes only, never narrative.

## Statistical Analysis
TBD. (No inferential statistics are permitted here by gate (f); the section will report
counts, rates, and the measured position yield for H-0013.)

## Interpretation
TBD.

## Conclusion
TBD.

## Follow-Up
- Adversarial-reviewer critique (HO-0003) BEFORE `status: RUNNING`.
- A FAIL on gates (b)–(e) routes to `research/failures/` and blocks H-0013.
- Downstream: H-0013 Texel fit on this dataset; then the Tier-R Elo claim as a NEW
  experiment under E-0012's harness (Q-0006 closes only there).

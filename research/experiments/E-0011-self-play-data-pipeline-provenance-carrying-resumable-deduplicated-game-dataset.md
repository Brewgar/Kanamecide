---
id: E-0011
type: experiment
title: "E-0011 — Self-play data pipeline: resumable, provenance-carrying, deduplicated game dataset for Texel fitting"
status: COMPLETED
result: PASS
elo_change: null
hypothesis: H-0013
priority: high
owner: systems-researcher
pre_registered: 2026-09-22
example: false
created: 2026-09-22
completed: 2026-09-24
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

## Addendum: R-0011 B1 response, 2026-09-23

> R-0011 (critique, COMPLETED): "FRESH games is an adjective, not an enforceable
> protocol field." ACCEPTED in full. The original pre-registered text above is UNCHANGED;
> this addendum pins the machine fields it lacked. Nothing below changes a threshold, a
> tier, or an N — per R-0011's own verdict, no DEC-0010 re-derivation is required.

**(B1.1) Dataset-identity fields — deliverable of Test Method step 5 and of W-0001's
exit check, recorded in Results/Provenance at campaign close (not "once they exist"):**

```
dataset_sha256: <SHA-256 of the final games JSONL bytes>
dataset_n_games: <integer, must equal gate (a) count>
dataset_path:    <local gitignored JSONL path>
```

**(B1.2) Downstream leakage contract** — the future Tier-R experiment (Q-0006's
"beats hand-tuned" claim) MUST satisfy all three clauses and record each in its own
Provenance section, or its verdict is void:

- (a) **Distinct salt:** its campaign salt MUST differ from BOTH E-0011's `20260922` and
  E-0010's `20260914`. The separation of the two existing salts is arithmetic, quoted
  from R-0011: |20260922 − 20260914| × 1,000,003 = **8,000,024** ≫ any game index in
  either plan, so no `(salt, game_index)` pair can collide across campaigns.
- (b) **Machine gate `training_game_overlap = 0`:** the future experiment's aggregator
  MUST rebuild every fresh game's full move list under the SAME normalization gate (c)
  uses (`tuple(opening) + tuple(san)`) and check every one against the pinned E-0011
  dataset (`dataset_sha256` above); the count of fresh move-lists present in the
  training set is `training_game_overlap`, and **= 0 is a gate** — reported in the
  experiment record, not merely asserted. (The aggregator machinery already exists: it
  is the dedup key.)
- (c) **`fitted_params_sha256`:** the future experiment MUST record the SHA-256 of the
  fitted parameter artifact (the Texel/NNUE weights actually loaded), so "retrain,
  then retest, then report the good run" is visible as a hash change between attempts.

Without (1)+(2) a later agent could satisfy every sentence of this record and still
decide Q-0006 on games that trained the eval — R-0011's exact failure mode. This clause
lands before `status: RUNNING` because that is when the artifact's identity becomes
fixed; E-0011 is still PENDING.

## Addendum: R-0011 B2 response, 2026-09-23

> R-0011: "Resume/torn-write semantics are undefined at exactly the boundary the drill
> must exercise." ACCEPTED in full. These definitions bind the build (step 2) and the
> run (step 3); the original text above is unchanged.

**(B2.1) Kill boundary.** The live mid-campaign kill MUST occur in the pre-registered
window **game [400, 600] of 1,000** — chosen so the resume necessarily adds ≥ 400
games, closing R-0011's observation that gate (e) as written FAILs if the kill
coincides with the last game (resume adds zero). A kill outside the window is recorded
as a protocol deviation and gate (e) is then evaluated on the deterministic drill
alone (B2.4).

**(B2.2) Presence test on resume.** A game counts as *present in the checkpoint* only
if its trailing JSONL line (i) parses as JSON, (ii) carries EVERY mandatory Dataset
field per gate (d)'s schema, and (iii) has a `game_id` in the dense expected range.
"An id appears on a line" is explicitly NOT the test: a line whose id matches but
whose schema fails counts as absent and triggers B2.3.

**(B2.3) Torn-write policy — quarantine, never silent truncate.** A kill during the
append can leave a partial trailing line. On resume the generator MUST: (i) test
whether the file's final line parses; (ii) if not, move that partial line verbatim to
`<games>.jsonl.torn` (sidecar, append mode across incidents) and record a
`torn_line_quarantined` incident (recoverable game_id, byte offset, timestamp) in the
run log; (iii) re-emit the affected game under its OWN id (per B2.2 the partial line
never counted as present). In-place truncation is prohibited: the sidecar is the
evidence of the incident.

**(B2.4) Deterministic kill→resume drill — a pre-registered acceptance step, IN
ADDITION to the live mid-campaign kill.** "An arbitrary point" almost never lands in
the write window (R-0011). The drill, which gate (e) requires alongside the live kill:
(i) copy the JSONL to a scratch path; (ii) truncate the copy mid-line at a chosen byte
offset inside a known game record; (iii) resume against the copy; (iv) assert — torn
line quarantined + incident logged, all pre-truncation games intact, the truncated
game re-emitted exactly once under its own id, duplicate-move-lists = 0, and final
valid count = pre-truncation valid count + resumed games.

**(B2.5) Log-preservation rule (answers R-0011: `runjob.py launch` unlinks the old
log).** Stated run policy, binding on step 3: **before any `runjob.py resume`, the
operator copies the pre-resume log to `run.log.<UTC-timestamp>.preserved`** and names
both files in the RUN record; the fresh launch log then starts empty by design. No
`research/scripts/` change is made (selftests stay green — nothing under
`research/scripts/` is touched by this session). Additionally, per R-0011:
`runjob.py`'s checkpoint telemetry counts raw `splitlines()`, so a torn line inflates
`checkpoint_lines`; **runjob counts are telemetry, never an integrity signal** — only
`tools/e0011_check.py`'s parsed-line counts are authoritative.

## Addendum: R-0011 B3 response, 2026-09-23

> R-0011: "Gate (d) is presence-only … and gate (f) is not machine-checkable as
> written." ACCEPTED in full. Gate (d) gains value-level conjuncts; gate (f) keeps its
> place in the rule but its enforcement route changes from aggregator (impossible) to
> reviewer. The original gate list above is unchanged; the conjuncts below ARE gates.

**(B3.1) Gate (d) strengthened — presence PLUS values.** PASS additionally requires
every one of these mechanical checks to hold over 100% of records (any failure = FAIL
of gate (d), named per check):

- `binary_sha256 ==` the campaign-pinned hash recorded at launch (today: EV-0010's
  `504EB01A…A6DAA`; a rebuild before launch re-pins BEFORE game 1, then is immutable
  for the campaign);
- `src_commit ==` HEAD at launch (recorded once, asserted per game);
- `eval_stage_a == eval_stage_b == 6`;
- `campaign_salt == 20260922`;
- `res ∈ {A, B, D}` and `end ∈ {mate, rule50, repetition, plycap, crash}` (the Dataset
  section's closed vocabulary);
- `plies > 0`;
- `time_finished >= time_started`;
- `a_white` boolean AND `a_white` alternates with `game_id` parity (the color
  protocol, machine-checked);
- `game_id` unique, dense, **0-based** (base pinned: E-0010's retained evidence is
  0-based — a 1-based driver inheriting 0-based resume logic is a re-emission bug,
  R-0011);
- `opening` re-derived from `random.Random(20260922 * 1000003 + game_id)` matches the
  recorded `opening` (the seed↔opening negative control from Sample Validity, now
  inside gate (d) so it cannot be skipped).

**(B3.2) Gate (f) gets a machine-checkable route.** The aggregator cannot read
intent, so gate (f) is assigned to the critique/verification layer: the re-critique
reviewer (HO-0006) and any later verifier MUST search Results / Statistical Analysis /
Interpretation / Conclusion for Elo/LOS/CI strength assertions in this record and
record the search command + output in their review. Gate (f) stays in the PASS list;
its check is a named reviewer step with evidence, not an aggregator count.

**Engine-free implementation check (R-0011 Proposed Experiment 2 — adopted as a build
acceptance step):** before any live run, the build session MUST run
`tools/e0011_check.py` over a synthetic 20-game JSONL containing (i) one torn line,
(ii) one wrong-hash game, (iii) one duplicate id, and show the aggregator FAILing all
three with the named conjuncts. Gate 0 is open as of 2026-09-23, but this remains
dry-run work, not a run of this experiment: E-0011 stays PENDING until the
re-critique clears it.

## Addendum: R-0011 N1–N7 (routed text) + Gate-0 UCI-entry note, 2026-09-23

Non-blocking findings, adopted as record text (R-0011's own routing):

- **N1 — measured yield replaces the ASSUMED prior; consequence ladder pinned.**
  R-0011 measured from EV-0001 (1,240 games): mean 130.3 plies/game ⇒ **130,335**
  positions/1,000 games (+10 opening plies ⇒ ≈140k total); quiet-proxy yield **76,887
  per 1,000 games** (59%); 5.8% of games hit the 300-ply cap. The Power section's
  ≈120k/≥50k ASSUMED figures are therefore conservative against evidence from the same
  harness family — the ≥500 positions/parameter sentence now rests on measurement, not
  assumption. **Consequence ladder (pre-registered, cannot be renegotiated after the
  run):** if the realized usable yield is **≥ 30k** positions ⇒ fit as planned; if
  **< 30k** ⇒ the fit is scoped to the mobility/tempo sub-set E-0010's ladder motivates
  and NO all-terms refit claim may be made from it. Parameter count stays an estimate
  (property of `src/`, not frozen until the fit is designed) — flagged same as yield.
- **N2 — "provenance-carrying" scoped:** the artifact is *audit- and
  legality-reproducible from the JSONL* (gates (b)/(c)/(d) re-derive everything from
  the record); it is **not bit-reproducible by re-running the engine** — seeded RNG
  replays the opening, but games run under wall-clock TC with TT/ID. No field claims
  engine replay.
- **N3 — time control pre-registered:** the campaign TC is **100 ms + 100 ms increment
  (O3d formula), ≤2 engine pairs** — identical to E-0010's, so the draw-regime
  provenance of labels is stated, not implied; the aggregator asserts a single distinct
  `tc_command` value across all games.
- **N4 — `san` field semantics pinned:** `san` = **post-opening engine moves only**
  (excludes the 10-ply `opening`), exactly as E-0010's retained data; the dedup key is
  `tuple(opening) + tuple(san)` and the position yield counts `san` plies (+ separate
  opening count). No double-counting.
- **N5 — end-type mix reported:** the aggregator's report MUST include `end` counts
  and a degenerate-game count (`san` ≤ 6 plies with `end=mate` — R-0011 measured
  20/1,240 = 1.6% in the retained data). Reporting, not gating.
- **N6 — colour-conditional score reported as a diagnostic, never a gate:** the
  aggregator reports White's score and A-score-by-color against R-0011/R-0012's
  measured prior (**White 58.5%** overall; k6 cells 0.783 as White vs 0.542 as Black).
  Named action on divergence: investigate as a harness bug (arms/color bookkeeping).
  A 50%-centred band would be an F6-class defect in reverse — explicitly prohibited as
  a gate. H-0013's fit protocol must not treat positions as colour-exchangeable
  without saying so (labels are strongly colour-dependent).
- **N7 — `RUN-0001` id reservation:** validate lists `RUN-0001` as a dangling id
  (referenced by SYSTEM.md and this record). The RUN record is created at launch;
  the reservation is intentional and the dangling reference is transient by design.

**Gate-0 / UCI-entry note (state change 2026-09-23, commit 360924c; flagged for the
build session):** Gate 0 is OPEN — `build\Release\kana.exe` exits 0 with the perft
suite PASS. BUT a probe this session showed that a piped token on stdin did NOT engage
UCI mode: the binary ran its DEFAULT perft harness instead. Before any live E-0011/E-0012
run, the build session MUST confirm the explicit UCI entry path — how
`e0010_match2.py`/`e0011_generate.py`'s `Popen([exe, "uci"])` handshake interacts with
this build (an init `uci` token on stdin, `runjob.py launch`'s detached spawn, or a
CLI flag) — and record the confirmed working invocation in the RUN record. Gate 0 being
open is engine *availability*; the critique loop (HO-0006/HO-0007) is still engine
*permission*. E-0011 stays PENDING.

## Addendum: R-0014 B3 response, 2026-09-23

> R-0014 (critique, COMPLETED): B1 FULLY DISCHARGED, B2 FULLY DISCHARGED, N1–N7 + UCI
> note DISCHARGED, gate (f) route executed PASS; **B3 PARTIAL — one new blocking
> finding: the declared `end` vocabulary is not closed over the harness family's
> reachable endings, and the `(Ns)` suffix is undeclared.** The fix below is landed
> VERBATIM as R-0014 ordered it (their "exact missing sentence", lines 145–150 of
> R-0014). Original text above is untouched; this block is pure additions.

**The operative sentence (R-0014 verbatim, adopted):**

> The `end` field's closed set is extended to `{mate, stalemate, draw-material, rule50,
> repetition, plycap, crash}` — and the record declares whether the `(Ns)` seconds
> suffix is part of the token or a separate `end_seconds` field; the Dataset section's
> `end` schema line and the B3.1 conjunct agree with the extended set.

**Decision on the suffix (the declaration R-0014 requires): the `(Ns)` suffix is NOT
part of the token; it is a separate `end_seconds` field.**
- **What N is:** whole elapsed seconds of the game — from the first engine move to
  terminal adjudication — one single definition for every end-class, no per-class
  variants (driver source of record: `e0010_match2.py` lines 119–125, `end + f"({dt:.0f}s)"`).
  Observed ranges in the retained evidence (my read-only scan, engine-free, pinned
  below): mate 0–19s, draw-claim 2–20s, draw-material 8–19s, stalemate 5–12s,
  plycap 19–21s.
- **Normative status:** `end_seconds` is REQUIRED TELEMETRY (integer ≥ 0, present in
  every record), NOT a member of the closed vocabulary and NOT part of any
  membership test: gate (d) checks the suffix-stripped token against the extended set
  and checks `end_seconds` is a non-negative integer. No class-specific range is
  gated (the retained evidence shows `mate(0s)` and `plycap(21s)`; both legal).
- **Emission + reader rule:** the new generator MUST emit `end` as a SUFFIX-FREE token
  plus `end_seconds` as its own field. For legacy/audit reads of EV-0001-family rows
  (`token(Ns)`), the reader splits at `(`: `end = token`, `end_seconds = int(N)`.
  Retained evidence stays valid under the reader rule without rewrite.

**Extended vocabulary, effective for this campaign:** `end` ∈ `{mate, stalemate,
draw-material, rule50, repetition, plycap, crash}` (R-0014's set, extended per the
verbatim sentence). Mapping of the retained legacy tokens (realized set, my scan):
`mate`→`mate`; `stalemate`→`stalemate`; `draw-material`→`draw-material`;
`plycap`→`plycap`; `draw-claim`→ the fifty-move/repetition pair — the new campaign
splits it into `rule50` (fifty-move claim fired) and `repetition` (threefold
repetition fired); for any legacy row the discriminator is not recoverable from the
retained JSONL alone, so audit reads map legacy `draw-claim` to the pair-union; `crash`
covers the pre-existing crash rule (engine died / illegal / timeout → recorded as
`crash` per the DEC-0010 crash=loss rule, alongside `crash_incident`).

**Dataset-schema agreement (item 3 of the ordered fix):** the Dataset section's `end`
schema line and the B2/B3.1 conjunct are amended BY THIS ADDENDUM (append-only — the
original lines remain visible above, as history): the operative schema for the
campaign is `end` ∈ the extended suffix-free set above AND `end_seconds` (int ≥ 0)
AND `crash_incident` when `end == crash`. `tools/e0011_check.py` implements exactly
this (extended set + suffix-strip reader rule); the synthetic-20-game negative test
gains a fourth fixture: one legacy-style suffixed `end` row must FAIL the campaign
schema while parsing cleanly under the reader rule (proving the rule is implemented,
not assumed).

**Evidence (this session's read-only scan; command → exit → path):**
`python research\context\_s12_endscan.py` → EXIT:0 →
`research\context\_s12_endscan_out.txt`. All-six realized totals (suffix-stripped):
mate 1043, draw-claim 80, plycap 72, draw-material 43, stalemate 2, total 1,240.
**Documentation nit surfaced (does not change the ruling):** R-0014 states
"draw-material (all six rungs, 33/1,240 games)"; my scan finds 43/1,240 — 33 is
exactly the k1–k5 subtotal (11+8+6+3+5), with k6 contributing the remaining 10. The
finding stands under either count (draw-material is present on every rung); the number
should be reconciled at the re-critique.




## Addendum: RUN-0001 close-out (2026-09-24)

RUN-0001 replacement segment is COMPLETED with `result: PASS`. This is a dataset-generation
verdict only; no strength assertion is made. The final generator process was PID 14276
after the recorded kill/resume, and the final checkpoint is 1,000 complete JSONL records.
The final event is `generator_complete` with `valid_after=1000` and the run log ends with
`COMPLETE games=1000 added=600`. The normal campaign path returns 0; the detached
`runjob.py` supervisor records process-gone rather than retaining a long-lived child's
OS return code, so this is the independently recorded terminal interpretation, not a
fabricated process-exit capture. `runjob.py status` independently returned 0 with
`FINISHED (process gone)` and a 1,000-item checkpoint.

### Gate evidence (all six PASS)

- (a) volume: `games=1000 min=1000`.
- (b) JSONL parse and python-chess legality: all 1,000 lines parsed; `illegal_move_count=0`.
- (c) duplicate move-lists: `duplicate_move_lists=0`; color balance `a_white=500`, `b_white=500`.
- (d) provenance/schema: all mandatory fields covered 1,000/1,000; dense unique IDs 0..999;
  named-value conjuncts pass; exactly one pinned time-control command.
- (e) live kill/resume and truncation drill: `kill_in_400_600=True`, `resume=True`,
  `grew=True`, `drill=True`, `torn_incidents=1`, `failures=0`, `duplicates=0`.
- (f) no strength assertion: `strength_assertion_lines=0`.

The finalizer captured checker exit `0` and `OVERALL PASS gates=6` in
`m0_audit/e0011/check_output.txt` (SHA-256
`9fe6b532ad08fce94890bc06b3969b35a0f625e57d94d8edd2851571876ed907`).

### Terminal artifact manifest

- Dataset: `C:/Users/tahae/Kanamecide/m0_audit/e0011/games.jsonl`; 1,000 rows; SHA-256
  `27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95`.
- Finalizer result: `C:/Users/tahae/Kanamecide/m0_audit/e0011/finalizer_result.json`; checker
  exit 0 and the same dataset/check-output hashes.
- Kill/resume evidence: `C:/Users/tahae/Kanamecide/m0_audit/e0011/kill_resume_evidence_v2.json`;
  SHA-256 `7acef0f44d75818f31e1feef184a8353efeecf1edfe3e9b6281447a0645d4bfb`.
- Preserved pre-resume log: `m0_audit/e0011/run.log.20260924T132806Z.preserved`;
  SHA-256 `390f4b8222570f9c5a9e9722130c9de1c16794c62a0946a07ee6c900f7879fc5`, identical to
  the evidence's `source_log_sha256`.
- Completed replacement log: `m0_audit/e0011/run.log`; SHA-256
  `cdb326daa45319fe3e7a67b36022c067fbf327b589fc59c3ad7352c82abd1a56`.
- Event sidecar: `m0_audit/e0011/games.jsonl.events.jsonl`; SHA-256
  `573fa6765068c7e3130079c23628d6c9432a5d172f50057fd2b7e9512b6abbb3`.

All 1,000 replacement rows carry binary SHA-256
`504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa` and source commit
`7b1dda15f675b884a8bf971eec4b53a0fdf2049f`. Attempt 1 remains preserved and excluded
under `m0_audit/e0011_failed_attempt1/`; its 202-row failed segment is not mixed into the
replacement checkpoint.

### Downstream leakage readiness

The pre-registered downstream leakage gate is ready but not executed here: the E-0010
campaign salt is `20260914`, the E-0011 salt is `20260922`, and the downstream E-0012
consumer must compute and record `training_game_overlap = 0` before using the dataset.
`fitted_params_sha256: PENDING_H-0013` is intentionally not fabricated here; no fitted
parameters or downstream strength result are claimed by this experiment. Independent
verification of this close-out is requested by HO-0009.


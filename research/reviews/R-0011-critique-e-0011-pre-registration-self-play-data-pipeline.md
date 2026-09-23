---
id: R-0011
type: review
reviewer: adversarial-reviewer
target: E-0011
kind: critique
status: COMPLETED
work_item: W-0001
related: [E-0011, W-0001, HO-0003, W-0005, E-0012, DEC-0010, D-0007, R-0009, E-0010, EV-0001, EV-0002, H-0013, Q-0006, F-0002]
example: false
created: 2026-09-22
---

# R-0011 — Critique of the E-0011 pre-registration (self-play data pipeline), before any RUNNING

## Scope

HO-0003, executed by the adversarial-reviewer seat (S-0010). I read E-0011, W-0001, DEC-0010,
D-0007, EV-0002, `runjob.py` and E-0010 in full; I re-ran
`python research/scripts/research.py validate` (exit 0, OK) and
`python research/context/w0005_sprt_replay.py` (exit 0); and — because the retained E-0010
JSONL files are read-only evidence that answers two of E-0011's flagged ASSUMED numbers — I
**measured** them myself from `e0010_k{1..6}n_games.jsonl` (EV-0001). Gate 0 was attempted
once: Device Guard block, no process (F-0002, 7th observation, `gate0.txt`); no engine ran,
and none is needed here. E-0011 stays PENDING (nothing below edits it).

Measurements I made this session (commands + outputs quoted in the Evidence appendix):

| Quantity | E-0011 says | I measured (1,240 retained games, EV-0001) |
|---|---|---|
| plies/game (`len(san)`, post-opening moves) | "assume mean ≈ 120" (ASSUMED) | **mean 130.3**, median 117, p10 57, p90 243, max 290 |
| positions per 1,000 games | "≈ 120k" (ASSUMED) | **130,335** engine-move positions (+10 opening plies/game ⇒ ≈140k total) |
| quiet-position yield (my proxy filter, opening skipped) | "conservatively ≥50k usable" (ASSUMED) | **76,887 per 1,000 games** (59 % of all plies) |
| games at the 300-ply cap | not stated | 72/1,240 = 5.8 % (`end=plycap`, `san` = 290) |
| duplicate move-lists | 0 (E-0010) | **0** (rebuilt as `tuple(opening)+tuple(san)`) |
| `game_id` in the retained files | E-0011 schema says "int, dense" | 0-based dense (k6n: 0..239, unique) — **base unspecified** |
| White's score (color-conditional) | not mentioned | **58.5 %** (725.5/1,240); k6 62.1 %; k6 A-score 0.783 as White vs 0.542 as Black |

Two of these (rows 1–3) mean the ASSUMED parts of E-0011's power section are **no longer
assumptions**: they are consistent with, and slightly conservative against, retained evidence
from the same harness family. That is a finding in the record's favour, and it is the only
reason the numbers are quoted here rather than merely asserted.

## Agreements

- **The tier mapping is right, and the separation it claims is the correct one.** DEC-0010's
  tiers govern *engine-strength deltas*; E-0011 delivers an artifact whose gates are counts.
  Attaching a tier to the dataset itself would re-invent the F6 defect. E-0011's own sentence
  ("the deliverable is an artifact; the strength claim lives elsewhere") is exactly the
  discipline DEC-0010 §"Mandatory shared protocol" requires, and it cites (not re-derives)
  the calibrated rule — correct per DEC-0010's re-derivation duty, which applies to a strength
  claim at *its own* TC/draw rate, i.e. to the future experiment, not here.
- **DEC-0010's shared protocol is faithfully inherited**: opening RNG as a function of
  (salt, index), same opening to both engines, alternating colors, duplicate-move-lists as an
  independence precondition, crash = loss recorded per game, one look. I verified the *dedup
  key* construction against the retained data (0 dups under `opening+san`), so gate (c)
  measures the same object as E-0010's post-hoc check.
- **The salt choice is provably non-colliding**: |20260922 − 20260914| × 1,000,003 =
  8,000,024 ≫ any game index in the plan, so no `(salt, game_id)` pair can collide with
  E-0010's stream. "The datasets cannot silently mix" holds as a statement about seeds.
- **Gate (b)'s crash clause is the DEC-0010 rule**, verbatim, and it forbids the two tempting
  cheats (silent restart, silent exclusion).
- **The volume/cost arithmetic checks out**: 1,000/769 = 1.30 h; 2,000/769 = 2.60 h.
- **±23.0 Elo reproduces exactly**: 1.96·371/√1000 = 22.99 (my code, Evidence appendix), and
  the companion "needs ~29,160 games sequentially" matches DEC-0010's Tier-R ASN(H1) =
  29,179.8 (re-derived by `w0005_sprt_replay.py`; R-0010 re-derived 29,159 from the
  un-rounded σ — the same number to σ-rounding). No Elo verdict at N=1,000 is correct, and no
  Elo gate exists in E-0011 — **that stance survives the steelman in Missing Arguments.**


## Disagreements — blocking findings (E-0011 must stay PENDING until these are fixed)

**B1 — "FRESH games" is an adjective, not an enforceable protocol field.** E-0011's
leakage-prevention claim ("never on the training games — that would leak the fit into its own
test") is currently enforced by *future good behaviour*: no field in E-0011 pins the training
set as an exclusion list, and no requirement is placed on the future Tier-R experiment. The
missing fields, precisely:

1. In E-0011's Results/Provenance: a required line `dataset_sha256` + `n_games` + the JSONL
   path, recorded at campaign close (the record now says the raw evidence will be hashed "once
   they exist" — a promise, not a field; make it a deliverable of step 5 and of W-0001's
   exit check).
2. A **"Downstream leakage contract"** clause that the future Tier-R experiment MUST satisfy:
   (a) a campaign salt distinct from `20260922`; (b) a machine check that **every fresh game's
   move list** (same normalization as gate (c)) is absent from the pinned E-0011 dataset,
   reported as `training_game_overlap`, with **= 0 as a gate** (the aggregator machinery
   already exists — it is the dedup key); (c) the hash of the fitted parameter artifact, so
   "retrain, then retest, then report the good run" would be visible.
3. Without (1)+(2) a later agent can satisfy every sentence of E-0011 and still decide Q-0006
   on games that trained the eval. The fix is text-level and cheap, and it must land before
   `status: RUNNING`, because that is when the artifact's identity becomes fixed.

**B2 — Resume/torn-write semantics are undefined at exactly the boundary the drill must
exercise.** Gate (e) ("no re-emitted ids") and step 4 ("kill the generator at an arbitrary
point") do not specify: (i) *which* boundary is killed (between games? mid-game? mid-JSONL
write?); (ii) the **presence test** on resume — "skips game_ids present in the checkpoint"
must mean "the line parses as JSON *and* carries all mandatory fields", not "an id appears on
a line"; (iii) the **torn-write policy**: a kill during the append leaves a partial trailing
line, and the record must say whether that line is quarantined (moved to a `.torn` sidecar
with a `torn_line_quarantined` incident) or truncated, and that the affected game is
re-emitted under its own id; (iv) a **deterministic drill**: "an arbitrary point" almost never
lands in the write window, so pre-register a synthetic-truncation drill (copy the JSONL,
truncate mid-line at a chosen byte offset, resume against the copy) *in addition to* the live
mid-campaign kill. `runjob.py` cannot supply the missing policy: `resume` is a plain re-launch
of the same command line, and its checkpoint telemetry counts **raw `splitlines()`**, so a torn
line counts as one item and would silently inflate "checkpoint_lines". Run-plan gap:
`runjob.py launch` deletes the existing log (`log.unlink()`), so a resume destroys the killed
attempt's log — the plan must copy/rename the pre-resume log as part of the evidence trail.
Also pre-register the kill point (e.g. "kill in [400, 600] of 1,000"), because gate (e) as
written FAILs if the kill coincides with the last game (resume adds zero games).

**B3 — Gate (d) is presence-only, so it can pass on a false-provenance dataset; and gate (f)
is not machine-checkable as written.** Gate (d) requires that "100 % of game records carry
every Dataset field" — a game played by a *different* binary, with a different salt, or with
`eval_stage_a != eval_stage_b`, passes (d) as long as the fields are filled with the wrong
values. Required value-level conjuncts (all mechanical): `binary_sha256 == pinned EV-0010
hash`; `src_commit == HEAD at launch`; `eval_stage_a == eval_stage_b == 6`; `campaign_salt ==
20260922`; `res` in {A,B,D} and `end` in the closed vocabulary; `plies > 0`;
`time_finished >= time_started`; `a_white` boolean; `game_id` unique and dense **with the base
pinned** (E-0010's evidence is 0-based; a 1-based driver inheriting 0-based resume logic is a
re-emission bug). Gate (f) ("no Elo assertion in Results/Conclusion") cannot be checked by an
aggregator at all — the record should say so and route it to the reviewer/verifier instead of
listing it among machine gates.

## Disagreements — non-blocking findings (route to the record)

- **N1 — Power section: replace the ASSUMED yield with the measured prior.** Rows 1–3 of the
  table above; gate-wise the assumption is *not* load-bearing (gates (a)–(f) are counts), but
  it is load-bearing for the *justification* that the fit is feasible. If the real yield were
  40k total positions (≈24–32k after a quiet filter), the "≥500 positions/parameter, far above
  classical Texel practice" claim becomes "≈240–320/parameter, above classical practice" —
  still workable, but a different sentence. Pre-register the consequence ladder now (e.g.
  "<30k usable ⇒ the fit is scoped to the mobility/tempo sub-set E-0010's ladder motivates; no
  all-terms refit") so the outcome cannot be renegotiated after the run.
- **N2 — "Provenance-carrying" must be scoped.** Seeded-RNG capture replays the *opening*, not
  the game: the engines play under a wall-clock TC with TT/ID, so exact re-execution is neither
  guaranteed nor claimed by any field. What *is* reproducible from the artifact is the audit and
  the legality — gate (b) re-validates every move, and the opening-vs-seed re-derivation catches
  RNG drift. Say so explicitly ("audit- and legality-reproducible from the JSONL; not
  bit-reproducible by re-running the engine"), because a future agent will otherwise assume
  replay.
- **N3 — the campaign's time control is not pre-registered.** The record only cites E-0010's TC
  in the baseline. A dataset's TC is part of its identity (labels inherit the draw regime); name
  it (e.g. 100 ms + 100 ms inc, ≤2 pairs) and have the aggregator assert a single distinct
  `tc_command` value across the campaign.
- **N4 — field-name ambiguity vs E-0010's schema.** E-0011 calls `san` the "full move list",
  while E-0010's `san` is the post-opening engine moves (verified: `opening` is a separate
  10-ply list). The dedup key "opening + moves" is correct only if `san` stays post-opening;
  rename it `moves`, or state the exclusion, or a 1,000-game dataset double-counts its openings
  in both the dedup key and the position yield.
- **N5 — report the end-type mix and degenerate games.** 20/1,240 retained games (1.6 %) have
  `san` ≤ 6 plies with `end=mate` (the random-opening protocol can end the game immediately).
  They are legal, deduped and provenance-carrying, so no gate fails — but the aggregator's
  reported distribution should include `end` counts, and a dataset that were *mostly* such games
  would still pass (a)–(f). Reporting, not gating, is the right call; it just has to be in the
  report.
- **N6 — white/color structure is unexamined and it is large.** In the retained data White
  scores **58.5 %** overall (k6: A-score 0.783 as White vs 0.542 as Black on the same pair) — a
  first-move/initiative effect of order +60 to +90 Elo at this TC. This *supports* E-0011's own
  claim that label/systematic bias, not sampling noise, is the binding constraint: the labels
  are strongly colour-dependent. Consequence: the aggregator should report the colour-conditional
  score (free, from the same data), and H-0013's fit protocol should not treat positions as
  colour-exchangeable without saying so. Do **not** turn this into a gate (see Missing
  Arguments).
- **N7 — `validate` reports `RUN-0001` as a dangling id** (referenced by SYSTEM.md and E-0011).
  Expected until the campaign runs; create the RUN record at launch and note the id reservation
  in W-0001 so the dangling reference is transient.

## Missing Arguments

- **The Elo steelman, and why it fails.** The opposite position is: "at N=1,000 a ±23-Elo
  half-width is enough to decide *something*, so the pipeline should take that decision while
  the games exist." The only decisions a ±23-Elo instrument can make are *gross* ones: a
  two-sided 95 % interval excludes 0 at |δ| ≥ 45 Elo, so a pre-registered canary at |δ| ≥ 60
  would have >99 % power — **useful against harness defects** (arms swapped, one engine not the
  pinned binary, colour bookkeeping wrong), **useless against strength claims** (the true effect
  is 0 by construction in a same-binary self-play dataset). But (i) E-0011's arms are the same
  binary and stage, so "strength" has no meaning to test; (ii) gates (b)–(e) plus the ±1 colour
  balance already cover the mechanically plausible failure modes; (iii) a canary built on the
  naive null "White ≈ 50 %" would fire on legitimate chess: I measured White at **58.5 %** in
  this exact harness family, so a 50 %-centred gate is wrong by ~8.5 points (≈2.6σ at N=1,000)
  and would be an F6-class defect in reverse. Correct resolution: no Elo gate in E-0011 (the
  record's stance is upheld); the colour-conditional score is a *reported diagnostic* against
  the measured prior (+60/+90 Elo), with a named action ("investigate as harness bug") rather
  than a verdict. If the author wants an integrity gate, it belongs in E-0012's live validation
  as a null-pair control (see R-0012 N4), not in the dataset record.
- **What E-0011 does not say about who computes the yield.** "the aggregator will MEASURE the
  realized position yield" — but the aggregate that matters to H-0013 (quiet positions, per game
  and total) is a *filtering* decision the aggregator must pin (which positions count as quiet,
  whether in-check positions are excluded, whether the position before or after the quiet move
  is labelled). One sentence, before the run.

## Factual Errors

None found in the claims that matter. Three precision nits, all in the record's own favour or
neutral: the "300-ply cap" is a *total* ply cap (opening + engine moves: capped games carry
`san` = 290 — keep the wording distinct from `plies`); the `a_white` counts are balanced as
claimed (100/200 per rung, 120/240 for k6, verified by me); the σ used in the ±23 arithmetic is
DEC-0010's calibrated 371 Elo/game, derived from *other* rungs' CI half-widths — fine for a
dataset-only claim (no engine delta is asserted), but the same number must not be reused as a
pre-registered σ for a strength claim without DEC-0010's re-derivation duty.

## Assumptions

- E-0011 assumes the E-0010 harness family generalises to a *generator* (same driver, more
  fields, checkpoint). My measurements from the retained data support the throughput/yield part;
  the resume part is exactly what B2 says is unspecified.
- E-0011 assumes the downstream fit needs "O(10²) parameters"; E-0010's `EvalCoeffs` and the
  mobility/tempo re-tune scope are consistent with that, but the actual count is a property of
  `src/`, which is not frozen until the fit is designed. Not blocking; it is the *other* half of
  the ≥500/parameter arithmetic and should carry the same "estimate, not measurement" flag as
  the yield.

## Proposed Experiments

1. **Addendum to E-0011** (author: researcher-architect, before RUNNING) implementing B1
   (leakage contract fields), B2 (resume/torn-write policy + deterministic drill + kill point +
   log preservation), B3 (value-level gate (d) conjuncts; gate (f) routed to review), and
   N1–N7 as text. The reviewer re-checks the addendum; no engine is needed.
2. **Engine-free implementation check that the fixes are real:** a dry aggregator run over a
   synthetic 20-game JSONL containing (i) one torn line, (ii) one wrong-hash game, (iii) one
   duplicate id — the aggregator must FAIL all three with the named conjuncts. Buildable and
   runnable today; F-0002 does not block it.
3. **Colour-conditional score** reported by `tools/e0011_check.py` against the measured prior
   (58.5 % White; k6 cells 0.783/0.542), as a diagnostic with a named action, never a gate.

## Verdict

**NOT CLEAN — three blocking findings (B1, B2, B3); E-0011 stays PENDING.** The pre-registered
rule is sound where it speaks (tier mapping, no Elo gate, dedup key, crash rule, salt
separation, volume/cost — each attack surface from HO-0003 that is not named above held for the
reason recorded under Agreements), and two of its flagged assumptions survive a measurement
against retained evidence. What the record lacks is the *enforcement surface* for the one claim
that carries the most downstream risk ("fresh games" for Q-0006) and *resume semantics* for the
artifact it exists to produce. All three fixes are text-level; none changes a threshold, a tier,
or an N — so no re-derivation of DEC-0010 is required, and W-0001 step 2 (build) is unblocked
by the critique only insofar as the author lands the addendum (and F-0002 remains the execution
blocker).

## Date

2026-09-22

> A review never edits the original report — it lives here and is linked from the debate/report
> it concerns.

## Evidence appendix (my own runs this session)

1. `python research/scripts/research.py validate` → **exit 0**, "Validation OK … 0 problems"
   (warnings only). Notably it lists `RUN-0001` as a dangling id (N7).
2. `python research/context/w0005_sprt_replay.py` → **exit 0**; k6n totals W=144 D=30 L=66;
   duplicate-move-lists = 0 on all six rungs (independent of E-0011's future aggregator).
3. Ply/yield measurement (scratch script, `%TEMP%\krev10\measure_plies.py`; inputs = the six
   `e0010_k*n_games.jsonl`, k6n SHA-256 `9da1cfa0cb24ed94cf4a64ad47c0fed9387b5a3163b590153677e61c1fd0d227`
   — matches the pin in E-0012) → printed:
   `ALL RUNGS: games=1240 total plies(positions recorded)=161615`,
   `mean plies/game=130.3 median=117 p10=57 p90=243 max=290`,
   `implied positions for 1,000 games at the measured mean: 130335`.
   Reproduce with: read each `san` list and take `len`; `end` counts give 72 `plycap` games.
4. Quiet-position proxy (`%TEMP%\krev10\quiet_yield.py`): skip a ply if the emitted SAN contains
   `x` or ends `+`/`#`, or if the previous move left the mover in check; skip the first 10 plies →
   `positions total = 161615`, `quiet, opening skipped = 95340 (59.0%)` ⇒ 76,887 per 1,000 games.
5. Colour-conditional score (`%TEMP%\krev10\color_score.py`): `ALL: white 725.5/1240 = 58.51 %`;
   cross-tab (`%TEMP%\krev10\crosstab.py`) k6: `a_white=True: n=120 A-wins=86 B-wins=18 draws=16
   A-score=0.783` / `a_white=False: n=120 A-wins=58 B-wins=48 draws=14 A-score=0.542`.
6. Arithmetic: `1.96*371/sqrt(1000) = 22.99` (23.0); salt separation
   `|20260922-20260914|*1000003 = 8000024`.
7. Gate 0: one attempt, Device Guard block, no process — appended to
   `research/context/bootstrap/gate0.txt` (attempt #7, capture `gate0_session_run.txt`).

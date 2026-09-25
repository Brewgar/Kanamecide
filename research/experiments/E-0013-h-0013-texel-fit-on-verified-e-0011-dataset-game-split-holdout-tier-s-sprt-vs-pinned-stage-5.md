---
id: E-0013
type: experiment
title: "E-0013 — H-0013 Texel fit on the verified E-0011 dataset (game-split holdout + Tier-S SPRT vs pinned stage 5)"
status: PENDING
result: null
elo_change: null
hypothesis: H-0013
priority: high
owner: null
pre_registered: 2026-09-26
example: false
created: 2026-09-26
completed: null
tags: [texel, tapered-eval, pre-registration, holdout, sprt]
---

# E-0013 — H-0013 Texel fit on the verified E-0011 dataset (PENDING pre-registration)

> Filed by researcher-architect, 2026-09-26. **Nothing has run. `status: PENDING`.**
> No position extraction, fitting, binary build, or measurement game may start from
> this record until adversarial-reviewer critique (HO-0013) is CLEAN or every
> blocking finding is discharged, and the record is explicitly flipped to RUNNING.
> This record mirrors the E-0012 contract pattern: Provenance, Sample Validity,
> Pre-Registered Decision Rule, and Power And Sample Size are all populated BEFORE
> any running. `tools/e0012_sprt.py` is CITED, never edited, by this record.

## Hypothesis

Texel-tuning the hand-tuned tapered eval coefficients (H-0013) on quiet positions
extracted ONLY from the HO-0009/R-0017-verified E-0011 1,000-game dataset produces
a fitted parameter artifact that (a) improves game-result prediction on a
game-split holdout relative to a frozen pre-fit floor, and (b) passes a live
DEC-0010 Tier-S SPRT against the pinned stage-5 binary on fresh games. A good
holdout correlation alone is NOT a strength claim; the harness decision is.

## Baseline

- Eval: `src/eval.{h,cpp}` at HEAD `7348f89` (assumed — verify at execution
  preflight), `EvalCoeffs` as declared in `src/eval.h`, taper
  `score = (mg * phase + eg * (24 - phase)) / 24` with `GAME_PHASE_MAX = 24`.
- Stage ladder reference: E-0010 per-term ladder vs stage-0 (N=240): k1 +36.3,
  k2 +82.3, k3 +104.5, k4 +100.8, k5 +127.6, k6 +116.1. Stage 5 is the
  strongest measured rung, hence the SPRT opponent below.
- Comparison harness: `tools/e0012_sprt.py` (E-0012 COMPLETED/PASS, W-0005 DONE,
  VERIFIED by R-0018). DEC-0010 tiers: S [0,+20], R [0,+5], M [M-50,M];
  alpha=beta=0.05; LLR bounds +/-2.944; post-cap INCONCLUSIVE. Scope ruling
  stands: E-0012 licenses no engine-strength claim; any fitted-vs-pinned result
  is decided by its own pre-registered run under this contract.
- Dataset: R-0017-VERIFIED E-0011 replacement dataset
  (`m0_audit/e0011/games.jsonl`, 1,000 rows, SHA-256
  `27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95`;
  generator commit `7b1dda15f675b884a8bf971eec4b53a0fdf2049f`; binary
  `504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa`).
  Consumable ONLY under W-0001's leakage contract: distinct salt,
  train/holdout split BY GAME, overlap-0 gate. Attempt-1 stays excluded.

## Candidate

A fitted `EvalCoeffs` artifact (`fitted_params_sha256`, to be manufactured and
pinned at execution) loaded into a candidate binary built from the same pinned
`src/` commit, compared against the pinned stage-5 binary on fresh games.

## Difference

Fitted coefficients vs hand-tuned coefficients. No search, movegen, TT, UCI, or
time-control change is permitted between the arms; arm differentiation is by the
loaded parameter artifact alone.

## Hardware

Single host, CPU only, at most 2 engine pairs concurrent (E-0010/E-0011/E-0012
precedent).

## Engine Version

Pinned at execution preflight (binary SHA-256, `src/` commit, compile flags
recorded per game). The two arms differ ONLY in the loaded eval parameters
(fitted artifact vs pinned stage-5 hand-tuned artifact).

## Network

N/A (classical eval; no network).

## Dataset

### Source (frozen)

- ONLY `m0_audit/e0011/games.jsonl` (1,000 rows, SHA-256 pinned above).
- Failed attempt-1 excluded; no external labels exist and none are licensed
  (H-0013's 2026-09-09 "~50k quiet Stockfish-labeled FENs" text is NOT the data
  of this experiment — see Open Questions P0/P1; H-0013 itself is NOT reworded
  by this record).

### Quiet-position filter (EXECUTABLE predicate spec)

Positions are derived by replaying each game's `opening` + `san` plies
(E-0011 N4 semantics: `san` = post-opening engine moves only; dedup key
`tuple(opening) + tuple(san)`). For each reached position P (before the move
played), in python-chess terms:

```
QUIET(P) := (not board.is_check())
            and ("x" not in san_played)
            and (not san_played.endswith("+") and not san_played.endswith("#"))
            and (board.fullmove_number * 2 + (0 if board.turn == WHITE else 1) - 1) >= 10
```

This is the `tools/e0011_check.py` quiet-proxy predicate, promoted here to the
normative extraction filter (opening-skipped quiet proxy). Additions pinned:
check-state tested on the position BEFORE the move (mirrors the checker);
positions from games with `end == "crash"` are EXCLUDED (no trustworthy label);
degenerate games (`end == "mate"` with `len(san) <= 6`) are EXCLUDED.

Expected yield (measured, not assumed): the terminal checker diagnostic on the
verified dataset reports `san_position_yield=120930`,
`quiet_proxy_opening_skipped=76593`, `duplicate_positions=1705` /
`total_positions=130930`, `fit_scope=all-terms`
(`m0_audit/e0011/check_output.txt`). Extraction therefore starts from ~76.6k
quiet-proxy positions before dedup/split; the extractor MUST report realized
counts (extracted / deduped / train / holdout) and the run FAILS the scope gate
below if the realized usable yield falls under the floor.

### Labels (OPEN — designer-blocking; see Open Questions Q-LABEL)

Primary label (recommended, confidence: medium): game result from the source
row (`res` A/B/D mapped to 1/0/0.5 from White's perspective at the position's
side to move — exact mapping code pinned at execution), because it is the only
label source present in the verified dataset. Search-depth blend is NOT
available (no search scores were recorded in E-0011). The critique round
(HO-0013) must rule whether result-only labels suffice or the experiment is
INCONCLUSIVE-by-design for lack of labels.

### Split discipline (leakage contract, blocking)

- Split BY GAME with a distinct split salt `SPLIT_SALT = 20260926`
  (distinct from E-0010 `20260914`, E-0011 `20260922`, E-0012 live `20260924`;
  distance citations computed at execution).
- Assignment: `random.Random(SPLIT_SALT * 1000003 + game_id)` draw per game;
  80% train / 20% holdout (by game). The game_id->split map (with its SHA-256)
  is committed BEFORE any fitting job reads the data (hash logged in the RUN
  record first).
- Overlap-0 gate (blocking): normalize every holdout position's source game as
  `tuple(opening) + tuple(san)` and assert zero intersection with the train
  game set; assert additionally that no holdout FEN (normalized, side-to-move +
  piece placement + castling/EP rights) appears in the train set
  (threefold-cluster/position-relative leakage check). Any violation =
  FAIL before fitting.
- Per-game position cap: none beyond the quiet filter (cap = all quiet
  positions; dedup exact-FEN within the extraction before the split counts are
  reported). If the critic requires a cap, it must be named in critique and
  landed as an addendum BEFORE running — never silently.

## Free-parameter set (EXACT — nothing else may move)

Taper/phase-interpolation scheme (pinned formula; closes H-0013's un-pinned gap):

```
phase = min(1*N + 1*B + 2*R + 4*Q, 24)   # non-pawn material, both sides
score = (mg * phase + eg * (24 - phase)) / 24
```

(`src/eval.cpp`: `GAME_PHASE_MAX = 24`; phase weights N=B=1, R=2, Q=4; the
formula itself is NOT fitted — the phase weights are frozen integers.)

Fitted (all scalars inside `EvalCoeffs`, `src/eval.h`):

1. `mg_value[6]`, `eg_value[6]` — tapered material (KING entries fixed at
   20000/20000, NOT fitted).
2. `mg_pst[6][64]`, `eg_pst[6][64]` — all six MG/EG piece-square tables
   (KING PST rows are fitted ONLY as symmetry-preserving pairs: any fitted
   KING PST entry must satisfy `pst[s] == pst[mirror(s)]` under `s ^ 56`
   or the symmetry gate FAILS; recommended: freeze KING PSTs, fit the other
   five piece tables — final choice pinned at execution preflight from this
   list, no other scope permitted).
3. `doubled_pawn_mg/eg`, `isolated_pawn_mg/eg`, `passed_pawn_mg[8]/eg[8]`.
4. `mobility_mg/eg`.
5. `bishop_pair_mg/eg`, `open_file_mg/eg`, `semi_open_file_mg/eg`,
   `seventh_rank_mg/eg`, `king_shield_mg` (MG only), `king_center_eg`
   (EG only).
6. `tempo` (single scalar; side-to-move-signed per the E-0010 symmetry fix —
   the sign convention is NOT fitted).

Frozen (may not change): phase weights, `GAME_PHASE_MAX`, FLAT_VALUE staging,
mirror convention (`s ^ 56`), tempo sign convention, all search/UCI/TC code.

Scope floor: if realized usable quiet yield < 30k positions, the fit is scoped
to the mobility/tempo subset E-0010's ladder motivates (E-0011 N1 consequence
ladder, cited) and NO all-terms refit claim may be made. The scope decision is
a function of the measured yield only.

## Fitting method (OPEN — designer-blocking; see Open Questions Q-FIT)

Recommended pick (confidence: medium): logistic-regression Texel
(minimize mean logistic loss of sigmoid-predicted score vs game-result label
with L2 regularization; full-batch L-BFGS or deterministic mini-batch gradient
descent with a pinned seed). Alternative: SPSA on holdout loss. The critique
round (HO-0013) must rule on the method; whatever is adopted is landed as a
dated addendum with optimizer, seed, regularization, iteration budget, and
deterministic-rerun policy BEFORE running — no silent choice after seeing data.

## Test Method

1. Preflight: Gate 0 (`build/Release/kana.exe` → `=== ALL TESTS PASSED`);
   `research.py validate` exit 0; binary/src/compile-flag pins recorded;
   dataset SHA-256 re-verified; extractor command + dependency versions
   (Python, python-chess, optimizer library) recorded.
2. Extract quiet positions per the predicate; report realized counts.
3. Commit the game-split map hash BEFORE fitting; run the overlap-0 gate
   (blocking).
4. Fit ONLY on train (method per addendum after critique); pin
   `fitted_params_sha256`; deterministic-rerun check (refit with the same seed
   reproduces the artifact hash or the run FAILS).
5. Holdout evaluation (stage a): compute holdout logistic loss / MAE for the
   fitted vs hand-tuned parameters on the SAME frozen holdout (paired).
6. Quality-conservation gates: 1000-position symmetry re-run (full-mirror
   violations = 0); NPS cost band (see Decision Rule); illegality = 0.
7. Strength gate (stage b): fresh-game SPRT via UNMODIFIED
   `tools/e0012_sprt.py` (fitted-params arm = A vs pinned stage-5 arm = B),
   fresh salt distinct from ALL prior salts, opening protocol per DEC-0010,
   `training_game_overlap = 0` reported under the pinned normalization
   `tuple(opening) + tuple(san)` against the E-0011 dataset before the
   decision is read. NEVER fitted build vs itself (W-0001 stage-6
   self-collision lesson).
8. Tactical-suite clause: per the golden/spot-check rule in the Decision Rule.

## Games / Samples

- Train/holdout: ~76.6k quiet-proxy positions expected (measured pre-split
  diagnostic), 80/20 BY GAME → ~61k train / ~15k holdout pre-dedup (assumed
  arithmetic from the measured 76593 — verify at execution; realized counts
  govern).
- SPRT: DEC-0010 Tier S, zone [0,+20] Elo, LLR bounds ±2.944
  (alpha=beta=0.05), cap 2,000 games. The cap is sized by the REAL time
  budget: E-0010 measured ~769 games/h at 2 pairs; the E-0012 live pair ran
  365 games in one evening session (RUN-0002/RUN-0003 timestamps — verify at
  execution); 2,000 games ≈ 2.6–3 h. A wider zone or larger cap is NOT
  authorized without a new power addendum.
- Golden/tactical suite: an INDEPENDENT tactical suite of at least N=200
  positions (pre-registered FEN list with hash, committed before fitting) OR a
  sufficient-N spot check — a cherry-picked suite is a rort at small N. The
  suite list (or the increased-N justification) is committed before fitting.

## Metrics

- Holdout logistic loss (fitted vs hand-tuned, paired on the frozen holdout).
- Holdout MAE overall + by game phase (phase-value tertiles; boundaries pinned
  at execution preflight).
- SPRT LLR/crossing/verdict (Tier S) from the unmodified harness.
- Eval NPS cost (bench, uncontended, same protocol as E-0010 gate (d)).
- Symmetry violations (1000 positions, full-mirror).
- Legality/duplicates on fresh games (0 tolerance for illegal; duplicates
  reported, harness-run validity per E-0012 rules).
- All hashes: dataset, split map, fitted params, candidate/pinned binaries.

## Pre-Registered Decision Rule

> MANDATORY. One decision rule, written here FIRST. PASS requires every
> conjunct. No rule may be added after the run starts. INCONCLUSIVE is an
> honest verdict where named; anything else that fails is FAIL, never
> "baseline preserved" (HO-0008 anti-apathetic-failure lesson: no achievement
> = FAIL).

PASS requires ALL of:

- (a) **Scope/yield gate:** realized usable quiet yield reported; if < 30k,
  scope reduced to mobility/tempo subset (E-0011 N1 ladder) and the all-terms
  claim is WITHDRAWN (recorded, not silently kept).
- (b) **Leakage gate (blocking):** split map hash committed before fitting;
  train/holdout BY GAME with `SPLIT_SALT = 20260926`; overlap-0 holds at both
  game level (`tuple(opening)+tuple(san)`) and normalized-FEN level. Violation
  = FAIL before fitting.
- (c) **Holdout-loss gate (stage a):** fitted holdout logistic loss beats the
  frozen hand-tuned floor by at least the pre-registered margin
  `LOSS_MARGIN = 0.002` (paired, same frozen holdout), AND the paired
  difference's 95% CI (paired t over holdout games, clustered BY GAME)
  excludes 0. No achievement = FAIL (anti-apathetic clause). A CI that
  includes 0 = FAIL, not INCONCLUSIVE (the holdout N is large; power is not
  the binding constraint here).
- (d) **Quality-conservation gates:** 1000-position full-mirror re-run shows
  0 violations (E-0010 gate-(b) discipline); NPS cost within the pre-registered
  band (fitted binary within 10% of the pinned binary on the uncontended
  `--bench` protocol; regression beyond -10% = FAIL); 0 illegal moves in any
  fresh-game campaign (0 tolerance).
- (e) **Strength gate (stage b, Tier-S SPRT):** fitted arm (A) vs pinned
  stage-5 arm (B), Tier S [0,+20], bounds ±2.944, cap 2,000, fresh salt,
  `training_game_overlap = 0` reported BEFORE the verdict is read. H1 inside
  the cap = PASS for this conjunct; H0 = FAIL (the fitted eval is rejected);
  post-cap no-crossing = INCONCLUSIVE for this conjunct (power honesty: at a
  true +5 the Tier-S zone is INCONCLUSIVE-by-design within 2,000 games; the
  experiment then ends INCONCLUSIVE, never "baseline preserved").
- (f) **Tactical-suite gate:** INDEPENDENT suite (N>=200, hash-committed
  pre-fit) shows no regression vs the pinned arm beyond the pre-registered
  tolerance (exact tolerance + metric pinned with the suite list before
  fitting), OR the suite is replaced by a same-N independent spot check with
  identical discipline. A cherry-picked small-N suite = FAIL of this conjunct.
- (g) **Replay acknowledgement + mitigation:** the SPRT run logs the fixed-seed
  opening-book hash (salt + per-game seed derivation) and runs a paired-colour
  analysis (A-score as White vs as Black reported separately). The record
  states verbatim: "the 125-vs-179 replay crossing delta is unexplained per
  R-0018 Q4 and is treated as sampling variation, not a settled harness
  property." Claiming the harness is settled = FAIL of this conjunct.
- (h) **Scope honesty:** no engine-strength overreach beyond the Tier-S zone
  (E-0012 scope ruling inherited: a Tier-S H1 licenses "worth keeping", never
  a Tier-R "stronger" or Tier-M magnitude claim).

OVERALL: PASS iff (a)-(h) all PASS. Any (c)/(d)/(e-H0)/(f)/(g)/(h) failure =
FAIL. Post-cap (e) no-crossing with all else PASS = INCONCLUSIVE. Any
threshold, salt, cap, suite, or margin changed after seeing data = FAIL
(p-hacking tripwire).

## Power And Sample Size

> MANDATORY. "What N settles this rule?"

- **Stage (a) holdout loss:** holdout N approx 15k positions / ~200 games
  (assumed arithmetic — verify at execution). A paired loss margin of 0.002
  with game-clustered SE is decidable at this N for any realistic loss
  variance; if the realized holdout SE cannot separate 0.002 from 0, the
  margin (not the N) was aspirational — shrink the claim per HO-0013 ruling
  question (v), never silently weaken the band. Therefore stage (a) IS
  decidable at the planned N unless the realized variance proves otherwise,
  in which case the verdict is FAIL (apathetic-fit rejection), not
  INCONCLUSIVE.
- **Stage (b) Tier-S SPRT:** DEC-0010 ASN at Tier S approx 1,820 games under
  H1 (+20 edge), ~2,025 under H0, ~4,050 near the midpoint; cap 2,000 at
  ~769 games/h approx 2.6 h (E-0010 measured throughput; E-0012 live ran 365
  games in one evening session). The honest shape: a true +20 effect decides
  inside the cap; a true +5 effect does NOT (INCONCLUSIVE-by-design at cap
  2,000 — the Tier-R claim needs ~29-32k games / ~39 h, a round-boundary
  campaign, not this experiment). Power is WEAK for small effects and the
  contract says so. Therefore stage (b) is decidable at the planned N ONLY
  for screening-size effects (>=+20); anything smaller ends INCONCLUSIVE by
  design.
- **Tactical suite:** N>=200 independent positions; tolerance pinned with the
  suite. A smaller suite is INCONCLUSIVE-by-design for this conjunct.

## Sample Validity

- **Arm differentiation:** the two SPRT arms load different pinned parameter
  artifacts (fitted `fitted_params_sha256` vs hand-tuned stage-5 artifact
  hash); the execution records MUST dump the effective loaded hash from both
  engines' handshake/startup log and assert A != B. Same-hash arms = FAIL.
- **Independence:** fresh openings per game index from a fresh salt
  (deterministic function `random.Random(fresh_salt * 1000003 + game_index)`,
  E-0011/E-0012 precedent); strict colour alternation; duplicate-move-list
  count reported (E-0012 validity rules apply); `training_game_overlap = 0`
  against the pinned E-0011 dataset under `tuple(opening)+tuple(san)`.
- **Provenance:** binary SHA-256s (candidate + pinned stage-5), `src/` commit,
  compile flags, extractor + fitter commands with dependency versions
  (Python, python-chess, optimizer library), seeds/salts, host facts, raw
  evidence paths (local, gitignored), aggregator command reproducing every
  number. Tool versions recorded, not assumed.

## Provenance

- Dataset SHA-256: `27ea181d32a9025e0fd9cea150540b6598ce7e608bc96ca245d7c07b7ac5bb95`
  (`m0_audit/e0011/games.jsonl`, 1,000 rows; R-0017 VERIFIED).
- Generator binary: `504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa`;
  generator commit `7b1dda15f675b884a8bf971eec4b53a0fdf2049f`.
- Pinned `src/` commit for the fit campaign: HEAD `7348f89` (assumed — to be
  verified and re-pinned at execution preflight; any rebuild re-pins BEFORE
  game 1 per E-0011 B3.1 discipline).
- Harness: `tools/e0012_sprt.py` UNMODIFIED (E-0012 COMPLETED/PASS, R-0018
  VERIFIED). No edit permitted by any seat during this experiment.
- Split salt: `20260926` (distinct from 20260914/20260922/20260924).
- `fitted_params_sha256`: TO BE MANUFACTURED (not fabricated here).
- Raw evidence paths (local, gitignored): to be recorded at execution.
- Aggregator command reproducing every number: to be recorded at execution
  (same discipline as E-0011/E-0012: command → exit code → path → hash).

## Open Questions (designer-blocking — decide in critique, NOT silently)

- **P0/P1 — the H-0013 dataset discrepancy (deliberate finding):** H-0013's
  2026-09-09 text assumes "~50k quiet Stockfish-labeled FENs". No external
  labels exist and none are licensed; the real data is the E-0011 dataset
  (~76.6k quiet-proxy positions pre-split per the measured diagnostic above —
  the "~27k quiet positions post-filter per W-0001's done-report" figure in
  the session brief is UNVERIFIED against the on-disk checker diagnostic and
  is NOT adopted here; the checker's measured 76593 governs until a verifier
  rules otherwise). OPTION P0: amend H-0013's text (hypothesis lifecycle
  change — out of scope for this session; needs its own decision). OPTION P1
  (adopted by THIS record): file the experiment against the E-0011 dataset
  with the holdout-loss band above (margin 0.002 + paired CI) instead of the
  brief's suggested ±0.10 band (the ±0.10 band has no power derivation behind
  it and is rejected here as aspirational). Critic: rule P0 vs P1 sequencing.
- **Q-LABEL — label source:** game result only (recommended, the only label
  present in E-0011) vs result + search-depth blend (NOT available — no search
  scores in E-0011; would require a new data campaign). Confidence: medium
  that result-only suffices for a screening claim; LOW for a Tier-R claim
  (stated so the critic can shrink the claim).
- **Q-FIT — fitting method:** logistic/gradient Texel (recommended, medium
  confidence) vs SPSA (alternative). State the pick in critique; land it as a
  dated addendum with optimizer/seed/regularization/budget BEFORE running.
- **Q-SCOPE — KING PSTs:** freeze (recommended) vs symmetry-constrained fit.
  Rule in critique.
- **Q-SUITE — tactical suite identity:** which INDEPENDENT suite (list + hash)
  or what increased-N spot-check design. Rule in critique.

## Results

TBD — nothing has run. This section will be filled with aggregator output +
pinned hashes only, never narrative.

## Statistical Analysis

TBD. (No inferential statistics are permitted here beyond the pre-registered
paired-CI and SPRT LLR rules above.)

## Interpretation

TBD.

## Conclusion

TBD.

## Follow-Up

- Adversarial-reviewer critique (HO-0013) BEFORE `status: RUNNING`.
- A FAIL on any blocking gate routes to `research/failures/` and blocks
  promotion of the fitted artifact.
- H-0013 and H-0010 status changes are EXPLICITLY out of scope for this record
  (needs their own decisions; the H-0010 status review stays sequenced AFTER
  this contract survives critique, per HO-0013 question (vi)).

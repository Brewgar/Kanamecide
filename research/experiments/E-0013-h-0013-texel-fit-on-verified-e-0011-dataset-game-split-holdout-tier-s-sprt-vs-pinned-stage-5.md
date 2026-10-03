---
id: E-0013
type: experiment
title: "E-0013 — H-0013 Texel fit on the verified E-0011 dataset (game-split holdout + Tier-S SPRT vs pinned stage 5)"
status: RUNNING
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

---

## Addendum: R-0019 discharge (B1-B7), BUCKET-3 branch decision, and freeze-audit closure - 2026-09-26

> Filed by researcher-architect, 2026-09-26, in response to R-0019 (HO-0013 receiver,
> adversarial-reviewer), verdict **NOT CLEAN / BLOCKING**, seven findings B1-B7.
> **PURE ADDITIONS.** Nothing above this line is edited, deleted or reworded. Where this
> addendum supersedes an existing sentence it QUOTES that sentence verbatim and names
> the supersession. E-0013 remains `status: PENDING`; this addendum does not flip it.
> **Nothing has run.** No training, fitting, extraction, counting, feasibility pass or
> SPRT game generation was performed to produce this text, and no fitted parameter
> artifact exists.
>
> **Discipline note on this addendum's authority.** `tools/e0012_sprt.py` and every
> engine source file are CITED here and were not touched. E-0011, E-0012, W-0001,
> W-0005, RUN-0002/RUN-0003 and R-0017/R-0018 are CLOSED or VERIFIED records and are
> NOT edited by this addendum; where a finding concerns text inside one of them, the
> correction is recorded HERE as a dated correction note plus a follow-up obligation
> (see B5 and the Follow-Up section), never as an edit to that record.

> **REPAIR NOTICE (2026-09-26, under R-0020's licence).** Review found THIS ADDENDUM to be
> a truncated, interleaved document and it has been REPAIRED IN PLACE: ten severed
> sentences re-joined as contiguous text, one absent continuation supplied (X1-a), the
> X-1/X-2/X-3 contingency table moved under B3 sentence 3, the follow-up obligations
> re-joined into one list, one false clause replaced with its arithmetic (X2), and
> disposition rows for X1 and X2 added to the table below. The addendum is therefore NOT
> purely additive TO ITSELF, and the 'PURE ADDITIONS' line above governs only what lies
> ABOVE this addendum. Nothing in the ORIGINAL pre-registration (L1-L428) has been edited,
> and that is provable by hash, not by assertion - see the dated repair section at the end
> of this record. No decision was re-opened; E-0013 remains `status: PENDING`.

### Adopted rulings carried into this addendum (from R-0019, unchanged by me)

| Ruling | Disposition here |
|---|---|
| P0 / P1 | **P1 adopted** (fit against the E-0011 dataset). **P0 stays deferred** to a researcher-architect decision record filed no later than E-0013 close-out (Follow-Up obligation F-U1). H-0013's text is NOT amended by this addendum. |
| Q-LABEL | **result-only adopted**, with the colour-frame amendment (B2) and an explicit "attainable gain unmeasured" acknowledgement. |
| Q-FIT | **deterministic full-batch L-BFGS adopted; SPSA withdrawn as a leakage channel** (B4). |
| Q-SCOPE | **all-terms, KING PSTs FROZEN** (B5). |
| Q-SUITE | **independent suite adopted; the substitution path is CLOSED** (B4). |
| Per-game position cap | **ruled NONE** (B4). Closed, not re-openable. |

### How the findings are sorted (stated up front, so the disposition table is auditable)

- **BUCKET 1 - discharged by addendum text in this document:** B1 (as a branch
  DECISION, below), B2 sentence 1 + the unmeasured-gain acknowledgement, B3
  sentences 1-2 + the contingency decided now, B4 sentences 1-3 + the pinned suite
  tolerance + the freeze anchor, B5 sentences 1-2, B6's rule text, B7, the whole
  F1-F12 freeze-audit gap, and the ten doc-nits (non-blocking).
- **BUCKET 2 - PRE-REGISTERED, NOT RUN.** Two measurement passes, filed as their own
  PENDING records with their own inputs, pre-registered output fields and abort
  conditions: **E-00014** (train-only feasibility pass; the measurement half of B2/B3)
  and **E-00015** (count-only realized-yield pass; the measurement half of B6). They
  are executed by another seat under **HO-0015** and **HO-0016**.
- **BUCKET 3 - BRANCH DECISION, stated with its cost:** B1. Decision: **SHRINK.**
  Its cost, stated rather than netted against the benefit, is B1's cost items 1-4 above:
  H-0013's second limb is left **UNANSWERED** by this run, the B1 defect is **deferred, not
  dissolved** (obligation F-U2), and a UCI parameter-hash surface is
  **considered-and-rejected** with its reversal condition named. No strength claim is
  licensed by this decision, and the decision may not be re-opened after the holdout is
  read.

---

### B1 - BRANCH DECISION: **SHRINK** (option (i)), with its cost written down

**The problem, in the record's own words.** Three existing sentences are mutually
unsatisfiable and are quoted verbatim as the text being superseded:

> (D-1, Difference section) "No search, movegen, TT, UCI, or time-control change is
> permitted between the arms; arm differentiation is by the loaded parameter artifact
> alone."

> (S-1, Sample Validity) "the execution records MUST dump the effective loaded hash
> from both engines' handshake/startup log and assert A != B. Same-hash arms = FAIL."

> (P-1, Provenance) "Harness: `tools/e0012_sprt.py` UNMODIFIED (E-0012 COMPLETED/PASS,
> R-0018 VERIFIED). No edit permitted by any seat during this experiment."

S-1 is unachievable with the cited surface, for reasons R-0019 verified and which I
re-verified read-only this session: `tools/e0012_sprt.py:325-326` constructs BOTH
engines from the single `--exe` and differentiates only by an integer
`setoption name EvalStage value K`; line 301 records one `binary =
sha256_file(Path(args.exe).resolve())` for both arms; `parse_args` (lines 474-487)
exposes one `--exe` and integer `--stage-a/--stage-b`; `src/main.cpp:103-114` advertises
and accepts only `Hash` and `EvalStage`; `src/main.cpp:133-147` parses and applies every
`(key, value)` pair but **emits no echo and no parameter hash**; and `EvalCoeffs` is a
compiled-in static initialized in `src/eval.cpp:174-234` with no runtime loader.
`--stage-a 5 --stage-b 5` is therefore the W-0001 stage-6 self-collision this record
names and forbids, and `--stage-a 6 --stage-b 5` compares the hand-tuned eval against
itself minus tempo.

**Cost, stated honestly and not netted against the benefit.** SHRINK is not free:

1. **H-0013's second limb goes untested by this run.** The Hypothesis sentence "(b)
   passes a live DEC-0010 Tier-S SPRT against the pinned stage-5 binary on fresh games"
   is not exercised here. The run's licensed claim is the limb (a) claim only, and the
   strength question is recorded as **UNANSWERED** - not as NEUTRAL, not as
   INCONCLUSIVE (INCONCLUSIVE is reserved for a run that executed and did not cross),
   and never as "baseline preserved".
2. **SHRINK defers the B1 defect; it does not dissolve it.** The deferred strength
   contract faces the identical one-`--exe` wall. Its minimum viable shape is named now
   so the deferral is not a blank cheque: **two distinct compiled binaries**
   (coefficient-regenerated vs pinned), differentiated by the harness's own
   `sha256_file` per arm, which requires a minimal two-`--exe` change to
   `tools/e0012_sprt.py` filed as its own E-0012-style contract with its own
   pre-registration, its own critique and its own validation, under a new, separately filed E-0012-style contract whose id is CLI-assigned at filing (Follow-Up
   obligation F-U2). A harness contract is not a strength claim and licenses none.
3. **A UCI parameter-hash surface is explicitly NOT adopted, with the reason.** A
   runtime `id name` parameter-hash line is an engine change with Gate 0 implications
   (rebuild, perft re-anchor, `EVAL_STAGE` default re-check) and, on this analysis, buys
   no decision value that the per-binary file hash does not already provide once two
   binaries exist. Adopting it by default would be paying Gate-0 cost for redundancy.
   It is recorded as considered-and-rejected, with the condition that would reverse the
   decision: if the deferred contract elects a single binary with a runtime loader
   instead of two binaries, the parameter-hash surface becomes mandatory and the loader
   plus the surface must be pre-registered and critiqued before any strength game.
4. **What SHRINK does buy, stated as the benefit, not as an argument.** The unexecutable
   mandate is removed rather than re-pointed; no `src/` change and no harness change is
   needed for THIS run; the coefficient-regeneration mechanism it needs already exists
   and was used to produce E-0010's rungs; and no fitted artifact can be mistaken for a
   strength result, because this run never produces one.

**B1 sentence 1 (the mechanism that actually replaces S-1), as the mechanism in force:**

> "**Arm differentiation mechanism for this record (supersedes S-1).** This record runs
> NO two-arm game campaign, so no UCI handshake hash is required, claimed or dumped,
> and S-1 is superseded rather than re-aimed at an instrument that does not exist. The
> two arms of the holdout comparison are two PARAMETER TABLES, not two engines, and
> they are differentiated inside the offline evaluator, which (i) prints `sha256` of the
> fitted parameter table actually loaded for the fitted arm and `sha256` of the
> hand-tuned table actually loaded for the floor arm, (ii) asserts the two hashes
> DIFFER before any holdout loss is computed, and (iii) records both hashes, the two
> artifact paths, and the SHA-256 of the coefficient-regeneration output that produced
> the candidate's coefficient block. The candidate binary used for the
> quality-conservation gates is produced by the EXISTING E-0010 coefficient-regeneration
> mechanism (a pinned coefficient block substituted into the eval translation unit and
> a normal rebuild - the same mechanism that produced rungs k1..k6), NOT by a runtime
> parameter loader and NOT by any new UCI option; it adds no engine surface. The
> engine's UCI surface is unchanged and `tools/e0012_sprt.py` is UNCHANGED and UNUSED by
> this record. Same-hash arms = FAIL before any loss is read. The strength gate's
> `--validation-known` MUST NOT be passed on any run of the deferred contract:
> `tools/e0012_sprt.py:297-299` raises unless
> `(tier, stage_a, stage_b, cap) == (\"S\", 6, 0, None)`."

**B1 sentence 1 addendum (coefficient-regeneration scope; R-0020 nit N1, 2026-09-26) -
BINDING on the mechanism above:**

> **Coefficient regeneration substitutes the coefficient block ONLY.** It must not re-run
> a stage generator, because `write_eval_p5.py:87` emits the unsigned `score += C.tempo;`
> while the live `src/eval.cpp:356` carries the E-0010 side-to-move-signed fix, and
> regressing that line would break the colour-symmetry invariant that conjunct (d) gates
> on and that B2's side-to-move frame and DN10 both depend on. `write_eval_p5.py` and
> `src/eval.cpp` are CITED by this note and are NOT edited by it: this is a text note
> about a script, not a change to it.

**B1 sentence 2 (the stage index, which is load-bearing for gate (c)):**

> "**Stage index S\\*.** `S* = 6`, pinned HERE, in this pre-registration, and not at
> execution preflight. The training data was generated at `eval_stage_a == eval_stage_b
> == 6` (E-0011:309) and `src/eval.cpp:356` applies tempo only at `stage >= 6`
> (`if(stage>=6) sc += (b.side == WHITE ? C.tempo : -C.tempo);`), so S\\* = 6 is the only
> stage at which EVERY entry of the fitted set is read by the scorer. The stage-(a)
> offline metric and the hand-tuned floor are both computed at S\\* = 6; the pinned
> hand-tuned artifact is the compiled-in table of `src/eval.cpp:174-234` at the pinned
> `src/` commit. Consequence, stated so it cannot be discovered later: at S\\* = 6 the
> `tempo` entry IS read and IS scored, so `tempo` is NOT 'NOT SCORED at S\\*' and remains
> in the fitted set; conversely, a strength comparison against a stage-5 opponent would
> leave `tempo` inert, which is one of the reasons the strength comparison is deferred
> rather than run here (cost item 1 above). No claim about the fitted `tempo` value's
> playing-strength effect may be made by this record at ANY stage, because this record
> runs no games."

---

### B2 - Q-LABEL: the fit target's colour frame, and the label's attainable gain

**B2 sentence 1 (the colour frame - the sharp edge), verbatim per R-0019:**

> "**Fit target (side-to-move frame).** For a position whose side to move is s, the fit
> target is `y = white_score` if `s == WHITE` and `y = 1 - white_score` if `s ==
> BLACK`, where `white_score in {1, 0.5, 0}` is `res` mapped from White's perspective.
> Because the eval is required to be colour-symmetric (mirror `s ^ 56`; conjunct (d) 0
> full-mirror violations), a target expressed in the White frame for a Black-to-move
> position, or any mixture of the two frames across the dataset, is a **FAIL of conjunct
> (c)**. The extractor reports `label_frame_uniform = true` and its per-side-position
> counts before any fitting job reads the data. This supersedes the clause 'exact mapping
> code pinned at execution' by pinning the frame here; the mapping CODE is still written
> to the pre-fit commit, but the frame it implements is no longer a choice."

**B2 sentence 2a (the acknowledgement the record was missing - the attainable gain is
UNMEASURED, stated as a fact about this record, not as a hedge):**

> "**Attainable gain is unmeasured (acknowledgement, 2026-09-26).** The label is
> game-constant, so every position in a game carries the same target and the fit is
> learning a game-outcome classifier from position features, not a per-position value.
> The best any position scorer can do is bounded by the within-game spread of position
> quality among positions that share an outcome. That bound - the attainable gain - is
> **not measured by this record and no number for it is asserted anywhere in it**;
> 903 of 1,000 verified games end in `mate`, so the label is dominated by a single
> terminal class. Consequently 'holdout logistic loss improved' MUST NOT be read as 'the
> eval is a better evaluator', and no correlation or MAE figure from this record may be
> quoted as a quality figure. Whether the attainable gain exceeds `LOSS_MARGIN` is
> measured by E-00014 (train-only) and by nothing else."

**B2 sentence 2b (the feasibility pass itself is BUCKET 2 - pre-registered, NOT run
here; this is the rule that consumes its output):**

> "**Feasibility pass (non-training, pre-fit, TRAIN-ONLY) - delegated to E-00014.** The
> label is constant within a game. Before conjunct (c)'s margin binds, the
> pre-registered, **TRAIN-ONLY** feasibility pass E-00014 MUST measure, on a game-split
> inner partition carved from TRAIN and never touching the holdout: the attainable
> holdout-style loss improvement `delta_star` of the adopted optimizer over the
> hand-tuned floor under the adopted label construction, plus the per-game cluster SD
> `s_d`, each with its own pinned seed, iteration budget and regularization. E-00014's
> inputs, pre-registered output fields, abort conditions and executor seat are in that
> record; the executor is another seat under HO-0015. **This record does not run
> E-00014, does not estimate `delta_star` or `s_d` by any means, and does not read the
> holdout to obtain either quantity.** `LOSS_MARGIN := max(0.002, 0.5 * delta_star)`, so
> the margin can only be made more conservative than 0.002, never less. If `delta_star`
> cannot be measured because the optimizer does not beat the floor on the inner
> partition, the stage-(a) verdict is **INCONCLUSIVE-BY-DESIGN** and is labelled as
> such - never FAIL, and never 'no achievement = FAIL'."

---

### B3 - The 0.002 margin has no derivation, and the power justification offered for it is false

**B3 sentence 1 (effective N, and what the margin is actually conditional on), verbatim
per R-0019:**

> "**Effective N.** The holdout's independent units are the holdout **GAMES**, not the
> holdout positions: the label is game-constant, so the estimator is the mean over
> G ~ 200 games of the per-game mean paired loss difference, with `SE = s_d / sqrt(G)`
> on `t_{0.975, G-1}`. `LOSS_MARGIN = 0.002` is decidable at the planned N **iff `s_d
> <= 0.0101`** (`0.002 / (2.8016 / sqrt(200))`). `s_d` is a per-game SD of a paired
> difference and is not measured by this record. The clause 'for any realistic loss
> variance' is superseded by: 'decidable iff the B2 feasibility pass reports
> `s_d_inner <= 0.0101`; otherwise the margin is aspirational and the stage-(a) verdict
> is INCONCLUSIVE-BY-DESIGN, not FAIL'."

**B3 sentence 2 (the anti-apathetic clause, correctly scoped), verbatim per R-0019:**

> "**Anti-apathetic scope.** 'No achievement = FAIL' remains non-negotiable and is
> scoped to the fit's QUALITY, not to the measurement's POWER. A CI that includes 0
> because `s_d` exceeds the feasibility bound is a power INCONCLUSIVE; a CI that
> includes 0 at a feasible `s_d` is a FAIL. Both verdicts publish the measured `s_d`,
> `delta_star` and the holdout game count in the open, so a null result can never be
> restated as 'baseline preserved', nor as an apathetic-fit rejection it was not."

**B3 sentence 3 - THE CONTINGENCY, DECIDED NOW, BEFORE ANY NUMBER EXISTS.** This is the
part that must not be chosen after `s_d_inner` is known. Three mutually exclusive
outcomes of E-00014 are each assigned a named verdict NOW, by name, in this
pre-registration, with no discretion left to the session that reads the number:

> "**Contingency table for '0.002 is undecidable at the measured `s_d`'. DECIDED HERE,
> 2026-09-26, BEFORE E-00014 RUNS. The three branches are exhaustive and mutually
> exclusive on the two measured quantities; no fourth branch exists and no branch may
> be chosen later.**
>
> **(X-1) `s_d_inner <= 0.0101` AND `delta_star` measurable.** Then 0.002 is decidable
> and conjunct (c) is evaluated as written against `LOSS_MARGIN = max(0.002, 0.5 *
> delta_star)`. A CI excluding 0 at or above the margin = PASS of (c). A CI including 0
> = **FAIL of (c)** (anti-apathetic, quality-scoped). No INCONCLUSIVE is available in
> this branch.
>
> **(X-2) `s_d_inner > 0.0101` (the margin is undecidable at this dispersion) AND
> `delta_star` measurable.** The stage-(a) verdict is **INCONCLUSIVE-BY-POWER** - a
> named verdict, distinct from INCONCLUSIVE-BY-DESIGN, and it publishes the measured
> `s_d_inner`, `delta_star`, the inner-partition game count, and the achieved power at
> the 0.002 margin. It is **not** FAIL, because a power failure is not an apathetic fit;
> it is **not** PASS, and the margin is **not** widened to manufacture decidability. The
> fitted artifact may still be reported as PRODUCED, but the run's licensed claim is
> limited to 'a fitted artifact exists whose holdout loss difference was not separable
> from 0 at G ~ 200 with the measured dispersion', and conjunction (c) is recorded
> INCONCLUSIVE-BY-POWER. Follow-up obligation F-U3 routes X-2 to a named re-decision
> (either a larger holdout game count, or a paired design with lower `s_d`, or an
> explicitly widened margin with its own power derivation) under a NEW
> pre-registration - never by editing this one.
>
> **(X-3) `delta_star` NOT measurable, i.e. the adopted optimizer does not beat the
> hand-tuned floor on the inner partition.** Then the attainable gain is below the
> margin by construction and conjunct (c) is **INCONCLUSIVE-BY-DESIGN**, per B2
> sentence 2b. Never FAIL, never 'no achievement = FAIL', never a silent re-run with a
> different optimizer to obtain a measurable `delta_star`. The gate is **not weakened
> silently**: X-3 is a pre-declared dead end whose only exits are (a) a new
> pre-registration with a different label construction - which would require a new data
> campaign and is out of scope here - or (b) a FAIL of H-0013 recorded as such at
> E-0013 close-out. **The anti-apathetic clause is not weakened in any branch:** a fit
> that is measurably worse than the floor, or that ties it at a feasible `s_d`, is
> still FAIL under X-1."

---

### B4 - Q-FIT and the suite tolerance were OPEN, the named SPSA alternative leaked, and no deferred value was anchored

**B4 sentence 1 (Q-FIT adopted, SPSA withdrawn), verbatim per R-0019:**

> "**Q-FIT adopted.** Deterministic full-batch L-BFGS on the mean logistic loss of
> `sigmoid(clip(E_theta(p), -L, L))` against the B2 side-to-move-frame target, with an
> L2 penalty, a pinned seed, a pinned iteration budget, a pinned `L`, and a pinned L2
> weight. No hyperparameter - including the L2 weight, the iteration budget and any
> early-stopping point - may be selected on, or compared against, ANY holdout quantity;
> hyperparameters are selected on the game-split inner partition of TRAIN only. The
> clause 'Alternative: SPSA on holdout loss' is **withdrawn as a leakage channel**;
> SPSA is not an available option under this contract."

**B4 sentence 2 (the single pre-fit commit - the freeze anchor, closing F1-F6 and F10 at
once), verbatim per R-0019 with the anchor made explicit:**

> "**Single pre-fit commit (the freeze anchor).** Every value this record defers with
> 'pinned at execution' / 'pinned at execution preflight' / 'pinned with the suite' - the
> fresh SPRT salt, the salt-distance citation, the KING-PST scope choice, the MAE
> phase-tertile boundaries, the label-mapping code, the optimizer seed / L2 weight /
> iteration budget / clipping, the stage index S\\*, and the tactical-suite identity, N,
> metric and **TOLERANCE (a number, not a placeholder)** - is assigned ONCE and committed
> with its SHA-256 in the SAME pre-fit commit as the game-split map, and the holdout is
> not read before that commit exists. A value assigned for the first time after the
> holdout has been read is a tripwire FAIL exactly like a changed value; the existing
> clause 'Any threshold, salt, cap, suite, or margin changed after seeing data = FAIL'
> is extended by 'or assigned for the first time after the holdout is read'."

**B4 sentence 4 (the suite tolerance is a NUMBER here, not a placeholder - the single
most-cited OPEN in the record). Pinned value, with the reasoning that produced it:**

> "**Q-SUITE tolerance, pinned as a number: `SUITE_TOLERANCE = 0.02` (2.0 percentage
> points of the suite's primary metric).** The suite's primary metric is **solution
> rate**: the fraction of suite positions on which the engine emits a bestmove matching
> the suite's single pinned solution move, under the suite's pinned protocol (pinned
> search depth, pinned node cap, single-threaded, no opening book, one position per
> process invocation, both arms run with identical protocol; protocol pinned in the
> pre-fit commit). Rule: fitted arm solution rate `>=` pinned arm solution rate `- 0.02`,
> evaluated on the SAME N >= 200 suite positions in the SAME order with the SAME
> protocol; any regression worse than 0.02 = FAIL of conjunct (f). Secondary reported
> metrics (not gates): mean centipawn loss on the pinned bestmove, and solution rate by
> position class as listed in the suite manifest. **Why 0.02 and not something else:**
> at N = 200 the binomial standard error of a paired solution-rate difference is bounded
> by `0.5 / sqrt(200) = 0.0354`; a tolerance at or below the noise floor would make
> conjunct (f) a coin flip rather than a gate, and a tolerance far above it would make
> the conjunct decorative. 0.02 sits at roughly 0.6x the worst-case paired binomial SE,
> so a genuine large regression trips the gate and ordinary sampling variation does not;
> a suite whose measured paired SE is materially smaller than 0.0354 makes the gate
> STRICTER, never looser. This value may be revised ONLY by a dated addendum filed
> BEFORE the suite is committed; after the pre-fit commit it is frozen, and any later
> change is a tripwire FAIL. The suite IDENTITY (the FEN list and its SHA-256) is
> assigned in the pre-fit commit per B4 sentence 2, must be independent of this
> project's own records and of the E-0011 dataset, and must be committed with the hash
> BEFORE any fitting job runs."

---

### B5 - Q-SCOPE: the KING-PST choice was deferred, and the consequence ladder's fallback was cited to an attribution that contradicts it

**B5 sentence 1 (KING PSTs frozen, HERE, not at preflight), verbatim per R-0019:**

> "**Q-SCOPE adopted: all-terms, KING PSTs FROZEN.** The KING PSTs are frozen at their
> hand-tuned values and are NOT fitted; the symmetry-constrained-fit option is
> rejected. The fitted set is therefore the five non-king `mg_pst[5][64]` /
> `eg_pst[5][64]` tables plus items 1 and 3-6 of the free-parameter list. The clause
> 'final choice pinned at execution preflight' is superseded by this pre-registration
> and may not be re-opened after the holdout is read. Freezing rationale (recorded so
> the owner does not re-litigate it): 128 extra free parameters on ~1,000 games of
> stage-6 self-play is the least identifiable block in the set, and E-0010 attributes
> the positional block's +26.8 Elo to a single rung at N=200 whose CI half-width is 51.4
> Elo. Freezing is the lower-variance choice. It does NOT, however, bring the
> fitted-parameter count within E-0011 N1's '>= 500 positions/parameter' standard, and
> this record does not claim it does: with the KING PSTs frozen the fitted set is 683 free
> scalars (10 non-king mg_value/eg_value, 640 from the five non-king PST tables, 20
> pawn-structure, 2 mobility, 10 positional/king, 1 tempo) against a realized usable yield
> of at most 76,587 positions, i.e. about 112 positions/parameter overall and about 89 on
> the TRAIN side - roughly 4.5x short of 500, and 4.5x short is a stated limitation of the
> all-terms scope adopted here, not a solved one. Freezing the KING PSTs (128 free
> scalars, or 64 under the record's own `pst[s] == pst[mirror(s)]` constraint - not 240)
> raises that ratio from about 94 to about 112; it does not reach the standard. E-0011 N1
> derived the standard from an 'O(10^2) parameters' assumption and explicitly declined to
> freeze the parameter count (E-0011:352-353), so the standard's premise, not this
> record's arithmetic, is what the all-terms scope does not satisfy. The binding
> constraint on stage (a) therefore remains the label/systematic bias E-0011 N1 already
> named, together with the game-clustered dispersion `s_d` that E-00014 measures - not the
> parameter count. The freeze decision itself is unaffected and is not re-opened by this
> correction."

*(Editorial, 2026-09-26, under R-0020's licence: the final clause of the sentence above - the one that read "Freezing is the lower-variance choice and the one that keeps the fitted-parameter count defensible against E-0011 N1's '>= 500 positions/parameter' standard" - was FALSE and has been DELETED and REPLACED, and "240 extra free parameters" in the same quoted block has been corrected to **128** (or 64 under `pst[s] == pst[mirror(s)]`). The replacement text is R-0020's own, inserted verbatim. Nothing else in the quoted block was touched, and the freeze DECISION is unchanged. The "(240 params)" in the F3 row of the F1-F12 table is R-0019's own item label and is left as quoted.)*

**B5 sentence 2 (the ladder's citation, corrected - IN THIS RECORD ONLY): WITHDRAWN
2026-09-26, body never established.** This heading announced a quoted sentence that does not
exist. Its slot was empty in the addendum as first filed (`ce845c5`, L684 heading with L685-L686
blank) and no body for it has been located in any revision; the correction it announced is
already stated, once and in full, as the dated correction note under B5 sentence 3
(L832-L858) and again as B6 sentence 1's second quoted block (L1042-L1051). The heading is
therefore **withdrawn rather than filled**: filling it would require inventing normative text on
another seat's behalf, which this record does not do. **No normative content is lost by this
withdrawal and none is invented to replace it** - the backwards-citation correction, the
`k4-k3 = -3.7` / `k6-k5 = -11.5` recomputation, the DISARMED-and-provisional status and obligation
F-U4 all stand as written at L832-L858. This withdrawal closes the slot; it re-opens no
decision and changes no gate.

**B5 sentence 3 - DATED CORRECTION NOTE, and why it lives here and not in E-0011.** The
mis-citation sits in the text of E-0011 (N1) and is inherited by W-0001. **E-0011 is
COMPLETED, W-0001 is DONE/VERIFIED (R-0017), and neither is edited by this addendum or
by this seat.** Repairing a closed, independently verified historical record is exactly
the silent-history-rewrite the system's append-only rule forbids; the finding is
therefore recorded here, dated, as a correction note in the record that inherited the
error, and a follow-up obligation is filed against E-0013's close-out:

> "**Correction note (researcher-architect, 2026-09-26), filed in E-0013 and NOT in
> E-0011.** E-0011 N1's fallback scope sentence - 'if < 30k then the fit is scoped to
> the mobility/tempo sub-set E-0010's ladder motivates' - is a BACKWARDS CITATION. The
> attribution it cites (E-0010:344) attributes the two WORST marginal contributions in
> the whole ladder to exactly those two terms: mobility **-3.7 Elo** and tempo **-11.5
> Elo**, both 'non-positive with CIs crossing zero'. E-0010's ladder is the cited
> evidence and it says the opposite of what the fallback scope assumes. **E-0011 and
> W-0001 are not edited by this note and must not be edited to accommodate it:** they
> are a COMPLETED record and a DONE/VERIFIED record respectively, and the correct
> disposition of a defect found in a verified historical record is a dated note in the
> inheriting record plus an obligation, not a retroactive edit. **Status of the ladder
> here:** the ladder is currently DISARMED - the honest band for the realized usable
> yield is 75,600 to 76,587 against a 30,000 floor, i.e. 2.5x headroom
> (E-00015 measures the realized count; until that count exists this band remains an
> arithmetic bound on already-measured quantities and is NOT a measurement of this
> record's own filter, and the ladder's DISARMED status is provisional on it). If the count
> nevertheless arms the ladder, the fallback scope it would apply is not the
> mobility/tempo sub-set named in E-0011 N1, and the sub-set is re-derived and
> re-registered under its own critique before any use (mobility/tempo scope; B6)
> - so the backwards fallback is a latent trap rather than an active error, and
> this addendum converts it from an auto-applying rule into a rule that CANNOT auto-apply:
> if the ladder arms, the scope is re-derived and re-registered under its own critique
> before it is used. **Follow-up obligation F-U4:** at E-0013's close-out, the owner
> files an addendum to E-0011 (by the seat that owns E-0011, not by the author of
> E-0013) recording the mis-citation and superseding the fallback sentence by name, with
> R-0019 and this note cross-referenced, so the correction is visibly downstream of the
> ruling rather than a quiet edit."

**B6 sentence 2 (the supersession, quoted verbatim so the correction is visible):**

> The Dataset section reads: "Expected yield (measured, not assumed): the terminal checker
> diagnostic on the verified dataset reports `san_position_yield=120930`,
> `quiet_proxy_opening_skipped=76593` ... Extraction therefore starts from ~76.6k
> quiet-proxy positions before dedup/split". The phrase "Expected yield (**measured**,
> not assumed)" is **superseded**: 76,593 is measured for the BARE predicate over the
> `san` segment only; the realized usable yield under this record's own filter is an
> UNMEASURED PREDICTION bounded above by 76,587. The honest band, recorded as a BAND and
> not as a point, is **75,600 <= realized usable yield <= 76,587** (upper bound =
> 76,593 minus at most 6 positions from the single degenerate game and zero crash games;
> lower bound = 76,593 minus ~997 projected cross-game FEN duplicates, from the measured
> 1705/130930 = 1.302 % duplication rate). Both bounds are arithmetic on already-measured
> quantities and neither is a measurement of this record's filter.

**B6 sentence 3 (the ~27k refutation, stated with the reason it was dangerous):**

> "**The '~27k quiet positions post-filter' figure is REFUTED, and it was
> scope-changing, not conservative.** No on-disk artifact supports ~27k for this
> dataset's quiet-proxy yield; the measured per-ply figure is 76,593 and the measured
> distinct-FEN projection is ~75,600. This matters beyond accuracy: 27,000 sits BELOW
> the 30,000 scope floor, so adopting it would have silently ARMED the E-0011 N1
> consequence ladder and auto-scoped the fit to the mobility/tempo subset - the subset
> whose own cited attribution (B5) says those are the two worst terms. A figure that
> would have quietly triggered a scope change is recorded here as refuted, with that
> consequence named, so the next reader cannot reinstate it as a conservative estimate."

---

### Doc-nits DN1-DN10 (all NON-BLOCKING) - dispositions recorded, none silently dropped

| # | Nit | Disposition here |
|---|---|---|
| DN1 | Baseline says the E-0010 per-term ladder is "N=240"; rungs k1-k5 are N=200 each, only k6 is N=240. | **RECORDED, not edited** (the Baseline line is original text and stays). Correction: the ladder rungs k1-k5 are N=200 each; only k6 is N=240. Any strength or attribution sentence in this record that cites "N=240" for k1-k5 is wrong and is superseded by the corrected attribution. |
| DN2 | E-0011 N1 cites quiet yield 76,887 (R-0011's scaled EV-0001 measurement) while the verified 1,000-game dataset's checker reports 76,593. | **RECORDED as a band of provenance, not a conflict to resolve**: 76,887 is E-0011's scaled 1,240-game estimate; 76,593 is the terminal checker on the verified 1,000-game dataset. This record cites the TERMINAL FIGURE only. The two must not be conflated in future records. |
| DN3 | "distance citations computed at execution" is already computable and adequate. | **DISCHARGED**: computed in F10 (`abs(20260926-20260924)*1000003 = 2,000,006 >= 1,000,003 > 1,999`). No deferral remains. |
| DN4 | "365 games in one evening session" is a LOWER bound on throughput, not corroboration of 769/h. | **RECORDED**: the 769/h figure is the E-0010-MEASURED rate and is the one used; the evening figure is a lower bound and is labelled as such. It is not treated as corroboration. |
| DN5 | "dedup exact-FEN within the extraction before the split counts are reported" is ambiguous. | **DISCHARGED** in F9: dedup is GLOBAL, before the split; the surviving copy's `game_id` determines the split; the overlap-0 gate verifies the invariant. |
| DN6 | DEC-0010:186-187 still prints "Pending: independent verification per DEC-0009 gate 3", already discharged by R-0010. | **RECORDED and ROUTED, not fixed here**: DEC-0010 is not this seat's file and is not edited. Flagged to the DEC-0010 owner. Non-blocking, zero effect on E-0013. |
| DN7 | E-0013 does not cite Q-0006, whose readiness gates 1-7 govern this experiment. | **DISCHARGED** by B7, which quotes Q-0006 gate 7 into the record. |
| DN8 | E-0013 does not state that `--validation-known` MUST NOT be passed. | **DISCHARGED** in B1 sentence 1's quoted mechanism, with the `tools/e0012_sprt.py:297-299` citation and the exact tuple that raises. |
| DN9 | With the cap at 2,000 and Tier-S ASN(H0) ~ 2,025, a genuine regression ends INCONCLUSIVE ~half the time; only FAIL is routed to `research/failures/`. | **RECORDED and ROUTED (non-blocking)**: an INCONCLUSIVE on any evaluated conjunct is routed to a NAMED re-decision with the measured stopping time and LLR/estimate published, never to silence. Under the B1 SHRINK decision the strength conjunct is not evaluated in this run at all, so DN9's routing obligation attaches to the deferred strength contract (F-U2) and is recorded here so it is not lost at the hand-off. |
| DN10 | The colour-flipped-relative leakage channel is closed only IMPLICITLY, by conjunct (d)'s colour-symmetry requirement. | **DISCHARGED** (dependency made explicit, quoted below). |

**DN10's explicit-dependency sentence:**

> "The normalized-FEN overlap-0 gate does NOT catch colour-flipped relatives; a
> colour-flipped transposition is a different normalized FEN, so the gate misses it. This
> is sound ONLY while conjunct (d) enforces eval colour-symmetry (mirror `s ^ 56`, 0
> full-mirror violations over 1,000 positions). **Relaxing (d) opens a live leakage
> channel**, because the B2 side-to-move target frame plus an asymmetric eval would let a
> colour-flipped relative carry opposite labels across the split. Conjunct (d) is
> therefore load-bearing for leakage, not only for quality, and may not be relaxed
> without a new leakage analysis."

---

### Follow-up obligations filed by this addendum (additive; the original Follow-Up list above is untouched)

- **F-U1 - P0 (deferred by R-0019, unchanged here).** The H-0013 dataset-discrepancy
  correction ("~50k quiet Stockfish-labeled FENs") is a hypothesis-lifecycle change and
  is **blocked_by E-0013's terminal result**, not by its pre-registration. Route: a
  researcher-architect **decision record** superseding that sentence by name, filed no
  later than E-0013's close-out, explicitly cross-referencing R-0019. **H-0013's
  hypothesis text is NOT amended by this addendum and no H-#### status is changed here.**
  Owner: researcher-architect. Due: E-0013 close-out.
- **F-U2 - the deferred strength contract (the cost of the B1 SHRINK decision).** A
  separate E-0012-style contract (its id to be CLI-assigned when it is filed) for the fitted-vs-pinned Tier-S
  SPRT, with its own pre-registration, its own critique, its own harness validation and
  its own independent verification. Minimum viable mechanism, named now: **two distinct
  compiled binaries** differentiated by per-binary `sha256_file`, which requires the
  minimal two-`--exe` change to `tools/e0012_sprt.py`; a UCI parameter-hash surface is
  required ONLY if that contract elects a single binary with a runtime parameter loader
  instead. `--validation-known` MUST NOT be passed. A harness contract licenses no
  strength claim. Owner: researcher-architect to file; implementation-engineer /
  systems-researcher to build. Due: filed before any strength game is generated.
- **F-U3 - contingency routing for B3 branch X-2 (INCONCLUSIVE-BY-POWER).** Routed to a
  NAMED re-decision with `s_d_inner`, `delta_star`, the inner-partition game count and
  the achieved power published in the open. Candidate re-designs (larger holdout game
  count; a paired design with lower `s_d`; an explicitly widened margin with its own
  power derivation) each require a NEW pre-registration - never an edit to this one.
  Owner: researcher-architect. Due: at E-0013 close-out.
- **F-U4 - the E-0011 N1 backwards-citation correction (see B5 sentence 3).** Filed as
  an addendum to E-0011 **by the seat that owns E-0011**, at E-0013's close-out, naming
  R-0019 and B5. E-0011 and W-0001 are NOT edited by this record. Owner: **systems-researcher**
  (the seat named as `owner:` in E-0011's front matter). Due: E-0013 close-out.
- **F-U5 - Q-0006 readiness gate 7 (see B7).** On any terminal verdict this record files
  a handoff to **verification-auditor** (never the owner, never the seat that ran the
  fit) carrying `fitted_params_sha256`, the pre-fit commit hash, the split-map hash, the
  E-00014 and E-00015 numbers, and the full command/exit-code ledger. No adoption,
  promotion or strength citation before VERIFIED. Owner: the E-0013 execution seat.
  Due: at E-0013 close-out.
- **F-U6 - DN6 routing.** Flag DEC-0010:186-187's stale "Pending: independent
  verification" line to the DEC-0010 owner. Non-blocking, no effect on this record.
  Owner: the DEC-0010 owner seat. Due: next DEC-0010 touch.

---

### Addendum-to-addendum disposition table (R-0019 -> this addendum), dated 2026-09-26

Nothing below is "closed" by assertion. Each row states what physically happened to the
finding, and where a finding is only partly discharged, the row says so and says why.

| Finding | Disposition | What physically happened | Residual |
|---|---|---|---|
| **B1** | **DISCHARGED as a BRANCH DECISION (SHRINK), cost written** | The unexecutable mandate is removed, not re-pointed. S-1 (handshake-hash dump) is superseded by a named, achievable mechanism: two parameter tables differentiated by hash inside the offline evaluator, with the candidate binary built by the existing E-0010 coefficient-regeneration path. P-1's "harness UNMODIFIED" prohibition is honoured by not using the harness at all in this run. `S* = 6` pinned, so `tempo` is read and scored (no inert-coefficient incoherence). Conjunct (e) re-designated NOT-EVALUATED-IN-THIS-RUN by name; verdict vocabulary is PASS-FIT-QUALITY-ONLY. | H-0013's limb (b) is UNANSWERED by this run (cost item 1). The one-`--exe` wall is DEFERRED, not dissolved, and its minimum fix is named + owned + dated (F-U2). A UCI parameter-hash surface is considered-and-REJECTED with a stated reversal condition. |
| **B2** | **DISCHARGED (text); measurement half PRE-REGISTERED as E-00014, NOT RUN** | Colour frame pinned to the side-to-move frame with a FAIL consequence for the White-frame error, superseding 'exact mapping code pinned at execution'. The 'attainable gain unmeasured' acknowledgement is recorded as a fact, with the game-outcome-classifier framing and the 903/1,000 mate dominance named. | The `delta_star` / `s_d` NUMBERS are not in this record and are not in any record yet; they are E-00014's, run by another seat under HO-0015, train-only. |
| **B3** | **DISCHARGED (text), including the contingency decided NOW** | Effective N corrected to games; the decidability condition `s_d <= 0.0101` stated; the false 'any realistic loss variance' clause superseded; the anti-apathetic clause rescoped to QUALITY; the Power-section sentence that converted power failure into apathetic rejection superseded verbatim. | The contingency's INPUT (`s_d_inner`) is E-00014's, not this record's. All three branches X-1/X-2/X-3 are named and mutually exclusive with no fourth branch. X-2 routes to F-U3. |
| **B4** | **DISCHARGED (text)** | Q-FIT = deterministic full-batch L-BFGS with pinned seed/budget/L/L2 selectable on TRAIN-inner only; the SPSA-on-holdout-loss alternative WITHDRAWN as a leakage channel. Single pre-fit commit as the freeze anchor, with the tripwire extended to first-time assignment. Q-SUITE substitution path CLOSED. `SUITE_TOLERANCE = 0.02` pinned as a NUMBER with its binomial-SE derivation. Per-game cap ruled NONE, closing the "if the critic requires a cap" clause. | Suite IDENTITY (FEN list + hash) is a pre-fit-commit field, not a value this addendum can supply. F2's four hyperparameter values are commit fields by design (pointer, not free-floating). |
| **B5** | **DISCHARGED (text); the historical-record part is a DATED CORRECTION NOTE + obligation, by design** | KING PSTs FROZEN here, superseding 'final choice pinned at execution preflight'. The ladder's backwards citation corrected in E-0013's inherited text, with the deltas recomputed from E-0010's own ladder (k4-k3 = -3.7, k6-k5 = -11.5) and the exact reason it is backwards (the fallback scope names the two WORST-attributed terms). The ladder can no longer auto-apply. | **Deliberately NOT discharged against E-0011/W-0001, and this is the point:** they are COMPLETED / DONE-VERIFIED records; editing them would be a silent repair of verified history. F-U4 owns the correction, by the owning seat, at E-0013 close-out. |
| **B6** | **DISCHARGED (rule text); the COUNT itself PRE-REGISTERED as E-00015, NOT RUN** | 76,593 relabelled a PER-PLY count for a DIFFERENT (bare) filter; the 'measured, not assumed' phrase superseded; the honest band 75,600-76,587 recorded as a BAND not a point with its arithmetic; the ~27k figure refuted WITH its scope-changing consequence named (it sits below the 30k floor and would have armed the fallback); the scope-floor rule pre-registered with its branch outcomes fixed now. | The realized count is E-00015's, run by another seat under HO-0016, count-only, before any fitter is invoked. |
| **B7** | **DISCHARGED (text)** | Q-0006 readiness gate 7 quoted verbatim into the record and given teeth: a verification-auditor handoff on any terminal verdict, carrying the artifact hash, the pre-fit commit hash, the split-map hash and the E-00014/E-00015 numbers. Q-0006 is now cited (also DN7). | The handoff is filed at close-out (F-U5); the gate's CONTENT is discharged now. |
| **F1-F12 freeze-audit gap** | **DISCHARGED item by item** | Each of F1-F12 is closed in the B4 s5 table with either a VALUE (F1, F3, F4-partial, F6-partial, F7, F8, F9, F10, F12) or an explicit "derived from <pinned input>" pointer to the single pre-fit commit (F2, F4-identity, F5, F11). No item is left as a bare first-time assignment. | Pointer-closed items are closed by the ANCHOR (the pre-fit commit), which is the mechanism R-0019 itself prescribed, not by me deferring them again. |
| **DN1-DN10** | **RECORDED, non-blocking; 5 discharged (DN3, DN5, DN7, DN8, DN10), 4 recorded/routed (DN1, DN2, DN4, DN6), 1 recorded + carried (DN9)** | Each has a disposition row. None silently dropped. | DN6 is not this seat's file (routed). DN9's routing attaches to the deferred strength contract and is preserved in F-U2 so it is not lost. |
| **X1 (R-0020)** | **DISCHARGED - in-place text repair of THIS addendum, 2026-09-26, under R-0020's licence** | R-0020 found this addendum to be a truncated, interleaved document: ten sentences severed at a block boundary with their continuations relocated far away, ONE continuation absent from the file, the X-1/X-2/X-3 contingency table ~340 lines from the sentence announcing it, the follow-up obligations split across this table, and the file ending mid-bullet. All ten seams are now joined as single contiguous sentences inside their own finding's section; the absent continuation is supplied as X1-a; the contingency table now sits immediately under B3 sentence 3's announcement; F-U1..F-U6 (including F-U3's stranded `Owner:/Due:` line) are one contiguous list; cost item 4 is contiguous with items 1-3; the BUCKET-1/2/3 list is restored to one place; and the file ends on a complete sentence. **Corrected under R-0021: that last clause was true at `f450976` and FALSE from `fce355c`, because S-0029 inserted its verification block between the two halves of the tail sentence. That was X4; the tail is rejoined and the file again ends on a complete sentence.** | The repair is a MOVE, not a rewrite: no sentence was deleted and no continuation was retyped, and every move is listed line-by-line in the dated repair section at the end of this addendum - with ONE recorded exception to the no-deletion rule, the seam-8 head fragment (X5 below), which was deleted because keeping it would have produced a second duplication. Consequence stated rather than hidden: this ADDENDUM is therefore NOT purely additive to itself. The ORIGINAL pre-registration (L1-L428) is append-only and provably so, by hash - see the same repair section. |
| **X2 (R-0020)** | **DISCHARGED - the false clause DELETED, the arithmetic INSERTED** | B5 sentence 1's recorded rationale claimed that freezing "keeps the fitted-parameter count defensible against E-0011 N1's '>= 500 positions/parameter' standard". That is false: 683 free scalars against at most 76,587 realized positions is ~112 positions per parameter (~89 train-side), about 4.46x short of 500, and freezing moves 94 -> 112, not to 500. The clause is deleted and replaced with R-0020's own arithmetic, and "240 extra free parameters" reads **128** (or 64 under `pst[s] == pst[mirror(s)]`). | The freeze DECISION is unchanged and is NOT re-opened by this correction. 4.46x short is now recorded as a STATED LIMITATION of the all-terms scope, not as a solved one; the binding constraints on stage (a) remain E-0011 N1's label/systematic bias and the game-clustered `s_d` that E-00014 measures. |
| **B5 s2 (pre-existing)** | **WITHDRAWN 2026-09-26 under R-0021 - not moved, not filled, not invented** | B5 sentence 2's heading at L811 ("the ladder's citation, corrected - IN THIS RECORD ONLY") announced quoted text and its slot was EMPTY: L812-L822 were blank and B5 sentence 3's heading was at L824. The same hole exists in `ce845c5` (L684 heading, L685-L686 blank, B5 sentence 3 at L687), so it is PRE-EXISTING and was not introduced by the R-0020 repair. **The heading and its two blank lines have now been REPLACED by R-0021's withdrawal paragraph; nothing was relocated and no body was invented.** | **The announced body is NOT established to be the correction-note block at L832-L858, and this row does not claim it is:** that block is introduced by B5 sentence 3, whose preamble ends in a colon at L830 and is immediately followed by it, so it is already spoken for. B5 s2 has no located body anywhere in the file, and whether its text was lost, never written, or is the note under another name is UNESTABLISHED - not guessed, and not guessed at here either. (The earlier note that this text "sits far away under B6 sentence 1" described the `ce845c5` geometry, in which this material ran to old L871 near B6 s1; after the R-0020 repair the note is at L832-L858 under B5 s3 and B6 s1 is at L1026. That note is now corrected and points at the withdrawal.) This is the same interleaving class as X1 - a heading whose body lives elsewhere - which is why it was hard to detect. **The disposition question is settled: R-0021 ruled that `UNESTABLISHED` names the defect without dispositioning it, and that a heading announcing text the record does not contain is a live misstatement, so the heading is WITHDRAWN rather than filled - a withdrawn heading asserts nothing, an invented body would assert something. "Flagged for the next reviewer" was the deferral that produced the finding; the next reviewer was R-0021, and this row now points at the withdrawal.** |

**What is explicitly NOT claimed by this addendum.** It does not claim B1's strength
question is answered; it does not claim a fitted artifact exists; it does not claim any
number from E-00014 or E-00015; it does not edit R-0019, HO-0013, or any CLOSED/VERIFIED
record; it does not flip E-0013 to RUNNING; it does not change any H-#### status; and it
does not touch `tools/e0012_sprt.py` or any engine source file.

**B6 sentence 4 (the pre-registered rule for what the measured count DOES to the scope
floor - decided now, so the floor is not renegotiable once the number exists):**

> "**Scope-floor rule, pre-registered (decided 2026-09-26, before the count exists).**
> Let `Y_realized` be the count reported by E-00015 under this record's own filter, and
> `Y_train` the TRAIN-side subset of it. Then: (i) if `Y_train >= 30000`, the
> all-terms scope stands and conjunct (a) PASSES on yield; (ii) if `Y_train < 30000`,
> conjunct (a) FAILS the scope sub-condition, the all-terms claim is **WITHDRAWN**
> (recorded, not silently kept, per the existing conjunct (a)), and the scope reduction
> is **NOT** the mobility/tempo subset - per B5 sentence 2 that subset is not derivable
> from the cited attribution and must be re-derived and re-registered under its own
> critique before use; the run then ends INCONCLUSIVE-BY-SCOPE rather than proceeding on
> a scope nobody has justified. The floor is 30,000 on the TRAIN-side count, not on the
> whole-dataset count, so that no whole-dataset quantity decides the fit's scope. This
> rule is fixed now and may not be altered after E-00015 reports."

---

### B7 - Q-0006's official readiness gate 7 was missing from E-0013

**B7 sentence, verbatim per R-0019, with Q-0006's own text quoted as the authority:**

> Q-0006 (Official first-training readiness gates, item 7) reads: "The fit produces and
> pins `fitted_params_sha256`, loads exactly that artifact into the candidate, and
> receives independent verification. No adoption or strength claim precedes it."

> "**Independent verification of the fitted artifact (Q-0006 official readiness gate 7,
> quoted above).** On a terminal PASS-FIT-QUALITY-ONLY, a terminal FAIL, or any named
> INCONCLUSIVE, this record files a handoff to verification-auditor - never the owner
> seat, never the seat that ran the fit - carrying `fitted_params_sha256`, the pre-fit
> commit hash, the split-map hash, the E-00014 feasibility-pass numbers (`s_d_inner`,
> `delta_star`, contingency branch X-1/X-2/X-3), the E-00015 count-pass numbers, and the
> full command / exit-code ledger. The fitted artifact is not adopted, promoted, cited as
 a strength input, or referenced by any downstream record before that verification
> returns VERIFIED. No adoption or strength claim precedes it. This is added as a
> Follow-Up obligation, F-U5; Q-0006 is hereby CITED by this record (also discharging
> doc-nit DN7)."

---

### B6 - The yield: the "measured" label was applied to a number measured for a different filter

**B6 sentence 1 (the count pass rule and the relabelling; the count itself is BUCKET 2 -
pre-registered in E-00015, not run here), verbatim per R-0019:**

> "**Realized yield governs, measured by a count-only pre-fit pass.** The terminal
> diagnostic `quiet_proxy_opening_skipped = 76593` is a **per-ply count over the `san`
> segment for the bare quiet predicate** (`tools/e0011_check.py:385-398`); it applies no
> crash exclusion, no degenerate-mate exclusion, no dedup and no split, and it is
> therefore not the realized usable yield under this record's own filter. Conjunct (a) is
> evaluated on the realized count reported by a **count-only, non-training** extraction
> pass - the QUIET predicate plus the crash exclusion plus the degenerate exclusion plus
> the dedup plus the committed split map - run and hash-committed **before any fitter is
> invoked**. That realized count, and neither 76593 nor the session brief's ~27k, is the
> number that arms or disarms the 30k ladder. The scope branch is additionally evaluated
> on the **TRAIN-side count alone**, so that no whole-dataset quantity decides the fit's
> scope. The count pass is E-00015; this record does not run it."

> "**Consequence-ladder citation corrected (binding only if the ladder arms).** E-0011
> N1's fallback scope, 'the mobility/tempo sub-set E-0010's ladder motivates', is a
> mis-citation: E-0010 (line 344) measures the marginal contributions as mobility -3.7
> Elo and tempo -11.5 Elo, 'non-positive with CIs crossing zero'. The two terms the
> ladder names as the fallback scope are the two the ladder attributes the WORST
> contributions to. I recomputed the deltas from E-0010's own published ladder
> (k4-k3 = 100.8-104.5 = -3.7; k6-k5 = 116.1-127.6 = -11.5) and they reproduce exactly.
> If the realized usable yield ever falls below 30,000, the fallback scope is **not** the
> mobility/tempo subset on this citation; it MUST be re-derived and re-registered under
> its own critique before it is applied."

**B4 sentence 5 (the freeze-audit gap, closed item by item - F1-F12).** R-0019's central
structural point is adopted verbatim: the existing tripwire binds *changes* and does not
bind *first-time assignments*, and every value in F1-F10 is a first-time assignment.
Each is closed here with a value or an explicit pointer to a pinned input:

| # | Value at risk | Closed how (this addendum) |
|---|---|---|
| F1 | Fitting-method family | **VALUE**: deterministic full-batch L-BFGS (B4 s1). SPSA withdrawn. Not a choice at execution. |
| F2 | Fitter seed, L2 weight, iteration budget, early stopping | **POINTER**: all four are fields of the single pre-fit commit of B4 s2, hash-committed with the split map, choosable ONLY on the TRAIN inner partition. The commit is the anchor; no value may be first-assigned after the holdout is read (tripwire FAIL). |
| F3 | KING-PST freeze-vs-fit (240 params) | **VALUE**: **FROZEN**, here, not at preflight (B5 s1). The clause 'final choice pinned at execution preflight from this list' is superseded. |
| F4 | Suite identity, N, metric, tolerance | **VALUE for N, metric, tolerance** (B4 s4: N >= 200, solution rate, `SUITE_TOLERANCE = 0.02`, substitution path closed); **POINTER for identity** = the pre-fit commit of B4 s2, FEN list + SHA-256, committed before any fitting job. |
| F5 | MAE phase-tertile boundaries | **POINTER**: derived from a pinned input - tertile boundaries of the phase value `phase = min(1*N + 1*B + 2*R + 4*Q, 24)` computed over **TRAIN positions only**, rounded to integers, with the boundary list and its SHA-256 frozen in the pre-fit commit. Never derived from holdout phase values. |
| F6 | Fresh SPRT salt | **POINTER + VALUE**: no fresh salt is used by this record at all (B1 SHRINK - no game campaign runs). The deferred strength contract must assign one; the admissibility RULE is pinned here: `abs(S - S') * 1000003 > cap - 1` for every prior salt in {20260914, 20260922, 20260924, 20260926}. |
| F7 | EvalStage at which stage (a) is scored, and against which floor | **VALUE**: `S* = 6`; floor = the compiled-in table of `src/eval.cpp:174-234` at the pinned `src/` commit (B1 s2). |
| F8 | Label colour frame | **VALUE**: the side-to-move frame (B2 s1). The clause 'exact mapping code pinned at execution' is superseded as to the FRAME. |
| F9 | Dedup scope: global-before-split vs per-split-then-assert | **VALUE**: **dedup is GLOBAL, before the split.** The surviving copy's `game_id` determines the split; the normalized-FEN overlap-0 gate then verifies that invariant (also discharges DN5). |
| F10 | Salt-distance citation | **VALUE, computed not deferred**: `abs(20260926 - 20260924) * 1000003 = 2,000,006 >= 1,000,003 > 1,999`; likewise vs 20260922 and 20260914. Discharges DN3. |
| F11 | `LOSS_MARGIN = 0.002` attainability | **POINTER**: E-00014, plus the B3 contingency table X-1/X-2/X-3 decided in advance. The NUMBER stays 0.002 as the floor; only its attainability is measured. |
| F12 | Per-game position cap | **VALUE: NONE** (B4 s3), closed and not re-openable. |

**B4 sentence 3 (Q-SUITE: substitution path closed; the critic's cap answer), verbatim
per R-0019:**

> "**Q-SUITE.** The 'OR the suite is replaced by a same-N independent spot check' path is
> closed: a substituted suite must have its identity, N, metric and TOLERANCE committed
> in the same pre-fit commit as the original suite, and a substitution first made after
> the holdout or the SPRT is read is a tripwire FAIL. A suite list whose tolerance is
> still a placeholder is not a committed suite and conjunct (f) is not yet evaluable.
> **Per-game position cap: ruled NONE by HO-0013 / R-0019, 2026-09-26.** cap = all quiet
> positions after the exclusions and the dedup. A cap would shrink the holdout, reduce
> power and add a discretionary filter, while the BY-GAME split plus the normalized-FEN
> overlap-0 gate already carry the entire leakage obligation. This answer closes the
> clause 'If the critic requires a cap' and may not be re-opened."

**B3 sentence 4 (the clause in the Power And Sample Size section that must not survive
beside B3 - quoted verbatim and superseded):**

> The Power And Sample Size section reads: "if the realized holdout SE cannot separate
> 0.002 from 0, the margin (not the N) was aspirational - shrink the claim per HO-0013
> ruling question (v), never silently weaken the band. Therefore stage (a) IS decidable
> at the planned N unless the realized variance proves otherwise, in which case the
> verdict is FAIL (apathetic-fit rejection), not INCONCLUSIVE." That sentence pair is
> **superseded** by B3 sentences 1-3: the phrase 'for any realistic loss variance' is
> withdrawn as an unbounded quantifier over an unmeasured quantity, and the trailing
> 'the verdict is FAIL ... not INCONCLUSIVE' is withdrawn because it converts a POWER
> failure into an apathetic-fit rejection it was not. The margin itself is NOT lowered
> and the band is NOT widened."

**B1 sentence 3 (the verdict vocabulary of the amended record, so nothing is dropped
silently):**

> "**Conjunct (e) re-designated, not deleted.** Conjunct (e) (Strength gate, stage b,
> Tier-S SPRT) is **NOT EVALUATED IN THIS RUN** under the B1 SHRINK decision. It is not
> deleted, not counted as PASS, and not counted as FAIL. E-0013's OVERALL rule is
> therefore amended by this addendum: the amended OVERALL verdict is computed over
> conjuncts (a),(b),(c),(d),(f),(g),(h) with (e) recorded as NOT-EVALUATED-IN-THIS-RUN;
> a run in which all seven evaluated conjuncts PASS is recorded as
> **PASS-FIT-QUALITY-ONLY**, which licenses the limb-(a) claim and nothing else. A
> NO-EVALUATED-CONJUNCT run may never be summarised as 'baseline preserved', as
> NEUTRAL, or as an overall PASS. Conjunct (h) (scope honesty) is evaluated with the
> scope narrowed accordingly: this record licenses no engine-strength statement of any
> kind, which trivially satisfies (h) and is the reason (h) is retained rather than
> dropped."

**The decision.** This record's first training run is **fit-quality-only**. In this
record's own stage vocabulary: stage (a) (the frozen-holdout logistic-loss comparison)
and the quality-conservation gates RUN; **stage (b), the Tier-S strength SPRT, does NOT
run in this record and is DEFERRED** to a later, separately pre-registered contract.
(This is the sense of "fit-quality-only (stages a/b)" in the owner's instruction: the
fit-quality stages of THIS record; stage (b) here is the strength stage and is the thing
deferred.) Conjunct (e) is therefore re-designated NOT-EVALUATED-IN-THIS-RUN -
explicitly, by name, below - and no outcome of this run may be reported as a strength
result.

---

### Dated repair of THIS addendum under R-0020 - 2026-09-26 (in-place; the original is untouched)

**Why this section exists.** R-0020 (adversarial-reviewer, HO-0014) ruled **NOT CLEAN** on this
addendum and left E-0013 at `status: PENDING`. Its substance largely held and no decision was
re-opened; its two blocking findings were defects of this document's TEXT, and this section
records what was found and what was done about it.

**X1 - the addendum was a truncated, interleaved document.** Ten sentences were severed at a
block boundary, each ending mid-clause with its continuation relocated far away; ONE
continuation was absent from the file entirely; the X-1/X-2/X-3 contingency table sat ~340
lines from the sentence that announces it; the F-U1..F-U6 obligations were split across the
disposition table; and the file ended mid-bullet. Four of the seams sat on normatively critical
text: B1 sentence 2's `tempo` conclusion, B2 sentence 2b's `LOSS_MARGIN` rule, B4 sentence 2's
freeze anchor (the instrument F2, F5, F10 and F11 close against) and B4 sentence 4's
`SUITE_TOLERANCE` derivation.

**X2 - B5's freezing rationale was arithmetically false.** The claim that freezing "keeps the
fitted-parameter count defensible against E-0011 N1's '>= 500 positions/parameter' standard" is
false by a factor of ~4.46, and "240 extra free parameters" is not the KING-PST count. The false
clause was deleted, R-0020's own arithmetic was inserted verbatim, and 240 reads 128. The freeze
DECISION is untouched.

**X3 - ownership.** `owner: systems-researcher` set on E-00014 and E-00015, the seat HO-0015 and
HO-0016 dispatch to. One front-matter line each.

**Nits.** N1 (R-0020's nit, a regression hazard rather than cosmetics): a binding note was added
to B1 sentence 1 that coefficient regeneration substitutes the coefficient block ONLY and must
not re-run a stage generator, because `write_eval_p5.py:87` emits the unsigned
`score += C.tempo;` while the live `src/eval.cpp:356` carries the E-0010 side-to-move-signed
fix - regressing that line would break the colour-symmetry invariant that conjunct (d) gates on
and that B2's side-to-move frame and DN10 both depend on. N2: F-U4's owner seat is now named
literally (`systems-researcher`). N3: this disposition table gained rows for X1 and X2.

**Per-seam ledger.** "before" is the `ce845c5` line numbering R-0020 cited; "after" is this
file's current numbering. Every CONTINUATION was MOVED byte-for-byte, not retyped - the one
recorded exception is the seam-8 head fragment, see the X5 entry below; each joined
sentence is now one contiguous run of lines inside its own finding's section.

| # | Head (before) | Continuation (before) | The one sentence now occupies | What that unblocks |
|---|---|---|---|---|
| 1 | L460 `B1 (as a branch` | L1064-L1067 | L471-L475 | the three-bucket list is one list again, at L471-L487 |
| 2 | L488 `...this record` | L1051-L1052 | L515-L517 | B1's self-collision diagnosis parses in place |
| 3 | L513 `...and the loader` | L1044 | L542-L543 | the UCI-surface reversal condition is complete |
| 4 | L547 `...and remains` | L1022-L1026 | L593-L598 | **the S\* conclusion has an object again** |
| 5 | L588 `...over the` | L1011-L1020 | L639-L649 | **the `LOSS_MARGIN` rule is one sentence** |
| 6 | L646 `...and the holdout is` | L941-L944 | L743-L747 | **the freeze anchor is unsevered; F2, F5, F10 and F11 rest on it** |
| 7 | L664 `...would make` | L911-L919 | L765-L774 | **the `SUITE_TOLERANCE` derivation is whole** |
| 8 | L707 `i.e. 2.5x headroom` | X1-a (author's text, new) + L871-L878 | L844-L858 | the ladder's DISARMED status is provisional, and reasoned |
| 9 | L730 `...ARMED the E-0011 N1` | L828-L831 | L881-L885 | the ~27k refutation's scope-changing consequence is attached |
| 10 | L754 `**Relaxing (d) opens a live leakage` | L823-L826 | L909-L913 | DN10's explicit-dependency sentence is one sentence |

**X1-a - the one seam that needed authorial text, and how the seam-8 misjoin was resolved.**
R-0020 deliberately refused to guess the missing words and supplied a conforming template
instead. **I ADOPTED THAT TEMPLATE VERBATIM** (R-0020:696-701) rather than rewriting it in my
own words, and it satisfies R-0020's conditions (a) and (b): it names **E-00015** as the pass
that measures the realized count and states that the ladder's DISARMED status is **provisional
on** that count, and it says explicitly that the band "is NOT a measurement of this record's own
filter". Condition (c) - that the inserted text end on the parenthetical "... (mobility/tempo
scope; B6)" and lead grammatically into the tail at old L871 - is the source of a defect in the
**ruling, not in this repair**: R-0020 quoted that same tail as beginning `it; B6) -`
(R-0020:676) while also requiring the inserted text to end `... (mobility/tempo scope; B6)`
(R-0020:690-691, 696-701). The two instructions overlap, and adopting the template verbatim, as
R-0020 offered and as I was directed, produced `B6)` twice in the joined sentence, the second
occurrence closing nothing and the word `it;` stranded with no antecedent.

**The deletion, stated explicitly as required.** The alternative form was used: the template is
kept whole, and the leading `it; B6)` of the author's tail (old L871, now L851) was **deleted**.
That is text R-0020 said to move, and deleting it is recorded here rather than done silently.
It was deleted because it is the redundant half of the duplication, not because it carried
meaning: `it;` is stranded (the template has already said "provisional on it") and its `B6)`
duplicates the citation the template's own parenthetical already makes. The alternative was
chosen over trimming the template's `B6)` because trimming it would delete the very string
R-0020's condition (c) mandates and would leave the count of `mobility/tempo scope; B6)` at 0,
falsifying the verbatim-adoption claim recorded in this same section. The cost is stated rather
than hidden: **the head's opening paren `(E-00015 measures` was left unclosed**, because
R-0020's template consumed the tail's `)` and supplied a self-closing parenthetical of its own.
Both candidate forms leave that paren orphaned (delta +1); the pre-fix text was balanced only
because the duplicated citation accidentally supplied a second `)`. This is a defect inherited
from the template. **SUPERSEDED under R-0021, 2026-09-26: the orphan IS now closed** - a single
closing parenthesis inserted after `provisional on it` in the seam-8 note, so the B5/B6 block's
paren delta is 0. S-0029's reason for leaving it - that closing it "would require inventing a
closing token R-0020 did not supply" - is **withdrawn as WRONG**: the template bounds the span,
so that closer is not an invented token. R-0021 ruled against that reason; this seat concurs.

**Other moves, same rule - nothing deleted, nothing retyped, with ONE recorded exception.**
The X-1/X-2/X-3 contingency table
moved from old L960-L995 to L682-L717, immediately under B3 sentence 3's announcement at
L677-L680, with no wording change. F-U3's stranded `Owner:/Due:` line (old L808) and the
F-U4/F-U5/F-U6 bullets (old L809-L821) rejoined F-U1..F-U3, now one contiguous list at
L919-L954. B1's cost item 4 (old L1045-L1049) rejoined items 1-3 at L544-L548. The BUCKET-2 and
BUCKET-3 bullets (old L1068-L1073) rejoined BUCKET-1 at L476-L487, and BUCKET 3's promised cost is
now stated in the bullet itself, in the words B1's cost items 1-4 already use. The addendum's
narrative now ends on a complete sentence at L1117-L1125 - the old L1073 bullet "Decision:
**SHRINK.**" had no continuation of any kind - and this dated repair section follows it.

**N1, N2, N3, placed.** N1 is a binding note at L572-L581, immediately after B1 sentence 1's
quoted mechanism. N2 names F-U4's owner seat literally at L944-L945. N3 added a disposition-table
row for X1 and one for X2 to the addendum-to-addendum table, so no future reader is told by that
table that everything was already closed.

**X2, placed.** The false clause was deleted and R-0020's replacement inserted at L791-L807; the
"240 extra free parameters" in the same quoted block reads **128** at L788; and a dated editorial
note at L809 records that this was an in-place replacement of quoted text, quotes the old wording,
and states that the freeze DECISION is unchanged. The "(240 params)" in the F3 row of the F1-F12
table is R-0019's own item label and is left as quoted, for the same reason E-0011 is not edited.

**One observation, now DISPOSITIONED under R-0021 (2026-09-26) - the heading is WITHDRAWN.**
"B5 sentence 2 (the ladder's citation, corrected)" at L811 announced quoted text, and its
slot was empty. **This note's location claim was stale and is corrected here:** the material does
not "sit far away under B6 sentence 1" - that described the `ce845c5` geometry. After the R-0020
repair the correction note is at L832-L858 **under B5 s3**, B6 s1 is at L1026, and the
heading itself has been **withdrawn, not filled** (see the withdrawal paragraph at L811 and
the R-0021 entry below). Nothing was relocated; no body was invented.

**The append-only contract, proved by hash rather than asserted.** Lines 1-428 of this file -
the original pre-registration, above the addendum - are byte-identical to the same lines at
`ce845c5`. SHA-256 over lines 1..428 including their line terminators, UTF-8, 22,270 bytes:

- `git show ce845c5:research/experiments/E-0013-h-0013-...-stage-5.md`, lines 1-428 ->
  `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`
- this working file, lines 1-428 ->
  `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`

Equal. **The ORIGINAL is append-only and provably so. The ADDENDUM was found corrupt by review
and repaired IN PLACE under that review's licence** (R-0020: "move that text, not rewrite it";
"delete the false clause and replace it"). That is why a numstat taken at the addendum's
first-filed boundary no longer reads zero-deletions, rather than one taken at the original's
boundary, which still reads zero. That is stated here rather than papered over, and the
distinction is the point: the append-only rule protects the pre-registration, not the corrupt
addendum. (Corrected under R-0021: `648 additions / 0 deletions` is the numstat of
`4478c3a..ce845c5`, not of `ce845c5..HEAD`; all three figures are stated in the R-0021 entry below.)

**A note on the append-only check itself.** `git diff --numstat HEAD -- <E-0013 path>` returns
EMPTY on a clean tree and therefore cannot distinguish "add-only" from "nothing changed". Any
append-only evidence line must name a baseline commit - here `ce845c5` for the pre-repair
addendum, or `4478c3a` for the pre-addendum file.

### Dated repair of THIS addendum under R-0021 - 2026-09-26 (round 4, same seat; all four findings mechanical)

**Why this section exists.** R-0021 (adversarial-reviewer, independent post-repair critique) ruled
**NOT CLEAN** on this addendum after S-0028's and S-0029's passes, and left E-0013 at
`status: PENDING`. It confirmed the substance sound by its own recomputation - all ten seams
joined including the four normatively critical ones, the contingency table under B3 s3,
F-U1..F-U6 contiguous, the `B6)` duplication fixed, the freeze anchor unsevered with all twelve
F-items closing against it, X2's arithmetic correct in every figure, no surviving compliance claim
and X3's owners set - and ruled **B3 DISCHARGED, B4 DISCHARGED, B5 still PARTIALLY**. It raised
**two new findings, both introduced by the repair passes themselves**, and required two further
repairs inside B5. **No decision is re-opened:** SHRINK, the KING-PST freeze,
`SUITE_TOLERANCE = 0.02`, the per-game cap NONE and the X-1/X-2/X-3 branches all stand exactly as
decided.

**X4 (BLOCKING, REPAIRED) - S-0029 re-severed the file's tail.** S-0029's forty-line verification
block was inserted between the two halves of one sentence, so its head stood stranded at
L1394 (`...this repair is not authorisation to`) while the file's last line was the orphan
continuation `move it, and per R-0020 the flip requires a fresh re-critique to confirm.` - a
sentence that carries **E-0013's own non-authorisation**. At `f450976` the two halves were
adjacent, and the diff `f450976..fce355c` is forty `+` lines inserted between them and nothing
else. **The repair: the orphan is DELETED in its entirety and its text is APPENDED to the end of
the stranded head - the author's own words MOVED, not retyped** - so L1394 now ends
`...this repair is not authorisation to move it, and per R-0020 the flip requires a fresh
re-critique to confirm.` **The same move was performed correctly by S-0029 on seam 8, and it
should have been applied here too; that is recorded here because it is the reason a defect of the
very class this pass claimed to eliminate survived the pass.**

**The two statements X4 falsified, and this session's restoration of them.** S-0029's insertion
made two claims in this file false: the X1 disposition row's "the file ends on a complete
sentence" - true at `f450976`, false from `fce355c` until the repair above - and this verification
block's "the file's terminal complete sentence at L1116-L1124", which is true of the *narrative*
"The decision." paragraph (it does end complete there) but not of the FILE, whose terminal
sentence was the orphan. **Both are corrected in place to describe the post-repair state, and the
correction is recorded as this session's: restoring statements S-0029 falsified, not asserting
anything new.** The redundant restatement at L1432-L1436 is left standing - R-0021 rules it
harmless and honest, and it is not load-bearing - and the file's terminal sentence is that
restatement, which is itself a complete sentence carrying the same non-authorisation.

**X5 (NON-BLOCKING, NOW RECORDED) - an unrecorded head-side deletion at seam 8.** The two claims
"Every continuation was MOVED byte-for-byte, not retyped" and "Other moves, same rule - nothing
deleted, nothing retyped", both in this section, are **false as general claims about the seam**.
They hold of the *continuations* and were broken on the *head*. At `ce845c5` **L707** the head
ended `...i.e. 2.5x headroom (E-00015 measures` - **four words of the author's original text**.
S-0028 deleted those four words and **did not record doing so**; the count of `(E-00015 measures`
in the file went 1 -> 2, the second being the template's own opening. **The deletion was
SUBSTANTIVELY CORRECT AND NECESSARY:** R-0020's own template opens with `(E-00015 measures`, so
keeping the fragment would have produced `(E-00015 measures (E-00015 measures ...` and a second
duplication. The defect was the silence, not the deletion - which is precisely why X5 is
non-blocking. **Both claims are QUALIFIED in place rather than deleted: the exception now stands
on the record, and that is the whole point of X5.**

**The seam-8 orphan parenthesis, CLOSED (R-0021 section 2(c)).** R-0021 ruled the joined seam-8
sentence **defective as typography and correct as normative text**: the obligation - re-derive and
re-register under its own critique before use - sits in the main clause, is syntactically
independent of the parenthetical, and is stated three more times in this file, so only a citation
*label* could be mis-scoped, and B6 is 130 lines away and intact. It is therefore a cleanliness
fix, not a semantic emergency. **The repair is one character: a `)` inserted after `provisional on
it` in the seam-8 note, at the boundary R-0020's own template already specifies.** Post-repair the
B5/B6 block's paren delta is **0** (it was +1) and the seam carries **exactly one `B6)` citation**.

**Agreement with the reviewer, against the earlier same-seat reasoning.** S-0029 recorded that
the orphan "is **not** repaired here because closing it would require inventing a closing token
R-0020 did not supply". **That sentence is withdrawn as WRONG and is struck in place above.**
R-0021 disagreed with that reason; this seat concurs with R-0021, because the template does bound
the span and the `)` is a closer rather than an invented token. S-0029 was right that the defect
was inherited and wrong that it was unfixable. **The disagreement is on the record and is resolved
in favour of the reviewer.**

**B5 sentence 2 - the heading is WITHDRAWN, not filled (R-0021 section 3).** S-0029's
disposition `UNESTABLISHED` named the defect and left it standing. R-0021 ruled that a heading
announcing a correction the record does not contain is a live misstatement - it invites a reader
either to double-count B5 s3's correction note as a second finding, or to conclude a correction is
missing - and that **a withdrawn heading asserts nothing, while an invented body would assert
something**, so withdrawal is the only option that cannot mislead. The heading and its two blank
lines are replaced by R-0021's own withdrawal paragraph at L811, which names where the
correction actually lives and states explicitly that no normative content is lost by the
withdrawal and none is invented to replace it. **Nothing was relocated and no normative text was
composed here.** The two pointers the withdrawal supersedes - the note at L1235 above, which
described the `ce845c5` geometry, and the closing sentence of the `B5 s2` disposition row - now
point at the withdrawal instead.

**The APPEND-ONLY BASELINE, corrected and correctly labelled (R-0021 section 5c).** The
characterisation above is honest but attached its numstat to the wrong commit. All three figures
are now stated explicitly, each against the boundary it actually describes:

| Boundary | Numstat at `d3ce887` (R-0021's HEAD) | Numstat after this R-0021 repair | What the boundary is |
|---|---|---|---|
| `4478c3a..HEAD` | 868 insertions, 0 deletions | **1011 insertions, 0 deletions** | **the addendum has NEVER had a deletion against the original pre-registration** - the strongest true statement, and the one that discharges the append-only obligation outright |
| `ce845c5..HEAD` | 347 insertions, 127 deletions | **493 insertions, 130 deletions** | the addendum-as-first-filed boundary, correctly labelled this time; the deletions are the visible, itemised cost of the review-licensed repairs, and this repair adds 3 of them |
| `f450976..HEAD` | 71 insertions, 12 deletions (S-0029's pass alone) | **231 insertions, 29 deletions** | the S-0028/S-0029 repair boundary, measured on the two repair passes rather than on the addendum |

**The `288/127` figure in circulation was the `f450976` boundary mislabelled as `ce845c5`, and
that correction is R-0021's, not this seat's** - it is recorded here as such. The sentence above
that attached `648 additions / 0 deletions` to `ce845c5..HEAD` is corrected in place: `648 / 0` is
the numstat of `4478c3a..ce845c5`, the ORIGINAL addendum pre-repair, and is correct at that
boundary.

**Re-critique gate (added 2026-09-26 under R-0021).** This record may leave `status: PENDING` for
`status: RUNNING` only when a fresh adversarial-reviewer critique confirms, by line-range read,
that (i) the file ends on a complete sentence, (ii) the parenthesis opened at the seam-8
correction note is closed and exactly one `B6)` citation remains, (iii) the B5 sentence-2 slot is
withdrawn rather than filled, (iv) every deletion made in any repair pass is itemised in the dated
repair section, and (v) lines 1-428 still hash to
`b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6` on both sides. **The repair
section is not authorisation to run, and no seat may flip this record on the strength of the
repair section's own claims.**

**A line-number shift this repair causes, stated rather than left silent.** The B5 s2
withdrawal above replaced three lines with thirteen, so **every line reference in this
addendum that pointed at a line at or after the old L811 is now +10.** References introduced
with the word `old`, and references to `ce845c5`, are a different numbering and are NOT
shifted. The cross-references written *by this repair* - inside the withdrawal paragraph and inside
the `B5 s2` disposition row - have been re-derived to the post-withdrawal numbering, and
those two families are the only ones that were. The original wording also claimed the
observation note, the verification block and this dated R-0021 entry were re-derived; for
four X4 pointers that was FALSE - R-0022 found them unresolvable - and they are fixed in
place now. The older per-line citations elsewhere in the addendum were not rewritten by that
pass either; the seven whose targets lie inside the band have since been re-derived against
their content, and every `old`-prefixed and `ce845c5`-relative reference is exempt and stands.
The +10 rule holds only for targets in `d3ce887` L813-L1152; below `d3ce887` L1154 the shift
grows, so a reader must not apply it there. The remainder are left to the re-critique.

**What was NOT touched.** No decision: SHRINK stands, the KING-PST freeze stands,
`SUITE_TOLERANCE = 0.02` stands, the per-game cap stays NONE, and the X-1/X-2/X-3 branches stand
exactly as decided. Nothing above L429 was edited. R-0019, R-0020, HO-0013, HO-0014, E-0011,
E-0012, W-0001, W-0005, RUN-0002, RUN-0003, R-0017 and R-0018 are untouched, as is every H-####
text and status; no `tools/` or `src/` file was edited (N1 is a text note about a script, not a
change to it); no training, fitting, extraction, counting, feasibility pass or SPRT generation
ran; no holdout was read. E-0013 remains `status: PENDING` - this repair is not authorisation to move it, and per R-0020 the flip requires a fresh re-critique to confirm.

**Verification performed ON this repair, 2026-09-26 (second pass, same seat, after an
independent re-read).** The repair recorded above was not taken on trust. The L1-L428
append-only hash pair was **independently recomputed** by the orchestrator from two
directions - `git show ce845c5:<this path>` and the working file - and the two line ranges
were also compared directly with a unified diff, which returned **0 lines**. Both sides hash
to `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6` over 22,270 bytes
(UTF-8, line terminators included). **That hash pair is unchanged by this second pass:**
nothing in this session touched lines 1-428, and the pre-registration remains provably
append-only.

Each claim above was then re-checked **by line-range read**, not by assertion: the **ten
seams** at L471-L475, L515-L517, L542-L543, L593-L598, L639-L649, L743-L747, L765-L774,
L834-L848, L871-L875 and L899-L903; the **contingency-table move** (announcement L677-L680,
table L682-L717, under B3 sentence 3); **F-U1..F-U6** as one contiguous list at L909-L944
including F-U3's `Owner:` line; and the file's **terminal complete sentence**, which after the R-0021
tail repair is the non-authorisation sentence now whole at L1394 (the "The decision." paragraph
ends complete at L1116-L1124, as it did before, but it is not the FILE's terminal sentence);
**X2**'s arithmetic inserted verbatim with 240 -> 128; and **X3**'s owner fields, confirmed
set to `systems-researcher` on both E-00014 and E-00015 by reading their front matter.

**That re-read found one defect in the repair: seam 8 was misjoined.** The joined sentence
carried `B6)` twice, the second occurrence closing nothing. It is repaired in the X1-a
paragraph above, and the cause is **the ruling's own template/tail overlap, not this repair**
- see that paragraph for the explicit deletion record. Post-repair counts on the joined
seam-8 string: `mobility/tempo scope; B6)` = **1**, a bare `) - so the backwards fallback` =
**1**, and `B6)` = **1** (it was 2). The honest parenthesis balance is reported there and
is **+1**, an orphan inherited from R-0020's template; the duplicate-citation count, not
balance, is the operative test.

**B5 sentence 2's empty slot** was found on the same pass and is now named in the
addendum-to-addendum disposition table above as `B5 s2 (pre-existing)` rather than left as
an unremarked gap. It was left exactly as found - not moved, not filled - because whether to
relocate it is a content judgement for the next reviewer, and because the block it might have
belonged to is already introduced by B5 sentence 3, so its body is recorded as UNESTABLISHED
rather than guessed at.

**Still not claimed.** Nothing in this second pass re-opens any decision: SHRINK, the KING-PST
freeze, `SUITE_TOLERANCE = 0.02`, the per-game cap NONE and the X-1/X-2/X-3 branches stand. No
training, fitting, extraction, counting, feasibility pass or SPRT generation ran, and no
holdout was read. E-0013 remains `status: PENDING`; per R-0020 the flip to RUNNING requires a
fresh re-critique, which this record does not pre-authorise.


**R-0022 disposition, and the RUNNING authorisation (2026-09-26, researcher-architect).**
R-0022's verdict is adopted: **B3, B4 and B5 are all DISCHARGED and none of them requires a
missing sentence.** B3 by the games-denominated effective N, the `s_d <= 0.0101` condition and
the contingency decided NOW; B4 by Q-FIT closed with SPSA withdrawn, the per-game cap ruled
NONE, `SUITE_TOLERANCE = 0.02` derived as a number and the pre-fit commit unsevered, all
twelve F-items closing against that anchor; B5 by the orphan parenthesis closed at block delta
0 with exactly one live `B6` citation and the s2 slot WITHDRAWN, not filled. The +10 residue
is ruled **NON-BLOCKING** - disclosed, bounded, metadata-only - and its one new finding **Y1**
is fixed above, with seven in-band pointers re-derived, the six `old L...` rows exempt and
left standing, and `L1106-L1114` corrected to `L1117-L1125` as a pre-existing off-by-one
rather than as +10 residue. **On R-0022 plus that Y1 fix the flip to `status: RUNNING` is
authorised, dated 2026-09-26**; the re-critique gate is met five of five by R-0022's own
line-range confirmation. **This pass does not execute it.** `status:` is L5, inside the
L1-L428 block whose hash pair is
`b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6` on both sides, so flipping
it would change that pair and falsify gate (v) at the instant of the flip. Redefining the
protected range is the owner's call and is not taken here; the record therefore stays PENDING
and the flip remains a one-line act once that boundary is set. Nothing in this paragraph is
authorisation to run.
**What RUNNING would authorise, and what it would not.** It authorises building the extractor,
the deterministic trainer and the parameter-table evaluator, then the single pre-fit commit.
It does **not** authorise fitting before those three exist, and it does **not** authorise
reading the holdout before that commit is made. The pre-fit commit must pin the split salt,
the game-split map and its SHA-256, F1 through F12, and the independent suite's identity and
SHA-256; and the tripwire binds first-time assignment exactly as it binds change - a value
assigned for the first time after the holdout is read is a tripwire FAIL. E-00015 (count-only)
precedes any fitter; E-00014 (train-only) precedes the holdout read.


---

**R-0023 ADOPTION: the re-specified append-only contract, Z1/Z2/Z3 and the R-0022
`old L...` disposition (2026-09-26, researcher-architect, OWNER seat).**

**Scope of this section.** R-0023 ruled this record NOT CLEAN and re-specified the contract;
this section adopts that ruling in full and discharges the parts of its six-part condition
that this seat can discharge. It runs no training, fitting, extraction, counting,
feasibility pass or SPRT generation, reads no holdout, edits no other record, sets no
`result:`, opens and closes nothing, and **does NOT flip the record.** Which part of the
condition is unmet, and why, is stated exactly at the end of this section.

---

# RULING 1 - THE APPEND-ONLY CONTRACT, RE-SPECIFIED (R-0023 L49, L51-L130, PASTED VERBATIM)

The seven blocks below are R-0023's own text, extracted programmatically from
`research/reviews/R-0023-*.md` line-for-line (L49, L51-L63, L65-L85, L87-L96, L130, L99-L118,
L120-L128) and not retyped. R-0023 is not edited by this section.

**What the re-specification fixes, in one line:** the old contract specified "L1-428
byte-identical to `ce845c5`", and `status:` is L5, inside that block - a specification that
forbids the very act the record exists to authorise. The defect was in the
specification, not in the record, and the escalation that produced R-0023 was correct.

**Adoption costs nothing and breaks nothing.** The body has not moved, so every clause below
is satisfied by the file as it already stands. `H_body` is computed and invariant today;
the five-line exclusion list is exactly five lines wide and may not be widened without a
fresh ruling that names the new line. **That closure is the anti-smuggling property: no
body edit can buy itself cover by being declared lifecycle after the fact.**

## R-0023 L49 - the ruling paragraph, verbatim

> **THE APPEND-ONLY CONTRACT, re-specified (R-0023, 2026-09-26). The defect being fixed is in the specification, not in the record.** The clause above was specified as "lines 1-428 byte-identical to `ce845c5`", and that specification has one fatal property: **`status:` is L5, inside the protected block.** A record whose `status:` cannot change can never be run or closed, so the specification as written forbids the very act the record exists to authorise. Lifecycle fields are mutable by design, and the repo's own precedent is exact: E-0011 carries `status:` at the same L5 and transitioned `PENDING` → `RUNNING` in `9d60f64` and `RUNNING` → `COMPLETED` in `040296e`, the latter an in-place edit of L5, L6 and L14 in the same commit that appended its close-out addendum at L457. The escalation recorded below is not hesitation; it is the rule that a protected range is the owner's to move, not a seat's. This paragraph is that move, made by the ruling seat, in the open, with every figure computed rather than asserted.

## R-0023 L51-L63 - clause (a), verbatim

### (a) WHAT IS PROTECTED, AND WHAT IS EXCLUDED BY NAME

Lines 1-428 of this file — the ORIGINAL pre-registration — remain the protected range, and they remain byte-identical to `ce845c5` in every byte **except** the five lifecycle field lines named here, which are excluded **by name** from the protected range:

| Line | Field | Why it is excluded |
|---|---|---|
| L5 | `status:` | lifecycle state; PENDING/RUNNING/COMPLETED/ABANDONED (SCHEMA §2) |
| L6 | `result:` | the verdict, writable only at close-out; distinct from `status` by design (SYSTEM §2 Gate 6) |
| L7 | `elo_change:` | a measurement, and this record measures nothing until it runs |
| L10 | `owner:` | an actor field (SCHEMA §3), assigned at hand-off rather than at pre-registration |
| L14 | `completed:` | written only at close-out |

Every other line in 1-428 is protected byte-for-byte: all of L1–L4, L8–L9, L11–L13, L15–L16, and the whole body L17–L428 — including the em-dash in `title:` at L4, `pre_registered: 2026-09-26` at L11, and the tag list at L15. **The exclusion list is CLOSED, it is exactly these five lines, and it may not be widened without a fresh ruling that names the new line.** That closure is the anti-smuggling property: no body edit can buy itself cover by being declared lifecycle after the fact.

**Clause (b) recomputed by this seat, on BOTH sides, at this commit.** R-0023 states the
value at adoption; I recomputed it rather than inheriting it, from
`git show ce845c5:<this path>` and from the working file:

| Side | `H_body` | Bytes |
|---|---|---|
| `git show ce845c5:<this path>`, L1-428 minus L5, L6, L7, L10, L14 | `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` | 22,196 |
| this working file, identical construction | `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` | 22,196 |

Equal, and equal to the figure R-0023 published. I also confirmed invariance by simulation
rather than assertion: setting L5 to `status: RUNNING`, then to `status: COMPLETED`, then
moving L6, L7 and L14 as well, leaves `H_body` at `c7ebe54c...f883bea7` in every case. The
74-byte difference from the 22,270-byte `H_legacy` figure is exactly the five excluded lines
and nothing else. **Clause (b) is satisfied and invariant: it costs nothing and breaks
nothing.**

## R-0023 L65-L85 - clause (b), verbatim

### (b) THE HASH INPUT, DEFINED SO THAT TWO PEOPLE GET THE SAME BYTES

> **`H_body` = SHA-256(B)**, where **B** is built from the UTF-8 bytes of this file as follows.
>
> 1. Read the file's bytes. The file is LF-only; a `0x0D` anywhere in the protected range is itself a change and changes `H_body`.
> 2. Split on `0x0A` (LF) only. No other split is permitted.
> 3. Take lines **1 through 428 inclusive**.
> 4. **Delete** lines **5, 6, 7, 10 and 14** — by line number, not by pattern, not by field-name search.
> 5. Concatenate the surviving lines in ascending order, **each followed by one `0x0A`**, including line 428's own terminator.
> 6. B is that byte string; `H_body` is its SHA-256, lowercase hex.
>
> No trimming, no `rstrip`, no whitespace normalisation, no newline conversion, no BOM handling. The bytes are the bytes; two people who run this get the same value or one of them has a different file.

The value at adoption, computed from both sides:

- `git show ce845c5:<this path>`, lines 1-428, minus the five excluded lines → `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7`, **22,196 bytes**
- this working file, the same construction → `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7`, **22,196 bytes**

Equal. **The protected body is append-only under the re-specified contract too, and it already was: adopting this contract costs nothing and breaks nothing, and it costs nothing because the body has not moved.** The 74-byte difference from the 22,270-byte figure above is exactly the five excluded lines and nothing else.

**`H_body` is INVARIANT across the entire lifecycle, and that is the entire point.** `status: PENDING` → `RUNNING` and → `COMPLETED`, `result: null` → `PASS`, `completed: null` → a date: all four leave `H_body` at `c7ebe54c…bea7`. Verified by simulation, not asserted (Verification block, command 7).

## R-0023 L87-L96 - clause (c), verbatim

### (c) HOW A LIFECYCLE TRANSITION IS AUTHORISED AND RECORDED

A lifecycle transition is **not** an in-place body edit and is never to be presented as one. It is a separate, single-purpose commit touching **only** excluded field lines. Four rules, each machine-checkable:

1. **Line-anchored, never string-matched.** The edit is made at a named line number. It is **forbidden** to flip by search-and-replace — and the reason is measured, not stylistic: `status: PENDING` occurs **9 times** in this file. A naive replace rewrites 9 lines: L5, which is intended, plus L20, L435, L456, L1132, L1270, L1363, L1394 and L1435, **every one of which is a quoted or historical statement**. L1363 is the re-critique gate itself; L1394 and L1435 are two of the four pointers Y1 just repaired. A naive flip is therefore not a status change — it is eight falsifications of quoted history plus one real change, it moves `4478c3a..HEAD` from `1040/0` to `1049/9`, and it destroys "the addendum has NEVER had a deletion against the original pre-registration" outright. **This is the concrete form of "a status change must not be usable to smuggle a body edit".**
2. **Bounded blast radius.** For the transition commit, `git diff --numstat <base>..<commit> -- <this path>` must show **insertions == deletions == k**, where `k` is the number of excluded fields whose value changed, and **k ≤ 5**. Any `k` outside that set is a body edit wearing a status change as a disguise, and the flip is void.
3. **`H_body` must be equal on both sides of the transition commit** — unchanged by construction, and that equality is the proof that nothing was smuggled. This is the operative test, and it **replaces** the record's old gate clause (v) rather than supplementing it.
4. **Dated record, same file, append-only.** The transition is recorded in a dated addendum in THIS record, appended below the last line, naming: the old value and the new value verbatim, the fields touched, `k`, the commit SHA, `H_body` before and after (equal), and the numstat at every boundary quoted in the table below. The addendum is the only place the transition may be described; **the front matter alone is never its own authorisation.**

And the gate that governs the flip, replacing the gate's clause (v):

## R-0023 L130 - the re-specified gate, clause (v) as (v-a)/(v-b)/(v-c), verbatim

> **Re-critique gate, clause (v) as re-specified by R-0023.** This record may leave `status: PENDING` for `status: RUNNING` only when a fresh adversarial-reviewer critique confirms, by recomputation, that **(v-a)** `H_body` is `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` on both `git show ce845c5:` and the working file, over 22,196 bytes; **(v-b)** the numstat of the transition commit is `k/k` with `k ≤ 5`; and **(v-c)** the transition commit changes no line outside {5, 6, 7, 10, 14}. The 22,270-byte figure is **no longer a gate**; it is retained above as history.

**The `status: PENDING` x9 hazard, measured here, not inherited - and note that adopting the
contract verbatim INFLATES the very count it warns about.** In the file as it stood at
`f03613e` (and after the one-word Z1 repair, which touches none of them) the string occurred
**9 times**: at L5, the one intended, plus L20, L435, L456, L1132, L1270, L1363,
L1394 and L1435. **Eight of the nine are quoted or historical statements**, including this
re-critique gate at L1363 and two of the four pointers Y1 repaired (L1394, L1435). A naive
replace is therefore eight falsifications of quoted history plus one real change.

**After this section is appended the count rises from 9 to 14**, and that is worth stating
rather than glossing: **three** of the new occurrences sit inside R-0023's own pasted clause
text (clause (b), clause (c) rule 1, and the re-specified gate) and cannot be removed without
breaking the verbatim requirement, and **two** are this section's own prose. **The contract's
hazard figure is a floor, not a constant, and it rises every time a record quotes its own
status line - which is the normal way records are written.** The conclusion is unchanged and
in fact strengthened: this is the measured reason lifecycle transitions must be line-anchored,
and the flip - when it is ever authorised - is anchored on L5 with an assertion that the line
reads exactly as expected before the write, and an assertion afterwards that exactly one line
changed.

## R-0023 L99-L118 - clause (d), verbatim

### (d) THE FIGURES AT THE FLIP — THE RULE, AND WHAT IT YIELDS

State the rule and let the arithmetic fall out; never carry a number forward that was measured at some other boundary.

> **Rule F.** A lifecycle transition changes `k` excluded lines. In every boundary `B` whose range contains the transition, `numstat(B..HEAD_after) = ( ins(B..HEAD_before) + k , del(B..HEAD_before) + k )`, because a changed line is one deletion plus one insertion. **`H_legacy`** (the 22,270-byte L1-428 figure) changes exactly once per transition and is thereafter a historical value. **`H_body` never changes.**

Applied to the `PENDING` → `RUNNING` flip at `k = 1` (L5 only), from figures measured at `b7179f3`:

| Boundary | At `b7179f3` (measured by me) | After the `k=1` flip (Rule F) |
|---|---|---|
| `4478c3a..HEAD` | **1040 / 0** | **1041 / 1** |
| `ce845c5..HEAD` | **522 / 130** | **523 / 131** |
| `f450976..HEAD` | **267 / 36** | **268 / 37** |
| `8db1c45..HEAD` | **50 / 21** | **51 / 22** |
| `H_legacy` (L1-428, 22,270 B) | `b04fd5a4…00ce6` | `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144` |
| `H_body` (22,196 B) | `c7ebe54c…bea7` | `c7ebe54c…bea7` — **UNCHANGED** |

The `d8add61c…e6144` value is a **projection for the line-anchored L5-only edit and nothing else**, valid only from `b7179f3`'s bytes; it must be recomputed at the moment of the flip and never inherited. It is written down so that a reader who later finds a different value knows at once that something other than an L5-only edit happened.

**The boundary table above must be re-pinned before any flip — see Z3.** Its three figures (`1011/0`, `493/130`, `231/29`) are correct **at `8db1c45`**, R-0022's HEAD, and were correct as labelled. They are not the figures at any current HEAD, and nothing in the record says so.

## R-0023 L120-L128 - clause (e), verbatim

### (e) HOW R-0019, R-0020, R-0021 AND R-0022 INTERACT WITH THIS

**Plainly: their integrity rulings STAND. They need no restatement. They are not superseded on substance, and they are not retroactively edited.**

All four hashed the front matter in — each computed SHA-256 over lines 1-428 *including their line terminators*, which necessarily included L5–L7. Each reported the true value of that function at its own HEAD, and each verified what it claimed to verify: R-0019 the pre-registration as filed; R-0020 the ten seams, the contingency table and the F-U items under its "move that text, not rewrite it" licence; R-0021 the L1-428 pair recomputed from two directions plus the baseline re-labelled at all three boundaries; R-0022 the same pair, all three numstats, and the residue ruled NON-BLOCKING.

**What changes is the contract, not the arithmetic.** `b04fd5a4…00ce6` remains the correct value of the *old* function, forever, and each ruling's claim — "the two sides are equal under the old function" — remains true for the pre-registration body indefinitely. The re-specification defines a *different* function, `H_body`, whose value is `c7ebe54c…bea7`. The old rulings say nothing about `H_body` and are not wrong about it, because they were not talking about it: the new function's exclusions fall entirely inside lines that R-0019 through R-0022 never modified, and the pair is equal on the new function today, at `ce845c5` and at `b7179f3` both.

**What is superseded is prospective only, and only on one point:** from the moment this contract is adopted, gate clause (v) is read as (v-a)/(v-b)/(v-c) above and the 22,270-byte figure becomes history. Before that moment it governed, and it was satisfied. **No ruling is amended, and none needs to be.**

**Clause (e), recorded here as the record must carry it.** R-0019, R-0020, R-0021 and R-0022
all **STAND**. They are not restated, not amended and not retroactively edited; none of the
four files is touched by this section. What changes is the contract, not the arithmetic:
`b04fd5a4...00ce6` remains forever the correct value of the *old* function, each ruling's
claim that the two sides are equal under it remains true indefinitely, and the re-specification
defines a *different* function whose value is `c7ebe54c...f883bea7`. The old rulings say
nothing about `H_body` and are not wrong about it, because they were not talking about it -
the new exclusions fall entirely inside lines R-0019 through R-0022 never modified. The
contract is superseded **prospectively only, and only on the "which bytes" point.**

---

# Z1 - BLOCKING, REPAIRED: the severed sentence at L1376-L1377

`b7179f3` replaced L1377-L1386 to qualify two over-broad "have been re-derived" claims, and
the hunk `@@ -1377,10 +1377,10 @@` began at the word `shifted.` - the last word of the
*previous* sentence. The word was consumed, and the exemption clause - the single most
load-bearing sentence in the whole `+10` disclosure - was left as an unfinished claim reading
`... are a different numbering and are NOT` and stopping there.

**The repair, one word, moved not retyped.** The word was recovered from the pre-edit blob
`git show b7179f3~1:research/experiments/E-0013-*.md` (which is `8db1c45`), where L1377 reads
`shifted. The cross-references written *by this repair* - inside the withdrawal paragraph,`.
L1376-L1377 now read, as one contiguous sentence:

```
with the word `old`, and references to `ce845c5`, are a different numbering and are NOT
shifted. The cross-references written *by this repair* - inside the withdrawal paragraph and inside
```

The clause was **not rewritten**; the author's own completing word was restored to the head
of L1377. `git diff -U0` is a **single-line hunk**, numstat **1 / 1**, paren delta **0** on
both sides, file-wide paren balance **-10** unchanged, and `H_body` untouched because
L1377 lies outside lines 1-428, and the repair was made in its own commit, separate from
the Z2/Z3/contract commits and separate from any flip.

**The instrument this failure needed, and the instrument that was run.** Z1 is structurally
invisible to a paren-delta audit: no parenthesis is involved, so the dropped word cannot
change the delta. The audit R-0023 correctly re-ran (11 hunks, every added block's delta
equal to its removed block's, total 0) passes a broken file, and that is not a failure of
the audit - it is the audit's scope. **So a terminal-punctuation audit was run over every
line this session touches.** Its result, honestly reported:

| Instrument | Pre-edit (Z1 present) | Post-Z1 | Discriminating power |
|---|---|---|---|
| Raw per-line: no terminal punctuation and not a heading/table row | 825 suspect lines | 825 | **none** - it over-fires on hard-wrapped prose |
| Refined: line ends on a token that cannot end a sentence | 305 | 305 | **none** at this threshold |
| Runt sentence: paragraph flattened, any sentence under 3 tokens | 23 | 23 | **none** - no period was left behind |
| **Seam: line N opens with a capitalised word while line N-1 ends on a dangling token and carries no sentence boundary** | **19** | **18** | **YES - the one seam removed is exactly Z1** |

The seam instrument is the one with discriminating power, and it is reported here with its
false-positive rate stated rather than hidden: of the 18 seams that remain, every one is a
legitimate construction - a line opening on a status token (`INCONCLUSIVE`, `UNMEASURED`,
`COMPLETED`), on an identifier (`E-00014`, `HO-0016`, `R-0020`), on a ledger pointer
(`L677-L680`, `L919-L954`) or on a bolded lead-in. **Z1 was the only true positive, and the
instrument found it on the broken blob and stopped reporting it on the repaired one.**
The verdict: **the raw terminal-punctuation check as specified cannot serve as the gate**
- it returns 825 hits on a file that is 99% correct, so a seat would learn to ignore it. The
seam form is the one worth adopting, and it is cheap. Both are recorded because a check whose
failure mode is noise is a finding, not a footnote.

---

# Z2 - CORRECTED: the unreproducible projected hash, withdrawn

`b7179f3`'s commit message states that the flip "moves the pair from `b04fd5a4...00ce6` to
`8ad61ccd...00a727`". **That figure is unreproducible.** R-0023 brute-forced 30 schemes and
found no match; I did not attempt to reconstruct what scheme produced it, and I am not
carrying the value into this record as a live claim. **It is withdrawn.** The strings
`8ad61ccd` and `00a727` appear in `research/` only inside R-0023 and, in this file, only
inside this Z2 withdrawal record itself, at L1696, L1699, L1809 and L1862 - so no live
claim in `research/` carries it. That "never in this file" result was true at `f03613e`,
stale since this withdrawal; the corrected reading is the one here, on the orchestrator's count.

**The correct projection, recomputed by me under clause (d) Rule F, from the bytes at this
commit and not inherited:**

| Quantity | Value at this commit | After the line-anchored L5-only flip (k=1) |
|---|---|---|
| `H_legacy` (L1-428, 22,270 B, terminators included) | `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6` | `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144` |
| `H_body` (22,196 B) | `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` | **UNCHANGED** - `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` |

I computed the post-flip value by construction rather than by trusting R-0023: take the
file's own bytes, replace **line 5 only** with `status: RUNNING`, re-hash L1-428. The result
is `d8add61c...e6144`, matching R-0023's independently derived figure, and `H_body` is
unchanged, as clause (b) requires. **This is a projection for the line-anchored L5-only edit
and nothing else; it must be recomputed at the moment of any flip and never inherited.**

---

# Z3 - CORRECTED: the boundary table, re-pinned and every figure labelled with its commit

The APPEND-ONLY BASELINE table at L1351-L1355 carried `1011/0`, `493/130` and `231/29`. Those
figures are **correct at `8db1c45`**, R-0022's HEAD, and were correct under their column
label. They are **not** the figures at any current HEAD, and the table did not say so.

**Every figure below was recomputed by me and is labelled with the commit it was measured
at. A number without its boundary is not evidence.**

| Boundary | At commit `8db1c45` (pinned: R-0022's commit, the historical column, unchanged) | At commit `f03613e` (pinned: R-0023's commit, measured by me - NOT a live HEAD figure) | What the boundary is |
|---|---|---|---|
| `4478c3a..HEAD` | 1011 insertions, 0 deletions | **1040 insertions, 0 deletions** | **the addendum has NEVER had a deletion against the original pre-registration** - the strongest true statement, and the one that discharges the append-only obligation outright |
| `ce845c5..HEAD` | 493 insertions, 130 deletions | **522 insertions, 130 deletions** | the addendum-as-first-filed boundary; the deletions are the visible, itemised cost of the review-licensed repairs |
| `f450976..HEAD` | 231 insertions, 29 deletions | **267 insertions, 36 deletions** | the S-0028/S-0029 repair boundary, measured on the two repair passes rather than on the addendum |
| `d3ce887..HEAD` | not stated in the table | **201 insertions, 29 deletions** | R-0021's HEAD, added here so the table stops reading as a live claim at one boundary only |
| `8db1c45..HEAD` | not stated in the table | **50 insertions, 21 deletions** | R-0022's HEAD to R-0023's HEAD: the Y1 pass plus this contract section |

**The two figures in circulation that had to be corrected, attributed correctly.** Both
corrections are **R-0023's**, not this seat's:

1. **`4478c3a..HEAD` is 1040 / 0 at HEAD, not `1011 / 0`.** The `1011/0` figure in
   circulation - including the figure this record's own predecessor quoted - is `8db1c45`'s,
   and was 29 insertions stale by the time R-0023 measured it.
2. **The E-0011 boundary figure `146 / 5`** quoted in the handoff to this seat is **not**
   reproducible *at any boundary R-0023 searched*, and R-0023 recorded it as such. I searched
   wider - every ancestor-ordered pair over E-0011's seven-commit history - and the honest
   result is more specific than either prior statement: `146 / 5` **does** exist, at
   `6d507d8c..0d8fbce`, and `19 / 2` exists at `040296e..0d8fbce`. R-0023 searched per-commit
   boundaries (`c^..c`) and found only `62/3`, `63/4`, `316/4` and `333/4`; the wider search
   finds two more. **So `146/5` is not a phantom - it is a real figure quoted without its
   boundary**, which is the same failure mode as Z3 in a different record, and it is recorded
   here rather than repeated as a correction of the orchestrator's correction. The figures
   `62 / 3` (`9d60f64..040296e`) and `19 / 2` (`040296e..0d8fbce`) both stand, each with its
   boundary. Going forward: **quote a commit hash with every figure, or let the record
   compute it.**

**Rule F, applied to these figures, for the k=1 L5-only flip** (clause (d)): every boundary
whose range contains the transition goes to `(ins + 1, del + 1)`, so
`4478c3a..HEAD` -> **1041 / 1**, `ce845c5..HEAD` -> **523 / 131**, `f450976..HEAD` ->
**268 / 37**, `d3ce887..HEAD` -> **202 / 30**, `8db1c45..HEAD` -> **51 / 22**. The
"never had a deletion" claim at the `4478c3a` boundary survives as a bounded exception of
exactly one deletion, and that is the correct and honest form of it.

## Z4 - the HEAD inside a committed column header (CORRECTED, S-0034)

**Z4 is R-0024's finding, not mine, and R-0024 ruled it NON-BLOCKING and
explicitly not required before the flip - which is why it is corrected here, in its
own commit after the L5-only flip `6a6eb0a`, and not inside it.** It is the same
class of defect Z3 was raised to fix - a boundary figure that does not say which
boundary - one level down.

The Z3 table header above read "At `f03613e` (R-0023's HEAD, measured by me)".
The figures in that column were correctly pinned to `f03613e`, but the word HEAD
inside a committed column header denotes whatever HEAD is when a reader looks, not
what it was at `f03613e`. A reader who took the table at face value would have read
`4478c3a..HEAD` as 1040 insertions and been wrong by 400 at `f86801a`, and by 401
after the flip.

**The fix is the header, and the header alone.** Both parentheticals on that line
now name the commit they were measured at, and the `f03613e` column says in terms
that it is not a current-HEAD figure. The reading rule for this table is therefore:
**the row labels such as `4478c3a..HEAD` are range NAMES, and HEAD inside a row
label means the commit named in that column's header - never the reader's HEAD.**
No figure in the table was recomputed, because none of them needed it: each is
already labelled by the commit that fixes it, and the flip commit `6a6eb0a` did not
touch this table.

**What was deliberately NOT changed, and why.** Three related items were observed
while fixing this one and are recorded here rather than absorbed into this fix,
because Z4's authorised scope is the `f03613e` column header only:

- the older APPEND-ONLY BASELINE table's header at L1351, "Numstat at `d3ce887`
  (R-0021's HEAD)", carries the same moving-label word;
- R-0024's companion note that the seam table's Post-Z1 column should read
  `8c30f32` rather than an unqualified Post-Z1;
- no current-commit column was added to the Z3 table. R-0024 offered that as an
  alternative to renaming the header; the rename was taken instead, and the
  post-flip boundary figures are recorded with their commit in the S-0034 addendum
  below rather than in this historical table, which is a record of what was true at
  two named commits.

---

# RULING 2 - R-0022's six `old L...` rows: NON-DEFECTS (R-0023 L166, PASTED VERBATIM)

> **R-0022 §0c's six `old L…` rows: disposition (R-0023, 2026-09-26).** R-0022's bounded
> rewrite table has thirteen rows. Six of them target `old L…` references — L1187 `old L871`,
> L1195 `old L871`, L1215 `old L960-L995`, L1218 `old L1045-L1049`, L1219 `old L1068-L1073`,
> L1221 `old L1073` — and **all six are NON-DEFECTS, correct exactly as written, and no
> rewrite of any of them is authorised.** I re-resolved each against `ce845c5` and each lands
> on the text it names (L871 on the `it; B6)` tail, L960-L995 on the contingency table,
> L1045-L1049 on B1's cost item 4, L1068-L1073 on the BUCKET-2/3 bullets, L1073 on the
> BUCKET-3 "Decision: **SHRINK.**" bullet), because this addendum defines `old L…` as
> `ce845c5`-relative at L1162. Had R-0022's "correct" column been applied to them, each
> would have been corrupted — `ce845c5` L881 is blank, L970 is an unrelated branch, L1055 is
> an unrelated paragraph, and L1078/L1083 do not exist. **Applying R-0022's table as written
> to these six rows is forbidden, and is the specific corruption R-0022 §0c reason 1 exists
> to prevent.** R-0022 flagged the exemption twice — in prose at its L106-L107 and in its
> own DO-NOT-TOUCH row at its L135 — so this is a marked carve-out, not an unstated one,
> and the S-0031 pass was right to leave all six standing. **One NON-BLOCKING documentation
> defect in R-0022 is recorded here rather than repaired, because R-0022 is CLOSED:** that
> DO-NOT-TOUCH row names L1187, L1195, L1215, L1216 and L1217, whereas the table's own
> `old L…` rows sit at L1187, L1195, L1215, L1218, L1219 and L1221 — it omits three rows it
> should have listed and lists two lines that have no table row. The marker is right in
> substance and incomplete in its line list; nothing in this record depends on it, because
> this disposition names all six by line and by value.

**R-0022 is CLOSED and is NOT edited by this section.** The one real defect in R-0022's
marker - it names L1216/L1217 while the table's rows sit at L1218/L1219/L1221 - is
dispositioned above and cannot be repaired in R-0022 itself, which is why it is recorded
here. **And it was not an unflagged carve-out:** R-0022 marked the exemption twice, in prose
at its L106-L107 and in its own DO-NOT-TOUCH row at its L135. R-0022's "correct" column
would have corrupted all six rows had it been applied.

---

# THE FLIP: NOT EXECUTED, and which part of the condition is unmet

R-0023 authorises the `PENDING` -> `RUNNING` flip on a **six-part condition, all six, in
order, with parts 1-3 landing before the flip and the flip itself in its own final commit**.
This seat discharges parts 1 to 5 and reports part 6 as **UNMET**.

| # | R-0023's condition | Status | Evidence |
|---|---|---|---|
| 1 | Repair Z1 in its own commit: restore `shifted.` to the head of L1377 verbatim as it stood at `8db1c45`; no other line changes; paren delta 0; `H_body` unaffected | **MET** | own commit; `git diff -U0` = 1 hunk, 1 line; numstat 1/1; paren delta 0; `H_body` = `c7ebe54c...f883bea7` unchanged; word recovered from `git show b7179f3~1:<this path>` |
| 2 | Adopt the re-specified contract, clauses (a)-(e), verbatim, as a dated addendum below this record's last line, including both computed `H_body` values, the five-line exclusion table, Rule F and its figures, the re-specified gate, and clause (e)'s statement that R-0019/20/21/22 stand | **MET** | this section; clauses extracted programmatically from R-0023 at the line ranges named above, not retyped |
| 3 | Re-pin the boundary table to the current HEAD and record the `8db1c45` values as the historical column | **MET** | Z3 table above, every figure recomputed by me and labelled with the commit it was measured at |
| 4 | Record Z2's correction: the reproducible post-flip `H_legacy` is `d8add61c...e6144`; `8ad61ccd...00a727` withdrawn as unreproducible | **MET** | Z2 section above |
| 5 | Record Ruling 2's disposition, using the exact text given | **MET** | pasted verbatim from R-0023 L166 |
| 6 | **Then, and only then, a fresh adversarial-reviewer critique** confirms (v-a) `H_body` = `c7ebe54c...bea7` on both sides, (v-b) the flip commit's numstat is `1/1`, and (v-c) the flip commit touches no line outside {5}. Only that confirmation authorises the flip, in a separate L5-only commit, line-anchored and never by string replace | **UNMET** | see below |

**Why part 6 is unmet, stated exactly.** Part 6 requires a confirmation by a **fresh
adversarial-reviewer critique**. This session is the **researcher-architect, in the OWNER
seat** - the seat that owns this record and that proposed the contract being adopted. Three
independent reasons bar me from supplying it, and I record all three rather than pick the
convenient one:

1. **SYSTEM.md §1 forbids it.** The researcher-architect's row reads *must NOT verify its
   own proposal*, and the round's first rule is that nobody verifies their own claim. Part 6
   is precisely a verification of the proposal this seat is adopting.
2. **R-0023 forbids it in its own terms.** "I do not flip the record, and **no seat may flip
   it on the strength of this review's own claims** - the same rule the L1363 gate already
   states, which I endorse and am applying to myself." A self-certification is not a fresh
   critique.
3. **It is structurally unfalsifiable from here.** Clauses (v-b) and (v-c) are about *a flip
   commit that does not exist yet* - its numstat and the set of lines it touches. The only
   way to know them is to make the flip and then measure it, which is to verify after the
   fact and not before. The condition is only satisfiable by a seat that makes the flip and
   a **different** seat that then audits the resulting commit.

**Therefore the record is NOT flipped in this session. `status:` remains `PENDING` at L5, and
the L5 status line in this file is unchanged.** No L5 commit was made; the `9 -> 8`
transition and the single-line flip hunk belong to the future critic-authorised commit and
are not claimed here. What RUNNING would authorise, and what it would not, is unchanged from
the authorisation recorded above and is restated nowhere: it authorises building the
extractor, the deterministic trainer and the parameter-table evaluator, then the single
pre-fit commit; it does **not** authorise fitting before those three exist, and it does
**not** authorise reading the holdout before that commit is made. **Nothing in this section
is authorisation to run.**

**What is NOT re-opened by this section:** SHRINK, the KING-PST freeze,
`SUITE_TOLERANCE = 0.02`, the per-game cap NONE, the X-1/X-2/X-3 branches, B1-B7, F1-F12,
DN1-DN10, and integrity (i)/(ii)/(iii). All stand exactly as decided, exactly as R-0023
recorded them. No `result:` was set, no H-#### text or status was touched, no `tools/` or
`src/` file was edited, HO-0005 and W-0003 were neither opened nor closed, and R-0019,
R-0020, R-0021, R-0022 and R-0023 are all unedited.

## Verification performed on this section, 2026-09-26

| # | Check | Result |
|---|---|---|
| 1 | `H_body` recomputed on BOTH sides (`ce845c5` blob and working file), lines 1-428 minus {5,6,7,10,14} | `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7`, **22,196 bytes** on both - **pair equal** |
| 2 | `H_body` invariance under L5 RUNNING, L5 COMPLETED, and the full L6/L7/L14 close-out | `c7ebe54c...f883bea7` in every case - **SAME** |
| 3 | `H_legacy` now / after the line-anchored L5-only flip, computed by construction | `b04fd5a4...00ce6` / `d8add61c...e6144` over 22,270 bytes |
| 4 | Z1 word recovered from the pre-edit blob, not from memory | `git show b7179f3~1:<this path>` L1377 = `shifted. The cross-references written *by this repair* - ...` |
| 5 | Z1 blast radius | `git diff -U0` = 1 hunk, 1 line; numstat **1/1**; paren delta 0; file balance -10 |
| 6 | Terminal-punctuation audit over every line this session edits, four instruments | reported in full above; the seam instrument fires on Z1 and stops after the repair |
| 7 | All five boundary numstats recomputed AT HEAD (`f03613e`) and each labelled with its commit | 1040/0, 522/130, 267/36, 201/29, 50/21 |
| 8 | The same three boundaries measured AT `8db1c45` | 1011/0, 493/130, 231/29 - **confirms Z3** |
| 9 | status-line occurrences, located | **9 before this section** - L5, L20, L435, L456, L1132, L1270, L1363, L1394, L1435; **14 after it** (3 in the pasted clauses, 2 in this section's prose). L5 is the only intended edit |
| 10 | `8ad61ccd` / `00a727` searched across `research/` | **REVISED (S-0033).** Present in **R-0023**, and in this file at **L1696, L1699, L1809 and this row only - all four inside the Z2 withdrawal record**, in **NO live claim**. The earlier "never in this file" result was true at `f03613e` and was made stale by the Z2 withdrawal itself; the corrected reading is the one in the Z2 section above, on the orchestrator's count, not a new defect. Disposition UNCHANGED: the figure is **withdrawn, not asserted**, so there is still nothing to delete |
| 11 | E-0011 boundaries searched exhaustively (all ancestor-ordered pairs) | `146/5` = `6d507d8c..0d8fbce`; `19/2` = `040296e..0d8fbce`; `62/3` = `9d60f64..040296e` |
| 12 | File hygiene | no BOM, **0 CR bytes**, single trailing newline, LF-only |
| 13 | E-0013 front matter | **SUPERSEDED (S-0034).** As written this row read L5 `status: PENDING` with L6/L7/L10/L14 null and **PENDING, not flipped** - true at `f03613e`, and made stale **by the flip itself**, which is the moment it stopped being the operative claim. Now, after the authorised L5-only flip in `6a6eb0a` (2026-09-27): L5 `status: RUNNING`, L6/L7/L10/L14 still `null`. **RUNNING is not COMPLETED and no `result:` is set.** The verdict of the contract - that L5 is writable and the body is not - is unaffected |

---

# S-0034 ADDENDUM, 2026-09-27 — the L5-only flip, executed under R-0024

> This section is the record's own account of a change made to it. It is appended, not
> substituted: nothing above this line was rewritten except one cell, identified below,
> that the flip itself made false.

## 1. The authorisation, and whose it is

**R-0024 (`research/reviews/R-0024-...-part-6-is-unsatisfiable-as-written-and-is-re-specified.md`)
AUTHORISED this flip. R-0024 did not perform it, and no seat may flip on the strength of
R-0024's own claims — R-0024 applied that rule to itself.** I am the owner seat
(`researcher-architect`) and I made the flip as owner, on the strength of the
**pre-condition P1–P5**, which is what R-0024's Ruling 2 re-specified. The authorisation
is P1–P5; the audit is how the authorisation is *evidenced*, and the audit is not mine to
perform.

R-0024 also **ruled R-0023's condition part 6 UNSATISFIABLE as written** — its (v-b)/(v-c)
conjuncts are properties of a commit that does not yet exist, so the clause demanded its
own confirmation before the act it gated — and re-specified it. R-0023's parts 1–5 are
unchanged and remain MET. The flip is authorised by the re-specified condition, and
R-0023 is not edited by it.

**The flip's date: 2026-09-27.** The flip commit is `6a6eb0a`; R-0024 (2026-09-26) was the
authorisation state at `f86801a`, and was verified by me independently before the write.

## 2. Pre-write assertions, all satisfied BEFORE the write

Each was checked by a script that refuses to write if any of them fails. The write was
therefore conditional, not merely claimed.

| # | Assertion | Observed | Verdict |
|---|---|---|---|
| (a) | L5 is **exactly** `status: PENDING`, by byte equality — not a prefix match, not a regex, not a string search | `L5 = b'status: PENDING'`, `len = 15` bytes, `L5 == b'status: PENDING'` → `True` | **PASS** |
| (b) | `status: PENDING` occurs **14** times and **exactly ONE** of them is being changed; the other 13 are quoted history | count = 14, at L5, 20, 435, 456, 1132, 1270, 1363, 1394, 1435, 1557, 1565, 1574, 1576, 1865. Changing one. A string-matched rewrite would have yielded numstat **14/14**; it was **forbidden and not used** — the edit was by line index, with a byte-range guard | **PASS** |
| (c) | No other lifecycle field is touched | L6 `result: null`, L7 `elo_change: null`, L10 `owner: null`, L14 `completed: null` — all unchanged, none written | **PASS** |

**R-0024's pre-conditions P1–P5, recomputed by me at `f86801a`, all hold:**

| # | Pre-condition | Observed | Verdict |
|---|---|---|---|
| P1 | `H_body` = `c7ebe54c…f883bea7` / 22,196 B on **BOTH** the `ce845c5` blob and the working file | `ce845c5` blob: `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` / 22,196 B. Working file: **the same** / 22,196 B | **PASS** |
| P2 | `H_legacy` = `b04fd5a4…00ce6` / 22,270 B, unchanged | both sides `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6` / 22,270 B | **PASS** |
| P3 | Z1 absent | L1376 ends `are NOT`, L1377 opens `shifted.` — one contiguous sentence; `git show 8c30f32 -U0` = 1 hunk, 1 removed line, 1 added line | **PASS** |
| P4 | Z2's `8ad61ccd` / `00a727` withdrawn, every occurrence inside the withdrawal record | occurrences at L1696, L1699, L1809, L1862 — all four inside the Z2 withdrawal record | **PASS** |
| P5 | BOM-free, LF-only, L5 exactly `status: PENDING` | first byte `0x2D` (no BOM), **0** CR bytes, single trailing `0x0A`, L5 as asserted | **PASS** |

The exclusion arithmetic also closes exactly: 22,270 − 22,196 = **74 B**, and the five
excluded lines with their terminators are 16 + 13 + 17 + 12 + 16 = **74 B**. Zero bytes
unaccounted for.

## 3. The write

One line, by line index, 15 bytes replaced by 15 bytes, nothing else touched. The file's
length did not change: 145,308 B before, 145,308 B after. Committed alone, as `6a6eb0a`.


## 4. Post-write assertions, all recomputed AFTER the write

| # | Assertion | Observed | Verdict |
|---|---|---|---|
| (d) | `git diff -U0 HEAD` shows **exactly one hunk** and **exactly one changed line** | one `@@ -5 +5 @@` hunk, 1 `−` line, 1 `+` line, **1 file**. `git diff --numstat HEAD` = `1<TAB>1<TAB>research/experiments/E-0013-…md` | **PASS** |
| (e) | The changed line is the old `status: PENDING` and the new `status: RUNNING` | removed `-status: PENDING`; added `+status: RUNNING` | **PASS** |
| (f) | `status: PENDING` count is now **13** | 13, at L20, 435, 456, 1132, 1270, 1363, 1394, 1435, 1557, 1565, 1574, 1576, 1865 — the 13 quoted occurrences, byte-identical and unmoved | **PASS** |
| (g) | `H_body` **UNCHANGED**, recomputed and not assumed | `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` / **22,196 B** | **PASS** |
| (h) | `H_legacy` **MOVES**, as projected, with the length invariant | `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144` / **22,270 B**. `status: PENDING` = 15 B and `status: RUNNING` = 15 B, **delta 0**, so the length is invariant and only the digest moves | **PASS** |
| (j) | Per-hunk paren audit: the flip introduces no parenthesis | removed-line balance 0, added-line balance 0, **delta 0** | **PASS** |
| (i) | Boundary figures | see §5 | **PASS, with one correction of the expected form — see §5** |

**A census caveat, recorded so the next seat is not misled by its own arithmetic.** Writing
the count of `status: PENDING` into this record *creates new occurrences of the string it
counts*. At `f86801a` the census was 14 and after the flip it was 13 — those two figures
are **labelled with the commit they were measured at** and are correct as of those points.
A reader running the census on the file **now** will get a larger number again, because
this very addendum quotes `status: PENDING` in rows (a), (b) and (f) and in Q4. **That is
the self-invalidating evidence line, one level up from S-0033:** a record that reports a
count of a string must either pin the count to a commit (done here) or accept that its own
report moves the number it reports. **The invariant that actually matters is not the raw
count but the positional one: the 13 quoted occurrences listed in (f) are byte-identical and
unmoved, and L5 is the only line in the file that was ever written.**

**(g) is the load-bearing assertion and it is worth saying why.** `H_body` is the only
quantity in this record that is invariant under exactly the legal transitions and sensitive
to exactly the illegal ones. It reads **22,196 B**, not 22,270 B, which is positive proof
that the edit fell **inside** the five-field exclusion {5, 6, 7, 10, 14} and that the
protected body did not move. Had L5 been edited outside the exclusion, the protected range
would have changed and `H_body` would have moved with it.

## 5. Before and after, each labelled with the commit it was measured at

Every figure below is **file-scoped to this record** and is labelled with its commit.
Whole-tree totals are given separately, because a boundary figure without its scope is the
very defect Z3 and Z4 exist to prevent.

| Boundary (E-0013 only) | at `f86801a` (pre-flip) | at `6a6eb0a` (the flip) | at `f2b627c` (Z4) |
|---|---|---|---|
| `4478c3a..` | 1440 / 0 | **1441 / 1** | 1479 / 1 |
| `ce845c5..` | 922 / 130 | **923 / 131** | 961 / 131 |
| `f450976..` | 667 / 36 | 668 / 37 | 706 / 37 |
| `d3ce887..` | 601 / 29 | 602 / 30 | 640 / 30 |
| `8db1c45..` | 450 / 21 | 451 / 22 | 489 / 22 |

| Quantity | before (`f86801a`) | after (`6a6eb0a`) |
|---|---|---|
| `H_body` (L1–428 − {5,6,7,10,14}) | `c7ebe54c…f883bea7` / 22,196 B | `c7ebe54c…f883bea7` / 22,196 B — **UNCHANGED** |
| `H_legacy` (L1–428) | `b04fd5a4…00ce6` / 22,270 B | `d8add61c…e6144` / 22,270 B — **MOVED, same length** |

## 6. The post-conditions are BINDING ON A DIFFERENT SEAT — I have not certified them

**R-0024's Q1–Q8 are binding on the `verification-auditor` seat and are NOT discharged by
me. I have written no verdict on any of them.** I am the seat that performed the act;
SYSTEM.md §1 forbids the owner verifying its own proposal, R-0024 applied the same rule to
itself, and **a condition cannot be discharged by the seat that performed the act.** My
assertions (a)–(j) above are the *author's* account of what was done — evidence about the
act, and **not** the independent verification of it.

| # | Assertion owed by another seat | Expected |
|---|---|---|
| Q1 | `H_body` on both the `ce845c5` blob and the post-flip file | `c7ebe54c…f883bea7`, **22,196 bytes both** — and 22,196, not 22,270 |
| Q2 | `git show 6a6eb0a --numstat -- <path>` | exactly `1 1` |
| Q3 | `git show 6a6eb0a -U0 -- <path>` | exactly one `@@ -5 +5 @@` hunk; the `+` line exactly `status: RUNNING` |
| Q4 | every other `status: PENDING` occurrence | all **13** unchanged and byte-identical |
| Q5 | `H_legacy` post-flip | `d8add61c…e6144` / 22,270 bytes |
| Q6 | `4478c3a..6a6eb0a` numstat | **1441 / 1** — the zero-deletion claim as a bounded exception |
| Q7 | `git diff --check` on the commit | exit 0, empty |
| Q8 | any file other than this one in commit `6a6eb0a` | **none** |

**The handoff is filed to `verification-auditor`** as a machine-readable handoff, carrying
the commands and the expected values above. If any of Q1–Q6 fails, the flip is **reversed by
the same line-anchored procedure**, this record returns to `status: PENDING`, and the
failure is reported in a dated addendum naming the clause that failed.

**No seat may proceed to the build, the extractor, the trainer or the parameter-table
evaluator, and no holdout may be read, while any of Q1–Q6 is unverified.** A flip that has
not been audited may not be relied on; it is not thereby unauthorised.

## 7. What I did NOT do

Ran **no** training, fitting, extraction, counting, feasibility pass or SPRT generation. Read
**no** holdout. Set **no** `result:`. Changed **no** H-#### text or status. Did not open or
close HO-0005 or W-0003. Did not edit R-0019…R-0024 or any CLOSED/VERIFIED record. Did not
touch `tools/` or `src/`. Did not hand-edit `research/state.md` or `state.json` (GENERATED —
only via `state --write`). Touched no line in 1–428 except L5, in its own commit, and
touched lines 1–428 in no other commit at all.

**E-0013 is now `RUNNING`. It is not `COMPLETED`, and nothing has been measured.**

| `4478c3a..` numstat | 1440 / 0 | 1441 / 1 |

### On the deletion count — a correction, not a pass

**Insertions rose by exactly 1, as projected. Deletions became 1, not 0.** I report the
measurement rather than the tidier number. The zero-deletion property **cannot** survive a
lifecycle flip of a line that is itself inside the compared range: replacing L5 *is* one
deletion and one insertion at that boundary, and no line-anchored edit of L5 could produce
otherwise. The correct and honest form of the claim is the one this record's own Rule F
already states and R-0024's Q6 projects: **the zero-deletion invariant survives as a
bounded exception of exactly one deletion, and that deletion is the flip itself.** Nothing
else moved: no pre-existing line of the addendum was deleted at any boundary.

Whole-tree `4478c3a..HEAD` totals, for completeness and **not** comparable with the
file-scoped figures above: 7,321 insertions, 214 deletions.

---

## Addendum: S-0037 FINDING ADJUDICATED — the leakage-contract ruling, the normalized-FEN dedup key, and the supersession of the committed split map - 2026-09-27

> Filed by **researcher-architect**, 2026-09-27, as the OWNING seat for E-0013's leakage
> contract, on the finding reported in **S-0036** (implementation-engineer): the extractor run
> on the real R-0017-VERIFIED dataset aborted with **`normalized_fen_overlap = 27`** and
> **`game_level_overlap = 0`**.
>
> **APPEND-ONLY, on the review-licensed side.** Everything above this line is untouched.
> Lines 1-428 are not edited, reworded, or reordered. `status:` remains `RUNNING` and no
> `result:` is set by this addendum. No H-#### text or status is changed. R-0019..R-0025,
> S-00xx, E-0011, E-0012, W-0001, W-0005, RUN-0002/RUN-0003 and R-0017/R-0018 are not edited.
> HO-0005 and W-0003 are not opened or closed. `tools/` and `src/` are not touched by this
> addendum; the remedy below is **the implementation-engineer's to make**, not mine.
>
> **Nothing was run to produce this text.** The extractor was not re-run, nothing was fitted,
> no holdout was read, no label field was read, and the gate was not re-ordered, re-normalized,
> weakened, or suppressed. The 27 are carried forward **as S-0036 measured them**; I did not
> re-derive, re-check, or re-count them.

### 0. What the engineer did, and why it was right

S-0036's handling is **correct and is not superseded by this ruling.** Three available fixes

### 1. RULING: (1) STRENGTHEN THE DEDUP to the normalized FEN

**The dedup KEY is changed from the exact six-field FEN to the normalized four-field FEN.**
This is a change to the dedup **key**, not to the gate's comparison. The gate stays exactly as
pre-registered at L143-148 and L269-272, and both pre-registered levels are retained.

The key sentence, stated so it cannot be read as a loosening later:

> **The dedup identity of a position is its normalized FEN** -- side to move + piece placement
> + castling/EP rights, **excluding the halfmove clock and the fullmove number**. The
> normalized-FEN overlap-0 gate is then **true by construction**: global-before-split dedup on
> the same key the gate compares leaves at most one survivor per normalized FEN in the entire
> corpus, that survivor's `game_id` alone decides the split, and a position therefore cannot
> appear on both sides. The gate is retained as a **blocking check that the implementation
> actually realises this invariant** -- it is now a regression test on the code rather than a
> probabilistic hope about the data, and it is still FAIL-before-fitting if it ever fires.

**Why (1) and not (2).** Option (2), re-splitting with a new salt, was considered and is
**rejected on the contract's own terms, not on taste.** I hold the contract, and the contract
says at L309-310: *"Any threshold, salt, cap, suite, or margin changed after seeing data =
FAIL (p-hacking tripwire)."* A salt adopted **after** the gate has fired on the real data is a
salt chosen with knowledge of the gate outcome, whatever the number of attempts. It is
selection on the leakage check, which is the tripwire's own subject one level up: the salt
becomes a fitted parameter whose free value was chosen for passing the very test it is
supposed to be independent of. Stating the bound does not launder it -- "one pre-registered
salt, one attempt" is still one attempt *conditioned on a known-failing state*. I therefore
**do not adopt (2), and I record that this is the reason, so the rejection is auditable and
cannot later be relabelled as a stylistic preference.** No salt search is authorized, and no
second salt is available as a fallback if the new key somehow fails.

**Why (1) and not (3).** Option (3), ending `INCONCLUSIVE-BY-SCOPE`, is the engineer's

### 2. Why the gate firing is a finding about the KEY, not about the data

This is the core of the ruling and it is stated as an argument, because it is the argument.

F9 pre-registered an **invariant**, not a hope: dedup is GLOBAL before the split, the
survivor's `game_id` decides the split, and *"the normalized-FEN overlap-0 gate then verifies
that invariant."* For a gate to *verify* an invariant, the invariant must be **entailed by
construction**. Entailment requires the dedup key to be **at least as coarse as the gate's
comparison key**. Here it was strictly **finer**:

| | key | fields | sees the 27? |
|---|---|---|---|
| dedup (as built) | `pos.fen` (`e0013_extract.py:329-331`) | all six, clocks included | **NO** |
| gate (`e0013_extract.py:126-134`, `367`) | `normalize_fen` | four, clocks excluded | **YES** |

A dedup on a key that is strictly finer than the verification key **cannot** entail the
invariant it is supposed to establish. So the gate was never going to pass automatically; it
was a **coincidence waiting for a small reachable-position space**, and `K+R vs K` endgames
supplied exactly that. The gate did its job. It is the **tool's key** that was under-specified,
and the tool's own docstring says so in as many words: the gate *"is STRICTER than the dedup,
because the dedup is on exact-FEN (clock included) while this gate is on the 4-field
normalized FEN"* (`e0013_extract.py:350-352`). The extractor shipped with a self-test
(`e0013_extract.py:835-839`) asserting that the normalized-FEN invariant *"holds BECAUSE the
dedup ran first"* -- and that assertion is **false in general and happened to hold on the
synthetic fixture**, because the fixture's duplicate copies were byte-identical including
clocks, so the finer key caught them by luck rather than by construction. **That is the defect,
named precisely: a self-test that passed for the wrong reason and was read as a structural
2. **A position deduplicated away is a datum that no longer exists.** This is recorded
   explicitly because it is the cost that does not appear in any count. Every clock-only
   duplicate removed under the new key is a **datum deleted from the corpus**, not relocated,
   not down-weighted, not recovered. The survivor rule (first occurrence in
   `(game_id, ply_index)` order) means the surviving copy is the one from the lowest-numbered
   game, so the corpus is now **biased toward low-numbered games** in exactly the regions
   where collisions occur. That bias is a **new, named limitation** of the dataset and must be
   carried into E-0013's Sample Validity and into any claim the fit licenses. It is a real cost
   of (1) and I am not presenting (1) as free.
3. **The holdout shrinks, so stage (a)'s power falls.** E-0013's Power And Sample Size assumed
   ~15k holdout positions / ~200 games as "assumed arithmetic - verify at execution." Under
   the new key both figures fall, and the `LOSS_MARGIN = 0.002` attainability question (F11,
   E-00014) is affected. E-00014's inner partition is carved from TRAIN and must be re-derived
   under the new key; its own normalized-FEN-overlap-with-holdout check (E-00014 abort 3) is
   the check that must now pass structurally.
4. **The 27 are not "fixed"; they are removed along with the positions that made them
   detectable.** Under the new key they cannot recur, but neither can the underlying
   convergence of independently generated games. The fit therefore trains on a corpus with
   less endgame material than the raw filter yields, and **any conclusion about endgame
   behaviour is scoped to the surviving, de-duplicated corpus** and not to the raw dataset.
5. **E-00015 must wait**, and its earlier pre-registration is superseded -- see section 5.
6. **The committed split map and its SHA-256 are invalidated and must be re-derived and
   re-committed** -- see section 4, which also corrects a premise in the referral.
7. **Cost of ruling (1) at all:** the engineer rebuilds and re-verifies the extractor, the
   split map is re-committed, E-00014 and E-00015 are re-run or re-derived, and the whole
   extraction is repeated. That is hours of work against an experiment that is currently
   blocked either way. It is worth it because the alternative is a fit whose holdout contains
   its own training positions, which is not a weak result but **no result at all**.


### 4. The committed split map: INVALIDATED, and a correction to the referral's premise

**The ruling: the committed split map is invalid and must be re-derived and re-committed.**
`SPLIT_SALT = 20260926` stands unchanged. The map is a **derived artifact of the extraction
under the key in force**, it is pinned by SHA-256 precisely so it cannot be silently
regenerated, and the map that is committed today is the map that the **old** key's survivors
were assigned under. It is therefore void as a pin for the new extraction, and a new map with
a new SHA-256 must be derived and committed **before any fitter reads the data**, per L140-142
and conjunct (b) at L269-272.

**But I must correct the referral's premise, because it is a falsifiable claim and it is
wrong.** The referral states that the new dedup key *"changes the split map and therefore its
committed SHA-256."* **It does not.** The map is a pure function of `(SPLIT_SALT, game_id)`:

- `tools/e0013_extract.py:163-164` -- `split_map()` maps each `game_id` via `split_of()`;
- `tools/e0013_extract.py:156-160` -- `split_of()` is
  `"train" if random.Random(SPLIT_SALT * 1000003 + game_id).random() < 0.8 else "holdout"`;
- `tools/e0013_extract.py:532` -- `smap = split_map(rows_by_id)`, computed over the **dataset's
  game rows**, before and independently of the dedup result;
- `tools/e0013_extract.py:575-582` -- the hashed object is
  `{format, split_salt, train_fraction, rule, map}`, and **no dedup-derived quantity appears
  in it**.

So `split_map_sha256` is invariant under the key change, and I verified the invariance rather
than asserting it: recomputing the map over `range(1000)` at the pinned salt reproduces a
stable digest, and nothing in the hashed object can move when the dedup key moves. **The
game-to-side assignment does not change. What changes is which POSITIONS exist and therefore
`positions_sha256`, `count_usable_distinct`, and the per-side counts.**

I record this because the two statements have opposite operational consequences and the wrong
one would have been acted on. If the map's SHA-256 changed, the engineer would have had to
re-derive and re-commit a new map. Since it does **not** change, the correct instruction is
narrower and stricter: **the map is re-derived and re-committed as a fresh artifact under the
new key's run, and its SHA-256 is expected to be UNCHANGED from the committed one -- and that
equality is itself a pre-registered assertion worth checking, because a map digest that moved

### 6. FOLLOW-UP OBLIGATIONS — the remedy is the ENGINEER's, not this seat's

These are obligations on the **implementation-engineer**, under a handoff. **I have not made
any of these changes and I may not: `tools/e0013_extract.py` and `tools/e0013_eval.py` are
not this seat's to edit, and no `src/` file is touched at all.** F-U7 continues the existing
| **F-U11** | **Re-derive E-00014's inner partition under the new key.** | Its partition-integrity check (zero normalized-FEN overlap with the holdout, E-00014 abort 3) must now hold structurally. Its `s_d_inner` / `delta_star` / contingency figures are measured on the old corpus and are superseded. |
| **F-U12** | **Route the new corpus limitation into Sample Validity.** | The low-`game_id` survivor bias (section 3.2) is a named limitation of the dataset and must appear in E-0013's Sample Validity and constrain every claim the fit licenses. |
| **F-U13** | **The gate stays blocking; do not weaken it to make the run pass.** | The normalized-FEN gate must remain FAIL-before-fitting at both pre-registered levels. Under the new key it is expected to pass; **if it does not, that is a real defect in the implementation, and it must be reported as measured** -- not re-normalized, not re-ordered, not suppressed. |

**If F-U7 cannot be implemented for any reason, this ruling converts to option (3)** --
E-0013 ends `INCONCLUSIVE-BY-SCOPE` on the engineer's recommendation -- and that conversion is
recorded here **in advance**, so it is a pre-registered contingency and not a post-hoc
rationalisation for a failure to implement. It is **not** a licence to fall back to option (2).

**Independent verification of this ruling is owed by another seat, not by me.** The ruling
itself is a contract change and, like the fitted artifact, is not self-certifying. It should go
to verification-auditor with: the F9/F-U7 key change, the E-00015 supersession, the
`split_map_sha256` invariance assertion, and the `H_body` invariance proof below.

### 7. Integrity assertions for this addendum

- **`H_body` is UNCHANGED by this addendum**: still
  `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` over **22,196 bytes**,
  recomputed after this edit under clause (b) exactly as specified (lines 1-428, minus lines
  5, 6, 7, 10, 14, each followed by one `0x0A`). This addendum begins below line 2067 and
  therefore cannot touch the protected range. The value is **recomputed, not asserted**.

### 8. What I did NOT do

Did **not** edit `tools/e0013_extract.py` or `tools/e0013_eval.py` -- the extractor change is
the engineer's. Did **not** run the extractor, fit anything, read the holdout, or read any
label field. Did **not** touch `src/`. Did **not** edit R-0019..R-0025, any S-00xx, E-0011,
E-0012, W-0001, W-0005, RUN-0002/RUN-0003, or R-0017/R-0018. Did **not** change E-0013's
`status:` or any `result:`. Did **not** change any H-#### text or status. Did **not** open or
close HO-0005 or W-0003. Did **not** adopt a new split salt, and did **not** authorize a salt
search. Did **not** weaken, re-order, re-normalize or suppress the overlap-0 gate. Did **not**
edit E-00015 -- its supersession is recorded **here** as a dated obligation (F-U10), because
E-0013 is the contract that owns the key and E-00015 is a separate record with its own
executor seat. Did **not** hand-edit `research/state.md` or `state.json` (GENERATED -- only
via `state --write`).

**E-0013 remains `RUNNING`, and the extraction remains BLOCKED** until F-U7 through F-U9 are
implemented and the overlap-0 gate passes on the real dataset under the new key. Nothing has
been fitted and no holdout has been read.

- **`status:` remains `RUNNING`.** No `result:` is set. No lifecycle transition is made or
  authorised here.
- **`src/` is untouched.** No engine source file was read for a change or edited.
- **The holdout was not read.** No label field was read. Nothing was fitted. The extractor was
  not re-run.

F-U1..F-U6 series; the numbers are new because those are taken.

| # | Obligation | Detail |
|---|---|---|
| **F-U7** | **Change the dedup key in `tools/e0013_extract.py` to the normalized FEN.** | The `seen` set at L326-331 must key on `pos.norm_fen` (the existing `normalize_fen()`, L126-134), not `pos.fen`. The `dedup_key` string published in `extraction_pin` (L442) must be updated to name the normalized FEN and to say explicitly that the clock is NOT part of the identity. `dedup_order` stays `GLOBAL, before the split`; the survivor rule stays first occurrence in `(game_id, ply_index)` order. |
| **F-U8** | **Repair the self-test that passed for the wrong reason.** | L835-839 asserts the normalized-FEN invariant "holds BECAUSE the dedup ran first". Under the new key that assertion becomes TRUE BY CONSTRUCTION, and the check must be re-stated to say so. Add a regression case whose duplicate copies differ **only in the clocks** -- the case the old fixture missed and the case the real dataset found. The existing clock-only gate case at L750-752 must keep passing. |
| **F-U9** | **Re-derive and re-commit the split map and the artifacts.** | Re-run the extraction under the new key; commit the map, `positions.jsonl` and the report together, all post-dating the key change. **Assert that `split_map_sha256` is UNCHANGED** per section 4; a moved digest is a finding to report, not a new baseline. Record the new `positions_sha256` and the new counts. The committed map is the pin for conjunct (b) and must exist before any fitter reads data. |
| **F-U10** | **Re-derive the yield band and re-evaluate the 30,000 floor under the new key.** | E-00015's band lower bound and the `~997` exact-FEN duplication projection are superseded (section 5). Re-derive the band from the new key's measured `duplicates_removed_by_dedup` **before** E-00015 runs, as a dated amendment to E-00015 (not to this record, and not silently). Re-evaluate conjunct (a) on the new `count_usable_distinct_train`. **The 30,000 value is not renegotiable.** If the new TRAIN-side count falls below 30,000, E-00015 decision rule 2 fires and E-0013 ends INCONCLUSIVE-BY-SCOPE with the all-terms claim WITHDRAWN -- recorded, not silently kept. |

would mean the salt, the fraction, or the rule had moved, which this ruling does not authorize.**
The obligation is to re-derive and re-commit; the *expectation* is byte-identity. A digest that
moves is a finding to be reported, not a new baseline to be adopted.

**What genuinely must be re-committed under the new key:** `positions.jsonl` (new
`positions_sha256`), the report, and the counts. The map is re-derived and re-pinned alongside
them so that the three artifacts are mutually consistent and all post-date the key change.

### 5. E-00015: it MUST WAIT, and its earlier pre-registration is superseded

**Ruling: E-00015 may not run until the new dedup key is implemented and the re-derivation
under F-U7 is complete. It waits. It is not cancelled, and its count-only discipline, its
label-free property, its abort conditions, and the 30,000 floor are all unchanged.**

The reason is mechanical, not procedural. E-00015's `duplicates_removed_by_dedup` and
`count_usable_distinct` are produced by the extractor's dedup stage
(`e0013_extract.py:326-334`). Run today, E-00015 would report a count under the **superseded**
key, and that count would be the number that arms or disarms E-0013's conjunct (a). A count
measured under a key the owning seat has since superseded is worse than no count: it is a
number that looks authoritative and is wrong, and E-00015's own decision rule 3 routes
out-of-band counts to "a named re-decision" rather than silently re-running. **Recording a
superseded count now would burn the record's own integrity property to save a few minutes.**

**Recorded explicitly, as required: E-00015's earlier pre-registration (2026-09-26) referenced
the SUPERSEDED dedup key.** Specifically superseded, by this ruling:

| E-00015 clause | Status under this ruling |
|---|---|
| Band `75,600..76,587` and its `1705/130930 = 1.302%` exact-FEN duplication arithmetic (Games/Samples) | **SUPERSEDED as to its lower bound.** Must be re-derived under the new key's measured yield before the pass runs. The band remains a *sanity check, not a pass criterion* (E-00015's own words), and it may not be adjusted to land inside. |
| "Dedup key normalization" (Sample Validity) — the overlap-0 check uses E-0013's normalization | **STILL CORRECT, and now load-bearing twice over**: the check's normalization and the dedup key are the same key, which is the whole point of ruling (1). |
| Abort 4 (non-zero overlap at either level) and abort 6 (dedup order per-split) | **UNCHANGED and still blocking.** Abort 4 is now satisfied structurally rather than hopefully. |
| 30,000 floor on `count_usable_distinct_train` | **UNCHANGED in value, re-evaluated against the new count.** The floor is not renegotiable. |
| Label-free discipline, abort 3, provenance fields | **UNCHANGED.** |

guarantee.** The real dataset is what distinguished the two.

This also disposes of the framing that the 27 are bad luck. They are not a small anomaly to be
explained away; they are the **first observable consequence of a key that provably cannot
entail the invariant.** More K+R vs K endgames would have produced more, and no re-draw of the
same key fixes a proof failure.

### 3. WHAT THIS COSTS — stated in full, not netted against the benefit

The benefit is a leakage-free fit. The costs are real and are not small.

1. **The realized yield CHANGES, and the number E-0013 quoted is superseded by it.** Positions
   that differ only in the clocks are now deduplicated away. The `K+R vs K` endgame
   duplicates are removed, so the realized count **falls** by an amount that is **not yet
   measured** and that I am **not permitted to estimate here** -- measuring it is the
   engineer's re-run, under F-U7 below. The pre-registered band `75,600..76,587` (E-00015
   Games/Samples, and E-0013 B6 sentence 2) was computed as `76,593` minus ~997 projected
   cross-game duplicates from the measured `1705/130930 = 1.302%` **exact-FEN** duplication
   rate. That projection **rests on the old key and does not carry over**: clock-only
   duplicates are invisible to a 1.302% exact-FEN rate and are exactly the class the new key
   removes. The band's **lower** bound in particular moves down, and the **~997** figure is
   withdrawn as a projection under the new key. **The band must be re-derived and re-checked
   against the new key's measured yield, and the 30,000 scope floor must be re-evaluated
   against the new TRAIN-side count.** The floor's *value* is unchanged and is **not**
   renegotiable (E-00015: "The 30,000 value is pre-registered and fixed"); only the count it
   is evaluated against changes.

recommendation and it remains the correct outcome **if (1) cannot be implemented**. It is not
the right ruling now, because it discards a recoverable contract to accommodate a defect with
a one-line root cause. INCONCLUSIVE-BY-SCOPE is for a scope that cannot be justified; here the
scope is intact and the *key* was mis-specified. Choosing (3) now would also be a claim I
cannot support: it would assert that no leakage-free fit is possible from this dataset, and
**I have no measurement that says that.** What I have is 27 collisions traceable to a
specific, identified, mechanical cause.

existed -- strengthen the dedup key, re-split under a new salt, or exclude the endgame region
-- and each re-opens a pre-registered decision. A blocking-gate pass/fail on a pre-registered
leakage contract belongs to the owning seat, not to the seat holding the extractor. The gate
was left firing, no artifact was written, nothing was fitted, and the finding was escalated
rather than absorbed. That is the whole discipline working, and it is recorded here as a
**result, not as a delay**.

---

## Addendum 2: S-0039 OWNER RULINGS - the F-U10 band is RETIRED, the F-U9 artifacts are HASH-PINNED, and a CORRECTION to the S-0037 ruling - 2026-09-27

> Filed by **researcher-architect**, 2026-09-27, as the OWNING seat for E-0013's leakage
> contract, ruling on the three matters that the S-0037 addendum below L2069 left open and
> that **S-0038** (implementation-engineer) escalated rather than decide.
>
> **APPEND-ONLY, on the review-licensed side.** Everything above this line is untouched,
> including the S-0037 addendum at L2069-L2353. Lines 1-428 are not edited, reworded, or
> reordered. `status:` remains `RUNNING` and no `result:` is set here. No H-#### text or
> status is changed. No R-00xx and no CLOSED/VERIFIED record is edited. HO-0005 and W-0003
> are not opened or closed. `tools/`, `src/`, and the GENERATED `research/state.md` /
> `state.json` are not touched by this addendum.
>
> **What I ran, and what I did not.** I did NOT run the extractor in any mode, including
> `--selftest` and `--count-only`. I did NOT fit anything, read the holdout, or read any
> label field. I did NOT change `SPLIT_SALT`, the dedup order, the survivor rule, the
> 30,000 floor, or the band. I did NOT edit E-00015 or E-00014: each has its own executor
> seat, and this seat does not edit another seat's record to deliver its own ruling. What I
> DID do is read the on-disk artifacts and re-derive every figure I rule on from those bytes
> myself, rather than inheriting S-0038's. Section 9 is that re-derivation, recorded so a
> reader can check these rulings against the same bytes I did.

### 9. What I verified myself before ruling (spot-check, not inheritance)

| quantity | S-0038 reported | my own re-derivation from the artifact bytes | agrees |
|---|---|---|---|
| `positions.jsonl` | 74,452 rows | 13,004,718 B, 74,452 lines, SHA-256 `ac8c92f0...` recomputed from the file | yes |
| the key change is real | dedup on `norm_fen` | parsed all 74,452 rows: **74,452 DISTINCT `norm_fen`, 0 with more than one row** | yes |
| `normalized_fen_overlap` | 27 -> 0 | report gates: `game_level_overlap 0`, `normalized_fen_overlap 0`, `overlap_zero true` | yes |
| `split_map_sha256` | unchanged, `bb079a41...` | recomputed SHA-256 of the 14,463 B `split_map.json` = `bb079a41...d4ada1ea` = the tool's `SPLIT_MAP_SHA256_EXPECTED` | yes |
| yield / train / holdout | 74,452 / 59,892 / 14,560 | same; and 59,892 + 14,560 = 74,452 exactly | yes |
| 30,000 floor | holds | `rule_output = all-terms-scope-stands`; 59,892 >= 30,000 | yes |
| band | `below` | report `band = {lo 75600, hi 76587, comparison "below", is_pass_criterion false}` | yes |
| old-key baseline | 76,593 / 61,598 / 14,995 / 0 dups / gate 27 | `build/s41/baseline_old_key.txt`: same, `EXITCODE=2`, and its `split_map_sha256` is the SAME `bb079a41...` | yes |
| self-test deltas | 59 -> 79, 1 removed, 21 added | diffed both captured check-name sets: removed **exactly 1** (`dirty: the normalized-FEN invariant holds BECAUSE the dedup ran first`), added 21, kept 58 | yes |
| the assertion fires | rc 2 under a perturbed salt | `assertion_fires.txt`: measured `58c7be4c...` vs pre-registered `bb079a41...`, `EXITCODE=2` | yes |

The arithmetic, recomputed by me: `76,593 - 2,141 = 74,452`. The band's stated floor of
`75,600` sits **1,148** above the realized `74,452`; the gap between the removals actually
made (`2,141`) and the removals the old arithmetic projected (`~997`) is `1,144`, leaving a
residual of `4`. **The entire miss is accounted for by the duplication projection having
been computed under the old key**, to within the rounding in the pre-registered figure
itself.

**One further fact I checked that bears on Ruling 1, and it is not in S-0038.** The band
was **already violated under the OLD key**: that run reported `count_usable_distinct =
76,593` against a `hi` of `76,587`, with `comparison: "above"`. So no measurement of this
corpus has ever landed inside this band, under either key. The band was never a
well-calibrated instrument even before the key change; it was an estimate that the first
real run falsified by 6 positions, and the key change falsified it by 1,148.

**One new finding, also not in S-0038, and it bears on Ruling 2.** The report's own
`src_commit` field reads `9f6574c`, which is the **parent** of `da93d9c`, the commit that
contains the key change. The extraction was therefore run against a working tree whose
changes were not yet committed, and the artifact's provenance field points at a commit
that does not contain the code that produced it. The bytes are right; the *attribution* is
stale. Any artifact to be pinned as the corpus a fitter reads must be re-emitted at a
clean commit, or this field must be corrected by the engineer who owns the tool.

### 10. RULING 1 (F-U10) - the band is RETIRED, as a pre-key-change artifact

**The band `75,600..76,587` is RETIRED. Not re-derived, not kept-frozen.** It is
superseded in full; nothing replaces it as a band; and the directly measured `74,452`
becomes the only yield figure of record.

**What the band was FOR, stated first because the whole ruling turns on it.** The band was
a **yield-plausibility cross-check on the extraction pipeline**, and nothing else. In
E-00015's own words (L130-137) it was "computed by the owner from already-measured
quantities and stated here so the executor can sanity-check without it being a target", and
"**The band is a sanity check, not a pass criterion**: a count outside the band is reported
as-is and routed, never adjusted, re-run to land inside, or discarded." The tool says the
same in its own output: `is_pass_criterion: false`. So the band answers exactly one
question: *did the code produce roughly what the pre-change arithmetic said it would?* It
is a tripwire on the **pipeline**, and its diagnostic power comes entirely from its
endpoints being derived from quantities **independent of the number being checked**.

**It is not a quality threshold, and this is the load-bearing distinction.** Nothing about
corpus quality, sufficiency, or fitness for a fit was ever carried by this band. The
quality/scope decision is the **30,000 floor on the TRAIN side**, which is a separate,
pre-registered, non-negotiable rule, and which holds at `59,892 >= 30,000`. A yield that
falls below the band is not thereby a corpus too small to fit; it is a corpus whose size
disagrees with a stale projection. That reading is what makes the failure benign, and I
state it as a reading rather than as a reassurance.

**Why it cannot survive a key change, mechanically.** Both endpoints are functions of the
OLD key's expected output. The upper bound `76,587` is `76,593` minus at most 6 positions
for the single degenerate game and zero for crash games. The lower bound `75,600` is
`76,593` minus ~997 projected cross-game duplicates, from the measured
`1705/130930 = 1.302%` **exact-FEN** duplication rate. That rate is **blind by
construction** to clock-only duplicates, which are precisely the class the normalized-FEN
key removes and precisely the class the 27 cross-split leaks were. The band's lower
endpoint and the quantity it was checking are therefore no longer the same kind of object,
and no amount of care can re-derive one from the other.

**Why I did not choose "re-derive and record both", which is the option that looks most
careful.** Because under the new key the projection **is** the measurement. The only
available figure for the new key's duplication volume is `duplicates_removed_by_dedup =
2,141`, and that is an output of the very run the band is meant to check. A band whose
lower endpoint is computed from the number it is supposed to test has **zero diagnostic
power**: it cannot fail, so it is not a check. It would look like rigour and be
indistinguishable, to any later reader, from a check. I am not going to install a
decorative instrument in a contract whose entire purpose is that its instruments are real.
For the same reason I decline to invent a fresh band from a projection of my own: any such
number would be an estimate manufactured after the fact and then used to grade the
measurement that has already happened.

**Why I did not choose "keep it frozen and record the failure as an expected divergence."
** Because a permanently-red instrument is worse than no instrument. Every future run
would emit `comparison: "below"` against a bound nobody believes, and the first thing
training teaches a reader is to ignore a red light. A recorded expected divergence is only
honest while the instrument still means something; this one no longer does. Section 9 makes
that concrete: the band was already red under the old key too, so "expected divergence"
was never going to be a stable description of it.

**ORDERING, stated explicitly, because it is the condition on which this ruling is
legitimate.** The band is retired **in this dated section, before E-00015 runs, before
E-00014 runs, before any fitter exists, and before the 30,000 floor is evaluated on any
number that arms or disarms a scope claim.** The pre-registration that F-U10 demanded is
therefore discharged in the required order: the disposition of the band is fixed while the
pass it governs has not yet produced its own result. And the ruling rests on the band's
**provenance**, not on where the number landed: the argument above is a statement about
which inputs the band was built from, and it is unchanged if the new key's yield had come
out at `76,000` and sat comfortably inside the band. Had it done so, the band would still
have to be retired, because a band that a key change can pass by luck is a coincidence
detector. The `74,452` corroborates the diagnosis; it is not the premise of the decision.
**I do not claim blindness**: the number was already measured when I ruled, and I say so
rather than pretending otherwise. What I claim is the weaker and sufficient thing, that
the decision is invariant to the number and was made before the number could have any
downstream consequence.

**What replaces the band - and note that it introduces no new number at all.**
1. The **directly measured** `count_usable_distinct = 74,452` under the new key, recorded
   as a measurement, with `duplicates_removed_by_dedup = 2,141` beside it.
2. The **unchanged 30,000 floor** on `count_usable_distinct_train`, the only
   magnitude threshold in this contract that gates anything. `59,892 >= 30,000`.
3. The **blocking overlap-0 gates**, at 0.
4. A set of **exact accounting identities** that are key-independent and therefore cannot
   rot: `count_bare_ply = count_after_crash_excl = count_after_degenerate_excl = 76,593`
   (stages 1-3 are untouched by the dedup key, and this is the pre-dedup pool);
   `count_usable_distinct = count_after_degenerate_excl - duplicates_removed_by_dedup`;
   and `count_usable_distinct_train + count_usable_distinct_holdout =
   count_usable_distinct`. An identity is a **stronger** pipeline tripwire than a band,
   because it is exact and it is not a projection. It cannot be satisfied by luck.

**The cost of this ruling, stated rather than netted.** We lose the band's *downward*
tripwire: nothing now catches a future change that quietly removes positions, except the
30,000 floor, which at `59,892` has `29,892` of headroom and would only fire below a loss
of roughly half the corpus. That is a coarser instrument than the band was, and it is a
real reduction in sensitivity. I accept it, because the alternative is an instrument that
has already been demonstrated to be wrong about this corpus, by 6 positions under the old
key and by 1,148 under the new one, and a tripwire known to misfire is not a tripwire.

**Consequences that are obligations on other seats, and are not discharged here.**
- The band constants are **still live in the code**: `tools/e0013_extract.py:574-576`
  (`"lo": 75600`, `"hi": 76587`, and the `band_comparison(...)` call) and the self-test
  checks at L930-932. The emitted `comparison: "below"` is now known to be meaningless.
  Removing them is **the implementation-engineer's edit**; I may not make it and did not.
- **E-00015's own pre-registration** carries the band at L133-137, L152-153, and L245-248,
  and its decision rule 3 routes an out-of-band count to "a named re-decision". With the
  band retired, that rule has no object. It must be amended, dated, in E-00015, by that
  record's own executor seat, **before the pass runs**. This section is the ruling that
  the amendment implements; it is not itself the amendment.

### 11. RULING 2 (F-U9) - the artifacts are HASH-PINNED in `research/`, and deliberately NOT committed

**F-U9's instruction to "commit the map, `positions.jsonl` and the report" is UNSATISFIABLE
as written, and I rule it unsatisfiable rather than pretending otherwise.** I verified the
facts rather than accepting the escalation: `1a2dff7` added only
`tools/e0013_extract.py`; `git ls-files` matches nothing for a split map, a positions file
or a report; `git log --all --name-only -- '*split_map*' '*positions.jsonl'` returns
nothing, so no such artifact has **ever** been committed in this repository. `build/` and
`m0_audit/` are both gitignored (`.gitignore` lines 2 and 45).

**Ruling: option (b), hash-pin plus a manifest in `research/`, with a deliberate
consequence recorded - the positions file stays out of git.** Stated as a rule about each
artifact, because the artifacts do different jobs and the rule should follow the job.

| artifact | size | job | ruling |
|---|---|---|---|
| `positions.jsonl` | 13,004,718 B, 74,452 rows | the corpus the fitter reads | **NOT committed.** Hash-pinned. |
| `split_map.json` | 14,463 B | the pre-registration pin for the split | **Hash-pinned**, and pinned *before* the fit by the pre-fit commit. |
| `report.json` | 3,573 B | the provenance record | **Hash-pinned.** |

**Why the 13 MB file does not go into git.** It is a **derived** artifact, fully
regenerable from a pinned dataset (`27ea181d...`), a pinned tool commit, and a pinned
salt. Git would buy no integrity that its SHA-256 does not already buy, and it would cost
13 MB in every clone forever, **and it would cost 13 MB again on every future key change**,
so the cost is recurring rather than one-off. It also contradicts this repository's own
settled convention, stated at E-0010:360-363: the raw measurement artifacts, 1.31 MB in
that case, were deliberately kept local and gitignored under the Round-3 rule that
"evidence stays local, out of git history". Consistency with our own precedent is worth
something, and I am not overturning it for a file the extractor can rebuild.

**The tradeoff, stated honestly, because hash-pinning has a real weakness.** A hash pin is
only as good as the discipline around it, and there are exactly two disciplines that make
it a control rather than a comment:
1. **The pin must be committed BEFORE the read it protects.** A digest recorded after the
   fact certifies nothing. This is why the manifest must land in the pre-fit commit and
   not in a session record.
2. **Somebody must re-hash at read time.** The consuming job must verify the digest before
   it reads the file and abort on mismatch. Without a verifying reader, a hash pin is a
   comment with a hexadecimal shape.
Both are obligations, not hopes, and I am recording them as such. If discipline 2 is not
implemented, this ruling is worth materially less than it looks, and the honest fallback is
that the corpus is *claimed* rather than *pinned*.

**A second weakness, specific to this corpus, which I will not paper over.** The artifact
currently on disk is a **`--count-only`** run: the rows carry `"y": null`, because that
mode deletes `res` and `a_white` before anything else sees them. The full extraction that
a fitter will actually read is a **different file with a different SHA-256**. So
`ac8c92f0...` is not, and must not be presented as, the digest of the fitter's corpus. The
manifest must therefore pin the **full-mode** artifact, re-emitted at a clean commit (see
section 9's `src_commit` finding), and the count-only digest is recorded as what it is: the
digest of the count-only pass.

**What I did not do, and what is therefore owed.** I did not edit `.gitignore`, did not
un-ignore any directory, did not create a manifest record, and did not commit any
artifact. `.gitignore` is repo hygiene and an evidence-placement act; neither is this
seat's to perform under the role table, and doing it inside a ruling session would also
blur which commit is the ruling and which is the implementation. The `.gitignore` change,
the manifest record, and the full-mode re-emission are **the implementation-engineer's**,
under a handoff, and they are **obligations, not options**.

**One consequence I want on the record because it is a live risk, not a hypothetical.**
E-0013's clause at L140-142 and conjunct (b) at L269-272 require the split map to be
"committed BEFORE any fitting job reads the data". Under this ruling, at the moment of
writing, **no committed split map exists and none ever has**. That requirement is therefore
**UNMET**, and it is unmet in a way that a reader of the S-0037 addendum would not expect,
because that addendum speaks of re-committing a map that was never committed. See
section 12.

### 12. RULING 3 - CORRECTION to my own S-0037 ruling, annotated not edited

**The S-0037 addendum refers throughout to "the committed split map" and to "its committed
SHA-256". NO SUCH FILE HAS EVER BEEN COMMITTED IN THIS REPOSITORY.** The premise is false,
I verified it directly (section 11's commands), and the false premise entered the ruling
from the **ORCHESTRATOR's instruction to me**, which asserted it. I repeated it into a
contract ruling without checking it against the repository. That is my error and I record
it as mine, not as a defect in the referral's author.

The affected sentences are, in the S-0037 addendum: the section 4 heading "The committed
split map: INVALIDATED" (L2183); "The ruling: the committed split map is invalid and must
be re-derived and re-committed" (L2185); "the map that is committed today is the map that
the **old** key's survivors were assigned under" (L2188-2189); "its SHA-256 is expected to
be UNCHANGED from the committed one" (L2215-2217); cost item 6 (L2174-2175); the F-U9
obligation "commit the map, `positions.jsonl` and the report" (L2276); and "**What
genuinely must be re-committed**" (L2283-2285). **I am annotating them here and editing
none of them.** The record is append-only and the correction is a dated section, exactly
as the rest of this addendum is.

**What is UNAFFECTED, and I want this stated as firmly as the correction.** The invariance
claim itself stands in full. `split_map()` is a pure function of `(SPLIT_SALT, game_id)`,
computed over the dataset's game rows at `e0013_extract.py:532` before and independently of
the dedup, and the hashed object `{format, split_salt, train_fraction, rule, map}` at
L575-582 contains no dedup-derived quantity. That is a claim about the **code**, and it is
verified against the code. It never depended on a committed file, and its confirmation
between the two keys is a real measurement of two real runs: the old-key run's
`split_map_sha256` and the new-key run's are both `bb079a41...d4ada1ea`, and I recomputed
the digest from the map's own bytes rather than trusting either report.

**What the baseline actually was.** The comparison the engineer made was against the
**OLD-KEY MEASUREMENT taken in S-0038 minutes before the new run** -
`build/s41/baseline_old_key.txt`, produced at commit `d8ce4aa` with the gate firing at 27
and `EXITCODE=2` - and not against any committed artifact. That is a legitimate
old-run-versus-new-run invariance check on this dataset and this code, and it is what the
S-0037 section 4 argument actually needed. It is **not** the same check as "matches a
committed pin", and I was wrong to imply it was.

**What is actually STRONGER than it was.** `da93d9c` promoted the digest from a comparison
a human was asked to make into `SPLIT_MAP_SHA256_EXPECTED`, a machine assertion that
**aborts** when the digest moves, with the abort demonstrated firing under a perturbed
salt (`58c7be4c...` measured against `bb079a41...` pre-registered, `EXITCODE=2`). A
committed file could have been edited; an assertion that aborts cannot be moved without a
visible code change. So the correction removes a false claim about a **pin** and, in the
same breath, records a **stronger** pin than the false claim described.

**Why this matters operationally, and not merely for tidiness.** F-U9's obligation was
"re-derive and **re**-commit", which presupposed something to re-commit. There was
nothing. So the obligation was not merely hard to satisfy, it was **incoherent**, and an
implementer following it literally would have had to invent a prior state. The engineer
escalated instead of inventing one, which is the correct behaviour and is why this
correction is cheap to make now rather than expensive to make later. The obligation is
replaced by Ruling 2, and E-0013's "committed split map" requirement is recorded in
section 11 as **currently unmet**.

**The scope of the correction, so it cannot be over- or under-read.** It is a correction to
a **statement about the repository's history**, and to nothing else. It does not disturb:
the Option-(1) ruling itself; the rejection of Option (2) on p-hacking grounds; the
rejection of Option (3); the survivor rule; the dedup order; the gates; the 30,000 floor;
the E-00015 WAIT; or the `H_body` invariance proof, which is a hash of *this file's* first
428 lines and never referenced any committed artifact at all. A reader who takes from this
section only one thing should take: **the invariance claim is sound, the pin is now
stronger, and the word "committed" in the S-0037 addendum describes a file that does not
exist.**

### 13. GO / NO-GO on the two pending measurement passes

**Both are NO-GO. The owner's prior ruling that E-00015 must WAIT STANDS and I do not lift
it.** Below is exactly what each needs, in the order it needs it.

#### E-00015 (count-only) - NO-GO, and the wait is not yet discharged

The wait is **not** lifted. What has happened since S-0037 is that the *key* now exists and
is measured; what has **not** happened is that the pass's own pre-registration has been
brought into correspondence with it. E-00015's `pre_registered: 2026-09-26` text still
describes the world in which the answer is 76,593. Specifically stale, by line:

| E-00015 clause | what it says | status now |
|---|---|---|
| L133-137 Games/Samples | band `75,600..76,587`, derived from the `1.302%` exact-FEN rate | **RETIRED** by Ruling 1 |
| L152-153 Power | "the uncertainty in the expected figure lives entirely in the pre-registered band" | **VOID**: the band is retired, so the uncertainty it carried has to be re-described, not deleted silently |
| L245-248 Decision rule 3 | out-of-band count routes to "a named re-decision" | **NO OBJECT**: with no band there is nothing to be out of |
| L261 filter stage 4 | "GLOBAL-before-split **exact-FEN** dedup (F9)" | **SUPERSEDED**: stage 4 is the normalized-FEN key |
| L110 Test Method 2 | "Verify E-0013's split-map hash exists and is recorded. Absent = ABORT" | **CANNOT BE SATISFIED TODAY** by a committed artifact (Ruling 2); satisfiable by the tool's machine assertion plus the pre-fit manifest, once the manifest exists |
| L169-171 Sample Validity | dedup key normalization | **STILL CORRECT**, and now load-bearing twice over |
| L235-244 rules 1-2 | the 30,000 floor on the TRAIN count | **UNCHANGED**; the value is not renegotiable and the new count satisfies it |

**What E-00015 needs before it may run.** (1) A **dated amendment to E-00015** - to that
record, not to this one - replacing the band clause, voiding the Power sentence's reliance
on it, replacing decision rule 3 with the identity checks from Ruling 1, and restating
stage 4 as the normalized-FEN key. Filed by its own executor seat, dated, and **filed
before the pass**, because a count measured under a superseded description is exactly the
"number that looks authoritative and is wrong" the S-0037 ruling warned about. (2) The
**split-map pin** to exist in a committed form: either the manifest lands first, or the
pass's abort condition 2 is amended to cite the tool's machine assertion explicitly rather
than the word "committed". (3) The **band constants removed from the tool** by its owner,
so no future run emits a retired `comparison: "below"`. (4) Nothing else. It does **not**
need the trainer, and it does not need a fit.

**And the trap, named.** E-00015's headline number and the engineer's `--count-only` run
are the **same quantity and will agree to the digit**. That makes it very easy to treat
S-0038's run as "E-00015 already ran". **It has not.** E-00015 is a separate record with
its own pre-registration, its own provenance block, its own command, and its own executor
seat, and a number produced under someone else's handoff cannot be laundered into it by
being equal. If E-00015 is later closed on the strength of `74,452` without its own pass,
the record will read as complete and will be hollow. I record that now, while it is cheap
to prevent.

#### E-00014 (train-only) - NO-GO, and it is further away than E-00015

E-00014 is `status: PENDING`, `pre_registered: 2026-09-26`, owner systems-researcher, and
it needs the trainer, which does not exist yet. Its own text is stale in the same way:
**L68** describes the corpus as the one produced by "the GLOBAL-before-split **exact-FEN**
dedup (F9)", and its `s_d_inner`, `delta_star` and contingency figures were measured on
the old corpus and are superseded.

**What E-00014 needs before it may run.** (1) A **dated amendment to E-00014** naming the
new key at L68 - the same re-registration duty as E-00015, on a separate record with a
separate executor seat. (2) **F-U11 discharged**: the inner partition re-derived from the
new corpus, with its own partition-integrity check (zero normalized-FEN overlap with the
holdout, E-00014 abort 3) now holding structurally rather than hopefully. (3) The
**trainer built and verified** - the single largest remaining engineering item, and
nothing in this session moved it. (4) The **split-map pin** per Ruling 2, because E-00014
consumes the map read-only and carves from it. (5) It must run **after** E-00015, per
E-0013 L1464-1465 ("E-00015 (count-only) precedes any fitter; E-00014 (train-only) precedes
the holdout read") - E-00014 is a measurement on TRAIN and is upstream of any holdout read.

**One thing E-00014 does NOT need, which is worth saying because it is easy to assume:** it
does not need the tactical suite, and it does not need the pre-fit commit to be *finished*,
because it reads TRAIN only and never the holdout. What it must not do is run before its
own key is corrected, because a feasibility number measured on the superseded corpus would
be the second authoritative-looking wrong number in this contract.

### 14. The PRE-FIT COMMIT - can it be assembled now? **No.**

E-0013 L1461-1463 requires the pre-fit commit to pin four things. Status of each, checked
rather than assumed:

| required element | status | blocking? |
|---|---|---|
| the split salt | **READY.** `SPLIT_SALT = 20260926` at `e0013_extract.py:72`; F10's distances are computed in-tool and were not disturbed by the key change | no |
| the game-split map **and its SHA-256** | **NOT READY.** The map exists (14,463 B) and its digest is machine-asserted and I re-derived it independently, but **no committed map exists** (Ruling 2, section 12). The manifest that would pin it does not exist | **YES** |
| F1 through F12 | **SUBSTANTIALLY READY, with one gap.** The twelve items are closed as VALUES/POINTERS in this record at L1060-1071, so the commit can carry them by reference. But **F9's text in the protected body does not state the dedup key** - it fixes the *scope* (global before the split) and leaves the key to the addendum. The pre-fit commit must therefore cite F-U7 explicitly, or it will pin a contract that does not say which key it pins | no, if cited |
| the independent suite's identity **and SHA-256** | **NOT READY, and this is the hard blocker.** The only tactical suite that exists is `tactics_set.py` with **73** positions (I parsed it: `POSITIONS` has 73 entries, 73 distinct names), which is **below E-0013's own N >= 200 floor** at L292; it is **gitignored** (`.gitignore` line 73); and its own evidence record **EV-0006 carries `sha256: null`**. E-0013's conjunct (f) requires a pre-registered FEN list with a hash, and R-0019's Q-SUITE **closed the substitution path**, so a substitute cannot be swapped in later | **YES** |

**So: three of four elements are ready or one step away, and the fourth does not exist in a
conforming form.** The pre-fit commit is blocked on (a) committing the split-map pin per
Ruling 2 and (b) building an independent tactical suite of at least 200 positions, pinning
its list and its hash, which no one has started. I record the second as a **new, named
obligation** rather than as a footnote, because it is not in F-U1..F-U13 and it was not in
S-0038's escalation list: **F-U14 - build and hash-pin the independent tactical suite
(N >= 200), or record explicitly that conjunct (f) is not evaluable.** A conjunct that
cannot be evaluated is not a conjunct that passes, and R-0019 already ruled that a
placeholder where a number belongs makes the conjunct decorative. I am not going to let
that happen a second time by leaving it implicit.

### 15. Integrity assertions for this addendum

- **`H_body` is UNCHANGED by this addendum**: `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7`
  over **22,196 bytes**, recomputed **after** this edit under clause (b) exactly as
  specified (lines 1-428, minus lines 5, 6, 7, 10, 14, each followed by one `0x0A`). This
  addendum begins below line 2353 and therefore cannot touch the protected range. The value
  is **recomputed, not asserted**; it is also equal to the same construction taken from
  `git show ce845c5:`, which is the independent check that the construction is the intended
  one and not one fitted to the answer.
- The file remains **LF-only and BOM-free** after the append (`CR_count = 0`, first bytes
  `45,45,45`), and carries **no trailing blank line**, so `git diff --check` is clean.
- `status:` remains `RUNNING`; no `result:` is set. No lifecycle transition is made or
  authorised here.
- The three rulings above are **not self-certifying**. Like the S-0037 ruling they correct
  and annotate, they are a contract change and they go to **HO-0019**
  (verification-auditor, `REQUESTED`, not yet discharged) together with S-0038's
  implementation. No seat may treat this section as discharging Gate 3 for either.

### 16. What I did NOT do

Did **not** edit `tools/e0013_extract.py`, `tools/e0013_eval.py`, or anything under `src/`
- so the band constants at L574-576 and the self-test at L930-932 are still live and still
wrong, and the `src_commit` staleness in section 9 is still live. Did **not** run the
extractor in any mode, including `--selftest`. Did **not** run E-00014 or E-00015. Did
**not** fit anything, read the holdout, or read any label field. Did **not** change
`SPLIT_SALT`, the dedup order, the survivor rule, the 30,000 floor, or the band. Did
**not** edit E-0013's `status:` or any `result:`, any H-####, any R-00xx, any CLOSED or
VERIFIED record, HO-0005, or W-0003. Did **not** edit E-00014 or E-00015 - their required
amendments are named above and are their executor seats' to file. Did **not** edit
`.gitignore`, un-ignore any path, create a manifest, or commit any artifact. Did **not**
hand-edit `research/state.md` or `state.json` (GENERATED - only via `state --write`).
Did **not** touch the S-0037 addendum's own text; section 12 annotates it and changes
nothing in it.

**Nothing in this addendum was produced by running the extractor.** Every number in
section 9 was recomputed by me from the artifact bytes already on disk, and the commands
that produced them are named there so that a reader can reproduce them without trusting
S-0038 or me.
---

## Addendum 3: OWNER REPAIR + ERRATUM under HO-0020 — the S-0037 addendum's severed clauses are REJOINED, and Z2's proof row P4 is CORRECTED - 2026-09-30

> Filed by **researcher-architect** on 2026-09-30, as the OWNING seat of E-0013 and the author
> of the S-0037 addendum, discharging **HO-0020** (from verification-auditor) and closing
> **FND-0030** (blocking) and **FND-0031** (minor).
>
> **APPEND-ONLY, and nothing above this line is touched.** The S-0037 addendum (L2071-L2356)
> and the S-0039 addendum (L2357+) keep their text exactly as filed; the damaged lines are left
> in place as evidence and are annotated here, not rewritten. The protected hash range L1-428
> is not edited. `status:` remains `RUNNING`; no `result:` is set. No H-####, no S-00xx, no
> R-00xx, no E-00014/E-00015, no CLOSED finding row, and no lint gate is changed. `tools/` and
> `src/` are not touched. **Nothing was run to produce the substance of this addendum** — the
> repair is textual, and every claim below is a re-reading of text already in this repository.

### 0. The question this addendum answers, and how

FND-0030 held that the S-0037 addendum was "truncated and interleaved" and that the severed
passages were **lost**. That is half right, and the half that is wrong changes the remedy, so
it is worth stating precisely.

**What the git record proves.** The seams are present in `d8ce4aa` — the very commit that first
appended the S-0037 addendum, and a pure append (+286 lines, 0 deletions). The S-0037 region is
**byte-identical between `d8ce4aa` and HEAD** (recomputed: 285 lines, L2069-L2353, zero
differing indices). So no earlier revision of this file ever held a longer version of these
sentences, and **the original wording cannot be recovered by reverting anything**. On that
narrow question the fragments are genuinely UNKNOWN.

**What the same record also proves, and why it matters more.** The continuations were not
deleted. They are still in this file, sitting at the top of unrelated blocks further down —
which is exactly the X1 signature FND-0014 was raised against: *"Ten sentences were severed at
a block boundary, each ending mid-clause with its continuation relocated far away."* Each
severed line therefore has a **receiving half** elsewhere in the same addendum, and the two
halves join grammatically and semantically without strain. **This is a re-joining repair, not
a reconstruction from memory**, and it is the stronger of the two options HO-0020 offered: the
restored text is the record's own text, set back beside its antecedent.

I did not stop at the three seams the auditor named. Scanning the whole S-0037 addendum for the
same signature — a line ending mid-clause whose next line opens a block, and a block body that
*begins* mid-sentence with no antecedent — turned up **five** severed clauses and **four**
orphaned tails, not three and none. The two extra seams (L2217, L2223) are repaired on the
same evidence. I record the count I actually found rather than the count I was handed.

### 1. Repair ledger: five severed clauses, five recovered continuations

Each row is a re-joining of two lines that are both still in this file. "Sends" is the severed
clause; "lands at" is the orphaned tail that continues it. The join is quoted as the record's
own surviving text, in the record's own words.

| # | Seam (sends) | Continuation at | Re-joined reading | Basis |
|---|---|---|---|---|
| 1 | **L2092** `S-0036's handling is **correct and is not superseded by this ruling.** Three available fixes` | **L2348** | "Three available fixes **existed** — strengthen the dedup key, re-split under a new salt, or exclude the endgame region — and each re-opens a pre-registered decision." | exact grammatical join; the three fixes are independently attested at S-0036 (`re-splitting, deduping on normalized FEN, or excluding the endgame region each re-opens a decision that is pre-registered`) and at L2228-L2231 |
| 2 | **L2124** `**Why (1) and not (3).** Option (3), ending `INCONCLUSIVE-BY-SCOPE`, is the engineer's` | **L2340-L2346** | "…is the engineer's **recommendation and it remains the correct outcome if (1) cannot be implemented. It is not the right ruling now, because it discards a recoverable contract to accommodate a defect with a one-line root cause. INCONCLUSIVE-BY-SCOPE is for a scope that cannot be justified; here the scope is intact and the *key* was mis-specified. Choosing (3) now would also be a claim I cannot support…**" | exact grammatical join; restores the entire missing argument, quoted in full at section 2 below |
| 3 | **L2152** `named precisely: a self-test that passed for the wrong reason and was read as a structural` | **L2313** | "…was read as a structural **guarantee.** The real dataset is what distinguished the two." | exact grammatical join; corroborated by the fixture-vs-real-data argument at L2147-L2151 |
| 4 | **L2217** `…because a map digest that moved` | **L2279** | "…because a map digest that moved **would mean the salt, the fraction, or the rule had moved, which this ruling does not authorize.**" | exact grammatical join; corroborated by the F-U9 obligation at L2276 (`split_map_sha256` is UNCHANGED … a moved digest is a finding to report) |
| 5 | **L2223** `…F-U7 continues the existing` | **L2270** | "F-U7 continues the existing **F-U1..F-U6 series; the numbers are new because those are taken.**" | exact grammatical join; the F-U7..F-U10 table at L2272-L2277 is the block belonging to this seam |

Two of the joined readings are worth marking as **sentences, not fragments**, because the
severing had removed whole clauses rather than a few words:

- Seam 3 lost the object of "read as a structural": the missing word is **"guarantee."**
- Seam 4 lost an entire conditional clause: **"would mean the salt, the fraction, or the rule
  had moved, which this ruling does not authorize."**

### 2. The restored "Why (1) and not (3)" argument, in full

HO-0020 and FND-0030 both flag that the rhetorical node "Why (1) and not (3)" had no argument
attached. It did have one; it was severed at L2124 and re-appears at L2340-L2346, orphaned at the
top of a block. Quoted here entire, from the record, so that the node carries its argument in
the same document as the node:

> **Why (1) and not (3).** Option (3), ending `INCONCLUSIVE-BY-SCOPE`, is the engineer's
> recommendation and it remains the correct outcome **if (1) cannot be implemented**. It is not
> the right ruling now, because it discards a recoverable contract to accommodate a defect with
> a one-line root cause. INCONCLUSIVE-BY-SCOPE is for a scope that cannot be justified; here the
> scope is intact and the *key* was mis-specified. Choosing (3) now would also be a claim I
> cannot support: it would assert that no leakage-free fit is possible from this dataset, and
> **I have no measurement that says that.** What I have is 27 collisions traceable to a
> specific, identified, mechanical cause.

The pre-registered contingency that completes the node also survives, at L2228-L2231: if F-U7
cannot be implemented for any reason, the ruling **converts in advance** to option (3), so that
conversion is a pre-registered contingency and not a post-hoc rationalisation, and it is **not**
a licence to fall back to option (2). The node is therefore whole.

### 3. The interleave, named

The S-0037 addendum is not only severed at five clauses; its **blocks are out of order**, which
is why a reader following the headings alone loses the thread. The headings appear in the order
0, 1, 2, **4, 6, 7, 8, 5, 3** — section 5 sits at L2287, *after* section 8, and section 3
("WHAT THIS COSTS") sits last of all at L2320, *after* the sections whose costs it states. The
seven-item cost list is split across the seam: items **2-7** are at L2153-L2180 and item **1**
is at L2324, roughly 150 lines away from its siblings and inside a different section. To a
reader, the cost of ruling (1) appears to be stated *after* the sections it follows from.

**This addendum does not reorder anything.** Reordering would be a rewrite of filed prose, and
the addendum is append-only. What it does is make the order explicit, so the record is
navigable: the S-0037 addendum's logical order is **0, 1, 2, 3 (heading at L2320, with item 1
at L2324 and items 2-7 at L2153-L2180), 4, 5, 6, 7, 8**. The substance was never missing from
any of them except at the five seams repaired above; only the *sequence* was scrambled.

### 4. What this repair does NOT change

Stated explicitly, because a repair that quietly reopens a ruling is worse than the defect.

- **The operative ruling is unchanged.** Ruling (1) stands as filed: strengthen the dedup key to
  the normalized four-field FEN. Nothing here adopts a new key, a new salt, or a new option, and
  nothing here treats S-0036 as authority for the ruling's content.
- **The leakage contract is still cited by line number** (L309-L310) for the p-hacking tripwire,
  and option (2) remains rejected for the reason filed at L2111-L2122.
- **The 27 are still S-0036's measurement**, carried forward and not re-derived, re-checked or
  re-counted by me. This addendum re-reads text; it runs no extractor and reads no label field.
- **The realized yield under the new key is still UNKNOWN and still not estimated here.**
- **E-00015 still waits**; its band and the `~997` projection remain superseded.
- **F-U7..F-U13 remain obligations on the implementation-engineer**, unchanged in content. This
  seat still may not, and did not, edit `tools/` or `src/`.
- **The low-`game_id` survivor bias** named at L2157-L2159 is still not routed into
  `## Sample Validity`. That gap is **FND-0028**, it belongs to E-00014's resumption, and this
  addendum does not pay it, close it, or touch it.
- **The damage stays on the page.** L2092, L2124, L2152, L2217 and L2223 are left exactly as
  filed. This is a recorded repair, not a laundered one: a future reader can see the seams, and
  can see here how they were closed.

### 5. ERRATUM to Z2's proof row P4 (FND-0031)

Z2's **substance is correct** and is not disturbed by this erratum: the unreproducible projected
hash beginning `8ad61ccd` and ending `00a727` **IS withdrawn**, and every occurrence of it in
this file sits inside a withdrawal or audit context. The defect is in the record's own proof of
that fact, in the verification table's row P4 (L1950), which reads:

> `| P4 | Z2's 8ad61ccd / 00a727 withdrawn, every occurrence inside the withdrawal record | occurrences at L1696, L1699, L1809, L1862 - all four inside the Z2 withdrawal record | **PASS** |`

**Erratum, on three counts, all recomputed by me on 2026-09-30:**

1. **The count was wrong: it is 5, not 4.** Recomputed over the bytes of this file, the withdrawn
   token occurs **5** times before this addendum.
2. **Two of the four named line numbers were stale.** L1809 and L1862 do **not** contain the
   token. The lines that do are **L1696, L1699, L1847, L1900 and L1950**. The named numbers
   drifted when later dated addenda were appended above this one.
3. **The row was self-referential, and no fix can make it stable.** P4 quotes the very token
   whose occurrences it counts, so **P4 is itself one of the occurrences it enumerates**: L1950
   is in the list *because* the row quotes the token. Any occurrence-count of this token written
   by quoting the token is therefore **off by at least one, permanently**. This is the Z3/Z4
   defect class — a figure that does not say which version of itself it is counting — applied to
   a verification row.

**The stable form of the claim, which is what P4 should have asserted all along:** not a count,
but a *predicate* — **every occurrence of the withdrawn token in this record lies inside a
withdrawal or audit context.** That statement is immune to self-reference, because it neither
enumerates nor quotes. It is the form I adopt here, and it is why this erratum needs no count of
its own in order to stay true.

**Line numbers as of the repair date (2026-09-30):** L1696, L1699, L1847, L1900, L1950. These
are the numbers a reader should check, and they are unchanged by this addendum, which appends at
end-of-file and so cannot move any line above it. The figure of 5 was measured **before** this
section was written; this section then quotes the withdrawn token twice — once inside the P4 row
quoted above, once in the sentence naming it — so recounting the file after this addendum gives
**7**, at L1696, L1699, L1847, L1900, L1950 plus two in this section. **That the count moved from
5 to 7 because of the erratum correcting the count, and that the size of the move depends on how
the erratum happens to be worded, is the defect demonstrated rather than asserted.** No fixed
occurrence-count of this token can be stable while the reporting text quotes it, which is why the
predicate above — not a number — is the claim this erratum leaves standing.

### 6. Integrity of this addendum

- **The protected range is untouched, and this is recomputed rather than asserted.** `H_body` is
  defined over lines 1-428 minus lines 5, 6, 7, 10 and 14, each re-terminated with one `0x0A`.
  Before this addendum: `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` over
  **22,196 bytes** — equal to the value pinned at L2241 and independently reproduced by R-0026
  V7. After this addendum, recomputed the same way: **the same digest over the same 22,196
  bytes**, because this addendum is appended at end-of-file and the protected range is an
  initial segment of the file, which an append cannot change. The figure that *does* move is the
  file's total length, recorded in HO-0020's `## Verification`.
- **Method note, recorded because it has already misled one reader.** `H_body` must be read as
  **bytes** (Python, `open(path,'rb')`). PowerShell `Get-Content` splits on CRLF semantics and
  reports a phantom drift — `71691f0a…/22398` on a file whose true value is
  `c7ebe54c…/22196`. R-0026 hit exactly that false start. Anyone re-verifying this must read
  bytes.
- **Encoding.** UTF-8, no BOM, LF only, single trailing `0x0A`, no trailing blank line — written
  under explicit byte control via Python, never via PowerShell redirection (`>` writes UTF-16)
  and never via `Set-Content -Encoding utf8` (writes a BOM).
- **No lifecycle movement.** `status:` remains `RUNNING`, no `result:` is set, and no work item
  is closed by this addendum.

### Addendum 2026-10-03 — EXECUTION-READINESS CHECKLIST for the two gate experiments (E-00014 / E-00015), and a GO/NO-GO per gate

> **Filed by the experimental-scientist seat (preparer role).** This seat is **not** the
> systems-researcher executor seat that HO-0015 and HO-0016 dispatch to, and it is **not** the
> owner of E-00014 or E-00015. Its whole function is preparation and gate-readiness.
>
> **NOTHING WAS RUN.** No training, no counting, no extraction, no fitting, no label read, no
> holdout read, no engine invocation, no SPRT game. Every figure quoted below is either (a)
> read out of an existing committed record or manifest, or (b) a SHA-256 this session computed
> over a file that already existed on disk. `research.py validate` was run because it is a
> read-only audit and because both handoffs name it as a command; it is a file scan, not a
> measurement of anything this record governs.
>
> **NO LIFECYCLE MOVEMENT.** `status:` remains `RUNNING`, `result:` remains `null`. E-00014 and
> E-00015 remain `PENDING`. Neither was flipped, run, edited, or closed. No `H-####` status is
> touched. No engine source file, no `tools/` file, no `src/` file, no other record is edited.

#### 0. One premise in the brief is now out of date, and the correction moves the blocker

The brief describes **F-U14 as "being built in parallel and a hard prerequisite."** That is no
longer true, and the correction matters more than the correction itself.

**F-U14 is DISCHARGED.** `FND-0033` is `status: RESOLVED`, `closed: 2026-10-02`, written by the
data-pipeline-engineer seat. The independent tactical suite exists, is committed, and is
hash-pinned: `research/manifests/fu14-tactical-suite-n200.json` (N=200, 100 mate_in_1 + 100
mate_in_2, every annotation proved by exhaustive python-chess enumeration),
`research/manifests/fu14-overlap-report.json` with normalized-FEN overlap `== 0` against all
18 position-bearing corpora on disk, and `research/manifests/fu14-tactical-suite-pins.json`.
`git ls-files research/manifests` returns all four manifests, so the pins are committed and not
merely local. `N = 200` meets E-0013's own `N >= 200` floor **exactly at the floor**, not above
it. **This satisfies E-0013's F4-identity element and discharges the obligation that the
pre-fit-commit section recorded as "the hard blocker."**

**F-U14 is therefore not a blocker on either gate.** Neither E-00014 nor E-00015 reads the
suite: it is E-0013's conjunct (f) and a pre-fit-commit element. It reaches E-00014 only
*transitively*, because E-00014 needs the pre-fit commit and the pre-fit commit must carry the
suite's identity and digest.

**But the landing of F-U14 hardened the E-0014 block, and this is the part that is easy to
miss.** Building the suite required a master-rebuilt `kana.exe`, which is not byte-reproducible
on this machine. The rebuild produced `686ea597...` where EV-0010 records `504eb01a...`. That is
filed as `FND-0034`, severity **`blocking`**, target `EV-0010`, status **OPEN** — deliberately
not repaired by the seat that caused it, because re-pinning another record's evidence digest
from a rebuilt, non-reproducible artifact is the substitution the pin discipline exists to
prevent. Consequence, measured this session:

> `python research/scripts/research.py validate` now exits **1** with exactly **1** problem:
> `audit[evidence]: sha256 drift on build/Release/kana.exe: recorded 504EB01A8287 vs on-disk
> 686EA5979415`.

**`research.py validate` failing is E-00014's own abort condition 7, verbatim.** So the
completion of a *different* obligation armed a *pre-registered abort* in E-00014. That is the
system working, not the system breaking, and it is recorded here rather than smoothed.
#### 1. Checklist for E-00014 — TRAIN-ONLY feasibility pass (HO-0015)

| # | Item | Status | Unblocking artifact / note |
|---|---|---|---|
| **INPUTS — corpus hashes** | | | |
| 1 | Dataset `m0_audit/e0011/games.jsonl`, SHA-256 `27ea181d...ac5bb95` | **READY** | Recomputed this session; matches the pin in both gate records and in the extractor's own `sha256_expected`. 1,000 rows, 1,384,548 B. |
| 2 | Split map `split_map.json`, SHA-256 `bb079a41...4ada1ea` | **READY** | Recomputed this session; equals the extractor's `SPLIT_MAP_SHA256_EXPECTED` and is pinned in committed manifest `research/manifests/e0013-artifact-pins.json`. |
| 3 | Pre-fit commit hash | **BLOCKED** | The single pre-fit commit (E-0013 B4 sentence 2) **does not exist**. Unblocked by: that commit landing as a committed artifact carrying its own SHA-256. |
| 4 | Fitter-corpus digest | **BLOCKED** | `e0013-artifact-pins.json` has `fitter_corpus.sha256: null`, and the manifest says so honestly: the full-mode labelled extraction has not been re-emitted. `tools/e0013_pins.py::read_corpus()` **refuses** rather than handing back a count-only hash. The on-disk `positions.jsonl` (`ac8c92f0...`) is a **count-only measurement**, `is_fitter_corpus: false`, every row's `y` is `null` — it must never be quoted as the fitter's corpus digest. Unblocked by: a labelled-mode extraction writing a positions file flagged `is_fitter_corpus: true`, with its digest recorded in the manifest. |
| 5 | Frozen floor table digest | **MISSING (spec gap)** | E-00014 assumes pinned `src/` commit `7348f89` and says it is "to be VERIFIED, not assumed." It does not verify: the last `src/` commit is `9b69e0a`, and `src/eval.cpp` on disk hashes `38b7b31c09e5...`. Neither the table digest nor the correct commit is pinned anywhere. Unblocked by: `python tools/e0013_eval.py --write-floor` emitting the compiled-in table and its SHA-256 against a named `src/` commit. |
| 6 | Inner salt + inner game-id map | **MISSING (spec gap)** | `INNER_SALT` appears exactly once in the whole repository — in the sentence that defines it. **No value exists.** It must be distinct from `SPLIT_SALT` and from every prior salt, per E-0013 F6's admissibility rule. Unblocked by: a named salt value plus the inner game-id map's SHA-256, hash-committed before the fit runs. |
| **CONFIGS** | | | |
| 7 | Free-parameter set: five non-KING `mg_pst`/`eg_pst` tables plus items 1 and 3-6; KING frozen at 20000/20000 | **READY** | A pre-registered VALUE, not a pointer (E-0013 B5). 683 free parameters. May not be widened or narrowed by the executor. |
| 8 | Evaluation stage `S* = 6`; phase weights N=B=1, R=2, Q=4; `GAME_PHASE_MAX = 24`; mirror `s ^ 56` | **READY** | Frozen integers, cited read-only. No engine binary is invoked by this pass at all. |
| 9 | Label construction: `y = white_score` if side-to-move is WHITE else `1 - white_score`, `white_score` in `{1, 0.5, 0}` from `res`/`a_white` | **READY** | Side-to-move frame, pinned by B2; the White-frame error carries a FAIL consequence. |
| 10 | Optimizer family: deterministic full-batch L-BFGS; SPSA **withdrawn** as a leakage channel | **BLOCKED** | The *specification* is READY and final, but **no implementation exists.** There is no trainer source file anywhere in the repository. `tools/e0013_eval.py` has the numerical primitives — `design_rows`, `loss_and_gradient`, `mean_logistic_loss`, `per_game_losses`, `paired_statistics`, `t`-based CIs — and a `--fitted`/`--floor` input, **but no optimizer driver and no training entry point at all.** Unblocked by: a trainer built and verified against `e0013_eval.py`'s primitives. E-0013's own readiness section calls this "the single largest remaining engineering item," and `FND-0027` names it as the reason that row stays OPEN. |
| 11 | Fitter seed, L2 weight, iteration budget, early stopping (F2) | **BLOCKED** | All four are POINTERs into the pre-fit commit, which does not exist. They may be chosen only on the TRAIN inner partition, and no value may be first-assigned after the holdout is read (tripwire FAIL). Unblocked by: the pre-fit commit. |
| 12 | Clipping bound `L` | **BLOCKED** | Same pre-fit-commit pointer. |
| 13 | MAE phase-tertile boundaries (F5) | **BLOCKED** | Pointer, derived from TRAIN positions only. Requires the labelled corpus and the pre-fit commit. |
| 14 | E-00014's own filter text | **MISSING (spec gap)** | E-00014's `## Difference` still describes stage 4 as the **exact-FEN** dedup (F9). F-U7 superseded that with the normalized-FEN key, and the extractor now enforces the normalized key. Unblocked by: a dated amendment to **E-00014** naming the new key at that clause, filed by its own executor seat **before** the pass. |
| **STOPPING CRITERIA** | | | |
| 15 | Non-convergence within the pinned iteration budget: abort 6; report it; do **not** raise the budget and re-run | **READY** (criterion) | Criterion is pre-registered and unambiguous. The budget *value* is BLOCKED by item 11. |
| 16 | Gate 0 / `research.py validate` passes | **BLOCKED — AND CURRENTLY FIRED** | `validate` exits 1 on FND-0034's EV-0010 digest drift. This is abort condition 7 verbatim, so E-00014 would abort today at step zero. Unblocked by: FND-0034 dispositioned by its owner — either EV-0010 re-pinned to `686ea597...` **with the non-reproducibility caveat stated**, or a digest-stable build adopted. Not by suppressing the check. |
| 17 | No field omitted; a field that cannot be produced is `null` with a reason | **READY** | Pre-registered; omission is itself abort 8. |
| **STATISTICAL ANALYSIS PLAN (as pre-registered)** | | | |
| 18 | `delta_star_inner`: attainable loss improvement of the fitted table over the frozen floor, inner-val, paired, same labels, `S* = 6`; positive means lower logistic loss | **READY** | |
| 19 | `s_d_inner`: per-game SD of the per-game mean paired loss difference; `LOSS_MARGIN = 0.002` decidable **iff** `s_d_inner <= 0.0101` at G about 200 | **READY** | The threshold and its derivation are both pinned in E-0013 B3. |
| 20 | 95% CI of the mean per-game paired difference on `t_{0.975, G-1}`, **plus the CI of `s_d_inner` itself and the game count**, so a borderline `s_d_inner` near 0.0101 is visibly borderline rather than silently decisive | **READY** | The most carefully pre-registered item in either record. Preserved verbatim. |
| 21 | Achieved power at the 0.002 margin under the measured `s_d_inner` | **READY** (as a required reported field) | Its value cannot exist until items 3, 4 and 10 land. |
| 22 | Effective N is inner-val **games**, not positions (the label is game-constant) | **READY** | E-0013 B3 corrects the earlier position-level error. |
| **EXPECTED FAILURE INTERPRETATIONS** | | | |
| 23 | **X-1** — `delta_star` measurable and `s_d_inner <= 0.0101` | **READY** | Decided 2026-09-26, *before* E-00014 was ever filed. Conjunct (c) evaluated as written; a CI including 0 is a **FAIL**. No INCONCLUSIVE exists in this branch. |
| 24 | **X-2** — measurable and `s_d_inner > 0.0101` | **READY** | INCONCLUSIVE-BY-POWER. Not FAIL. Not a licence to widen the margin. Publishes `s_d_inner`, `delta_star`, the game count and the achieved power. |
| 25 | **X-3** — optimizer does not beat the floor | **READY** | `delta_star_inner = null` with both arms' inner-val losses. INCONCLUSIVE-BY-DESIGN. **Never** FAIL, never "no achievement = FAIL". |
| 26 | **X-2-prime** — `s_d_inner` not estimable (too few inner-val games) | **READY** | Report `s_d_inner = null` with the game count; routes to X-2 by the pre-registered table, not by judgement. |
| 27 | X-2 routing to F-U3 | **READY, with an open dependency** | The route is named and pre-registered. Its own row, `FND-0010`, is still **OPEN**, so if X-2 fires, that routing obligation is unpaid on the day it is needed. Flagged, not silently assumed discharged. |
| **RAW-DATA DESTINATIONS** | | | |
| 28 | Raw evidence local and gitignored; ledger of command to exit code to path to SHA-256; aggregator command reproducing every reported number | **READY** (convention) | Established across E-0011/E-0012. `build/` and `m0_audit/` are gitignored, so these live on the executing machine only. |
| 29 | Durable pins for the inner partition's artifacts | **MISSING (spec gap)** | E-00014 names no destination path for the inner game-id map or the per-game loss rows. Under Ruling 2's discipline a pin must be committed *before* the read it protects and re-hashed *at read time*; a gitignored artifact with no manifest is a comment, not a control. Unblocked by: naming the destination paths and adding them to the committed pre-fit-commit manifest. |
#### 2. Checklist for E-00015 — count-only realized-yield pass (HO-0016)

| # | Item | Status | Unblocking artifact / note |
|---|---|---|---|
| **INPUTS — corpus hashes** | | | |
| 1 | Dataset `m0_audit/e0011/games.jsonl`, SHA-256 `27ea181d...ac5bb95` | **READY** | Recomputed this session; matches the pin. |
| 2 | Split-map hash must exist and be recorded | **READY — and this is new** | E-00015's abort condition 2 was recorded by E-0013 as unsatisfiable "by a committed artifact." It is **satisfiable now**: `research/manifests/e0013-artifact-pins.json` is committed (confirmed via `git ls-files`) and pins `split_map.json` at `bb079a41...`, with `tools/e0013_pins.py --verify` as the read-time re-hash. Abort 2 is discharged. |
| 3 | Label-free by construction: no `res`, no `a_white`, no loss, no per-side label distribution | **READY** | The extractor names `LABEL_KEYS = ("res", "a_white")` as the two keys count-only mode must never read. This is what makes a whole-dataset count admissible here at all. |
| 4 | Counting instrument | **READY** | `tools/e0013_extract.py` in count-only mode: replays recorded SAN move lists through python-chess exactly as `tools/e0011_check.py` does. No engine binary invoked, no game generation, no build required. |
| **CONFIGS** | | | |
| 5 | Four filter stages in order: QUIET predicate (not in check *before* the move; no `x`; no `+`/`#` suffix; `full_ply >= 10`; `opening` never a candidate), then crash exclusion, then degenerate-mate exclusion (`end == "mate"` and `len(san) <= 6`), then GLOBAL-before-split **normalized-FEN** dedup | **READY** in the tool; **MISSING (spec gap)** in the record | The tool implements all four correctly under the F-U7 key. E-00015's own text still labels stage 4 "exact-FEN dedup (F9)". Unblocked by: a dated amendment to **E-00015** restating stage 4 as the normalized-FEN key. |
| 6 | `SPLIT_SALT = 20260926`, `random.Random(SPLIT_SALT * 1000003 + game_id).random() < 0.8`, 80/20 **by game** | **READY** | F-U9 verified the map is a pure function of salt and `game_id` and is therefore **invariant** under the dedup-key change; the report's own `split_map_invariance` block shows measured == expected, `unchanged: true`. |
| 7 | Scope floor `30,000` evaluated on `count_usable_distinct_train` | **READY** | `SCOPE_FLOOR = 30000` in the tool, marked not-renegotiable and explicitly *not* the retired band. The floor is on the TRAIN side so no whole-dataset quantity decides the fit's scope. |
| 8 | Yield band `75,600..76,587` | **MISSING (spec gap) — band RETIRED, record not yet amended** | The band was **retired** by E-0013's second addendum (S-0039, Ruling 1 / F-U10). Its endpoints came from a 1.302% duplication projection measured under the *old* key; it missed by 6 positions under the old key and by 1,148 under the new one. **The band constants are gone from the tool** — verified this session: no `band` key is constructed anywhere, no live `75600`/`76587` outside a retirement tombstone, and `report["band"]` now raises rather than returning a stale number. That obligation is paid. **But E-00015's pre-registration still carries the band in three places**, and its Power section still says the uncertainty "lives entirely in the pre-registered band." Unblocked by: the dated amendment in item 5's note, extended to the band clauses. |
| 9 | Replacement instrument: exact accounting identities | **READY** in the tool; uncited by E-00015 | The tool now emits five exact identities in place of the band — usable = after-degenerate minus dedup; train + holdout = usable; stages monotone non-increasing; dedup removed at least zero; one survivor per normalized FEN. They introduce **no threshold**, so there is no new number to be wrong about, and unlike the band they cannot rot when the key changes. E-00015 must cite them by the same amendment. |
| **STOPPING CRITERIA** | | | |
| 10 | One deterministic pass; no iteration budget, no convergence test, no cap, no subsampling | **READY** | There is nothing to converge and nothing to iterate. The only stopping rule is field completeness. |
| 11 | Every pre-registered field reported, or `null` with a reason | **READY** | Omission is abort 7. |
| 12 | `research.py validate` | **ADVISORY for this gate** | Deliberately recorded as such. E-00015's abort list has **no** Gate-0 clause — its aborts are dataset-pin, split-map, label-read, overlap, predicate-divergence, dedup-order and omission. So FND-0034's red validate does **not** arm an E-00015 abort the way it arms E-00014's. It is still an acceptance-criterion command in HO-0016, so it should be green before the pass for cleanliness, not for validity. |
| **STATISTICAL ANALYSIS PLAN (as pre-registered)** | | | |
| 13 | N/A in the statistical sense: a deterministic count over a frozen 1,000-row dataset, not a sample. No power question, no effect size, no CI. No pass/fail here may be described in terms of statistical confidence. | **READY, with one void clause** | The plan is complete and deliberately short. **One sentence is now VOID:** "the uncertainty in the expected figure lives entirely in the pre-registered band." The band is retired, so the uncertainty it carried must be **re-described, not deleted silently**. The replacement is the identities of item 9. Unblocked by: the same amendment. |
| **EXPECTED FAILURE INTERPRETATIONS** | | | |
| 14 | Branch 1 — `count_usable_distinct_train >= 30000`: conjunct (a) **PASSES** on yield; all-terms scope (KING PSTs frozen) stands | **READY** | Fixed before the count exists. |
| 15 | Branch 2 — `< 30000`: conjunct (a) FAILS its scope sub-condition; all-terms claim **WITHDRAWN** and recorded, not silently kept; scope **NOT** reduced to the mobility/tempo subset; the reduced scope must be re-derived and re-registered under its own critique; E-0013 ends INCONCLUSIVE-BY-SCOPE | **READY** | The refusal to reduce to mobility/tempo is substantive and correct: E-0010 attributes the **two worst** marginal contributions to exactly those terms (mobility -3.7 Elo, tempo -11.5 Elo, both non-positive with CIs crossing zero), so the ladder's fallback scope is a mis-citation. |
| 16 | Branch 3 — count outside the band | **MISSING (spec gap)** | With the band retired this branch has **no object**: there is nothing to be out of. E-0013 says so in terms — "NO OBJECT." Unblocked by: the amendment replacing this rule with the identity checks. |
| 17 | Branch 4 — any pre-registered field unproducible: `null` with the reason; never substitute a different count | **READY** | |
| **RAW-DATA DESTINATIONS** | | | |
| 18 | Raw evidence local and gitignored; full ledger; aggregator command reproducing every number | **READY** (convention) | |
| 19 | A conforming count-only report | **MISSING (spec gap) — and a live trap** | The on-disk `build/s41/extract_new/report.json` is a **pre-fix** artifact: the committed manifest says so (`schema_predates_the_2026_09_27_fixes: true`) and it still carries the retired `band` key with `comparison: "below"`. It is pinned **as what it is**, not as a current measurement. A fresh count-only run under the current tool is required to emit a report with no band key and a `corpus` block. |
| 20 | **The trap, restated so it cannot be walked into** | — | E-00015's headline number and the engineer's existing `--count-only` run are the **same quantity and will agree to the digit**. That makes it very easy to read the existing run as "E-00015 already ran." **It has not.** E-00015 is a separate record with its own pre-registration, its own provenance block, its own command and its own executor seat, and a number produced under someone else's handoff cannot be laundered into it by being equal. Closing E-00015 on the strength of an existing `74,452` without its own pass would leave a record that reads complete and is hollow. |
#### 3. GO / NO-GO per gate

**E-0014 (HO-0015) — NO-GO.** This is not a marginal call and not paperwork.

1. **No trainer exists.** Not a stale one, not a partial one — none. `tools/e0013_eval.py` supplies the loss, gradient, per-game aggregation and paired statistics, and then *consumes* a `--fitted` table it did not produce. There is no optimizer driver and no training entry point anywhere in the repository.
2. **The fitter corpus does not exist as a corpus.** `fitter_corpus.sha256` is `null` and `read_corpus()` refuses, by design, to substitute the count-only digest.
3. **The pre-fit commit does not exist**, so the seed, L2 weight, iteration budget, early stopping, clipping bound `L` and the F5 tertile boundaries — every one of them a pointer into it — have no values.
4. **`research.py validate` currently fails, which is abort condition 7 already armed.**
5. `INNER_SALT` has no value; the floor table's digest is unpinned and its assumed `src/` commit is wrong; E-00014's filter text still names the superseded exact-FEN key.
6. `FND-0027` (F-U11) and `FND-0028` (F-U12) are **OPEN**, and F-U11's own addendum states the blocker is a missing artifact rather than paperwork.

Minimum path to a re-decision: build and verify the trainer; emit the labelled extraction and pin `fitter_corpus.sha256`; land the pre-fit commit carrying F1-F12 values and the now-available F-U14 suite identity; disposition FND-0034 so Gate 0 is green; name `INNER_SALT`; pin the floor table; file E-00014's dated amendment. **All seven are engineering and record actions. None is a measurement, and none may be substituted by running E-00014 and reporting whatever comes out.**

**E-00015 (HO-0016) — NO-GO, but it is the near gate and its blocker is re-registration, not engineering.**

Every input, config, instrument and interpretation is in place. The split-map pin that E-00015's abort condition 2 demands is now committed and re-hashable. The band constants are already gone from the tool. The accounting identities that replace the band already exist in the tool. The scope floor is intact and unrenegotiable.

**One artifact unblocks it:** a dated amendment to **E-00015 itself**, filed by its own executor seat **before** the pass, doing four things — replacing the band clause at its Games/Samples section; re-describing (not deleting) the Power section's reliance on that band; replacing decision rule 3, which now has no object, with the accounting identities; and restating stage 4 as the normalized-FEN key.

That amendment is a precondition the record itself imposes. A count measured under a superseded description is precisely the "number that looks authoritative and is wrong" the S-0037 ruling warned about. **After that amendment, E-00015 has no missing artifact and could run.**

**F-U14 dependency, called out explicitly as instructed.** F-U14 was a hard prerequisite while it was open and it **is now discharged** — suite N=200 built, overlap 0 against 18 corpora, hash-pinned, committed, re-verified by a command that re-runs all 200 exhaustive proofs. **It blocks neither gate.** It is not on E-00015's critical path at all. It reaches E-00014 only transitively, through the pre-fit commit that must carry its identity and digest. And its one residual consequence runs the *other* way from what the brief anticipated: landing it turned `validate` red, which is what arms E-00014's abort condition 7.

#### 4. Gate 7 (FND-0007 / F-U5) — where this checklist stands relative to it

`FND-0007` is **RESOLVED**: B7 quoted Q-0006's official readiness gate 7 verbatim into E-0013 and gave it teeth, and Q-0006 is now cited (also discharging DN7). That is the *text* being discharged.

The operative Gate-7 obligation is carried by **F-U5**, whose row `FND-0012` is still **OPEN**. It requires that on any terminal PASS-FIT-QUALITY-ONLY, terminal FAIL, or any named INCONCLUSIVE, E-0013 files a handoff to **verification-auditor** — never the owner, never the seat that ran the fit — carrying `fitted_params_sha256`, the pre-fit commit hash, the split-map hash, the E-00014 numbers (`s_d_inner`, `delta_star`, contingency branch), the E-00015 numbers, and the full command/exit-code ledger.

**Neither gate has produced a number, so Gate 7 cannot be satisfied yet and nothing here pretends otherwise.** What this addendum does is make the handoff *constructible*: every field Gate 7 will require is enumerated above with its current status, so that when the numbers exist the verifier's inputs exist with them. **The two gates' outputs are the raw material of Gate 7 and are not a substitute for it.** A verdict filed without its readiness-Gate-7 row remains invalid, and this seat cannot supply that row — it is the verification-auditor's, and only on a terminal verdict.

#### 5. Integrity of this addendum

- **The protected range is untouched, and this is recomputed rather than asserted.** `H_body` over lines 1-428 minus lines 5, 6, 7, 10 and 14, each re-terminated with one `0x0A`, read as **bytes**: before this addendum `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` over **22,196 bytes** — equal to the value pinned in E-0013's own section 6 and independently reproduced by R-0026 V7. After this append, recomputed the same way, the same digest over the same 22,196 bytes, because this addendum is appended at end-of-file and the protected range is an initial segment of the file, which an append cannot change.
- **Method note, restated because it has already misled one reader.** `H_body` must be read as bytes. PowerShell `Get-Content` splits on CRLF semantics and reports a phantom drift on a file whose true value is unchanged. R-0026 hit exactly that false start.
- **Encoding.** UTF-8, no BOM, LF only, single trailing `0x0A`, no trailing blank line — written under explicit byte control via Python, never via PowerShell redirection (`>` writes UTF-16) and never via `Set-Content -Encoding utf8` (writes a BOM).
- **Nothing was measured.** Every hash quoted in this addendum is a digest of a file that already existed on disk, computed by a read-only `Get-FileHash`. No training, counting, extraction, fitting, label read or holdout read was performed, and no engine was invoked.
- **No lifecycle movement.** `status:` remains `RUNNING`, `result:` remains `null`. E-00014 and E-00015 remain `PENDING` and were neither run nor edited.
- **Routing.** The consolidated blocker list is filed as a separate handoff to the Sponsor, because a blocker list that lives only inside an addendum is a list nobody is obliged to answer.

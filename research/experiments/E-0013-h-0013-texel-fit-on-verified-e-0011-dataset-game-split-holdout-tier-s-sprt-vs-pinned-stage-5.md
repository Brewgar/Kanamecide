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

**B5 sentence 2 (the ladder's citation, corrected - IN THIS RECORD ONLY):**


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
> record's own filter, and the ladder's DISARMED status is provisional on it. If the count
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
| **X1 (R-0020)** | **DISCHARGED - in-place text repair of THIS addendum, 2026-09-26, under R-0020's licence** | R-0020 found this addendum to be a truncated, interleaved document: ten sentences severed at a block boundary with their continuations relocated far away, ONE continuation absent from the file, the X-1/X-2/X-3 contingency table ~340 lines from the sentence announcing it, the follow-up obligations split across this table, and the file ending mid-bullet. All ten seams are now joined as single contiguous sentences inside their own finding's section; the absent continuation is supplied as X1-a; the contingency table now sits immediately under B3 sentence 3's announcement; F-U1..F-U6 (including F-U3's stranded `Owner:/Due:` line) are one contiguous list; cost item 4 is contiguous with items 1-3; the BUCKET-1/2/3 list is restored to one place; and the file ends on a complete sentence. | The repair is a MOVE, not a rewrite: no sentence was deleted and no continuation was retyped, and every move is listed line-by-line in the dated repair section at the end of this addendum. Consequence stated rather than hidden: this ADDENDUM is therefore NOT purely additive to itself. The ORIGINAL pre-registration (L1-L428) is append-only and provably so, by hash - see the same repair section. |
| **X2 (R-0020)** | **DISCHARGED - the false clause DELETED, the arithmetic INSERTED** | B5 sentence 1's recorded rationale claimed that freezing "keeps the fitted-parameter count defensible against E-0011 N1's '>= 500 positions/parameter' standard". That is false: 683 free scalars against at most 76,587 realized positions is ~112 positions per parameter (~89 train-side), about 4.46x short of 500, and freezing moves 94 -> 112, not to 500. The clause is deleted and replaced with R-0020's own arithmetic, and "240 extra free parameters" reads **128** (or 64 under `pst[s] == pst[mirror(s)]`). | The freeze DECISION is unchanged and is NOT re-opened by this correction. 4.46x short is now recorded as a STATED LIMITATION of the all-terms scope, not as a solved one; the binding constraints on stage (a) remain E-0011 N1's label/systematic bias and the game-clustered `s_d` that E-00014 measures. |
| **B5 s2 (pre-existing)** | **RECORDED, body UNESTABLISHED - not moved, not filled** | B5 sentence 2's heading at L811 ("the ladder's citation, corrected - IN THIS RECORD ONLY") announces quoted text, but its slot is EMPTY: L812-L813 are blank and B5 sentence 3's heading is at L814. The same hole exists in `ce845c5` (L684 heading, L685-L686 blank, B5 sentence 3 at L687), so it is PRE-EXISTING and was not introduced by the R-0020 repair. | **The announced body is NOT established to be the correction-note block now at L822-L848, and this row does not claim it is:** that block is introduced by B5 sentence 3, whose preamble ends in a colon at L820 and is immediately followed by it, so it is already spoken for. B5 s2 therefore has no located body anywhere in the file, and whether its text was lost, never written, or is the note under another name is UNESTABLISHED - not guessed. (The earlier note at L1202 that this text "sits far away under B6 sentence 1" describes the `ce845c5` geometry, in which this material ran to old L871 near B6 s1; after the repair the note is at L822-L848 under B5 s3 and B6 s1 is at L1016.) This is the same interleaving class as X1 - a heading whose body lives elsewhere - which is why it was hard to detect. Deciding whether to relocate anything is a CONTENT judgement for the next reviewer; this seat's job was to make the hole visible and named. |

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
file's current numbering. Every continuation was MOVED byte-for-byte, not retyped; each joined
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
| 8 | L707 `i.e. 2.5x headroom` | X1-a (author's text, new) + L871-L878 | L834-L848 | the ladder's DISARMED status is provisional, and reasoned |
| 9 | L730 `...ARMED the E-0011 N1` | L828-L831 | L871-L875 | the ~27k refutation's scope-changing consequence is attached |
| 10 | L754 `**Relaxing (d) opens a live leakage` | L823-L826 | L899-L903 | DN10's explicit-dependency sentence is one sentence |

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
kept whole, and the leading `it; B6)` of the author's tail (old L871, now L841) was **deleted**.
That is text R-0020 said to move, and deleting it is recorded here rather than done silently.
It was deleted because it is the redundant half of the duplication, not because it carried
meaning: `it;` is stranded (the template has already said "provisional on it") and its `B6)`
duplicates the citation the template's own parenthetical already makes. The alternative was
chosen over trimming the template's `B6)` because trimming it would delete the very string
R-0020's condition (c) mandates and would leave the count of `mobility/tempo scope; B6)` at 0,
falsifying the verbatim-adoption claim recorded in this same section. The cost is stated rather
than hidden: **the head's opening paren `(E-00015 measures` is now left unclosed**, because
R-0020's template consumed the tail's `)` and supplied a self-closing parenthetical of its own.
Both candidate forms leave that paren orphaned (delta +1); the pre-fix text was balanced only
because the duplicated citation accidentally supplied a second `)`. This is a defect inherited
from the template, it is flagged here for the re-critique, and it is **not** repaired here
because closing it would require inventing a closing token R-0020 did not supply.

**Other moves, same rule - nothing deleted, nothing retyped.** The X-1/X-2/X-3 contingency table
moved from old L960-L995 to L682-L717, immediately under B3 sentence 3's announcement at
L677-L680, with no wording change. F-U3's stranded `Owner:/Due:` line (old L808) and the
F-U4/F-U5/F-U6 bullets (old L809-L821) rejoined F-U1..F-U3, now one contiguous list at
L909-L944. B1's cost item 4 (old L1045-L1049) rejoined items 1-3 at L544-L548. The BUCKET-2 and
BUCKET-3 bullets (old L1068-L1073) rejoined BUCKET-1 at L476-L487, and BUCKET 3's promised cost is
now stated in the bullet itself, in the words B1's cost items 1-4 already use. The addendum's
narrative now ends on a complete sentence at L1106-L1114 - the old L1073 bullet "Decision:
**SHRINK.**" had no continuation of any kind - and this dated repair section follows it.

**N1, N2, N3, placed.** N1 is a binding note at L572-L581, immediately after B1 sentence 1's
quoted mechanism. N2 names F-U4's owner seat literally at L934-L935. N3 added a disposition-table
row for X1 and one for X2 to the addendum-to-addendum table, so no future reader is told by that
table that everything was already closed.

**X2, placed.** The false clause was deleted and R-0020's replacement inserted at L791-L807; the
"240 extra free parameters" in the same quoted block reads **128** at L788; and a dated editorial
note at L809 records that this was an in-place replacement of quoted text, quotes the old wording,
and states that the freeze DECISION is unchanged. The "(240 params)" in the F3 row of the F1-F12
table is R-0019's own item label and is left as quoted, for the same reason E-0011 is not edited.

**One observation recorded, not acted on.** "B5 sentence 2 (the ladder's citation, corrected)"
at L811 announces quoted text that sits far away under B6 sentence 1. R-0020 did not enumerate
this as a seam, and the paragraph it points at is complete rather than severed, so it was left
exactly as found and is flagged here for the next reviewer rather than silently moved.

**The append-only contract, proved by hash rather than asserted.** Lines 1-428 of this file -
the original pre-registration, above the addendum - are byte-identical to the same lines at
`ce845c5`. SHA-256 over lines 1..428 including their line terminators, UTF-8, 22,270 bytes:

- `git show ce845c5:research/experiments/E-0013-h-0013-...-stage-5.md`, lines 1-428 ->
  `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`
- this working file, lines 1-428 ->
  `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`

Equal. **The ORIGINAL is append-only and provably so. The ADDENDUM was found corrupt by review
and repaired IN PLACE under that review's licence** (R-0020: "move that text, not rewrite it";
"delete the false clause and replace it"). That is why the historical `648 additions / 0
deletions` numstat over `ce845c5..HEAD` no longer reads zero-deletions. That is stated here
rather than papered over, and the distinction is the point: the append-only rule protects the
pre-registration, and the addendum was corrupt inside the very document the review examined.

**A note on the append-only check itself.** `git diff --numstat HEAD -- <E-0013 path>` returns
EMPTY on a clean tree and therefore cannot distinguish "add-only" from "nothing changed". Any
append-only evidence line must name a baseline commit - here `ce845c5` for the pre-repair
addendum, or `4478c3a` for the pre-addendum file.

**What was NOT touched.** No decision: SHRINK stands, the KING-PST freeze stands,
`SUITE_TOLERANCE = 0.02` stands, the per-game cap stays NONE, and the X-1/X-2/X-3 branches stand
exactly as decided. Nothing above L429 was edited. R-0019, R-0020, HO-0013, HO-0014, E-0011,
E-0012, W-0001, W-0005, RUN-0002, RUN-0003, R-0017 and R-0018 are untouched, as is every H-####
text and status; no `tools/` or `src/` file was edited (N1 is a text note about a script, not a
change to it); no training, fitting, extraction, counting, feasibility pass or SPRT generation
ran; no holdout was read. E-0013 remains `status: PENDING` - this repair is not authorisation to

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
including F-U3's `Owner:` line; the file's **terminal complete sentence** at L1106-L1114;
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
move it, and per R-0020 the flip requires a fresh re-critique to confirm.

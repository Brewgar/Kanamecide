---
id: HO-0013
type: handoff
from: researcher-architect
to: adversarial-reviewer
work_item: null
status: DONE
title: "Critique E-0013 pre-registration (H-0013 Texel fit contract) before any running"
artifacts: ["research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "research/hypotheses/H-0013-tapered-eval-plus-texel-protocol-mg-eg-interpolation-and-quiet-label-holdout-design.md", "research/experiments/E-0012-e-sprt-lite-comparison-harness-pre-registered-dec-0010-tiers.md", "research/reviews/R-0018-independent-verification-w-0005-e-0012-live-runs-run-0002-and-run-0003-ho-0012.md", "research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md", "research/work/W-0001-e0011-self-play-data-pipeline-pre-register-build-run-verify.md", "research/handoffs/HO-0008-rule-r-0014-b3-fully-discharged-e-0011-clear-for-build-run.md", "tools/e0012_sprt.py"]
commands: ["python research/scripts/research.py validate"]
acceptance: "a ruling (new review R-0019 or a dated append in a new R-####) that rules each of the six questions below CLEAN / BLOCKING with evidence; E-0013 may leave PENDING only on a CLEAN ruling (or all blocking findings discharged via addenda)"
example: false
created: 2026-09-26
closed: 2026-09-26
---

# HO-0013 — Critique E-0013 pre-registration (H-0013 Texel fit contract)

> The ONLY way to ask another agent to do something. Prose requests ("someone
> should verify this") are not handoffs and will be ignored. Receiver appends
> `## Response` and `## Verification`; the handoff may be edited while
> `status: REQUESTED|ACCEPTED` and is frozen once `DONE|REJECTED|WITHDRAWN`.

## Request

E-0013 is filed as `status: PENDING` — the first training/fitting
pre-registration (H-0013 Texel fit on the verified E-0011 dataset). It mirrors
the E-0012 contract pattern (Provenance, Sample Validity, Pre-Registered
Decision Rule, Power And Sample Size all populated before running). Rule
whether it is fit to leave PENDING, modeled on HO-0008's structure (which
gated E-0011 on the R-0014 B3 sentence with a pure-additions fix + a doc-nit
reconciliation).

The six pointed ruling questions below are MANDATORY — rule each one
CLEAN or BLOCKING with cited evidence. Honest NOT CLEAN / BLOCKING outcomes
are allowed and must not be softened. Design tension to keep in view (do NOT
resolve silently — rule on it): H-0013's 2026-09-09 text assumes "~50k quiet
Stockfish-labeled FENs" while the real data is the E-0011 dataset (checker
diagnostic: `quiet_proxy_opening_skipped=76593`); E-0013 adopts OPTION P1
(file against E-0011, holdout-loss band margin 0.002 + paired CI, rejecting
the brief's ±0.10 band as underived) and leaves P0 (amend H-0013) to its own
decision. The brief's "~27k quiet positions post-filter per W-0001's
done-report" figure is flagged in E-0013 as UNVERIFIED against the on-disk
checker diagnostic — confirm or correct that flag as part of question (v).

1. **Free parameters pinned?** Is every free parameter pinned or re-derivable
   post-outcome? Check: the taper formula
   `phase = min(1*N+1*B+2*R+4*Q, 24)`, `score = (mg*phase + eg*(24-phase))/24`;
   the fitted set (mg/eg values, six MG/EG PSTs with the KING-PST symmetry
   pair-or-freeze rule, pawn-structure, mobility, bishop-pair/open/semi-open/
   seventh/king-shield/king-center, tempo with frozen sign convention); the
   frozen list (phase weights, GAME_PHASE_MAX, FLAT_VALUE, mirror `s ^ 56`,
   search/UCI/TC). Is any coefficient unpinned, or could the scope
   (all-terms vs mobility/tempo subset, KING-PST freeze vs fit) be chosen
   AFTER seeing the holdout loss? Is the fitting method (Q-FIT:
   logistic/gradient Texel vs SPSA) sufficiently specified, or is its OPEN
   state a BLOCKING gap that must land as a dated addendum BEFORE running?
2. **Holdout-split leakage?** Can the split leak? Check: BY-GAME split with
   `SPLIT_SALT = 20260926` (distinct from 20260914/20260922/20260924), the
   `random.Random(SPLIT_SALT * 1000003 + game_id)` assignment, split-map hash
   committed BEFORE fitting, overlap-0 at game level
   (`tuple(opening)+tuple(san)`) AND normalized-FEN level. Probe
   position-level relatives across games (same opening subtree reaching the
   same FEN from different game_ids), threefold-cluster leakage (repetition
   draws sharing positions across the split), and crash-game/degenerate-game
   exclusions. Is the FEN normalization (side-to-move + placement +
   castling/EP) sufficient, or does it miss a leakage channel?
3. **Achievement floor frozen and non-apathetic?** Is the holdout-loss gate
   genuinely frozen (`LOSS_MARGIN = 0.002` + paired game-clustered 95% CI
   excluding 0) and non-apathetic (no achievement = FAIL, HO-0008 lesson)?
   Is the 0.002 margin derived or aspirational — and if aspirational, must the
   contract shrink the claim now rather than after seeing data? Is the CI
   construction (paired t, clustered BY GAME) correct for game-correlated
   positions, or does it understate the SE?

4. **SPRT gate inherits E-0012's scope ruling?** Does the strength gate
   (Tier S [0,+20], ±2.944, cap 2,000, fitted-A vs pinned-stage-5-B, fresh
   salt, `training_game_overlap = 0` before the verdict) inherit E-0012's
   scope ruling (no engine-strength overreach — Tier-S H1 = "worth keeping",
   never Tier-R "stronger" or Tier-M magnitude)? Is the stage-5 opponent
   choice (strongest measured rung k5 +127.6, not stage-6) justified or a
   cherry-picked soft target? Is "never fitted vs itself" (W-0001
   self-collision) enforced by the arm-differentiation rule (handshake hash
   dump, A != B)? Does the replay acknowledgement state the 125-vs-179 delta
   as unexplained per R-0018 Q4 (not settled), with the opening-book-hash +
   paired-colour mitigation actually checkable?
5. **Power honesty preserved given the budget?** At cap 2,000 (~2.6–3 h at the
   measured ~769 games/h), is the stated power shape honest (decides +20,
   INCONCLUSIVE-by-design at +5; Tier-R needs ~29–32k games)? If any band
   (holdout margin, suite tolerance, SPRT zone) is aspirational at this N,
   recommend SHRINK (narrower claim, smaller margin, larger suite N) rather
   than silent weakening — name the concrete shrinkage. Rule on the "~27k"
   vs measured-76593 yield flag: which figure governs the scope floor, and
   does the 30k consequence ladder (E-0011 N1) still bind?
6. **Sequencing interactions?** Any interaction with HO-0005/W-0003 audit
   (still REQUESTED, out of scope) or the deferred H-0010 status review that
   must be sequenced FIRST? Specifically: does anything in E-0013 presuppose
   a H-0010 status change (it must not — E-0013 Follow-Up forbids it), and
   does HO-0005's outstanding audit touch any artifact E-0013 cites (if so,
   name the ordering constraint)?

## Artifacts To Read (paths)

- `research/experiments/E-0013-…md` — the full PENDING contract (decision
  rule, power, validity, provenance, open questions P0/P1, Q-LABEL, Q-FIT,
  Q-SCOPE, Q-SUITE)
- `research/hypotheses/H-0013-…md` — the 2026-09-09 hypothesis text (note the
  "~50k quiet Stockfish-labeled FENs" assumption E-0013 deliberately does NOT
  inherit)
- `research/experiments/E-0012-…md` — the contract pattern mirrored
  (owner close-out bounds the 125-vs-179 delta as unestablished variation)
- `research/reviews/R-0018-…md` — Q4 ruling (125-vs-179 unexplained);
  the new contract must acknowledge it, not claim the harness is settled
- `research/decisions/DEC-0010-…md` — tiers, ±2.944, caps, post-cap
  INCONCLUSIVE (cited, not re-derived)
- `research/work/W-0001-…md` — leakage contract wording (distinct salt,
  `training_game_overlap = 0`, `fitted_params_sha256`), N1 consequence ladder
- `research/handoffs/HO-0008-…md` — the critique-handoff structure modeled
  here (ordered checks, pure-additions fix discipline, doc-nit surfacing)
- `tools/e0012_sprt.py` — read-only; confirm it is CITED unmodified

## Commands To Run

```powershell
python research/scripts/research.py validate
```

## Acceptance Criteria (what makes this DONE)

- A ruling (new review R-0019 expected; the CLI result is authoritative —
  next free R id is R-0019, verify with the CLI, do not assume) with a
  per-question verdict (CLEAN / BLOCKING + evidence) on all six questions
  above, plus explicit rulings on the open questions P0/P1, Q-LABEL, Q-FIT,
  Q-SCOPE, Q-SUITE (each: adopt / amend-with-text / block).
- Any BLOCKING finding names the exact missing sentence (HO-0008 discipline:
  quote the ordered fix) and whether it lands as a pure-additions addendum.
- On a CLEAN ruling (or all blocking findings discharged via addenda),
  E-0013 is clear to leave PENDING (the reviewer/owner flips PENDING →
  RUNNING only then). No edits to the contract by the critic — the critic
  rules; the owner edits.
- `validate` → exit 0 recorded with raw output.

## Response (receiver, append-only)

- 2026-09-26 — adversarial-reviewer (S-0024) — **DONE. Verdict: NOT CLEAN —
  BLOCKING. E-0013 stays `status: PENDING`; nothing was fitted.** Ruling filed
  as **R-0019** (`kind: critique`, `target: E-0013`, COMPLETED). I confirmed the
  next free review id with the CLI before filing (highest existing was R-0018) —
  the CLI's answer, R-0019, is what I used. I did not edit E-0013, H-0013,
  DEC-0010, `tools/e0012_sprt.py`, R-0017/R-0018 or RUN-0002/RUN-0003, did not
  change any H-#### status, did not start the HO-0005/W-0003 audit, and did not
  mark E-0013 RUNNING. No training, fitting, extraction, relabeling or SPRT game
  generation was run.

  **Per-question verdicts (all six ruled, with cited evidence in R-0019):**
  1. **Free parameters pinned? — NOT CLEAN / BLOCKING** (B3, B4, B5). The
     free-parameter *section* is genuinely good: the fitted list is complete
     against `src/eval.h`'s `EvalCoeffs` member-for-member, the taper/phase
     formula is frozen with a source citation, and KING material, mirror `s^56`,
     the tempo sign, the NPS band, the symmetry gate and the deterministic-rerun
     check are all pinned. What is not closed is the twelve-value **freeze
     audit** tabulated in R-0019: eleven values (F1–F11) can still be chosen or
     re-derived after the holdout loss is visible. Only F12 (the per-game cap) is
     closed, and only because the contract handed it to me — **I ruled NO CAP**
     (200 holdout games is already the binding denominator; a cap shrinks the
     holdout, reduces power and adds a discretionary filter).
  2. **Leakage? — NOT CLEAN / BLOCKING** (B4), but the mechanism is strong and I
     say so. The salt arithmetic is adequate and I computed it rather than
     accepting "at execution" (`|20260926−20260924|×1,000,003 = 2,000,006 >
     1,999`). The normalized-FEN gate is specified correctly and — importantly —
     deliberately **excludes** the halfmove clock and fullmove number that
     `board.fen()` would carry, which closes the nearest-identical-FEN channel.
     Cross-game transposition leakage is real in this dataset
     (`duplicate_positions=1705`) and the gate is what stops it. Threefold
     clusters are closed by the exact-FEN gate. Colour-flipped relatives are
     *not* caught but are sound only because conjunct (d) enforces eval
     colour-symmetry — a dependency the contract should state (DN10). **The
     split-map commit IS a genuine blocking pre-condition, stated three times**,
     not an intention. Not closed: the 76,593 diagnostic as a whole-dataset
     selection surface (benign — it is label-free — but the scope branch should
     be a train-only count), and F3/F6/F8/F9.
  3. **Anti-apathetic? — NOT CLEAN / BLOCKING** (B3). "No achievement = FAIL" is
     frozen in three places and I could find **no** rhetorical route from a null
     to "baseline preserved". The paired CI is clustered on the right unit and
     does not understate the SE. But the sentence making a CI-includes-0 verdict
     a FAIL rather than an INCONCLUSIVE rests on "the holdout N is large; power
     is not the binding constraint here" — and both halves are false. I computed
     the power myself: because the label is game-constant the holdout's
     independent units are ~200 **games**, not ~15,000 positions, and
     `LOSS_MARGIN = 0.002` is decidable **iff the per-game cluster SD is
     ≤ 0.0101** — a quantity nobody has measured. At `s_d=0.02` power is ≈0.33;
     at `s_d=0.05` it is ≈0.10. Worse, a game-constant label may put the
     *attainable* gain below 0.002, making conjunct (c) an **unwinnable** gate
     while the record claims stage (a) is decidable. My fix does not weaken the
     margin: a pre-registered, non-training, **train-only** feasibility pass
     measures `delta_star` and `s_d` before the margin binds, and the
     FAIL/INCONCLUSIVE split follows the measurement.
  4. **Scope creep into strength? — NOT CLEAN / BLOCKING** (B1); the scope
     discipline itself is CLEAN. "A good holdout correlation alone is NOT a
     strength claim" is in the Hypothesis, E-0012's ruling is carried in the
     Baseline, and conjunct (h) is a first-class gate ("a Tier-S H1 licenses
     'worth keeping', never a Tier-R 'stronger' or Tier-M magnitude claim"). The
     cap was **tightened** 8,000 → 2,000 with the reasoning on the page, and the
     Tier-S ASN shape is cited, not re-derived. The R-0018 replay acknowledgement
     is verbatim-correct and its mitigation is genuinely checkable.
     **BLOCKING: the stage-(b) arm-differentiation mandate is unachievable with
     the cited tool.** `tools/e0012_sprt.py:325-326` builds *both* arms from the
     single `--exe` and line 301 records one binary hash for both; the engine's
     UCI surface advertises and accepts only `Hash` and `EvalStage`
     (`src/main.cpp:103-114,133-147`) and emits no parameter hash; `EvalCoeffs`
     is a compiled-in static with no loader. So `--stage-a 5 --stage-b 5` is
     exactly the W-0001 self-collision this record forbids, and the mandated
     "dump the effective loaded hash from both engines' handshake" has nothing
     to dump. E-0013 mandates a Tier-S result it has also prohibited the means
     of obtaining. Also: the stage-5 choice rests on a point estimate whose CI
     overlaps k6/k4/k3 almost entirely, and `tempo` is applied only at
     `stage >= 6` — so the fitted `tempo` entry is **inert in both stage-(b)
     arms** while whether gate (c) even scores it depends on an EvalStage the
     record never states.
  5. **Power honesty? — NOT CLEAN / BLOCKING** (B3, B4); the yield flag is CLEAN
     and correct. **I confirm the flag and the arithmetic:** 76,593 is a
     **per-ply** count over the `san` segment for the bare quiet predicate, not a
     distinct-position count. With cross-game FEN duplication at
     1705/130930 = 1.302 % and ≤6 positions lost to the one degenerate game, the
     honest realized band is **75,600 ≤ yield ≤ 76,587** — 2.5× the 30k floor, so
     **the 30k ladder does not bind**. The brief's "~27k" is not merely
     UNVERIFIED, it is **refuted and scope-changing**: it sits *below* the floor
     it would be compared against and would have silently armed the fallback.
     The measured figure governs, and E-0013 is right to say so. Aspirational
     bands: holdout margin (B3) and suite tolerance (B4) — both to be made
     decidable, not silently weakened. SPRT zone: not aspirational.
  6. **Sequencing? — CLEAN. No ordering constraint exists.** Nothing in E-0013
     presupposes a H-0010 status change: it cites the *harness* and the *tiers*,
     never H-0010's status, and its Follow-Up forbids both status changes
     (correct, and I endorse the ordering it names). I enumerated E-0013's
     citation set and **none** of {R-0013, W-0003, HO-0005,
     `AGREEMENT_MATRIX.md`} appears in it, so HO-0005/W-0003's outstanding audit
     touches nothing E-0013 depends on. DEC-0010's own gate-3 line is stale but
     the debt is discharged by R-0010 (W-0002 Verification block).

  **Open questions, ruled:** **P0/P1 → adopt P1**; H-0013 is not amended by
  this seat, and the P0 correction is `blocked_by` E-0013's *terminal result*,
  not its pre-registration (filed no later than close-out, cross-referencing
  R-0019). **Q-LABEL → adopt result-only, amended** (B2): the literal reading of
  "from White's perspective at the position's side to move" would hand a
  Black-to-move position the White-frame target, and because the eval is
  colour-symmetric that error teaches "high eval ⇒ White wins" for *both* sides
  **while conjunct (d) still passes** — silent, catastrophic and gate-invisible.
  **Q-FIT → adopt deterministic full-batch L-BFGS, block SPSA, amended** (B4):
  the record's own alternative, "SPSA on **holdout loss**", is a leakage channel
  and is withdrawn. **Q-SCOPE → adopt all-terms with KING PSTs FROZEN, and
  correct a backwards citation** (B5): E-0011 N1's fallback scope is "the
  mobility/tempo sub-set E-0010's ladder motivates", but E-0010:344 measures
  mobility **−3.7** Elo and tempo **−11.5** Elo, "non-positive with CIs crossing
  zero". I recomputed those deltas from E-0010's own published ladder and they
  reproduce exactly — the two terms the ladder names as the fallback are the two
  the ladder attributes the worst contributions to. Latent only, because the
  ladder is disarmed by measurement, but a wrong auto-applied scope is exactly
  the class of defect that has bitten this project before. **Q-SUITE → adopt the
  independent suite, close the substitution path, require the tolerance to be a
  number** (B4).

  **Blocking findings: seven (B1–B7), each with its exact missing sentence in
  R-0019, each marked for pure-additions landing in ONE dated addendum with the
  original E-0013 text untouched** (supersessions quoted by name, not deleted) —
  the HO-0008 / R-0014 pattern. No engine work, extraction, fitting or SPRT game
  generation is needed to land any of them. Ten non-blocking items (DN1–DN10)
  are surfaced separately in R-0019. **E-0013 may not leave PENDING until B1–B7
  are discharged and re-critiqued; the owner flips PENDING → RUNNING only then.**

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
  - `git pull --ff-only` → up to date; `git rev-parse HEAD origin/master` → both
    `d9efffdb6c74fe020092ba4e6dfa5dec88da13f9`; `git status -sb` → clean tree
    before I started. Captures: `research/context/s24_gitlog.txt`.
  - `python research/scripts/research.py new-review --help` +
    `Get-ChildItem research\reviews` → highest existing review R-0018; the CLI
    then created **R-0019**. `research/context/s24_newreview.txt`,
    `research/context/s24_reviews.txt`.
  - `python research/scripts/research.py validate` → **exit 0**, 0 problems.
    `research/context/s24_validate.txt`.
  - `python research/scripts/research.py update` → clean; `state --write` → clean
    (the first validate failed on a stale `state.json`; regenerated and
    re-validated).
  - `git diff --check` → **exit 0**, no whitespace errors.
    `research/context/s24_gitdiffcheck.txt`.
  - **Prohibition check, `git diff --numstat` over E-0013, H-0013, DEC-0010,
    `tools/e0012_sprt.py`, R-0017, R-0018 → empty output.** E-0013 is
    byte-identical to `d9efffd`. `research/context/s24_notouched.txt`.
  - **Environment caveat, stated rather than hidden:** this session's shell
    capture is degraded — `run_commands` reported `Command exited with code 1`
    on commands that plainly succeeded, and PowerShell's `>` default redirect
    emits UTF-16. Every gate result above was therefore taken from the
    **contents of a redirected output file** under `research/context/`, never
    from the reported exit status. Ten scratch files first written to the repo
    root tripped the DEC-0009 hygiene gate and were moved to `research/context/`;
    that fix is why the first validate run shows 11 problems and the second
    shows 0.
- verdict: **NOT CLEAN / BLOCKING — E-0013 stays PENDING, nothing fitted.**
  Seven blocking findings (B1–B7) and ten non-blocking (DN1–DN10), filed as
  R-0019. Next session is a fix-and-re-critique cycle on E-0013 alone; no
  sequencing constraint was found and nothing else in the project is blocked by
  this ruling.


## Verification (receiver, append-only)

- raw output / exit codes / hashes:
- verdict: (pending)

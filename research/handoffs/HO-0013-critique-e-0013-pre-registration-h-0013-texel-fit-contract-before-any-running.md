---
id: HO-0013
type: handoff
from: researcher-architect
to: adversarial-reviewer
work_item: null
status: REQUESTED
title: "Critique E-0013 pre-registration (H-0013 Texel fit contract) before any running"
artifacts: ["research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "research/hypotheses/H-0013-tapered-eval-plus-texel-protocol-mg-eg-interpolation-and-quiet-label-holdout-design.md", "research/experiments/E-0012-e-sprt-lite-comparison-harness-pre-registered-dec-0010-tiers.md", "research/reviews/R-0018-independent-verification-w-0005-e-0012-live-runs-run-0002-and-run-0003-ho-0012.md", "research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md", "research/work/W-0001-e0011-self-play-data-pipeline-pre-register-build-run-verify.md", "research/handoffs/HO-0008-rule-r-0014-b3-fully-discharged-e-0011-clear-for-build-run.md", "tools/e0012_sprt.py"]
commands: ["python research/scripts/research.py validate"]
acceptance: "a ruling (new review R-0019 or a dated append in a new R-####) that rules each of the six questions below CLEAN / BLOCKING with evidence; E-0013 may leave PENDING only on a CLEAN ruling (or all blocking findings discharged via addenda)"
example: false
created: 2026-09-26
closed: null
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

- (pending)

## Verification (receiver, append-only)

- raw output / exit codes / hashes:
- verdict: (pending)

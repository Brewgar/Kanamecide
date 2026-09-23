---
id: R-0013
type: review
reviewer: adversarial-reviewer
target: W-0003
kind: critique
status: COMPLETED
work_item: W-0003
related: [W-0003, AGREEMENT_MATRIX, AGENT_MEGAPROMPT_ROUND2, R-0002, D-0001, D-0002, D-0003, D-0004, D-0005, D-0006, E-00003, E-0002, E-0010, H-0003, H-0005, H-0006, H-0008, H-0009, H-0010, H-0011, DEC-0004, DEC-0005, DEC-0008, DEC-0009, DEC-0010]
example: false
created: 2026-09-22
---

# R-0013 — Round-2 AGREEMENT_MATRIX backfill (adversarial-reviewer column), as an addendum review

## Scope

W-0003 (owner: adversarial-reviewer, opened 2026-09-14 from Round 2's leftover). Round 2's
`research/AGREEMENT_MATRIX.md` requires each agent to fill **only its own column**, one cell per
debate, with `<state> — <one-line AGREE/DISAGREE reason>` where state ∈ {AGREED, ROUTED,
CONFLICT}. My column was left empty in all six rows. Per W-0003 and DEC-0009 the honest
completion is an **append-only review record**, not an edit to the matrix: I verified the matrix
is untouched since its last commit (`9b69e0a`, 2026-09-14 00:01:50 +0300; `git status` clean for
that path) and I did not write to it. This record carries the column that should have been filled
in Round 2, sourced from my own Round-2 outputs (R-0002, my Agent C/D positions in D-0002…D-0006,
`beliefs.md`, `current_position.md`), with a `since:` note wherever the collective has moved the
item on — so the backfill is *historical*, not a re-litigation.

## Round-2 artifacts reviewed (W-0003 exit check)

- `research/AGREEMENT_MATRIX.md` (the artifact being backfilled; not edited).
- `research/AGENT_MEGAPROMPT_ROUND2.md` (§2's three terminal states; §3.C/§6's matrix rules).
- `research/reviews/R-0002-…` (my review of the six-report researcher-architect corpus — the three
  required answers: D-0004 confirmed at runtime; H-0010's SPRT bar direction right,
  parameterization wrong → two tiers; H-0005's falsification bound is ratio < 3.0, and the record
  stated it backwards).
- `research/debates/D-0001-…` (row present, but **`example: true`** — mock positions only) and
  `D-0002-…`, `D-0003-…`, `D-0004-…`, `D-0005-…`, `D-0006-…` (my Agent C/D entries).
- `research/experiments/E-00003-…` (the measured /O2-vs-/Od baseline the D-0002/D-0003 rows cite).
- `research/hypotheses/H-0003, H-0005, H-0006, H-0008, H-0009, H-0010, H-0011` (the hypotheses the
  rows route to).
- `research/agents/adversarial-reviewer/{beliefs.md, current_position.md}` (the standing record of
  the positions backfilled here).
- `research/work/W-0003-…` (this item) and E-0010's Follow-Up (cited as the routing source — see
  Factual Errors).

## The column that should have been there (Round-2 states)

| Debate | adversarial-reviewer cell |
|---|---|
| D-0001 | **ROUTED** (mock row) — AGREE with classical-first because MCTS/PUCT without a policy-value net is circular (nets need games; games need a playing engine) and the GPU branch needs its own latency/throughput gate; DISAGREE with treating E-00004 as that gate as written (wrong fan-out, thresholds not PUCT-shaped — re-spec before it gates anything). *since:* D-0001 is an `example: true` debate; the live positions live in H-0003/H-0015 and the O-series records, and the roadmap is now settled by evidence (O3d COMPLETE, E-0010 measured), not by this row. |
| D-0002 | **AGREED** — AGREE with researcher-architect that pre-E-0002 NPS numbers may be cited only as provisional (~2 sig figs, unpinned, single machine) and that `kana_o2.exe` stays excluded until its provenance is documented; DISAGREE with the "no NPS number is interpretable" framing, because E-00003 had already measured the /O2-vs-/Od gap (~2.3x; counts bit-identical; I re-ran it). Rule: trust is (value + protocol + provenance); any number that changes a roadmap or enters project_state.md must be E-0002-certified. *since:* E-0002 is COMPLETED and the baseline CERTIFIED (43–47 Mnps /O2, 5 reps, pinned, SHA-256 logged) — implemented, so this row is now AGREED-by-evidence. |
| D-0003 | **ROUTED** — AGREE with the revised 1.3–2.5x magnitude as the working prior (my conf 0.5, not 0.6: slider share unprofiled) and DISAGREE with the backwards falsification sentence in H-0005's addendum; pre-register exactly ONE 4-way partition at /O2, bit-identical perft counts, within-session paired runs, ratio + CI: ≥3.0 → H-0005 holds; [1.3, 3.0) → H-0006 supported; (1.0, 1.3) → both magnitudes falsified, direction survives; ≤1.0 → both falsified. A point estimate near 1.3 or 3.0 is not a decision; report the CI. *since:* E-00005's profile left the slider-attributable share unmeasured and E-PEXT has not run, so the row remains ROUTED — the experiment is fully pre-registered and unexecuted. |
| D-0004 | **AGREED** — AGREE with the pseudo-legal reading, DEMONSTRATED not inspected: pinned-rook FEN `7k/8/8/8/8/8/8/r3R2K w - - 0 1` gives perft(1) = 9 legal vs `generate_moves` = 16 pseudo-legal; adopt "pseudo-legal + king-safety filter at the search/perft site", fix the DEC-0005/README wording, no behavior change. *since:* DEC-0008 ratified exactly that (2026-09-10) and the search/eval work consumes it as the contract — AGREED-by-decision. |
| D-0005 | **ROUTED** — AGREE with keeping make/unmake (DEC-0004) as the O3 default (conf 0.6) and DISAGREE with running copy-make as a blocking gate: pre-register a side microbench with a ≥5 % time-to-depth advantage at a depth with ≥10 s TTD, reproduced on both suites, else DEC-0004 stands; both paths must produce identical search results (the debate is cost attribution, not correctness). *since:* E-COPYMAKE still unrun; row remains ROUTED. |
| D-0006 | **AGREED** (on the conclusion, with an amendment) — AGREE quiescence-first (conf 0.65) but NOT for the architect's stated reason (leaf-noise); the decisive argument is that a PVS/TT node-count measured before quiescence is re-measured after it, so the reverse order saves no work and delays the first score-interpretable engine. AMEND the resolution: the "crossover" experiment as written is vacuous (both paths converge by construction — a tie-break is not evidence); pre-register measurable proxies instead (days-to-interpretable-SPRT, fixed-depth nodes/TTD matrix, regression pins while quiescence is developed). *since:* executed as the O3a→O3b→O3c→O3d staged build with node-count pins (E-00006…E-00009); the amendment is satisfied in substance. |

## Agreements

- The matrix's three-state vocabulary was the right device for Round 2: "unanimity is only
  expected on the demonstrated facts" (perft 10/10, the /O2-vs-/Od gap, the pseudo-legal
  contract) is exactly what my column shows — AGREED on the two demonstrated rows (D-0002,
  D-0004), ROUTED on the three empirical ones (D-0001 mock, D-0003, D-0005), AGREED-with-amendment
  on the one methodology row (D-0006). No row was or is a CONFLICT: every open item had (or now
  has) a pre-registered decision rule, which is the property Round 2 existed to produce.
- The states above are consistent with my Round-2 record and with every subsequent ratification —
  nothing in this backfill contradicts DEC-0008, DEC-0010, E-0002 or the O-series results.

## Disagreements

None about content. One process observation: the matrix's states have no on-disk home now that
the matrix is frozen (all six debates are still formally `status: OPEN`, and two of the three
CONFLICT-resolution devices live in other record kinds — decisions and experiments). That is a
limitation of the *tooling*, not of the backfill; this review is the durable statement of the
column, and W-0003's exit check is satisfied by naming it here.

## Missing Arguments

None required for W-0003's exit check. For completeness: the column cannot state a *current*
position on D-0001/D-0003/D-0005 better than "ROUTED" until their experiments run (E-PEXT,
E-COPYMAKE); when they do, the states move by evidence in the experiment/decision records, not by
editing the frozen matrix — the matrix is a Round-2 artifact and stays that way.

## Factual Errors

Two citation/format nits in the surrounding paperwork, neither affecting the backfill's content:

1. W-0003's work log says the item was "routed from E-0010's open item (ii)". E-0010's Follow-Up
   carries items **(1)–(4)**, none of which is the matrix column; the actual obligation comes from
   `AGREEMENT_MATRIX.md`'s own header ("adversarial-reviewer — fill your column from R-0002 and
   your D-0002…D-0006 positions") and from Round 2 §3.C/§6. The citation should be corrected in
   W-0003's closing note (routing, not content).
2. The matrix's D-0001 row mixes a **mock** debate (`example: true`) with real positions from
   other agents; its reviewer cell must therefore be read as illustrative — flagged in the table
   above rather than silently treated as a real Round-2 disagreement.

## Assumptions

- The positions backfilled here are the ones I held in Round 2 as recorded in R-0002 /
  D-0002…D-0006; where my later records refined a number (e.g. the 1.3–2.5x prior at conf 0.5,
  H-0010's two tiers), the backfill uses the Round-2 form and marks the refinement with `since:`.
- "AGREED" in the matrix's vocabulary means "demonstrated or pre-registered; no further work
  before it may be acted on" (Round 2 §2), not "we all believe the same thing" — D-0006's
  AGREED-with-amendment is consistent with that reading.

## Proposed Experiments

None — this is a backfill, not an empirical item. The two routed rows already have their
pre-registered experiments (E-PEXT via D-0003's 4-way partition; E-COPYMAKE via the ≥5 % TTD rule)
queued behind the current Round-4 work; when they run, the debate states close by record.

## Verdict

**COMPLETED — the backfill is closed as a review record and the matrix is untouched.** Exit
check: this review is COMPLETED and names every Round-2 artifact it covers (above). W-0003 now
requires `verified_by != owner`, so a handoff (**HO-0005**) is filed to the verification-auditor
seat; W-0003 stays IN_PROGRESS until that verification lands. Nothing here changes any hypothesis,
decision, or experiment.

## Date

2026-09-22

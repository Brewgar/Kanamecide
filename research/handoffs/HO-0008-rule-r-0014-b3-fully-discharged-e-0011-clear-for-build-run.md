---
id: HO-0008
type: handoff
from: researcher-architect
to: adversarial-reviewer
work_item: W-0001
status: DONE
title: Rule R-0014 B3 fully discharged after the end-vocabulary addendum (E-0011 clear for build+run)
artifacts: ["research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md", "research/reviews/R-0014-critique-e-0011-addenda-b1-b2-b3-response-ruling.md", "research/context/_s12_endscan.py", "research/context/_s12_endscan_out.txt"]
commands: ["git diff --numstat research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md", "python research\\context\\_s12_endscan.py", "python research/scripts/research.py validate"]
acceptance: "a ruling (new review or a dated append to a new R-####) that R-0014 B3 is FULLY discharged and E-0011 is clear for build+run; E-0011 may then leave PENDING"
example: false
created: 2026-09-23
closed: 2026-09-23
---

# HO-0008 — Rule R-0014 B3 fully discharged (end vocabulary + (Ns) suffix)

## Request
R-0014 ruled PARTIAL with exactly one blocking item: the `end` vocabulary vs the
retained EV-0001-family JSONL (`stalemate`, `draw-material` present; undeclared `(Ns)`
suffix). The fix is landed in a new dated addendum — **"Addendum: R-0014 B3 response,
2026-09-23"** — at the end of E-0011, as **pure additions** (verify: `git diff --numstat`
shows `+65/−0`; the original text is untouched). Rule whether it is exactly R-0014's
ordered fix:

1. closed set extended to `{mate, stalemate, draw-material, rule50, repetition, plycap,
   crash}` (R-0014's verbatim sentence quoted in the addendum);
2. `(Ns)` declared: NOT part of the token — a separate `end_seconds` field; N = whole
   elapsed game seconds (single definition for every class, driver source cited);
   normative status = required telemetry, never part of the membership test; legacy
   reader rule = split at `(`;
3. Dataset schema line + B3.1 conjunct amended by the addendum (append-only), plus the
   legacy-token mapping (`draw-claim` → {rule50, repetition} split; `crash` covering the
   crash rule) and a 4th synthetic-test fixture (legacy suffixed row must FAIL campaign
   schema, parse under the reader rule).

Check independently: my read-only scan (`_s12_endscan.py`, engine-free, EXIT:0) shows
all-six realized totals mate 1043 / draw-claim 80 / plycap 72 / draw-material 43 /
stalemate 2 = 1,240, every raw token suffixed. **Surfaced doc nit for your ruling:** you
state "draw-material (all six rungs, 33/1,240)"; 33 is exactly the k1–k5 subtotal —
all-six is 43 (k6 contributes 10). The finding stands under either count; please
reconcile the number as part of the ruling.

## Artifacts To Read (paths)
- `research/experiments/E-0011-…md` — last section ("Addendum: R-0014 B3 response")
- `research/reviews/R-0014-critique-e-0011-addenda-b1-b2-b3-response-ruling.md` (the order)
- `research/context/_s12_endscan.py` + `_s12_endscan_out.txt` (scan + output)

## Commands To Run
```powershell
git diff --numstat research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md
python research\context\_s12_endscan.py     # read-only; expect exit 0, totals as above
python research/scripts/research.py validate
```

## Acceptance Criteria (what makes this DONE)
- A ruling that **B3 is FULLY discharged** (the ONE remaining block from R-0014) —
  as a new review record or a dated append in a new R-#### — with the command outputs
  above in its evidence.
- On that ruling, E-0011 is **clear for build+run** (still contingent on the build
  session's own acceptance steps; the reviewer/owner flips PENDING → RUNNING).

## Response (receiver, append-only)
- 2026-09-23 — adversarial-reviewer (S-0014) — **DONE. Ruling: B3 FULLY DISCHARGED (FIXED) —
  E-0011 is CLEARED FOR BUILD+RUN.** Review: **R-0016** (`kind: critique`, `target: E-0011`,
  linked W-0001 + HO-0008, COMPLETED). All three micro-checks pass, each with the command +
  output pasted into R-0016's evidence appendix:
  1. **Vocabulary matches the retained evidence.** `python research\context\_s12_endscan.py` →
     exit 0; normalized all-six totals mate 1043 / draw-claim 80 / plycap 72 / draw-material 43
     / stalemate 2 (= 1,240, every token suffixed). The extended set
     `{mate, stalemate, draw-material, rule50, repetition, plycap, crash}` maps every realized
     legacy token explicitly (incl. `draw-claim` → rule50|repetition pair, with the honest
     "legacy discriminator not recoverable; audit reads map to the pair-union" caveat) and the
     set is closed over the family's reachable endings.
  2. **Suffix policy declared and schema-consistent.** `(Ns)` is NOT part of the token; it is a
     separate `end_seconds` field (required telemetry, never in the membership test); gate (d)
     checks the suffix-stripped token + a non-negative int `end_seconds`; emission is
     suffix-free and a legacy reader rule (split at `(`) keeps the retained evidence valid;
     the Dataset section's `end` line + B3.1 conjunct are amended BY the addendum (append-only)
     with the operative schema stated inline; the synthetic-20 negative test gains a 4th
     fixture (legacy-suffixed row must FAIL the campaign schema while parsing under the reader
     rule), so the rule is implemented, not assumed.
  3. **Pure additions.** `git diff --numstat 690e145 5026fb5 -- 'research/experiments/E-0011*'`
     → `65 0` (0 deletions, one trailing hunk `@@ -389,5 +389,70 @@`); no `-` content lines.
  **Doc-n reconciled (my error):** R-0014's "33 draw-material games" was the k1–k5 subtotal
  (11+8+6+3+5); the correct all-six figure is **43/1,240**, k6 contributing 10. The finding was
  never in doubt (present on every rung) but the number was wrong and is corrected in R-0016.
  One non-blocking note for the build seat: pin the `rule50` vs `repetition` precedence for
  the rare both-predicates-fires case (immaterial to any gate). `validate` → exit 0, 0 problems.
  Combined with R-0014 (B1/B2/N1–N7/UCI/gate-(f)) the record is clean; the reviewer/owner may
  flip E-0011 PENDING → RUNNING.

## Verification (receiver, append-only)
- raw output / exit codes / hashes: `python research\context\_s12_endscan.py` → exit 0
  (`mate 1043, draw-claim 80, plycap 72, draw-material 43, stalemate 2`, total 1,240; per-rung
  draw-material 11/8/6/3/5/10).
  `git diff --numstat 690e145 5026fb5 -- 'research/experiments/E-0011*'` → `65  0` (0 deletions;
  single trailing hunk). `python research/scripts/research.py validate` → exit 0, "Validation
  OK — statuses are in-vocabulary; … repo-root hygiene is respected". No engine work run.
- verdict: **B3 FIXED / FULLY DISCHARGED — E-0011 cleared for build+run** (subject to the
  build session's own pre-registered acceptance steps: synthetic-20 FAIL demo incl. the 4th
  legacy-suffix fixture, the deterministic truncation drill, and the UCI entry path confirmed
  first). No engine work was run this micro-session.

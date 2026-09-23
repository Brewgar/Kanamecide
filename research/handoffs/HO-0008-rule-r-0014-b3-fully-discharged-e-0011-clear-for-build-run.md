---
id: HO-0008
type: handoff
from: researcher-architect
to: adversarial-reviewer
work_item: W-0001
status: REQUESTED
title: Rule R-0014 B3 fully discharged after the end-vocabulary addendum (E-0011 clear for build+run)
artifacts: ["research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md", "research/reviews/R-0014-critique-e-0011-addenda-b1-b2-b3-response-ruling.md", "research/context/_s12_endscan.py", "research/context/_s12_endscan_out.txt"]
commands: ["git diff --numstat research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md", "python research\\context\\_s12_endscan.py", "python research/scripts/research.py validate"]
acceptance: "a ruling (new review or a dated append to a new R-####) that R-0014 B3 is FULLY discharged and E-0011 is clear for build+run; E-0011 may then leave PENDING"
example: false
created: 2026-09-23
closed: null
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
- (pending)

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: (pending)

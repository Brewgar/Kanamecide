---
id: R-0016
type: review
reviewer: adversarial-reviewer
target: E-0011
kind: critique
status: COMPLETED
work_item: W-0001
related: [E-0011, R-0014, HO-0008, W-0001, EV-0001, R-0011]
example: false
created: 2026-09-23
---

# R-0016 — Ruling on R-0014 B3 (E-0011 `end` vocabulary + `(Ns)` suffix) after the 2026-09-23 addendum

## Scope

HO-0008, adversarial-reviewer micro-session (S-0014). Micro-brief: check minimally and exactly
three things — (i) the closed `end` vocabulary now matches what the EV-0001-family JSONL
actually contains; (ii) the `(Ns)` suffix policy is declared and consistent with the Dataset
schema line; (iii) `git diff` of the E-0011 change against the S-0011 state is pure additions.
No engine work was run. The addendum under review is "Addendum: R-0014 B3 response,
2026-09-23" in E-0011 (author commit `5026fb5`).

## Check 1 — vocabulary vs EV-0001-family reality: **PASS**

`python research\context\_s12_endscan.py` → **EXIT 0**; normalized (suffix-stripped) realized
totals over all six retained rungs: **mate 1043, draw-claim 80, plycap 72, draw-material 43,
stalemate 2 = 1,240** (every raw token is suffixed, e.g. `mate(8s)`).

The addendum's operative set is `{mate, stalemate, draw-material, rule50, repetition, plycap,
crash}` and it maps every realized legacy token explicitly: `mate`→`mate`, `stalemate`→`stalemate`,
`draw-material`→`draw-material`, `plycap`→`plycap`, `draw-claim`→ the `rule50` / `repetition`
pair (with the honest statement that "for any legacy row the discriminator is not recoverable
from the retained JSONL alone, so audit reads map legacy `draw-claim` to the pair-union"), and
`crash` for the DEC-0010 crash rule alongside `crash_incident`. The set is therefore **closed
over the family's reachable endings** — the exact defect R-0014 named — and the two terminals
my spot-check found (`stalemate`, `draw-material`) are now first-class members.

## Check 2 — suffix policy declared and schema-consistent: **PASS**

Quoting the declaration:

> **Decision on the suffix …: the `(Ns)` suffix is NOT part of the token; it is a separate
> `end_seconds` field.** … **Normative status:** `end_seconds` is REQUIRED TELEMETRY (integer
> ≥ 0, present in every record), NOT a member of the closed vocabulary and NOT part of any
> membership test: gate (d) checks the suffix-stripped token against the extended set and
> checks `end_seconds` is a non-negative integer. … the reader splits at `(`. … Retained
> evidence stays valid under the reader rule without rewrite.

and the schema-agreement clause:

> **Dataset-schema agreement:** … the Dataset section's `end` schema line and the B2/B3.1
> conjunct are amended BY THIS ADDENDUM (append-only …): the operative schema for the campaign
> is `end` ∈ the extended suffix-free set above AND `end_seconds` (int ≥ 0) AND `crash_incident`
> when `end == crash`. `tools/e0011_check.py` implements exactly this … the synthetic-20-game
> negative test gains a fourth fixture: one legacy-style suffixed `end` row must FAIL the
> campaign schema while parsing cleanly under the reader rule (proving the rule is implemented,
> not assumed).

This is the exact choice R-0014 offered ("strip at emission or promote to a distinct field"),
it is internally consistent (token, field, gate test, and reader rule all agree), and the
original schema line is preserved as history while the operative schema is stated in the
addendum — the same append-only mechanism used by B1.1/B1.2. The 4th synthetic fixture means
the reader rule is testable at build time, not merely asserted.

## Check 3 — pure additions: **PASS**

```
git diff --numstat 690e145 5026fb5 -- 'research/experiments/E-0011*'
  → 65	0	research/experiments/E-0011-…-deduplicated-game-dataset.md
removed ('-') content lines in that diff → (none)
hunk header → @@ -389,5 +389,70 @@   (append at EOF; context lines only)
```
65 insertions, 0 deletions, single trailing hunk. The original pre-registered text is intact.

## Doc-n reconciliation (the architect surfaced a real error in MY review)

R-0014 states "draw-material (insufficient material, 33 games across the retained evidence)". The
architect's scan is right: **all-six is 43**; 33 is exactly the k1–k5 subtotal
(11 + 8 + 6 + 3 + 5), with k6 contributing 10. My S-0010 spot-check printed the per-rung
suffixed groups and I summed the first five rungs when I wrote the 33. **Corrected figure:
43/1,240 games (3.5 %), present on every rung** (11, 8, 6, 3, 5, 10). The finding itself —
`draw-material` is a reachable ending absent from the declared vocabulary — is unchanged and
was correct under either count; the number was the error, and it is reconciled here. Thanks for
the catch; a reviewer's arithmetic gets audited like everyone else's.

## Non-blocking implementation note (for the build seat, not a finding)

The new campaign splits legacy `draw-claim` into `rule50` (fifty-move claim fired) and
`repetition` (threefold repetition fired). python-chess can, in rare positions, have
`is_repetition(3)` and `can_claim_fifty_moves()` both true (≥100 plies with no pawn move or
capture, plus a threefold). The record does not state which label wins in that overlap. It is
immaterial to every gate (both labels are in the closed set; nothing branches on the
distinction) — but the implementer should pick a precedence (e.g. check repetition first) and
write it in one comment, so the `end` field is deterministic. Recorded for completeness, not
as a condition.

## Verdict

**B3: FIXED (FULLY DISCHARGED).** All three ordered elements landed verbatim, the vocabulary
matches the retained evidence, the suffix policy is declared and consistent, and the change is
pure additions. Combined with R-0014's rulings (B1, B2, N1–N7, UCI note, gate (f)) **E-0011 is
cleared for build+run** — with the standing pre-conditions that are the build session's own
acceptance steps (synthetic-20 FAIL demo incl. the 4th legacy-suffix fixture, the deterministic
truncation drill, and confirming the UCI entry path before any live run). The reviewer/owner
flips E-0011 PENDING → RUNNING; the ruleset, thresholds, tiers and N-values are unchanged by
this addendum.

## Date

2026-09-23

## Evidence appendix

1. `python research\context\_s12_endscan.py` → EXIT 0 →
   `research\context\_s12_endscan_out.txt`; normalized: mate 1043, draw-claim 80, plycap 72,
   draw-material 43, stalemate 2; per-rung draw-material: k1n 11, k2n 8, k3n 6, k4n 3, k5n 5,
   k6n 10.
2. `git diff --numstat 690e145 5026fb5 -- 'research/experiments/E-0011*'` → `65  0`; no `-` lines;
   one hunk `@@ -389,5 +389,70 @@`.
3. `python research/scripts/research.py validate` → EXIT 0, "Validation OK … repo-root hygiene is
   respected".
4. Addendum text quoted above (E-0011, "Addendum: R-0014 B3 response, 2026-09-23", lines
   392–455).

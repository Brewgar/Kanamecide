---
id: W-0002
type: work
title: "Recalibrate the E-0010 effect-size decision rule (D-0007 -> DEC-0010)"
round: 4
owner: adversarial-reviewer
status: IN_PROGRESS
deliverable: "research/debates/D-0007-*.md (RESOLVED) + research/decisions/DEC-0010-*.md (ACTIVE) + addendum review on E-0010"
exit_check: "DEC-0010 ACTIVE citing E-0010's measured CI95; E-0010 outcome restated under the calibrated rule in an ADDENDUM review (record untouched)"
evidence: ["research/debates/D-0007-e0010-effect-size-decision-rule-what-is-decidable-at-achievable-n.md (RESOLVED; arithmetic incl. N-vs-half-width, ASN table, the fixed-sample counter-case)", "research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md (ACTIVE; tiers S/R/M with margins, alpha=beta=0.05, LLR +/-2.944, caps 8k/30k/8k, post-cap INCONCLUSIVE, draw/opening/color/crash protocol, E-0010 outcome table)", "research/reviews/R-0009-addendum-e0010-outcome-under-the-dec-0010-calibrated-rule.md (COMPLETED, kind: critique; E-0010 untouched)", "research/context/w0002_power.py + w0002_power_output.txt (reproducible derivation; conservative Elo-space and score-space LLR cross-check)", "research/context/bootstrap/gate0.txt (Gate 0 attempted once this session: App Control policy block, no process started — F-0002 class)"]
verified_by: null
verification_verdict: null
example: false
created: 2026-09-14
closed: null
---

# W-0002 — Recalibrate the E-0010 effect-size decision rule

## Objective
The pre-registered ">=150 Elo" bar for E-0010 was a guess with no power analysis: at
N=240 the CI half-width is ~±47 Elo, so the rule could never be confirmed (R-0003 F6).
Decide, openly, what the rule should be — then restate E-0010's outcome under it.

## Deliverable (exact path(s))
- `research/debates/D-0007-*.md`, `research/decisions/DEC-0010-*.md`,
  `research/reviews/R-####-*.md` (addendum review on E-0010; the E-0010 record itself is
  append-only and must not be edited).

## Exit Check
```powershell
python research/scripts/research.py validate   # OK
python research/scripts/research.py decisions  # DEC-0010 listed ACTIVE
```

## Evidence
- (to be filled)

## Work Log (append-only while OPEN)
- 2026-09-14 — opened by Round-4 meta-agent; routed from E-0010's open item (i).
- 2026-09-21 — adversarial-reviewer (this session): deliverable complete.
  (1) Gate 0 attempted ONCE as instructed: `build\Release\kana.exe` → App Control
  policy block, no process started (F-0002 class; output in
  `research/context/bootstrap/gate0.txt`); W-0002 needs no engine and proceeded.
  (2) Derived the full cost table from MEASURED E-0010 numbers (sigma=371 Elo/game
  from the six verified rung CIs; throughput 769 games/hour from the 1240-game/5807 s
  campaign) — script `research/context/w0002_power.py`, output
  `research/context/w0002_power_output.txt`. Key results: 20-Elo screen ~1.8-2.0k
  games ASN (cap 8k); 5-Elo regression ~29-32k ASN (cap 30k, midpoint effects →
  INCONCLUSIVE by design); ">=150" is **unwinnable at any N** when the true effect is
  below 150, and costs ~14.9k games to confirm against a true +160; the [100,150]
  zone SPRT decides the E-0010 magnitude question in ~910 predicted games (routed in
  D-0007 as E-MAG-6V0).
  (3) Filed `debates/D-0007-...` (RESOLVED by arithmetic, scope stated; Agent B's
  fixed-sample objection recorded as the strongest counter-case, not papered over;
  routed residuals named: W-0005 model validation, E-MAG-6V0 magnitude decision).
  (4) Filed `decisions/DEC-0010-...` (ACTIVE; tiers S/R/M with null/alternative
  margins, alpha=beta=0.05 → LLR +/-2.944, caps 8,000/30,000/8,000, post-cap
  INCONCLUSIVE, trinomial draws-as-halves model, E-0010 opening/color protocol,
  crash/stall=loss, one-look rule, reversal conditions).
  (5) Filed `reviews/R-0009-...` (kind: critique, COMPLETED; E-0010 untouched;
  restatement: screening PASS, regression PASS, [100,150] magnitude INCONCLUSIVE at
  N=240; explicit list of what remains unproven).
  (6) E-0010, R-0004, R-0008, H-0010 were READ ONLY — no edits to reviewed records.
  (7) Cannot self-verify (owner = this seat): handoff filed to verification-auditor
  to re-run the exit check; item stays IN_PROGRESS until a fresh verifier decides.

## Verification
- verified_by: (pending — handoff `HO-0002` filed 2026-09-21 to the rotating
  verification-auditor seat; the owner of W-0002 is this seat, so it cannot self-verify)
- verdict: (pending the fresh verifier's INDEPENDENT re-run of the exit check)
- evidence: (to be filed by the verifier as a `kind: verification` review record +
  raw command outputs; acceptance criteria in HO-0002)
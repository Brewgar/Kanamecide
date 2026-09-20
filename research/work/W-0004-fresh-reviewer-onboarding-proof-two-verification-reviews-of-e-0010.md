---
id: W-0004
type: work
title: "Fresh-reviewer onboarding proof: two independent verification reviews of E-0010"
round: 4
owner: verification-auditor
status: OPEN
deliverable: "two research/reviews/R-#### (kind: verification) of E-0010 by brand-new agents, plus updated agents/ASSIGNMENTS.md rows"
exit_check: "two verification reviews COMPLETED, each re-running e0010_report.py and listing any number that did not reproduce; reviewers are not owners of any verified item"
evidence: []
verified_by: null
verification_verdict: null
example: false
created: 2026-09-14
closed: null
---

# W-0004 — Fresh-reviewer onboarding proof

## Objective
The owner will onboard two completely new agents. Prove the bootstrap path works: each
new agent starts from the repo ALONE (research/README.md → AGENT_MEGAPROMPT.md →
agents/verification-auditor/profile.md → `research.py status --brief` → Gate 0) and
delivers one `kind: verification` review of E-0010 — re-running
`python e0010_report.py`, recomputing the ladder Elo/CI/LOS numbers, and checking
`duplicate-move-lists=0`.

## Deliverable (exact path(s))
- `research/reviews/R-####-verification-of-e-0010-*.md` ×2
- `research/agents/ASSIGNMENTS.md` rows for the two occupants.

## Exit Check
```powershell
python research/scripts/research.py reviews     # both listed, COMPLETED
python research/scripts/research.py validate    # OK
```

## Evidence
- (to be filled)

## Work Log (append-only while OPEN)
- 2026-09-14 — opened by Round-4 meta-agent (SYSTEM.md §5; G1/Q5).
- 2026-09-14 — verification-auditor seat, occupant 1 (fresh agent, zero chat history):
  bootstrap completed per SYSTEM.md §11 (README → MEGAPROMPT → ASSIGNMENTS row found →
  profile/current_position/beliefs → ROUND4 megaprompt → SYSTEM.md → project_state →
  index skim). Gate 0: `build\Release\kana.exe` → 10/10 PASS, `=== ALL TESTS PASSED`
  (exit 0). `research.py validate` → OK. Ran `python e0010_report.py` (exit 0) and
  reproduced EVERY published E-0010 number (full k1-k6 ladder Elo/CI95/LOS, W/L/D,
  N per rung, bad=0 legality, duplicate-move-lists=0 on every rung, k6 +116.1 /
  [+70.8,+163.5] / LOS 100.00% / N=240, FAIL verdict per pre-registered rule).
  Recomputed binary SHA-256 `504EB01A…A6DAA` — matches the measurement binary. Gate
  (b)/(d) confirmed from raw `e0010_gates_bd.txt` (not re-executed live). Two cosmetic
  nits recorded (Wrate label collision in the aggregator; front-matter "(N=240)"
  ambiguity). Filed `research/reviews/R-0004-…` (kind: verification), verdict VERIFIED.
  Occupant 2's review still pending — item remains OPEN.
- 2026-09-20 — verification-auditor seat, occupant 3 (fresh agent, zero chat history):
  the second required review is delivered — `reviews/R-0008-second-independent-verification-of-e-0010-fresh-agent-w-0004-occupant-3.md`
  (kind: verification, COMPLETED, **VERIFIED**). Re-ran `python e0010_report.py` (exit 0;
  full k1–k6 ladder reproduced; gate (c) FAIL exactly as recorded), added a from-scratch
  k6 recomputation via a different algorithm (Elo +116.1225, CI95 [+70.76,+163.51],
  LOS 99.999980%), re-derived all six raw JSONL tallies (`res` counts == `result.txt`;
  dupes=0; BAD=0; 1240 games total) and recomputed `kana.exe` SHA-256 = EV-0010's
  (`504EB01A…A6DAA`). Deliverable (two reviews) is now complete (R-0004 + R-0008).
  Item left **OPEN**: its owner is this role itself, so DEC-0009 gate 3
  (`verified_by` ≠ owner) cannot be satisfied by this seat — needs a non-seat verifier
  or an owner decision. Gate 0 was blocked this session (F-0002), so gates (b)/(d) were
  re-read, not re-executed.

## Verification
- verified_by: verification-auditor seat, occupant 1 — review R-0004
  (`research/reviews/R-0004-independent-verification-of-e-0010-fresh-agent-w-0004-occupant-1.md`,
  kind: verification, status: COMPLETED)
- verdict (R-0004, on the E-0010 reproduction): VERIFIED — every published E-0010
  number reproduced from raw evidence by a fresh agent with no prior chat history;
  the recorded FAIL follows the pre-registered decision rule as written. No number
  failed to reproduce.
- evidence: `python e0010_report.py` exit 0 (raw output retained at
  `research/context/_e0010_report_out.txt`, gitignored local); perft 10/10
  `=== ALL TESTS PASSED` (`research/context/_gate0.txt`); SHA-256 recomputed
  (`research/context/_kana_sha.txt`); raw JSONL/result/gates files read directly.
- Note: W-0004's exit check requires TWO verification reviews (occupant 2 pending);
  this item therefore stays OPEN and unmarked-DONE until the second review lands.
  The verifier (occupant 1) is not the owner of E-0010, W-0001, or W-0002.
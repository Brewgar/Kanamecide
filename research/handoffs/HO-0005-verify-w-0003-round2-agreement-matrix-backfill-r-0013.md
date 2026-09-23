---
id: HO-0005
type: handoff
from: adversarial-reviewer
to: verification-auditor
work_item: W-0003
status: REQUESTED
title: "Verify W-0003: R-0013 (Round-2 AGREEMENT_MATRIX backfill) and the untouched matrix"
artifacts: ["research/reviews/R-0013-round2-agreement-matrix-backfill.md", "research/work/W-0003-round2-agreement-matrix-reviewer-column-backfill.md", "research/AGREEMENT_MATRIX.md", "research/AGENT_MEGAPROMPT_ROUND2.md", "research/reviews/R-0002-review-of-researcher-architect-6-report-corpus-pseudo-legal-contract-sprt-bar-falsification-bounds.md"]
commands: ["python research/scripts/research.py validate", "git --no-pager log -1 --format='%h %ci' -- research/AGREEMENT_MATRIX.md", "git --no-pager status --porcelain -- research/AGREEMENT_MATRIX.md"]
acceptance: "a kind:verification review (R-####) COMPLETED that states: (a) R-0013's six row states match my Round-2 positions as recorded in R-0002 and D-0002..D-0006 (Agent C/D); (b) the matrix file is byte-untouched since 9b69e0a / no local modifications; (c) R-0013's exit-check claim (names every Round-2 artifact reviewed) is accurate; then set W-0003 verified_by=verification-auditor, verdict VERIFIED or a named defect"
example: false
created: 2026-09-22
closed: null
---

# HO-0005 — Verify the W-0003 backfill review (R-0013)

## Request

W-0003's exit condition requires `verified_by != owner`; the owner is the adversarial-reviewer
(this seat), so the verification belongs to your seat. Verify, without re-trusting my summary:

1. **State fidelity:** each of R-0013's six cells (D-0001…D-0006) asserts a Round-2 position.
   Check them against the on-disk Round-2 evidence: my Agent C/D entries in
   `research/debates/D-0002..D-0006`, R-0002's three required answers, and
   `agents/adversarial-reviewer/beliefs.md`. Flag any cell whose stated position is NOT the one
   found in those records (a misquoted history is exactly what a backfill must not produce).
2. **Matrix untouched:** `git log -1` on `research/AGREEMENT_MATRIX.md` must still be
   `9b69e0a` (2026-09-14) and `git status --porcelain -- research/AGREEMENT_MATRIX.md` must be
   empty; also check `git diff 9b69e0a...HEAD -- research/AGREEMENT_MATRIX.md` is empty.
3. **Exit-check truth:** R-0013's "Round-2 artifacts reviewed" list is the exit check; confirm
   every listed artifact exists and that the list contains the matrix, the Round-2 megaprompt,
   R-0002, D-0001..D-0006 and E-00003.
4. Note for the record (no rework required): R-0013 flags two citations for correction
   (W-0003's "E-0010's open item (ii)" routing note; the D-0001 mock row). Confirm both exist so
   the correction can proceed with an independent witness.

## Artifacts To Read (paths)

- `research/reviews/R-0013-round2-agreement-matrix-backfill.md`
- `research/work/W-0003-round2-agreement-matrix-reviewer-column-backfill.md`
- `research/AGREEMENT_MATRIX.md` (read-only)
- `research/AGENT_MEGAPROMPT_ROUND2.md` (states + matrix rules)
- `research/reviews/R-0002-*.md` and `research/debates/D-0002..D-0006` (the source positions)
- `research/agents/adversarial-reviewer/beliefs.md` / `current_position.md`

## Commands To Run

```powershell
python research/scripts/research.py validate
git --no-pager log -1 --format='%h %ci' -- research/AGREEMENT_MATRIX.md
git --no-pager status --porcelain -- research/AGREEMENT_MATRIX.md
git --no-pager diff 9b69e0a...HEAD --stat -- research/AGREEMENT_MATRIX.md
```

## Acceptance Criteria (what makes this DONE)

- One `kind: verification` review, COMPLETED, `target: W-0003`, linked to HO-0005, that rules on
  items 1–3 above (VERIFIED / PARTIAL / CONTRADICTED / UNVERIFIABLE with evidence per item), and
  closes W-0003's Verification block accordingly (`verified_by: verification-auditor`).

## Response (receiver, append-only)
- (pending)

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: (pending)

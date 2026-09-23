---
id: HO-0007
type: handoff
from: researcher-architect
to: adversarial-reviewer
work_item: W-0005
status: REQUESTED
title: Re-critique E-0012's R-0012 addenda (B1/B2 responses + adopted null-pair control) before any RUNNING
artifacts: ["research/experiments/E-0012-e-sprt-lite-comparison-harness-pre-registered-dec-0010-tiers.md", "research/reviews/R-0012-critique-e-0012-pre-registration-and-offline-sprt-replay.md", "research/work/W-0005-e-sprt-lite-comparison-harness-pre-register-build-validate.md", "research/context/w0005_sprt_replay.py", "research/context/w0005_sprt_replay_output.txt", ".gitignore"]
commands: ["git log --oneline -- research/context/w0005_sprt_replay.py research/context/w0005_sprt_replay_output.txt", "python research/context/w0005_sprt_replay.py", "python research/scripts/research.py validate"]
acceptance: "a NEW critique review (R-####) targeting E-0012's addenda, status COMPLETED, ruling B1 and B2 discharged or still-blocking and accepting-or-attacking the adopted N4 null-pair control; E-0012 stays PENDING unless the ruling is clean"
example: false
created: 2026-09-23
closed: null
---

# HO-0007 — Re-critique the E-0012 addenda (R-0012's blocking findings + N4)

## Request
You filed R-0012 (NOT CLEAN, B1/B2 + N1–N5). Dated addenda are now in E-0012 —
original text untouched (append-only; verify with git). Re-critique **only the
addenda**, ruling each item:

- **B1:** "Addendum: R-0012 B1 response, 2026-09-23" — `.gitignore` negation for the
  two replay artifacts (commit `16ac1ff`); the committed content must byte-match the
  SHA-256s already pinned in E-0012 since `2a9d997`, closing your audit gap: git
  history now shows (i) the hash pins published at 2a9d997 and (ii) the tracked files
  matching them from 16ac1ff onward. Verify both, and verify `validate` stayed green
  after the `.gitignore` change.
- **B2:** "Addendum: R-0012 B2 response, 2026-09-23" — write order (JSONL line fsync
  first, checkpoint after), JSONL authoritative on resume, recompute-by-replay,
  `resume_mismatch` incident, continue-only-at-1e-9-else-ABORT+FAILED, the
  FP-ordering + within-1e-9-of-bound qualification on "identical decision", the
  self-consistency-check limitation (scale detector = offline exact-value reproduction
  + unit tests), the runjob facts (launch unlinks log → harness preserves it;
  splitlines telemetry ≠ integrity signal), and the split-at-every-k unit test as a
  pre-registered harness acceptance step.
- **N4 (your recommendation): ADOPTED, not rejected** — "Addendum: R-0012 N4 adopted +
  N1/N2/N3/N5 text, 2026-09-23" pre-registers the live null-pair control (stage-6 vs
  stage-6, cap 240, Tier-S statistic, colour-corrected null vs your measured White
  58.5%, your drift/sd arithmetic cited — it doubles as the honest-INCONCLUSIVE-path
  test). Attack the exact acceptance formulation if it is wrong; silence is not an
  option per your own N4.
- **N1/N2/N3/N5 text:** band information content (sd ≈ 42, ±1.9σ, ~5.4% false-FAIL,
  detection floor 1.79×/0.69×, (v2)-FAIL → harness-audit-first), refinement-clause
  draw-model requirement, offline-replay blind classes, σ circularity sentence in
  Interpretation — all in the same addendum.

## Artifacts To Read (paths)
- `research/experiments/E-0012-e-sprt-lite-comparison-harness-pre-registered-dec-0010-tiers.md`
  (addenda start at "## Addendum: R-0012 B1 response")
- `research/reviews/R-0012-critique-e-0012-pre-registration-and-offline-sprt-replay.md`
- `research/context/w0005_sprt_replay.py` + `research/context/w0005_sprt_replay_output.txt`
  (now git-tracked) and `.gitignore`

## Commands To Run
```powershell
git log --oneline -- research/context/w0005_sprt_replay.py research/context/w0005_sprt_replay_output.txt  # expect: 16ac1ff
git show 16ac1ff --stat                                          # both files added
certutil -hashfile research\context\w0005_sprt_replay.py SHA256  # expect: 94631d6b...33c (E-0012's pin)
certutil -hashfile research\context\w0005_sprt_replay_output.txt SHA256  # expect: 9cd40402...35ad
python research\context\w0005_sprt_replay.py                     # expect: exit 0, same numbers
python research/scripts/research.py validate                     # expect: OK, 0 problems
```

## Acceptance Criteria (what makes this DONE)
- A NEW `kind: critique` review (R-####), COMPLETED, target E-0012, linked W-0005 and
  HO-0007, with per-item rulings (B1, B2, N4-adopted, N-text: discharged |
  still-blocking) and the git/hash/validate outputs above in its evidence appendix.
- E-0012 stays PENDING unless that ruling is clean AND no new blocking finding appears.
- Verifier is the reviewer seat; I do not re-critique my own fixes.

## Response (receiver, append-only)
- (pending)

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: (pending)

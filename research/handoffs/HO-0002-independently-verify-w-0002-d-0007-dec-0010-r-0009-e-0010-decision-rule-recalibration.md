---
id: HO-0002
type: handoff
from: adversarial-reviewer
to: verification-auditor
work_item: W-0002
status: REQUESTED
title: Independently verify W-0002: D-0007 + DEC-0010 + R-0009 (E-0010 decision-rule recalibration)
artifacts: ["research/debates/D-0007-e0010-effect-size-decision-rule-what-is-decidable-at-achievable-n.md", "research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md", "research/reviews/R-0009-addendum-e0010-outcome-under-the-dec-0010-calibrated-rule.md", "research/context/w0002_power.py", "research/context/w0002_power_output.txt"]
commands: ["python research/scripts/research.py validate", "python research/scripts/research.py decisions", "python research/context/w0002_power.py"]
acceptance: "validate OK 0 problems AND DEC-0010 ACTIVE AND R-0009 COMPLETED AND D-0007 RESOLVED AND w0002_power.py reproduces w0002_power_output.txt AND E-0010 byte-identical to pre-session state AND 3+ of the listed numbers re-derived from scratch"
example: false
created: 2026-09-21
closed: null
---

# HO-0002 — Independently verify W-0002: D-0007 + DEC-0010 + R-0009 (E-0010 decision-rule recalibration)

> The ONLY way to ask another agent to do something. Prose requests ("someone should
> verify this") are not handoffs and will be ignored. Receiver appends `## Response`
> and `## Verification`; the handoff may be edited while `status: REQUESTED|ACCEPTED`
> and is frozen once `DONE|REJECTED|WITHDRAWN`.

## Request

Take this from a zero-history seat (the rotating verification-auditor). Do NOT accept
the author's summary. W-0002's deliverable exists; its owner (adversarial-reviewer) cannot
self-verify (DEC-0009 gate 3), so this handoff asks you to re-run the exit check and
decide whether the three records are what they claim to be: (a) D-0007 RESOLVED on
arithmetic that is actually in the record; (b) DEC-0010 ACTIVE and citing E-0010's
MEASURED CI95 and real power arithmetic; (c) R-0009 an addendum review that restates
E-0010's outcome without touching E-0010.

## Artifacts To Read (paths)
- `research/debates/D-0007-e0010-effect-size-decision-rule-what-is-decidable-at-achievable-n.md`
- `research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md`
- `research/reviews/R-0009-addendum-e0010-outcome-under-the-dec-0010-calibrated-rule.md`
- `research/experiments/E-0010-ee-val-tapered-hand-tuned-evaluation-term-by-term-self-play-elo-attribution.md` (target; append-only — confirm untouched)
- `research/context/w0002_power.py` + `research/context/w0002_power_output.txt` (the arithmetic to re-run)
- `research/work/W-0002-recalibrate-e0010-effect-size-decision-rule-d-0007-dec-0010.md`

## Commands To Run
```powershell
python research/scripts/research.py validate            # expect: OK, 0 problems
python research/scripts/research.py decisions           # expect: DEC-0010 listed ACTIVE
python research/scripts/research.py reviews             # expect: R-0009 COMPLETED
python research/scripts/research.py debates             # expect: D-0007 RESOLVED
python research/context/w0002_power.py                  # re-run the derivation; compare to w0002_power_output.txt
git log --oneline -1 -- research/experiments/E-0010-ee-val-tapered-hand-tuned-evaluation-term-by-term-self-play-elo-attribution.md  # E-0010 last touched BEFORE this session's commit
```

## Acceptance Criteria (what makes this DONE)
- `validate` exit 0 with 0 problems; DEC-0010 ACTIVE; R-0009 COMPLETED; D-0007 RESOLVED.
- `w0002_power.py` re-run reproduces the output file's numbers (or any difference is
  itemized and shown to change/not change the tier verdicts).
- Independent arithmetic check: at least THREE of the following re-derived from scratch
  by you — E-0010's k6 Elo (+116.1 = 400*log10(160/82)), the six per-rung sigma values
  (h*sqrt(N)/1.96 from the recorded CIs), the fixed-sample Ns (3,722 / 59,545 / 14,886),
  the ASN values for the three tiers, and the E-0010 cumulative-LLR verdicts
  (S: H1 accepted; R: fixed-sample pass; M[100,150]: inside bounds at N=240).
- E-0010 record is byte-identical to its pre-session state (git evidence).
- Verdict written in `## Verification` below plus a `kind: verification` review record;
  W-0002 `verified_by`/`verification_verdict` filled by YOU (not the owner), or a
  CONTRADICTED/PARTIAL verdict with named defects.

## Response (receiver, append-only)
- 2026-09-21 — (role) — ...(receiver fills)

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: ...
---
id: W-0001
type: work
title: "E-0011 self-play data pipeline (pre-register, build, run, verify)"
round: 4
owner: systems-researcher
status: OPEN
deliverable: "research/experiments/E-0011-*.md + resumable generator (tools/) + >=1000-game dataset (local)"
exit_check: "generator output: >=1000 legal deduplicated games, duplicate-move-lists=0; resume-from-checkpoint adds no duplicates"
evidence: []
verified_by: null
verification_verdict: null
example: false
created: 2026-09-14
closed: null
---

# W-0001 — E-0011 self-play data pipeline

## Objective
Turn the E-0010 match harness into a resumable, provenance-carrying self-play game
generator + position dataset — the prerequisite for Texel fitting (H-0013) and NNUE.

## Deliverable (exact path(s))
- `research/experiments/E-0011-*.md` (PENDING → RUNNING → COMPLETED)
- Generator script + dataset under a gitignored evidence dir (local), documented in a
  RUN record (`research/runs/`).

## Exit Check
```powershell
# after the run: aggregator over the JSONL checkpoint reports
#   games>=1000, legal=True, duplicate-move-lists=0
# and `runjob.py resume` re-launch adds new games without duplicates.
```

## Evidence
- (to be filled: command → exit code → output path → SHA-256 → src commit)

## Work Log (append-only while OPEN)
- 2026-09-14 — opened by Round-4 meta-agent (SYSTEM.md/DEC-0009 rollout).

## Verification
- verified_by: (a different agent than owner)
- verdict: (VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE)
- evidence: (review record id + command outputs)

> Sequence per AGENT_MEGAPROMPT_ROUND4.md: pre-registration (with power + sample
> validity) must be critiqued by adversarial-reviewer BEFORE `status: RUNNING`. Run under
> `runjob.py` with heartbeat/checkpoint/resume; ≤ 2 engine pairs.
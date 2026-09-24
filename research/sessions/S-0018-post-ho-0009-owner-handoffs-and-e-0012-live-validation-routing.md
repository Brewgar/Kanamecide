---
id: S-0018
type: session
agent: researcher-architect
round: 4
title: Post-HO-0009 owner handoffs and E-0012 live-validation routing
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-24
closed: 2026-09-24
---

# S-0018 — Post-HO-0009 owner handoffs and E-0012 live-validation routing (researcher-architect)

> Coordination and preflight only. No live E-0012 campaign or training was run by this seat.

## Round / Work Items Touched

- W-0001 — routed the owner-side close-out to systems-researcher after R-0017.
- W-0005 / E-0012 — routed the frozen live known-difference and N4 null-pair execution to systems-researcher.
- HO-0010 and HO-0011 — filed as executable handoffs.
- R-0017, HO-0009, and S-0017 — read as the prerequisite verification evidence.

## What I Did (with evidence)

| # | Action | Evidence (command → exit code → path) | Calibration |
|---|---|---|---|
| 1 | Confirmed the verification-auditor commit is synchronized locally. | `git pull --ff-only` → up to date at `69e874c`; clean before edits. | demonstrated |
| 2 | Ran the E-0012 frozen self-test and retained-data replay. | `python tools/e0012_sprt.py --self-test` → 0; `--replay e0010_k6n_games.jsonl` → 0, `REPLAY_SANITY PASS`; capture `research/context/s18_post_ho0009_routing_preflight.txt`. | demonstrated |
| 3 | Filed the W-0001 owner close-out handoff. | `HO-0010`; requires DONE only after R-0017 VERIFIED and forbids dataset/E-0011/RUN-0001 edits. | demonstrated record state |
| 4 | Filed the E-0012 execution handoff with exact runjob commands and frozen gates. | `HO-0011`; requires RUN-0002/RUN-0003, no silent retries, no training, and independent verification before W-0005 closure. | demonstrated record state |
| 5 | Regenerated projections and closed this session. | `update` → 0, `state --write` → 0, `validate` → 0; advisory/grandfathered warnings only. | demonstrated |

## What I Did NOT Do (and why)

- Did not edit W-0001: its owner is systems-researcher, and the researcher-architect must not mark a work item DONE.
- Did not run either E-0012 live campaign: execution belongs to systems-researcher and the handoff preserves the runjob/RUN-record requirements.
- Did not start Texel/NNUE training, create H-0013, or claim E-0012/harness success.
- Did not self-verify W-0005 or change R-0017, RUN-0001, E-0011, the dataset, source, or tooling.

## Claims I Made That Are NOT Yet Verified

- E-0012's live known-difference and N4 null-pair results remain unknown. They require the systems-researcher execution, raw evidence, and a fresh verification-auditor review.
- W-0001 lifecycle closure is pending the systems-researcher owner action in HO-0010; R-0017 is independently VERIFIED, but that is not the same record transition.
- H-0013 training readiness remains blocked on W-0005/E-0012 and the future pre-registration/critique gates.

## Environment Facts Learned

- The CLI still reported W-0001 as `IN_PROGRESS` after R-0017 because the verifier correctly left owner-controlled lifecycle fields untouched.
- W-0005 is owned by researcher-architect, but its live execution/build is explicitly assigned to systems-researcher in HO-0011.
- The frozen E-0012 tool self-test passes all 239 split points; retained k6 replay reproduces the expected game-179 crossing. These are preflight facts, not live validation.

## State Left On Disk

- `research/handoffs/HO-0010-close-w-0001-after-r-0017-independent-verification.md` — REQUESTED.
- `research/handoffs/HO-0011-execute-e-0012-live-known-difference-and-null-pair-controls.md` — REQUESTED.
- `research/index.md`, `research/state.md`, `research/state.json` — regenerated projections.
- `research/context/s18_post_ho0009_routing_preflight.txt` — local evidence capture.

## Next Action For The Successor

1. Send HO-0010 to a systems-researcher instance to close W-0001 without touching the verified dataset evidence.
2. Send HO-0011 to systems-researcher for the two frozen live E-0012 jobs.
3. After raw results exist, assign a fresh verification-auditor to W-0005/E-0012.
4. Only after W-0005 is independently VERIFIED may the researcher-architect consider the next H-0013 pre-registration.

## Escalations (owner decisions needed)

- None for routing. The next live campaigns remain pre-registered and must report honest PASS/FAIL/INCONCLUSIVE outcomes without changing the contract.

## Validation Status

- Gate 0 → PASS (exit 0, all tests/perft anchors passed).
- E-0012 `--self-test` → PASS (exit 0, 239 split points).
- E-0012 retained replay → PASS (exit 0, game 179, `REPLAY_SANITY PASS`).
- `research.py update` → exit 0.
- `research.py state --write` → exit 0.
- `research.py validate` → exit 0; advisory/grandfathered warnings only.
- No live E-0012 campaign or training was launched.

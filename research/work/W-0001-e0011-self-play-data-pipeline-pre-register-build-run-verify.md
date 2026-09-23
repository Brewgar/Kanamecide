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
- 2026-09-22 — researcher-architect: step 1 (pre-registration) filed —
  `research/experiments/E-0011-*.md` (PENDING). Deliverable contract (≥1,000 legal
  deduplicated provenance-carrying games, JSONL, legal-move-flushed, resume gate),
  DEC-0010 tier mapping (artifact checks here; the downstream "beats hand-tuned" claim
  is Tier R on fresh games under E-0012, NOT this record — no conflation), power/sample
  discussion (1,000 games ≈ 120k positions ≳ the Texel fit's needs; h(1000) = ±23 Elo
  ⇒ no Elo verdict possible, none claimed), run plan (`tools/e0011_generate.py` +
  `tools/e0011_check.py` under `runjob.py`, ≤2 pairs, evidence pinning) written.
  Status stays OPEN; NOTHING ran (F-0002). Handoff HO-0003 requests adversarial-reviewer
  critique BEFORE any RUNNING. Next: implementation-engineer build + systems-researcher
  run, after critique.
- 2026-09-22 — adversarial-reviewer (S-0010, via HO-0003): R-0011 COMPLETED, verdict
  NOT CLEAN — three blocking findings (B1 leakage contract, B2 resume/torn-write, B3
  gate strengthening) + N1–N7 non-blocking; E-0011 stays PENDING. (Recorded here for
  work-log continuity; the review itself is R-0011.)
- 2026-09-23 — researcher-architect: R-0011 addenda filed in E-0011 — "Addendum:
  R-0011 B1 response, 2026-09-23" (dataset_sha256/n_games/path fields; downstream
  leakage contract: distinct-salt rule citing |20260922−20260914|·1000003 = 8,000,024,
  machine gate training_game_overlap = 0, fitted_params_sha256), "Addendum: R-0011 B2
  response, 2026-09-23" (kill window [400,600], presence test, torn-line quarantine
  sidecar, deterministic truncation drill, runjob log-preservation policy + telemetry
  caveat — no research/scripts/ change), "Addendum: R-0011 B3 response, 2026-09-23"
  (gate (d) value-level conjuncts incl. 0-based game_id pin + seed↔opening re-derivation;
  gate (f) routed to reviewer with command evidence; synthetic-20-game aggregator
  negative test adopted as build acceptance), "Addendum: R-0011 N1–N7 + Gate-0 UCI-entry
  note, 2026-09-23". Original pre-registered text untouched (append-only). Gate 0 OPEN
  (attempt #10, exit 0) but session engine-free by design; E-0011 stays PENDING.
  HO-0006 filed for re-critique of the addenda.

- 2026-09-22 — adversarial-reviewer: HO-0003 critique filed as **R-0011** (COMPLETED,
  `kind: critique`, `target: E-0011`). Verdict: **NOT CLEAN — blocking findings B1 (downstream
  leakage contract: pin `dataset_sha256` at campaign close + write the future Tier-R experiment's
  obligations — distinct salt, `training_game_overlap = 0` machine gate against the pinned
  dataset, fitted-parameter hash), B2 (resume/torn-write semantics: kill boundary, presence
  test, torn-line policy, deterministic truncation drill, kill point [400,600], preserve the
  pre-resume log — `runjob.py launch` unlinks it), B3 (gate (d) presence-only → value-level
  conjuncts; gate (f) routed to reviewer); E-0011 stays PENDING** (F-0002 independently blocks
  execution). N1–N7 record-level; two flagged assumptions measured against EV-0001 and
  supported (130.3 plies/game ⇒ ~130k positions/1,000 games; quiet-yield proxy ≈76.9k/1,000;
  White 58.5 %). Next: researcher-architect's addendum → re-critique before `status: RUNNING`.
  E-0011 record not edited by this seat; HO-0003 closed DONE.

## Verification
- verified_by: (a different agent than owner)
- verdict: (VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE)
- evidence: (review record id + command outputs)

> Sequence per AGENT_MEGAPROMPT_ROUND4.md: pre-registration (with power + sample
> validity) must be critiqued by adversarial-reviewer BEFORE `status: RUNNING`. Run under
> `runjob.py` with heartbeat/checkpoint/resume; ≤ 2 engine pairs.
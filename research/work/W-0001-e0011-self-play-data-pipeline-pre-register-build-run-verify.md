---
id: W-0001
type: work
title: "E-0011 self-play data pipeline (pre-register, build, run, verify)"
round: 4
owner: systems-researcher
status: IN_PROGRESS
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
- 2026-09-23 — adversarial-reviewer (S-0012, via HO-0006): R-0014 COMPLETED — B1/B2/N-set
  FULLY DISCHARGED, gate (f) PASS, but B3 PARTIAL with ONE new blocking finding: the
  declared `end` vocabulary is not closed over the harness family's reachable endings
  (stalemate, draw-material) and the `(Ns)` suffix is undeclared. (Continuity entry; the
  review is R-0014.)
- 2026-09-23 — researcher-architect (S-0013): R-0014 B3 fix landed VERBATIM as
  "Addendum: R-0014 B3 response, 2026-09-23" — `end` closed set extended to
  {mate, stalemate, draw-material, rule50, repetition, plycap, crash}; `(Ns)` declared
  as a separate `end_seconds` field (definition: whole elapsed game seconds, one
  definition for every class; normative status: required telemetry, never part of the
  membership test; legacy rows read by suffix-strip rule); Dataset schema line + B3.1
  conjunct amended by the addendum; synthetic-20 test gains a 4th fixture (legacy
  suffixed row must FAIL campaign schema, parse under reader rule). Read-only scan
  pinned (`_s12_endscan_out.txt`: mate 1043, draw-claim 80, plycap 72, draw-material 43,
  stalemate 2); doc nit surfaced (R-0014's 33 = k1–k5 subtotal; all-six = 43; ruling
  unaffected). git diff: +65/−0, pure additions. Work item status left OPEN; HO-0008
  filed for the full-discharge ruling.

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
- 2026-09-23 — adversarial-reviewer: HO-0006 re-critique filed as **R-0014** (COMPLETED,
  `kind: critique`, `target: E-0011`). Verdict: **PARTIAL — B1 and B2 FULLY DISCHARGED**
  (leakage contract is now field-enforced: `dataset_sha256`/`dataset_n_games` as a step-5
  deliverable + `training_game_overlap = 0` machine gate with named normalization
  `tuple(opening)+tuple(san)` + distinct-salt rule + `fitted_params_sha256`; kill window
  [400,600], presence test = parse+schema+dense id, `.torn` quarantine + incident +
  re-emit-under-own-id, deterministic truncation drill as a pre-registered gate-(e)
  acceptance step, log-preservation as evidence-auditable run policy, runjob counts ruled
  telemetry-only). **N1–N7 + Gate-0/UCI note DISCHARGED; gate (f) executed by the reviewer
  route (0 strength-assertion lines in Results/Stat.Analysis/Interpretation/Conclusion).**
  **B3 PARTIAL — ONE new blocking finding** from the HO-0006-ordered spot-check of the ten
  value-level conjuncts against EV-0010's actual JSONL shape: the declared closed `end`
  vocabulary `{mate, rule50, repetition, plycap, crash}` omits `stalemate` (k2n/k5n) and
  `draw-material` (ALL six rungs, 33/1,240 games), and every retained emission carries an
  `(Ns)` seconds suffix with no declared suffix policy — a legal game can have no legal label,
  forcing a gate-(d) false FAIL or a provenance lie at emit time. Missing sentence (fix is one
  line): extend the set to `{mate, stalemate, draw-material, rule50, repetition, plycap, crash}`
  + declare the suffix policy (strip at emission or separate `end_seconds` field), Dataset
  schema line in agreement. **E-0011 stays PENDING on exactly that sentence.** Gate 0 OPEN
  (attempt #11, my own run, exit 0; piped token ran the DEFAULT perft harness — the UCI-entry
  flag is in the record's text and remains a build-session MUST). E-0011 not edited by this
  seat; HO-0006 closed DONE.
- 2026-09-23 — adversarial-reviewer: HO-0008 micro-ruling filed as **R-0016** (COMPLETED,
  `kind: critique`, `target: E-0011`). Verdict: **B3 FIXED / FULLY DISCHARGED — E-0011 is
  CLEARED FOR BUILD+RUN.** All three ordered elements verified: (i) the closed `end` vocabulary
  now matches the EV-0001-family JSONL exactly — scan EXIT 0, normalized all-six totals
  mate 1043 / draw-claim 80 / plycap 72 / draw-material 43 / stalemate 2 = 1,240, every realized
  legacy token explicitly mapped into `{mate, stalemate, draw-material, rule50, repetition,
  plycap, crash}`; (ii) the `(Ns)` policy is declared and schema-consistent — separate
  `end_seconds` field, required telemetry, never in the membership test, suffix-strip reader
  rule keeps retained evidence valid, Dataset + B3.1 conjuncts amended by the addendum
  (append-only) and a 4th synthetic fixture makes the reader rule testable; (iii)
  `git diff --numstat 690e145 5026fb5 -- 'research/experiments/E-0011*'` → `65 0` (0 deletions,
  single trailing hunk — pure additions). Doc-n reconciled: the architect was right that R-0014's
  "33 draw-material games" was the k1–k5 subtotal — the correct all-six figure is 43/1,240 (k6
  contributes 10); corrected in R-0016 (the finding itself was unaffected). One non-blocking
  build note: pin the rule50-vs-repetition precedence in the rare both-predicates case.
  E-0011 may now leave PENDING (reviewer/owner flips the status); the build session's own
  pre-registered acceptance steps (synthetic-20 FAIL demo incl. 4th fixture, deterministic
  truncation drill, UCI entry path FIRST) remain the gates on the live campaign. E-0011 not
  edited by this seat; HO-0008 closed DONE.
- 2026-09-24 — S-0015 bundled implementation-engineer + systems-researcher for W-0001 step 2 and W-0005 step 2. Gate 0 attempt #13 exited 0 with 10/10 perft PASS; explicit UCI path proved as `Popen([kana.exe, "uci"])` + stdin `uci` (transcript/hash in RUN-0001). `tools/e0011_generate.py`, `tools/e0011_check.py`, `tools/e0012_sprt.py`, and `tools/uci_probe.py` built at code commit `752216c`. Acceptance: synthetic-20 checker exit 1 named torn-line/wrong-hash/duplicate-ID/legacy-suffix defects; deterministic 1,000-game truncation drill PASS at kill game 500, 500 re-emissions, final dense 1,000, duplicate-move-lists=0; 6/6 live smoke legal. E-0012 retained k6 Tier-S replay PASS: H1 game 179, LLR +2.9847724801; every-k split test PASS at 239/239 points. E-0011 flipped PENDING→RUNNING, owner systems-researcher, immediately before RUN-0001 launch; W-0001 OPEN→IN_PROGRESS. No pre-registered text/threshold/N/cap changed.
- 2026-09-24 — S-0015 live contradiction/failure recorded: RUN-0001 attempt 1 stopped at 202 complete games after two crash losses because the next readiness failure aborted instead of becoming another crash record. Failed artifacts are preserved under `m0_audit/e0011_failed_attempt1/` (JSONL SHA-256 `1a95e8dd…e76bfa`; zero duplicate move-lists). Code fixed in `7b1dda15f675b884a8bf971eec4b53a0fdf2049f`: readiness/construction failures now score crash=loss, engine pairs are explicitly recreated after crashes, and reader shutdown is deterministic. Crash unit PASS; repaired 1,000-game drill PASS at 500 with zero duplicates. Attempt 1 is excluded; replacement dataset will be wholly pinned to `7b1dda1`. No gate, N, cap, or threshold changed.


## Verification
- verified_by: (a different agent than owner)
- verdict: (VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE)
- evidence: (review record id + command outputs)

> Sequence per AGENT_MEGAPROMPT_ROUND4.md: pre-registration (with power + sample
> validity) must be critiqued by adversarial-reviewer BEFORE `status: RUNNING`. Run under
> `runjob.py` with heartbeat/checkpoint/resume; ≤ 2 engine pairs.
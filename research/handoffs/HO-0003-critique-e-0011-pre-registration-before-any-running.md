---
id: HO-0003
type: handoff
from: researcher-architect
to: adversarial-reviewer
work_item: W-0001
status: DONE
title: Critique the E-0011 pre-registration (W-0001 step 1) BEFORE any RUNNING
artifacts: ["research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md", "research/work/W-0001-e0011-self-play-data-pipeline-pre-register-build-run-verify.md", "research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md", "research/debates/D-0007-e0010-effect-size-decision-rule-what-is-decidable-at-achievable-n.md"]
commands: ["python research/scripts/research.py validate"]
acceptance: "a kind:critique review COMPLETED, linked to E-0011 and W-0001; E-0011 stays PENDING unless the review raises no blocking finding"
example: false
created: 2026-09-22
closed: 2026-09-22
---

# HO-0003 — Critique the E-0011 pre-registration before any RUNNING

## Request
Per the Round-4 sequencing rule (AGENT_MEGAPROMPT_ROUND4 / W-0001 note), the E-0011
pre-registration must be critiqued by you before anyone sets `status: RUNNING`. Attack,
specifically: (1) gate completeness — can any gate (a)–(f) pass while the dataset is in
fact useless (e.g. degenerate openings passing dedup, provenance fields present but
false, resume re-emitting games in a way the audit misses)? (2) the claim that E-0011
needs no DEC-0010 tier — is mapping the downstream "beats hand-tuned" claim to Tier R
(on fresh games) correct, or does Q-0006 demand something else? (3) the Texel
sample-size reasoning (≈120k positions ⇒ ≥500 positions/parameter; sampling noise not
the binding constraint — label/self-play bias is). (4) the 2,000-game campaign cap and
the ±23 Elo h(1000) arithmetic. (5) Run plan § runjob.py usage. Findings that would
change the rule must be named BEFORE it runs; cosmetic findings route to the record.

## Artifacts To Read (paths)
- `research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md`
- `research/work/W-0001-e0011-self-play-data-pipeline-pre-register-build-run-verify.md`
- `research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md` (protocol it cites)
- `research/debates/D-0007-e0010-effect-size-decision-rule-what-is-decidable-at-achievable-n.md`
- `research/evidence/EV-0002-e0010-reproduction-harness.md` (the harness E-0011 forks)

## Commands To Run
```powershell
python research/scripts/research.py validate    # expect: OK, 0 problems
```

## Acceptance Criteria (what makes this DONE)
- A `kind: critique` review (R-####) exists with status COMPLETED, `target: E-0011`,
  linked to W-0001; it names either "no blocking findings" or a numbered blocking list.
- E-0011's `status` stays PENDING unless that review raises no blocking finding AND the
  gate-0 block (F-0002) is lifted by the owner.

## Response (receiver, append-only)
- 2026-09-22 — adversarial-reviewer (S-0010) — **DONE. Verdict: NOT CLEAN — three blocking
  findings; E-0011 stays PENDING** (and would stay PENDING under F-0002 regardless).
  Review: **R-0011** (`kind: critique`, `target: E-0011`, linked to W-0001, COMPLETED).
  Blocking for `status: RUNNING`:
  1. **B1 — leakage contract missing:** "fresh games" for the downstream Tier-R claim is an
     adjective, not a field. Missing: (i) `dataset_sha256`/`n_games` pinned at campaign close as
     a *deliverable*; (ii) a written "downstream leakage contract" (distinct salt + machine
     `training_game_overlap = 0` gate against the pinned dataset + hash of the fitted-parameter
     artifact).
  2. **B2 — resume/torn-write semantics undefined:** the kill boundary is unspecified, the
     presence test on resume is unspecified, the torn-trailing-line policy is absent, and the
     drill is not deterministic (add a synthetic-truncation resume drill + a pre-registered kill
     point in [400,600]; also: `runjob.py launch` deletes the previous log — preserve it).
  3. **B3 — gate (d) is presence-only (wrong-value fields pass it) and gate (f) is not
     machine-checkable as listed:** add value-level conjuncts (hash/salt/stage/res/end/plies/
     times/a_white, id uniqueness + density + base) and route (f) to reviewer/verifier.
  Non-blocking N1–N7 include two *measurements* that upgrade the ARMED assumptions:
  130.3 plies/game ⇒ ≈130k engine-move positions per 1,000 games and a quiet-position proxy
  ≈76,887/1,000 (vs the flagged "≈120k" and "≥50k" — both supported); White scores 58.5 % in
  the retained 1,240 games (k6: 0.783 vs 0.542 by color cell) — the Elo-canary steelman is
  answered: **no Elo gate belongs in E-0011**, and a "50 %" color gate would be an F6-class
  defect in reverse (measured prior ≈ +60..+90 Elo for White). All fixes are text-level for the
  researcher-architect; none changes a tier, a threshold, or an N. Re-critique follows the
  addendum.

## Verification (receiver, append-only)
- raw output / exit codes / hashes: `python research/scripts/research.py validate` → exit 0
  ("Validation OK — statuses are in-vocabulary; … 0 problems", warnings only). Gate 0: one
  attempt of `build\Release\kana.exe` → Device Guard block, no process (attempt #7;
  `research/context/bootstrap/gate0.txt`). Ply/yield/colour measurements from the
  `e0010_k{1..6}n_games.jsonl` evidence (k6n SHA-256
  `9da1cfa0cb24ed94cf4a64ad47c0fed9387b5a3163b590153677e61c1fd0d227`, matching E-0012's pin):
  mean 130.3 plies/game, N=1240, total 161,615 engine-move positions, 72 plycap games, dup
  move-lists = 0, `a_white` 100/200 (120/240 k6), White 725.5/1240 = 58.51 %. Arithmetic:
  `1.96*371/sqrt(1000) = 22.99` (= ±23.0); salt separation |20260922−20260914|·1000003 =
  8,000,024 ≫ max index. Full line-quoted output in R-0011's Evidence appendix.
- verdict: critiques upheld as stated; E-0011 stays PENDING pending an addendum (B1–B3) — and
  independently pending F-0002 (Gate 0 still blocked).

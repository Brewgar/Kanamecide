---
id: S-0009
type: session
agent: researcher-architect
round: 4
title: "W-0001/W-0005 step 1: E-0011 + E-0012 pre-registrations filed; offline SPRT replay PASS; HO-0003/HO-0004; Gate-0 re-block"
status: CLOSED
context_budget: "bootstrap re-read (~12k tok): README, MEGAPROMPT_ROUND4, SYSTEM, role files, W-0001/W-0005, E-0010, DEC-0010, D-0007, R-0009, EV-0001/2/10, w0002_power.py"
example: false
created: 2026-09-22
closed: 2026-09-22
---

# S-0009 — Session (researcher-architect)

## Round / Work Items Touched
- W-0001 (OPEN) — step 1 (pre-registration) filed; handoff HO-0003 out.
- W-0005 (OPEN) — step 1 (pre-registration) filed + offline ASN-model validation; HO-0004 out.

## What I Did (with evidence)
| # | Action | Evidence (command → exit code → path) |
|---|---|---|
| 1 | Gate 0 attempted exactly once | `build\Release\kana.exe` → Device Guard/App Control block text, no process started (F-0002, 6th observation) → `research/context/bootstrap/gate0.txt` (appended) + `gate0_s9_attempt.txt` (sha 49d51319…0a3f31) |
| 2 | E-0011 pre-registration filed (PENDING) | `research/experiments/E-0011-self-play-data-pipeline-provenance-carrying-resumable-deduplicated-game-dataset.md` — gates (a)–(f), DEC-0010 tier mapping (no tier on the dataset; downstream claim = Tier R on fresh games), power (1,000 g ≈ 120k pos; h(1000)=±23 Elo ⇒ no Elo gate), run plan (`tools/e0011_generate.py` + `tools/e0011_check.py` under `runjob.py`, ≤2 pairs, salt 20260922) |
| 3 | W-0001 work log appended; status left OPEN | same file, work-log entry 2026-09-22 |
| 4 | HO-0003 filed to adversarial-reviewer | `research/handoffs/HO-0003-*.md` (REQUESTED) |
| 5 | Wrote + ran the offline SPRT replay | `python research\context\w0005_sprt_replay.py` → EXIT:0 → `research/context/w0005_sprt_replay_output.txt`; no engine; input JSONL untouched (read-only) |
| 6 | E-0012 pre-registration filed (PENDING) with the offline report | `research/experiments/E-0012-e-sprt-lite-comparison-harness-pre-registered-dec-0010-tiers.md` — contract (lite LLR ±2.9444, caps 8k/30k/8k, post-cap INCONCLUSIVE, crash=loss, runjob-resumable), live-validation bands (v1)–(v4), offline results pinned with SHA-256s |
| 7 | W-0005 work log appended; status left OPEN | same file, work-log entry 2026-09-22 |
| 8 | HO-0004 filed to adversarial-reviewer | `research/handoffs/HO-0004-*.md` (REQUESTED) |
| 9 | Seat memory + assignments updated | `agents/researcher-architect/{beliefs,current_position}.md` (dated appends), `agents/ASSIGNMENTS.md` notes |
| 10 | Session close | `update` / `state --write` / `validate` / `round --round 4` outputs in `research/context/_s9_close.txt` |

## Offline replay numbers (the reproducibility story)
- Inputs: EV-0001 rung files, hash-pinned inside E-0012 (k6n = `9da1cfa0…fd0d227`);
  totals re-derived match E-0010 exactly on all six rungs; duplicate-move-lists=0.
- k6 Tier S [0,+20]: H1 accepted at game **179** (final +2.985) vs predictions 191
  (Wald-Elo) / 173 (exact-lite) / ~133 (score-space) — within pre-committed [100,260].
- k6 Tier R [0,+5]: undecided at 240 (final +1.098; predictions 494/713) — as predicted.
- k6 Tier M [100,150]: undecided at 240, final −0.673 (drift toward H0; ~910 predicted).
- ASN(H1)/ASN(H0) re-derived with σ=371.0: 1823.7/2026.4 (S), 29179.8/32422.0 (R),
  291.8/324.2 (M) — ≤0.1% off R-0010's values, attributable entirely to σ rounding.
- Script sha `94631d6b…33c`, output sha `9cd40402…35ad`; reproduce with the command in
  row 5; bands were committed in the script docstring before the first execution.

## What I Did NOT Do (and why)
- Did NOT run any engine, match, or generation (Gate 0 hard-block, F-0002; my assignment
  also forbade it). No engine numbers claimed except quoted E-0010 record values.
- Did NOT set E-0011/E-0012 to RUNNING, nor touch W-0001/W-0005 status (critique gate).
- Did NOT edit D-0007, DEC-0010, R-0009/R-0010, E-0010, W-0002, W-0004 (append-only rule).
- Did NOT attempt W-0003/W-0006 remainder (out of this session's scope).

## Claims I Made That Are NOT Yet Verified
- E-0011's pre-registration correctness/completeness (routed: HO-0003).
- E-0012's contract, bands, and the claim that the offline replay discharges D-0007's
  residual (routed: HO-0004).
- Both are my own claims about my own records — they require the adversarial-reviewer.

## Environment Facts Learned
- Gate 0 remains a hard block (6th observation, 2026-09-22); `runjob.py` launch would
  equally fail — every engine execution this round is contingent on the owner's policy fix.
- `research.py new-handoff` with a single-quoted title containing parentheses failed
  under this shell (no record created; HO-0003/HO-0004 were written manually instead).
- Terminal capture in this IDE is unreliable for combined commands; single-purpose
  `cmd /c "... > file & type file"` works.

## State Left On Disk
- New: experiments/E-0011*, experiments/E-0012*, handoffs/HO-0003*, handoffs/HO-0004*,
  context/w0005_sprt_replay.py + _output.txt, sessions/S-0009*, bootstrap/gate0 appends.
- Appended: W-0001/W-0005 work logs, researcher-architect seat memory, ASSIGNMENTS.md.
- Untouched (verified): all closed records and the EV-0001 JSONL set.

## Next Action For The Successor
1. adversarial-reviewer: HO-0003 and HO-0004 critiques; both must be non-blocking
   before systems-researcher builds `tools/e0012_sprt.py` / `tools/e0011_generate.py`.
2. Everything executable waits on F-0002 (owner policy action — escalation).
3. W-0003 and W-0006 remainder remain open for their owners.

## Escalations (owner decisions needed)
- F-0002: Device Guard/App Control policy still blocks every engine run. Rounds cannot
  complete their engine-bearing exit checks until the owner allow-lists or rebuilds
  under a permitted policy.

## Validation Status
- `python research/scripts/research.py update` / `state --write` / `validate` /
  `round --round 4` — outputs in `research/context/_s9_close.txt` (validate must be OK,
  0 problems; round expected non-zero: W-0001/W-0003/W-0005/W-0006 not DONE+VERIFIED).

  (Wald-Elo) / 173 (exact-lite) / ~133 (score-space) — within pre-committed [100,260].
- k6 Tier R [0,+5]: undecided at 240 (final +1.098; predictions 494/713) — as predicted.
- k6 Tier M [100,150]: undecided at 240, final −0.673 (drift toward H0; ~910 predicted).
- ASN(H1)/ASN(H0) re-derived with σ=371.0: 1823.7/2026.4 (S), 29179.8/32422.0 (R),
  291.8/324.2 (M) — ≤0.1% off R-0010's values, attributable entirely to σ rounding.
- Script sha `94631d6b…33c`, output sha `9cd40402…35ad`; reproduce with the command in
  row 5; bands were committed in the script docstring before the first execution.

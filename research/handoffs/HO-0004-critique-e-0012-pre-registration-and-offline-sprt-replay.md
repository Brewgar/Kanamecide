---
id: HO-0004
type: handoff
from: researcher-architect
to: adversarial-reviewer
work_item: W-0005
status: DONE
title: Critique the E-0012 pre-registration and its offline SPRT replay validation BEFORE any RUNNING
artifacts: ["research/experiments/E-0012-e-sprt-lite-comparison-harness-pre-registered-dec-0010-tiers.md", "research/work/W-0005-e-sprt-lite-comparison-harness-pre-register-build-validate.md", "research/context/w0005_sprt_replay.py", "research/context/w0005_sprt_replay_output.txt", "research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md"]
commands: ["python research/context/w0005_sprt_replay.py", "python research/context/w0002_power.py", "python research/scripts/research.py validate"]
acceptance: "a kind:critique review COMPLETED, linked to E-0012 and W-0005; replay reproduces (crossing=179 / finals +2.985, +1.098, -0.673 on k6) or differences itemized; E-0012 stays PENDING unless no blocking finding"
example: false
created: 2026-09-22
closed: 2026-09-22
---

# HO-0004 — Critique E-0012 (E-SPRT-lite contract + offline replay) before any RUNNING

## Request
Critique, per the W-0005 sequencing rule, before any `status: RUNNING`. Target classes:
(1) the LLR formula choice (draws-as-halves binomial vs exact trinomial — DEC-0010 keeps
the exact form an "allowed refinement if validated"; is lite-first defensible?);
(2) the pre-committed acceptance bands (Tier S crossing ∈ [100,260]; Tier R/M
undecided-at-240) — too wide? too narrow? peeking?; (3) the live-validation bands
(v1)–(v4), especially n_stop ∈ [80,800]; (4) any way the offline replay could pass
while the live harness is broken (classes the replay cannot see); (5) arithmetic:
re-run the replay; independently re-check the ASN re-derivation and the
191/173/133 predictions against DEC-0010 and w0002_power.py. Also rule whether the
offline report in fact discharges D-0007's routed "W-0005 model validation" residual,
or only part of it.

## Artifacts To Read (paths)
- `research/experiments/E-0012-e-sprt-lite-comparison-harness-pre-registered-dec-0010-tiers.md`
- `research/work/W-0005-e-sprt-lite-comparison-harness-pre-register-build-validate.md`
- `research/context/w0005_sprt_replay.py` + `research/context/w0005_sprt_replay_output.txt`
  (SHA-256 pinned inside E-0012's Provenance section)
- `research/decisions/DEC-0010-two-tier-sprt-effect-size-decision-rule.md`
- `research/debates/D-0007-*.md` (the residual this claims to discharge)
- EV-0001 rung files `e0010_k{1..6}n_games.jsonl` (root, gitignored, READ-ONLY)

## Commands To Run
```powershell
python research\context\w0005_sprt_replay.py   # expect exit 0; k6 S: H1 @179; R/M undecided
python research\context\w0002_power.py         # the calibration the replay checks against
python research\scripts\research.py validate   # expect: OK, 0 problems
```

## Acceptance Criteria (what makes this DONE)
- A `kind: critique` review (R-####), COMPLETED, `target: E-0012`, linked to W-0005,
  with a blocking/no-blocking verdict on each of the five target classes above.
- The reviewer re-ran the replay and either reproduces k6 crossing=179 with finals
  +2.985 / +1.098 / −0.673 or items the difference precisely.
- E-0012 `status` stays PENDING unless the review is non-blocking AND F-0002 is lifted.

## Response (receiver, append-only)
- 2026-09-22 — adversarial-reviewer (S-0010) — **DONE. Verdict: NOT CLEAN — two blocking
  findings; E-0012 stays PENDING** (and independently stays blocked by F-0002; no rule text,
  tier, bound, cap or band changes).
  Review: **R-0012** (`kind: critique`, `target: E-0012`, linked to W-0005, COMPLETED), with my
  own-code re-derivation of the k6 finals (never the author's script):
  S [=179, +2.985] R [undecided, +1.098] M [undecided, −0.673] — all reproduce exactly, and my
  fresh run of `w0005_sprt_replay.py` is line-for-line identical to the pinned output file
  (44/44 non-blank lines, ASCII-normalised).
  Blocking for `status: RUNNING`:
  1. **B1 — the bands' pre-run commitment is asserted, not git-verifiable:**
     `research/context/w0005_sprt_replay.py` is gitignored (`.gitignore:118`) and has no history;
     current artifact hashes DO match E-0012's pins (no post-commit edit), but the claim is only
     mtime-consistent, not provable. Fix: track the script + output (or a `.gitignore` exception).
  2. **B2 — resume/durability policy missing:** write order/durability order of the JSONL vs the
     checkpoint, authoritative artifact and failure path (abort on mismatch), the 1e-9 assertion
     is self-consistency only, and "identical decision when resumed" needs an FP/order
     qualification + a split-at-every-k unit test.
  Non-blocking N1–N5 (quantified): the [100,260] band is ≈±1.9σ around the k6 crossing time
  (sd ≈ 42; ~5.4 % false-FAIL rate; detects a ≥1.79×/≤0.69× scale error), Tier R/M "no decision
  in 240" bands are consistency-tautologies (≈4.6σ / ≈1.7σ), lite-first is defensible because the
  exact trinomial needs a *pre-registered draw model*, the live-only failure classes are
  enumerated, and a live null-pair (stage-6 vs stage-6) control is recommended against per-arm
  bias (colour-corrected: White prior 58.5 %, not 50 %). The inspector's anomaly is **ruled the
  rule working as designed**: DEC-0010 says "H0 … delta <= M − 50; H1 … delta >= M … the test
  guarantees error control only AT the zone edges", and k1/k2's true effects (36.3/82.3) sit
  below M−50 — the early H0 decisions at games 79/192 are correct "not ≥150" verdicts.
  D-0007's routed residual is **partially** discharged: the screen half is reproducible (179 vs
  191/173), the regress half (~713) has no realized counterpart and is a near-certain
  consistency check only; W-0005 correctly stays OPEN.

## Verification (receiver, append-only)
- raw output / exit codes / hashes: `python research/context/w0005_sprt_replay.py` → **exit 0**
  (k6: S H1 @179 +2.985; R none +1.098; M none −0.673; all-rung totals match E-0010;
  dup=0; EXIT:0). `python research/context/w0002_power.py` → **exit 0** (σ=371; ASN
  S 1822/2025, R 29,159/32,399, M 292/324; score-space crossings 133/495/970).
  `python research/scripts/research.py validate` → **exit 0**, 0 problems. Independent
  derivation output (my script, `%TEMP%\krev10\independent_llr.py`): full lines quoted in
  R-0012's Evidence appendix, incl. closed-form totals +4.093/+1.098/−0.673 and drift/sd
  0.01705/0.05444. Pinned hashes verified current: script `94631d6b…d1233c`, output
  `9cd40402…ea35ad`, k6n input `9da1cfa0…fd0d227` (all equal E-0012 §Provenance); E-0012 has
  exactly one commit (`2a9d997`); `git log` on the replay script is empty. Gate 0: one attempt,
  Device Guard block, no process (`gate0.txt` attempt #7).
- verdict: replay reproduces (crossing=179; finals +2.985/+1.098/−0.673) from my own code; the
  two blocking items are execution/provenance preconditions to land before RUNNING; the
  pre-registered rule is unchanged.

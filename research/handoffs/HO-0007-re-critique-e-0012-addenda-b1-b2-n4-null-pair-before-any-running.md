---
id: HO-0007
type: handoff
from: researcher-architect
to: adversarial-reviewer
work_item: W-0005
status: DONE
title: Re-critique E-0012's R-0012 addenda (B1/B2 responses + adopted null-pair control) before any RUNNING
artifacts: ["research/experiments/E-0012-e-sprt-lite-comparison-harness-pre-registered-dec-0010-tiers.md", "research/reviews/R-0012-critique-e-0012-pre-registration-and-offline-sprt-replay.md", "research/work/W-0005-e-sprt-lite-comparison-harness-pre-register-build-validate.md", "research/context/w0005_sprt_replay.py", "research/context/w0005_sprt_replay_output.txt", ".gitignore"]
commands: ["git log --oneline -- research/context/w0005_sprt_replay.py research/context/w0005_sprt_replay_output.txt", "python research/context/w0005_sprt_replay.py", "python research/scripts/research.py validate"]
acceptance: "a NEW critique review (R-####) targeting E-0012's addenda, status COMPLETED, ruling B1 and B2 discharged or still-blocking and accepting-or-attacking the adopted N4 null-pair control; E-0012 stays PENDING unless the ruling is clean"
example: false
created: 2026-09-23
closed: 2026-09-23
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
- 2026-09-23 — adversarial-reviewer (S-0012) — **DONE. Verdict: CLEAN.** Review:
  **R-0015** (`kind: critique`, `target: E-0012`, linked W-0005 + HO-0007, COMPLETED), every
  clause quoted next to its verdict.
  - **B1 discharged**: I re-ran the whole chain myself — `git ls-files …w0005` (both tracked),
    `certutil -hashfile` for both (`94631d6b…d1233c` and `9cd40402…ea35ad`, both equal the
    pins), `git show 16ac1ff --stat` (.gitignore +4 and the two artifacts added), `.gitignore`
    lines 118→123 contain the negations, `git show 2a9d997:…E-0012…` already contains those
    same two hashes, `git log` on either artifact = `16ac1ff` only. The audit chain (pin at
    2a9d997 → files tracked at 16ac1ff → any later edit breaks it) is real now. `validate` exit
    0, replay re-run exit 0 (same numbers, dup=0, all totals match).
  - **B2 discharged**: write order pinned (JSONL append → fsync → checkpoint → fsync; reverse
    prohibited; JSONL-ahead is the safe crash direction); JSONL authoritative on resume with
    recompute-by-replay and `resume_mismatch` incident; continue-only-at-1e-9 else ABORT+FAILED
    (no silent repair, no silent preference for the checkpoint); self-consistency limitation
    named with the scale/sign detectors split out (offline exact-value + unit tests); the
    FP-ordering qualification on "identical decision" is honest — the absolute form is retired
    and the only remaining occurrences of "identical" are the code-path sentence (--replay/live
    share LLR code) and B2.v's test assertion, and B2.iv declares the 1e-9 boundary incident
    explicitly; split-at-every-k pre-registered as a harness acceptance step (every k, identical
    verdict AND crossing index OR both-none, mismatch-free log, MUST pass before live).
  - **N4 adopted** with cap 240, the Tier-S lite-LLR statistic I named, the colour-corrected
    null at the measured White 58.5% prior, and an explicit prohibition on 50%-centred bands
    (the trap I warned about). My own arithmetic is cited as ground (≈0.0123 LLR bias for an
    H1-cross; sd ≈ 0.058/game from the drift model). My *PASS* form is the well-formed "no H1
    acceptance within cap + null-consistent final LLR" — and the covered "INCONCLUSIVE-path" gap
    from R-0012's Missing Arguments. I have nothing else to add; the trap arrived intact.
  - **N1/N2/N3/N5 text** all landed verbatim and the D-0007 residual wording accepts my partial
    discharge.
  One forward note (not blocking): the `end`-vocabulary under-closure (E-0011's B3-new in
  R-0014) is shareable with the harness's own records; keep the same discipline there.
  E-0012 is **CLEAN** — cleared for the build session (B2.v split-at-every-k + UCI-entry
  probe + (v1)–(v4) + N4 in one sitting).

## Verification (receiver, append-only)
- raw output / exit codes / hashes: `git ls-files research/context | Select-String w0005` →
  both artifacts tracked. `certutil -hashfile research\context\w0005_sprt_replay.py SHA256` →
  `94631d6b1105795f83f662a35df1db260ce9db8df286c1f0fdd5fb3f39d1233c` (== pin).
  `certutil -hashfile research\context\w0005_sprt_replay_output.txt SHA256` →
  `9cd40402e5426a09367c1a9c370aa9fa89ff8c2aab8f4e03d4983e8d68ea35ad` (== pin).
  `git show 16ac1ff --stat` → `.gitignore | 4 +`, both artifacts added, `3 files changed,
  214 insertions(+)`. `git show 2a9d997:…E-0012… | Select-String 94631d6b|9cd40402` → both pins
  already published there. `git log --oneline -- …w0005…` → `16ac1ff` only.
  `python research/context/w0005_sprt_replay.py` → exit 0: k6 S H1@179 final +2.985; R none
  +1.098; M none −0.673; all six rung totals match E-0010; dup=0 per rung;
  ASN(H1) 1823.7/29179.8/291.8 re-derived.
  `python research/scripts/research.py validate` → exit 0, 0 problems.
- verdict: CLEAN. E-0012 stays PENDING on nothing (only the B2.v build-acceptance test + the
  E-0011 end-vocabulary fix from R-0014 gate the live run, neither negotiable).

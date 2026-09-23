---
id: R-0015
type: review
reviewer: adversarial-reviewer
target: E-0012
kind: critique
status: COMPLETED
work_item: W-0005
related: [E-0012, R-0012, HO-0007, W-0005, DEC-0010, D-0007, EV-0001]
example: false
created: 2026-09-23
---

# R-0015 — Re-critique of E-0012's R-0012 addenda (HO-0007)

## Scope

HO-0007, adversarial-reviewer seat, S-0012. Ruling only the dated 2026-09-23 addenda
(original text untouched — `git diff 2a9d997 690e145` shows a single append hunk
`@@ -213,3 +213,141 @@`, pure additions). I re-ran the whole B1 provenance chain myself (the
commands below), re-ran the replay, and re-checked the "identical decision" qualifier for
absolutes. Gate 0 is OPEN (attempt #11, my own run — see R-0014's bootstrapping).

## Rulings per finding

### B1 — **FULLY DISCHARGED** (the whole audit chain is git-based now)

I re-ran every step with my own hands; the chain is closed:

```
git ls-files research/context | Select-String w0005
  → research/context/w0005_sprt_replay.py
    research/context/w0005_sprt_replay_output.txt                     (both tracked)

certutil -hashfile research\context\w0005_sprt_replay.py SHA-256
  → 94631d6b1105795f83f662a35df1db260ce9db8df286c1f0fdd5fb3f39d1233c   (== pin)
certutil -hashfile research\context\w0005_sprt_replay_output.txt SHA-256
  → 9cd40402e5426a09367c1a9c370aa9fa89ff8c2aab8f4e03d4983e8d68ea35ad   (== pin)

git show 16ac1ff --stat
  → .gitignore                                    |   4 +
    research/context/w0005_sprt_replay.py         | 160 +…
    research/context/w0005_sprt_replay_output.txt |  50 +…
    3 files changed, 214 insertions(+)                            (the fix commit)

.gitignore (HEAD)                → L122 / L123 hold the two `!` negations right after
                                   L118's `research/context/*`

git show 2a9d997:E-0012          → the two SHA-256 lines are already published there
git log -- …w0005_sprt_replay*.p* → 16ac1ff (the only commit touching the two files)

python research\scripts\research.py validate      → exit 0, "Validation OK … 0 problems"
python research\context\w0005_sprt_replay.py      → exit 0, same numbers (k6 H1@179,
                                                     +2.985/+1.098/−0.673, dup=0, all match)
```

So the audit chain is now (i) `2a9d997` publishes the pins AND the band text, (ii) `16ac1ff`
adds the files whose bytes match those pins, (iii) any future edit of either file fails
`validate *and* shows up as a diff. This is exactly the "git-auditable" outcome my R-0012 B1
asked for.

### B2 — **FULLY DISCHARGED** (all five items pinned)

> **(B2.i) Write/durability order:** — (1) append the game's JSONL line; (2) `fsync` the JSONL;
> (3) write the checkpoint (W/D/L, cumulative LLR, next_game_index, tier, salt); (4) `fsync`
> the checkpoint. A crash between (2) and (4) leaves the JSONL AHEAD of the checkpoint — the
> designed, safe direction (see ii). The reverse order is prohibited.

> **(B2.ii) Authoritative artifact + failure path:** the **JSONL is authoritative**. On resume:
> recompute W/D/L and the cumulative LLR by replaying the JSONL through the same LLR code;
> record a `resume_mismatch` incident if the recomputed state differs from the checkpoint at
> all; **continue only if recomputed == checkpoint to 1e-9; otherwise ABORT the run and file it
> FAILED** (never "repair", never silently prefer the checkpoint).

> **(B2.iii) The assertion is a self-consistency check only.** … The scale/sign detectors are
> named and separate: the offline exact-value reproduction (crossing 179, finals +2.985 /
> +1.098 / −0.673 — committed artifacts above) plus the unit tests (i)–(iii) already in Test
> Method.

> **(B2.iv) FP-ordering qualification — "identical decision when run in one process or resumed"
> is qualified, not absolute.** It holds **up to floating-point summation order** … and only if
> no cumulative LLR lands within 1e-9 of a bound — a sample that touches a bound within 1e-9 is
> treated as a boundary touch and decides … recorded as a `bound_within_epsilon` incident for
> audit. The absolute form is retired …

> **(B2.v) Split-at-every-k unit test — pre-registered harness acceptance step.** For a canned
> W/D/L sequence … for **every** split point k ∈ [1, N−1], run (a) in one process and (b) as
> run→kill at k→resume; assert identical verdict AND identical crossing index (or both none),
> and a `resume_mismatch`-free log. `tools/e0012_sprt.py` MUST pass this before any live run.

**FP-qualification honesty check** (the task's own trap): I searched the whole record for
remaining absolute claims. The only other occurrences of "identical" in E-0012 are
"identical LLR code path" (a statement that the offline `--replay` mode and the live mode share
the implementation — a sound fact, not the qualified run-vs-resume claim) and B2.v's test
assertion ("identical verdict AND identical crossing index"). **No absolute claim remains.** The
absolute form is honestly retired: the rule says what "identical" means, what test proves the
weaker claim, and what counts as a boundary incident. (That is the right migration — the disk
semantics stayed put; the *claim* became honest.)

### N4 (my recommendation, adopted) — **DISCHARGED** (cleanest possible answer to my own warning)

> **stage-6 vs stage-6** … **cap 240 games** (~0.3 h at the measured 769 games/h), decision
> statistic = the cumulative Tier-S lite LLR.

> - the run must **complete under the cap without adopting a biased verdict**: … a +2.944
>   acceptance within 240 games would require a constant per-game bias of ≈ 0.0123 LLR — the
>   reviewer's arithmetic, ≈ 0.24 σ/game from their delta-method drift ≈ −0.0015/game and sd ≈
>   0.058/game. **Control PASS = no H1 acceptance within the cap and the final cumulative LLR's
>   sign/magnitude consistent with the colour-corrected null** …
> - **the null is colour-corrected, not 50%:** White scores **58.5%** in the retained E-0010
>   data (R-0011's measurement …), so any expected-score term in the control uses that measured
>   prior — a naive 50%-centred band is explicitly prohibited (F6 in reverse);
> - a Control FAIL (H1 acceptance on a null pair) = **harness bias alarm**, treated as a
>   (v1)–(v4)-class harness FAIL: audit first (arms, colour bookkeeping, seeding), never "the
>   engines differ";
> - side benefit, stated: this control is also the live test of the honest-INCONCLUSIVE / cap
>   path that the offline replay can never reach.

All four of my N4 axes answered with text: the cap is real (240), the statistic is the Tier-S
lite LLR I named, the null is colour-corrected (the 58.5% prior, with a 50%-centred band
*explicitly prohibited*), and a FAIL routes to the harness-audit-first action. My own
prediction (≈ +0.0123 LLR bias for a crossing) is quoted as cited ground for the alarm's
meaningfulness. No trap arrived, and the "the offline replay cannot see INCONCLUSIVE" gap is
now covered by a live companion gate that runs the cap. I have nothing to add.

### N1/N2/N3/N5 text — **DISCHARGED**

All landed: band information content (sd ≈ 42, ±1.9σ, ~5.4% false-FAIL, detection floor
1.79×/0.69×, (v2)-FAIL → harness-audit-first before any model verdict), the tightened
refinement clause ("pre-registered draw model … otherwise the refinement is a degrees-of-
freedom generator. Lite stays the shipping form."), the blind-classes list appended to
Interpretation, and the σ "reproduces-the-k6-half-width-is-a-consistency-check" sentence.
The D-0007 residual wording accepts my partial discharge.

## Disagreements

None.

## Missing Arguments

None.

## Factual Errors

None in the new text. One observation-only note: the replay output file's em-dash byte is a
Windows-1252 console capture artifact (in `%TEMP%\krev10` of S-0010 I had verified 44/44
text-identical lines); today the file is now unchanged and hash-matched, so the byte quirk is
history, not a live issue.

## Assumptions

None new.

## Proposed Experiments

1. The build session now runs `tools/e0012_sprt.py` (with the B2.v split-at-every-k acceptance
   test), then the (v1)–(v4) live validation at stage-6 vs stage-0 *(the 240-game handoff
   known-difference run)*, and then the adopted N4 null-pair control (stage-6 vs stage-6,
   cap 240), same `runjob.py` discipline, log-preservation rule as E-0011's B2.5.
2. The `(Ns)` suffix question in R-0014 (E-0011's B3-new) is *also* relevant for E-0012's own
   checkpoint records — the same naming discipline applies when the harness logs its own
   JSONL lines (`crash` etc.); keep the vocabulary commitment in the same shape across the two
   tools.

## Verdict

**CLEAN. R-0012's B1 and B2 are discharged (all evidence re-run by me, quoted above), and the
adopted N4 null-pair control is well-formed and pre-registered with the colour-corrected
null.** E-0012 is cleared for `status: RUNNING` by this reviewer — with the pre-condition that
the build session first passes the B2.v split-at-every-k acceptance test and pins the E-0011
consistency note (the *end*-vocabulary fix in R-0014, small and shareable). The offline replay
reproduced exactly: k6 S H1 @179, finals +2.985 / +1.098 / −0.673; all six rung totals match
E-0010; dup=0.

## Date

2026-09-23

> A review never edits the original report — it lives here and is linked from the debate/report
> it concerns.

## Evidence appendix

1. `git ls-files research/context | Select-String w0005` → both files listed (tracked).
2. `certutil -hashfile …` → SHA-256 equals both pins (script `94631d6b…1233c`,
   output `9cd40402…ea35ad`).
3. `git show 16ac1ff --stat` → `.gitignore` +4, both artifacts added, 214 insertions; and
   `git show 2a9d997:…E-0012…` already contains those same hashes (chain closed at publish time).
4. `git log` on either artifact → single commit `16ac1ff`.
5. `python research/context/w0005_sprt_replay.py` → exit 0, all numbers identical to the pin
   (see report text: k6 S H1 @179 +2.985, R +1.098, M −0.673; all rung totals match E-0010;
   dup=0 per rung; ASN(H1) 1823.7/29179.8/291.8 re-derived).
6. `python research/scripts/research.py validate` → exit 0 (existing warnings only).
7. Absolute-claim sweep on E-0012: remaining "identical" occurrences are the code-path sentence
   (replay/live sharing) and B2.v's test assertion; no absolute claim to "identical decision"
   outside B2.iv's qualified form.
8. Gate 0 (attempt #11, my run): exit 0, `=== ALL TESTS PASSED` (see R-0014).

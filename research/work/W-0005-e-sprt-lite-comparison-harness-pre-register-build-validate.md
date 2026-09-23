---
id: W-0005
type: work
title: "E-SPRT-lite comparison harness: pre-register, build, validate against known difference"
round: 4
owner: researcher-architect
status: OPEN
deliverable: "research/experiments/E-#### (pre-registered) + resumable SPRT harness + validation run vs stage-6/stage-0"
exit_check: "harness decides a known-difference pair (EvalStage 6 vs 0) within its pre-registered bounds; decision sign matches the E-0010 measurement"
evidence: []
verified_by: null
verification_verdict: null
example: false
created: 2026-09-14
closed: null
---

# W-0005 — E-SPRT-lite comparison harness (H-0010)

## Objective
Every future A/B claim currently depends on ad-hoc match harnesses. Build the standing
comparison harness with pre-registered two-tier error control: screening δ≈20 Elo,
regression δ=5, LLR bounds ±2.944, game cap → INCONCLUSIVE. Resumable, runjob-compatible.

## Deliverable (exact path(s))
- Pre-registered experiment record (PENDING) BEFORE any code runs.
- Harness script + validation RUN record.

## Exit Check
```powershell
# harness output: LLR crossed a bound within cap; verdict consistent with E-0010's
# stage-6 > stage-0 (+116.1 Elo) sign and rough magnitude band.
```

## Evidence
- (to be filled)

## Work Log (append-only while OPEN)
- 2026-09-14 — opened by Round-4 meta-agent; sequencing depends on W-0002's calibrated rule.
- 2026-09-22 — researcher-architect: step 1 (pre-registration) filed —
  `research/experiments/E-0012-*.md` (PENDING): harness contract (lite LLR, ±2.9444,
  caps 8k/30k/8k, post-cap INCONCLUSIVE, crash=loss, runjob-resumable), known-difference
  design (stage-6 vs stage-0, bands vs E-0010's +116.1), and the OFFLINE validation
  (D-0007's routed ASN-model residual): realized replay of EV-0001's k1..k6 JSONL
  through the lite LLR — k6 Tier S H1 at game **179** (pred 191/173/133), Tier R
  undecided at 240 (pred 713), Tier M undecided, LLR −0.673 <0; ASN(H1) re-derived
  1823.7/29179.8/291.8 (≈ R-0010's 1822/29159/292; σ rounding). Script + output pinned
  at `research/context/w0005_sprt_replay.py` / `…_output.txt` (SHA-256 in E-0012).
  Status stays OPEN; handoff HO-0004 to adversarial-reviewer BEFORE any RUNNING.
  Live validation remains blocked by F-0002.
- 2026-09-22 — adversarial-reviewer (S-0010, via HO-0004): R-0012 COMPLETED, verdict
  NOT CLEAN — two blocking findings (B1 untracked band-commitment artifact, B2
  resume/durability + FP-qualification) + N1–N5 non-blocking (N4 recommends a live
  null-pair control); E-0012 stays PENDING. (Continuity entry; the review is R-0012.)
- 2026-09-23 — researcher-architect: R-0012 addenda filed in E-0012 — "Addendum:
  R-0012 B1 response, 2026-09-23" (.gitignore negation; replay script + output now
  git-tracked in commit 16ac1ff; content re-certutil-verified against the pins from
  2a9d997; validate green post-change), "Addendum: R-0012 B2 response, 2026-09-23"
  (JSONL-line-fsync→checkpoint order, JSONL authoritative + resume_mismatch incident +
  ABORT-at-1e-9, self-consistency limitation named, FP-ordering + bound-within-1e-9
  qualification, split-at-every-k unit test as harness acceptance, runjob unlink/
  splitlines facts), "Addendum: R-0012 N4 adopted + N1/N2/N3/N5 text, 2026-09-23"
  (null-pair control stage-6 vs stage-6, cap 240, colour-corrected null at White
  58.5%, FAIL = harness-bias alarm; band sd ≈42 / ±1.9σ / 5.4% false-FAIL / detection
  floor 1.79×–0.69×; refinement needs pre-registered draw model; blind-class list; σ
  circularity sentence). Original text untouched. No scripts/ changes (selftests not
  touched). E-0012 stays PENDING; HO-0007 filed for re-critique. Gate 0 now OPEN but
  session engine-free by design.

- 2026-09-22 — adversarial-reviewer: HO-0004 critique filed as **R-0012** (COMPLETED,
  `kind: critique`, `target: E-0012`). Verdict: **NOT CLEAN — blocking findings B1 (the bands'
  pre-run commitment is not git-verifiable: replay script + output are gitignored with no
  history; hashes match E-0012's pins, mtimes consistent — fix: track the artifacts) and B2
  (resume/durability policy: JSONL-vs-checkpoint write order, authoritative artifact + abort on
  mismatch, 1e-9 assertion is self-consistency only, "identical decision when resumed" needs the
  FP qualification + split-at-every-k unit test); E-0012 stays PENDING** (also F-0002). N1–N5
  quantify the bands' information content (Tier S band ≈±1.9σ; R/M near-tautologies), rule the
  k1/k2 Tier-M anomaly "working as designed" (true effects below M−50; DEC-0010 §Tier M
  margins), judge lite-first correct (exact trinomial needs a pre-registered draw model), and
  state D-0007's residual as only partially discharged (713-promise untested). Replay reproduced
  exactly from my own code: k6 S H1 @179, finals +2.985/+1.098/−0.673; scripts/hashes pinned in
  R-0012's Evidence appendix. E-0012 record not edited by this seat.
- 2026-09-23 — adversarial-reviewer: HO-0007 re-critique filed as **R-0015** (COMPLETED,
  `kind: critique`, `target: E-0012`). Verdict: **CLEAN** — B1 chain re-run by me end-to-end
  (`git ls-files` shows both artifacts tracked; `certutil` = 94631d6b…d1233c and
  9cd40402…ea35ad = the pins published at 2a9d997; `16ac1ff` adds both files + the
  `.gitignore` negations; `git log` on either artifact = `16ac1ff` only; `validate` exit 0;
  replay re-run exit 0 with identical numbers). B2 discharged (write order JSONL→fsync→
  checkpoint→fsync with reverse prohibited, JSONL authoritative + `resume_mismatch` +
  ABORT-at-1e-9, self-consistency limitation named, FP-ordering qualification honest — the
  absolute "identical decision" form is retired and no absolute claim survives anywhere in
  the record, split-at-every-k pre-registered as harness acceptance). N4 ADOPTED and
  well-formed (stage-6 vs stage-6, cap 240, Tier-S lite-LLR statistic, colour-corrected null
  at the measured White 58.5%, 50%-centred band explicitly prohibited, FAIL → harness-audit
  first; closes the offline-replay INCONCLUSIVE gap). N1/N2/N3/N5 text landed; D-0007 residual
  wording accepted. **E-0012 is clean and cleared for the build session** (B2.v acceptance test
  + UCI-entry confirmation + (v1)–(v4) + N4 in one sitting). Shared forward note (not
  blocking): apply E-0011's R-0014 `end`-vocabulary fix to the harness's own records too.
  E-0012 not edited by this seat; HO-0007 closed DONE.

## Verification

## Verification
- verified_by: (a different agent than owner)
- verdict: (VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE)
- evidence: (review record id + command outputs)
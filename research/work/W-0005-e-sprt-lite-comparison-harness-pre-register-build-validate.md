---
id: W-0005
type: work
title: "E-SPRT-lite comparison harness: pre-register, build, validate against known difference"
round: 4
owner: researcher-architect
status: DONE
deliverable: "research/experiments/E-#### (pre-registered) + resumable SPRT harness + validation run vs stage-6/stage-0"
exit_check: "harness decides a known-difference pair (EvalStage 6 vs 0) within its pre-registered bounds; decision sign matches the E-0010 measurement"
evidence: ["research/runs/RUN-0002-e-0012-live-known-difference-validation.md", "research/runs/RUN-0003-e-0012-n4-null-pair-control.md", "research/reviews/R-0018-independent-verification-w-0005-e-0012-live-runs-run-0002-and-run-0003-ho-0012.md", "tools/e0012_sprt.py", "m0_audit/e0012_known/games.jsonl", "m0_audit/e0012_null/games.jsonl"]
verified_by: "verification-auditor (fresh occupant, rotating seat; HO-0012 receiver)"
verification_verdict: VERIFIED
example: false
created: 2026-09-14
closed: 2026-09-25
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

- 2026-09-24 — S-0015 bundled implementation-engineer + systems-researcher for W-0005 step 2. Built `tools/e0012_sprt.py` at `752216c`: exact Tier-S/R/M margins/caps, ±ln(19) lite LLR, crash=loss, one-look, suffix-free end/end_seconds records, JSONL→fsync→checkpoint→fsync, JSONL-authoritative resume with `resume_mismatch` and ≤1e-9 continue/ABORT rule, bound-within-epsilon incident, N4 colour-corrected control fields, and live/replay shared core. Acceptance: retained k6 SHA-256 `9da1cfa0…fd0d227` reproduced H1 at game 179, LLR `+2.9847724800839215`; R +1.0976584432 INCONCLUSIVE; M -0.6733541385 INCONCLUSIVE. Split-at-every-k acceptance PASS for all 239 split points on a 240-game no-boundary W/D/L sequence, with no incident; cap/monotonicity/epsilon/mismatch-abort assertions PASS. E-0012 deliberately remains PENDING because no E-0012 live run started in S-0015; dataset milestone has priority.

- 2026-09-25 — researcher-architect (S-0020, owner record note; evidence produced by
  systems-researcher under HO-0011 / S-0019): **live phase executed, contract held
  frozen.** RUN-0002 (known-difference: Tier S, stage 6 vs 0, cap 8,000, salt 20260924)
  COMPLETED exit 0 — **H1 accepted at game 125** ∈ [80, 800], LLR +2.9591 ≥ 2.9444,
  W80/D20/L25, 0 duplicate move lists, 125/125 legal, 0 incidents. RUN-0003 (N4 null
  pair stage 6 vs 6, cap 240) COMPLETED exit 0 — **no H1**, INCONCLUSIVE at cap, LLR
  −0.6852, colour-corrected null (`white_prior 0.585`, `band_centred_at_50pct: false`,
  `pass: true`), 240/240 legal. Executor-side independent audit PASS on both
  (`m0_audit/s0018/e0012_audit.py`); single uninterrupted executions, `--retry 0`
  honoured; all artifact SHA-256s recorded. Record set committed pre-launch at
  `7aab350`; harness-stamped `src_commit` matches. **Status stays OPEN** — the
  executor's audit is independent of the harness but not of the executor; verification
  fields untouched pending the fresh verification-auditor review routed via HO-0012
  (expected R-0018). The 125 (live) vs 179 (offline replay) Tier-S crossing delta is
  flagged to the auditor as unestablished, consistent-by-(N1) with sampling noise only;
  NO engine-strength claim is licensed by RUN-0002.
- 2026-09-25 — researcher-architect (S-0022, **owner close-out**): R-0018 COMPLETED with
  verdict **VERIFIED** (fresh verification-auditor occupant via HO-0012): independent
  re-derivation matched the executor records exactly — LLR recomputations agree to
  < 1e-9 (RUN-0002 +2.9590633873412573 H1 @ 125 ∈ [80, 800]; RUN-0003
  −0.6852460784333203 INCONCLUSIVE at cap 240); 365/365 games legal on an independent
  python-chess replay; 0 duplicate move lists; 0 incidents; every SHA-256 pin matched
  (incl. binary == EV-0010 pin `504eb01a…6daa`); contract immutability confirmed (zero
  E-0012 contract edits after pre-launch commit `7aab350`, per-row `src_commit` and
  salt 20260924 uniform); all 6 HO-0012 ruling questions PASS, incl. the colour-corrected
  null band (58.5% prior; 50%-centred band prohibited and unused; null LLR ≈ −0.76σ,
  consistent, no harness bias) and the 125-vs-179 ruling (within the pre-declared (N1)
  sampling allowance; cause unestablished; **no engine-strength claim licensed**).
  **Exit check satisfied**: the harness decided the known-difference pair within its
  pre-registered bounds and the decision sign matches the E-0010 measurement
  (stage 6 > stage 0). Closing W-0005 **DONE**; `verified_by`/`verification_verdict`
  set from R-0018. E-0012's record transitions RUNNING → COMPLETED (result: PASS —
  harness-validation claim only).

## Verification

## Verification
- verified_by: verification-auditor (fresh occupant, rotating seat; HO-0012 receiver)
- verdict: VERIFIED
- evidence: research/reviews/R-0018-independent-verification-w-0005-e-0012-live-runs-run-0002-and-run-0003-ho-0012.md (COMPLETED, kind: verification, target: W-0005) — independent LLR recomputation from raw JSONL matched checkpoints to < 1e-9; python-chess legality replay 125/125 + 240/240, duplicate move lists 0; certutil SHA-256 re-checks matched RUN-0002/RUN-0003 pins (known JSONL 637a9fa4…d407, null JSONL 5654db60…e30d, binary 504eb01a…6daa); contract immutability via git history (no E-0012 contract edits after 7aab350); all 6 HO-0012 ruling questions ruled PASS/VERIFIED.
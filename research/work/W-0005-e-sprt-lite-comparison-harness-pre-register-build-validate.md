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

## Verification
- verified_by: (a different agent than owner)
- verdict: (VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE)
- evidence: (review record id + command outputs)
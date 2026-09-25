---
id: HO-0012
type: handoff
from: researcher-architect
to: verification-auditor
work_item: W-0005
status: REQUESTED
title: Independent verification: W-0005 E-0012 live runs RUN-0002 and RUN-0003
artifacts: ["research/work/W-0005-e-sprt-lite-comparison-harness-pre-register-build-validate.md", "research/experiments/E-0012-e-sprt-lite-comparison-harness-pre-registered-dec-0010-tiers.md", "research/runs/RUN-0002-e-0012-live-known-difference-validation.md", "research/runs/RUN-0003-e-0012-n4-null-pair-control.md", "research/handoffs/HO-0011-execute-e-0012-live-known-difference-and-null-pair-controls.md", "research/sessions/S-0019-ho-0010-w-0001-close-out-and-ho-0011-e-0012-live-validation.md", "tools/e0012_sprt.py"]
commands: ["build\\Release\\kana.exe", "python research/scripts/research.py validate", "python tools/e0012_sprt.py --self-test", "python research/scripts/research.py new-review --title ...", "python research/scripts/research.py update", "python research/scripts/research.py state --write"]
acceptance: "Fresh verification-auditor independently re-derives both RUN-0002/RUN-0003 results from the raw local artifacts (own LLR recomputation, python-chess legality replay, SHA-256 re-checks, contract-immutability history check), files R-0018 COMPLETED with an explicit verdict on the 6 ruling questions, and records raw exit codes. W-0005 lifecycle and verification fields are NOT touched by the auditor."
example: false
created: 2026-09-25
closed: null
---

# HO-0012 — Independent verification: W-0005 E-0012 live runs RUN-0002 and RUN-0003

> The ONLY way to ask another agent to do something. Prose requests ("someone should
> verify this") are not handoffs and will be ignored. Receiver appends `## Response`
> and `## Verification`; the handoff may be edited while `status: REQUESTED|ACCEPTED`
> and is frozen once `DONE|REJECTED|WITHDRAWN`.

## Request

Act as a **fresh verification-auditor** (a new occupant; occupant 5 verified W-0001 under
HO-0009/S-0017 — different work item, but this seat must not have produced any of the
evidence under review). HO-0011 has been discharged by systems-researcher (S-0019): both
E-0012 live runs are terminal. Your job is the **independent** opinion on that live
evidence for W-0005.

**Re-derive; do not re-run and do not trust.** The verdict must come from the raw local
artifacts (`m0_audit/e0012_known/`, `m0_audit/e0012_null/`). The executor-side audit
(`m0_audit/s0018/e0012_audit.py`) is independent of the harness computation but NOT of
the executor — treat it as an implementation to reproduce/cross-check with your own run
of it, never as evidence to cite. The executor's recorded numbers are claims, not facts.

You must NOT change W-0005's lifecycle or verification fields, and you must NOT edit
E-0012, RUN-0002, RUN-0003, or the raw artifacts. Your deliverable is the review record
(R-0018 expected; the CLI result is authoritative) plus this handoff's append-only
Response/Verification sections. Honest NOT VERIFIED / PARTIAL / BLOCKER outcomes are
allowed and must not be softened.

This is the E-0012 **harness-validation** review. RUN-0002's H1 acceptance is a claim
about the harness deciding a known difference; it licenses **no engine-strength claim**,
and your verdict must say so explicitly.

## Artifacts To Read (paths)

- `research/work/W-0005-e-sprt-lite-comparison-harness-pre-register-build-validate.md`
- `research/experiments/E-0012-e-sprt-lite-comparison-harness-pre-registered-dec-0010-tiers.md`
- `research/reviews/R-0012-critique-e-0012-pre-registration-and-offline-sprt-replay.md`
- `research/reviews/R-0015-critique-e-0012-addenda-b1-b2-n4-null-pair-ruling.md`
- `research/handoffs/HO-0011-execute-e-0012-live-known-difference-and-null-pair-controls.md`
- `research/runs/RUN-0002-e-0012-live-known-difference-validation.md`
- `research/runs/RUN-0003-e-0012-n4-null-pair-control.md`
- `research/sessions/S-0019-ho-0010-w-0001-close-out-and-ho-0011-e-0012-live-validation.md`
- `tools\e0012_sprt.py`
- `research/agents/verification-auditor/profile.md`
- Raw local evidence: `m0_audit/e0012_known/` and `m0_audit/e0012_null/`
  (`games.jsonl`, `checkpoint.json`, `run.log`, `heartbeat.txt`; `incidents.jsonl`
  must be absent), plus `m0_audit/s0018/e0012_audit.py` and its outputs.

## Commands To Run

Gate and preflight:

```powershell
cd C:\Users\tahae\Kanamecide
build\Release\kana.exe
python research/scripts/research.py validate
python tools\e0012_sprt.py --self-test
```

Then, from the raw artifacts only:

1. Re-hash (certutil SHA-256) every artifact in both evidence dirs and compare against the
   hashes recorded in RUN-0002/RUN-0003 (`637a9fa4…d407` known JSONL; `5654db60…e30d` null
   JSONL; binary `504eb01a…6daa` == the EV-0010 pin).
2. Recompute the cumulative lite-LLR series independently from each `games.jsonl` and
   compare against `checkpoint.json` (known: 2.9590633873412573 @ game 125, H1;
   null: −0.6852460784333203 @ cap 240, INCONCLUSIVE).
3. Replay all 125 + 240 games through python-chess (or equivalent) for legality and
   duplicate-move-list = 0.
4. Contract immutability: the runjob commands recorded in the RUN records must equal the
   frozen HO-0011 commands verbatim; `git log` on E-0012's contract text must show no
   contract change after the pre-launch commit `7aab350`; every JSONL row's `src_commit`
   must equal the launch-time HEAD and `campaign_salt` must be 20260924.
5. Run the executor's audit script yourself on both campaigns
   (`python m0_audit/s0018/e0012_audit.py <games.jsonl> <checkpoint.json> 6 0 8000 20260924`
   and `… 6 6 240 20260924`) and confirm `RESULT: PASS` with empty `problems` — as your
   own execution, not as cited evidence.

File the review:

```powershell
python research/scripts/research.py new-review --title "Independent verification: W-0005 E-0012 live runs RUN-0002 and RUN-0003 (HO-0012)"
python research/scripts/research.py update
python research/scripts/research.py state --write
python research/scripts/research.py validate
```

## Ruling Questions (answer each explicitly in the review)

1. **RUN-0002**: do recomputed LLR/verdict/crossing match (H1 @ 125 ∈ [80, 800])?
   Duplicates 0? 125/125 legal? Incident absence corroborated by run.log/heartbeat?
2. **RUN-0003**: do recomputed LLR/verdict match (no H1, INCONCLUSIVE at cap 240)?
   Was the null band colour-corrected (`white_prior 0.585`, `band_centred_at_50pct:
   false`, `pass: true`) — never the prohibited 50%-centred band? Is the as-is negative
   final LLR (−0.685 ≈ −0.76σ against R-0015's delta-method sd ≈ 0.90 at 240 games)
   consistent with the null, or is there evidence of harness bias?
3. **Contract fidelity**: frozen parameters only — Tier S, ±2.9444 bounds, default cap
   8000 / null cap 240, salt 20260924, stages per command — and zero post-launch edits to
   E-0012's contract text.
4. **125-vs-179**: the live Tier-S crossing at game 125 vs the offline replay's 179 is
   within E-0012's (N1) pre-declared ≈5.4% two-sided false-FAIL sampling allowance.
   Rule on consistency; rule explicitly that the *cause* of the earlier live crossing is
   not established and that RUN-0002 licenses no engine-strength claim.
5. **Crash-rule accounting**: incidents absent; confirm nothing in run.log requires
   crash=loss handling to have fired.
6. **Liveness/durability**: single uninterrupted executions, `--retry 0` honoured, no
   resume/relaunch; supervisor heartbeats reach EXIT lines with matching line counts.

## Acceptance Criteria (what makes this DONE)

1. The review record (expected R-0018) is COMPLETED with an explicit verdict
   (VERIFIED / CONTRADICTED / PARTIAL / UNVERIFIABLE) covering all 6 ruling questions,
   with raw exit codes and re-computed hashes.
2. All re-derived numbers match the RUN records, or every mismatch is reported verbatim
   with the raw output — no silent reconciliation.
3. W-0005's front matter fields (`status`, `verified_by`, `verification_verdict`) are
   untouched by you; the owner closes W-0005 only AFTER consulting your review.
4. `update`, `state --write`, `validate` run to exit 0; commit/push recorded here.
5. Handoff transitions REQUESTED → ACCEPTED → **DONE** (DEC-0009 handoff vocabulary:
   `CLOSED` is rejected by `validate`; set `closed:` to the date).

## Response (receiver, append-only)
- 2026-09-25 — (role) — ...

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: ...
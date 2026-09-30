---
id: FND-0005
type: finding
title: "B5 Q-SCOPE: the KING-PST choice was deferred, and the consequence ladder'"
status: RESOLVED
example: false
created: 2026-09-29
target: E-0013
severity: blocking
raised_by: chief-architect (extraction; original raisers in source)
review: E-0013-h-0013-texel-fit-on-verified-e-0011-datas
resolution: B5 (Q-SCOPE: the KING-PST choice was deferred, and the consequence ladder's fallback was cited to a contradicting attribution): DISCHARGED (text). KING PSTs FROZEN at E-0013 L782; the backwards ladder citation is corrected with deltas recomputed from E-0010's own ladder.
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0005

## Origin
Prose item `B5` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> Q-SCOPE: the KING-PST choice was deferred, and the consequence ladder's fallback was cited to an attribution that contradicts it

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `
### B5 - Q-SCOPE: the KING-PST choice was deferred, and the consequence ladder's fallback was cited to an attribution that contradicts it

**B5 sentence 1 (KING PSTs frozen, HERE, not at preflight), verbatim per R-0019:**`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED (text); the historical-record half is a dated correction note + obligation, by design.**
B5 has two halves: the *scope choice* (deferred to preflight) and a *backwards citation* in the
consequence ladder. The first is discharged by deciding it here; the second is deliberately NOT
discharged by editing E-0011/W-0001, because those are COMPLETED / DONE-VERIFIED records and
silently repairing verified history is the thing this system exists to prevent.

**Commands re-run this session (2026-09-30), output in `_obs/vf/`:**

1. **The choice is made HERE, not deferred** — `Select-String research/experiments/E-0013-*.md
   -Pattern 'KING PST|KING-PST'` → `E-0013 L782: '> **Q-SCOPE adopted: all-terms, KING PSTs FROZEN.**'`,
   superseding the inherited `'final choice pinned at execution preflight'` (L469 disposition row
   confirms: `| Q-SCOPE | **all-terms, KING PSTs FROZEN** (B5). |`).
2. **I recomputed the ladder deltas from E-0010's own numbers rather than accepting the record's** —
   `_obs/parts/b56math.py` → `B5: k4-k3 = 100.8-104.5 = -3.7   (record: -3.7)` and
   `B5: k6-k5 = 116.1-127.6 = -11.5   (record: -11.5)`. **Both reproduce exactly.** The record's
   claim at L1048 ("(k4-k3 = 100.8-104.5 = -3.7; k6-k5 = 116.1-127.6 = -11.5) and they reproduce
   exactly") is true, and I confirm it independently.
3. **The mis-citation is named, and the reason the ladder can no longer auto-apply is stated** —
   `E-0013 L1044-L1045`: the fallback scope named the two WORST-attributed terms (mobility -3.7 Elo,
   tempo -11.5 Elo), i.e. the ladder pointed *backwards* at the terms that had been removed. Because
   the citation is corrected and the deltas recomputed, the auto-apply is disarmed.
4. **The "deliberately not discharged" half is correctly routed, not quietly dropped** —
   `E-0013 L969` residual column: *"Deliberately NOT discharged against E-0011/W-0001, and this is
   the point: they are COMPLETED / DONE-VERIFIED records … F-U4 owns the correction, by the owning
   seat, at E-0013 close-out."*
5. Target integrity — `_obs/vf/hb.py` → `H_body sha256 = c7ebe54c…bea7` / `22196` bytes, unchanged.

**Residual uncertainty (stated, not smoothed):** R-0020 ruled B5 **PARTIALLY DISCHARGED**; I verified
the two things B5 itself turned on (the choice is made in-record at L782; the deltas reproduce) but
did **not** re-derive E-0010's ladder from its source run — I took `100.8 / 104.5 / 116.1 / 127.6` from
E-0013's own transcription at L1048. The correction obligation itself (**F-U4**, FND-0011) remains
OPEN at `major` and is owned by the E-0011 seat, not by me.


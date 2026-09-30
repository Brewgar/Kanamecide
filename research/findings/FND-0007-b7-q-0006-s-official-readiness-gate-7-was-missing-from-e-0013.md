---
id: FND-0007
type: finding
title: "B7 Q-0006's official readiness gate 7 was missing from E-0013"
status: RESOLVED
example: false
created: 2026-09-29
target: E-0013
severity: blocking
raised_by: chief-architect (extraction; original raisers in source)
review: E-0013-h-0013-texel-fit-on-verified-e-0011-datas
resolution: B7 (Q-0006's official readiness gate 7 was missing from E-0013): DISCHARGED (text). Q-0006 readiness gate 7 is quoted into the record and given teeth - a verification-auditor handoff on any terminal verdict, carrying the artifact hash, the pre-fit commit hash and the split-map hash.
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0007

## Origin
Prose item `B7` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> Q-0006's official readiness gate 7 was missing from E-0013

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `
### B7 - Q-0006's official readiness gate 7 was missing from E-0013

**B7 sentence, verbatim per R-0019, with Q-0006's own text quoted as the authority:**`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED (text).** B7 was an *omission* finding: Q-0006's official readiness gate 7 was
missing from E-0013. The discharge is that the gate is now quoted into the record **and given teeth**
— a gate that is quoted but cannot fire is not a gate.

**Commands re-run this session (2026-09-30), output in `_obs/vf/`:**

1. **Q-0006 is now cited by E-0013** — `Select-String research/experiments/E-0013-*.md
   -Pattern 'readiness gate 7|gate 7'` → `E-0013 L899`:
   `| DN7 | E-0013 does not cite Q-0006, whose readiness gates 1-7 govern this experiment. |
   **DISCHARGED** by B7, which quotes Q-0006 gate 7 into the record. |`
   The omission is closed and the closure is cross-referenced from the DN-table, so a reader arriving
   via DN7 lands on the discharge.
2. **The gate has teeth, not just a quotation** — `E-0013 L946-L951` (obligation **F-U5**):
   *"On any terminal verdict this record files a handoff to **verification-auditor** (never the owner,
   never the seat that ran the fit) carrying `fitted_params_sha256`, the pre-fit commit hash, the
   split-map hash, the E-00014 and E-00015 numbers, and the full command/exit-code ledger. No
   adoption, promotion or strength citation before VERIFIED. Owner: the E-0013 execution seat. Due:
   at E-0013 close-out."*
   I checked the property that makes this a gate rather than a note: **the addressee is an independent
   seat and the trigger is a state transition (any terminal verdict)**, and adoption is blocked until
   VERIFIED. That is Gate 3 written into E-0013's own text.
3. **This is the row I am discharging from inside the mechanism it describes.** The gate's addressee
   is `verification-auditor`; the seat discharging it is `verification-auditor`, and it is neither the
   owner (`researcher-architect`) nor the repairer (`implementation-engineer`). Gate 3 satisfied.
4. **The split-map hash the gate will require is independently reproducible today** — the exact
   command HO-0019 V6 specifies, re-run this session (`_obs/vf/v6.txt`):
   `python -c "import sys; sys.path.insert(0,'tools'); import e0013_extract as e; m=e.canonical_json({...})"`
   → `bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea`, **matching the published
   value exactly**. So the gate's evidence requirement is satisfiable, not aspirational.
5. Target integrity — `_obs/vf/hb.py` → `H_body sha256 = c7ebe54c…bea7` / `22196` bytes, unchanged.

**Residual uncertainty (stated, not smoothed):** B7's *content* is discharged; its *filing* is not
yet done. F-U5 says the handoff is filed **at E-0013 close-out**, and E-0013 has not reached a
terminal verdict — so no terminal-verdict handoff exists or is owed yet. **F-U5 = FND-0012** remains
OPEN at `major` and correctly does not gate lint. I did not fabricate a terminal verdict to satisfy
it, and I did not flip any status.


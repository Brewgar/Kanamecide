---
id: FND-0025
type: finding
title: "F-U9 Re-derive and re-commit the split map and the artifacts"
status: RESOLVED
example: false
created: 2026-09-30
severity: major
target: E-0013
raised_by: researcher-architect (S-0036..S-0040 F-U family)
review: E-0013
source_key: F-U9
resolution: F-U9 (re-derive and re-commit the split map and the artifacts): DISCHARGED. Artifacts are HASH-PINNED by the S-0039 owner ruling and the pin is reproducible: 'split map: the published hash is reproducible from the file' PASS, and I independently recomputed the digest bb079a41...a1ea to the published value.
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0025

## Finding

## Origin
Prose item `F-U9` extracted from the E-0013 F-U7..F-U13 obligation table, which carries the items recorded across sessions S-0036..S-0040.

## Finding
The obligation as stated in E-0013's own table. The source record is the authority; a verifier closes this row only with commands, outputs and hashes.

## Target
- Record: E-0013#F-U9

## Evidence
- Extracted by the verification-auditor's idempotent migration (`_obs/parts/extract_fu.py`), which skips any key already present as a `source_key:` in research/findings/.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED.** The artifacts are re-derived and **hash-pinned**, and I reproduced the pin
independently rather than reading it.

**Commands re-run this session (2026-09-30), output in `_obs/vf/fu_evidence.txt` and `_obs/vf/v6.txt`:**

1. `python tools/e0013_extract.py --selftest` → `SELFTEST PASS checks=112 failed=0`, **exit 0**.
2. The pin is **reproducible from the file**, which is the property that makes it a pin:
   `PASS  split map: the published hash is reproducible from the file`
3. **I recomputed the split-map digest myself**, using the exact expression the handoff specifies
   (`canonical_json` over format / `split_salt` / `train_fraction` / rule / `map` for
   `split_map(range(1000))`):
   → `bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea`
   **Identical to the published value.** This is HO-0019's V6 and F-U9's evidence requirement at once.
4. **V6's actual prediction is confirmed, not assumed** — the hashed object is a pure function of
   (`SPLIT_SALT`, `game_id`) and contains **no dedup-derived quantity**: the keys are `format`,
   `split_salt`, `train_fraction`, `rule` and `map`. The split cannot move when the dedup key moves,
   which is exactly why this digest is invariant across the key change.
5. Provenance discipline is enforced in code, so a stale artifact cannot be inherited silently:
   `PASS  provenance: a previous report's src_commit is NEVER read back`,
   `PASS  provenance: the poisoned digest is overwritten, not inherited`,
   `PASS  dataset pin: a wrong hash aborts`.

**Residual uncertainty (stated, not smoothed):** the S-0039 owner ruling (E-0013 L2357,
`### 10. RULING 1 (F-U10)` … `RULING 2` on the pins) is the *authority* for what the pins are; I
verified the pins are **reproducible and correctly specified**, not that the owner selected the
right set of files to pin. Separately, I observed the tool **abort rather than write** on a
provenance mismatch (`ABORT: SRC-COMMIT PIN VIOLATED … nothing is written`), which is the correct
behaviour but does mean the hash-pinned artifacts are not currently regenerable from a dirty tree.


## Evidence
_commands, outputs, hashes_


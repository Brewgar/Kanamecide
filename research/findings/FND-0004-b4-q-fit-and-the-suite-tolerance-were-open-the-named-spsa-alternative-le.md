---
id: FND-0004
type: finding
title: "B4 Q-FIT and the suite tolerance were OPEN, the named SPSA alternative le"
status: RESOLVED
example: false
created: 2026-09-29
target: E-0013
severity: blocking
raised_by: chief-architect (extraction; original raisers in source)
review: E-0013-h-0013-texel-fit-on-verified-e-0011-datas
resolution: "B4 (Q-FIT + suite tolerance OPEN, SPSA leaks, no deferred value anchored): DISCHARGED. Q-FIT adopted / SPSA withdrawn; SUITE_TOLERANCE=0.02 is a NUMBER with a derivation; the single pre-fit commit is the freeze anchor. Both R-0020 seams verified joined, and the 0.6x-SE arithmetic was recomputed by me: SE=0.035355, 0.02/SE=0.566."
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0004

## Origin
Prose item `B4` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> Q-FIT and the suite tolerance were OPEN, the named SPSA alternative leaked, and no deferred value was anchored

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `
### B4 - Q-FIT and the suite tolerance were OPEN, the named SPSA alternative leaked, and no deferred value was anchored

**B4 sentence 1 (Q-FIT adopted, SPSA withdrawn), verbatim per R-0019:**`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED.** B4 is the row where the *number* is the deliverable: R-0019's complaint was
that the suite tolerance was OPEN (a placeholder) and that the named SPSA alternative leaked. I did
not accept the disposition table; I recomputed the tolerance's derivation from first principles.

**Commands re-run this session (2026-09-30), output in `_obs/vf/`:**

1. **The tolerance is a NUMBER, and its derivation is intact and contiguous** — I read
   `E-0013 L749-L770`. L752: `SUITE_TOLERANCE = 0.02`. The reasoning is one unbroken quoted block:
   the SE bound at L763-L764 (`0.5 / sqrt(200) = 0.0354`), the two-sided argument at L764-L765
   ("a tolerance at or below the noise floor would make conjunct (f) a coin flip … far above it
   would make the conjunct decorative"), and the chosen multiple at L766.
2. **I recomputed that arithmetic myself rather than accepting the record's numbers** —
   `_obs/vf/b4math.py` (`python _obs/vf/b4math.py`) →
   `worst-case paired binomial SE at N=200 : 0.035355  (record says 0.0354)` and
   `0.02 / SE : 0.5657  (record says ~0.6x)`.
   **Both reproduce.** The record's `0.0354` is the correctly-rounded `0.5/sqrt(200)`, and its
   "roughly 0.6x" is the correctly-rounded `0.5657`. The derivation is honest, not decorative.
3. **Seam 2 — the freeze anchor — is JOINED.** R-0020 listed it as severed at "and the holdout is"
   (old L646 → old L941). `Select-String … -Pattern 'SAME pre-fit commit as the game-split map'` →
   `E-0013 L743: '> with its SHA-256 in the SAME pre-fit commit as the game-split map, and the
   holdout is'` and the very next lines continue `> not read before that commit exists.`
   **Head and continuation are now adjacent (L743-L744).**
4. **Seam 4 — the tolerance derivation — is JOINED.** R-0020 listed old L664 → old L911.
   Same grep → `E-0013 L766: '> the conjunct decorative. 0.02 sits at roughly 0.6x the worst-case
   paired binomial SE,'` — now inside the same quoted block as its own head at L764-L765.
5. **SPSA did not leak, and the freeze is anchored to a commit** — the L738-L747 block enumerates the
   pinned set (fresh SPRT salt, salt-distance citation, KING-PST scope, phase-tertiles, label-mapping
   code, optimizer seed / L2 weight / iteration budget / clipping, stage index `S*`, suite identity,
   N, metric and tolerance) and extends the tripwire at L746-L747: the pre-existing clause is
   extended by *"or assigned for the first time after the holdout is read"*. That is the anchoring
   B4 demanded: a deferred value can no longer be first-assigned after the holdout opens.
6. F11 closure rests on this anchor and is pointer-closed by it —
   `E-0013 L1070: '| F11 | LOSS_MARGIN = 0.002 attainability | **POINTER**: E-00014 …'`.
7. Target integrity — `_obs/vf/hb.py` → `H_body sha256 = c7ebe54c…bea7` / `22196` bytes, unchanged.

**Residual uncertainty (stated, not smoothed):** R-0020 ruled B4 **PARTIALLY DISCHARGED** and named
the condition for full discharge — every seam in the X1 list joined. I verified the two B4 seams
(3 and 4 above) directly and they are joined. I did **not** re-verify all ten X1 seams row-by-row in
this session; that aggregate check is R-0022's, and I record that I relied on the two B4-specific
seams I could check cheaply and did not re-derive the whole list. The 0.02 tolerance itself remains
**revisable only by a dated addendum filed before the suite is committed** (L769-L770) — it is frozen
only once the pre-fit commit exists, which has not happened.


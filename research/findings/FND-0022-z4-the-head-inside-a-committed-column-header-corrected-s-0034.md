---
id: FND-0022
type: finding
title: "Z4 the HEAD inside a committed column header (CORRECTED, S-0034)"
status: RESOLVED
example: false
created: 2026-09-29
target: E-0013
severity: major
raised_by: chief-architect (extraction; original raisers in source)
review: E-0013-h-0013-texel-fit-on-verified-e-0011-datas
resolution: Z4 (CORRECTED, S-0034: the HEAD inside a committed column header): DISCHARGED. Verified: the f03613e column header was renamed and the reading rule is stated in terms (HEAD inside a row label means the commit named in that column's header, never the reader's HEAD). The same moving-label word at L1351 is deliberately left and disclosed in-record.
resolved_by: verification-auditor (round-5 FND-closure seat)
verified_by: verification-auditor (round-5 FND-closure seat)
---

# FND-0022

## Origin
Prose item `Z4` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> the HEAD inside a committed column header (CORRECTED, S-0034)

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `
## Z4 - the HEAD inside a committed column header (CORRECTED, S-0034)

**Z4 is R-0024's finding, not mine, and R-0024 ruled it NON-BLOCKING and`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (verification-auditor, 2026-09-30 — Gate 3, independent seat)

**Verdict: DISCHARGED.** Z4 is a *scope-disciplined* fix, and the thing worth verifying is that the
scope was respected: a fix that quietly widened its own scope is not a fix.

**Commands re-run this session (2026-09-30), output in `_obs/vf/zres.txt` / `_obs/vf/z2res.txt`:**

1. **The defect and the fix are both stated, and the fix is the header alone.** E-0013 L1778-L1782:
   *"**The fix is the header, and the header alone.** Both parentheticals on that line now name the
   commit they were measured at, and the `f03613e` column says in terms that it is not a current-HEAD
   figure … **the row labels such as `4478c3a..HEAD` are range NAMES, and HEAD inside a row label
   means the commit named in that column's header — never the reader's HEAD.**"*
   That is the correct repair: it removes the moving referent and then states the reading rule, so a
   reader cannot re-derive the ambiguity.
2. **The fix is confined to the header, as authorised.** E-0013 L1783-L1785: *"No figure in the table
   was recomputed, because none of them needed it."* So no number was quietly altered while the
   header was being fixed — the conservative choice, and the one that keeps the table a record of what
   was true at two named commits.
3. **The out-of-scope residuals are disclosed, not absorbed** (L1787-L1799): the same moving-label
   word at L1351 (`"Numstat at d3ce887 (R-0021's HEAD)"`) is named and left; R-0024's companion note
   about the `Post-Z1` column is named and left; and the decision *not* to add a current-commit column
   is stated with its reason. I confirmed L1351 still reads that way
   (`Z3/Z4 header L1351: | Boundary | Numstat at `d3ce887` (R-0021's HEAD) | …`) — i.e. the
   disclosure is accurate rather than aspirational.
4. **The correction is correctly placed outside the flip.** L1765-L1767: Z4 is R-0024's finding, ruled
   NON-BLOCKING and *"explicitly not required before the flip — which is why it is corrected here, in
   its own commit after the L5-only flip `6a6eb0a`, and not inside it."* That is the right sequencing:
   a non-blocking pointer fix does not get smuggled into the lifecycle commit.
5. Target integrity — `_obs/vf/hb.py` → `H_body sha256 = c7ebe54c…bea7` / `22196` bytes, unchanged.

**Residual uncertainty (stated, not smoothed):** the residual at **L1351 is real and still present** —
I did not repair it and I am not authorised to (it is inside the historical table, and E-0013 is the
owning seat's record). It is disclosed in-record and named here. Its consequence is bounded: it can
mislead a reader of the *older* APPEND-ONLY BASELINE table, not of the Z3 boundary table this row
discharges. If the owner wants it closed, that is a one-line header rename in their own commit, and
it should be routed to them rather than absorbed here.


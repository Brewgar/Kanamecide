---
id: FND-0009
type: finding
title: "F-U2 the deferred strength contract (the cost of the B1 SHRINK decision).**"
status: OPEN
example: false
created: 2026-09-29
target: E-0013
severity: major
raised_by: chief-architect (extraction; original raisers in source)
review: E-0013-h-0013-texel-fit-on-verified-e-0011-datas
resolution: 
resolved_by: 
verified_by: 
---

# FND-0009

## Origin
Prose item `F-U2` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> the deferred strength contract (the cost of the B1 SHRINK decision).** A

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `  Owner: researcher-architect. Due: E-0013 close-out.
- **F-U2 - the deferred strength contract (the cost of the B1 SHRINK decision).** A
  separate E-0012-style contract (its id to be CLI-assigned when it is filed) for the fitted-vs-pinned Tier-S
  SPRT, with its own pre-registration, its own critique, its own harness validation and`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (fill when closing)
- ...

## Addendum 2026-09-30 — verification-auditor (round-5 ledger-tail seat, Gate 3) — **NOT DISCHARGED; row stays OPEN**

**This row is NOT closed.** The deferred strength contract (the cost of the B1 SHRINK decision) has
not been filed, and the single-`--exe` wall it names still stands.

**What the finding asks.** File a separate E-0012-style contract for the fitted-vs-pinned Tier-S
SPRT (id CLI-assigned at filing) with its own pre-registration, critique, harness validation and
independent verification; the named minimum mechanism is two distinct binaries differentiated by
per-binary `sha256_file`, requiring the minimal two-`--exe` change to `tools/e0012_sprt.py`;
`--validation-known` MUST NOT be passed. Due: filed before any strength game is generated.
(E-0013 L926-L935 = F-U2.)

**Commands I ran this session, and what they show.**

1. `Get-ChildItem research/experiments -Name` (`_obs/experiments_list.txt`) → the newest experiment
   ids are E-00014/E-00015 (count/feasibility passes, PENDING); there is no strength-contract record.
2. Phrase walk over `research/` (byte-wise, `_obs/probe_rows.py` → `_obs/probe.txt`):
   "fitted-vs-pinned" appears only in E-0013 (L48, L927), FND-0009's own seed text, and R-0019
   L281 — never as a filed contract.
3. `tools/e0012_sprt.py` argparse, byte-wise (`_obs/probe.txt`) → L474
   `parser.add_argument("--exe", default=str(DEFAULT_EXE))`: exactly ONE `--exe`; the two-binary
   mechanism is unbuilt.
4. The trigger has not fired: under the B1 SHRINK decision the strength conjunct is not evaluated
   in this run (E-0013 L965), so no strength game has been generated.

**Exactly what is missing to discharge this row.**
(a) the filed strength contract, with its own pre-registration, critique, harness validation and
    independent verification;
(b) the minimal two-`--exe` change to `tools/e0012_sprt.py` (or the single-binary alternative,
    only if the contract so elects);
(c) executor/owner assignment for the build (E-0013 L934 names the roles at filing).

**Not touched by me (binding):** I did not edit `tools/`, generate a strength game, or pass
`--validation-known`.


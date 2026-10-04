---
id: W-0009
type: work
title: Digest-stable Release build (/Brepro or equivalent) so an evidence binary pin is reproducible from source, not from a preserved copy
round: 7
owner: implementation-engineer
status: OPEN
deliverable: "_obs/brepro/ reproducibility report: N consecutive clean Release builds of the same src commit, the sha256 of each, the toolchain identifiers that vary, and the one build recipe that yields a stable digest; plus a NEW EV-00NN evidence record for the stable binary (path points at a tracked archived copy, per DEC-0013)"
exit_check: "two clean 'cmake --build build --config Release' cycles from the same src commit produce byte-identical kana.exe (same sha256), or the report names the specific varying input (PE timestamp / PDB path / __DATE__ / linker build id) and the recipe that pins it; 'python research/scripts/research.py validate' exits 0"
evidence: []
verified_by: null
verification_verdict: null
example: false
created: 2026-10-03
closed: null
---

# W-0009 — Digest-stable Release build (/Brepro or equivalent) so an evidence binary pin is reproducible from source, not from a preserved copy

> A work item is the unit of "done". Round N is over only when every work item of
> round N is `status: DONE` AND has been verified by an agent that did not produce it
> (`verified_by` + `verification_verdict: VERIFIED`). See `research/SYSTEM.md` §4/§5.

## Objective
Make the Release binary byte-reproducible from source on this host, so a future EV-00NN
binary pin is reproducible-by-rebuild instead of bound to a preserved copy (the caveat
DEC-0013 currently forces on EV-0010 and EV-0011 after FND-0034).

## Deliverable (exact path(s))
- `_obs/brepro/` report (+ raw build logs + per-build sha256 table).
- A new `research/evidence/EV-00NN-*.md` for the resulting stable binary (archived copy under
  `_obs/evidence/`, tracked by exception, per DEC-0013).

## Exit Check
> The machine-runnable command that decides DONE. Run it before claiming DONE, and
> paste its raw output (exit code included) under Evidence.

```powershell
cmake --build build --config Release ; Get-FileHash build\Release\kana.exe -Algorithm SHA256
cmake --build build --config Release ; Get-FileHash build\Release\kana.exe -Algorithm SHA256
# the two hashes must be equal for this item to succeed
python research/scripts/research.py validate   # exit 0
```

## Evidence
> command → exit code → output path → artifact SHA-256 → `src/` commit (where code ran).

- (to be filled by the owner when executed; handed off as HO-0024)

## Work Log (append-only while OPEN)
- 2026-10-03 — filed by chief-architect under Sponsor Ruling 1 (FND-0034 disposition, option (a)
  + HW-3 follow-up; staged `_obs/rulingpkg/A4_HW3_brepro_handoff.md`). Pin rule: W-0009's own
  resulting binary becomes a NEW evidence record with an archived path; existing EV-0010 /
  EV-0011 are NEVER re-pinned to it (DEC-0013).

## Verification
> Filled by the verifying agent (a different agent than `owner`), never by the owner.

- verified_by: (role)
- verdict: (VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE)
- evidence: (review record id, e.g. R-0004, plus the command outputs)
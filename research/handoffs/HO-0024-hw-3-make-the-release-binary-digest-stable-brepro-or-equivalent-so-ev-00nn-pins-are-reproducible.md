---
id: HO-0024
type: handoff
from: chief-architect
to: implementation-engineer
work_item: W-0009
status: REQUESTED
title: HW-3: make the Release binary digest-stable (/Brepro or equivalent) so EV-00NN pins are reproducible
artifacts: []
commands: []
acceptance: null
example: false
created: 2026-10-03
closed: null
---

# HO-0024 — HW-3: make the Release binary digest-stable (/Brepro or equivalent) so EV-00NN pins are reproducible

> The ONLY way to ask another agent to do something. Prose requests ("someone should
> verify this") are not handoffs and will be ignored. Receiver appends `## Response`
> and `## Verification`; the handoff may be edited while `status: REQUESTED|ACCEPTED`
> and is frozen once `DONE|REJECTED|WITHDRAWN`.

## Request
FND-0034 was dispositionsed 2026-10-03 under Sponsor Ruling 1: EV-0010 was re-pinned to the
epoch-source binary `686EA5979415054982703985C543CEB9EE7C0CD47C166903CAF8C79D12276F3B` **with an
explicit non-reproducibility caveat**, because this host's MSVC toolchain does not emit
byte-identical output twice (same source → same-size, different-digest binaries: live output has
drifted twice, once per rebuild). Per DEC-0013 the pins are now content-addressed archived copies
under `_obs/evidence/` (tracked by exception). That closes today's loop, **but it leaves every
pin's validity resting on a preserved copy rather than a reproducible build.**

This item closes that gap: make the Release binary digest-stable (`/Brepro` or equivalent), so
future pinned binaries are reproducible from source.

**Do NOT re-pin EV-0010 or EV-0011 when you do this.** Both are permanently bound to their
respective epochs (E-0010 epoch and the FND-0035 F2/F3 repair epoch). A digest-stable recipe
produces a NEW binary, which archives first and then files a NEW EV-00NN record with a tracked
archived `path:` (DEC-0013). Existing pins are not retro-cleaned by the existence of a better
recipe.

## Artifacts To Read (paths)
- `research/decisions/DEC-0013-evidence-pins-are-content-addressed-archived-artifacts.md`
- `research/findings/FND-0034-ev-0010-binary-digest-drift-after-rebuild.md` (the Erratum rows
  E1/E2/E6 document the non-reproducibility directly)
- `research/evidence/EV-0010-e0010-measurement-binary.md`, `research/evidence/EV-0011-fnd0035-f2-f3-repair-binary-and-validation.md`
- `CMakeLists.txt` (current flags), `build.bat`
- `_obs/rulingpkg/A4_HW3_brepro_handoff.md` (the staged version of this handoff; reconciliation
  note lives in S-0045)

## Commands To Run
```powershell
cd c:\Users\tahae\Kanamecide
cmake --build build --config Release ; Get-FileHash build\Release\kana.exe -Algorithm SHA256
cmake --build build --config Release ; Get-FileHash build\Release\kana.exe -Algorithm SHA256
# the two hashes must be equal for this item to succeed; if not, name the varying input
python research/scripts/research.py validate
```

## Acceptance Criteria (what makes this DONE)
- Two consecutive clean Release builds from the same `src` commit, sha256 recorded for each,
  with full commands and exit codes, in `_obs/brepro/`.
- If they differ: the report names the varying input (candidates: PE `TimeDateStamp`, embedded
  PDB path, `__DATE__`/`__TIME__`, linker build id, an unsorted static-lib link) and states the
  recipe that removes it; if a recipe is found, the cycle is re-demonstrated with it.
- A new evidence record is filed for the stable binary (new id, own `sha256`, own `regenerate`,
  own `cites`, archived `path:`) — **not** an edit to EV-0010 or EV-0011.
- `python research/scripts/research.py validate` exits 0 at the end, with the problem count
  explicitly named.
- `git --no-pager status --porcelain` reviewed: no tracked `src/` or `research/` file changed
  except the new EV record, this record's Response, and W-0009's log.

## Response (receiver, append-only)
- 2026-10-03 — (role) — ...

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: ...
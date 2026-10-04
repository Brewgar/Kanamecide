---
id: EV-0010
type: evidence
title: "E-0010 measurement binary (the current build/Release/kana.exe)"
status: REGISTERED
path: _obs/evidence/EV-0010__kana_686ea5979415.exe
kind: binary
sha256: "686EA5979415054982703985C543CEB9EE7C0CD47C166903CAF8C79D12276F3B"
regenerate: "NON-REPRODUCIBLE as bytes on this host (re-pinned 2026-10-03; Sponsor Ruling 1 / FND-0034 / DEC-0013). A rebuild of the SAME epoch source (last src commit 9b69e0a, 2026-09-14) yields a same-size, different-digest binary: this MSVC toolchain does not emit byte-identical output twice. Verify by hashing the ARCHIVED bytes at this record's path: - a tracked, content-addressed artifact - NOT by rebuilding, and NOT by hashing the live build/Release/kana.exe (which has since been rebuilt to EV-0011's post-repair binary). Digest-stable builds are filed as W-0009 / HO-0024; until they land, this digest is the content address of a preserved artifact, not a reproducible output."
retention: keep
cites: [E-0010]
example: false
created: 2026-09-19
last_updated: 2026-10-03
---

# EV-0010 — E-0010 measurement binary (current build/Release/kana.exe)

## What this is
The binary that produced E-0010 (the+tapered eval campaign): gates (a) perft+legality,
(b) symmetry, (c) Elo ladder, (d) NPS. Verified live by W-0004 occupant 1 (R-0004): the
on-disk binary matches this exact hash and runs 10/10 perft.

## Where it lives
- `build/Release/kana.exe` (rebuildable from commit 9b69e0a).

## How to regenerate / verify
```powershell
build.bat
Get-FileHash build\Release\kana.exe -Algorithm SHA256   # -> 504EB01A…A6DAA
build\Release\kana.exe                                  # 10/10 perft, ALL TESTS PASSED
```

## What it proves / supports
- E-0010 (all four gates) + the current champion claim (O3d + E-0010 eval).
- This is the binary to re-run E-0011 match campaigns against.
- This is the binary to re-run E-0011 match campaigns against.

> ### 2026-10-03 addendum — digest re-pinned and path re-pointed (FND-0034 dispositioned; Sponsor Ruling 1; DEC-0013)
>
> **The pin moved from `504EB01A…A6DAA` to `686EA597…F3B`.** The original 2026-09-19 bytes are
> gone from this machine and cannot be restored; the re-pinned digest is the content address of
> the preserved epoch-source binary — `git --no-pager diff --stat 9b69e0a bda64c7 -- src` is
> empty, so nothing in `src/` changed from the epoch up to the last pre-repair commit.
>
> **Deviation from the staged ruling text, stated openly.** The staged disposition
> (`_obs/rulingpkg/A3_EV-0010_repin.md`) kept `path: build/Release/kana.exe`, because it was
> written before the FND-0035 F2/F3 repairs landed. Since then the live output has been rebuilt
> (`A0951F4F…`, EV-0011), so a live-path pin would fail validation even after the re-pin. Under
> DEC-0013 a live build output is never a pin target; this record's `path:` now names the
> tracked archive `_obs/evidence/EV-0010__kana_686ea5979415.exe` (hash verified identical to the
> `_obs/fnd0035/binary/kana_pre_Release.exe` snapshot). The deviation IS the binding rule of
> DEC-0013, applied at birth.
>
> **Not claimed.** That `686EA597…` reproduces E-0010's ladder numbers — it has not been re-run.
> The historical `504EB01A…` affinity to E-0010's campaign remains; the re-pinned digest names a
> binary of the same source, checked by the archived bytes, not by a fresh build.
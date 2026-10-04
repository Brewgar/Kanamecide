---
id: FND-0034
type: finding
title: "EV-0010 pinned Release binary digest no longer matches the on-disk binary after a master rebuild; research.py validate now fails on evidence-hash drift (not repaired by the F-U14 seat - owner and chief-architect route)"
status: RESOLVED
example: false
created: 2026-10-02
severity: blocking
target: EV-0010
raised_by: data-pipeline-engineer (F-U14 seat; side effect of the F-U14 smoke pass build, found by research.py validate)
review: EV-0010
resolution: Option (a) executed under Sponsor Ruling 1, adapted post-inversion: EV-0010 re-pinned to the epoch-source binary 686EA5979415054982703985C543CEB9EE7C0CD47C166903CAF8C79D12276F3B with dated non-reproducibility caveat; path re-anchored to tracked archive _obs/evidence/EV-0010__kana_686ea5979415.exe under DEC-0013 (live build outputs are never pin targets); EV-0011 hardened to _obs/evidence/EV-0011__kana_a0951f4f40b5.exe; digest-stable build follow-up filed as W-0009/HO-0024; Evidence block filled (rows E1-E9); validate re-derived exit 0 / 0 problems.
resolved_by: chief-architect
verified_by: 
---

# FND-0034

## Finding
Raised by the F-U14 seat on 2026-10-02 while producing the F-U14 smoke pass, and NOT repaired there because the repair is this record owner own act. FACTS, all re-runnable: (1) `cmake --build build --config Release` was run to obtain a Release binary that provably corresponds to current master (HEAD f5883dc; `git log -- src` shows the last src commit is 9b69e0a, 2026-09-14, predating every E-0010/E-0011/E-0012 measurement). (2) The rebuild produced build/Release/kana.exe sha256 686ea5979415054982703985c543ceb9ee7c0cd47c166903caf8c79d12276f3b, 121344 B - NOT byte-identical to the 504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa recorded in this evidence record (same size, different digest: the MSVC build is not byte-reproducible here). (3) `python research/scripts/research.py validate` therefore now FAILS with `audit[evidence]: sha256 drift on build/Release/kana.exe: recorded 504EB01A8287 vs on-disk 686EA5979415 (evidence/EV-0010-e0010-measurement-binary.md)` - 1 problem, exit non-zero. (4) The pinned bytes cannot be restored on this machine: build/Release/kana.exe was the only copy (build/Audit 8f783212, build_o2/Release 0d4899ca, and m0_audit/build + m0_ctrl/build have no Release binary), so there is no 504eb01a artifact left to copy back. WHAT THIS SEAT DID NOT DO, deliberately: it did not edit this evidence record. Re-pinning an evidence digest after the fact, from a rebuilt artifact, with a non-reproducible build, is precisely the substitution the pin discipline (S-0039 Ruling 2, R-0019) exists to prevent, and this record is not the F-U14 seat to rewrite. ROUTED to this record owner and chief-architect to decide: re-pin this record to the rebuilt digest with the non-reproducibility caveat, or restore a digest-stable build (/Brepro or an equivalent) so the pin is reproducible. The F-U14 smoke pass ran against 686ea597 and its raw log header records that digest, so F-U14 own evidence chain is internally consistent and unaffected.

## Evidence

Every row is re-runnable from `c:\Users\tahae\Kanamecide` with no setup. Filled 2026-10-03 by
the chief-architect under Sponsor Ruling 1 (`_obs/rulingpkg/`, staged 2026-10-03), and
**re-derived for post-repair reality**: the FND-0035 F2/F3 repairs (`dd4051a`) landed BEFORE this
disposition was executed, inverting the ruling package's own preferred order, so the rows below
record the state actually observed at disposition time, not the state the staged text assumed.

| # | Command | Observed, 2026-10-03 | Establishes |
|---|---|---|---|
| E1 | `Get-FileHash build\Release\kana.exe -Algorithm SHA256` | `A0951F4F40B5B85923BA832362C378009F0F8ED7C4DD20BB39EF70F59B5D8BCF` | the on-disk digest has drifted a SECOND time (post-F2/F3 repair build) — exactly the recurrence this finding warned about |
| E2 | `(Get-Item build\Release\kana.exe).Length` | `121856` | the on-disk binary is now the post-repair build (different size from both previous binaries 121344), registered as EV-0011 |
| E3 | `git --no-pager log -1 --format='%H %ci %s' -- src` | `dd4051a92daf834cf4a73f1878a0c894b0b6d1b8`, `2026-10-03` (FND-0035 F2/F3 repair) | `src/` moved once beyond the E-0010 epoch, in one named commit carrying its own evidence record (EV-0011) |
| E4 | `git --no-pager diff --stat 9b69e0a bda64c7 -- src` | **empty output, exit 0** | decisive row: nothing in `src/` changed from the E-0010 epoch (`9b69e0a`, 2026-09-14) up to the commit immediately preceding the repair — the `686EA597…` smoke build (F-U14) is a build of epoch-identical source |
| E4b | `git --no-pager diff --stat 9b69e0a HEAD -- src` | only `src/search.cpp` (23 insertions, 7 deletions) | the entire post-epoch delta is the FND-0035 F2/F3 repair; no other source drift exists |
| E5 | `Get-FileHash src\eval.cpp -Algorithm SHA256` | `38B7B31C09E5…` | matches the hash E-0013's 2026-10-03 readiness addendum cites — eval source unmoved under either record |
| E6 | `git ls-files --error-unmatch build/Release/kana.exe` | exit 1 (untracked; `build/` is gitignored) | the live build output is a local artifact — which is why a digest can drift without any commit recording it, and why the live path is UNFIT as a pin target (DEC-0013) |
| E7 | `python research/scripts/research.py validate` (pre-disposition, this session) | exit 1, exactly 1 problem: `sha256 drift on build/Release/kana.exe: recorded 504EB01A8287… vs on-disk a0951f4f40b5…` | the single armed failure at disposition time; nothing else in the corpus is red |
| E8 | `Get-FileHash _obs\evidence\EV-0010__kana_686ea5979415.exe -Algorithm SHA256` | `686EA5979415054982703985C543CEB9EE7C0CD47C166903CAF8C79D12276F3B` (identical to `_obs/fnd0035/binary/kana_pre_Release.exe`, which is git-tracked) | the epoch-source binary is preserved as an archived artifact, so a re-pinned EV-0010 is checkable after the fact, not merely asserted |
| E9 | `Get-FileHash _obs\evidence\EV-0011__kana_a0951f4f40b5.exe -Algorithm SHA256` | `A0951F4F40B5B85923BA832362C378009F0F8ED7C4DD20BB39EF70F59B5D8BCF` (identical to E1) | the post-repair binary is likewise archived; EV-0011's `path:` is re-pointed to it under DEC-0013 (see EV-0011's 2026-10-03 addendum) |

**What E3+E4+E4b+E5 jointly establish.** The `686EA597…` build and the pre-drift `504EB01A…`
build were builds of the SAME source (the E-0010 epoch: `9b69e0a`, 2026-09-14; nothing in `src/`
moved until the named repair commit `dd4051a`). The digest moved without the subject moving. That
is the whole basis on which re-pinning is defensible — and it is why the re-pin must carry a
non-reproducibility caveat rather than a claim of byte-reproducibility.

**What none of these rows establishes.** That `686EA597…` reproduces E-0010's *numbers*. It is
source-identical to the epoch and content-addressed; it has never been re-run against the E-0010
ladder. Any claim requiring E-0010's numbers cites E-0010, EV-0001 and EV-0002 — not this digest.

_The Evidence block above was filled under Sponsor Ruling 1 on 2026-10-03; the placeholder line
that stood here was the finding's own unfilled Evidence slot, replaced by that fill._

## Disposition (Sponsor ruling, 2026-10-03 — chief-architect seat, Ruling 1)

**Ruled: option (a) + HW-3 follow-up.** EV-0010 is re-pinned to
`686EA5979415054982703985C543CEB9EE7C0CD47C166903CAF8C79D12276F3B` — with an explicit
non-reproducibility caveat — the preserved epoch-source binary is archived as a tracked,
content-addressed artifact, and digest-stable builds are filed as the follow-up
(W-0009 / HO-0024). The pin field is re-anchored per DEC-0013 (filed today): a live build
output is never a pin target; `path:` now names `_obs/evidence/EV-0010__kana_686ea5979415.exe`.

**Why this is a disposition and not the substitution the pin discipline forbids.** The protected
rule (S-0039 Ruling 2, R-0019) is that a pin may not be moved to whatever the last build happened
to produce. The evidence rows E3/E4/E4b/E5 show the re-pinned binary is a build of the *same
subject* (epoch-identical source at the time it was built); only the toolchain's output bytes
were unstable. What is surrendered — surrendered loudly, in EV-0010's `regenerate:` — is
byte-reproducibility of the pin. This record therefore closes **with a stated limitation**, not
silently.

**The order inversion, recorded.** The ruling package prescribed: disposition FIRST, then the
FND-0035 F2/F3 repairs, then a new EV for the post-repair binary. Execution inverted it: the
repairs (`dd4051a`) and EV-0011 landed before this disposition. No evidence value was lost —
the pre-repair binary had already been archived by the repair seat at `_obs/fnd0035/binary/` —
but the staged disposition text was written against an on-disk binary that the inversion deleted.
DEC-0013's archived-artifact model is the structural repair: no future order dependency exists,
because a pin never names a live path again.

**What is NOT claimed.** That `686EA597…` reproduces E-0010's numbers. It has not been re-run
against the ladder. Any claim requiring those numbers cites E-0010 / EV-0001 / EV-0002 — not this
digest. EV-0010 stays bound to E-0010's epoch permanently; the post-repair binary is EV-0011.

## Resolution

EV-0010 re-pinned to the archived epoch-source binary (`686EA597…`, tracked at
`_obs/evidence/EV-0010__kana_686ea5979415.exe`) with an explicit non-reproducibility caveat; the
live build output is no longer a pin target (DEC-0013); digest-stable build filed as W-0009 with
handoff HO-0024; `research.py validate` re-derived green at the close of this disposition.
Non-reproducibility is a stated limitation, recorded openly; E-0010's numbers are unaffected and
do not depend on this digest.

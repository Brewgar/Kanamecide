---
id: FND-0034
type: finding
title: "EV-0010 pinned Release binary digest no longer matches the on-disk binary after a master rebuild; research.py validate now fails on evidence-hash drift (not repaired by the F-U14 seat - owner and chief-architect route)"
status: OPEN
example: false
created: 2026-10-02
severity: blocking
target: EV-0010
raised_by: data-pipeline-engineer (F-U14 seat; side effect of the F-U14 smoke pass build, found by research.py validate)
review: EV-0010
resolution: 
resolved_by: 
verified_by: 
---

# FND-0034

## Finding
Raised by the F-U14 seat on 2026-10-02 while producing the F-U14 smoke pass, and NOT repaired there because the repair is this record owner own act. FACTS, all re-runnable: (1) `cmake --build build --config Release` was run to obtain a Release binary that provably corresponds to current master (HEAD f5883dc; `git log -- src` shows the last src commit is 9b69e0a, 2026-09-14, predating every E-0010/E-0011/E-0012 measurement). (2) The rebuild produced build/Release/kana.exe sha256 686ea5979415054982703985c543ceb9ee7c0cd47c166903caf8c79d12276f3b, 121344 B - NOT byte-identical to the 504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa recorded in this evidence record (same size, different digest: the MSVC build is not byte-reproducible here). (3) `python research/scripts/research.py validate` therefore now FAILS with `audit[evidence]: sha256 drift on build/Release/kana.exe: recorded 504EB01A8287 vs on-disk 686EA5979415 (evidence/EV-0010-e0010-measurement-binary.md)` - 1 problem, exit non-zero. (4) The pinned bytes cannot be restored on this machine: build/Release/kana.exe was the only copy (build/Audit 8f783212, build_o2/Release 0d4899ca, and m0_audit/build + m0_ctrl/build have no Release binary), so there is no 504eb01a artifact left to copy back. WHAT THIS SEAT DID NOT DO, deliberately: it did not edit this evidence record. Re-pinning an evidence digest after the fact, from a rebuilt artifact, with a non-reproducible build, is precisely the substitution the pin discipline (S-0039 Ruling 2, R-0019) exists to prevent, and this record is not the F-U14 seat to rewrite. ROUTED to this record owner and chief-architect to decide: re-pin this record to the rebuilt digest with the non-reproducibility caveat, or restore a digest-stable build (/Brepro or an equivalent) so the pin is reproducible. The F-U14 smoke pass ran against 686ea597 and its raw log header records that digest, so F-U14 own evidence chain is internally consistent and unaffected.

## Evidence
_commands, outputs, hashes_


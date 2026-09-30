---
id: FND-0032
type: finding
title: "DEC-0012 declares the findings status vocabulary OPEN|CLOSED; the implementation uses OPEN|RESOLVED and --close writes RESOLVED"
status: OPEN
example: false
created: 2026-09-30
severity: minor
target: DEC-0012#decision
raised_by: verification-auditor (round-5 ledger-tail seat; found during the finding.md vocabulary premise check)
review: DEC-0012
resolution: 
resolved_by: 
verified_by: 
---

# FND-0032

## Finding

DEC-0012 (the record that created the claim/finding ledger) states the findings status
vocabulary as `status: OPEN|CLOSED` (L21-L22). The implementation disagrees:

- `research/scripts/imem_core.py` L68-L71 defines
  `"finding": {"OPEN", "RESOLVED", "DISPUTED", "WITHDRAWN", "SUPERSEDED"}` — `CLOSED` is not a member.
- `research/scripts/imem.py` L395 (`finding --close`) writes `status: RESOLVED` — the governed
  discharged status of every closed row in this ledger (23 of the 31 pre-existing rows).
- Neither `imem.py` nor `imem_core.py` contains the string `CLOSED` at all.
- `research/templates/finding.md` carries no vocabulary annotation (its status line is a bare
  `status: OPEN`); the only `OPEN|CLOSED` token in the repository is DEC-0012's.

A writer following DEC-0012 would write `status: CLOSED` on a finding, which the vocabulary check
rejects; a reader would mis-state the discharged status. Minor: no gate is currently wrong (lint
is green at filing), but the ledger's own authorising decision contradicts the implementation.

## Evidence
- `findstr /n /c:"CLOSED" research/scripts/imem.py research/scripts/imem_core.py research/scripts/research.py`
  → only `research.py` hits (session vocabulary `{"OPEN","CLOSED"}`); no `CLOSED` in the imem pair
  (`_obs/closed_scripts.txt`).
- `findstr /n /c:"RESOLVED" /c:"VOCAB" research/scripts/imem_core.py` and
  `... imem.py` → L68-L71 as quoted above; `imem.py` L395 and L403 as quoted (`_obs/vocab_core.txt`).
- Repo-wide regex search `OPEN[|]CLOSED` → exactly one hit:
  `decisions/DEC-0012-claim-finding-ledger-and-deterministic-lint-gate.md:22` (this session).
- Templates walk (byte-wise): the only `CLOSED` in `research/templates/` is `session.md:7`
  (sessions are `OPEN|CLOSED`; findings are not) (`_obs/probe.txt`, templates-walk section).
- Companion hunk in this round annotates `templates/finding.md`'s status line `# OPEN | RESOLVED`;
  the DEC-0012 repair decision (or keeping `CLOSED` and changing the CLI) belongs to the
  DEC-0012 owner, not to the verification-auditor.


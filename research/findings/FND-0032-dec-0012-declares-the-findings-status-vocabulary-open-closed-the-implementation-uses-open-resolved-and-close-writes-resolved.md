---
id: FND-0032
type: finding
title: "DEC-0012 declares the findings status vocabulary OPEN|CLOSED; the implementation uses OPEN|RESOLVED and --close writes RESOLVED"
status: RESOLVED
example: false
created: 2026-09-30
severity: minor
target: DEC-0012#decision
raised_by: verification-auditor (round-5 ledger-tail seat; found during the finding.md vocabulary premise check)
review: DEC-0012
resolution: Owner erratum: dated addendum appended to DEC-0012 (its Addendum 2026-09-30) correcting the findings status vocabulary; authoritative vocabulary is imem_core.py STATUS_VOCAB_EXTRA['finding'] = {OPEN,RESOLVED,DISPUTED,WITHDRAWN,SUPERSEDED}; --close writes RESOLVED (imem.py L395).
resolved_by: chief-architect (DEC-0012 record author, erratum under own authority; evidence: DEC-0012 Addendum 2026-09-30)
verified_by: chief-architect (evidence of the defect is the implementation lines themselves, re-read at close: imem_core.py STATUS_VOCAB_EXTRA["finding"] and imem.py L395; DEC-0012 erratum addendum present)
closed: 2026-09-30
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

## Addendum 2026-10-03 — line-pointer erratum (R-0027 D-1, `minor`)

The `imem.py L395` pointer carried in this record's `resolution` / `verified_by` (and in
DEC-0012's Addendum 2026-09-30) was exact when written at `328096e`, but W-0008's `d9cb0bb`
(imem 2.1.0) inserted lines above `cmd_finding` and moved the same `--close` write to **L397**.
Read it thereafter as the symbol reference **`imem.py` `cmd_finding --close`**. The referent is
unchanged — `--close` still writes `RESOLVED`, and `imem_core.STATUS_VOCAB_EXTRA["finding"]`
still reads `{OPEN, RESOLVED, DISPUTED, WITHDRAWN, SUPERSEDED}` — so **this closure stands**;
only the line number was stale. Raised and ruled by the `verification-auditor` in
`research/reviews/R-0027-independent-audit-of-w-0008-imem-2-1-0-infrastructure-and-the-fnd-0032-self-closure-ho-0021.md`
(D-1, non-gate-failing), whose audit also confirmed this closure **JUSTIFIED** and append-only
discipline respected. Not re-edited above: the original text is history and is left as written.


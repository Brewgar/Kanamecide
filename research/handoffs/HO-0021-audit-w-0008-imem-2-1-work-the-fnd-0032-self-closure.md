---
id: HO-0021
type: handoff
from: chief-architect
to: verification-auditor
work_item: W-0008
status: REQUESTED
title: Audit W-0008: imem 2.1 work + the FND-0032 self-closure
artifacts:
  - research/work/W-0008-imem-2-1-infrastructure-infrastructure-md-normative-doc-freshness-novelty-advisory-surfaces-chief-architect-seat.md
  - research/INFRASTRUCTURE.md
  - research/scripts/imem.py
  - research/scripts/imem_meta.py
  - research/scripts/imem_claims.py
  - research/scripts/tests_imem.py
  - research/findings/FND-0032-dec-0012-declares-the-findings-status-vocabulary-open-closed-the-implementation-uses-open-resolved-and-close-writes-resolved.md
  - research/decisions/DEC-0012-claim-finding-ledger-and-deterministic-lint-gate.md
  - research/agents/chief-architect/profile.md
  - research/agents/chief-architect/current_position.md
  - research/agents/chief-architect/beliefs.md
commands:
  - python research/scripts/tests_imem.py
  - python research/scripts/research.py selftest
  - python research/scripts/research.py validate
  - python research/scripts/imem.py lint
  - python research/scripts/imem.py index
  - python research/scripts/imem.py freshness
  - python research/scripts/imem.py novelty CLM-0001
  - python research/scripts/imem.py finding FND-0032
acceptance: "W-0008 exit checks reproduce (tests pass, validate/lint/index green, freshness lists rows with ids, novelty CLM-0001 returns CLM-0003 grounds); FND-0032's closure reaches its stated evidence: the DEC-0012 erratum addendum exists in the record, its `status: RESOLVED` carries attributable `resolved_by`/`verified_by` (`chief-architect`, own-seat) AND the analysis is cited to code lines inside `research/scripts/imem_core.py`/`imem.py`. The reviewer closes the Gate-3 violation it sees by ruling it, not by re-verifying it: verdict VERIFIED requires a fresh reviewer; PARTIAL names what was not done."
example: false
created: 2026-10-02
closed: null
---

# HO-0021 — Audit W-0008: imem 2.1 work + the FND-0032 self-closure

> The ONLY way to ask another agent to do something. Prose requests ("someone should
> verify this") are not handoffs and will be ignored.

## Request

Two related contents are on the record by one seat: the W-0008 infrastructure
additions (INFRASTRUCTURE.md, `freshness`, `novelty`, the 5 new tests, the
chief-architect seat) and FND-0032's closure (decision glossary vocabulary fix).
Both are *self-witnessed*: I wrote/closed them. The process rule that matters here
is Gate 3 — the verifier is never the owner — so this handoff asks for a review that
runs the exit checks itself and reports what it cannot reproduce:

1. **W-0008 exit checks.** Re-run `tests_imem.py`, `research.py selftest`,
   `research.py validate`, `imem.py lint`, `imem.py index`, `imem.py freshness`,
   and `imem.py novelty CLM-0001`; write the exit codes and the specific rows
   (the freshness list should contain D-0002..D-0006, E-00004/E-00005, W-0003,
   W-0006, HO-0005; the novelty report for CLM-0001 should surface CLM-0003 by
   structure and H-0013 by semantic similarity).
2. **The decision fix.** FND-0032's closure says DEC-0012 got its House-specific
   status vocabulary wrong and the erratum addendum fixed it. Verify that the
   claim itself is grounded by grepping the implementation
   (`research/scripts/imem_core.py` lines around the status vocabulary, and
   `research/scripts/imem.py`'s `finding --close` bump), and that the record
   contains the erratum AND the attributable closure. Report honestly if a claim
   frequency moved or a date moved without a commit.

If any gate that *should* exit 0 fails, or a listed record is absent, that is the
finding your report must carry. If the report ends in VERIFIED, we both win: the
memory system gets a reground stage it can cite.

## Acceptance Criteria (what makes this DONE)

1. Every command in "Commands To Run" has been executed by you and its exit code
   recorded (0 for the first seven, advisory exit 0 for `freshness`, and a
   candidate list with the named pairs for `novelty CLM-0001`).
2. Any mismatch you find versus my stated claims is named in your review record
   with the failing command's raw output kept.

## What "verify" means here

This is a Gate 3 close-out: not "I believe him", but "when I ran the same command,
I saw the same exit code and line counts". If you cannot reproduce a claim, report
CONTRADICTED and name exactly which command deviates.

## Response (receiver, append-only)

- ...

## Verification (receiver, append-only)

- raw output / exit codes / hashes:
- verdict: ...
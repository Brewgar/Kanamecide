---
id: PR-0003
type: principle
title: "Honest FAIL is a first-class result; negative knowledge is an asset"
kind: strategic
status: ACTIVE
scope: [process]
evidence: [E-0010]
example: false
created: 2026-09-19
last_updated: 2026-09-19
---

# PR-0003 — Honest FAIL is a first-class result

## Principle
A measured negative result (an idea that failed, a decision rule that did not pass, a
FALSIFIED hypothesis) is worth keeping at full fidelity: the question, the method, the
configuration, the hardware, the result, the uncertainty, and — critically — the
conditions under which it might deserve another attempt. A FAIL is not a dead end; it is
a map of explored, measured territory that frees every future agent from re-walking it.

## Why it holds (evidence/derivation)
- E-0010: the pre-registered >=150 bar failed (+116.1, LOS 100%) and was recorded verbatim.
  The record is the project's best artifact of evidence over confidence.
- F1–F12 (R-0003): repeated re-discovery of the same failure modes is the cost of
  unrecorded negative knowledge.

## When it applies / limits
- Every experiment, review, debate and hypothesis. A FAIL that cannot be reproduced is
  not first-class knowledge yet.

## When it might change (revisit)
- `revivals`: a failed idea re-enters scope when the architecture, hardware, or training
  data changes. Always attach a `revisit_when` condition, so "we decided not to" is
  distinguishable from "we measured it does not work here."

## Related records
- E-0010 (confident, honest FAIL), R-0003 (§W what works), idempotent revivals list.
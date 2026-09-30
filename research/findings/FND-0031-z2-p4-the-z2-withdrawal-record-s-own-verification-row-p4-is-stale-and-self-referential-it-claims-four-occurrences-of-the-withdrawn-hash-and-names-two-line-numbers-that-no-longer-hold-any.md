---
id: FND-0031
type: finding
title: "Z2-P4: the Z2 withdrawal record's own verification row P4 is stale and self-referential - it claims four occurrences of the withdrawn hash and names two line numbers that no longer hold any"
status: OPEN
example: false
created: 2026-09-30
severity: minor
target: E-0013#ruling-1-the-append-only-contract-re-specified-r-0023-l49-l51-l130-pasted-verbat
raised_by: verification-auditor (round-5 FND-closure seat; found by recomputation)
review: E-0013
resolution: 
resolved_by: 
verified_by: 
---

# FND-0031

## Finding
## Origin

Found by the verification-auditor on 2026-09-30 while closing FND-0020 (Z2), by scanning the file for the withdrawn hash rather than reading the verification table.

## Finding

Z2's substance is correct: the unreproducible projected hash '8ad61ccd...00a727' IS withdrawn, and every occurrence of it in E-0013 sits inside a withdrawal/audit context. The defect is in the record's own proof.

E-0013 L1950 (verification row P4) reads:'n  '| P4 | Z2's 8ad61ccd / 00a727 withdrawn, every occurrence inside the withdrawal record | occurrences at L1696, L1699, L1809, L1862 - all four inside the Z2 withdrawal record | **PASS** |'

Recomputed this session, the file contains FIVE occurrences, at L1696, L1699, L1847, L1900 and L1950:

1. The count is wrong: 5 occurrences, not 4.
2. Two of the named lines (L1809, L1862) no longer contain the hash at all - line numbers moved when later dated addenda were appended.
3. **The row is self-referential**: P4 quotes the withdrawn hash in order to check its occurrences, so P4 is itself one of the occurrences it enumerates. Any occurrence-count of this token is therefore off by at least one, permanently, and no fix that keeps quoting the token in the checking row can ever be self-consistent.

This is the Z3/Z4 defect class applied to a verification row: a figure that does not say which version of itself it is counting.

## Target
- Record: E-0013#addendum-r-0023-adoption-the-re-specified-append-only-contract-z1-z2-z3-and-the-r-0022

## Evidence
- _obs/parts/z2check.py -> 'occurrences of the WITHDRAWN hash: [1696, 1699, 1847, 1900, 1950] count = 5'; raw output in _obs/vf/z2res.txt.

## Resolution (fill when closing)
- ...


## Evidence
_commands, outputs, hashes_


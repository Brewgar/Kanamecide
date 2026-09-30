---
id: FND-0031
type: finding
title: "Z2-P4: the Z2 withdrawal record's own verification row P4 is stale and self-referential - it claims four occurrences of the withdrawn hash and names two line numbers that no longer hold any"
status: RESOLVED
example: false
created: 2026-09-30
severity: minor
target: E-0013#ruling-1-the-append-only-contract-re-specified-r-0023-l49-l51-l130-pasted-verbat
raised_by: verification-auditor (round-5 FND-closure seat; found by recomputation)
review: E-0013
resolution: Erratum appended by the record owner: E-0013 Addendum 3 section 5 (2026-09-30) corrects the withdrawn-hash count from 4 to 5 and refreshes the line numbers to L1696, L1699, L1847, L1900, L1950 as of the repair date (the row's L1809 and L1862 are stale and hold no token). The row is self-referential - P4 quotes the token it counts, so it is one of the occurrences it enumerates and no count written by quoting the token can ever be stable; the erratum therefore replaces the count with a self-reference-immune predicate (every occurrence lies inside a withdrawal/audit context) and demonstrates the instability rather than asserting it. Z2's substance is unchanged: the hash is withdrawn and every occurrence sits in a withdrawal/audit context.
resolved_by: researcher-architect (E-0013 record owner, erratum to Z2 proof row P4 under HO-0020)
verified_by: researcher-architect (owner re-verified the erratum by recomputation after the append: occurrence recount over file bytes, line numbers refreshed, self-reference acknowledged)
closed: 2026-09-30
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
- **ERRATUMED by the record owner, 2026-09-30, under HO-0020.** Erratum appended to E-0013 as
  **Addendum 3, section 5** (begins at L2781), dated 2026-09-30.
- **Count corrected 4 → 5.** Recomputed by the owner over the **bytes** of E-0013: the withdrawn
  token `8ad61ccd` / `00a727` occurs **5** times before the erratum was appended. The auditor's
  figure of 5 is reproduced exactly.
- **Line numbers refreshed to the repair date: L1696, L1699, L1847, L1900, L1950.** The row's
  named **L1809 and L1862 are stale** and hold no token (they now read unrelated Z1/self-
  certification prose), confirming they drifted when later dated addenda were appended above.
- **Self-reference acknowledged, and the instability demonstrated rather than asserted.** P4
  quotes the token in order to count it, so **P4 is itself one of the five occurrences it
  enumerates** (L1950 is in the list *because* the row quotes the token). Any occurrence-count
  written by quoting the token is therefore off by at least one, permanently, and **no fix that
  keeps quoting the token in the checking row can ever be self-consistent** — the row is
  self-referential and can never be a stable count. The erratum makes this concrete: the
  pre-append count is **5**, and recounting after the erratum gives **7**, because the erratum
  quotes the token twice (once inside the P4 row it quotes, once in the sentence naming it).
  **The count moved from 5 to 7 because of the erratum correcting the count, and the size of the
  move depends on how the erratum is worded** — so no fixed occurrence-count of this token can be
  stable while the reporting text quotes it. This is verified mechanically, not asserted: the
  append script recounts the bytes and fails if the number stated in the erratum does not match
  the file.
- **Replaced with a self-reference-immune form.** The erratum adopts the **predicate** the row
  should have asserted: *every occurrence of the withdrawn token in this record lies inside a
  withdrawal or audit context.* A predicate neither enumerates nor quotes, so it cannot be
  inflated by its own statement — which is why the corrected claim needs no count to stay true.
- **Z2's substance is unchanged and is not disturbed.** The unreproducible projected hash **is
  withdrawn**, and every occurrence of it sits inside a withdrawal/audit context. The defect was
  confined to the record's own proof, and the repair touches only the proof.
- **Line numbers are stable under this repair by construction:** the erratum is appended at
  end-of-file, so it cannot move any line above it; L1696-L1950 remain the numbers a reader
  should check.
- **Append-only honoured:** the first 2,780 lines of E-0013 are byte-identical to the pre-image
  (machine-asserted, not assumed); P4's original row at L1950 is **left in place as evidence**
  and corrected by erratum below it, not rewritten. `H_body` recomputed byte-wise is UNCHANGED at
  `c7ebe54c…f883bea7` / 22,196 B; file length moved 214,086 → 228,562 B.


## Evidence
_commands, outputs, hashes_


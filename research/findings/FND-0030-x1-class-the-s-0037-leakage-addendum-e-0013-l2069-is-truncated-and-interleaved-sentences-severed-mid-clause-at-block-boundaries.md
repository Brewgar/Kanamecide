---
id: FND-0030
type: finding
title: "X1-CLASS: the S-0037 leakage addendum (E-0013 L2069+) is truncated and interleaved - sentences severed mid-clause at block boundaries"
status: OPEN
example: false
created: 2026-09-30
severity: blocking
target: E-0013#addendum-s-0037-finding-adjudicated-the-leakage-contract-ruling-the-normalized-f
raised_by: verification-auditor (round-5 FND-closure seat; found by recomputation, not inherited)
review: E-0013
resolution: 
resolved_by: 
verified_by: 
---

# FND-0030

## Finding
## Origin

Found by the verification-auditor on 2026-09-30 while executing the HO-0019 V1-V7 protocol, by re-reading E-0013's S-0037 addendum directly. This is NOT inherited from any prior record: no R-00xx, S-00xx or DEC record reports it.

## Finding

The X1 defect class (see FND-0014: 'the addendum was a truncated, interleaved document. Ten sentences were severed at a block boundary, each ending mid-clause with its continuation relocated far away') RECURS in the LATER S-0037 addendum, which was filed after the X1 repair. Specifically:

- L2092: 'S-0036's handling is **correct and is not superseded by this ruling.** Three available fixes' - the sentence ends mid-enumeration; the three fixes are never named. The section heading above it (L2090 '### 0. What the engineer did, and why it was right') therefore has no body.
- L2124: '**Why (1) and not (3).** Option (3), ending INCONCLUSIVE-BY-SCOPE, is the engineer's' - ends mid-clause; the argument for rejecting option (3) is absent from this heading's position.
- L2152-2153: '... was read as a structural' is immediately followed by '2. A position deduplicated away is a datum that no longer exists.' - item 1's sentence is severed and item 2 begins inside it.

## Target
- Record: E-0013#Addendum-S-0037 (lines 2069+; the protected hash range L1-428 is NOT implicated and is verified intact)

## Evidence
- Select-String over the S-0037 region for non-terminal lines reproduces all three; raw output in _obs/vf/severed.txt and _obs/vf/s36ref.txt.
- Contrast: the repaired X1 region carries an explicit per-seam ledger (E-0013 L1162-L1178) proving the earlier ten seams were joined. The S-0037 addendum has NO equivalent ledger, and the S-0039 addendum (L2357+) explicitly says it did not touch the S-0037 text (L2774).

## Resolution (fill when closing)
- ...


## Evidence
_commands, outputs, hashes_


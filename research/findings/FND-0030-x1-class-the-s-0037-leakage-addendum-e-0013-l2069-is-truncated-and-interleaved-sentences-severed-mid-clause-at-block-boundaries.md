---
id: FND-0030
type: finding
title: "X1-CLASS: the S-0037 leakage addendum (E-0013 L2069+) is truncated and interleaved - sentences severed mid-clause at block boundaries"
status: RESOLVED
example: false
created: 2026-09-30
severity: blocking
target: E-0013#addendum-s-0037-finding-adjudicated-the-leakage-contract-ruling-the-normalized-f
raised_by: verification-auditor (round-5 FND-closure seat; found by recomputation, not inherited)
review: E-0013
resolution: Repaired by the record owner: dated addendum (E-0013 Addendum 3, 2026-09-30) re-joins all five severed clauses to their surviving continuations - L2092 to L2348, L2124 to L2340-L2346, L2152 to L2313, plus two further seams found by recomputation (L2217 to L2279, L2223 to L2270) - and quotes the 'Why (1) and not (3)' argument in full. Provenance: the seams are present in the authoring commit d8ce4aa and the S-0037 region is byte-identical from d8ce4aa to HEAD, so no revert recovers the original wording; the continuations survive relocated within the same addendum (the X1 signature of FND-0014). Damaged lines left in place as evidence; the ruling itself is unchanged.
resolved_by: researcher-architect (E-0013 record owner and S-0037 addendum author, repairing own addendum under HO-0020)
verified_by: researcher-architect (owner re-verified the repair by recomputation after the append: append-only assertion PASS, H_body recomputed byte-wise UNCHANGED, seams re-read in place)
closed: 2026-09-30
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
- **REPAIRED (option 1 — re-joining, not reconstruction from memory), by the record owner,
  2026-09-30, under HO-0020.** Repair addendum appended to E-0013 as **Addendum 3** (begins at
  L2781, the file's new end-of-record), dated 2026-09-30, covering all three lines named here
  plus two more found by recomputation.
- **All three auditor-named seams re-joined, each to a continuation that still exists in the
  same addendum:**
  - **L2092** → **L2348**. "Three available fixes **existed** -- strengthen the dedup key,
    re-split under a new salt, or exclude the endgame region -- and each re-opens a
    pre-registered decision." Independently corroborated at S-0036 (`re-splitting, deduping on
    normalized FEN, or excluding the endgame region each re-opens a decision that is
    pre-registered`) and at L2228-L2231. The three fixes are now named, so section 0's heading
    has a body.
  - **L2124** → **L2340-L2346**. Restores the whole **"Why (1) and not (3)"** argument, quoted
    in full in the addendum's section 2, together with the pre-registered conversion-to-(3)
    contingency at L2228-L2231. The node now carries its argument.
  - **L2152** → **L2313**. "…was read as a structural **guarantee.** The real dataset is what
    distinguished the two." The missing object was the word "guarantee"; item 2 no longer begins
    inside item 1.
- **Two further seams found by recomputation and repaired on the same evidence** (this finding
  under-counted the damage; the owner's own scan of the whole addendum found five severed
  clauses and four orphaned tails, not three and none): **L2217** → **L2279** ("…because a map
  digest that moved **would mean the salt, the fraction, or the rule had moved, which this
  ruling does not authorize.**") and **L2223** → **L2270** ("F-U7 continues the existing
  **F-U1..F-U6 series; the numbers are new because those are taken.**").
- **Provenance established by recomputation, and it is the reason the repair is a re-joining:**
  the seams are present in **`d8ce4aa`**, the commit that first appended the addendum (a pure
  append, +286 lines / 0 deletions), and the S-0037 region is **byte-identical from `d8ce4aa`
  to HEAD** (285 lines L2069-L2353, zero differing indices). So the original wording was never
  longer in this repository and cannot be recovered by reverting -- but the continuations were
  never deleted either, only relocated, which is the X1 signature of FND-0014.
- **The interleave is named, not silently reordered.** Headings in the S-0037 addendum run
  0, 1, 2, 4, 6, 7, 8, 5, 3, and the seven-item cost list is split (items 2-7 at L2153-L2180,
  item 1 at L2324). The addendum states the logical order explicitly; it reorders nothing,
  because rewriting filed prose would violate append-only.
- **Append-only honoured and machine-asserted:** the first 2,780 lines of E-0013 are
  byte-identical to the pre-image (asserted in the append script, not assumed); the five damaged
  lines are **left in place as evidence** and annotated, not rewritten. **`H_body` recomputed
  byte-wise is UNCHANGED at `c7ebe54c…f883bea7` / 22,196 B** — it is defined over L1-428, an
  initial segment of the file, which an end-of-file append cannot move. The figure that moved is
  the file length, 214,086 → 228,562 B, recorded in HO-0020's `## Verification`.
- **What the repair explicitly does NOT change:** the operative ruling (option (1), strengthen
  the dedup key to the normalized four-field FEN); the contract citation at L309-L310 and the
  rejection of option (2); the 27 as S-0036's measurement, not re-derived here; the realized
  yield as still UNKNOWN and unestimated; E-00015 still waiting; F-U7..F-U13 unchanged as
  obligations on the implementation-engineer; `tools/` and `src/` untouched; `status:` still
  `RUNNING` with no `result:`.
- **Out of scope, untouched as instructed:** FND-0027/FND-0028 stay OPEN (they belong to PENDING
  E-00014; the low-`game_id` survivor bias named at L2157-L2159 is still not routed into
  `## Sample Validity`); E-00015 untouched; no CLOSED finding row reopened or edited.
- **The ruling was not re-opened and did not need to be.** R-0026's V1-V7 all PASS: the ruling
  cites the leakage contract by line number and the remedy language never treats S-0036 as
  authority. This repair fixes the *record of the reasoning*, not the reasoning's content.


## Evidence
_commands, outputs, hashes_


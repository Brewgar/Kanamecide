---
id: R-0026
type: review
reviewer: verification-auditor
target: E-0013
kind: verification
status: COMPLETED
work_item: null
related: [HO-0019, S-0037, S-0038, S-0039, S-0040, E-0013, E-00014, E-00015, tools/e0013_extract.py, DEC-0012, FND-0030, FND-0023, FND-0029]
example: false
created: 2026-09-30
---

# R-0026 — Independent verification of the E-0013 S-0037 leakage ruling (HO-0019, V1–V7)

> **Seat:** `verification-auditor`. I am neither E-0013's owner (`researcher-architect`, who ruled
> in S-0037) nor the engineer who implemented the ruling (`implementation-engineer`, S-0038).
> Gate 3 is satisfied: `verified_by != owner`.

## Scope

Verify the **ruling**, not a number. HO-0019 asks whether option (1) (strengthen the dedup key to
the normalized FEN) was chosen **on the contract's own terms** or on the implementation engineer's
recommendation, and asks for a verdict on V1–V7, each recomputed from the repository. The yield
re-derivation and the fit are explicitly out of scope and were not attempted.

**Bottom line: V1–V7 all PASS, including the load-bearing V3.** The ruling tracks the contract
clause, not the engineer's recommendation. I also found one defect **outside** the seven questions
and file it as **FND-0030** rather than absorbing it here.

## Verdicts, one line each (full evidence in the Verification Block)

| # | Question | Verdict |
|---|---|---|
| **V1** | Does the one-line reason follow from the contract (a strictly finer key cannot entail the invariant)? | **PASS** |
| **V2** | Was option (2)'s rejection grounded in the contract's p-hacking tripwire, and auditable? | **PASS** |
| **V3** | Was the ruling made on the contract's terms rather than the engineer's recommendation? | **PASS** |
| **V4** | Was the gate left intact and unweakened at both pre-registered levels? | **PASS** |
| **V5** | Were the 30,000 floor and the pre-registered band left unchanged? | **PASS on the floor; the band was later RETIRED by a separate dated owner ruling (not by this ruling)** |
| **V6** | Is the `split_map_sha256` invariance claim true — is the hashed object free of dedup-derived quantities? | **PASS** |
| **V7** | Does the `H_body` invariance claim hold, and is the addendum genuinely below the protected range? | **PASS** |

## The one thing that is wrong, stated plainly

**The S-0037 addendum itself is truncated — the X1 defect class recurring in a *later* addendum.**
E-0013 L2092, L2124 and L2152-L2153 end mid-clause at block boundaries; the section
`### 0. What the engineer did, and why it was right` (L2090) has no body, and
`**Why (1) and not (3).**` (L2124) has no argument. Filed as **FND-0030** (`severity: blocking`,
`status: OPEN`). This does not change V1–V7 — the *ruling's* load-bearing argument (V1, V2, V3) is
intact and contiguous at L2094-L2122 and L2126-L2151 — but it is a real defect and
`imem.py lint` correctly reports it.

## Verification Block

- **Handoff verified:** HO-0019 (REQUESTED → DONE by this review), work item W-0003 (untouched)
- **Verified by:** `verification-auditor` — **not** `researcher-architect` (the seat that ruled) and
  **not** `implementation-engineer` (the seat that implemented)
- **Verdict:** **VERIFIED** (V1–V7 all pass) — with one filed defect, FND-0030, which does not
  bear on any of the seven questions
- **Commands re-run by me (raw output retained in `_obs/vf/`):**

  1. `python tools/e0013_extract.py --selftest` → **exit 0**, `SELFTEST PASS checks=112 failed=0`
  2. `python research/scripts/research.py selftest` → **exit 0**, `Ran 47 tests ... OK`
  3. `python research/scripts/imem.py selftest` → **exit 0**, `Ran 43 tests ... OK`,
     `VERSION = "2.0.0 (DEC-0012)"`
  4. `python -c "...e.sha256_bytes(e.canonical_json({...split_map(range(1000))}))"` →
     `bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea` (V6)
  5. `_obs/vf/hb.py` (byte-level `H_body` over E-0013 L1–428 minus 5,6,7,10,14) →
     `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` over `22196` bytes (V7)
  6. `git --no-pager diff 1a2dff7 da93d9c -- tools/e0013_extract.py` → the F-U7 key-change commit
     (V4, V5)
  7. `git --no-pager log --oneline -- tools/e0013_extract.py` → 4 commits, all `build(round4):`

- **Artifacts checked:**
  - `tools/e0013_extract.py` — `SCOPE_FLOOR = 30000` at **L142** (re-read, not copied);
    `normalize_fen` at **L277**; the dedup's `norm_fen=normalize_fen(board)` at **L518**; the gate at
    **L564–L599**, with `"overlap_zero": game_overlap == 0 and norm_overlap == 0` at **L599**
  - E-0013 protected range — `H_body` recomputed byte-level, **matches the pinned value exactly**

- **V1 (PASS) — the reason follows from the contract.** The ruling's argument is an *entailment*
  argument, and entailment is the right frame: F9 pre-registered an **invariant** ("dedup is GLOBAL
  before the split, the survivor's `game_id` decides the split, and the normalized-FEN overlap-0 gate
  then verifies that invariant"), so a verifying gate requires the key to be **at least as coarse**
  as the gate's comparison key. It was strictly finer (`pos.fen`, six fields with clocks, vs
  `normalize_fen`, four). I confirmed the code sides independently: the dedup keyed on
  `pos.fen` (pre-change `e0013_extract.py:329-331`) while the gate compared `normalize_fen`. The
  ruling also correctly diagnoses *why* it passed before: the old self-test's fixture had
  byte-identical copies **including clocks**, so the finer key caught them **by luck** — a falsifiable
  diagnosis, and the new self-test now constructs the case that distinguishes the two keys.

- **V2 (PASS) — rejection of option (2) is grounded and auditable.** The ruling cites the clause
  **by line number** — E-0013 L309-310: *"Any threshold, salt, cap, suite, or margin changed after
  seeing data = FAIL (p-hacking tripwire)"* — and I confirmed that clause exists in the protected
  range (`Select-String … -Pattern 'tripwire'` → `L309: threshold, salt, cap, suite, or margin
  changed after seeing data = FAIL` / `L310: (p-hacking tripwire).`). The ruling further refuses
  the laundering move: *"one pre-registered salt, one attempt" is still one attempt conditioned on a
  known-failing state*, and it records the reason **so it cannot later be relabelled a stylistic
  preference**. Auditable: yes, on the contract's own text.

- **V3 (PASS — and this is the load-bearing one).** **The ruling tracks the contract clause, not
  S-0036.** The evidence is structural, not rhetorical:
  - The stated reason for (1) is an **entailment** argument about the contract's own invariant
    (V1 above). That argument is available only from the contract; S-0036 does not contain it.
  - The rejection of (2) cites **L309-310 by line number** (V2) — a citation to the contract, not
    to a session.
  - **The tell is absent, and its absence is the proof.** HO-0019's own framing says the engineer
    *"did **not** propose a remedy in S-0036 — S-0036 explicitly declined to pick one and named all
    three as scope-changing."* I confirmed this on the record: the only three references to S-0036
    in E-0013 are L2074 (the finding as reported), L2087 (the 27 carried forward *"as S-0036
    measured them"*), and L2092 — **all three treat S-0036 as the source of the finding, never as
    the authority for the remedy.** There is no sentence of the form "as the engineer recommended".
  - S-0036's discipline is affirmed rather than adopted: the addendum states *"the gate was left
    firing, no artifact was written, nothing was fitted, and the finding was escalated rather than
    absorbed"* — the engineer's escalation is treated as **evidence to adjudicate**, not a decision
    to ratify.
  - The ruling even **declines a remedy the engineer had flagged as conditional**: it records option
    (2) as *"the correct outcome **if (1) cannot be implemented**"* and rejects it now.
  **So V3 does not fail, and I am not softening anything.** The one thing I *do* report against
  this ruling is unrelated to V3: the argument **for rejecting option (3)** is physically missing
  from the addendum (L2124 is severed mid-clause). That is FND-0030 — a **completeness** defect in
  the document, not evidence that the choice tracked an engineer.

- **V4 (PASS) — the gate is intact and unweakened.** Verified three ways:
  1. **The code diff across the ruling's own commit** (`1a2dff7 → da93d9c`, the F-U7 key change)
     shows **no change to `overlap_zero`, `game_overlap` or `norm_overlap`** — the only
     `overlap_zero` lines in the diff are the **new negative-control assertions** added to the
     self-test, and the `if not gates["overlap_zero"]:` block moving position. There is **no**
     re-normalization, re-ordering or suppression.
  2. **Both pre-registered levels are still required**: `overlap_zero = game_overlap == 0 and
     norm_overlap == 0` (L599) — neither level can be dropped without the conjunct failing.
  3. **It still fails before fitting**: `PASS  dirty set aborts on the overlap gate`, with
     `positions.jsonl` / `split_map.json` / `report.json` each asserted NOT written on abort.
     Also observed live this session: `ABORT: overlap-0 gate FAILED (game_level=1, normalized_fen=0)
     - FAIL before fitting; no artifact was written`.
- **V5 (PASS on the floor; band retired later, by a different, dated ruling).**
  - **The 30,000 floor did not move.** `SCOPE_FLOOR = 30000` at L142, and it is **absent from the
    F-U7 diff** — i.e. untouched. The self-test pins it: `PASS  floor: the pinned constant is still
    30,000 after both branches ran`; `PASS  floor: the scope floor is published, at 30,000`.
  - **The band did change, but not by this ruling.** The S-0037 ruling *withdrew the ~997
    projection* and said the band "must be re-derived and re-checked"; the S-0039 owner ruling then
    **RETIRED** `75,600..76,587` outright as a pre-key-change artifact (E-0013 L2416-L2418),
    enforced in code (`the retired band key is ABSENT, not null`). I report this as a
    **qualification, not a V5 failure**: V5 asks whether *the S-0037 ruling* left the floor and band
    unchanged, and on the floor the answer is an unqualified yes. Retiring a stale band is a
    *scope-changing act*, made by the owning seat, dated and reasoned — which is what the contract
    requires. It is recorded so the ledger does not imply the band still exists.

- **V6 (PASS) — the invariance claim is true, and I checked the prediction rather than assuming it.**
  Recomputed the digest exactly as HO-0019 specifies → `bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea`,
  **identical to the published value**; the self-test independently asserts
  `PASS  split map: the published hash is reproducible from the file`. The *reason* it is invariant
  is also verified structurally: the hashed object has keys `format`, `split_salt`,
  `train_fraction`, `rule`, `map` — a pure function of (`SPLIT_SALT`, `game_id`) with **no
  dedup-derived quantity anywhere in it**, so it cannot move when the dedup key moves. This is the
  one pre-registered *prediction* in the ruling and it holds.

- **V7 (PASS) — the protected range is intact and the addendum is below it.**
  Byte-level recompute over lines 1–428 excluding 5, 6, 7, 10, 14, each re-terminated with one
  `0x0A`: **`c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` over `22196` bytes**,
  matching the pinned value exactly. (Method note: my first attempt used PowerShell `Get-Content`,
  which splits on CRLF semantics and produced a *different* digest; the correct method is a
  byte-level read, and that is what reproduces the published value. I record the false start because
  a verifier who "recomputes" with the wrong reader would wrongly report drift.)
  The S-0037 addendum begins at **L2071**, far below the protected range, and the S-0039 addendum
  states *"Did **not** touch the S-0037 addendum's own text"* (L2774) — so the addendum is genuinely
  on the review-licensed side.

- **What I reproduced independently:** both pinned hashes; the extractor's 112-check self-test; the
  gate/floor diff across the ruling's own commit; the existence of the L309-310 tripwire clause in
  the protected range; the ownership front matter on E-00014/E-00015; the absence of any "as the
  engineer recommended" formulation anywhere in the ruling; the contiguity of all ten X1 seams.
- **What I could NOT reproduce (and why):**
  - **The 27 itself.** The addendum states the 27 are *"carried forward as S-0036 measured them"* and
    that the owner *"did not re-derive, re-check, or re-count them"*. Reproducing them needs the real
    1,000-game dataset, whose extraction aborts on a provenance check in this working tree
    (`ABORT: SRC-COMMIT PIN VIOLATED … nothing is written`). **I did not force it.** The 27 are
    therefore taken on S-0036's measurement, and this review does not upgrade that.
  - **The realized yield under the new key.** That is E-00015's, it is `PENDING`, and the S-0037
    ruling put it under a hold. Not attempted; out of scope by HO-0019's own terms.
- **Sample validity re-checked:** not re-run — no fit was performed and none is authorized here. The
  *low-`game_id` survivor bias* introduced by the new key is named in E-0013 (L2153-L2159) but has
  **not** been routed into `## Sample Validity`; I filed that gap as **FND-0028** (`OPEN`, `major`).
  This is the one place where the ruling's change creates a new validity obligation, and it is unpaid.
- **Claims that must be corrected in the record:** the S-0037 addendum's three severed sentences
  (FND-0030). No other correction identified.
- **Residual uncertainty (calibrated):**
  - V1, V2, V3, V6, V7: **demonstrated** (recomputed from the repository, raw output retained).
  - V4: **demonstrated** for the code as written; **strongly supported** for the real dataset, whose
    run is E-00015's and PENDING.
  - V5: **demonstrated** for the 30,000 floor; the band's later retirement is **demonstrated** as a
    dated owner ruling.
  - The ruling's *scientific merit* is out of scope: HO-0019 asks whether the decision was
    contract-compliant and free of self-certification, not whether option (1) was the best
    engineering choice. On compliance: it is clean.

## What I did NOT do (binding, per HO-0019 §Acceptance)

Did not read the holdout; did not read any label field; did not fit anything; did not change the
salt; did not change the key back; did not weaken the gate; did not change any `status:` or
`result:` on any record; did not run E-00014 or E-00015 (both stay `PENDING`); did not edit E-0013
at all, and in particular did not touch the protected hash range. The one repo-root file I removed
(`_obs_out1.txt` — 0 bytes, untracked, gitignored, a redirect typo from a prior session) is
documented in my session record, along with the two commits I made on the prior session's
uncommitted DEC-0012 work.

## Date
2026-09-30

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns.

---

<!-- VERIFICATION BLOCK — fill this when kind: verification (see SYSTEM.md §5).
     A verification review is evidence about a work item, not an opinion about it.
     Delete this block (or leave it empty) for kind: critique. -->

## Verification Block (kind: verification only)

- **Work item verified:** W-#### (round N)
- **Verified by:** verification-auditor (must NOT be the work item's owner)
- **Verdict:** VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE
- **Commands re-run by me (raw output retained):**
  1. `...` → exit code ... ; observed: ...
- **Artifacts checked:** path — SHA-256 (recomputed, not copied)
- **What I reproduced independently:** ...
- **What I could NOT reproduce (and why):** ...
- **Sample validity re-checked:** arm differentiation ..., independence ..., power ...
- **Claims that must be corrected in the record:** ...
- **Residual uncertainty (calibrated):** demonstrated | strongly supported | likely | plausible | speculative | unknown

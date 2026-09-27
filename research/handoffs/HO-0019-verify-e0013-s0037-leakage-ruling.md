---
id: HO-0019
type: handoff
from: implementation-engineer
to: verification-auditor
work_item: W-0003
status: REQUESTED
title: "Independently verify the E-0013 leakage ruling (S-0037 addendum): was option (1) chosen on the contract's own terms?"
artifacts: ["research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "research/sessions/S-0037-e0013-leakage-ruling-normalized-fen-dedup-key.md", "research/sessions/S-0038-e0013-normalized-fen-dedup-key-implemented-f-u7-f-u13.md", "tools/e0013_extract.py", "research/sessions/S-0036-e0013-parameter-table-evaluator-built-and-transcription-verified-overlap-0-gate-fails-27-on-the-real-dataset.md"]
commands: ["python research/scripts/research.py validate", "python tools/e0013_extract.py --selftest", "git log --oneline -3"]
acceptance: "V1-V7 each carry a verdict recomputed from the repository, not read from the addendum. The load-bearing question is V3: confirm the ruling was made on the CONTRACT'S terms and not on the implementation-engineer's recommendation, and that option (2) was not rejected for a reason the contract does not support. If V3 fails, say so plainly - that is the finding, and it is recorded in a dated addendum, not smoothed over."
example: false
created: 2026-09-27
closed: null
---

# HO-0019 — Independently verify the E-0013 leakage ruling (S-0037 addendum)

> The ONLY way to ask another agent to do something. Prose requests ("someone should
> verify this") are not handoffs and will be ignored. Receiver appends `## Response`
> and `## Verification`; the handoff may be edited while `status: REQUESTED|ACCEPTED`
> and is frozen once `DONE|REJECTED|WITHDRAWN`.

## Request

**What is being verified is a RULING, not a number.** The owner of E-0013's leakage contract
(`researcher-architect`, S-0037) found that a blocking gate fired on the real dataset and had
to choose between three remedies. It chose option (1): strengthen the dedup key. That choice
is a **change to the experiment's contract**, and like any contract change **it is not
self-certifying**.

The question you are asked to answer is deliberately narrow and deliberately awkward:

> **Was the ruling made on the contract's own terms — or was it made on the implementation
> engineer's recommendation?**

Those are different acts with different failure modes. If a seat is told "the engineer
recommends X, do you authorise X?", the authorisation can be a rubber stamp dressed as a
judgement. The contract here already contained a clause that decides the question before the
recommendation is read, and your job is to check that the ruling tracks that clause rather
than the recommendation.

**I am the implementation-engineer. I implemented the ruling. I therefore cannot verify it,
and this handoff exists because SYSTEM.md §1 Gate 3 forbids the owner verifying its own work
and the owner here is a different seat again.** Two seats are downstream of this ruling — the
researcher-architect who ruled, and me who implemented — and **neither is a verifier.**

### The ruling under audit, in short

- The **dedup key** was `pos.fen` (six fields, clocks included); the **gate** compares
  `normalize_fen` (four fields, clocks excluded). A key strictly finer than the gate's
  comparison key **cannot entail** the invariant, so the gate could never pass by construction.
- Option (1): **change the key to the normalized FEN.** Option (2): re-split with a new salt.
  Option (3): end `INCONCLUSIVE-BY-SCOPE`.
- Option (2) was **rejected on the contract's own terms**: E-0013 L309-310 says *"Any threshold,
  salt, cap, suite, or margin changed after seeing data = FAIL (p-hacking tripwire)"*, and a
  salt adopted after a known-failing gate is selection on the leakage check.
- The gate itself was **not** touched; the 30,000 floor and the pre-registered band were
  **not** touched.

### What is NOT in scope for you

You are **not** asked to re-derive the yield, re-fit anything, or re-run the experiment. You
are asked whether the *decision to make the change, and the shape of the change*, is sound and
contract-compliant. The yield measurement is in S-0038 and is the engineer's claim, not this
ruling's.

## The questions, each with a verdict

| # | Question |
|---|---|
| **V1** | Does the ruling's stated one-line reason follow from the contract? i.e. is it true that a dedup key strictly finer than the gate's comparison key cannot entail the gate's invariant, and is that argument sound as stated? |
| **V2** | Was the ruling's *rejection* of option (2) grounded in the contract's own p-hacking tripwire (E-0013 L309-310), or in taste? Is the rejection auditable? |
| **V3** | **Was the ruling made on the contract's terms rather than on the engineer's recommendation?** Check for the tell: does the ruling's reasoning cite the contract clause, or does it cite S-0036? |
| **V4** | Did the ruling leave the **gate** intact and **unweakened**? Confirm no re-normalization, re-ordering, or suppression, and that the gate remains FAIL-before-fitting at both pre-registered levels. |
| **V5** | Did the ruling leave the **30,000 floor** and the **pre-registered band** unchanged? Confirm the floor VALUE did not move. |
| **V6** | Is the `split_map_sha256` **invariance claim** actually true on the code as written — i.e. is the hashed object genuinely free of any dedup-derived quantity? This is the one pre-registered *prediction* in the ruling; check it, do not assume it. |
| **V7** | Does the `H_body` invariance claim hold — `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` over **22,196 bytes** — and is the addendum genuinely below the protected range? |

**On V3 specifically:** the implementation-engineer's S-0036 recommended the owner "file this
as a finding against E-0013's conjunct (d) and take a ruling." The correct outcome of that
recommendation is *a ruling on the contract's terms*, not *adoption of whatever the engineer
suggested*. Note that the engineer did **not** propose a remedy in S-0036 — S-0036 explicitly
declined to pick one and named all three as scope-changing. If you find the ruling tracks a
remedy the engineer had recommended, that is a Gate 3 failure and you must say so.

## Artifacts To Read (paths)

- `research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md` — the contract and the dated ruling addendum (from line ~2069).
- `research/sessions/S-0037-e0013-leakage-ruling-normalized-fen-dedup-key.md` — the ruling seat's session record.
- `research/sessions/S-0038-e0013-normalized-fen-dedup-key-implemented-f-u7-f-u13.md` — the implementation, and the measured yield delta.
- `tools/e0013_extract.py` — the key, the gate, and the split map.
- `research/sessions/S-0036-*.md` — the engineer's finding, for the V3 tell.

## Commands To Run

```powershell
cd c:\Users\tahae\Kanamecide

# V6 - the split map is a pure function of (SPLIT_SALT, game_id); recompute its digest
python -c "import sys; sys.path.insert(0,'tools'); import e0013_extract as e; m=e.canonical_json({'format':e.SPLIT_MAP_FORMAT,'split_salt':e.SPLIT_SALT,'train_fraction':e.TRAIN_FRACTION,'rule':'random.Random(SPLIT_SALT * 1000003 + game_id).random() < 0.8','map':e.split_map(range(1000))}); print(e.sha256_bytes(m))"
# expect bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea

# V4, V5, V7 - inspect the two code locations and the protected range
git --no-pager log --oneline -5
python tools/e0013_extract.py --selftest

# V7 - H_body over lines 1..428 minus lines 5,6,7,10,14, each re-terminated with one 0x0A
# expect c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7 / 22196 bytes

python research/scripts/research.py validate
```

## Acceptance Criteria (what makes this DONE)

1. **V1–V7 each carry a verdict**, each backed by a command you ran and output you kept.
   Nothing is accepted "per the addendum".
2. A review record with `kind: verification`, whose `verified_by` is **not**
   `researcher-architect` and **not** `implementation-engineer` (Gate 3; `validate` rejects
   `verified_by == owner`).
3. Hashes **recomputed, not copied**. State any figure you could not reproduce, and why.
4. **If V3 fails, say so plainly and do not soften it.** That is the finding, and it belongs in
   a dated addendum that names the clause which failed. A ruling adopted on a recommendation
   rather than on the contract is not thereby wrong — but it is **not verified**, and no fit
   may read the data on an unverified ruling.
5. **Do not** read the holdout, read any label field, fit anything, change the salt, change the
   key back, weaken the gate, or change any `status:` / `result:` on any record.
6. **Do not** run E-00015. It stays `PENDING` until its band is re-derived under the new key.

## Response (receiver, append-only)
- {{DATE}} — (role) — ...

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: ...

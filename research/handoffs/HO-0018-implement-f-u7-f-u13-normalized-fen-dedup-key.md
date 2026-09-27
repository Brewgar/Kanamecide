---
id: HO-0018
type: handoff
from: implementation-engineer
to: implementation-engineer
work_item: W-0003
status: REQUESTED
title: "Implement the E-0013 Option-(1) leakage remediation F-U7..F-U13: the dedup key is the normalized FEN"
artifacts: ["research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "research/sessions/S-0037-e0013-leakage-ruling-normalized-fen-dedup-key.md", "tools/e0013_extract.py", "research/sessions/S-0038-e0013-normalized-fen-dedup-key-implemented-f-u7-f-u13.md"]
commands: ["python tools/e0013_extract.py --selftest", "python tools/e0013_extract.py --count-only --out-dir build/s41/extract_new", "python research/scripts/research.py validate"]
acceptance: "F-U7..F-U13 discharged as stated, with the gate left blocking. Each clause below is binding and each names what would be a violation."
example: false
created: 2026-09-27
closed: null
---

# HO-0018 — Implement the E-0013 Option-(1) leakage remediation (F-U7..F-U13)

> The ONLY way to ask another agent to do something. Prose requests ("someone should
> verify this") are not handoffs and will be ignored. Receiver appends `## Response`
> and `## Verification`; the handoff may be edited while `status: REQUESTED|ACCEPTED`
> and is frozen once `DONE|REJECTED|WITHDRAWN`.

## Request

**This handoff is deliberately self-contained. You do not need to read S-0037 or the E-0013
addendum to execute it; everything you need is below.** Read them only to audit the ruling
itself, which is a *different* seat's job (HO-0019).

You are being asked to change one line of behaviour in `tools/e0013_extract.py` and to repair
a test that was passing for the wrong reason.

### The one-line cause

The dedup key was `pos.fen` — the **exact six-field FEN, clocks included**. The overlap-0 gate
compares `normalize_fen` — the **four-field FEN, clocks excluded**. A dedup key *strictly
finer* than the key the gate compares **cannot entail** the invariant the gate is supposed to
verify, so the gate could never pass by construction; it could only ever pass by coincidence.
A corpus with a small reachable-position space supplies that coincidence's failure, and
`K+R vs K` endgames did exactly that: 27 identical four-field FENs, one labelled copy on the
train side and one on the holdout side, differing **only in the halfmove clock and the
fullmove number**.

### The change

**Change the dedup KEY. Do not touch the gate.** The gate's own comparison is already correct
and pre-registered. Weakening the gate to match the key would invert the fix — it would delete
the instrument that detected the defect.

> **The dedup identity of a position is its NORMALIZED FEN** — side to move + piece placement
> + castling/EP rights. **The halfmove clock and the fullmove number are NOT part of the
> identity.**

Under that key, global-before-split dedup leaves at most one survivor per normalized FEN in
the whole corpus, that survivor's `game_id` alone decides the split, and a position therefore
cannot appear on both sides. **The gate then holds by construction and is retained as a
blocking regression test on the implementation** — still FAIL-before-fitting, still at both
pre-registered levels.

### What is FROZEN. Changing any of these is a violation, not a judgement call.

| Frozen | Value | If you think it should move |
|---|---|---|
| dedup **order** | GLOBAL, before the split (F9) | route it to the owner as a finding |
| survivor rule | first occurrence in `(game_id, ply_index)` order | route it to the owner |
| `SPLIT_SALT` | `20260926` | **never** — a salt chosen after a known-failing gate is selection on the leakage check |
| the 30,000 floor | `30000` | **never** — the owner's ruling says the value does not move |
| the pre-registered band | `75600..76587` | **never** — frozen, and a sanity check, not a pass criterion |
| E-0013 `status:` / any `result:` | `RUNNING` / none | not yours to set |

### F-U7 — change the dedup key in `tools/e0013_extract.py`

- The `seen` set at **L326-331** must key on `pos.norm_fen` (the existing `normalize_fen()`,
  L126-134), not `pos.fen`.
- The `dedup_key` string published in `extraction_pin` at **L442** must name the normalized
  FEN and state explicitly that the clock is **not** part of the identity.
- `dedup_order` stays `GLOBAL, before the split`; the survivor rule is unchanged.

### F-U8 — repair the self-test that passed for the wrong reason

- **L835-839** asserts the normalized-FEN invariant "holds BECAUSE the dedup ran first". Under
  the new key that becomes **true by construction**, and the check must be re-stated to say so.
  The old assertion was **false in general**: it held only because that fixture's duplicate
  copies were byte-identical *including clocks*, so the finer key caught them by luck.
- **Add a permanent regression fixture whose duplicate copies differ ONLY in the clocks** —
  the case the old fixture missed and the case the real dataset found.
- **Add the negative control:** a fixture that genuinely SHOULD fail the gate, so that the
  gate's *firing* is itself tested. A gate nobody has seen fire is not a tested gate. This is
  in addition to the existing check at L750-752, which must keep passing.
- Demonstrate the new fixture **failing on the old key and passing on the new one.** A
  regression test that has never been seen red proves nothing.

### F-U9 — re-derive and re-commit the split map and the artifacts

- Re-run the extraction under the new key. Record the new `positions_sha256` and the new counts.
- **Assert that `split_map_sha256` is UNCHANGED.** `split_map()` is a pure function of
  `(SPLIT_SALT, game_id)` (L152-164) computed at L532 over the dataset's game rows, before and
  independently of the dedup result, and the hashed object `{format, split_salt,
  train_fraction, rule, map}` (L575-582) contains **no dedup-derived quantity**. So the digest
  is invariant under this change and is expected to be byte-identical.
- **This is a checkable prediction. Check it; do not assume it.** **A digest that MOVES is a
  finding to report, not a new baseline to adopt** — it would mean the salt, the fraction or
  the rule moved, which this ruling does not authorise. Abort and report if it moves.
- `positions_sha256` and the position counts **WILL** change. Report both.

### F-U10 — re-derive the yield band and re-evaluate the 30,000 floor

- E-00015's band lower bound and the `~997` exact-FEN duplication projection are **superseded**.
  Re-derive from the new key's measured `duplicates_removed_by_dedup` **before** E-00015 runs,
  as a dated amendment to E-00015 — not to E-0013, and not silently.
- **The 30,000 value is not renegotiable.** Re-evaluate conjunct (a) on the new
  `count_usable_distinct_train`.

### F-U11 — re-derive E-00014's inner partition under the new key

- Its `s_d_inner` / `delta_star` / contingency figures were measured on the old corpus and are
  superseded. Its partition-integrity check (zero normalized-FEN overlap with the holdout,
  abort 3) must now hold **structurally**.

### F-U12 — route the corpus limitation into Sample Validity

- The **low-`game_id` survivor bias** is a new, named limitation. The survivor rule keeps the
  copy from the lowest-numbered game, so the corpus is now biased toward low-numbered games
  exactly where collisions occur. **A position deduplicated away is a datum deleted from the
  corpus** — not relocated, not down-weighted, not recovered. It must appear in E-0013's
  Sample Validity and must constrain every claim the fit licenses.

### F-U13 — the gate stays blocking. Do not weaken it to make the run pass.

- It must remain FAIL-before-fitting at **both** pre-registered levels. Under the new key it is
  expected to pass. **If it does not, that is a real defect in the implementation and it must
  be reported as measured** — not re-normalized, not re-ordered, not suppressed.

## Hard stops — read these before you touch anything

1. **Do not read the holdout. Do not read any label field. Do not fit anything.**
2. **Do not edit anything under `src/`.**
3. **Do not run E-00015.** It stays `PENDING`. Its pre-registration references the superseded
   key; running it now would arm or disarm E-0013's conjunct (a) with a number measured under
   a superseded key, which is worse than no number at all.
4. **Do not re-split, do not adjust the 30,000 floor, do not exclude the endgame region.** Each
   of those is a scope change, and the scope was just ruled on. If the realized
   distinct-position count falls below 30,000: **report that as a measurement and stop.**
5. **Do not change E-0013's `status:` or any `result:`. Do not change any H-#### text or
   status. Do not open or close HO-0005 or W-0003. Do not edit any R-00xx / S-00xx /
   CLOSED / VERIFIED record.**
6. **New scratch goes under `build/s41/`, never the repo root.**

## Pre-registered contingency — read this before you give up

**If F-U7 cannot be implemented for any reason, the ruling converts IN ADVANCE to option (3):**
E-0013 ends `INCONCLUSIVE-BY-SCOPE`. This is recorded in advance precisely so it cannot later
be read as a rationalisation for a failure to try. **It is not a licence to fall back to
option (2) (re-split with a new salt).** There is no second salt available as a fallback.

## Artifacts To Read (paths)

- `tools/e0013_extract.py` — the only file you may edit. L126-134 (`normalize_fen`), L326-331
  (the dedup), L340-378 (the gate, read-only), L442 (the published `dedup_key`), L750-752 and
  L835-839 (the self-tests to repair).

## Commands To Run

```powershell
cd c:\Users\tahae\Kanamecide

# the self-test, before and after your change
python tools/e0013_extract.py --selftest

# the run under the new key. --count-only reads no label field at all.
python tools/e0013_extract.py --count-only --out-dir build/s41/extract_new

# the memory layer
python research/scripts/research.py update
python research/scripts/research.py state --write
python research/scripts/research.py validate
git diff --check
```

## Acceptance Criteria (what makes this DONE)

1. The dedup key is the normalized FEN, at the two code locations, shown before and after.
2. **The `split_map_sha256` invariance assertion, shown actually running and its verdict stated
   either way.** The pre-registered value is
   `bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea`.
3. The **yield delta measured, not estimated** — old and new counts side by side. The owner
   explicitly declined to estimate it; do not supply a guess in its place.
4. The **clock-only-duplicate fixture**, shown failing on the old key and passing on the new one.
5. The **negative-control gate fixture**, shown firing.
6. All self-tests re-run and passing, with real output. **If you change any pre-existing check,
   say which one and why** — one of the 59 that passed before was testing the wrong thing.
7. `update`, `state --write`, `validate`, `git diff --check` all exit 0.

## Response (receiver, append-only)

- 2026-09-27 — (implementation-engineer) — executed in the same session that filed this handoff;
  full evidence in `research/sessions/S-0038-e0013-normalized-fen-dedup-key-implemented-f-u7-f-u13.md`.

## Verification (receiver, append-only)

- raw output / exit codes / hashes: see S-0038 and the evidence files it names.
- verdict: **PENDING independent verification.** Neither this implementation nor the ruling
  that authorised it is self-certifying. The *ruling* is routed to **HO-0019**
  (verification-auditor); do not treat S-0038 as discharging Gate 3.
## Commands To Run
```powershell
...
```

## Acceptance Criteria (what makes this DONE)
...

## Response (receiver, append-only)
- 2026-09-27 — (role) — ...

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: ...

---
id: HO-0020
type: handoff
from: verification-auditor
to: researcher-architect
work_item: null
status: REQUESTED
title: "Owner repair: the S-0037 leakage addendum on E-0013 is truncated/interleaved (FND-0030, blocking) and Z2's own proof row P4 is stale and self-referential (FND-0031, minor)"
artifacts: ["research/findings/FND-0030-x1-class-the-s-0037-leakage-addendum-e-0013-l2069-is-truncated-and-interleaved-sentences-severed-mid-clause-at-block-boundaries.md", "research/findings/FND-0031-z2-p4-the-z2-withdrawal-record-s-own-verification-row-p4-is-stale-and-self-referential-it-claims-four-occurrences-of-the-withdrawn-hash-and-names-two-line-numbers-that-no-longer-hold-any.md", "research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "research/reviews/R-0026-independent-verification-of-the-e-0013-s-0037-leakage-ruling-under-ho-0019-v1-v7-gate-3.md"]
commands: ["python research/scripts/imem.py findings FND-0030", "python research/scripts/imem.py finding FND-0030 --write --close --resolution <note> --by <agent> --by-context <context>", "python research/scripts/research.py validate", "python research/scripts/imem.py lint"]
acceptance: "The repair addendum is appended to E-0013; FND-0030 and FND-0031 are CLOSED with attributable --by strings and verified_by set by hand; imem lint returns to problems=0; validate exit 0."
example: false
created: 2026-09-30
closed: null
---

# HO-0020 — Owner repair of the truncated S-0037 leakage addendum (FND-0030) and Z2's P4 row (FND-0031)

> The ONLY way to ask another agent to do something. Prose requests ("someone should
> verify this") are not handoffs and will be ignored. Receiver appends `## Response`
> and `## Verification`; the handoff may be edited while `status: REQUESTED|ACCEPTED`
> and is frozen once `DONE|REJECTED|WITHDRAWN`.

## Request

You (researcher-architect, owner of the E-0013 record and author of the S-0037 leakage
addendum) are asked to repair two defects the verification-auditor found **by
recomputation** during the FND-closure round (S-0041, R-0026). Both are in the E-0013
record, which is RUNNING and editable by you. Neither was repairable by the auditor —
Gate 3 forbids the verifier editing the owner's record.

### FND-0030 (blocking — gates the lint, and E-0013's eventual close)

The S-0037 leakage-ruling addendum (E-0013, the `addendum-s-0037-...` anchor, L2069+)
is **truncated and interleaved**: sentences are severed mid-clause at block boundaries,
specifically at **L2092, L2124 and L2152**, and the rhetorical node "Why (1) and not
(3)" has no argument attached. This is the X1 defect class — the same failure B3/B4/B5
were discharged against — recurring in a *later* addendum *after* the X1 repair was
ruling-complete. The operative ruling content is verifiable (R-0026 V1–V7 all PASS:
the ruling cites the leakage contract by line number, L309–310; the remedy language
never treats S-0036 as authority) — but the **prose record of the reasoning is
physically damaged**, and a damaged reasoning record cannot carry weight in a later
dispute.

**Options, in order of preference:**
1. Reconstruct the severed sentences from your session artifacts (S-0036/S-0037 source
   text) and append a dated repair addendum to E-0013 quoting the restored clauses and
   the argument for "Why (1) and not (3)", naming L2092/L2124/L2152 explicitly.
2. If the original wording is genuinely lost: append a dated addendum ruling those three
   passage fragments **UNKNOWN**, restating the operative ruling cleanly so the record
   is self-contained — a recorded loss, not a silent one.

"Nobody will notice" is not an option; the auditor already noticed, and FND-0030 is
blocking precisely so the record cannot close E-0013 over it.

### FND-0031 (minor — piggyback)

Z2's withdrawal-record proof row **P4** claims the withdrawn hash appears 4 times;
the file has **5** occurrences, two of its named line numbers are stale, and the row
is **self-referential** (it quotes the token it counts, inflating the count by 1).
Append an erratum line in the same addendum style: actual count 5, current line
numbers as of the repair date, and the acknowledgement that a self-referential count
can never be stable — then close the row.

### Explicitly out of scope
FND-0027 (F-U11) and FND-0028 (F-U12) stay OPEN — E-00014 is PENDING with no trainer
and the `game_id` bias is not routed into `## Sample Validity`; those rows attach to
E-00014's resumption, not to this handoff. Do not close them here. Do not touch
E-00015 (PENDING by owner ruling; the gigaleak re-split is superseded pathology). Do
not reopen or edit any CLOSED finding row; repairs are append-only.

## Artifacts To Read (paths)

- `research/findings/FND-0030-*.md` and `FND-0031-*.md` — the defect records (full
  provenance in `## Origin` / `## Evidence`).
- `research/experiments/E-0013-*.md` — the record to repair (anchor named above).
- `research/sessions/S-0037-e0013-leakage-ruling-normalized-fen-dedup-key.md` — the
  session whose addendum is damaged; reconstruct from here if possible.
- `research/reviews/R-0026-*.md` — V1–V7 evidence that the *ruling* stands; your
  repair fixes the *record* of the reasoning, not the ruling.

## Commands To Run

```powershell
cd c:\Users\tahae\Kanamecide

# read the two rows (full origin/evidence bodies)
python research/scripts/imem.py findings FND-0030
python research/scripts/imem.py findings FND-0031

# after appending the repair/erratum addendum to E-0013:
python research/scripts/imem.py finding FND-0030 --write --close `
  --resolution "Repaired by owner: dated addendum restores the severed clauses at L2092/L2124/L2152 and supplies the 'Why (1) and not (3)' argument (or rules them UNKNOWN with a clean restatement)." `
  --by "researcher-architect (E-0013 record owner, repairing own addendum under HO-0020)"
python research/scripts/imem.py finding FND-0031 --write --close `
  --resolution "Erratum appended: withdrawn-hash count is 5 (self-reference acknowledged), line numbers refreshed." `
  --by "researcher-architect (E-0013 record owner, erratum under HO-0020)"
# then set verified_by + closed: + fill ## Resolution on both rows by hand
# (the --close command deliberately does not set verified_by)

python research/scripts/research.py update
python research/scripts/research.py state --write
python research/scripts/research.py validate   # expect: Validation OK, exit 0
python research/scripts/imem.py lint           # expect: problems = 0, exit 0
```

## Acceptance Criteria (what makes this DONE)

1. A dated repair/erratum addendum exists on E-0013 covering all three severed line
   numbers, the missing "Why (1) and not (3)" argument, and the P4 erratum.
2. FND-0030 and FND-0031 are CLOSED (attributable `--by`, `verified_by` set by hand,
   `closed:` filled, `## Resolution` summarises the repair).
3. `imem.py lint` → `problems: 0`, exit 0; `research.py validate` → exit 0.
4. Nothing else moved: no other row re-opened, E-00014/E-00015 untouched, protected
   hash range untouched, `H_body` of E-0013 re-verified byte-identical after your edit
   (**read bytes, not `Get-Content`** — CRLF splitting produces a false drift reading:
   `71691f0a…/22398` on a file whose true value is `c7ebe54c…/22196`).
5. `## Response` and `## Verification` appended below; `status: DONE`, `closed:` set;
   commit as `research(round4): owner repair per HO-0020 ...`.

## Response (receiver, append-only)
- (pending)

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict:

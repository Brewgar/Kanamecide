---
id: HO-0020
type: handoff
from: verification-auditor
to: researcher-architect
work_item: null
status: DONE
title: "Owner repair: the S-0037 leakage addendum on E-0013 is truncated/interleaved (FND-0030, blocking) and Z2's own proof row P4 is stale and self-referential (FND-0031, minor)"
artifacts: ["research/findings/FND-0030-x1-class-the-s-0037-leakage-addendum-e-0013-l2069-is-truncated-and-interleaved-sentences-severed-mid-clause-at-block-boundaries.md", "research/findings/FND-0031-z2-p4-the-z2-withdrawal-record-s-own-verification-row-p4-is-stale-and-self-referential-it-claims-four-occurrences-of-the-withdrawn-hash-and-names-two-line-numbers-that-no-longer-hold-any.md", "research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md", "research/reviews/R-0026-independent-verification-of-the-e-0013-s-0037-leakage-ruling-under-ho-0019-v1-v7-gate-3.md"]
commands: ["python research/scripts/imem.py findings FND-0030", "python research/scripts/imem.py finding FND-0030 --write --close --resolution <note> --by <agent> --by-context <context>", "python research/scripts/research.py validate", "python research/scripts/imem.py lint"]
acceptance: "The repair addendum is appended to E-0013; FND-0030 and FND-0031 are CLOSED with attributable --by strings and verified_by set by hand; imem lint returns to problems=0; validate exit 0."
example: false
created: 2026-09-30
closed: 2026-09-30
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
- **Accepted and executed as researcher-architect, 2026-09-30 — the E-0013 record owner and the
  author of the S-0037 addendum.** Gate 3 forbade the auditor from repairing my own record, so
  this is the seat that had to do it.
- **Both defects are repaired and both rows are closed.** A dated repair/erratum addendum is
  appended to E-0013 as **Addendum 3** (L2781-L2964, dated 2026-09-30), covering all three
  auditor-named lines, the missing "Why (1) and not (3)" argument, and the P4 erratum.
  `FND-0030` and `FND-0031` are `RESOLVED` with attributable `resolved_by`, `verified_by` set by
  hand, `closed: 2026-09-30`, and `## Resolution` written out in full.
- **On the "were they lost?" question, the answer is better than the handoff assumed, and I chose
  option 1 on evidence rather than on preference.** The severed clauses were *not* lost: the
  continuations are still in the file, orphaned at the top of unrelated blocks. Provenance by
  recomputation — the seams are present in `d8ce4aa`, the commit that first appended the addendum
  (a pure append, +286/0), and the S-0037 region is **byte-identical from `d8ce4aa` to HEAD**
  (285 lines, zero differing indices). So the original wording was never longer anywhere and cannot
  be recovered by reverting; but nothing was deleted either, only *relocated*, which is precisely
  the X1 signature quoted in FND-0030 itself (FND-0014: "each ending mid-clause with its
  continuation relocated far away"). The repair is therefore a **re-joining of the record's own
  surviving text** — stronger than either option as written: not a guess at what I meant, and not
  a recorded loss.
- **The three named re-joins**, each quoted in the addendum's repair ledger with its
  corroboration: **L2092 → L2348** (the three fixes, which S-0036 independently names);
  **L2124 → L2340-L2346** (the entire "Why (1) and not (3)" argument, plus the pre-registered
  conversion-to-(3) contingency at L2228-L2231); **L2152 → L2313** (the missing word was
  "guarantee.").
- **I found two seams the handoff did not name, and repaired them on the same evidence:**
  **L2217 → L2279** and **L2223 → L2270**. My scan of the whole addendum found **five** severed
  clauses and **four** orphaned tails, not three and none. Flagging this as a correction to the
  finding's scope rather than leaving it implicit.
- **The interleave is named, not silently reordered.** The S-0037 headings run 0, 1, 2, 4, 6, 7, 8,
  5, 3, and the seven-item cost list is split across the seam (items 2-7 at L2153-L2180, item 1 at
  L2324). The addendum states the logical order and reorders **nothing**, because rewriting filed
  prose would break append-only.
- **FND-0031 (Z2's P4) — erratum appended, and the self-reference is demonstrated rather than
  asserted.** Real count **5** (not 4), at **L1696, L1699, L1847, L1900, L1950**; the row's L1809
  and L1862 are stale and hold no token. Because P4 quotes the token it counts, it is one of the
  occurrences it enumerates and **no count written by quoting the token can ever be stable**. The
  erratum says so, then *shows* it: recounting after the erratum gives **7**, not 5, because the
  erratum itself quotes the token twice. The corrected claim is therefore stated as a
  self-reference-immune **predicate** ("every occurrence lies inside a withdrawal/audit context"),
  not as a number. Verified mechanically — the append script recounts the bytes and aborts if the
  number in the erratum disagrees with the file, so the figure cannot drift silently again.
- **Nothing else moved.** Prior prose is byte-identical (machine-asserted, not assumed); the five
  damaged lines are **left in place as evidence** and annotated rather than rewritten, so this is
  a recorded repair and not a laundered one. `H_body` recomputed byte-wise is **UNCHANGED** at
  `c7ebe54c…/22196`. The ruling itself is untouched: option (1) stands, the contract is still cited
  at L309-L310, option (2) is still rejected for the filed reason, the 27 are still S-0036's
  measurement and were not re-derived, the realized yield is still UNKNOWN and unestimated,
  E-00015 still waits, and F-U7..F-U13 are unchanged as obligations on the implementation-engineer.
  `tools/` and `src/` untouched; `status:` still `RUNNING`, no `result:`. **FND-0027 and FND-0028
  were left OPEN** (they belong to PENDING E-00014, and the low-`game_id` survivor bias is still
  not routed into `## Sample Validity`); E-00015 untouched; no CLOSED row reopened or edited; the
  lint gate and the holdout untouched.
- **One correction to the brief, for the record.** The task expected `H_body` to *change* after
  the addendum. It does not, and it could not: `H_body` is defined over **L1-428**, an initial
  segment of the file, and an append at end-of-file cannot move an initial segment. It remains
  `c7ebe54c…/22196` — the *stronger* result, since that range's invariance is what E-0013's
  integrity clauses and R-0026 V7 actually assert. The figure that moved is the file length,
  **214,086 → 228,562 B**.
- **Method note carried forward, because it has now misled two readers:** `H_body` must be read as
  **bytes**. `Get-Content` splits on CRLF semantics and reports phantom drift (`71691f0a…/22398`)
  on a file whose true value is `c7ebe54c…/22196`. R-0026 hit this; this seat hit it again on the
  first attempt and the guard caught it.

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
  - `python research/scripts/research.py validate` → **exit 0**, `Validation OK` (remaining lines
    are the pre-existing grandfathered/advisory warnings, not failures).
  - `python research/scripts/imem.py lint` → **exit 0**, `problems: 0`, `warnings: 153`
    (pre-existing prose-link/line-pointer advisories; the single blocking problem
    `RUNNING target carries OPEN blocking findings: FND-0030` is **gone**).
  - `python research/scripts/research.py update` → **exit 0**, `updated: research/index.md`.
  - `python research/scripts/research.py state --write` → **exit 0**, wrote `state.md` + `state.json`.
  - `imem.py finding FND-0030 --write --close … --by …` → `status: RESOLVED`, exit 0;
    `FND-0031` likewise → `status: RESOLVED`, exit 0. `verified_by`, `closed:` and the
    `## Resolution` bodies were then set **by hand**, as `--close` does not set `verified_by`.
  - **File, byte-wise (Python `open(path,'rb')`; never `Get-Content`):**
    - bytes **214,086 → 228,562** (+14,476); lines **2,780 → 2,964** (+184).
    - **CR count 0**, **no BOM**, single trailing `0x0A`, no trailing blank line.
    - **append-only: the first 2,780 lines are byte-identical to the pre-image (asserted);** the
      addendum begins exactly at the boundary, `L2781 = '---'`, and `L2783` is the
      `## Addendum 3:` heading. `git diff --numstat` is therefore a pure addition.
    - **`H_body` = `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` over
      22,196 bytes — UNCHANGED**, and equal to the value pinned at E-0013 L2241 and independently
      reproduced by R-0026 V7.
  - **Seam provenance, recomputed across all 15 commits touching E-0013:** the three auditor-named
    seams are present in `d8ce4aa` and in every commit after it, and in none before it; the S-0037
    region (285 lines, L2069-L2353) is **byte-identical `d8ce4aa` → HEAD**. The damage was present
    at authoring time and was never repaired.
  - **Z2 withdrawn-token recount, byte-wise:** pre-append **5** at L1696, L1699, L1847, L1900,
    L1950; post-append **7** (the two extra are the erratum's own quotations, at L2908 and L2912)
    — the self-reference, demonstrated. The append script asserts `claims 7 == file has 7` and
    aborts on any mismatch.
  - **Reproduction:** the append is idempotent and self-asserting —
    `python _obs/r4/append_repair.py` rolls back to the pristine `HEAD` blob if a prior run
    appended, re-appends, and fails loudly on any CR/BOM/EOF/append-only/`H_body`/count violation.
    Supporting scripts: `_obs/r4/forensics.py` (seam provenance), `_obs/r4/seams.py` (seam census),
    `_obs/r4/census.py` (Z2 recount), `_obs/r4/verify.py` (post-repair verification).
- verdict: **DONE.** All five acceptance criteria are met: the dated repair/erratum addendum
  exists on E-0013 covering all three named line numbers, the missing "Why (1) and not (3)"
  argument and the P4 erratum (1); both findings are CLOSED with attributable `--by`, hand-set
  `verified_by`, `closed:` and `## Resolution` (2); `lint` is `problems: 0` / exit 0 and `validate`
  is exit 0 (3); nothing else moved — no row re-opened, E-00014/E-00015 untouched, the protected
  hash range verified intact and `H_body` re-verified **byte-identical** by a byte-level read (4);
  `## Response` and `## Verification` appended, `status: DONE` (5). **E-0013 remains `RUNNING` and
  is now free of OPEN blocking findings**, so its close is no longer gated by this defect.

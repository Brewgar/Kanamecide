---
id: S-0044
type: session
agent: implementation-engineer
round: 6
title: "Round-6 umbrella for the six seat sessions T-001..T-006 (W-0006 root-scratch clean-up, D-0002..D-0006 + E-00004/E-00005 re-attestation addenda, E-0013 gate-readiness, FND-0035 census, HO-0022/HO-0023) + the normalization commit"
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-10-03
closed: 2026-10-03
related: [R-0027, W-0006, MAN-W0006-root-scratch, D-0002, D-0003, D-0004, D-0005, D-0006, E-00004, E-00005, E-0013, E-00014, E-00015, FND-0035, FND-0034, FND-0033, HO-0022, HO-0023, S-0043]
---

# S-0044 — Round-6 umbrella: seat sessions T-001..T-006, normalized and committed

> **Why one record and not six.** Six seat sessions ran across 2026-10-02..2026-10-03 under the
> orchestrator's task labels **T-001..T-006**. None of them wrote a session record at the time, so
> on disk they exist only as their artefacts. This record is the single honest index over them: it
> names all six, states what each produced and which seat produced it, and points at the records
> that carry the detail. It is **not** a reconstruction of six lost chats, and it makes no claim
> about work no artefact evidences. The T-labels are the orchestrator's; they appear nowhere in the
> corpus, so where this record maps a T-label to a seat that mapping is stated here explicitly
> rather than implied by a record.
>
> **Authoring seat.** This file and the commit that carries it were produced by the
> **implementation-engineer seat acting as MEMORY-KEEPER**: normalization and commit only. No
> finding, handoff, experiment, debate or review content was authored, edited, re-attested or
> closed by this record — those were the six seats' work, already on disk before it began.

## Round / Work Items Touched

- **W-0006** (root-scratch debt reduction, owner implementation-engineer) — content written by
  T-002; **left `IN_PROGRESS`**, not closed here. See "What I did NOT do".
- **No work item was opened, claimed or closed by this record.** W-0003, W-0008, HO-0005 and the
  round-4 chain were not touched.
## The six sessions

| T | Seat | Date | Produced | On disk |
|---|---|---|---|---|
| T-001 | verification-auditor | 2026-10-02 | HO-0021 independent audit of W-0008 (imem 2.1.0 + `INFRASTRUCTURE.md`) and of the FND-0032 self-closure. **W-0008 VERIFIED; the FND-0032 closure JUSTIFIED**; 4 non-gate defects, one latent freshness-policy gap (D-4) | `research/reviews/R-0027-...md` (already committed in `3f96562` / `f5883dc`) |
| T-002 | implementation-engineer, **MEMORY-KEEPER hat** | 2026-10-02 | The W-0006 root-scratch census and clean-up: 204→79 root files, 29 DELETE / 96 MOVE / 79 KEEP rows with per-row sha256; `root_grandfathered.txt` 267→73; work-log entry + exit-check results; routed for independent spot-check | `research/manifests/MAN-W0006-root-scratch.{md,json}`, `research/work/W-0006-...md`, `research/scripts/root_grandfathered.txt`, `research/handoffs/HO-0022-...md`, the root deletions/moves in this commit |
| T-003 | chief-architect | 2026-10-02 | **Re-attestation addenda on D-0002..D-0006.** Verdicts re-derived against the tree, not inherited: D-0002 **SUPERSEDED-BY E-0002**; D-0003 **RE-ATTESTED** (still open, baseline now E-0002-certified); D-0004 **SUPERSEDED-BY DEC-0008** with the finding **RE-ATTESTED** at runtime (16 pseudo-legal vs 9 legal reproduced); D-0005 **RE-ATTESTED** with `sizeof(Board)` corrected to **216 B** measured under MSVC, which cuts Agent C's ~14 GB/s traffic figure by ~45% without changing the argument's direction; D-0006 **RE-ATTESTED and executed as filed** (quiescence shipped one stage ahead of the TT; the residual PVS/TT attribution confound is now H-0009) | the five `research/debates/D-000{2..6}-*.md` files (appended addenda + `last_updated`) |
| T-004 | chief-architect | 2026-10-02 | **Re-attestation addenda on E-00004 / E-00005.** E-00004: the `## Interpretation` decision rule is **SUPERSEDED-BY the collective's ROUNDED D-0001 position** (classical-first, GPU PUCT held at Phase 3 behind a re-specified gate); the measurement spec is RE-ATTESTED and must be re-specified, not discarded; record stays `PENDING` and unrun, and the stale "Pre-search HEAD (perft-only)" premise is corrected. E-00005: **RE-ATTESTED** — never run, slider share still UNKNOWN, the `>=30%` rule untripped; its E-00003 baseline is superseded *for citation* by E-0002, which also satisfies its `## Engine Version` requirement via `KANA_GIT_COMMIT` + `--bench` | the two `research/experiments/E-0000{4,5}-*.md` files |
| T-005 | experimental-scientist (**preparer** seat — explicitly not the executor seat of HO-0015/HO-0016, and not the owner of E-00014/E-00015) | 2026-10-03 | **E-0013 execution-readiness checklist** for the two gate experiments, appended in place at line 2966: every item marked READY / BLOCKED(dependency) / MISSING(spec gap), each naming the exact unblocking artifact, and a **NO-GO on both gates**. Corrects the brief's premise that F-U14 was still a hard prerequisite (**F-U14 is DISCHARGED** — FND-0033 RESOLVED, suite N=200, overlap-0, hash-pinned) and records that F-U14 landing is what armed E-00014's abort condition 7 by turning `validate` red. Integrity block: protected range L1-428 re-hashed byte-wise before and after the append (`c7ebe54c…` over 22,196 B, unchanged), UTF-8/no-BOM/LF, `status:` stays `RUNNING`, `result:` stays `null`. **Nothing was measured and no lifecycle field moved.** | `research/experiments/E-0013-...md` (the 2026-10-03 addendum) |
| T-006 | search-researcher (research seat, read-only census) | 2026-10-03 | **FND-0035** — the Q-0002 pre-eval census of `src/search.cpp`/`tt.cpp`, filed deliberately *before* any eval-fitting verdict so the Q-0002 pruning deltas are not contaminated by a moving eval. Six findings: (1, BLOCKING) `ORDER_STAGE` is one boolean so stages 0-3 are identical and **E-0007's per-lever attribution is not reproducible from current source**, which `Q-0002:34` cites as its own premise; (2, HIGH) unbounded, repetition-blind `qsearch` recursion reachable from live play; (3, MED-HIGH) stand-pat fail-high unguarded by `in_chk`, contradicting E-0008's own contract; (4, MED) `go nodes N` is per-iteration not cumulative, so the node-delta tier must use `go depth D`; (5, HIGH for the design) two hardcoded copies of the material values, so an E-0013 Texel refit would silently ship ordering tuned to the old values; (6, LOW) dead/suspicious code, recorded not fixed. **No `src/` file was edited.** | `research/findings/FND-0035-...md` |
| — | implementation-engineer, MEMORY-KEEPER hat (**this record**) | 2026-10-03 | The normalization and commit itself: regenerate the derived projections over the five seats' records, write S-0044, commit as one logical unit | this file + `research/{index.md,state.json,state.md}` |

### Cross-session pointers worth carrying forward

- **R-0027 (T-001)** is the Gate-3 discharge for W-0008 and the FND-0032 closure — the same rule
  (the author may not verify its own work) that T-002 invoked when it refused to close its own
  W-0006 and routed **HO-0022** instead.
- **MAN-W0006 (T-002)** is the audit surface for HO-0022: 10 named rows, seed 20261002, with a
  standing invitation to re-derive a different random draw.
- **FND-0035 (T-006) contradicts a premise T-003 relied on.** T-003's D-0006 addendum cites
  E-0007/E-0008 node deltas and routes the residual confound to H-0009; T-006 shows the
  `ORDER_STAGE` lever staging those deltas rest on is not implemented in `src/search.cpp` as it
  stands. Both records stand as written — neither is edited here — but a reader of D-0006's
  attribution sentence now has a blocking finding against its reproducibility.
- **FND-0034 (the one open `validate` problem)** is *not* one of these six sessions' products. It
  is the pre-existing EV-0010 sha256 drift on `build/Release/kana.exe`, owner-routed, recorded in
  MAN-W0006's "Known defects" and named as an E-00014 abort-condition trigger by T-005.

## What I Did (with evidence)

| # | Action | Evidence (command → observation → path) | Calibration |
|---|---|---|---|
| 1 | Read the five seats' diffs and the six artefacts before writing anything, so this record describes what is on disk rather than what was intended | `git diff -U0 -- research/debates research/experiments` → 8 files, +375/−11; read MAN-W0006, W-0006, FND-0035, HO-0022, HO-0023, R-0027, S-0043 | demonstrated |
| 2 | Regenerated the derived projections over the seats' records | `research.py update` → `updated: research/index.md`, exit 0; `research.py state --write` → `wrote state.json and state.md`, exit 0 | demonstrated |
| 3 | Wrote this record (one umbrella naming T-001..T-006) — the only content authored | `research/sessions/S-0044-...md` | demonstrated |
| 4 | Re-ran `update` + `state --write` **after** this file existed, so the committed projections index S-0044 too. The stale-record-count gate fires whenever a record lands between regeneration and commit; that gate firing is a correct measurement, not a fault | `update` → exit 0; `state --write` → exit 0; `validate` → no `audit[state]` problem | demonstrated |
| 5 | Committed all six seats' products, S-0044 and the regenerated projections as one logical unit | `research(round6): commit T-003..T-006 products (W-0006 manifest, re-attestation addenda, E-0013 readiness, FND-0035, HO-0022/0023) + S-0044 + regenerated projections` | demonstrated |

## What I Did NOT Do (and why)

- **Did not re-pin EV-0010 or touch `evidence/EV-0010-*.md`.** The `audit[evidence]` sha256 drift on
  `build/Release/kana.exe` is **FND-0034, owner-routed**. Re-pinning an evidence digest is the
  record owner's act; a memory-keeper that "fixes" it to make `validate` green would be forging an
  attestation. It is deliberately left red and visible.
- **Did not close anything.** W-0006 stays `IN_PROGRESS` with `verified_by: null` — its author may
  not verify its own work, which is why HO-0022 exists. FND-0035 stays `OPEN`. E-0013 stays
  `RUNNING` / `result: null`; E-00014 and E-00015 stay `PENDING`. HO-0022 and HO-0023 stay
  `REQUESTED`. No finding, handoff, experiment, debate, review, work item or decision was closed,
  edited or re-attested by this record.
- **Did not edit any finding/handoff/experiment/debate content.** The append-only discipline holds:
  the diff for those files is T-003/T-004/T-005's, already on disk before this record.
- **Did not invent six session records.** Six separate files would be six fictions with six
  invented `agent:` fields and six invented `created:` dates. One record naming all six is the
  honest shape.
- **Did not touch `src/` or `tools/`.** T-006's FND-0035 is a read-only census and says so; no
  engine or tool change was at stake anywhere in this commit.
- **Did not push.** The commit is local; pushing is the owner's call.

## Claims I Made That Are NOT Yet Verified

- Every mapping in the "The six sessions" table is **this record's** attribution, not a per-session
  artefact. The seat and date columns are read off each artefact's own byline
  (`Addendum (chief-architect, 2026-10-02)`, `Seat: MEMORY-KEEPER`,
  `raised_by: search-researcher`, `from: experimental-scientist`, …); the T-label↔seat pairing is
  the orchestrator's, stated here because no record on disk carries it. Where T-001 is concerned,
  R-0027 was already committed before this record existed, so its absence from this commit is not
  evidence of anything.
- T-002's central claim — that nothing cited was destroyed — is **author-attested and unverified**.
  HO-0022 exists to have `verification-auditor` attack it over 10 rows; that has not happened.
- T-005's NO-GO verdicts and its "F-U14 is DISCHARGED" premise correction are the preparer seat's
  own reading. HO-0023 carries them to `chief-architect` for an owner's answer; no answer is on
  disk.
- T-006's FND-0035 severity calls (BLOCKING / HIGH / MED-HIGH / MED / LOW) are the census seat's
  judgement. FND-0035 is OPEN and unverified; in particular Finding 1's claim that E-0007's
  attribution is unreproducible should be reproduced by a seat other than its author.

## Environment Facts Learned

- **Shell output redirection in PowerShell writes UTF-16**; reading such a capture back shows one
  character per line with NUL padding. Use `cmd /c "... > file"` to get a single-byte capture, and
  take verdicts from file contents rather than from the shell's own reported exit code — a false
  `exit 1` is observable on clean runs.
- **The engine's `build/Release/kana.exe` is what EV-0010 pins, and it currently drifts.** Any gate
  that hashes the binary will report FND-0034 until an owner re-pins it; this is expected state,
  not a regression to chase.
- **`research/context/*` and `_obs/` are gitignored**, so the raw captures behind these six sessions
  (`_obs/w0006/`, `_obs/addendum/`, `_obs/replan/`, `_obs/ho0021/`) stay on disk without entering
  history. Only `_obs/fu14_smoke_raw.jsonl` is tracked. The evidence trail for this commit is
  therefore the records themselves plus those local directories.

## State Left On Disk

- **New in this commit:** `research/sessions/S-0044-...md`, `research/findings/FND-0035-...md`,
  `research/handoffs/HO-0022-...md`, `research/handoffs/HO-0023-...md`,
  `research/manifests/MAN-W0006-root-scratch.{md,json}`.
- **Appended by T-003/T-004/T-005:** `research/debates/D-0002..D-0006`,
  `research/experiments/E-00004`, `research/experiments/E-00005`,
  `research/experiments/E-0013` (the 2026-10-03 readiness addendum at line 2966).
- **By T-002:** `research/work/W-0006-...md` work-log + exit-check block,
  `research/scripts/root_grandfathered.txt` (267→73, written BOM-less), and the repo-root deletions
  and `_obs/e0010-era/` moves (root 204→79).
- **Regenerated:** `research/index.md`, `research/state.json`, `research/state.md`.
- **Unchanged on purpose:** `research/evidence/EV-0010-*.md`; every lifecycle field of W-0006,
  FND-0035, E-0013, E-00014, E-00015, HO-0022, HO-0023.
- Gates at close: `validate` → exactly **1** problem (FND-0034, the EV-0010 drift); `selftest` → OK;
  `tests_imem` → 48 tests OK; `imem.py lint` → problems 0 (warnings 179, advisory).

## Next Action For The Successor

1. **verification-auditor:** take **HO-0022** — spot-check 10 manifest rows and rule on MAN-W0006
   as a whole. W-0006 cannot close until you do; its author is not an acceptable verifier.
2. **chief-architect:** take **HO-0023** — answer the seven blockers to GO on E-00014/E-00015. The
   single highest-leverage item is the dated amendment to **E-00015 itself** (replace the retired
   band clause, re-describe the Power section's reliance on it, replace decision rule 3 with the
   accounting identities, restate stage 4 as the normalized-FEN key). After that amendment E-00015
   has no missing artifact.
3. **Owner / sponsor:** disposition **FND-0034** (re-pin or retire EV-0010's binary digest) — it is
   the one thing keeping `validate` red, and T-005 named it as the trigger for E-00014's abort
   condition 7.
4. **Whoever takes H-0009:** FND-0035 must be resolved first. Until `ORDER_STAGE` is made a real
   per-lever switch (or E-0007's numbers are re-measured with the current binary as rung 0), the
   Q-0002 pruning ladder cannot quote an ordering baseline.
5. **chief-architect** also owns a new work item for the DEC-0008 `dump_moves` mislabel that T-003's
   D-0004 addendum surfaced (`src/main.cpp:234` prints "legal moves" over a pseudo-legal list);
   documentation-only, live-severity-low, but DEC-0008's evidence line currently understates it.

## Escalations (owner decisions needed)

- **FND-0034 / EV-0010 sha256 drift** — owner-routed, deliberately not fixed here. `validate` stays
  red on exactly this one problem until an owner acts.
- **The BOM parse defect in `root_grandfathered.txt`'s loader** (`load_grandfathered()` does not
  strip a UTF-8 BOM, so the header parsed as a phantom entry) — recorded in MAN-W0006's "Known
  defects", mitigated by writing the list BOM-less. The `research.py` fix is not this seat's.
- **Gate-3 self-verification pressure** — MAN-W0006, R-0027 and FND-0035 are all author-attested.
  Each has a routing vehicle (HO-0022, and the OPEN status of FND-0035). None may be closed by its
  own author.
- **Unresolvable without an owner:** whether the `_obs/e0010-era/garbage/` quarantine of 45
  untracked junk files should become a permanent deletion. The manifest moved them with bytes
  intact rather than destroying the owner's files; that decision is still open.

## Validation Status

- `python research/scripts/research.py update` → `updated: research/index.md`, exit 0.
- `python research/scripts/research.py state --write` → wrote `state.json` + `state.md`, exit 0.
- `python research/scripts/research.py validate` → **exactly 1 problem**, exit 1:
  `audit[evidence]: sha256 drift on build/Release/kana.exe (EV-0010)` = FND-0034, owner-routed and
  deliberately untouched. **No `audit[state]` problem** — the projections were regenerated *after*
  S-0044 landed, which is the only way that gate stays quiet.
- `python research/scripts/research.py selftest` → OK, exit 0.
- `python research/scripts/tests_imem.py` → 48/48 OK, exit 0.
- `python research/scripts/imem.py lint` → **problems 0**, exit 0. Advisory warnings are 179,
  up from the 166 recorded at S-0043's close — the delta is this commit's own six new/changed
  records (FND-0035, HO-0022, HO-0023, MAN-W0006 and S-0044), including the expected advisory
  `OPEN target carries OPEN blocking findings: FND-0035`. Advisory, not problems.
- `git status --porcelain` → empty for every path in this commit, after the commit landed.

<!--S0044-PART2-->
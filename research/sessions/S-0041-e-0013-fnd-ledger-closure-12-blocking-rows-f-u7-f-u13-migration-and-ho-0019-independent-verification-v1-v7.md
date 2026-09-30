---
id: S-0041
type: session
agent: verification-auditor
round: 4
title: E-0013 FND ledger closure (12 blocking rows), F-U7..F-U13 migration, and HO-0019 independent verification (V1-V7)
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-30
closed: 2026-09-30
related: [HO-0019, R-0026, E-0013, E-00014, E-00015, FND-0001, FND-0018, FND-0023, FND-0029, FND-0030, FND-0031, DEC-0012, S-0037, S-0038, S-0039, S-0040]
---

# S-0041 — E-0013 FND ledger closure + HO-0019 verification (verification-auditor)

> Seat: **verification-auditor**. I am neither E-0013's owner (`researcher-architect`) nor the
> engineer who repaired it (`implementation-engineer`), so Gate 3 binds and is satisfied on every row
> I closed: `verified_by: verification-auditor` throughout.

## Round / Work Items Touched
- **HO-0019** (receiver) — `REQUESTED` → **DONE**. All seven verdicts recomputed from the repository.
- **W-0003** — **not claimed, not closed.** It remains `IN_PROGRESS` with `verified_by: null`; closing
  it is not this seat's to do and was out of scope.
- No work item created or closed. No hypothesis, decision or experiment status touched.

## What I Did (with evidence)

| # | Action | Evidence (command → exit code → path) | Calibration |
|---|---|---|---|
| 1 | Re-established the baseline, all four checks | `research.py selftest` → 0 (47/47); `imem.py selftest` → 0 (43/43, `VERSION 2.0.0 (DEC-0012)`); `research.py validate` → **1 (FAILED)**; `imem.py lint` → 1 (1 problem, 128 warnings) → `_obs/vf/` | demonstrated |
| 2 | **Found the brief's premise wrong on `validate`** | `validate` FAILED on `repo root: '_obs_out1.txt' is not a sanctioned root file` — 0 bytes, untracked, gitignored (`.gitignore:106`), created 11:19:56 by a prior session's redirect typo. Not present in the brief's expected state | demonstrated |
| 3 | Cleared the hygiene blocker without weakening the gate | deleted the 0-byte file (`_obs/vf/pre_del.txt`); `validate` → **0, "Validation OK"**. Added nothing to `root_grandfathered.txt`; the gate itself untouched | demonstrated |
| 4 | Committed the prior session's **uncommitted** DEC-0012 work, verbatim, split by purpose | `74aed25` (`build(round4):` tooling) + `a8a902a` (`research(round4):` records). Content unmodified — `git add` only | demonstrated |
| 5 | **Closed the 12 blocking rows** one at a time | `imem.py finding FND-XXXX --write --close … --by "verification-auditor"` per row; each then given `verified_by` and a `## Resolution` body naming commands + outputs. `lint`: **problems 1 → 0, exit 1 → 0** | demonstrated |
| 6 | Did **not** trust the disposition table where R-0020 said "PARTIALLY DISCHARGED" | B3/B4/B5 were conditional on the X1 seams being joined. Wrote `_obs/parts/seams.py`: **all 10 seams contiguous = True** (`_obs/vf/seamsres.txt`) | demonstrated |
| 7 | Recomputed the arithmetic instead of copying it | B4: `0.5/sqrt(200)=0.035355`, `0.02/SE=0.566`; B5: `k4-k3=-3.7`, `k6-k5=-11.5`; B6: `76593-76587=6`, `1.302%→997`, `75600/30000=2.52x`; X2: `500/112.1=4.46`, KING-PST=128 not 240 → `_obs/parts/b4math.py`, `b56math.py`, `x2b.py` | demonstrated |
| 8 | Recomputed both pinned hashes | `H_body = c7ebe54c…bea7` / **22196 B** (byte-level, `_obs/vf/hb.py`); split-map digest = `bb079a41…a1ea` (HO-0019's exact command, `_obs/vf/v6.txt`) | demonstrated |
| 9 | Filed F-U7..F-U13 as FND-0023..0029, **idempotently** | `_obs/parts/extract_fu.py`: 1st run `created=7`; **dry re-run `created=0`** (7× `SKIP`) → `_obs/vf/fu1.txt` | demonstrated |
| 10 | Closed F-U7/8/9/10/13, **left F-U11 + F-U12 OPEN** with dated addenda | F-U11: E-00014 is `PENDING`, its L68 still says exact-FEN, the trainer *"does not exist yet"*. F-U12: the low-`game_id` bias is named but **not** in `## Sample Validity` | demonstrated |
| 11 | Verified F-U13 **negatively** (a gate is shown un-weakened by its failure paths) | `PASS gate FIRES on a genuine cross-split clock-only leak`; `positions.jsonl`/`split_map.json`/`report.json` NOT written on abort; live `ABORT: overlap-0 gate FAILED … no artifact was written` | demonstrated |
| 12 | Disposed of HO-0019 per its own V1–V7 protocol; filed **R-0026** (`kind: verification`) | **V1–V7 all PASS incl. V3.** V3 evidence: all three S-0036 references in E-0013 treat S-0036 as the source of the *finding*, never the authority for the *remedy* | demonstrated |
| 13 | **Filed two new findings I found by recomputation** | **FND-0030** (`blocking`, OPEN): the S-0037 addendum L2092/L2124/L2152 are severed — the X1 class recurring in a *later* addendum. **FND-0031** (`minor`, OPEN): Z2's own proof row P4 is stale (claims 4 occurrences, file has 5) and self-referential | demonstrated |
| 14 | Left lint red **on purpose** | `lint` reports exactly one problem: `RUNNING target carries OPEN blocking findings: FND-0030`. A defect I found and did not repair stays open; forcing it green would be the failure mode this ledger exists to catch | demonstrated |

## What I Did NOT Do (and why)
- **Did not edit E-0013 at all.** The protected hash range (L1-428) is recomputed and byte-identical
  (`c7ebe54c…bea7`/22196). E-0013 is the owning seat's record.
- **Did not read the holdout, read any label field, or fit anything** (HO-0019 §Acceptance 5).
- **Did not run E-00014 or E-00015.** Both stay `PENDING`; E-00015's hold ("may not run until the new
  dedup key is implemented and the re-derivation under F-U7 is complete") is untouched.
- **Did not change the salt, revert the key, or weaken the gate.**
- **Did not change any `status:`/`result:` on any record** other than the findings I closed and HO-0019.
- **Did not close FND-0008..0013, FND-0027, FND-0028, FND-0030, FND-0031.** An open ledger that lies
  in either direction is worthless; these are genuinely unpaid.
- **Did not touch CLM-0001..0003** — a claim moves out of OPEN only when the fitted artifact is
  consumed, which is downstream of E-0013 actually running.
- **Did not modify any tooling, schema, severity vocabulary or gate.** `git diff HEAD -- research/scripts/`
  was empty after the 12 closures: lint went green because rows were discharged, not because the
  check was softened.
- **Did not "fix" the 27.** Reproducing it needs the real dataset, which aborts on a provenance pin in
  this tree (`ABORT: SRC-COMMIT PIN VIOLATED … nothing is written`). I did not force it; the 27 remain
  S-0036's measurement and this session does not upgrade that.

## Claims I Made That Are NOT Yet Verified
- **The 27** (`normalized_fen_overlap = 27`) — carried on S-0036's authority, unreproduced. *Strongly
  supported*; the mechanism is confirmed by the clock-only fixtures, the specific count is not.
- **The realized yield under the new key** — unknown. E-00015's, PENDING. *Unknown.*
- **F-U11's structural partition-integrity** — asserted nowhere demonstrable. *Unknown.*
- **The low-`game_id` survivor bias magnitude** — named but unquantified. *Unknown.*
- **Z3's boundary figures** (`1011/0`, `493/130`, `231/29`) — labelling verified, arithmetic not
  re-derived. *Strongly supported* (R-0022's `numstat`).
- **Z1's word provenance** (recovered from the pre-edit blob) — end state verified, provenance not
  re-derived. *Strongly supported.*

## Environment Facts Learned
- **The DEC-0012 institutional-memory system was entirely uncommitted at HEAD `2f31549`.** A verifier
  arriving at the stated HEAD audits an uncommitted corpus; check `git status` before trusting a
  megaprompt's "already committed" claim.
- **PowerShell `Get-Content` cannot reproduce a byte-level hash.** It splits on CRLF semantics and gave
  `71691f0a…/22398 B` for `H_body` where a byte-level read gives the published `c7ebe54c…/22196 B`. A
  verifier using the wrong reader would report **false drift**. Use `open(path,"rb")`.
- **`imem.py finding --close` writes an UNQUOTED `resolution:`.** A resolution containing `": "` is
  invalid YAML and duplicates the key once quoted by hand. `_obs/parts/fixfm2.py` normalises this
  idempotently (prints `NOCHANGE` on re-run) — but this is a real footgun in the close path.
- **`imem.py new-finding --anchor` silently double-prefixes** when both `--target` and `--anchor`
  carry the record id, yielding `E-0013#E-0013#…`, and `anchor_ok: False` is reported **after** the
  file is written. Always read back the anchor and prefer the `suggested_anchor` it prints.
- **Parallel shell commands collide** in this environment (all four of my initial baseline commands
  returned the same terminal buffer). Redirect to `_obs/` and read the file.
- `imem.py lint` warning count is **128**, not the 127 the megaprompt predicted (one extra advisory).

## State Left On Disk
- **`imem.py lint`: `problems: 0` → then `problems: 1`** — the one problem is **FND-0030**, my own new
  blocking finding. This is the correct end state, not a regression.
- Findings ledger: 31 rows. **23 closed** (FND-0001..0007, 0014..0022, 0023..0026, 0029),
  **8 open** (FND-0008..0013 major/deferred, FND-0027 + FND-0028 F-U11/F-U12 unpaid,
  FND-0030 + FND-0031 new).
- **R-0026** filed (`kind: verification`, `reviewer: verification-auditor`, `status: COMPLETED`).
- **HO-0019** `DONE`, `closed: 2026-09-30`, `## Response` + `## Verification` appended.
- **S-0041** (this record). Repo root clean; `_obs_out1.txt` removed and documented.
- No `research/_index/` or `_obs/` content committed (both gitignored).

## Next Action For The Successor
1. **The owner (`researcher-architect`) owns FND-0030** — repair the three severed sentences in E-0013's
   S-0037 addendum (L2092, L2124, L2152) as a **dated addendum**, and carry a per-seam ledger like the
   X1 repair did (E-0013 L1162-L1178). Until then `imem.py lint` stays at exit 1, **by design**.
2. **FND-0027 (F-U11)** needs the **trainer built and verified** before E-00014 can run; that is the
   single largest remaining engineering item and it gates every fitter.
3. **FND-0028 (F-U12)** needs the low-`game_id` survivor bias written into `## Sample Validity` with an
   explicit constraint on what the fit may license.
4. **E-00015's dated amendment** (band retired; stage 4 restated) precedes any count under the new key.
5. **FND-0008..0013** are `P0 deferred`/routing flags — review whether each should stay open or be
   re-scoped now that the B-family is discharged.
6. **W-0003 still has `verified_by: null`** and will keep blocking `research.py round --round 4`.

## Escalations (owner decisions needed)
- **Is the S-0037 addendum's truncation in scope for a contract repair, or is the addendum frozen as
  historical?** If frozen, FND-0030 should be re-scoped to a "known-defect, record-only" note rather
  than a repair. I cannot decide this: it changes a record the owning seat wrote.
- **FND-0030 blocks the G4 training-readiness gate** ("adversarial critique CLEAN or all blocking
  findings discharged before RUNNING"). E-0013 is `RUNNING` with one open blocking finding. Either the
  finding is repaired, or the owner records a dated, reasoned decision that a record-only truncation in
  a post-RUNNING addendum does not gate. **I am not making that call.**
- **FND-0011 (F-U4)** — the E-0011 backwards-citation correction is owed by the *E-0011 owning seat*,
  not by me and not by E-0013's owner. It needs a handoff if it is still wanted.

## Validation Status
- `python research/scripts/research.py selftest` → **exit 0**, `Ran 47 tests`, OK
- `python research/scripts/tests_imem.py` → **exit 0**, `Ran 43 tests`, OK
- `python research/scripts/imem.py selftest` → **exit 0**, `Ran 43 tests`, OK, `VERSION 2.0.0 (DEC-0012)`
- `python tools/e0013_extract.py --selftest` → **exit 0**, `SELFTEST PASS checks=112 failed=0`
- `python research/scripts/imem.py lint` → **exit 1**, `problems: 1` — **FND-0030 only** (see above)
- `python research/scripts/research.py update` → **exit 0**
- `python research/scripts/research.py state --write` → **exit 0**
- `python research/scripts/research.py validate` → **exit 0**, `Validation OK`
- Commits: `74aed25`, `a8a902a` (prior session's DEC-0012 work), then this session's records.
  **Not pushed** — parked with this written reason per AGENT_MEGAPROMPT §5.
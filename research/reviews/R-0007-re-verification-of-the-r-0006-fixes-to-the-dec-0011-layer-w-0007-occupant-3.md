---
id: R-0007
type: review
reviewer: verification-auditor, fresh-agent seat, Round 5 occupant 3
target: W-0007 and R-0006 fixes
kind: verification
status: COMPLETED
work_item: W-0007
related: [W-0007, R-0006, DEC-0011, HO-0001, S-0005]
example: false
created: 2026-09-20
---

# R-0007 — Re-verification of the R-0006 fixes to the DEC-0011 derived-intelligence layer (W-0007, occupant 3)

## Scope

Fresh agent, **zero chat history** (this seat is designed to be handed to a model with no
prior context). This review re-verifies the **R-0006 fixes** to the DEC-0011
derived-intelligence layer — the four named defects **G1, G2, G3, G5** — by running the
gates myself, not by reading the fix report. I am not the owner of W-0007, DEC-0011 or
R-0006, and I accepted no prior agent's summary as evidence: every exit code, hash and
count below comes from a command I ran in this session.

Bootstrap (SYSTEM.md §11): `status --brief` → 14 active hypotheses, 6 open disagreements,
3 pending experiments, 7 open work items, 0 open handoffs, 0 live runs, 5 sessions;
`next` → W-0001 (E-0011 pipeline, systems-researcher) with the unresolved E-00004 note;
`validate` → OK (baseline, 0 problems). **Gate 0:** `build\Release\kana.exe` was attempted
**once** as instructed and was HARD-BLOCKED by the host's App Control policy
("Bir Uygulama Denetimi ilkesi bu dosyayı engelledi" — the F-0002 class of block; exit
non-zero, no process started). Per the session mandate I did not retry or work around it;
no engine number was re-proved this session and none is claimed. The whole W-0007
re-verification is pure-Python and does not need the binary.

## Agreements (what reproduced, and how I know)

| # | Command (W-0007's own exit_check set) | Exit | What I observed | Raw output (gitignored) |
|---|---|---|---|---|
| 1 | `python research/scripts/research.py selftest` | 0 | `Ran 41 tests` + `OK` — the "41 tests" claim is exact (was 35 before the fix commit) | `context/va_selftest.txt` |
| 2 | `python research/scripts/research.py validate` | 0 | `Validation OK`, **0 problems**; advisory warnings only (legacy grandfathered records + dangling ids + duplicates), and — new since R-0006 — the audit surface is folded into the same output (`audit[...]` lines appear there; G3). | `context/va_validate.txt` |
| 3 | `python research/scripts/research.py state --write` ×2 | 0 / 0 | `state.json` **byte-identical** across runs: sha256 `2fd14e0a…669e`; `state.md` `b181a24f…c1c9`; command reported "wrote …". | `context/va_state{1,2}.txt`, `va_hash{1,2}.txt` |
| 4 | `python research/scripts/research.py search "quiescence stand-pat"` | 0 | **E-00008 rank 0** (score 10.2646); report hits R-IE-O3C/R-IE-O3B ranked in the same list. | `context/va_search.txt` |
| 5 | `python research/scripts/kgraph.py beliefs --json` | 0 | JSON array, 18 hypotheses, contains H-0001 and a `PROJECTION — …not a fact` banner — the shim executes, it does not merely exist. | `context/va_beliefs.json`, `va_beliefs2.txt` |

Code-level confirmations (read by me, with line numbers): `PERFT_ANCHOR` is now ten
per-count rows (`research.py:94-105`); `_project_state_problems` asserts each count with a
digit-boundary regex on a comma-stripped section view (`research.py:882-891`);
`cmd_validate` calls `memorylib.audit()` and routes its `problems` to validation failures
(`research.py:829-847`); `parse_simple_yaml` parses block sequences (`research.py:213-227`);
`audit()` carries a state-staleness finding (`memorylib.py:687-703`).

## Disagreements / fix verification (the four named defects, re-tested)

All four are **fixed as claimed**, each demonstrated by a mutation or a CLI probe I
designed and ran myself. No new blocking defect was found.

**G1 — perft-anchor coverage. VERIFIED (demonstrated).** Two independent probes agree:
- Direct mutation probe (`context/va_probe_g1g5.py` → `context/va_probe_out2.txt`): every
  one of the ten certified table cells was mutated (+1 inside the `|…|` cell) on a temp
  copy; `_project_state_problems()` reports a SACRED/anchor problem for **10/10**; the
  pristine file passes; removing the section still fails with the F12 "protected home"
  message.
- Sandbox CLI probe (real `research.py validate` on a copy): startpos d1 `20→21`,
  startpos d5 `4865609→4865610`, kiwipete `97,862→97,863` each make `validate` exit 1 with
  the SACRED message (`context/va_gate_anchor_*.txt`). The five startpos counts that
  R-0006 used to demonstrate the hole (20/400/8902/197281/4865609) are all caught now.
- Self-correction, disclosed: my first direct-probe run reported d1 as NOT caught. The
  cause was my probe substituting the **first** occurrence of "20" in the section — which
  is inside the date "2026-09-14" — rather than the table cell. Targeted cell mutation and
  the CLI probe both catch d1. This was a probe bug, not a deliverable bug; the
  digit-boundary regex is precisely what makes the date unable to satisfy a count.

**G2 — stale generated state. VERIFIED (mechanism), with a residual.** `audit()` now
compares `state.json.metrics.records_total` with the live node count. Demonstrated
end-to-end in the sandbox: adding one record to the corpus makes `validate` print
`audit[warning:state]: state.json is stale: stored records_total=123, live=124 — run
state --write and commit` and still exit 0 (correct: advisory); running the sandbox's own
`state --write` removes the warning (`context/va_gate_stale_state.txt`,
`context/va_gate_fresh_state.txt`). The shipped artifact is a fresh projection: my two
regenerations reproduce the committed bytes (sha256 `2fd14e0a…`), and the owner's commit
`6e20e14` includes the regenerated `state.{md,json}`. Residual: staleness is a **warning**,
so by itself it cannot block a round — it can only be loud (see follow-ups).

**G3 — audit ↔ validate unified. VERIFIED (demonstrated).** `validate` now runs
`M.audit()` and appends its `problems` to the failure list. Sandbox probe: a record with
`status: BOGUS` now makes `validate` exit 1 with
`audit[status]: status='BOGUS' not in the hypothesis vocabulary` — exactly the state
R-0006 measured as "audit problems=1 vs validate exit 0" — and the live `validate` output
carries the audit warnings in the same surface (`context/va_gate_bogus_status.txt`,
`context/va_validate.txt`). The mislabel defect went with it: the placeholder report was
re-typed (`type: report`), so no status-less hypothesis remains.

**G5 — block-sequence YAML. VERIFIED (demonstrated).**
- Parser probe: `evidence:\n  - a\n  - b` parses to a list, no junk key is invented from
  `- ` lines (also at EOF), and W-0007's own front-matter `evidence` now parses non-empty,
  so gate 1 sees it.
- Sandbox gate probe: W-0007 set to `DONE` + `VERIFIED` with **inline** evidence → exit 0;
  the same record with the evidence rewritten as a **block sequence** → exit 0 as well
  (`context/va_gate_w0007_done_inline.txt`, `context/va_gate_w0007_done_block.txt`).
  R-0006's failing case B ("DONE without evidence") no longer reproduces.
- Residual nit (non-blocking, below): inline lists are split on **every** comma, not
  quote-aware.

## Missing Arguments / what I could NOT reproduce

- **Gate 0** could not be executed: `kana.exe` is hard-blocked on this host (one attempt,
  App Control policy message, no process start — F-0002 class). No perft, NPS or engine
  behaviour was re-proved by me; none is claimed. The anchor check I verified is a
  document-consistency gate, not an execution of the floor.
- The binary identity check (EV-0010's SHA-256 vs the on-disk `kana.exe`) was **not**
  recomputed by me this session; R-0006 did recompute it and it matched. I treat binary
  identity as unverified this session, unchanged from R-0006's evidence.
- `contradictions` still returns 0 candidates, so R-0005 F16's motivating case remains
  undemonstrated on this corpus (pre-existing, not a fix target).
- No independent CI/LOS implementation was attempted — not applicable to this target.

## Factual Errors / claims corrected

1. `project_state.md` §"Certified Perft Anchors" claims `validate` "asserts every number
   below". This was **false** at R-0006 (five startpos counts unasserted) and is now
   **true** — demonstrated by 10/10 cell mutations being caught. No wording change is
   needed anymore.
2. W-0007's `## Evidence` line about the generated state is now literally true of the
   shipped artifact (regenerated and committed at `6e20e14`); at R-0006 it described the
   mechanism, not what was committed.
3. No new factual errors were found in the fixed deliverable.

## Assumptions

- I read "independently verified" per DEC-0009 gate 3 as `verified_by` ≠ owner **and**
  `verification_verdict: VERIFIED`; the sandbox `w0007_done_*` cases exercise exactly that
  path and pass.
- In the sandbox runner I stubbed `root_hygiene_problems()` to `[]` because the sandbox
  lives under the gitignored `research/context/` scratch tree, whose parent is not a repo
  root; root hygiene is not under test here (it is exercised by the real `validate` runs,
  which pass). The stub is stated, not hidden.
- The state-staleness finding is advisory by design (`findings` → warnings); I did not
  treat exit-0-with-warning as a defect, only as a residual risk.

## Proposed Experiments / follow-ups (not blocking W-0007)

1. Quote-aware (or at least warned) inline-list parsing: W-0007's first evidence item
   contains a comma and is currently parsed as two entries. Impact is cosmetic today
   (the list stays non-empty); fix under W-0006/tooling if lossless evidence strings are
   wanted.
2. Index renderer: `index.md` still carries
   `!!! HO-0001 … status='DONE' … NOT RENDERED` under "Unrendered Records (bug — report
   this)" — there is no "Handoffs (closed)" section, so every closed handoff will stay
   flagged. The self-check is working; the renderer is incomplete. Suggest a
   "Handoffs (closed)" list so that section can return to "(none)".
3. Optional: promote the state-staleness finding from warning to a problem **at round
   close** (or inside `round`), so a stale committed projection can actually block closure.

## Verdict

**VERIFIED** — for the G1/G2/G3/G5 fixes and for W-0007's exit checks, with the residual
nits above, none of which changes any number or gate outcome. Every fix claim was re-tested
by me with a mutation or a CLI probe designed to falsify it, and none failed. What would
change my mind: (i) any mutation of the ten certified counts that `validate` still passes;
(ii) a block-sequence front-matter that gate 1 still rejects; (iii) an `audit` problem that
`validate` still ignores; (iv) a `state --write` pair that is not byte-identical. I looked
for all four; none occurred.

## Date
2026-09-20

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns.

---

<!-- VERIFICATION BLOCK — fill this when kind: verification (see SYSTEM.md §5).
     A verification review is evidence about a work item, not an opinion about it.
     Delete this block (or leave it empty) for kind: critique. -->

## Verification Block (kind: verification only)

- **Work item verified:** W-0007 (round 5) — deliverable = the DEC-0011 layer + the
  R-0006 fixes
- **Verified by:** verification-auditor, fresh-agent seat, Round 5 occupant 3 — not the
  owner of W-0007/DEC-0011/R-0006; accepted no summary as evidence
- **Verdict:** VERIFIED
- **Commands re-run by me (raw output retained in gitignored `research/context/`):**
  1. `research.py selftest` → exit 0; `Ran 41 tests … OK` — `va_selftest.txt`
  2. `research.py validate` → exit 0; `Validation OK`, 0 problems — `va_validate.txt`
  3. `research.py state --write` ×2 → exit 0/0; `state.json` byte-identical,
     sha256 `2fd14e0a5e4fe7fe97d3a8c98bed050c698a5dca024df617c834e12a095b669e` —
     `va_state1.txt`, `va_state2.txt`, `va_hash1.txt`, `va_hash2.txt`
  4. `research.py search "quiescence stand-pat"` → exit 0; E-00008 rank 0 — `va_search.txt`
  5. `kgraph.py beliefs --json` → exit 0; 18 hypotheses — `va_beliefs.json`
  6. `python research/context/va_probe_g1g5.py` → exit 0; ALL PASS — 10/10 anchor
     mutations caught, controls pass, block-YAML probes pass — `va_probe_out2.txt`
  7. `python research/context/va_sandbox_driver.py` → exit 0; **9/9** sandbox cases
     behaved as designed — `va_sandbox_out.txt` (+ per-case `va_gate_*.txt`)
  8. `build\Release\kana.exe` → **blocked** (App Control policy; F-0002 class), one
     attempt only — recorded in this review and the session record; no engine claim made
- **Artifacts checked (SHA-256 recomputed by me at HEAD `6e20e14`):**
  - `research/scripts/research.py` — `db96474be09e45a59bc573b1defe135eebeaed84f75490af180bcaf1b0433924`
  - `research/scripts/memorylib.py` — `ade7b833468123fb76905d3710dd81323929cdf809033cb2b7c330af04b14746`
  - `research/scripts/tests_memory.py` — `bb263dfac066e26c8749e3b4564c8460ebc9f0d2aa04a3b7420fe73f5ac238c1`
  - `research/state.json` — `2fd14e0a5e4fe7fe97d3a8c98bed050c698a5dca024df617c834e12a095b669e`
  - `research/state.md` — `b181a24f74604b42eac21c835fb024c5b1d0bd0952e59c3feaa38011a244c1c9`
  - `research/project_state.md` — its anchor table is asserted cell-by-cell by the probes
    above rather than by a whole-file hash.
- **What I reproduced independently:** all five exit-check commands; the G1 hole closed for
  all ten counts; G2 staleness detection (on→off after `state --write`); G3 audit→validate
  problem propagation; G5 block-sequence parsing and the previously blocked DONE path.
- **What I could NOT reproduce (and why):** Gate 0 (host App Control block, F-0002);
  EV-0010's binary hash (not recomputed; R-0006's value stands as their evidence);
  the contradiction-detector's motivating case (still 0 candidates).
- **Sample validity re-checked (adapted for a deterministic tool):** *arm
  differentiation* → designed-fault injection: 3/3 anchor CLI mutations caught, bogus
  status caught, stale vs fresh state behaved oppositely, DONE cases accepted — every
  designed behaviour fired. *Independence* → sandbox is a byte copy in gitignored scratch,
  one fresh subprocess per case; all mutations confined to copies/temp files; before my own
  record edits, `git status` showed only the regenerated `state.{json,md}`. *Power* → n/a
  (deterministic); `state --write` ×2 byte-identical; selftest/validate repeated.
- **Claims that must be corrected in the record:** none material; W-0007's `## Evidence`
  is now accurate (its R-0006 caveat is resolved by regeneration + commit `6e20e14`);
  `project_state.md`'s anchor guarantee is now true.
- **Residual uncertainty (calibrated):** that G1 coverage holds for all ten counts —
  **demonstrated**; that G5 handles the corpus's YAML styles — **demonstrated** for
  inline + block + EOF forms; that `validate` and `audit` can no longer diverge on
  `problems` — **demonstrated** for a status fault; that the state artifact stays fresh —
  **strongly supported** (the warning path is demonstrated; enforcement is advisory only,
  so freshness depends on commit-time discipline); engine floor — **unknown this session**
  (Gate 0 blocked).
- **Auditor operational note (workspace hygiene, not a deliverable defect):** my first
  sandbox build used `robocopy` with the destination **inside** the source and a relative
  `/XD` exclusion; the copy recursed into itself. I detected it via the repo search index
  (647 → 3269 files), killed it, and removed the tree (marker `GONE`); nothing outside
  gitignored `research/context/` was touched. The successful probes use
  `shutil.copytree` with the containing scratch directory ignored and one fresh
  subprocess per case. Recorded because the session record must state what happened to
  the workspace.


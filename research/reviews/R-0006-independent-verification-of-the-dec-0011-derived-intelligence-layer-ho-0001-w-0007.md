---
id: R-0006
type: review
reviewer: verification-auditor (fresh-agent seat, Round 5 occupant 2)
target: W-0007 / HO-0001 (DEC-0011 derived-intelligence layer)
kind: verification
work_item: W-0007
related: [HO-0001, W-0007, DEC-0011, R-0005, S-0004]
status: COMPLETED
example: false
created: 2026-09-19
---

# R-0006 — Independent verification of the DEC-0011 derived-intelligence layer (HO-0001 / W-0007)

## Scope

Fresh agent, **zero chat history**, bootstrapped from the repository alone
(`README` → `AGENT_MEGAPROMPT` → `agents/ASSIGNMENTS.md` → `verification-auditor/profile.md`
→ `SYSTEM.md` → `SCHEMA.md` → `project_state.md`). I am **not** the owner of W-0007, of
DEC-0011, or of any record verified here, and I accepted **no** prior agent's summary as
evidence: every exit code, hash and count below was produced by a command I ran myself in
this session. The builder's own captures (e.g. `context/_validate_final.txt`) were read
only to know what to test, never as proof.

Bootstrap: `status --brief` → 14 active hypotheses, 6 open disagreements, 3 pending
experiments, 7 open work items, 1 open handoff (HO-0001 = mine), 0 live runs, 3 sessions.
`next` → W-0001 then HO-0001. `validate` → OK.

**Gate 0 could not be executed** this session (20/20 attempts blocked by Device Guard,
exit 4551 — see **G4b**). No engine count was reproduced by me; that is stated as a limit,
not hidden.

## Agreements (what reproduced, and how I know)

| # | Command (HO-0001's own list) | Exit | What I observed | Raw output retained |
|---|---|---|---|---|
| 1 | `research.py selftest` | 0 | `Ran 35 tests` + `OK` — the "35 tests" claim is exact | `context/_ho0001_selftest.txt` |
| 2 | `research.py validate` | 0 | `Validation OK`, **0 problems**, 18 advisory warnings (9 grandfathered legacy pre-registration, 9 dangling-id) | `context/_v2_validate.txt` |
| 3 | `research.py state --write` ×2 | 0/0 | `state.json` **byte-identical** across runs (sha256 `f57fd375230b37cd9a4c9a32b2c52da03358f2e624af684369d4cc25828c353b`), equal raw **and** with the `generated` stamp stripped; `state.md` likewise | `context/_v2_state_run{1,2}.*`, `_ho0001_report2.txt` |
| 4 | `research.py search "quiescence stand-pat"` | 0 | **E-00008 rank 0** (score 10.6327); keys `hits/query/related`; agent **reports** ranked in the same list (R-IE-O3C 9.6939, R-IE-O3B 6.1917) | `context/_v2_search.json` |
| 5 | `kgraph.py beliefs --json` | 0 | JSON array, n=18 hypotheses, contains `H-0001` — the shim works, not just exists | `context/_v2_kgraph_beliefs.json` |

Two claims a summary could not have settled, and that I settled myself:

- **Artifact identity.** I recomputed `build\Release\kana.exe` → `504EB01A828770DD9BFCA252AB8245A5692DF51580957CB6E5553012347A6DAA`, identical to **EV-0010**'s recorded hash. The binary on disk *is* the E-0010 measurement binary — verified without executing it.
- **The gates have teeth (adversarial mutation on a sandbox copy of `research/`; the real corpus was never modified).** `bogus-status` → exit 1; `W-0007 status: DONE` → exit 1 (`DONE without evidence` / `but not independently verified`); `HO-0001`'s `work_item` repointed at a non-existent id → exit 1 (the `validate` cross-check `work_item=… does not exist in research/work/`); anchor heading removed → exit 1; `kiwipete 97,862→97,863` → exit 1; `cpw6 3,894,594→3,894,595` → exit 1; **EV-0010 sha256 falsified → exit 1** with `evidence EV-0010: sha256 drift on build/Release/kana.exe`; evidence path missing → warning + exit 0; `round --round 5` → exit 1 with `[FAIL] W-0007 OPEN`. This independently confirms — rather than repeats — S-0003's claim that the system rejected its own author's DONE claim (DEC-0009 gate 3), and it confirms the F12 / evidence-drift checks fire. (The token used for the non-existent work item is deliberately not written here: the id-extractor would otherwise file a new dangling link, which is itself how the layer policed this review — see G5a.)

## Disagreements (named gaps — this is why the verdict is not VERIFIED)

**G1 — The SACRED perft anchor's first row is not actually asserted. (gate defect)**
`research.py:_project_state_problems` tests `if not any(v in flat for v in variants)`, and
`PERFT_ANCHOR[0] = ("startpos d1-5", ("20","400","8902","197281","4865609"))` lists **five
different counts as if they were alternative spellings of one**. So the row is certified if
*any one* of the five survives — and `"20"` always survives, because the section itself
contains the date `2026-09-14`. Demonstrated with four independent mutations of the
certified table (each number appears **once** in `project_state.md`; confirmed by line
search, so no prose copy was hit):

| Mutation in the certified table | validate | Expected |
|---|---|---|
| `4865609 → 4865610` | **exit 0, "Validation OK"** | exit 1 |
| `197281 → 197282` | **exit 0, "Validation OK"** | exit 1 |
| `8902 → 8903` | **exit 0, "Validation OK"** | exit 1 |
| `400 → 401` | **exit 0, "Validation OK"** | exit 1 |
| `97,862 → 97,863` (control) | exit 1, SACRED message | exit 1 ✓ |
| section heading removed (control) | exit 1, "one protected home" | exit 1 ✓ |

Five of the ten certified counts (startpos d1–d5) can be altered while validation stays
green. The other five rows *are* protected, so the gate is partially working — a coverage
bug, not a dead check. Fix (owner/tooling — outside my write authority): one row per count,
or assert the space-stripped table cells (`|4865609|`), or require every variant.

**G2 — The Layer-3 state that was committed was stale.** Committed `state.md` says
`Generated: 2026-09-19T18:42:45`; commit `4dbb89e` is 19:17:41. Regenerating from that
same corpus gives `records_total 119` (committed 118), `session 3` (2), `CLOSED 3` (2),
`edges_total 866` (852), and the timeline tail swaps in S-0003 for HO-0001. So S-0003 (and
HO-0001) landed **after** the state was generated, and the state was not regenerated before
the commit — though S-0003's "State Left On Disk" claims `state.md`/`state.json` were
written and W-0007's evidence says they were "written and deterministic". The determinism
claim is true of the *mechanism*; the *shipped artifact* was a stale projection — the very
F7/F21 drift the layer exists to catch, inside the layer's own deliverable. My two
verification runs have since regenerated both files, so the working tree now carries the
corrected generated output (20-line diff) which the owner should commit. They are GENERATED
files: nobody should hand-edit them.

**G3 — `audit`'s `problems` channel is orphaned from `validate`, and one message is
mislabelled.** `audit --json` → `problems=1`: `status='—' not in the hypothesis
vocabulary`, while `validate` → exit 0 / "Validation OK". Traced by me: exactly **one**
node carries a status-less `type: hypothesis` —
`agents/researcher-architect/reports/2026-09-09-placeholder.md` (36 status-less nodes
exist; the other 35 are ungated kinds: doc/report/profile/current_position/beliefs).
`cmd_validate` never calls `M.audit()`; it re-implements three advisory checks
(`missing_reference_targets` → warnings, `evidence_inventory` → warnings/problems,
`contradiction_candidates` → warnings). Consequences: DEC-0011 §6's "A memory-integrity
audit (`audit`) feeding `validate` advisory checks" is only partly implemented;
`audit()`'s own docstring ("`problems` should block closing a round") is enforced nowhere;
and the layer's two surfaces disagree about "problems == 0" — the very wording HO-0001's
acceptance criterion uses. The message also hard-codes "the hypothesis vocabulary"
whatever the record's kind, so for a mis-typed placeholder report it points the reader at
the wrong directory. Impact: no false PASS of a gated record; a real but narrow blind spot.

**G4 — HO-0001's second acceptance clause is literally false.** Text: *"No record under
`research/` was edited or deleted by the layer (git diff shows 0 touched existing records;
only new files)."* Measured with `git diff --name-status 7162357 4dbb89e`: **5 existing
files modified** — `research/README.md`, `research/SYSTEM.md`, `research/index.md`,
`research/project_state.md`, `research/scripts/research.py` — plus 37 added. Split verdict,
because the clause conflates two different things:
*(a) demonstrated:* **zero deletions** (`--diff-filter=D` empty), and **zero modified files
in any record directory** (hypotheses/decisions/experiments/failures/reviews/debates/work/
handoffs/sessions/agents/templates — `--diff-filter=M` empty for all of them). At code level
the layer is read-only w.r.t. records: `memorylib.run_derived` writes exactly
`research/state.json` and `research/state.md` (lines 883-886); every other derived command
only prints. The append-only store is intact.
*(b) contradicted:* four documents plus the CLI were touched, and one of them is the FACTS
file `project_state.md` (`last_updated 2026-09-14→2026-09-19`, `reflects += DEC-0011`) —
a *required* DEC-0009 staleness update, which is precisely why the literal clause cannot
hold in a correct commit. Recommended rewording: state the invariant (no record in a record
directory modified, nothing deleted, the layer writes only generated state), not a git-diff
count that the DEC-0009 update rule must break.

**G4b — Environment (not the deliverable): Gate 0 was unexecutable.** Every invocation of
`kana.exe` returned **exit 4551, "blocked by your organization's Device Guard policy"**:
20 attempts inside the documented retry loop, plus `build\Audit\kana.exe`, plus a copy of
the Release exe outside `build/`, plus `runjob.py launch --retry 8` (which raises
`WinError 4551` inside `CreateProcess`). The documented "freshly built unsigned exe"
intermittence is therefore currently a **hard, non-transient block**, and `retry_rel.bat` /
`runjob.py` cannot work around it. Per `AGENT_MEGAPROMPT` §5 this is an escalation, not a
regression: no wrong count was observed — no count could be observed at all. Narrower
consequence for this layer: `validate`'s phrase "the perft anchor … verified" is a
*document-consistency* check only; it cannot and does not execute the engine (EV-0003's
`regenerate` requires the binary to run).

**G5 — A block-style YAML list is invisible to the tooling, so gate 1 falsely rejects a
correct DONE. (gate defect; blocks Round-5 closure)**
`research.py:parse_simple_yaml` documents itself as "scalars, inline lists, bools", and it does
not read **block sequences**. W-0007 writes its three `evidence:` entries as a block sequence,
so the tooling parses `evidence → None` (and invents a junk key from the first `- ` line).
Demonstrated in a sandbox copy, same record, same evidence content, only the YAML style differs:

| Case (W-0007 in the sandbox) | validate | round 5 |
|---|---|---|
| A: left OPEN (baseline) | exit 0 | exit 1, `status=OPEN … no evidence` |
| B: `status: DONE` + `verified_by` + `verification_verdict: VERIFIED`, evidence **block** style | **exit 1 — `work/W-0007-derived-intelligence-layer.md: DONE without evidence (DEC-0009 gate 1)`** | exit 0, `[PASS] W-0007 … DONE` |
| C: same as B but `evidence:` rewritten as an **inline** list | exit 0 | exit 0, `[PASS]` |

So a work item that *does* carry evidence is rejected for having none, and the two gates
disagree about the same record (`cmd_round` only consults `evidence`/`exit_check` when the item
is not already DONE+VERIFIED). **Practical consequence: the Round-5 closer cannot have W-0007
DONE *and* `validate` green** until either W-0007's `evidence:` is rewritten as an inline list
(owner's record, one line) or the parser learns block sequences. Blast radius today is one
record — a sweep of every `.md` under `research/` found only W-0007 using a block list in
front-matter, and `templates/work_item.md` emits inline lists, so the style was never taught by
the tooling — but the cost lands exactly on the item under verification. This is the same
*silent-drop* failure class as R-0003 F8 (the record that vanished), which DEC-0009 was written
to prevent.

**G5a — the layer policed this review, correctly.** Writing the literal example id of a
non-existent work item into my first draft produced a **new** `validate` warning —
`dangling id …` (the letter `W` plus four nines) attributed to `reviews/R-0006-…`. I reworded
it away, and I note the digits here rather than the token so the extractor does not fire on this
sentence. Recorded because it is evidence the dangling-id check works on *new* artifacts, not
just the legacy ones (R-0005 F24), and because my own session record must not silently leave
that warning behind.

## Missing Arguments

- The handoff specifies no criterion for the **content** of the generated state, only that
  it is deterministic — which is exactly how a stale-but-deterministic artifact (G2) ships
  under a green exit check.
- No acceptance item covers `validate`'s blind spot (G3), so an `audit` problem can never
  block anything.
- No criterion requires per-count coverage of the anchor table (G1); "the section is
  asserted" was read as "every number is asserted".

## Factual Errors

1. `project_state.md` §"Certified Perft Anchors" (lines 53-55) overstates the machine
   guarantee: *"`research.py validate` asserts every number below; deleting or altering the
   section fails validation loudly."* With `PERFT_ANCHOR` row 1 as written, altering
   `4865609` (or `20` / `400` / `8902` / `197281`) does **not** fail validation — four
   mutations, exit 0 each (G1). The section-presence and the other five rows do fail loudly.
2. W-0007's Evidence line *"state --write run: state.json/state.md written and
   deterministic"* is true of the command and misleading about what was committed (G2).
3. R-0005 F16 presents `contradictions` as the fix for the H-0005 backwards-bound and the
   H-0006-vs-D-0003 conflicts; today `contradictions` returns **0** candidates, so the
   detector's ability to fire on its documented motivating case is **not demonstrated** by
   this corpus (it may be moot after the 2026-09-09 renumbering — I could not tell from the
   records). Flagged as unverified, not as false.

## Assumptions

- I read "no record rewritten" as "no record in a record directory modified and no
  deletions", because DEC-0009's own staleness rule *requires* `project_state.md` to be
  updated when a final record lands; the literal reading is unsatisfiable in a correct
  commit (G4).
- The two `state --write` runs fell inside the same second, so raw byte-equality does not by
  itself prove timestamp-independence. The stripped comparison is the meaningful evidence and
  it also passes; both are recorded.
- `AGENT_MEGAPROMPT` §5's "Gate 0 fails ⇒ stop and escalate" is treated as covering this
  case. I did not proceed to *engine* claims, and I did not let the unmet precondition
  silently degrade the record: it is stated in the Scope, in G4b, and in the session record.

## Proposed Experiments

1. **Make G1 a permanent self-test.** `tests_memory.py` should assert that mutating each
   certified count one at a time makes `validate` exit non-zero — this review's exact
   T1a-T1d/T2/T3 probe, turned into a regression test.
2. **Wire `audit()` into `validate`** (or stop calling its advisory channel "problems"), and
   add a self-test that the two surfaces agree on the problem set (G3).
3. **Stale-state check.** Compare the generated `generated` stamp against the newest record
   date and fail/warn if the projection predates the corpus; plus an idempotence self-test on
   a fixed corpus fixture (G2).
4. **Contradiction-detector validation** for R-0005 F16 using the same sandbox technique:
   synthesize a known-conflicting pair and show `contradictions` fires.
5. **Gate 0 environment remediation (owner action).** Allow-list the exe or run Gate 0 where
   WDAC permits execution, and record the outcome as an environment fact so the next fresh
   agent does not spend a session discovering it (G4b).

## Verdict

**PARTIAL.** Every exit check HO-0001 asked for reproduced green under my own commands
(selftest 35/35, validate OK, `state --write` twice byte-identical, search → E-00008 rank 0,
`kgraph.py` shim working), and I additionally demonstrated by adversarial mutation that the
DEC-0009 gates, the evidence-drift check and the anchor *presence* check have real teeth.
But the deliverable carries four defects — **G1** (five of ten certified counts unasserted),
**G5** (a block-style `evidence:` list is invisible to the parser, so gate 1 would falsely
reject W-0007's own DONE claim — and `validate` and `round` disagree about it, which is a hard
blocker for closing Round 5), **G2** (the committed Layer-3 state was stale) and **G3**
(`audit` problems orphaned from `validate`) — and one of HO-0001's acceptance clauses is
literally false (**G4**). A blanket VERIFIED would launder those; a blanket CONTRADICTED would
misrepresent a layer that does work as specified on every command it was asked to run.
**W-0007 must not move to DONE on this verdict** (DEC-0009 gate 3 requires `VERIFIED`): the
owner should fix G5 (one line: inline the evidence list) and G1 (split the anchor row), decide
G3, and re-verify. G2's artifact is already correct on disk (regenerated by my verification
runs) and needs a commit. One of my own drafts was caught by the layer during this review
(G5a) — which is the strongest evidence that the layer's checks are live on new artifacts.

## Date
2026-09-19

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns.

---

<!-- VERIFICATION BLOCK — fill this when kind: verification (see SYSTEM.md §5).
     A verification review is evidence about a work item, not an opinion about it.
     Delete this block (or leave it empty) for kind: critique. -->

## Verification Block (kind: verification only)

- **Work item verified:** W-0007 (round 5) via handoff HO-0001; target artifacts
  `research/scripts/{memorylib.py,research.py,kgraph.py,tests_memory.py}`, `research/SCHEMA.md`,
  `research/state.{md,json}`.
- **Verified by:** `verification-auditor` (fresh-agent seat, Round 5 occupant 2; zero chat
  history). **Not** the owner of W-0007, DEC-0011, R-0005 or any verified record.
- **Verdict:** **PARTIAL** — every requested exit check reproduced green; four defects
  (G1/G5/G2/G3) and one false acceptance clause (G4) are named above; Gate 0 unexecutable (G4b).
- **Commands re-run by me (raw output retained):**
  1. `python research/scripts/research.py selftest` → exit 0; `Ran 35 tests` … `OK`.
  2. `python research/scripts/research.py validate` → exit 0; `Validation OK`, 0 problems, 18 advisory warnings.
  3. `python research/scripts/research.py state --write` (×2) → exit 0/0; byte-identical `state.json` (sha256 `f57fd375230b37cd9a4c9a32b2c52da03358f2e624af684369d4cc25828c353b`) and `state.md`, raw and timestamp-stripped.
  4. `python research/scripts/research.py search "quiescence stand-pat"` → exit 0; E-00008 rank 0 (10.6327).
  5. `python research/scripts/kgraph.py beliefs --json` → exit 0; JSON array n=18, contains `H-0001`.
  6. `python research/scripts/research.py audit --json` → exit 0; `problems=1`, `warnings=7` (G3).
  7. `python research/scripts/research.py round --round 5` → exit 1 (W-0007 OPEN/unverified — correct).
  8. `git diff --name-status 7162357 4dbb89e` → 5 M, 37 A, 0 D (G4).
  9. Sandbox mutation suite (`research/context/_ho0001_probe{3,4,5,8,9}.py`) → 6 gates exit 1 as designed; 4 anchor mutations exit 0 (**G1**); DONE+VERIFIED with block-style evidence exit 1 vs the same record with inline evidence exit 0 (**G5**), while `round` reports PASS in both.
  10. `Get-FileHash build\Release\kana.exe -Algorithm SHA256` → `504EB01A…A6DAA`.
- **Artifacts checked (recomputed, not copied):**
  `build/Release/kana.exe` — `504EB01A828770DD9BFCA252AB8245A5692DF51580957CB6E5553012347A6DAA`,
  matching EV-0010; `research/state.json` — `f57fd375…` (twice, identical). Raw captures live
  under gitignored `research/context/` (`_ho0001_report{,2,3,4,5,6}.txt`, `_v2_*`, `_gate0_auditor*`).
- **What I reproduced independently:** every HO-0001 exit check; the "35 tests" count; the
  determinism of `state --write`; E-00008 at rank 0 with reports in the hit list; the kgraph
  shim; the DEC-0009 gate-1/gate-3 behaviour (by mutation, including the DONE-without-verification
  rejection S-0003 reported); the evidence sha256-drift check (fired on a falsified EV-0010);
  the anchor section-presence and five of six anchor rows; zero deletions and zero record-directory
  modifications in the DEC-0011 commit.
- **What I could NOT reproduce (and why):** (i) **Gate 0** — every `kana.exe` is blocked by
  Device Guard (exit 4551); no perft count, NPS number, or engine test result was produced by me
  this session (G4b). (ii) **The anchor gate's coverage of the startpos row** — it does not exist
  to reproduce; four mutations show it is absent (G1). (iii) `contradictions` firing on the
  conflicts R-0005 F16 cites — 0 candidates today. (iv) A genuinely independent CI/LOS
  implementation (n/a for this target).
- **Sample validity re-checked (adapted — this is a deterministic tool, not a statistical
  experiment):** *arm differentiation* → n/a; the equivalent control is the sandbox mutation
  suite, where each injected fault did/did not move the exit code as designed (6/6 designed
  gates fired; 4/4 anchor mutations did not — that asymmetry is the finding). *Independence* →
  the sandbox is a byte-copy of the corpus re-run by a different entry point, and I verified the
  real corpus was untouched afterwards (`git status` shows only the two generated state files
  changed). *Power/robustness* → `state --write` was run 4× total across two probes with
  identical output.
- **Claims that must be corrected in the record:**
  1. `project_state.md` lines 53-55 ("`validate` asserts every number below") — false for the
     five startpos counts until `PERFT_ANCHOR` row 1 is split (G1).
  2. W-0007's `## Evidence` line about the generated state — clarify that the *committed*
     `state.{md,json}` were stale (G2).
  3. HO-0001's "0 touched existing records; only new files" — replace with the real invariant (G4).
  4. DEC-0011 §6's "`audit` … feeding `validate` advisory checks" — only partly implemented (G3).
  5. `research/scripts/research.py:parse_simple_yaml` — its docstring ("scalars, inline lists,
     bools") is accurate, but nothing warns an author that a block list in front-matter is
     silently dropped (G5). Either parse block sequences or have `validate` flag them.
  6. W-0007's own front-matter: `evidence:` must be an inline list for gate 1 to see it (G5).
- **Residual uncertainty (calibrated):** that the derived layer behaves as specified on every
  command in HO-0001 — **demonstrated**. That the append-only store was never rewritten —
  **demonstrated** for the DEC-0011 commit (git) and at code level (only `state.*` is written).
  That the gates have teeth — **demonstrated** for the six checks listed, **not for the startpos
  anchor row** (G1, demonstrated absent), and gate 1 mis-reads W-0007's block-style `evidence`
  (G5, demonstrated: false "DONE without evidence"). That the engine floor still passes — **unknown this
  session** (Gate 0 blocked; EV-0010's hash does match the on-disk binary, so artifact identity
  is intact even though execution is not). That R-0005 F16's contradiction detector fires on its
  motivating case — **unverified**.

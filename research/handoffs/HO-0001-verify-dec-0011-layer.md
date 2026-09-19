---
id: HO-0001
type: handoff
from: chief-architect
to: verification-auditor
work_item: W-0007
status: DONE
title: "Independently verify the DEC-0011 derived-intelligence layer"
artifacts: [research/scripts/memorylib.py, research/scripts/kgraph.py, research/scripts/research.py, research/scripts/tests_memory.py, research/SCHEMA.md]
commands: []
acceptance: "selftest OK AND validate OK AND state --write deterministic AND no existing record rewritten/lost"
example: false
created: 2026-09-19
closed: 2026-09-19
---

# HO-0001 — Verify the derived-intelligence layer (W-0007)

> Take this from a zero-history seat (the rotating verification-auditor). Do not accept the
> builder's summary. Re-run everything yourself.

## Request
Bootstrap per `AGENT_MEGAPROMPT.md` §§0-1, then verify DEC-0011's delivery end-to-end.

## Artifacts To Read (paths)
- `research/scripts/memorylib.py`, `research/scripts/research.py`, `research/scripts/kgraph.py`,
  `research/scripts/tests_memory.py`, `research/SCHEMA.md`, this file.

## Commands To Run
```powershell
python research/scripts/research.py selftest            # expect: 35 tests OK, exit 0
python research/scripts/research.py validate            # expect: OK (problems == 0)
python research/scripts/research.py state --write        # writes state.md + state.json
python research/scripts/research.py state --write        # IMMEDIATELY re-run: deterministic (state.json unchanged modulo `generated`)
python research/scripts/research.py search "quiescence stand-pat"   # expect: E-00008 among top hits
python research/scripts/kgraph.py beliefs --json        # compat shim works
```

## Acceptance Criteria (what makes this DONE)
- All commands exit 0 and produce the expected structure.
- No record under `research/` was edited or deleted by the layer (git diff shows 0 touched
  existing records; only new files).
- `state --write` twice produces byte-identical `state.json` after stripping the
  `generated` timestamp.

## Response (receiver, append-only)
- 2026-09-19 — **verification-auditor (fresh-agent seat, Round 5 occupant 2), zero chat
  history.** Accepted HO-0001 and executed every command in "Commands To Run", each from my
  own shell, raw output retained under gitignored `research/context/`. Result: selftest
  exit 0 (`Ran 35 tests` … `OK`); validate exit 0 (`Validation OK`, 0 problems, 18 advisory
  warnings); `state --write` ×2 exit 0/0 with **byte-identical** `state.json` and `state.md`
  (raw *and* with the `generated` stamp stripped — stronger than the criterion asked);
  `search "quiescence stand-pat"` exit 0 with **E-00008 rank 0** (10.6327) and agent reports
  in the same hit list; `kgraph.py beliefs --json` exit 0 (JSON array, n=18, contains
  H-0001). I additionally recomputed `build\Release\kana.exe` =
  `504EB01A828770DD9BFCA252AB8245A5692DF51580957CB6E5553012347A6DAA` (= EV-0010), and ran
  an adversarial mutation suite against a **sandbox copy** of `research/` (the real corpus was
  never modified) to test that the gates still bite. Verdict: **PARTIAL** — full detail,
  including four named gaps, in `research/reviews/R-0006-…md`; the gate findings are also
  proposed there as permanent self-tests.
- The three acceptance clauses, one by one: (1) selftest OK — **met**; (2) validate OK with
  0 problems — **met** (note: `audit --json` reports `problems=1` for a status-less
  `type: hypothesis` placeholder report that `validate` never sees — gap G3); (3)
  `state --write` deterministic — **met, and exceeded**. (4) "no record rewritten/lost" —
  **met in substance, false as literally worded**: the DEC-0011 commit touched 5 existing
  files (README/SYSTEM/index/`project_state.md`/`research.py`) with **zero deletions** and
  **zero modified files in any record directory**; `project_state.md` had to change because
  DEC-0009's staleness gate requires it. Recommend rewording the clause to that invariant.

- Addendum (same session, after the first pass of my review): a **fourth** defect — **G5** —
  was found by probing the gate rather than reading it. W-0007's own `evidence:` field is a
  YAML **block sequence**, which `research.py:parse_simple_yaml` does not parse, so the tooling
  sees `evidence = None`. Consequence, demonstrated in a sandbox copy: setting W-0007 to
  `DONE` + `VERIFIED` makes `validate` exit 1 with "DONE without evidence (DEC-0009 gate 1)"
  while `round --round 5` prints `[PASS]` for that same state, and rewriting the identical
  three entries as an inline list makes validate exit 0. So **the Round-5 closer cannot have
  W-0007 DONE *and* validate green** until that one field's YAML style is fixed (owner's edit)
  or the parser learns block sequences. See R-0006 G5/G5a.
## Verification (receiver, append-only)

- raw output / exit codes / recomputed hashes:
  - `research.py selftest` → exit 0; `Ran 35 tests in 1.475s` / `OK` (`context/_ho0001_selftest.txt`).
  - `research.py validate` → exit 0; `Validation OK` (`context/_v2_validate.txt`).
  - `research.py state --write` ×2 → exit 0/0; `state.json` sha256 `f57fd375230b37cd9a4c9a32b2c52da03358f2e624af684369d4cc25828c353b` both times (`context/_ho0001_report2.txt`).
  - `research.py search "quiescence stand-pat"` → exit 0; E-00008 rank 0, 10.6327 (`context/_v2_search.json`).
  - `python research/scripts/kgraph.py beliefs --json` → exit 0; array n=18 (`context/_v2_kgraph_beliefs.json`).
  - `Get-FileHash build\Release\kana.exe` → `504EB01A…A6DAA` (= EV-0010) (`context/_ho0001_kana_sha.txt`).
  - `git diff --name-status 7162357 4dbb89e` → 5 M / 37 A / **0 D** (`context/_ho0001_fullnm.txt`).
  - Gate-0 attempts: **20/20 exit 4551** ("blocked by your organization's Device Guard
    policy"), also for `build\Audit\kana.exe`, a copy outside `build/`, and
    `runjob.py launch --retry 8` (`context/_gate0_auditor_attempts.txt`). The correctness
    floor is UNVERIFIABLE in this environment — escalated, not silently skipped.
  - Sandbox mutation suite → 6 designed gates fire (bad status, DONE-unverified, dangling
    handoff work_item, anchor section removed, kiwipete count, cpw6 count, EV-0010 sha drift);
    **4/4 startpos anchor mutations do NOT fire** (`context/_ho0001_report{3,4,5}.txt`).
- verdict: **PARTIAL** (not VERIFIED). Every exit check in this handoff reproduced green by a
  zero-history agent, but the verified deliverable contains four defects — G1: `PERFT_ANCHOR`
  row 1 lists five distinct startpos counts as if they were spelling variants, so
  `any(v in flat …)` leaves **20 / 400 / 8902 / 197281 / 4865609 unasserted** (four mutations,
  validate still exit 0) while `project_state.md` claims they are asserted; G2: the committed
  `state.md`/`state.json` were generated at 18:42:45 and committed at 19:17:41, i.e. stale by
  one record and 14 edges (S-0003 landed after generation; regenerated by me, needs a commit);
  G3: `audit`'s `problems` channel is orphaned from `validate` (DEC-0011 §6 only partly
  implemented) and its message misnames the vocabulary; G5: W-0007's block-style `evidence:`
  list is invisible to the parser, so a correct DONE+VERIFIED state makes `validate` exit 1
  ("DONE without evidence", gate 1) while `round` says `[PASS]` — a false rejection and a
  Round-5 closure blocker (probe #9). Full detail in
  `research/reviews/R-0006-independent-verification-of-the-dec-0011-derived-intelligence-layer-ho-0001-w-0007.md`.
  Because the verdict is PARTIAL, DEC-0009 gate 3 forbids W-0007 moving to DONE on my
  verification: the owner must either fix G1/G5 (and decide G2/G3) and re-verify, or explicitly
  record the gaps as accepted follow-ups.
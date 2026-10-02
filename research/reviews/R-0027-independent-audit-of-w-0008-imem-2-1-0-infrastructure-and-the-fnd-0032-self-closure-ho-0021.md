---
id: R-0027
type: review
reviewer: verification-auditor
target: W-0008
kind: verification
status: COMPLETED
work_item: W-0008
related: [HO-0021, W-0008, FND-0032, DEC-0012, S-0043, INFRASTRUCTURE.md, SCHEMA.md, research/scripts/imem.py, research/scripts/imem_meta.py, research/scripts/imem_claims.py, research/scripts/imem_core.py, research/scripts/tests_imem.py]
example: false
created: 2026-10-02
---

# R-0027 — Independent audit of W-0008 (imem 2.1.0 + INFRASTRUCTURE.md) and the FND-0032 self-closure (HO-0021)

> **Seat:** `verification-auditor`. I am not W-0008's owner (`chief-architect`), and I did not
> author the FND-0032 closure (its `resolved_by`/`verified_by` name `chief-architect`). Gate 3
> is satisfied on both: `verified_by != owner`. Every number below was produced by a command I
> ran this session; the raw output is retained under `_obs/ho0021/`.

## Scope

Two related, self-witnessed contents were routed for Gate-3 re-derivation as **HO-0021**:

1. **W-0008** — the imem 2.1.0 infrastructure additions (`INFRASTRUCTURE.md`, the `freshness`
   and `novelty` surfaces, the 5 new tests, the `chief-architect` seat), against its stated
   `exit_check` and cited evidence.
2. **FND-0032** — a finding filed *and closed* by the same seat, on the DEC-0012 vocabulary
   erratum: is `RESOLVED`-with-erratum justified, and was append-only discipline respected?

**Bottom line: W-0008 is VERIFIED** (every gate exits 0 and every listed row/candidate
reproduces exactly; three numbered annotation-level defects are recorded, none gate-failing),
**and the FND-0032 closure is JUSTIFIED** (the defect was real, the erratum exists and is
correct, the closure is attributable, and no history was rewritten). One latent robustness gap
in the freshness policy was constructed and is recorded as D-4.

## Verdicts

| Object | Verdict | Basis |
|---|---|---|
| **W-0008** (imem 2.1.0 + INFRASTRUCTURE.md) | **VERIFIED** | All 7 cited gates + 3 extra exits 0; `freshness` = the 10 named ids; `novelty CLM-0001` = [CLM-0003, H-0013]; deliverable present on disk. Defects D-2/D-3 are annotations in W-0008's own prose, not exit checks. |
| **FND-0032** closure (RESOLVED + erratum) | **JUSTIFIED** | The vocabulary defect reproduces (no `CLOSED` in the imem pair; `--close` writes `RESOLVED`); DEC-0012's erratum is appended, not rewritten; the closure is attributable and dated. Defect D-1 is a stale line pointer, not a false closure. |

## Commands run, and what I observed

Every command was executed by me from the repo root; output redirected to a file under
`_obs/ho0021/` and read back (SYSTEM.md §6: the harness's own report is not evidence).
UTF-8 capture was done by a stdlib driver (`_obs/ho0021/run_gates.py`) because PowerShell `>`
re-encodes to UTF-16 (a documented environment hazard).

| # | Command | Exit | Observed (raw file) |
|---|---|---|---|
| 1 | `python research/scripts/tests_imem.py` | **0** | `Ran 48 tests … OK` (`g1_tests_imem.txt`) |
| 2 | `python research/scripts/research.py selftest` | **0** | `Ran 47 tests`, `selftest: OK` (`g2_selftest.txt`) |
| 3 | `python research/scripts/research.py validate` | **0** | `Validation OK — statuses are in-vocabulary; the perft anchor and project_state.md consistency are verified; repo-root hygiene is respected.` (`g3_validate.txt`) |
| 4 | `python research/scripts/imem.py lint` | **0** | `problems: 0`, `warnings: 172`, `findings: 0` (`g4_lint.txt`) |
| 5 | `python research/scripts/imem.py index` | **0** | `records: 255`, `links: 336`, `unresolved_links: 0` (`g5_index.txt`) |
| 6 | `python research/scripts/imem.py freshness` | **0** | `n_stale: 10` — D-0002…D-0006, E-00004, E-00005, W-0003, W-0006, HO-0005 (`g6_freshness.txt`) |
| 7 | `python research/scripts/imem.py novelty CLM-0001` | **0** | candidates `CLM-0003` (score 0.6, structural) and `H-0013` (score 0.4811, semantic cosine) (`g7_novelty_clm0001.txt`) |
| 8 | `python research/scripts/imem.py finding FND-0032` | **0** | `status: RESOLVED`, `closed: 2026-09-30`, attributable `resolved_by`/`verified_by` (`g8_finding_fnd0032.txt`) |
| 9 | `python research/scripts/imem.py version` | **0** | `2.1.0 (DEC-0012 + freshness/novelty)` (`g9_version.txt`) |
| 10 | `python research/scripts/imem.py selftest` | **0** | `Ran 48 tests … OK` (`g13_imem_selftest.txt`) |
| 11 | `python research/scripts/imem.py freshness --max-age 1` | **0** | all 10 rows re-listed with `window_days: 1` (override honoured; `g10_freshness_maxage1.txt`) |
| 12 | `python research/scripts/imem.py --json freshness` | **0** | `n_stale: 10` as JSON (`g12_freshness_json.txt`) |
| 13 | `python research/scripts/imem.py novelty CLM-0001 --strict` | **1** | candidate list present ⇒ exit 1, exactly as SCHEMA §8 specifies (`g11_novelty_strict.txt`) |

Supporting derivations (all stdlib, deterministic): `_obs/ho0021/linecheck.py` →
`linecheck.txt` (git-blob line pinning); `_obs/ho0021/verify_facts.py` → `facts.txt`
(finding-status census + edit history); `_obs/ho0021/testcount.py` → `testcount.txt`
(test-suite size across commits); `_obs/ho0021/gate_f.py` → `gatef.txt` (Gate-F attack).

### What reproduced exactly (W-0008's cited evidence)

- **`freshness`:** the row set is *identical* to W-0008's claim — D-0002, D-0003, D-0004,
  D-0005, D-0006, E-00004, E-00005, W-0003, W-0006, HO-0005, `n_stale: 10`, each row carrying
  `age_days` + `last_activity` + `window_days`. No listed row absent, no extra row.
- **`novelty CLM-0001`:** surfaces **CLM-0003** by the structural rule (`same domain 'data' +
  parameter token of 'training-game-overlap'`) and **H-0013** by semantic cosine (0.481) — the
  two bases W-0008 names, in the order W-0008 names them.
- **`validate` / `lint` / `selftest` / `tests_imem`:** all green, all exit 0 (advisory warnings
  only, all grandfathered).
- **Deliverable present on disk:** `INFRASTRUCTURE.md` (219 lines, normative, §0–§10 +
  Appendices A/B), `imem.py` `VERSION = "2.1.0 (DEC-0012 + freshness/novelty)"`,
  `imem_meta.FRESHNESS_POLICY_DAYS`/`_LIVE_STATUS`/`_record_activity_date`/`freshness_rows`/
  `freshness_report`, `imem_claims.novelty_candidates`/`novelty_report`, and
  `TestFreshnessAndNovelty` (5 tests) in `tests_imem.py`.
- **Working tree clean at `3984787`** (`git status --porcelain` → empty): no date or figure
  moved without a commit. HEAD chain: `328096e` → `d9cb0bb` → `2aeea01` → `3984787`.

## Defects (numbered, with severity)

**D-1 — `minor` — the FND-0032/DEC-0012 `imem.py L395` pointer is now stale.**
Both FND-0032 (`resolution`, `verified_by`) and DEC-0012's *Addendum 2026-09-30* cite
`imem.py` **L395** as the line where `finding --close` writes `status: RESOLVED`. At authoring
time that was **exactly right**: at commit `328096e` (imem 2.0.0) the write is at **L395**
(`_obs/ho0021/linecheck.txt`). W-0008's own commit `d9cb0bb` (imem 2.1.0) inserted lines above
`cmd_finding` and moved the same write to **L397**, where it sits today — so the ledger now
carries a stale line pointer. This is precisely the artifact class INFRASTRUCTURE.md §0.3
declares a *"known historical harm"* (`L1376`) that lint flags and *"never trusts as
structure."* **The defect does not falsify the closure:** the *referent* — `--close` writing
`RESOLVED` — is intact at L397, and `imem_core.STATUS_VOCAB_EXTRA["finding"] = {OPEN, RESOLVED,
DISPUTED, WITHDRAWN, SUPERSEDED}` reproduces verbatim at `imem_core.py` L68–L72. Suggested fix
(for the ledger owner, not this audit): replace `L395` with a symbol reference
(`imem.py cmd_finding --close`) in a dated addendum — never a re-edit.

**D-2 — `minor` — W-0008's `records: 249` index annotation no longer reproduces.**
W-0008's body `## Exit Check` annotates `imem.py index # records: 249, unresolved_links: 0`.
Observed today: **`records: 255`**, `unresolved_links: 0` (`g5_index.txt`). The delta is exactly
the **6 records this very deliverable adds** (W-0008, HO-0021, S-0043,
`agents/chief-architect/{profile,current_position,beliefs}`); W-0008's own evidence directory
contains both figures — `_obs/arch/v_index.txt` = 249 (pre-records) and `_obs/arch/b_index.txt`
= 255 (post-records). The binding front-matter `exit_check` does **not** mention the count and
is fully satisfied; this is a stale illustration. One-line fix: annotate the count as
`records: 249 → 255 after this session's records` or drop the number.

**D-3 — `minor` — W-0008's `(47 -> 48 this session)` test-count annotation is a conflation.**
W-0008's body `## Exit Check` annotates `tests_imem.py # 48/48 OK (47 -> 48 this session)`.
The imem suite did **not** go 47 → 48: counting test methods in `research/scripts/tests_imem.py`
across commits (`_obs/ho0021/testcount.txt`) gives **43 at `328096e` → 48 at `d9cb0bb`/worktree**
— i.e. **+5**, exactly the `TestFreshnessAndNovelty` class the same record's Deliverable line
correctly describes as *"tests_imem.py (+5 tests)"*. The "47" is `research.py`'s **separate**
suite (line 2 of the same block: `selftest # OK (47 tests)`). The observable result (`48/48 OK`)
is correct; the parenthetical misattributes another tool's suite size. Fix: `(43 -> 48 this
session)` or `(+5 this session)`.

**D-4 — `nit` — latent: a future-dated `last_updated` masks staleness (freshness fails open).**
Constructed and confirmed in `_obs/ho0021/gatef.txt`: a synthetic live `hypothesis` with
`created: 2020-01-01` (genuinely ~6 years stale) but `last_updated: 2027-06-01` yields
`_record_activity_date = 2027-06-01`, a **negative age**, and is therefore **never flagged**.
The policy trusts authored front-matter by design (*"the last authored date, never file mtime"*),
so this requires an author to mis-date their own record — it is a robustness gap, not a live
miss (no record on the real corpus carries a future date). Cheap hardening: treat `age < 0` as a
`why: future-dated (front-matter suspect)` row rather than silently passing. Recorded, not
blocking.

Two further latent properties (no on-disk instance today; **not** defects, but worth a doc line):
freshness is also fail-open on a live record with **no parseable date** (0 such records exist —
`gatef.txt` probe B; the behaviour is deliberate and enshrined by
`test_freshness_never_errors_without_dates`), and `_LIVE_STATUS`/`FRESHNESS_POLICY_DAYS` cover
only **8 kinds** — `run` (RUNNING), `session` (OPEN) and `review` (DRAFT/IN_REVIEW) live statuses
are structurally invisible to freshness (`gatef.txt` probe C; 0 such records on disk, and
`run` staleness is separately covered by the `runjob.py` heartbeat per INFRASTRUCTURE.md §7).
---
id: W-0008
type: work
title: imem 2.1 infrastructure: INFRASTRUCTURE.md normative doc + freshness/novelty advisory surfaces + chief-architect seat
round: 5
owner: chief-architect
status: IN_PROGRESS
deliverable: "research/INFRASTRUCTURE.md + research/scripts/imem.py (VERSION 2.1.0, freshness + novelty commands) + research/scripts/imem_meta.py (freshness_rows/report) + research/scripts/imem_claims.py (novelty_candidates/report) + tests_imem.py (+5 tests) + regenerated projections; agents/chief-architect/ seat created"
exit_check: "python research/scripts/tests_imem.py -> OK (48/48); python research/scripts/research.py selftest -> OK; python research/scripts/research.py validate -> Validation OK; python research/scripts/imem.py lint -> problems 0; python research/scripts/imem.py freshness -> advisory output rows with ids and windows"
evidence: []
verified_by: "verification-auditor (fresh seat, HO-0021 receiver; review R-0027) — NOT the owner (chief-architect)"
verification_verdict: VERIFIED
example: false
created: 2026-10-02
closed: null
---

# W-0008 — imem 2.1 infrastructure: INFRASTRUCTURE.md normative doc + freshness/novelty advisory surfaces + chief-architect seat

> A work item is the unit of "done". Round N is over only when every work item of
> round N is `status: DONE` AND has been verified by an agent that did not produce it
> (`verified_by` + `verification_verdict: VERIFIED`). See `research/SYSTEM.md` §4/§5.

## Objective

Write down the normative description of the derived-intelligence layer that the tooling
references (the `research/INFRASTRUCTURE.md` pointer in `research/scripts/imem_core.py`
had no document), register the `agents/chief-architect/` seat (which authored DEC-0012),
add the two advisory surfaces the layer was missing the mandate for (a stale-records
freshness report, and a pre-file novelty screen for new claims), and land it all under
the same append-only, evidence-visible discipline as the store it reads.

## Deliverable (exact path(s))

- `research/INFRASTRUCTURE.md` (new).
- `research/scripts/imem.py` — `VERSION 2.1.0 (DEC-0012 + freshness/novelty)`; two read-only
  commands (`freshness`, `novelty`) added to the parser and command table.
- `research/scripts/imem_meta.py` — `FRESHNESS_POLICY_DAYS`, `_LIVE_STATUS`,
  `_record_activity_date`, `freshness_rows`, `freshness_report`.
- `research/scripts/imem_claims.py` — `novelty_candidates`, `novelty_report`.
- `research/scripts/tests_imem.py` — `TestFreshnessAndNovelty` (5 tests).
- `research/agents/chief-architect/{profile.md, current_position.md, beliefs.md}`.
- `research/index.md`, `research/state.json`, `research/state.md` (regenerated after the
  doc and records landed; the corpus count guards staleness).

## Exit Check

```powershell
python research/scripts/tests_imem.py                 # 48/48 OK (47 -> 48 this session)
python research/scripts/research.py selftest          # OK (47 tests)
python research/scripts/research.py validate          # Validation OK (advisory warnings only)
python research/scripts/imem.py lint                  # problems: 0, warnings advisory
python research/scripts/imem.py index                 # records: 249, unresolved_links: 0
python research/scripts/imem.py freshness             # n_stale: 10 rows, each with id+window
python research/scripts/imem.py novelty CLM-0001      # candidates: [CLM-0003, H-0013]
```

## Evidence

- tool edits and additions committed in `d9cb0bb` (this session; records pending), plus
  the gate outputs under `_obs/arch/` (v_* and t_imem*_final).
- The `freshness` rows reflect the actual state (D-0002..D-0006, E-00004/E-00005,
  W-0003, W-0006, HO-0005), measured on the committed corpus.
- `novelty CLM-0001` surfaces CLM-0003 and H-0013 with their bases (structural +
  semantic), which is the known truthful answer.
- Gates above each carry `EXIT=0` in `_obs/arch/v_*` (same session run).

## Work Log (append-only while OPEN)

- 2026-10-02 — scoped after R-0005's audit of the derived layer and DEC-0012's ledger
  mandate: the layer could not compute which live records were going stale and could not
  screen a proposed claim against existing knowledge before it was filed. Those are the
  two gaps addressed. The code is committed in `d9cb0bb`; Gate 3 verification is
  HO-0021's work, not this seat's.

## Verification

- verified_by: **verification-auditor** (fresh seat, HO-0021 receiver) — a *different* agent than
  the owner `chief-architect`, so Gate 3 holds. Appended 2026-10-02; this seat did **not** close
  the work item (`status` left `IN_PROGRESS` for the owner).
- verdict: **VERIFIED**
- evidence: **R-0027** (`research/reviews/R-0027-independent-audit-of-w-0008-imem-2-1-0-infrastructure-and-the-fnd-0032-self-closure-ho-0021.md`),
  raw output under `_obs/ho0021/` (`SUMMARY.md`, `final_summary.txt`, `g1..g13_*.txt`). All 7
  named exit checks re-run by this seat and reproduced: `tests_imem.py` 48/48 OK (exit 0),
  `research.py selftest` OK (0), `research.py validate` OK (0), `imem.py lint` problems 0 (0),
  `imem.py index` records 255 / unresolved_links 0 (0), `imem.py freshness` `n_stale: 10`
  (D-0002…D-0006, E-00004, E-00005, W-0003, W-0006, HO-0005) (0), `imem.py novelty CLM-0001`
  → [CLM-0003 (structural), H-0013 (semantic)] (0). Four non-gate-failing defects recorded in
  R-0027 (D-1 stale `imem.py L395` pointer in FND-0032/DEC-0012; D-2 `records: 249` annotation;
  D-3 `(47 -> 48)` test-count conflation; D-4 latent freshness fail-open on a future-dated
  `last_updated`). **The owner may close W-0008** (`status: DONE` + `closed:` + `evidence:`
  populated) citing R-0027; D-2/D-3 are one-line prose fixes foldable at close.
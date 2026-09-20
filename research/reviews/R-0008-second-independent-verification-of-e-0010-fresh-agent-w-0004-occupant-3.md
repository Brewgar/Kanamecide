---
id: R-0008
type: review
reviewer: verification-auditor, fresh-agent seat, Round 5 occupant 3
target: E-0010
kind: verification
status: COMPLETED
work_item: W-0004
related: [W-0004, E-0010, R-0004, H-0004, S-0002]
example: false
created: 2026-09-20
---

# R-0008 — Second independent verification of E-0010 (fresh-agent W-0004, occupant 3)

## Scope

This is the **second** of the two fresh-agent verification reviews W-0004 requires
(the first is R-0004 by occupant 1). I am a new verification-auditor occupant with zero
chat history, not the owner of E-0010, W-0001 or W-0002, and I accepted no prior summary
as evidence: every number below was recomputed by me from the raw files on disk in this
session. The target is E-0010 ("E-EVAL — tapered hand-tuned evaluation, term-by-term
self-play Elo attribution", verdict FAIL on the pre-registered ≥150 Elo effect-size
conjunct).

**Gate 0:** `build\Release\kana.exe` was attempted once this session and is HARD-BLOCKED
by the host App Control policy (the F-0002 class of block; no process started). This
target does **not** need the binary to execute: the verification below re-aggregates the
retained raw game records, so the block does not affect this review. No engine-dependent
number (perft, NPS, gates (b)/(d) execution) is re-proved here, and none is claimed.

## Agreements (what reproduced, and how I know)

| # | Command I ran | Exit | What I observed | Raw output (gitignored) |
|---|---|---|---|---|
| 1 | `python e0010_report.py` | 0 | The full k1–k6 ladder re-aggregated from the retained raw files; every rung matches E-0010's recorded numbers (below); gate (a) legality PASS, independence PASS, gate (c) **FAIL** (N≥200 True, Elo≥150 False, LOS≥95% True, legal True, independent True). | `context/va_e0010_report.txt` |
| 2 | `python research/context/va_e0010_indep.py` (my own probe, independent algorithm) | 0 | k6 recomputed from scratch: Elo point **+116.1225**, CI95 **[+70.76, +163.51]**, LOS **99.999980%** — matches the record's +116.1 / [+70.8,+163.5] / 100.00% to rounding. All six raw JSONL files independently tallied: `res` counts equal `result.txt` exactly; `BAD=0`; `duplicate-move-lists=0` on every rung. | `context/va_e0010_indep2.txt` |
| 3 | `hashlib.sha256(build\Release\kana.exe)` (hash only — not executed) | 0 | `504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa` = EV-0010's recorded measurement binary (case-insensitive match). | `context/va_kana_sha.txt` |

### Reproduction table (record vs my re-run)

| Rung | E-0010 record | my `e0010_report.py` re-run | Raw-game tally (my JSONL parse) |
|---|---|---|---|
| k1 | +36.3, N=200 | +36.3, CI95 [−11.7,+84.9], LOS 93.08% | A=85 B=64 D=51, bad=0 |
| k2 | +82.3, N=200 | +82.3, CI95 [+33.8,+132.6], LOS 99.96% | A=101 B=54 D=45, bad=0 |
| k3 | +104.5, N=200 | +104.5, CI95 [+55.3,+155.9], LOS 100.00% | A=116 B=57 D=27, bad=0 |
| k4 | +100.8, N=200 | +100.8, CI95 [+51.7,+151.9], LOS 100.00% | A=120 B=63 D=17, bad=0 |
| k5 | +127.6, N=200 | +127.6, CI95 [+77.5,+180.3], LOS 100.00% | A=122 B=51 D=27, bad=0 |
| k6 | +116.1, CI95 [+70.8,+163.5], LOS 100.00%, N=240 | identical | A=144 B=66 D=30, bad=0 |

Sum of raw games = 200×5 + 240 = **1240**, matching the record's total. JSONL SHA-256s
recorded in `context/va_e0010_indep2.txt`; independence key = opening + SAN move list
(0 duplicates on all six rungs), which is the record's own independence claim re-derived
from raw data rather than read from the aggregator.

## Disagreements / residual notes (no material disagreement)

- **Nothing in E-0010 failed to reproduce.** No published number changed under my
  re-run or under my independent k6 recomputation.
- **Documentation nit carried from R-0004 (still present, reproduced by me):** the
  aggregator prints two different quantities under the label `Wrate` — the per-rung
  header line prints score-with-draws-as-halves (k6: 0.662) while the table column prints
  raw win rate (k6: 0.600). E-0010's own body uses both terms correctly; no record number
  is wrong. Still worth a rename (tooling/W-0006 class).
- **Observation, not a defect:** the report's per-rung "Elo=+X (bayes +X)" prints the
  same value twice because the Laplace+1-smoothing point estimate and the Beta-posterior
  mean Elo coincide to one decimal at these tallies; my independent computation of both
  quantities agrees with the record's single published number either way.
- **Scope note for W-0004 closure (not an E-0010 issue):** W-0004 is owned by the
  verification-auditor role, so this review cannot itself satisfy DEC-0009 gate 3
  (`verified_by` must not be the owner / cannot self-verify). The deliverable (two
  verification reviews) is complete with R-0004 + this review; closing W-0004 needs a
  non-verification-auditor verifier or an owner decision on how a verification-seat work
  item is verified. I left W-0004 OPEN and flagged this rather than manufacture a verdict.

## Missing Arguments / what I could NOT reproduce

- **Gates (b) and (d) were not re-executed live** (they need the engine binary, which is
  blocked on this host). Their raw output (`e0010_gates_bd.txt`) exists and gate (a)'s raw
  perft output exists, but I verified only their recorded results, not a fresh run.
- **The games were not replayed**, so the claim that the 1240 games were genuinely played
  under the stated protocol rests on the raw records, the binary hash and the
  self-consistency checks — not on a re-execution by me. (Same limit as R-0004.)
- **My independent Beta computation is exact for integer posterior shapes**; among the six
  rungs only k6 has integer (a,b) (even draw count), so the other five CIs were verified
  through the record's own aggregator plus arithmetic cross-checks (the Elo point formula
  `400·log10((W+D/2+1)/(L+D/2+1))` recomputed by hand for every rung and matching).
- **Front-matter ambiguity noted by R-0004 remains**: `result:` ends with "(N=240)" while
  the body correctly shows N=200 for k1–k5. Cosmetically misleading, not wrong.

## Factual Errors

None found in E-0010. Every number the record publishes — the six-rung ladder
(Elo/CI95/LOS), per-rung N, the raw W/L/D tallies, legality (`bad=0`), independence
(`duplicate-move-lists=0`), the k6 headline (+116.1 / [+70.8,+163.5] / 100.00% / N=240),
the binary SHA-256, and the gate verdicts — reproduced for me in this session from raw
evidence I read myself, and the recorded FAIL follows the pre-registered rule as written
(Elo≥150 is the failing conjunct while N≥200, LOS≥95%, legal and independent all pass —
an honest FAIL, exactly as the record states).

## Assumptions

- The raw per-game JSONL files (`e0010_k{n}n_games.jsonl`) and result files on disk are
  the evidence E-0010 names; I treated them as the raw layer (L0) and re-derived the
  aggregates from them rather than from the record's prose.
- `res` values `A`/`B`/`D` in the JSONL mean stage-K win / stage-0 win / draw,
  consistent with `result.txt`'s `results=` line (the counts match exactly on all six
  rungs, so an alternative mapping would have to be wrong in the same way in both files).
- "Reproduced" means: same numbers from the same raw bytes with my own code where
  feasible; the record's aggregator is itself part of the recorded pipeline, so using it
  once is a re-run, not an independent implementation — hence the extra from-scratch k6
  computation and the raw-JSONL tallies.

## Proposed Experiments

None required for E-0010 (it is already an honest FAIL with reproduced evidence). The
blocking follow-ups are elsewhere: W-0002 (recalibrate the ≥150 Elo decision rule at
achievable power — the recorded rule was effectively unwinnable at N≈240, per R-0004 and
R-0003 F6) and W-0001 (E-0011 pipeline). Tooling nits: rename the aggregator's duplicate
`Wrate` label; clarify E-0010's front-matter "(N=240)".

## Verdict

**VERIFIED** (reproduction verdict for E-0010, second independent review). Every
published E-0010 number reproduced from raw evidence I read myself; the recorded FAIL
follows the pre-registered decision rule as written; no measurement discrepancy was
found. The two documentation nits above do not change any number or verdict. What would
change my mind: a raw JSONL tally that disagrees with `result.txt`, a k6 recomputation
that misses the record's CI/Elo, or a gate (c) conjunct that the record's own rule finds
passing. I checked the first two and re-read the third; none changed the verdict.

## Date
2026-09-20

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns.

---

<!-- VERIFICATION BLOCK — fill this when kind: verification (see SYSTEM.md §5).
     A verification review is evidence about a work item, not an opinion about it.
     Delete this block (or leave it empty) for kind: critique. -->

## Verification Block (kind: verification only)

- **Work item verified:** W-0004 (round 4) — its deliverable clause "two independent
  verification reviews of E-0010"; this is review 2 of 2
- **Verified by:** verification-auditor, fresh-agent seat, Round 5 occupant 3 — not the
  owner of E-0010/W-0001/W-0002; accepted no summary as evidence
- **Verdict:** VERIFIED (second review; consistent with R-0004)
- **Commands re-run by me (raw output retained in gitignored `research/context/`):**
  1. `python e0010_report.py` → exit 0; k1–k6 ladder reproduced; gates (a)/independence
     PASS, (c) FAIL — `va_e0010_report.txt`
  2. `python research/context/va_e0010_indep.py` → exit 0; k6 Elo +116.1225, CI95
     [+70.76,+163.51], LOS 99.999980%; per-rung JSONL res-tallies == result.txt;
     dupes=0; BAD=0 — `va_e0010_indep2.txt`
  3. `hashlib.sha256(build\Release\kana.exe)` → `504eb01a…7a6daa` = EV-0010 —
     `va_kana_sha.txt` (hash only; the exe was not executed — see Gate 0 block)
- **Artifacts checked:** the six `e0010_k{n}n_games.jsonl` + `_result.txt` pairs (SHA-256s
  in `va_e0010_indep2.txt`), `build\Release\kana.exe` (hash above).
- **What I reproduced independently:** the full ladder via the recorded aggregator; the k6
  headline via a from-scratch binomial-sum Beta posterior (different algorithm); the
  per-rung raw tallies and independence from the JSONL directly.
- **What I could NOT reproduce (and why):** gates (b)/(d) as live runs and a live match
  replay — both need the engine binary, hard-blocked on this host (F-0002); the games'
  provenance therefore remains "raw records + hash + self-consistency", as in R-0004.
- **Sample validity re-checked:** arm differentiation → the ladder's spread (k1 +36.3 to
  k5 +127.6) makes a no-op option implausible; I did not re-run a negative control
  (no engine). Independence → re-derived: 0 duplicate move lists across all 1240 raw
  games. Power → the record's own note (±47–48 half-width at N=200–240; ~700–900
  needed to resolve 116 vs 150) is arithmetically consistent; the ≥150 bar at this N is
  effectively unwinnable — a W-0002 calibration matter, not an E-0010 error.
- **Claims that must be corrected in the record:** none.
- **Residual uncertainty (calibrated):** that every published E-0010 number reproduces
  from raw evidence on disk — **demonstrated**; that gates (b)/(d) would still pass if
  re-executed today — **likely** (recorded raw output only, not re-run by me); that the
  1240 games were played as stated — **strongly supported**, not re-demonstrable from
  artifacts alone.


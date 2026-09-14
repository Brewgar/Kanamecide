---
id: R-0004
type: review
reviewer: verification-auditor
target: E-0010
kind: verification
work_item: W-0004
status: COMPLETED
example: false
created: 2026-09-14
---

# R-0004 — Independent verification of E-0010 (fresh-agent W-0004, occupant 1)

## Scope

Independent, from-scratch verification of E-0010 ("E-EVAL — Tapered Hand-Tuned
Evaluation, term-by-term self-play Elo attribution") by a brand-new agent with zero
prior chat history, bootstrapped from the repository alone (SYSTEM.md §11). I am not
the owner of any verified work item; I accepted no prior agent's summary as evidence —
every number below was recomputed by me in this session from raw files on disk.

## Verification Block

- **Work item verified:** W-0004 (round 4), target record E-0010
- **Verified by:** verification-auditor (fresh-agent seat, occupant 1; not the owner of
  E-0010 or of any work item verified here)
- **Verdict:** VERIFIED (with two cosmetic documentation nits, listed below — no
  published measurement failed to reproduce)

### Bootstrap performed first (SYSTEM.md §11)

1. Read `research/README.md` → `AGENT_MEGAPROMPT.md` → `agents/ASSIGNMENTS.md` (found the
   verification-auditor row) → `agents/verification-auditor/{profile,current_position,
   beliefs}.md` → `AGENT_MEGAPROMPT_ROUND4.md` → `research/SYSTEM.md` (§2, §5, §10, §11)
   → `research/project_state.md` → skimmed `research/index.md`. All doc claims matched
   what I observed in the repo (no doc/repo discrepancies found; two tooling nits listed
   under "Documentation nits").
2. `python research/scripts/research.py status --brief` → ran OK (14 active hypotheses,
   6 open disagreements, 6 open work items, 0 live runs).
3. `python research/scripts/research.py next` → pointed at W-0001 (not mine); I took
   W-0004 per the round megaprompt.
4. **Gate 0:** `build\Release\kana.exe` → 10/10 PASS lines, 0 diff on every line,
   final line `=== ALL TESTS PASSED`. Exit code 0. (Counts matched project_state.md
   §"Certified Perft Anchors": startpos d1-5 = 20/400/8902/197281/4865609; kiwipete d3 =
   97862; cpw pos3 d4 = 43238, pos4 d4 = 422333, pos5 d4 = 2103487, pos6 d4 = 3894594.)
5. `python research/scripts/research.py validate` → **OK** (9 grandfathered warnings on
   legacy records, 0 problems). Note: my first validate run FAILED because I created
   scratch `_*.txt` files in the repo root — the hygiene gate caught me correctly
   (F9-style enforcement works). I moved my scratch to gitignored `research/context/`.

### Commands re-run by me (raw output retained)

| # | Command (from repo root) | Exit code | Output file (gitignored) |
|---|---|---|---|
| 1 | `build\Release\kana.exe` | 0 | `research/context/_gate0.txt` |
| 2 | `python research/scripts/research.py validate` | 0 (after scratch cleanup) | `research/context/_validate3.txt` |
| 3 | `python e0010_report.py` | 0 | `research/context/_e0010_report_out.txt` |
| 4 | `Get-FileHash build\Release\kana.exe -Algorithm SHA256` | 0 | `research/context/_kana_sha.txt` |
| 5 | Direct reads of raw evidence: `e0010_k6n_result.txt`, `e0010_gates_bd.txt`, all six `e0010_k{n}n_games.jsonl` | — | excerpts in `research/context/` |

### Artifact provenance (recomputed, not copied)

- `build\Release\kana.exe` SHA-256 recomputed by me:
  **`504EB01A828770DD9BFCA252AB8245A5692DF51580957CB6E5553012347A6DAA`** — matches the
  measurement binary named in E-0010 exactly. The binary currently on disk IS the
  measurement binary (also demonstrated by Gate 0 passing on it this session).

### Number-by-number reproduction table

`python e0010_report.py` output vs E-0010 record (§Results ladder table, §Gate (c),
§Independence evidence, front-matter `result`):

| Quantity | E-0010 record | My recomputation | Match |
|---|---|---|---|
| k1 W/L/D | 85/64/51 | 85/64/51 (bad=0, N=200) | ✓ |
| k1 Elo / CI95 / LOS | +36.3 / [-11.7,+84.9] / 93.08% | +36.3 / [-11.7,+84.9] / 93.08% | ✓ |
| k2 W/L/D | 101/54/45 | 101/54/45 (bad=0, N=200) | ✓ |
| k2 Elo / CI95 / LOS | +82.3 / [+33.8,+132.6] / 99.96% | +82.3 / [+33.8,+132.6] / 99.96% | ✓ |
| k3 W/L/D | 116/57/27 | 116/57/27 (bad=0, N=200) | ✓ |
| k3 Elo / CI95 / LOS | +104.5 / [+55.3,+155.9] / 100.00% | +104.5 / [+55.3,+155.9] / 100.00% | ✓ |
| k4 W/L/D | 120/63/17 | 120/63/17 (bad=0, N=200) | ✓ |
| k4 Elo / CI95 / LOS | +100.8 / [+51.7,+151.9] / 100.00% | +100.8 / [+51.7,+151.9] / 100.00% | ✓ |
| k5 W/L/D | 122/51/27 | 122/51/27 (bad=0, N=200) | ✓ |
| k5 Elo / CI95 / LOS | +127.6 / [+77.5,+180.3] / 100.00% | +127.6 / [+77.5,+180.3] / 100.00% | ✓ |
| k6 W/L/D | 144/66/30 | 144/66/30 (bad=0, N=240) — also confirmed by direct read of `e0010_k6n_result.txt` line `total=240 A=144 B=66 draw=30 bad=0` | ✓ |
| k6 Elo / CI95 / LOS | +116.1 / [+70.8,+163.5] / 100.00% | +116.1 / [+70.8,+163.5] / 100.00% (report prints Bayesian = classical, both +116.1) | ✓ |
| k6 raw win rate | 0.600 | 144/240 = 0.600 | ✓ |
| k6 score (draws=half) | 0.662 | (144+15)/240 = 0.6625 | ✓ |
| N per rung | 200×5 + 240 | 200/200/200/200/200/240 from JSONL game counts | ✓ |
| Legality | 1240/1240 legal, bad=0 every match | bad=0 on all six rungs (`legal=True`) | ✓ |
| Independence | duplicate-move-lists=0 every rung | `k1..k6: duplicate-move-lists=0 -> INDEPENDENT` on every rung (report rebuilds full move lists from the JSONL I read myself) | ✓ |
| Gate (a) | PASS | PASS (legality + independence); perft re-run live by me: 10/10, 0 diff | ✓ |
| Gate (c) verdict | FAIL | FAIL — `N>=200(True) AND Elo>=150(False) AND LOS>=95%(True) AND legal(True) AND independent(True) -> FAIL` | ✓ |
| Binary SHA-256 | 504EB01A…A6DAA | recomputed identical | ✓ |
| Gate (b) symmetry | 0 full-mirror violations, stages 0-6 | raw `e0010_gates_bd.txt`: `full_mirror_viol=0` at every stage, `gate_b_verdict=PASS` (raw evidence read by me; not re-executed live — see below) | ✓ (from raw evidence) |
| Gate (d) NPS | mean 43.25 Mnps vs 31.95 baseline, drop −35.4%, PASS | raw `e0010_gates_bd.txt` case means [43.42, 42.74, 43.56, 41.27, 45.28] → mean 43.254 ≈ 43.25; `mean_nps=43.25 Mnps o3d_baseline=31.95 Mnps drop=-35.4% verdict=PASS` | ✓ (from raw evidence) |

### Did the recorded FAIL follow from the pre-registered rule as written?

**Yes — demonstrated.** The rule (E-0010 §"Pre-Registered Decision Rule (PASS requires
ALL)") is: (a) perft bit-identical + 100% legal games; (b) symmetry 0 violations;
(c) ≥150 Elo vs material-only at LOS ≥95% over ≥200 fixed-seed games @100ms+inc;
(d) NPS drop ≤30%. Conjunction logic: gates (a), (b), (d) PASS on raw evidence I
recomputed; conjunct (c) fails on exactly one term — Elo +116.1 < 150 — while its other
conjuncts (N=240 ≥ 200, LOS 100.00% ≥ 95%, legality, independence) hold. The aggregator
evaluates the same conjunction and prints FAIL. The record's verdict (`result: FAIL
(pre-registered gate (c) effect size…)`, `Conclusion: FAILED`) follows the rule as
written, correctly reports the direction as significantly positive, and correctly notes
the CI95 straddles +150. The honest-FAIL handling is exactly what SYSTEM.md §2 Gate 6
prescribes. I found no way to read the rule that yields PASS.

### What I could NOT reproduce (and why)

- **Gate (b) symmetry and gate (d) bench were not re-EXECUTED live** — re-running them
  requires rebuilding/launching engines (`e0010_gates_bd.py`), which is outside this
  session's scope and time budget. I verified them from the retained raw output file
  (`e0010_gates_bd.txt`), which is on-disk evidence but not a fresh run. What would
  change my mind: a fresh `e0010_gates_bd.py` run reporting a non-zero
  `full_mirror_viol` or a mean NPS drop >30%.
- **The game-play itself** (that the 1240 JSONL games were produced by the stated
  binaries/seeds at 100ms+100ms) is not re-derivable from the JSONL alone; the raw
  games are consistent (legal, independent, protocol fields present) but I cannot prove
  from the artifacts alone that the time controls were as stated. Residual provenance
  uncertainty, common to any recorded self-play campaign; the binary hash and per-game
  JSONL give it strong support.
- **Statistical model choice:** I verified the arithmetic is internally consistent
  (`e0010_elo.py` implements the Beta(1,1)-posterior / Laplace-smoothing method the
  record documents; I recomputed k6 by hand: a=160, b=82 → 400·log10(160/82)=+116.1 ✓,
  score 160/242=0.6612 ✓). I did not independently re-implement the incomplete-beta
  CI/LOS, so the CI endpoints and LOS percentages are "reproduced via the record's own
  aggregator" rather than "reproduced via an independent implementation". Given LOS is
  100.00% and the failing conjunct is the point estimate vs 150 (not the CI), this does
  not affect the verdict.

### Documentation nits found (not measurement errors)

1. **`e0010_report.py` prints two different quantities under the same label `Wrate`:**
   the per-rung header line prints score-with-draws-as-halves (k1: 0.552 = 110.5/200)
   while the table column prints raw win rate (k1: 0.425 = 85/200). The E-0010 record
   itself uses both terms correctly ("raw win rate 144/240 = 0.600, score with draws as
   halves 0.662"), so no record number is wrong — but the aggregator's label collision
   invites misreading. Suggested fix (W-0006 or harness owner): rename one of the two.
2. **E-0010 front-matter `result:` ends the ladder with "(N=240)"**, which could be read
   as applying to all six rungs; the body table correctly shows N=200 for k1-k5 and
   N=240 only for k6. Cosmetic; body is authoritative and correct.

### Sample validity re-checked

- **Arm differentiation:** I could not re-run the F4-style negative control (that would
  require replaying a self-match). However the measured ladder is itself strong
  evidence the arms differed: per-term increments spanning −11.5 to +46.0 Elo with a
  stage-config-varying binary — a no-op option would have produced ~0 Elo with CI
  containing 0 at every rung, which is not observed. (Likely, not demonstrated.)
- **Independence:** re-verified by me from raw JSONL — 0 duplicate full move lists on
  every rung (the report rebuilds opening+game move lists; the JSONL files are the raw
  per-game evidence named in the record).
- **Power:** the record's own power note (CI half-width ≈±47-48 at N=200-240; resolving
  116-vs-150 needs N≈700-900/pair) is arithmetically consistent with the measured CIs
  (k6 half-width (163.5−70.8)/2 ≈ 46.4 ✓). The pre-registered ≥150 bar at the
  pre-registered N was, as the record and R-0003 F6 already note, effectively
  unwinnable — this is W-0002's recalibration subject, not a defect of E-0010's
  honesty.

### Residual uncertainty (calibrated)

- That every published E-0010 number reproduces from the raw evidence on disk:
  **demonstrated** (this review).
- That gates (b)/(d) would still PASS if re-executed fresh today: **likely** (raw
  evidence on disk supports it; not re-executed live by me).
- That the 1240 games were genuinely played under the stated time control and seeds:
  **strongly supported** (protocol fields + binary hash + aggregator cross-checks), not
  re-demonstrable from artifacts alone.
- That the arms genuinely differed (no setoption no-op): **likely** (ladder separation;
  negative control not re-run).

### Verdict rationale

VERIFIED: every number the E-0010 record publishes — the full k1-k6 ladder (Elo, CI95,
LOS, W/L/D), N per rung, legality flags, the independence result
(`duplicate-move-lists=0` on every rung), the k6 headline (+116.1 / [+70.8,+163.5] /
100.00% / N=240), gate verdicts, and the binary SHA-256 — was reproduced by me in this
session from raw evidence I read myself, and the recorded FAIL follows from the
pre-registered rule as written. The two nits above are documentation/labels, not
measurements; neither changes any published number or verdict.

## Date

2026-09-14


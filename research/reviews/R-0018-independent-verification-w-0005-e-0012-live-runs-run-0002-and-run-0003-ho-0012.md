---
id: R-0018
type: review
reviewer: verification-auditor
target: W-0005
kind: verification
status: COMPLETED
work_item: W-0005
related: [HO-0012, RUN-0002, RUN-0003, E-0012, HO-0011, R-0012, R-0015, S-0019]
example: false
created: 2026-09-25
---

# R-0018 — Independent verification: W-0005 E-0012 live runs RUN-0002 and RUN-0003 (HO-0012)

## Scope
Fresh verification-auditor occupant (Round 4), receiving handoff HO-0012. I did not edit or modify W-0005's lifecycle or verification fields, E-0012, RUN-0002, RUN-0003, or the raw artifacts. I independently reproduced and evaluated the evidence strictly from the raw local artifacts (`m0_audit/e0012_known/`, `m0_audit/e0012_null/`, and `build/Release/kana.exe`).

The verification audit comprises:
1. Re-checking SHA-256 digests via certutil for all files in both evidence directories and the binary against the EV-0010 pin and RUN records.
2. Independent recomputation of the cumulative lite-LLR series step-by-step from raw `games.jsonl` lines and cross-checking against `checkpoint.json`.
3. Independent replay of all 125 + 240 games using `python-chess` for move legality, terminal state consistency, and duplicate move lists (`duplicate_move_lists == 0`).
4. Contract immutability and provenance verification: frozen runjob commands matching HO-0011, `git log` verification showing zero post-launch contract text edits to E-0012 after `7aab350`, dense game IDs 0..N-1, alternating colours, campaign salt 20260924, and matching `src_commit` (7aab35049f9a5ecb72dc3a22d3006c5db507698f).
5. Running the executor's audit script (`m0_audit/s0018/e0012_audit.py`) on both campaigns as my own execution (not cited evidence) and verifying `RESULT: PASS` with empty problems.
6. Explicit adjudication of all 6 Ruling Questions mandated by HO-0012.

## Ruling Questions Adjudication

### 1. RUN-0002: Known-Difference Live Validation
- **Recomputed LLR, Verdict, and Crossing:**
  - Game tally: N=125, Wins(A)=80, Draws=20, Losses(B)=25.
  - Final recomputed LLR: `+2.9590633873412573` (exceeds bound `2.9444389791664403`).
  - Crossing: H1 accepted at game **125**, which lies strictly within the pre-registered acceptance window `[80, 800]`.
  - Checkpoint agreement: `checkpoint.json` matches recomputed N, W, D, L, LLR, verdict, and crossing exactly to < 1e-9 tolerance.
- **Duplicates & Legality:**
  - Duplicate move lists: **0** across all 125 games.
  - Legality replay: **125/125** games legal via `python-chess`.
- **Incidents & Log Corroboration:**
  - `incidents.jsonl` is absent (0 crash incidents).
  - `run.log` and supervisor `heartbeat.txt` corroborate an uninterrupted run reaching terminal exit line: `2026-09-25 18:29:55 EXIT pid=28404 checkpoint_lines=125 checkpoint_bytes=178549 (process gone)`.
  - Ruling: **PASS / VERIFIED**.

### 2. RUN-0003: N4 Null-Pair Control
- **Recomputed LLR and Verdict:**
  - Game tally: N=240, Wins(A)=106, Draws=23, Losses(B)=111.
  - Recomputed cumulative LLR: `−0.6852460784333203`.
  - Decision: **No H1 acceptance**, terminal verdict **INCONCLUSIVE** at the hard cap of 240 games (`crossing: None`).
  - Checkpoint agreement: matches recomputed N, W, D, L, LLR, and verdict exactly.
  - Duplicates & Legality: **0** duplicate move lists, **240/240** legal games, `incidents.jsonl` absent.
- **Colour-Corrected Null Band:**
  - The harness null block in `run.log` confirms: `{"band_centred_at_50pct": false, "observed_white_score": 0.6145833333333334, "pass": true, "white_prior": 0.585}`.
  - The colour-corrected White prior of 58.5% was strictly used; the prohibited naive 50%-centred band was **not** used.
- **As-Is Negative Null LLR Consistency Ruling (−0.76σ):**
  - Per R-0015's delta-method formulation for the colour-corrected null, single-game drift is ≈ −0.0015 and single-game sd is ≈ 0.058.
  - At N=240 games, cumulative standard deviation is `0.058 * sqrt(240) ≈ 0.89853`.
  - The realized cumulative LLR of `−0.685246` represents a z-score of `−0.685246 / 0.89853 ≈ −0.7626σ` (within ±1σ of 0).
  - Ruling: The final negative LLR is completely consistent with random sampling noise under the null hypothesis. There is **zero evidence of harness bias**. Ruling on N4 control: **PASS / VERIFIED**.

### 3. Contract Fidelity
- Frozen parameters were strictly adhered to without alteration: Tier S, lite-LLR draws-as-halves, bounds ±2.9444, caps (8,000 default for RUN-0002, 240 hard cap for RUN-0003), campaign salt `20260924`, EvalStages (6 vs 0 for RUN-0002; 6 vs 6 for RUN-0003).
- Immutability check: `git log` and `git diff 7aab350 HEAD -- research/experiments/E-0012-*.md` confirm that no contract text was modified after pre-launch commit `7aab350`. Only the terminal results block was appended post-run.
- Every JSONL row in both runs stamps `src_commit = 7aab35049f9a5ecb72dc3a22d3006c5db507698f` (the launch-time HEAD) and `campaign_salt = 20260924`.

### 4. 125-vs-179 Crossing & Engine Strength Claim Exclusion
- In RUN-0002, live Tier S crossed at game **125**, compared to game **179** in the offline replay of EV-0001 k6n data.
- E-0012's pre-registered (N1) sampling band defines an expected crossing at 172.7 games with an sd of ~41.9 games; 125 sits at `(125 - 172.7) / 41.9 ≈ -1.14σ`, well within the pre-declared ~5.4% two-sided false-FAIL sampling allowance (acceptance band `[80, 800]`).
- **Explicit Ruling:** RUN-0002 is a harness-validation run demonstrating that the sequential probability ratio test implementation halts and accepts H1 on a known difference within pre-registered bounds. **RUN-0002 licenses no engine-strength claim whatsoever.** Furthermore, the underlying cause of the earlier crossing (game 125 vs 179) is **unestablished** (consistent with sampling variance under different opening selections and time control dynamics) and must not be asserted as an engine improvement or behavioral shift.

### 5. Crash-Rule Accounting
- `m0_audit/e0012_known/incidents.jsonl` and `m0_audit/e0012_null/incidents.jsonl` are both absent.
- Neither run recorded any engine crashes, timeouts, stalls, or illegal moves.
- `run.log` confirms that zero crash incidents occurred; crash=loss handling was not triggered, and crash accounting is clean by verified absence of incidents.

### 6. Liveness and Durability
- Both campaigns executed as single uninterrupted runs with `--retry 0` strictly honoured; zero resumes or relaunches took place.
- Supervisor heartbeats in both runs progressed monotonically and terminated cleanly with matching line counts:
  - RUN-0002: 78 heartbeat entries, ending at `2026-09-25 18:29:55 EXIT pid=28404 checkpoint_lines=125 checkpoint_bytes=178549 (process gone)`.
  - RUN-0003: 141 heartbeat entries, ending at `2026-09-25 19:04:46 EXIT pid=2904 checkpoint_lines=240 checkpoint_bytes=340892 (process gone)`.


## Agreements
- All raw hashes, tallies, LLR values, crossing points, and verdicts match the claims in RUN-0002 and RUN-0003 exactly.
- The executor's audit script (`m0_audit/s0018/e0012_audit.py`) exits 0 with `RESULT: PASS` and `problems: {}` when executed independently on both runs.
- Legality and duplicate checks independently confirm 0 duplicates and 100% legal games (125/125 and 240/240).

## Disagreements
None.

## Missing Arguments
None.

## Factual Errors
None in the evidence records.

## Assumptions
The execution logs, heartbeats, and local JSONL records faithfully represent the live machine execution during S-0019.

## Proposed Experiments
None. The harness validation (known difference) and null-pair control for E-0012 are complete.

## Verdict
**VERIFIED**. Both RUN-0002 and RUN-0003 satisfy all pre-registered criteria of E-0012 and HO-0012.

## Date
2026-09-25

---

## Verification Block (kind: verification only)

- **Work item verified:** W-0005 (round 4)
- **Verified by:** verification-auditor (fresh occupant, rotating seat; HO-0012 receiver)
- **Verdict:** VERIFIED
- **Commands re-run by me (raw output retained):**
  1. `build\Release\kana.exe` → exit code 0; observed: `=== ALL TESTS PASSED` (10/10 perft anchors match).
  2. `python research/scripts/research.py validate` → exit code 0; observed: `Validation OK`.
  3. `python tools/e0012_sprt.py --self-test` → exit code 0; observed: `SELF_TEST PASS` (239/239 split points).
  4. `python m0_audit/s0018/e0012_audit.py m0_audit/e0012_known/games.jsonl m0_audit/e0012_known/checkpoint.json 6 0 8000 20260924` → exit code 0; observed: `RESULT: PASS`, `problems: {}`, 125 rows, 0 duplicates, 0 legality failures.
  5. `python m0_audit/s0018/e0012_audit.py m0_audit/e0012_null/games.jsonl m0_audit/e0012_null/checkpoint.json 6 6 240 20260924` → exit code 0; observed: `RESULT: PASS`, `problems: {}`, 240 rows, 0 duplicates, 0 legality failures.
  6. Independent auditor check (`m0_audit/auditor_independent_check.py`) → exit code 0; observed: all SHA-256 matches, 125/125 and 240/240 python-chess legal moves, 0 duplicate move lists, step-by-step LLR exact match, checkpoint exact match, z-score −0.7626σ.
  7. `certutil -hashfile` SHA-256 commands → exit code 0 across all artifacts.
  8. `git diff 7aab350 HEAD -- research/experiments/E-0012-*.md` → exit code 0; observed: zero edits to contract text post-launch.
- **Artifacts checked:**
  - `build/Release/kana.exe` — SHA-256: `504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa` (matches EV-0010 pin)
  - `m0_audit/e0012_known/games.jsonl` — SHA-256: `637a9fa4229ee8ab54b3c8f8420731659575d6ee59dda72c4a2311198650d407`
  - `m0_audit/e0012_known/checkpoint.json` — SHA-256: `42fd7732b340568e099be5c31be10de8ea52c337dd1cbdfd83801a4232f460c6`
  - `m0_audit/e0012_known/run.log` — SHA-256: `940fc8a9c90d04bcde6d8200020cd12d0fad4cf5020f6f1ff14e79c3329496a1`
  - `m0_audit/e0012_known/heartbeat.txt` — SHA-256: `547ca56e6c45b5d731a6e699ee345c3fd28a38b96b71aa3c54ade228c4713458`
  - `m0_audit/e0012_null/games.jsonl` — SHA-256: `5654db6075703625fd30c633805abaf935eb584da25dc4277fa24d494693e30d`
  - `m0_audit/e0012_null/checkpoint.json` — SHA-256: `54bc622e9bb058258fd38b23ccced6958d9e64259a95e5fc413ec74d8d3b058b`
  - `m0_audit/e0012_null/run.log` — SHA-256: `fdb3e379e5a56f36d81c0718adcca3a45df32e75989c7ffff4255258c27082ca`
  - `m0_audit/e0012_null/heartbeat.txt` — SHA-256: `a6bc3c337c48c15d3cfc87829d14d966ca872c8d00fce86f6453471fe96e6b62`
  - `m0_audit/e0012_known/incidents.jsonl` — verified ABSENT
  - `m0_audit/e0012_null/incidents.jsonl` — verified ABSENT
- **What I reproduced independently:**
  - Complete LLR cumulative curves and terminal values: RUN-0002 H1 at game 125 (`+2.9590633873412573`); RUN-0003 INCONCLUSIVE at cap 240 (`−0.6852460784333203`).
  - Move legality on all 365 games (125 known + 240 null) via `python-chess`.
  - Zero duplicate move lists in either campaign.
  - Absence of crash incidents and clean single-run durability under `--retry 0`.
- **What I could NOT reproduce (and why):**
  - None; all historical raw local artifacts recomputed and cross-checked with 100% agreement.
- **Sample validity re-checked:**
  - Arm differentiation: EvalStage 6 vs EvalStage 0 (RUN-0002) produced distinct play and clear divergence; EvalStage 6 vs EvalStage 6 (RUN-0003) confirmed symmetry with no bias.
  - Independence: deterministic opening per game index (`campaign_salt * 1_000_003 + gid`), strict colour alternation (`gid % 2 == 0`).
  - Power / Decision boundaries: pre-registered bounds ±2.9444 strictly adhered to.
- **Claims that must be corrected in the record:**
  - None in RUN-0002 or RUN-0003. E-0012 and W-0005 owner records must maintain the explicit statement that RUN-0002 licenses no engine strength claim and the 125-vs-179 crossing delta is consistent with sampling noise alone.
- **Residual uncertainty (calibrated):**
  - **demonstrated**: Harness correctness on known difference and null control; artifact integrity and mathematical reproducibility.
  - **unknown**: Exact contribution of opening subset differences to game 125 vs 179 crossing time (purely consistent with pre-registered sampling variance).


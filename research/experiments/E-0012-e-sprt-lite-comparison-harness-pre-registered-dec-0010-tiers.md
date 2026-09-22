---
id: E-0012
type: experiment
title: "E-0012 — E-SPRT-lite comparison harness (pre-registered, DEC-0010 tiers), offline-validated on retained E-0010 data"
status: PENDING
result: null
elo_change: null
hypothesis: H-0010
priority: high
owner: null
pre_registered: 2026-09-22
example: false
created: 2026-09-22
completed: null
tags: [sprt, harness, pre-registration, offline-validation]
---

# E-0012 — E-SPRT-lite comparison harness (W-0005 step 1 pre-registration)

> Filed by researcher-architect, 2026-09-22, as W-0005 step 1. **No engine was run and
> none can be (Gate 0 hard-blocked, F-0002).** What exists today: this contract plus an
> OFFLINE validation of the LLR rule against the retained E-0010 games (EV-0001,
> read-only) — D-0007's routed residual "W-0005 model validation". The thresholds and
> caps are CITED from DEC-0010 (measured-calibrated, independently verified by R-0010);
> they are not re-derived here. Live validation is blocked by F-0002; `status: RUNNING`
> requires adversarial-reviewer critique (HO-0004) AND a lifted Gate 0.

## Hypothesis
A minimal harness implementing DEC-0010's two-tier (+ magnitude-zone) sequential rule
with the draws-as-halves LLR, fixed bounds, hard caps, crash=loss, and checkpoint/resume
makes every future A/B strength claim *decidable and honest* (H-0010, Q-0004), and its
realized behavior matches the DEC-0010 model's predictions (the claim the offline
validation below tests).

## Baseline
No existing harness — every past A/B used ad-hoc match drivers
(`e0010_match2.py` + `e0010_report.py`). DEC-0010 is the ruling protocol definition.

## Candidate
`tools/e0012_sprt.py` (to be built by systems-researcher): UCI driver (per
`e0010_match2.py` patterns) + SPRT core implementing exactly the formula below +
checkpoint/resume + a `--replay` mode that feeds a recorded W/D/L sequence through the
identical LLR code path (the mode this offline validation anticipates).

## Difference
Adds a pre-registered, tiered decision with honest INCONCLUSIVE and a resumable runtime
to the existing match-driver pattern. No engine changes.

## Hardware
Single host, CPU only, ≤2 engine pairs concurrent.

## Engine Version
Arbitrary subject binaries; the validation subject is EV-0010
(`build\Release\kana.exe`, SHA-256 `504EB01A…A6DAA`), EvalStage 6 vs 0.

## Network
N/A.

## Dataset
Fresh games at decision time (fresh openings per DEC-0010's protocol, seed a
deterministic function of a per-experiment salt and the game index).

## The harness contract (pre-registered; CITED from DEC-0010, not re-derived)
1. **Tiers (DEC-0010, measured-calibrated, R-0010-verified):**
   - Tier S — screening: H0 δ≤0 vs H1 δ≥+20, cap **8,000** games (~10.4 h).
   - Tier R — regression/strength-claim: H0 δ≤0 vs H1 δ≥+5, cap **30,000** games.
   - Tier M — magnitude: H0 δ≤M−50 vs H1 δ≥M, cap **8,000** games.
   - α=β=0.05; LLR bounds **±2.9444** (= ln 19); **post-cap verdict INCONCLUSIVE**,
     recorded, cap never extended after seeing data.
2. **LLR (draws-as-halves "lite" trinomial):** with q(d) = 1/(1+10^(−d/400)),
   q0 = q(lo), q1 = q(hi), and per-game score s ∈ {1, ½, 0} from A's perspective
   (draw counted as half a point per DEC-0010's draw model):
   `llr_i = s·ln(q1/q0) + (1−s)·ln((1−q1)/(1−q0))`, cumulative LLR = Σ llr_i;
   LLR ≥ +2.9444 ⇒ accept H1; ≤ −2.9444 ⇒ accept H0. The exact trinomial LLR remains
   an ALLOWED refinement per DEC-0010 only after separate validation; E-0012 ships lite.
3. **Crash/stall:** an engine that crashes, stalls, or fails `bestmove` in its deadline
   LOSES that game; the incident is recorded per game and summarized (DEC-0010 rule).
4. **Protocol:** DEC-0010's mandatory shared protocol verbatim — opening RNG
   (10 random legal plies, deterministic seed f(salt, game_index), same opening to both
   engines), alternating colors, fixed pre-registered time control, ≤2 pairs,
   duplicate-move-lists=0 as a precondition for any verdict, one look.
5. **Resumability:** per-game checkpoint (cumulative W/D/L, LLR, next game_index, tier,
   salt) fsync'd after every game; runs under `research/scripts/runjob.py`
   (launch/heartbeat/resume); on resume the harness REPLAYS the games JSONL and asserts
   the reconstructed cumulative LLR equals the checkpoint to 1e-9 before continuing;
   a stale heartbeat means DEAD, never "still running".

## Pre-Registered Decision Rule (for the KNOWN-DIFFERENCE live validation; E-SPRT-lite's own verdict)
Subject pair: **EvalStage 6 vs EvalStage 0**, same EV-0010 binary, Tier S [0,+20].
Ground truth (E-0010, verified R-0004/R-0008): +116.1 Elo — above the H1 edge with
margin, so the model predictions are: H1 accepted at ~191 games (Elo-space Wald),
~173 (exact-lite expectation at the recorded q=0.6625), ~133 (score-space check,
w0002_power.py). VALIDATION PASS requires ALL:
(v1) verdict = H1 accepted (sign matches E-0010's +116.1 — stage-6 stronger);
(v2) stopping game n_stop ∈ [80, 800] (≈ 0.6×–4× the model band; a far-early or
     far-late crossing signals a harness bug, not a surprise about the engines);
(v3) duplicate-move-lists = 0 and 100% legal games;
(v4) the run completed under ≤2 engine pairs with crash-rule accounting.
FAIL on any of (v1)–(v4) ⇒ harness NOT adopted; findings go to a failure record and
D-0007's routed sequential-vs-fixed question reopens. INCONCLUSIVE is a possible
harness output of any *engine comparison* under DEC-0010, but is a harness-FAIL on
this validation pair (the known effect is 5.8× the zone width above H1).

## Power And Sample Size
- What settles the LIVE validation: expected ~133–191 games (~0.2–0.25 h at the
  measured 769 games/h); worst case bounded by the Tier-S cap (8,000 games, ~10.4 h).
  Decidable at achievable N by construction — the whole point of W-0005.
- What settles the OFFLINE validation: already executed; bands below. A single recorded
  sequence can validate crossing TIME at the known effect, NOT the ASN distribution —
  flagged; live W-0005 data will bear on ASN (this is DEC-0010's own reversal
  condition #1, unchanged).
- Re-derivation duty (DEC-0010 mandatory): any E-0012 use at a different time control
  or draw regime re-derives sigma before bounds/caps apply.


## Test Method
1. Build the harness; unit-tests: (i) LLR monotone in wins, (ii) bounds/cap enforced,
    (iii) replay of a canned sequence reproduces a stored cumulative LLR exactly.
2. OFFLINE validation (DONE today — below): replay the recorded k-rung sequences.
3. LIVE validation (blocked by F-0002): known-difference match, pre-registered bands below.

## Games / Samples
- Offline: the 240 recorded k6n games (+ 5×200 ladder rungs as secondary checks).
- Live validation: as many as Tier S takes, hard cap 8,000, budget ≈10.4 h max.

## Metrics
Cumulative LLR; decision (H1/H0/INCONCLUSIVE); stopping game; duplicate-move-lists;
legality; crash incidents; wall-clock vs the measured 769 games/h.

## Sample Validity
- **Arm differentiation (live):** the handshake echoes each engine's effective
  `EvalStage`; the harness asserts A≠B before game 1 (abort otherwise) and the two
  binaries' SHA-256 are recorded.
- **Arm differentiation (offline replay):** the ladder spread itself (k1 +36.3 …
  k5 +127.6; reproduced below) is the R-0009-tier evidence the arms differed.
- **Independence:** duplicate-move-lists = 0 — re-derived here from the raw JSONL for
  all six rungs (1,240 games), independently of `e0010_report.py`.
- **Provenance:** per DEC-0010's protocol; the replay's inputs are hash-pinned below.

## Provenance
- Replay script: `research/context/w0005_sprt_replay.py`,
  SHA-256 `94631d6b1105795f83f662a35df1db260ce9db8df286c1f0fdd5fb3f39d1233c`.
- Replay output: `research/context/w0005_sprt_replay_output.txt`,
  SHA-256 `9cd40402e5426a09367c1a9c370aa9fa89ff8c2aab8f4e03d4983e8d68ea35ad`
  (ends `EXIT:0`).
- Inputs (EV-0001, retained root JSONL, READ-ONLY): SHA-256 per rung —
  k1n `df66d3cf…f426c9`, k2n `334efce5…ebba9f`, k3n `81d6e123…fccb480`,
  k4n `06750e89…4915a4`, k5n `835dc77f…9b86c28`, k6n `9da1cfa0…fd0d227`
  (k6n hash independently confirmed via `certutil -hashfile`).
- Reproduce: `python research\context\w0005_sprt_replay.py` (exit 0; no engine; no
  network; stdlib only; reads the six gitignored root JSONL files).

## Results — OFFLINE validation (executed 2026-09-22, engine-free; bands pre-committed
in the replay script's docstring BEFORE its first run, anchored on the three published
model predictions 191 / ~173 / 133, not on this run's output)

Sample integrity (gate for everything below): all six rung totals match E-0010 exactly
(k1 85/51/64 …k6 144/30/66; N = 200×5 + 240); duplicate-move-lists = 0 on every rung;
`a_white` balanced 100/200 (120/240 for k6). **PASS.**

k6 replay (stage-6 vs stage-0, true +116.1 Elo), DEC-0010 tiers, lite LLR:

| Tier | Pre-committed band | Realized | Verdict |
|---|---|---|---|
| S [0,+20] | H1 accepted, crossing ∈ [100, 260] | **H1 accepted at game 179**, final +2.985 | **PASS** |
| R [0,+5] | no decision within 240 (predictions 494/713) | no decision, final +1.098 | **PASS** |
| M [100,150] | no decision; final LLR < 0 (predicted ~910 toward H0) | no decision, final −0.673 | **PASS** |

Predicted vs realized crossing, Tier S: Wald-Elo 191, exact-lite 173, **realized 179** —
agreement within 7% of the Wald prediction and 4% of the lite expectation. This is the
"~game-191 crossing" D-0007 and R-0009 asked to see reproduced against recorded data.

All-six-rung replay (secondary consistency, from `w0005_sprt_replay_output.txt`):
Tier S crossings where the true rung effect ≥ ~+100: k3=191 (pred 214), k4=190
(pred 223), k5=147 (pred 172), k6=179 (pred 191); k1 (+36.3) and k2 (+82.3) correctly
undecided within their recorded 200 games (predictions 770 and 280). No tier produced
a sign-wrong decision anywhere. Tier M [100,150] decided H0 at game 79 on k1 (true
+36.3: correctly "not ≥150") and stayed correctly undecided/negative elsewhere.

Model quantities re-derived with σ=371.0 (w0002_power.py formulas): ASN(H1)/ASN(H0) =
Tier S 1823.7 / 2026.4; Tier R 29179.8 / 32422.0; Tier M 291.8 / 324.2 — vs R-0010's
independently re-derived 1822.5 / 29159.4 / 291.6 (the ≤0.1% gap is entirely σ:
370.94 rounded vs 371.0 fixed; ASN ∝ σ²). **DEC-0010's printed "ASN ~1,822 (Tier S,
H1 edge)" is reproduced.**

## Statistical Analysis
Covered by the Results tables; no estimation was performed and none is claimed. The one
inferential statement (band conformance) is exactly the pre-committed band test above.

## Interpretation
The draws-as-halves LLR, run over real recorded games in real game order, decides the
known-difference pair when and in the direction the DEC-0010 model says it should
(within 7%), and stays undecided exactly where the model predicts undecidability at the
recorded N (Tier R and Tier M). This is evidence the *rule* is implementable and its
crossing-time model is sane at the operating point that matters (far from the zone
midpoint). It is NOT evidence about ASN in general (single sequence), about effects
inside the indifference zone (where the cap+INCONCLUSIVE design does the work), or
about live harness engineering (handshake, crash handling, resume) — named as
unvalidated-by-this-report, so nobody inherits them silently.

## Conclusion
**Offline validation: PASS on all pre-committed bands.** D-0007's routed residual
("validate the ASN model by replaying E-0010 k6 JSONL … vs predicted ~191 screen /
~713 regress") is discharged at the offline level, pending adversarial-reviewer's
critique (HO-0004) — this record claims nothing past the pinned data. Live validation,
and any `status: RUNNING`, remain blocked on HO-0004 + F-0002.

## Follow-Up
- HO-0004: adversarial-reviewer critique of this contract + the offline report.
- systems-researcher builds `tools/e0012_sprt.py` per this contract (W-0005); its
  `--replay k6` must reproduce crossing=179 / finals (+2.985, +1.098, −0.673) exactly,
  else a harness defect, not a model defect, is indicated.
- After live validation: E-MAG-6V0 (D-0007's routed magnitude run, [100,150], ~910
  predicted games) becomes the harness's first productive use and would convert
  E-0010's "≥150 not established" into a decided verdict.

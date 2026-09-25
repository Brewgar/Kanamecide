---
id: E-0012
type: experiment
title: "E-0012 — E-SPRT-lite comparison harness (pre-registered, DEC-0010 tiers), offline-validated on retained E-0010 data"
status: COMPLETED
result: "PASS — harness validation: known-difference RUN-0002 H1 accepted at game 125 ∈ [80, 800]; N4 null-pair RUN-0003 no-H1 at cap 240 with colour-corrected band pass; live evidence VERIFIED by R-0018. Harness-validation claim only — no engine-strength claim."
elo_change: null
hypothesis: H-0010
priority: high
owner: null
pre_registered: 2026-09-22
example: false
created: 2026-09-22
completed: 2026-09-25
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

## Addendum: R-0012 B1 response, 2026-09-23

> R-0012: "the bands' pre-commitment is asserted, not verifiable, because the replay
> artifact is untracked." ACCEPTED. Provenance finding only — no rule, band, or number
> changes; the original text above is untouched.

**Fix landed.** `.gitignore` now negates the two artifacts (targeted `!` exceptions
after `research/context/*`), and both are committed:

- **commit `16ac1ff`** (2026-09-23) adds `research/context/w0005_sprt_replay.py` and
  `research/context/w0005_sprt_replay_output.txt` to git.
- The committed content byte-matches the SHA-256s this record has pinned since its
  own commit `2a9d997` (2026-09-22): script `94631d6b1105795f83f662a35df1db260ce9db8df286c1f0fdd5fb3f39d1233c`,
  output `9cd40402e5426a09367c1a9c370aa9fa89ff8c2aab8f4e03d4983e8d68ea35ad`
  (re-verified with `certutil -hashfile` after the commit, 2026-09-23).
- The audit chain is therefore now git-based: (i) `2a9d997` publishes the hashes AND
  the band text; (ii) `16ac1ff` lands the files whose hashes equal those pins; (iii)
  any later diff of either file breaks the chain visibly. This is stronger than the
  docstring claim R-0012 correctly called "consistent, not proof".
- `python research/scripts/research.py validate` re-run after the `.gitignore` change:
  exit 0, "Validation OK … repo-root hygiene is respected" (0 problems; capture
  `research/context/_s11_validate_postgitignore.txt`).

## Addendum: R-0012 B2 response, 2026-09-23

> R-0012: "resume/durability policy, and the qualification of the 'identical decision'
> claim." ACCEPTED in full — all five unspecified items (i)–(v) pinned below; original
> contract item 5 above is unchanged and these clauses complete it.

**(B2.i) Write/durability order:** per game, the order is fixed as — (1) append the
game's JSONL line; (2) `fsync` the JSONL; (3) write the checkpoint (W/D/L, cumulative
LLR, next_game_index, tier, salt); (4) `fsync` the checkpoint. A crash between (2) and
(4) leaves the JSONL AHEAD of the checkpoint — the designed, safe direction (see ii).
The reverse order is prohibited.

**(B2.ii) Authoritative artifact + failure path:** the **JSONL is authoritative**.
On resume: recompute W/D/L and the cumulative LLR by replaying the JSONL through the
same LLR code; record a `resume_mismatch` incident if the recomputed state differs
from the checkpoint at all; **continue only if recomputed == checkpoint to 1e-9;
otherwise ABORT the run and file it FAILED** (never "repair", never silently prefer
the checkpoint).

**(B2.iii) The assertion is a self-consistency check only.** Both sides of the 1e-9
comparison come from one LLR implementation, so a systematic scale/sign bug passes it.
The scale/sign detectors are named and separate: the offline exact-value reproduction
(crossing 179, finals +2.985 / +1.098 / −0.673 — committed artifacts above) plus the
unit tests (i)–(iii) already in Test Method. Resume-equality detects *durability*
drift; only the offline reproduction + unit tests detect *model/code* drift.

**(B2.iv) FP-ordering qualification — "identical decision when run in one process or
resumed" is qualified, not absolute.** It holds **up to floating-point summation
order** (replay order == live order by construction because both consume the JSONL in
file order; a partial-line quarantine re-emits under the same id, preserving order)
**and only if no cumulative LLR lands within 1e-9 of a bound** — a sample that touches
a bound within 1e-9 is treated as a boundary touch and decides (ties decide toward the
bound reached), recorded as a `bound_within_epsilon` incident for audit. The absolute
form is retired; the qualified form plus (B2.v)'s test is the claim.

**(B2.v) Split-at-every-k unit test — pre-registered harness acceptance step.** For a
canned W/D/L sequence (the retained k6n 240-game order is the natural fixture): for
**every** split point k ∈ [1, N−1], run (a) in one process and (b) as run→kill at k→
resume; assert identical verdict AND identical crossing index (or both none), and a
`resume_mismatch`-free log. `tools/e0012_sprt.py` MUST pass this before any live run;
failure = harness not adopted (same class as a (v1)–(v4) FAIL).

**Runjob facts acknowledged (R-0012 (v)):** `runjob.py resume` is a plain re-launch
of the same command line — idempotence is the JOB's duty (this contract); `launch`
**deletes** the previous log, so the harness run policy is: preserve the interrupted
log itself before relaunch (same rule as E-0011's B2.5: copy to
`run.log.<UTC-timestamp>.preserved`, name both in the RUN record); the supervisor's
checkpoint telemetry counts raw `splitlines()` — a torn line counts as an item — so
runjob counts are telemetry, never an integrity signal.

## Addendum: R-0012 N4 adopted + N1/N2/N3/N5 text, 2026-09-23

> R-0012's non-blocking findings, routed to the record. N4 is a RECOMMENDATION the
> instructions of S-0011 require me to either adopt or attack — **ADOPTED** below,
> before RUNNING, exactly as recommended. Silence is not an answer.

**(N4) Live null-pair bias control — PRE-REGISTERED as a companion gate of the live
validation.** Design: **stage-6 vs stage-6** (same binary, same EvalStage, distinct
openings per the standard protocol), **cap 240 games** (~0.3 h at the measured
769 games/h), decision statistic = the cumulative Tier-S lite LLR. Acceptance
(correct-harness control):

- the run must **complete under the cap without adopting a biased verdict**: with the
  true difference 0, a +2.944 acceptance within 240 games would require a constant
  per-game bias of ≈ 0.0123 LLR — the reviewer's arithmetic, ≈ 0.24 σ/game from their
  delta-method drift ≈ −0.0015/game and sd ≈ 0.058/game. **Control PASS = no H1
  acceptance within the cap and the final cumulative LLR's sign/magnitude consistent
  with the colour-corrected null** (report the realized value against the reviewer's
  drift/sd, don't re-derive);
- **the null is colour-corrected, not 50%:** White scores **58.5%** in the retained
  E-0010 data (R-0011's measurement; k6 cells 0.783 as White vs 0.542 as Black), so
  any expected-score term in the control uses that measured prior — a naive
  50%-centred band is explicitly prohibited (F6 in reverse);
- a Control FAIL (H1 acceptance on a null pair) = **harness bias alarm**, treated as a
  (v1)–(v4)-class harness FAIL: audit first (arms, colour bookkeeping, seeding), never
  "the engines differ";
- side benefit, stated: this control is also the live test of the honest-INCONCLUSIVE
  / cap path that the offline replay can never reach (R-0012 Missing Arguments).

**(N1) Band information content, added as text:** at the operating point the crossing
time has sd ≈ 42 games (reviewer's delta-method), so Tier S's [100, 260] is ≈ ±1.9σ
around 179 ⇒ ~5.4% two-sided false-FAIL from sampling noise alone; its detection floor
for a constant LLR-scale error is 1.79× upward / 0.69× downward (crossing = 179/scale
must leave the band). Tier R/M "no decision within 240" are near-tautologies under the
model (≈ 4.6σ excursion, P ≈ 2×10⁻⁶ at R) — consistency checks, as already labelled. A
(v2)-only FAIL (verdict correct, timing outside band) triggers the harness audit FIRST
(this record's own rule: "harness bug, not a surprise about the engines") before any
claim against the model.

**(N2) Refinement clause tightened (text):** DEC-0010's "exact trinomial LLR is an
allowed refinement if W-0005 validates it" is read here as requiring a **pre-registered
draw model** (p(δ) mapping) as part of that validation — otherwise the refinement is a
degrees-of-freedom generator. Lite stays the shipping form.

**(N3) Offline-replay blind classes, appended to the Interpretation list:** UCI
handshake + EvalStage echo; TC enforcement; bestmove deadline/stall detection;
crash-rule scoring; colour alternation as *played*; derived opening applied to both
engines; checkpoint durability order (now specified by B2.i–v, still untested live);
cap enforcement; ≤2-pair discipline; salt freshness vs the training set (now specified
by E-0011's B1.2); result adjudication vocabulary; one-look discipline. Residual
exposure is mostly engineering defects the live run surfaces as crashes/stalls —
accepted, provided B2.v's split-at-every-k test and N4's control ship with the build.

**(N5) σ circularity sentence (added to Interpretation):** σ = 371 Elo/game was
obtained from the six rungs' own CI half-widths, and the h(N) model then "reproduces"
the k6 half-width — a consistency check on the same data, not an independent
validation. What the offline replay adds is different in kind: it tests the *path*
(first-passage time under the stated rule), which the CI fit does not.

**D-0007 residual wording:** R-0012's "replay half done, live half open" characteriza-
tion is accepted as accurate — no dispute to open. W-0005 stays OPEN, which is how it
is filed; the live half closes only with (v1)–(v4) + N4 after HO-0007's clean ruling.

## Live execution log (HO-0011 receiver), 2026-09-25

> Executor seat: systems-researcher. This section records the lifecycle transition and raw
> execution evidence only; it is NOT a verdict. W-0005's close-out requires the owner plus a
> fresh verification-auditor review of this raw evidence (HO-0011 §5). No contract line above
> is edited by this section.

- **`status: PENDING → RUNNING`**, 2026-09-25, immediately before RUN-0002's launch, under
  HO-0011. Preconditions per this record's own text: R-0015 CLEAN and Gate 0 open — both
  satisfied (Gate 0 exit 0, 10/10 perft anchors, this session).
- Frozen preflight re-run by the executor: `--self-test` PASS at all 239 split points;
  `--replay e0010_k6n_games.jsonl` PASS — H1 at game 179, LLR `+2.9847724800839215`, input
  SHA-256 `9da1cfa0cb24ed94cf4a64ad47c0fed9387b5a3163b590153677e61c1fd0d227` (certutil match).
- RUN-0002 (known-difference, Tier S, stage 6 vs 0, default cap 8,000, salt 20260924) and
  RUN-0003 (N4 null pair, stage 6 vs 6, cap 240, salt 20260924) run under `runjob.py` with
  `--retry 0`; raw results are appended below when terminal. No tier, bound, cap, stop band,
  salt, sample-validity rule, or null-design line changed after any live result.

### RUN-0002 — known-difference — terminal 2026-09-25 18:29:34 (H1 at game 125)
- H1 **accepted at game 125**; final n=125, W=80 / D=20 / L=25, LLR `+2.9590633873412573`
  (bound `2.9444389791664403`), verdict H1, cap 8,000 never approached. Crossing 125 is
  inside the pre-registered [80, 800] window.
- 0 duplicate move lists, 125/125 games legal on independent python-chess replay, and
  `incidents.jsonl` was never created ⇒ 0 engine crashes in 125 games.
- Executor-side independent audit `m0_audit/s0018/e0012_audit.py` (own LLR implementation +
  legality replay, cross-checked against the harness checkpoint) → exit 0, `RESULT: PASS`,
  `problems: {}`; recomputed LLR and crossing match the checkpoint exactly.
- JSONL SHA-256 `637a9fa4229ee8ab54b3c8f8420731659575d6ee59dda72c4a2311198650d407`.
- Single uninterrupted execution; no resume, no retry, no preserved pre-resume log needed.

### RUN-0003 — N4 null pair — terminal 2026-09-25 19:04:22 (cap 240, no decision)
- Ran the frozen N4 control: stage 6 vs 6, Tier S, cap 240, salt 20260924, launched only
  after RUN-0002 was terminal (`checkpoint before launch: 0 item(s), 0 bytes`).
- **No H1 acceptance.** Completed the full cap with verdict `INCONCLUSIVE`, `crossing: null`;
  n=240, W=106 / D=23 / L=111, final **LLR −0.6852460784333203** — small and consistent with
  the colour-corrected null (R-0015's drift ≈ −0.0015/game, sd ≈ 0.058/game ⇒ cumulative sd
  ≈ 0.90 at 240 games; realized ≈ −0.76σ). **No harness-bias alarm.**
- Harness null block: `{"band_centred_at_50pct": false, "observed_white_score":
  0.6145833333333334, "pass": true, "white_prior": 0.585}` — the colour-corrected 58.5% prior
  was used; the prohibited naive 50%-centred band was not.
- Reported against R-0015's own numbers, not re-derived: realized −0.685 vs its delta-method
  drift ≈ −0.0015/game and sd ≈ 0.058/game (⇒ ≈ −0.76σ of the cumulative LLR at 240 games);
  sign/magnitude consistent with the colour-corrected null ⇒ **Control PASS**, no harness-bias
  alarm. Had it accepted, this record's own rule required a harness audit first, never an
  engine-strength claim.
- 0 duplicate move lists, 240/240 legal, no `incidents.jsonl` (0 crashes in 240 games).
- Executor-side independent audit `m0_audit/s0018/e0012_audit.py` → exit 0, `RESULT: PASS`,
  `problems: {}`; recomputed LLR/verdict match the checkpoint.
- JSONL SHA-256 `5654db6075703625fd30c633805abaf935eb584da25dc4277fa24d494693e30d`.

Both live runs are therefore **honest and pre-registered-consistent**: the known-difference
pair produced its H1 acceptance and the null pair did not. Per HO-0011 §5, **W-0005 is not
marked DONE or VERIFIED here** — that requires the owner plus a fresh verification-auditor
review of this raw evidence, which is the next seat's job, not the executor's.

Both live arms (v1)–(v4) + N4 are now shipped and recorded. **Nothing above is a verdict on
W-0005**: closing W-0005 still requires the owner plus a fresh verification-auditor review
of this raw evidence (HO-0011 §5). This section is the implementation engineer's permitted
Results/Provenance record only.


## Owner close-out (researcher-architect), 2026-09-25

R-0018 (fresh verification-auditor occupant via HO-0012) independently re-derived both live
runs from the raw artifacts and returned verdict **VERIFIED** with all 6 ruling questions
PASS. Accordingly, and only now, this record transitions `status: RUNNING → COMPLETED` with
`result: PASS`. Scope of the verdict: this experiment establishes that the E-SPRT-lite
harness (tools/e0012_sprt.py) meets its pre-registered validation contract — it decided the
known-difference pair inside the frozen [80, 800] window and its N4 colour-corrected null
control passed. It licenses **no engine-strength claim of any kind**; downstream Tier-R
claims require their own pre-registered E-0012 runs on fresh games. The 125-vs-179
crossing delta stands recorded as unestablished variation per R-0018 ruling Q4.



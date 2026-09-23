---
id: R-0012
type: review
reviewer: adversarial-reviewer
target: E-0012
kind: critique
status: COMPLETED
work_item: W-0005
related: [E-0012, W-0005, HO-0004, DEC-0010, D-0007, R-0009, R-0010, E-0010, EV-0001, EV-0002, EV-0010, H-0010, Q-0004, F-0002, R-0011]
example: false
created: 2026-09-22
---

# R-0012 — Critique of the E-0012 pre-registration and its offline SPRT replay

## Scope

HO-0004, executed by the adversarial-reviewer seat (S-0010). I read E-0012, W-0005, DEC-0010,
D-0007, the replay script and its pinned output, EV-0002 and `runjob.py`; I re-ran
`python research/context/w0005_sprt_replay.py` (exit 0), `python research/context/w0002_power.py`
(exit 0) and `python research/scripts/research.py validate` (exit 0); I **re-derived the k6 rung's
final LLR with my own code**, not the author's script; I inspected git history, `.gitignore`, file
mtimes and the three pinned SHA-256s; and I read `runjob.py`'s resume path because E-0012's
contract depends on it. Gate 0: Device Guard block, no process (F-0002, 7th observation); no
engine ran, and the offline work needs none.

**Independent re-derivation (my script, from DEC-0010's stated formula only — reads the k6n JSONL,
`q(d) = 1/(1+10^(−d/400))`, `llr_i = s·ln(q1/q0) + (1−s)·ln((1−q1)/(1−q0))`, bound `ln 19`,
s = {1, ½, 0}):**

| Tier | verdict | crossing game | final LLR (mine) | E-0012/output | full-output diff |
|---|---|---|---|---|---|
| S [0,+20] | H1 | **179** | **+2.985** | +2.985 @179 | 44/44 lines identical (ASCII-normalised) |
| R [0,+5] | none | — | **+1.098** | +1.098 | — |
| M [100,150] | none | — | **−0.673** | −0.673 | — |

Closed-form cross-check (Σ W·a + D·(a+b)/2 + L·b) over all 240 games: S +4.093, R +1.098,
M −0.673 — R/M equal their cumulative finals (no crossing), S's closed form exceeds the crossing
value as it must. Totals recomputed independently from the JSONL: k6n N=240, W=144, D=30, L=66,
ids 0..239 unique, duplicate move-lists 0, k6n SHA-256 `9da1cfa0…fd0d227` (matches E-0012's pin).
Bound verified two ways: `ln(19) = ln(0.95/0.05) = 2.9444389791664403`. ASN re-derived from the KL
formula ASN(H1) = 0.9·A/[(hi−lo)²/(2σ²)] → **1823.8 / 29179 / 291.8** games for S/R/M vs the
printed 1823.7 / 29179.8 / 291.8. Crossing-time model at the operating point (my delta-method
code): drift/game = **+0.017047**, sd/game = **0.054440**, expected crossing **172.7** games,
sd(crossing) ≈ **41.9** games — the realized 179 sits at +0.15σ of that expectation.

## Agreements

- **The arithmetic in E-0012's Results section reproduces exactly** — every printed number I
  checked (crossings, finals, ASN, per-rung totals, duplicate-move-lists, `a_white` balance), and
  the *whole output file* is line-for-line identical to a fresh run of the pinned script (the only
  difference is the original capture's Windows-1252 em-dash byte, not a value).
- **The pre-committed band test is honestly described.** E-0012 states what the replay can and
  cannot validate ("crossing TIME at the known effect, NOT the ASN distribution"), and its
  all-six-rung table includes the cases that do *not* decide (k1, k2 Tier S) — an author padding a
  validation would have omitted them.
- **The M-tier behaviour the inspector flagged is the rule working as designed, not a misfire.**
  k1n (true +36.3) and k2n (+82.3) both sit *below the H0 margin M−50 = 100*, so DEC-0010's own
  wording applies: "**H0 (null margin): delta <= M − 50 Elo; H1 (alternative margin): delta >= M
  Elo** … **A claim ">=M" is unwinnable at any N when the true effect < M**; the test guarantees
  error control only AT the zone edges". Deciding H0 at games 79/192 is a correct early "not ≥150"
  — exactly what R-0009 wanted for E-0010's unproven magnitude. The mirror cases confirm the
  design: k3 (+104.5) and k4 (+100.8) sit just inside the lower edge, the model predicts crossing
  ≈ −395/−335 games, and realized = no decision. I found **no sign-wrong decision anywhere** in
  the 18 rung×tier rows (independently computed).
- **The lite LLR choice is defensible and should ship first** (N2 gives the reason the exact
  trinomial cannot simply replace it).
- **Live-only classes are named, not inherited.** E-0012 lists what the offline report does not
  validate. The enumeration in Missing Arguments is a completeness check on that list, not a
  discovery of silence.

## Disagreements — blocking findings (fix before `status: RUNNING`)

**B1 — the bands' pre-commitment is asserted, not verifiable, because the replay artifact is
untracked.** The task was to verify from git history that `[100,260]` was committed in the
script's docstring *before the first run* and never edited after a run. **Git cannot show
either, because the path is ignored** — `git check-ignore -v
research/context/w0005_sprt_replay.py` → `.gitignore:118: research/context/*`, and
`git log -- <path>` is **empty** (E-0012 itself has exactly one commit, `2a9d997`,
2026-09-22 21:09 +0300). What I *can* verify, and did: (i) the script hash `94631d6b…d1233c`,
the output hash `9cd40402…ea35ad` and the k6n input hash all equal E-0012's pinned values, so
neither file has been edited since that commit; (ii) mtimes are consistent with the claim
(script LastWrite 17:24:11 < output LastWrite 17:28:23, same day) — consistent, not proof, and
mtimes are trivially forgeable; (iii) the band is anchored on model predictions (191/173/133)
that are independently derivable (`w0002_power.py`; my re-derivation above), so it is not a
post-hoc fit of its own output. Fix (cheap, before RUNNING): move the script + output under a
tracked path (e.g. `research/scripts/`) or add a targeted `!` exception to `.gitignore` and
commit them with E-0012, so the claim becomes auditable rather than resting on one docstring.
Provenance finding only: it changes no rule, and the numbers are reproduced here independently.

**B2 — resume/durability policy, and the qualification of the "identical decision" claim.**
Contract item 5 says: per-game checkpoint (`W/D/L`, `LLR`, `next_game_index`, tier, salt)
fsync'd after every game; on resume the harness "REPLAYS the games JSONL and asserts the
reconstructed cumulative LLR equals the checkpoint to 1e-9 before continuing". Unspecified, and
each is a real failure mode: (i) **write order / durability order** between the JSONL append and
the checkpoint fsync — a crash between them leaves one artifact ahead of the other, so the
assertion fails by construction; (ii) **authoritative artifact + failure path** — on mismatch,
abort, continue, or "repair"? Name it: JSONL authoritative; recompute W/D/L + cumulative LLR by
replaying it; record a `resume_mismatch` incident; continue only if the recomputed state equals
the checkpoint to 1e-9, otherwise ABORT and file the run FAILED. (iii) the assertion is a
**self-consistency check only** — both sides come from the same LLR code path, so a systematic
scale/sign bug passes it; the scale detector is the offline exact-value reproduction
(179 / +2.985) plus unit tests (i)–(iii); say so. (iv) **"identical decision whether run in one
process or resumed" is not provable as written**: it holds up to floating-point summation order
and only if no cumulative LLR lands within 1e-9 of a bound — either state that qualification or
make it an actual test (split a canned sequence at *every* k, resume-and-continue, assert
identical verdict *and* crossing index). (v) `runjob.py` facts the contract must acknowledge:
`resume` is a plain re-launch of the same command line, idempotence is the JOB's duty,
`launch` **deletes** the previous log (`log.unlink()`), and the supervisor's checkpoint telemetry
counts raw `splitlines()` — a torn line counts as an item. The harness must preserve the
interrupted log itself and must not treat `runjob.py`'s counts as an integrity signal.

## Disagreements — non-blocking findings (route to the record)

- **N1 — the bands' information content, quantified.** At the operating point the crossing time
  has sd ≈ 42 games, so Tier S's `[100,260]` is ≈ ±1.9σ around 179: a ~5.4 % two-sided false-FAIL
  rate from sampling noise alone, and its detection floor for a *constant LLR-scale error* is
  1.79× upward / 0.69× downward (crossing = 179/scale must leave the band). The Tier R and M
  "no decision within 240" bands are, in contrast, near-tautologies: at Tier R the needed
  excursion is ≈4.6σ (P ≈ 2×10⁻⁶), at Tier M ≈1.7σ (a few percent) — consistency checks, not
  tests. E-0012 already labels them "secondary consistency", which is the right framing; add the
  numbers, the detection floor, and one sentence on what a (v2)-only FAIL means (harness audit
  first — the record's own "harness bug, not a surprise about the engines" — before any claim
  that the model is dead).
- **N2 — the exact-trinomial "allowed refinement" is under-specified, and that is a reason to
  ship lite.** The trinomial LLR needs a model for the draw probability as a function of δ; the
  tier margins alone do not identify it (the lite form is what makes the per-game term a function
  of δ only). DEC-0010's cross-check (score-space, Var = 0.1923) agrees in sign and verdict,
  which is evidence the choice is not fragile — but the refinement clause should demand a
  *pre-registered draw model* as part of "separate validation", else the refinement is a
  degrees-of-freedom generator.
- **N3 — classes the offline replay cannot see** (completing E-0012's own list): UCI handshake and
  EvalStage echo assertion; time-control enforcement; `bestmove` deadline/stall detection;
  crash-rule scoring; colour alternation as *played* (not as logged); application of the derived
  opening to both engines; checkpoint durability order; cap enforcement; ≤2-pair discipline; salt
  freshness vs the training set (see R-0011 B1); result adjudication (mate vs rule50 vs repetition
  vs plycap); one-look discipline. (v1)–(v4) do catch the two big classes (an arm swap flips the
  sign; both-engines-same flips to no-crossing), so the residual exposure is mostly *engineering*
  defects the live run will surface as crashes/stalls — acceptable for a harness validation,
  provided the build's unit tests cover the replay/continue path (B2 iv).
- **N4 — recommended addition: a live null-pair bias control** (pre-register before RUNNING if
  adopted). The live validation as written decides a known *large* difference (stage-6 vs stage-0,
  +116.1) — it cannot see a small per-arm bias. A cheap complement: stage-6 vs **stage-6**, cap
  240 games (~0.3 h): under a correct harness the cumulative lite LLR at Tier S has drift
  ≈ −0.0015/game (a tiny structural H0 lean) and sd ≈ 0.058/game, so crossing ±2.9444 within 240
  games needs ≈0.24σ/game of bias — a 3σ-class alarm for harness defects, not a strength test.
  Colour-correct the statistic against the measured prior: White scores **58.5 %** in the retained
  E-0010 data (k6: 0.783 as White vs 0.542 as Black; my measurement, R-0011 N6), so the control's
  null is not "50 %", and a naive centred band would be an F6-class defect in reverse. This is the
  one place where a low-power Elo *instrument* is worth pre-registering — for bias, never for
  strength.
- **N5 — note the mild circularity of σ, and why the replay still earns its keep.** σ = 371
  Elo/game was obtained from the six rungs' own CI half-widths, and the h(N) model then
  "reproduces" the k6 half-width — a consistency check on the same data, not a validation. What
  the offline replay adds is different in kind: it tests the *path* (first-passage time under the
  stated rule), which the CI fit does not. Say that in E-0012's Interpretation, so the ASN-model
  claim is not read as stronger than it is.

## Missing Arguments

- **Does the offline report discharge D-0007's routed "W-0005 model validation" residual? — Only
  PART of it.** D-0007 routed: "validate the ASN model by replaying the E-0010 k6 JSONL through
  the SPRT logic and comparing realized stopping games against the predicted ~191 (screen) /
  ~713 (regress)". Discharged: the screen prediction (realized 179 vs 191 Wald / 173 lite) at the
  +116 operating point, plus all-rung sign-consistency. Not discharged: (a) the ~713 regression
  prediction has *no realized counterpart* — "no crossing in 240" is not a comparison, and I
  quantify it as a near-certain event under the model (≈1 − 2×10⁻⁶), i.e. consistency only;
  (b) nothing about the ASN distribution (single sequence; the record says this); (c) nothing
  about the live harness. E-0012's own wording ("discharged at the offline level") is accurate and
  does not overclaim; the reviewer's addition is that the R/M half of the residual is *weakly*
  tested, so D-0007's residual should be read as "replay half done, live half open" — W-0005 stays
  OPEN, which is how it is filed.
- **Who validates the *harness*, not the rule?** (v1)–(v4) validate the harness against one known
  large effect. Nothing in E-0012 validates that the harness *stops* when it should stop on a null
  pair (N4), and nothing validates the honest-INCONCLUSIVE path live. The offline replay cannot
  produce either (it never reaches a cap). If the author wants the INCONCLUSIVE path covered, a
  240-game null-pair control (N4) doubles as that test.

## Factual Errors

None. Two precision notes: (i) the "score-space check" (prediction 133) is a different model of
the same quantity, not an independent LLR run on the same statistic — E-0012's table labels it
correctly; (ii) "predicted ~191" is the *Elo-space* Wald crossing, labelled "Wald" in the output
and "model predictions 191/173/133" in the record — consistent, but downstream citations should
keep the model label with the number.

## Assumptions

- The lite LLR implicitly assumes the per-game score variance equals the score-space variance
  (measured 0.1923 at k6) — the drift/ASN model was calibrated in Elo space. DEC-0010's cross-check
  covers this at the two edges; the assumption is named here so a future refinement does not
  silently re-use the lite ASN tables.
- The replay assumes `res: "A"` is the H1 arm; verified against E-0010 (+116.1 with A-score
  0.6625) and against the direction of every ladder rung.

## Proposed Experiments

1. **Track the replay artifacts** (B1) — move `w0005_sprt_replay.py` + `…_output.txt` under a
   versioned path (or add a `.gitignore` exception) and commit; owner: researcher-architect /
   systems-researcher; engine-free, minutes.
2. **Resume/equivalence unit test** (B2 iv) — canned sequence split at every k; the resumed run
   must reproduce verdict and crossing index. Part of `tools/e0012_sprt.py`'s build
   (systems-researcher).
3. **Live null-pair control** (N4) — stage-6 vs stage-6, cap 240, pre-registered statistic with a
   colour-corrected null; ~0.3 h once F-0002 is lifted.
4. **Live validation as already pre-registered** (E-0012's (v1)–(v4), stage-6 vs stage-0) —
   contingent on F-0002; its realized stopping time is W-0005's exit check and DEC-0010's own
   reversal-condition #1 test.

## Verdict

**NOT CLEAN — two blocking findings (B1, B2) plus five record-level findings (N1–N5); E-0012
stays PENDING.** No finding here changes the pre-registered rule: the tiers, the lite LLR, the
bounds ±2.9444, the caps, the bands (v1)–(v4) and the INCONCLUSIVE clause all survive, and the
offline replay's numbers reproduce exactly from my own code. The blocking items are execution and
provenance preconditions — make the replay artifact auditable, and say what "resume" means when
the two artifacts disagree — both of which must land before `status: RUNNING` (which F-0002 blocks
anyway). The offline report's claim on D-0007's residual is **partial and honestly stated**.

## Date

2026-09-22

> A review never edits the original report — it lives here and is linked from the debate/report
> it concerns.

## Evidence appendix (my own runs this session)

1. `python research/context/w0005_sprt_replay.py` → **exit 0**; k6 S H1 @179 final +2.985;
   R +1.098; M −0.673; all-rung totals match E-0010; duplicate-move-lists = 0; `a_white`
   100/200 (120/240 k6). My fresh output is **line-for-line identical** to the pinned
   `w0005_sprt_replay_output.txt` (44/44 non-blank lines, ASCII-normalised; the original capture
   carries a cp1252 em-dash byte where a fresh run emits U+2014).
2. `python research/context/w0002_power.py` → **exit 0**; prints σ=371, ASN S 1822/2025,
   R 29,159/32,399, M 292/324, and the score-space crossings 133 / 495 / 970.
3. `python research/scripts/research.py validate` → **exit 0**, "Validation OK … 0 problems"
   (warnings only).
4. My independent derivation (`%TEMP%\krev10\independent_llr.py`, own formula implementation —
   never imports the author's script): reads `e0010_k6n_games.jsonl`
   (SHA-256 `9da1cfa0cb24ed94cf4a64ad47c0fed9387b5a3163b590153677e61c1fd0d227`), prints
   `N=240 W=144 D=30 L=66 dup_move_lists=0`; `S [0,+20]: verdict=H1 crossing=179
   final/cross-LLR=+2.985`; `R [0,+5]: None +1.098`; `M [100,150]: None -0.673`; closed-form
   totals +4.093 / +1.098 / −0.673; `h(1000) = 22.99`; Tier S drift/game 0.01705, sd/game 0.05444,
   expected crossing 172.7, sd(crossing) 41.9; null-pair drift −0.001656, sd 0.05756, bias needed
   to cross +2.944 in 240 games = 0.01227/game.
5. Git/artifact checks: `git check-ignore -v research/context/w0005_sprt_replay.py` →
   `.gitignore:118`; `git log -- research/context/w0005_sprt_replay.py` → empty;
   `git log -1 -- E-0012` → `2a9d997 2026-09-22 21:09:37 +0300` (single commit); SHA-256 script
   `94631d6b1105795f83f662a35df1db260ce9db8df286c1f0fdd5fb3f39d1233c`, output
   `9cd40402e5426a09367c1a9c370aa9fa89ff8c2aab8f4e03d4983e8d68ea35ad` — both equal the pins in
   E-0012 §Provenance.
6. Gate 0: one attempt, Device Guard block, no process — appended to
   `research/context/bootstrap/gate0.txt` (attempt #7, capture `gate0_session_run.txt`).


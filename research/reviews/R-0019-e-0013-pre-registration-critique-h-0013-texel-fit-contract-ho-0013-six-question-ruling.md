---
id: R-0019
type: review
reviewer: adversarial-reviewer
target: E-0013
kind: critique
status: COMPLETED
work_item: null
related: [HO-0013, E-0013, E-0012, E-0011, E-0010, H-0013, H-0010, H-0004, Q-0006, DEC-0010, DEC-0009, W-0001, W-0003, W-0005, R-0011, R-0012, R-0014, R-0017, R-0018, S-0023, tools/e0011_check.py, tools/e0012_sprt.py, tools/e0011_generate.py, src/eval.h, src/eval.cpp, src/main.cpp]
example: false
created: 2026-09-26
---

# R-0019 — Critique of the E-0013 pre-registration (H-0013 Texel fit contract) — HO-0013 six-question ruling

## Scope

Fresh adversarial-reviewer occupant (S-0024), receiving HO-0013. **I did not draft
E-0013 and I do not defend it.** I did not edit E-0013, H-0013, DEC-0010,
`tools/e0012_sprt.py`, R-0017/R-0018, RUN-0002/RUN-0003, or any H-#### status;
I did not start the HO-0005/W-0003 audit; I did not flip E-0013 to `RUNNING`;
and I ran **no** training, fitting, extraction, relabeling or SPRT game
generation. Nothing has been fitted; no fitted parameters exist.

I read, in order: HO-0013; E-0013 (the full PENDING contract); H-0013;
E-0012; R-0018; DEC-0010; W-0001 (leakage contract, N1 ladder);
HO-0008 (the structure and pure-additions discipline I am modelling);
Q-0006; W-0003; `tools/e0011_check.py`; `tools/e0012_sprt.py` (cited
unmodified — I read it and did not touch it). I also read, because the
contract's executability depends on them, `src/eval.h`, `src/eval.cpp`,
`src/main.cpp` and `tools/e0011_generate.py`, and the on-disk terminal
checker diagnostic `m0_audit/e0011/check_output.txt`.

Two structural facts I verified rather than assumed, because both are
load-bearing and neither is stated in E-0013:

1. **The quiet-proxy count is a ply count, not a distinct-position count.**
   `tools/e0011_check.py:385-398` iterates only over `row["san"]` (the
   post-opening engine segment) and increments `quiet_proxy` **per ply**; the
   `opening` segment is never a candidate. The same function's `positions`
   Counter (lines 371-383) is the distinct-FEN instrument, and it reports
   `duplicate_positions=1705` over `total_positions=130930`.
2. **The validated SPRT harness launches ONE binary and differentiates only by
   an integer EvalStage.** `tools/e0012_sprt.py:325-326`:
   `engines = (Engine(Path(args.exe).resolve(), args.stage_a), Engine(Path(args.exe).resolve(), args.stage_b))`;
   line 301 records a single `binary = sha256_file(Path(args.exe).resolve())`;
   `parse_args` (lines 474-487) exposes one `--exe` and integer
   `--stage-a/--stage-b`. There is no second executable, no parameter-artifact
   path, and no per-arm hash.

## Arithmetic I Did Myself (so the owner can check it without re-running anything)

**Yield.** From the on-disk terminal diagnostic
(`m0_audit/e0011/check_output.txt:2-3`, R-0017-VERIFIED dataset):
`san_position_yield=120930`, `opening_plies=10000`,
`quiet_proxy_opening_skipped=76593`, `duplicate_positions=1705`,
`total_positions=130930`, `degenerate_mate_san_le_6=1`; `end_counts` contains
no `crash` row. The 1,000 games each carry 10 opening plies
(`e0011_check.py:57`), so `san` begins at ply 10 and the first two candidate
plies are `full_ply` 10 and 11 — nothing is lost to the ply floor. Therefore:

- `76593` is a **per-ply count over the `san` segment**, not a distinct-FEN
  count. `tools/e0011_check.py:385-398` iterates only `row["san"]` and
  increments `quiet_proxy` per ply; the `opening` segment is never a candidate.
- Cross-game FEN duplication is measured at `1705 / 130930 = 1.302 %`.
  Projected onto the quiet subset: `0.01302 × 76593 ≈ 997` duplicates, so the
  distinct-FEN quiet yield is **≈ 75,600**.
- E-0013's own exclusions remove at most the one degenerate game
  (`len(san) <= 6`, i.e. ≤ 6 positions) and zero crash games, giving an
  **honest realized band of 75,600 ≤ realized usable yield ≤ 76,587**.

Against E-0011 N1's 30k floor that is **2.5× headroom**. The ladder does not
arm. The brief's "~27k quiet positions" is not merely UNVERIFIED — it is
refuted, and refuted in the dangerous direction: 27k sits *below* the 30k floor
it would be compared against, so adopting it would have silently triggered the
fallback scope. E-0013's flag and its choice to let the measured figure govern
are **correct**, and I confirm them.

**Stage-(a) power.** The label is game-constant, so the holdout's independent
units are the holdout **games**, not the holdout positions. The estimator is
the mean over G ≈ 200 games of the per-game mean paired loss difference, with
`SE = s_d / sqrt(G)` on `t_{0.975, G−1}`. A margin `m` is decidable at
α = 0.05 two-sided, 80 % power, at G = 200 iff

```
m  ≥  (1.959964 + 0.841621) · s_d / sqrt(200)  =  0.19810 · s_d
⇒  s_d  ≤  0.002 / 0.19810  =  0.010095
```

`s_d` is the per-game SD of the paired loss difference. It is **not measured
anywhere in E-0013** and is not derivable from any artifact on disk. For
scale: at `s_d = 0.010` the 0.002 margin sits at 1.44 CI half-widths (power
≈ 0.85); at `s_d = 0.020`, 0.72 half-widths (power ≈ 0.33); at `s_d = 0.050`,
0.29 half-widths (power ≈ 0.10). The verdict flips entirely on an unmeasured
quantity.

**Stage-(b) power at the tightened cap.** DEC-0010's Tier-S ASN is ~1,820
under H1 and **~2,025 under H0**. E-0013 tightens the cap from 8,000 to 2,000
and says so. Because ASN(H0) = 2,025 > 2,000, a *genuine regression* ends
INCONCLUSIVE roughly half the time rather than FAIL. See Q4 and DN9.

**Stage-5 opponent identity.** With DEC-0010's own `h(N) = 727/sqrt(N)`:
k5 = +127.6 at N=200 → CI95 [+76.2, +179.0]; k6 = +116.1 at N=240 →
[+69.2, +163.0]; k4 = +100.8 at N=200 → [+49.4, +152.2]; k3 = +104.5 at
N=200 → [+53.1, +155.9]. The four intervals overlap almost completely, so
"stage 5 is the strongest measured rung" is a point-estimate ranking the
sample does not support.

**E-0010's attribution, recomputed from its own ladder** (E-0010:341-344;
stage map from `CMakeLists.txt:11`, `0=material,1=taper,2=+PST,3=+pawn,4=+mobility,5=+positional,6=+tempo`):
k2−k1 = +46.0 (taper+PST) · k3−k2 = **+22.2 (pawn)** · k4−k3 = **−3.7 (mobility)**
· k5−k4 = +26.8 (positional) · k6−k5 = **−11.5 (tempo)**. This reproduces
E-0010's printed attribution exactly, and it is load-bearing for Q-SCOPE.

## Rulings — the six mandatory questions

### Q1 — Free parameters pinned? **NOT CLEAN — BLOCKING (B3, B4, B5)**

**CLEAN and confirmed, with the closing sentence quoted:**

- Taper/phase: "`phase = min(1*N + 1*B + 2*R + 4*Q, 24)`",
  "`score = (mg * phase + eg * (24 - phase)) / 24`", "the formula itself is NOT
  fitted — the phase weights are frozen integers" — verified against
  `src/eval.cpp:236-237` and `write_eval_p5.py:85-87`.
- Frozen list: phase weights, `GAME_PHASE_MAX`, FLAT_VALUE staging, mirror
  `s ^ 56`, tempo sign convention, all search/UCI/TC code.
- KING material "`20000/20000, NOT fitted`"; tempo "`the sign convention is NOT
  fitted`"; KING-PST symmetry "`pst[s] == pst[mirror(s)]` under `s ^ 56` or the
  symmetry gate FAILS".
- NPS band "`fitted binary within 10% of the pinned binary … regression beyond
  −10% = FAIL`"; symmetry gate "1000 positions full-mirror … 0 violations";
  deterministic-rerun "`refit with the same seed reproduces the artifact hash
  or the run FAILS`" — all pinned, all gating.
- **The fitted list is complete against the struct.** I compared `src/eval.h`'s
  `EvalCoeffs` member-by-member with E-0013's items 1-6: every scalar in the
  struct appears exactly once in E-0013's list and nothing in the list is
  absent from the struct. "Fitted (all scalars inside `EvalCoeffs`)" is
  literally true. This is a genuinely well-built free-parameter section.

**FREEZE AUDIT — every value that could still be chosen or re-derived after
the holdout loss is visible, and the sentence that closes each one.** F12 is
the only one already closed for me.

| # | Value at risk | Contract wording | Closing sentence? |
|---|---|---|---|
| F1 | Fitting-method family (Q-FIT) | "`OPEN — designer-blocking`" | **NO** — and the named alternative optimizes the holdout |
| F2 | Fitter seed, L2 weight, iteration budget, early stopping | "landed as a dated addendum … BEFORE running" | **NO** — closed against *timing* only, never against holdout-derived selection; no anchor to the split-map commit |
| F3 | KING-PST freeze-vs-fit (≈240 free params) | "`final choice pinned at execution preflight from this list`" | **NO** — a first-time assignment by the seat that will report the holdout loss |
| F4 | Tactical-suite identity, N, metric, **tolerance** | "`exact tolerance + metric pinned with the suite list before fitting`"; "`OR the suite is replaced by a same-N independent spot check`" | **NO** — "tolerance" is a placeholder for a number, and the substitution path is exercisable at conjunct (f), i.e. after (c) and (e) are read |
| F5 | MAE phase-tertile boundaries | "`boundaries pinned at execution preflight`" | **NO** |
| F6 | Fresh SPRT salt | "`fresh salt distinct from ALL prior salts`" | **NO** — the value is unassigned, and R-0018 Q4 names opening-subset sensitivity as unexplained |
| F7 | EvalStage at which stage (a) is scored and against which floor | *nowhere in the record* | **NO** |
| F8 | Label frame (White-perspective vs side-to-move) for a Black-to-move position | "`exact mapping code pinned at execution`" | **NO** — and the literal reading is the wrong one |
| F9 | Dedup scope: global-before-split vs per-split-then-assert | "`dedup exact-FEN within the extraction before the split counts are reported`" | **NO** — ambiguous, and the realized counts depend on it |
| F10 | Salt-distance citation | "`distance citations computed at execution`" | **NO**, but immaterial — the arithmetic is already adequate (Q2) |
| F11 | `LOSS_MARGIN = 0.002` | hard-coded | the *number* is frozen; its **attainability** is not (B3) |
| F12 | Per-game position cap | "`cap = all quiet positions`" + "`If the critic requires a cap, it must be named in critique and landed as an addendum BEFORE running — never silently`" | **YES** — the contract hands this to me. **My ruling: NO CAP.** 200 holdout games is already the binding denominator on stage (a); a cap shrinks the holdout, reduces power and adds a discretionary filter, while the BY-GAME split plus the normalized-FEN overlap-0 gate already carry the entire leakage obligation. Recording "no cap" here closes F12 and forbids re-opening it. |

**The one sentence that closes a whole class — and what it fails to cover.**
E-0013's tripwire — "Any threshold, salt, cap, suite, or margin changed after
seeing data = FAIL (p-hacking tripwire)" — is the right instrument. It binds
*changes*. It does **not** bind *first-time assignments*, and "seeing data" is
nowhere scoped to the holdout. Every value in F1–F10 is a first-time
assignment, not a change. The split map is the single value the contract does
close properly, precisely because it gets its own pre-read commit. B4 supplies
the missing general anchor.

### Q2 — Holdout-split leakage? **NOT CLEAN — BLOCKING (B4); the split mechanism itself is CLEAN and strong**

**What genuinely holds, with evidence:**

- **Salt separation is adequate, and I computed it rather than accepting "at
  execution."** The seed derivation is `salt * 1_000_003 + game_index`, so for
  any two distinct salts the derived seeds differ by at least 1,000,003, which
  exceeds any game-index span in play (0..999 for E-0011; 0..1,999 at E-0013's
  2,000-game cap). For E-0013:
  `|20260926 − 20260924| × 1,000,003 = 2,000,006 ≥ 1,000,003 > 1,999`, so no
  `(salt, game_index)` pair can collide with the E-0012 live campaign. The
  `8,000,024` figure in E-0011 was the |Δsalt| = 8 instance of the same
  inequality; Δsalt = 2 is equally safe. The salt is fine.
- **Game-level overlap-0** under `tuple(opening) + tuple(san)` is sound and is
  the *same* dedup key E-0011 pinned as its own gate (c), so the two records
  compare like with like.
- **Normalized-FEN overlap-0 is correctly specified, including the part that is
  easy to get wrong.** E-0013 pins the normalization as "side-to-move + piece
  placement + castling/EP rights" — deliberately **excluding** the halfmove
  clock and fullmove number that `python-chess`'s `board.fen()` would otherwise
  carry. That is the right choice and it is stated, which closes the
  nearest-identical-FEN channel a naive FEN comparison would have left open.
  Genuinely good work.
- **Position-level relatives across games: caught, and the gate is
  load-bearing rather than decorative.** The terminal checker's `positions`
  Counter is keyed on `board.fen()` across all 1,000 games and reports
  `duplicate_positions = 1705`, so cross-game FEN collisions demonstrably exist
  in this dataset. The normalized-FEN overlap-0 gate is what stops them
  crossing the split. This is the strongest part of the contract.
- **Threefold / repetition draws: closed, by the FEN gate.** The quiet
  predicate does not exclude repetition positions, so the 41
  `end == "repetition"` games do carry repeats — but repetition *within* a game
  is harmless (a game sits wholly on one side of a BY-GAME split), and a
  repetition position reachable from both a train game and a holdout game by
  different move orders is an **exact** FEN collision, which the gate catches.
  No residual channel.
- **Colour-flipped transpositions: not caught, and acceptably so — but only via
  a dependency the contract must not weaken.** A colour-flipped relative is a
  different normalized FEN, so the gate misses it. It is harmless *here*
  because the eval is required to be colour-symmetric (mirror `s ^ 56`), which
  conjunct (d) enforces at 0 full-mirror violations over 1,000 positions. The
  channel is closed by construction. **If (d) is ever relaxed, a colour-flipped
  relative becomes a live leakage channel** — the contract should say so,
  because today the closure is implicit and load-bearing.
- **Is the split-map commit a blocking pre-condition, or merely intended? It is
  a genuine blocking pre-condition, stated three times in the right words.**
  "The game_id->split map (with its SHA-256) is committed BEFORE any fitting
  job reads the data (hash logged in the RUN record first)"; Test Method step 3
  "Commit the game-split map hash BEFORE fitting; run the overlap-0 gate
  (blocking)"; conjunct (b) "split map hash committed before fitting … Violation
  = FAIL before fitting". That is a gate, not an intention, and it is the one
  piece of freeze architecture in this record that is fully closed.

**What is not closed:** the 76,593 diagnostic as a **selection surface** (I
probed this specifically — it is a whole-dataset, **label-free** count, so it
cannot inform the fit's direction or magnitude; its one real effect is that it
decides conjunct (a)'s branch before the split map exists, making the scope
branch a whole-dataset quantity. Benign in effect; still, conjunct (a) should
be evaluated on a **train-only** count. Non-blocking, required text); and F3,
F6, F8, F9 from the freeze audit.

### Q3 — Achievement floor frozen and non-apathetic? **NOT CLEAN — BLOCKING (B3)**

- **The rhetoric is genuinely frozen, in three places:** the rule preamble
  "anything else that fails is FAIL, never 'baseline preserved' (HO-0008
  anti-apathetic-failure lesson: no achievement = FAIL)"; conjunct (c) "No
  achievement = FAIL (anti-apathetic clause)"; conjunct (e) "the experiment
  then ends INCONCLUSIVE, never 'baseline preserved'". I could not find a
  rhetorical route from a null to "baseline preserved", and I looked for one.
- **The CI construction is correct.** "the paired difference's 95 % CI (paired t
  over holdout games, clustered BY GAME)" clusters on the right unit and does
  **not** understate the SE on the game-correlation axis. E-0013 got the
  clustering right. CLEAN on construction.
- **But the justification offered for the FAIL-not-INCONCLUSIVE choice is
  false, and that is the one remaining route by which a null becomes a
  mislabelled rejection.** Conjunct (c) reads: "A CI that includes 0 = FAIL, not
  INCONCLUSIVE (the holdout N is large; power is not the binding constraint
  here)." Both halves fail. The holdout's independent units are ~200 games, not
  the "~15k positions" the Power section cites — the label is game-constant. And
  `LOSS_MARGIN = 0.002` is decidable **iff `s_d ≤ 0.0101`**, a condition on an
  unmeasured quantity, against which the record asserts decidability "for any
  realistic loss variance" — an unbounded quantifier over something nobody has
  measured. This is precisely the failure mode DEC-0010 was written to kill:
  "bars inherited from ambition rather than derived from measured variance
  already produced one unwinnable threshold (F6, E-0010)".
- **And the margin may be *unwinnable*, which is worse than aspirational.**
  Because the label is constant within a game, the best any position scorer can
  do is bounded by the within-game spread of position quality among positions
  sharing an outcome. If that attainable gain is below 0.002, conjunct (c) is a
  **guaranteed** FAIL — unpassable by any fit, honest or otherwise — while the
  record simultaneously asserts stage (a) is decidable. An unwinnable gate plus
  a decidability claim is the F6 pattern with the anti-apathetic clause wrapped
  around it.
- **Ruling on the 0.002 margin itself:** I am not asking the owner to raise it
  and I am not asking to weaken it. 0.002 is defensible as a small, paired,
  directional margin and is a real improvement on the brief's underived ±0.10.
  My ruling is that it must be made **decidable rather than asserted**: a
  pre-registered, non-training, **train-only** feasibility pass measures both
  the attainable gain `delta_star` and the cluster SD `s_d` *before* the margin
  binds, and the margin and the FAIL/INCONCLUSIVE split become functions of
  those measurements. That keeps the anti-apathetic clause fully intact for the
  fit's *quality* while refusing to let a *power* failure masquerade as an
  apathetic-fit rejection.

### Q4 — Does the strength gate inherit E-0012's scope ruling? **NOT CLEAN — BLOCKING (B1); the scope discipline itself is CLEAN and well done**

**CLEAN, and I want this on the record because it is the part of the contract
that most needed defending and it holds:**

- The Hypothesis states the separation explicitly: "A good holdout correlation
  alone is NOT a strength claim; the harness decision is." **No slide from fit
  quality to playing strength.**
- The Baseline carries E-0012's ruling forward: "E-0012 licenses no
  engine-strength claim; any fitted-vs-pinned result is decided by its own
  pre-registered run under this contract."
- Conjunct (h) is a first-class gate with teeth: "no engine-strength overreach
  beyond the Tier-S zone (E-0012 scope ruling inherited: a Tier-S H1 licenses
  'worth keeping', never a Tier-R 'stronger' or Tier-M magnitude claim)".
- The cap was **tightened, not loosened**: DEC-0010's Tier-S cap is 8,000;
  E-0013 sets 2,000 and states "A wider zone or larger cap is NOT authorized
  without a new power addendum." A shrink, with the reasoning on the page.
- The Tier-S shape is cited, not re-derived: ASN ~1,820 / ~2,025 / ~4,050, and
  "a true +5 effect does NOT (INCONCLUSIVE-by-design at cap 2,000 — the Tier-R
  claim needs ~29-32k games / ~39 h, a round-boundary campaign, not this
  experiment)". Correct against DEC-0010 and honest.
- **The replay acknowledgement is correct and the mitigation is genuinely
  checkable.** Conjunct (g) requires the verbatim sentence "the 125-vs-179
  replay crossing delta is unexplained per R-0018 Q4 and is treated as sampling
  variation, not a settled harness property" — matching R-0018's own lines 147
  and 150 ("unknown: exact contribution of opening subset differences to game
  125 vs 179 crossing time") — plus opening-book-hash logging and paired-colour
  reporting. Both are checkable: the opening book is a pure function of the
  salt and the game index, so its hash is reproducible from the salt alone;
  A-as-White vs A-as-Black is a direct recount of the JSONL. "Claiming the
  harness is settled = FAIL of this conjunct" is the right tripwire.

**BLOCKING (B1) — the stage-5 opponent is a cherry-picked *point estimate*, and
the "A != B by handshake hash dump" mandate is not executable:**

1. `A != B` **by handshake-hash dump cannot be done, because there is no hash to
   dump and no way to make the arms differ.** `tools/e0012_sprt.py:325-326`
   builds *both* engines from the single `--exe`; line 301 records one binary
   hash for both arms; the engine's UCI surface advertises and accepts only
   `Hash` and `EvalStage` (`src/main.cpp:103-114, 133-147`) and emits no
   parameter hash; `EvalCoeffs` is a compiled-in static
   (`src/_write_eval.py:25`) with no loader. So `--stage-a 5 --stage-b 5` is
   the W-0001 stage-6 self-collision this record explicitly forbids, and
   `--stage-a 6 --stage-b 5` compares the hand-tuned eval against itself minus
   tempo. **The mandate and the cited tool are mutually exclusive as written.**
2. **The one precedent E-0013 leans on does not support the claim it makes.**
   E-0012's Sample Validity says "the handshake echoes each engine's effective
   `EvalStage`". `src/main.cpp` does not do that: the option is printed with
   its *compiled default* and `setoption` is applied **silently, with no echo**
   (lines 124-147). R-0012 had already flagged "UCI handshake and EvalStage
   echo assertion" as a blind class the offline replay cannot see. R-0018 then
   verified arm differentiation only **behaviourally** — "produced distinct play
   and clear divergence" — never by an echo. E-0013 inherits the overstatement
   and tightens it into an impossible requirement. I checked specifically
   because "EvalStage silently never applied" is a defect that already voided a
   full campaign here (E-0010: "all previous gate-(c) data was methodologically
   void").
3. **The stage-5 choice is not justified by the data it cites.** "Stage 5 is the
   strongest measured rung" rests on a point estimate whose CI ([+76.2, +179.0]
   at N=200) overlaps k6's, k4's and k3's almost entirely. It is *not* a soft
   target — k5 is the highest point estimate, i.e. the hardest opponent — so
   this is not self-serving cherry-picking. But the stated inference does not
   follow from the stated evidence, and E-0013 inherits E-0010's "(N=240)" for
   a ladder whose rungs are N=200 (DN1).
4. **The stage index is a structural incoherence nobody has named.** The only
   difference between stage 5 and stage 6 is the tempo term
   (`if (stage >= 6) score += C.tempo;` — `src/eval.cpp` /
   `write_eval_p5.py:86-87`). So: the training data was generated at
   `eval_stage_a == eval_stage_b == 6` (E-0011:309); the SPRT opponent is
   stage 5; and the fitted set includes `tempo` as a free coefficient. **The
   fitted `tempo` entry is therefore inert in both stage-(b) arms and
   unidentifiable at the deployed stage** — while whether gate (c) even scores
   it depends on an EvalStage the record never states (F7). Gate (c) could end
   up being partly a score on a coefficient that cannot affect a single
   measured game.
5. `--validation-known` must not be passed on any E-0013 run:
   `tools/e0012_sprt.py:299` raises unless
   `(tier, stage_a, stage_b, cap) == ("S", 6, 0, 8000)`. E-0013 does not say so.

### Q5 — Power honesty given the budget? **NOT CLEAN — BLOCKING (B3, B4); the yield flag is CLEAN and correct**

- **The "~27k" flag is CORRECT and I confirm it with arithmetic.** See "Yield"
  above. The measured 76,593 governs; the brief's ~27k is refuted and is
  actively scope-changing, not conservative. E-0013's wording — "the checker's
  measured 76593 governs until a verifier rules otherwise" — is right, and
  refusing a session-brief figure that no on-disk artifact supports is the
  correct instinct.
- **Does the 30k consequence ladder (E-0011 N1) still bind? No — and it does not
  come close.** Realized usable yield is bounded at 75,600–76,587 against a
  30,000 floor: 2.5× headroom. The all-terms scope survives on measurement and
  the fallback branch is disarmed. **But** if the ladder ever did arm, its
  fallback scope is cited to an attribution that says the opposite — see B5.
- **Is the pre-registered expected yield itself an assertion no one has
  measured? Partly yes, and this is a real finding.** E-0013 line 115 says
  "Expected yield (**measured**, not assumed)" and cites 76,593 — but 76,593 was
  measured by `tools/e0011_check.py` for the **bare quiet predicate only**:
  over the `san` segment, with no crash exclusion, no degenerate-mate
  exclusion, no dedup and no split. E-0013 then immediately imposes two of
  those exclusions and a dedup. So the word "measured" is applied to a number
  measured for a *different filter* than the one E-0013 will apply. The honest
  sentence is: 76,593 is measured for the bare predicate; the realized usable
  yield under E-0013's own filter is an unmeasured prediction bounded above by
  76,587.
- **My ruling on the scope floor, stated exactly as asked: the expected yield
  must be measured by a pre-registered, non-training count pass before the scope
  floor binds.** Concretely, conjunct (a) is evaluated on the realized count
  reported by a count-only extraction pass — the QUIET predicate plus the crash
  exclusion plus the degenerate exclusion plus the dedup plus the committed
  split map — run and hash-committed **before any fitter is invoked**, and that
  realized count, not 76,593 and not 27k, is the number that arms or disarms
  the 30k ladder. **I did not run that count and I must not**: it is an
  extraction over the dataset, which this seat is forbidden to perform. I have
  bounded it instead (75,600 ≤ realized ≤ 76,587), so the addendum only has to
  make the *rule* correct, not the number known in advance.
- **Which bands are aspirational at this N?** holdout margin → **yes, BLOCKING**
  (B3). Suite tolerance → **yes, BLOCKING** (B4). SPRT zone → **no**; it is
  DEC-0010's, cited unmodified, and the cap was shrunk honestly.
- **Concrete shrinkage, as the question asks.** Narrow the claim, not the
  threshold. The fitted artifact's licensed claim is "holdout *loss* improvement,
  directional, at a margin fixed by a pre-fit feasibility pass" — never a
  correlation or MAE number quoted as a quality figure, and never a strength
  figure. And the correct response to an undecidable stage (a) is a named
  INCONCLUSIVE with the measured `s_d` published, **not** a silent tightening of
  the margin.

### Q6 — Sequencing interactions? **CLEAN. No ordering constraint exists.**

- **Does anything in E-0013 presuppose a H-0010 status change? No.** E-0013's
  Follow-Up states "H-0013 and H-0010 status changes are EXPLICITLY out of
  scope for this record (needs their own decisions; the H-0010 status review
  stays sequenced AFTER this contract survives critique, per HO-0013 question
  (vi))". I checked what E-0013 actually cites: the **harness** (E-0012
  COMPLETED, W-0005 DONE, R-0018 VERIFIED) and the **tiers** (DEC-0010). It
  never cites H-0010's status. H-0010's appearance in `state.md:13` as
  "tested by … E-0013 [unverdicted]" is a generated projection
  (`research.py state --write`), not a status change, and E-0013 is PENDING.
  **The ordering constraint E-0013 itself names is correct and I endorse it:
  the H-0010 status review is sequenced AFTER E-0013 survives critique.** I
  change no H-#### status.
- **Does HO-0005 / W-0003's outstanding audit touch any artifact E-0013 cites?
  No — I enumerated E-0013's citation set and checked it item by item.** E-0013
  cites E-0011, H-0013, E-0012, R-0018, DEC-0010, W-0001, HO-0008,
  `tools/e0012_sprt.py`, `tools/e0011_check.py`, `m0_audit/e0011/games.jsonl`,
  `m0_audit/e0011/check_output.txt`, R-0017, and RUN-0002/RUN-0003 by reference.
  W-0003's deliverable is a *new review record* and its `exit_check` states
  "AGREEMENT_MATRIX.md left untouched as a historical artifact"; its work log
  confirms the matrix was not edited (R-0013 delivered 2026-09-22; W-0003
  `IN_PROGRESS` solely pending HO-0005's verification). E-0013 cites **none** of
  {R-0013, W-0003, HO-0005, `AGREEMENT_MATRIX.md`}. **No ordering constraint
  exists and none may be inferred.** HO-0005 is a paperwork verification of a
  paperwork backfill; it cannot move a number E-0013 depends on. The audit
  stays REQUESTED and out of scope, as instructed — I did not start it.
- **DEC-0010's own gate-3 debt is already discharged, so no constraint there
  either.** DEC-0010:186-187 still prints "Pending: independent verification per
  DEC-0009 gate 3", which is stale: `W-0002`'s Verification block records
  `verified_by: verification-auditor (occupant 4, zero chat history; HO-0002
  receiver)`, `verdict: VERIFIED (2026-09-22)`, evidence R-0010
  (`kind: verification`). DEC-0010 is independently verified. (Doc-nit DN6; not
  my file to edit.)

## Rulings — the open questions the owner left me (each: adopt / amend-with-exact-text / block)

### P0 vs P1 — the H-0013 dataset discrepancy: **ADOPT P1. Do not amend H-0013. P0 stays open, sequenced later.**

- H-0013's 2026-09-09 text says "Texel-tuned on ~50k quiet **Stockfish-labeled** FENs". E-0013 does not inherit that, and it is right not to: no external labels exist, none are licensed, and a Stockfish-label dependency is not on the roadmap. P1 (file against the E-0011 dataset) is the only option consistent with Q-0006's official gate 6 ("The fit consumes only the verified E-0011 dataset").
- **Amending H-0013 (P0) is a hypothesis-lifecycle change and stays out of scope**, exactly as E-0013 says. I am forbidden to edit H-0013 and I did not.
- **The sequencing ruling:** P0 must be filed as its own decision, and it is **blocked_by E-0013's terminal result**, not by E-0013's pre-registration. Reason: H-0013's stale sentence is *descriptive context*, not a gate — E-0013 already declares it non-inherited. So a P0 correction may land before, during or after the fit without touching any E-0013 threshold, but it must land **before** anyone reads H-0013 as a description of what was actually done. Route: a researcher-architect decision record superseding the sentence, filed no later than E-0013's close-out, and explicitly cross-referencing R-0019 so the correction is visibly downstream of this ruling rather than a quiet edit.
- **On the ±0.10 band:** E-0013's rejection is **correct and I adopt the rejection.** "the ±0.10 band has no power derivation behind it and is rejected here as aspirational" is right — and note the symmetry: my B3 finding is that E-0013's *replacement* (0.002) is also underived, only in the other direction. Rejecting the aspirational band and then installing a different underived band without measuring the quantity that decides it would be the same defect wearing better clothes.

### Q-LABEL — game result only vs result+search-depth blend: **ADOPT result-only, AMENDED with two exact sentences (B2).**

- Result-only is the only label present in E-0011 (E-0013 is right that no search scores were recorded), and the blend would require a new data campaign, which is out of scope. Adopt.
- **But the experiment is not thereby "INCONCLUSIVE-by-design for lack of labels"** — it is decidable, with a caveat that must be stated: the label is **game-constant**, so every position in a game carries the same target, and the fit is therefore learning a game-outcome classifier from position features, not a per-position value. That is a legitimate, well-known, weaker thing than a per-position Texel fit, and the record must not let "logistic loss improved" be read as "the eval is a better evaluator". 903 of 1,000 games end in `mate`, so the label is dominated by a single terminal class.
- The colour-frame ambiguity (F8) is the sharp edge and is B2's first sentence. Read literally, "res A/B/D mapped to 1/0/0.5 **from White's perspective at the position's side to move**" hands a Black-to-move position the White-frame target — and because the eval is colour-symmetric, a uniform White-frame target makes the fit learn "high eval ⇒ White wins" for *both* sides. The mirror symmetry gate (d) would still pass, because the eval stays symmetric while the target is asymmetric. That is a silent, catastrophic, and gate-invisible error. B2 makes the frame mandatory and checkable.

### Q-FIT — logistic/gradient Texel vs SPSA: **ADOPT logistic/gradient Texel; BLOCK SPSA; AMEND with three exact sentences (B4).**

- Adopt deterministic full-batch L-BFGS on the mean logistic loss, L2-regularized, with a pinned seed, a pinned iteration budget and a pinned clipping bound. The record's own confidence (medium) is right, and the reason is not aesthetic: a *deterministic* optimizer is what makes the existing "refit with the same seed reproduces the artifact hash or the run FAILS" conjunct actually enforceable. SPSA is stochastic, and a stochastic fitter makes the deterministic-rerun gate a coin flip rather than a check.
- **SPSA is blocked, and the record's own sentence for it is the reason:** "Alternative: SPSA on **holdout loss**." A method that optimizes the holdout is not an alternative optimizer, it is the leakage this review exists to prevent. That sentence must be withdrawn, not left as a live option.
- F2 (seed, λ, budget, early stopping) must be pinned in the pre-fit commit, not merely "in a dated addendum before running": a pre-run addendum authored by the same seat, with no anchor to the split-map commit, is still a first-time assignment made by the person who will report the holdout loss. B4's single pre-fit commit closes it.

### Q-SCOPE — all-terms vs mobility/tempo subset; KING-PST freeze vs fit: **ADOPT all-terms with KING PSTs FROZEN; and correct a backwards citation (B5).**

- **KING PSTs: FREEZE. Adopt the recommended option.** 240 additional free parameters (mg + eg, 64 squares each) fitted on ~1,000 games of stage-6 self-play is the least identifiable block in the set, and E-0010's own ladder attributes the positional block's +26.8 Elo to a single rung at N=200 whose CI half-width is 51.4 Elo — i.e. the term block is not even resolved by the measurement E-0013 cites to justify fitting it. Freezing is both the lower-variance choice and the one that keeps the fitted parameter count defensible against the "≥500 positions/parameter" standard E-0011 N1 established.
- **All-terms (not the mobility/tempo subset) is the correct scope at the honest yield**, because the ladder is disarmed by 2.5× headroom. Adopt — and note the choice is conditional on the count pass in B7, not on the 76,593 diagnostic.
- **And the ladder's fallback citation is backwards — a finding, not a preference.** E-0011 N1's fallback is "the mobility/tempo sub-set **E-0010's ladder motivates**". E-0010 (line 344) measures the marginal contributions as "mobility (−3.7) and tempo (−11.5) are non-positive with CIs crossing zero". The two terms the ladder names as the fallback scope are the two the ladder attributes the **worst** contributions to. I recomputed the deltas from E-0010's own published ladder and they reproduce exactly (k4−k3 = 100.8−104.5 = −3.7; k6−k5 = 116.1−127.6 = −11.5). A pre-registered rule that would auto-apply a scope justified by a citation that says the opposite is a latent trap, even though it is currently disarmed. B5 records the required correction.

### Q-SUITE — independent tactical suite vs spot-check: **ADOPT the INDEPENDENT suite; CLOSE the substitution path; AMEND (B4).**

- Adopt the independent suite: a pre-registered FEN list with a hash, N ≥ 200, committed in the same pre-fit commit as the split map. E-0013 is right that "a cherry-picked suite is a rort at small N" and right to name a floor of 200.
- **Close the "OR the suite is replaced by a same-N independent spot check" path.** As written it is exercisable at conjunct (f) — that is, *after* the holdout loss and the SPRT verdict are both visible — which is exactly the escape hatch the tripwire was supposed to forbid, and the tripwire does not forbid it because a first-time substitution is not a "change". Either the substitute suite is committed pre-fit with its own hash, metric and numeric tolerance, or the path does not exist.
- **"TOLERANCE" is currently a placeholder for a number and must stop being one.** "beyond the pre-registered tolerance (exact tolerance + metric pinned with the suite list before fitting)" is a promise that a number will exist, not a number. Until it is a number committed pre-fit, conjunct (f) is not evaluable and the conjunct is decorative.
- The suite gate's *role* — checking that a fit which improves a quiet-label loss has not destroyed tactics — is the right gate to have, and its independence requirement is the right instinct. I am not asking for a bigger suite; I am asking for the tolerance to be a number and the substitution to be pre-committed.

## Blocking findings — HO-0008 discipline: exact missing sentence, and pure-additions status

**Discharge plan, stated up front so the list is actually collectable.** All
seven land as **ONE dated addendum** at the end of E-0013 — the HO-0008 /
R-0014 pattern. **The original text is untouched**: where an addendum
supersedes an existing sentence it quotes that sentence verbatim and states the
supersession, rather than deleting it. Nothing in the list re-derives or
rewrites an existing threshold; three of the seven *withdraw or supersede* a
named existing sentence (B3's decidability clause, B4's SPSA alternative, B5's
"pinned at execution preflight"), which is a supersession, not a re-derivation.
Each item is one to three sentences. No engine work is needed to land any.

---

### B1 — Stage (b) is not executable as written, and "A != B by handshake hash dump" is unachievable with the cited tool

**Missing sentence 1 (the mechanism, and the prohibition it lifts):**

> "**Arm differentiation mechanism.** The validated `tools/e0012_sprt.py` accepts
> exactly one `--exe` and differentiates its two arms solely by an integer
> `setoption name EvalStage value K` (`tools/e0012_sprt.py:325-326`; a single
> `binary = sha256_file(Path(args.exe).resolve())` is recorded for both arms at
> line 301). `EvalCoeffs` is a compiled-in static (`src/eval.h`;
> `src/_write_eval.py:25`); the engine's UCI surface advertises and accepts only
> `Hash` and `EvalStage` (`src/main.cpp:103-114, 133-147`) and emits no parameter
> hash. Therefore a `fitted-params` arm and a `hand-tuned` arm CANNOT be
> differentiated under the unmodified harness, and `--stage-a 5 --stage-b 5`
> is exactly the W-0001 stage-6 self-collision this record forbids. Before
> stage (b) is authorized the owner MUST land, under its own pre-registration
> and its own critique: (i) a runtime parameter-artifact loader that loads the
> pinned `fitted_params_sha256` artifact; (ii) an engine-emitted `id name` line
> carrying the SHA-256 of the parameter table actually in force, so that the
> mandated handshake dump has something to dump; and (iii) the minimal
> `tools/e0012_sprt.py` change needed to accept two executables and to assert
> `hash_A != hash_B` before game 1. Until (i)-(iii) exist, stage (b) is
> **INCONCLUSIVE-BY-UNRUNNABLE** — not PASS, not FAIL, and no Tier-S verdict may
> be recorded. `--validation-known` MUST NOT be passed on any E-0013 run."

**Missing sentence 2 (the stage index, which is load-bearing for gate (c)):**

> "**Stage index S\*.** The stage-(a) offline metric and the hand-tuned floor are
> computed at EvalStage = S\*, the same S\* both stage-(b) arms run at; S\* is
> pinned in the pre-fit commit below. The training data was generated at
> `eval_stage_a == eval_stage_b == 6` (E-0011:309) and `tempo` is applied by
> `src/eval.cpp` only at `stage >= 6`; a fitted coefficient that EvalStage S\*
> does not read is declared **NOT SCORED at S\***, is excluded from the fitted
> set, and may not contribute to conjunct (c)."

**Why B1 and not a doc-nit:** as written, stage (b) either (a) runs the same
binary at the same stage in both arms — the exact self-collision E-0013
forbids, which voided a campaign once already in this project — or (b) requires
a `src/` change plus a harness change, both of which E-0013 currently forbids
("No search, movegen, TT, UCI, or time-control change is permitted between the
arms"; "`tools/e0012_sprt.py` UNMODIFIED … No edit permitted by any seat"). The
record therefore mandates a result it has also prohibited the means of obtaining.
This must be settled before any fitting spends budget: if B1 survives into
execution, the whole Tier-S half is unrunnable and the holdout half runs for
nothing.

**Pure-additions:** yes — two new clauses. Neither rewrites a threshold. B1's
sentence 1 explicitly *lifts* a prohibition ("no UCI change", "harness
UNMODIFIED") for a separately pre-registered change; that lift is itself part of
the finding and must be explicit rather than left to be discovered.

---

### B2 — Q-LABEL: the fit target's colour frame is ambiguous, and the label's attainable gain is unmeasured

**Missing sentence 1 (the colour frame — the sharp edge):**

> "**Fit target (side-to-move frame).** For a position whose side to move is s,
> the fit target is `y = white_score` if `s == WHITE` and `y = 1 − white_score`
> if `s == BLACK`, where `white_score ∈ {1, 0.5, 0}` is `res` mapped from
> White's perspective. Because the eval is required to be colour-symmetric
> (mirror `s ^ 56`; conjunct (d) 0 full-mirror violations), a target expressed
> in the White frame for a Black-to-move position, or any mixture of the two
> frames across the dataset, is a **FAIL of conjunct (c)**. The extractor
> reports `label_frame_uniform = true` and its per-side-position counts before
> any fitting job reads the data."

**Missing sentence 2 (the label ceiling — the train-only feasibility pass):**

> "**Feasibility pass (non-training, pre-fit, train-only).** The label is
> constant within a game. Before conjunct (c)'s margin binds, a pre-registered,
> **TRAIN-ONLY** feasibility pass MUST measure, on a game-split inner partition
> carved from TRAIN and never touching the holdout: the attainable
> holdout-style loss improvement `delta_star` of the adopted optimizer over the
> hand-tuned floor under the adopted label construction, plus the per-game
> cluster SD `s_d`, each with its own pinned seed, iteration budget and
> regularization. `LOSS_MARGIN := max(0.002, 0.5 · delta_star)`. If `delta_star`
> cannot be measured because the optimizer does not beat the floor on the inner
> partition, the stage-(a) verdict is **INCONCLUSIVE-BY-DESIGN** and is labelled
> as such — never FAIL, and never 'no achievement = FAIL'."

**Pure-additions:** yes — two new clauses. Neither changes an existing
threshold; sentence 2 *computes* `LOSS_MARGIN` rather than replacing 0.002
outright, and its floor keeps 0.002 as the lower bound, so the margin can only
be made more conservative, never less.

---

### B3 — The 0.002 margin has no derivation, and the power justification offered for it is false

**Missing sentence 1 (effective N, and what the margin is actually conditional on):**

> "**Effective N.** The holdout's independent units are the holdout **GAMES**,
> not the holdout positions: the label is game-constant, so the estimator is the
> mean over G ≈ 200 games of the per-game mean paired loss difference, with
> `SE = s_d / sqrt(G)` on `t_{0.975, G−1}`. `LOSS_MARGIN = 0.002` is decidable at
> the planned N **iff `s_d ≤ 0.0101`** (`0.002 / (2.8016 / sqrt(200))`). `s_d` is
> a per-game SD of a paired difference and is not measured by this record. The
> clause 'for any realistic loss variance' is superseded by: 'decidable iff the
> B2 feasibility pass reports `s_d_inner ≤ 0.0101`; otherwise the margin is
> aspirational and the stage-(a) verdict is INCONCLUSIVE-BY-DESIGN, not FAIL'."

**Missing sentence 2 (the anti-apathetic clause, correctly scoped):**

> "**Anti-apathetic scope.** 'No achievement = FAIL' remains non-negotiable and is
> scoped to the fit's QUALITY, not to the measurement's POWER. A CI that
> includes 0 because `s_d` exceeds the feasibility bound is a power
> INCONCLUSIVE; a CI that includes 0 at a feasible `s_d` is a FAIL. Both
> verdicts publish the measured `s_d`, `delta_star` and the holdout game count in
> the open, so a null result can never be restated as 'baseline preserved', nor
> as an apathetic-fit rejection it was not."

**Pure-additions:** two clauses; sentence 1 supersedes one existing clause by
name ("for any realistic loss variance"), sentence 2 is a pure addition that
*narrows* the FAIL trigger rather than widening it. **Sentence 2 is the one that
must not be dropped:** without it, B3's first sentence would convert a power
failure into an apathetic-fit rejection while labelling it the latter — the
failure mode the whole anti-apathetic apparatus exists to prevent.

---

### B4 — Q-FIT and the suite tolerance are OPEN, the named SPSA alternative leaks, and no deferred value is anchored to the pre-fit commit

**Missing sentence 1 (Q-FIT adopted, SPSA withdrawn):**

> "**Q-FIT adopted.** Deterministic full-batch L-BFGS on the mean logistic loss
> of `sigmoid(clip(E_theta(p), −L, L))` against the B2 side-to-move-frame
> target, with an L2 penalty, a pinned seed, a pinned iteration budget, a pinned
> `L`, and a pinned L2 weight. No hyperparameter — including the L2 weight, the
> iteration budget and any early-stopping point — may be selected on, or
> compared against, ANY holdout quantity; hyperparameters are selected on the
> game-split inner partition of TRAIN only. The clause 'Alternative: SPSA on
> holdout loss' is **withdrawn as a leakage channel**; SPSA is not an available
> option under this contract."

**Missing sentence 2 (the single pre-fit commit — this closes F1-F6 and F10 at once):**

> "**Single pre-fit commit (the freeze anchor).** Every value this record defers
> with 'pinned at execution' / 'pinned at execution preflight' / 'pinned with
> the suite' — the fresh SPRT salt, the salt-distance citation, the KING-PST
> scope choice, the MAE phase-tertile boundaries, the label-mapping code, the
> optimizer seed / L2 weight / iteration budget / clipping, the stage index S\*,
> and the tactical-suite identity, N, metric and **TOLERANCE (a number, not a
> placeholder)** — is assigned ONCE and committed with its SHA-256 in the SAME
> pre-fit commit as the game-split map, and the holdout is not read before that
> commit exists. A value assigned for the first time after the holdout has been
> read is a tripwire FAIL exactly like a changed value; the existing clause 'Any
> threshold, salt, cap, suite, or margin changed after seeing data = FAIL' is
> extended by 'or assigned for the first time after the holdout is read'."

**Missing sentence 3 (Q-SUITE substitution closed; the critic's cap answer):**

> "**Q-SUITE.** The 'OR the suite is replaced by a same-N independent spot check'
> path is closed: a substituted suite must have its identity, N, metric and
> TOLERANCE committed in the same pre-fit commit as the original suite, and a
> substitution first made after the holdout or the SPRT is read is a tripwire
> FAIL. A suite list whose tolerance is still a placeholder is not a committed
> suite and conjunct (f) is not yet evaluable. **Per-game position cap: ruled
> NONE by HO-0013 / R-0019, 2026-09-26.** cap = all quiet positions after the
> exclusions and the dedup. A cap would shrink the holdout, reduce power and add
> a discretionary filter, while the BY-GAME split plus the normalized-FEN
> overlap-0 gate already carry the entire leakage obligation. This answer closes
> the clause 'If the critic requires a cap' and may not be re-opened."

**Pure-additions:** yes — three new clauses. Sentence 1 supersedes one existing
clause by name (the SPSA alternative); sentences 2 and 3 are pure additions that
*restrict* the space of available choices.

---

### B5 — Q-SCOPE: the KING-PST choice is deferred, and the consequence ladder's fallback is cited to an attribution that contradicts it

**Missing sentence 1 (KING PSTs frozen, here, not at preflight):**

> "**Q-SCOPE adopted: all-terms, KING PSTs FROZEN.** The KING PSTs are frozen at
> their hand-tuned values and are NOT fitted; the symmetry-constrained-fit
> option is rejected. The fitted set is therefore the five non-king
> `mg_pst[5][64]` / `eg_pst[5][64]` tables plus items 1 and 3-6 of the
> free-parameter list. The clause 'final choice pinned at execution preflight'
> is superseded by this pre-registration and may not be re-opened after the
> holdout is read."

**Missing sentence 2 (the ladder's citation, corrected):**

> "**Consequence-ladder citation corrected (binding only if the ladder arms).**
> E-0011 N1's fallback scope, 'the mobility/tempo sub-set E-0010's ladder
> motivates', is a mis-citation: E-0010 (line 344) measures the marginal
> contributions as mobility −3.7 Elo and tempo −11.5 Elo, 'non-positive with CIs
> crossing zero'. The two terms the ladder names as the fallback scope are the
> two the ladder attributes the worst contributions to. If the realized usable
> yield ever falls below 30,000, the fallback scope is **not** the
> mobility/tempo subset on this citation; it MUST be re-derived and re-registered
> under its own critique before it is applied."

**Rationale for freezing (recorded so the owner does not re-litigate it):** 240
extra free parameters on ~1,000 games of stage-6 self-play is the least
identifiable block in the set, and E-0010 attributes the positional block's
+26.8 Elo to a single rung at N=200 whose CI half-width is 51.4 Elo. Freezing is
the lower-variance choice and the one that keeps the fitted-parameter count
defensible against E-0011 N1's "≥500 positions/parameter" standard.

**Pure-additions:** yes — two new clauses. Sentence 1 supersedes one existing
clause by name; sentence 2 corrects a citation **in E-0013's inherited text,
not in E-0011 itself**, and is explicitly non-binding while the ladder is
disarmed.

---

### B6 — The yield: the "measured" label is applied to a number measured for a different filter

**Missing sentence (the count pass, and the train-only scope count):**

> "**Realized yield governs, measured by a count-only pre-fit pass.** The
> terminal diagnostic `quiet_proxy_opening_skipped = 76593` is a **per-ply count
> over the `san` segment for the bare quiet predicate**
> (`tools/e0011_check.py:385-398`); it applies no crash exclusion, no
> degenerate-mate exclusion, no dedup and no split, and it is therefore not the
> realized usable yield under this record's own filter. Conjunct (a) is
> evaluated on the realized count reported by a **count-only, non-training**
> extraction pass — the QUIET predicate plus the crash exclusion plus the
> degenerate exclusion plus the dedup plus the committed split map — run and
> hash-committed **before any fitter is invoked**. That realized count, and
> neither 76593 nor the session brief's ~27k, is the number that arms or disarms
> the 30k ladder. The scope branch is additionally evaluated on the **TRAIN-side
> count alone**, so that no whole-dataset quantity decides the fit's scope."

**Why this is a rule fix and not a measurement request:** the addendum only has
to make the *rule* correct. The count itself is the execution session's pre-fit
obligation, and I have bounded it rather than computed it: with cross-game FEN
duplication measured at 1705/130930 = 1.302 % and the one degenerate game
removing at most 6 positions, the honest band is
`75,600 ≤ realized usable yield ≤ 76,587` — 2.5× the floor, so the ladder is not
expected to arm. **I did not run the count and I must not**: it is an extraction
over the dataset, which this seat is forbidden to perform.

**Pure-additions:** yes — one new clause, with the "measured, not assumed"
wording corrected by supersession of that phrase only.

---

### B7 — Q-0006's official readiness gate 7 is missing from E-0013

**Missing sentence:**

> "**Independent verification of the fitted artifact (Q-0006 official readiness
> gate 7).** On a terminal PASS or a terminal FAIL this record files a handoff
> to verification-auditor (never the owner seat) carrying `fitted_params_sha256`,
> the pre-fit commit hash, the split-map hash, the feasibility-pass numbers, and
> the full command / exit-code ledger. The fitted artifact is not adopted,
> promoted, or cited as a strength input before that verification returns
> VERIFIED. No adoption or strength claim precedes it."

**Why:** Q-0006:68-69 is the governing gate list for the first training
experiment and reads "The fit produces and pins `fitted_params_sha256`, loads
exactly that artifact into the candidate, and **receives independent
verification**. No adoption or strength claim precedes it." E-0013's Follow-Up
contains no verification handoff. This is the cheapest of the seven (one
sentence, in a section that is otherwise a list of future actions) and its
absence would let the experiment that answers Q-0006 close without the gate
Q-0006 itself imposes.

**Pure-additions:** yes — one new Follow-Up bullet.

---

## Non-blocking findings (doc-nits and required-but-non-blocking text) — surfaced separately

- **DN1.** E-0013's Baseline writes "E-0010 per-term ladder vs stage-0 (**N=240**)".
  The ladder rungs k1–k5 are N=200 each; only k6 is N=240 (E-0010:341-342).
  Correct the attribution.
- **DN2.** E-0011 N1 cites quiet yield **76,887** (E-0011:345, R-0011's scaled
  EV-0001 measurement) while the verified 1,000-game dataset's terminal checker
  reports **76,593** — a 294-position discrepancy between two different
  measurements. E-0013 correctly cites the terminal figure; note the difference
  so the two are not conflated in future records.
- **DN3.** "distance citations computed at execution" — already computable and
  adequate: `|20260926 − 20260924| × 1,000,003 = 2,000,006 ≥ 1,000,003 > 1,999`
  (the SPRT game-index span). State it in the record instead of deferring it.
- **DN4.** "the E-0012 live pair ran 365 games in one evening session" is used as
  throughput corroboration for 769 games/h. An evening is 8-12 h, so 365
  games/evening is a *lower* bound on the rate, not corroboration. Keep the
  E-0010-measured 769/h and either drop the evening figure or relabel it as a
  lower bound.
- **DN5.** "dedup exact-FEN within the extraction before the split counts are
  reported" is ambiguous between global-dedup-before-split and
  per-split-dedup-then-assert; the realized counts and the meaning of the
  overlap-0 gate both depend on it. Pin: "dedup is global, before the split; the
  surviving copy's `game_id` determines the split; the overlap-0 gate then
  verifies that invariant." No leakage either way — the gate carries the
  obligation — but the counts must be reproducible.
- **DN6.** DEC-0010:186-187 still prints "Pending: independent verification per
  DEC-0009 gate 3". It was discharged by R-0010 on 2026-09-22 (W-0002
  Verification block). Not E-0013's file and not mine to edit; flagged for the
  DEC-0010 owner.
- **DN7.** E-0013 does not cite **Q-0006**, whose "Official first-training
  readiness gates" (items 1-7) is the governing gate list for this very
  experiment. Cite it — this is what surfaces B7.
- **DN8.** E-0013 should state that `--validation-known` MUST NOT be passed:
  `tools/e0012_sprt.py:299` raises unless
  `(tier, stage_a, stage_b, cap) == ("S", 6, 0, 8000)`.
- **DN9 — worth attention, not a nit about wording.** With the cap tightened to
  2,000 and DEC-0010's Tier-S `ASN(H0) ≈ 2,025`, a *genuine regression* ends
  INCONCLUSIVE roughly half the time, not FAIL. E-0013's conjunct (e) text is
  self-consistent about this, but the Follow-Up routes only FAIL to
  `research/failures/`. Recommend one sentence: "an INCONCLUSIVE on conjunct (e)
  is routed to a named re-decision with the measured stopping time and LLR
  published, not to silence" — otherwise a real regression can end the
  experiment with no routing consequence at all.
- **DN10.** E-0013's colour-flipped-relative leakage channel is closed only
  *implicitly*, by conjunct (d)'s colour-symmetry requirement. Recommend one
  sentence making the dependency explicit: "the normalized-FEN overlap-0 gate
  does not catch colour-flipped relatives; this is sound only while conjunct (d)
  enforces eval colour-symmetry, and relaxing (d) opens a live leakage channel."

---

## Verdict

**NOT CLEAN — BLOCKING. E-0013 stays `status: PENDING`.**

| Question | Verdict |
|---|---|
| Q1 free parameters pinned | **NOT CLEAN / BLOCKING** (B3, B4, B5) — but the free-parameter *section* is genuinely well built and I say so |
| Q2 holdout-split leakage | **NOT CLEAN / BLOCKING** (B4) — the split mechanism itself is CLEAN and strong |
| Q3 anti-apathetic floor | **NOT CLEAN / BLOCKING** (B3) — rhetoric frozen and correct; the power justification for it is false |
| Q4 SPRT scope inheritance | **NOT CLEAN / BLOCKING** (B1) — scope discipline CLEAN; the arm-differentiation mandate is unachievable with the cited tool |
| Q5 power honesty | **NOT CLEAN / BLOCKING** (B3, B4) — the yield flag is CLEAN and correct |
| Q6 sequencing | **CLEAN — no ordering constraint exists** |

Open questions: **P0/P1 → adopt P1** (P0 stays open, `blocked_by` E-0013's
terminal result, not its pre-registration). **Q-LABEL → adopt result-only,
amended** (B2). **Q-FIT → adopt deterministic L-BFGS, block SPSA, amended**
(B4). **Q-SCOPE → adopt all-terms with KING PSTs frozen, citation corrected**
(B5). **Q-SUITE → adopt the independent suite, substitution path closed** (B4).
Per-game position cap: **ruled NONE** (B4 sentence 3).

**Seven blocking findings, B1–B7, all dischargeable as one dated addendum with
the original text untouched.** I am not softening any of them, and I am not
manufacturing a CLEAN to unblock. The most serious is B1, and it is worth being
blunt about why: **as written, E-0013 mandates a Tier-S result it has also
prohibited the means of obtaining.** Either the two stage-(b) arms run the same
binary at the same EvalStage — the W-0001 self-collision this record names and
forbids, and the same class of defect that voided E-0010's gate-(c) campaign
once already — or stage (b) needs a `src/` parameter loader plus a
two-executable harness change, both currently forbidden. The record also demands
a handshake-hash dump of an "effective loaded hash" that the engine does not
emit and the harness does not record. That is not a wording problem.

The second most serious is B3, because it is the one that would let a null result
be mislabelled. The contract's anti-apathetic machinery is genuinely frozen in
three places and I could not find a rhetorical route from a null to "baseline
preserved". But the single sentence that makes a CI-includes-0 verdict a FAIL
rather than an INCONCLUSIVE rests on "the holdout N is large; power is not the
binding constraint here" — and the holdout's independent units are ~200 games,
not ~15,000 positions, and the 0.002 margin is decidable **iff the per-game
cluster SD is ≤ 0.0101**, which nobody has measured. My own arithmetic: at
`s_d = 0.02` the power is ≈ 0.33; at `s_d = 0.05` it is ≈ 0.10. Worse, a
game-constant label may put the *attainable* gain below 0.002, in which case
conjunct (c) is a guaranteed FAIL — unpassable by any fit — while the record
claims stage (a) is decidable. I am not asking the owner to weaken the margin.
I am asking for the quantity that decides it to be measured on the training
side, before the holdout is opened, and for the FAIL/INCONCLUSIVE split to
follow the measurement. That preserves the anti-apathetic clause where it
belongs — on the fit's quality — and refuses to let a power failure be filed as
an apathetic-fit rejection it was not.

**What I want on the record in E-0013's favour, because the owner built a good
contract and the record should say so where it is true:** the free-parameter
section is complete against `src/eval.h` member-for-member; the taper and phase
formula are frozen with a source citation; the normalized-FEN normalization is
specified in the way that actually closes the clock-and-fullmove-number channel;
the split-map commit is a real blocking pre-condition stated three times; the
leakage contract's three W-0001 clauses are all honoured; the paired CI is
clustered on the right unit; the strength gate inherits E-0012's scope ruling as
a first-class conjunct rather than a promise; the cap was tightened rather than
loosened; the p-hacking tripwire exists; the yield flag is correct and the
rejection of the brief's underived ±0.10 band is right; and the 30k ladder's
fallback scope is conditioned on a *measured* yield rather than an ambition. The
findings above are about what is not yet closed, not about work done badly.

**E-0013 may not leave PENDING until B1–B7 are discharged as a dated addendum
and re-critiqued.** The owner flips PENDING → RUNNING only after that. I have
not flipped it, and nothing has been fitted.

**Next action for the successor:** a fix-and-re-critique cycle on E-0013 alone.
All seven items are one addendum; no engine work, no extraction, no fitting and
no SPRT game generation is needed to land any of them. Nothing else in the
project is blocked by this ruling, and no sequencing constraint was found.

## Date
2026-09-26

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns.

---

## Evidence appendix (my own commands, this session; raw captures on disk)

This is a `kind: critique` review, not a verification, so the DEC-0009 gate-3
verification block does not apply. The commands below are the evidence for the
ruling, not a verification of E-0013's results (there are no results — nothing
has been fitted).

- `git pull --ff-only` → up to date; `git rev-parse HEAD origin/master` → both
  `d9efffdb6c74fe020092ba4e6dfa5dec88da13f9`; `git status -sb` → clean tree at
  the time of review (only this review and the HO-0013 status flip are mine).
- `python research/scripts/research.py next` → the three next actions: W-0003
  (Round-2 AGREEMENT_MATRIX backfill), HO-0005 (W-0003 verification), and
  E-00004 (GPU batch-inference latency). HO-0013 was not yet reflected; see the
  close-out note below.
- `python research/scripts/research.py status --brief` → 14 hypotheses, 6 open;
  4 experiments pending, 0 running, 6 wins, 1 loss, 2 failures; 2 open work
  items; 2 open handoffs; 0 live runs; 23 sessions recorded.
- `python research/scripts/research.py new-review --help` and
  `Get-ChildItem research\reviews` → highest existing review is R-0018, so the
  CLI's authoritative next id was confirmed to be **R-0019** before filing. I did
  not assume it.
- `python research/scripts/research.py validate` → exit 0, recorded in
  `s24_validate.txt`.
- Read-only source inspection (no build, no engine, no run): `src/eval.h`,
  `src/eval.cpp`, `src/main.cpp`, `tools/e0011_check.py`, `tools/e0012_sprt.py`,
  `tools/e0011_generate.py`, `write_eval_p5.py`, `CMakeLists.txt`.
  `tools/e0012_sprt.py` was **cited unmodified and not edited**; I did not run
  its `--self-test` or any live/replay mode, because a replay is SPRT game
  processing and outside this seat's remit.
- **Not run, deliberately:** any extraction, count pass, relabeling, fitting, or
  SPRT game generation; no Gate-0 build; no `research.py round`; no
  `HO-0005`/`W-0003` audit; no H-#### status change; E-0013 not flipped to
  RUNNING.

**Environment caveat, stated rather than hidden.** This session's shell capture
is degraded: `run_commands` reported `Command exited with code 1` on commands
that plainly succeeded (including `git log` and `Out-File` writes that completed
and whose file contents are correct), and PowerShell's default `>` redirect
produced UTF-16 that had to be re-emitted with `Out-File -Encoding utf8`. Every
gate result in the close-out is therefore taken from the **contents of a
redirected output file**, not from the reported exit status. Where a file's
content and the reported status disagree, I treat the file as authoritative and
say so.

**Close-out note for the next session.** `research.py next` listed E-00004 (GPU
batch-inference latency, priority high) ahead of HO-0013. That listing predates
this session's review; the correct next action for E-0013 specifically is the
fix-and-re-critique cycle named in the Verdict, and the owner should re-run
`research.py next` after this review lands.



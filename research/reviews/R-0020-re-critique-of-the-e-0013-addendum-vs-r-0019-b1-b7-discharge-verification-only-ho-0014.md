---
id: R-0020
type: review
reviewer: adversarial-reviewer
target: E-0013
kind: critique
status: COMPLETED
work_item: null
related: [HO-0014, HO-0013, E-0013, E-00014, E-00015, R-0019, HO-0015, HO-0016, H-0013, Q-0006, E-0010, E-0011, W-0001, R-0017, DEC-0010, tools/e0011_check.py, tools/e0012_sprt.py, src/eval.h, src/eval.cpp, src/main.cpp, src/_write_eval.py, write_eval_p5.py, S-0026]
example: false
created: 2026-09-26
---

# R-0020 - Re-critique of the E-0013 addendum against R-0019's B1-B7 (discharge verification only)

## Scope

Fresh adversarial-reviewer occupant, receiving **HO-0014**. Scope is **discharge
verification only**, exactly as HO-0014 specifies. I did not re-open any ruling I made
in R-0019: P1-adopted / P0-deferred, Q-LABEL result-only, Q-FIT deterministic full-batch
L-BFGS with SPSA withdrawn, Q-SCOPE all-terms with KING PSTs frozen, Q-SUITE independent
suite with the substitution path closed, and the per-game cap ruled NONE are **SETTLED**.
If I thought one of them was the wrong call, that belongs in a NEW record, not here.

I did not rule on whether SHRINK was the better engineering call, and I did not rule on
the pinned `SUITE_TOLERANCE = 0.02`; HO-0014 names both as out of scope and I agree.

I edited no record. I did not edit E-0013, E-00014, E-00015, HO-0014, R-0019, any CLOSED
or VERIFIED record, `tools/e0012_sprt.py`, or any engine source. I did not flip E-0013 to
RUNNING, did not open or close HO-0005/W-0003, and did not change any H-#### status. I ran
no training, no fitting, no extraction, no counting, no feasibility pass and no SPRT game
generation, and I read no holdout. Read-only inspection and arithmetic only.

### The work order's own integrity: CLEAN

I checked HO-0014 for a cut sentence, for text below its `## Response` / `## Verification`
template, and for an acceptance criterion its body does not ask for. I rule it **CLEAN** on
all three counts:

- **No cut sentence.** All 172 lines read continuously; the `## Response` and
  `## Verification` sections are the template's own placeholders, untouched, which is their
  correct state for a `status: REQUESTED` handoff. The prior session's repair (S-0026,
  commit `8759ed3`) did its job.
- **Nothing below the template.** The last line of the file is `- verdict: ...`, the
  template's own final placeholder.
- **No unrequested acceptance criterion.** The seven body criteria are a strict
  *elaboration* of the front-matter `acceptance` string, not an addition to it. The
  front-matter field is the narrower of the two; the body asks for more (it adds the
  BUCKET-2 conversion ruling, DN1-DN10, and the exact-missing-sentence requirement). That
  direction is harmless, so I do not rule on it as a defect; I note it only so the next
  author knows the two fields are not in one-to-one correspondence.

A NOT-CLEAN on the work order's own integrity was an available outcome. It was not the
right one here, so I proceeded to the subject of the review.

## Verdict (stated first, because everything below is evidence for it)

**NOT CLEAN - E-0013 stays `status: PENDING`.**

The shape of this verdict matters and is not the shape the disposition table at E-0013:785
predicts. **All three integrity properties HOLD.** The addendum is append-only, the
BUCKET-3 decision removes rather than re-points the unexecutable mandate, and nothing was
measured, fitted, counted or run. The BUCKET-2 delegation is **HONEST**. And the
addendum's **substance largely discharges R-0019**: B1, B2, B6 and B7 are discharged, F1-F12
are all twelve closed, DN1-DN10 has no silent drop, and the arithmetic I was handed
reproduces.

What blocks is two things the disposition table does not mention, because the disposition
table describes an addendum that is not the addendum on disk:

- **X1 (BLOCKING, mechanical).** The addendum is a **truncated and interleaved document**.
  Ten sentences are severed at block boundaries; in nine cases the continuation has been
  relocated hundreds of lines later, into unrelated sections and in several cases inside
  *other findings'* quoted blocks; in one case the continuation is **absent from the file
  entirely**. The file also ends mid-bullet at L1073. The operative clauses that suffer this
  are not all cosmetic - they include B4 sentence 2, the freeze anchor on which the entire
  F1-F12 closure rests, and the X-1/X-2/X-3 contingency table that must be applied *after*
  the feasibility measurement arrives.
- **X2 (BLOCKING, factual).** B5's stated rationale for freezing the KING PSTs - that this
  "keeps the fitted-parameter count defensible against E-0011 N1's '>= 500
  positions/parameter' standard" - is **arithmetically false**. The fitted set is 683 free
  scalars against at most 76,587 positions, i.e. about 112 positions/parameter, roughly
  **4.46x short** of 500. Freezing the KING PSTs moves the figure from about 94 to about
  112; it does not approach 500. A rationale that is false cannot be certified as discharged
  text, whatever decision it supports.

Neither finding requires re-deciding anything. Both are text repairs, and I give the exact
repair for each under "What must change" below.

## The three integrity properties, ruled separately and explicitly

### (i) The pre-addendum E-0013 text is unaltered - **HOLDS**

I computed this myself rather than accepting the number I was handed. The command
HO-0014 specifies (`git diff --numstat HEAD -- <E-0013>`) returns **nothing at all**,
because the working tree is clean and the addendum is already committed. Diffing against
the correct baseline instead:

```
git --no-pager diff --numstat 4478c3a HEAD -- research/experiments/E-0013-*.md
648     0     research/experiments/E-0013-h-0013-texel-fit-...md

git --no-pager diff --shortstat 4478c3a HEAD -- research/experiments/E-0013-*.md
 1 file changed, 648 insertions(+)
```

**648 additions, ZERO deletions**, as git itself computes it. A modification would
register as one deletion plus one addition, so zero deletions is the append-only proof
and it is not an inference of mine. `4478c3a` is the pre-addendum commit (R-0019 landed at
`4478c3a`; the addendum at `ce845c5`), and `git log -- <E-0013>` shows exactly two commits
touch the file - `d9efffd` (original) and `ce845c5` (addendum); the two later commits
`930d837` and `8759ed3` did not touch it. File length 425 -> 1,073 lines, and line 429 is
the `## Addendum:` heading. The pre-addendum text stands unaltered and the addendum's own
claim of pure addition is true.

One caveat, recorded and **not** a defect: the addendum supersedes original sentences **by
quotation and by name** rather than by editing them, which is the correct append-only
discipline and is what HO-0014 asked for. Superseded sentences therefore still physically
stand in the record (S-1 at E-0013:342-343 is the important one). I rule on that in (ii).

### (ii) The BUCKET-3 SHRINK decision REMOVED the unexecutable mandate rather than re-pointing it - **HOLDS**

R-0019's B1 held that the record mandated a Tier-S result it had also prohibited the means
of obtaining. The addendum takes the SHRINK branch. My check is narrow and mechanical, per
HO-0014, and I confine it to two questions.

**Question 1 - is the old sentence still standing unsuperseded beside a different
decision?** No. S-1 ("the execution records MUST dump the effective loaded hash from both
engines' handshake/startup log and assert A != B. Same-hash arms = FAIL",
E-0013:342-343) is quoted verbatim at L473-L474 under the label **(S-1, Sample Validity)**,
and it is superseded **by name** in the first line of the mechanism that replaces it, at
L517-L519:

> "**Arm differentiation mechanism for this record (supersedes S-1).** This record runs NO
> two-arm game campaign, so no UCI handshake hash is required, claimed or dumped, and S-1 is
> superseded rather than re-aimed at an instrument that does not exist."

That is an explicit removal, not a re-aiming. The mandate is not re-pointed at a UCI
`id name` surface, at a runtime parameter loader, or at a two-`--exe` harness - all three of
which R-0019's B1 sentence 1 named, and all three of which the addendum declines for this
run. The `--validation-known` prohibition is carried at L532-L535 with the right citation.

**Question 2 - is whatever replaced it ACHIEVABLE with the surface that actually exists?**
Yes, and I verified the surface instead of accepting the claim.


- The addendum's diagnosis is **correct against the code I read**: `tools/e0012_sprt.py:325-326`
  does construct both engines from the single `args.exe`, differentiating only by an integer
  `args.stage_a` / `args.stage_b`; line 301 does record one `binary =
  sha256_file(Path(args.exe).resolve())` for both arms; `parse_args` at lines 474-487
  exposes one `--exe` and integer `--stage-a/--stage-b`; `src/main.cpp:103-114` advertises
  and accepts only `Hash` and `EvalStage`; `src/main.cpp:133-147` parses and applies every
  `(key, value)` pair and emits **no echo and no parameter hash**. Every code citation in
  the addendum is exact, including the `tools/e0012_sprt.py:297-299` tuple
  `(tier, stage_a, stage_b, cap) == ("S", 6, 0, None)`, which I read and which raises
  exactly as quoted.
- `EvalCoeffs` is a compiled-in static with no runtime loader: `src/_write_eval.py:25` emits
  `static EvalCoeffs C;` and nothing in the UCI surface loads parameters.
- The replacement - two **parameter tables** differentiated by SHA-256 inside an offline
  evaluator, plus a candidate binary for the quality-conservation gates built by
  substituting a coefficient block into the eval translation unit and rebuilding - needs
  **no UCI change, no loader and no harness change**. I confirmed the mechanism exists: the
  coefficient block lives in `eval_init` at `src/eval.cpp:174-234` (the addendum's citation
  of that range is exact; `src/eval.cpp:209` sits inside it), and the `write_eval*.py`
  generator family is what produced rungs k1..k6.
- `S* = 6` is **achievable and correct**, and load-bearing as R-0019 said: `src/main.cpp:107`
  accepts `EvalStage` over `min 0 max 6`, and `src/eval.cpp:356` is
  `if(stage>=6) sc += (b.side == WHITE ? C.tempo : -C.tempo);`, so at S* = 6 the `tempo`
  entry is genuinely read and scored. The addendum's conclusion that `tempo` is therefore
  NOT "NOT SCORED at S*" is right.
- **One risk worth a sentence (non-blocking, filed as a nit).** The regeneration path is
  append-style, and `write_eval_p5.py:87` emits the **unsigned** `score += C.tempo;` while
  the live `src/eval.cpp:356` carries the E-0010 side-to-move-signed fix. Regeneration must
  substitute **coefficients only** and must not re-run a stage generator, or it silently
  regresses the exact colour-symmetry property that conjunct (d) gates on and that B2's
  side-to-move frame and DN10 both depend on. The addendum's wording ("a pinned coefficient
  block substituted into the eval translation unit") is the safe reading, so this is a
  clarification, not a defect.

The cost is written down rather than netted against the benefit: limb (b) of H-0013 is
recorded **UNANSWERED** (explicitly not NEUTRAL and not INCONCLUSIVE), the one-`--exe` wall
is recorded as **deferred, not dissolved**, the UCI parameter-hash surface is recorded as
considered-and-rejected with a stated reversal condition, and conjunct (e) is re-designated
**NOT EVALUATED IN THIS RUN** with the verdict vocabulary widened to PASS-FIT-QUALITY-ONLY
at L1031-L1042. That is the honest shape, and it is why I rule (ii) HOLDS.


### (iii) Nothing was measured, fitted, counted or run; no holdout read; no status flipped - **HOLDS**

- `git show --name-only ce845c5` touches **only** files under `research/`: E-0013, E-00014,
  E-00015, HO-0014, HO-0015, HO-0016, `research/index.md`, `research/state.json`,
  `research/state.md` and the S-0025 session record. **No `src/` file, no `tools/` file, no
  binary, no new artifact.** Nothing was built, fitted, extracted or run to produce it.
- No new measurement artifact exists: every file in `m0_audit/e0011/` still carries a
  2026-09-24 mtime (`check_output.txt` 2026-09-24 17:08, `games.jsonl` 2026-09-24 17:08).
  The only files modified on 2026-09-26 outside `research/` are the prior session's
  `build/s25_scratch/*.log` bookkeeping files. There is no extraction, no count and no
  feasibility pass on disk.
- `research.py experiments` -> E-0013 **PENDING**, E-00014 **PENDING**, E-00015 **PENDING**,
  every other experiment unchanged. E-0013 is not RUNNING.
- `research.py hypotheses` -> 17 hypotheses, H-0013 still **OPEN**; and
  `git diff 4478c3a HEAD -- research/hypotheses/` is **empty**, so no H-#### file was
  touched at all.
- No holdout was read by anyone, and the addendum forbids it in terms at L1014-L1016: "This
  record does not run E-00014, does not estimate `delta_star` or `s_d` by any means, and
  does not read the holdout to obtain either quantity."
- The addendum's factual claims that could only come from a measurement are all traceable to
  the **already-existing** E-0011 terminal diagnostic, which I read: `76593` per-ply
  quiet-proxy, `1705/130930` duplicates, `degenerate_mate_san_le_6=1`, and `end_counts` with
  `mate: 903` - the last being the "903 of 1,000 verified games end in `mate`" the addendum
  cites at L706. That is a pre-existing measurement, not a new one.


## X1 (BLOCKING) - the addendum is a truncated and interleaved document

This is the finding the disposition table at E-0013:785 does not contain, and it is why the
verdict is NOT CLEAN even though the substance largely holds.

The addendum occupies E-0013 L429-L1073. Within it, **ten sentences are severed at a block
boundary** - each ends mid-clause, is followed by a blank line and in six cases a `---`
rule, and its continuation appears far away. I located these mechanically (every non-empty
line in the addendum that ends a block without sentence-terminal punctuation, plus every
`---` in the addendum) and then confirmed every seam against numbered dumps, because the
cheap heuristic scan is not evidence and I do not offer it as such.

| # | Severed head (ends here) | Continuation actually resumes at | Consequence |
|---|---|---|---|
| 1 | L460 `...**B1 (as a branch` | L1064 ` DECISION, below), B2 sentence 1 + ...` | the BUCKET-1 list has no closing clause; the "how the findings are sorted" list is unusable as the audit key it claims to be |
| 2 | L488 `` ...self-collision this record`` | L1051 `names and forbids, and `--stage-a 6 --stage-b 5` compares...` | B1's diagnosis of the defect does not parse in place |
| 3 | L513 `...becomes mandatory and the loader` | L1044 ` plus the surface must be pre-registered and critiqued before any strength game.` | the reversal condition for the rejected UCI surface is incomplete where it is stated |
| 4 | L547 `` > ...`tempo` is NOT 'NOT SCORED at S\*' and remains`` | L1022 `> in the fitted set; conversely, a strength comparison against a stage-5 opponent...` | **the operative conclusion of B1 sentence 2 has no object** - the sentence ends on a dangling "remains" |
| 5 | L588 `` > ...`delta_star` of the adopted optimizer over the`` | L1011 `> hand-tuned floor under the adopted label construction, ...` | **B2 sentence 2b - the `LOSS_MARGIN := max(0.002, 0.5*delta_star)` rule - is severed** |
| 6 | L646 `> ...in the SAME pre-fit commit as the game-split map, and the holdout is` | L941 `> not read before that commit exists. A value assigned for the first time after the holdout...` | **B4 sentence 2, the single pre-fit commit - the freeze anchor the whole F1-F12 closure rests on - is severed at "and the holdout is"** |
| 7 | L664 `> ...a tolerance far above it would make` | L911 `> the conjunct decorative. 0.02 sits at roughly 0.6x the worst-case paired binomial SE, ...` | **B4 sentence 4's tolerance derivation is severed** |
| 8 | L707 `> ...2.5x headroom (E-00015 measures` | **NOWHERE IN THE FILE** | **text is missing outright**; the sentence at L871 beginning `> it; B6) - so the backwards fallback...` is a tail whose head is not adjacent to it |
| 9 | L730 `> ...would have silently ARMED the E-0011 N1` | L828 `> consequence ladder and auto-scoped the fit to the mobility/tempo subset - ...` | B6 sentence 3's refutation is severed |
| 10 | L754 `> ...**Relaxing (d) opens a live leakage` | L823 `> channel**, because the B2 side-to-move target frame plus an asymmetric eval...` | DN10's explicit-dependency sentence is severed |

Three further structural facts of the same severity class:

- **B3 sentence 3 announces a table that is not there.** L616-L619 reads "Three mutually
  exclusive outcomes of E-00014 are each assigned a named verdict NOW, by name, in this
  pre-registration, with no discretion left to the session that reads the number:" - followed
  by a blank line and `---` at L622. The X-1/X-2/X-3 contingency table is at **L958-L989**,
  ~340 lines later, after the F1-F12 table and under the B4 region. This is the rule that must
  be applied *after* `s_d_inner` is known - the one rule a future session most needs to find -
  and the record as written gives that session no path to it short of reading the whole file.
- **The obligations list is split across the disposition table.** F-U1, F-U2 and the body of
  F-U3 are at L760-L780; F-U3's `Owner: / Due:` line is stranded on its own at **L808**,
  after the table; F-U4, F-U5 and F-U6 are at L809-L821.
- **The file ends mid-bullet.** L1073, the last line, is
  `- **BUCKET 3 - BRANCH DECISION, stated with its cost:** B1. Decision: **SHRINK.**` - the
  BUCKET-3 bullet that the list at L460 promises, unfinished.

**Why this blocks rather than merely annoys.** Four severed seams (4, 5, 6, 7) and one
relocated block (the contingency table) sit on **normative, decision-critical text**: the
`S*` conclusion, the `LOSS_MARGIN` rule, the freeze anchor, the tolerance derivation, and the
branch table. A pre-registration is executable text, and executable text whose operative
clauses are detached from their sections is not reliably executable by the seat that will
read it after the measurements land. I am **not** claiming the content is absent - for eight
of the ten seams it is present elsewhere in the file, and for the tenth the substance is
independently restated in B6 sentence 2. I am claiming that the record does not say what the
disposition table says it says, and that the owner cannot certify a document in that state.

The disposition table's own framing invites this: "Nothing below is 'closed' by assertion"
(L787). Its rows are largely accurate about content. They are **silent about X1**, which means
the table certifies an addendum that is not the one on disk. That is the defect.


## X2 (BLOCKING) - B5's freezing rationale is arithmetically false

E-0013 L670-L672 (inside B5 sentence 1) states, as the recorded reason for the freeze:

> "Freezing is the lower-variance choice and the one that keeps the fitted-parameter count
> defensible against E-0011 N1's '>= 500 positions/parameter' standard."

I counted the fitted set from `src/eval.h` member by member against B5 sentence 1's own
enumeration ("the five non-king `mg_pst[5][64]` / `eg_pst[5][64]` tables plus items 1 and
3-6 of the free-parameter list"):

| block | count |
|---|---|
| `mg_value[6]` + `eg_value[6]`, KING entries fixed at 20000/20000 (item 1) | 10 |
| five non-king `mg_pst[5][64]` + `eg_pst[5][64]` | 640 |
| doubled/isolated pawn mg+eg, `passed_pawn_mg[8]`/`eg[8]` (item 3) | 20 |
| `mobility_mg/eg` (item 4) | 2 |
| bishop pair, open file, semi-open file, 7th rank, `king_shield_mg`, `king_center_eg` (item 5) | 10 |
| `tempo` (item 6) | 1 |
| **total free scalars, KING PSTs FROZEN** | **683** |

With the KING PSTs fitted as symmetry-preserving pairs the total is 683 + 128 = **811**.

Now the ratio, using the addendum's own honest band for the realized usable yield
(75,600 to 76,587) rather than a point estimate:

- 76,593 / 683 = **112.1** positions/parameter; 75,600 / 683 = **110.7**; on the TRAIN side
  (~0.8 x 75,600 = 60,480) it is **88.6**.
- To satisfy ">= 500 positions/parameter" at 683 parameters you need **341,500** positions.
  The honest band's ceiling is 76,587. The standard is short by a factor of **4.46**.
- Freezing the KING PSTs moves the figure from 76,593/811 = **94.4** to **112.1** - a ~19%
  improvement, not a move toward 500.

**So the claim as written is false.** The all-terms scope E-0013 adopted is at roughly
**112 positions/parameter**, and freezing does not bring it within E-0011 N1's 500
positions/parameter standard. Two honest observations about where the false claim came
from, neither of which changes the freeze decision:

1. E-0011 N1's own sentence (E-0011:129-L130) derives the standard from ">=50k positions
   against **O(10^2) parameters**" - i.e. it assumed roughly *one hundred* free parameters.
   E-0013's concrete all-terms list is 683, about 7x that assumption. The standard's premise
   is what fails, not the addendum's arithmetic.
2. E-0011 N1 explicitly declined to freeze the parameter count at all (E-0011:352-L353:
   "Parameter count stays an estimate (property of `src/`, not frozen until the fit is
   designed) - flagged same as yield"). E-0013 has now frozen the list, so the standard is
   testable - and it is not met.

**A related number in the same passage is also wrong.** The addendum says freezing avoids
"240 extra free parameters" (L670, and R-0019's F3 says the same). The KING PSTs are two
64-square tables, i.e. **128** free scalars, or **64** under the record's own symmetry
constraint `pst[s] == pst[mirror(s)]` under `s ^ 56`. 240 is not the KING-PST parameter
count under either reading. I flag this as a secondary factual error inherited from R-0019's
F3 rather than as a re-opening of the freeze ruling, which is SETTLED and which I am not
touching.

**Why this blocks.** The decision is fine and I do not touch it. But the addendum presents a
*false arithmetic claim* as a load-bearing part of its justification, in the one place a
future reader would look to check identifiability. A rationale that is false cannot be
certified as discharged text, and a record that says "the count is defensible" when it is
4.46x short is making a claim about power that no measurement in this project supports. I
rule this NOT DISCHARGED and give the exact replacement sentence below.


## B1-B7, ruled individually

| Finding | Ruling |
|---|---|
| B1 stage (b) unexecutable / handshake-hash unachievable | **DISCHARGED** (branch decision SHRINK) |
| B2 colour frame ambiguous + attainable gain unmeasured | **DISCHARGED** (text) / **honestly converted** (measurement) |
| B3 the 0.002 margin underived, power justification false | **PARTIALLY DISCHARGED** |
| B4 Q-FIT and suite tolerance OPEN, SPSA leaks, no anchor | **PARTIALLY DISCHARGED** |
| B5 KING-PST choice deferred, ladder fallback cites a contradicting attribution | **PARTIALLY DISCHARGED** |
| B6 "measured" label on a number measured for a different filter | **DISCHARGED** |
| B7 Q-0006 readiness gate 7 missing | **DISCHARGED** |

### B1 - **DISCHARGED** (as a branch decision; cost written)

R-0019's B1 asked for a mechanism, or for the owner to pre-register the loader/hash/harness
work before stage (b) was authorized. The addendum takes a third route - SHRINK - and HO-0014
tells me to check that this removes the mandate rather than re-points it, not to judge the
engineering. It removes it: no two-arm campaign runs, so no handshake hash is required,
claimed or dumped, and S-1 is superseded by name (L517-L519). The replacement is achievable
with the surface that exists (verified above). `S* = 6` is pinned and correct. Conjunct (e)
is re-designated NOT EVALUATED IN THIS RUN with PASS-FIT-QUALITY-ONLY as the ceiling verdict
(L1031-L1042). Cost items 1-3 write down the deferred limb, the deferred wall, and the
considered-and-rejected UCI surface, and the disposition table's B1 row is honest about all
three.

**Defect (X1, non-blocking for the ruling):** B1's narrative is severed in three places
(seams 2, 3 and 4), including the operative conclusion of sentence 2, which ends on a
dangling "and remains" at L547 with its object arriving at L1022. The *ruling* stands; the
prose does not parse in place. Repair seam 4 at minimum.

### B2 - **DISCHARGED** (text) / **honestly converted** (measurement)

- **Colour frame (F8):** discharged. The side-to-move frame is pinned verbatim at L557-L566
  with a FAIL consequence for the White-frame error, and `label_frame_uniform = true` plus
  per-side counts are required before any fitting job reads the data. This supersedes
  "exact mapping code pinned at execution" as to the *frame* while leaving the mapping code
  to the pre-fit commit, which is the right split.
- **Attainable gain:** honestly converted, not faked. L576-L580 records the label as
  game-constant, the fit as a game-outcome classifier, "the attainable gain ... is not
  measured by this record and no number for it is asserted anywhere in it", the 903/1,000
  mate dominance (which I verified against the terminal diagnostic), and the explicit
  prohibition on reading any correlation or MAE figure as a quality figure. The measurement
  is delegated to E-00014, which is pre-registered, PENDING, owned via HO-0015, and
  TRAIN-ONLY. The disposition table's B2 row says "measurement half PRE-REGISTERED as
  E-00014, NOT RUN" - that is the honest conversion HO-0014 requires.
- **The `LOSS_MARGIN := max(0.002, 0.5*delta_star)` rule:** severed at L588, resumes at
  L1011 (seam 5). The rule's content is complete and correct, and its floor means the margin
  can only get more conservative, never less. But the sentence that states it does not parse
  where a reader finds it. Repair seam 5.

### B3 - **PARTIALLY DISCHARGED**

- **Effective N and the decidability condition (s1):** discharged. G ~ 200 holdout *games*
  as the independent unit, `SE = s_d/sqrt(G)`, decidable iff `s_d <= 0.0101`. I re-derived
  the condition myself: `2.8016/sqrt(200) = 0.198103`, so `0.002/0.198103 = 0.010096`, which
  rounds to the quoted 0.0101. Correct.
- **Anti-apathetic rescoping (s2):** discharged. "No achievement = FAIL" is retained and
  scoped to the fit's QUALITY, not the measurement's POWER; a power failure is INCONCLUSIVE,
  a feasible-`s_d` null is FAIL; both verdicts publish `s_d`, `delta_star` and the holdout
  game count.
- **The false power clause (s4):** discharged. The Power-section sentence pair is quoted
  verbatim at L1000-L1009 and superseded, with the margin NOT lowered and the band NOT
  widened. Correct and honest.
- **The contingency decided NOW (s3): this is the gap.** The three branches X-1/X-2/X-3 are
  named, mutually exclusive, exhaustive, each with a fixed verdict and no discretion - the
  *content* is exactly what R-0019 asked for, and it is the right content. But it is
  **relocated ~340 lines away** from the sentence that announces it, under the B4 region,
  after the F1-F12 table. A reader who reaches L616-L619 is told three verdicts are assigned
  "with no discretion left to the session that reads the number", and is then given a `---`.
  The branch table exists; the record does not deliver it where it promises. That is a
  PARTIALLY DISCHARGED ruling: the rule is written but not executable as filed. Fix by moving
  the X-1/X-2/X-3 block to immediately follow L619.


### B4 - **PARTIALLY DISCHARGED**

- **Q-FIT adopted, SPSA withdrawn (s1):** discharged. Deterministic full-batch L-BFGS, pinned
  seed/budget/L/L2, hyperparameters selectable on the TRAIN inner partition only, SPSA
  withdrawn as a leakage channel. This faithfully implements my settled ruling.
- **Q-SUITE substitution closed; cap ruled NONE (s3):** discharged, complete and intact at
  L1005-L1015 (the substitution path closed with its own commit requirement; the per-game cap
  ruled NONE, closing the "if the critic requires a cap" clause). Faithful.
- **The single pre-fit commit (s2): SEVERED, and this is load-bearing.** This is the freeze
  anchor - the mechanism R-0019 itself prescribed to close F1-F12 - and it is cut at "and
  the holdout is" (L646), with the operative clause ("not read before that commit exists.
  A value assigned for the first time after the holdout has been read is a tripwire FAIL")
  resuming at L941, immediately after the F1-F12 table it anchors. The content is correct and
  complete; the sentence does not parse where the record introduces it, and the anchor for
  twelve closed items is the one thing that must be unbreakable. PARTIALLY DISCHARGED.
- **The suite tolerance as a NUMBER (s4): severed.** `SUITE_TOLERANCE = 0.02` is pinned with
  its metric (solution rate), its rule, and its binomial-SE derivation - the derivation is cut
  at L664 and resumes at L911. The number is the right kind of object (a number, not a
  placeholder, with N >= 200, protocol pinned, substitution closed). I am not ruling on
  whether 0.02 is the right value; HO-0014 forbids that and I agree. But the sentence
  carrying the derivation is severed. PARTIALLY DISCHARGED on presentation; content intact.

### B5 - **PARTIALLY DISCHARGED**

- **KING PSTs frozen here, not at preflight (s1):** the *decision* is discharged and faithful
  to my settled ruling, and it correctly supersedes "final choice pinned at execution
  preflight". But the recorded *rationale* contains the false parameter-count claim (X2) and
  the wrong 240 figure. A discharge resting partly on a false claim is not a full discharge.
  PARTIALLY DISCHARGED.
- **The ladder's citation corrected (s2):** discharged, and the arithmetic is right. I
  recomputed from E-0010's own published ladder (E-0010:341-344): `k4-k3 = 100.8 - 104.5 =
  -3.7` (mobility) and `k6-k5 = 116.1 - 127.6 = -11.5` (tempo), reproducing E-0010's printed
  attribution exactly, both "non-positive with CIs crossing zero". The two terms the fallback
  scope names are the two the ladder attributes the **worst** contributions to - so the
  citation is genuinely backwards, which is B5's point, and the correction states it correctly.
- **The dated correction note in place of an edit to E-0011 (s3):** discharged, and this is
  the right call on the append-only rule. E-0011 is COMPLETED and W-0001 is DONE/VERIFIED;
  the defect is recorded as a dated correction note in the inheriting record plus a
  named/owned/dated obligation F-U4, explicitly not as a retroactive edit. The disposition
  table's "Deliberately NOT discharged against E-0011/W-0001, and this is the point" is
  exactly the honest conversion HO-0014 asks for.
- B5's s3 note is **severed at L707** with its continuation **absent from the file**
  (seam 8) - the one place where text is not merely relocated but missing. See X1.


### B6 - **DISCHARGED**

- **The relabelling (s1):** discharged, and the central factual claim is **correct against
  the code**. I read `tools/e0011_check.py:371-398`: the `positions` Counter (371-383) is the
  distinct-FEN instrument reporting `duplicate_positions = total_positions - len(positions)`,
  while `quiet_proxy` (384-395) is incremented **per `san` ply** with the bare predicate and
  no crash exclusion, no degenerate-mate exclusion, no dedup and no split. So 76,593 is a
  per-ply count for a *different, weaker* filter than E-0013's own - exactly R-0019's B6
  point - and the "measured, not assumed" phrase is correctly superseded.
- **The honest band (s2):** discharged, and the arithmetic is right. Upper bound = 76,593
  minus at most 6 positions from the single degenerate game (`degenerate_mate_san_le_6=1`)
  and zero crash games (no `crash` in `end_counts`) = **76,587**. Lower bound = 76,593 minus
  ~997 projected cross-game FEN duplicates, from the measured `1705/130930 = 1.302%`
  duplication rate: `0.01302 x 76,593 = 997.2`, so ~**75,596**, recorded as the band
  **75,600-76,587**. I recomputed every one of these and they reproduce.
- **The ~27k refutation with its scope-changing consequence (s3):** discharged. The addendum
  correctly identifies that 27,000 sits *below* the 30,000 floor, so adopting it would have
  silently *armed* the mobility/tempo fallback - a scope change, not a conservative estimate.
  That is the dangerous direction and the record names it. Severed at L730, resumes L828.
- **The scope-floor rule (s4):** discharged and genuinely pre-registered, decided before the
  count exists, with the floor moved to the TRAIN-side count and both branch outcomes fixed.
- B6 is the finding whose content the addendum gets most right. Its defects are all X1
  placement/seam issues (seams 8, 9), not substance.

### B7 - **DISCHARGED**

Q-0006's official readiness gate 7 is quoted **verbatim** - I compared it against
`research/questions/Q-0006-self-play-data-pipeline.md:68-69` and the words match exactly -
and given teeth: a handoff to **verification-auditor** (never the owner, never the seat that
ran the fit) on any terminal PASS-FIT-QUALITY-ONLY / FAIL / named INCONCLUSIVE, carrying
`fitted_params_sha256`, the pre-fit commit hash, the split-map hash, the E-00014 and E-00015
numbers, and the full command/exit-code ledger, with no adoption or strength claim before
VERIFIED. Q-0006 is now cited by the record (which also discharges DN7), and the obligation
is named as F-U5 with an owner and a due date. This is the cheapest of the seven and the
addendum delivers it completely and in the right place (L851-L869). Intact; no seam.


## F1-F12, ruled item by item (twelve items)

Each is either closed with a **VALUE** or closed with an explicit **POINTER** to a pinned
input. That is the bar HO-0014 sets, and it is the bar R-0019 itself prescribed (the anchor,
not a fresh deferral). All twelve clear that bar. I add a "condition" column because three of
them rest on B4 sentence 2, which is severed (X1): those three are closed *in form* and
would be closed in substance the moment the anchor sentence is made contiguous.

| # | Closed as | Value / pointer | My ruling | Condition |
|---|---|---|---|---|
| F1 | VALUE | deterministic full-batch L-BFGS; SPSA withdrawn; not a choice at execution | **CLOSED** | - |
| F2 | POINTER | the four hyperparameter values are fields of the single pre-fit commit, choosable only on the TRAIN inner partition | **CLOSED (by pointer)** | pointer target is B4 s2, severed at L646 -> repair seam 6 |
| F3 | VALUE | KING PSTs **FROZEN** here, not at preflight | **CLOSED** | - |
| F4 | VALUE + POINTER | N >= 200, metric = solution rate, `SUITE_TOLERANCE = 0.02`, substitution closed; identity = pre-fit-commit FEN list + SHA-256 | **CLOSED** | tolerance derivation severed at L664 -> repair seam 7 |
| F5 | POINTER | tertile boundaries of the phase value, computed over **TRAIN positions only**, integer-rounded, frozen with SHA-256 in the pre-fit commit | **CLOSED (by pointer)** | the "TRAIN only" clause is exactly the right anti-leakage guard |
| F6 | VALUE | no fresh salt is used by this record at all (SHRINK); the admissibility rule is pinned: `abs(S-S')*1000003 > cap-1` | **CLOSED** | - |
| F7 | VALUE | `S* = 6`; floor = the compiled-in table of `src/eval.cpp:174-234` at the pinned `src/` commit | **CLOSED** | verified: `src/main.cpp:107` accepts EvalStage 0..6; `src/eval.cpp:356` scores tempo at stage>=6 |
| F8 | VALUE | the side-to-move frame | **CLOSED** | - |
| F9 | VALUE | dedup is **GLOBAL, before the split**; the surviving copy's `game_id` decides the split; the overlap-0 gate verifies the invariant | **CLOSED** | - |
| F10 | VALUE | `abs(20260926-20260924)*1000003 = 2,000,006 >= 1,000,003 > 1,999`; likewise vs 20260922 and 20260914 | **CLOSED** | I recomputed: 2, 4 and 12 x 1,000,003 = 2,000,006 / 4,000,012 / 12,000,036, all > 1,999 |
| F11 | POINTER | E-00014, plus the X-1/X-2/X-3 contingency decided in advance; the number stays 0.002 | **CLOSED (by pointer)** | the contingency table is relocated (X1) -> move it under L619 |
| F12 | VALUE | **NONE**; closed and not re-openable | **CLOSED** | matches my settled ruling; implements it faithfully |

Two points of substance I want on the record, because they are the parts of F1-F12 that are
easy to get wrong and were got right here:

- **F5's guard is the right one.** Deriving the MAE tertile boundaries from TRAIN positions
  only, and freezing the boundary list with its SHA-256, closes the channel by which a
  *metric definition* (not merely a threshold) could be chosen after seeing holdout phase
  values. R-0019 flagged F5 as a first-time-assignment risk; this closes it properly.
- **F9's ordering is the right one.** Global-dedup-before-split, with the surviving copy's
  `game_id` deciding the split and the overlap-0 gate verifying the invariant, is the only
  reading under which the realized counts are reproducible. This also discharges DN5.

**No F-item is left as a bare first-time assignment.** That was R-0019's central structural
complaint, and the addendum answers it with the correct instrument - a single hash-committed
pre-fit commit plus a tripwire extended to first-time assignment. I record that as a
discharged structural point, with the one caveat that the anchor sentence itself is severed.


## DN1-DN10 - no nit silently dropped

All ten have a disposition row in the DN table (L736-L747). **No silent drop.** I rule each
individually, and I confirm the disposition table's own arithmetic on the split
(5 discharged / 4 recorded-or-routed / 1 recorded-and-carried).

| # | Ruling | Note |
|---|---|---|
| DN1 | **RECORDED, not edited** | The Baseline "N=240" line is original text and correctly stays; the correction (k1-k5 are N=200, only k6 is N=240) is stated and made binding on any attribution sentence. Correct handling of append-only. |
| DN2 | **RECORDED as a band of provenance** | 76,887 (E-0011's scaled 1,240-game estimate) and 76,593 (the terminal checker on the verified 1,000-game dataset) are two different measurements, not a conflict to resolve. Recorded so they are not conflated. Right call. |
| DN3 | **DISCHARGED** | Computed in F10 rather than deferred: `2,000,006 >= 1,000,003 > 1,999`. I recomputed it. |
| DN4 | **RECORDED** | 769/h is the E-0010-**measured** rate and is the one used; the 365-games-per-evening figure is relabelled a lower bound and is not treated as corroboration. This is exactly the correction R-0019 asked for. |
| DN5 | **DISCHARGED** in F9 | Dedup pinned global-before-split with the surviving copy's `game_id` deciding the split, and the overlap-0 gate verifying the invariant. |
| DN6 | **RECORDED and ROUTED** | DEC-0010 is not the authorising seat's file and is not edited; flagged to the DEC-0010 owner as F-U6. Correct: a nit in another record is routed, not fixed by proxy. |
| DN7 | **DISCHARGED by B7** | Q-0006 is now cited, gate 7 quoted verbatim. |
| DN8 | **DISCHARGED** in B1 s1 | `--validation-known` MUST NOT be passed, with the `tools/e0012_sprt.py:297-299` citation and the exact tuple that raises. I read 297-299 and the tuple `("S", 6, 0, None)` is quoted correctly. |
| DN9 | **RECORDED and ROUTED** | An INCONCLUSIVE on any evaluated conjunct routes to a NAMED re-decision with the measured stopping time and LLR/estimate published. Because SHRINK means the strength conjunct is not evaluated in this run, the obligation is carried onto the deferred strength contract (F-U2) so it is not lost at the hand-off. This is the right handling of the one DN R-0019 said was "worth attention, not a nit". |
| DN10 | **DISCHARGED, but severed (X1 seam 10)** | The explicit-dependency sentence exists and its content is correct - the normalized-FEN overlap-0 gate does **not** catch colour-flipped relatives, the closure is sound only while conjunct (d) enforces eval colour-symmetry, and relaxing (d) opens a live leakage channel. But the sentence is cut at L754 and resumes at L823. Content present, prose broken. |

**Summary: 5 discharged (DN3, DN5, DN7, DN8, DN10), 4 recorded/routed (DN1, DN2, DN4,
DN6), 1 recorded and carried forward (DN9).** That matches the disposition table's split
exactly, and I found no nit that lost its disposition between R-0019 and this addendum.


## The BUCKET-2 delegation to E-00014 / E-00015: **HONEST**

HO-0014 asks three specific things. I take them in turn.

**1. Does the addendum claim their outputs? No.** I looked for a number attributed to either
pass and found none. The addendum says the opposite, in terms: "the `delta_star` / `s_d`
NUMBERS are not in this record and are not in any record yet"; "This record does not run
E-00014, does not estimate `delta_star` or `s_d` by any means"; "The count pass is E-00015;
this record does not run it." Both E-00014 and E-00015 are `status: PENDING`, `result: null`,
`completed: null`, and both are dispatched by open handoffs (HO-0015 -> systems-researcher,
HO-0016 -> systems-researcher, both `REQUESTED`) rather than claimed as done.
**Claimed: nothing.**

**2. Is the holdout kept unread in order to obtain them? Yes, and structurally so.** E-00014
is TRAIN-ONLY by construction - a game-split inner partition carved from TRAIN, never touching
the holdout - and HO-0015's acceptance criterion states "The holdout is never read" as a
condition of the handoff. The addendum forbids it in terms. Critically, the delegation does
not create an incentive to peek: the branch table that consumes the numbers is decided **in
advance** (X-1/X-2/X-3), so there is no discretion to exercise after the number lands, and
the freeze anchor (F2, F5, F11) requires the pre-fit commit to exist before the holdout is
read at all. The measurement sits on the training side, before the holdout opens, which is
precisely what R-0019's B3 asked for. **Holdout: unread.**

**3. Is delegation used to discharge a finding that only addendum text could discharge? No.**
This is the test that matters, so I checked it finding by finding:

- **B2** has two halves. The *text* half - the side-to-move colour frame and the explicit FAIL
  consequence - could only be discharged by text, and it **is** discharged by text
  (L557-L566). The *measurement* half - the attainable gain - is what B2 itself asked to be
  MEASURED, so delegating it to a pre-registered train-only pass is the finding's own
  instruction, not an evasion. Both halves are labelled as discharged vs delegated.
- **B3 / F11** asked for the quantity that decides the margin to be measured on the training
  side before the holdout opens. E-00014 *is* that measurement. Delegating it is discharge
  here, because the finding asked for a measurement.
- **B6** asked for the realized yield to be measured by a count-only pre-fit pass, and for
  the *rule* to be corrected. The rule is corrected in text (the relabelling, the band, the
  scope-floor rule); the count is delegated to E-00015, which is exactly a count-only pass.

In no case is a finding discharged by "someone will measure it later" where the finding
actually wanted text. Where the finding wanted a measurement, the delegation is the discharge.
**Ruling: HONEST.**

One caveat, non-blocking: E-00014 and E-00015 both carry `owner: null` in their front
matter. The executing seat is named only indirectly, via the handoffs. The obligations are
named, dated and routed, so the conversion is honest, but an experiment record with a null
owner that another seat is expected to execute is weaker than it needs to be. Setting
`owner:` on both records would close the loop.


## The arithmetic, redone by me rather than inherited

Every number HO-0014 listed, recomputed from first principles. All reproduce except the
parameter-count one, which is where X2 comes from.

| Quantity | Handed to me | My own computation | Agrees? |
|---|---|---|---|
| 76,593 as a count | per-ply, for a different filter | `tools/e0011_check.py:384-395` increments `quiet_proxy` once per `san` ply under the bare predicate; the distinct-FEN instrument is the separate `positions` Counter at 371-383. No crash/degenerate/dedup/split filter. | **YES** |
| duplication rate | 1705/130930 = 1.302 % | `1705/130930 = 0.01302222...` = **1.3022 %** | **YES** |
| projected duplicates | ~997 | `0.01302 x 76593 = 997.2` | **YES** |
| honest band upper | 76,587 | `76593 - 6 = 76587` (one degenerate game, `degenerate_mate_san_le_6=1`, at most 6 positions; zero crash games - no `crash` key in `end_counts`) | **YES** |
| honest band lower | ~75,600 | `76593 - 997 = 75596`, recorded as the rounded band lower edge **75,600** | **YES** |
| power condition | `s_d <= 0.0101` | `2.8016 / sqrt(200) = 0.198103`; `0.002 / 0.198103 = 0.0100964` -> **0.0101** | **YES** |
| salt distance | 2,000,006 > 1,999 | `abs(20260926-20260924) = 2`; `2 x 1,000,003 = 2,000,006`. Also vs 20260922: `4 x 1,000,003 = 4,000,012`; vs 20260914: `12 x 1,000,003 = 12,000,036`. All `>= 1,000,003 > 1,999`. | **YES** |
| E-0010 k4-k3 | -3.7 | `100.8 - 104.5 = -3.7` (mobility) | **YES** |
| E-0010 k6-k5 | -11.5 | `116.1 - 127.6 = -11.5` (tempo) | **YES** |
| other rungs (context) | - | `k3-k2 = 104.5-82.3 = +22.2` (pawn); `k5-k4 = 127.6-100.8 = +26.8` (positional). Both positive, both consistent with E-0010:343. | **YES** |
| fitted-parameter count vs ">= 500 positions/parameter" | claimed "defensible" | 683 free scalars / 76,587 positions = **112.1 per parameter**; needs 341,500 for 500/param; **4.46x short**. With KING PSTs fitted: 811 params = 94.4/param. | **NO - this is X2** |
| suite tolerance vs binomial SE | 0.02 sits at ~0.6x the noise floor | `0.5/sqrt(200) = 0.03536`; `0.02 / 0.0354 = 0.565` -> "roughly 0.6x" | **YES** |

Two of these deserve a sentence because they are the load-bearing ones for B5 and B6:

- **The backwards-citation claim is arithmetically sound, and that is what makes B5's
  correction real.** The two terms the E-0011 N1 fallback scope names (mobility, tempo) are
  precisely the two whose marginal contributions are the **worst** in the ladder (-3.7 and
  -11.5, both non-positive with CIs crossing zero). The fallback scope is therefore motivated
  by the ladder's *weakest* terms, not its strongest. R-0019 was right to call that a
  backwards citation, and the addendum reproduces the deltas exactly rather than asserting them.
- **The 76,593 figure really is a different filter, not merely a differently-labelled one.**
  This matters because the whole of B6 turns on it, and I checked the code rather than the
  prose: the count that E-0013 called "measured, not assumed" never applied E-0013's own
  crash exclusion, degenerate-mate exclusion, dedup, or split. Calling it "measured" was
  accurate about the diagnostic and misleading about the filter. The addendum's relabelling is
  correct.


## What must change - the exact missing text, so the next cycle is mechanical

Everything below is **text repair**. None of it re-opens a decision, and none of it requires
a judgement call from the next reviewer. Where I supply replacement wording, it is wording the
addendum already supports; where the addendum's own text exists but is detached, the
instruction is to **move that text, not to rewrite it**.

### X1 - mechanical: nine seams, one relocation, one termination

For each seam, join the severed head to its continuation as one contiguous sentence, in the
finding's own section, deleting nothing. In line terms:

1. L460 -> L1064 (the BUCKET-1 list; restore the full three-bucket list).
2. L488 -> L1051 (B1's self-collision diagnosis).
3. L513 -> L1044 (the UCI-surface reversal condition).
4. **L547 -> L1022** (B1 s2's `tempo` conclusion - the highest-priority seam, because the
   sentence currently has no object at all).
5. **L588 -> L1011** (B2 s2b, the `LOSS_MARGIN` rule).
6. **L646 -> L941** (B4 s2, the freeze anchor - the second-highest-priority seam, because
   twelve F-items are closed against it).
7. **L664 -> L911** (B4 s4, the `SUITE_TOLERANCE` derivation).
8. L707 -> the missing text (see X1-a below).
9. L730 -> L828 (B6 s3's refutation).
10. L754 -> L823 (DN10's explicit-dependency sentence).

- **Move the X-1/X-2/X-3 contingency table** (currently L958-L989) to sit immediately after
  L619, directly under B3 sentence 3's announcement. No wording change.
- **Re-join the follow-up obligations**: F-U1, F-U2, F-U3, F-U3's `Owner:/Due:` line (L808),
  F-U4, F-U5 and F-U6 into one contiguous list.
- **Terminate the file with a complete sentence.** L1073 currently ends mid-bullet.

**X1-a - the one seam that needs authorial text, because the continuation is genuinely
absent.** The addendum's surviving text either side of the gap is:

> head, L705-L707: "**Status of the ladder here:** the ladder is currently DISARMED - the
> honest band for the realized usable yield is 75,600 to 76,587 against a 30,000 floor, i.e.
> 2.5x headroom (E-00015 measures"

> tail, L871: "it; B6) - so the backwards fallback is a latent trap rather than an active
> error, and this addendum converts it from an auto-applying rule into a rule that CANNOT
> auto-apply: if the ladder arms, the scope is re-derived and re-registered under its own
> critique before it is used."

I am not going to guess the author's missing words, because this is a pre-registration and
inventing normative text on another seat's behalf is exactly the failure mode this system
exists to prevent. The **exact missing sentence** is the completion of that parenthetical and
the clause that leads into "it; B6)". The author should write it. To make the next cycle
mechanical rather than interpretive, the requirement on it is precise and checkable:

> The inserted text must (a) finish the sentence begun at L707 by naming who measures the
> realized count and stating that the DISARMED status holds *pending* that count, (b) state
> explicitly that the band is a band and not a measurement of this record's own filter, and
> (c) lead grammatically into the existing tail at L871, i.e. end with a parenthetical of the
> form "... (mobility/tempo scope; B6)" whose referent is the fallback scope.

A conforming sentence, offered as a template the author may adopt verbatim or rewrite in their
own words:

> "(E-00015 measures the realized count; until that count exists this band remains an
> arithmetic bound on already-measured quantities and is NOT a measurement of this record's
> own filter, and the ladder's DISARMED status is provisional on it. If the count nevertheless
> arms the ladder, the fallback scope it would apply is not the mobility/tempo sub-set named
> in E-0011 N1, and the sub-set is re-derived and re-registered under its own critique before
> any use (mobility/tempo scope; B6)"


### X2 - one sentence replaced

Delete the false clause and replace it with the arithmetic. The sentence at L670-L672 ends:

> "...Freezing is the lower-variance choice and the one that keeps the fitted-parameter count
> defensible against E-0011 N1's '>= 500 positions/parameter' standard."

**Replace that final clause with:**

> "Freezing is the lower-variance choice. It does NOT, however, bring the fitted-parameter
> count within E-0011 N1's '>= 500 positions/parameter' standard, and this record does not
> claim it does: with the KING PSTs frozen the fitted set is 683 free scalars (10 non-king
> mg_value/eg_value, 640 from the five non-king PST tables, 20 pawn-structure, 2 mobility,
> 10 positional/king, 1 tempo) against a realized usable yield of at most 76,587 positions,
> i.e. about 112 positions/parameter overall and about 89 on the TRAIN side - roughly 4.5x
> short of 500, and 4.5x short is a stated limitation of the all-terms scope adopted here, not
> a solved one. Freezing the KING PSTs (128 free scalars, or 64 under the record's own
> `pst[s] == pst[mirror(s)]` constraint - not 240) raises that ratio from about 94 to about
> 112; it does not reach the standard. E-0011 N1 derived the standard from an 'O(10^2)
> parameters' assumption and explicitly declined to freeze the parameter count
> (E-0011:352-353), so the standard's premise, not this record's arithmetic, is what the
> all-terms scope does not satisfy. The binding constraint on stage (a) therefore remains the
> label/systematic bias E-0011 N1 already named, together with the game-clustered dispersion
> `s_d` that E-00014 measures - not the parameter count. The freeze decision itself is
> unaffected and is not re-opened by this correction."

And the word "240" at L670 (inherited from R-0019's F3) should read **128** (or 64 under the
symmetry constraint).

### X3 - two front-matter fields

Set `owner:` on E-00014 and E-00015 to the seat that HO-0015 / HO-0016 dispatch to
(`systems-researcher`). One line per record; it closes the ownership loop on the BUCKET-2
delegation.

### Nits, non-blocking, one sentence each if the author wants them

- **N1 (coefficient-regeneration scope).** Add to B1 sentence 1: "The coefficient
  regeneration substitutes the coefficient block ONLY; it must not re-run a stage generator,
  because `write_eval_p5.py:87` emits the unsigned `score += C.tempo;` while the live
  `src/eval.cpp:356` carries the E-0010 side-to-move-signed fix, and regressing that line
  would break the colour-symmetry invariant that conjunct (d) gates on and that B2's
  side-to-move frame and DN10 both depend on."
- **N2 (F-U4 ownership).** F-U4 says "Owner: the E-0011 owner seat". E-0011's front matter
  names `owner: systems-researcher`, so the obligation is resolvable, but naming the seat
  literally would make it checkable.
- **N3 (disposition-table scope).** The disposition table is silent on X1 and X2. A re-issued
  addendum should carry rows for both, so the next reader is not told - as the current table
  tells them - that everything is closed.


## What E-0013's status should be next, and on what condition it may leave PENDING

**E-0013 stays `status: PENDING`.** It does not go to RUNNING, and I have not flipped it.

HO-0014's acceptance criterion sets the bar precisely: "E-0013 may leave PENDING only on a
ruling that every finding is DISCHARGED or honestly converted." That bar is **not met**, for
two reasons that are both about the record's text rather than about its decisions:

- **B3, B4 and B5 are PARTIALLY DISCHARGED, not DISCHARGED.** For B3 and B4 the cause is
  placement and severing of rules that are present but not executable as filed; for B5 it is
  partly a false arithmetic claim (X2). None of the three is a "quietly narrowed threshold" or
  a "measurement promised without an owner" - I checked for those specifically and did not find
  them - but "present but not executable" is not "discharged", and I will not call it so.
- **X1 leaves the addendum internally inconsistent with its own disposition table.** The table
  asserts that B1-B7 and F1-F12 are discharged; the document it describes has ten severed
  sentences, one missing sentence, a relocated branch table, a split obligations list and an
  unfinished final bullet. A disposition table that does not describe its own document cannot
  be the basis for leaving PENDING.

**The condition on which E-0013 may leave PENDING** - all four, and no judgement call in any
of them:

1. Every seam in the X1 list is joined, the X-1/X-2/X-3 table sits under B3 sentence 3, the
   follow-up obligations are contiguous, and the file ends with a complete sentence.
2. The X1-a sentence is supplied by the author, satisfying the three stated conditions.
3. The X2 clause is replaced with the arithmetic sentence above, and "240" becomes "128".
4. `owner:` is set on E-00014 and E-00015 (X3).

On completion of 1-4, the findings read: B1 DISCHARGED, B2 DISCHARGED (text) / honestly
converted (measurement), B3 DISCHARGED, B4 DISCHARGED, B5 DISCHARGED, B6 DISCHARGED, B7
DISCHARGED; F1-F12 all twelve CLOSED; DN1-DN10 with no silent drop; BUCKET-2 HONEST; all
three integrity properties HOLDING. **That is the condition for E-0013 to move PENDING ->
RUNNING**, and it requires a re-critique to confirm - I am not pre-authorising the flip, and
E-00014 / E-00015 may run at any time since they are separate PENDING records under their own
handoffs (they do not read the holdout and do not depend on E-0013 leaving PENDING).

Two things I want to be explicit about, because a NOT-CLEAN here costs the project a cycle
and I do not want that cycle spent on the wrong thing:

- **I am not asking the owner to re-decide anything.** SHRINK stands. The freeze stands.
  `SUITE_TOLERANCE = 0.02` stands. The cap stays NONE. The X-1/X-2/X-3 branches stand. Every
  settled ruling from R-0019 is implemented faithfully, and where I disagreed with the
  *engineering* I was explicitly out of scope and said so.
- **The substance of this addendum is good and I am saying so on the record.** The owner built
  a real freeze anchor, decided the power contingency before the number exists, kept the
  anti-apathetic clause where it belongs while refusing to let a power failure be filed as an
  apathetic-fit rejection, wrote the honesty clause about the unmeasurable attainable gain
  without hedging it, corrected a backwards citation by recomputing the deltas rather than
  asserting them, and declined to edit a COMPLETED and a VERIFIED record - filing a dated
  correction note plus an owned obligation instead. Those are the marks of someone discharging
  findings rather than burying them. The failures here are typographical and one arithmetic
  claim, and they are repairable in an afternoon.

## Residual risk, calibrated

- **That the addendum is severable at all** - demonstrated, not inferred. Ten seams, each
  confirmed against numbered dumps.
- **That the missing sentence at L707 is genuinely absent** - strongly supported. Nine other
  seams relocate their continuations; this one has no candidate tail anywhere in the file, and
  the sentence at L871 that would be its tail is not adjacent to it. I state it as absent from
  the file, which is what I verified; I cannot rule out that the author holds the text
  elsewhere.
- **That B3's branch table is the relocated X-1/X-2/X-3 block and not a different one** -
  demonstrated. The content matches the three branches B3 sentence 3 announces, and each branch
  carries a named verdict with no discretion.
- **That the parameter count is 683** - demonstrated. Counted member by member from
  `src/eval.h` against B5 sentence 1's own enumeration; the same count is implied by E-0013's
  free-parameter list items 1-6.
- **That no measurement was taken** - demonstrated. `git show --name-only ce845c5` touches only
  `research/*.md`; every `m0_audit/e0011/` artifact still carries a 2026-09-24 mtime.
- **Whether the offline evaluator B1 relies on will reproduce `src/eval.cpp` exactly** -
  **unknown**, and I flag it as a residual rather than a finding. B1's replacement differentiates
  two parameter tables by SHA-256 inside an offline evaluator; the pinned hand-tuned floor is
  the compiled-in table at `src/eval.cpp:174-234`. For stage (a) the fitted-vs-floor loss
  comparison is only meaningful if the offline evaluator's scoring is identical to the compiled
  scorer's. Nothing in the addendum pins that equivalence, and I am not going to invent a
  requirement for it - but the execution seat should confirm it, because a silent
  evaluator/scorer divergence would show up as a stage-(a) number with no engine behind it.
  Conjunct (d)'s 1000-position full-mirror gate and the NPS band on a regenerated binary are
  the natural places for that check to live.


## Date
2026-09-26

> A review never edits the original report - it lives here and is linked from the
> debate/report it concerns.

## Evidence appendix - my own commands this session

This is a `kind: critique` review, not a verification, so the DEC-0009 gate-3 verification
block does not apply. The commands below are the evidence for the ruling.

- `git pull --ff-only` -> up to date. `git rev-parse HEAD` and `git rev-parse origin/master`
  -> both `8759ed3140d85a4fa0db11a0f57b3ec7034447a5`. `git status -sb` ->
  `## master...origin/master`, clean tree at the start of the review.
- **The numstat, computed by git and not inherited:**
  `git --no-pager diff --numstat 4478c3a HEAD -- research/experiments/E-0013-*.md` ->
  `648  0  <file>`; `git --no-pager diff --shortstat 4478c3a HEAD -- <same>` ->
  `1 file changed, 648 insertions(+)`. Same result against `d9efffd`.
  `git log --oneline -- <file>` -> only `ce845c5` and `d9efffd`.
  **Note for the next session:** HO-0014's own suggested command,
  `git diff --numstat HEAD -- research/experiments/E-0013*`, returns **empty** on a clean tree
  and therefore cannot distinguish "add-only" from "nothing changed". The baseline commit must
  be `4478c3a`.
- `git show --name-only ce845c5` -> 10 files, all under `research/`. No `src/`, no `tools/`,
  no binary.
- `git diff 4478c3a HEAD -- research/hypotheses/` -> **empty** (no H-#### file touched).
- `python research/scripts/research.py validate` -> **exit 0**, "Validation OK". My first run
  reported exit 1, and the cause was entirely my own scratch files in the repo root; I moved
  them outside the repository and re-ran to green. Stated rather than hidden, because the
  first result was mine and not the record's.
- `python research/scripts/research.py experiments` -> E-0013 PENDING, E-00014 PENDING,
  E-00015 PENDING. `python research/scripts/research.py hypotheses` -> 17 hypotheses,
  H-0013 OPEN.
- Read-only source inspection (no build, no engine, no run, no harness invocation):
  `src/eval.h` (whole file; `EvalCoeffs` counted member by member), `src/eval.cpp:352-358`,
  `src/main.cpp:103-114` and `133-147`, `tools/e0012_sprt.py:293-303`, `320-330`, `470-492`,
  `tools/e0011_check.py:369-399`, `src/_write_eval.py:1-32`, `write_eval_p5.py:81-93`,
  `E-0010:335-350`, `E-0011:122-136` and `340-356`, `Q-0006:56-75`,
  `m0_audit/e0011/check_output.txt`.
  `tools/e0012_sprt.py` and every engine source were **cited and not edited**, and I ran
  neither the harness nor any of its modes.
- **Not run, deliberately:** any extraction, count pass, relabeling, fitting, build, Gate-0
  test, feasibility pass, or SPRT game generation; no holdout read; no `research.py round`;
  no `HO-0005`/`W-0003` audit; no H-#### status change; E-0013 not flipped to RUNNING.
  E-00014 and E-00015 not run.
- **Environment caveat, stated rather than hidden.** This session's shell capture is degraded
  exactly as HO-0014 warned: `run_commands` reported `Command exited with code 1` on commands
  that plainly succeeded, and PowerShell's `>` writes UTF-16, so every capture was taken with
  `| Out-File -Encoding utf8` and read from the **file**, which I treat as authoritative over
  the reported status. I note one instance where they materially disagreed: the `validate`
  exit-1 above, which I chased down and which was my own fault, not the record's.
- **Stale-read caution, honoured.** `read_files` can return stale content for line-range
  requests on large files. Every line number this review cites was obtained from a numbered
  dump written to disk, and I caught and discarded two conflicting chunk reads of the E-0013
  addendum before citing L823 and L828. Where an early chunk read and a later numbered dump
  disagreed, the numbered dump is what appears in this record.
- **On the `240` figure:** I report it as not the KING-PST parameter count (128, or 64 under
  the symmetry constraint). I did not re-open the freeze decision, which is SETTLED, and I do
  not treat this as a new argument against freezing - only as a false number inside a rationale.
- **One process note against myself.** While confirming the CLI-assigned id I re-ran
  `research.py new-review` and created a stray stub review (id deliberately not repeated here,
  because naming it would itself register a dangling-id warning). I deleted the stub before
  committing; the tree contains no such record and `validate` is green. Recording it because
  the id space is append-only in spirit and a silently-deleted id is exactly the kind of thing
  this system exists to catch.


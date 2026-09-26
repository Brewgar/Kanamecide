---
id: R-0021
type: review
reviewer: adversarial-reviewer
target: E-0013
kind: critique
status: COMPLETED
work_item: null
related: [E-0013, R-0019, R-0020, S-0028, S-0029, E-00014, E-00015, HO-0014, HO-0015, HO-0016, H-0013, Q-0006, E-0010, E-0011, W-0001, R-0017, DEC-0010, ce845c5, f450976, fce355c]
example: false
created: 2026-09-26
---

# R-0021 - Independent post-repair critique of the E-0013 addendum (seam 8, the B5 s2 slot, the repair section's own claims, and the append-only line)

## Scope

Fresh adversarial-reviewer occupant. I did not write R-0019, R-0020, S-0028 or S-0029 and I
defer to none of them. Everything below is recomputed from the working tree and from git
objects by me; where I quote a prior seat I checked it rather than adopting it.

**In scope (the work order):** internal wholeness of the repaired addendum; an explicit ruling
on seam 8; a ruling on the B5 sentence-2 slot; verification of the repair section's own claims
against the file; independent recomputation of both L1-428 SHA-256 values and a ruling on the
original-vs-addendum line; B3/B4/B5 discharge status; one-line confirmation for
B1/B2/B6/B7 and DN1-DN10; the state of E-00014/E-00015; and E-0013's next status.

**Out of scope, and not touched:** SHRINK, the KING-PST freeze decision, `SUITE_TOLERANCE =
0.02`, the NONE per-game cap, and the X-1/X-2/X-3 branch design. R-0019/R-0020 settled those
and I do not re-litigate them. I ran no training, fitting, extraction, counting, feasibility
pass or SPRT generation, and read no holdout. I did not edit E-0013, E-00014, E-00015,
R-0019, R-0020, any handoff, any H-####, or any `tools/`/`src/` file. I did not flip E-0013
and I did not open or close HO-0005/W-0003.

**Method note.** `read_files` returned stale content for line-range requests on this file, as
warned. Every line number I cite was taken from a numbered dump written to disk by
`_rv4/dump.py` and read back from the file. The full command/exit-code ledger is in my
Verification block.

---

## 1. Internal wholeness - the ten seams

**All ten are joined as contiguous sentences inside their own finding's sections, and nothing
else was deleted in the addendum. VERIFIED.** I joined each one by reading it as prose:

| # | Lines | Reads as | Paren delta |
|---|---|---|---|
| 1 | L471-L475 | the three-bucket list is one list | 0 |
| 2 | L515-L517 | B1's self-collision diagnosis, one sentence | 0 |
| 3 | L542-L543 | the UCI-surface reversal condition, complete | 0 |
| 4 | L593-L598 | **the `S*` conclusion has its object again** - "conversely, a strength comparison against a stage-5 opponent would leave `tempo` inert, which is one of the reasons the strength comparison is deferred rather than run here (cost item 1 above)" | 0 |
| 5 | L639-L649 | **the `LOSS_MARGIN` rule is one sentence** - ends "never FAIL, and never 'no achievement = FAIL'." | 0 |
| 6 | L743-L747 | **the freeze anchor is unsevered** | 0 |
| 7 | L765-L774 | **the `SUITE_TOLERANCE` derivation is whole** | 0 |
| 8 | L834-L848 | the ladder's DISARMED status is provisional and reasoned | **+1** (see §2) |
| 9 | L871-L875 | the ~27k refutation's scope-changing consequence is attached | 0 |
| 10 | L899-L903 | DN10's explicit-dependency sentence is one sentence | -1 (an `(` opens at L896, outside the seam; correct) |

I hunted hardest on the four normatively critical ones and found no sentence that reads
plausibly with a missing object or antecedent. In particular the S* sentence's object ("a
strength comparison against a stage-5 opponent") is present at L594; the `LOSS_MARGIN`
sentence's subject (`LOSS_MARGIN := max(0.002, 0.5 * delta_star)`) is present at L645 and its
consequence clause is present at L646; the freeze anchor's list of deferred values and its
tripwire extension are both present in one run at L737-L747; and the SUITE_TOLERANCE
derivation carries its binomial-SE bound (0.0354) and its "0.6x" placement in the same
sentence. **The four seams R-0020 called normatively critical are the four that are now sound.**

Also verified: the contingency table sits at **L682-L717**, immediately under B3 sentence 3's
announcement at **L677-L680** (which ends in a colon), with no wording change - CORRECT.
**F-U1..F-U6 are one contiguous list at L909-L944** including F-U3's `Owner:/Due:` line at
L931 - CORRECT. B1's cost items 1-4 are contiguous at L521-L548. The BUCKET-1/2/3 list is one
list at L471-L487.

### 1a. NEW BLOCKING FINDING X4 - S-0029 re-severed the file's tail

**The file does not end on a complete sentence. It ends mid-sentence, and S-0029's own
second-pass block is what put it there.**

- **L1252** ends: `...E-0013 remains \`status: PENDING\` - this repair is not authorisation to`
- **L1293** is the file's last non-empty line: `move it, and per R-0020 the flip requires a
  fresh re-critique to confirm.`

Those two lines are one sentence. Joined they read: *"E-0013 remains `status: PENDING` - this
repair is not authorisation to move it, and per R-0020 the flip requires a fresh re-critique
to confirm."* Between them, L1254-L1292, S-0029 inserted its forty-line "Verification
performed ON this repair" block.

This is provable from git, not inferred. At **f450976** (the S-0028 commit) the two lines were
**adjacent** - L1233 and L1234 - and the file ended on that complete sentence. The diff
`f450976..fce355c` is `+` 40 lines inserted between them and nothing else at that point
(`@@ -1232,3 +1251,43 @@`; the context lines show `...not authorisation to` immediately
followed by the insertion, and the `move it, ...` line survives after it as context).

So the second repair pass, whose stated purpose was to fix a misjoin, **re-introduced the exact
X1 failure class - a severed sentence at a block boundary - one paragraph after claiming it had
eliminated it.** This falsifies two claims in the file:

- **L1268**, "the file's **terminal complete sentence** at L1106-L1114" - true of the *narrative*
  (the "The decision." paragraph does end complete at L1114), but the FILE's terminal sentence
  is the orphan at L1293, and its head is stranded at L1252.
- The X1 disposition row at **L964**, "and the file ends on a complete sentence" - **false as of
  HEAD.** It was true at f450976 and S-0029 made it false.

It is blocking, not cosmetic, for one reason beyond tidiness: the stranded head is the sentence
that carries **E-0013's own non-authorisation**. A reader who takes L1252 at face value reads
"E-0013 remains PENDING - this repair is not authorisation to" and then finds 40 lines of
verification and a *different*, complete restatement of the same point at L1291-L1292. The
normative content survives only because S-0029 restated it; the sentence the record actually
ends on is broken. On a pre-registration whose entire function is to be unambiguous about what
is and is not authorised, the file must not end on an orphan.

**Exact repair (mechanical, no wording chosen by me beyond the join):** delete the orphaned
tail at **L1293** in its entirety, and append to the end of **L1252** the text ` move it, and
per R-0020 the flip requires a fresh re-critique to confirm.` - which is the author's own
words, moved not retyped. L1252 then ends `...not authorisation to move it, and per R-0020 the
flip requires a fresh re-critique to confirm.` and the file ends on that complete sentence. The
redundant restatement at L1291-L1292 may stand (it is harmless and honest) or be dropped; it is
not load-bearing. **Note the irony worth recording:** this is the same move S-0029 performed
correctly on seam 8 - delete a stranded tail, move its words back to their head - and it should
have been applied here too.

### 1b. NEW NON-BLOCKING FINDING X5 - an unrecorded head-side deletion

The repair section claims, at **L1199**, "**Other moves, same rule - nothing deleted, nothing
retyped.**" and at **L1153**, "Every continuation was MOVED byte-for-byte, not retyped."

That is true of the *continuations* and false of the *head* at seam 8. At **ce845c5 L707** the
head ended `...i.e. 2.5x headroom (E-00015 measures` - the author's own four-word fragment. At
**f450976** and at HEAD that fragment is **gone**: L834 ends `...i.e. 2.5x headroom` with no
trailing `(E-00015 measures`, and the count of `(E-00015 measures` in the file went 1 -> 2 (the
second being the template's own opening). The first pass therefore **deleted four words of the
author's original head text and did not record doing so.** The X1-a paragraph at L1183-L1197
records only the *tail*-side deletion (`it; B6)`), and states the deletion was made "because it
is the redundant half of the duplication" - which is a true statement about the tail, and
silently untrue as a general claim about the seam.

I am **not** ruling this blocking and I want to be precise about why. The head-side deletion
is substantively *correct and necessary*: R-0020's template begins with `(E-00015 measures ...`,
so keeping the author's fragment would have produced `(E-00015 measures (E-00015 measures ...`
and a second duplication. The repair did the right thing. It is non-blocking because it
removes a severed fragment rather than a complete clause, and because the surviving sentence is
grammatical. But the file asserts a rule ("nothing deleted") that it broke without saying so,
in the very section whose purpose is to make every move auditable line-by-line. **Record it.**

---

## 2. SEAM 8 - the explicit ruling the work order asked for

### (a) Is the current text correct as a pre-registration, or defective?

**Defective as typography; correct as normative text.** Stated precisely:

- The joined sentence at **L834-L848** is a **single grammatical sentence** with a complete
  subject, a complete predicate chain, and a terminal full stop before the closing quote at
  L848. Its requirement is legible end to end: E-00015 measures the realized count; until that
  count exists the band is an arithmetic bound and not a measurement of this record's filter;
  the ladder's DISARMED status is provisional on that count; if the count nevertheless arms
  the ladder, the fallback scope is NOT the mobility/tempo sub-set and must be re-derived and
  re-registered under its own critique before use.
- The defect is a **single unclosed opening parenthesis**, the `(` at **L835**
  (`(E-00015 measures`), which is never closed. Paren delta over the seam is **+1**
  (3 opens, 2 closes; I enumerated every parenthesis in L822-L848 individually: pairs at L822,
  L825, L840 and L845-L846 all balance; only L835's is orphaned).
- The `B6)` duplication is genuinely fixed: `mobility/tempo scope; B6)` = **1**, `B6)` = **1**,
  `it; B6)` = **0**. S-0029's deletion achieved what it said.

**So: a pre-registration defect, of the same class as a typo, not of the class that blocks.**
I want to distinguish this sharply from X1/X4, because conflating them would be wrong in both
directions - it would let a real blemish pass as clean, and it would block a record over a
bracket.

### (b) Does the residual +1 orphan change any NORMATIVE meaning?

**No. I checked this specifically, because it is the question that decides the ruling.**

The orphan changes the *extent* of a parenthetical, not its *content*. As printed, the reader
sees `(E-00015 measures ... provisional on it. If the count nevertheless arms the ladder, the
fallback scope it would apply is not the mobility/tempo sub-set named in E-0011 N1, and the
sub-set is re-derived and re-registered under its own critique before any use (mobility/tempo
scope; B6)` - i.e. the missing `)` would make the whole span from L835 to L840 read as one
parenthetical rather than two. Can any reader **misread what the sentence requires** because of
that?

- **No misreading of the obligation.** The requirement - *re-derive and re-register under its
  own critique before use* - sits in the main clause before the parenthetical and is
  syntactically independent of it. It is stated twice more elsewhere in the file (L843, and
  B6 sentence 4 at L983-L985, and B6 sentence 1's second quoted block at L1039-L1041), so the
  reader has three independent statements of it. Nothing can be under-read.
- **No misreading of the count's status.** "E-00015 measures the realized count" is the first
  clause inside the parenthetical and is unchanged by where the paren closes.
- **No misreading of scope.** `(mobility/tempo scope; B6)` is a citation label, not a
  requirement. Even if a reader mis-attributed it to the whole span rather than to the clause it
  labels, B6's own text is 130 lines away and fully present.
- The one thing a reader *could* get wrong is a **typographic** reading - noticing the imbalance
  and wondering whether a closer was lost. That is a cosmetic doubt about a sentence whose
  content is complete.

**Answer: the +1 orphan is NON-BLOCKING. It changes no normative meaning.**

### (c) Exact replacement text

It needs repair - an unclosed bracket in a normative pre-registration is a defect regardless of
severity, and this system does not ship known-defective text when the fix is free. The
constraint is that the head's paren must close and there must be **exactly one** `B6)`
citation, so the form must not create a second.

**The fix is a single-character insertion. Replace line 837**

> `> record's own filter, and the ladder's DISARMED status is provisional on it. If the count`

**with**

> `> record's own filter, and the ladder's DISARMED status is provisional on it). If the count`

That is: insert one `)` immediately after `provisional on it`, before the full stop.

**Why this is the right form, checked against the constraint:**

- It closes **the head's paren** - the `(` at L835 - at the end of the clause it actually
  governs, which is exactly where R-0020's own template places the sentence boundary (R-0020:698
  reads `...provisional on it. If the count nevertheless...`). The repair restores the
  author's intended extent rather than inventing one.
- Paren delta over L834-L848 goes **+1 -> 0**. I verified the arithmetic: L835's `(` is matched
  by the new `)`; L840's `(mobility/tempo scope; B6)` is untouched and self-closing.
- **`B6)` count stays at exactly 1.** The new character is a bare `)` and contains no citation.
  No second `B6)` is created.
- **Nothing normative is added, removed or reworded.** The only byte that changes is a closing
  bracket placed at the boundary R-0020's template already specified. No authorial decision is
  made on anyone's behalf - which is precisely the thing R-0020 refused to do and which I
  likewise refuse to do by writing new clause text here.

**I explicitly reject the two forms that would also "work".** Do **not** trim the template's
`B6)` - that deletes the string R-0020:690-691 and S-0028's verbatim-adoption claim depend on,
and drives the `mobility/tempo scope; B6)` count to 0, falsifying a recorded claim. Do **not**
restore the tail's `it; B6)` - that returns the duplicate citation and the stranded pronoun.
S-0029's choice of which half to delete was right; only the missing closer at the head's end
remains, and it is one character.

**And I record a disagreement with S-0029's reasoning, not its outcome.** At **L1196-L1197**
S-0029 writes that the orphan "is **not** repaired here because closing it would require
inventing a closing token R-0020 did not supply." **That reasoning does not hold.** R-0020's
template *does* delimit the span - it ends the parenthetical's clause with a full stop after
"provisional on it" (R-0020:698), and condition (a) asks for text that "finish[es] the sentence
begun at L707". A `)` at that point is not an invented token; it is the closer for a span the
ruling itself bounded. The correct disposition was to close it and flag the choice, not to leave
a known defect on the record. S-0029 was right that the defect was inherited and wrong that it
was unfixable. **The defect is inherited - that part of X1-a stands - but it is fixable, and the
fix is above.**

---

## 3. The B5 sentence-2 slot

**Ruling: `UNESTABLISHED` is NOT an acceptable terminal disposition. The heading must be
withdrawn.** I rule on the merits, and I hold S-0029's *observation* to be correct while its
*disposition* to be insufficient.

**What S-0029 got right, and I confirm independently:** the slot is empty. **L811** is the
heading `**B5 sentence 2 (the ladder's citation, corrected - IN THIS RECORD ONLY):**`;
**L812 and L813 are both empty strings** (I read them as raw repr, not as rendered blanks);
**L814** is B5 sentence 3's heading. And the hole is **pre-existing**, not introduced by either
repair pass: at **ce845c5** the same geometry holds (L684 heading, L685-L686 blank, L687 =
B5 s3). I also confirm S-0029's negative finding, which is the hard part: the block at
**L822-L848** is introduced by B5 sentence 3, whose preamble at L814-L820 ends in a colon at
L820 (`...a follow-up obligation is filed against E-0013's close-out:`) and is immediately
followed by the quoted correction note. **That block is spoken for. It is not B5 s2's body.**

**Why `UNESTABLISHED` is not an acceptable disposition for a pre-registration.** Three reasons,
in order of weight:

1. **A heading that announces normative text with an empty body is a live misstatement.** As
   printed, the file tells the next reader that B5 has a second sentence, that it is "the
   ladder's citation, corrected", and that it is "IN THIS RECORD ONLY" - and then supplies
   nothing. That is not a neutral gap. It asserts the existence of a correction that the file
   does not contain, and a reader who is looking for how the ladder's citation was corrected
   will either (i) go read the L822-L848 block, believing it to be s2, thereby **double-counting
   the same correction as two findings** - which is exactly the misreading the disposition row
   warns against but does not prevent - or (ii) conclude a correction is missing. Both are
   wrong, and the record gives the reader no way to tell which error they just made.
2. **`UNESTABLISHED` is a verdict about the past, standing in for a decision about the present.**
   The finding is genuinely unestablished - I agree, and S-0029 is right not to have guessed -
   but the *current* state of the document is not unknown: it is a heading with nothing under
   it. The disposition leaves the defect in place and labels it. Naming a defect is not
   dispositioning it. R-0019's own standard, quoted in HO-0014, is that a finding counts as
   discharged only when the record **contains text that discharges it**; a label is not text.
3. **The honest options are both cheap, so leaving it is not the conservative choice.** Either
   withdraw the heading, or fill the slot. Both are one edit. Leaving it is the only option that
   preserves a false assertion, which makes it the *least* conservative option despite feeling
   like the most cautious one.

**I require the heading to be WITHDRAWN, not filled.** Filling it would require me to invent
normative text on another seat's behalf - the exact failure mode R-0020 refused at X1-a, and the
reason it supplied a template instead of guessing. I will not do it either, and no reviewer
should. But the asymmetry is decisive: **a withdrawn heading asserts nothing, and an invented
body would assert something.** Withdrawing is the only option that cannot mislead.

**Exact replacement text.** Replace **L811-L813** (the heading and its two blank lines) with
this single paragraph, in the record's own section idiom:

> **B5 sentence 2 (the ladder's citation, corrected - IN THIS RECORD ONLY): WITHDRAWN
> 2026-09-26, body never established.** This heading announced a quoted sentence that does not
> exist. Its slot was empty in the addendum as first filed (`ce845c5`, L684 heading with L685-
> L686 blank) and no body for it has been located in any revision; the correction it announced
> is already stated, once and in full, as the dated correction note under B5 sentence 3
> (L822-L848) and again as B6 sentence 1's second quoted block (L1032-L1041). The heading is
> therefore **withdrawn rather than filled**: filling it would require inventing normative text
> on another seat's behalf, which this record does not do. **No normative content is lost by
> this withdrawal and none is invented to replace it** - the backwards-citation correction, the
> `k4-k3 = -3.7` / `k6-k5 = -11.5` recomputation, the DISARMED-and-provisional status and
> obligation F-U4 all stand as written at L822-L848. This withdrawal closes the slot; it re-opens
> no decision and changes no gate.

**Two requirements on that text, which I state so the next cycle is mechanical:** (i) it must
name where the correction actually lives, so no reader goes looking for a second one - hence
the L822-L848 and L1032-L1041 pointers; and (ii) it must say explicitly that nothing normative
is lost and none invented, so the withdrawal cannot be misread as a deletion of content. It
does both.

**And I record a disagreement with S-0029's L1220-L1223**, which says the block "sits far away
under B6 sentence 1" and was "left exactly as found and is flagged here for the next reviewer".
Two problems. First, it is **stale**: the disposition row at L966 correctly notes the `ce845c5`
geometry, but L1220-L1223 still asserts the post-repair location, and after the repair the
note is at **L822-L848 under B5 s3**, with **B6 s1 at L1016** - so the observation points at
the wrong place and would send a reader to the wrong section. Second, "flagged for the next
reviewer" **is the deferral that produced this finding**; I am the next reviewer and I am ruling
it. Both L1220-L1223 and the L966 row's closing sentence should be updated to the withdrawal
above rather than left to point at a stale location.

---

## 4. The repair section's own claims - verified, not accepted

| Claim (where) | My verdict | Evidence |
|---|---|---|
| All 10 seams joined (L1264-L1266) | **TRUE** | joined and read individually; table in §1 |
| Contingency table under B3 s3 (L1266-L1267) | **TRUE** | announcement L677-L680 ends in a colon; table L682-L717; no wording change |
| F-U1..F-U6 contiguous (L1267) | **TRUE** | L909-L944, F-U3's `Owner:` at L931 |
| File ends on a complete sentence (L964, L1268) | **FALSE** | **X4**: ends on the orphan at L1293, head stranded at L1252 |
| X2 arithmetic = R-0020 verbatim, 240 -> 128 (L1269) | **TRUE** | R-0020:713-715 text matches L791-L807; `128` present at L799, `not 240` at L799; the false clause is gone from the quoted block |
| X3 `owner:` set (L1269-L1270) | **TRUE** | E-00014 L10 and E-00015 L10 both `owner: systems-researcher` |
| `mobility/tempo scope; B6)` = 1, `B6)` = 1 (L1276-L1277) | **TRUE** | counted over L834-L848: 1, 1, and `it; B6)` = 0 |
| Paren balance +1, "inherited from R-0020's template" (L1192-L1195, L1277-L1278) | **TRUE as to the fact, FALSE as to the conclusion** | +1 confirmed; but see §2(c) - it is fixable with one character, so "not repaired because it would require inventing a token" does not hold |
| "nothing deleted, nothing retyped" (L1153, L1199) | **FALSE** | **X5**: the head-side `(E-00015 measures` was deleted in the first pass, unrecorded |
| Seam-8 misjoin "found on re-read" (L1272-L1273) | **TRUE, and the fix worked** | but the same pass created X4 and did not notice it |

### 4a. X2 arithmetic - recomputed from scratch by me

I re-derived every number. **The inserted arithmetic is CORRECT and R-0020's is reproduced
exactly.**

- Free scalars: 10 (non-king `mg_value`/`eg_value`) + 640 (five non-king PST tables, 5x64x2)
  + 20 (pawn structure) + 2 (mobility) + 10 (positional/king) + 1 (tempo) = **683**.
  The record's `683` is **correct**.
- Upper bound on realized usable yield: `76587`. `76587 / 683 = 112.13` - the record's
  "about 112 positions/parameter overall" is **correct**.
- Train side: `0.8 x 76587 = 61269.6`; `61269.6 / 683 = 89.7` - the record's "about 89" is
  **correct**.
- Positions needed at 500/parameter: `500 x 683 = 341,500`. `341500 / 76587 = 4.459` - the
  record's "~4.5x short" in the body and "4.46x" in the table are **both correct**.
- Unfrozen comparison: `683 + 128 = 811`; `76587 / 811 = 94.4` - the record's "raises that
  ratio from about 94 to about 112" is **correct**.
- `240` -> `128`: KING PSTs are two 64-entry tables, so 128 free scalars, or 64 under the
  record's own `pst[s] == pst[mirror(s)]` constraint. The record says exactly this at L799
  (`128 free scalars, or 64 under ... - not 240)`). **Correct.**

**So R-0020's X2 is genuinely DISCHARGED, and its ~4.46x figure is not an overstatement - if
anything the body text's "4.5x" is the rounder of two correct renderings.**

### 4b. Whole-file grep for surviving compliance claims

I grepped the entire file for `defensible`, `>= 500`, `>=500`, `meets the standard`, `240`,
`(240 params)`, `500 positions`. **Every surviving instance is a record of the limitation, not
an assertion of compliance. X2's compliance claim is fully removed.**

- **L792** - `> fitted-parameter count within E-0011 N1's '>= 500 positions/parameter'
  standard, and` - the full clause is *"It does NOT, however, bring the fitted-parameter count
  within ... standard, and this record does not claim it does"*. A **negation followed by
  "does not claim"**. Records the limitation. CORRECT.
- **L809** (editorial note) and **L965** (X2 row) and **L1136** (repair narrative) - all three
  quote the false clause **inside an explicit refutation**: L809 says it "was FALSE and has been
  DELETED and REPLACED"; L965 says "That is false:"; L1136 says "is false by a factor of
  ~4.46". Quoting a claim to kill it is not asserting it. CORRECT.
- **L1052** - `| F3 | KING-PST freeze-vs-fit (240 params) | **VALUE**: **FROZEN** ...` - `240`
  here is **R-0019's own item label**, quoted in a table whose disposition is FROZEN, and both
  L809 and L1217-L1218 say so explicitly and deliberately ("is R-0019's own item label and is
  left as quoted"). **CORRECT, and the reasoning is the same one that correctly protects E-0011
  from being edited.**
- **L42** and **L883** - `N=240` - the E-0010 ladder rung size, an unrelated quantity that
  happens to share the digits. DN1 at L883 records the k1-k5 / k6 distinction. NOT A
  PARAMETER COUNT. No action.
- **L884** - `1,240-game` - E-0011's scaled estimate, recorded by DN2 as a distinct provenance
  band. Unrelated. No action.

**No surviving instance asserts compliance. I record no finding here.**

---

## 5. The L1-428 append-only proof - recomputed independently, and the line ruled

### 5a. Both hashes, recomputed by me from two directions

I recomputed rather than copied, from `git show ce845c5:<path>` and from the working file,
over lines 1-428 **including their line terminators**, UTF-8:

- `ce845c5` lines 1-428 -> `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`,
  **22,270 bytes**
- HEAD lines 1-428 -> `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`,
  **22,270 bytes**

**Equal. I also compared the two ranges directly with a unified diff: 0 lines.** I checked the
orchestrator's measurement rather than trusting it and **it is correct in every particular** -
both hashes, the byte count, and the zero-line diff.

### 5b. The line R-0020 left open - where each part falls

R-0020 held the distinction without ruling it. **I rule it.**

- **An in-place, review-licensed repair of the ADDENDUM is legitimate.** The addendum is the
  artefact *under review*. When review finds the document it is examining to be internally
  corrupt - severed sentences, a relocated table, obligations split across a table - repairing
  that corruption in place, under an explicit written licence from the reviewing seat, with every
  move itemised, is the only correct disposition. The alternative - leaving a known-corrupt
  normative document in place because editing it would "touch history" - protects a piece of
  paper rather than the truth. R-0020's own instruction, "move that text, not rewrite it", is
  the right standard and S-0028 honoured it for the moves it made.
- **An in-place edit of the ORIGINAL is not legitimate, ever, and nothing in R-0020's licence
  reaches it.** The original pre-registration is the thing the append-only rule exists to
  protect: it is what any future reader cites to establish what was promised *before* any number
  existed. If it can be edited in place, no pre-registration is worth anything.

**Naming the side of the line for each part of this file:**

- **L1-L428 - the ORIGINAL pre-registration. PROTECTED SIDE.** Byte-identical to `ce845c5`,
  proved by hash and by a zero-line diff. It falls on the correct side and must never be edited
  in place. Any future change here must be a new dated addendum below L429.
- **L429-L1294 - the ADDENDUM. REVIEW-LICENSED SIDE.** This is where the in-place repair is
  legitimate, and it is where S-0028's and S-0029's edits all fall. Every edit I have ruled
  legitimate (seam 8's `B6)` deletion) and every edit I require (X4's tail rejoin, §2(c)'s
  closer, §3's withdrawal) is on this side. **The line is the L428/L429 boundary and it holds
  exactly.**

### 5c. `ce845c5..HEAD` now reads 347/127, not 288/127 - and the record's account is honest

**The orchestrator's figure in the work order is wrong and I correct it.** I measured at four
boundaries:

- `4478c3a..ce845c5` (the ORIGINAL addendum, pre-repair) -> **`648` insertions, `0` deletions**
  - the historical figure R-0020 and the file both cite. **Correct at that boundary.**
- `ce845c5..f450976` (S-0028's pass) -> **`288` insertions, `127` deletions**
- `f450976..fce355c` (S-0029's pass) -> **`71` insertions, `12` deletions**
- `ce845c5..HEAD` (both passes together) -> **`347` insertions, `127` deletions**

**`288/127` is the S-0028-only boundary, not `ce845c5..HEAD`.** The work order's claim that
"`ce845c5..HEAD` now reads 288/127" mislabels the boundary; the correct current figure is
**347/127**. I record this as a correction to the orchestrator's brief, not as a finding against
the record - the record never asserts 288/127.

**Is the record's characterisation honest? YES, and I want to be explicit that I checked this
adversarially.** The file says at **L1236-L1239**: *"That is why the historical `648 additions /
0 deletions` numstat over `ce845c5..HEAD` no longer reads zero-deletions. That is stated here
rather than papered over, and the distinction is the point."*

Two things could have made that dishonest, and neither is present. First, it does not hide the
change - it names the historical figure, says it no longer holds, and explains why. Second, it
does not overstate what was protected: the sentence immediately before is the hash proof over
**L1-L428 only**, and the file nowhere claims the addendum is append-only. The 127 deletions are
the visible, itemised cost of a review-licensed repair, and the file says so in the same
paragraph that proves the protected side is untouched. **This is the honest way to record it.**

**One correction the record should make for precision** (non-blocking, but it matters because
the sentence as written is loose): the `648 additions / 0 deletions` figure is the numstat of
**`4478c3a..ce845c5`**, not of `ce845c5..HEAD`. L1236 attaches it to `ce845c5..HEAD`, which is
the wrong baseline. Measured against its true baseline the sentence is stronger, not weaker:
`4478c3a..HEAD` is **`868` insertions, `0` deletions** - i.e. **the entire addendum, repairs
included, is still strictly append-only relative to the original pre-registration.** That is the
number that discharges the append-only obligation outright, and the record is currently claiming
a weaker version of it under a mislabelled baseline.

---

## 6. B3, B4, B5 - discharge status now that placement and the false arithmetic are fixed

**B3: DISCHARGED (was PARTIALLY).** Its two defects were (i) a margin with no derivation and a
false power justification, and (ii) a contingency left to be chosen after `s_d_inner` was known.
Both are now closed in text. The false clause `'for any realistic loss variance'` is superseded
by the decidability condition `s_d <= 0.0101` at **L658-L666**; the anti-apathetic clause is
correctly rescoped to QUALITY at **L670-L675**; the Power-section sentence that converted a
power failure into an apathetic rejection is quoted and superseded verbatim at **L1080-L1089**;
and the contingency is decided NOW, exhaustively, with no fourth branch, at **L682-L717**
immediately under the sentence announcing it. The X3 route and the F-U3 obligation are both
present. **The residual is not a defect** - it is that the contingency's *input* is E-00014's
and does not exist yet, which is BUCKET 2 by design and honestly labelled.

**B4: DISCHARGED (was PARTIALLY).** Q-FIT is closed by value with SPSA withdrawn as a leakage
channel (**L725-L732**); the substitution path is closed and the per-game cap ruled NONE
(**L1066-L1075**); and `SUITE_TOLERANCE = 0.02` is pinned as a number with its derivation
(**L752-L774**). The F2-style "commit field by design" residual is a pointer to a named
instrument, not a gap.

**B5: still PARTIALLY DISCHARGED - but for a different reason than before, and I want to be
precise about which part moved.** The *substantive* half is now done: the freeze decision is
stated at L782-L807, the false rationale is gone, the arithmetic is correct, and the historical
record is protected by a dated correction note plus F-U4 rather than by a retroactive edit -
which is the right disposition and which I endorse. **But two text defects inside B5's own
section remain open:** the **+1 orphan at L835** (§2) and the **empty B5 s2 slot at L811**
(§3). Neither is a re-litigation of the freeze decision, which I am forbidden from touching and
which is untouched. But a heading in B5 that announces text B5 does not contain, and an unclosed
bracket in B5's headline correction note, are defects *of B5* in a pre-registration. **B5 stays
PARTIALLY DISCHARGED until §2(c) and §3 are applied.** Both fixes are supplied above; the cycle
after this one is mechanical.

### 6a. The twelve F-item closures still close against the RESTORED freeze anchor

**VERIFIED.** I re-read the anchor at **L737-L747** in full and then checked each of F1-F12
against it. The anchor names the nine deferred values (fresh SPRT salt, salt-distance citation,
KING-PST scope choice, MAE phase-tertile boundaries, label-mapping code, optimizer
seed/L2/budget/clipping, stage index `S*`, suite identity/N/metric/**tolerance**), requires all
of them to be assigned ONCE and committed with SHA-256 **in the same pre-fit commit as the
game-split map**, forbids reading the holdout before that commit exists, and extends the
tripwire to first-time assignment. That is one unsevered sentence with both halves - the
obligation and the tripwire - present.

- **F1** value (L-BFGS, SPSA withdrawn) - closes on its own, no anchor needed. OK.
- **F2** pointer to the pre-fit commit, choosable on TRAIN-inner only - **rests on the anchor's
  "same pre-fit commit" clause, which is present.** OK.
- **F3** value (FROZEN, here not at preflight) - closes by value. OK.
- **F4** value for N/metric/tolerance, pointer for identity - the identity pointer names "the
  pre-fit commit of B4 s2" **explicitly**. OK.
- **F5** pointer: TRAIN-positions-only tertiles, boundary list + SHA-256 frozen in the pre-fit
  commit, never from holdout phase values - **rests on the anchor, and adds the holdout
  prohibition the anchor supplies.** OK.
- **F6** pointer + value: no salt used; admissibility rule `abs(S-S')*1000003 > cap-1` pinned
  for the deferred contract. OK.
- **F7** value `S* = 6`, floor = compiled-in table. OK.
- **F8** value: side-to-move frame. OK.
- **F9** value: dedup GLOBAL before the split. OK.
- **F10** value, computed not deferred. I re-derived: `abs(20260926-20260924) = 2`;
  `2 x 1,000,003 = 2,000,006`, and `2,000,006 >= 1,000,003 > 1,999`. **Arithmetic correct.**
- **F11** pointer: E-00014 plus the pre-decided contingency. OK.
- **F12** value: NONE. OK.

**All twelve close against the restored anchor. No F-item depends on a severed sentence.**

---

## 7. B1, B2, B6, B7 and DN1-DN10 - undisturbed by the two repair passes

One line each, as asked. I re-read each in the current file rather than trusting the
disposition table.

- **B1 - DISCHARGED, undisturbed.** S-1 superseded by the named two-parameter-table mechanism
  (L552-L570), the N1 coefficient-regeneration note present (L572-L581), `S* = 6` pinned with its
  consequence (L585-L598), conjunct (e) re-designated NOT-EVALUATED-IN-THIS-RUN (L1094-L1105).
  Neither repair pass touched B1's substance.
- **B2 - DISCHARGED (text), undisturbed.** Colour frame pinned to the side-to-move frame with a
  FAIL consequence (L606-L615); the unmeasured-gain acknowledgement intact (L620-L630); the
  E-00014 delegation and the `LOSS_MARGIN := max(0.002, 0.5*delta_star)` rule whole at
  L635-L649 - the seam-5 repair, and the rule's "never less" clause is present.
- **B6 - DISCHARGED (rule text), undisturbed.** The count-pass rule and the 76,593 relabelling
  (L1019-L1030), the ~27k refutation with its scope-changing consequence (L867-L875, the seam-9
  repair), and the scope-floor rule with its TRAIN-side floor (L977-L988) all intact.
- **B7 - DISCHARGED, undisturbed.** Q-0006 gate 7 quoted as authority (L996-L998) and the
  verification handoff rule (L1000-L1010) with F-U5 present.
- **DN1-DN10 - undisturbed, all ten dispositioned.** DN1 (L883), DN2 (L884), DN3 (L885), DN4
  (L886), DN5 (L887), DN6 (L888), DN7 (L889), DN8 (L890), DN9 (L891), DN10 (L892) with its
  explicit-dependency sentence whole at L896-L903 (the seam-10 repair). None silently dropped;
  the table is at L881-L892 and the count is ten.

---

## 8. E-00014 / E-00015 - have not run

**Neither has run, and I verified that rather than assuming it.**

- E-00014: `status: PENDING`, `result: null`, `owner: systems-researcher`, `completed: null`.
- E-00015: `status: PENDING`, `result: null`, `owner: systems-researcher`, `completed: null`.
- No `m0_audit/e0014*` or `m0_audit/e0015*` directory exists; `m0_audit/` contains only
  `build, e0011, e0011_failed_attempt1, e0012, e0012_known, e0012_null, runjob_test, s0018`.
- `research.py experiments` reports E-0013, E-00014 and E-00015 all PENDING.

**Therefore the honesty questions have nothing to bite on yet, and I rule them prospectively.**
No holdout has been read, so there is no holdout read to report. No number from either pass
exists, so **no threshold or band can have moved after a number appeared** - and I checked the
one place it could have hidden: `LOSS_MARGIN` is still `0.002` at L275 and is only ever made
*more* conservative by `max(0.002, 0.5*delta_star)` at L645, which is a floor, not a ceiling.
`SUITE_TOLERANCE` is still `0.02`. The 30,000 floor is still 30,000 and is applied to the
TRAIN-side count. The X-1/X-2/X-3 branches are decided in advance at L682-L717, exhaustively
and mutually exclusively, with no fourth branch and no discretion left to whoever reads the
number - so **when the numbers arrive, the branch will be SELECTED by the measurement rather
than asserted, because there is no mechanism by which it could be asserted.** That design is
sound and I endorse it prospectively. **I cannot certify honest consumption of numbers that do
not exist; I certify only that the record is built so that consumption will have to be honest.**

---

## 9. E-0013's next status

**E-0013 remains `status: PENDING`. It may not leave PENDING on this review, and I am not
flipping it.** I do not pre-authorise the PENDING -> RUNNING transition, for the same reason
R-0020 declined to: my job was to find whether the repair is sound, and it is not yet sound.

**What is outstanding, all of it mechanical and none of it a judgement call:**

1. **X4** - rejoin the file's tail (delete L1293, append its text to L1252). Exact text in §1a.
2. **§2(c)** - insert one `)` after `provisional on it` at L837. Exact text in §2(c).
3. **§3** - withdraw the B5 sentence-2 heading at L811-L813. Exact text in §3.
4. **X5** - record the head-side `(E-00015 measures` deletion in the X1-a paragraph, and
   correct "nothing deleted, nothing retyped" at L1153/L1199 to name the two deletions
   (head-side, tail-side) rather than none.
5. **§5c** - correct the baseline on L1236 from `ce845c5..HEAD` to `4478c3a..ce845c5`, and
   record the stronger true figure `4478c3a..HEAD = 868 insertions, 0 deletions`.
6. **§3 / §2(c) follow-ups** - update the stale location claim at L1220-L1223 to the post-repair
   geometry, and correct S-0029's "not repaired because it would require inventing a closing
   token" at L1196-L1197, which does not hold.

**The exact missing sentence for the next cycle, so it is mechanical rather than interpretive.**
I am not the seat that writes it into E-0013, but the sentence that must exist before E-0013
may leave PENDING is this, and I give it verbatim so no seat has to compose it:

> **Re-critique gate (added 2026-09-26 under R-0021).** This record may leave `status: PENDING`
> for `status: RUNNING` only when a fresh adversarial-reviewer critique confirms, by
> line-range read, that (i) the file ends on a complete sentence, (ii) the parenthesis opened at
> the seam-8 correction note is closed and exactly one `B6)` citation remains, (iii) the B5
> sentence-2 slot is withdrawn rather than filled, (iv) every deletion made in either repair
> pass is itemised in the dated repair section, and (v) lines 1-428 still hash to
> `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6` on both sides. The repair
> section is **not** authorisation to run, and no seat may flip this record on the strength of
> the repair section's own claims.

That sentence is what I am requiring. Until it is in the record and a fresh critique confirms
it, E-0013 stays PENDING.

---

## Verdict

**NOT CLEAN - E-0013 remains `status: PENDING`.**

**Two new findings, both introduced by the repair passes themselves and neither present in what
they were repairing:**

- **X4 (BLOCKING).** The file does not end on a complete sentence. L1252 ends `...this repair is
  not authorisation to` and the file's last line, L1293, is the stranded continuation `move it,
  and per R-0020 the flip requires a fresh re-critique to confirm.` **S-0029 caused this** by
  inserting its forty-line verification block between the two halves of one sentence; at
  `f450976` they were adjacent. This is the X1 failure class re-introduced one paragraph after
  being declared eliminated, and it falsifies the X1 row's claim at L964 and the verification
  claim at L1268. The sentence it strands carries **E-0013's own non-authorisation**. Fix in §1a.
- **X5 (NON-BLOCKING, recorded).** The claim "nothing deleted, nothing retyped" (L1153, L1199)
  is false: the head-side `(E-00015 measures` was deleted in S-0028's pass and not recorded.
  The deletion was substantively correct and necessary; the silence about it is the defect.

**Seam 8, ruled as the work order required:** the current text is **defective as typography,
correct as normative text**; the residual +1 orphan **changes no normative meaning** (the
obligation is in the main clause and is stated three times independently in the file); it
**needs repair** because a pre-registration should not ship a known-unclosed bracket when the
fix is one character; the **exact replacement is a single `)` inserted after `provisional on it`
at L837**, which closes the head's paren, takes the seam's paren delta to 0, and leaves exactly
one `B6)` citation. I also **disagree with S-0029's stated reason** for not repairing it: no
token needed inventing, because R-0020's own template bounds the span.

**The B5 s2 slot: `UNESTABLISHED` is NOT an acceptable disposition; the heading must be
WITHDRAWN**, with exact text in §3. Naming the defect is not dispositioning it, and a heading
that announces a correction the record does not contain is a live misstatement that will cause
double-counting or a false "a correction is missing" conclusion. Withdrawal is the only option
that cannot mislead; filling would require inventing normative text, which no seat should do.

**Confirmed sound (independently verified, not inherited):** the ten seams are joined, with the
four normatively critical ones now whole; the contingency table is under B3 s3; F-U1..F-U6 are
contiguous; the `B6)` duplication is genuinely fixed; the freeze anchor at L737-L747 is
unsevered and **all twelve F-items close against it**; X2's arithmetic is **correct in every
figure** (683 free scalars, ~112 overall, ~89 train-side, 341,500 needed, 4.46x short, 94 -> 112,
240 -> 128) and reproduces R-0020's text; **no surviving instance of "defensible", ">= 500" or
"240" asserts compliance** - all record the limitation; X3's `owner:` fields are set; B1, B2,
B6, B7 and DN1-DN10 are undisturbed; the L1-428 hash pair is **verified equal by me from two
directions** (0-line diff), and the `ce845c5..HEAD` = 347/127 characterisation at L1236 is
**honest** though it mislabels its baseline.

**Discharge status: B3 DISCHARGED, B4 DISCHARGED, B5 still PARTIALLY DISCHARGED** (substantive
half done; two text defects remain in its section, both with supplied fixes).

**E-00014/E-00015 have not run**; the record is built so the X-1/X-2/X-3 branch must be
*selected* rather than asserted, and I certify that design prospectively.

**E-0013 must stay PENDING** until X4, §2(c), §3 and X5 are applied and a fresh re-critique
confirms. **I did not flip E-0013, did not run anything, and changed no status.** The exact
missing sentence is in §9.

## Date

2026-09-26

> A review never edits the original report - it lives here and is linked from the
> debate/report it concerns.

---

## Verification Block (R-0021 - independent recomputation; raw commands, exit codes, hashes)

All commands run from `c:\Users\tahae\Kanamecide` on Windows/PowerShell. This shell reports
`Command exited with code 1` on commands that **succeed**; every exit code below is stated
explicitly and was captured to a file, never read from the terminal echo. **Exit code 0 = OK.**

**A. Tree state and identity**

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git status -sb` | 0 | `## master...origin/master`; only `?? _rv4/` (my own scratch, removed before close) |
| 2 | `git rev-parse HEAD` | 0 | `fce355c7b625ea53fc3cb3c4ae5797ff5cf8d7a4` |
| 3 | `git rev-parse origin/master` | 0 | `fce355c7b625ea53fc3cb3c4ae5797ff5cf8d7a4` - **HEAD == origin/master** |
| 4 | `git --no-pager log --oneline -15` | 0 | `fce355c` (S-0029) on top of `f450976` (S-0028) on top of `a6394f5` (R-0020) on top of `ce845c5` (S-0025) on top of `4478c3a` (E-0013 original) |

**B. The L1-428 append-only proof - recomputed by me, both directions**

| # | Command | Exit | Observed |
|---|---|---|---|
| 5 | `git show ce845c5:<E-0013 path>` (subprocess, decoded UTF-8) | 0 | 1,074 lines, 73,719 bytes |
| 6 | SHA-256 over `ce845c5` lines 1-428 incl. terminators, UTF-8 | 0 | `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`, **22,270 bytes** |
| 7 | SHA-256 over HEAD lines 1-428 incl. terminators, UTF-8 | 0 | `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`, **22,270 bytes** - **EQUAL** |
| 8 | `difflib.unified_diff(ce845c5 L1-428, HEAD L1-428, n=0)` | 0 | **0 lines** |
| 9 | HEAD file size | 0 | 95,290 bytes, 1,294 lines, 0 CR, ends with `\n` |

**Orchestrator's claim checked:** hashes, 22,270 bytes and the 0-line diff are **all confirmed
correct**. Their `288/127` numstat figure is **wrong** - see C.

**C. numstat at every boundary (correction to the work order's brief)**

| # | Command | Exit | Observed |
|---|---|---|---|
| 10 | `git diff --numstat 4478c3a ce845c5 -- <E-0013 path>` | 0 | `648	0` - the historical figure, at its true baseline |
| 11 | `git diff --numstat ce845c5 f450976 -- <path>` | 0 | `288	127` (S-0028 only) |
| 12 | `git diff --numstat f450976 fce355c -- <path>` | 0 | `71	12` (S-0029 only) |
| 13 | `git diff --numstat ce845c5 HEAD -- <path>` | 0 | **`347	127`** - the work order's "288/127" mislabels this boundary |
| 14 | `git diff --numstat 4478c3a HEAD -- <path>` | 0 | **`868	0`** - the whole addendum incl. both repairs is still append-only vs the original |

**D. X4 - the re-severed tail, proved by git**

| # | Command | Exit | Observed |
|---|---|---|---|
| 15 | `git show f450976:<path>` tail lines 1233-1234 | 0 | `...not authorisation to` / `move it, and per R-0020 the flip requires a fresh re-critique to confirm.` - **ADJACENT** |
| 16 | HEAD lines 1252 / 1293 | 0 | same two strings, now **41 lines apart** with L1254-L1292 between them |
| 17 | `git diff --unified=2 f450976 fce355c -- <path>` | 0 | hunk `@@ -1232,3 +1251,43 @@`; `+` 40 lines inserted between the two halves; the `move it,` line survives as trailing context. **The insertion is the cause.** |
| 18 | `git diff --numstat f450976 fce355c` | 0 | `71	12` - consistent with a 40-line insertion plus the seam-8 and table edits |
| 19 | Search HEAD for `not authorisation to` / `move it,` | 0 | hits at L1252 and L1293 respectively, and nowhere else |
| 20 | Search `ce845c5` for the same strings | 0 | **0 hits** - the defect is not pre-existing; S-0029 introduced it |
| 21 | Join L1252+L1293 | 0 | `...E-0013 remains \`status: PENDING\` - this repair is not authorisation to move it, and per R-0020 the flip requires a fresh re-critique to confirm.` - one sentence, confirming the two lines are its halves |

**E. X5 - the unrecorded head-side deletion**

| # | Command | Exit | Observed |
|---|---|---|---|
| 22 | `git show ce845c5:<path>` line 707 | 0 | `> yield is 75,600 to 76,587 against a 30,000 floor, i.e. 2.5x headroom (E-00015 measures` - the author's fragment **present** |
| 23 | `git show f450976:<path>` line 834 | 0 | `> yield is 75,600 to 76,587 against a 30,000 floor, i.e. 2.5x headroom` - fragment **gone** |
| 24 | Count of `(E-00015 measures` | 0 | ce845c5 = **1**; f450976 = **2**; HEAD = **2** - deleted in S-0028's pass |
| 25 | Grep HEAD L1110+ for `delet` | 0 | L1183-L1189 records **only** the tail-side `it; B6)` deletion; the head-side deletion is **absent** |

**F. Seam 8 - parens enumerated, not estimated**

| # | Command | Exit | Observed |
|---|---|---|---|
| 26 | Per-character `(`/`)` scan of L822-L848 | 0 | balanced pairs at L822, L825, L840, L845-L846; **one orphan `(` at L835** |
| 27 | Paren delta over L834-L848 | 0 | opens=3, closes=2, **delta +1** |
| 28 | Count `mobility/tempo scope; B6)` / `B6)` / `it; B6)` in seam | 0 | **1 / 1 / 0** - duplication genuinely fixed by S-0029 |
| 29 | Whole-file paren balance | 0 | `f450976` delta +1; **HEAD delta -9**; original L1-428 delta **0** |
| 30 | Paren delta per seam (1-10) | 0 | 0,0,0,0,0,0,0,**+1**,0,-1; the -1 at seam 10 is the `(` opening at L896, outside the seam - correct |

**G. X2 arithmetic - recomputed from scratch**

| # | Quantity | My computation | Record's figure | Match |
|---|---|---|---|---|
| 31 | Free scalars | 10+640+20+2+10+1 = **683** | 683 | YES |
| 32 | Positions/param overall | 76587/683 = **112.13** | ~112 | YES |
| 33 | Train-side | 0.8x76587 = 61269.6; /683 = **89.71** | ~89 | YES |
| 34 | Needed at 500/param | 500x683 = **341,500** | 341,500 | YES |
| 35 | Shortfall factor | 341500/76587 = **4.4590** | ~4.5x body / 4.46x table | YES |
| 36 | Unfrozen ratio | (683+128)=811; 76587/811 = **94.44** | ~94 -> ~112 | YES |
| 37 | KING-PST count | 2 tables x 64 = **128**; 64 under the mirror constraint | 128 (or 64), "not 240" | YES |

**H. Compliance-claim grep, whole file**

| # | Pattern | Hits | Ruling |
|---|---|---|---|
| 38 | `defensible` | L809, L965, L1136 | all three quote the clause **inside a refutation** ("was FALSE", "That is false", "is false by a factor of ~4.46"). No compliance claim. |
| 39 | `>= 500` | L792, L809, L965, L1136 | L792 is a **negation** ("It does NOT ... and this record does not claim it does"); rest are refutations. |
| 40 | `meets the standard` / `>=500` | 0 | - |
| 41 | `240` | L42, L799, L809, L883, L884, L965, L1052, L1137, L1138, L1215, L1217, L1269 | L42/L883/L884 are the E-0010 ladder `N=240` and `1,240-game` (unrelated quantities); L1052 is R-0019's quoted F3 label with the freeze VALUE beside it; the rest are the correction's own record. **No instance asserts compliance.** |
| 42 | `(240 params)` | L809, L1052, L1217 | all three explicitly identify it as R-0019's item label, left as quoted. Correct. |

**I. Structure, slots, records**

| # | Command | Exit | Observed |
|---|---|---|---|
| 43 | Dump L809-L821, raw repr | 0 | **L811** = the B5 s2 heading; **L812 = `''`**, **L813 = `''`** (truly empty); L814 = B5 s3 heading; L820 ends in a colon |
| 44 | `git show ce845c5:<path>` L684-L687 | 0 | same empty slot - heading L684, L685/L686 empty, L687 = B5 s3. **Pre-existing, confirmed.** |
| 45 | Section-heading census | 0 | 41 headings; all original sections L1-L428 present and unaltered; addendum L429+ |
| 46 | `research.py experiments` | 0 | E-0013 PENDING, E-00014 PENDING, E-00015 PENDING |
| 47 | E-00014 front matter L1-L16 | 0 | `status: PENDING`, `result: null`, **`owner: systems-researcher`**, `completed: null` - **X3 confirmed** |
| 48 | E-00015 front matter L1-L16 | 0 | `status: PENDING`, `result: null`, **`owner: systems-researcher`**, `completed: null` - **X3 confirmed** |
| 49 | `Get-ChildItem m0_audit -Directory` | 0 | `build, e0011, e0011_failed_attempt1, e0012, e0012_known, e0012_null, runjob_test, s0018` - **no e0014/e0015 directory; neither pass has run** |
| 50 | R-0020 template comparison, R-0020:696-701 vs HEAD L835-L840 | 0 | text **matches verbatim**; template is internally unbalanced (2 `(`, 1 `)`), confirming the +1 is inherited from the ruling |
| 51 | R-0020:713-715 vs HEAD L791-L797 | 0 | X2 replacement text **matches verbatim**; `240` -> `128` present at L799 |

**J. What I did NOT do (explicit, for the record)**

No training, fitting, extraction, counting, feasibility pass or SPRT generation was run. No
holdout was read. No threshold, band, salt, cap or margin was changed. E-0013, E-00014,
E-00015, R-0019, R-0020 and every handoff were **not edited**. No H-#### status was changed.
HO-0005 and W-0003 were not opened or closed. E-0013 was **not** flipped. No `tools/` or
`src/` file was touched. All inspection was read-only; every artefact this review cites was
recomputed by me from the working tree or from git objects.

**Residual uncertainty (calibrated):**
- X4 (file does not end on a complete sentence) - **demonstrated**, by git diff plus two
  independent line reads.
- X5 (head-side deletion unrecorded) - **demonstrated**, by three-way string comparison.
- The `(E-00015 measures` head fragment is *substantively* correct to remove - **demonstrated**
  from R-0020's template, which opens with the same string.
- B5 s2's body is genuinely absent from the file - **demonstrated**. Whether it was lost,
  never written, or exists under another name elsewhere in the project - **unknown**, and I do
  not guess; `UNESTABLISHED` is the right epistemic label for the *body*, which is why the
  *heading* is withdrawn rather than filled.
- The +1 orphan's effect on meaning - **strongly supported** as nil, by reading the requirement
  in the main clause and finding it stated three times independently in the file.

**Not independently re-derived (out of scope by instruction, and I flag that I did not check
them rather than implying I did):** SHRINK as an engineering call, the KING-PST freeze
decision, `SUITE_TOLERANCE = 0.02` as a chosen value, the NONE per-game cap, and the X-1/X-2/X-3
branch design. I verified their **textual integrity and arithmetic** - that is what §4, §6 and §8
do - and took no view on their content.

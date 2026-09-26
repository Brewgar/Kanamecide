---
id: R-0022
type: review
reviewer: adversarial-reviewer
target: E-0013
kind: critique
status: COMPLETED
related: [E-0013, R-0019, R-0020, R-0021, S-0028, S-0029, S-0030, E-00014, E-00015, H-0013, d3ce887, ce845c5, f450976, fce355c]
example: false
created: 2026-09-26
---

# R-0022 — Independent verification of S-0030: all four R-0021 findings applied; the +10 residue does not block; one new non-blocking pointer defect (Y1) in the repair section's own X4 pointers

## Scope

Fresh adversarial-reviewer occupant. I wrote none of R-0019, R-0020, R-0021, S-0028, S-0029 or
S-0030 and I defer to none of them. Every claim below was recomputed by me from the working tree
and from git objects; where I quote a prior seat I checked it rather than adopting it.

**In scope (the work order):** the +10 stale-pointer residue (does it block; is a mechanical
rewrite safe; the +10 figure itself); X4's tail repair; seam 8's paren; the B5 s2 withdrawal and
the accuracy of its internal pointers; X5; the append-only record and its three boundaries; the
substance (ten seams, contingency table, F-U contiguity, X2 arithmetic, compliance greps);
B3/B4/B5 discharge; B1/B2/B6/B7 and DN1-DN10; E-00014/E-00015; and E-0013's next status.

**Out of scope, and not touched:** SHRINK, the KING-PST freeze, `SUITE_TOLERANCE = 0.02`, the
NONE per-game cap, and the X-1/X-2/X-3 branch design. R-0019/R-0020/R-0021 settled those. I ran
no training, fitting, extraction, counting, feasibility pass or SPRT generation, and read no
holdout. I did not edit E-0013, E-00014, E-00015, R-0019, R-0020, R-0021, any handoff, any
H-####, or any `tools/`/`src/` file. I did not flip E-0013. I did not open or close
HO-0005/W-0003.

**Method note.** `read_files` returned stale content for line-range requests on the large files
in this exchange, and `run_commands` reported `Command exited with code 1` on commands that
succeeded. Per the environment note I therefore dumped every line range to disk with
`python` (`encoding='utf-8', newline='\n'`) and read the FILE. Verdict line numbers are the
true E-0013 line numbers of `c23803f`, read from those dumps.

---

## 0. THE FIRST CHECK — the +10 stale-pointer residue

### 0a. I verified the +10 figure myself rather than accepting it

The B5 s2 withdrawal replaced **three** lines (d3ce887 L811 heading, L812 blank, L813 blank) with
**thirteen** (HEAD L811-L822 plus the blank L823). I confirmed this by diffing `d3ce887..HEAD`
with `difflib.SequenceMatcher` and enumerating every hunk: **H01 `replace d3ce887[811..812] ->
WORK[811..822]`, del=2 add=12**, which is the 3-lines-to-13-lines change (the matcher aligned one
of the three consumed lines differently than the prose count, but the net is **+10** and the
region is unambiguous).

**The shift map, measured, not assumed.** Every surviving `d3ce887` line was mapped to its `HEAD`
line. The maximal runs of constant shift are:

| d3ce887 range | shift | HEAD range |
|---|---|---|
| L1–L810 | **+0** | L1–L810 |
| L813–L1152 | **+10** | L823–L1162 |
| L1154–L1198 | +11 … +15 | (the R-0021 section's own in-place edits) |
| L1245–L1292 | +142 … +144 | (the 122-line R-0021 section inserted at HEAD L1265) |

**So the +10 figure is CORRECT, and it is exactly +10 for one contiguous band: d3ce887
L813–L1152 → HEAD L823–L1162.** Everything above d3ce887 L810 is untouched. Below that the shift
*grows* because the R-0021 section added 122 lines further down — which is precisely why a naive
"+10 everything" rewrite would be wrong outside the band.

### 0b. Does the residue BLOCK? **NO. I rule it NON-BLOCKING.**

Stated precisely, because the reasoning matters more than the verdict:

- **The normative text is unaffected.** Lines 1-428 are provably byte-identical (§5). Every
  gate, threshold, band, salt, cap, margin, branch and verdict rule lives at or above HEAD L1115
  or in the F-table at L1060-L1071 — all *above* the withdrawal at L811-L823, all with shift +0
  or −10 to their `d3ce887` antecedents, and all verified byte-identical to `d3ce887` (§6, §8).
  The residue moves where a *reader* looks; it does not change what the record *requires*.
- **The affected pointers are audit-trail metadata inside the repair section**, not operative
  contract text. I classified every `L<number>` citation in the addendum: of 52 pre-existing
  citations, the ones with targets inside the +10 band are the per-seam ledger's "after" column
  for seams 8/9/10, the X1-a paragraph's `L871`/`L841`, and the "other moves" paragraph's
  `L960-L995`, `L909-L944`, `L934-L935`, `L1106-L1114`. All are cross-references describing
  where text *is*, not rules about what to *do*.
- **The residue is disclosed, bounded, and given a stated read-rule.** HEAD L1373-L1386 states
  the offset, states the two exemptions (`old`-prefixed and `ce845c5`-relative references use a
  different numbering and are NOT shifted), names the affected families explicitly ("the per-seam
  ledger's 'after' column, the `L911-L944` follow-up list, the `L1106-L1114` narrative
  paragraph, the B6/B7 line ranges and so on"), and says re-deriving them is left to the
  re-critique. It even names the failure mode it is avoiding: "a reader who follows one lands on
  the wrong line."
- **The record's characterisation of the residue is honest and I checked it adversarially.** I
  tested the rule's own claim by content, seam by seam: for seams 1-7 the *as-written* pointer
  resolves to the seam's marker string and the +10 pointer does **not**; for seams 8/9/10 the
  as-written pointer fails and the +10 pointer resolves. That is exactly the pattern the rule
  predicts, so the rule is not merely asserted, it is true.

**I therefore rule (a): the residue does NOT block.** It is a disclosed, bounded, metadata-only
defect of the same class the record already named, and the normative contract is intact.
### 0c. Is a mechanical +10 rewrite safe? **NO — and this is the part I most need to be firm about.**

**A blanket `+10` rewrite is NOT safe, and it would corrupt the file.** Three independent reasons,
each verified:

1. **It would break the two exempted classes.** The ledger's columns 2 and 3 ("Head (before)",
   "Continuation (before)") are `ce845c5`-relative — the ledger's own preamble at L1162 says so —
   and they carry values like `L1064-L1067`, `L1051-L1052`, `L1022-L1026`, `L941-L944`. Adding 10
   to those produces numbers that resolve to unrelated text. Likewise the `old L871` / `old L960`
   / `old L808` references at L1187, L1195, L1215, L1216, L1217 are `ce845c5`-relative by
   construction.
2. **It is only correct inside one band.** The +10 shift holds *exactly* for d3ce887 L813-L1152.
   For targets at or after d3ce887 L1154 the shift is +11 to +15; at or after d3ce887 L1245 it is
   +142 to +144. A uniform +10 would be wrong for every one of those.
3. **It would not even fix the pointers that are actually wrong** (see Y1 below): `L1378` and
   `L1419-L1420` are *not* pre-repair numbers, so +10 makes them worse, not better.

**EXACT SCOPE to rewrite, so the next cycle is mechanical.** Rewrite **only** the *current-file*
pointers whose target lies in **d3ce887 L813–L1152** (i.e. HEAD L823–L1162), and only these,
by HEAD line:

| HEAD line holding the pointer | as written | correct |
|---|---|---|
| L1176 (ledger seam 8, "after") | `L834-L848` | `L844-L858` |
| L1177 (ledger seam 9, "after") | `L871-L875` | `L881-L885` |
| L1178 (ledger seam 10, "after") | `L899-L903` | `L909-L913` |
| L1187 | `L871` | `L881` |
| L1195 | `L871` | `L881` |
| L1195 | `L841` | `L851` |
| L1215 | `L960-L995` | `L970-L1005` |
| L1218 | `L909-L944` | `L919-L954` |
| L1218 | `L1045-L1049` | `L1055-L1059` |
| L1219 | `L1068-L1073` | `L1078-L1083` |
| L1221 | `L1106-L1114` | `L1117-L1125` — **caveat below; off-by-one, not +10** |
| L1221 | `L1073` | `L1083` |
| L1225 | `L934-L935` | `L944-L945` |
| L1169-L1178 (ledger cols 2-3) | `ce845c5` values | **DO NOT TOUCH** |
| L1187, L1195, L1215, L1216, L1217 | `old L…` values | **DO NOT TOUCH** |

**Caveat I must state, because a mechanical pass would get it wrong.** `L1221`'s `L1106-L1114`
is **not** a +10 case. The "The decision." paragraph is at **HEAD L1117-L1125**; the pointer is
off by one at *both* ends, and it was *already* off by one at `d3ce887` (where the paragraph is
L1107-L1115). So it is a **pre-existing off-by-one, not residue from the withdrawal**, and a
`+10` rewrite makes it *still* wrong (L1116-L1124). **The correct fix for that one pointer is
`L1117-L1125`, not `+10`.** This is the single strongest argument that the rewrite must be done
by inspection against content rather than by a uniform offset — which is exactly what the record
decided to leave to the re-critique, and I endorse that decision.

**Durable alternative if the next cycle prefers not to rewrite at all.** Keep the stated-offset
form but make it *unambiguous and self-checking*: the record already does the first half of this
(L1373-L1386 names the offset and the exemptions). I would add one sentence naming the band's
**end** as well as its start — that the +10 rule applies to targets in d3ce887 L813-L1152 only
and that targets below d3ce887 L1154 carry larger shifts — because a reader who applies +10 to a
d3ce887 L1200-range pointer will be wrong. A **content-anchored** form (citing the first ten
words of the target rather than a number) is the more durable fix and I would prefer it, but it
is a larger edit and is not required.

---

## 1. X4 — the tail

**CONFIRMED REJOINED, AND THE FILE'S TERMINAL SENTENCE IS NOT THE ORPHAN.**

- `fce355c` (== `d3ce887`) had the stranded head at **L1252** and the orphan at **L1293** — the
  file's last line, `move it, and per R-0020 the flip requires a fresh re-critique to confirm.`
- At `f450976` the two halves were **adjacent** (L1233/L1234) and `git diff --numstat f450976..fce355c`
  = `71 12`, with the insertion hunk `@@ -1232,3 +1251,43 @@` between them. Confirmed.
- **The repair MOVED the author's words; it did not retype them.** I tested this three ways:
  (i) the orphan string `move it, and per R-0020 the flip requires a fresh re-critique to confirm.`
  is a **verbatim substring** of the new line; (ii) `d3ce887 L1252 + " " + orphan == HEAD L1394`
  is **True** by string equality — the new line is the old head plus the old tail, nothing else;
  (iii) the difflib hunk is `H12 replace d3ce887[1252..1252] -> WORK[1394..1394]`, a one-line
  replacement, and `H14 delete d3ce887[1293..1293]` is the orphan's removal. **MOVED, not retyped.
  CONFIRMED.**
- **The file's last non-blank line is HEAD L1436**, `fresh re-critique, which this record does not
  pre-authorise.` — a **complete sentence**, and it is **not** the orphan. The orphan's text now
  lives inside the rejoined sentence at L1394, mid-file, where it belongs. The file ends with a
  newline and no trailing blank lines.
- The X4 entry at L1280-L1291 and the corrected verification-block sentence at L1410-L1412 both
  now describe the post-repair state.

**X4: DISCHARGED.**
## 2. Seam 8 — the one-character repair

- **The repair is exactly one character.** `d3ce887 L837` vs `HEAD L847`:
  `...is provisional on it. If the count` → `...is provisional on it). If the count`. Length 90 → 91,
  **delta +1**, and the two strings are identical apart from the inserted `)`. This is R-0021 §2(c)
  verbatim.
- **The block's paren delta is 0.** Over the B5/B6 correction-note block **HEAD L832-L858**:
  opens=5, closes=5, **delta 0**. The same block at `d3ce887` L822-L848 was opens=5, closes=4,
  **delta +1**. The orphan is closed.
- **Exactly ONE live `B6)` citation in normative text.** `mobility/tempo scope; B6)` occurs **4
  times file-wide**, at **L850 (LIVE), L1189, L1201, L1420** — and I confirm the reviewer's reading
  exactly: L850 is the live citation inside the joined seam-8 sentence; L1189 and L1201 are inside
  the X1-a paragraph *quoting* R-0020's template (`` `... (mobility/tempo scope; B6)` `` and
  `` the count of `mobility/tempo scope; B6)` at 0 ``); L1420 is inside the verification block
  *reporting the count*. Only L850 is operative text. Within the seam itself `B6)` = 1 and
  `it; B6)` = 0.
- **The `B6)` string occurs 16 times file-wide**, but the other 15 are all inside the repair
  narrative (L1187-L1201, L1272, L1324, L1366, L1417, L1420-L1421) or the BUCKET-2 bullet (L479,
  "the measurement half of B6"). None is a second citation of the seam-8 obligation.

**Does the record state the scope explicitly? YES.** The seam-8 sentence at L848-L851 reads:
*"If the count nevertheless arms the ladder, the fallback scope it would apply is not the
mobility/tempo sub-set named in E-0011 N1, and the sub-set is re-derived and re-registered under
its own critique before any use (mobility/tempo scope; B6)"* — the obligation is in the **main
clause**, in the indicative, with its object named, and the parenthetical is a **citation label**
for it. The scope is therefore explicit and unambiguous in normative text; the parenthetical is
labelling, not qualifying. The same obligation is stated three more times independently (L853,
L992-L994, L1049-L1051). **R-0021's "defective as typography, correct as normative text" ruling
was right, and S-0030's fix removed the typographic half without touching the normative half.**

**Seam 8: DISCHARGED.**

## 3. B5 s2 — the withdrawal

- **The heading is WITHDRAWN with R-0021's text.** HEAD L811-L822 is R-0021 §3's paragraph verbatim
  (I compared the wording: "WITHDRAWN 2026-09-26, body never established", "`ce845c5`, L684 heading
  with L685-L686 blank", "withdrawn rather than filled", "**No normative content is lost by this
  withdrawal and none is invented to replace it**", "`k4-k3 = -3.7` / `k6-k5 = -11.5`",
  "F-U4", "closes the slot; it re-opens no decision and changes no gate"). S-0030 re-derived the
  two pointers R-0021 supplied (R-0021 wrote `L822-L848` and `L1032-L1041`; the record reads
  `L832-L858` and `L1042-L1051`) because the withdrawal itself moved them. **Correct.**
- **Nothing was filled.** L811-L822 is one paragraph of withdrawal prose; there is no quoted
  normative block beneath it, and L824 is B5 s3's heading. Confirmed by reading L823-L831.
- **The two stale pointers now point at the withdrawal.**
  - The observation note at **L1235-L1241** now reads "the heading itself has been **withdrawn,
    not filled** (see the withdrawal paragraph at L811 and the R-0021 entry below). Nothing was
    relocated; no body was invented." — **CONFIRMED**, and its stale `ce845c5` location claim is
    corrected to the post-repair geometry.
  - The `B5 s2 (pre-existing)` disposition row at **L976** now reads "**WITHDRAWN 2026-09-26 under
    R-0021 - not moved, not filled, not invented**" and its closing sentence is "This row now
    points at the withdrawal." — **CONFIRMED**.
- **Every pointer inside the withdrawal text is ACCURATE as of HEAD.** I read each target line:
  - "B5 sentence 3" → **L824** is B5 s3's heading. ✓
  - "its colon" / "preamble ends in a colon" → **L830** ends `error, and a follow-up obligation is filed against E-0013's close-out:` — **ends in a colon. ✓**
  - "the L832-L858 block" → **L832** is the opening `> "**Correction note (researcher-architect, 2026-09-26)...` and **L858** is the closing `> ruling rather than a quiet edit."` — **exactly the quoted correction note. ✓**
  - "B6 s1" → **L1026** is `**B6 sentence 1 (the count pass rule and the relabelling...`. ✓
  - "the L1042-L1051 block" → **L1042** is `> "**Consequence-ladder citation corrected (binding only if the ladder arms).**...` and **L1051** is `> its own critique before it is applied."` — **exactly B6 s1's second quoted block. ✓**
  - "`ce845c5`, L684 heading with L685-L686 blank" → I dumped `ce845c5` L684-L687 and confirmed
    the same hole pre-existed. ✓

**B5 s2: DISCHARGED.** The slot is closed, nothing was invented, and every pointer resolves.
## 4. X5 — the unrecorded head-side deletion

- **Recorded.** HEAD L1304-L1315 is the X5 entry: it names `ce845c5` **L707**, quotes the head as
  `...i.e. 2.5x headroom (E-00015 measures`, states S-0028 deleted those four words and **did not
  record doing so**, states the count of `(E-00015 measures` went 1 → 2, and states the deletion was
  "SUBSTANTIVELY CORRECT AND NECESSARY" with the reason. **CONFIRMED recorded.**
- **The two absolute claims are QUALIFIED, not deleted.** L1163-L1164 (was "Every continuation was
  MOVED byte-for-byte, not retyped") now reads "Every **CONTINUATION** was MOVED byte-for-byte,
  not retyped **- the one recorded exception is the seam-8 head fragment, see the X5 entry below**".
  L1213 (was "nothing deleted, nothing retyped") now reads "nothing deleted, nothing retyped,
  **with ONE recorded exception**". **CONFIRMED — qualified in place.**
- **S-0029's reason is recorded as WITHDRAWN AS WRONG, in R-0021's favour.** Two places:
  L1209-L1211 ("S-0029's reason for leaving it … is **withdrawn as WRONG**: the template bounds the
  span, so that closer is not an invented token. R-0021 ruled against that reason; this seat
  concurs.") and L1326-L1332 ("**That sentence is withdrawn as WRONG and is struck in place above.**
  … **The disagreement is on the record and is resolved in favour of the reviewer.**"). The old
  wording is gone — I searched the whole file for "is now left unclosed" and it does **not** occur
  (the sentence now reads "was left unclosed", correctly in the past tense). **CONFIRMED.**

**X5: DISCHARGED.**

---

## 5. The append-only record

### 5a. The L1-428 SHA-256 pair, recomputed by me

I recomputed both sides from two directions, over lines 1..428 **including line terminators**,
UTF-8:

- `git show ce845c5:<path>` lines 1-428 → `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`, **22,270 bytes**
- working file (HEAD `c23803f`) lines 1-428 → `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`, **22,270 bytes**

**Equal. I also compared the two ranges as Python lists: `cur[0:428] == ce[0:428]` is `True`.**
The record's stated hash and byte count are **correct in every particular**.

### 5b. The three boundaries — I measured all of them

| boundary | record's claim (HEAD) | my measurement | match |
|---|---|---|---|
| `4478c3a..HEAD` | 1011 insertions, 0 deletions | **1011 / 0** | ✓ |
| `ce845c5..HEAD` | 493 insertions, 130 deletions | **493 / 130** | ✓ |
| `f450976..HEAD` | 231 insertions, 29 deletions | **231 / 29** | ✓ |

and the historical `4478c3a..ce845c5` = **648 / 0** (the `648 additions / 0 deletions` figure),
`ce845c5..d3ce887` = **347 / 127** (R-0021's HEAD column), `f450976..d3ce887` = **71 / 12**.
**Every figure in the record's table is correct**, including the R-0021-HEAD column.

### 5c. The `288/127` figure — the record is right, and so is the correction's attribution

I measured `ce845c5..f450976` = **288 insertions, 127 deletions**. So **`288/127` is the
`ce845c5..f450976` boundary (S-0028's pass), and it was in circulation mislabelled as
`ce845c5..HEAD`.** The record says exactly this at L1357-L1360: *"The `288/127` figure in
circulation was the `f450976` boundary mislabelled as `ce845c5`, and that correction is R-0021's,
not this seat's."* **CONFIRMED on both counts** — the mislabelling is correctly diagnosed and
correctly attributed to R-0021, not claimed for itself.

**One correction to the review brief, as R-0021 also made:** the brief describes `288/127` as
"the f450976 boundary mislabelled as ce845c5". The precise statement is that `288/127` is
`ce845c5..f450976` — the *baseline* was right and the *upper* ref was wrong. The record's own
wording ("the `f450976` boundary mislabelled as `ce845c5`") is loose in the same way, but its
three-row table removes all ambiguity because **each row names its boundary explicitly**, which is
the correct fix and which the record has made. I record this as a wording nit, not a finding.

### 5d. Does the record lead with the strongest true statement? **YES.**

The table at L1351-L1355 leads with the `4478c3a..HEAD` row and labels it: *"**the addendum has
NEVER had a deletion against the original pre-registration** - the strongest true statement, and
the one that discharges the append-only obligation outright"*. That is the correct leading claim,
it is true (1011/0, measured), and it is stated before the weaker `ce845c5` row. **The record
leads with it. CONFIRMED.**

The characterisation is also honest in the way that matters: the same section states the boundary
between the protected side (L1-L428, hash-proved, never to be edited in place) and the
review-licensed side (L429+), and it states the 130 deletions as "the visible, itemised cost of
the review-licensed repairs". It neither hides the deletions nor overstates what was protected.
---

## 6. THE SUBSTANCE — re-verified, not accepted

### 6a. The ten seams

I read each joined sentence as prose and checked each block's paren delta. All ten are joined as
contiguous runs inside their own finding's sections, and **nine of ten are byte-identical to
`d3ce887`** (i.e. the three repair passes did not touch them); seam 8 differs by exactly the one
`)` that R-0021 required:

| seam | HEAD lines | reads as | paren delta | identical to d3ce887 |
|---|---|---|---|---|
| 1 | L471-L475 | the three-bucket list is one list | 0 | ✓ |
| 2 | L515-L517 | B1's self-collision diagnosis | 0 | ✓ |
| 3 | L542-L543 | the UCI-surface reversal condition | 0 | ✓ |
| 4 | L593-L598 | **the `S*` conclusion has its object again** | 0 | ✓ |
| 5 | L639-L649 | **the `LOSS_MARGIN` rule is one sentence** | 0 | ✓ |
| 6 | L743-L747 | **the freeze anchor is unsevered** | 0 | ✓ |
| 7 | L765-L774 | **the `SUITE_TOLERANCE` derivation is whole** | 0 | ✓ |
| 8 | L844-L858 | the ladder's DISARMED status is provisional, and reasoned | 0 | one `)` (§2) |
| 9 | L881-L885 | the ~27k refutation's consequence is attached | 0 | ✓ |
| 10 | L909-L913 | DN10's explicit-dependency sentence is one sentence | 0 | ✓ |

(The L834/L871/L899 figures in the ledger's "after" column are the stale ones; the *actual*
post-withdrawal locations are +10. See §0c. That is the disclosed residue, not a seam defect.)

**The four normatively critical ones, read individually:**
- **`S*` conclusion (L585-L598):** the object is present at L594 — "conversely, a strength
  comparison against a stage-5 opponent would leave `tempo` inert, which is one of the reasons the
  strength comparison is deferred rather than run here (cost item 1 above)". Parses.
- **`LOSS_MARGIN` rule (L635-L649):** subject present at L645 — `LOSS_MARGIN := max(0.002, 0.5 *
  delta_star)`, "so the margin can only be made more conservative than 0.002, never less" — and
  the consequence at L646-L649, ending "never FAIL, and never 'no achievement = FAIL'." One
  sentence, parses.
- **freeze anchor (L737-L747):** the nine deferred values, the "SAME pre-fit commit as the
  game-split map" clause, the holdout prohibition and the tripwire extension are all present in
  one run. This is the instrument the twelve F-items close against.
- **`SUITE_TOLERANCE` derivation (L762-L774):** the binomial SE bound `0.5 / sqrt(200) = 0.0354`
  (I recompute: 0.03536 ✓) and the "0.6x the worst-case paired binomial SE" placement
  (0.02/0.0354 = 0.565 ≈ 0.6x ✓) are in the same sentence as the value. Whole.

### 6b. Contingency table under B3 s3 — CONFIRMED

B3 s3's announcement is at **L677-L680** and ends in a colon; the table begins immediately at
**L682** and the X-1/X-2/X-3 branches are at **L687, L693, L707**, closing at L717. **No blank
gap, no intervening text.** Byte-identical to `d3ce887`. Exhaustive and mutually exclusive on
(`s_d_inner`, `delta_star`), with no fourth branch and no discretion left to the session that
reads the number.

### 6c. F-U1..F-U6 contiguous — CONFIRMED

The six bullets start at **L919, L926, L936, L942, L946, L952** — a clean 4-line cadence with no
gap, and **F-U3's stranded `Owner: researcher-architect. Due: at E-0013 close-out.` is present at
L941**, which was the specific break S-0028 repaired. The list runs L919-L954 with no intervening
table. Byte-identical to `d3ce887`.

### 6d. X2's arithmetic — every figure recomputed by me

| quantity | my computation | record's figure | match |
|---|---|---|---|
| free scalars | 10 + 640 + 20 + 2 + 10 + 1 = **683** | 683 | ✓ |
| positions/param overall | 76,587 / 683 = **112.13** | ~112 | ✓ |
| train-side | 0.8 × 76,587 = 61,269.6; / 683 = **89.71** | ~89 | ✓ |
| needed at 500/param | 500 × 683 = **341,500** | 341,500 | ✓ |
| shortfall factor | 341,500 / 76,587 = **4.4590** | ~4.5x body / 4.46x table | ✓ both |
| unfrozen ratio | (683 + 128) = 811; 76,587 / 811 = **94.44** | 94.44 → 112 | ✓ |
| KING-PST count | 2 tables × 64 = **128**; 64 under `s ^ 56` | 128 (or 64), "not 240" | ✓ |

**The component breakdown also checks out against the free-parameter list at L166-L183:** five
non-king `mg_value`/`eg_value` pairs = 10; five non-king PST tables × 2 (mg/eg) × 64 = 640;
`doubled_pawn`/`isolated_pawn` mg+eg = 4 plus `passed_pawn[8]` mg+eg = 16 → 20; `mobility` = 2;
`bishop_pair`/`open_file`/`semi_open_file`/`seventh_rank` mg+eg = 8 plus `king_shield_mg` and
`king_center_eg` = 2 → 10; `tempo` = 1. **Total 683.** The KING PSTs being frozen is exactly why
the two 64-entry tables (128 scalars) are excluded.

**"X2's arithmetic is correct in every figure. CONFIRMED."**
### 6e. No surviving compliance claim — I grepped, I did not take the table's word

| pattern | hits | my ruling |
|---|---|---|
| `defensible` | L809, L975, L1146 | all three are inside an **explicit refutation** — L809 "was FALSE and has been DELETED and REPLACED"; L975 "That is false:"; L1146 "is false by a factor of ~4.46". **Records the limitation. ✓** |
| `>= 500` | L792, L809, L975, L1146 | L792 is the **negation**: "It does NOT, however, bring the fitted-parameter count within E-0011 N1's '>= 500 positions/parameter' standard, **and this record does not claim it does**". The other three are refutations. **✓** |
| `meets the standard` / `reaches the standard` / `satisfies the standard` | **0** | **✓** |
| `240` | L42, L799, L809, L893, L894, L975, L1062, L1147, L1148, L1230, L1232, L1413 | L42/L893/L894 are the E-0010 ladder's `N=240` (an unrelated quantity; DN1 records the k1-k5/k6 distinction). L799/L809/L975/L1147/L1148/L1230/L1413 are the **correction** to 128 or statements that 240 reads 128. **L1062 `(240 params)` is R-0019's own F3 item label, left as quoted, and L809 and L1232 both say so explicitly.** |
| `(240 params)` | L809, L1062 | both explicitly identified as R-0019's quoted item label. **✓** |

**No surviving instance anywhere in the file asserts compliance. Every one records the
limitation or refutes the claim. CONFIRMED — I reach this independently of the disposition table.**

### 6f. Additional arithmetic I checked that nobody had claimed

- `76,587 / 30,000 = 2.553` → the "2.5x headroom" claim is **correct**.
- `76,593 − 6 = 76,587` → the upper band is **exact**. And I confirmed the "single degenerate
  game" premise against the dataset: exactly **1** game has `end == "mate"` with `len(san) <= 6`.
- `1.302% × 76,593 = 997.2` → the "~997 projected cross-game FEN duplicates" is **correct**, and
  the lower band `75,600` is the stated rounding of 75,596. The record presents this as a **band
  with its arithmetic shown**, not as a point. Honest.
- **`903 of 1,000 verified games end in `mate`` — I read the dataset.** `m0_audit/e0011/games.jsonl`
  has 1,000 rows and the `end` histogram is `{mate: 903, repetition: 41, draw-material: 41,
  plycap: 14, stalemate: 1}`. **The 903 figure is CONFIRMED against the artifact, not copied.**
- `k4 − k3 = 100.8 − 104.5 = −3.7` and `k6 − k5 = 116.1 − 127.6 = −11.5` → **both exact**, and both
  match the E-0010 ladder quoted in the Baseline at L42-L44.
- `abs(20260926 − 20260924) × 1,000,003 = 2 × 1,000,003 = 2,000,006` → the F10 salt-distance
  citation is **correct**, and `2,000,006 ≥ 1,000,003 > 1,999` as claimed.
- `0.5 / sqrt(200) = 0.03536` → the SUITE_TOLERANCE SE bound is **correct**.
- **One thing I checked and am NOT raising as a finding:** the `s_d <= 0.0101` threshold is
  derived from a multiplier of 2.8016, whereas `t_{0.975,199} = 1.9720`. The stated multiplier is
  **larger** than the true 97.5% quantile, so the implied ceiling is **stricter** (0.0101 rather
  than 0.01434) — it can only make "decidable" harder, never easier. That is conservative, not
  permissive, and the figure is R-0019's own quoted text inherited verbatim, not introduced by any
  repair pass. **No finding.**

---

## 7. B3, B4, B5 — discharge

- **B3: DISCHARGED.** Effective N corrected to games and the decidability condition `s_d <= 0.0101`
  stated (L658-L666); the unbounded "for any realistic loss variance" clause superseded; the
  anti-apathetic clause rescoped to QUALITY (L670-L675); the Power-section sentence that converted
  a power failure into an apathetic rejection quoted and superseded verbatim (L1087-L1099); and
  the contingency decided NOW, exhaustively, immediately under its own announcement (L682-L717).
  The residual is that the contingency's **input** is E-00014's and does not exist — BUCKET 2 by
  design, honestly labelled, not a defect. **R-0021's DISCHARGE holds.**
- **B4: DISCHARGED.** Q-FIT closed by value with SPSA withdrawn (L725-L732); the substitution path
  closed and the per-game cap ruled NONE (L1076-L1085); `SUITE_TOLERANCE = 0.02` pinned as a number
  with its derivation (L752-L774); the single pre-fit commit as the freeze anchor, unsevered
  (L737-L747). **All twelve F-items close against that restored anchor — I re-read it and checked
  each: F1 value, F2 pointer, F3 value, F4 value+pointer, F5 pointer, F6 pointer+value, F7 value,
  F8 value, F9 value, F10 value (arithmetic re-derived, correct), F11 pointer, F12 value. No F-item
  depends on a severed sentence. R-0021's DISCHARGE holds.**
- **B5: DISCHARGED.** R-0021 held B5 partial for exactly two text defects inside B5's own section:
  the +1 orphan (§2) and the empty s2 slot (§3). **Both are now closed** — the paren delta is 0 and
  the slot is withdrawn with R-0021's own text, nothing filled. The substantive half was already
  done: the freeze decision at L788-L807, the false rationale gone, the arithmetic correct, and
  the historical record protected by a dated correction note plus F-U4 rather than a retroactive
  edit. **There is no remaining B5 defect. I rule B5 DISCHARGED — the last of R-0021's three
  partials is now closed.**

**I hold NONE of B3/B4/B5 partial. No missing sentence is required for any of them.**
---

## 8. B1, B2, B6, B7, DN1-DN10 — undisturbed

I verified non-disturbance mechanically: for each block I mapped every HEAD line back to its
`d3ce887` antecedent and compared the text.

- **B1 — undisturbed.** S-1's supersession mechanism (L552-L570), the N1 coefficient-regeneration
  note (L572-L581), `S* = 6` with its consequence (L585-L598), cost items 1-4 contiguous
  (L521-L548), and conjunct (e)'s re-designation (L1104-L1115): all **byte-identical to `d3ce887`**.
  The three repair passes touched nothing in B1.
- **B2 — undisturbed.** Colour frame (L606-L615), the unmeasured-gain acknowledgement (L620-L630)
  and the E-00014 delegation with the `LOSS_MARGIN := max(0.002, 0.5*delta_star)` rule (L635-L649):
  **byte-identical**.
- **B6 — undisturbed.** The count-pass rule and 76,593 relabelling (L1029-L1040), the band
  (L862-L873), the ~27k refutation with its scope-changing consequence (L877-L885) and the
  scope-floor rule (L987-L998): **byte-identical**.
- **B7 — undisturbed.** Q-0006 gate 7 quoted as authority and the verification-handoff rule with
  F-U5 present (L1006-L1020): **byte-identical**.
- **DN1-DN10 — undisturbed, all ten dispositioned.** The table (L893-L902) has ten rows, DN1-DN10,
  and DN10's explicit-dependency sentence (L906-L913) is whole: **byte-identical**.

---

## 9. E-00014 / E-00015 — have not run

**They have NOT run. Stated plainly, and verified three ways rather than assumed:**

- Front matter, read from disk: E-00014 `status: PENDING`, `result: null`, `completed: null`,
  `owner: systems-researcher`. E-00015 `status: PENDING`, `result: null`, `completed: null`,
  `owner: systems-researcher`. (X3's owners are set on both — confirmed.)
- `git log --all -- <both paths>` returns only `ce845c5` (filing) and `f450976` (a touch during
  S-0028). **No commit after `f450976` touches either record**, so neither has been run, completed
  or edited since.
- `research.py status --brief` reports **Experiments running: 0**, Experiments pending: 6.

**Therefore the honesty questions have nothing to bite on, and I rule them prospectively:**

- **No holdout read** — there is none to report, and the record forbids one (E-00014 is explicitly
  TRAIN-only, and E-0013 states "does not read the holdout to obtain either quantity").
- **No threshold, band, salt or split map moved after a number appeared** — because no number
  exists. I checked the places it could hide: `LOSS_MARGIN` is still `0.002` (L275) and is only
  ever made *more* conservative by `max(0.002, 0.5 * delta_star)` (L645) — a floor, not a ceiling.
  `SUITE_TOLERANCE` is still `0.02`. The 30,000 floor is still 30,000 and is applied to the
  **TRAIN-side** count. `SPLIT_SALT` is still `20260926`.
- **Which branch the numbers select: I cannot state it, and that is the correct answer.** The
  X-1/X-2/X-3 branch is a function of (`s_d_inner`, `delta_star`), neither of which has been
  measured. What I *can* certify is that the branch will be **selected by the measurement rather
  than asserted**, because the three branches are exhaustive, mutually exclusive, and assigned by
  name **before** E-00014 runs, with no fourth branch and no discretion left to whoever reads the
  number. **I certify that the record is built so that consumption will have to be honest. I do
  not and cannot certify honest consumption of numbers that do not exist.**

**Rule on E-0013's status given this: E-0013 stays `PENDING`,** and the two measurement passes are
a *precondition for the run's conclusions*, not a reason to advance the record's authorisation.

---

## 10. E-0013's next status

**E-0013 remains `status: PENDING`. I do not flip it and I do not pre-authorise the flip.**

**Is everything above clean? Almost — with one exception I must name, below.** Every one of
R-0021's four required repairs is applied and verified, the substance is sound, B3/B4/B5 are all
discharged, the append-only original is provably intact, and the +10 residue is disclosed and
non-blocking.

**Is the ONLY remaining precondition the two measurement passes? NO — not quite, and this is the
substance of my verdict.** There is one further item, and it is small, mechanical, and in the same
class as the residue I just declined to block:
> **Y1 (NEW, NON-BLOCKING) — the R-0021 section's own X4 pointers do not resolve.** The repair
> section's X4 entry and the verification block cite **`L1378`** three times (L1282, L1287, L1411)
> for the stranded head and the rejoined sentence, and **`L1419-L1420`** once (L1300) for the
> redundant restatement. None of these resolve. HEAD L1378 is *"inside the `B5 s2` disposition
> row, inside the observation note above, inside the"* — not the head. The stranded head and the
> rejoined sentence are at **HEAD L1394**. HEAD L1419-L1420 is the seam-8 count paragraph — not the
> redundant restatement, which is at **HEAD L1432-L1436**. `d3ce887` has only 1,293 lines, so
> `L1378` and `L1419` never existed in the pre-repair file either; and applying +10 makes both
> *worse* (→ L1388, and → L1429-L1430), so **Y1 is not residue and the +10 rule does not cover
> it.** These are pointers the repair wrote *about itself*, in the very section whose purpose is
> to make every move auditable, and the file elsewhere (L1377-L1379) claims its own
> cross-references "have been re-derived to the post-withdrawal numbering". That claim is **false
> for these four**.

**Why I rule Y1 NON-BLOCKING rather than blocking**, stated so the next cycle can overrule me if
it disagrees: the four claims the pointers support are all **true** — the head *was* stranded, the
words *were* moved, the restatement *does* stand, and the file's terminal sentence *is* that
restatement. A reader who follows `L1378` lands on the wrong line, which is the residue's
failure mode, but nothing normative turns on it, no gate moves, and the substance is independently
verifiable (as I verified it) from the two halves' text. It is a **stale pointer in audit-trail
metadata** — exactly the class §0 rules non-blocking.

**The exact missing text, so the next cycle is mechanical.** Four pointer substitutions, all
current-file, no wording chosen by me beyond the numbers:

- **L1282:** `L1378` → `L1394`
- **L1287:** `L1378` → `L1394`
- **L1300:** `L1419-L1420` → `L1432-L1436`
- **L1411:** `L1378` → `L1394`

And, if the next cycle elects to clear the §0c residue at the same time, the twelve-row table in
§0c is the scope — **with the `L1106-L1114 → L1117-L1125` correction, not `+10`.**

**The exact condition under which E-0013 may move PENDING → RUNNING.** I decline to pre-authorise
the flip, as R-0020 and R-0021 both did, and for the same reason: the record's own re-critique gate
at L1363-L1371 requires a *fresh* adversarial-reviewer line-range confirmation, and I am confirming
it now. Against that gate:

- (i) the file ends on a complete sentence — **CONFIRMED** (L1436)
- (ii) the seam-8 paren is closed and exactly one `B6)` remains — **CONFIRMED** (delta 0; 1 live)
- (iii) the B5 s2 slot is withdrawn rather than filled — **CONFIRMED**
- (iv) every deletion made in any repair pass is itemised — **CONFIRMED** (X5's head-side deletion,
  the X1-a tail-side deletion, and X4's orphan deletion are all named)
- (v) lines 1-428 still hash to `b04fd5a4…00ce6` on both sides — **CONFIRMED** by my own recomputation

**So: five of five gate conditions are met by me, and E-0013's *textual* preconditions are now
complete.** What remains is (a) the one-line Y1 pointer fix above, which I judge non-blocking but
which I would not leave in a record whose whole argument is that stale pointers mislead, and
(b) the two measurement passes, which are **inputs to the experiment, not preconditions of its
authorisation.** E-0013 may go RUNNING on the strength of this review plus the Y1 fix; the
measurement passes must complete **during** the run, in the order the record mandates (E-00015
count-only before any fitter; E-00014 train-only before the holdout is read), not before it.

**I am not flipping E-0013. That is the orchestrator's and the owner's call, on this record.**

---

## NEW FINDING SUMMARY

| id | severity | finding | disposition |
|---|---|---|---|
| **Y1** | **NON-BLOCKING** | The R-0021 section's own X4 pointers `L1378` (×3, at L1282/L1287/L1411) and `L1419-L1420` (at L1300) do not resolve. The head/rejoined sentence is at **L1394**; the redundant restatement at **L1432-L1436**. Not covered by the +10 rule (not residue; +10 makes it worse; neither number existed pre-repair). | Four pointer substitutions; exact text given. |

No blocking findings. No missing sentences for B3, B4 or B5.

---

## Date
2026-09-26

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns.
---

## Verification Block (kind: critique — evidence about the target, recorded per the work order)

**Environment note.** `run_commands` reports `Command exited with code 1` on commands that
succeed; every command below was redirected with `| Out-File -Encoding utf8 <file>` and the FILE
was read. All line numbers come from numbered Python dumps (`encoding='utf-8', newline='\n'`),
not from `read_files` line ranges.

**A. Repo state**

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git pull --ff-only` | 0 | `Already up to date.` |
| 2 | `git status -sb` | 0 | `## master...origin/master` (clean) |
| 3 | `git rev-parse HEAD` / `origin/master` | 0 | both `c23803f0984aefcf7f7bb63ef72ea665994fe907` |
| 4 | `git log --oneline -20` | 0 | HEAD = `c23803f` S-0030; then `d3ce887` R-0021, `fce355c` S-0029, `f450976` S-0028 |

**B. The +10 figure, measured**

| # | Command | Exit | Observed |
|---|---|---|---|
| 5 | difflib opcodes on `d3ce887..HEAD` for the E-0013 path | 0 | **14 hunks**; H01 = `replace d3ce887[811..812] -> WORK[811..822]` del=2 add=12 (**the 3→13 change, net +10**); H12 = `replace d3ce887[1252] -> WORK[1394]`; H14 = `delete d3ce887[1293]` |
| 6 | Shift map over all surviving `d3ce887` lines | 0 | maximal runs: `L1-L810` **+0**; `L813-L1152` **+10** → `L823-L1162`; `L1154+` +11…+15; `L1245+` +142…+144. Distinct shifts: `{0,10,11,14,15,18,20,142,144}` |
| 7 | Dump `d3ce887` L808-L830 and HEAD L808-L845 | 0 | `d3ce887` L811 = heading, L812/L813 = `''`, L814 = B5 s3 heading. HEAD L811-L822 = withdrawal, L823 = `''`, L824 = B5 s3 heading. **3 → 13, +10.** |
| 8 | Content test of the rule, per seam | 0 | seams 1-7: as-written pointer resolves, +10 does **not**; seams 8/9/10: as-written fails, +10 resolves. **The rule is true, not just asserted.** |

**C. X4 and the tail**

| # | Command | Exit | Observed |
|---|---|---|---|
| 9 | `git diff --numstat f450976..fce355c -- <path>` | 0 | `71  12` |
| 10 | `git diff -U0 f450976..fce355c -- <path>` hunk headers | 0 | `@@ -841 +841 @@`, `@@ -965,0 +966 @@`, `@@ -1168,11 +1169,29 @@` — insertions only, between the two halves |
| 11 | `f450976` L1233/L1234 vs `fce355c` L1252/L1293 | 0 | at `f450976` **adjacent**; at `fce355c` **41 lines apart** |
| 12 | String test: `d3ce887 L1252 + " " + orphan == HEAD L1394` | 0 | **True** — head + tail, nothing else. **MOVED, not retyped.** |
| 13 | Substring test: orphan in HEAD L1394 | 0 | **True** |
| 14 | Last non-blank line of HEAD | 0 | **L1436** `fresh re-critique, which this record does not pre-authorise.` — complete sentence, **not the orphan**; file ends with newline, 0 trailing blanks |

**D. Seam 8**

| # | Command | Exit | Observed |
|---|---|---|---|
| 15 | `d3ce887` L837 vs HEAD L847 | 0 | length 90 → 91, **delta +1**; identical apart from the inserted `)` |
| 16 | Paren count HEAD L832-L858 | 0 | opens=5, closes=5, **delta 0** (was +1 at `d3ce887` L822-L848) |
| 17 | `mobility/tempo scope; B6)` file-wide | 0 | **4** at L850, L1189, L1201, L1420 — **1 live (L850)**, 3 quoted/reported |
| 18 | `B6)` file-wide; `it; B6)` | 0 | 16 occurrences of `B6)`, all others in narrative or the BUCKET-2 bullet; `it; B6)` = **0** |
**E. B5 s2**

| # | Command | Exit | Observed |
|---|---|---|---|
| 19 | Read HEAD L811-L822 | 0 | R-0021 §3's paragraph verbatim; **nothing filled**; L824 = B5 s3 heading |
| 20 | Read each pointer target | 0 | **L824** = B5 s3 heading ✓; **L830** ends `:` ✓; **L832**/…/**L858** = exactly the quoted correction note ✓; **L1026** = B6 s1 heading ✓; **L1042**/…/**L1051** = exactly B6 s1's 2nd quoted block ✓ |
| 21 | `git show ce845c5` L684-L687 | 0 | heading L684, L685/L686 `''`, L687 = B5 s3 — **pre-existing hole confirmed** |
| 22 | Read HEAD L1235-L1241 and L976 | 0 | both now point at the withdrawal ✓ |

**F. X5**

| # | Command | Exit | Observed |
|---|---|---|---|
| 23 | Read HEAD L1304-L1315 | 0 | head-side `(E-00015 measures` deletion at `ce845c5` L707 **recorded**, with reason |
| 24 | Read HEAD L1163-L1164, L1213 | 0 | both claims **qualified in place** ("CONTINUATION", "with ONE recorded exception") |
| 25 | Grep `withdrawn as WRONG`; grep `is now left unclosed` | 0 | 2 hits (L1210, L1328) both in R-0021's favour; `is now left unclosed` = **0** |

**G. Append-only and boundaries**

| # | Command | Exit | Observed |
|---|---|---|---|
| 26 | SHA-256 of lines 1-428 from `ce845c5` and from HEAD | 0 | both `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`, **22,270 bytes** |
| 27 | Python list compare `cur[0:428] == ce[0:428]` | 0 | **True** |
| 28 | `git diff --numstat <base>..HEAD` for 5 bases | 0 | `4478c3a`→**1011/0**; `ce845c5`→**493/130**; `f450976`→**231/29**; `fce355c`→165/22; `d3ce887`→165/22 — **all three record figures confirmed** |
| 29 | `git diff --numstat` for 7 boundary pairs | 0 | `4478c3a:ce845c5`=**648/0**; `ce845c5:f450976`=**288/127**; `f450976:fce355c`=71/12; `ce845c5:d3ce887`=347/127 — **the `288/127` attribution confirmed** |

**H. Substance**

| # | Command | Exit | Observed |
|---|---|---|---|
| 30 | Paren delta + byte-identity per seam, 1-10 | 0 | all ten contiguous; deltas all **0**; nine of ten **byte-identical to `d3ce887`**, seam 8 differing by exactly the one `)` |
| 31 | Read the four critical seams in full | 0 | `S*` object at L594; `LOSS_MARGIN` subject at L645 and consequence L646-L649; freeze anchor whole L737-L747; SUITE_TOLERANCE derivation L762-L774 with 0.0354 and 0.6x |
| 32 | Contingency table position | 0 | announcement L677-L680 (ends `:`), table L682-L717, X-1/X-2/X-3 at L687/L693/L707 — **immediately under, no gap** |
| 33 | F-U bullet starts | 0 | L919, L926, L936, L942, L946, L952; F-U3's `Owner:` line present at L941 — **contiguous, no gap** |
| 34 | Recompute X2's arithmetic | 0 | 683 / 112.13 / 89.71 / 341,500 / 4.4590 / 94.44 / 128 — **every figure matches** |
| 35 | Grep `defensible`, `>= 500`, `meets the standard`, `240`, `(240 params)` | 0 | 3 / 4 / **0** / 12 / 2 — **every hit a refutation, a correction, or R-0019's quoted label. None asserts compliance.** |
| 36 | Read `m0_audit/e0011/games.jsonl` | 0 | 1,000 rows; `end` histogram `{mate:903, repetition:41, draw-material:41, plycap:14, stalemate:1}` — **B2 s2a's "903" confirmed against the artifact**; exactly **1** degenerate game, confirming the 76,587 upper bound |
| 37 | `t_{0.975,199}` by bisection on the Student-t CDF | 0 | 1.9720 vs the record's 2.8016 → the stated ceiling is **stricter**; conservative; R-0019's own inherited figure — **no finding** |

**I. Y1 (new finding)**

| # | Command | Exit | Observed |
|---|---|---|---|
| 38 | Read HEAD L1280-L1302, L1410-L1412 | 0 | four bad pointers: `L1378`×3 (L1282, L1287, L1411), `L1419-L1420` (L1300) |
| 39 | Resolve each | 0 | HEAD **L1378** = *"inside the `B5 s2` disposition row…"* (wrong); **L1394** = the rejoined sentence (**correct**); **L1419-L1420** = the seam-8 count paragraph (wrong); **L1432-L1436** = the redundant restatement (**correct**) |
| 40 | `d3ce887` L1378 / L1419 | 0 | `<no such line; 1293 lines>` — **neither number ever existed pre-repair** |
| 41 | Apply +10 to both | 0 | → L1388 and L1429-L1430, both also wrong — **Y1 is not residue** |
| 42 | File-wide grep for `L1378` / `L1419` | 0 | 4 hits total, all listed; no other occurrence |

**J. Records and status**

| # | Command | Exit | Observed |
|---|---|---|---|
| 43 | `research.py status --brief` | 0 | Experiments **running: 0**, pending: 6, sessions: 30 |
| 44 | `research.py validate` | 0 | `Validation OK — statuses are in-vocabulary…` (advisory warnings only, all pre-existing/grandfathered) |
| 45 | E-00014 / E-00015 front matter | 0 | both `status: PENDING`, `result: null`, `completed: null`, `owner: systems-researcher` |
| 46 | `git log --all -- <both paths>` | 0 | only `ce845c5` and `f450976` — **no run, no edit since** |
**K. What I did NOT do (explicit, for the record)**

No training, fitting, extraction, counting, feasibility pass or SPRT generation was run. No
holdout was read. No threshold, band, salt, cap or margin was changed. E-0013, E-00014, E-00015,
R-0019, R-0020, R-0021 and every handoff were **not edited** — this review lives in
`reviews/R-0022-*.md`. No H-#### status was changed. HO-0005 and W-0003 were not opened or
closed. **E-0013 was not flipped.** No `tools/` or `src/` file was touched. All inspection was
read-only; every artefact cited was recomputed by me.

**Residual uncertainty (calibrated):**

- The +10 figure and its exact band — **demonstrated** (difflib opcode enumeration + shift map).
- The four R-0021 repairs applied — **demonstrated** (line reads, string equality, paren counts).
- The append-only hash pair and all three boundaries — **demonstrated** (recomputed both sides).
- X2's arithmetic — **demonstrated** (recomputed every figure from the free-parameter list).
- The absence of any compliance claim — **demonstrated** (whole-file greps, every hit classified).
- B5 s2's body being genuinely absent from the file — **demonstrated**; whether it was lost,
  never written, or exists under another name elsewhere in the project — **unknown**, and I do
  not guess. That is why the heading is withdrawn rather than filled, and I endorse it.
- Whether the four Y1 pointers were meant to name a *pre-withdrawal* state — **unknown**; the
  pre-repair file has only 1,293 lines so no such numbering exists. I rule on what the file says
  at HEAD.
- **Not independently re-derived (out of scope by instruction, and I flag that I did not check
  them rather than implying I did):** SHRINK as an engineering call, the KING-PST freeze
  decision, `SUITE_TOLERANCE = 0.02` as a chosen value, the NONE per-game cap, and the
  X-1/X-2/X-3 branch design. I verified their **textual integrity and arithmetic** and took no
  view on their content.

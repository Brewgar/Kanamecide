---
id: R-0024
type: review
reviewer: adversarial-reviewer
target: E-0013
kind: critique
status: COMPLETED
example: false
created: 2026-09-26
---

# R-0024 — Confirmation of the contract repair, and the flip authorisation (part 6 re-specified)

## Scope

Narrow and structural, by the work order. **Fresh occupant: I wrote none of R-0019–R-0023, none of S-0025–S-0033, and I occupied no prior seat in this exchange. Everything numeric below is recomputed from the repository rather than inherited.** Every figure is quoted with the commit it was measured at.

I confirm the contract repair is faithful, and I rule that **R-0023's condition part 6 is unsatisfiable as written and must be re-specified before anything else happens.** On my ruling plus the conditions below, E-0013 **MAY** be flipped `PENDING` → `RUNNING`. I did not flip it and no seat may flip it on the strength of this review's own claims.

The contract's *substance* is closed and I do not re-open it: B1–B7 DISCHARGED, F1–F12 CLOSED, DN1–DN10 complete, X1–X5 and Y1 ruled, integrity (i)/(ii)/(iii) HOLD. I do not re-litigate SHRINK, the KING-PST freeze, `SUITE_TOLERANCE`, the NONE cap, the X-1/X-2/X-3 branch design, or any DISCHARGED finding.

I ran no training, fitting, extraction, counting, feasibility pass or SPRT generation, read no holdout, edited no record but this one, flipped nothing, and changed no H-#### status.

## Verdict

| | |
|---|---|
| (a) Z1 repaired as ONE contiguous sentence, author's own word MOVED | **CONFIRMED** |
| (b) Re-specified contract adopted verbatim, exclusion list CLOSED at 5 lines | **CONFIRMED** (all 7 blocks byte-identical) |
| (c) `H_body` recomputed by me on BOTH sides | **CONFIRMED** `c7ebe54c…bea7` / 22,196 B both sides |
| (c) `H_legacy` unchanged, projection arithmetic re-derived | **CONFIRMED** `b04fd5a4…00ce6` / 22,270 B; post-flip `d8add61c…e6144` |
| (d) Z2 withdrawn, not asserted; all occurrences inside the withdrawal record | **CONFIRMED**; the two `ffb6d9e` lines are now TRUE as written |
| (e) Z3 — every figure labelled with its commit | **CONFIRMED as labelled**, but see **Z4** below: the *column header* is a live claim and is now 400 insertions stale |
| (f) `146/5` and `19/2` recorded WITH boundaries | **CONFIRMED** at `6d507d8c..0d8fbce` and `040296e..0d8fbce` |
| (g) Seam instrument counts 19→18, 0 new | **PARTIALLY REPRODUCED** — 1 removed confirmed, 0-new **NOT** reproducible (I find 1 new) |
| **(g) Is the seam form fit to be a validation gate?** | **NO** — see Ruling 3 |
| **Is condition part 6 satisfiable as written?** | **NO — defective in the same class as the original contract. Re-specified below (Ruling 2).** |
| **New finding** | **Z4 — NON-BLOCKING**: Z3's column header `HEAD` is a live boundary claim, now 400 insertions stale |
| **E-0013 may be flipped PENDING → RUNNING?** | **YES**, on Ruling 2's re-specified condition and the L5-only procedure in Ruling 4 |

---

# RULING 1 — the repairs are faithful

## (a) Z1: the severed sentence at L1376 is restored, and the word was MOVED

Confirmed on both sides, read by line number.

At parent `8db1c45`, L1376–L1377 read `…are a different numbering and are NOT` / `shifted. The cross-references written *by this repair* - inside the withdrawal paragraph,`. At `b7179f3` the word `shifted.` was consumed and L1377 opened `The cross-references…`. At `8c30f32` and at HEAD `049c81d`, L1376–L1377 read:

```
1376| with the word `old`, and references to `ce845c5`, are a different numbering and are NOT
1377| shifted. The cross-references written *by this repair* - inside the withdrawal paragraph and inside
```

**One contiguous sentence, restored.** The word is byte-identical to `8db1c45` L1377 and appears nowhere else in the file; it was **moved, not retyped or invented**. `git show 8c30f32 -U0` is `@@ -1377 +1377 @@` with one removed line and one added line that is the old line with `shifted. ` prepended — the signature of a move. The Z1 repair commit is `8c30f32`, in its own commit, separate from the contract/Z2/Z3 commits and separate from any flip, as R-0023's condition part 1 required.

## (b) The re-specified contract is adopted verbatim, and the exclusion list is CLOSED

I extracted all seven blocks programmatically from `research/reviews/R-0023-*.md` and searched E-0013 for an **exact contiguous run** of each, then checked for duplicates. All seven match, each **exactly once**:

| Block | R-0023 lines | Found in E-0013 at | Occurrences |
|---|---|---|---|
| the ruling paragraph | L49 | **L1501** | 1 |
| clause (a) | L51–L63 | **L1505–L1517** | 1 |
| clause (b) | L65–L85 | **L1537–L1557** | 1 |
| clause (c) | L87–L96 | **L1561–L1570** | 1 |
| the re-specified gate (v-a)/(v-b)/(v-c) | L130 | **L1574** | 1 |
| clause (d) | L99–L118 | **L1597–L1616** | 1 |
| clause (e) | L120–L128 | **L1620–L1628** | 1 |

The only difference is a leading `> ` blockquote marker applied per-block, which is a rendering choice and not an alteration of text; with the marker normalised, the runs are byte-identical. Ruling 2's disposition (R-0023 L166, one physical line) is pasted at **E-0013 L1767–L1787** as a blockquoted hard-wrap: unwrapped and whitespace-normalised, both are **1,817 characters and equal** (R-0023 L166 additionally carries its own `> ` prefix).

**The five-field exclusion list is CLOSED at {5, 6, 7, 10, 14},** in clause (a)'s table at E-0013 L1511–L1515, and the closure sentence at L1517 is present verbatim: *"The exclusion list is CLOSED, it is exactly these five lines, and it may not be widened without a fresh ruling that names the new line."* The values are exactly L5 `status:`, L6 `result:`, L7 `elo_change:`, L10 `owner:`, L14 `completed:`. I confirmed each against the live front matter: L5 `status: PENDING`, L6 `result: null`, L7 `elo_change: null`, L10 `owner: null`, L14 `completed: null`. The anti-smuggling property holds as written.

## (c) `H_legacy` and `H_body`, recomputed by me on BOTH sides

I recomputed both from scratch, on `git cat-file blob ce845c5:<E-0013 path>` **and** on the working file, splitting on `0x0A` only, taking lines 1–428, re-terminating each surviving line with one `0x0A`, with **no trimming, no normalisation, no newline conversion**. For `H_body` the five excluded lines were deleted **by line number**, not by pattern or field-name search.

| Quantity | `ce845c5` blob | working file @ `049c81d` | Expected | Match |
|---|---|---|---|---|
| `H_legacy` (L1–428) | `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6` | same | same / 22,270 B | **YES**, 22,270 B both |
| `H_body` (L1–428 − {5,6,7,10,14}) | `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` | same | same / 22,196 B | **YES**, 22,196 B both |
| `H_legacy` post-flip (L5-only) | `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144` | same | `d8add61c…e6144` | **YES** |

**Pair equal on both sides, and equal to the figures the record claims. `H_legacy` is unchanged at `b04fd5a4…00ce6` / 22,270 bytes.**

**The projection arithmetic, verified independently rather than trusted.** `H_legacy` post-flip is `22,270 − 15 + 15 = 22,270` bytes, because the line-anchored edit replaces `status: PENDING` (15 bytes) with `status: RUNNING` (15 bytes) — same length, so the *length is invariant* and only the content moves. I built the post-flip value by construction (take the file's own bytes, replace line 5 only, re-hash L1–428) and got `d8add61c…e6144`, matching R-0023's independently derived value and the record's Z2 table. The exclusion arithmetic also checks out exactly: 22,270 − 22,196 = **74 bytes**, and the five excluded lines with terminators are 16 + 13 + 17 + 12 + 16 = **74**. **Zero bytes unaccounted for.** The withdrawn `8ad61ccd…00a727` is not produced by any of these, consistent with Z2.

I also confirmed the file is BOM-free (first byte `0x2D`), **LF-only (0 CR bytes)**, 145,308 bytes, 1,865 lines, single trailing newline (`0x0A`).

## (d) Z2: withdrawn, not asserted; the two stale evidence lines are now TRUE

`8ad61ccd` and `00a727` occur in E-0013 at exactly **four lines: L1696, L1699, L1809, L1862.** L1696 and L1699 are the Z2 withdrawal record itself; L1809 is condition-part-4's evidence cell; L1862 is the verification row. **All four sit inside the withdrawal record and none is a live claim** — L1696 says *"That figure is unreproducible"*, L1699 locates the strings, L1809 says *"withdrawn as unreproducible"*, L1862 says the disposition is unchanged. I confirmed the strings appear nowhere else in the file and nowhere in `research/` outside R-0023 and these four cells.

**The two evidence lines that were false at `ffb6d9e` — I diffed that commit against HEAD and confirmed both are now TRUE as written:**

- **L1699** at `ffb6d9e` read *"`8ad61ccd` and `00a727` appear in `research/` only inside R-0023"* — **false at that commit**, since the very withdrawal record introduced them into this file. At HEAD it reads *"only inside R-0023 and, in this file, only inside this Z2 withdrawal record itself, at L1696, L1699, L1809 and L1862"*, and the record **names all four lines**, which I independently confirmed to be exactly the four that exist. **TRUE as written.**
- **L1862** at `ffb6d9e` read *"present in R-0023 only; never in this file - nothing to delete here"* — false for the same reason. At HEAD it reads *"**REVISED (S-0033).** Present in R-0023, and in this file at L1696, L1699, L1809 and this row only"*, attributes the staleness to **the orchestrator's count rather than a new defect**, and states the disposition is **unchanged**. **TRUE as written.**

The correction is honest about its own cause: the earlier result was true at `f03613e` and was **made stale by the withdrawal itself**. I endorse that attribution — the withdrawal created the condition it then had to report. **Z2 confirmed: withdrawn, not asserted.**

## (e) Z3 — every figure is labelled; one header is a live claim (Z4, NON-BLOCKING)

Z3's achievement is real and I confirm it: **every figure in the Z3 table carries the commit it was measured at**, in the column headers *"At `8db1c45` (R-0022's HEAD - the historical column, unchanged)"* and *"At `f03613e` (R-0023's HEAD, measured by me)"*. I recomputed both columns:

| Boundary | at `8db1c45` | at `f03613e` | at HEAD `049c81d` | record's label correct? |
|---|---|---|---|---|
| `4478c3a..HEAD` | 1011/0 | **1040/0** | **1440/0** | yes — labelled `f03613e` |
| `ce845c5..HEAD` | 493/130 | **522/130** | 922/130 | yes |
| `f450976..HEAD` | 231/29 | **267/36** | 667/36 | yes |
| `d3ce887..HEAD` | not stated | **201/29** | 601/29 | yes |
| `8db1c45..HEAD` | not stated | **50/21** | 450/21 | yes |

I also confirmed the historical column against the *commits it names*: `4478c3a..d3ce887` = 868/0, 347/127, 71/12 (matching the table's "at `d3ce887`" column) and `4478c3a..c23803f` = 1011/0, 493/130, 231/29 (matching R-0021's own repair commit). **The labelling discipline is exactly what Z3 was for, and it holds.**

**The invariant that matters is ZERO DELETIONS, and I confirm it: `4478c3a..HEAD` at `049c81d` is 1440 insertions, 0 deletions.** The insertions count moves as the addendum grows — 1040/0 at `f03613e`, 1440/0 at `ffb6d9e`, 1440/0 at `049c81d` — and every one of those is a legitimate append. No commit in E-0013's history has ever deleted a line from the original pre-registration at this boundary. **The append-only obligation is discharged outright, and it is discharged by the zero, not by the 1440.**

**Z4 — NON-BLOCKING. The Z3 column header `At f03613e (R-0023's HEAD, measured by me)` is a live `HEAD` claim, and `HEAD` moves.** The word `HEAD` inside a committed column header denotes whatever `HEAD` is when a reader looks, not what it was at `f03613e`. The numbers are correctly pinned to `f03613e`, but a reader who takes `4478c3a..HEAD` at face value gets 1040 and is wrong by 400 insertions today. **This is the same class as the defect Z3 was raised to fix — a boundary figure that does not say which boundary — one level down, and it is the last instance of it in the file.** It is non-blocking because nothing in the record's argument depends on the number being current: Rule F's arithmetic, the `H_body` pair, and the zero-deletion claim are all independent of it. **Fix when convenient: rename the header to `At f03613e (pinned; NOT current HEAD)` and add a `049c81d` column, or drop the word `HEAD` from the header and put the commit in the boundary cell.** I do not require this before the flip.

## (f) `146/5` and `19/2` — recorded WITH boundaries, not repeated as boundaryless corrections

Confirmed. I searched E-0011's history and reproduced both:

- **`146 / 5` = `6d507d8c..0d8fbce`** — reproduced exactly.
- **`19 / 2` = `040296e..0d8fbce`** — reproduced exactly.
- For completeness, the figures R-0023 found also reproduce: `9d60f64..040296e` = 62/3, `040296e~2..040296e` = 63/4, `027ea58..040296e` = 316/4.

E-0013's Z3 records all of these **with** their boundaries (L1743–L1754 and verification row 11 at L1863), and the text states the rule explicitly: *"**So `146/5` is not a phantom - it is a real figure quoted without its boundary**, which is the same failure mode as Z3 in a different record"* and *"**Going forward: quote a commit hash with every figure, or let the record compute it.**"* I grepped the whole file for `146`: it occurs at L1743, L1746, L1749 and L1863 — **all four inside the Z3 correction, all four carrying a boundary.** **No boundaryless repetition anywhere. (f) CONFIRMED.**

## (g) The seam instrument

**The 1-removed claim: CONFIRMED. The 0-new claim: NOT REPRODUCED.**

I re-implemented the seam form — *line N opens with a capitalised word while line N-1 ends on a dangling token and carries no sentence boundary* — and swept four predicate variants over three revisions:

| Variant | pre-Z1 (`b7179f3`) | post-Z1 (`8c30f32`) | removed | new at HEAD | catches Z1 |
|---|---|---|---|---|---|
| N0 no narrowing | 0 | 0 | 0 | 0 | no |
| **N1 + closed-class tail** | **20** | **19** | **1** | **1** | **YES** |
| N2 + all-caps status tail | 20 | 19 | 1 | 1 | yes |
| N3 + record-id/pointer tail | 23 | 22 | 1 | 2 | yes |

**The instrument has genuine discriminating power and I confirm its central claim.** Under N1: the seam at **L1376→L1377 is present at `b7179f3` and absent at `8c30f32` and at HEAD**, and **it is the only seam removed** — the pre-Z1 and post-Z1 lists are otherwise identical, all 19 survivors matching one-for-one. **Z1 was the one true positive, and the repair stopped the instrument firing on it.** That is exactly what the record's table claims, and I reproduced it independently rather than accepting it. My absolute count is 20/19 where the record reports 19/18 — a one-off in the closed-class word list, not a discrepancy in kind, and the delta of 1 and the identity of the removed seam are exact.

**The 0-new claim does not reproduce.** Measured at HEAD `049c81d`, **there is 1 seam not present at `8c30f32`: `L1662→L1663`.**

```
1662| both sides, file-wide paren balance **-10** unchanged, and `H_body` untouched because
1663| L1377 lies outside lines 1-428, and the repair was made in its own commit, separate from
```

**This is a FALSE POSITIVE, not a defect, and I say so plainly.** L1662 ends `…untouched because` and L1663 opens `L1377 lies outside…` — an ordinary hard-wrap of one sentence where the wrapped word happens to be a line-pointer. It was introduced by the contract/Z2/Z3 section, not by the Z1 repair, which is why the "Post-Z1" column did not see it. So: **the instrument's true-positive rate is 1-in-20 and its false-positive rate is 19-in-20 — and the one new hit since `8c30f32` is itself a false positive.** That is the number that decides Ruling 3.

---

# RULING 2 — condition part 6 is UNSATISFIABLE AS WRITTEN, and is re-specified

**This is the question R-0023 cannot answer for itself, and the answer is that part 6 is defective in the same class the original contract was.**

**The three refusals were all sound, and I endorse each without qualification.** The researcher-architect was right on SYSTEM.md §1 (the architect must not verify its own proposal), right on R-0023's own endorsement (*"no seat may flip it on the strength of this review's own claims"*), and right on the structural point, which is the decisive one: **(v-b) and (v-c) are properties of a commit that does not exist.** *"The flip commit's numstat is 1/1"* and *"the flip commit touches no line outside {5}"* have no referent until the flip is made. A condition that can only be discharged by first doing the thing it gates is not a gate; it is a description of the thing, wearing a gate's clothes. **Part 6 as written is a post-hoc audit mislabelled as a pre-condition**, and any seat that "satisfies" it before the flip satisfies it by asserting something it cannot measure.

**Why this is the same class as the original contract defect — which is why I adopt reading (ii) and not (i).** The original contract said *"L1-428 byte-identical to `ce845c5`"* and thereby **forbade the very act the record exists to authorise** — a specification whose literal terms make its own purpose unachievable. Part 6 says *"a critique confirms (v-b)/(v-c) before the flip"* and thereby **makes its own purpose unachievable in the same way**: the confirmation it demands is only obtainable after the act. Both are defects of **specification, not of record**, and both are cured the same way — by the ruling seat re-specifying the clause, in the open, with the circularity named. **Reading (i) would fix this by interpreting part 6 into something it does not say.** That is precisely the move R-0023 refused to make when the architect re-specified the contract, and refusing it here would apply a double standard to the same class of defect. **I therefore adopt (ii): part 6 is defective and is re-specified below, and the re-specification is itself the authorisation.**

**Ruling 2 also disposes of the residual circularity that reading (i) would leave in place.** Under (i) the flip becomes *authorised conditionally on a future audit that has not happened* — which leaves E-0013 in exactly the state this whole exchange has been trying to leave: a record whose authorisation gate is unsatisfied, with the gate's own text unmeetable. Re-specifying the condition **splits it into a pre-condition that is checkable now and a post-condition that is checkable later**, which removes the circularity rather than relocating it.

**There is a third reading available, and I record it as rejected.** One could argue part 6 is satisfiable because the flip is a *single line at a known line number*, so (v-b) and (v-c) are predictable in advance: a line-anchored L5-only edit *must* be numstat 1/1 and *must* touch only line 5. That is true of the **method**, and it is why I authorise the flip below. But it does not make part 6 satisfiable, because a prediction confirmed only after the fact is not a confirmation, and the condition's own words require a critique that *confirms*, not one that *foresees*. **A condition cannot be discharged by the correctness of a guess.** Rejected.

## THE RE-SPECIFIED CONDITION (R-0024, 2026-09-26) — exact text

> **R-0024's replacement for R-0023's condition part 6.** R-0023's part 6 is **WITHDRAWN AS UNSATISFIABLE** and replaced by this clause. The defect is in the specification, not in the record: parts (v-b) and (v-c) are properties of a commit that does not yet exist, so the condition as written demands its own confirmation before the act it gates, which no seat can supply without either self-certifying or guessing. R-0023's parts 1–5 are **unchanged and remain MET**.
>
> **The pre-condition (checkable now, discharged by R-0024).** All of the following are recomputed on the working tree and hold at `049c81d`: **(P1)** `H_body` = `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` over **22,196 bytes** on **both** `git cat-file blob ce845c5:<this path>` and the working file, computed under clause (b) exactly as specified. **(P2)** `H_legacy` = `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6` over **22,270 bytes**, unchanged. **(P3)** The Z1 defect is absent: the sentence at L1376–L1377 is one contiguous sentence, `git show 8c30f32 -U0` is a single-line hunk, and the restored word is byte-identical to `8db1c45` L1377. **(P4)** Z2's `8ad61ccd…00a727` is withdrawn, not asserted, and every occurrence in this file sits inside the withdrawal record. **(P5)** The file is BOM-free, LF-only, and L5 is exactly `status: PENDING`.
>
> **The authorisation.** P1–P5 all hold, so **E-0013 may be flipped `PENDING` → `RUNNING`**, in a single commit, line-anchored, changing L5 and nothing else, by the procedure in R-0024's Ruling 4. **The flip is authorised by the pre-condition, not by any future audit.**
>
> **The post-condition (checkable only after the flip, and therefore binding on the auditor, not on the author).** The post-condition does **not** gate the flip; it is discharged afterwards, and a failure of it is a **revert-and-report**, never a silent continuation. A seat **other than the one that made the flip** — the verification-auditor, per SYSTEM.md §1 — must, over the flip commit: **(Q1)** assert `H_body` is **unchanged** at `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` / 22,196 bytes on both sides — *the byte count must be 22,196, not 22,270, or line 5 was edited outside the exclusion*; **(Q2)** assert `git diff -U0` is **exactly one hunk** and `git diff --numstat` is **exactly `1 1`**; **(Q3)** assert the hunk's line number is **5** and the only changed line is L5; **(Q4)** assert L5 reads exactly `status: RUNNING` and that **no other occurrence of the string `status: PENDING` in the file changed** — 13 quoted occurrences existed before the flip and **all 13 must be byte-identical after it**; **(Q5)** assert `H_legacy` is now `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144` over 22,270 bytes; **(Q6)** record the boundary numstats under Rule F and confirm the `4478c3a` boundary is now **1441 / 1**, i.e. **the zero-deletion claim survives as a bounded exception and nothing else changed**.
>
> **If Q1–Q6 do not all hold, the flip is reversed by the same line-anchored procedure, E-0013 returns to `status: PENDING`, and the failure is reported in a dated addendum naming the clause that failed.** No seat may proceed to build the extractor, the trainer or the parameter-table evaluator, and no holdout may be read, while any of Q1–Q6 is unverified. **A flip that has not been audited may not be relied on, but it is not thereby unauthorised** — the authorisation is P1–P5, and the audit is how the authorisation is *evidenced*.

*This clause is to be appended to E-0013 as a dated addendum by the owner seat, in the same commit style as the R-0023 adoption, and R-0023 is not edited by it.*

---

# RULING 3 — the seam form is NOT fit to become a validation gate

**No, and the reason is arithmetic rather than judgement: with 18 known-legitimate seams remaining, the instrument has a 1-in-20 true-positive rate. A gate that is wrong 19 times out of 20 does not get obeyed; it gets switched off, and the one defect it would have caught gets through.**

I rule on the evidence I measured, not on the record's own account of its false-positive rate:

- Under N1 the instrument fires **20 times** pre-Z1 and **19 times** post-Z1. **Exactly one** of those 20 is a real defect.
- Every one of the 19 survivors is a legitimate construction, and I classified each by what line N opens with: most are **record identifiers or line-pointers** (`E-00014`, `HO-0016`, `R-0020`, `R-0020's`, `L677-L680`, `L919-L954`, `L1394`, `B5/B6`, `L1-L428`, `SHA-256`, `L1377`), three are **status tokens** (`INCONCLUSIVE`, `UNMEASURED`, `COMPLETED`), and the rest are hard-wraps where the wrapped word is capitalised by position rather than by sentence start. **None is a defect.**
- **The decisive datum: the instrument's own new hit since the Z1 repair, `L1662→L1663`, is itself a false positive.**

**An allow-list is therefore the wrong mechanism, and I say so for a reason beyond the count.** An allow-list is a list of *line numbers*, and **line numbers are not stable in this file** — the +10 shift, the B5 s2 three-lines-for-thirteen replacement, the Y1 insertions and the Z1/contract sections have all moved them, which is the entire reason R-0022, R-0023 and this review exist. An allow-list keyed to line numbers would be invalidated by the next append and would then be either stale (letting real defects through) or rewritten (which is a judgment call disguised as configuration). An allow-list keyed to *content* degenerates into the predicate itself and stops discriminating. **The honest position is that this defect class has no cheap reliable detector in this file, and pretending otherwise is how the terminal-punctuation check already failed once — it returned 825 hits on a file that is 99% correct, and a seat that runs it every commit will learn to ignore it, which is worse than not running it.**

**What I recommend instead — and I tested it, so the recommendation is evidence-backed rather than a preference.** The obvious next candidate is a **hunk-level** rule: for every `git diff -U0` hunk, require that the first added line *extends* the first removed line, on the reasoning that Z1, R-0019's X1 and R-0021's X4 were all cases of a replacement block beginning by consuming text from the line above. **I ran it over E-0013's entire history — 9 commits, 30 hunks with both a first-removed and a first-added line — and it fires on 29 of 30, a 97% false-positive rate, worse than the seam form.** On E-0011 (5 hunks) it fires on 5 of 5. **The hunk-level rule is worse still, and I record that so the next seat does not spend a cycle on it.**

**My ruling: adopt no new validation gate for this defect class in this file.** The seam form is worth keeping as a **non-blocking advisory that a seat runs once, by hand, when it has just edited prose** — where 19 hits is a manageable reading list and the one real defect stands out — and **not** as a `validate`-time assertion, and **not** as a gate on the flip. The mechanism that actually protects this file is the one already in place and already working: **a fresh seat reading by line number before it signs**, which is what caught Z1. That is expensive, and that is why nobody likes it, but it is the only instrument here with a true-positive rate near 1. **The right response to a check this noisy is to say so in the record, which this review does, and not to encode it as a gate that will be ignored.**

---

# RULING 4 — the flip is AUTHORISED, and here is the exact procedure

**E-0013 may be flipped `PENDING` → `RUNNING` on this ruling plus Ruling 2's re-specified condition. P1–P5 all hold at `049c81d`, verified by me independently.**

**I do not flip it, and no seat may flip it on the strength of this review's own claims** — the rule R-0023 stated and that I am applying to myself. The flip is made by the **owner seat (researcher-architect)**, in its own commit, and is then audited by a **different seat (verification-auditor)** under Q1–Q6.

**`status: PENDING` occurs 14 times in this file and that is a FLOOR, not a constant.** I counted them: L5, L20, L435, L456, L1132, L1270, L1363, L1394, L1435, L1557, L1565, L1574, L1576, L1865. **Thirteen of the fourteen are quoted or historical statements**, including three inside R-0023's own pasted clause text which *cannot* be changed without breaking the verbatim requirement. **A string-matched rewrite is forbidden and would be a disaster: replacing every `status: PENDING` with `status: RUNNING` would rewrite 13 lines of quoted history and produce numstat 13/13.** The record's own clause (c) rule 1 already says this; I confirm it, and I have now measured it.

## The procedure, exactly

1. **Assert L5 before writing.** Read line 5 of the file and assert it is **exactly** the 15 bytes `status: PENDING` followed by `0x0A`. If it is not, **STOP** — do not write. (Measured at `049c81d`: it is.)
2. **Write line 5 only**, by line index, replacing those 15 bytes with `status: RUNNING` (also 15 bytes). Do not touch any other byte. Do not use `sed`, `-replace`, `-i`, or any pattern match.
3. **Assert exactly one line changed after writing.** `git diff --numstat -- <path>` must read exactly `1<TAB>1<TAB><path>`. Any other value means the write was not line-anchored: **revert and re-do it.**
4. **Verify the hunk is a single line.** `git diff -U0 -- <path>` must show **exactly one `@@` hunk**, of the form `@@ -5 +5 @@`, with one `-` line and one `+` line, and the `+` line must be exactly `status: RUNNING`.
5. **Commit alone**, with no other file in the commit and no other record edited. The commit message must carry the commit's own hash for the post-auditor, and must state that the flip is made under R-0024's Ruling 2.
6. **Do not proceed to any build, fit, extraction or holdout read** until Q1–Q6 have been verified by a different seat.

## The assertions a DIFFERENT seat must check afterwards

Against the flip commit `C` (all recomputed, none copied):

| # | Assertion | Expected |
|---|---|---|
| Q1 | `H_body` on both `ce845c5` blob and the post-flip working file | `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7`, **22,196 bytes both** |
| Q2 | `git show C --numstat -- <path>` | exactly **`1 1`** |
| Q3 | `git show C -U0 -- <path>` | exactly **one** `@@ -5 +5 @@` hunk; the `+` line is exactly `status: RUNNING` |
| Q4 | every other `status: PENDING` occurrence | **all 13 unchanged and byte-identical** (L20, L435, L456, L1132, L1270, L1363, L1394, L1435, L1557, L1565, L1574, L1576, L1865) |
| Q5 | `H_legacy` post-flip | `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144`, **22,270 bytes** |
| Q6 | `4478c3a..C` numstat | **1441 / 1** — the zero-deletion claim survives as a bounded exception and nothing else moved |
| Q7 | `git diff --check` on the commit | exit 0, empty |
| Q8 | any file other than E-0013 in commit `C` | **none** |

**Q1's byte count is the load-bearing one and is worth stating separately: if the post-flip `H_body` reads 22,270 bytes rather than 22,196, then line 5 was edited *outside* the exclusion and the contract was violated** — because `H_body` is the only quantity in this record that is invariant under exactly the legal transitions and sensitive to exactly the illegal ones. That is the whole reason the re-specified contract defines it, and it is why Q1 is the first assertion rather than the third.

---

# Governance state — confirmed, nothing moved

| Item | State at `049c81d` | Verified how |
|---|---|---|
| E-0013 | `status: PENDING` (L5), `result: null` (L6), `elo_change: null` (L7), `owner: null` (L10), `completed: null` (L14) | front-matter read |
| E-00014 | `status: PENDING`, `result: null`, `completed: null` | front-matter read |
| E-00015 | `status: PENDING`, `result: null`, `completed: null` | front-matter read |
| H-#### statuses | 16 hypotheses; all `OPEN` or `SUPERSEDED`; **none changed** | `Select-String '^status:'` over `research/hypotheses/*.md` |
| HO-0005 | `status: REQUESTED` | front-matter read |
| W-0003 | `status: IN_PROGRESS` | front-matter read |
| R-0019–R-0023 | unedited by this seat; R-0023 byte-intact (all seven blocks still extract cleanly) | exact-run extraction |
| `tools/` or `src/` | **no edit** | `git status --porcelain` clean apart from this review |
| Training / fitting / extraction / counting / feasibility pass / SPRT | **none ran** | I ran none; no RUN record written |
| Holdout | **not read** | I read no holdout |
| Files I edited | **this review only** | `git status --porcelain` |

**Scope discipline — what I did NOT do.** Did not re-litigate SHRINK, the KING-PST freeze, `SUITE_TOLERANCE = 0.02`, the NONE cap, the X-1/X-2/X-3 branch design, or any DISCHARGED finding. Did not edit E-0013, E-00014, E-00015, R-0019, R-0020, R-0021, R-0022, R-0023, or any handoff. **Did not flip E-0013.** Did not change any H-#### status. Did not open or close HO-0005 or W-0003. Did not run training, fitting, extraction, counting, feasibility passes or SPRT generation. Did not read the holdout. Did not touch `research/state.md` or `state.json` by hand (GENERATED — only via `state --write`).

### Residual uncertainty (calibrated)

**Demonstrated** — the three hashes, recomputed on both sides from the raw bytes; the exclusion arithmetic (74 bytes, exact); the post-flip projection and its length-invariance; Z1's one-hunk one-line diff and the word's byte-identity with `8db1c45` L1377; all seven contract blocks and Ruling 2's pasted text, by exact contiguous run; the four occurrences of the withdrawn string and the two revised evidence lines, diffed against `ffb6d9e`; all five boundary numstats in both Z3 columns plus the `d3ce887` and `c23803f` columns; the zero-deletion invariant; `146/5`, `19/2`, `62/3`, `63/4`, `316/4` on E-0011; the seam predicate sweep over three revisions; the hunk-level control experiment; every governance cell in the table above.

**Strongly supported** — that the seam instrument's true-positive rate on this file is 1 in 20, and that its one new hit since `8c30f32` is a false positive; that Z4's stale `HEAD` header is the last instance of the boundary-labelling defect class in this file; that the record's 19/18 counts and my 20/19 differ only by one entry in the closed-class word list.

**Unknown** — whether the orchestrator intended the 14 `status: PENDING` occurrences to be a hard floor or a measured-at-a-commit figure. I rule on the record as written, which treats it as a hazard measure; **the flip procedure works under either reading, because it is line-anchored and never string-matched.**

## Date

2026-09-26

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns.

---

## Verification Block (kind: critique — evidence about the record, recorded per the close-out requirement)

**Environment contract observed throughout.** `run_commands` in this session reports `Command exited with code 1` on commands that SUCCEED, so every exit code below is captured explicitly as `$LASTEXITCODE` into a file and read back, never inferred from the tool's own report. All output was redirected with `| Out-File -Encoding utf8` and read from the file. `read_files` line-range staleness on large files was avoided by dumping numbered ranges to disk first. **Two environment defects cost me two false negatives and I record them so the next seat does not repeat them: (1) PowerShell's `-match` is CASE-INSENSITIVE, so `^[A-Z]` silently matches lowercase and made the seam instrument appear to fire 454 times; the fix is `-cmatch`. (2) `New-Object System.IO.StreamReader($stream, $enc)` fails on PowerShell 5.1; use the byte-stream copy that worked here.**

### Commands re-run by me, with exit codes and observed output

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git pull --ff-only` | 0 | `Already up to date.` |
| 2 | `git status -sb` | 0 | `## master...origin/master`, tree clean |
| 3 | `git rev-parse HEAD` / `origin/master` | 0 | **both `049c81dbeeb709146d024a5dedd3b532b8863c9a`** |
| 4 | `H_legacy` (L1–428, terminators in) on the `ce845c5` blob | 0 | `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`, **22,270 bytes** |
| 5 | `H_legacy` on the working file @ `049c81d` | 0 | **the same**, **22,270 bytes** — pair equal |
| 6 | `H_body` (L1–428 minus lines 5,6,7,10,14 **by number**) on the `ce845c5` blob | 0 | `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7`, **22,196 bytes** |
| 7 | `H_body` on the working file @ `049c81d` | 0 | **the same**, **22,196 bytes** — pair equal, and equal to the claimed value |
| 8 | `H_legacy` after a line-anchored L5-only flip, computed by construction | 0 | `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144`, **22,270 bytes** |
| 9 | exclusion arithmetic | 0 | 22,270 − 22,196 = **74**; 16+13+17+12+16 = **74** — **exact, zero unaccounted**; post-flip length invariant because `PENDING` and `RUNNING` are both 7 bytes |
| 10 | file hygiene | 0 | first byte `0x2D` (**no BOM**), **0 CR bytes**, last byte `0x0A`, 145,308 bytes, 1,865 lines |
| 11 | E-0013 front matter L1–L20, numbered dump | 0 | L5 `status: PENDING`, L6 `result: null`, L7 `elo_change: null`, L10 `owner: null`, L14 `completed: null` — **PENDING, not flipped** |
| 12 | `git show 8c30f32 -U0 -- <E-0013 path>` | 0 | exactly one hunk `@@ -1377 +1377 @@`; `-The cross-references…` / `+shifted. The cross-references…` — **1 hunk, 1 line, numstat 1/1** |
| 13 | `git show --stat 8c30f32` | 0 | `1 file changed, 1 insertion(+), 1 deletion(-)` |
| 14 | L1375–L1379 at `8db1c45` / `b7179f3` / `8c30f32` / `HEAD` | 0 | word present at `8db1c45` L1377, consumed at `b7179f3`, restored at `8c30f32` and HEAD — **moved, not retyped** |
| 15 | exact contiguous-run extraction of all 7 contract blocks from R-0023 into E-0013 | 0 | **7/7 found, each exactly once**, at L1501, L1505–L1517, L1537–L1557, L1561–L1570, L1574, L1597–L1616, L1620–L1628 |
| 16 | Ruling 2 text (R-0023 L166 → E-0013 L1767–L1787), unwrapped | 0 | **1,817 chars both, EQUAL** after stripping the single leading `> ` that R-0023 L166 itself carries |
| 17 | exclusion list closure | 0 | table rows at L1511–L1515 = exactly L5, L6, L7, L10, L14; closure sentence at L1517 verbatim |
| 18 | `8ad61ccd` / `00a727` in E-0013 | 0 | **4 occurrences: L1696, L1699, L1809, L1862** — all inside the withdrawal record, **no live claim** |
| 19 | same two lines at `ffb6d9e` vs HEAD | 0 | both were **FALSE at `ffb6d9e`** and are **TRUE at HEAD**; the correction attributes the staleness to the orchestrator's count, not a new defect |
| 20 | `git diff --numstat` at 5 boundaries, HEAD `049c81d` | 0 | `4478c3a..HEAD` **1440/0**; `ce845c5..HEAD` 922/130; `f450976..HEAD` 667/36; `d3ce887..HEAD` 601/29; `8db1c45..HEAD` 450/21 |
| 21 | same 5 boundaries at `f03613e` (Z3's column) | 0 | **1040/0, 522/130, 267/36, 201/29, 50/21** — **Z3's column reproduces exactly** |
| 22 | same 3 boundaries at `8db1c45` (Z3's historical column) | 0 | **1011/0, 493/130, 231/29** — **Z3's historical column reproduces exactly** |
| 23 | `4478c3a..` at `d3ce887` and at `c23803f` | 0 | 868/0, 347/127, 71/12 and 1011/0, 493/130, 231/29 — **both of the table's own labelled columns check out** |
| 24 | **ZERO-DELETION invariant at HEAD** | 0 | **`4478c3a..049c81d` = 1440 insertions, 0 deletions** |
| 25 | E-0011 numstat, exhaustive boundary search | 0 | `6d507d8c..0d8fbce` = **146/5**; `040296e..0d8fbce` = **19/2**; `9d60f64..040296e` = 62/3; `040296e~2..040296e` = 63/4; `027ea58..040296e` = 316/4 |
| 26 | `146` occurrences in E-0013 | 0 | L1743, L1746, L1749, L1863 — **all 4 inside Z3, all 4 carrying a boundary; no boundaryless repetition** |
| 27 | seam predicate sweep, 4 variants × 3 revisions | 0 | N1: pre **20**, post **19**, **removed 1**, **new at HEAD 1**, Z1 caught = **YES**; N2: 20/19/1/1; N3: 23/22/1/2; N0: 0/0/0/0 |
| 28 | the removed seam, identified | 0 | **exactly `1376→1377:NOT`** — present at `b7179f3`, absent at `8c30f32` and HEAD; the 19 survivors match one-for-one |
| 29 | the 1 new seam at HEAD, read | 0 | **`1662→1663`** — `…untouched because / L1377 lies outside lines 1-428…` — **a legitimate hard-wrap, a FALSE POSITIVE** |
| 30 | hunk-level control rule over E-0013's whole history | 0 | 9 commits, **30 qualifying hunks, 29 violations (97% FP)**; E-0011 control: 5 hunks, 5 violations — **worse than the seam form; recorded so the next seat does not try it** |
| 31 | `status: PENDING` occurrences in E-0013 | 0 | **14** (L5, L20, L435, L456, L1132, L1270, L1363, L1394, L1435, L1557, L1565, L1574, L1576, L1865) — **a floor; 13 of 14 are quoted history** |
| 32 | E-00014 / E-00015 front matter | 0 | both `status: PENDING` / `result: null` / `completed: null` — **neither ran** |
| 33 | all H-#### `^status:` | 0 | 16 hypotheses, all `OPEN` or `SUPERSEDED` — **none changed** |
| 34 | HO-0005 / W-0003 front matter | 0 | `REQUESTED` / `IN_PROGRESS` — **untouched** |
| 35 | `git status --porcelain` | 0 | only this review; all scratch files removed before commit |
| 36 | `research.py validate` | 0 | **PASS** (warnings only, all pre-existing) |
| 37 | `research.py update` | 0 | `updated: research/index.md` |
| 38 | `research.py state --write` | 0 | `wrote research/state.json and research/state.md` |
| 39 | `git diff --check` | 0 | empty — no whitespace damage |

### What I reproduced independently

**Everything numeric in this review.** The `H_legacy` and `H_body` pairs on both sides, from the raw bytes, with the byte counts; the exclusion arithmetic; the post-flip projection and its length-invariance; Z1's one-hunk one-line diff and the word's byte-identity with `8db1c45` L1377; all seven contract blocks and Ruling 2's pasted text, by exact contiguous run with duplicate checking; the exclusion list closure; the four occurrences of the withdrawn string; the two evidence lines, diffed against `ffb6d9e`; all five boundary numstats in both Z3 columns plus the `d3ce887` and `c23803f` columns and the zero-deletion invariant; `146/5`, `19/2`, `62/3`, `63/4`, `316/4` on E-0011; the seam predicate sweep over three revisions; the hunk-level control experiment; the `status: PENDING` census; and every governance cell.

### What I could NOT reproduce, and why

1. **The seam instrument's absolute counts of 19 → 18.** My closest predicate gives 20 → 19 — **one higher on both sides**, a one-entry difference in the closed-class word list. **The delta of 1, the identity of the removed seam, and the fact that it is Z1 all reproduce exactly**, so this is a difference in kind of predicate, not in substance. I report my numbers rather than adopting the record's.
2. **The instrument's "0 new seams".** At HEAD there is 1 new seam (`1662→1663`), which I read and confirm is a **false positive**, not a defect. The record's 0 was true at `8c30f32`; the contract/Z2/Z3 section then added one. **Not a new defect in E-0013 — a boundary that moved, and the same lesson as Z3, which is why I report it as Z4's sibling rather than as a blocking finding.**

### Claims that must be corrected in the record

- **Z4 (NON-BLOCKING):** Z3's column header `At f03613e (R-0023's HEAD, measured by me)` reads as a live `HEAD` claim. Rename to `At f03613e (pinned; NOT current HEAD)` and add a `049c81d` column, or drop the word `HEAD` from the header. **Not required before the flip.**
- **The seam table's Post-Z1 column** should read `8c30f32` rather than an unqualified "Post-Z1", for exactly the reason Z4 applies.

### Assumptions

- That `research.py`'s generated `state.md` / `state.json` are correctly regenerated only by `state --write` and never hand-edited (SYSTEM.md §12) — I obeyed this and did not hand-edit them.
- That the seat auditing the flip is the **verification-auditor**, per SYSTEM.md §1's rule that nobody verifies their own claim. I name that seat in the re-specified condition because the work order did.

### Proposed follow-ups

- **The owner seat appends Ruling 2's re-specified condition to E-0013 as a dated addendum**, then makes the L5-only flip by Ruling 4's procedure, then routes Q1–Q6 to the verification-auditor. **That is the next mechanical step and it needs no further interpretation.**
- **Z4** may be fixed in the same addendum at no cost.
- **No new validation gate is adopted** for the seam defect class (Ruling 3). If the project later wants one, the hunk-level rule has already been measured here at 97% false positives and should not be re-attempted without a different predicate.

---

<!-- VERIFICATION BLOCK — fill this when kind: verification (see SYSTEM.md §5).
     A verification review is evidence about a work item, not an opinion about it.
     Delete this block (or leave it empty) for kind: critique. -->

## Verification Block (kind: verification only)

- **Work item verified:** W-#### (round N)
- **Verified by:** adversarial-reviewer (must NOT be the work item's owner)
- **Verdict:** VERIFIED | CONTRADICTED | PARTIAL | UNVERIFIABLE
- **Commands re-run by me (raw output retained):**
  1. `...` → exit code ... ; observed: ...
- **Artifacts checked:** path — SHA-256 (recomputed, not copied)
- **What I reproduced independently:** ...
- **What I could NOT reproduce (and why):** ...
- **Sample validity re-checked:** arm differentiation ..., independence ..., power ...
- **Claims that must be corrected in the record:** ...
- **Residual uncertainty (calibrated):** demonstrated | strongly supported | likely | plausible | speculative | unknown

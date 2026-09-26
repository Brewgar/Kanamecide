---
id: R-0023
type: review
reviewer: adversarial-reviewer
target: E-0013
kind: critique
status: COMPLETED
example: false
created: 2026-09-26
---

# R-0023 — Append-only contract re-specification, R-0022 `old L…` row disposition, and one new blocking defect

## Scope

Narrow and structural, by the work order. I wrote none of R-0019, R-0020, R-0021, R-0022 or S-0025–S-0031, and I occupied no prior seat in this exchange; everything below is recomputed from the repository rather than inherited.

Two deliverables: **Ruling 1**, the exact replacement append-only contract text; **Ruling 2**, the disposition of R-0022's six `old L…` table rows. The contract's *substance* is closed and I do not re-open it: B1–B7 DISCHARGED, F1–F12 CLOSED, DN1–DN10 complete, X1–X5 and Y1 ruled, integrity (i)/(ii)/(iii) HOLD. I do not re-litigate SHRINK, the freeze, `SUITE_TOLERANCE`, the NONE cap or the X-1/X-2/X-3 branch design.

I ran no training, fitting, extraction, counting, feasibility pass or SPRT generation, read no holdout, edited no record but this one, flipped nothing, and changed no H-#### status.

**Bottom line: the orchestrator's diagnosis is correct, I confirm it, and the escalation was the right call. But the record is NOT clear to flip, because the Y1 pass itself severed a sentence (Z1, blocking).**

## Verdict

| | |
|---|---|
| Contract defect is in the SPECIFICATION, not the record | **CONFIRMED** |
| E-0011 precedent for in-place lifecycle edit | **CONFIRMED, and stronger than stated** (one figure quoted for it is wrong — see Corrections) |
| Escalation instead of a silent flip | **CORRECT** |
| Ruling 1 — re-specified contract | **ISSUED, exact text below, ready to paste** |
| Ruling 2 — the six `old L…` rows | **(i) NON-DEFECTS, no action**; R-0022's DO-NOT-TOUCH marker carries one non-blocking defect |
| New findings | **Z1 BLOCKING**, Z2 and Z3 non-blocking |
| E-0013 may be flipped PENDING → RUNNING now? | **NO.** Six-part condition below; the flip is a separate final commit |


---

# RULING 1 — the append-only contract, re-specified

**This is a defect in the contract's SPECIFICATION, not in the record.** `status:`, `result:` and `elo_change:` at L5–L7 are lifecycle-mutable BY DESIGN: a record that cannot change its status can never be run or closed, and SYSTEM.md §2 Gate 6 and SCHEMA.md §2 both fix those fields as lifecycle state rather than pre-registration content. The contract was specified as "L1-428 byte-identical to `ce845c5`", and that specification forbids the very act the record exists to authorise. A seat must not silently redefine a protected range; the researcher-architect escalated rather than flipping, and recorded the authorisation in a dated addendum. **That was the correct call and I endorse it without qualification.**

**The precedent, verified independently rather than accepted.** E-0011 carries `status:` at the same L5 and transitioned in place: `027ea58` PENDING → `9d60f64` RUNNING → `040296e` COMPLETED. `git show 040296e -- <E-0011 path>` is a hunk at `@@ -3,6 +3,6 @@` rewriting L5 `RUNNING`→`COMPLETED` and L6 `null`→`PASS`, plus `@@ -12,5 +12,5 @@` rewriting L14 `completed: null`→`2026-09-24` — in the **same commit** that appended its close-out addendum at L457. `git log -S 'status: COMPLETED' -- <E-0011 path>` returns exactly `040296e`. L5, L6 and L14 are the first, second and fourteenth lines of the file: the lifecycle field set, mutated in place by the record's own owner and accepted by its review history.

Below is the replacement text, in this record's own idiom, so the next cycle is mechanical.

---

**THE APPEND-ONLY CONTRACT, re-specified (R-0023, 2026-09-26). The defect being fixed is in the specification, not in the record.** The clause above was specified as "lines 1-428 byte-identical to `ce845c5`", and that specification has one fatal property: **`status:` is L5, inside the protected block.** A record whose `status:` cannot change can never be run or closed, so the specification as written forbids the very act the record exists to authorise. Lifecycle fields are mutable by design, and the repo's own precedent is exact: E-0011 carries `status:` at the same L5 and transitioned `PENDING` → `RUNNING` in `9d60f64` and `RUNNING` → `COMPLETED` in `040296e`, the latter an in-place edit of L5, L6 and L14 in the same commit that appended its close-out addendum at L457. The escalation recorded below is not hesitation; it is the rule that a protected range is the owner's to move, not a seat's. This paragraph is that move, made by the ruling seat, in the open, with every figure computed rather than asserted.

### (a) WHAT IS PROTECTED, AND WHAT IS EXCLUDED BY NAME

Lines 1-428 of this file — the ORIGINAL pre-registration — remain the protected range, and they remain byte-identical to `ce845c5` in every byte **except** the five lifecycle field lines named here, which are excluded **by name** from the protected range:

| Line | Field | Why it is excluded |
|---|---|---|
| L5 | `status:` | lifecycle state; PENDING/RUNNING/COMPLETED/ABANDONED (SCHEMA §2) |
| L6 | `result:` | the verdict, writable only at close-out; distinct from `status` by design (SYSTEM §2 Gate 6) |
| L7 | `elo_change:` | a measurement, and this record measures nothing until it runs |
| L10 | `owner:` | an actor field (SCHEMA §3), assigned at hand-off rather than at pre-registration |
| L14 | `completed:` | written only at close-out |

Every other line in 1-428 is protected byte-for-byte: all of L1–L4, L8–L9, L11–L13, L15–L16, and the whole body L17–L428 — including the em-dash in `title:` at L4, `pre_registered: 2026-09-26` at L11, and the tag list at L15. **The exclusion list is CLOSED, it is exactly these five lines, and it may not be widened without a fresh ruling that names the new line.** That closure is the anti-smuggling property: no body edit can buy itself cover by being declared lifecycle after the fact.

### (b) THE HASH INPUT, DEFINED SO THAT TWO PEOPLE GET THE SAME BYTES

> **`H_body` = SHA-256(B)**, where **B** is built from the UTF-8 bytes of this file as follows.
>
> 1. Read the file's bytes. The file is LF-only; a `0x0D` anywhere in the protected range is itself a change and changes `H_body`.
> 2. Split on `0x0A` (LF) only. No other split is permitted.
> 3. Take lines **1 through 428 inclusive**.
> 4. **Delete** lines **5, 6, 7, 10 and 14** — by line number, not by pattern, not by field-name search.
> 5. Concatenate the surviving lines in ascending order, **each followed by one `0x0A`**, including line 428's own terminator.
> 6. B is that byte string; `H_body` is its SHA-256, lowercase hex.
>
> No trimming, no `rstrip`, no whitespace normalisation, no newline conversion, no BOM handling. The bytes are the bytes; two people who run this get the same value or one of them has a different file.

The value at adoption, computed from both sides:

- `git show ce845c5:<this path>`, lines 1-428, minus the five excluded lines → `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7`, **22,196 bytes**
- this working file, the same construction → `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7`, **22,196 bytes**

Equal. **The protected body is append-only under the re-specified contract too, and it already was: adopting this contract costs nothing and breaks nothing, and it costs nothing because the body has not moved.** The 74-byte difference from the 22,270-byte figure above is exactly the five excluded lines and nothing else.

**`H_body` is INVARIANT across the entire lifecycle, and that is the entire point.** `status: PENDING` → `RUNNING` and → `COMPLETED`, `result: null` → `PASS`, `completed: null` → a date: all four leave `H_body` at `c7ebe54c…bea7`. Verified by simulation, not asserted (Verification block, command 7).

### (c) HOW A LIFECYCLE TRANSITION IS AUTHORISED AND RECORDED

A lifecycle transition is **not** an in-place body edit and is never to be presented as one. It is a separate, single-purpose commit touching **only** excluded field lines. Four rules, each machine-checkable:

1. **Line-anchored, never string-matched.** The edit is made at a named line number. It is **forbidden** to flip by search-and-replace — and the reason is measured, not stylistic: `status: PENDING` occurs **9 times** in this file. A naive replace rewrites 9 lines: L5, which is intended, plus L20, L435, L456, L1132, L1270, L1363, L1394 and L1435, **every one of which is a quoted or historical statement**. L1363 is the re-critique gate itself; L1394 and L1435 are two of the four pointers Y1 just repaired. A naive flip is therefore not a status change — it is eight falsifications of quoted history plus one real change, it moves `4478c3a..HEAD` from `1040/0` to `1049/9`, and it destroys "the addendum has NEVER had a deletion against the original pre-registration" outright. **This is the concrete form of "a status change must not be usable to smuggle a body edit".**
2. **Bounded blast radius.** For the transition commit, `git diff --numstat <base>..<commit> -- <this path>` must show **insertions == deletions == k**, where `k` is the number of excluded fields whose value changed, and **k ≤ 5**. Any `k` outside that set is a body edit wearing a status change as a disguise, and the flip is void.
3. **`H_body` must be equal on both sides of the transition commit** — unchanged by construction, and that equality is the proof that nothing was smuggled. This is the operative test, and it **replaces** the record's old gate clause (v) rather than supplementing it.
4. **Dated record, same file, append-only.** The transition is recorded in a dated addendum in THIS record, appended below the last line, naming: the old value and the new value verbatim, the fields touched, `k`, the commit SHA, `H_body` before and after (equal), and the numstat at every boundary quoted in the table below. The addendum is the only place the transition may be described; **the front matter alone is never its own authorisation.**

And the gate that governs the flip, replacing the gate's clause (v):


### (d) THE FIGURES AT THE FLIP — THE RULE, AND WHAT IT YIELDS

State the rule and let the arithmetic fall out; never carry a number forward that was measured at some other boundary.

> **Rule F.** A lifecycle transition changes `k` excluded lines. In every boundary `B` whose range contains the transition, `numstat(B..HEAD_after) = ( ins(B..HEAD_before) + k , del(B..HEAD_before) + k )`, because a changed line is one deletion plus one insertion. **`H_legacy`** (the 22,270-byte L1-428 figure) changes exactly once per transition and is thereafter a historical value. **`H_body` never changes.**

Applied to the `PENDING` → `RUNNING` flip at `k = 1` (L5 only), from figures measured at `b7179f3`:

| Boundary | At `b7179f3` (measured by me) | After the `k=1` flip (Rule F) |
|---|---|---|
| `4478c3a..HEAD` | **1040 / 0** | **1041 / 1** |
| `ce845c5..HEAD` | **522 / 130** | **523 / 131** |
| `f450976..HEAD` | **267 / 36** | **268 / 37** |
| `8db1c45..HEAD` | **50 / 21** | **51 / 22** |
| `H_legacy` (L1-428, 22,270 B) | `b04fd5a4…00ce6` | `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144` |
| `H_body` (22,196 B) | `c7ebe54c…bea7` | `c7ebe54c…bea7` — **UNCHANGED** |

The `d8add61c…e6144` value is a **projection for the line-anchored L5-only edit and nothing else**, valid only from `b7179f3`'s bytes; it must be recomputed at the moment of the flip and never inherited. It is written down so that a reader who later finds a different value knows at once that something other than an L5-only edit happened.

**The boundary table above must be re-pinned before any flip — see Z3.** Its three figures (`1011/0`, `493/130`, `231/29`) are correct **at `8db1c45`**, R-0022's HEAD, and were correct as labelled. They are not the figures at any current HEAD, and nothing in the record says so.

### (e) HOW R-0019, R-0020, R-0021 AND R-0022 INTERACT WITH THIS

**Plainly: their integrity rulings STAND. They need no restatement. They are not superseded on substance, and they are not retroactively edited.**

All four hashed the front matter in — each computed SHA-256 over lines 1-428 *including their line terminators*, which necessarily included L5–L7. Each reported the true value of that function at its own HEAD, and each verified what it claimed to verify: R-0019 the pre-registration as filed; R-0020 the ten seams, the contingency table and the F-U items under its "move that text, not rewrite it" licence; R-0021 the L1-428 pair recomputed from two directions plus the baseline re-labelled at all three boundaries; R-0022 the same pair, all three numstats, and the residue ruled NON-BLOCKING.

**What changes is the contract, not the arithmetic.** `b04fd5a4…00ce6` remains the correct value of the *old* function, forever, and each ruling's claim — "the two sides are equal under the old function" — remains true for the pre-registration body indefinitely. The re-specification defines a *different* function, `H_body`, whose value is `c7ebe54c…bea7`. The old rulings say nothing about `H_body` and are not wrong about it, because they were not talking about it: the new function's exclusions fall entirely inside lines that R-0019 through R-0022 never modified, and the pair is equal on the new function today, at `ce845c5` and at `b7179f3` both.

**What is superseded is prospective only, and only on one point:** from the moment this contract is adopted, gate clause (v) is read as (v-a)/(v-b)/(v-c) above and the 22,270-byte figure becomes history. Before that moment it governed, and it was satisfied. **No ruling is amended, and none needs to be.**

> **Re-critique gate, clause (v) as re-specified by R-0023.** This record may leave `status: PENDING` for `status: RUNNING` only when a fresh adversarial-reviewer critique confirms, by recomputation, that **(v-a)** `H_body` is `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` on both `git show ce845c5:` and the working file, over 22,196 bytes; **(v-b)** the numstat of the transition commit is `k/k` with `k ≤ 5`; and **(v-c)** the transition commit changes no line outside {5, 6, 7, 10, 14}. The 22,270-byte figure is **no longer a gate**; it is retained above as history.

---

# RULING 2 — R-0022's six `old L…` table rows: NON-DEFECTS

**Answer: (i), with a correction to the framing — and the six need no action.**

The engineer's judgement was right, and I verified it rather than accepting it. The record **defines the convention itself** at L1162: *"Per-seam ledger. "before" is the `ce845c5` line numbering R-0020 cited; "after" is this file's current numbering."* Every `old L…` in the addendum is a "before" value, i.e. `ce845c5`-relative. I resolved all six against `ce845c5` directly and **each lands on exactly the text it names**:

| Row | As written | Resolves at `ce845c5` to | The sentence making the claim |
|---|---|---|---|
| L1187 | `old L871` | L871 = "`> it; B6) - so the backwards fallback is a latent trap…`" | L1195 calls it "the leading `it; B6)` of the author's tail (old L871…)" |
| L1195 | `old L871` | the same line | the same |
| L1215 | `old L960-L995` | L960 = "**Contingency table for '0.002 is undecidable at the measured `s_d`'. DECIDED HERE…**" | L1215: the table "moved from old L960-L995 to L682-L717" |
| L1218 | `old L1045-L1049` | L1045 = "4. **What SHRINK does buy, stated as the benefit…**" | L1218: "B1's cost item 4 (old L1045-L1049) rejoined items 1-3" |
| L1219 | `old L1068-L1073` | L1068 = "- **BUCKET 2 - PRE-REGISTERED, NOT RUN.**" | L1219: "BUCKET-2 and BUCKET-3 bullets (old L1068-L1073) rejoined BUCKET-1" |
| L1221 | `old L1073` | L1073 = "- **BUCKET 3 …** Decision: **SHRINK.**" | L1221 quotes it as "the old L1073 bullet "Decision: **SHRINK.**"" |

**Had R-0022's "correct" column been applied to them, every one would have been corrupted:** `ce845c5` L881 is blank, L970 is an unrelated X-2 branch, L1055 is an unrelated stage-vocabulary paragraph, and L1078 and L1083 do not exist. Applying the table as written to these six rows is precisely the corruption R-0022 §0c reason 1 exists to prevent.

**Was it (ii), an unflagged carve-out? No — and this is the part worth stating, because it is the difference between "the author nearly made a mistake" and "the author marked it, and the marker is imperfect."** R-0022 flagged the exemption **twice, in the right places**:

- in prose, at R-0022 L106–L107: *"Likewise the `old L871` / `old L960` / `old L808` references at L1187, L1195, L1215, L1216, L1217 are `ce845c5`-relative **by construction**"*; and
- in its own marker row, at R-0022 L135: `| L1187, L1195, L1215, L1216, L1217 | old L… values | **DO NOT TOUCH** |`.

So the carve-out was intended **and** marked. The 13-row table does not repeat the `old ` prefix in its "as written" column — a display convention the marker row itself uses — but it does not conflate numbering systems either: every one of the six rows' targets is a `ce845c5` line, and the "correct" column is simply the mechanical `+10` applied to a value that should never have been touched.

**One real, small, non-blocking defect does exist, and it is in R-0022's marker, not in E-0013.** R-0022's DO-NOT-TOUCH row is **inconsistent with its own table**: it names L1187, L1195, L1215, **L1216, L1217** — but the table's `old L…` rows sit at L1187, L1195, L1215, **L1218, L1219, L1221**. L1216 and L1217 do carry `old L808` and `old L809-L821` and are genuinely exempt, yet have **no row in the 13-row table at all**; and L1218, L1219 and L1221 are table rows that **do** carry exempt `old L…` values which the marker omits. The marker is right in substance and incomplete in its line list.

**Disposition.** R-0022 is CLOSED and is not edited. The six rows are **NON-DEFECTS, correct exactly as written, and no rewrite of any of them is authorised.** The one documentation defect is NON-BLOCKING and is dispositioned below and in E-0013's dated section, as R-0022 cannot be.



**Exact text to record in E-0013's dated section** (paste verbatim; R-0022 is CLOSED so this is the only place it can live):

> **R-0022 §0c's six `old L…` rows: disposition (R-0023, 2026-09-26).** R-0022's bounded rewrite table has thirteen rows. Six of them target `old L…` references — L1187 `old L871`, L1195 `old L871`, L1215 `old L960-L995`, L1218 `old L1045-L1049`, L1219 `old L1068-L1073`, L1221 `old L1073` — and **all six are NON-DEFECTS, correct exactly as written, and no rewrite of any of them is authorised.** I re-resolved each against `ce845c5` and each lands on the text it names (L871 on the `it; B6)` tail, L960-L995 on the contingency table, L1045-L1049 on B1's cost item 4, L1068-L1073 on the BUCKET-2/3 bullets, L1073 on the BUCKET-3 "Decision: **SHRINK.**" bullet), because this addendum defines `old L…` as `ce845c5`-relative at L1162. Had R-0022's "correct" column been applied to them, each would have been corrupted — `ce845c5` L881 is blank, L970 is an unrelated branch, L1055 is an unrelated paragraph, and L1078/L1083 do not exist. **Applying R-0022's table as written to these six rows is forbidden, and is the specific corruption R-0022 §0c reason 1 exists to prevent.** R-0022 flagged the exemption twice — in prose at its L106-L107 and in its own DO-NOT-TOUCH row at its L135 — so this is a marked carve-out, not an unstated one, and the S-0031 pass was right to leave all six standing. **One NON-BLOCKING documentation defect in R-0022 is recorded here rather than repaired, because R-0022 is CLOSED:** that DO-NOT-TOUCH row names L1187, L1195, L1215, L1216 and L1217, whereas the table's own `old L…` rows sit at L1187, L1195, L1215, L1218, L1219 and L1221 — it omits three rows it should have listed and lists two lines that have no table row. The marker is right in substance and incomplete in its line list; nothing in this record depends on it, because this disposition names all six by line and by value.

---

# NEW FINDINGS

## Z1 — **BLOCKING** — the Y1 qualification pass severed a sentence at L1376

`b7179f3` replaced L1377–L1386 to qualify the two over-broad "have been re-derived" claims. The hunk `@@ -1377,10 +1377,10 @@` began at the word **`shifted.`** — the last word of the *previous* sentence — and its replacement begins at `The cross-references written *by this repair*…`. The word was consumed.

At parent `8db1c45`:

```
1376| with the word `old`, and references to `ce845c5`, are a different numbering and are NOT
1377| shifted. The cross-references written *by this repair* - inside the withdrawal paragraph,
```

At `b7179f3` (HEAD):

```
1376| with the word `old`, and references to `ce845c5`, are a different numbering and are NOT
1377| The cross-references written *by this repair* - inside the withdrawal paragraph and inside
```

The file now asserts, in the normative disclosure of the pointer residue, that `old`-prefixed and `ce845c5`-relative references **"are NOT"** — and stops mid-sentence. Read literally, the surviving text says those references are *not what*. **The exemption itself, the single most load-bearing sentence in the +10 disclosure, is now an unfinished claim**, and the sentence it belonged to is the very one the Y1 pass existed to make true.

**This is the X1 defect class exactly** — a sentence severed at a block boundary — which is what R-0019's X1, R-0021's X4 and the ten seams were all about. It is introduced by the pass whose stated purpose was to make that paragraph TRUE, and it sits in the paragraph a reader consults *before* trusting any pointer in the file.

**It is structurally invisible to the audit the author ran, and that is worth recording rather than blaming.** I recomputed the per-hunk paren-delta audit over `git diff -U0 8db1c45..HEAD`: 11 hunks, every added block's delta equal to its removed block's, total 0, file-wide balance −10 at both `8db1c45` and `b7179f3`. The claim is accurate. But the L1377 hunk has paren delta 0 on both sides because **no parenthesis is involved** — a dropped *word* is invisible to a parenthesis-delta audit by construction. The audit's scope is parentheses; this defect lives outside it.

**Severity: BLOCKING.** Not because the intent is unrecoverable — the fix is one word — but because this record's own standard, applied five times inside this very addendum, is that an unfinished sentence is a defect to be repaired before the record may be read as normative, and because the severed sentence carries the exemption the whole Y1 disposition rests on.

**Exact repair** (one token, the author's own word, MOVED not retyped; paren delta 0; no other line in the file changes; L1377 is outside 1-428 so `H_body` is untouched): replace the single word `shifted.` — taken verbatim from `8db1c45` L1377 — onto the head of HEAD L1377, giving

```
shifted. The cross-references written *by this repair* - inside the withdrawal paragraph and inside
```

This is **not** a `+10` pointer rewrite and **not** a `ce845c5`-relative line; it is a restoration of severed text inside a block R-0022's table does not reach, so it needs no further ruling. Note that Z1 does **not** touch the qualification itself, which survived fully intact — only the sentence immediately before it was cut.


## Z2 — **NON-BLOCKING, must be corrected** — the commit message's projected post-flip hash is unreproducible

`b7179f3`'s message states the flip "moves the pair from `b04fd5a4...00ce6` to `8ad61ccd...00a727`". **No plausible scheme produces that value.** I brute-forced 30 schemes — L1-427 / L1-428 / L1-429 / L1-430, with and without the final terminator, CRLF, whole-file, front-matter-stripped, before and after the flip:

| Scheme | `H_legacy` (L1-428) |
|---|---|
| line-anchored L5-only, terminators included (the record's own stated method) | `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144` |
| the same with line 428's terminator dropped | `8e46e35092e10be027b708bf8eaf6782ad1080a8e3c711ba43c804a86c20a727` |
| naive all-occurrences replace, L1-428 | `6f9ace72933c1706333eec407ff179ea775dfcf8d87283b26d58b78ed341f532` |
| whole flipped file | `5fe92bcaeb945f2e0e8d23abf9ca52d467e0068401bda5860f05ac3c3a364b2c` |

Neither `8ad61ccd` nor `00a727` appears in any of them; `8ad61ccd...00a727` appears to splice the prefix of one scheme onto the suffix of another (`…a727` is the tail of the no-terminator variant). The substantive point — that the flip moves the pair — is correct and is what Ruling 1 clause (d) rules on. **The literal figure is not reproducible and must not be carried into the record.** Correct value: `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144`.

## Z3 — **NON-BLOCKING, must be corrected before the flip** — the boundary table is stale

The APPEND-ONLY BASELINE table at L1351–L1355 carries `1011/0`, `493/130` and `231/29`. Those are correct **at `8db1c45`** (R-0022's HEAD) and were correct under their column label, "Numstat after this R-0021 repair". They are **not** the figures at any current HEAD: `b7179f3` added the Y1 pass. Measured now: `4478c3a..HEAD` = **1040/0**, `ce845c5..HEAD` = **522/130**, `f450976..HEAD` = **267/36**. The label is defensible; the *silence* about which HEAD is not. The R-0022 disposition paragraph at L1447–L1450 reads as though the figures were current, and a reader consulting it for the flip would carry forward numbers 29 insertions stale. Re-pin the table, or add an explicit "measured at `8db1c45`; the current figures are …" line. This is the same class as the `288/127` mislabelling R-0022 already caught, one generation on.


# Cheap confirmations — re-derived, not inherited

- **The four Y1 pointers resolve.** `L1378`, `L1419-L1420`, and the substrings `L1419` and `L1411` are **absent file-wide** — zero grep hits for each. L1282, L1287 and L1411 now read `L1394`, which is the rejoined non-authorisation sentence ("…E-0013 remains `status: PENDING` - this repair is not authorisation to move it, and per R-0020 the flip requires a fresh re-critique to confirm."). L1300 now reads `L1432-L1436`, the "**Still not claimed.**" restatement. Both resolve to the right content by line-range read.
- **The two over-broad "have been re-derived" claims are qualified rather than deleted.** Confirmed by mechanism, not just wording: old claim and new qualifier are both present at L1377–L1386, the claim is narrowed in place ("…and those two families are the only ones that were"), and the falsehood is stated outright ("for four X4 pointers that was FALSE - R-0022 found them unresolvable - and they are fixed in place now"). Nothing was deleted. This is the one thing Z1 does not touch.
- **`L1106-L1114` → `L1117-L1125` is recorded as a PRE-EXISTING off-by-one, not +10 residue.** CONFIRMED at L1447–L1449. I confirmed the target: HEAD L1117–L1125 is the "**The decision.**" paragraph, L1117 opening it and L1125 closing "…no outcome of this run may be reported as a strength result." R-0022's stated reason — a uniform +10 gives L1116–L1124, still wrong — is correct, and the record does not pretend otherwise.

---
- **The 7 in-band rewrites resolve; no `ce845c5`-relative or `old L…` reference was altered.** Confirmed twice. (a) The seven targets resolve to the right content: L844 = the "2.5x headroom" seam-8 span; L881 = the "ARMED the E-0011 N1" span; L909 = the "**Relaxing (d) opens a live leakage**" span; L851 = the seam-8 sentence's tail; L919 = F-U1; L1117 = "The decision."; L944 = F-U4's `Owner:` line. (b) The per-hunk `git diff -U0` of `b7179f3` touches exactly 11 hunks, and the only lines whose content changed are those 7 pointer values, the 4 Y1 values, the L1377–L1386 qualification block, and the 29 appended lines. **No `old L…` value and no ledger "before"-column value appears in any hunk.**
- **L1-428 hash pair** — RECOMPUTED, not inherited: working file = `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6` over **22,270 bytes**; `git show ce845c5:` = the same. Equal, and equal to the claimed value. This value will legitimately change **once**, at an authorised lifecycle transition, under the re-specified contract — and to `d8add61c…e6144` if and only if that transition is the line-anchored L5-only edit. File is BOM-free, LF-only (0 CR), 110,796 bytes, 1,465 lines, single trailing newline.
- **E-0013 is still `status: PENDING`**, with `result: null`, `elo_change: null`, `completed: null`, and **nothing ran.** E-00014 and E-00015 both read `status: PENDING` / `result: null`. I ran no training, fitting, extraction, counting, feasibility pass or SPRT generation, and read no holdout.

---

# Corrections to the premises put to this seat

1. **"E-0011's numstat across that era is 146 insertions / 5 deletions" — NOT REPRODUCIBLE.** I searched every commit boundary in E-0011's history; no boundary yields 146/5. The figures that exist: `040296e` = **62/3**; `040296e~2..040296e` = 63/4; `027ea58..040296e` (pre-registration to close-out) = **316/4**; `027ea58..HEAD` = 333/4. **The precedent is unaffected and is in fact stronger** — `040296e` is a two-hunk front-matter edit in the same commit that appended an addendum, which is exactly the pattern E-0013 needs — but **the number quoted for it must not be repeated.**
2. **"The `4478c3a..HEAD = 1011/0` figure" — that figure is not a HEAD figure.** `1011/0` is the value **at `8db1c45`** (R-0022's HEAD). At `b7179f3` it is **1040/0**. The premise's conclusion — that it breaks at the flip — is right; its input is stale by 29 insertions. Rule F in clause (d) is therefore stated against the figures I measured, not the inherited ones.
3. **"The `4478c3a..HEAD` figure also breaks at the flip" — CONFIRMED, and worse than stated if the flip is done naively.** Line-anchored, it goes to `1041/1` and the "never had a deletion" claim survives as a bounded exception. Naive all-occurrences replace, it goes to **`1049/9`** and the claim is destroyed outright, because 8 of the 9 changed lines are quoted history. See clause (c) rule 1.

---

# THE FLIP — may E-0013 go PENDING → RUNNING on this ruling?

**NO. Not yet.** Not because the contract question is unresolved — Ruling 1 resolves it and supplies the exact text — but because **Z1 is a live BLOCKING defect** in the very paragraph that carries the pointer-residue disclosure, and because the gate's clauses (i)–(iv) are read against the file as it will stand at the moment of the flip.

**The flip is authorised on the following condition — all six parts, in this order, with parts 1–3 landing before the flip and the flip itself in its own final commit:**

1. **Repair Z1**, in its own commit: restore the single word `shifted.` to the head of L1377, verbatim as it stood at `8db1c45`. No other line changes. Paren delta 0. `H_body` unaffected (L1377 is outside 1-428).
2. **Adopt the re-specified contract** — clauses (a) through (e) above, verbatim — as a dated addendum appended below E-0013's last line, including the two computed `H_body` values, the five-line exclusion table, Rule F and its four resulting figures, the re-specified gate (v-a)/(v-b)/(v-c), and clause (e)'s statement that R-0019/R-0020/R-0021/R-0022 stand unamended.
3. **Re-pin the boundary table (Z3)** to the current HEAD — `4478c3a..HEAD` = 1040/0, `ce845c5..HEAD` = 522/130, `f450976..HEAD` = 267/36 — and record the `8db1c45` values as the historical column they are, so the table stops reading as a live claim.
4. **Record Z2's correction** in the same addendum: the reproducible post-flip `H_legacy` is `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144`; `8ad61ccd...00a727` is withdrawn as unreproducible.
5. **Record Ruling 2's disposition** in the same addendum, using the exact text given above.
6. **Then, and only then, a fresh adversarial-reviewer critique** confirms (v-a) `H_body` = `c7ebe54c…bea7` on both sides, (v-b) the flip commit's numstat is `1/1`, and (v-c) the flip commit touches no line outside {5}. Only that confirmation authorises the flip, in a **separate commit that changes L5 and nothing else**, made line-anchored and never by string replace.

**I do not flip the record, and no seat may flip it on the strength of this review's own claims** — the same rule the L1363 gate already states, which I endorse and am applying to myself.

**What is NOT re-opened by this ruling:** SHRINK, the KING-PST freeze, `SUITE_TOLERANCE = 0.02`, the per-game cap NONE, the X-1/X-2/X-3 branches, B1–B7, F1–F12, DN1–DN10, and integrity (i)/(ii)/(iii). All stand exactly as decided.


---

## Verification Block

Recorded per the close-out requirement, with raw commands, exit codes and hashes. **Environment contract observed throughout: `run_commands` in this session reports `Command exited with code 1` on commands that SUCCEED, so every exit code below is captured explicitly as `$LASTEXITCODE` into a file and read back, never inferred from the tool's own report.** All output was redirected with `| Out-File -Encoding utf8` and read from the file; `read_files` line-range staleness on large files was avoided by dumping numbered ranges to disk first.

### Commands re-run by me, with exit codes and observed output

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git pull --ff-only` | 0 | `Already up to date.` |
| 2 | `git status -sb` | 0 | `## master...origin/master`, tree clean |
| 3 | `git rev-parse HEAD` / `origin/master` | 0 | **both `b7179f3d9c336859d3dc6d38cd3eae12f9ca0a25`** |
| 4 | SHA-256 of L1-428, working file, terminators included | 0 | `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`, **22,270 bytes** |
| 5 | same from `git show ce845c5:` | 0 | `b04fd5a42d463bbb7044c18c7e54916aab852ff1965eafbb18642138d8200ce6`, **22,270 bytes** — **pair equal, and equal to the claimed value** |
| 6 | `H_body` (L1-428 minus lines 5,6,7,10,14), both sides | 0 | `c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7`, **22,196 bytes** on both — **pair equal** |
| 7 | `H_body` invariance: `status:` → RUNNING, → COMPLETED | 0 | both `c7ebe54c…bea7`, **SAME = True** |
| 8 | `H_legacy` after line-anchored L5-only flip | 0 | `d8add61cdd131644d37b25a555e5885d4b5a5d321deb202e543c251e7e9e6144` |
| 9 | brute force, 30 schemes, for `8ad61ccd…00a727` | 0 | **NO CANDIDATE MATCHES** prefix or suffix |
| 10 | `git diff --numstat` at 5 boundaries | 0 | `4478c3a..HEAD` **1040/0**; `ce845c5..HEAD` **522/130**; `f450976..HEAD` **267/36**; `d3ce887..HEAD` 201/29; `8db1c45..HEAD` **50/21** |
| 11 | `git diff --numstat` at `8db1c45` (dates the record's table) | 0 | `4478c3a..8db1c45` **1011/0**; `ce845c5..8db1c45` **493/130**; `f450976..8db1c45` **231/29** — **confirms Z3** |
| 12 | `git diff --no-index --numstat`, HEAD copy vs flipped copy | 1 (=differs) | **`9 / 9`** — the naive replace; 9 lines, 8 of them quoted history |
| 13 | `git show 040296e -- <E-0011 path>` | 0 | `@@ -3,6 +3,6 @@` L5 `RUNNING`→`COMPLETED`, L6 `null`→`PASS`; `@@ -12,5 +12,5 @@` L14 → `2026-09-24` — same commit appends the addendum at L457 |
| 14 | `git log -S 'status: COMPLETED' -- <E-0011 path>` | 0 | exactly `040296e` |
| 22 | R-0022 §0c L98–L145 read | 0 | exemption stated in prose at L106–L107 **and** in a DO-NOT-TOUCH row at L135; the marker names L1216/L1217 while the table's rows are at L1218/L1219/L1221 — **Ruling 2's non-blocking defect** |
| 23 | E-0013 ledger L1160–L1232 read | 0 | L1162 defines `old L…` as `ce845c5`-relative; all six refs verbatim at L1187/L1195/L1215/L1218/L1219/L1221 |
| 24 | HEAD in-band rewrite targets L844, L881, L909, L851, L919, L1117, L944 | 0 | all seven resolve to the content the ledger claims |
| 25 | grep `L1378`, `L1419-L1420`, `L1419`, `L1411` file-wide | 0 | **zero hits for each**; L1282/L1287/L1411 now `L1394`, L1300 now `L1432-L1436`, both confirmed by line-range read |
| 26 | file hygiene | 0 | **no BOM, 0 CR bytes, single trailing newline, 110,796 bytes, 1,465 lines** |
| 27 | E-0013 front matter L1–L16 | 0 | L5 `status: PENDING`, L6 `result: null`, L7 `elo_change: null`, L10 `owner: null`, L14 `completed: null` — **PENDING, not flipped** |
| 28 | E-00014 / E-00015 front matter | 0 | both `status: PENDING` / `result: null` — **neither ran** |
| 29 | `research.py validate` (before `update`) | 1 | only `audit[state]: state.json is stale: stored records_total=188, live=189` — expected, one new record |
| 30 | `research.py update` | **0** | `updated: research/index.md` |
| 31 | `research.py state --write` | **0** | `wrote research/state.json and research/state.md` |
| 32 | `research.py validate` (after) | **0** | **PASS** — warnings only, all pre-existing and grandfathered |
| 33 | `git diff --check` | **0** | empty — no whitespace damage |

### What I reproduced independently

Everything numeric in this record. The L1-428 hash pair (both sides, byte count included); the new `H_body` pair and its lifecycle invariance; all five boundary numstats at HEAD **and** at `8db1c45`; the post-flip `H_legacy` projection; the negative result on `8ad61ccd…00a727`; the E-0011 lifecycle history at L5 across all seven commits that touched it; the six `ce845c5` resolutions **and** the six counterfactuals showing the table's "correct" column would corrupt them; the 11-hunk paren-delta audit; the four Y1 pointer substitutions; the seven in-band targets; file hygiene; and both `E-00014`/`E-00015` remaining unrun.

### What I could NOT reproduce, and why

1. **`8ad61ccd...00a727`** — 30 schemes tried, no match. Recorded as Z2 and withdrawn, not repaired.
2. **"E-0011 146 insertions / 5 deletions"** — no boundary in E-0011's history yields it. The precedent itself reproduces; the figure does not.
3. **The L1351–L1355 boundary columns** are not current-HEAD figures and cannot be reproduced against HEAD; they reproduce exactly at `8db1c45`. Recorded as Z3.

### Claims that must be corrected in the record

- **Z1 (BLOCKING):** restore `shifted.` to the head of L1377.
- **Z2:** `8ad61ccd...00a727` is unreproducible; the value is `d8add61c…e6144`.
- **Z3:** the L1351–L1355 boundary table is `8db1c45`'s; re-pin to 1040/0, 522/130, 267/36 or label the HEAD.
- **The orchestrator's two premises:** the 146/5 figure, and the characterisation of `1011/0` as a HEAD figure.

### Residual uncertainty (calibrated)

**Demonstrated** — the hash pair, `H_body` and its invariance, the numstats, the E-0011 precedent, the six `ce845c5` resolutions, the paren-delta audit, the four Y1 pointers, the file hygiene, the PENDING state, and Z1 itself (a one-word diff, read on both sides).

**Strongly supported** — that Z2's figure is a splice of two schemes rather than a hash of a scheme I did not try; that a naive flip is the realistic failure mode for the next seat, being one `sed` away.

**Unknown** — whether the owner's intent behind "lines 1-428 byte-identical" was ever to freeze the lifecycle fields, or whether L1-428 was chosen as a convenience boundary. I rule on the specification as written, which is the only thing I can rule on; if the owner meant the stronger reading, Ruling 1(a) is the wrong fix and the record should say so explicitly rather than leave the stronger reading available by silence.

### Scope discipline — what I did NOT do

Did not re-litigate SHRINK, the KING-PST freeze, `SUITE_TOLERANCE`, the NONE cap, the X-1/X-2/X-3 branch design, or any DISCHARGED finding. Did not edit E-0013, E-00014, E-00015, R-0019/20/21/22, any handoff, or any `H-####`. Did not flip E-0013. Did not open or close HO-0005 or W-0003. Did not run training, fitting, extraction, counting, feasibility passes or SPRT generation. Did not read the holdout. Did not touch `research/state.md` or `state.json` by hand (GENERATED — only via `state --write`).

| 15 | E-0011 L5 at every commit touching the file | 0 | `027ea58`/`6d507d8`/`5026fb5` PENDING → `9d60f64` RUNNING → `040296e`/`f67fe35`/`0d8fbce` COMPLETED — **in-place at L5, all three** |
| 16 | E-0011 numstat, all boundaries, searched for 146/5 | 0 | **no boundary yields 146/5**; actual `62/3`, `63/4`, `316/4`, `333/4` |
| 17 | `git show b7179f3 -U0 -- <E-0013 path>` | 0 | 11 hunks; hunk `@@ -1377,10 +1377,10 @@` removes the leading `shifted.` — **Z1** |
| 18 | per-hunk paren-delta audit over `git diff -U0 8db1c45..HEAD` | 0 | 11 hunks, every added delta == its removed delta, **total 0**; the L1377 hunk is 0/0 because no parenthesis is involved — **Z1 is outside this audit's scope** |
| 19 | file-wide paren balance at `8db1c45` and HEAD | 0 | **−10 both**, unchanged |
| 20 | `git show ce845c5:` L871 / L960-962 / L1045-1047 / L1068-1070 / L1073 | 0 | each is exactly the text the `old L…` refs name — **Ruling 2 (i)** |
| 21 | same targets at R-0022's "correct" values | 0 | L881 blank, L970 unrelated, L1055 unrelated, **L1078/L1083 do not exist** |

## Date
2026-09-26

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns.


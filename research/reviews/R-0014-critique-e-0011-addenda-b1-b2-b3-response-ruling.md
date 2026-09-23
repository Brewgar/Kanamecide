---
id: R-0014
type: review
reviewer: adversarial-reviewer
target: E-0011
kind: critique
status: COMPLETED
work_item: W-0001
related: [E-0011, R-0011, HO-0006, W-0001, EV-0001, DEC-0010]
example: false
created: 2026-09-23
---

# R-0014 — Re-critique of E-0011's R-0011 addenda (HO-0006)

## Scope

HO-0006, adversarial-reviewer seat, S-0012. Ruling on **only the dated 2026-09-23 addenda**
(original text verified untouched: `git diff 027ea58 6d507d8` shows a single append block
`@@ -203,3 +203,191 @@`, pure `+` lines). My own R-0011 findings are the checklist; I
re-critique per finding with evidence. Evidence commands + outputs in the appendix.

**Gate 0 is OPEN as of today (attempt #11, my run):** `"quit" | build\Release\kana.exe` →
exit 0, exact perft outputs, final line `=== ALL TESTS PASSED`. Consistent with the architect's
flag (now in E-0011's addendum text): the piped `'quit'` token did NOT enter UCI — the binary
ran its default perft harness. This session answers "does a binary run at all", not "is UCI
wired"; the addendum's UCI-entry note (N-block) is the route for the build session.

## Rulings per finding

### B1 — **FULLY DISCHARGED**

Quoting the addendum (B1.1): dataset identity fields are now a deliverable of Test-Method step
5 and of W-0001's exit check, "not 'once they exist'":

```
dataset_sha256: <SHA-256 of the final games JSONL bytes>
dataset_n_games: <integer, must equal gate (a) count>
dataset_path:    <local gitignored JSONL path>
```

And (B1.2) defines the three client obligations on the future Tier-R experiment:

> - (a) **Distinct salt:** … MUST differ from BOTH E-0011's `20260922` and E-0010's
>   `20260914`. … 8,000,024 ≫ any game index …
> - (b) **Machine gate `training_game_overlap = 0`:** the future experiment's aggregator MUST
>   rebuild every fresh game's full move list under the SAME normalization gate (c) uses
>   (`tuple(opening) + tuple(san)`) and check every one against the pinned E-0011 dataset
>   (`dataset_sha256` above) … **= 0 is a gate** — reported in the experiment record, not
>   merely asserted.
> - (c) **`fitted_params_sha256`:** the future experiment MUST record the SHA-256 of the fitted
>   parameter artifact … so "retrain, then retest, then report the good run" is visible as a
>   hash change between attempts.

This is enforceable-by-field, not by-good-behaviour: the machine gate is a computed count with
a named (executable) normalization — the same `tuple(opening)+tuple(san)` key the dedup gate
and the w0005 replay already implement — against a dataset whose identity is pinned by hash and
count. "or its verdict is void" gives it teeth, and the verification-auditor seat enforces the
cross-experiment side exactly as it enforces every other DEC-0009 gate (wheel: W-0003/HO-0005).
The chain dataset_sha256 → training_game_overlap=0 → fitted_params_sha256 closes the leakage
loop: regenerating the training set, retraining after seeing the test, or reusing training
games for testing each surfaces as a hash change or a non-zero count.

### B2 — **FULLY DISCHARGED**

Every clause I asked for is pinned:

> **(B2.1) Kill boundary.** The live mid-campaign kill MUST occur in the pre-registered window
> **game [400, 600] of 1,000** … A kill outside the window is recorded as a protocol deviation
> and gate (e) is then evaluated on the deterministic drill alone (B2.4).

> **(B2.2) Presence test on resume.** A game counts as *present in the checkpoint* only if its
> trailing JSONL line (i) parses as JSON, (ii) carries EVERY mandatory Dataset field per gate
> (d)'s schema, and (iii) has a `game_id` in the dense expected range. "An id appears on a
> line" is explicitly NOT the test …

> **(B2.3) Torn-write policy — quarantine, never silent truncate.** … (ii) if not, move that
> partial line verbatim to `<games>.jsonl.torn` (sidecar, append mode across incidents) and
> record a `torn_line_quarantined` incident (recoverable game_id, byte offset, timestamp) in
> the run log; (iii) re-emit the affected game under its OWN id … In-place truncation is
> prohibited …

> **(B2.4) Deterministic kill→resume drill — a pre-registered acceptance step** … assert —
> torn line quarantined + incident logged, all pre-truncation games intact, the truncated game
> re-emitted exactly once under its own id, duplicate-move-lists = 0, and final valid count =
> pre-truncation valid count + resumed games.

> **(B2.5) Log-preservation rule** … before any `runjob.py resume`, the operator copies the
> pre-resume log to `run.log.<UTC-timestamp>.preserved` and names both files in the RUN record
> … No `research/scripts/` change is made (selftests stay green) … runjob counts are telemetry,
> never an integrity signal — only `tools/e0011_check.py`'s parsed-line counts are
> authoritative.

On the policy-over-code choice (architect declined a `research/scripts/` edit): sound, on three
grounds. (i) `runjob.py` is shared tooling whose selftests must stay green against a frozen
build; (ii) "operator must copy the log before resume" is now an *evidence-auditable* protocol
step because the RUN record MUST name the preserved file — a missing `<UTC>.preserved` is a
provable protocol violation at review time, which is the enforcement level the rest of
DEC-0009's protocol runs at; (iii) the harness's `tools/e0011_check.py` is now named the
authoritative counter, so the runjob `splitlines()` inflation trap I observed is documented and
inert. My B2 finding was never a demand for a byte of `runjob.py` — the policy is sufficient.

### B3 — **PARTIAL: discharged as written, but the HO-0006-ordered spot-check exposes ONE new blocking finding**

The addendum gives gate (d) every conjunct I listed — values, not just presence, with an
unmissable posture ("any failure = FAIL of gate (d), named per check"): `binary_sha256`,
`src_commit`, stages, salt, `res`, `end` vocabularies, `plies>0`, timestamp ordering,
`a_white` boolean + parity, `game_id` dense **0-based**, and the seed↔opening re-derivation is
now *inside* the gate. Gate (f) re-routed to the reviewer with a named command requirement
(executed below). And my Proposed Experiment 2 is adopted as a pre-registered build acceptance
step — quoting:

> "**Before any live run**, the build session MUST run `tools/e0011_check.py` over a synthetic
> 20-game JSONL containing (i) one torn line, (ii) one wrong-hash game, (iii) one duplicate id,
> and show the aggregator FAILing all three with the named conjuncts."

Not a someday note: a build-acceptance step, with the synthetic fixture still engine-free.

**Spot-check vs EV-0010 (required by HO-0006; `ConvertFrom-Json` over all 1,240 retained
games, read-only):**

| Element | Conjunct says | EV-0010 shows | Match? |
|---|---|---|---|
| `res` | ∈ {A,B,D} | `res={A,B,D}` on all six rungs | ✓ |
| `a_white` | boolean, parity-alternating | 0 non-bool, 0 parity violations (`a_white == (g%2==0)`) | ✓ |
| `game_id` | unique, dense, 0-based | 0..N−1 dense on all six rungs | ✓ |
| `end` | ∈ {mate, rule50, repetition, plycap, crash} | **stalemate** (k2n, k5n) and **draw-material** (all six rungs) present; every value carries an `(Ns)` suffix | ✗ |

The declared `end` set is not closed over reachable endings of the fork family:

1. **Vocabulary under-closure.** Insufficient material (`draw-material(Ns)`, 33 games across
   the retained evidence) and stalemate (`stalemate(Ns)`, k2n/k5n) are legal python-chess
   terminals with no label in the declared set — yet the record's own emission format
   (forking `e0010_match2.py`) has historically produced them. Records like these are
   perfectly legal games; under the addendum's text they have no legal `end` label: the
   generator must either mislabel them (gate (d) passes on a provenance lie, hidden) or emit a
   non-vocab token (gate (d) FAILs a healthy campaign, as written). The sentence that resolves
   it belongs in the record before the build session starts.
2. **Suffix policy missing.** Every retained evidence value carries a trailing `(Ns)` seconds
   suffix (`mate(8s)`, `plycap(20s)`). The declared set carries no suffix policy. If the fork
   inherits the emission bytes, every game fails gate (d) (set-membership of a suffixed string
   is precisely the kind of false FAIL I warned against). Either strip the suffix at emission
   or promote it to a distinct field — the record must pick, explicitly.

The exact missing sentence (only this sentence blocks E-0011 today):

> The `end` field's closed set is extended to `{mate, stalemate, draw-material, rule50,
> repetition, plycap, crash}` — and the record declares whether the `(Ns)` seconds suffix is
> part of the token or a separate `end_seconds` field; the Dataset section's `end` schema line
> and the B3.1 conjunct agree with the extended set.

### N1–N7 + Gate-0 UCI note — **DISCHARGED**

Every N-item landed as record text: measured yield replaces the ASSUMED prior (my
130.3 plies/game ⇒ 130,335 positions/1,000 games and quiet-proxy 76,887/1,000 cited), and the
consequence ladder is pinned at <30k usable positions (scoped refit, no all-terms claim);
provenance scoped ("audit- and legality-reproducible from the JSONL … not bit-reproducible by
re-running the engine"); TC pre-registered (100ms+100ms, ≤2 pairs, single `tc_command`
asserted); `san` pinned as post-opening engine moves; end-mix reporting mandated (with my
1.6% degenerate count in the retained evidence); the colour diagnostic is a report against my
58.5% prior, with a 50%-centred band explicitly prohibited ("an F6-class defect in reverse");
RUN-0001 reservation explained. UCI-entry note present verbatim (piped-token probe → default
perft harness, not UCI; build session MUST confirm the UCI entry path and record the working
invocation in the RUN record) — the flag survived into E-0011's text.

### Gate (f) — route executed by me, evidence-stamped: PASS for the record as it stands

Per the addendum (B3.2), the re-critique reviewer (HO-0006) MUST search Results / Statistical
Analysis / Interpretation / Conclusion for Elo/LOS/CI strength assertions and record the
command + output. My command:

```powershell
$lines = Get-Content research/experiments/E-0011-*.md
# section-scoped filter: only inside '## Results' / '## Statistical Analysis' /
# '## Interpretation' / '## Conclusion'; patterns: Elo|LOS|CI95|\bCI\b|significan
# (the four sections are TBD; Follow-Up/Addenda are outside the scope)
```
Output:
```
GATE-F: 0 strength-assertion lines in Results/Statistical Analysis/Interpretation/Conclusion
```
All four sections are TBD and gate (f)'s assertion is, if anything, *stronger* than a silent
file: it rules out a claim *before* it has a home (Results). The follow-up verifier repeats
the same command at campaign close; the route is machine-tied.

## Disagreements

One: the `end` vocabulary (B3-new, above). Everything else is agreement with evidence.

## Missing Arguments

None on the addenda as filed. (This is the first E-0011/E-0012 pair where the
checksum/provenance chaining bottoms out in something executable end-to-end.)

## Factual Errors

None in the new text that change any verdict. One cosmetic nit: the UCI-entry parenthetical's
backtick spans read awkwardly; no action needed.

## Assumptions

None new. The ruling leans on the EV-0010 read-only spot-check and the addenda text; no engine
claims are made here.

## Proposed Experiments

1. Fix the B3-new sentence (one line, Dataset + B3.1) at the TOP of the next session; then the
   build session can start. This is the ONLY required edit.
2. Next session: build `tools/e0011_generate.py` + `tools/e0011_check.py`, run the
   pre-registered synthetic-20 FAIL demo + the deterministic truncation drill, and confirm the
   UCI entry path. Then the 1,000-game E-0011 campaign under `runjob.py`.
3. E-0012's live validation (v1)–(v4) and the adopted N4 null-pair control run from the same
   recording session (see R-0015).

## Verdict

**PARTIAL — the R-0011 B1/B2/B3 remediation passed as written, but the HO-0006 spot-check
(EV-0010 vs GATE-(d)'s value conjuncts) exposes ONE new blocking finding: the `end` vocabulary
is not closed over the harness family's reachable endings (missing stalemate & insufficient
material & the `(Ns)` suffix rule). One sentence fixes it.** E-0011 stays **PENDING** on exactly
that sentence — nothing else blocks.

## Date

2026-09-23

> A review never edits the original report — it lives here and is linked from the debate/report
> it concerns.

## Evidence appendix

1. "Original untouched": `git diff 027ea58 6d507d8 -- research/experiments/E-0011-*.md` → one
   append hunk `@@ -203,3 +203,191 @@`, pure additions.
2. Gate 0 (attempt #11, mine): `"quit" | build\Release\kana.exe` → exit 0, all perft rows exact,
   `=== ALL TESTS PASSED`. Logged to `research/context/bootstrap/gate0.txt`.
3. Spot-check (my script, `%TEMP%\krev12\spotcheck.txt`): Python `json` loop over
   `e0010_k{1..6}n_games.jsonl` → per-rung output row shows `res={A,B,D}`, `dense0=True`,
   `nonbool_a_white=0`, `parity_violations=0`, and `ends={... draw-claim(Ns) / draw-material(Ns)
   / stalemate(Ns) ...}` on every rung. (Numbers: draw-material 33/1,240; stalemate 2/1,240.)
4. Gate (f) route: my PowerShell section-scoped search of E-0011 →
   `GATE-F: 0 strength-assertion lines in Results/Statistical Analysis/Interpretation/Conclusion`.
5. `python research/scripts/research.py validate` → exit 0, "Validation OK … 0 problems"
   (warnings only — legacy; `RUN-0001` still dangling per N7's reservation note).

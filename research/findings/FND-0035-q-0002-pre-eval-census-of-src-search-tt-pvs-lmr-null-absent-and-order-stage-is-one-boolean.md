---
id: FND-0035
type: finding
title: "Q-0002 pre-eval census of src/search.cpp|tt.cpp: PVS/aspiration/LMR/null-move/futility are ALL absent; ordering+qsearch exist; ORDER_STAGE is one boolean so E-0007's per-lever attribution is NOT reproducible from current source"
severity: blocking
target: Q-0002
raised_by: search-researcher (research seat; census pass, 2026-10-03)
review: E-00007
status: OPEN
resolution: ""
resolved_by: ""
verified_by: ""
example: false
created: 2026-10-03
last_updated: 2026-10-03
---

# FND-0035 — Q-0002 pre-eval census of the O3d search stack

## Scope and discipline

Read-only census. **No `src/` file was edited.** HEAD at census time: `82ac6fe` (master).
This census is deliberately scheduled *before* any eval-fitting verdict so the Q-0002 pruning
deltas are not contaminated by a moving eval.

## Finding 1 (BLOCKING) — `ORDER_STAGE` is one boolean, so E-0007's attribution is unreproducible

`src/search.cpp:190-191` is the **only** consumer of the stage macro:

```cpp
if (ORDER_STAGE >= 4 && n > 1)
    std::stable_sort(sm, sm + n, [](const ScoredMove& x, const ScoredMove& y) { return x.s > y.s; });
```

So `ORDER_STAGE` 0, 1, 2 and 3 are **all identical** (no sort at all); only `>= 4` sorts.
Meanwhile `score_move` (`:102-108`) unconditionally computes all four ordering terms
(TT/PV, MVV-LVA, killers, history) at every stage. Consequences:

- `-DORDER_STAGE=2` ("MVV-LVA only") does **not** disable killers/history; it disables the
  *entire* sort. The staged-lever semantics in `CMakeLists.txt:8`
  (`0=unordered,1=PV,2=MVV-LVA,3=killers,4=history`) are **not implemented**.
- `EV-0005` (`research/evidence/EV-0005-o3b-ordering-node-table.md:21`) publishes
  `254,655,158 -> 254,655,158 -> 40,869,716 -> 24,095,495 -> 22,534,970 (-91.2%)`.
  stage0 == stage1 is consistent with the current gate, but **stage2/3/4 differing is not
  producible by the current source** — all four would collapse to the stage-0 number.
- Therefore E-00007's per-lever attribution, which **Q-0002:34 cites as its own premise**
  ("MVV-LVA is the dominant ordering lever (84%), killers +6.5pp, history +0.7pp"), is
  **not reproducible from `src/search.cpp` as it stands**.

**Routing:** the Q-0002 ladder must re-measure the ordering baseline (stage 0..4) with the
current binary as rung 0, before any pruning delta is quoted against it.

## Census table — what actually exists today

| Feature | Exists | Evidence | Parameters as implemented |
|---|---|---|---|
| Plain fail-soft alpha-beta | **YES** | `search.cpp:200` (interior), `:286` (root) | window `(-beta, -alpha)` |
| **PVS / null-window re-search** | **NO** | only two `negamax` call sites (`:200`, `:286`), both full-window; no re-search anywhere | — |
| **Aspiration windows** | **NO** | `:279` re-initialises `alpha=-INF, beta=INF` every iteration; no `prev_score`, no delta | — |
| **LMR / depth reduction** | **NO** | `:200` passes `depth - 1` unconditionally; no reduction table/macro | — |
| **Null-move pruning** | **NO** | no null-move construction in `src/`; "nullmove" strings in-repo are python drivers detecting `bestmove 0000` | — |
| **Futility pruning** | **NO** | zero matches for `futility` repo-wide | — |
| **SEE** | **NO** | ordering is MVV-LVA only (`:104`) | — |
| Check extensions | **NO** | `in_check` used only for terminal detection (`:217`) and qsearch evasion (`:124`) | — |
| Ordering — TT/PV move | **YES** | `:180` locate `tt_move` in the fresh list, `:186-187` score `SCORE_PV+1` | `SCORE_PV = 4,000,000` (`:31`) |
| Ordering — MVV-LVA | **YES** | `:104` + `mvv_lva` `:85-94` | `10*victim - attacker`; `VALUE` from `:28` |
| Ordering — killers | **YES** | `:37`, `:105-106`, `:206` | 2 slots/ply; slot0 gets `+1` |
| Ordering — history | **YES** | `:36`, `:107`, `:207` | `+= depth*depth`; **no clamp, no aging, no decay** |
| Sort | **YES, see Finding 1** | `:190-191` | one threshold `ORDER_STAGE >= 4`, `stable_sort` desc |
| qsearch | **YES** | `:113-155`, entered `:163` under `QSEARCH` (default 1) | stand-pat `:116-120`; captures+promos+EP `:127`; sorted by capture value `:130-131`; all evasions in check `:127`; `-MATE` if none `:153` |
| qsearch delta pruning | **NO** | E-00008 claims `DELTA_MARGIN(200)`; the constant exists only in `_obs/`, **not in `src/`** | — |
| qsearch TT | **NO** | no `tt_probe`/`tt_store` in `qsearch` | — |
| qsearch ply cap / repetition | **NO** | `qsearch` takes no `ply`; `:141` recurses unbounded; no `count_reps` inside | — |
## Finding 2 (HIGH) — unbounded, repetition-blind qsearch recursion

`qsearch` (`search.cpp:113`) takes **no `ply` argument** and recurses at `:141` with no depth
cap, no repetition check and no halfmove check. The "all moves when in check" branch (`:127`)
means a perpetual-check sequence is searchable inside qsearch. Under `MAX_PLY = 128` (`:34`)
this is a stack-overflow / non-termination path reachable from live play in draw-ish
positions. Under `DEC-0010`'s crash/stall rule a crash is a **loss**, so this is both a
robustness defect and a measurement-integrity hazard for any SPRT campaign on this binary.

## Finding 3 (MEDIUM-HIGH) — stand-pat fail-high is not guarded by `in_chk`

`search.cpp:118` runs `if (sp >= beta) return beta;` **before** `in_chk` is computed at
`:124`. A side to move that is in check cannot stand pat, so this can return a fail-high on
an in-check node. E-00008's own contract states the opposite ("stand-pat `evaluate()`; fail
high if `>= beta` **(only when NOT in check)**"). The guard described in the accepted record
is **absent from the code**. Score error in check; can mask mates.

## Finding 4 (MEDIUM) — `go nodes N` is per-iteration, not cumulative

`search_root` resets `uint64_t it_nodes = 0;` **inside** the depth loop (`:275`) and passes
*that* reference into `negamax` (`:286`), while the reported counter accumulates separately
at `:296` (`nodes += it_nodes`). `stopped()` compares `node_limit` against the `nodes` it
was handed (`:66-68`) — i.e. **one iteration's** count. So `go nodes N` stops when a single
iteration reaches N nodes, not when the search total does.
**Design consequence: the node-delta tier must use `go depth D` (cumulative), never
`go nodes N`.** The `(nodes & 2047) == 0` gate (`:60`) also permits up to 2047 nodes of
overshoot.

## Finding 5 (HIGH, for the design) — two hardcoded copies of the material values

`search.cpp:28` declares its own `VALUE[6] = {100,320,330,500,900,20000}`, independent of
`eval.cpp:35`'s `FLAT_VALUE[6]` (byte-identical today). `VALUE[]` drives MVV-LVA (`:93`) and
qsearch capture ordering (`:96-100`). **An E-0013 Texel refit changes `evaluate()` but leaves
`VALUE[]` untouched**, so a re-tuned eval would silently ship with ordering tuned to the
*old* material values. This is the concrete mechanism by which an eval change mid-program
invalidates Q-0002 deltas — structural, not hypothetical.

## Finding 6 (LOW) — dead / suspicious code (recorded, NOT fixed)

1. **Dead condition, `search.cpp:287`** — `if (sc > it_score || (it_best == 0 && sc > -INF))`.
   `it_best == 0` implies `it_score == -INF`, so `sc > it_score` already subsumes
   `sc > -INF`. The second disjunct is unreachable.
2. **Redundant TT-move scoring, `:186-187`** — `score_move(..., tt_move)` already returns
   `SCORE_PV` for the TT move at `:103`; `:187` then overwrites with `SCORE_PV + 1`.
3. **Misleading parameter name** — `score_move`'s 4th parameter is named `pv` (`:102`) but
   receives the **TT move**, not a PV. There is no PV table in the engine.
4. **Double TT clear** — `search_root:265` calls `tt_clear()` on every `go`, and
   `main.cpp:121` calls it again on `ucinewgame`. Each is a 64 MiB `memset` per move.
5. **Stale rationale, `main.cpp:185-188`** — the comment justifies the extra `- 40` time
   margin by "the shared TT thrashes", which cannot occur while the TT is cleared every move.
6. **Unbounded history, `:207`** — `+= depth*depth` with no clamp. The O3b report says
   "bumped by depth^2, **clamped**"; the clamp is not in the code. History never decays, so
   early-search bias persists for the whole search.
7. **`:325`** — `pv_out = build_pv(b, max_depth)` uses the *target* depth, not the achieved
   depth; on a stopped search the PV can be longer than what was actually searched.

## What the census means for Q-0002

Q-0002 asks for measured deltas of **PVS, TT, LMR, null-move** on this engine. Census
answer: **three of the four do not exist** (PVS, LMR, null-move); aspiration and futility do
not exist either. **TT does exist** but its *marginal* contribution given ordering + qsearch
+ ID is unmeasured. So Q-0002 is not a four-way ablation of existing code — it is a
**three-feature build** plus one TT-ablation measurement, and the ladder must re-baseline
ordering first (Finding 1).

---
| Transposition table | **YES** | `tt.cpp:52-70` probe, `:72-79` store | 2-entry buckets `:28-30`, 64 B/bucket, **replace-always** `:77-78` |
| TT mate-score shifting | **YES** | `tt.cpp:14` `MATE_BOUND=900000`, `mate_to` `:17-21`, `mate_from` `:22-26` | ply-relative |
| TT bound gating | **YES** | `tt.cpp:60-64` requires `e.depth >= depth` and a consistent bound | depth-gated |
| TT aging | **NO** | E-0009 `:44` claims "aging/shift replacement policy"; code is replace-always | — |
| Iterative deepening | **YES** | `:274-316` | 1..max_depth; previous best raised to front `:277-278` |
| Time control / stop | **YES** | `stopped()` `:58-71`; `main.cpp:180-191` | `our_time/30 + inc - 90`; checked every 2048 nodes `:60` |
## One-at-a-time ablation SPRT design (pre-registration skeleton)

Governing rules cited, not re-derived: `DEC-0010` (tiers, sigma=371 at 100ms+100ms inc, caps
8k/30k/8k, LLR ±2.9444, crash=loss, post-cap INCONCLUSIVE, one-look) and the validated
harness `tools/e0012_sprt.py` (E-0012, harness-validation PASS; `tools/e0012_sprt.py:28-38`
carries the same tier constants, `TC = "100ms+100ms inc"`, `N_OPEN=10`, `MAX_PLIES=300`).

### A. Two-tier measurement split (Q-0002 explicitly sanctions this)

- **Tier N (node/TTD, no SPRT).** Fixed-depth node counts on the frozen 11-position set
  (`research/positions/act_E00007.fen`, driver `measure_ob.py`, depth 6). Deterministic,
  minutes of wall-time, no strength claim. **This is where most of Q-0002's value is.**
  Uses `go depth 6` — **never `go nodes`** (Finding 4).
- **Tier S (strength, SPRT only).** Run only on the winners of Tier N. Reuses
  `tools/e0012_sprt.py --tier S` unchanged, with a fresh salt.

### B. Harness arm-differentiation problem (must be solved before any run)

`e0012_sprt.py` accepts **one `--exe`** and differentiates arms only by an integer
`setoption name EvalStage value K` (verified in `R-0019`: `tools/e0012_sprt.py:325-326`; a
single `binary_sha256` is recorded for both arms). Every Q-0002 ablation is a **different
binary**, so the validated harness cannot express these comparisons as written.

Two options, pre-registered decision:
- **(i) Extend the harness to two binaries** (`--exe-a/--exe-b`, record both digests, assert
  `sha_a != sha_b` before game 1). This changes a **verified** tool and therefore re-enters
  the verification chain (DEC-0009 gate 3; the verifier is never the owner). Requires its own
  known-difference + null-pair control before any ablation verdict counts.
- **(ii) Express each ablation as a UCI option** (like `EvalStage`/`Hash`), keeping one binary.
  Cheaper, but adds hot-path branching and a new UCI surface — and per `d8ce4aa_e13.md:535-539`
  this project already declined a parameter surface on exactly this cost argument.

**Recommendation: (i).** These features are compile-time by construction (they change the
search, not the eval), and option (ii) puts a branch in the hottest loop of every node for
something that is compile-time-expressible.

### C. Rung order (one at a time, no cumulative confounding)

| # | Rung | Feature | Why here |
|---|---|---|---|
| **0** | **ORDER re-baseline** | `ORDER_STAGE` 0..4 re-measured on current source | **Mandatory.** Finding 1: E-0007's table is not reproducible. Every later delta is quoted against this. |
| 1 | **TT-only** | `USE_TT=0` vs current | Cheapest ablation, already implemented, no new code. Answers "what does TT buy *given* ordering+qsearch+ID" — the unmeasured half of Q-0002. |
| 2 | **PVS-only** | `PVS=0` vs current | Changes window structure, not node *content*; orthogonal to 1. |
| 3 | **TT + PVS** | both | Only now is the interaction visible — this is the confound Q-0002:24 explicitly names. |
| 4 | **Null-move** | `NMP=0` vs the rung-3 winner | Needs a verification search + eval-scale margin; unreadable before windows/TT are fixed. |
| 5 | **LMR** | `LMR=0` vs the rung-4 winner | Most parameters, most interaction with the TT; last. |
| 6 | **Aspiration** | `ASP=0` vs current | Cheap, but interacts with ID's previous-iteration score; last-but-one. |

**Gate between rungs:** a rung proceeds only if the previous rung (a) passes perft 10/10
bit-identical on Release **and** Audit-with-asserts, (b) has 0 illegal moves over a
random-mover sanity set, (c) has 0 key-mismatch assert fires. Any failure **stops the
ladder**; it does not silently skip to the next rung.

### D. Per-rung pre-registration skeleton (fill before `status: RUNNING`)

```
id / type: experiment         hypothesis: (H-id)      pre_registered: <date>
Arms:        A = <flags>,  B = <flags>      (sha256 of BOTH binaries recorded)
Mechanism:   two-binary --exe-a/--exe-b     (harness extension, re-verified)
Tier:        N (nodes)  |  S (strength)
Time control: 100ms+100ms inc   (DEC-0010's; sigma=371 applies ONLY here)
Openings:    10 random legal plies, seed = f(salt, game_index), same opening both arms
Colours:     alternating, balanced
Salt:        fresh; differs from E-0010's 20260914 / E-0011's 20260922
### E. Re-baseline risk if the eval changes mid-program

The sharpest design constraint, and **E-0013 (Texel fit) is currently `status: RUNNING`**, so
this risk is live, not hypothetical.

1. **Node deltas are eval-conditional.** LMR and null-move margins are expressed in eval
   units; a re-fit eval changes which nodes those heuristics fire on. A Tier-N delta measured
   on eval epoch E0 does not transfer to E1.
   **Rule:** every rung records `EVAL_STAGE` **and** the eval artifact hash. Deltas are
   comparable only within one eval epoch; cross-epoch deltas are **not** pooled.
2. **Silent hybrid engines (Finding 5).** `search.cpp:28` `VALUE[]` is independent of
   `eval.cpp:35` `FLAT_VALUE[]`. After a Texel refit the engine would be tuned-eval +
   old-material-ordering, and **no record would say so**.
   **Rule:** rung provenance MUST pin both hashes; if they diverge, the rung is quarantined,
   not reported.
3. **The strength ladder's reference arm moves.** SPRT measures a *difference*; if the
   baseline binary is rebuilt mid-ladder, rungs stop being comparable to each other.
   **Rule:** all rungs in one ladder share **one frozen baseline binary**, hash-pinned, and a
   rebuild **restarts the ladder** rather than continuing it.
4. **Ordering re-baseline invalidation (Finding 1).** Rung 0 is itself an eval-epoch
   measurement. If the eval changes, rung 0 must be re-run before the ladder resumes.
   **Rule:** rung 0 is re-validated (re-measured, hash-matched) at the start of every new eval
   epoch; a mismatch blocks the ladder.

**Recommended sequencing (the direct answer to the risk):** run **Tier N (rungs 0-3, the whole
node-delta ladder) to completion NOW, before E-0013 lands** — Tier N is engine-only, needs no
eval verdict, is deterministic, and is exactly the "measured first" this census was scheduled
to enable. Defer **Tier S** (strength SPRT) until the eval epoch is frozen. If E-0013 lands
mid-Tier-N: stop, quarantine, re-run rung 0, restart the ladder on the new epoch. **Do not
splice.**

## Recommended disposition

- **Q-0002 stays OPEN** pending the Phase-3 dispatch.
- Finding 1 is **blocking for the evidence base** (E-0007's attribution is not reproducible);
  route to implementation-engineer + verification-auditor as a source-vs-record divergence
  question — did the gate regress, or was EV-0005 measured on different code?
- Findings 2 and 3 are **correctness smells to record, not fix in this pass** (Gate-F
  discipline). Finding 2 should gate any live SPRT campaign on this binary.
- Finding 4 is a **protocol constraint**: use `go depth`, not `go nodes`.
- Finding 6 items are **low-severity dead-code candidates** for a future cleanup pass.

## Handoffs

- **adversarial-reviewer:** attack pass on this record, targeted at (i) Finding 1's
  source-vs-record divergence claim, (ii) whether Finding 2 is reachable in the 11-position
  set or only in adversarial positions, (iii) whether the two-binary harness extension
  (§B option i) can preserve the E-0012 validation claim or forces re-validation from scratch.
- **chief-architect:** fold §C (rung order) and §E (re-baseline rules) into the Phase-3
  dispatch, with §E's sequencing recommendation ("Tier N before E-0013 lands") as a
  scheduling dependency rather than prose.

## Not done, deliberately

No `src/` file was edited. No engine was run. No strength number is claimed. No tier, bound,
cap or stop band is re-derived here — all are cited from `DEC-0010` and the validated E-0012
harness.
Positions:   research/positions/act_E00007.fen (Tier N), frozen
Node metric: go depth 6, cumulative, NOT go nodes      (Finding 4)
Independence gate: 0 duplicate move-lists, 100% legal  (pre-condition, not post-hoc)
Crash rule:  crash/stall/missing-bestmove = LOSS, recorded per game
Node band:   <stated BEFORE the run, e.g. "-30%..-70% nodes, else INCONCLUSIVE">
Strength band: Tier S H0<=0 vs H1>=+20, cap 8000, post-cap INCONCLUSIVE
One look:    bounds/cap/verdict fixed before game 1; never extended after seeing data
Provenance:  src commit, both binary sha256, CMake cache values, EVAL_STAGE + eval hash pinned
Verdict:     H1 / H0 / INCONCLUSIVE — recorded verbatim, including negative results
```

**Honest-band discipline** (the FND-0003 / R-0003 F6 defect class): if realised variance
cannot separate the margin from 0 at the planned N, the verdict is **INCONCLUSIVE** and the
*band* shrinks in the pre-registration — never after seeing data.

---
| Node limit | **YES (suspect)** | `:66-68` | see Finding 4 |
| Threefold repetition | **YES** | `count_reps` `:73-78`, applied `:160` | count >= 2 (3rd occurrence) |
| 50-move rule | **YES** | `:161` | `halfmove >= 100` |
| Killer/history on cutoff | **YES** | `:204-209` | quiet moves only |
| Path-stack balance | **VERIFIED OK** | push `:195`, pop `:214`; all early returns outside the window | — |
| DEC-0008 filter | **VERIFIED OK** | `:198`, `:285`, `:139`, `:244` | TT move is an ordering hint re-found in the fresh list `:180`, never trusted as legal |

---
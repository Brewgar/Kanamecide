---
id: S-0024
type: session
agent: adversarial-reviewer
round: 4
title: "HO-0013 / R-0019 — critique of the E-0013 Texel pre-registration: NOT CLEAN, seven blocking findings, E-0013 stays PENDING"
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-26
closed: 2026-09-26
---

# S-0024 — Session (adversarial-reviewer, fresh occupant, HO-0013 receiver)

> Fresh occupant of the adversarial-reviewer seat. I did not draft E-0013 and I
> did not defend it. Nothing was fitted; no training has ever run in this project.

## Round / Work Items Touched
- HO-0013 (received, ACCEPTED → DONE by me) — critique of the E-0013 pre-registration.
- R-0019 (filed, `kind: critique`, `target: E-0013`, COMPLETED) — the ruling.
- No work item was opened, closed or marked VERIFIED by me. No H-#### status changed.

## What I Did (with evidence)
| # | Action | Evidence (command → exit code → path) | Calibration |
|---|---|---|---|
| 1 | Verified repo state: `git pull --ff-only`, `git status -sb`, `git rev-parse HEAD origin/master` | `research/context/s24_gitlog.txt` — HEAD == origin/master == `d9efffdb6c74fe020092ba4e6dfa5dec88da13f9` | demonstrated |
| 2 | Read the mandated set: HO-0013, E-0013, H-0013, E-0012, R-0018, DEC-0010, W-0001, HO-0008, Q-0006, W-0003, `tools/e0011_check.py`, `tools/e0012_sprt.py` | file reads; `research/context/s24_reviews.txt` | demonstrated |
| 3 | Confirmed the CLI's authoritative next review id (did **not** assume R-0019) | `python research/scripts/research.py new-review …` → `research/context/s24_newreview.txt`; highest existing = R-0018 | demonstrated |
| 4 | Proved the harness/eval cannot express E-0013's stage-(b) arms | `tools/e0012_sprt.py:325-326` (one `--exe`, both arms), `:301` (one binary hash), `:299` (`--validation-known` frozen to 6v0); `src/main.cpp:103-114,133-147` (UCI surface = Hash + EvalStage only, no echo, no param hash); `src/eval.h` + `src/_write_eval.py:25` (`EvalCoeffs` a compiled-in static) | demonstrated |
| 5 | Proved 76593 is a per-ply count, not a distinct-position count | `tools/e0011_check.py:385-398` (loops `row["san"]` only, increments per ply) vs `:371-383` (`positions` Counter, `duplicate_positions=1705` of `total_positions=130930`); `m0_audit/e0011/check_output.txt:2-3` | demonstrated |
| 6 | Computed stage-(a) power myself: margin 0.002 decidable **iff** per-game cluster SD `s_d ≤ 0.0101` at G≈200 clusters | own arithmetic in R-0019 ("Arithmetic I Did Myself"); `0.002 / (2.8016/√200)` | demonstrated (the arithmetic); the input `s_d` is **unmeasured** |
| 7 | Bounded the realized yield without running the count | 1705/130930 = 1.302 % duplication → ≈75,600 distinct; ≤6 positions lost to the one degenerate game; 0 crash games → band 75,600–76,587 vs the 30k floor | demonstrated (bounded, not measured) |
| 8 | Recomputed E-0010's per-term attribution from its own ladder | k4−k3 = 100.8−104.5 = −3.7 (mobility); k6−k5 = 116.1−127.6 = −11.5 (tempo) — reproduces E-0010:344 exactly | demonstrated |
| 9 | Computed the k5/k6 CIs from DEC-0010's own `h(N)=727/√N` | k5 N=200 → [+76.2,+179.0]; k6 N=240 → [+69.2,+163.0] — overlapping | demonstrated |
| 10 | Ruled all six questions + P0/P1 and Q-LABEL/Q-FIT/Q-SCOPE/Q-SUITE | `research/reviews/R-0019-…md` | demonstrated |
| 11 | Gates green + committed + pushed | `research/context/s24_validate.txt`, `s24_gitdiffcheck.txt`, `s24_gitlog2.txt` | demonstrated |

## What I Did NOT Do (and why)
- **Did not edit E-0013, H-0013, DEC-0010, `tools/e0012_sprt.py`, R-0017/R-0018, RUN-0002/RUN-0003.** Verified by `git diff --numstat` on all of those paths → empty (`research/context/s24_notouched.txt`). A critic rules; the owner edits.
- **Did not run any training, fitting, extraction, relabeling or SPRT game generation.** No Gate-0 build either. In particular I did **not** run the quiet-position count pass that B6 requires: it is an extraction over the dataset, outside this seat's remit. I bounded the yield instead.
- **Did not flip E-0013 to RUNNING**, and did not touch any H-#### status. The owner flips PENDING → RUNNING only after B1–B7 are discharged.
- **Did not start the HO-0005 / W-0003 audit** (still REQUESTED, out of scope). I only read W-0003 to determine whether it constrains E-0013 — it does not.
- **Did not run `tools/e0012_sprt.py --self-test` or any replay/live mode**, because replay is SPRT game processing. I read the file and cited it unmodified.
- **Did not manufacture a CLEAN.** Five of six questions are NOT CLEAN / BLOCKING. Q6 is CLEAN because it genuinely is, not because I was looking for a way to unblock.

## Claims I Made That Are NOT Yet Verified
- **`s_d ≤ 0.0101` is a conditional, not a measurement.** R-0019 states the condition and says the quantity is unmeasured. Routed to the owner as B2/B3: it must be measured by a pre-registered, non-training, TRAIN-ONLY feasibility pass before `LOSS_MARGIN` binds.
- **The realized yield band 75,600–76,587 is a bound I derived, not a count I measured.** Routed as B6; the execution session owns the count pass.
- **B1's claim that stage (b) needs a `src/` change plus a harness change is an inference from reading the code**, not an observed failure (I did not attempt a run, deliberately). It is strong — the code admits no other reading — but it is a reading. A re-critic should confirm it against the owner's intended mechanism.
- **My "stage 5 is the strongest rung is not supported at the stated N" claim** rests on DEC-0010's own `h(N)` model applied to E-0010's published per-rung N and point estimates. It is arithmetic on published values, not a re-run of the rungs.

## Environment Facts Learned
- **This environment's shell capture is degraded and this materially affects gate discipline.** `run_commands` reported `Command exited with code 1` on commands that plainly succeeded (e.g. `git log`, `Out-File` writes whose contents are correct). I therefore redirected **every** gate command's raw output to a file under `research/context/` and treated the **file contents** as authoritative, never the reported status. This is stated in R-0019's evidence appendix rather than hidden.
- PowerShell's `>` default redirect writes **UTF-16**, which the file reader mangles into spaced characters. Use `| Out-File -Encoding utf8` for every capture.
- **Repo-root hygiene is enforced by `validate` (DEC-0009):** ten `s24_*.txt` scratch files written to the repo root failed the gate. Fixed by moving them to `research/context/`. Future sessions should write captures there from the start.
- `research.py validate` also fails on a stale `state.json`; `state --write` + commit is required after filing a record.
- `research.py next` (run before this review landed) offered E-00004 (GPU batch-inference latency, priority high) ahead of HO-0013. Re-run `next` after this session to get the current ordering.

## State Left On Disk
- `research/reviews/R-0019-e-0013-pre-registration-critique-h-0013-texel-fit-contract-ho-0013-six-question-ruling.md` — COMPLETED, NOT CLEAN, 7 blocking findings (B1–B7), 10 non-blocking (DN1–DN10).
- `research/handoffs/HO-0013-…md` — flipped REQUESTED → ACCEPTED at the start, ACCEPTED → DONE at close-out, with `## Response` and `## Verification` appended (append-only; the request section and the six questions untouched).
- `research/state.md` / `state.json` — regenerated via `state --write`.
- Raw captures: `research/context/s24_*.txt`.
- **E-0013 itself is byte-identical to `d9efffd`.** Nothing was fitted; no fitted parameters exist.

## Next Action For The Successor
1. **Fix-and-re-critique cycle on E-0013 alone.** B1–B7 land as **ONE dated addendum** at the end of E-0013, original text untouched, supersessions quoted by name. No engine work, extraction, fitting or SPRT generation is needed to land any of them.
2. Priority order if the owner wants a staged discharge: **B1 first** (it decides whether stage (b) is runnable at all, and therefore whether the `src/`/harness work has to be pre-registered and critiqued on its own), then **B2 + B3** (the label frame and the margin's decidability), then **B4 + B5**, then B6, then B7.
3. Re-critique the addendum as a new R-#### (or a dated append to R-0019). Only on a CLEAN ruling may the owner flip E-0013 PENDING → RUNNING.
4. Route the first training execution (implementation-engineer + systems-researcher, fresh verification-auditor afterward) **only after** that.
5. Separately and at the owner's convenience: DN1–DN10, and the P0 decision record amending H-0013's stale "~50k quiet Stockfish-labeled FENs" sentence (`blocked_by` E-0013's terminal result, not its pre-registration).
6. Unrelated and untouched by this ruling: W-0003 / HO-0005 (Round-2 AGREEMENT_MATRIX backfill verification) remains open; E-00004 (GPU latency) is a separate high-priority track.

## Escalations (owner decisions needed)
- **E-0013 must decide, before any fitting spend, how stage (b) is to be made runnable** (B1). Three honest options: (i) pre-register and separately critique a `src/` parameter-artifact loader + engine-emitted param hash + a two-executable harness change; (ii) drop stage (b) from E-0013 entirely and re-scope it as a pure holdout-fit-quality experiment, deferring all strength claims to a later record that first builds the needed mechanism; (iii) run stage (b) as a **new** experiment under its own contract once the mechanism exists. I recommend (ii) or (iii) over (i) for a first training run, because (i) front-loads an engine change into the project's first training execution. **This is the owner's call; I only rule that the current contract cannot be executed as written.**
- The owner should confirm whether the 30k consequence ladder (E-0011 N1) is corrected in E-0011 as well as in E-0013's inherited text. B5 corrects it only in E-0013 (the only file I may not edit but may name). E-0011 is a completed, verified record; I did not touch it.

## Validation Status
- `python research/scripts/research.py validate` → **exit 0** after `state --write` and the root-hygiene fix; raw output `research/context/s24_validate.txt`.
- `python research/scripts/research.py update` → run; `state --write` → run; both clean.
- `git diff --check` → **exit 0**, no whitespace errors; `research/context/s24_gitdiffcheck.txt`.
- Committed and pushed to `origin master`; HEAD == origin/master with a clean tree (`research/context/s24_gitlog2.txt`).
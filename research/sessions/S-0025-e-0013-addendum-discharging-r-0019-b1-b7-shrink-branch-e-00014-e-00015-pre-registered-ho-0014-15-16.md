---
id: S-0025
type: session
agent: researcher-architect
round: 4
title: "E-0013 addendum discharging R-0019 B1-B7 (SHRINK branch) + E-00014/E-00015 pre-registered + HO-0014/15/16"
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-26
closed: 2026-09-26
---

# S-0025 — Session (researcher-architect)

> One session record per agent session, written to disk BEFORE the chat ends. It is
> the handoff to whoever runs next. Keep it short and factual; the records are the
> detail.

## Round / Work Items Touched

- E-0013 — dated pure-additions addendum landing R-0019's B1-B7, the F1-F12 freeze-audit
  closure, DN1-DN10 dispositions, the addendum-to-addendum disposition table, and six
  follow-up obligations. **Stays `status: PENDING`.** Not flipped to RUNNING.
- E-00014 (NEW, PENDING) — TRAIN-ONLY feasibility pass sub-contract. Measurement, not
  training. Not run.
- E-00015 (NEW, PENDING) — count-only realized usable quiet yield pass sub-contract.
  Measurement, not training. Not run.
- HO-0014 (NEW, REQUESTED) — re-critique handoff to adversarial-reviewer, scope =
  DISCHARGE VERIFICATION ONLY.
- HO-0015 (NEW, REQUESTED) — E-00014 execution handoff to systems-researcher.
- HO-0016 (NEW, REQUESTED) — E-00015 execution handoff to systems-researcher.


## What I Did NOT Do (and why)

- **No training, no fitting, no extraction, no counting, no feasibility pass, no SPRT
  game generation, no holdout read.** This seat produced text only. The two measurements
  R-0019 asked for are pre-registered in E-00014/E-00015 and routed to another seat.
- **Did not edit R-0019** or HO-0013's request section.
- **Did not edit any CLOSED/VERIFIED record** (E-0011, E-0012, W-0001, W-0005,
  RUN-0002/0003, R-0017/R-0018). The B5 backwards citation lives in E-0011's N1 text; I
  recorded it as a **dated correction note in E-0013** plus follow-up obligation F-U4
  (owned by the E-0011 owner seat), rather than silently repairing a verified record.
- **Did not touch `tools/e0012_sprt.py` or any engine source file.** Read-only.
- **Did not flip E-0013 to RUNNING.**
- **Did not open or close HO-0005 / W-0003.**
- **Did not change any H-#### status**, and did not amend H-0013's hypothesis text — P0
  stays deferred to E-0013 close-out (F-U1), exactly as R-0019 ruled.
- **Did not run Gate 0** (`kana.exe` → `ALL TESTS PASSED`). This session touched no
  engine source, so the anchor is untouched; but I flag that I did NOT reproduce it this
  session, and the next seat that touches the engine must.

## Claims I Made That Are NOT Yet Verified

Every claim in the E-0013 addendum is **unverified by design** — that is what HO-0014 is
for. Specifically unverified:
- That B1-B7 are actually discharged (as opposed to merely asserted). HO-0014.
- That the BUCKET-3 SHRINK decision genuinely removes the unexecutable mandate rather
  than re-pointing it. This is the claim I am least able to self-certify, and HO-0014
  asks the critic to rule on it mechanically, without being told which way I think it
  goes. HO-0014.
- That `SUITE_TOLERANCE = 0.02` is the right number. It is derived from the worst-case
  paired binomial SE at N=200 (0.5/sqrt(200) = 0.0354), and that derivation is my
  judgement, not a measurement. HO-0014 may reject it.
- That `S* = 6` is the right stage index. It is the only stage at which every fitted
  entry is read, and the data was generated at stage 6; that is an argument, not a
  measurement.
- The band 75,600-76,587 and the `s_d <= 0.0101` threshold are R-0019's arithmetic,
  which I reproduced rather than re-derived from new data.

## Next Action For The Successor

1. **adversarial-reviewer: take HO-0014.** Discharge verification only over B1-B7, the
   F1-F12 gap, DN1-DN10, the three integrity properties, and the BUCKET-2 conversion.
   E-0013 stays PENDING until that ruling.
2. **researcher-architect:** on a CLEAN (or fully-honest) ruling, E-0013 may leave PENDING
   — and the first thing its execution does is run E-00015 and E-00014 (both must
   pre-date the fit and pre-date any holdout read).
3. **systems-researcher:** HO-0015 / HO-0016 when the pre-conditions (E-0013's committed
   split map and pre-fit commit) exist.
4. The E-0012-style **strength contract** (F-U2) is still to be filed by
   researcher-architect; it is the named cost of the SHRINK decision and it is the thing
   that will eventually need the two-`--exe` harness change.

## Escalations (owner decisions needed)

- **The SHRINK decision leaves H-0013 half-untested until F-U2 lands.** That is a real,
  deliberate reduction in what this round can conclude, recorded as cost item 1 in the
  addendum. If the project wants the strength question answered sooner, the alternative
  is EXTEND and its Gate-0 / harness-validation cost — an owner call, not mine.
- **SUITE_TOLERANCE = 0.02** is an owner-set number derived from a worst-case binomial
  bound, not measured. Flagged for the critic rather than buried.
- **DN6** (DEC-0010:186-187's stale "Pending: independent verification" line) is not this
  seat's file; routed to the DEC-0010 owner as F-U6.

## Validation Status

All verdicts below are read from redirected output FILES, not from the shell's reported
exit status (see Environment Facts).

- `python research/scripts/research.py validate` → exit 0; remaining output is
  grandfathered/advisory warnings only, no failures.
- `python research/scripts/research.py update` → exit 0.
- `python research/scripts/research.py state --write` → exit 0.
- `git diff --check` → exit 0 (no whitespace errors).
- `git diff --numstat -- 'research/experiments/E-0013*'` → `648  0` (pure additions).
- Committed as `research(round4): ...` and pushed to `origin master`; `HEAD` ==
  `origin/master`, tree clean.


## Environment Facts Learned

- **Shell capture is degraded, and this is load-bearing for how this session's evidence
  was read.** `run_commands` reported `Command exited with code 1` on commands that
  plainly succeeded — including `git log`, `git rev-parse`, `Out-File` writes, and the
  `research.py` subcommands. **Every verdict in this record is taken from the contents
  of a redirected output FILE, never from the reported exit status.** Where file content
  and reported status disagree, the file is authoritative and the discrepancy is stated.
- PowerShell `>` writes UTF-16, which mangles these records. All writes used
  `| Out-File -Encoding utf8` or a Python `io.open(..., encoding='utf-8')` write.
- The `read_files` tool returned **stale cached content** for `start_line`/`end_line`
  range requests on a large file (R-0019). Workaround that worked: re-emit the file in
  fixed-size line-numbered chunks to disk and read the chunks. Worth knowing before the
  next agent trusts a ranged read of a long record.
- Repo-root hygiene is enforced: stray `.tmp*` scratch files at the root are validate
  WARNINGS under DEC-0009 and must be cleaned before commit. Mine were removed.

## State Left On Disk

- `research/experiments/E-0013-*.md` — addendum appended, `648 additions / 0 deletions`,
  still `status: PENDING`.
- `research/experiments/E-00014-*.md`, `E-00015-*.md` — NEW, PENDING, unrun.
- `research/handoffs/HO-0014-*.md` (adversarial-reviewer), `HO-0015-*.md`,
  `HO-0016-*.md` (systems-researcher) — NEW, REQUESTED.
- `research/sessions/S-0025-*.md` — this record.

## What I Did (with evidence)

| # | Action | Evidence (command → exit code → path) | Calibration |
|---|---|---|---|
| 1 | Repo state verified before any edit | `git pull --ff-only`; `git rev-parse HEAD` → `4478c3ab8748e1edb0889e2a9cc2c0259cda4412`, equal to `origin/master`; `git status -sb` → `## master...origin/master` | HIGH — read from a redirected file, not from the tool's reported status (see Environment Facts) |
| 2 | Read R-0019 in full (926 lines) in 40-line chunks | `research/reviews/R-0019-*.md` | HIGH — read verbatim, all seven findings and the exact missing sentences captured |
| 3 | Re-verified B1's structural claims READ-ONLY against the real surface | `tools/e0012_sprt.py:293-345,471-490` (one `--exe`; both `Engine(...)` built from `args.exe`; single `binary = sha256_file(...)` at :301); `src/main.cpp:103-114` (only `Hash`, `EvalStage` advertised), `:124-147` (setoption applied silently, **no echo**); `src/eval.cpp:174-234` (`EvalCoeffs` is a compiled-in static), `:356` (`if(stage>=6) sc += ...tempo`) | HIGH — R-0019's central claim confirmed independently; the UCI surface really has no parameter hash to dump |
| 4 | Re-verified B6's per-ply claim | `tools/e0011_check.py:385-398` iterates only `row["san"]` and increments `quiet_proxy` per ply; `:371-383` is the separate distinct-FEN Counter | HIGH |
| 5 | Re-verified B5's backwards citation arithmetically | `E-0010:341-344`: k4-k3 = 100.8-104.5 = **-3.7**; k6-k5 = 116.1-127.6 = **-11.5** | HIGH — reproduces E-0010's printed attribution exactly |
| 6 | Confirmed CLI-assigned IDs before writing | `research.py experiments` / `handoffs` → the CLI allocated **E-00014/E-00015** (not E-0014/E-0015) and HO-0014/15/16; I corrected my addendum's forward references to match | HIGH — caught and fixed before commit; this is why "verify with the CLI" mattered |
| 7 | Landed the E-0013 addendum as **pure additions** | `git diff --numstat -- 'research/experiments/E-0013*'` → **`648  0`** | HIGH — zero deletions is the append-only proof, and it is the evidence HO-0014 asks the critic to re-verify independently |
| 8 | Filed E-00014 and E-00015 PENDING, each with inputs, pre-registered output fields, and abort conditions | `research/experiments/E-00014-*.md` (8 abort conditions, 4 branches), `E-00015-*.md` (7 abort conditions, 4 branches) | HIGH — no field omitted; every branch maps to a named E-0013 outcome |
| 9 | Filed HO-0014 (discharge verification only, answer withheld) + HO-0015/HO-0016 | `research/handoffs/HO-001{4,5,6}-*.md` | HIGH |
| 10 | Corrected a dangling forward-reference I had introduced | validate flagged `dangling id E-00016`; I removed the id and left the contract CLI-assigned-at-filing | HIGH — self-caught by validate, fixed before commit |

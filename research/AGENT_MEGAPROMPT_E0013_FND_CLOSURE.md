# AGENT MEGAPROMPT — Close the E-0013 finding ledger (post-DEC-0012 / imem)

> **Date:** 2026-09-30 (anchor date convention: ledger dates are real session dates; see DEC / SYSTEM.md).
> **Role you occupy:** **verification-auditor** (fresh seat). You are NOT the owner of E-0013
> and NOT the implementation-engineer who repaired it. Gate 3 of SYSTEM.md applies: no seat
> verifies its own work, and `research.py validate` rejects `verified_by == owner`.
> **Prerequisite reading, in order:** `research/AGENT_MEGAPROMPT.md` (or
> `python research/scripts/research.py megaprompt`) → `SYSTEM.md` → this file →
> `research/DECISIONS/` entry DEC-0012 → the handoffs named below.

## Why this prompt exists

DEC-0012 built the institutional-memory system (`research/scripts/imem*.py`, commands
`index, lint, anchors, graph, search, ask, promote, findings, finding, new-claim,
new-finding, audit, selftest, ...`) and integrated two new record types end-to-end:
**claim** (CLM) and **finding** (FND). A mechanical, idempotent migration extracted the
E-0013 critique corpus into `research/findings/FND-*.md` (22 rows) and three design claims
into `research/claims/CLM-*.md`.

The migration **filed everything OPEN by design** — an extractor never closes a finding;
only a verifier with evidence does. As a result, the DEC-0012 lint gate now reports exactly
**one** blocking problem:

```
RUNNING target carries OPEN blocking findings: FND-0001..FND-0007, FND-0014..FND-0018
```

E-0013's `status: RUNNING` is **legitimate** — commit `6a6eb0a` records the deliberated
PENDING→RUNNING flip authorised under R-0024, and the R-0025/HO-0017 audit (session S-0035)
verified the flip Q1–Q8 with **no revert**. But the G4 training-readiness rule ("adversarial
critique CLEAN or all blocking findings discharged before RUNNING") is now machine-checkable,
and the ledger says the discharge was never *formally closed* row-by-row. Your job is to do
that closure — with evidence — until `imem.py lint` exits 0.

## The ten laws (violating any one invalidates the session)

1. **Markdown + YAML front matter is the only canonical store.** `research/_index/`
   (imem SQLite/JSON cache) is derived and disposable — never hand-edit it, never commit it.
2. **Records are append-only.** Never rewrite, delete, or renumber history. Corrections go
   in dated addenda. E-0013's protected hash range (`H_body`, ~L1–428) is immutable.
3. **No silent closures.** A FND row closes only via the command below, only with a
   resolution that names the evidence (records + commands + outputs/hashes).
4. **Gate 3:** `verified_by` must be an independent seat — that is you, `verification-auditor`.
   Never `researcher-architect` (owner) and never `implementation-engineer` (repairer).
5. **Recompute, don't copy.** Any hash/verdict you cite was recomputed by you this session.
6. **One purpose per commit**, conventional prefixes: `research(round4): ...`,
   `build(round4): ...`. Scratch goes to `_obs/` (gitignored), never the repo root.
7. **Session-close checklist is mandatory** (see §6). `validate` must exit 0.
8. **Large writes** are assembled in `_obs/parts/*.py` chunks and concatenated — no single
   tool call over ~6000 chars. Migration scripts must be **idempotent** (glob-check before write).
9. **E-00015 stays PENDING** and the holdout/labels are untouchable (see HO-0019 §Acceptance,
   which forbids reading holdout, fitting anything, changing salt/key/gate, or flipping
   statuses without authority).
10. **If the evidence fails, say so plainly.** A finding that is NOT discharged stays OPEN
    and you file the gap as dated evidence inside the FND record. Do not smooth it over.

## 1. Current state of the world (verified 2026-09-30)

| Check | Command | Expected |
|---|---|---|
| Core selftest | `python research/scripts/research.py selftest` | 47/47 OK |
| Corpus validator | `python research/scripts/research.py validate` | `OK` (advisory warnings only, all grandfathered) |
| imem unit tests | `python research/scripts/tests_imem.py` | 43/43 OK (runs against the live corpus) |
| imem selftest | `python research/scripts/imem.py selftest` | 43/43 OK, `VERSION = 2.0.0 (DEC-0012)` |
| imem lint | `python research/scripts/imem.py lint` | **exit 1: 1 problem, 127 warnings** |

Inventory: corpus ~228 records; `research/findings/` holds FND-0001..FND-0022, all OPEN;
`research/claims/` holds CLM-0001..CLM-0003. The 127 lint `warnings` (prose-links pointing
at ids only in body text, `Lnnnn` line-number pointers) are advisory, pre-date imem, and are
**not** part of your task — do not mass-edit old records to silence them. `research.py state`
claims/findings sections, `state.md`, `state.json`, `index.md` are already regenerated and
green. `.gitignore` now covers `research/_index/` and `_obs/`.

Key history anchors (all committed):
- `6a6eb0a` E-0013 lifecycle flip PENDING→RUNNING under R-0024 (L5-only; S-0031 records it
  was authorised-but-not-executed).
- S-0035 consumed HO-0017: R-0025's independent audit of the flip → Q1–Q8 verified, no revert.
- S-0036: parameter-table evaluator built; **overlap-0 gate FAILed 27** on the real dataset.
- S-0037: owner leakage ruling — dedup key strengthened to the **normalized FEN** (option 1);
  salt re-split (option 2) rejected on the contract's own terms; E-00015 band superseded,
  told to wait.
- S-0038: F-U7..F-U13 implemented; overlap-0 gate 27 → 0; yield measured, not estimated.
- S-0039: owner rulings — F-U10 band **RETIRED**, F-U9 artifacts **HASH-PINNED**, one
  correction to the S-0037 ruling.
- S-0040 (HEAD `2f31549` at writing): band retired, provenance pinned, label step built.
- HO-0019 (`status: REQUESTED`): independent verification of the S-0037 leakage ruling,
  verdicts V1–V7, addressed to you. See §5.

## 2. FND ledger map (who raised what, who must have discharged it)

| FND rows | Prefix | Severity | Raised in | Discharge chain to verify |
|---|---|---|---|---|
| FND-0001..0007 | B1..B7 | blocking | R-0019 re-critique of E-0013 | Repair sessions S-0026..S-0034; re-critique R-0020 (discharge-verification-only, consumed via HO-0014); R-0021 rulings; R-0022 independent verification; R-0024 flip authorisation; R-0025/HO-0017 audit |
| FND-0008..0013 | F-U1..F-U6 | major | R-0019/R-0020 family | Mostly `P0 deferred` / routing flags — some may legitimately stay OPEN (major findings do NOT block the lint gate) |
| FND-0014..0018 | X1..X5 | blocking | R-0021 rulings era | S-0029/S-0030 repairs; R-0022 title asserts "all four R-0021 findings applied"; X4/X5 source bullets literally say **DISCHARGED** |
| FND-0019..0022 | Z1..Z4 | major | R-0025 audit era | Z1 "REPAIRED", Z2 "CORRECTED ... withdrawn", Z3 "CORRECTED", Z4 "CORRECTED, S-0034" in the source prose |

## 3. PRIMARY TASK — close the 12 blocking rows on E-0013 (lint exit 1 → 0)

Scope: **FND-0001..FND-0007 and FND-0014..FND-0018** (target `E-0013`, severity `blocking`,
status `OPEN`). While you are at it, apply the same procedure to the major rows whose source
prose already claims a disposition (FND-0019..0022: Z1–Z4 all claim REPAIRED/CORRECTED) —
they do not gate lint, but an open ledger that lies in either direction is worthless.

### 3.1 Per-row loop (run for EVERY row; no batch-closing)

1. **Read the row:** `python research/scripts/imem.py finding FND-XXXX` gives front matter;
   open the file for the `## Origin` quote and the extraction context, then open the **source
   record** (the `review:` field / Origin names it) and find the original prose item.
2. **Reconstruct the claimed discharge:** follow the chain in the §2 table. For each row you
   must be able to name (a) the repair session(s), (b) the verification review, (c) the ruling
   that accepted it. `python research/scripts/imem.py provenance FND-XXXX` and
   `... graph FND-XXXX -d 2` show what is already linked; `... search "<keywords>"` finds the
   repair sessions.
3. **Independently spot-check the load-bearing fact** of that row with a command you run
   *now* (re-run the extractor selftest `python tools/e0013_extract.py --selftest`,
   `git --no-pager log` the protected range, grep the addendum for the repaired sentence,
   recompute a hash — whatever THIS row actually asserts). Keep the raw output; it goes into
   the row's evidence.
4. **Verdict:**
   - **Discharged** → close it (3.2).
   - **Not discharged / evidence missing** → leave `status: OPEN`, append
     `## Addendum {{DATE}} — verification-auditor` to the FND record stating exactly what is
     missing, and file it in your session record. That is a finding, and it is not smoothed over.
   - **Severity wrong** (e.g. source was advisory, not blocking) → do NOT close silently;
     lower severity only with a resolution that quotes the source disposition, same command path.

### 3.2 Close mechanics (exact)

```
python research/scripts/imem.py finding FND-0017 --write ^
  --close "X4 tail-sever: re-severed file verified intact by R-0022; repaired in S-0030; audit R-0025 Q? no-revert" ^
  --by "verification-auditor (round-5 closure seat)"
```

`--close` sets `status: RESOLVED`, `resolution:`, `resolved_by:`. It refuses non-OPEN rows
and refuses to run without `--write`. **It does NOT set `verified_by:`** — after each close,
edit the front matter to set `verified_by: verification-auditor (...)` yourself, fill the
`## Resolution` body section with the evidence (commands + outputs), and bump
`last_updated:`. One row = one close = one evidence paragraph.

### 3.3 Success criteria

- `python research/scripts/imem.py lint` → `counts.problems: 0`, **exit 0**. If any blocking
  row justifiably stays OPEN, the lint problem persists by design — then that row's addendum
  is the deliverable and you escalate to the owner via `research.py new-handoff`, not via a
  forced close.
- `python research/scripts/research.py validate` → OK.

## 4. SECONDARY TASK — extend the migration to F-U7..F-U13

The original extractor
(`_obs/parts/migrate_e0013.py` — scratch, kept for reference; pattern: `imem_core.new_record`
+ glob idempotence, first occurrence wins) scanned only E-0013 and reviews R-0010/0011/
R-0019..R-0025. The **later** findings F-U7..F-U13 live in sessions S-0036..S-0040 and were
never filed. Extend the ledger:

1. Extract `F-U7..F-U13` from S-0036/S-0037/S-0038/S-0039 into `FND-0023+` via
   `python research/scripts/imem.py new-finding` (or the proven script pattern — it must stay
   idempotent: re-running it adds nothing). Severity: `major` (F-U prefix), target `E-0013`.
2. Their rulings already exist (S-0037 option-1 ruling; S-0038 implementation, gate 27→0;
   S-0039 F-U9 hash-pinned, F-U10 band retired). Under the §3.1 loop, spot-check the
   load-bearing fact per row (`python tools/e0013_extract.py --selftest`; the split-map digest
   from HO-0019; the gate output) and close the ones genuinely implemented — same Gate-3
   discipline. Anything without verifiable evidence stays OPEN with an addendum.
3. Do **not** touch CLM-0001..CLM-0003: a claim moves out of OPEN only when the fitted
   artifact is consumed — that is downstream of HO-0019 and of E-0013 actually running.

## 5. HO-0019 — on your desk, formally separate

`research/handoffs/HO-0019-verify-e0013-s0037-leakage-ruling.md` is `REQUESTED` and
addressed to your seat: independently verify the S-0037 leakage ruling, verdicts V1–V7, each
recomputed from the repository (the split-map digest step is spelled out in the handoff —
expected `bb079a41630161bcd33a3a5df7890546dfe0c8329cc6bfed5ee35a83d4ada1ea`; `H_body`
`c7ebe54ce8cd51ac90483744a3d11e56a04fc5d48c0d8669e0804f53f883bea7` over 22,196 bytes).
Its acceptance criteria and its **forbidden actions** (no holdout, no fitting, no salt/key/gate
changes, no status flips beyond your own records, E-00015 stays PENDING) are binding. The
load-bearing check is **V3**: the ruling must track the contract's clause, not the engineer's
recommendation — if it doesn't, say so plainly, in a dated addendum. Consume it properly:
append `## Response` + `## Verification` sections, set `closed`, and file the review record
(`research.py new-review --kind verification`).

## 6. Session-close checklist (MANDATORY — all green before you commit)

```powershell
cd c:\Users\tahae\Kanamecide
python research/scripts/research.py selftest      # 47/47
python research/scripts/tests_imem.py             # 43/43
python research/scripts/imem.py selftest          # 43/43, VERSION mentions DEC-0012
python research/scripts/imem.py lint              # goal: counts.problems: 0, exit 0
python research/scripts/research.py update        # rebuild derived state
python research/scripts/research.py state --write # regenerate state.md / state.json
python research/scripts/research.py validate      # MUST exit 0
python research/scripts/imem.py findings --json   # ledger sanity: open vs closed
```

Then: file your session record (`research.py new-session` — next id after S-0040; describe
verdicts, per-FND dispositions, and any residual OPEN rows), close HO-0019 only via its own
protocol, and commit (`research(round4): ...`; if you touched tooling, separate
`build(round4): ...` commit). Never commit `_obs/`, `research/_index/`, or any
unsanctioned root file (`validate` enforces root hygiene).

## 7. Definition of done

1. `imem.py lint` exit 0 **or** every residual `problems[]` entry traced to a row whose
   addendum states precisely what evidence is missing, plus a handoff to the owner.
2. All closed rows carry `status: RESOLVED`, `resolution` naming records+commands,
   `resolved_by:` `verification-auditor`, `verified_by:` `verification-auditor`, and a filled
   `## Resolution` body. No row closed "per the addendum" alone — every close has at least
   one command you re-ran this session.
3. F-U7..F-U13 exist as FND rows (idempotent extraction proven by a dry re-run adding 0).
4. HO-0019 disposed of (DONE/REJECTED/WITHDRAWN per its protocol) or explicitly flagged as
   the next session's work with reasons.
5. All § 6 commands green; one purpose per commit; repo root hygiene intact.

## 8. Hard prohibitions (recap — the failure modes of this exact task)

- No closing in bulk, no blanket "discharged per R-0022" resolutions — per-row evidence.
- No weakening/removing the lint gate or the finding schema to make lint green.
- No edits to E-0013's protected hash range (~L1–428) or to any committed addendum.
- No new severity/status vocab values without a DEC record.
- No touching `research/_index/` by hand; if the cache is stale, `imem.py index` rebuilds it.
- No E-00015 execution, no holdout reads, no fitting (HO-0019 binding text).
- No prose-only requests to other agents — handoffs exist for that (`new-handoff`).

*If anything here contradicts a bound record (DEC, review, handoff), the record wins —
and the contradiction itself is a finding: file it.*





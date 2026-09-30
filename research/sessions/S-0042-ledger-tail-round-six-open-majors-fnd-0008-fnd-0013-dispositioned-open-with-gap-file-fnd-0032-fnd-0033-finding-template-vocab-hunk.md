---
id: S-0042
type: session
agent: verification-auditor
round: 4
title: Ledger-tail round: six OPEN majors (FND-0008..FND-0013) dispositioned OPEN-with-gap; file FND-0032/FND-0033; finding template vocab hunk
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-30
closed: 2026-09-30
related: [E-0013, E-00014, E-00015, FND-0008, FND-0009, FND-0010, FND-0011, FND-0012, FND-0013, FND-0027, FND-0028, FND-0032, FND-0033, DEC-0010, DEC-0012, H-0013, E-0011, Q-0006, S-0039, S-0040, S-0041]
---

# S-0042 — Ledger-tail round: six OPEN majors dispositioned (verification-auditor)

> Seat: **verification-auditor**. Gate 3 throughout: I am neither E-0013's owner
> (researcher-architect) nor its repairer (implementation-engineer). Every verdict below rests on
> a command I re-ran this session; nothing was closed on a table, a summary, or another seat's
> word.

## Round / Work Items Touched
- No work item claimed, started or closed. No new handoff filed (the two new FND rows are the routing vehicle).
- **Findings ledger**: FND-0008..FND-0013 dispositioned — **all six stay OPEN**, each with a dated `## Addendum` naming the missing evidence; **FND-0032**, **FND-0033** filed (found by recomputation); `research/templates/finding.md` status line annotated `# OPEN | RESOLVED` (one hunk, committed separately).
- **Untouched as briefed**: FND-0027/FND-0028 (blocked on PENDING E-00014); E-00014/E-00015 (stay PENDING); E-0013 (no byte written; protected range L1-428 never approached); every RESOLVED row.

## What I Did (with evidence)
| # | Action | Evidence (command → observation → path) | Calibration |
|---|---|---|---|
| 1 | Re-established the four baseline numbers | `research.py selftest` → **47/47 OK, exit 0**; `research.py validate` → **Validation OK, exit 0**; `imem.py lint` → **problems 0** (warnings 153, advisory), exit 0; `imem.py --json findings` → **count 31, OPEN exactly {FND-0008..0013, FND-0027, FND-0028}, all major** → `_obs/{selftest,validate,lint,findings}.txt`, `_obs/rows.txt` | demonstrated |
| 2 | **Found the brief's premise wrong on the template** | `research/templates/finding.md` carries **no** "OPEN | CLOSED" vocabulary comment (status line was a bare `status: OPEN`). The stale token lives in **DEC-0012 L22** (`status: OPEN|CLOSED`), contradicted by `imem_core.py` L68-L71 (`{"OPEN","RESOLVED","DISPUTED","WITHDRAWN","SUPERSEDED"}`) and `imem.py` L395 (writes `RESOLVED`); repo-wide `OPEN[|]CLOSED` search: exactly one hit, DEC-0012:22 → `_obs/{probe,closed_scripts,vocab_core}.txt` | demonstrated |
| 3 | Dispositioned FND-0008..FND-0013 one at a time | per-row re-runs in the table below; six dated open-with-gap addenda appended to the rows | demonstrated |
| 4 | Filed FND-0032 (minor: DEC-0012 vocab vs implementation) and FND-0033 (major: F-U14 absent from the ledger) | `imem.py new-finding` ×2 → `anchor_ok: True` both; bodies written by hand → `research/findings/FND-0032-*.md`, `FND-0033-*.md` | demonstrated |
| 5 | Annotated the template status line to match the CLI | `research/templates/finding.md` L9 → `status: OPEN  # OPEN | RESOLVED  (imem.py finding --close writes RESOLVED)`; one hunk, separate commit | demonstrated |
| 6 | Session close (final) | `imem.py index` → 248 records / 315 links / 0 unresolved, exit 0; `research.py update` / `state --write` / `validate` → OK, exit 0; `imem.py lint` → **problems 0, findings 0, exit 0** (advisory warnings only) | demonstrated |

## Per-row dispositions (FND-0008..FND-0013)

| Row | Verdict | Load-bearing command re-run this session | Evidence it stays open |
|---|---|---|---|
| FND-0008 (F-U1) | **STAY-OPEN** | byte-wise read of `H-0013-*.md`; `findstr "50k"/"H-0013"` over `decisions/` | H-0013 L25-L27 still says "~50k quiet Stockfish-labeled FENs"; no DEC supersedes; E-0013 RUNNING → close-out trigger unreached |
| FND-0009 (F-U2) | **STAY-OPEN** | `experiments/` listing; phrase walk "fitted-vs-pinned"; `e0012_sprt.py` argparse | contract unfiled (no E-0016+); `--exe` is still a single argument (L474); no strength game generated |
| FND-0010 (F-U3) | **STAY-OPEN** | byte-wise read of E-00014 | E-00014 PENDING, `result: null`; X-2 cannot fire; no named re-decision in `decisions/` |
| FND-0011 (F-U4) | **STAY-OPEN** | byte-wise scan of E-0011 (535 lines) + `git log` E-0011 | zero "R-0019"/"backwards" hits in E-0011; last E-0011 commit predates the obligation |
| FND-0012 (F-U5) | **STAY-OPEN** | E-0013 front matter; handoffs listing; Q-0006 L58-L69 | E-0013 RUNNING (no terminal verdict); no gate-7 handoff exists; gate text verified verbatim |
| FND-0013 (F-U6) | **STAY-OPEN** | byte-wise read of DEC-0010 L184-L188; `git log` DEC-0010 | stale line live at L186-L187; DEC-0010 has exactly one commit ever ("next touch" never happened); no handoff to its owner |

None of the six met the discharge bar: each records a future-dated obligation (close-out / terminal verdict / pre-strength-game / next DEC touch) whose act has not occurred. No `--close` was run; the addenda are the deliverable.

## What I Did NOT Do (and why)
- Did not close any of the six rows — no dischargeable evidence exists; closing would assert what has not been shown.
- Did not touch FND-0027/FND-0028, E-00014, E-00015, or any RESOLVED row; did not edit E-0013 (protected L1-428 untouched; no addendum needed there).
- Did not read the holdout, fit anything, pass `--validation-known`, or generate strength games.
- Did not repair DEC-0010 or DEC-0012 (owner records) — the mismatches are filed as findings instead.
- Did not weaken the lint gate or mass-edit the advisory warnings.

## Claims I Made That Are NOT Yet Verified
- None new; every disposition above cites a command run this session.

## Environment Facts Learned
- PowerShell `*>` captures are **UTF-16LE** (read_files shows nulls); parse byte-wise in python (`_obs/parse_findings.py`).
- Appending `"EXIT=$LASTEXITCODE"` to a JSON capture makes it invalid JSON — strip to the last `}` before parsing.
- **Brief premises can be wrong about file content** (S-0041 found the `validate` premise wrong; this round the `finding.md` premise was wrong). Read the named file before editing it.
- `git status` captured in the same command batch as a file-creating command can miss that file — re-check before committing.

## State Left On Disk
- `imem.py lint` final: **problems 0** (advisory warnings only; prose-link/line-pointer class, not edited). Findings ledger: **33 rows — 23 RESOLVED, 10 OPEN** = FND-0008..0013 + FND-0027 + FND-0028 + FND-0032 + FND-0033.
- `research.py validate` / `update` / `state --write`: OK (see Validation Status). `research/_index/` rebuilt (derived; uncommitted).
- Commits: (a) template hunk `research(round4): templates/finding.md — status vocabulary OPEN | RESOLVED`; (b) dispositions + this session `research(round4): ledger-tail round ...` — separate commits. Repo root clean; `_obs/` uncommitted.

## Next Action For The Successor
1. The six rows discharge only when their owners act: F-U1 (researcher-architect DEC superseding H-0013's "~50k" sentence), F-U2 (filed strength contract), F-U3 (named re-decision if X-2 fires), F-U4 (E-0011 addendum by its owner), F-U5 (gate-7 handoff on terminal verdict), F-U6 (flag DEC-0010's stale line at next touch).
2. DEC-0012 owner: resolve the vocabulary mismatch (FND-0032) — amend the record by dated addendum or change the CLI; my reading: `RESOLVED` is the governed status.
3. researcher-architect: file F-U14 and assign its owner (FND-0033). FND-0027/FND-0028 remain blocked on E-00014.
4. W-0003 still `verified_by: null` (blocks `research.py round --round 4`); unchanged by this round.

## Escalations (owner decisions needed)
- DEC-0012's vocabulary text vs the implementation (FND-0032): record owner rules; the verification seat does not edit decision records.
- F-U14 ownership is unassigned (S-0039/S-0040) and untracked until FND-0033 is actioned.

## Validation Status
- `python research/scripts/research.py validate` → `Validation OK` (exit 0)
- `python research/scripts/research.py update` → regenerated (exit 0)
- `python research/scripts/research.py state --write` → state.json + state.md written (exit 0)
- `python research/scripts/imem.py lint` → `problems: 0`, `findings: 0` (exit 0)
- `python research/scripts/imem.py index` → 248 records / 315 links / 0 unresolved (exit 0)
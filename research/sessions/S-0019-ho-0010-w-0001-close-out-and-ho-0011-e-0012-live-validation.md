---
id: S-0019
type: session
agent: systems-researcher
round: 4
title: HO-0010 W-0001 close-out and HO-0011 E-0012 live validation
status: CLOSED
context_budget: "reading <= ~15k tokens; no project state kept only in chat"
example: false
created: 2026-09-25
closed: 2026-09-25
---

# S-0019 — Session (systems-researcher)

> One session record per agent session, written to disk BEFORE the chat ends. It is
> the handoff to whoever runs next. Keep it short and factual; the records are the
> detail.

## Round / Work Items Touched
- Round 4. W-0001 (record close-out only), W-0005 (E-0012 live execution), E-0012, RUN-0002,
  RUN-0003, HO-0010, HO-0011, S-0019.

## What I Did (with evidence)
| # | Action | Evidence (command → exit code → path) | Calibration |
|---|---|---|---|
| 1 | Boot: read the 5 mandated files | `Read` → n/a → `research/AGENT_MEGAPROMPT*.md`, `research/agents/systems-researcher/profile.md`, `research/handoffs/HO-001*.md` | High |
| 2 | Gate 0 | `build\Release\kana.exe` → **0**, printed `=== ALL TESTS PASSED` → `m0_audit/s0018/gate0.txt` | High |
| 3 | Phase A — confirmed R-0017 COMPLETED/VERIFIED, then closed W-0001 lifecycle DONE + Work Log entry citing R-0017, HO-0009, S-0017; HO-0010 → DONE | `update` → 0, `state --write` → 0, `validate` → 0 → `m0_audit/s0018/phaseA_*.txt`; commit `340579b` | High |
| 4 | Phase B preflight (all before any launch) | `research.py validate` → 0; `e0012_sprt.py --self-test` → 0 (239/239 split points); `--replay e0010_k6n_games.jsonl` → 0, REPLAY_SANITY PASS crossing game 179, input SHA-256 `9da1cfa0…0d227` (certutil match) → `m0_audit/s0018/preflight/*` | High |
| 5 | Created both RUN records **before** launching, with exact command, heartbeat, checkpoint, resume policy, `concurrency_cap: 2`, binary hash, source commit | `research.py new-run --work W-0005 …` → 0 / 0 → `m0_audit/s0018/newrun2.txt`, `newrun3.txt` | High |
| 6 | Fixed real defects `validate` found in my own scaffolds (missing `created`; null front-matter heartbeat/checkpoint/command; RUN-0003 claiming RUNNING before launch) | `validate` 1 → fixes → 0 → `m0_audit/s0018/validate_mid*.txt` | High |
| 7 | Committed + pushed the record set before launching, so JSONL `src_commit` == origin/master HEAD | `git commit`/`git push` → 0 → commit `7aab350` = launch-time HEAD | High |
| 8 | Launched RUN-0002 (known-difference, `--retry 0`) | `runjob.py launch --id RUN-0002 …` → **LAUNCH2_EXIT=0**, detached pid 28404, supervisor 29264 → `m0_audit/s0018/launch2.txt` | High |
| 9 | RUN-0002 terminal: **H1 accepted at game 125**, LLR `+2.9590633873412573` ≥ bound `2.9444389791664403`, n=125, W80/D20/L25, 0 incidents | heartbeat final line `18:29:55 EXIT pid=28404 checkpoint_lines=125` → `m0_audit/e0012_known/{run.log,heartbeat.txt,checkpoint.json}` | High |
| 10 | Independent audit of RUN-0002 (own LLR impl + python-chess legality replay of all 125 games) | `python m0_audit/s0018/e0012_audit.py … 6 0 8000 20260924` → **AUDIT_EXIT=0**, `RESULT: PASS`, `problems: {}`, 0 duplicates, 0 legality failures → `m0_audit/s0018/audit_known_final.json` | High |
| 11 | Launched RUN-0003 (N4 null pair) only after RUN-0002 was terminal | `runjob.py launch --id RUN-0003 …` → **LAUNCH3_EXIT=0**, `checkpoint before launch: 0 item(s), 0 bytes`, pid 2904 → `m0_audit/s0018/launch3.txt` | High |
| 12 | RUN-0003 terminal at the cap: **no H1 acceptance**, `crossing: null`, verdict `INCONCLUSIVE`, n=240, W106/D23/L111, LLR `−0.6852460784333203`, harness `null_control.pass = true` | heartbeat final line `19:04:46 EXIT pid=2904 checkpoint_lines=240` → `m0_audit/e0012_null/*` | High |
| 13 | Independent audit of RUN-0003 | `python m0_audit/s0018/e0012_audit.py … 6 6 240 20260924` → **AUDIT_NULL_EXIT=0**, `RESULT: PASS`, `problems: {}`, 240 rows, 0 duplicates, 0 legality failures → `m0_audit/s0018/audit_null_final.json` | High |
| 14 | Corrected the null heartbeat hash in the records (an earlier capture predated the final `EXIT` line) and re-verified all 9 artifact hashes against the files on disk | `certutil -hashfile …` → 0, all 9 `IN_RECORDS=True` | High |
| 15 | Filled E-0012's permitted Results/Provenance live-execution section (no contract line touched) | editor → n/a → `research/experiments/E-0012-…md` §"Live execution log" | High |
| 16 | Close-out | `update` → 0; `state --write` → 0; `validate` → 0 (grandfathered warnings only) → `m0_audit/s0018/closeout2.txt` | High |

## What I Did NOT Do (and why)
- **Did not mark W-0005 DONE or VERIFIED.** HO-0011 §5 reserves that for the owner plus a
  fresh verification-auditor review of the raw evidence; the executor-side audits above are
  audit artifacts, not self-verification.
- **Did not modify** W-0005 owner fields, E-0012's contract (tiers/bounds/caps/stop bands/
  salt/N4 null design), R-0015, R-0017, RUN-0001, E-0011, the E-0011 dataset, source code, or
  `tools/e0012_sprt.py`. The contract stayed frozen *after* I had seen live numbers.
- **Did not re-verify W-0001.** Phase A was a record close-out on R-0017's existing VERIFIED
  verdict — not a second verification, and not permission to consume the dataset.
- **Did not run any training and did not create H-0013.**
- **Did not retry, resume, or re-launch anything.** Both runs completed in a single
  uninterrupted execution, so no pre-resume log existed to preserve; `--retry 0` held on both.
- **Did not tune anything to make the null control look better**; the final negative LLR is
  reported as-is.

## Claims I Made That Are NOT Yet Verified
- "The harness has no colour bias and the E-0012 live path works" — supported by my own
  recomputation and python-chess replay, but **not independently reviewed**. Route to a
  verification-auditor against the raw artifacts (`m0_audit/e0012_known/`,
  `m0_audit/e0012_null/`).
- "W-0005's live half is now complete and closeable" — the owner/verification-auditor call,
  not mine.
- Tier S crossed at 125 here vs 179 in the offline replay. E-0012's own (N1) text pre-declares
  ≈5.4% two-sided false-FAIL from sampling noise alone, so this is not a contradiction — but
  the *reason* for the earlier crossing is **not established** by this session and must not be
  asserted as an engine-strength result.

## Environment Facts Learned
- Foreground `Start-Sleep` waits are killed at ~15 s in this shell; poll with single short
  commands, or watch via a detached `Start-Process powershell` poller appending to a log file.
- A held `n` in the SPRT checkpoint is not necessarily a stall — check heartbeat file age and
  `kana.exe` CPU first (this session: HB age 1 s, 2 engine processes, n advancing).
- Rate observed: ~10 s/game at Tier S stage 6 with 2 engines; RUN-0002's 125 games ≈19 min,
  RUN-0003's 240 games ≈34 min.
- `validate` enforces the DEC-0009 **handoff** vocabulary: `CLOSED` is rejected, the terminal
  handoff state is `DONE`. (The first close-out attempt failed on exactly this; fixed.)
- `new-run` scaffolds have null front-matter, which `validate` flags — fill them before
  committing.

## State Left On Disk
- `m0_audit/e0012_known/` — RUN-0002: `games.jsonl` (125 rows, SHA-256
  `637a9fa4229ee8ab54b3c8f8420731659575d6ee59dda72c4a2311198650d407`), `checkpoint.json`,
  `run.log`, `heartbeat.txt`; no `incidents.jsonl` (0 crashes).
- `m0_audit/e0012_null/` — RUN-0003: `games.jsonl` (240 rows, SHA-256
  `5654db6075703625fd30c633805abaf935eb584da25dc4277fa24d494693e30d`), `checkpoint.json`,
  `run.log`, `heartbeat.txt`; no `incidents.jsonl` (0 crashes).
- `m0_audit/s0018/` — gate0, preflight, launch logs, independent audits, hash captures,
  close-out logs, and the read-only observer scripts.
- Records: W-0001 DONE, HO-0010 DONE, RUN-0002/RUN-0003 COMPLETED (exit 0), E-0012 RUNNING with
  a live-execution results section, HO-0011 DONE. **W-0005 deliberately left OPEN.**

## Next Action For The Successor
- A **verification-auditor** should re-derive both results from the raw JSONL (recompute the
  LLR, replay legality, re-hash every artifact) and rule on the E-0012 live evidence; then the
  **owner** decides W-0005's lifecycle. Neither step is a systems-researcher action.

## Escalations (owner decisions needed)
- W-0005 close-out decision (owner + fresh verification-auditor review) — unblocked by HO-0011
  but not mine to make.
- Whether the earlier-than-expected Tier S crossing (125 vs the model's 179) warrants any model
  comment, or is left as recorded sampling variation.

## Validation Status
- `python research/scripts/research.py update` → **0** (`m0_audit/s0018/closeout2.txt`)
- `python research/scripts/research.py state --write` → **0**
- `python research/scripts/research.py validate` → **0** (grandfathered/advisory warnings only;
  no failures)
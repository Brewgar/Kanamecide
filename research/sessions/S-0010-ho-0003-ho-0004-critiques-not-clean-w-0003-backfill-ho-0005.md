---
id: S-0010
type: session
agent: adversarial-reviewer
round: 4
title: "HO-0003/HO-0004 critiques (R-0011/R-0012: both NOT CLEAN) + W-0003 backfill (R-0013) + HO-0005"
status: CLOSED
context_budget: "reading heavy on the records (~bootstrap + 2 pre-registrations + DEC-0010/D-0007 + runjob.py + Round-2 corpus); all work was record arithmetic + git inspection, no engine"
example: false
created: 2026-09-22
closed: 2026-09-22
---

# S-0010 — Session (adversarial-reviewer)

> Gate 0 attempted exactly once before any work: `build\Release\kana.exe` → Device Guard /
> App Control block, no process, exit 1 (F-0002; 7th observation on record;
> `research/context/bootstrap/gate0.txt`, capture `gate0_session_run.txt` — empty because the
> shell, not the process, emits the block message). Not retried; policy untouched.

## Round / Work Items Touched

- **W-0001 — HO-0003 → R-0011** (critique of E-0011's pre-registration), verdict NOT CLEAN
  (3 blocking findings), HO-0003 → DONE. Work log appended; E-0011 stays PENDING.
- **W-0005 — HO-0004 → R-0012** (critique of E-0012 + offline SPRT replay), verdict NOT CLEAN
  (2 blocking findings), HO-0004 → DONE. Work log appended; E-0012 stays PENDING.
- **W-0003 — R-0013** (Round-2 AGREEMENT_MATRIX backfill addendum), review COMPLETED, matrix
  not edited (verified `git log -1` = `9b69e0a`, status clean); W-0003 → IN_PROGRESS;
  **HO-0005** filed to verification-auditor (the required verified-by-ne-owner check).

## What I Did (with evidence)

| # | Action | Evidence (command → exit code → path) | Calibration |
|---|---|---|---|
| 1 | Gate 0, exactly once | `build\Release\kana.exe` → exit 1, no process → `research/context/bootstrap/gate0.txt` (attempt #7) | demonstrated |
| 2 | Re-ran the offline replay | `python research/context/w0005_sprt_replay.py` → exit 0; output line-for-line identical to the pinned `w0005_sprt_replay_output.txt` (44/44 non-blank lines, ASCII-normalised; only the cp1252 em-dash byte differs) | demonstrated |
| 3 | Re-ran the calibration script | `python research/context/w0002_power.py` → exit 0 (σ=371; ASN S 1822/2025, R 29,159/32,399, M 292/324) | demonstrated |
| 4 | Validated the memory store | `python research/scripts/research.py validate` → exit 0, "0 problems" (warnings only; RUN-0001 listed as dangling — noted as R-0011 N7) | demonstrated |
| 5 | Independently re-derived the LLR finals from my own code (no import of the author's script; formula from DEC-0010's text) | `%TEMP%\krev10\independent_llr.py` → exit 0 → k6 `S: H1 @179 +2.985`, `R: none +1.098`, `M: none −0.673`; closed-form totals over 240: S +4.093, R +1.098, M −0.673; bound ln19 = 2.9444389791664403 verified two ways; h(1000) = 22.99 Elo; Tier-S drift/sd 0.017047/0.054440 per game ⇒ crossing sd ≈ 41.9 games | demonstrated |
| 6 | Measured E-0011's flagged assumptions from retained evidence (EV-0001, read-only) | my scratch scripts (`%TEMP%\krev10\measure_plies.py`, `quiet_yield.py`, `color_score.py`, `crosstab.py`) → exit 0 → 1,240 games: mean **130.3 plies/game** (median 117, p10 57, p90 243, max 290), 72 plycap games (5.8 %), 20 sub-12-ply degenerate games (1.6 %), duplicate move-lists = 0, ids 0-based dense; quiet-yield proxy ≈**76,887**/1,000 games; **White 58.51 %** (k6: A-score 0.783 as White vs 0.542 as Black) | demonstrated |
| 7 | Band pre-commitment check | `git check-ignore -v research/context/w0005_sprt_replay.py` → `.gitignore:118`; `git log -- research/context/w0005_sprt_replay.py` → **empty** (untracked); pinned hashes all match current files; E-0012 single commit `2a9d997` | demonstrated |
| 8 | M-tier "anomaly" ruling | k1n (true +36.3) and k2n (+82.3) sit below M−50=100 → early H0 at games 79/192 is DEC-0010's zones working as designed; k3/k4 (+104.5/+100.8) just inside the lower edge → no crossing, as predicted (−395/−335) | demonstrated (re-derived) |

## What I Did NOT Do (and why)

- Did not run or build the engine (F-0002; Gate 0 blocks it — 7th attempt logged).
- Did not edit E-0011/E-0012/DEC-0010/D-0007/R-0009/R-0010/EV-0001 (read-only by the rules that
  bind this seat; the reviewer's fix is a named addendum, not an edit).
- Did not edit `research/AGREEMENT_MATRIX.md` (historical artifact; exit-check requirement).
- Did not author the B1–B3 fixes for E-0011/E-0012 or the null-pair control — the critique names;
  the author fixes.
- Did not verify my own W-0003 deliverable (HO-0005 goes to verification-auditor).

## Claims I Made That Are NOT Yet Verified (routed)

- R-0013's state fidelity to the Round-2 record → **HO-0005** (verification-auditor).
- My measured numbers (0.783/0.542 color cells; 130.3 plies/game; 76,887 quiet-yield) are quoted
  from my own runs with commands + input hashes; a verification seat can re-run them from the
  pinned EV-0001 files without an engine.

## Environment Facts Learned

- Gate 0 block is stable across seven observations and three seats (F-0002, exit 4551); the
  shell, not the process, prints the policy line, so a redirected capture file is empty.
- `runjob.py launch` deletes the existing log before launching (`log.unlink()`) — the E-0011/
  E-0012 run plans must preserve the interrupted log on resume (a blocking-finding detail,
  R-0011 B2 / R-0012 B2); and its checkpoint telemetry counts raw `splitlines()` (a torn trailing
  line inflates the count).
- PowerShell's `>` capture writes UTF-16LE; the pinned `w0005_sprt_replay_output.txt` carries a
  cp1252 em-dash — byte-level comparison of console captures is unsafe; compare decoded text.
- `research/context/*` is gitignored (`.gitignore:118`) — anything written there is untracked by
  design; see R-0012 B1.

## State Left On Disk

- `research/reviews/R-0011`, `R-0012`, `R-0013` (COMPLETED).
- `research/handoffs/HO-0003`, `HO-0004` (DONE, responses + verification appended);
  `research/handoffs/HO-0005` (REQUESTED).
- `research/work/W-0001`, `W-0005` (OPEN, work-log note), `W-0003` (IN_PROGRESS, evidence set).
- `research/context/bootstrap/gate0.txt` (+attempt #7). No other research-path writes.

## Next Action For The Successor

- researcher-architect: land the E-0011 addendum (B1–B3, N1–N7) and the E-0012 fixes (track the
  replay artifacts; the resume/durability policy) so the two PENDING experiments can be
  re-critiqued; then, when F-0002 is lifted, W-0001 step 2 build and the E-0012 live validation
  (plus optionally the N4 null-pair control).
- verification-auditor: accept HO-0005 and either verify W-0003 (R-0013) or name a defect.
- Everything else: F-0002 (owner); W-0006 remainder (implementation-engineer).

## Escalations (owner decisions needed)

- **F-0002** — Gate 0 hard block persists after seven observations (exit 4551 / App Control).
  No engine-dependent work can progress until the owner allow-lists or rebuilds under a
  permitted policy. W-0001 step 2 (build) and E-0012 live validation both wait on it.

## Validation Status

- `python research/scripts/research.py update` → index regenerated
- `python research/scripts/research.py state --write` → state.md/state.json regenerated
- `python research/scripts/research.py validate` → OK, 0 problems (exit 0)
- `python research/scripts/research.py round --round 4` → exits non-zero by design: W-0001,
  W-0003 (pending verification), W-0005 and W-0006 remain open/unverified; W-0002, W-0004 and
  W-0007 are DONE.


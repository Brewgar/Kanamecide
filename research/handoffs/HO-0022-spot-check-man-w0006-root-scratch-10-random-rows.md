---
id: HO-0022
type: handoff
from: implementation-engineer
to: verification-auditor
work_item: W-0006
status: REQUESTED
title: "Spot-check 10 random rows of MAN-W0006-ROOT-SCRATCH-001 (root-scratch debt reduction)"
artifacts:
  - research/manifests/MAN-W0006-root-scratch.md
  - research/manifests/MAN-W0006-root-scratch.json
  - research/work/W-0006-root-scratch-debt-reduction-grandfathered-list-shrink.md
  - research/scripts/root_grandfathered.txt
  - research/findings/FND-0034-ev-0010-binary-digest-drift-after-rebuild.md
commands: []
acceptance: null
example: false
created: 2026-10-02
closed: null
---

# HO-0022 — Spot-check MAN-W0006-ROOT-SCRATCH-001

## Request

The MEMORY-KEEPER seat executed the W-0006 root-scratch clean-up: **root files 204 -> 79**,
`root_grandfathered.txt` **267 -> 73** entries, 29 files deleted, 96 moved to
`_obs/e0010-era/`. The seat authored the manifest, so it may not verify its own work
(DEC-0009 gate 3). Please independently spot-check **10 randomly chosen rows** and rule on
the whole.

Headline claims to attack, in priority order:
1. **Nothing cited was destroyed.** 79 rows are `KEEP` because the ledger cites them. If
   even one of those was actually uncited junk, or if any genuinely-cited file was moved
   or deleted, the manifest's central claim is false.
2. **Every `DELETE` row was safe.** All 29 must be either git-TRACKED (restorable from
   `HEAD`) or zero-byte. Verify this independently — do not take the manifest's word.
3. **No evidence was lost.** All 96 moved files must exist at their manifest destination
   with a matching sha256.
4. **`validate` was not made falsely green.** `validate` reports 1 problem (EV-0010
   sha256 drift). Confirm that is genuinely pre-existing (FND-0034) and that this session
   did not suppress a problem it should have surfaced.

## The 10 rows to check (seed 20261002, `random.sample` over all 204 rows)

| # | file | action | class | bytes | sha256 |
|---|---|---|---|---|---|
| 1 | `e0010_k1_err.txt` | KEEP | CITED | 2 | `8c14fdf5c613f56e…` |
| 2 | `sl_outB.txt` | MOVE | GARBAGE | 16 | `6b57ee7ef07f85ba…` |
| 3 | `e0010_elo.py` | KEEP | CITED | 3524 | `caefc07bb021cdf3b…` |
| 4 | `g2d_out.txt` | MOVE | GARBAGE | 332 | `ecfca313d860bb29…` |
| 5 | `sp_driver.py` | KEEP | CITED | 5313 | `1cffdae16802871e…` |
| 6 | `write_eval.py` | KEEP | CITED | 2267 | `93c5f70178b597aa…` |
| 7 | `stage3.txt` | MOVE | EVIDENCE | 1331 | `32e238d1e63c5796…` |
| 8 | `random_selfplay.py` | KEEP | CITED | 4227 | `8dfc2f4ed4b015e2…` |
| 9 | `uci_rel.out` | DELETE | GARBAGE | 152 | `480575ff2c009e92…` |
| 10 | `run_stopB.bat` | MOVE | TOOLING | 184 | `d234c2d1a67d9ac6…` |

Re-derive your own sample if you prefer (`random.seed(...)` is only so the check is
reproducible); a different random draw is equally valid and arguably a better test.

## Artifacts To Read (paths)
- `research/manifests/MAN-W0006-root-scratch.md` — the full 204-row table + method + defects
- `research/manifests/MAN-W0006-root-scratch.json` — same, machine-readable
- `research/work/W-0006-root-scratch-debt-reduction-grandfathered-list-shrink.md` — the work log
- `_obs/w0006/triage.py`, `_obs/w0006/apply.py` — the harness that produced and executed it
- `_obs/w0006/post_validate.log`, `_obs/w0006/apply_log.txt`, `_obs/w0006/_base.txt` — raw output

## Commands To Run
```powershell
# independent citation check for the KEEP rows (word-boundary, not substring)
python research/scripts/research.py hygiene

# the 10 spot-checks
git cat-file -e HEAD:uci_rel.out            # row 9 must be restorable
Get-FileHash _obs/e0010-era/garbage/sl_outB.txt, _obs/e0010-era/garbage/g2d_out.txt -Algorithm SHA256
Get-FileHash _obs/e0010-era/evidence/stage3.txt, _obs/e0010-era/tooling/run_stopB.bat -Algorithm SHA256

# the two gates
python research/scripts/research.py validate
python e0010_report.py
python research/scripts/research.py selftest

# confirm nothing cited vanished from root
git status --porcelain            # 18 tracked deletions; each must be an uncited scratch file
```

## Acceptance Criteria (what makes this DONE)
- All 10 rows independently re-derived, each ruled CORRECT or DEFECT with the command output.
- An independent answer to: **were any of the 18 git-tracked deletions actually cited by
  a research record?** (The seat's claim: no — they are `uci_rel.out`, `uci_t1/t2/t3.out`,
  `update_out.txt`, `validate_out.txt` and 12 `.bat`/`.py` one-offs.)
- A ruling on whether quarantine-instead-of-delete for the 45 untracked junk files is
  acceptable, or whether the owner wants them destroyed outright. **This is the one
  judgement call in the manifest that deviates from the brief's literal wording**, and it
  needs an owner verdict, not a reviewer's.
- `validate` confirmed at exactly the pre-existing baseline (1 problem = FND-0034).
- Verdict appended below; if any defect, name it and route back to the owner.

## Two things this seat deliberately did NOT do (check they were correct)
1. **Did not repair FND-0034** (EV-0010 sha256 drift). Re-pinning an evidence digest is
   the record owner's act; the manifest must not make `validate` green by weakening a pin.
2. **Did not move `kana_o3b.exe` / `kana_o3c.exe`** (939 KB, the only non-e0010 root
   debt left). They are cited by W-0006's own 2026-09-21 note, which already flagged them
   for an owner decision. Confirm that reading, or route them for disposal.

## Response (receiver, append-only)
- {{DATE}} — (role) — ...

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: ...

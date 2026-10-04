---
id: HO-0022
type: handoff
from: implementation-engineer
to: verification-auditor
work_item: W-0006
status: DONE
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
closed: 2026-10-04
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
- 2026-10-03 — verification-auditor (fresh seat, Gate 3) — HO-0022 executed. I did not author
  the manifest, the harness or `root_grandfathered.txt`; every number below is re-derived by my
  own code from the manifest JSON + the filesystem + git, without importing `triage.py` or
  `research.py`'s citation logic. Verdict: **DEFECTS (4, numbered below)** — all four are
  defects in the *claims and their verification method*, not evidence loss. Nothing cited was
  destroyed; no byte is unrecoverable. See `## Verification` for the raw evidence.

### Gate results (all four re-run, quoted)

| gate | command | result |
|---|---|---|
| `validate` | `python research/scripts/research.py validate` | **exit 1, exactly 1 problem** — `audit[evidence]: sha256 drift on build/Release/kana.exe: recorded 504EB01A8287… vs on-disk 686EA5979415… (evidence/EV-0010-e0010-measurement-binary.md)`. Pre-existing = FND-0034. Not suppressed. |
| `selftest` | `python research/scripts/research.py selftest` | **exit 0** — `Ran 47 tests in 5.108s` / `OK` |
| `tests_imem` | `python -m unittest discover -s research/scripts -p 'tests_imem.py'` | **exit 0** — `Ran 48 tests in 0.539s` / `OK` |
| `imem lint` | `python research/scripts/imem.py lint` | **exit 0** — `problems: 0, warnings: 179, findings: 2` (findings = FND-0034 on EV-0010, FND-0035 on Q-0002 — both correctly surfaced, not suppressed) |
| `e0010_report.py` | `python e0010_report.py` | **exit 0** — all six rungs reproduced: k1 +36.3 / k2 +82.3 / k3 +104.5 / k4 +100.8 / k5 +127.6 / **k6 +116.1** (bayes +116.1, CI95 [+70.8,+163.5], LOS 100.00%, N=240); `duplicate-move-lists=0 -> INDEPENDENT` on k1–k6; gate (a) PASS, gate (c) FAIL (Elo>=150 false) — identical to the pre-clean-up run |

`research.py` was **not modified** by the clean-up: `git diff f5883dc..HEAD -- research/scripts/research.py`
is **empty**. The only change under `research/scripts/` is `root_grandfathered.txt`
(+10/−196 insertions/deletions). This is the decisive evidence for attack #4: the EV-0010
evidence-sha256 check that fires is the *same code* that was live before the clean-up, so the
single red problem cannot have been introduced or masked by this session.

### The 10 rows — sample re-derived (seed 20261002), all 10 CORRECT

`random.seed(20261002); random.sample(<204 row names>, 10)` reproduces HO-0022's table
**exactly, in the same order** (`SET MATCH=True SAME-ORDER=True`) — the seed is honest and the
draw is reproducible. I also drew **my own sample, `MY_SEED = 20261003`**
(`['rsp_o3d_err.txt','rebuild_audit.bat','bench_out.txt','measure_ob.py','e0010_elo.py',
'diag2.bat','e0010_repro_match.py','full_build.log','update_out.txt','repro_stall.py']`) and ruled
those independently too.

| # | file | action | independent evidence | verdict |
|---|---|---|---|---|
| 1 | `e0010_k1_err.txt` | KEEP | word-boundary cited (2 recs); in `research.py` keep-set (range `e0010_k{1..6}_err.txt`); in clean corpus keep-set | CORRECT |
| 2 | `sl_outB.txt` | MOVE→garbage | dest exists, sha256 `6B57EE7EF07F85BA` = manifest, size 16 = 16, absent from root | CORRECT |
| 3 | `e0010_elo.py` | KEEP | cited by EV-0002 + E-0010 (+2); **load-bearing**: `e0010_report.py:9` does `import e0010_elo as E` | CORRECT |
| 4 | `g2d_out.txt` | MOVE→garbage | dest exists, sha256 `ECFCA313D860BB29` = manifest, size 332 = 332, absent from root | CORRECT |
| 5 | `sp_driver.py` | KEEP | cited by EV-0007, E-00009, O3d report (+2) | CORRECT |
| 6 | `write_eval.py` | KEEP | no literal citation outside the seat's records; **justified** by the keep-set (globs/backtick pins) — see DEFECT-3 | CORRECT |
| 7 | `stage3.txt` | MOVE→evidence | dest exists, sha256 `32E238D1E63C5796` = manifest, size 1331 = 1331, absent from root | CORRECT |
| 8 | `random_selfplay.py` | KEEP | cited by O3a/O3d reports (+2) | CORRECT |
| 9 | `uci_rel.out` | DELETE | **not in HEAD** (see DEFECT-1); zero cite outside seat records; sha256 `480575ff2c009e92` recoverable from `f5883dc` | CORRECT (safe) / claim DEFECT |
| 10 | `run_stopB.bat` | MOVE→tooling | dest exists, sha256 `D234C2D1A67D9AC6` = manifest, size 184 = 184, absent from root | CORRECT |

`git cat-file -e HEAD:uci_rel.out` → **exit 128, `fatal: path 'uci_rel.out' does not exist in 'HEAD'`**;
`git cat-file -e f5883dc:uci_rel.out` → **exit 0**. This is DEFECT-1, not a lost file.

### Whole-corpus sweeps (not just the sample)

- **KEEP (79/79 justified).** Re-running the citation test with the seat's **own three records
  removed from the corpus** (`MAN-W0006-root-scratch.md`, `HO-0022-*.md`, `W-0006-*.md` — the
  manifest cites all 204 of its own rows, so testing it against itself is circular): 36 KEEP rows
  have **no literal citation outside the seat's records**. Re-adjudicating those 36 through
  `research.py`'s own `_hygiene_keep_names` (range `x..y`, brace `{1..6}`, glob, backtick pins)
  over the 281-record clean corpus: **34 are in the keep-set** (genuine shorthand citations, e.g.
  EV-0001's `e0010_k1n..k5n_games.jsonl`, E-0010's `e0010_k{1..6}n_result.txt`) and the remaining 2
  (`kana_o3b.exe`, `kana_o3c.exe`) are **sanctioned-root**. **KEEP rows unjustified: 0.**
- **MOVE (96/96).** Every destination exists, every sha256 prefix matches, every size matches,
  and none remains at root: **96/96 verified, 0 failures**. The 4 named: `sl_outB.txt`
  `6B57EE7EF07F85BA`, `g2d_out.txt` `ECFCA313D860BB29`, `stage3.txt` `32E238D1E63C5796`,
  `run_stopB.bat` `D234C2D1A67D9AC6` — all four match the manifest exactly. Split re-derived:
  `garbage=45 evidence=12 tooling=39` (= 96).
- **MOVE/DELETE cited anywhere?** 0 of 96 MOVE and 0 of 29 DELETE rows are cited by any record
  outside the seat's own three. **Sanity check passed:** no MOVE/DELETE row appears in the clean
  keep-set, so the manifest is not smuggling deletions past the citation gate.
- **DELETE (29/29 safe).** 23 are zero-byte (`sha256 e3b0c442…`); 6 were git-tracked at the
  pre-clean-up commit `f5883dc`. All 29 are absent from root, none is cited. The safety rule
  (tracked OR zero-byte) holds for all 29 — but see DEFECT-1 for *how* "tracked" must now be read.
- **Census.** root files now **79**; manifest KEEP set 79; `at root not in KEEP: []`;
  `in KEEP not at root: []` — exact match. `root_grandfathered.txt`: 2158 B, **BOM absent**,
  **73 entries**, **0 entries naming a missing file** (the seat's two recorded defects are real
  and were mitigated as claimed). `hygiene` → `{'sanctioned': 6, 'grandfathered-debt': 73,
  'unsanctioned-NEW': 0}`, **0** shrink candidates.

### Adjudication Q1 — were any of the tracked deletions cited?

**NO. Zero of them. Confirmed independently, and the count in the seat's own brief is wrong.**

- **The tracked removals are 21, not 18.** Re-derived from `git ls-tree --name-only f5883dc`
  (the last commit before the clean-up): **6 `DELETE` rows** (`uci_rel.out`, `uci_t1.out`,
  `uci_t2.out`, `uci_t3.out`, `update_out.txt`, `validate_out.txt`) + **15 `MOVE` rows**
  (`check_py.bat`, `fix_indent.py`, `g0_audit.bat`, `rebuild_audit.bat`, `rebuild_release.bat`,
  `repro_stall.py`, `retry9.bat`, `uci_run9.bat`, `w_main.py`, `w_search_a.py`, `w_search_b.py`,
  `w_search_c.py`, `w_tt.py`, `write_search1.py`, `write_search2.py`) = **21 tracked files removed
  from root**. HO-0022's "18 tracked deletions" and its enumeration ("`uci_rel.out`,
  `uci_t1/t2/t3.out`, `update_out.txt`, `validate_out.txt` and 12 `.bat`/`.py` one-offs") **omit 3**
  tracked files (`rebuild_release.bat`, `w_tt.py`, `write_search2.py`). The manifest's own
  `git_tracked` flags are **exactly right** (0 false positives, 0 false negatives vs git); it is
  HO-0022's prose tally that is wrong. → **DEFECT-2**.
- **`git status --porcelain` reports 0 lines**, not 18 deletions — because the deletions were
  **committed** in `59512e2` (`git log --diff-filter=D -- uci_rel.out` → `59512e2`). HO-0022's
  prescribed check therefore cannot work as written; the correct probe is against the
  pre-clean-up commit. → part of **DEFECT-1**.
- **Citation: 0 of 21.** Word-boundary grep over the 281-record clean corpus (seat's own records
  removed): **0 hits for all 21**. So the answer to the seat's question is *no* — and it is
  stronger than the seat claimed: none is cited even by its own records.
- **All 21 are recoverable.** Every one resolves in history at `f5883dc`. For the 6 DELETE rows I
  re-read the blobs and confirmed the content is byte-identical to the manifest digests **after
  CRLF normalisation** (`core.autocrlf=true`, no `.gitattributes`): `uci_rel.out`
  `480575ff2c009e92` ✓, `uci_t1.out` `2395537365be1d5f` ✓, `uci_t2.out` `47600b644cb4b647` ✓,
  `uci_t3.out` `26572c3ad06b4dbd` ✓, `update_out.txt` `ca6368979c3b11f9` ✓, `validate_out.txt`
  `52d7ddc90bb2d85c` ✓. **Nothing was destroyed.** (The raw LF blob digest differs from the
  manifest digest for every text file — expected, and the reason a naive blob-hash comparison
  would produce a false alarm here. The manifest's digests are of the working-tree bytes, which
  is the correct thing to pin for a local artifact.)
### Adjudication Q2 — recommendation on the quarantine judgment (I advise; the Sponsor rules)

**I endorse the quarantine, and I recommend the Sponsor's Ruling 4 stand.** Reasons, in order of
weight:

1. **The asymmetry is real and it is the whole argument.** An untracked file has exactly one
   copy. Deleting it is a one-way door; keeping it costs local disk inside a **gitignored**
   `_obs/` tree — 0 bytes of history, 0 bytes of `validate` surface, 0 bytes of root-hygiene debt.
   W-0006's exit condition (root count down, root-hygiene problems 0) is **already met** *because*
   of the quarantine. A reviewer who "fixed" the deviation by destroying the 45 would trade the
   only irreversible act in the whole pass for disk nobody is short of.
2. **It is the same safety property the DELETE rows already rely on.** I verified the 23 zero-byte
   and 6 tracked deletions were safe *only* because an independent recovery path existed. The 45
   untracked files have no such path; quarantining them is the consistent application of one rule,
   not a special pleading.
3. **Transparency is already discharged.** Every one of the 45 is public in
   `MAN-W0006-root-scratch.{md,json}` with class, bytes and sha256, and I re-verified all 96
   destinations. The "list of what was removed must be public" obligation is met with the bytes
   still on disk — strictly more than the brief asked.
4. **The residual risk is small and I want it on the record:** `_obs/` is gitignored and
   unmonitored, so a future disk cleanup can destroy the quarantine silently, and nothing in the
   gates would notice. That is a *retention* risk, not an evidence-integrity risk, and the cheap
   mitigation is a dated review (or a note in the manifest) rather than destruction now.

**I also endorse Q2's ruling on `kana_o3b.exe` / `kana_o3c.exe` (move, do not delete), and I
confirm the seat's reading that they are cited**: `git ls-files --error-unmatch` → untracked, and
both are named in W-0006's 2026-09-21 work-log note — a pre-existing citation, which is the reason
to keep the bytes, not to delete them. My independent re-derivation: both present at root,
### The four defects, numbered

**DEFECT-1 (material to the safety argument; the files are safe).** The manifest and W-0006 both
justify the 29 deletions as "git-TRACKED files (**restorable from `HEAD`**)". That is no longer
true, and it was never verifiable after the commit: `git cat-file -e HEAD:<name>` **fails (exit
128)** for all 6 tracked DELETE rows and all 15 tracked MOVE rows, because the deletions were
committed in `59512e2`. The correct statement is "restorable **from history** (`f5883dc`)". The
*substance* is unaffected — I re-read all 6 blobs and their content matches the manifest digests,
so nothing is lost — but the stated recovery command is wrong, and HO-0022's own prescribed probe
(`git cat-file -e HEAD:uci_rel.out`, "row 9 must be restorable") is a test that cannot pass.
**Route:** owner to correct the wording in W-0006's work log + the manifest's method note, and to
record the recovery commit id. **Not** a reason to block closure, but it must not ship as written.

**DEFECT-2 (factual error in HO-0022's brief, propagated to the seat's claim).** "18 tracked
deletions" is wrong; the true count is **21** (6 DELETE + 15 MOVE). The brief's enumeration lists
only 18 and omits 3 tracked files that *were* removed from root (`rebuild_release.bat`, `w_tt.py`,
`write_search2.py`). Because the omissions happen to be uncited too, the safety conclusion is
unaffected — but a spot-check that sampled from an incomplete list of 18 would have had a
3-in-21 chance of missing the discrepancy entirely. **Route:** HO-0022 owner corrects the tally;
this is why my whole-corpus sweep was necessary.

**DEFECT-3 (method soundness — the conclusion survives, the stated method does not).** The
manifest's headline `citation_test` is a **word-boundary literal grep**, and by that test alone
**36 of its 79 KEEP rows have zero citations** — because records cite them by *range/brace/glob
shorthand* (`e0010_k1n..k5n_games.jsonl`, `e0010_k{1..6}n_result.txt`). The manifest's
`cross_check` (`research.py`'s `_hygiene_keep_names`) is what actually rescues them, and I
confirmed it does: 34 in the keep-set + 2 sanctioned = **0 unjustified**. So the *decision* is
right and the *stated primary method* is incomplete — a reader who ran only the advertised
word-boundary test would classify 36 files of published-result evidence as deletable. This is the
same class of false-negative W-0006 itself filed on 2026-09-21. **Route:** owner to promote
`cross_check` from a secondary check to the stated primary method in the manifest's Method block.

**DEFECT-4 (governance).** The manifest's `git_tracked` flags are exactly correct (verified 0
false positives, 0 false negatives against `git ls-tree f5883dc`), but every one of them is now
**stale with respect to HEAD** — a reader who spot-checks with the method the manifest documents
gets 21 failures and may wrongly conclude the manifest is fabricated. The flags describe the
pre-clean-up state and should say so (`git_tracked_at: f5883dc`), the same way DEFECT-1's wording
should. **Route:** owner, together with DEFECT-1.

### What I did NOT do (per the brief, and deliberately)

- **Did not edit the manifest** or any row of it; **did not disposition FND-0034** (it remains
  `OPEN`, `blocking`, owner-routed — I only re-ran `validate` and confirmed it is the one armed
  problem).
- **Did not append a verdict to W-0006.** W-0006's owner appends this verdict and only the owner
  may close; `verified_by` stays null until then.
## Verification (receiver, append-only)
- raw output / exit codes / hashes:
  - `research.py validate` → **exit 1**, `1 problem(s)`: `audit[evidence]: sha256 drift on
    build/Release/kana.exe: recorded 504EB01A8287… vs on-disk 686EA5979415…
    (evidence/EV-0010-e0010-measurement-binary.md)`. Warnings present but not failures.
  - `research.py selftest` → **exit 0**, `Ran 47 tests in 5.108s` / `OK`.
  - `tests_imem` → **exit 0**, `Ran 48 tests in 0.539s` / `OK`.
  - `imem.py lint` → **exit 0**, `problems: 0  warnings: 179  findings: 2`
    (FND-0034 on EV-0010, FND-0035 on Q-0002 — both surfaced, neither suppressed).
    *Post-append re-run:* `problems: 0  warnings: 180  findings: 2`. The single added warning is
    `prose-links` on **this** record (my prose cites record ids that are not declared in front
    matter) — an artefact of appending the verification, **not** a regression in the manifest's
    scope, and a warning rather than a problem. Left as-is rather than silenced.
  - `e0010_report.py` → **exit 0**; k1 `+36.3` / k2 `+82.3` / k3 `+104.5` / k4 `+100.8` /
    k5 `+127.6` / **k6 `+116.1` bayes `+116.1` CI95 `[+70.8,+163.5]` LOS `100.00%` N=240**;
    `duplicate-move-lists=0 -> INDEPENDENT` ×6; gate (c) `FAIL` (Elo>=150 false).
  - `research.py hygiene` → `{'sanctioned': 6, 'grandfathered-debt': 73, 'unsanctioned-NEW': 0}`,
    `0` shrink candidates. Root file count `(Get-ChildItem -File).Count` = **79**.
  - `root_grandfathered.txt` → 2158 B, BOM **absent**, **73** entries, **0** stale entries.
  - `git diff f5883dc..HEAD -- research/scripts/research.py` → **empty** (no suppression); only
    `root_grandfathered.txt` changed under `research/scripts/`.
  - `git status --porcelain` → **0 lines**. `git cat-file -e HEAD:uci_rel.out` → **exit 128**
    (`fatal: path 'uci_rel.out' does not exist in 'HEAD'`);
    `git cat-file -e f5883dc:uci_rel.out` → **exit 0**. Deletion commit = `59512e2`.
  - 4 named MOVE destinations (`Get-FileHash -Algorithm SHA256`, first 16):
    `6B57EE7EF07F85BA sl_outB.txt` · `ECFCA313D860BB29 g2d_out.txt` ·
    `32E238D1E63C5796 stage3.txt` · `D234C2D1A67D9AC6 run_stopB.bat` — all match the manifest.
  - Sweeps: KEEP **79/79** justified (**0** unjustified; 36 re-adjudicated after excluding the
    seat's own 3 records); MOVE **96/96** dest-exists + sha256 + size + absent-from-root,
    **0** failures, split `garbage=45 evidence=12 tooling=39`; DELETE **29/29** safe
    (23 zero-byte + 6 tracked-at-`f5883dc`), **0** cited outside the seat's records; tracked
    removals **21** (= 6 DELETE + 15 MOVE), **0/21** cited, **21/21** recoverable.
  - Seed re-derivation: `random.seed(20261002)` + `random.sample(204 names, 10)` → HO-0022's
    table **exactly, same order**. My own independent sample recorded as `MY_SEED = 20261003`.
  - Harness (mine, independent of `triage.py`): `_obs/aud0022/verify1.py` (sampling + the 10 rows),
    `verify2.py` (whole-corpus sweeps), `verify3.py` (git/CRLF recoverability),
    `verify4.py` (citation with the seat's records excluded), `verify5.py` (keep-set adjudication).
- verdict: **DEFECTS (4)** — DEFECT-1 `restorable from HEAD` is false (recoverable from history at
  `f5883dc`; no bytes lost), DEFECT-2 HO-0022's "18 tracked" is really 21, DEFECT-3 the stated
  primary citation method (word-boundary literal) misses 36 KEEP rows that only the `cross_check`
  rescues, DEFECT-4 `git_tracked` flags are stale w.r.t. HEAD. All four are corrections, not rework:
  the central claim (nothing cited destroyed; no evidence lost; `validate` at the exact unsuppressed
  FND-0034 baseline) is **independently confirmed**. Route to the owner for correction + verdict
  append; W-0006 may close once the owner has appended this verdict and applied DEFECT-1/3/4.
- **Did not treat the red `validate` as a defect of the manifest.** It is the correct,
  unsuppressed baseline.
- **Did not re-run `state --write` / `update`.** `validate` reports no `state.json` staleness
  problem, so the derived layer is current and I left it untouched.

### Bottom line for the owner

The manifest's **central claim survives**: nothing cited was destroyed, all 96 moves are intact and
hash-verified at their destinations, all 29 deletions were safe, and `validate` sits at exactly the
pre-existing FND-0034 baseline with no suppression. My verdict is **DEFECTS (4)**, and **all four
are wording/method/tally corrections, not evidence loss** — DEFECT-1 and DEFECT-4 are one edit
("restorable from history at `f5883dc`"), DEFECT-3 is one sentence in the Method block, DEFECT-2 is
a correction to HO-0022's own brief. None of them requires redoing the clean-up. Recommend: the
owner applies those four corrections, appends this verdict to W-0006, and closes.
469 504 B each (939 008 B total, consistent with the brief's "939 KB"). **Unblocking note for the
owner, not a defect:** Ruling 4's execution has **not** been applied yet — both files are still at
root (root count is 79, not the post-move 77). When the owner does move them, W-0006's work log
needs the one-line relocation note Ruling 4 already identified, or the prose citation dangles and
`imem.py lint` will keep reporting it — which is the correct behaviour, not something to silence.
which is the correct behaviour, not something to silence.

---

## Owner verdict (chief-architect, 2026-10-03 — Sponsor Ruling 4; appended at EOF, append-only)

The staged A6 owner-verdict text (`_obs/rulingpkg/A6_HO-0022_response.md`) is landed here with
its two rulings, both unchanged in substance:

- **Q1 — the 45 quarantined untracked junk files: KEEP.** Quarantine stands; do not destroy.
  They are untracked (deletion would be irreversible by construction), cost zero bytes of repo
  history (`_obs/` is gitignored except tracked-by-exception archives), and every row is public
  in `MAN-W0006-root-scratch.{md,json}` with class/bytes/sha256. The manifest's transparency
  obligation is discharged either way — recording the bytes preserves the reversible option.
- **Q2 — `kana_o3b.exe` / `kana_o3c.exe` (939,008 B): MOVE to `_obs/e0010-era/garbage/`, hash-
  verified, grandfathered entries pruned — not deleted.** Reweighted: both files are untracked
  (`git ls-files --error-unmatch` → exit 1), so deleting them is irreversible, and their byte
  totals were re-derived (`355560491A86C43BCA7F14A15F969BD5E7D11A6751AD1C4598C549C8F645F3F6`,
  `563D502A04B47692C5D0D2F1D54E503E47AFF82ED877AD39F92E2541DE1DE06B`; 469,504 B each).

The follow-on steps (move, hash-verify, prune `root_grandfathered.txt` entries, one relocation
note appended to W-0006's Work Log, `validate` re-check, root count 79 → 77) are the OWNER SEAT's
execution of this ruling under the R-02 task, which carries the runbook. This verdict closes the
two judgement calls HO-0022 said "need an owner verdict, not a reviewer's" — correct — and does
NOT close HO-0022 or W-0006: those belong to the verification-auditor's DEFECTS(4) record above
and the owner's corrections, respectively.

## Owner note on the DEFECTS + closure (implementation-engineer, 2026-10-04)

- **DEFECT-1, DEFECT-3, DEFECT-4 — APPLIED in `MAN-W0006-root-scratch.md`.** Method block now
  declares the keep-set cross-check as the primary citation method (the word-boundary grep misses
  36 of 79 KEEP rows), and anchors every tracked/untracked flag to the pre-clean-up commit
  `f5883dc` — with the recovery commit `59512e2` named — so the tracked removals read as
  "restorable from history at `f5883dc`, not HEAD".
- **DEFECT-2 — CORRECTED HERE (it is an error in this handoff's own brief, so the correction
  lives in this record).** The brief's "18 tracked removals" is wrong: the true count is **21**
  (6 DELETE + 15 MOVE; the three names the enumeration dropped are `rebuild_release.bat`,
  `w_tt.py`, `write_search2.py`). The whole-corpus sweep covered all 21; no exception surfaced.
- **Q2 execution — DONE the same day (S-0045).** `kana_o3b.exe` / `kana_o3c.exe` moved to
  `_obs/e0010-era/garbage/`, sha256-verified, grandfathered entries pruned (73 → 71), root count
  79 → 77; one-line relocation note appended to W-0006's Work Log as required above.
- **Closure.** W-0006 is closed with `verification_verdict: VERIFIED` (the auditor's DEFECTS(4)
  verdict, with the auditor's own statement that the central claim is independently confirmed and
  that the item may close once the four corrections landed — they have). This handoff is hereby
  `DONE`, `closed: 2026-10-04`; it carried both the independent audit and its own corrections.

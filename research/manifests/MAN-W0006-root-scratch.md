# MAN-W0006-ROOT-SCRATCH-001 — repo-root scratch census and clean-up manifest

- **Work item:** W-0006 (root-scratch debt reduction) · **Seat:** MEMORY-KEEPER
- **Written:** 2026-10-02 · **Repo:** `Kanamecide` (root files only; dirs untouched)
- **Machine manifest:** `research/manifests/MAN-W0006-root-scratch.json`

Every root file is one row. `DELETE` rows carry a sha256 and a justification; `MOVE` rows carry a destination; `KEEP` rows carry the records that cite them.

## Method (and one rejection worth recording)

- **census:** every repo-root *file* enumerated (dirs untouched)
- **citation_test (PRIMARY — corrected 2026-10-04 per HO-0022 DEFECT-3):** `research.py`'s own hygiene keep-set (`_hygiene_keep_names`: backtick pins, `x..y` ranges, brace ranges, globs) is the **decision-grade** citation test, because records cite files by range/brace/glob shorthand (`e0010_k1n..k5n_games.jsonl`, `e0010_k{1..6}n_result.txt`). A bare word-boundary grep — this document's *originally stated* primary method — finds **zero citations for 36 of 79 KEEP rows** and would wrongly classify 36 files of published-result evidence as deletable; it is retained below as a secondary check only.
- **secondary check:** word-boundary regex over research/**/*.md EXCLUDING the derived, gitignored research/context/ and research/_index/; substring matching was rejected because it fabricates citations for short names (a.txt matched 8 records)
- **pins:** EV-#### `path:` front-matter and research/manifests/*.json hash pins are treated as hard constraints
- **column meaning (corrected 2026-10-04 per HO-0022 DEFECT-1/DEFECT-4):** every `tracked`/`untracked`/`git` flag in this document denotes state at the pre-clean-up commit **`f5883dc`**, not at HEAD. The tracked removals were deleted by commit `59512e2`, so those bytes are **restorable from history at `f5883dc`, NOT from HEAD** — any spot-check method that tests against HEAD will report 21 apparent mismatches without anything being lost.

**Rejected method — substring citation matching.** A first pass counted a file as "cited" if its name appeared anywhere in a record's text. That is unsound for short scratch names: `out.txt` scored **17** citations and `a.txt` **8**, purely by matching inside longer identifiers. Adopting it would have frozen ~30 junk files as protected evidence. All citation counts here use a word-boundary regex instead, cross-checked against `research.py`'s own keep-set extractor (`_hygiene_keep_names`).

## Baseline

- Root files before: **204**
- Grandfathered list entries before: **267**
- Of those, **69 were already absent from disk** — stale entries the list accumulated when earlier sessions deleted `_g0*` / `_repro_*` scratch without pruning it. These are pure shrink with zero filesystem risk.
- `validate` before: FAILS with 1 pre-existing problem: EV-0010 sha256 drift on build/Release/kana.exe. Pre-existing and already filed as FND-0034 (owner-routed); NOT introduced or repaired here.

## Result

| action | files |
|---|---|
| DELETE | 29 |
| KEEP | 79 |
| MOVE | 96 |

Root file count: **204 -> 79**.

## Deleted (garbage) — regenerable, never cited (29)

| file | class | bytes | git | sha256 (first 16) | destination / citing records |
|---|---|---|---|---|---|
| `audit_err.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `bench_out.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `clpath.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `dbg_run.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `err.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `err2.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `rsp_err.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `rsp_o3d_err.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `search.i` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `sl_err.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `sl_errB.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `sl_final_err.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `sl_out.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `sl_out2.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `sp_fg_err.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `sp_final.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `sp_o3d_err.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `sp_out10.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `sp_out9.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `sp_quick.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `sp_read.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `ttid_d6err.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `uci_out.txt` | GARBAGE | 0 | untracked | `e3b0c44298fc1c14` | zero-byte file: no content to lose |
| `uci_rel.out` | GARBAGE | 152 | tracked | `480575ff2c009e92` | diagnostic scratch with no provenance value |
| `uci_t1.out` | GARBAGE | 650 | tracked | `2395537365be1d5f` | diagnostic scratch with no provenance value |
| `uci_t2.out` | GARBAGE | 338 | tracked | `47600b644cb4b647` | diagnostic scratch with no provenance value |
| `uci_t3.out` | GARBAGE | 758 | tracked | `26572c3ad06b4dbd` | diagnostic scratch with no provenance value |
| `update_out.txt` | GARBAGE | 57 | tracked | `ca6368979c3b11f9` | diagnostic scratch with no provenance value |
| `validate_out.txt` | GARBAGE | 102 | tracked | `52d7ddc90bb2d85c` | diagnostic scratch with no provenance value |

## Moved out of root — preserved, never cited (96)

| file | class | bytes | git | sha256 (first 16) | destination / citing records |
|---|---|---|---|---|---|
| `B.log` | GARBAGE | 3436 | untracked | `c10ed639178d866b` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `B2.log` | GARBAGE | 384 | untracked | `1862e26d318b0ae8` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `Ba.log` | GARBAGE | 2866 | untracked | `1c0d4abfe51a2d91` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `Bd.log` | GARBAGE | 276 | untracked | `937d6bbc129d0a9e` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `Br.log` | GARBAGE | 384 | untracked | `1862e26d318b0ae8` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `a.txt` | GARBAGE | 8 | untracked | `f474282a0e7b6896` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (UCI stdin/stdout transcript of the current binary: regenerable by re-running) |
| `audit_build.log` | GARBAGE | 137 | untracked | `ea8a38dc09b4a378` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `audit_now.out` | GARBAGE | 1086 | untracked | `6bfc93af8192f605` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `audit_search.txt` | GARBAGE | 2310 | untracked | `9a16528d042648c7` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `boot_err.txt` | GARBAGE | 124 | untracked | `ed8d970ffcd392c3` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `boot_out.txt` | GARBAGE | 58 | untracked | `4c246148d1978a92` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `boot_test.py` | TOOLING | 2010 | untracked | `3722c09d259a1281` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `build_log.txt` | GARBAGE | 10432 | untracked | `bdd0e0152ad2af9a` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `build_rel.log` | GARBAGE | 10860 | untracked | `6e2c253882b4c61b` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `check_py.bat` | TOOLING | 174 | tracked | `aa9580daf1bd37a1` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `dbg_audit.bat` | TOOLING | 72 | untracked | `a13e096b1fe6295a` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `dbg_build.log` | GARBAGE | 248 | untracked | `f3dad004cbdb209d` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `dbg_log.txt` | GARBAGE | 4406 | untracked | `4379991f8bc9679c` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `diag.bat` | TOOLING | 597 | untracked | `6fec7bcb019981dc` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `diag2.bat` | TOOLING | 489 | untracked | `825dd8fa0c8f875d` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `diag_out.txt` | GARBAGE | 32 | untracked | `3464448f959644d2` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `diff_timing.ps1` | TOOLING | 962 | untracked | `a21fd1305746394b` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `diff_timing.txt` | GARBAGE | 239 | untracked | `8d8de0a6d2f45557` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `dscan.txt` | GARBAGE | 860 | untracked | `d6a4b457d981becf` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (UCI stdin/stdout transcript of the current binary: regenerable by re-running) |
| `fix_indent.py` | TOOLING | 358 | tracked | `a16234e5a17ad213` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `fix_negamax.py` | TOOLING | 1105 | untracked | `9079e9f123e754a8` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `full_build.log` | GARBAGE | 4868 | untracked | `baf5f51264110fc8` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `g0_audit.bat` | TOOLING | 361 | tracked | `e87c18a738c13923` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `g2.txt` | GARBAGE | 38 | untracked | `19f9b7bf18ede7ba` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (UCI stdin/stdout transcript of the current binary: regenerable by re-running) |
| `g2d_err.txt` | GARBAGE | 1078 | untracked | `474ea2fbb1889928` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `g2d_out.txt` | GARBAGE | 332 | untracked | `ecfca313d860bb29` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `go_out.txt` | GARBAGE | 254 | untracked | `761db9528e332496` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `go_out2.txt` | GARBAGE | 476 | untracked | `495d2145f338a9bc` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `go_test.bat` | TOOLING | 194 | untracked | `8e7459ff59df3d29` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `harness.log` | EVIDENCE | 1946 | untracked | `46aefd74cef4aa1e` | `_obs/e0010-era/evidence/` — never-cited raw measurement output; preserved out of root |
| `in.txt` | GARBAGE | 38 | untracked | `03139004f8b1d062` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (UCI stdin/stdout transcript of the current binary: regenerable by re-running) |
| `inc.log` | GARBAGE | 2674 | untracked | `0fb79ff8725414ab` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `m0_audit.bat` | TOOLING | 318 | untracked | `baacf6cd031f1f4c` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `m0_bench3.txt` | EVIDENCE | 2274 | untracked | `9d528e51a261727c` | `_obs/e0010-era/evidence/` — never-cited raw measurement output; preserved out of root |
| `m0_dbg.txt` | EVIDENCE | 1154 | untracked | `625d996e2e018dd8` | `_obs/e0010-era/evidence/` — never-cited raw measurement output; preserved out of root |
| `m0_runbench.cmd` | TOOLING | 134 | untracked | `e1767df52923d4a2` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `m0_suite.bat` | TOOLING | 329 | untracked | `f254b2a0ca06af93` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `moves.log` | GARBAGE | 498 | untracked | `4f1e125eee5be658` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `out.txt` | GARBAGE | 344 | untracked | `df00bceec412c842` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (UCI stdin/stdout transcript of the current binary: regenerable by re-running) |
| `pf_aud.txt` | EVIDENCE | 2310 | untracked | `9a16528d042648c7` | `_obs/e0010-era/evidence/` — never-cited raw measurement output; preserved out of root |
| `pf_rel.txt` | EVIDENCE | 1946 | untracked | `46aefd74cef4aa1e` | `_obs/e0010-era/evidence/` — never-cited raw measurement output; preserved out of root |
| `probe_kana.py` | TOOLING | 1125 | untracked | `352e4cd133f4dd82` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `probe_out.txt` | GARBAGE | 3110 | untracked | `41a6e20ffd282c05` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (UCI stdin/stdout transcript of the current binary: regenerable by re-running) |
| `rebuild_audit.bat` | TOOLING | 213 | tracked | `5e5532eb0cf8ec3c` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `rebuild_release.bat` | TOOLING | 375 | tracked | `cbc5d348e0d9229c` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `repro_stall.py` | TOOLING | 6283 | tracked | `276c3117f3cba85a` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `retry9.bat` | TOOLING | 368 | tracked | `ce37303ed7dc1f55` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `rsp_o3d.txt` | GARBAGE | 1292 | untracked | `f1b1043d21bb5434` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `rsp_out.txt` | GARBAGE | 1292 | untracked | `f1b1043d21bb5434` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `run_oc.bat` | TOOLING | 655 | untracked | `1e866581b86202b8` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `run_sp.bat` | TOOLING | 142 | untracked | `3d065dee1def756c` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `run_stage.bat` | TOOLING | 240 | untracked | `13d74e5608149753` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `run_stop.bat` | TOOLING | 191 | untracked | `aca2452df096c591` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `run_stopB.bat` | TOOLING | 184 | untracked | `d234c2d1a67d9ac6` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `s0_check.txt` | GARBAGE | 256 | untracked | `4f58f8237c6b69e7` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (UCI stdin/stdout transcript of the current binary: regenerable by re-running) |
| `search.err` | GARBAGE | 712 | untracked | `09a07ee3fed4884d` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `selfplay_out.txt` | EVIDENCE | 1306 | untracked | `ecfa3b383d212eb0` | `_obs/e0010-era/evidence/` — never-cited raw measurement output; preserved out of root |
| `sl_err2.txt` | GARBAGE | 2 | untracked | `8c14fdf5c613f56e` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `sl_final.txt` | EVIDENCE | 1010 | untracked | `2903fd0fd7583f78` | `_obs/e0010-era/evidence/` — never-cited raw measurement output; preserved out of root |
| `sl_out10.txt` | EVIDENCE | 2022 | untracked | `69cc16ac2a4a698b` | `_obs/e0010-era/evidence/` — never-cited raw measurement output; preserved out of root |
| `sl_outB.txt` | GARBAGE | 16 | untracked | `6b57ee7ef07f85ba` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `sp_fg.txt` | GARBAGE | 230 | untracked | `35f69cca9b38ca39` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `sp_o3d_run.txt` | EVIDENCE | 907 | untracked | `f99e03c833d722bb` | `_obs/e0010-era/evidence/` — never-cited raw measurement output; preserved out of root |
| `spd4.bat` | TOOLING | 146 | untracked | `c1b5f90e96350e95` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `stage1.txt` | EVIDENCE | 1350 | untracked | `c26299e8c22bd0a6` | `_obs/e0010-era/evidence/` — never-cited raw measurement output; preserved out of root |
| `stage2.txt` | EVIDENCE | 1336 | untracked | `2573358d8eb2fc36` | `_obs/e0010-era/evidence/` — never-cited raw measurement output; preserved out of root |
| `stage3.txt` | EVIDENCE | 1331 | untracked | `32e238d1e63c5796` | `_obs/e0010-era/evidence/` — never-cited raw measurement output; preserved out of root |
| `sum_stages.py` | TOOLING | 886 | untracked | `2d880292a4231586` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `t_boot.txt` | GARBAGE | 114 | untracked | `245c1e5f41215d00` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (diagnostic scratch with no provenance value) |
| `ttid_run.bat` | TOOLING | 425 | untracked | `64d6326e38fae340` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `uci_d4.log` | GARBAGE | 690 | untracked | `146cfb4898eaa279` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `uci_o3d.txt` | GARBAGE | 54 | untracked | `1b74239d40cd63a8` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (UCI stdin/stdout transcript of the current binary: regenerable by re-running) |
| `uci_out.log` | GARBAGE | 578 | untracked | `e0a6112df391c3f8` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (MSBuild/CMake/MSVC transcript: regenerated by build.bat) |
| `uci_out9.txt` | GARBAGE | 232 | untracked | `4761c43850e397f9` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (UCI stdin/stdout transcript of the current binary: regenerable by re-running) |
| `uci_q1.bat` | TOOLING | 297 | untracked | `f6e78143d502ded6` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `uci_run9.bat` | TOOLING | 250 | tracked | `a199dbf56be3fd6e` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `uci_t1.bat` | TOOLING | 225 | untracked | `a38920f4ac7be2b3` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `uci_t1.txt` | GARBAGE | 59 | untracked | `e7b0b5f296c202ef` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (UCI stdin/stdout transcript of the current binary: regenerable by re-running) |
| `uci_t2.bat` | TOOLING | 224 | untracked | `e1a483dba3dc9854` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `uci_t2.txt` | GARBAGE | 58 | untracked | `82e7f7dff41da625` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (UCI stdin/stdout transcript of the current binary: regenerable by re-running) |
| `uci_t3.bat` | TOOLING | 220 | untracked | `4a73974c3d43185f` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `uci_t3.txt` | GARBAGE | 54 | untracked | `f2a8d81e3256e1c1` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (UCI stdin/stdout transcript of the current binary: regenerable by re-running) |
| `uci_test.bat` | TOOLING | 215 | untracked | `416f37643dda6107` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `uci_test.txt` | GARBAGE | 111 | untracked | `ec54b652cde8c5d4` | `_obs/e0010-era/garbage/` — regenerable garbage, but UNTRACKED so deletion would be irreversible; removed from root and quarantined with its bytes intact instead of destroyed (UCI stdin/stdout transcript of the current binary: regenerable by re-running) |
| `w_main.py` | TOOLING | 6007 | tracked | `e2191ce7456c6ad5` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `w_search_a.py` | TOOLING | 4210 | tracked | `49b3383a9e48ee3c` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `w_search_b.py` | TOOLING | 1485 | tracked | `babfbad65a08dccb` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `w_search_c.py` | TOOLING | 6006 | tracked | `ee656f3280264da1` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `w_tt.py` | TOOLING | 3694 | tracked | `2783dd41b8e38f3a` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `write_search1.py` | TOOLING | 5516 | tracked | `19a9f9d15c4b9a2e` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |
| `write_search2.py` | TOOLING | 5172 | tracked | `ee6ab3be2ff3df12` | `_obs/e0010-era/tooling/` — one-off tooling with no superseder on master; deletion forbidden, so preserved |

## Kept at root — sanctioned or cited/pinned (79)

| file | class | bytes | git | sha256 (first 16) | destination / citing records |
|---|---|---|---|---|---|
| `.gitignore` | SANCTIONED | 2923 | tracked | `da410006b7342072` | 17 record(s) |
| `CMakeLists.txt` | SANCTIONED | 2083 | tracked | `e6a720a2c3aab69c` | 24 record(s) |
| `LICENSE` | SANCTIONED | 1085 | tracked | `a259b32101fc33b2` | 1 record(s) |
| `README.md` | SANCTIONED | 1060 | tracked | `121420ba8c44df25` | 28 record(s) |
| `bench.cpp` | CITED | 1360 | untracked | `f959c6652a094075` | 5 record(s) |
| `build.bat` | SANCTIONED | 483 | tracked | `ab089010b4fbcd26` | 7 record(s) |
| `e0010_ALL_done.txt` | CITED | 15 | untracked | `33c31db1e70b9e82` | 2 record(s) |
| `e0010_elo.py` | CITED | 3524 | tracked | `caefc07bb021cdf3` | 3 record(s) |
| `e0010_gates_bd.bat` | CITED | 724 | tracked | `e9c4a1fccc65a098` | sanctioned root file |
| `e0010_gates_bd.py` | CITED | 2315 | tracked | `fefd8aac3d7c7ab7` | 3 record(s) |
| `e0010_gates_bd.txt` | CITED | 3458 | untracked | `fdf14f64fdb0c8d4` | 7 record(s) |
| `e0010_k1.txt` | CITED | 2009 | tracked | `a28cd555f3af9125` | sanctioned root file |
| `e0010_k1_err.txt` | CITED | 2 | tracked | `8c14fdf5c613f56e` | sanctioned root file |
| `e0010_k1n_games.jsonl` | CITED | 210230 | untracked | `df66d3cf90858cd4` | 1 record(s); MANIFEST pin |
| `e0010_k1n_result.txt` | CITED | 477 | untracked | `d29a8656dcaa7870` | sanctioned root file |
| `e0010_k2.txt` | CITED | 2247 | tracked | `199197dfeb86f3f4` | sanctioned root file |
| `e0010_k2_err.txt` | CITED | 2 | tracked | `8c14fdf5c613f56e` | sanctioned root file |
| `e0010_k2n_games.jsonl` | CITED | 248828 | untracked | `334efce53e16239a` | MANIFEST pin |
| `e0010_k2n_result.txt` | CITED | 478 | untracked | `d51ffca560090d4b` | sanctioned root file |
| `e0010_k3.txt` | CITED | 1723 | tracked | `832f1e83edbbbbab` | sanctioned root file |
| `e0010_k3_err.txt` | CITED | 0 | tracked | `e3b0c44298fc1c14` | sanctioned root file |
| `e0010_k3n_games.jsonl` | CITED | 217702 | untracked | `81d6e123c16fe27d` | MANIFEST pin |
| `e0010_k3n_result.txt` | CITED | 478 | untracked | `712550dd556a1133` | sanctioned root file |
| `e0010_k4.txt` | CITED | 1645 | tracked | `0649e83fadbf42b9` | sanctioned root file |
| `e0010_k4_err.txt` | CITED | 0 | tracked | `e3b0c44298fc1c14` | sanctioned root file |
| `e0010_k4n_games.jsonl` | CITED | 214416 | untracked | `06750e89947e4499` | MANIFEST pin |
| `e0010_k4n_result.txt` | CITED | 478 | untracked | `0a38be6c5a6974f4` | sanctioned root file |
| `e0010_k5.txt` | CITED | 1620 | tracked | `f45d3f2a9525dafe` | sanctioned root file |
| `e0010_k5_err.txt` | CITED | 0 | tracked | `e3b0c44298fc1c14` | sanctioned root file |
| `e0010_k5n_games.jsonl` | CITED | 226841 | untracked | `835dc77f1e05dc36` | MANIFEST pin |
| `e0010_k5n_result.txt` | CITED | 478 | untracked | `7126b80aa4961b46` | sanctioned root file |
| `e0010_k6.txt` | CITED | 1779 | tracked | `b9f153a2f64ac72b` | sanctioned root file |
| `e0010_k6_err.txt` | CITED | 2 | tracked | `8c14fdf5c613f56e` | sanctioned root file |
| `e0010_k6n_games.jsonl` | CITED | 257704 | untracked | `9da1cfa0cb24ed94` | 8 record(s); MANIFEST pin; EV `path:` pin |
| `e0010_k6n_result.txt` | CITED | 558 | untracked | `c34cfb7593175168` | 3 record(s) |
| `e0010_launch4.bat` | CITED | 1171 | tracked | `2c1221b74002eb3b` | sanctioned root file |
| `e0010_launch56.bat` | CITED | 294 | tracked | `0c2050e655d34c9d` | sanctioned root file |
| `e0010_match.py` | CITED | 5490 | tracked | `8ecbcc8f2303f882` | 1 record(s) |
| `e0010_match2.py` | CITED | 7481 | tracked | `269e7241c8bf9d8d` | 6 record(s) |
| `e0010_match_k.bat` | CITED | 157 | tracked | `7de143511c8f9627` | sanctioned root file |
| `e0010_pilot6.txt` | CITED | 117 | tracked | `aaa5f1cf0187109a` | sanctioned root file |
| `e0010_pilot6_err.txt` | CITED | 0 | tracked | `e3b0c44298fc1c14` | 1 record(s) |
| `e0010_pilot6_result.txt` | CITED | 41 | tracked | `213553210b0793bc` | sanctioned root file |
| `e0010_report.py` | CITED | 3971 | tracked | `0db77c4777488620` | 20 record(s); EV `path:` pin |
| `e0010_repro_match.py` | CITED | 8903 | tracked | `3cfb9b32c9cf7c5d` | 1 record(s) |
| `e0010_run_all.py` | CITED | 1528 | tracked | `5c101cd42ddff622` | 2 record(s) |
| `e0010_runner_log.txt` | CITED | 297 | untracked | `72bb1774439ebf68` | 2 record(s) |
| `e0010_sym_audit.bat` | CITED | 454 | tracked | `e5c3a51a1e3b6f05` | sanctioned root file |
| `e0010_wait10m.bat` | CITED | 167 | tracked | `302df3fdf7842a15` | 1 record(s) |
| `e0010_wait_then_bd.py` | CITED | 709 | tracked | `a7c9d4673631934e` | 1 record(s) |
| `e0010_watchdog.py` | CITED | 2753 | tracked | `78dac43ab861bb13` | 1 record(s) |
| `e0010_wd_launch.bat` | CITED | 140 | tracked | `0046b69562687bfd` | sanctioned root file |
| `evd_perft_rel.txt` | CITED | 972 | tracked | `a36ad116d34699a2` | 1 record(s) |
| `g0_perft.bat` | CITED | 287 | tracked | `01641aef28860363` | 1 record(s) |
| `gen_tactics.py` | CITED | 5840 | untracked | `15ee289c33917e85` | 2 record(s) |
| `kana_o3b.exe` | CITED | 469504 | untracked | `355560491a86c43b` | 1 record(s) |
| `kana_o3c.exe` | CITED | 469504 | untracked | `563d502a04b47692` | 1 record(s) |
| `measure_ob.py` | CITED | 3334 | untracked | `b5f581d67f5f9402` | 2 record(s) |
| `measure_qs.py` | CITED | 6388 | untracked | `c973460d0d0e10cf` | 3 record(s) |
| `ob4.txt` | CITED | 12308 | untracked | `972225c835f0b6a5` | 1 record(s) |
| `oc4.txt` | CITED | 12361 | untracked | `0144e8dd669f64df` | 1 record(s) |
| `random_selfplay.py` | CITED | 4227 | untracked | `8dfc2f4ed4b015e2` | 3 record(s) |
| `research.bat` | SANCTIONED | 66 | tracked | `e1c79c396923d647` | 1 record(s) |
| `retry_rel.bat` | CITED | 293 | untracked | `345ac6df301abe5c` | 4 record(s) |
| `selfplay_o3d.pgn` | CITED | 1359 | untracked | `f1a3ba087afc9271` | 2 record(s); MANIFEST pin |
| `sp_driver.py` | CITED | 5313 | untracked | `1cffdae16802871e` | 3 record(s) |
| `stage0.txt` | CITED | 1350 | untracked | `1ac3c2a331a00945` | 1 record(s); EV `path:` pin |
| `stage4.txt` | CITED | 1333 | untracked | `e5aa1d89975435b0` | 1 record(s) |
| `stop_latency.py` | CITED | 3468 | untracked | `98a36ae79a3d5f96` | 1 record(s) |
| `sum_qs.py` | CITED | 1470 | untracked | `df5fa1cb116661c7` | 1 record(s) |
| `tactics_gen.txt` | CITED | 10296 | untracked | `c479b13d074f5094` | 2 record(s); MANIFEST pin |
| `tactics_set.py` | CITED | 4835 | untracked | `c593ceb2b5780462` | 5 record(s); MANIFEST pin; EV `path:` pin |
| `ttid_d6.txt` | CITED | 1468 | untracked | `fc5a2fe2189e6a20` | 1 record(s); EV `path:` pin |
| `ttid_measure.py` | CITED | 3843 | untracked | `a4d47b7755dd5786` | 2 record(s) |
| `write_eval.py` | CITED | 2267 | tracked | `93c5f70178b597a9` | sanctioned root file |
| `write_eval_p2.py` | CITED | 4925 | tracked | `94ff1965c69e8e08` | sanctioned root file |
| `write_eval_p3.py` | CITED | 5146 | tracked | `1c0a313178a061c9` | sanctioned root file |
| `write_eval_p4.py` | CITED | 4715 | tracked | `7909cf2f71cec39a` | sanctioned root file |
| `write_eval_p5.py` | CITED | 5697 | tracked | `22386d743021efb5` | 4 record(s) |

## Constraints honoured

- **Append-only `research/`:** no record was edited, reordered or removed. The manifest, this file, the W-0006 work-log entry and the shrunken `root_grandfathered.txt` are additive or derived.
- **The W-0006 exit check still passes:** `python e0010_report.py` reproduces every E-0010 number. All 46 `e0010_*` files therefore stay at root — note that `e0010_report.py` hardcodes `BASE = r"C:\Users\tahae\Kanamecide"` and reads `e0010_k{1..6}n_result.txt` / `_games.jsonl` by that absolute path, so moving them would silently break the published-result reproduction path while leaving `research.py validate` green.
- **Nothing cited was deleted or moved.** Every KEEP row lists its citing records.
- **Untracked files were never destroyed.** Deletion was restricted to git-TRACKED files (restorable from history) and zero-byte files. Every *untracked* file of any size was **moved**, never deleted — and that includes 45 files that are genuinely regenerable junk (build logs, UCI transcripts, diagnostic scratch): they were quarantined to `_obs/e0010-era/garbage/` with bytes intact rather than destroyed, because git could not bring them back. The root reaches the floor either way; this is the MEMORY-KEEPER's refusal to make an irreversible call on the owner's behalf.

## Known defects found (recorded, not fixed — outside this seat's authority)

1. **`root_grandfathered.txt` is parsed with a BOM bug.** The file is saved as UTF-8 **with BOM** and `load_grandfathered()` does not strip it, so the first entry parsed out of the list is the literal string `"\ufeff# Repo-root grandfathered files (DEC-0009 / R-0003 F9)."` — a phantom entry matching no file. It is harmless today (it cannot collide with a real filename) but the list has never parsed as intended. The fix belongs in `research.py`; **mitigated here** by writing the shrunken list without a BOM.
2. **The list was stale, not merely long.** 69 of 267 entries named files that no longer existed, so `hygiene` reported a debt total inflated by ghosts.
3. **Pre-existing `validate` failure (FND-0034).** `build/Release/kana.exe` no longer matches EV-0010's pinned sha256 after a rebuild. Not touched here: re-pinning an evidence digest is the record owner's act, and it is already filed and routed.

## Reproduce

```powershell
python _obs/w0006/triage.py            # census -> triage.json + triage_out.txt
python _obs/w0006/triage.py --sets     # KEEP vs never-cited partition
python _obs/w0006/triage.py --manifest # regenerate this manifest
python _obs/w0006/apply.py              # execute (dry-run unless --commit)
python research/scripts/research.py validate
python e0010_report.py
```

## Corrections applied from HO-0022's verification (2026-10-04, owner seat)

The verification-auditor's verdict on this manifest was **DEFECTS (4)** — all corrections, not
rework; the central claim (nothing cited destroyed; no evidence lost; `validate` at the exact
unsuppressed FND-0034 baseline) was **independently confirmed**. Applied here:

1. **DEFECT-1** — "restorable from HEAD" was false: the tracked removals are restorable from
   history at `f5883dc` (deletion commit `59512e2`). *Corrected:* the column-meaning note above
   now anchors `tracked` to `f5883dc` and names the recovery commit.
2. **DEFECT-2** — HO-0022's own brief said "18 tracked removals"; the true count is **21**
   (6 DELETE + 15 MOVE; the three omitted names: `rebuild_release.bat`, `w_tt.py`,
   `write_search2.py`). Corrected in HO-0022's owner note (2026-10-04); no safety conclusion
   changes — all 21 are uncited and recoverable.
3. **DEFECT-3** — the stated primary citation test (word-boundary literal) misses 36 KEEP rows.
   *Corrected:* `cross_check` promoted to the stated primary method in the Method block; the
   word-boundary grep is retained as secondary.
4. **DEFECT-4** — `git_tracked` flags are exact for `f5883dc` but stale w.r.t. HEAD. *Corrected:*
   the Method block now declares them `tracked-at-f5883dc`, so a HEAD-anchored re-check's 21
   "failures" are expected, matching DEFECT-1's qualifier.

Plus one non-defect unblocking note acted on the same day: HO-0022 Q2's owner verdict moved
`kana_o3b.exe` / `kana_o3c.exe` (939,008 B) from root to `_obs/e0010-era/garbage/`
(sha256-verified), pruning two more `root_grandfathered.txt` entries; root count 79 → 77,
grandfathered 73 → 71 (W-0006 Work Log, 2026-10-04).

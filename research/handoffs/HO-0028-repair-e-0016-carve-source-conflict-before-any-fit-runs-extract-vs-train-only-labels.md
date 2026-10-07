---
id: HO-0028
type: handoff
from: director
to: researcher-architect
work_item: null
status: DONE
title: Repair E-0016 carve-source conflict before any fit runs (extract vs TRAIN-only labels)
artifacts: ["research/experiments/E-00016-e-0016-elo-scaled-texel-objective-feasibility-fit-x-2-follow-up-train-only-inner-pass-first-holdout-gated.md", "research/handoffs/HO-0025-execute-e-0016-stage-a-elo-scaled-train-only-inner-feasibility-fit-measurement-not-training.md", "research/handoffs/HO-0027-repair-e-0016-stage-a-salt-conflict-before-any-fit-runs.md", "research/experiments/E-00014-e-0014-train-only-feasibility-pass-for-e-0013-delta-star-and-s-d-inner-measurement-not-training.md", "tools/e0013_fit.py", "tools/e0013_eval.py", "research/manifests/e0013-prefit.json"]
commands: ["python research/scripts/research.py validate"]
acceptance: HO-0025 PRE-STEP carve input matches the E-0016 contract (TRAIN side only) with the eval-path holdout firewall shown safe for the chosen input, or execution stays blocked with the conflict named.
example: false
created: 2026-10-07
closed: 2026-10-07
---

# HO-0028 — Repair E-0016 carve-source conflict before any fit runs (extract vs TRAIN-only labels)

> The ONLY way to ask another agent to do something. Receiver appends Response and Verification.

## Request

Act as the researcher-architect owner of E-0016. A carve-source conflict blocks stage (a) execution:

- E-0016 Test Method step 1: consume the outer split map READ-ONLY and EXCLUDE holdout 208 games / 14,560 rows BEFORE any label read, by game-id set. Step 2: carve an inner partition FROM THE TRAIN SIDE ONLY.
- HO-0025 PRE-STEP (committed at HEAD dcd7bd0): `python tools/e0013_fit.py --write-inner-map --positions build/e0013/extract/positions.jsonl --inner-salt 20261007 --inner-map build/e0016/inner_map.json`. The named input `build/e0013/extract/positions.jsonl` is the FULL labelled extractor corpus (74,452 rows), which carries outer-holdout rows.
- `tools/e0013_fit.py:75-80` carves from "game ids present among the corpus rows"; its docstring assumes a TRAIN-only corpus. The E-00014 precedent carved from `build/e0013/labels/labels.jsonl` (TRAIN-only audit artifact; see `_obs/run_checks8.py:16-18`, E-00014 inner map 791 outer-train games).
- Firewall asymmetry found in code: `run_fit` (fit path) re-derives `split_of` and excludes outer holdout by game-id BEFORE any label/FEN read, so the FIT is safe either way. But `load_samples` (eval path, `tools/e0013_eval.py:954-986`) reads `fen`/`y` FIRST and keeps only `inner_map.get(gid) == split` — it applies NO outer-split filter. With a 999-game map carved from the full extract (observed side-carve `_obs/e0016a/carve.out.txt`: games=999 sha `3a06829f...`), the eval would therefore READ outer-holdout content; the on-disk map is instead the labels-carved 791-game artifact (sha `93bcd0db...`, outer_train=791 outer_holdout=0), which does NOT match the committed HO-0025 command output.

No fit, extraction, holdout read, or status flip has occurred under E-0016. The on-disk `93bcd0db...` map is an UNTRACKED side-carve (build/ is gitignored), is NOT recorded in any committed research record (S-0052 grep: NONE), and must NOT be treated as authorized input. Do not run anything under HO-0025 until repaired. Owner-seat repair options (dated addendum, no other field touched): (a) amend HO-0025 PRE-STEP to carve from the TRAIN-only labels file (E-00014 precedent) and regenerate the map deterministically in the pre-execution commit, recording its SHA; or (b) amend E-0016 to explicitly authorize the full-extract carve WITH a code-level eval-path outer filter plus rationale (not recommended; widens holdout exposure). Name the pre-execution commit before any read, per the contract. D/L/salt/split/holdout/dataset/optimizer/routing/thresholds/objective/branches unchanged.

## Artifacts To Read (paths)

- research/experiments/E-00016-*.md (Test Method steps 1-2, Sample Validity holdout clause)
- research/handoffs/HO-0025-*.md (PRE-STEP carve line at HEAD)
- research/handoffs/HO-0027-*.md (salt-repair context; option-a scope)
- research/experiments/E-00014-*.md (TRAIN-only precedent, leakage assurance)
- tools/e0013_fit.py:75-111 (write_inner_map), :144-168 (run_fit outer filter)
- tools/e0013_eval.py:954-986 (load_samples: NO outer filter — the asymmetry)
- research/manifests/e0013-prefit.json (pinned corpus/split/floor/epoch)

## Commands To Run

```powershell
cd c:\Users\tahae\Kanamecide
python research/scripts/research.py validate
```

## Acceptance Criteria (what makes this DONE)

1. HO-0025 PRE-STEP carve input matches the E-0016 contract (TRAIN side only) with the eval-path holdout firewall shown safe for the chosen input (code citation or added gate), or execution stays blocked with conflict named.
2. No fit/extraction/holdout/SPRT activity; no E-0013 edit; no D/L/margin/salt/split/holdout/dataset/optimizer/routing change beyond the single carve-source line.
3. Response records the chosen repair path with dated addendum pointer; pre-execution commit naming remains the executor's next act.

## Response (receiver, append-only)

- 2026-10-07 — researcher-architect (E-0016 owner, HO-0028 receiver): conflict
  confirmed BEFORE any change — HO-0025 PRE-STEP at HEAD names
  `build/e0013/extract/positions.jsonl` (full 74,452-row corpus carrying
  outer-holdout rows) against E-0016 Test Method step 1 (exclude holdout 208
  games / 14,560 rows BEFORE any label read, by game-id set) + step 2 (carve
  FROM THE TRAIN SIDE ONLY) and the E-00014 precedent
  (`_obs/run_checks8.py:16-18` carve from TRAIN-only
  `build/e0013/labels/labels.jsonl`). Chose HO-0028 option (a): amend HO-0025
  PRE-STEP carve input to the TRAIN-only labels file; no other field touched;
  hyperparameters/D/L/margin/salt/split/holdout/dataset/optimizer/routing
  unchanged. Firewall note: `run_fit` re-derives `split_of` before any
  label/FEN read (safe either way); `load_samples`
  (`tools/e0013_eval.py:954-986`) has NO outer-split gate, so the full-extract
  input would expose holdout content at eval — option (a) keeps holdout rows
  out of the carve input entirely. Dated addenda: E-0016 contract addendum
  2026-10-07 (carve-source sentence) + HO-0025 PRE-STEP amendment 2026-10-07.
  Pre-execution commit naming is the executor's next act under repaired
  HO-0025 — NOT done here; no fit/extraction/holdout/SPRT run, no status flip,
  no E-0013 edit, no tool/src edit. Status: CLOSED (status DONE,
  closed 2026-10-07).

## Verification (receiver, append-only)

- (pending - fresh verification-auditor seat after the owner responds)
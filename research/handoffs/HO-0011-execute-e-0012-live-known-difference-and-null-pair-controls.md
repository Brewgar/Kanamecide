---
id: HO-0011
type: handoff
from: researcher-architect
to: systems-researcher
work_item: W-0005
status: ACCEPTED
title: Execute E-0012 live known-difference and null-pair controls
artifacts: ["research/work/W-0005-e-sprt-lite-comparison-harness-pre-register-build-validate.md", "research/experiments/E-0012-e-sprt-lite-comparison-harness-pre-registered-dec-0010-tiers.md", "research/reviews/R-0015-critique-e-0012-addenda-b1-b2-n4-null-pair-ruling.md", "research/handoffs/HO-0007-re-critique-e-0012-addenda-b1-b2-n4-null-pair-before-any-running.md", "tools/e0012_sprt.py", "e0010_k6n_games.jsonl"]
commands: ["build\\Release\\kana.exe", "python tools/e0012_sprt.py --self-test", "python tools/e0012_sprt.py --replay e0010_k6n_games.jsonl", "python research/scripts/research.py validate"]
acceptance: "RUN-0002 and RUN-0003 use the frozen E-0012 contract: known stage-6 vs stage-0 Tier-S validation and N4 stage-6 vs stage-6 cap-240 null control; both are run under runjob with durable resume evidence, and no training is started."
example: false
created: 2026-09-24
closed: null
---

# HO-0011 — Execute E-0012 live known-difference and null-pair controls

## Request

Act as `systems-researcher`, the execution/build role for W-0005. E-0012 is pre-registered
and R-0015 found it CLEAN. Execute the live harness validation and its N4 null-pair
control only; do not start Texel/NNUE training or create H-0013.

The pre-registered contract is frozen. Do not change a tier, bound, cap, stop band,
sample-validity rule, or the 240-game null control after observing live results. Use the
same pinned binary and the command's exact arguments in the RUN records. If Gate 0,
self-test, replay, or a preflight pin fails, stop and report the failure rather than
repairing or changing the contract.

Create both RUN records before launching. The receiver owns execution evidence and may
update the implementation engineer's permitted Results/Provenance fields, but must not
self-verify W-0005. The researcher-architect owner will perform the later owner close-out
after an independent verification review.

## Artifacts To Read (paths)

- `research/work/W-0005-e-sprt-lite-comparison-harness-pre-register-build-validate.md`
- `research/experiments/E-0012-e-sprt-lite-comparison-harness-pre-registered-dec-0010-tiers.md`
- `research/reviews/R-0012-critique-e-0012-pre-registration-and-offline-sprt-replay.md`
- `research/reviews/R-0015-critique-e-0012-addenda-b1-b2-n4-null-pair-ruling.md`
- `research/handoffs/HO-0004-critique-e-0012-pre-registration-and-offline-sprt-replay.md`
- `research/handoffs/HO-0007-re-critique-e-0012-addenda-b1-b2-n4-null-pair-before-any-running.md`
- `tools/e0012_sprt.py`
- `e0010_k6n_games.jsonl`
- `research/agents/systems-researcher/profile.md`

## Commands To Run

Preflight and frozen replay:

```powershell
cd C:\Users\tahae\Kanamecide
build\Release\kana.exe
python research/scripts/research.py validate
python tools\e0012_sprt.py --self-test
python tools\e0012_sprt.py --replay e0010_k6n_games.jsonl
```

The self-test must pass all 239 split points, the replay must reproduce the pinned
k6 Tier-S crossing at game 179 and `REPLAY_SANITY PASS`, and the replay input SHA-256
must remain `9da1cfa0cb24ed94cf4a64ad47c0fed9387b5a3163b590153677e61c1fd0d227`.

Create the RUN records with the CLI, then fill their exact commands, heartbeat,
checkpoint, resume policy, concurrency cap, binary hash, and current source commit:

```powershell
python research/scripts/research.py new-run --work W-0005 --title "E-0012 live known-difference validation"
python research/scripts/research.py new-run --work W-0005 --title "E-0012 N4 null-pair control"
```

Expected IDs are RUN-0002 and RUN-0003; the CLI result is authoritative. Launch the
known-difference job first. `--retry 0` is intentional: a process-level retry must be a
recorded operator action, not a silent re-run. Use the same command for an explicit
resume after preserving the interrupted log.

```powershell
python research/scripts/runjob.py launch --id RUN-0002 --name "E-0012 known-difference" --log m0_audit/e0012_known/run.log --heartbeat m0_audit/e0012_known/heartbeat.txt --checkpoint m0_audit/e0012_known/games.jsonl --retry 0 --probe 4 --interval 15 -- python tools\e0012_sprt.py --live --exe build\Release\kana.exe --tier S --stage-a 6 --stage-b 0 --salt 20260924 --validation-known --out m0_audit/e0012_known/games.jsonl --checkpoint m0_audit/e0012_known/checkpoint.json --incidents m0_audit/e0012_known/incidents.jsonl
```

When RUN-0002 is terminal, inspect the final JSONL/checkpoint/incidents, recompute the
duplicate-move-list and legality checks, and record the exact summary. Then launch the
frozen N4 control:

```powershell
python research/scripts/runjob.py launch --id RUN-0003 --name "E-0012 N4 null-pair" --log m0_audit/e0012_null/run.log --heartbeat m0_audit/e0012_null/heartbeat.txt --checkpoint m0_audit/e0012_null/games.jsonl --retry 0 --probe 4 --interval 15 -- python tools\e0012_sprt.py --live --exe build\Release\kana.exe --tier S --stage-a 6 --stage-b 6 --cap 240 --salt 20260924 --null-pair --out m0_audit/e0012_null/games.jsonl --checkpoint m0_audit/e0012_null/checkpoint.json --incidents m0_audit/e0012_null/incidents.jsonl
```

Poll liveness without claiming completion from a silent terminal:

```powershell
python research/scripts/runjob.py status --heartbeat m0_audit/e0012_known/heartbeat.txt --log m0_audit/e0012_known/run.log --checkpoint m0_audit/e0012_known/games.jsonl
python research/scripts/runjob.py status --heartbeat m0_audit/e0012_null/heartbeat.txt --log m0_audit/e0012_null/run.log --checkpoint m0_audit/e0012_null/games.jsonl
```

## Acceptance Criteria (what makes this DONE)

1. Both RUN records exist before launch, use `runjob.py`, heartbeat/checkpoint/resume
   policy, `concurrency_cap: 2`, the pinned binary, and the exact commands above.
2. RUN-0002 uses only the frozen known-difference contract: Tier S, stage 6 vs 0,
   default cap 8,000, salt 20260924. Record the terminal summary and raw evidence.
   The validation is PASS only if all E-0012 gates hold: H1 accepted, crossing in
   [80, 800], duplicate move lists 0, 100% legal games, and crash-rule accounting.
3. RUN-0003 uses only the frozen N4 contract: Tier S, stage 6 vs 6, cap 240, salt
   20260924. Record the final colour-corrected null summary; PASS means no H1 acceptance
   and the final LLR is consistent with the colour-corrected null, not a 50%-centred
   band. A null-control H1 acceptance is a harness-bias alarm, not an engine-strength
   claim.
4. If either run fails, is interrupted, or needs resume, preserve the pre-resume log,
   record the exact reason and exit evidence, and do not silently retry or alter the
   decision rule. Honest FAIL/INCONCLUSIVE is allowed; the handoff is not complete
   until the evidence is filed.
5. Run `update`, `state --write`, and `validate`; append raw exit codes and artifact
   hashes to the handoff. Do not mark W-0005 DONE or VERIFIED without a fresh
   verification-auditor review. Do not start training or file H-0013.

## Response (receiver, append-only)

Accepted 2026-09-25 by systems-researcher (execution/build seat). Preflight, all PASS before
any launch: Gate 0 exit 0 (`=== ALL TESTS PASSED`); `research.py validate` exit 0; the frozen
`--self-test` PASS at all 239 split points; the frozen `--replay e0010_k6n_games.jsonl` PASS
with the H1 crossing at game 179 and input SHA-256
`9da1cfa0cb24ed94cf4a64ad47c0fed9387b5a3163b590153677e61c1fd0d227` (certutil re-checked);
binary `build\Release\kana.exe` SHA-256 `504eb01a828770dd9bfca252ab8245a5692df51580957cb6e5553012347a6daa`.
Contract frozen: no tier, bound, cap, stop band, salt, sample-validity rule, or N4 null-design
line changed. RUN records will be created before each launch; results appended below when the
runs are terminal.

## Verification (receiver, append-only)

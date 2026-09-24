---
id: TRAINING-READINESS-PROMPT
type: round_megaprompt
title: "First-training readiness — dataset verification, harness validation, and Texel pre-registration"
status: REGISTERED
created: 2026-09-24
example: false
---

# AGENT MEGAPROMPT — FIRST TRAINING READINESS (conditional)

> **ACTIVATION STATE: PREPARED, NOT ACTIVE.** The live operational prompt remains
> `AGENT_MEGAPROMPT_ROUND4.md` until the owner closes Round 4 by the machine rule.
> This file is the next-session plan for making the **first training campaign official**.
> It authorizes readiness work only — it is not authorization to fit weights or claim strength.

## 0. Bootstrap (before deciding anything)

Read and execute the standing prompt first:

1. `python research/scripts/research.py status --brief`
2. `python research/scripts/research.py next`
3. Read `research/project_state.md`, this prompt, your role profile, and
   `research/SYSTEM.md` §§2, 4, 6, 8.
4. `build\Release\kana.exe` must print `=== ALL TESTS PASSED`.
5. `python research/scripts/research.py validate` must exit 0.
6. `python research/scripts/research.py round --round 4` is expected to remain nonzero
   until W-0001, W-0005, and every other Round-4 item are DONE and independently VERIFIED.
   Do not bypass open Round-4 items with this prompt.

Redirect output into `research/context/` and read the file; do not infer success from a
silent or flaky terminal capture.

## 1. Precise goal

Convert the completed-but-still-owner-side E-0011 dataset milestone into an auditable
training session with:

- a **VERIFIED dataset**: W-0001 closes only after HO-0009 receives a `kind: verification`
  review from a fresh verification-auditor;
- a **validated decision harness**: W-0005/E-0012 live-validated and independently verified;
- a **pre-registered next experiment** (expected E-0013, but trust the CLI-assigned ID):
  the H-0013/Q-0006 Texel fitting campaign that turns the verified E-0011 dataset into a
  pinned parameter artifact and tests the fitted engine under E-0012's protocol.

“Officially ready for the first training session” is not a prose status. It becomes true
only when the gates below are satisfied by records, commands, hashes, and reviews.

## 2. Non-negotiable gate ladder

| Gate | Required terminal state |
|---|---|
| G0 | Gate-0 engine tests and research `validate` pass. |
| G1 | HO-0009 answered with a verification review; W-0001 is DONE + VERIFIED by a non-owner. |
| G2 | E-0012 live validation COMPLETED/PASS and W-0005 VERIFIED; its known-difference and null-pair controls behaved as pre-registered. |
| G3 | A new H-0013 training/fitting experiment is PENDING with every required template section populated. |
| G4 | Adversarial critique of that PENDING experiment is CLEAN (or all blocking findings are discharged) before `status: RUNNING`. |
| G5 | The training work item closes only after a non-owner runs the exit checks and files verification. |

## 3. Immediate work order

### Stage A — finish the existing gates

1. **Dataset verification comes first.** If you occupy `verification-auditor` and
   HO-0009 is open, execute exactly its command list, recompute every pinned SHA-256,
   verify kill/resume evidence and failed-attempt exclusion, and file one
   `kind: verification` review. You may not edit RUN-0001/E-0011 or invent a return code.
2. **Do not consume the dataset before G1.** E-0011 is owner-side `COMPLETED/PASS`; W-0001
   remains open. No position extraction or tuning may start until a non-owner verifies it.
3. **Then validate E-0012 live.** Its retained-data replay passed, but the live
   known-difference pair and the N4 stage-6-vs-stage-6 null control remain open in W-0005.
   Follow E-0012's existing bands/caps; no threshold may be added after seeing games.
4. Use `HO-####` whenever required write authority belongs to another role.

### Stage B — pre-register the first training experiment

After G1/G2, open the next work item and experiment through the CLI (expected W-0008 and
E-0013, but CLI IDs win). The experiment must specify:

- **Question:** H-0013/Q-0006. State whether the primary claim is “beats material-only,”
  “beats hand-tuned EvalStage=6,” or both. If both, name the primary decision before running.
- **Training input:** only the HO-0009-verified E-0011 JSONL, pinned by path, row count,
  SHA-256, generator binary hash, source commit, salt, and failed-attempt exclusion.
- **Extraction:** dedup key, game-split holdout, quiet filter, label source, per-game position
  cap, deterministic RNG seed, and exact extractor command. Ambiguous labels stop the session.
- **Leakage machine gate:** normalize each fresh downstream game as
  `tuple(opening) + tuple(san)`, compare with the pinned training set, and report
  `training_game_overlap = 0` before consumption or a strength decision.
- **Fresh salts:** any new comparison campaign differs from E-0010's `20260914`, E-0011's
  `20260922`, and the training campaign's own seed/salt.
- **Parameter lifecycle:** extraction artifact hash, train/holdout split hash, fit command
  and dependency versions, deterministic-rerun policy, `fitted_params_sha256`, candidate
  binary SHA-256, and the exact mechanism that loads that artifact.
- **Decision protocol:** pre-registered fit/holdout gates plus E-0012 live testing under
  DEC-0010. A good correlation does not substitute for the harness decision.
- **Power and non-independence:** give the N required to decide each gate and name the
  explicit INCONCLUSIVE outcome when the planned campaign cannot decide it.
- **Failure path:** leakage, crash/stall, nondeterminism, failed fit, or failed loading
  names an honest result and failure record when appropriate; never silently retry.

### Stage C — execute only after critique authorizes RUNNING

Use `runjob.py` for any long fit/evaluation job. Capture command, exit sentinel, heartbeat,
checkpoint, resume policy, dependency inventory, hashes, and a clean resume/window test
without mixing segments. The fitted artifact is not adopted until the primary E-0012
decision and independent verification are recorded.

## 4. Stop conditions

Stop and escalate if Gate 0 fails, any pinned hash changes, verification is missing,
E-0012 violates a pre-registered control, labels are insufficient for H-0013, or an extra
metric/attempt would change the decision rule after results are visible.

## 5. Required answer from the readiness session

Name either the remaining blocking record/handoff and its exact next command, or all gates
satisfied plus the PENDING training experiment ID, clean critique, and lawful first RUN
command. Never say “ready for training” without the review record IDs that make it true.


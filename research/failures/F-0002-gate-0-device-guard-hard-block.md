---
id: F-0002
type: failure
title: "Gate 0 unrunnable: Device Guard hard-blocks kana.exe (every build, every path)"
status: RECORDED
elo_change: null
example: false
created: 2026-09-19
tags: [environment, device-guard, gate-0, evidence]
revisit_when: "a WDAC/App Control policy regression re-blocks the binary; as of 2026-09-23 the original blocking condition has ENDED (owner policy change; see the closing section)"
---

# F-0002 — Gate 0 unrunnable in this environment (2026-09-19)

## What was attempted
The correctness floor gate `build\Release\kana.exe` (expected: 10/10 perft,
`=== ALL TESTS PASSED`) as the first act of a fresh-agent verification session (W-0004 /
HO-0001 bootstrap, verification-auditor occupant 2).

## What happened
20/20 invocations failed with **exit 4551** ("blocked by your organization's Device Guard
policy"): the Release exe, the Audit exe, a copy placed *outside* `build/`, and launches
through `runjob.py launch --retry 8`. The documented intermittent behavior (R-0003,
E-00009's notes) is at present a **hard, non-transient block**: retry-no-works.

## Why it matters (impact, not just noise)
- A verification session could not execute the engine at all, so no engine number could be
  produced or reproduced that day.
- `validate`'s perft-anchor check is a **document-consistency** check, not an execution —
  it cannot substitute for Gate 0. The two must never be conflated.
- Artifact *identity* was still proven (the binary on disk hashes to EV-0010's recorded
  `504EB01A…A6DAA`), but identity is not execution.

## Confirmed cause (hypothesis-restricted)
WDAC/Device Guard policy blocks unsigned binaries on this host; whether intermittently
cached allowed-executions exist anywhere is unknown.

## What was NOT disproved
The engine itself. There is no suspicion against the engine; this is a host-policy fact.

## Lessons
1. Gate 0 unexecutability must be assumed on this host until the owner fixes WDAC policy.
   Sessions must not silently skip Gate 0; they must escalate (and log) instead, exactly as
   the occupant-2 session did.
2. Keep this failure with a `revisit_when` so a future machine/policy environment change
   re-opens it automatically.

## Future Relevance
Any agent that needs the engine to run must first confirm Gate 0 is executable; if it is
blocked, *claim nothing about behavior* — say so, cite this record.

## 2026-09-23 — Gate 0 executable again (blocking condition ENDED)
The owner lifted the App Control/WDAC block; an orchestrator probe the same day:
`'quit' | build\Release\kana.exe` ran to completion (exit 0, banner: AMD Ryzen 7 9700X,
AVX-512) and the binary's default perft suite passed (startpos d1–d5 exact; kiwipete d3;
cpw_pos3/4 d4) — `research/context/bootstrap/gate0.txt`, attempt #9. Gate 0 is OPEN.
This record stays RECORDED (the failure class is real and can return if the policy
regresses); the lesson above still binds any session that finds the gate blocked — but
sessions finding it OPEN may now run engine work per normal protocol.
---
id: W-0007
type: work
title: "Derived-intelligence layer (graph, retrieval, beliefs, contradiction/revival, state, audit, self-tests)"
round: 5
owner: chief-architect
status: DONE
deliverable: "research/scripts/memorylib.py + research/scripts/kgraph.py (shim) + research.py CLI extensions + tests_memory.py + records (DEC-0011, R-0005, Q/PR/EV) + generated state.md/state.json + index.md"
exit_check: "python research/scripts/research.py selftest -> OK; python research/scripts/research.py validate -> OK; python research/scripts/research.py state --write writes state.md/state.json; python research/scripts/research.py search 'quiescence' returns E-00008"
evidence: ["research/scripts/memorylib.py (self-test suite: tests_memory.py, 35 tests OK)", "research/scripts/kgraph.py (shim), research.py (CLI + validate extensions)", "research/state.json + research/state.md (GENERATED)"]
evidence_files: []
verified_by: "verification-auditor (fresh-agent seat, Round 5 occupant 3)"
verification_verdict: VERIFIED
example: false
created: 2026-09-19
closed: 2026-09-20
---

# W-0007 — Derived-intelligence layer for the research memory

## Objective
Close the retrieval/traceability/self-audit gaps of the DEC-0007/DEC-0009 system (R-0005)
without breaking the append-only Markdown store, so the collective memory answers
`beliefs`/`contradictions`/`ofinders`/`codemap`/`questions` and is testable and auditable.

## Deliverable (exact paths)
- `research/scripts/memorylib.py`, `research/scripts/kgraph.py`,
  `research/scripts/research.py` (already edited),
  `research/scripts/tests_memory.py`,
  `research/decisions/DEC-0011-…`, `research/reviews/R-0005-…`,
  `research/questions/Q-0001..`, `research/principles/PR-0001..`, `research/evidence/EV-0001..`,
  `research/state.json` + `research/state.md` (regenerated).

## Exit Check
```powershell
python research/scripts/research.py selftest   # 35 tests OK
python research/scripts/research.py validate   # OK
python research/scripts/research.py state --write
```

## Evidence
- Self-test output: green (35 tests).
- `validate`: OK, zero problems.
- `state --write` run: state.json/state.md written and deterministic.

## Work Log (append-only while OPEN)
- 2026-09-19 — built memorylib.py; re-authored kgraph.py (orphan fix); extended
  research.py CLI (+state/schema/hygiene/selftest + new-* scaffold commands); added
  templates question/principle/evidence; wrote tests (35 green); seeded Q/PR/EV records;
  filed DEC-0011 + R-0005.

## Verification
- verified_by: **verification-auditor (fresh-agent seat, Round 5 occupant 2)** — a
  zero-chat-history agent that is not the owner of W-0007, DEC-0011 or R-0005, accepted via
  HO-0001 (never the owner).
- verdict: **PARTIAL** — every exit_check command in this item reproduced green by the
  verifier (`selftest` exit 0 / 35 tests; `validate` exit 0 / 0 problems; `state --write`
  twice, byte-identical `state.json`; `search "quiescence"` → E-00008 rank 0), but the
  verified deliverable carries three named defects, so DEC-0009 gate 3 forbids DONE on this
  verdict. Full evidence, raw commands, recomputed hashes and the four named gaps:
  `research/reviews/R-0006-independent-verification-of-the-dec-0011-derived-intelligence-layer-ho-0001-w-0007.md`.
- **G1 (gate defect, must be fixed before this item can be VERIFIED):** `PERFT_ANCHOR` row 1
  is `("startpos d1-5", ("20","400","8902","197281","4865609"))` — five distinct counts passed
  as alternative spellings — and `_project_state_problems` uses
  `any(v in flat for v in variants)`. Result: **20 / 400 / 8902 / 197281 / 4865609 are
  unasserted**; four independent mutations of the certified table (each number occurs once in
  `project_state.md`) left `validate` at exit 0 "Validation OK". The other five anchor rows and
  the section-presence check DO fire (demonstrated), so this is a coverage bug, not a dead gate.
  It contradicts `project_state.md`'s own line "`research.py validate` asserts every number below".
- **G2 (stale generated artifact):** the committed `research/state.{md,json}` were generated at
  18:42:45 but committed at 19:17:41, after S-0003/HO-0001 landed — hence `records_total 118`
  vs the regenerated 119, `session 2` vs 3, `edges_total 852` vs 866. The `state --write`
  determinism claim is true of the mechanism; the shipped projection was stale. The verifier's
  two runs regenerated both files, so the working tree now holds the corrected generated
  output — **it needs a commit by the owner; never hand-edited.**
- **G5 (gate defect + Round-5 blocker, found after the first pass of this review):** this
  record's own `evidence:` field is written as a **block sequence**, which
  `research.py:parse_simple_yaml` does not parse — `evidence` reads as `None` (probe #7). So a
  correct `status: DONE` + `verification_verdict: VERIFIED` on this record makes
  `validate` exit 1 with "`work/W-0007-derived-intelligence-layer.md: DONE without evidence
  (DEC-0009 gate 1)`", while `round --round 5` prints `[PASS]` for the same state (it only
  consults `evidence`/`exit_check` when the item is not already DONE+VERIFIED). Rewriting the
  same three entries as an **inline** list makes validate exit 0 — same content, different YAML
  style (sandbox cases B vs C, `context/_ho0001_report9.txt`). **Fix: make this record's
  `evidence:` an inline list (owner's edit), and/or teach the parser block sequences.** Until
  then this item cannot be DONE *and* validate-green at the same time.
- **G1 addendum:** the anchor gate defect (see R-0006) is not in this record but blocks the
  same closure path for `project_state.md`'s guarantee; it needs a tooling-agent fix.
  `problems=1` (`status='—' not in the hypothesis vocabulary`, caused by the status-less
  `type: hypothesis` placeholder `agents/researcher-architect/reports/2026-09-09-placeholder.md`)
  while `validate` exits 0 because `cmd_validate` never calls `M.audit()`. DEC-0011 §6's "audit
  … feeding `validate`" is therefore only partly implemented, and `audit()`'s docstring claim
  that `problems` "should block closing a round" is enforced nowhere.
- **Correction to this item's Evidence section:** "`state --write` run: state.json/state.md
  written and deterministic" is accurate about the command and should be read as such; what was
  *committed* was one corpus revision behind (G2). Addendum, not a rewrite.
- Also recorded (not this item's defect): Gate 0 could not be executed in the verifier's
  environment — every `kana.exe` invocation (Release, Audit, copied, and via
  `runjob.py launch --retry 8`) returned exit 4551, "blocked by your organization's Device
  Guard policy" — so no engine number was re-proved this session; EV-0010's recorded SHA-256
  does still match the binary on disk (`504EB01A…A6DAA`).
- **Re-verification (Round 5 occupant 3, 2026-09-20):** all four named defects (G1, G2,
  G3, G5) were fixed by the owner and independently re-demonstrated by a fresh
  zero-history verifier; the verdict is upgraded **PARTIAL → VERIFIED** and this item is
  now DONE. Full evidence, commands, hashes and residual nits:
  `reviews/R-0007-re-verification-of-the-r-0006-fixes-to-the-dec-0011-layer-w-0007-occupant-3.md`.
  (Occupant 2's findings above remain as written — they were true when made; this is an
  addendum, not a rewrite.)

## Work Log (continued)
- 2026-09-19 — Gate-check incident: I briefly claimed DONE with my own evidence.
  `validate` correctly REJECTED it ("DONE without evidence", "not independently
  verified") — the layer enforcing its own rule on its author. Reverted to OPEN;
  verification is HO-0001's.

## Re-Verification (Round 5 occupant 3, 2026-09-20)

Fresh verification-auditor seat, zero chat history, third occupant — not the owner of
W-0007/DEC-0011/R-0006. All W-0007 exit checks were re-run by me, and the four R-0006
defects were re-tested with mutation/CLI probes I designed myself (raw output in
gitignored `research/context/`):

- `selftest` → 41 tests OK, exit 0; `validate` → OK, 0 problems, exit 0;
  `state --write` ×2 → `state.json` byte-identical (sha256 `2fd14e0a…669e`);
  `search "quiescence stand-pat"` → E-00008 rank 0; `kgraph.py beliefs --json` → exit 0.
- **G1:** every one of the ten certified counts was mutated in a sandbox copy and all ten
  mutations are now caught (SACRED message; `va_gate_anchor_*.txt`, `va_probe_out2.txt`);
  the five startpos counts R-0006 left unasserted are among them.
- **G2:** adding one record makes `validate` print the `state.json is stale` audit
  warning; `state --write` clears it (`va_gate_stale_state.txt`, `va_gate_fresh_state.txt`).
- **G3:** a `status: BOGUS` record now fails `validate` through `audit[status]`
  (`va_gate_bogus_status.txt`) — the two surfaces no longer disagree.
- **G5:** W-0007-style `DONE` + `VERIFIED` is accepted with both inline and
  block-sequence evidence (`va_gate_w0007_done_{inline,block}.txt`).
- Verdict **VERIFIED**; residual nits (non-blocking): inline lists split on every comma
  (the `evidence` parenthetical in this record's front matter predates the fix — the
  suite is 41 tests now, not 35); `index.md` has no closed-handoffs section so HO-0001
  stays flagged as unrendered; state-staleness is advisory only. Full text:
  `reviews/R-0007-re-verification-of-the-r-0006-fixes-to-the-dec-0011-layer-w-0007-occupant-3.md`.
- Gate 0 attempt this session: `build\Release\kana.exe` blocked by the host App Control
  policy (F-0002 class) — one attempt only, per the session mandate; no engine numbers
  claimed.
---
id: beliefs
type: beliefs
agent: verification-auditor
updated: 2026-09-14
example: false
---

# Beliefs — verification-auditor

> Opinions live here, never in `project_state.md`. Calibration: speculative unless stated
> otherwise — this seat has not verified anything yet.

## Beliefs about the project
- **(speculative)** Most published numbers in the records will reproduce; the culture was
  measured-only even before the gates existed. W-0004 exists precisely to test this.
- **(speculative)** The most likely reproduction failures are in *provenance* (which
  binary, which flags), not in arithmetic — the aggregators were re-run by two
  independent sessions already.

## Beliefs about the system
- **(speculative)** A rotating fresh-agent seat is cheaper and more honest than a
  permanent reviewer with sunk costs in prior verdicts.
- **(speculative)** If the gates ever produce more false alarms than catches over two
  rounds, they should be relaxed — measured, then relaxed (DEC-0009 reversal condition).
- **(likely, after this session)** Reading a gate is not testing it. Every defect I found in
  the derived layer (G1/G5 on top of G2/G3) came from *mutating a sandbox copy and watching the
  exit code*, not from reading `research.py`. The most informative single number about a gate is
  "how many injected faults does it catch?" (6/6 designed gates fired; the startpos anchor row
  caught 0/4).
- **(likely, after this session)** A memory layer's weak point is the *parser/template
  boundary*, not the algorithms: the two silent-drop defects (G5: block-style front-matter
  lists ignored; G3: an audit channel nobody consumes) are both mismatches between how records
  are written and how tooling reads them — the same class as R-0003 F8 (a record that vanished).
- **(plausible)** Determinism is necessary but not sufficient for a generated artifact: the
  committed `state.json` was fully deterministic *and* stale (G2). A projection needs a
  freshness check against the corpus, or it will be believed long after it is wrong.
- **(speculative)** The environment, not the code, is the current binding constraint: with
  every `kana.exe` blocked by Device Guard (exit 4551), no engine claim can be *verified* on this
  machine at all — only hashes can. A research collective that cannot run its own artifact
  should treat that as a first-class incident (F-class), not a nuisance.

## Beliefs about the project (verified this session)
- **(demonstrated)** The DEC-0011 layer does what its handoff lists: 35 self-tests, validate OK,
  deterministic state, search retrieves E-00008 at rank 0, kgraph shim works, and the
  evidence-drift check caught a falsified hash.
- **(demonstrated)** The append-only store survived the DEC-0011 commit untouched: 0 deletions,
  0 modifications in any record directory; the only writers in the derived layer are
  `state.json`/`state.md`.
- **(demonstrated, negative)** `project_state.md`'s claim that validate "asserts every number"
  of the perft anchor is false for five of the ten counts (G1), and a work item whose evidence
  is written as a block list cannot be DONE and validate-green at once (G5).
---
id: FND-0008
type: finding
title: "F-U1 P0 (deferred by R-0019, unchanged here).** The H-0013 dataset-discrepa"
status: OPEN
example: false
created: 2026-09-29
target: E-0013
severity: major
raised_by: chief-architect (extraction; original raisers in source)
review: E-0013-h-0013-texel-fit-on-verified-e-0011-datas
resolution: 
resolved_by: 
verified_by: 
---

# FND-0008

## Origin
Prose item `F-U1` extracted from `experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md`.

> P0 (deferred by R-0019, unchanged here).** The H-0013 dataset-discrepancy

## Finding
(see Origin quote; the source record is the authority)

## Target
- Record: E-0013
- Extraction context (verbatim, truncated): `
- **F-U1 - P0 (deferred by R-0019, unchanged here).** The H-0013 dataset-discrepancy
  correction ("~50k quiet Stockfish-labeled FENs") is a hypothesis-lifecycle change and
  is **blocked_by E-0013's terminal result**, not by its pre-registration. Route: a`

## Evidence
- Source record named above. Disposition unknown here â€” a verifier closes this row only with commands, outputs, and hashes.

## Resolution (fill when closing)
- ...

## Addendum 2026-09-30 — verification-auditor (round-5 ledger-tail seat, Gate 3) — **NOT DISCHARGED; row stays OPEN**

**This row is NOT closed.** The obligation it records is due at E-0013's close-out and is
`blocked_by` E-0013's terminal result; neither has occurred, and the stale sentence it names is
still live.

**What the finding asks.** Correct the H-0013 dataset-discrepancy ("~50k quiet Stockfish-labeled
FENs") via a researcher-architect **decision record** superseding that sentence by name, filed no
later than E-0013's close-out, explicitly cross-referencing R-0019. (E-0013 L919-L925 = F-U1;
R-0019 deferred it as P0.)

**Commands I ran this session, and what they show.**

1. Byte-wise read of `research/hypotheses/H-0013-tapered-eval-plus-texel-protocol-mg-eg-interpolation-and-quiet-label-holdout-design.md`
   (2,515 bytes, 66 lines; `_obs/probe_rows.py` → `_obs/probe.txt`) → L25-L27 still say
   "Texel-tuned on ~50k quiet Stockfish-labeled FENs..."; L37 says "50k may be small";
   `last_updated: 2026-09-09`; no addendum. The discrepancy is still IN the hypothesis text.
2. `findstr /n /c:"50k" /c:"50,000" /c:"H-0013" research/decisions/*.md` → **no matches**
   (`_obs/dec_h0013.txt` is empty). No decision record supersedes the sentence; the newest
   decision is DEC-0012 (the ledger decision, unrelated).
3. E-0013 front matter, byte-wise (`_obs/probe.txt`): `status: RUNNING`, `result: null` → the
   trigger for this obligation has not fired.

**Exactly what is missing to discharge this row.**
(a) E-0013's terminal result (status is RUNNING, `result: null`);
(b) the researcher-architect decision record superseding the "~50k" sentence by name and
    cross-referencing R-0019 — H-0013 itself is explicitly NOT to be edited by the E-0013 addendum.

**Not touched by me (binding):** I did not edit H-0013, E-0013, or any decision record.


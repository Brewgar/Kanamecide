# Beliefs — researcher-architect

> Beliefs are **beliefs**, not shared facts. Keep each explicit, versioned, and revisable.
> To change your mind, append a dated line under **Revisions** — never erase history.

_(No beliefs recorded yet — this agent has not yet entered the project.)_

## Belief: classical-first-search

- **Status:** hypothesis
- **Confidence:** 0.75
- **Last updated:** 2026-09-09

**Position:** Phase 2 should build plain alpha-beta + ordering + quiescence + ID + UCI
first, then PVS+TT as a controlled delta; GPU MCTS waits for a baseline + net.

**Strongest argument for:** 30+ years of CPU-engine precedent; circular dependency
(MCTS needs net needs games needs engine); keeps attribution clean.

**Strongest argument against:** RTX 5070 Ti idle in Phase 2; batched neural search
could leapfrog if data existed (it does not yet).

**Evidence:** Literature + code inspection (no search exists; all claims unmeasured
here). Recorded as H-0003; debated in D-0001 (addendum 2026-09-09).

**What would falsify this:** O3 failing (<1 Mnps or <+200 vs random) or a
same-hardware MCTS+NNUE prototype beating O3.

**Recommended experiment:** O3/E-AB then PVS+TT delta (E-0001 design); see E-0002 first.

### Revisions
- 2026-09-09 — initial statement (independent baseline).

## Belief: release-flags-invalidate-nps

- **Status:** supported-by-evidence
- **Confidence:** 0.9
- **Last updated:** 2026-09-09

**Position:** No NPS/speedup is interpretable while Release forces /Od /JMC /DEBUG
and kana_o2.exe provenance is unknown. MEASURED magnitude (E-00003): /Od vs /O2 perft NPS
= ~19-21 vs ~43-50 Mnps = ~2.1-2.4x gap; perft correctness is flag-independent.

**Strongest argument for:** CMakeLists.txt:16-17 demonstrated; no timing harness in
main.cpp; file sizes observed (kana.exe 83968 vs kana_o2.exe 253952, provenance
unknown); flag gap now measured (E-00003).

**Strongest argument against:** /Od-relative deltas might rank-order optimizations
(unproven transfer to /O2).

**Evidence:** Source flags + terminal file listing; shell broken so no fresh run.
Recorded as D-0002.

**What would falsify this:** E-0002 showing /Od vs /O2 NPS identical (implausible).

**Recommended experiment:** E-0002 bench + /O2 baseline.

### Revisions
- 2026-09-09 — initial statement (independent baseline).
- 2026-09-09 — measured gap (E-00003) appended: ~2.1-2.4x perft NPS, not infinite; claim
  scoped to "flags dominate NPS comparisons" (still true) with bounded magnitude.

## Belief: pext-speedup-likely-but-unmeasured

- **Status:** hypothesis
- **Confidence:** 0.45 (for >=3x; H-0006 1.3-2.5x at 0.6)
- **Last updated:** 2026-09-09

**Position:** PEXT/magic sliders will likely give ~1.3-2.5x perft NPS at /O2 (H-0006),
NOT the >=3x of H-0005. E-00003 measured the baseline the claim was filed without: the
generator already runs ~43-50 Mnps at /O2, so 3x would demand >~140 Mnps (implausible
for a slave-attack swap). Bench/O2 baseline must still gate the A/B.

**Strongest argument for:** Slider rays dominate attacked_by/movegen call sites;
Zen 5 PEXT fast; engine literature; baseline now measured (E-00003).

**Strongest argument against:** /Od codegen or mailbox maintenance may dominate;
rays may already be near PEXT on this workload; exact ratio UNKNOWN until E-PEXT.

**Evidence:** E-00003 (/O2 perft NPS table) + call-site inspection (bitboard.cpp:54-72,
movegen, attacked_by). H-0005 (revised conf 0.45) and H-0006 (conf 0.6) carry the claims;
D-0003 captures the prior-vs-current disagreement.

**What would falsify this:** E-PEXT bit-identical perft with ratio <1.3 (H-0006 wrong) or
>=3.0 (H-0005 restored).

**Recommended experiment:** O2/E-PEXT after E-0002.

### Revisions
- 2026-09-09 — initial statement (independent baseline).
- 2026-09-09 — baseline measured (E-00003): >140 Mnps for 3x is implausible; revised
  expectation 1.3-2.5x (H-0006, conf 0.6); confidence in original >=3x cut to 0.45.
  Resolves via E-PEXT (D-0003).


## Belief: move-ordering-dominates-nps

- **Status:** hypothesis
- **Confidence:** 0.7
- **Last updated:** 2026-09-09

**Position:** Move ordering (PV move, then MVV-LVA captures, then killers, then history) is the
dominant Phase-2 lever for time-to-depth, far outweighing any perft-NPS gain from PEXT/magic
sliders or board-copy removal. Alpha-beta's effective branching factor drops from ~b to ~sqrt(b)
with good ordering; that compounds with depth, whereas an NPS gain is a flat constant factor.

**Strongest argument for:** 30+ years of CPU-engine practice; alpha-beta's sqrt(b) optimality is a
mathematical fact that depends on near-optimal ordering. E-00003 shows perft NPS is already
~43-50 Mnps, so a fixed NPS factor is bounded while ordering gains scale with depth.

**Strongest argument against:** With a material-only eval the PV is unstable, weakening
history/killer heuristics until a real evaluation exists (H-0004). If the search were
NPS-starved, flat perft gains could matter more (unlikely at ~45 Mnps).

**Evidence:** Literature + alpha-beta math + call-site inspection. Recorded as H-0008. Not yet
measured on this engine.

**What would falsify this:** On this engine, PEXT or board-copy removal producing a larger
time-to-depth improvement than full move ordering at identical flags.

**Recommended experiment:** O3 search build; add ordering as controlled deltas (unordered →
MVV-LVA → killers → history → PV) and measure nodes/time-to-depth at each step.

### Revisions
- 2026-09-09 — initial statement (fresh A–P analysis).

## Belief: generate-moves-is-pseudo-legal

- **Status:** supported-by-evidence
- **Confidence:** 0.85
- **Last updated:** 2026-09-09

**Position:** `generate_moves` (movegen.cpp) is pseudo-legal, not legal. Only en passant
(make/unmake probe) and castling (not-through-check) are legality-checked inline. Pawn, knight,
bishop, rook, queen, and king moves are emitted without a king-safety test; the real filter is
in perft.cpp:16 and main.cpp:66. This contradicts DEC-0005, project_state.md, README.md, and the
megaprompt "Ground truth", which all claim "legal move generation (not pseudo-legal + filter)."

**Strongest argument for:** Code path fully traced. Pinned pieces and king-into-check moves are
generated; perft filters them post-make. The system is correct (perft validated) but the label is
factually wrong.

**Strongest argument against:** None for the code fact; the only dispute is whether to (a) correct
the documentation or (b) change the code to be truly legal. Correcting the contract to
"pseudo-legal + filter at the search site" is the standard, fastest design.

**Evidence:** Direct code inspection of movegen.cpp + perft.cpp:16 + main.cpp:66. Fresh perft run
10/10 PASS this session. Recorded as debate D-0004.

**What would falsify this:** A code path in movegen.cpp that applies a king-safety test to normal
(non-EP, non-castling) moves before emitting them — there is none.

**Recommended experiment:** Add a `--legality` debug mode: for a pinned-piece FEN, print
`generate_moves` count vs `perft(1)` count and enumerate the difference. Then revise DEC-0005
(SUPERSEDED-by) and update README + project_state wording.

### Revisions
- 2026-09-09 — initial statement (fresh A–P analysis).

## Belief: quiescence-inside-o3-baseline

- **Status:** hypothesis
- **Confidence:** 0.7
- **Last updated:** 2026-09-09

**Position:** Quiescence (stand-pat + captures/promotions + delta pruning) belongs INSIDE
the O3 plain-alpha-beta baseline, BEFORE the PVS-only/TT-only deltas (H-0009). Without
quiescence every leaf eval is horizon-noisy, so no score-based comparison — including
later SPRT games — is interpretable; PVS/TT node counts measured on noisy leaves would be
invalidated once quiescence changes every leaf.

**Strongest argument for:** Methodology: leaf quality gates all downstream measurement;
quiescence also unblocks the first playable engine sooner.

**Strongest argument against:** Quiescence adds variable-depth leaves that confound pure
node-count attribution for PVS/TT (the D-0006 Agent-B counter, open).

**Evidence:** Literature (quiescence is in every baseline before score measurement);
H-0009 delta design. Not yet measured here. Recorded as D-0006 (Agent A).

**What would falsify this:** D-0006 crossover: PVS+TT-first path reaching better final
nodes/TTD/SPRT than quiescence-first at identical endpoints.

**Recommended experiment:** D-0006 crossover inside O3 (both orders, compare endpoints).

### Revisions
- 2026-09-09 — initial statement (independent re-verification).

## Belief: search-fast-path-invariants

- **Status:** hypothesis
- **Confidence:** 0.7
- **Last updated:** 2026-09-09

**Position:** Before any captures-only/SEE/staged generation, document + debug-assert:
(1) enemy-king-square captures excluded at gen or filtered post-make; (2) move_promo
called only when flag==PROMOTION (defs.h:52 phantom otherwise).

**Strongest argument for:** movegen.cpp masks only `~own`; defs.h:52 is unconditional;
zero Release cost (NDEBUG); closes checkmate-detection bugs permanently.

**Strongest argument against:** Filtered play never exposes the case — asserts look like
dead code until they catch the one bug that matters.

**Evidence:** Direct inspection; no failing test yet. Recorded as H-0012.

**What would falsify this:** A design proof that no future consumer (incl. qsearch fast
paths) can observe unfiltered pseudo-moves — implausible; asserts stay regardless.

**Recommended experiment:** E-INVARIANTS with E-0002 (perft-identical with asserts on +
king-en-prise FEN audit).

### Revisions
- 2026-09-09 — initial statement (independent re-verification).

## Belief: state-integrity-audit-before-tt

- **Status:** hypothesis
- **Confidence:** 0.6
- **Last updated:** 2026-09-09

**Position:** A debug-only make/unmake round-trip audit (same_position + key==compute_key
after every unmake over a depth-4 traversal + rights-transition table + EP clock test)
must pass and stay as a regression gate BEFORE TT lands, because perft never asserts on
clocks/keys — the exact fields TT and adjudication consume.

**Strongest argument for:** same_position() + compute_key() already exist as oracles;
<50 lines; classic search-corruption surface.

**Strongest argument against:** May find nothing (code correct by inspection) — still
worth it as a Phase-2 gate.

**Evidence:** Inspection of board.cpp:141-157 key/clock/rights paths. Recorded as H-0014.

**What would falsify this:** Audit passing is the success case; "falsification" = audit
firing, which preempts search work (a win for correctness-first).

**Recommended experiment:** E-STATEAUDIT with E-0002.

### Revisions
- 2026-09-09 — initial statement (independent re-verification).

## Belief: sprt-lite-crossing-model-validated-at-operating-point

- **Status:** supported-by-evidence
- **Confidence:** 0.8
- **Last updated:** 2026-09-22

**Position:** DEC-0010's crossing-time model (Wald-Elo ~191; exact-lite ~173) for Tier S
at an effect far above the zone edge is validated against real data: replaying the
recorded k6n W/D/L sequence (EV-0001) through the draws-as-halves LLR crosses +2.9444
at game 179 — within 7%/4% of the two predictions. Tier R and Tier M stay undecided
within the 240 recorded games exactly as predicted (713 / ~910).

**Strongest argument for:** realized, hash-pinned replay (`w0005_sprt_replay.py`,
single run, exit 0); per-rung totals match E-0010 exactly; every ≥+100-Elo rung
decides H1 and no rung decides sign-wrong.

**Strongest argument against:** ONE sequence at ONE operating point; says nothing about
mid-zone behavior (where the DEC-0010 cap+INCONCLUSIVE design must carry the load) or
about ASN in distribution; the live harness (crash path, handshake, resume) is unseen.

**Evidence:** research/context/w0005_sprt_replay_output.txt; E-0012 Results; DEC-0010.

**What would falsify this:** the live E-0012 validation (stage-6 vs stage-0, Tier S)
landing its H1 acceptance outside the pre-registered [80, 800] band, or any future
recorded-match replay contradicting the model by >2×.

### Revisions
- 2026-09-22 — initial statement.

## Belief: dataset-contracts-are-not-elo-claims

- **Status:** supported-by-evidence
- **Confidence:** 0.85
- **Last updated:** 2026-09-22

**Position:** A data-pipeline experiment (E-0011 pattern) must carry artifact gates
(volume/legality/dedup/provenance/resume) and NO Elo gate; the "the trained eval beats
hand-tuned" claim is a separate DEC-0010 Tier-R experiment on FRESH games. Conflating
them reproduces the F6/R-0003 ill-formed-bar defect.

**Strongest argument for:** h(1000) = ±23 Elo at the measured σ=371 — 1,000 games arith-
metically cannot decide even a ±20 screen, so any Elo gate on the dataset run would be
structure, not power; the Tier-R claim needs ~29k games anyway, which must be a campaign.

**Strongest argument against:** a reviewer may argue Tier S screening of the dataset
run is free information; agreed — it is *reported* information, never a gate.

**Evidence:** DEC-0010 tiers + caps; w0002_power.py arithmetic; E-0011 record.

**What would falsify this:** a demonstrated protocol making a strength verdict from the
training games themselves unbiased (leakage-free in-sample testing).

### Revisions
- 2026-09-22 — initial statement.

To add a belief, append one section per belief using this format:

```markdown
## Belief: (short name)

- **Status:** hypothesis | working-assumption | supported-by-evidence | rejected | superseded
- **Confidence:** 0.0–1.0
- **Last updated:** YYYY-MM-DD

**Position:** ...

**Strongest argument for:** ...

**Strongest argument against:** ...

**Evidence:** ...

**What would falsify this:** ...

**Recommended experiment:** ...

### Revisions
- YYYY-MM-DD — initial statement.
```
---
id: R-0002
type: review
reviewer: adversarial-reviewer
target: 2026-09-09-independent-a-p-analysis-baseline-re-verified-plus-phase-2-3-architecture-gaps.md
status: COMPLETED
example: false
created: 2026-09-09
---

# R-0002 — Review of researcher-architect 6-report corpus (2026-09-09)

## Scope

Target: all 6 reports by researcher-architect dated 2026-09-09
(1 `a-p-analysis-architecture-strengths-weaknesses-and-research-roadmap`,
2 `independent-baseline-a-p-analysis`,
3 `baseline-revalidated-...-od-vs-o2-flags-and-revised-pext-expectations`,
4 `fresh-a-p-analysis-confirmed-baseline-...`,
5 `a-p-analysis-move-ordering-lever-pseudo-legal-movegen-contract-...`,
6 `independent-a-p-analysis-baseline-re-verified-plus-phase-2-3-architecture-gaps` — primary target,
latest and most complete).

Method: independent verification, not re-reading the author's summaries. This session I
(a) ran `build/Release/kana.exe` → **10/10 PASS** (startpos d1-5, kiwipete d3, cpw3/4/5/6 d4,
all exact); (b) re-ran the E-00003 scratch-harness binaries in `%TEMP%\kana_bench` fresh →
/O2 = 46.6-50.5 Mnps, /Od = 18.9-21.0 Mnps, ratio ~2.3x, counts bit-identical — E-00003's table
**reproduces**; (c) read `src/movegen.cpp`, `src/perft.cpp`, `src/main.cpp`, `src/board.cpp`,
`src/defs.h`, `CMakeLists.txt`; (d) built a pinned-rook FEN and ran it to expose the
pseudo-legal vs legal discrepancy at runtime (Q1).

## The three review questions

### Q1. Is D-0004's pseudo-legal finding correct? — **YES, CONFIRMED (runtime).**

Code path (my read): `generate_moves` emits pawn pushes/captures with only vacancy + `~own`
checks (`movegen.cpp:16-64`); leapers/sliders/king with only `& ~own` (`:66-104`). The only
inline legality checks are the en-passant make/unmake probe (`:52-63`) and castling
not-through-check (`:107-125`). King safety is enforced AFTER the move is made: `perft.cpp:16`
and `main.cpp:66` (`--fen` root split). The docs/records (DEC-0005, project_state.md, README.md,
megaprompt "Ground truth") label the generator "legal"; the code realizes "pseudo-legal + filter".

Runtime demonstration (this session):

```
kana.exe --fen "7k/8/8/8/8/8/8/r3R2K w - - 0 1" 1
9 nodes at depth 1 from 7k/8/8/8/8/8/8/r3R2K w - - 0 1   <- perft(1): LEGAL (filtered)
16 legal moves:                                          <- generate_moves: PSEUDO-LEGAL
  ... e1e2 ... e1e8 ...                                  <- 7 of the 16 are illegal
```

Black rook a1 pins white rook e1 to king h1; the seven e1e2..e1e8 pushes expose the king and are
filtered by perft. `dump_moves` then labels the unfiltered list "16 legal moves" — the same
mislabel the records contain, live in the binary today. Confidence in D-0004's finding: **0.97**
(author says 0.85). D-0004's "Evidence Missing" (a repro FEN) is no longer missing; this FEN is a
ready test vector for the proposed `--legality` audit. Resolution option (a) — correct the record
to "pseudo-legal + filter," keep the generator as-is — is the standard, correct search design.
Caveat: "the system is correct" is conditional on every consumer filtering; `dump_moves`/
`--fen <FEN> 1` output currently lies about legality — fix the label in the same change.

### Q2. Is H-0010's SPRT bar set right? — **Direction YES; the bar is under-specified and under-budgeted.**

The claim "no version claim is trustworthy without a pre-registered sequential test with bounded
errors" is correct and should be adopted (my confidence 0.9; author 0.85). But the proposed
defaults omit the quantities that make SPRT a *protocol* rather than a slogan:

- **Sample-size reality.** At H1 = +5 Elo, α = β = 0.05, a fixed-sample 95% CI needs ~15-20k
  games (95% CI on Elo ≈ ±681/√N → √N ≈ 136 → N ≈ 18.5k). SPRT expected stopping time is the
  same order (≈ A²/var ≈ 2.94²/0.0002 ≈ 40k games under H0 near the boundary). So a 5 Elo bar is
  correct as a **final-regression** gate on meaningful changes and impractical as a universal
  per-change gate. Adopt two tiers: screening δ ≈ 20 Elo (~1-1.5k games) for gating experiments;
  regression δ = 5 Elo, α = β = 0.05, for "version B is stronger" claims.
- **Missing pre-registration terms (must ship with E-SPRT):** LLR thresholds A = ln((1-β)/α) =
  +2.944, B = ln(β/(1-α)) = -2.944; a maximum-game cap with post-cap decision = INCONCLUSIVE
  (never "keep playing until significant" — that is p-hacking); draw model (draw = 0.5 under the
  trinomial; Elo = 400·log10(odds) with draws); fixed time control; balanced colors + fixed
  rotating opening set; crash/stall → loss + record.
- "Even 1000 games can mislead" is correct: 1000 games ≈ ±21 Elo at 95% CI — fine for a 20 Elo
  gate, useless for a 5 Elo claim. This is why the tiers must be explicit.

### Q3. What is H-0005's falsification bound? — **Measured E-PEXT/perft NPS ratio (PEXT ÷ ray, /O2, bit-identical counts) < 3.0.**

H-0005 claims "≥3x perft NPS"; a claim is falsified when the measured quantity falls BELOW the
claimed bar. Pre-registered rule (matching D-0003's intent, which gets this right):

- ratio ≥ 3.0 → H-0005 CONFIRMED; H-0006 rejected.
- 1.3 ≤ ratio < 3.0 → H-0005 rejected; H-0006 (1.3-2.5x) supported.
- 1.0 < ratio < 1.3 → both magnitude claims rejected (direction only).
- ratio ≤ 1.0 → H-0005 and H-0006 both rejected.

**Factual error to fix:** H-0005's Measurement Addendum says "Falsification of H-0005 requires
E-PEXT NPS ratio >= 3.0" — backwards; ≥3x *confirms* H-0005. D-0003's decision rule leaves
[0,1.3) ∪ (2.5,3.0) uncovered, and H-0006's own "<1.0x" contradicts D-0003's "<1.3." Pin exactly
one partition before E-PEXT, and use within-session paired runs with a CI (E-00003 is
cross-session/unpinned; a point ratio near 1.3 or 3.0 is not a decision).

## Agreements (confirmed claims)

1. Perft correctness (10/10 exact) is **demonstrated** — re-ran it: matches.
2. E-00003's NPS table is **reproducible** — re-ran the harness fresh: /O2 46.6-50.5, /Od
   18.9-21.0 Mnps, ~2.3x. The "~2 sig figs, single machine, unpinned" caveat must survive into E-0002.
3. CMake forces `/Od /Zi /EHsc /JMC` + `/DEBUG` (CMakeLists.txt:16-17) — **demonstrated**. Note: it
   applies to ALL build types, not only Release; "Release ships debug flags" understates slightly.
4. `kana_o2.exe` (253,952 B) has unrecorded provenance and stays excluded from claims (D-0002).
5. Classical-first (H-0003 0.75), ordering-dominance (H-0008), PVS+TT deltas (H-0009),
   quiescence-inside-O3 (D-0006) are likely by literature + the circular-dependency argument,
   correctly labeled unmeasured here. I hold slightly lower: H-0008 0.65, H-0009 0.65 — the
   quantitative ranges (50-90%, 30-70%) have no engine-specific basis yet.
6. PEXT 1.3-2.5x (H-0006) is a reasonable working prior; I hold **0.5**, not 0.6 — the
   slider-attributable share of perft time is unprofiled. The ≥3x arithmetic (>140 Mnps ⇒ sliders
   ≈ 70%+ of time today) is sound; the direction is implausible.
7. H-0012 (king-capture exclusion + promo-phantom asserts, 0.7) — correct and cheap; `move_promo`
   on a non-PROMOTION move returns a phantom piece (defs.h:52). Required before any fast path.
8. H-0014 (state-integrity audit, 0.6) — well-motivated; perft counts moves, not clocks/keys.
9. Roadmap order (E-0002 → O3 with quiescence inside → PVS/TT deltas → E-PEXT → E-COPYMAKE →
   eval/Texel → SPRT → self-play → NNUE) accepted; dates correctly not commitments.

## Disagreements / attacks

1. **H-0005's addendum "falsification" sentence is wrong** (Q3) — a spec-level error that would
   corrupt the E-PEXT decision rule if copied into the experiment record.
2. **H-0010's bar under-specifies the protocol and under-budgets the games** (Q2). Split the
   hypothesis into "SPRT is required" (adopt now) and "default parameters" (adopt with cap +
   tiers).
3. **D-0002's framing is a false dichotomy.** "Can ANY NPS number be trusted?" conflates
   provisional (E-00003: measured, reproducible, ~2 sig figs, unpinned) with certified (E-0002:
   5 reps + hash logging + protocol). Post-E-00003 the answer is neither "no NPS claim is
   interpretable" nor "numbers are fine": provisional numbers exist; certification gates any
   claim that changes the roadmap. /Od-relative deltas are acceptable only for cheap rank-order
   screening, on the untested assumption that codegen is a near-uniform multiplier.
4. **D-0006: A's conclusion (quiescence first) is right; A's stated rationale is too strong.**
   The "comparisons uninterpretable without quiescence" argument is decisive for eval-delta and
   SPRT stages, not for the first-vs-random milestone (a random mover is beaten by any search).
   The decisive argument is B's own format: PVS/TT deltas measured on a fixed-depth
   no-quiescence tree do not carry forward once quiescence changes every leaf — you re-measure
   anyway, so B's order saves nothing while delaying the first playable engine. I take A's side
   with an amendment: the "crossover" experiment as written is vacuous on its own metric (both
   paths converge to the same final configuration by construction; "if identical, A wins" is a
   tie-break, not evidence). Pre-register instead: "days to first interpretable SPRT result +
   final nodes/TTD matrix + fixed-depth plain-AB node counts as regression pins while quiescence
   is developed." Confidence: 0.65 for quiescence-first.
5. **D-0005/H-0011: keep make/unmake as the O3 default.** H-0011's enabling argument ("~312 B
   fits in L1; memcpy is cheap") misses the multiplier: ~45 Mnps × 312 B ≈ 14 GB/s of memcpy
   traffic per node-copy versus O(undo-bytes) for make/unmake. Do not revisit DEC-0004
   preemptively; run E-COPYMAKE as a side microbench with a pre-registered rule (copy-make wins
   only if ≥5% TTD advantage at a depth with ≥10 s TTD, reproduced). Priors: literature favors
   make/unmake (0.6); copy-make wins in 10-14 (0.4). I will not fight a measurement.
6. **D-0003: revision discipline is good; the partition is incomplete** (Q3); add the
   paired-run/noise protocol to E-PEXT.
7. **Confidence overclaiming:** D-0002 position A as filed ("no NPS claim interpretable," 0.9)
   was wrong after E-00003; the addendum correctly walked it back to "measured ~2.3x." The
   addendum pattern handles this well — keep it; do not delete.

## Missing Arguments

- H-0010: no cap, no draw model, no pairing/color protocol, no time control, no post-cap decision.
- D-0003/H-0005/H-0006: no CI/noise plan for the ratio; the ratio partition is incomplete.
- D-0006: no criteria for "interpretable", no fixed-depth regression pins, no razoring /
  delta-pruning margin scoping.
- H-0009/H-0008: no engine-specific justification for the node-reduction ranges.
- H-0004/H-0013: no demonstration that Texel-on-quiet-labels transfers to play (holdout + SPRT
  is the right test; keep it).
- H-0011: no accounting of per-node memcpy bandwidth (Disagreement 5).

## Factual Errors

1. H-0005 addendum: "Falsification of H-0005 requires E-PEXT NPS ratio >= 3.0" — backwards (Q3).
2. H-0006 "Falsifiable bounds: <1.0x" vs D-0003 "falsification of H-0006 requires ratio < 1.3" —
   the two records disagree; exactly one rule may be pre-registered.
3. `main.cpp:11-17`/`dump_moves` prints "N legal moves" for a pseudo-legal list — live mislabel;
   the corpus's own diagnosis (mislabeled contract) is itself visible in the shipped harness.
4. Reports 1-3 and the megaprompt "Ground truth" call `generate_moves` "legal" — factually wrong
   about the code; self-corrected by reports 4-6 via new reports + D-0004 (correct process).
5. "Release ships /Od" — /Od is unconditional on all build types (CMakeLists.txt:16); severity
   negligible, the measured ~2.3x gap is unaffected.

## Assumptions (flagged, need measurement)

- Move ordering cuts nodes 50-90% (theory + all-engine practice; unmeasured here).
- Eval gains from Texel transfer from quiet labels to game play.
- Unpinned single-machine NPS is a stable ordering of versions (needs E-0002).
- PEXT exchange-rate ranking is the same at /O2 as at /Od.
- "No asserts needed in Release" — true for NDEBUG logic; `--legality`/`--audit` modes are
  tests, not asserts, and must ship as debug flags, not NDEBUG-only code.

## Proposed Experiments (pre-registered bars)

1. **E-LEGALITY** (resolves D-0004): `--legality` audit; print `generate_moves` count vs
   perft(1) count on the pinned-rook FEN (`7k/8/8/8/8/8/8/r3R2K w - - 0 1`, expect 16 vs 9) plus
   ~10 more adversarial FENs; fix the `dump_moves` label; file DEC-0005 SUPERSEDED-by revision.
   No behavior change to perft.
2. **E-SPRT pre-registration** (resolves H-0010): two-tier bar (screening δ=20, regression δ=5;
   α=β=0.05; LLR ±2.944; cap 30,000 games; draws=0.5 trinomial; 1000-pos rotating opening set;
   balanced colors; crash=loss; post-cap=INCONCLUSIVE) written into the experiment record before
   the first game.
3. **E-PEXT** (resolves D-0003): 4-way partition from Q3; within-session paired A/B; ratio + CI;
   counts bit-identical.
4. **E-COPYMAKE** (resolves D-0005): pre-registered ≥5% TTD rule at depths 6-14, two suites.
5. **E-0002**: certified bench, 5 reps, flags+hash logged — required before any of the above
   numbers are cited as facts.

## Verdict

The corpus is the most methodologically disciplined material in the collective so far: facts
separated from beliefs, measurements re-run by their author, and the H-0005→H-0006 and D-0002
addenda model the exact correction behavior the megaprompt demands. The central factual claim
(D-0004 pseudo-legal) is **correct — reproduced at runtime (16 vs 9)**. The central statistical
claim (H-0010 SPRT) is **correct in direction, under-specified in its bar**. The falsification
apparatus for H-0005/H-0006 **contains one backwards sentence and two conflicting bounds — fix
before E-PEXT** (Q3 rule). Roadmap order approved with the D-0006 amendment. I take positions in
D-0002..D-0006 as Agent C, appended to each debate record.

## Date
2026-09-09

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns. H-0005 and H-0010 receive dated addenda, per the record-update
> pattern (append, never overwrite).
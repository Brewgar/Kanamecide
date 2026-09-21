# Beliefs — adversarial-reviewer

> Beliefs are **beliefs**, not shared facts. Keep each explicit, versioned, and revisable.
> To change your mind, append a dated line under **Revisions** — never erase history.

## Belief: Perft correctness and the E-00003 baseline are demonstrated and reproducible

- **Status:** supported-by-evidence
- **Confidence:** 0.9
- **Last updated:** 2026-09-09

**Position:** `kana.exe` perft 10/10 PASS and the /O2 ~43-50 Mnps vs /Od ~19-21 Mnps baseline
(~2.3x) are facts on this machine, reproduced by me on 2026-09-09 (fresh run: /O2 =
46.6-50.5 Mnps, /Od = 18.9-21.0 Mnps, all counts bit-identical).

**Strongest argument for:** two independent runs (E-00003 author + me) agree; nodes are
deterministic counts; harness binaries exist.

**Strongest argument against:** single machine, unpinned, ~2 sig figs; cross-session.

**Evidence:** my runs this session; E-00003 record; `%TEMP%\kana_bench`.

**What would falsify this:** a re-build at /O2 differing >5%, or perft failing on another
machine with identical src.

**Recommended experiment:** E-0002 (5 reps + flags + binary hash) — already scheduled.

### Revisions
- 2026-09-09 — initial statement.

## Belief: `generate_moves` is pseudo-legal, not legal (D-0004 correct)

- **Status:** supported-by-evidence
- **Confidence:** 0.97
- **Last updated:** 2026-09-09

**Position:** Only EP (probe) and castling are legality-checked inline; king safety is filtered
post-make (perft.cpp:16, main.cpp:66). Contract: pseudo-legal + filter at the search site.
The docs/mislabel must be corrected; the generator must NOT be made fully legal.

**Strongest argument for:** runtime repro — pinned-rook FEN `7k/8/8/8/8/8/8/r3R2K w - - 0 1`
gives perft(1) = 9 vs generate_moves = 16 (7 illegal e1e2..e1e8 pushes).

**Strongest argument against:** none found; perft being correct does NOT make the generator legal.

**Evidence:** code read (movegen.cpp:16-125) + runtime output this session; D-0004.

**What would falsify this:** a code change that adds inline king-safety to all branches and a
FEN where generate_moves == legal count in a pinned position (impossible by construction today).

**Recommended experiment:** E-LEGALITY audit flag; fix `dump_moves` label.

### Revisions
- 2026-09-09 — initial statement.

## Belief: No version-strength claim is trustworthy without a pre-registered sequential test

- **Status:** working-assumption
- **Confidence:** 0.9 direction; parameterization is mine (below), not yet adopted.
- **Last updated:** 2026-09-09

**Position:** SPRT-style testing with pre-registered bounds is required BEFORE "version B is
stronger" enters the record. Refined defaults: screening H1 = +20 Elo (~1-1.5k games), regression
H1 = +5 Elo with α = β = 0.05 (LLR ±2.944, cap 30k games, draws = 0.5 trinomial, balanced colors,
fixed openings, crash = loss, post-cap = INCONCLUSIVE).

**Strongest argument for:** 1000 games ≈ ±21 Elo at 95% CI — insufficient for 5-Elo claims;
SPRT bounds errors with a finite cap.

**Strongest argument against:** a properly powered fixed-sample test with pre-registered N gives
the same error control; SPRT's advantage is expected sample size, not correctness — so the *cap*
and *pre-registration* are the load-bearing parts, not the sequentiality.

**Evidence:** Wald (1947); Stockfish/LC0 practice; R-0002 Q2 arithmetic.

**What would falsify this:** a demonstrated fixed-sample protocol achieving the same error rates
cheaper on this hardware would demote sequential testing to an optimization.

**Recommended experiment:** E-SPRT with the two-tier pre-registration (H-0010 addendum).

### Revisions
- 2026-09-09 — initial statement.
- 2026-09-21 — **ADOPTED AS PROJECT POLICY: DEC-0010** (calibration of this belief, from
  W-0002 / D-0007). Parameters now measured-variance-derived, not sketched:
  screening [0, +20] with cap 8,000 games; regression [0, +5] with cap 30,000;
  magnitude claims only as wide-zone SPRTs [M-50, M]; α=β=0.05, LLR ±2.944; post-cap
  INCONCLUSIVE. The earlier "screening ~1-1.5k games" sketch was low: with the measured
  σ=371 Elo/game the ASN is ~1.8-2.0k. Agent B's strongest-argument-against (fixed-sample
  equivalence) is now a recorded standing objection in D-0007, not a defeater: the tiers
  are defined by margins/error rates, so fixed-N implementations remain valid. What
  falsifies the calibration remains as stated: a demonstrated cheaper protocol with the
  same error rates on this host → W-0005's realized stopping times are the test.

## Belief: H-0005's falsification bound is E-PEXT NPS ratio < 3.0 at /O2


- **Status:** working-assumption
- **Confidence:** 0.85 (protocol requirement); 0.5 (H-0006 1.3-2.5x magnitude)
- **Last updated:** 2026-09-09

**Position:** "≥3x" is falsified by ratio < 3.0 (H-0005's addendum says ≥3.0 — backwards).
Pre-register the full 4-way partition (R-0002 Q3); pin the H-0006 bound conflict (<1.0 vs <1.3).

**Strongest argument for:** a claim is falsified when the measurement falls below it; H-0005's
own addendum contradicts D-0003's (correct) restoration rule.

**Strongest argument against:** the added rigor may look like pedantry — but without one rule,
E-PEXT's result is ambiguous at exactly the boundary the rule is meant to test.

**Evidence:** H-0005 addendum text vs D-0003 decision rule; R-0002.

**What would falsify this:** adoption of a different partition by the collective with rationale
(a live possibility; the point is ONE pre-registered rule).

**Recommended experiment:** E-PEXT with within-session paired A/B + CI.

### Revisions
- 2026-09-09 — initial statement.
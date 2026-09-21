---
type: current_position
agent: adversarial-reviewer
confidence: 0.65
focus: "Falsification & statistical rigor of proposals"
last_updated: 2026-09-09
---

# Current Position — adversarial-reviewer

## Overall Assessment (first entry, 2026-09-09)

Reviewed researcher-architect's 6-report corpus (review R-0002) and took positions in
D-0002..D-0006 (Agent C/D). Independent verification THIS session, not inspection:
- `build/Release/kana.exe` → **10/10 PASS** (all exact counts).
- E-00003 scratch harness re-run fresh → /O2 = 46.6-50.5 Mnps, /Od = 18.9-21.0 Mnps,
  ratio ~2.3x, counts bit-identical. E-00003 **reproduces**.
- Pinned-rook FEN `7k/8/8/8/8/8/8/r3R2K w - - 0 1`: `perft(1)` = 9 legal vs
    `generate_moves` = 16 pseudo-legal (e1e2..e1e8 illegal) — **D-0004 confirmed at runtime**.
- `src/movegen.cpp:5-128` read directly: pawn/knight/bishop/rook/queen/king branches apply
  only vacancy + `& ~own` (no king-safety test); only EP probe (:52-63) and castling
  not-through-check (:107-125) are inline legality checks. Confirms the pseudo-legal contract.

The corpus is the most disciplined material in the collective so far: facts vs beliefs separated,
measurements re-run by the author, self-corrections via addenda (H-0005→H-0006, D-0002). Central
findings confirmed; the bars and falsification bounds need the fixes in R-0002.

## Review Summary — Three Required Answers

Reviewed all 6 reports by researcher-architect (2026-09-09). Independent verification
performed THIS session: built `build/Release/kana.exe` from source (cmake + MSVC 19.51),
ran the perft suite (10/10 PASS, exact counts), ran the pinned-rook FEN diagnostic, and
read `src/movegen.cpp:5-128` directly. Positions taken in D-0002..D-0006 as Agent C.

1. **Is D-0004's pseudo-legal finding correct?** — YES, CONFIRMED. `generate_moves`
   (movegen.cpp:5-128) emits pseudo-legal moves (pawns: vacancy checks only;
   knights/bishops/rooks/queens/king: only `& ~own`); no king-safety test. Only the
   en-passant make/unmake probe (`:52-63`) and castling not-through-check (`:107-125`)
   are inline legality checks. King safety is filtered post-make in `perft.cpp:16`
   and `main.cpp:66`. Runtime repro: pinned-rook FEN `7k/8/8/8/8/8/8/r3R2K w - - 0 1`
   → perft(1) = 9 legal vs generate_moves = 16 pseudo-legal (7 illegal e1e2..e1e8
   expose the king). DEC-0005 wording must be corrected to "pseudo-legal + filter at
   the search site." Confidence: 0.97.

2. **Is H-0010's SPRT bar set right?** — Direction YES (SPRT required before any
   version-claim); parameterization NO. H-0010's defaults omit the quantities that make
   SPRT a *protocol* rather than a slogan: LLR thresholds (A = +2.944, B = −2.944),
   maximum-game cap with post-cap = INCONCLUSIVE (never "keep playing until
   significant"), draw model (draws = 0.5 under trinomial; Elo = 400·log10(odds)),
   pairing/color protocol, fixed time control, and a fixed rotating opening set.
   At H1 = +5 Elo, α = β = 0.05, a fixed-sample 95% CI needs ~15-20k games
   (±681/√N); SPRT expected stopping time is the same order (~10k-40k under H0
   near the boundary). A 5-Elo gate is a final-regression gate, not a per-change gate.
   Adopt two tiers: screening δ ≈ 20 Elo (~1-1.5k games) for gating experiments;
   regression δ = 5 Elo for "version B is stronger" claims. Addendum written into
   H-0010; full protocol in R-0002 Q2 and beliefs.md.

3. **What is H-0005's falsification bound?** — Measured E-PEXT perft-NPS ratio
   (PEXT ÷ ray-stepping, /O2, bit-identical perft counts, within-session paired A/B
   runs, ratio + CI) < 3.0. H-0005 claims "≥3x"; a ratio below 3.0 falsifies it. The
   H-0005 Measurement Addendum sentence "Falsification of H-0005 requires ratio >= 3.0"
   is BACKWARDS (≥3x CONFIRMS H-0005) — corrected via addendum. Full 4-way partition
   pre-registered in D-0003 / H-0005 addendum / R-0002 Q3:
   - ratio ≥ 3.0 → H-0005 CONFIRMED; H-0006 rejected.
   - 1.3 ≤ ratio < 3.0 → H-0005 falsified; H-0006 (1.3-2.5x) supported.
   - 1.0 < ratio < 1.3 → both magnitude claims falsified (direction only).
   - ratio ≤ 1.0 → H-0005 and H-0006 both falsified.
   H-0006's original "<1.0x" wording conflicted with this; an adversarial-reviewer
   addendum has been appended to H-0006 to align it with the D-0003 partition.

## Strongest Parts
1. Perft correctness + E-00003 NPS baseline: demonstrated, reproducible (re-ran it).
2. D-0004 pseudo-legal finding: correct; reproduced (16 vs 9).
3. Addendum self-correction pattern: the right process, keep it.
4. Classical-first roadmap with staged deltas: sound and correctly labeled unmeasured.

## Weakest Parts
1. H-0010's SPRT bar is a slogan, not a protocol: no cap, draw model, pairing/color protocol,
   time control, or post-cap decision; 5 Elo at α=β=0.05 costs ~15-20k+ games → needs two tiers.
2. H-0005's addendum states the falsification bound BACKWARDS (says ≥3.0; should be <3.0).
   RESOLVED — added adversarial-reviewer addendum to H-0006 aligning its "<1.0x" bound
   with D-0003's "<1.3"; the 4-way partition in D-0003/H-0005 addendum is now the single
   pre-registered rule. Remaining: still needs the E-PEXT experiment to run.
3. D-0006's cross-over decision rule is vacuous: both orders converge to the same final
   configuration by construction ("if identical, A wins" is a tie-break, not evidence).

## Current Preferred Architecture
No change to the roadmap order: E-0002 (certified bench + /O2) → O3 (plain-AB + staged ordering +
quiescence INSIDE the baseline + ID + UCI) → PVS-only/TT-only deltas (H-0009) → E-PEXT (H-0006/
D-0003) → E-MGCOPY (H-0007) → E-COPYMAKE (H-0011/D-0005, side microbench) → SPRT (H-0010,
two-tier) → eval tapered+Texel (H-0004/H-0013) → self-play → NNUE. Positions: quiescence-first
(D-0006, 0.65); make/unmake stays unless E-COPYMAKE shows ≥5% TTD (D-0005, 0.6); pseudo-legal +
filter as the search contract with the label fixed (D-0004, 0.97).

## Highest-Value Research Direction
Statistical discipline as a first-class deliverable: E-0002 certification protocol for every
number that enters project_state.md, and E-SPRT two-tier pre-registration (δ=20 screening /
δ=5 regression; α=β=0.05; LLR ±2.944; cap 30k; draws=0.5; post-cap INCONCLUSIVE).

## Major Concerns
1. Uncertified NPS numbers being cited as facts (rule: provisional-only until E-0002).
2. Search consumers trusting `generate_moves` as fully legal (fix label + document contract).
3. ~~Falsification bounds that conflict across records~~ — RESOLVED by H-0006 addendum +
   D-0003 4-way partition; one rule pre-registered before E-PEXT.
4. Any p-hacking vector in SPRT design ("keep playing until significant" must be forbidden).

## Open Questions
- PEXT magnitude (E-PEXT, partition as in R-0002 Q3).
- Copy-make crossover depth (E-COPYMAKE).
- Whether 5 Elo regression on THIS hardware is affordable in wall-time (needs the E-SPRT
  screening tier first).

## Confidence
0.65 overall. Perft + baseline + D-0004 finding: **demonstrated** (0.9+). SPRT direction needed:
0.9. PEXT 1.3-2.5x magnitude: 0.5. Quiescence-first: 0.65. /Od ranking transfer: 0.7 (assumption).
H-0008/H-0009 node-reduction ranges: 0.65. I hold slightly below the architect on every
unmeasured magnitude — that is the job.

## What Would Change My Mind
- E-PEXT ratio ≥ 3.0 at /O2 (restores H-0005); ratio < 1.3 (both magnitude claims falsified;
  direction "PEXT ≥ ray" survives or not); ratio < 1.0 (rays win; both H's fully rejected).
- E-COPYMAKE showing ≥5% TTD at any depth 6-14, reproduced → revisit DEC-0004.
- A certified SPRT run showing δ=5 Elo decisions in <10k games on this hardware → keep one tier.
- A search regression pin failing during quiescence development → quiescence-first costlier than
  assumed; reconsider order (D-0006).
- A same-hardware MCTS+NNUE prototype out-SPRTing O3 → architecture revisitation.

## Last Updated
2026-09-09

2026-09-21 — W-0002 session (E-0010 decision-rule recalibration): D-0007 RESOLVED,
DEC-0010 ACTIVE (two-tier + magnitude-zone SPRT calibrated from measured σ=371 Elo/game;
caps 8k/30k/8k), R-0009 addendum on E-0010 (screening PASS / regression PASS / ">=150"
not established at N=240). Handoff HO-0002 to verification-auditor; W-0002 IN_PROGRESS
pending independent verification. Gate 0: hard-blocked (F-0002), attempted once.

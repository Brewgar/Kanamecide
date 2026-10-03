---
id: D-0004
type: debate
title: generate_moves is pseudo-legal not legal: reconcile DEC-0005 wording and the search contract
status: OPEN
participants: [researcher-architect, adversarial-reviewer]
example: false
created: 2026-09-09
last_updated: 2026-10-02
---

# D-0004 — generate_moves is pseudo-legal not legal: reconcile DEC-0005 wording and the search contract

## Question
`src/movegen.cpp` `generate_moves` is documented (DEC-0005, `project_state.md`, `README.md`, and
the megaprompt "Ground truth") as generating only LEGAL moves. Code inspection shows it emits
pseudo-legal moves for every piece type except en passant (make/unmake probe) and castling
(not-through-check); king-safety filtering is applied later in `perft.cpp` and `main.cpp`.
Should the project (a) correct the wording/decision to "pseudo-legal + filter at the search
site", or (b) change `generate_moves` to be truly legal — and what is the correct search-phase
contract?

## Agent A — researcher-architect (this report's position)
Position: The implementation is pseudo-legal; correct the record and adopt pseudo-legal + king-safety filter as the search contract.
Confidence: 0.85 (code path fully traced; demonstrated by inspection).
Argument: A pinned piece (rook/bishop/queen/pawn) and a king moving into check are emitted by
`generate_moves`; `perft.cpp:16` and `main.cpp:66` filter them via `!attacked_by(...)`. This is
the standard, fastest design for search (generate pseudo-legal, test legality once per move that
is actually made, or at the leaf). Making `generate_moves` fully legal at the source would
duplicate king-safety work and hurt NPS. The correctness risk is not the code (perft is
validated) but the misleading "legal move generation" claim, which could cause a future consumer
(UCI `go`, eval, debugging asserts) to trust unfiltered output.

## Agent B — the project's documented claim (DEC-0005 / project_state.md / README.md)
Position: "legal move generation (not pseudo-legal + filter)."
Confidence: (recorded as a fact, not a belief.)
Argument: The wording was reconstructed from README and records intent ("never emit an illegal
move"), but does not match the current code, which realizes correctness by filtering in perft.

## Agent C — adversarial-reviewer (2026-09-09)
Position: CONFIRMED by independent runtime repro, not only inspection. Constructed a pinned-rook
FEN (black rook a1 pins white rook e1 to king h1; `7k/8/8/8/8/8/8/r3R2K w - - 0 1`):
`kana.exe --fen <fen> 1` prints **9 nodes at depth 1** (perft's legally-filtered count) while
`dump_moves` lists **16 "legal moves"** (generate_moves pseudo-legal output; e1e2..e1e8 are
illegal — they expose the king). The mislabel is live in the shipped harness today. This FEN
satisfies D-0004's "Evidence Missing" (a quantitative repro). Adopt resolution (a): correct the
record + keep pseudo-legal + filter at the search site (the standard, fastest design; making
generate_moves fully legal would duplicate work and cost NPS). Optional hardening: assert
`legal` count == pseudo-legal count at startpos ("--moves" case) so the label can never drift.
Confidence: 0.97 on the finding (author: 0.85). Disagree with nothing material; recommend the
E-LEGALITY audit (run the FEN + ~10 adversarial FENs through perft(1) vs generate_moves in a
debug flag; file DEC-0005 SUPERSEDED-by).

## Points of Agreement
Perft correctness is demonstrated (10/10 exact this session). The make/unmake EP probe and the
castling checks are genuinely legality-checked inline. The system as a whole is correct because a
king-safety filter exists on every path that matters today.

## Points of Disagreement
Whether `generate_moves` should be called (and consumed) as "legal" (documentation) vs
"pseudo-legal" (code), and whether search should consume a truly-legal generator or a
pseudo-legal one plus a fast filter.

## Evidence Available
`movegen.cpp`: pawn/knight/bishop/rook/queen/king branches apply only `& ~own` (and a pawn-push
vacancy check), with no king-safety test; EP uses a make/unmake probe; castling checks attacked
squares. `perft.cpp:16` applies `!attacked_by(b, king_sq[us], side)` after make_move. `main.cpp:66`
does the same for root moves. Fresh run 2026-09-09: 10/10 perft PASS; `--moves` lists 20 startpos
moves (a position where pseudo-legal == legal, concealing the distinction).

## Evidence Missing
A minimal repro FEN (e.g. a piece pinned to the king, or a king able to step into check) where
`generate_moves` count exceeds the legal count — to quantify, not merely inspect. No test asserts
the "legal" property anywhere.

## Proposed Resolution Experiment
Add a `--legality` debug mode: for a pinned-piece FEN, print the `generate_moves` count vs
`perft(1)` count and enumerate the difference. Then file a DEC-0005 revision (SUPERSEDED-by) that
states "pseudo-legal generation + king-safety filter in search/perft navigation" and update
README + project_state wording. No behavior change is required — this is a contract/documentation
correction plus an explicit search-side legality step (already needed for Phase 2).

## Resolution
(unresolved — do not force consensus)

## Date
2026-09-09

## Addendum (chief-architect, 2026-10-02) — RE-ATTESTATION: SUPERSEDED-BY DEC-0008 (finding RE-ATTESTED)

**Verdict on the question: SUPERSEDED-BY `DEC-0008`** (ACTIVE, 2026-09-10), which adopted resolution
(a) — correct the record, keep pseudo-legal generation plus a king-safety filter at the search/perft
site. `DEC-0005` now carries `status: SUPERSEDED, superseded_by: DEC-0008` and its own supersession
addendum. The contract question posed above is answered; the debate text is history.

**Verdict on the finding: RE-ATTESTED — re-verified at runtime this session, not inherited.**

- `build\Release\kana.exe --fen "7k/8/8/8/8/8/8/r3R2K w - - 0 1" --moves` prints `TOTAL: 9` for the
  legality-filtered perft(1) split while the pseudo-legal list prints `16 legal moves:` — 16 vs 9,
  exactly as filed above, with e1e2..e1e8 present in the list.
- The generator is unchanged in the relevant region: `src/movegen.cpp:78,86,94` apply only `& ~own`
  to bishop/rook/queen attacks with no king-safety test; the en-passant make/unmake probe is still
  at `:52-63`; the castling not-through-check tests are still at `:107-125`; `src/perft.cpp:16`
  still applies `!attacked_by(b, b.king_sq[us], b.side)` after `make_move`.
- Perft anchor green on the same binary: 10/10 exact, including startpos d5 = 4,865,609.

**One item from this record's Proposed Resolution is still OPEN.** DEC-0008's Evidence section
promises the `dump_moves` mislabel "to be corrected in the same Milestone-1 change". It was not:
`src/main.cpp:234` still reads `printf("%d legal moves:\n", n);` over an unfiltered pseudo-legal
list, and the run above shows the wrong label shipping in the current binary. The `--legality` audit
mode was also never added.

This is **not** a correctness defect — every consumer filters (`src/perft.cpp:16`, `src/search.cpp:139`
in `qsearch`, the root move loop) — but it means DEC-0008's evidence line understates the remaining
debt. The mislabel is live-severity-low, documentation-only. A fresh seat should file this as its
own work item rather than let it live inside an addendum.

**Status:** the debate's question is answered (SUPERSEDED-BY DEC-0008); the finding stands and the
label fix remains outstanding.
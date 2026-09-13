# KANAMECIDE — ROUND 2 CONSENSUS MEGAPROMPT

> Companion to `research/AGENT_MEGAPROMPT.md`. Read that file first and treat it as your system
> prompt; this document adds the Round-2 task. The orchestrator hands this file to each agent
> together with its role profile (`research/agents/<role>/profile.md`).

## 0. Purpose of this round

The collective produces research value in two ways: **independent analysis** and **convergence**.
Round 1 produced the analysis (7 researcher-architect reports, review R-0002, debates D-0002–D-0006,
hypotheses H-0003–H-0015, and the first measured baseline E-00003). Round 2 exists to:

1. Get **every** agent into the project — two roles have never entered.
2. Force **explicit agreement/disagreement** on every open debate. No silent abstentions.
3. Produce an **improvement agenda** for Phase 2 (search) that the whole collective owns,
   not just one role.
4. Convert every open empirical question into a **pre-registered resolution experiment**, so
   Round 3 is "run experiments", not "argue more".

## 1. Facts as of 2026-09-09 (demonstrated — do not relitigate)

- **Engine:** Phase 1 correctness complete. `build\Release\kana.exe` perft **10/10 PASS**, exact
  counts (startpos d1–5; kiwipete d3; cpw3/4/5/6 d4). Re-verified by three separate runs.
- **Build flags:** Release ships `/Od /Zi /EHsc /JMC` + `/DEBUG` (`CMakeLists.txt:16-17`).
  E-00003 measured **/O2 ≈ 43–50 Mnps vs /Od ≈ 19–21 Mnps** on startpos d5 (~2.1–2.4× gap),
  perft counts bit-identical across both builds (correctness is flag-independent).
- **Movegen contract:** `generate_moves` (`movegen.cpp`) is **pseudo-legal, not legal**.
  Only en-passant (make/unmake probe) and castling (not-through-check) are legality-checked
  inline; king-safety filtering lives in `perft.cpp:16` and `main.cpp:66`. Confirmed at runtime
  (pinned-rook FEN `7k/8/8/8/8/8/8/r3R2K w - - 0 1` → 9 legal vs 16 pseudo-legal). → D-0004.
- **No search, no evaluation, no UCI.** Nothing in `src/` has been edited this phase.
- **`kana_o2.exe`** exists in build/Release (253,952 B) with unrecorded provenance — it is NOT
  evidence and is excluded from claims until documented (D-0002).

## 2. State of the collective — "have the agents reached absolute agreement?"

**No. And that is the correct state of a research collective at this stage.**

"Absolute agreement" is not the goal. The goal is that **every open question lands in exactly
one of three terminal states**:

1. **AGREED (fact or procedure)** — demonstrated or pre-registered; no further work before it
   may be acted on.
2. **ROUTED (open, empirical)** — no belief-agreement needed, but a single *pre-registered
   decision rule* exists so the disagreement becomes a measurement instead of an argument.
3. **CONFLICT (open, unresolved)** — the positions share no test yet. This round must drive
   every CONFLICT down to ROUTED, then to AGREED when the experiment runs.

Round 2 closes when **every debate D-0001…D-0006 is AGREED or ROUTED** — not when everyone
agrees. Unanimity is only expected on the demonstrated facts (perft 10/10, the /O2 vs /Od gap,
and the pseudo-legal contract).

- **6 debates OPEN, 0 resolved** (D-0001 … D-0006).
- **14 active hypotheses; 0 accepted or rejected on evidence.** H-0001, F-0001, E-0001 are
  `example: true` mocks and must be cited only as format examples.
- **Two of four agents have not entered the project at all** — `systems-researcher` and
  `implementation-engineer` still have placeholder `current_position.md` files.
- Between the two active agents there is **convergence on facts and procedure, divergence on
  magnitudes and parameterization**:

| Question | researcher-architect | adversarial-reviewer | Status |
|---|---|---|---|
| Perft 10/10 correctness | demonstrated | demonstrated | AGREED (fact) |
| Pseudo-legal contract (D-0004) | 0.85 | 0.97, confirmed by repro | AGREED |
| /Od→/O2 gap ≈ 2.3× (D-0002) | measured | reproduced | AGREED (fact, E-00003) |
| Classical-first roadmap (D-0001) | 0.75 | no objection filed | AGREED (default) |
| PEXT speedup magnitude (D-0003) | 1.3–2.5× (0.6) | 0.5; needs slider-share profile | OPEN (empirical) |
| SPRT bar (H-0010) | "required before claims" | "required, but two-tier δ=20/δ=5 + cap + draw model" | OPEN (parameterization) |
| O3 order & metrics (D-0006) | quiescence-first 0.7 | quiescence-first 0.65; crossover rule vacuous | PARTLY OPEN |
| Copy-make (D-0005) | plausible 0.55 | make/unmake 0.6; ≥5% TTD gate | OPEN (empirical) |
| /Od ranking transfer (D-0002) | unknown until certified | 0.7 screening-only | OPEN (assumption) |

- **R-0002 raises three objections against the architect corpus that are UNANSWERED:**
  1. H-0010's SPRT bar is a slogan, not a protocol (no cap, no draw model, no pre-registration).
  2. H-0005's falsification bound was stated backwards (≥3.0 confirms, does not falsify) — patched
     by addendum, but the patch must be ratified.
  3. D-0006's crossover experiment is vacuous (both arms converge to the identical final
     configuration; "if identical, A wins" is a tie-break, not evidence).
- **`research/IMPLEMENTATION_MEGAPROMPT_DRAFT.md`** exists and carries a status banner: it is
  **NOT a consensus product and NOT consent to implement.** Its gate is exactly this round: the
  three other agents review the architect corpus and file no material objection (or the objection
  is resolved with a concrete pre-registered fix).

Do **not** manufacture consensus where evidence is missing. The unit of resolution is a
(pre-registered) measurement, not a vote.
---

## 3. Required deliverables - ALL FOUR AGENTS

Every agent MUST produce all of A-G this round. Output goes in your own directory
(`research/agents/<role>/`); never edit another agent's files; never edit `project_state.md`
with opinions.

**A. Enter (or re-enter) the project.** Update `research/agents/<role>/current_position.md`
with a dated "Round 2" section; keep all prior provenance text. If you are
`systems-researcher` or `implementation-engineer`, this is your FIRST entry - produce a full
A-P assessment from your own profile's lens (architecture / strengths / weaknesses /
correctness / perf / methodology), not a two-line placeholder.

**B. State your opinion of the project state.** Exactly two labeled paragraphs:
- "Strongest and most trustworthy" (what you would bet on, and why the evidence supports it),
- "Weakest and most likely wrong" (what you suspect is wrong or over-confident, and why).

**C. Answer the agreement questions explicitly — and record them in the shared ledger.**
For EACH debate D-0001 through D-0006, write in your own files:
- your position (one sentence),
- your confidence (0-1),
- one sentence of the form "I agree with <agent> on <claim> because <reason>" or
  "I disagree with <agent> on <claim> because <reason>".
- If your position is "insufficient evidence", that is allowed - but you must state which
  measurement would change it, and name the experiment (see F).
Then append your row to the collective matrix `research/AGREEMENT_MATRIX.md` — one
`AGREED / ROUTED / CONFLICT` state plus a one-line AGREE/DISAGREE reason per debate. This is
the only shared file you may edit this round, and only to fill your own row.
- NO abstentions. D-0001 currently contains only EXAMPLE positions; it needs real ones.

**D. Respond to the three unanswered objections in R-0002.** For each of
(1) SPRT parameterization, (2) H-0005 falsification bound patch, (3) D-0006 vacuous crossover
rule - state: support / refute / amend, with a SPECIFIC change to the record. Leave nothing
pending silence this round.

**E. Propose project improvements.** Maximum 5, prioritized. Each must specify: WHAT,
WHERE (file/function/process), WHY (the belief being replaced), EXPECTED BENEFIT
(quantified where possible), and HOW TO MEASURE IT (pre-registered metric). A proposal
without a measurement is a comment, not a proposal.

**F. Pre-register ONE experiment** that would change your mind on your single biggest open
disagreement. Create or update `research/experiments/E-####` with: hypothesis, baseline,
candidate, difference, hardware, dataset, test method, metrics, and the DECISION RULE
(what result maps to which conclusion). Use `python research/scripts/research.py new-experiment`.

**G. Do NOT edit `src/`.** Code is implementation-engineer's output AFTER Round 2 closes and
the draft's gates pass. You may include exact code sketches inside your report body.
---

## 4. Per-agent focus for Round 2

- **researcher-architect** - Defend or amend the corpus against R-0002 items 1 and 3; file real
  positions into D-0001 (currently EXAMPLE-only); ratify the D-0004 pseudo-legal contract
  resolution and the DEC-0005 supersession; publish the Phase-2 build order (E-0002 then O3 with
  quiescence inside, then PVS/TT deltas, then E-PEXT, then E-COPYMAKE, then E-SPRT) as your
  pre-registration.
- **adversarial-reviewer** - Review every new position for statistical/evidential rigor; flag
  any re-import of an unmeasured magnitude as fact; adjudicate D-0002/D-0004 resolutions once
  the engineer and systems agent have spoken; keep the falsification-bound ledger per debate.
- **systems-researcher** - FIRST ENTRY. Establish hardware ceilings: pinned perft NPS,
  PEXT instruction latency on Zen 5, AVX-512 VNNI throughput, RTX 5070 Ti batch-inference
  latency curves. Advise whether E-0002's `--bench` must pin threads/affinity. Define the
  data/self-play pipeline prerequisites for Phase 3. Place a feasibility gate on GPU MCTS for
  D-0001 (what must be measured before PUCT on this card is even arguable).
- **implementation-engineer** - FIRST ENTRY. Cost the implementation draft's Milestones 0-3
  in effort and risk; state whether the O3 milestone (quiescence + ordering + ID + UCI in one
  shot) should be split, and into which sub-milestones; propose the bench/correctness harness
  you would build first (E-0002); flag any perft-invalidating hazard in the pseudo-legal +
  king-safety-filter contract before you trust it in search.

---

## 5. Method rules (standing megaprompt, reiterated for this round)

- Calibrated language only: demonstrated / strongly supported / likely / plausible /
  speculative / unknown.
- Facts live in `research/project_state.md`; opinions live in your role directory. Never rewrite
  an existing record - append addenda (the tooling never overwrites).
- One pre-registered decision rule per experiment BEFORE it runs.
- Agent confidence is a hypothesis, never evidence. Do not update your position because someone
  is confident; update it because a measurement or derivation moved.
- Consensus is not a prize. Disagreement with reasons is the deliverable; the record preserves
  both positions until evidence resolves them.

---

## 6. Sequencing, exit criteria, and the gate

1. All four agents complete section 3 (A-G), fill their row in `research/AGREEMENT_MATRIX.md`,
   and run `python research/scripts/research.py update` (regenerates `index.md`/status).
2. **First-entry verification** (systems-researcher, implementation-engineer): before taking a
   position, independently reproduce the two demonstrated findings — perft 10/10, and the
   `7k/8/8/8/8/8/8/r3R2K w - - 0 1` repro (16 pseudo-legal vs 9 legal). Mark each "verified" or
   "contradicted" in your position; do not inherit either from the corpus.
3. The orchestrator merges the four improvement proposals (3.E) into the scope of
   `IMPLEMENTATION_MEGAPROMPT_DRAFT.md` and files any newly required resolution experiment.
4. **Exit criteria — Round 2 closes when ALL of:** every agent has a dated Round-2 position in
   `current_position.md`; every debate D-0001…D-0006 is AGREED or ROUTED in the matrix; the three
   R-0002 objections are answered by all four; and every empirical question has exactly one
   pre-registered decision rule. Unanimity of belief is NOT an exit criterion.
5. **The gate is dissent-gated, not consensus-gated.** `IMPLEMENTATION_MEGAPROMPT_DRAFT.md` opens
   for Milestone 0 when no agent files a *material* objection. A material objection is admissible
   only if it (a) demonstrates a factual/measurement error, or (b) names a concrete pre-registered
   experiment whose result would change the milestone. A bare "I disagree" with neither is not a
   position — route it back to section 3. Unresolved material objections block Milestone 0 and
   route to their pre-registered experiment.
6. Round 3 = execution: run the pre-registered experiments, write results back into
   `experiments/E-####` records, update `project_state.md` with any new demonstrated facts.
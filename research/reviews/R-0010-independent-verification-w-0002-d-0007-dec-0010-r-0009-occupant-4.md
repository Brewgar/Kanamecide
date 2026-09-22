---
id: R-0010
type: review
reviewer: verification-auditor
target: W-0002
kind: verification
status: COMPLETED
work_item: W-0002
related: [D-0007, DEC-0010, R-0009, E-0010, HO-0002, EV-0001, EV-0010, F-0002]
example: false
created: 2026-09-22
---

# R-0010 — Independent verification of W-0002 (D-0007 + DEC-0010 + R-0009), verification-auditor occupant 4

## Scope

HO-0002, executed by the rotating verification-auditor seat (occupant 4, zero chat
history; the host could not even run the engine — measured below). I did not accept
the owner's summary: I re-ran every command in the handoff's command list, re-derived
five families of numbers from scratch in my own script
(`research/context/va4_rederive.py`), and checked the E-0010 record against git
history.

## Agreements

- D-0007 is genuinely RESOLVED and its resolution text contains the arithmetic, the
  strongest counter-case (Agent B), and the explicit scope limits — not a slogan.
- DEC-0010 is ACTIVE and cites E-0010's MEASURED CI95 (+116.1, [+70.8,+163.5], N=240)
  plus the derived power tables; every derived number I checked reproduces.
- R-0009 is COMPLETED, `kind: critique`, an addendum that restates E-0010's outcome
  under DEC-0010 without touching E-0010 — confirmed read-only by git (below).
- Gate 0 matches F-0002: one attempt at `build\Release\kana.exe` produced the
  App Control / Device Guard policy block with no process started
  (`research/context/bootstrap/gate0.txt`). No engine numbers were claimed by me this
  session, and none of the W-0002 records claim a *new* measured engine number — every
  input cites E-0010's 2026-09-14 measurement (pinned by EV-0001/EV-0010).

## Disagreements

None material. Two numerical nits, neither verdict-relevant (see Factual Errors).

## Missing Arguments

None required for the acceptance criteria. The intermediate ASN claim "ASN ~4,050 near
the midpoint d=5 or 15 (Tier S)" recomputes as 2.9444/(100/137,545) ≈ 4,050 games —
matches.

## Factual Errors

None that change any tier verdict or the resolution. Two documentation-class nits:

1. **ASN(H0) column is ~11% above textbook Wald** (D-0007's ASN table; DEC-0010's
   "Expected cost" rows; `w0002_power.py` line 48). For symmetric alpha=beta the Wald
   boundary expectation under H0 is `alpha*A + (1-alpha)*B = -0.9*A`, so
   ASN(H0) = 0.9*A/KL = **1,822 / 29,159 / 292** games for tiers S/R/M — identical to
   ASN(H1). The records print 2,025 / 32,399 / 324 (i.e. A/KL). The error runs
   **conservative** (overstates cost), so every "this is expensive" conclusion stands;
   the "sequential vs fixed" framing in D-0007/DEC-0010 is unaffected.
2. **"Within 1.2%" rounding.** The h(N)=1.96*371/sqrt(N) model predicts h(240)=46.92
   vs the measured 46.35 — a **1.23%** mismatch, which the records round to 1.2%.
   Immaterial (both DEC-0010 and R-0009 treat it as a model-sanity check only).

Also noted, not an error in any record: HO-0002's command list names
`research.py reviews`, which is **not a subcommand** (usage error; raw capture
`research/context/va4_reviews.txt`). R-0009's COMPLETED status was instead verified
from its front-matter plus `validate`'s in-vocabulary scan of all reviews — the same
evidence class the acceptance criterion asks for.

## Assumptions

- I took E-0010's W/L/D, CI95, and throughput as MEASURED inputs (per HO-0002's
  scoping: E-0010's measurements are the domain of R-0004/R-0008, both VERIFIED).
- The re-derivations use the declared Wald/normal model; where the records also offer
  the score-space (trinomial, draws-as-halves) convention I recomputed that too and
  got the same side of every bound.

## Proposed Experiments

None. The already-routed follow-ups stand: W-0005 (offline SPRT-ASN validation against
the retained E-0010 JSONL — no engine needed) and E-MAG-6V0 (the ~910-game [100,150]
decision — engine-dependent, blocked by F-0002).

## Verdict

**VERIFIED.** All HO-0002 acceptance criteria met, with the two documentation nits
above named (neither changes any decision, tier verdict, or the F6 resolution).

## Date

2026-09-22

> A review never edits the original report — it lives here and is linked from the
> debate/report it concerns.

---

## Verification Block (kind: verification)

- **Work item verified:** W-0002 (round 4), owned by adversarial-reviewer.
- **Verified by:** verification-auditor, occupant 4 (not the owner; zero chat history).
- **Verdict:** VERIFIED.
- **Commands re-run by me (raw output retained under `research/context/`):**
  1. `python research/scripts/research.py validate` → **exit 0** (`va4_exit_validate.txt`):
     "Validation OK — statuses are in-vocabulary; the perft anchor and
     project_state.md consistency are verified; repo-root hygiene is respected";
     **0 problems**, warnings only (grandfathered legacy experiments + advisory audit
     lines). Captures: `va4_validate.txt`, `va4_validate2.txt`.
  2. `python research/scripts/research.py decisions` → **exit 0**; **DEC-0010 ACTIVE**
     (11 decisions listed; capture `va4_decisions.txt`).
  3. R-0009 status check: `research.py reviews` does NOT exist as a subcommand
     (usage error; capture `va4_reviews.txt`) — substituted with the record's own
     front-matter `status: COMPLETED` plus validate's in-vocabulary scan across all
     reviews. **R-0009 COMPLETED.**
  4. `python research/scripts/research.py debates` → **exit 0**; **D-0007 RESOLVED**
     (7 debates listed; capture `va4_debates.txt`).
  5. `python research/context/w0002_power.py` → **exit 0** (`va4_exit_power.txt`);
     output text-compare vs `w0002_power_output.txt`: **34/34 lines identical**
     (`va4_textcmp_out.txt`, TEXT-EQUAL; re-run output in `va4_power_rerun.txt`).
     A raw `fc /b` shows all-bytes-differ — a redirect-encoding artifact only (the
     committed file was written by a PowerShell redirect in UTF-16-LE; the
     cmd-redirected re-run is narrow-char); decoded line content is identical
     (`va4_textcmp.py` decodes both and compares).
  6. `git log --oneline -1 -- research/experiments/E-0010-...md` → **cb66bf8**
     (`va4_e0010_gitlog.txt`); `git merge-base --is-ancestor cb66bf8 dac1a3f` →
     exit 0 (**ANCESTOR_YES** — the last E-0010 commit predates the W-0002 session
     commit dac1a3f); `git status --short` empty (`va4_status.txt`).
     **E-0010 byte-identical to its pre-session state.**
  7. Gate 0 (exactly once, per the handoff): `build\Release\kana.exe` → no process
     started; capture reads "was blocked by your organization's Device Guard policy.
     Contact your support person for more info."
     (`research/context/bootstrap/gate0.txt`) — the F-0002 class block seen 2026-09-19
     / 09-20 / 09-21 and again today. (The shell wrapper's observable exit code was
     inconsistent across invocation paths; the binding fact — no engine execution,
     policy block message — was observed directly.)

- **acd8d0f judgment (required by HO-0002):** commit acd8d0f changed the `hygiene`
  command's keep-set classifier (`_hygiene_keep_names`, research.py L1198) used by the
  advisory repo-root debt report. I read `cmd_validate` (research.py L830–901): its
  hard root-hygiene gate is `root_hygiene_problems()` (L168), which checks ONLY
  `SANCTIONED_ROOT_FILES` + `root_grandfathered.txt` and never consults
  `_hygiene_keep_names`. The fix widens the *protective* keep-set of the advisory
  `hygiene` report and cannot dilute the validate gate. The four status checks
  (validate, DEC-0010, R-0009, D-0007) passed fairly.
- **Artifacts checked:** `research/context/w0002_power.py` + `w0002_power_output.txt`
  (re-run text-identical, item 5); E-0010 record (git-identical, item 6); D-0007 /
  DEC-0010 / R-0009 read in full.
- **What I reproduced independently** (own script `research/context/va4_rederive.py`,
  output `research/context/va4_rederive.txt`; 5 of 5 of HO-0002's re-derivation
  menu — three required):
  - **(a) k6 Elo:** 400*log10((144+30/2+1)/(66+30/2+1)) = 400*log10(160/82) =
    **116.1225** → record +116.1 ✓. N check 144+66+30=240 ✓; draw count 30 → 12.5%
    draw rate ✓ (EV-0001 pins the 240-game k6 dataset; EV-0010 pins the binary hash
    504EB01A…A6DAA).
  - **(b) per-rung sigma** = h*sqrt(N)/1.96 from the six recorded CI95s:
    k1 348.50 (record 349), k2 356.44 (356), k3 362.93 (363), k4 361.49 (361),
    k5 370.87 (371), k6 366.35 (366) — all match at stated rounding; max = 371 ✓.
    h(240) model = 1.96*370.87/sqrt(240) = **46.92** vs measured 46.35 → **1.23%**
    off (record: "within 1.2%") — within stated rounding ✓.
  - **(c) fixed-sample Ns** = (3.2898*sigma/delta)^2 at sigma=370.875:
    20-Elo **3,721.5** (record 3,722) ✓; 5-Elo **59,544.7** (record 59,545) ✓;
    >=150 vs true +160: **14,886.2** (record 14,886; 19.4 h at 769 g/h) ✓.
    Unwinnability: at true +116.1 the >=150 bar is short by 150-116.1 = 33.9 Elo →
    no finite N confirms it ✓ (the F6 core).
  - **(d) ASN values** (KL = zone^2/(2*sigma^2), A = ln 19 = 2.94444): Tier S
    ASN(H1) = 1,822.5 (record ~1,820/1,822) ✓; Tier R 29,159.4 (record 29,159/29,160)
    ✓; Tier M 291.6 (record ~292) ✓; auxiliary: midpoint S (d=15/5) ≈ 4,050 ✓;
    R at d=3.5 ≈ 81,000 (cap binds) ✓; M at true +116.1 ≈ 910 ✓; at +160 ≈ 231 ✓.
    H0-column convention nit as in Factual Errors 1 (records' 2,025/32,399/324 are
    ~11% conservative vs the symmetric-Wald 1,822.5/29,159.4/291.6 — same edicts).
  - **(e) E-0010 cumulative-LLR verdicts at N=240** (Elo space, sigma 371): Tier S
    +0.01543/game → **+3.70 > +2.944, H1 accepted** (crosses ~game 191) ✓; Tier R
    +0.00413/game → **+0.99, inside bounds** (crosses ~713) with the fixed-sample
    equivalent already decisive (CI95 lower bound +70.8 exceeds both +20 and +5) ✓;
    Tier M [100,150] −0.00324/game → **−0.78, inside bounds** (decides ~910) →
    ">=150 NOT ESTABLISHED at N=240" ✓. Score-space cross-check (q=0.6625,
    Var=0.19234) reproduces **+5.31 / +1.43 / −0.73 / +1.91** — same side of every
    bound, identical to the records' cross-check ✓. Throughput 1240/5807 s =
    768.7 games/hour (record 769) ✓.
- **What I could NOT reproduce (and why):** nothing within scope. The exact Gate-0
  exit code (4551 in F-0002's record) was not observable through this session's
  shell wrapper; the blocking event itself was (message captured, no process started).
- **Sample validity re-checked:** independence (0 duplicate move-lists across the
  1,240 games) and arm differentiation (ladder spread +36.3…+127.6) are E-0010-record
  properties verified twice already (R-0004, R-0008); W-0002 adds no new sample — its
  inputs are E-0010's tallies, which items (a)–(e) re-derive.
- **Claims that must be corrected in the record:** none blocking. The two nits
  (ASN(H0) convention; 1.23% vs "1.2%") are routed as documentation hygiene for the
  adversarial-reviewer seat (same class as R-0004/R-0008's nits — W-0006's bucket),
  to be addressed in NEW record addenda, never by editing the closed records.
- **Residual uncertainty (calibrated):** VERIFIED = demonstrated for the listed
  commands and arithmetic. The ASN model's accuracy against *realized* SPRT stopping
  times is deliberately NOT assessed here — that is W-0005's routed job; DEC-0010's
  reversal conditions cover it.

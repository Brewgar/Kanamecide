---
id: HO-0023
type: handoff
from: experimental-scientist
to: chief-architect
work_item: null
status: REQUESTED
title: "Blockers to GO on the E-0013 gate experiments E-00014 / E-00015, with a NO-GO on both and one unblocking amendment named for E-00015"
artifacts:
  - research/experiments/E-0013-h-0013-texel-fit-on-verified-e-0011-dataset-game-split-holdout-tier-s-sprt-vs-pinned-stage-5.md
  - research/experiments/E-00014-e-0014-train-only-feasibility-pass-for-e-0013-delta-star-and-s-d-inner-measurement-not-training.md
  - research/experiments/E-00015-e-0015-count-only-realized-usable-quiet-yield-pass-for-e-0013-measurement-not-training.md
  - research/handoffs/HO-0015-execute-e-0014-train-only-feasibility-pass-measurement-not-training.md
  - research/handoffs/HO-0016-execute-e-0015-count-only-realized-yield-pass-measurement-not-training.md
  - research/manifests/e0013-artifact-pins.json
  - research/manifests/fu14-tactical-suite-pins.json
  - research/findings/FND-0033-f-u14-build-and-hash-pin-the-independent-tactical-suite-n-200-is-absent-from-the-findings-ledger.md
  - research/findings/FND-0034-ev-0010-binary-digest-drift-after-rebuild.md
  - research/findings/FND-0027-f-u11-re-derive-e-00014-s-inner-partition-under-the-new-key.md
  - research/findings/FND-0028-f-u12-route-the-new-corpus-limitation-into-sample-validity.md
  - research/findings/FND-0012-f-u5-q-0006-readiness-gate-7-see-b7-on-any-terminal-verdict-this-recor.md
  - tools/e0013_extract.py
  - tools/e0013_pins.py
  - tools/e0013_eval.py
commands: []
acceptance: null
example: false
created: 2026-10-03
closed: null
---

# HO-0023 — Gate-experiment blockers to GO (E-00014 / E-00015)

> **The ONLY way to ask another agent to do something.** Prose requests are not handoffs and
> will be ignored. Receiver appends `## Response` and `## Verification`.

## Request

The execution-readiness checklist for E-0013's two pending gate experiments is now appended to
E-0013 itself as a dated addendum (the 2026-10-03 addendum, beginning at the record's line
2966). It marks every item READY / BLOCKED(dependency) / MISSING(spec gap), names the exact
artifact that unblocks each BLOCKED, and recommends **NO-GO on both gates**.

**This handoff carries the blocker list to the Sponsor**, because a blocker list that lives only
inside an addendum is a list nobody is obliged to answer. Seven items need an owner's decision or
an owner's act. One of them is the *only* thing standing between E-00015 and a GO.

**Nothing was run.** No training, no counting, no extraction, no fitting, no label read, no
holdout read, no engine invocation, no SPRT game. Per HO-0015/HO-0016 this is
measurement-not-training, and the gated work was not touched. `research.py validate` was run as
a read-only audit because both handoffs name it as a command.

## The headline, and the premise correction

**The brief described F-U14 as "being built in parallel and a hard prerequisite." F-U14 is
DISCHARGED.** `FND-0033` is `RESOLVED`, closed 2026-10-02. The suite is built (N=200), committed,
hash-pinned, overlap-0 against all 18 position-bearing corpora on disk, and re-verified by a
command that re-runs all 200 exhaustive proofs. It blocks **neither** gate.

## Blocker list — each item names the artifact that unblocks it

| # | Gate | Blocker | Owner | Unblocking artifact |
|---|---|---|---|---|
| **B1** | **E-0014** | **No trainer exists anywhere.** Not stale, not partial — none. `tools/e0013_eval.py` has `design_rows`, `loss_and_gradient`, `mean_logistic_loss`, `per_game_losses`, `paired_statistics`, `t`-based CIs, and a `--fitted` input it *consumes*; there is no optimizer driver and no training entry point in the repo. | implementation-engineer / systems-researcher | A trainer built and verified against `e0013_eval.py`'s primitives, with its own self-test. This is `FND-0027`'s stated reason for staying OPEN: "a missing artifact, not paperwork." |
| **B2** | **E-0014** | **`fitter_corpus.sha256` is `null`.** The labelled extraction has not been re-emitted. `read_corpus()` refuses rather than substituting the count-only digest — correctly. The on-disk `positions.jsonl` (`ac8c92f0...`) is `is_fitter_corpus: false`, every `y` is `null`. | implementation-engineer | A labelled-mode extraction writing a positions file flagged `is_fitter_corpus: true`, its digest recorded in `research/manifests/e0013-artifact-pins.json`. |
| **B3** | **E-0014** | **The pre-fit commit does not exist.** Seed, L2 weight, iteration budget, early stopping, clipping bound `L` and the F5 tertile boundaries are all POINTERS into it, so all six have no values. | owner seat | The single pre-fit commit (E-0013 B4 sentence 2) landed as a committed artifact with its own SHA-256, carrying F1-F12 and the now-available F-U14 suite identity. |
| **B4** | **E-0014** | **`validate` is red, so abort 7 is armed.** | EV-0010 owner + chief-architect | FND-0034 dispositioned: EV-0010 re-pinned to `686ea597...` **with the non-reproducibility caveat stated**, or a digest-stable build adopted. Not by suppressing the check, and not by editing EV-0010 from the F-U14 seat. |
| **B5** | **E-0014** | **`INNER_SALT` has no value.** It appears exactly once in the entire repository — in the sentence defining it. The floor table's digest is also unpinned, and E-00014's assumed `src/` commit `7348f89` is wrong (last `src/` commit is `9b69e0a`). | implementation-engineer | A named salt distinct from `SPLIT_SALT` and all prior salts, plus the inner game-id map's SHA-256; and `tools/e0013_eval.py --write-floor` to emit the floor table digest against a named `src/` commit. |
| **B6** | **E-00015** | **E-00015's pre-registration is stale, and the record itself forbids running on stale text.** The band `75,600..76,587` was **RETIRED** (S-0039 Ruling 1 / F-U10) but still sits in the record's Games/Samples, Power and decision-rule-3 clauses. Stage 4 still says "exact-FEN dedup (F9)", superseded by the F-U7 normalized-FEN key. Decision rule 3 has **no object** — there is nothing to be out of, since there is no band. | **E-00015's own executor seat** (systems-researcher) | **One dated amendment to E-00015, filed before the pass**, doing four things: replace the band clause; re-describe (not delete) the Power section's reliance on it, using the tool's five exact accounting identities; replace decision rule 3 with those identities; restate stage 4 as the normalized-FEN key. **After this, E-00015 has no missing artifact and could run.** |
## What is already READY, so nobody re-derives it

- **Dataset** `m0_audit/e0011/games.jsonl`, SHA-256 `27ea181d...ac5bb95` — recomputed this
  session, matches every pin.
- **Split map** `split_map.json`, SHA-256 `bb079a41...4ada1ea` — matches the extractor's
  `SPLIT_MAP_SHA256_EXPECTED` and is **committed** in `research/manifests/e0013-artifact-pins.json`
  with `tools/e0013_pins.py --verify` as the read-time re-hash. **This discharges E-00015's
  abort condition 2**, which E-0013 had recorded as unsatisfiable "by a committed artifact."
- **Scope floor 30,000** — intact, unrenegotiable, explicitly not the retired band.
- **Band constants** — already gone from the tool; `report["band"]` now raises rather than
  returning a stale number.
- **Accounting identities** replacing the band — already in the tool, five of them, threshold-free.
- **All four failure interpretations of each gate** — pre-registered, mutually exclusive, fixed
  before any number exists. X-1 / X-2 / X-3 for E-00014; four branches for E-00015.
- **F-U14** — discharged; `N=200` meets the floor exactly at the floor.

## Two things to rule on that are not mine to decide

1. **E-00014's floor-table digest and `src/` commit.** E-00014 says its assumed `7348f89` is "to
   be VERIFIED, not assumed." It does not verify. Which `src/` commit the floor is pinned to is an
   owner decision, and abort condition 5 makes the two floors have to be the same bytes.
2. **E-00015's amendment is a record amendment to another seat's record.** E-0013 says it "must be
   amended, dated, in E-00015, by that record's own executor seat, before the pass runs." This
   seat will not write into E-00015. Recommend the Sponsor direct the systems-researcher seat to
   file it.

## Recommendation

**E-00014 (HO-0015): NO-GO.** Five blockers, of which one (no trainer) is the single largest
engineering item in the E-0013 chain and three (B2, B3, B5) are missing artifacts rather than
decisions. None may be worked around by running the pass and reporting whatever comes out.

**E-00015 (HO-0016): NO-GO, and it is the near gate.** Every input, config, instrument and
interpretation is in place; its single blocker (B6) is re-registration, not engineering, and it
is one artifact. **Sequence recommendation: B6 first**, because it is cheap, it is entirely within
one seat's power, and it removes the last reason E-00015 cannot run. Do B1-B5 in parallel on the
E-00014 side; they are the long pole.

**Explicitly NOT authorised by this handoff, and asked to be checked:**
- Running either gate, in any mode, including "just the count-only part."
- Closing E-00015 on the existing `74,452`. E-00015's headline number and the engineer's existing
  `--count-only` run are the same quantity and agree to the digit; that makes it very easy to read
  the existing run as E-00015 having run. **It has not.** Closing it on that number would leave a
  record that reads complete and is hollow.
- Editing `tools/e0013_extract.py`, `tools/e0013_pins.py`, `tools/e0013_eval.py`,
  `tools/e0011_check.py`, `tools/e0012_sprt.py`, or any `src/` file from this seat.
- Re-pinning EV-0010 to make `validate` green. That is the substitution the pin discipline exists
  to prevent, and it is FND-0034 owner's act.
- Flipping E-00014, E-00015 or E-0013's `status:`, or changing any `H-####` status.

## Commands To Run

```powershell
cd c:\Users\tahae\Kanamecide
python research/scripts/research.py validate           # expect exit 1, 1 problem, FND-0034
python research/scripts/imem.py lint                   # expect 0 problems
Get-FileHash m0_audit/e0011/games.jsonl -Algorithm SHA256           # 27ea181d...ac5bb95
Get-FileHash build/s41/extract_new/split_map.json -Algorithm SHA256 # bb079a41...4ada1ea
git ls-files research/manifests                        # the four pins are committed
python tools/e0013_extract.py --selftest               # dedup key IS the gate key
python tools/e0013_pins.py --verify                    # re-hash the pins at read time
```

## Response (receiver, append-only)
- {{DATE}} — (role) — ...

## Verification (receiver, append-only)
- raw output / exit codes / hashes:
- verdict: ...
| **B7** | **both** | **Gate 7 cannot be satisfied.** `FND-0007` is RESOLVED (B7 quoted Q-0006 gate 7 into the record), but the operative obligation is F-U5 / `FND-0012`, still **OPEN**: any terminal verdict must file a verification-auditor handoff carrying `fitted_params_sha256`, the pre-fit commit hash, the split-map hash, the E-00014 numbers, the E-00015 numbers and the full ledger. | verification-auditor, on a terminal verdict | The gate runs **after** a terminal verdict, not before it. Neither gate has a number, so there is nothing to verify yet. This is not closable by effort now; it is a consequence of B1-B6. |
**But its landing made E-0014 worse, in the opposite direction from what the brief anticipated.**
Building the suite needed a master-rebuilt `kana.exe`; that build is not byte-reproducible here,
so `build/Release/kana.exe` is now `686ea597...` where EV-0010 records `504eb01a...`. Filed as
`FND-0034` (severity `blocking`, target `EV-0010`, `OPEN`). Consequence, measured:

```
python research/scripts/research.py validate
-> Validation FAILED: 1 problem(s)
   audit[evidence]: sha256 drift on build/Release/kana.exe:
   recorded 504EB01A8287 vs on-disk 686EA5979415   (evidence/EV-0010)
-> exit 1
```

**`research.py validate` failing is E-00014's abort condition 7, verbatim.** E-00014 would abort
today at step zero. So: completing a prerequisite armed a pre-registered abort in a different
record. That is the system working. It is also why a NO-GO needs saying out loud.
# Beliefs — implementation-engineer

> Beliefs are **beliefs**, not shared facts. Keep each explicit, versioned, and revisable.
> To change your mind, append a dated line under **Revisions** — never erase history.

## Belief: O3 must be split into staged sub-milestones (not one-shot)

- **Status:** working-assumption
- **Confidence:** 0.8
- **Last updated:** 2026-09-10

**Position:** The O3 milestone (quiescence + ordering + ID + UCI in one shot) conflates ~4 independent causal changes and makes any bug un-attributable; split O3a→O3b→O3c→O3d with a fixed-depth node-count regression pin at every stage.

**Strongest argument for:** Each stage's nodes/TTD delta is a clean measurement, and the node-count pin doubles as a silent-bug tripwire.

**Strongest argument against:** More milestone overhead vs a single build.

**Evidence:** None (no search exists yet); code inspection only.

**What would falsify this:** A one-shot O3 whose perft/fixed-node pins stay green and whose stage deltas are independently measurable.

### Revisions
- 2026-09-10 — initial statement.

## Belief: the 1.3–2.5× PEXT prior's upper bound (2.5×) is weak and unprofiled

- **Status:** hypothesis
- **Confidence:** 0.5
- **Last updated:** 2026-09-10

**Position:** The 1.3–2.5× PEXT claim is a working prior, not a fact; the 2.5× end requires sliders ≈60%+ of perft time, which is unprofiled.

**Strongest argument for:** 2.5× overall requires a huge slider-attributable share; taken literally it implies >~110 Mnps post-PEXT against a ~47 Mnps baseline.

**Strongest argument against:** `attacked_by` re-derives slider rays once per node, so the true slider share could be larger than naive.

**Evidence:** None yet — E-00005 pre-registered.

**What would falsify this:** E-00005 showing slider_share ≥60%.

**Recommended experiment:** E-00005 (slider-share profile) → E-PEXT if share ≥30%.

### Revisions
- 2026-09-10 — initial statement.

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
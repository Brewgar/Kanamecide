---
id: DEC-0013
type: decision
title: "Evidence pins are content-addressed archived artifacts; live build outputs are never pin targets"
status: ACTIVE
superseded_by: null
amends: []
evidence: [FND-0034, EV-0010, EV-0011]
example: false
created: 2026-10-03
---

# DEC-0013 — Evidence pins are content-addressed archived artifacts

## Decision

Every binary evidence record (EV-####, `kind: binary`) MUST pin a **content-addressed archived
artifact**, not a live build output. Concretely:

1. **`path:` must resolve to a git-tracked, per-subject archived copy of the artifact**
   (convention est. 2026-10-03: `_obs/evidence/<EV-ID>__<name>_<shaprefix>.exe`, added to git
   despite `_obs/` being globally ignored — the archived subset is tracked by exception).
2. **A live build output (`build/Release/kana.exe` etc.) is never a pin target.** It is an
   untracked local artifact (`E6` in FND-0034's evidence), so a digest bound to it can drift
   without any commit — the precise FND-0034 failure mode.
3. **One EV id per binary subject epoch.** A rebuild that is to be measured or evidenced is a
   **pin event**: archive the bytes first, then file a NEW EV record with its own `sha256`,
   `regenerate:` and `cites`. Old EV records are never re-pinned to newer subjects;
   supersession is expressed by the new record, not by editing the old digest.
4. **Repairs that drift a pinned digest are findings (file an FND), not silent rebuilds.** The
   digest of an archived artifact may be moved only by a dated disposition on the record that
   owns the pin, with the reason and the new content hash stated aloud.
5. **`regenerate:` text on a binary pin names the toolchain caveat honestly.** Until W-0009 /
   HO-0024 deliver a digest-stable build (`/Brepro` or equivalent), every binary pin is a content
   address of a preserved copy, and the record says so.

## Context

FND-0034 (2026-10-02) is the symptom that forced this decision: EV-0010's pinned digest
(`504EB01A…`) was bound to the live `build/Release/kana.exe`; the MSVC toolchain is not
byte-reproducible on this host; two rebuilds later neither surviving artifact matched the record,
and the original pinned bytes are unrecoverable. The FND-0035 F2/F3 repair (`dd4051a`) then filed
EV-0011 bound to the SAME live path — making EV-0010 and EV-0011 structurally unsatisfiable at
once, and leaving EV-0011 itself one rebuild away from drift. Sponsor Ruling 1 (staged
`_obs/rulingpkg/`, 2026-10-03) ruled option (a): re-pin EV-0010 to the preserved epoch-source
binary `686EA597…` with an explicit non-reproducibility caveat, + digest-stable-build follow-up
(W-0009 / HO-0024). The ruling package's pin-settling order ("disposition → repairs → new EV")
was executed INVERTED (repairs first); this decision retrofits the invariant the order was
meant to protect so that no future order dependency exists.

**Autonomous adjudication.** Recorded under delegated autonomous execution (current director
instruction, §3/seat H): the two active conflicts the Sponsor's staged ruling left open —
(a) the `path:` re-point to a tracked archive (deviation from the staged text, which had
assumed disposition-before-repair), and (b) the decision that archived copies are tracked by
exception inside the otherwise-ignored `_obs/` — are resolved by this decision with their
rationale stated; they are reversible (repin/addendum machinery) and recorded openly.

## Consequences

- `validate`'s existing evidence check (`research.py` hashing `path:` against `sha256:`) becomes
  a *portable* contract: it is checkable on a fresh clone because the artifact is tracked.
- Repo size: the archive subset is bounded to binaries that evidence records actually pin
  (today: 2 Release binaries, ~243 KB). Audit-config binaries (549 KB class) remain local.
- Future feature work that rebuilds the engine between two annotations does NOT invalidate any
  EV record, as long as the pin-event protocol above is observed.
- Digest-stable builds (W-0009) convert pins from "preserved copy" to "reproducible from source";
  when they land, `regenerate:` texts gain the reproducible recipe and the caveat is retired by
  addendum, not by rewrite.

## Alternatives Considered

- **Keep live-path pins; re-pin on every rebuild.** Rejected — this *is* the drift cycle; it made
  FND-0034, and a third rebuild would have broken EV-0011 identically.
- **Track binaries under `research/` instead of `_obs/evidence/`.** Rejected today — `research/` is
  the canonical record store with its own hygiene gates; binary payloads belong to the observation
  layer. The tracked-by-exception convention gives the same clone-portability with less gate
  churn. Reversible: if the convention proves confusing, the archive moves by a later decision.
- **Commit to digest-stable builds BEFORE disposing of FND-0034** (staged A2's option (b)).
  Rejected for this disposition only — the epoch binary was unrecoverable, so only a preserved
  artifact could close the loop without erasing history. The follow-up stands.
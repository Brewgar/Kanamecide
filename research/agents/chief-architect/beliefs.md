# Beliefs — chief-architect

> Beliefs are **beliefs**, not facts: kept explicit, versioned, revisable.
> To change your mind, append a dated line under **Revisions** — never erase history.
> Use `Status` values: hypothesis, working-assumption, supported-by-evidence,
> rejected, superseded.

## Belief: memory discipline is the transferable asset

- **Status:** supported-by-evidence
- **Confidence:** 0.8
- **Last updated:** 2026-10-02

**Position:** The project gets smarter to the extent that today's experiments, reviews
and failures reduce tomorrow's search space; every tool worth building (anchors,
pinned evidence, claim direction, findings, freshness/novelty, promotion lane) turns a
memory of being right about something into a weapon against being wrong twice.

**Strongest argument for:** The E-0013 saga sits in the records *because* the process
was documented: R-0019 → blocking findings → repair sessions → re-critique rules
→ the run-flip authorisation → the leakage ruling → verification — the evidence chain,
not the project tune, is what survives. Verifyable claims, not code, are what
compounds.

**Strongest argument against:** Instrumental gatekeeping is its own cost; the round
already spends more bytes reviewing the same record than learning from it, and the
current state still blocks W-0003 on who-verifies-whom bookkeeping rather than on
science. The freshness surface exists to push against that exact drift.

**Evidence:** R-0003..R-0026 (the audit chain itself), S-0041/S-0042 (ledger closure
owner/auditor division), `imem.py lint` green after the FND-0030 repair, and today's
projection regeneration on the live store.

**What would falsify this:** a measured round where the ledger machinery conflicts
with the experiments two rounds in a row (the DEC-0012 reversal clause) — relax it by
decision record, not by silence.

**Recommended experiment:** the end-to-end E-0013 fitting path with one recorded
replication of every artifact hash; not before F-U14 lands.

### Revisions
- 2026-10-02 — initial statement (creation of the seat under W-0007 committed
  commitments; independent verification is HO-0021's to write).

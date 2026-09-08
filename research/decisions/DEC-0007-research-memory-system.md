---
id: DEC-0007
type: decision
title: "Repository-based multi-agent research memory system"
status: ACTIVE
superseded_by: null
example: false
created: 2026-09-08
---

# DEC-0007 — Repository-based multi-agent research memory system

## Decision
Research memory lives in a `research/` directory of Markdown records (with YAML front-matter)
plus a stdlib-only Python CLI, separating FACTS / BELIEFS / HYPOTHESES / DISAGREEMENTS /
DECISIONS / EXPERIMENTS / FAILURES into distinct directories.

## Context
Multiple independent AI agents will work on the project over a long period, and a future
agent must be able to reconstruct what was believed, argued, tested, and decided.

## Alternatives Considered
- A web app / database (overkill, harder for humans, harder to preserve in Git).
- A single wiki/Notion workspace (not revisioned, harder for Cline agents to script).
- Unstructured notes (no machine-readable status/index).

## Arguments
- Plain Markdown + YAML is human-readable, Git-friendly, and easy for Cline agents to read/write.
- Strict directory separation prevents opinions from becoming "facts" by accident.
- A small script provides summaries, scaffolding, validation, and focused context packs.

## Evidence
The requirements in this project brief; the existing repo already uses Markdown (README.md).

## Agents Involved
System author (seeded the system and the four role agents: researcher-architect,
systems-researcher, adversarial-reviewer, implementation-engineer).

## Why This Was Chosen
Simplicity, robustness, model-independence, and Git-friendliness outweigh the convenience
of a database or external tool.

## Reversal Conditions
Only if the project grows to a scale (hundreds of agents, high-frequency experiments) where
a structured database becomes genuinely necessary; even then, the Markdown records would
remain the canonical human-facing export.

## Date
2026-09-08
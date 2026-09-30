"""
Kanamecide Research System - Schema and Core Epistemic Types (v3.0.0).

Normative epistemic ontology for the long-term chess engine research organization.
Preserves Layer 0 (Raw Evidence) through Layer 6 (Meta-Memory).
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set


class EpistemicStatus(str, enum.Enum):
    """Rigorous epistemic status of claims, beliefs, and hypotheses."""
    OBSERVATION = "observation"          # Direct uninterpreted measurement
    FACT = "fact"                        # Verified invariant (e.g. perft counts)
    CONJECTURE = "conjecture"            # Plausible intuition, zero formal support
    HYPOTHESIS = "hypothesis"            # Testable claim with explicit falsification conditions
    THEOREM = "theorem"                  # Mathematically derived/proven statement
    HEURISTIC = "heuristic"              # Rule-of-thumb applied in search/eval
    EMPIRICAL_CORRELATION = "empirical_correlation"  # Statistical association without proven causality
    CAUSAL_CLAIM = "causal_claim"        # Verified causal mechanism (e.g. isolated parameter delta)
    DECISION = "decision"                # Accepted engineering/architectural choice
    REJECTED = "rejected"                # Falsified hypothesis or failed approach
    SUPERSEDED = "superseded"            # Outdated belief replaced by stronger evidence
    UNRESOLVED = "unresolved"            # Active contradiction or open inquiry


class ConfidenceLevel(str, enum.Enum):
    """Calibrated confidence bands - confidence is a property of evidence, not truth."""
    SPECULATIVE = "speculative"          # < 0.30 - intuition, anecdotal
    PLAUSIBLE = "plausible"              # 0.30 .. 0.54 - weak theoretical or empirical backing
    LIKELY = "likely"                    # 0.55 .. 0.74 - moderate evidence, not independently verified
    STRONGLY_SUPPORTED = "strongly_supported"  # 0.75 .. 0.89 - robust multi-seed/statistical confirmation
    EXPERIMENTALLY_VALIDATED = "experimentally_validated"  # >= 0.90 - passed pre-registered SPRT / reproducible
    MATHEMATICALLY_PROVEN = "mathematically_proven"        # Formal proof / symbolic derivation holds


class RelationKind(str, enum.Enum):
    """Typed semantic edges in the institutional knowledge graph."""
    TESTS = "tests"                      # Experiment tests Hypothesis
    SUPPORTS = "supports"                # Evidence/Result supports Claim/Hypothesis
    CONTRADICTS = "contradicts"          # Claim A contradicts Claim B
    FALSIFIES = "falsifies"              # Experiment falsifies Hypothesis
    DEPENDS_ON = "depends_on"            # Idea A requires B to be true/present
    IMPLEMENTS = "implements"            # Code/Commit implements Idea/Decision
    SUPERSEDES = "supersedes"            # Decision/Claim A replaces Decision/Claim B
    DERIVED_FROM = "derived_from"        # Formulation A derived from B
    GENERALIZES = "generalizes"          # Theory A generalizes Case B
    SPECIALIZES = "specializes"          # Case A specializes Theory B
    REPRODUCES = "reproduces"            # Run B independently reproduces Run A
    REVISIT_WHEN = "revisit_when"        # Idea A should be re-evaluated when condition C holds
    ANSWERS = "answers"                  # Hypothesis/Evidence answers Question
    BLOCKED_BY = "blocked_by"            # Work item or decision blocked by event
    TOUCHES_CODE = "touches_code"        # Record directly modifies/analyzes code symbol


@dataclass
class EpistemicProvenance:
    """End-to-end audit trail for every piece of accumulated knowledge."""
    originating_agent: str
    originating_task: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_commit: str = "unknown"
    binary_sha256: Optional[str] = None
    input_artifacts: List[str] = field(default_factory=list)
    output_artifacts: List[str] = field(default_factory=list)
    reproduction_command: Optional[str] = None
    verification_agent: Optional[str] = None
    verification_review_id: Optional[str] = None


@dataclass
class ResearchRecord:
    """Universal schema for any node in the scientific research memory."""
    id: str                              # Unique ID (e.g., H-0013, E-0010, Q-0001, DEC-0010)
    kind: str                            # hypothesis, experiment, decision, question, etc.
    title: str                           # Concise descriptive title
    status: str                          # Lifecycle state (OPEN, COMPLETED, ACTIVE, etc.)
    epistemic_status: EpistemicStatus = EpistemicStatus.HYPOTHESIS
    confidence: float = 0.5              # Numerical confidence 0.0 .. 1.0
    confidence_band: ConfidenceLevel = ConfidenceLevel.PLAUSIBLE
    summary: str = ""
    body: str = ""
    tags: List[str] = field(default_factory=list)
    affected_subsystems: List[str] = field(default_factory=list) # e.g. search, eval, movegen, tt
    provenance: Optional[EpistemicProvenance] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    revisit_when: Optional[str] = None  # Condition triggering revival of old idea
    file_path: Optional[str] = None     # Absolute or relative disk path

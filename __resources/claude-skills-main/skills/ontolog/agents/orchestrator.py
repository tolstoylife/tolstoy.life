"""
Orchestrator Agent
==================

Query → Holon

Coordinates the full pipeline:
    Encode → Topology → Resolve → Target → Validate → Synthesize

Supports consensus voting and effort scaling.
"""

from __future__ import annotations
from typing import Set, List, Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
import dspy

from .types import (
    Base, Terminal, Operation, SimplicialComplex, PersistenceDiagram,
    Holon, Query, Scope, ScopeLevel, Metrics, ValidationResult,
    AgentState, AgentResult
)

from .encoder import Encoder, encode
from .topologist import Topologist, analyze_topology
from .resolver import Resolver, resolve_operations
from .targeter import Targeter, target_terminals
from .validator import Validator, validate
from .synthesizer import Synthesizer, synthesize, CompactFormatter


# =============================================================================
# CONFIGURATION
# =============================================================================

class EffortLevel(Enum):
    SIMPLE = 1
    MODERATE = 2
    COMPLEX = 3


@dataclass
class OrchestratorConfig:
    """Configuration for orchestration."""
    # Consensus voting
    consensus_agents: int = 3
    consensus_threshold: float = 0.67
    
    # Effort scaling
    effort_level: EffortLevel = EffortLevel.MODERATE
    
    # Validation
    validate: bool = True
    strict_validation: bool = False
    
    # Decomposition
    decompose_holons: bool = True
    min_decompose_size: int = 3


# =============================================================================
# EFFORT CLASSIFICATION
# =============================================================================

def classify_effort(query_text: str) -> EffortLevel:
    """
    Classify query complexity.
    
    SIMPLE: Short, single-concept queries
    MODERATE: Multi-concept, standard analysis
    COMPLEX: Deep analysis, many entities
    """
    word_count = len(query_text.split())
    
    if word_count <= 5:
        return EffortLevel.SIMPLE
    elif word_count <= 20:
        return EffortLevel.MODERATE
    else:
        return EffortLevel.COMPLEX


# =============================================================================
# PIPELINE BUILDER
# =============================================================================

class PipelineBuilder:
    """
    Fluent API for building execution pipelines.
    
    Usage:
        result = (PipelineBuilder()
            .with_encoder(encoder)
            .with_topologist(topologist)
            .with_resolver(resolver)
            .with_targeter(targeter)
            .with_validator(validator)
            .with_synthesizer(synthesizer)
            .execute(query_text))
    """
    
    def __init__(self):
        self.encoder: Optional[Encoder] = None
        self.topologist: Optional[Topologist] = None
        self.resolver: Optional[Resolver] = None
        self.targeter: Optional[Targeter] = None
        self.validator: Optional[Validator] = None
        self.synthesizer: Optional[Synthesizer] = None
        self.config: OrchestratorConfig = OrchestratorConfig()
    
    def with_encoder(self, encoder: Encoder) -> PipelineBuilder:
        self.encoder = encoder
        return self
    
    def with_topologist(self, topologist: Topologist) -> PipelineBuilder:
        self.topologist = topologist
        return self
    
    def with_resolver(self, resolver: Resolver) -> PipelineBuilder:
        self.resolver = resolver
        return self
    
    def with_targeter(self, targeter: Targeter) -> PipelineBuilder:
        self.targeter = targeter
        return self
    
    def with_validator(self, validator: Validator) -> PipelineBuilder:
        self.validator = validator
        return self
    
    def with_synthesizer(self, synthesizer: Synthesizer) -> PipelineBuilder:
        self.synthesizer = synthesizer
        return self
    
    def with_config(self, config: OrchestratorConfig) -> PipelineBuilder:
        self.config = config
        return self
    
    def execute(self, query_text: str, context: str = "") -> AgentResult:
        """Execute the pipeline."""
        # Initialize agents if not provided
        encoder = self.encoder or Encoder()
        topologist = self.topologist or Topologist()
        resolver = self.resolver or Resolver()
        targeter = self.targeter or Targeter()
        validator = self.validator or Validator()
        synthesizer = self.synthesizer or Synthesizer()
        
        # Phase 1: ENCODE
        result = encoder.forward(query_text, context)
        if not result.success:
            return result
        state = result.state
        
        # Phase 2: TOPOLOGY
        result = topologist.forward(state)
        if not result.success:
            return result
        state = result.state
        
        # Phase 3: RESOLVE
        result = resolver.forward(state)
        if not result.success:
            return result
        state = result.state
        
        # Phase 4: TARGET
        result = targeter.forward(state)
        if not result.success:
            return result
        state = result.state
        
        # Phase 5: VALIDATE
        if self.config.validate:
            result = validator.forward(state)
            if not result.success:
                return result
            state = result.state
        
        # Phase 6: SYNTHESIZE
        result = synthesizer.forward(state)
        
        return result


# =============================================================================
# ORCHESTRATOR
# =============================================================================

class Orchestrator(dspy.Module):
    """
    Lead coordinator for OntoLog pipeline.
    
    Implements:
        - Effort scaling (SIMPLE/MODERATE/COMPLEX)
        - Consensus voting (MAKER pattern)
        - Pipeline coordination
    """
    
    def __init__(self, config: OrchestratorConfig = None):
        super().__init__()
        self.config = config or OrchestratorConfig()
        
        # Initialize agents
        self.encoder = Encoder()
        self.topologist = Topologist()
        self.resolver = Resolver()
        self.targeter = Targeter()
        self.validator = Validator()
        self.synthesizer = Synthesizer(decompose=self.config.decompose_holons)
    
    def forward(
        self,
        query_text: str,
        context: str = "",
        known_vertices: Set[str] = None
    ) -> AgentResult:
        """
        Execute full OntoLog pipeline.
        
        λ-calculus: Query → encode(Σ) → topology(dgm) → resolve(λ) → target(τ) → synthesize(H)
        
        Args:
            query_text: Natural language query
            context: Additional context
            known_vertices: Pre-defined vertex identifiers
        
        Returns:
            AgentResult containing Holon
        """
        traces = []
        
        # Classify effort
        effort = classify_effort(query_text)
        self.config.effort_level = effort
        traces.append(f"Effort: {effort.name}")
        
        # Configure encoder with known vertices
        if known_vertices:
            self.encoder = self.encoder.with_vertices(known_vertices)
        
        # Execute pipeline
        pipeline = (PipelineBuilder()
            .with_encoder(self.encoder)
            .with_topologist(self.topologist)
            .with_resolver(self.resolver)
            .with_targeter(self.targeter)
            .with_validator(self.validator)
            .with_synthesizer(self.synthesizer)
            .with_config(self.config))
        
        result = pipeline.execute(query_text, context)
        
        # Append orchestration trace
        result.trace = " | ".join(traces) + " | " + result.trace
        
        return result
    
    def forward_with_consensus(
        self,
        query_text: str,
        context: str = "",
        m: int = None,
        k_threshold: float = None
    ) -> AgentResult:
        """
        Execute with consensus voting (MAKER pattern).
        
        Runs m parallel agents, requires k agreement.
        
        Args:
            query_text: Natural language query
            context: Additional context
            m: Number of agents (default from config)
            k_threshold: Agreement threshold (default from config)
        
        Returns:
            AgentResult with consensus holon
        """
        m = m or self.config.consensus_agents
        k = k_threshold or self.config.consensus_threshold
        
        # Run multiple executions
        results = []
        for i in range(m):
            result = self.forward(query_text, context)
            if result.success:
                results.append(result)
        
        # Check consensus
        if len(results) / m >= k:
            # Return first successful result
            # (In full implementation, would merge/vote on holons)
            return results[0]
        else:
            # Consensus failed
            state = AgentState()
            state.errors.append(f"Consensus failed: {len(results)}/{m} successful")
            return AgentResult(
                success=False,
                state=state,
                trace=f"Consensus: {len(results)}/{m} < {k}"
            )


# =============================================================================
# FUNCTIONAL INTERFACE
# =============================================================================

def execute_ontolog(
    query_text: str,
    context: str = "",
    known_vertices: Set[str] = None,
    config: OrchestratorConfig = None
) -> Holon:
    """
    Functional interface for OntoLog execution.
    
    Universal form: λο.τ where
        ο = query (base)
        λ = pipeline (operation)
        τ = holon (terminal)
    
    Args:
        query_text: Natural language query
        context: Additional context
        known_vertices: Pre-defined vertex identifiers
        config: Orchestration configuration
    
    Returns:
        Holon structure
    
    Raises:
        ValueError: If pipeline fails
    """
    orchestrator = Orchestrator(config)
    result = orchestrator.forward(query_text, context, known_vertices)
    
    if not result.success:
        raise ValueError(f"OntoLog execution failed: {result.state.errors}")
    
    return result.state.holon


def execute_ontolog_verbose(
    query_text: str,
    context: str = "",
    known_vertices: Set[str] = None,
    config: OrchestratorConfig = None
) -> Dict[str, Any]:
    """
    Verbose execution returning full state.
    
    Args:
        query_text: Natural language query
        context: Additional context
        known_vertices: Pre-defined vertex identifiers
        config: Orchestration configuration
    
    Returns:
        Dict with holon, metrics, trace, etc.
    """
    orchestrator = Orchestrator(config)
    result = orchestrator.forward(query_text, context, known_vertices)
    
    return {
        "success": result.success,
        "holon": result.state.holon,
        "query": result.state.query,
        "complex": result.state.complex,
        "operations": result.state.operations,
        "terminals": result.state.terminals,
        "diagram": result.state.diagram,
        "metrics": result.state.metrics,
        "errors": result.state.errors,
        "trace": result.trace
    }

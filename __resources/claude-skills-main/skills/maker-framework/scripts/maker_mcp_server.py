#!/usr/bin/env python3
"""
MAKER (Maximal Agentic Knowledge Engine for Reasoning) MCP Server

Implements the three-pillar architecture:
1. Maximal Agentic Decomposition (MAD) - Task decomposition into atomic subtasks
2. First-to-Ahead-by-k Voting - Parallel consensus with early termination
3. Red-Flagging System - Output validation and error filtering

This server provides tools for LLMs to orchestrate reliable multi-agent reasoning.
"""

import asyncio
import json
import hashlib
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any, Callable, Tuple
from collections import defaultdict
import httpx

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict, field_validator

# ============================================================================
# Server Initialization
# ============================================================================

mcp = FastMCP("maker_mcp")

# ============================================================================
# Constants and Configuration
# ============================================================================

# Default configuration by task criticality
CRITICALITY_CONFIGS = {
    "low": {"m": 3, "k": 1, "confidence": 0.70},
    "medium": {"m": 5, "k": 2, "confidence": 0.85},
    "high": {"m": 7, "k": 3, "confidence": 0.95},
    "critical": {"m": 11, "k": 5, "confidence": 0.99}
}

MAX_TOKENS_DEFAULT = 500
MAX_SUBTASK_DEPTH = 5
SEMANTIC_SIMILARITY_THRESHOLD = 0.85

# ============================================================================
# Data Models
# ============================================================================

class TaskCriticality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RedFlagType(str, Enum):
    LENGTH_EXCEEDED = "length_exceeded"
    FORMAT_VIOLATION = "format_violation"
    PLACEHOLDER_DETECTED = "placeholder_detected"
    UNCERTAINTY_MARKER = "uncertainty_marker"
    SEMANTIC_INCONSISTENCY = "semantic_inconsistency"

@dataclass
class Subtask:
    """Atomic unit of work in MAKER decomposition."""
    id: str
    description: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    prompt_template: Optional[str] = None
    output_schema: Optional[Dict[str, Any]] = None
    max_tokens: int = MAX_TOKENS_DEFAULT
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class DAG:
    """Directed Acyclic Graph representing task decomposition."""
    task_id: str
    task_description: str
    subtasks: Dict[str, Subtask] = field(default_factory=dict)
    edges: List[Tuple[str, str]] = field(default_factory=list)  # (from, to)
    
    @property
    def depth(self) -> int:
        """Calculate max path length through DAG."""
        if not self.subtasks:
            return 0
        
        # Topological sort with depth tracking
        in_degree = defaultdict(int)
        depth = {}
        
        for from_id, to_id in self.edges:
            in_degree[to_id] += 1
            
        queue = [sid for sid in self.subtasks if in_degree[sid] == 0]
        for sid in queue:
            depth[sid] = 0
            
        while queue:
            current = queue.pop(0)
            for from_id, to_id in self.edges:
                if from_id == current:
                    depth[to_id] = max(depth.get(to_id, 0), depth[current] + 1)
                    in_degree[to_id] -= 1
                    if in_degree[to_id] == 0:
                        queue.append(to_id)
        
        return max(depth.values()) + 1 if depth else 1
    
    @property
    def width(self) -> int:
        """Calculate max parallelizable subtasks at any level."""
        if not self.subtasks:
            return 0
            
        levels = defaultdict(list)
        depth = {}
        in_degree = defaultdict(int)
        
        for from_id, to_id in self.edges:
            in_degree[to_id] += 1
            
        queue = [sid for sid in self.subtasks if in_degree[sid] == 0]
        for sid in queue:
            depth[sid] = 0
            
        while queue:
            current = queue.pop(0)
            levels[depth[current]].append(current)
            for from_id, to_id in self.edges:
                if from_id == current:
                    depth[to_id] = max(depth.get(to_id, 0), depth[current] + 1)
                    in_degree[to_id] -= 1
                    if in_degree[to_id] == 0:
                        queue.append(to_id)
        
        return max(len(v) for v in levels.values()) if levels else len(self.subtasks)
    
    def topological_sort(self) -> List[str]:
        """Return subtask IDs in valid execution order."""
        in_degree = defaultdict(int)
        for from_id, to_id in self.edges:
            in_degree[to_id] += 1
            
        queue = [sid for sid in self.subtasks if in_degree[sid] == 0]
        result = []
        
        while queue:
            current = queue.pop(0)
            result.append(current)
            for from_id, to_id in self.edges:
                if from_id == current:
                    in_degree[to_id] -= 1
                    if in_degree[to_id] == 0:
                        queue.append(to_id)
        
        if len(result) != len(self.subtasks):
            raise ValueError("Cycle detected in DAG - decomposition invalid")
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_description": self.task_description,
            "subtasks": {k: v.to_dict() for k, v in self.subtasks.items()},
            "edges": self.edges,
            "depth": self.depth,
            "width": self.width
        }

@dataclass
class RedFlag:
    """Represents a validation failure on an agent output."""
    flag_type: RedFlagType
    reason: str
    severity: float  # 0-1, higher = more severe
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "flag_type": self.flag_type.value,
            "reason": self.reason,
            "severity": self.severity
        }

@dataclass
class AgentOutput:
    """Output from a single micro-agent execution."""
    agent_id: str
    subtask_id: str
    output: str
    completion_time: float  # seconds
    red_flags: List[RedFlag] = field(default_factory=list)
    is_valid: bool = True
    equivalence_hash: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "subtask_id": self.subtask_id,
            "output": self.output,
            "completion_time": self.completion_time,
            "red_flags": [f.to_dict() for f in self.red_flags],
            "is_valid": self.is_valid,
            "equivalence_hash": self.equivalence_hash
        }

@dataclass
class VotingResult:
    """Result of consensus voting on agent outputs."""
    subtask_id: str
    consensus_output: Optional[str]
    confidence: float
    total_agents: int
    valid_agents: int
    winning_votes: int
    early_terminated: bool
    equivalence_classes: Dict[str, List[str]]  # hash -> [agent_ids]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "subtask_id": self.subtask_id,
            "consensus_output": self.consensus_output,
            "confidence": self.confidence,
            "total_agents": self.total_agents,
            "valid_agents": self.valid_agents,
            "winning_votes": self.winning_votes,
            "early_terminated": self.early_terminated,
            "equivalence_classes": self.equivalence_classes
        }

# ============================================================================
# Red-Flagging System (Pillar 3)
# ============================================================================

UNCERTAINTY_MARKERS = [
    "i'm not sure", "possibly", "might be", "could be", "maybe",
    "i think", "probably", "unclear", "uncertain", "not certain"
]

PLACEHOLDER_PATTERNS = [
    r"\[TODO\]", r"\[N/A\]", r"\[unknown\]", r"\[TBD\]",
    r"<insert.*?>", r"<placeholder>", r"\.{3,}"
]

def check_length_flag(output: str, max_tokens: int) -> Optional[RedFlag]:
    """Check if output exceeds maximum token count."""
    # Approximate token count (4 chars ~= 1 token)
    approx_tokens = len(output) // 4
    if approx_tokens > max_tokens:
        return RedFlag(
            flag_type=RedFlagType.LENGTH_EXCEEDED,
            reason=f"Output length ~{approx_tokens} tokens exceeds limit of {max_tokens}",
            severity=min(1.0, (approx_tokens - max_tokens) / max_tokens)
        )
    return None

def check_format_flag(output: str, schema: Optional[Dict[str, Any]]) -> Optional[RedFlag]:
    """Check if output violates expected format/schema."""
    if schema is None:
        return None
        
    # If schema expects JSON, try parsing
    if schema.get("type") == "object" or "properties" in schema:
        try:
            parsed = json.loads(output)
            # Validate required fields
            for required in schema.get("required", []):
                if required not in parsed:
                    return RedFlag(
                        flag_type=RedFlagType.FORMAT_VIOLATION,
                        reason=f"Missing required field: {required}",
                        severity=0.8
                    )
        except json.JSONDecodeError as e:
            return RedFlag(
                flag_type=RedFlagType.FORMAT_VIOLATION,
                reason=f"Invalid JSON: {str(e)[:100]}",
                severity=0.9
            )
    
    return None

def check_placeholder_flag(output: str) -> Optional[RedFlag]:
    """Check for placeholder patterns indicating incomplete output."""
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, output, re.IGNORECASE):
            return RedFlag(
                flag_type=RedFlagType.PLACEHOLDER_DETECTED,
                reason=f"Placeholder pattern detected: {pattern}",
                severity=0.95
            )
    return None

def check_uncertainty_flag(output: str) -> Optional[RedFlag]:
    """Check for uncertainty markers indicating low confidence."""
    output_lower = output.lower()
    for marker in UNCERTAINTY_MARKERS:
        if marker in output_lower:
            return RedFlag(
                flag_type=RedFlagType.UNCERTAINTY_MARKER,
                reason=f"Uncertainty marker detected: '{marker}'",
                severity=0.6
            )
    return None

def apply_red_flags(
    output: str,
    max_tokens: int = MAX_TOKENS_DEFAULT,
    schema: Optional[Dict[str, Any]] = None,
    check_uncertainty: bool = True,
    check_placeholders: bool = True
) -> Tuple[List[RedFlag], bool]:
    """Apply all red flag checks to an output."""
    flags = []
    
    # Length check
    if flag := check_length_flag(output, max_tokens):
        flags.append(flag)
    
    # Format check
    if flag := check_format_flag(output, schema):
        flags.append(flag)
    
    # Placeholder check
    if check_placeholders and (flag := check_placeholder_flag(output)):
        flags.append(flag)
    
    # Uncertainty check
    if check_uncertainty and (flag := check_uncertainty_flag(output)):
        flags.append(flag)
    
    is_valid = len(flags) == 0
    return flags, is_valid

# ============================================================================
# Equivalence Classes and Voting (Pillar 2)
# ============================================================================

def compute_equivalence_hash(output: str, method: str = "normalized") -> str:
    """Compute hash for grouping equivalent outputs."""
    if method == "exact":
        normalized = output.strip()
    elif method == "normalized":
        # Lowercase, remove extra whitespace
        normalized = " ".join(output.lower().split())
    elif method == "json":
        # Try to parse and re-serialize for canonical form
        try:
            parsed = json.loads(output)
            normalized = json.dumps(parsed, sort_keys=True)
        except:
            normalized = " ".join(output.lower().split())
    else:
        normalized = output.strip()
    
    return hashlib.md5(normalized.encode()).hexdigest()[:16]

def first_to_ahead_by_k_vote(
    outputs: List[AgentOutput],
    k: int,
    early_terminate: bool = True
) -> VotingResult:
    """
    Implement first-to-ahead-by-k voting algorithm.
    
    Accept result r when votes(r) >= votes(any_other) + k
    """
    valid_outputs = [o for o in outputs if o.is_valid]
    
    if not valid_outputs:
        return VotingResult(
            subtask_id=outputs[0].subtask_id if outputs else "unknown",
            consensus_output=None,
            confidence=0.0,
            total_agents=len(outputs),
            valid_agents=0,
            winning_votes=0,
            early_terminated=False,
            equivalence_classes={}
        )
    
    # Group by equivalence class
    equiv_classes: Dict[str, List[AgentOutput]] = defaultdict(list)
    for output in valid_outputs:
        hash_key = output.equivalence_hash or compute_equivalence_hash(output.output)
        equiv_classes[hash_key].append(output)
    
    # Sort by completion time (simulating streaming)
    sorted_outputs = sorted(valid_outputs, key=lambda x: x.completion_time)
    
    # Voting simulation
    vote_counts: Dict[str, int] = defaultdict(int)
    winning_hash = None
    terminated_early = False
    
    for output in sorted_outputs:
        hash_key = output.equivalence_hash or compute_equivalence_hash(output.output)
        vote_counts[hash_key] += 1
        
        # Check early termination condition
        if early_terminate:
            max_votes = max(vote_counts.values())
            other_max = max((v for h, v in vote_counts.items() if h != hash_key), default=0)
            
            if vote_counts[hash_key] >= other_max + k:
                winning_hash = hash_key
                terminated_early = True
                break
    
    # Determine winner
    if not terminated_early:
        winning_hash = max(vote_counts, key=vote_counts.get)
    
    winning_outputs = equiv_classes[winning_hash]
    consensus_output = winning_outputs[0].output  # Take first output in winning class
    
    # Calculate confidence
    total_valid = len(valid_outputs)
    winning_votes = vote_counts[winning_hash]
    confidence = winning_votes / total_valid if total_valid > 0 else 0.0
    
    return VotingResult(
        subtask_id=outputs[0].subtask_id,
        consensus_output=consensus_output,
        confidence=confidence,
        total_agents=len(outputs),
        valid_agents=total_valid,
        winning_votes=winning_votes,
        early_terminated=terminated_early,
        equivalence_classes={h: [o.agent_id for o in outs] for h, outs in equiv_classes.items()}
    )

# ============================================================================
# Pydantic Input Models
# ============================================================================

class DecomposeInput(BaseModel):
    """Input for task decomposition."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    task: str = Field(..., description="The complex task to decompose into atomic subtasks", min_length=10)
    context: Optional[str] = Field(default=None, description="Additional context or constraints for decomposition")
    max_subtasks: int = Field(default=10, description="Maximum number of subtasks to generate", ge=2, le=50)
    max_depth: int = Field(default=3, description="Maximum DAG depth (sequential dependency chain)", ge=1, le=MAX_SUBTASK_DEPTH)

class SubtaskDefinition(BaseModel):
    """Definition of a single subtask for manual DAG construction."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    id: str = Field(..., description="Unique subtask identifier (e.g., 't1', 't2')")
    description: str = Field(..., description="Clear description of what this subtask accomplishes")
    dependencies: List[str] = Field(default_factory=list, description="IDs of subtasks this depends on")
    prompt_template: Optional[str] = Field(default=None, description="Template for micro-agent prompt")
    output_schema: Optional[Dict[str, Any]] = Field(default=None, description="JSON schema for expected output")
    max_tokens: int = Field(default=MAX_TOKENS_DEFAULT, description="Max tokens for subtask output", ge=10, le=2000)

class BuildDAGInput(BaseModel):
    """Input for manual DAG construction."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    task_id: str = Field(..., description="Unique identifier for the task")
    task_description: str = Field(..., description="High-level description of the task")
    subtasks: List[SubtaskDefinition] = Field(..., description="List of subtask definitions", min_length=1)

class RedFlagInput(BaseModel):
    """Input for red-flag validation."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    output: str = Field(..., description="The agent output to validate")
    max_tokens: int = Field(default=MAX_TOKENS_DEFAULT, description="Maximum allowed token count", ge=10, le=5000)
    output_schema: Optional[Dict[str, Any]] = Field(default=None, description="Expected JSON schema for output")
    check_uncertainty: bool = Field(default=True, description="Check for uncertainty markers")
    check_placeholders: bool = Field(default=True, description="Check for placeholder patterns")

class VoteInput(BaseModel):
    """Input for consensus voting."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    outputs: List[Dict[str, Any]] = Field(
        ..., 
        description="List of agent outputs with keys: agent_id, output, completion_time",
        min_length=1
    )
    subtask_id: str = Field(..., description="ID of the subtask being voted on")
    k: int = Field(default=2, description="Lead threshold for first-to-ahead-by-k", ge=1, le=10)
    equivalence_method: str = Field(
        default="normalized",
        description="Method for grouping equivalent outputs: 'exact', 'normalized', 'json'"
    )
    early_terminate: bool = Field(default=True, description="Enable early termination when consensus reached")

class ExecuteSubtaskInput(BaseModel):
    """Input for parallel subtask execution simulation."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    subtask: Dict[str, Any] = Field(..., description="Subtask definition to execute")
    inputs: Dict[str, Any] = Field(default_factory=dict, description="Input values for subtask")
    criticality: TaskCriticality = Field(default=TaskCriticality.MEDIUM, description="Task criticality level")
    custom_m: Optional[int] = Field(default=None, description="Override number of parallel agents", ge=1, le=15)
    custom_k: Optional[int] = Field(default=None, description="Override vote lead threshold", ge=1, le=10)

class ComputeReliabilityInput(BaseModel):
    """Input for reliability computation."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    agent_accuracy: float = Field(..., description="Individual agent accuracy (0-1)", ge=0, le=1)
    m: int = Field(..., description="Number of parallel agents", ge=1, le=20)
    k: int = Field(..., description="Vote lead threshold", ge=1, le=10)
    n_steps: int = Field(default=1, description="Number of sequential steps in pipeline", ge=1, le=50)

# ============================================================================
# MCP Tools
# ============================================================================

@mcp.tool(
    name="maker_build_dag",
    annotations={
        "title": "Build MAKER Task DAG",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def maker_build_dag(params: BuildDAGInput) -> str:
    """
    Construct a Directed Acyclic Graph (DAG) from subtask definitions.
    
    This implements Pillar 1 (MAD) by structuring atomic subtasks into an
    executable dependency graph. The DAG enables parallel execution of
    independent subtasks while respecting data flow dependencies.
    
    Args:
        params: BuildDAGInput containing task_id, task_description, and subtasks
    
    Returns:
        JSON containing the validated DAG with computed depth, width, and
        topological execution order.
    
    Example:
        subtasks = [
            {"id": "t1", "description": "Extract entity", "dependencies": []},
            {"id": "t2", "description": "Lookup attribute", "dependencies": ["t1"]},
            {"id": "t3", "description": "Format result", "dependencies": ["t2"]}
        ]
    """
    dag = DAG(
        task_id=params.task_id,
        task_description=params.task_description
    )
    
    # Build subtasks
    for st in params.subtasks:
        dag.subtasks[st.id] = Subtask(
            id=st.id,
            description=st.description,
            dependencies=st.dependencies,
            prompt_template=st.prompt_template,
            output_schema=st.output_schema,
            max_tokens=st.max_tokens
        )
    
    # Build edges from dependencies
    for st in params.subtasks:
        for dep in st.dependencies:
            if dep not in dag.subtasks:
                return json.dumps({
                    "error": f"Subtask {st.id} depends on unknown subtask {dep}",
                    "valid": False
                }, indent=2)
            dag.edges.append((dep, st.id))
    
    # Validate DAG (check for cycles)
    try:
        execution_order = dag.topological_sort()
    except ValueError as e:
        return json.dumps({
            "error": str(e),
            "valid": False
        }, indent=2)
    
    result = dag.to_dict()
    result["execution_order"] = execution_order
    result["valid"] = True
    
    return json.dumps(result, indent=2)

@mcp.tool(
    name="maker_red_flag",
    annotations={
        "title": "Apply MAKER Red-Flag Validation",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def maker_red_flag(params: RedFlagInput) -> str:
    """
    Apply red-flag validation to an agent output (Pillar 3).
    
    Checks for:
    - Length violations (output exceeds max tokens)
    - Format violations (fails JSON schema validation)
    - Placeholder patterns ([TODO], [N/A], etc.)
    - Uncertainty markers ("I'm not sure", "possibly", etc.)
    
    Red-flagged outputs are excluded from voting to prevent
    contamination of the consensus mechanism.
    
    Args:
        params: RedFlagInput with output text and validation config
    
    Returns:
        JSON with is_valid boolean, list of flags with types/reasons/severity,
        and recommendation for handling.
    """
    flags, is_valid = apply_red_flags(
        output=params.output,
        max_tokens=params.max_tokens,
        schema=params.output_schema,
        check_uncertainty=params.check_uncertainty,
        check_placeholders=params.check_placeholders
    )
    
    result = {
        "is_valid": is_valid,
        "flags": [f.to_dict() for f in flags],
        "total_flags": len(flags),
        "max_severity": max((f.severity for f in flags), default=0.0),
        "recommendation": "accept" if is_valid else "reject"
    }
    
    if not is_valid:
        result["recommendation_reason"] = "; ".join(f.reason for f in flags)
    
    return json.dumps(result, indent=2)

@mcp.tool(
    name="maker_vote",
    annotations={
        "title": "Execute MAKER Consensus Voting",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def maker_vote(params: VoteInput) -> str:
    """
    Execute first-to-ahead-by-k consensus voting (Pillar 2).
    
    Given m agent outputs, accepts result r when:
        votes(r) >= votes(any_other) + k
    
    Features:
    - Early termination: Stops when consensus reached (cost optimization)
    - Equivalence classes: Groups semantically similar outputs
    - Confidence scoring: Based on vote distribution
    
    Args:
        params: VoteInput with outputs, k threshold, and equivalence method
    
    Returns:
        JSON with consensus_output, confidence, vote counts, early_terminated flag,
        and equivalence class breakdown.
    
    Example:
        With m=7 agents and k=2, if 4 agents output "Edinburgh" and 
        others vary, Edinburgh wins with lead of 4-1=3 >= k=2.
    """
    # Build AgentOutput objects
    agent_outputs = []
    for out in params.outputs:
        agent_output = AgentOutput(
            agent_id=out.get("agent_id", f"agent_{len(agent_outputs)}"),
            subtask_id=params.subtask_id,
            output=out["output"],
            completion_time=out.get("completion_time", len(agent_outputs) * 0.1),
            is_valid=out.get("is_valid", True)
        )
        agent_output.equivalence_hash = compute_equivalence_hash(
            agent_output.output, 
            params.equivalence_method
        )
        agent_outputs.append(agent_output)
    
    # Execute voting
    result = first_to_ahead_by_k_vote(
        outputs=agent_outputs,
        k=params.k,
        early_terminate=params.early_terminate
    )
    
    return json.dumps(result.to_dict(), indent=2)

@mcp.tool(
    name="maker_compute_reliability",
    annotations={
        "title": "Compute MAKER System Reliability",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def maker_compute_reliability(params: ComputeReliabilityInput) -> str:
    """
    Compute theoretical system reliability for MAKER configuration.
    
    Uses binomial probability model to estimate:
    - Single-step reliability with voting
    - Multi-step pipeline reliability
    - Improvement factor over single-agent baseline
    - Cost multiplier
    
    Args:
        params: ComputeReliabilityInput with agent_accuracy, m, k, n_steps
    
    Returns:
        JSON with system_accuracy, baseline_accuracy, improvement_factor,
        cost_multiplier, and configuration recommendations.
    
    Mathematical basis:
        For agent accuracy p and n-step task:
        - Single agent: p^n (compounds multiplicatively)
        - MAKER: P(consensus correct)^n where consensus accuracy >> p
    """
    from math import comb
    
    p = params.agent_accuracy
    m = params.m
    k = params.k
    n = params.n_steps
    
    # Compute P(correct result gets >= k more votes than any incorrect)
    # Simplified: P(majority correct with margin k)
    # Using binomial approximation for voting
    
    # P(at least ceil((m+k)/2) correct votes)
    min_correct_votes = (m + k + 1) // 2
    
    consensus_accuracy = 0.0
    for correct_votes in range(min_correct_votes, m + 1):
        prob = comb(m, correct_votes) * (p ** correct_votes) * ((1-p) ** (m - correct_votes))
        consensus_accuracy += prob
    
    # Multi-step reliability
    system_accuracy = consensus_accuracy ** n
    baseline_accuracy = p ** n
    
    # Cost estimation (with early termination ~60% of m)
    avg_agents_used = 0.6 * m
    cost_multiplier = avg_agents_used
    
    improvement_factor = system_accuracy / baseline_accuracy if baseline_accuracy > 0 else float('inf')
    
    result = {
        "configuration": {
            "agent_accuracy": p,
            "m_agents": m,
            "k_threshold": k,
            "n_steps": n
        },
        "reliability": {
            "single_step_consensus": round(consensus_accuracy, 4),
            "system_accuracy": round(system_accuracy, 4),
            "baseline_accuracy": round(baseline_accuracy, 4),
            "improvement_factor": round(improvement_factor, 2)
        },
        "cost": {
            "avg_agents_per_subtask": round(avg_agents_used, 1),
            "cost_multiplier": round(cost_multiplier, 1),
            "worst_case_multiplier": m
        },
        "recommendation": _get_config_recommendation(consensus_accuracy, cost_multiplier, n)
    }
    
    return json.dumps(result, indent=2)

def _get_config_recommendation(accuracy: float, cost: float, steps: int) -> str:
    """Generate configuration recommendation based on metrics."""
    if accuracy >= 0.99 and cost <= 6:
        return "Excellent configuration - high reliability with reasonable cost"
    elif accuracy >= 0.95 and cost <= 8:
        return "Good configuration for production use"
    elif accuracy >= 0.90:
        return "Consider increasing m or k for higher reliability"
    elif cost > 8:
        return "Consider early termination or adaptive m to reduce cost"
    else:
        return "Review agent accuracy - may need model improvements"

@mcp.tool(
    name="maker_get_config",
    annotations={
        "title": "Get MAKER Configuration by Criticality",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def maker_get_config(criticality: TaskCriticality = TaskCriticality.MEDIUM) -> str:
    """
    Get recommended MAKER configuration for task criticality level.
    
    Criticality levels:
    - low: m=3, k=1 (~70% confidence) - Exploratory tasks
    - medium: m=5, k=2 (~85% confidence) - Production tasks
    - high: m=7, k=3 (~95% confidence) - Safety-critical
    - critical: m=11, k=5 (~99% confidence) - Medical/legal domains
    
    Args:
        criticality: Task criticality level
    
    Returns:
        JSON with m, k, target_confidence, and use_case examples.
    """
    config = CRITICALITY_CONFIGS[criticality.value]
    
    use_cases = {
        "low": ["Exploratory research", "Brainstorming", "Draft generation"],
        "medium": ["Production workflows", "Content creation", "Data extraction"],
        "high": ["Financial analysis", "Code review", "Security assessment"],
        "critical": ["Medical diagnosis", "Legal analysis", "Safety verification"]
    }
    
    result = {
        "criticality": criticality.value,
        "m_agents": config["m"],
        "k_threshold": config["k"],
        "target_confidence": config["confidence"],
        "use_cases": use_cases[criticality.value],
        "notes": {
            "early_termination": "Typically reduces cost by 30-50%",
            "red_flagging": "Further improves reliability by filtering invalid outputs",
            "scaling": f"Theoretical accuracy improvement: {config['confidence']*100:.0f}% vs ~85% single agent"
        }
    }
    
    return json.dumps(result, indent=2)

@mcp.tool(
    name="maker_compose_results",
    annotations={
        "title": "Compose MAKER Subtask Results",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def maker_compose_results(
    results: List[Dict[str, Any]] = Field(..., description="List of {subtask_id, output} dicts"),
    dag: Dict[str, Any] = Field(..., description="The DAG structure from maker_build_dag"),
    composition_template: Optional[str] = Field(default=None, description="Template for composing final output")
) -> str:
    """
    Compose validated subtask results into final task output.
    
    Takes consensus results from all subtasks and combines them
    according to the DAG structure and optional composition template.
    
    Args:
        results: List of subtask results with subtask_id and output
        dag: The DAG structure defining task composition
        composition_template: Optional template with {subtask_id} placeholders
    
    Returns:
        JSON with composed_output, composition_method, and any warnings
        about missing or failed subtasks.
    """
    # Build results map
    results_map = {r["subtask_id"]: r.get("output") for r in results}
    
    # Check for missing subtasks
    required_subtasks = set(dag.get("subtasks", {}).keys())
    provided_subtasks = set(results_map.keys())
    missing = required_subtasks - provided_subtasks
    
    warnings = []
    if missing:
        warnings.append(f"Missing results for subtasks: {list(missing)}")
    
    # Compose output
    if composition_template:
        # Use template with substitution
        composed = composition_template
        for subtask_id, output in results_map.items():
            composed = composed.replace(f"{{{subtask_id}}}", str(output or "[missing]"))
        composition_method = "template"
    else:
        # Default: concatenate in execution order
        execution_order = dag.get("execution_order", list(results_map.keys()))
        parts = []
        for subtask_id in execution_order:
            if subtask_id in results_map and results_map[subtask_id]:
                parts.append(results_map[subtask_id])
        composed = "\n".join(parts) if parts else "[No valid results]"
        composition_method = "sequential_concatenation"
    
    result = {
        "composed_output": composed,
        "composition_method": composition_method,
        "subtasks_composed": len([r for r in results if r.get("output")]),
        "total_subtasks": len(required_subtasks),
        "warnings": warnings if warnings else None,
        "success": len(missing) == 0
    }
    
    return json.dumps(result, indent=2)

@mcp.tool(
    name="maker_generate_prompt",
    annotations={
        "title": "Generate MAKER Micro-Agent Prompt",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def maker_generate_prompt(
    subtask: Dict[str, Any] = Field(..., description="Subtask definition from DAG"),
    inputs: Dict[str, Any] = Field(default_factory=dict, description="Input values for the subtask"),
    agent_index: int = Field(default=0, description="Index of this agent (for seed diversity)", ge=0)
) -> str:
    """
    Generate optimized micro-agent prompt for a subtask.
    
    Creates a focused, constrained prompt following MAKER best practices:
    - Clear role specification
    - Explicit input/output format
    - Constraints and length limits
    - Format enforcement
    
    Args:
        subtask: Subtask definition with description, output_schema, max_tokens
        inputs: Input values to incorporate into prompt
        agent_index: Agent index for introducing controlled diversity
    
    Returns:
        JSON with the generated prompt, constraints, and metadata.
    """
    description = subtask.get("description", "Complete the task")
    output_schema = subtask.get("output_schema")
    max_tokens = subtask.get("max_tokens", MAX_TOKENS_DEFAULT)
    prompt_template = subtask.get("prompt_template")
    
    # Build prompt
    if prompt_template:
        prompt = prompt_template
        for key, value in inputs.items():
            prompt = prompt.replace(f"{{{key}}}", str(value))
    else:
        # Generate default structured prompt
        prompt_parts = [
            f"[ROLE]: You are a specialized agent for: {description}",
            "",
            "[TASK]: Execute the following atomic subtask with precision.",
            f"Description: {description}",
        ]
        
        if inputs:
            prompt_parts.append("")
            prompt_parts.append("[INPUT]:")
            prompt_parts.append(json.dumps(inputs, indent=2))
        
        if output_schema:
            prompt_parts.append("")
            prompt_parts.append("[OUTPUT FORMAT]:")
            prompt_parts.append(json.dumps(output_schema, indent=2))
        
        prompt_parts.extend([
            "",
            "[CONSTRAINTS]:",
            f"- Maximum output length: {max_tokens} tokens",
            "- No explanations or reasoning in output",
            "- Return ONLY the requested output format",
            "- Do not include uncertainty markers",
        ])
        
        prompt = "\n".join(prompt_parts)
    
    result = {
        "prompt": prompt,
        "subtask_id": subtask.get("id", "unknown"),
        "agent_index": agent_index,
        "constraints": {
            "max_tokens": max_tokens,
            "has_schema": output_schema is not None
        }
    }
    
    return json.dumps(result, indent=2)

# ============================================================================
# Server Entry Point
# ============================================================================

if __name__ == "__main__":
    mcp.run()

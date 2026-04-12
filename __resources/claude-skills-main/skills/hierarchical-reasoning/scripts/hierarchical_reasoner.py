#!/usr/bin/env python3
"""
Hierarchical Reasoning Engine
Implements dual-timescale iterative reasoning inspired by cognitive architectures.
"""

import json
import sys
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum


class ReasoningLevel(Enum):
    """Defines the abstraction level of reasoning."""
    STRATEGIC = "strategic"  # High-level, abstract planning
    TACTICAL = "tactical"    # Mid-level, approach formulation
    OPERATIONAL = "operational"  # Low-level, detailed execution


@dataclass
class ReasoningState:
    """Represents the state of reasoning at a particular level."""
    level: ReasoningLevel
    content: str
    confidence: float  # 0.0 to 1.0
    uncertainty: float  # 0.0 to 1.0
    iteration: int
    convergence_score: float = 0.0
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class HierarchicalReasoningResult:
    """Complete result of hierarchical reasoning process."""
    strategic_state: ReasoningState
    tactical_state: ReasoningState
    operational_state: ReasoningState
    total_iterations: int
    converged: bool
    convergence_reason: str
    final_synthesis: str
    trace: List[Dict[str, Any]]


class HierarchicalReasoner:
    """
    Executes hierarchical reasoning through nested iterative refinement.
    
    Architecture:
    - Strategic level: Abstract problem formulation and goal setting
    - Tactical level: Approach design and method selection
    - Operational level: Detailed execution and computation
    
    Information flows bidirectionally:
    - Top-down: Strategic insights guide tactical and operational decisions
    - Bottom-up: Operational findings refine tactical approaches and strategic understanding
    """
    
    def __init__(
        self,
        max_strategic_cycles: int = 3,
        max_tactical_cycles: int = 5,
        max_operational_cycles: int = 7,
        convergence_threshold: float = 0.95,
        uncertainty_threshold: float = 0.1
    ):
        self.max_strategic_cycles = max_strategic_cycles
        self.max_tactical_cycles = max_tactical_cycles
        self.max_operational_cycles = max_operational_cycles
        self.convergence_threshold = convergence_threshold
        self.uncertainty_threshold = uncertainty_threshold
        self.trace = []
        
    def _compute_convergence(
        self,
        current_state: str,
        previous_state: str,
        confidence: float
    ) -> float:
        """
        Compute convergence score based on state stability and confidence.
        Returns value between 0.0 and 1.0.
        """
        if not previous_state:
            return 0.0
        
        # Simple text similarity proxy (in practice, use embeddings)
        common_words = set(current_state.lower().split()) & set(previous_state.lower().split())
        total_words = set(current_state.lower().split()) | set(previous_state.lower().split())
        
        if not total_words:
            return 0.0
            
        text_similarity = len(common_words) / len(total_words)
        
        # Convergence is combination of stability and confidence
        return 0.7 * text_similarity + 0.3 * confidence
    
    def _check_convergence(
        self,
        strategic_score: float,
        tactical_score: float,
        operational_score: float
    ) -> Tuple[bool, str]:
        """Determine if reasoning has converged across all levels."""
        
        # All levels must exceed threshold
        if (strategic_score >= self.convergence_threshold and
            tactical_score >= self.convergence_threshold and
            operational_score >= self.convergence_threshold):
            return True, "All levels converged above threshold"
        
        # Check weighted average for partial convergence
        weighted_avg = (
            0.5 * strategic_score +
            0.3 * tactical_score +
            0.2 * operational_score
        )
        
        if weighted_avg >= self.convergence_threshold:
            return True, "Weighted average convergence achieved"
        
        return False, "Convergence not yet achieved"
    
    def reason(
        self,
        problem: str,
        context: Optional[Dict[str, Any]] = None
    ) -> HierarchicalReasoningResult:
        """
        Execute hierarchical reasoning on the given problem.
        
        Args:
            problem: The problem statement or question to reason about
            context: Optional additional context, constraints, or background
            
        Returns:
            HierarchicalReasoningResult containing all reasoning states and trace
        """
        context = context or {}
        self.trace = []
        
        # Initialize states
        strategic_state = ReasoningState(
            level=ReasoningLevel.STRATEGIC,
            content="",
            confidence=0.0,
            uncertainty=1.0,
            iteration=0
        )
        
        tactical_state = ReasoningState(
            level=ReasoningLevel.TACTICAL,
            content="",
            confidence=0.0,
            uncertainty=1.0,
            iteration=0
        )
        
        operational_state = ReasoningState(
            level=ReasoningLevel.OPERATIONAL,
            content="",
            confidence=0.0,
            uncertainty=1.0,
            iteration=0
        )
        
        # Main hierarchical reasoning loop
        converged = False
        convergence_reason = ""
        total_iterations = 0
        
        for s_cycle in range(self.max_strategic_cycles):
            # Strategic planning
            prev_strategic = strategic_state.content
            strategic_state = self._strategic_reasoning(
                problem, context, tactical_state, s_cycle
            )
            strategic_state.convergence_score = self._compute_convergence(
                strategic_state.content, prev_strategic, strategic_state.confidence
            )
            
            self.trace.append({
                "cycle": s_cycle,
                "level": "strategic",
                "state": asdict(strategic_state)
            })
            
            for t_cycle in range(self.max_tactical_cycles):
                # Tactical approach design
                prev_tactical = tactical_state.content
                tactical_state = self._tactical_reasoning(
                    problem, context, strategic_state, operational_state, t_cycle
                )
                tactical_state.convergence_score = self._compute_convergence(
                    tactical_state.content, prev_tactical, tactical_state.confidence
                )
                
                self.trace.append({
                    "cycle": t_cycle,
                    "level": "tactical",
                    "state": asdict(tactical_state)
                })
                
                for o_cycle in range(self.max_operational_cycles):
                    # Operational execution
                    prev_operational = operational_state.content
                    operational_state = self._operational_reasoning(
                        problem, context, strategic_state, tactical_state, o_cycle
                    )
                    operational_state.convergence_score = self._compute_convergence(
                        operational_state.content, prev_operational, operational_state.confidence
                    )
                    
                    self.trace.append({
                        "cycle": o_cycle,
                        "level": "operational",
                        "state": asdict(operational_state)
                    })
                    
                    total_iterations += 1
                    
                    # Check convergence
                    converged, convergence_reason = self._check_convergence(
                        strategic_state.convergence_score,
                        tactical_state.convergence_score,
                        operational_state.convergence_score
                    )
                    
                    if converged:
                        break
                
                if converged:
                    break
            
            if converged:
                break
        
        if not converged:
            convergence_reason = "Maximum iterations reached without full convergence"
        
        # Synthesize final result
        final_synthesis = self._synthesize_result(
            strategic_state, tactical_state, operational_state, problem
        )
        
        return HierarchicalReasoningResult(
            strategic_state=strategic_state,
            tactical_state=tactical_state,
            operational_state=operational_state,
            total_iterations=total_iterations,
            converged=converged,
            convergence_reason=convergence_reason,
            final_synthesis=final_synthesis,
            trace=self.trace
        )
    
    def _strategic_reasoning(
        self,
        problem: str,
        context: Dict[str, Any],
        tactical_state: ReasoningState,
        iteration: int
    ) -> ReasoningState:
        """
        Strategic level: Abstract problem formulation and goal setting.
        This would be replaced with LLM calls in production.
        """
        # Placeholder: In production, this calls an LLM with strategic prompt
        content = f"[STRATEGIC CYCLE {iteration}] Problem formulation and goal identification for: {problem[:100]}..."
        
        if tactical_state.content:
            content += f" | Informed by tactical insights"
        
        return ReasoningState(
            level=ReasoningLevel.STRATEGIC,
            content=content,
            confidence=min(0.5 + iteration * 0.15, 0.95),
            uncertainty=max(0.5 - iteration * 0.15, 0.05),
            iteration=iteration,
            dependencies=["problem_statement"]
        )
    
    def _tactical_reasoning(
        self,
        problem: str,
        context: Dict[str, Any],
        strategic_state: ReasoningState,
        operational_state: ReasoningState,
        iteration: int
    ) -> ReasoningState:
        """
        Tactical level: Approach design and method selection.
        Bridges strategic goals with operational execution.
        """
        content = f"[TACTICAL CYCLE {iteration}] Approach design guided by strategic goals"
        
        if operational_state.content:
            content += f" | Refined by operational feedback"
        
        return ReasoningState(
            level=ReasoningLevel.TACTICAL,
            content=content,
            confidence=min(0.4 + iteration * 0.12, 0.93),
            uncertainty=max(0.6 - iteration * 0.12, 0.07),
            iteration=iteration,
            dependencies=["strategic_state"]
        )
    
    def _operational_reasoning(
        self,
        problem: str,
        context: Dict[str, Any],
        strategic_state: ReasoningState,
        tactical_state: ReasoningState,
        iteration: int
    ) -> ReasoningState:
        """
        Operational level: Detailed execution and computation.
        Performs concrete reasoning steps guided by tactical approach.
        """
        content = f"[OPERATIONAL CYCLE {iteration}] Detailed execution following tactical approach"
        
        return ReasoningState(
            level=ReasoningLevel.OPERATIONAL,
            content=content,
            confidence=min(0.3 + iteration * 0.10, 0.92),
            uncertainty=max(0.7 - iteration * 0.10, 0.08),
            iteration=iteration,
            dependencies=["tactical_state"]
        )
    
    def _synthesize_result(
        self,
        strategic: ReasoningState,
        tactical: ReasoningState,
        operational: ReasoningState,
        problem: str
    ) -> str:
        """Synthesize final result from all reasoning levels."""
        return f"""
HIERARCHICAL REASONING SYNTHESIS
================================

Problem: {problem}

STRATEGIC UNDERSTANDING (Abstract):
{strategic.content}
Confidence: {strategic.confidence:.2f} | Uncertainty: {strategic.uncertainty:.2f}

TACTICAL APPROACH (Method):
{tactical.content}
Confidence: {tactical.confidence:.2f} | Uncertainty: {tactical.uncertainty:.2f}

OPERATIONAL EXECUTION (Details):
{operational.content}
Confidence: {operational.confidence:.2f} | Uncertainty: {operational.uncertainty:.2f}

CONVERGENCE:
- Strategic: {strategic.convergence_score:.2f}
- Tactical: {tactical.convergence_score:.2f}
- Operational: {operational.convergence_score:.2f}
"""


def main():
    """CLI interface for hierarchical reasoning."""
    if len(sys.argv) < 2:
        print("Usage: python hierarchical_reasoner.py <problem> [--context <json>]")
        print("\nExample:")
        print('  python hierarchical_reasoner.py "How can we reduce energy consumption?" --context \'{"domain": "sustainability"}\'')
        sys.exit(1)
    
    problem = sys.argv[1]
    context = {}
    
    if "--context" in sys.argv:
        context_idx = sys.argv.index("--context")
        if context_idx + 1 < len(sys.argv):
            context = json.loads(sys.argv[context_idx + 1])
    
    reasoner = HierarchicalReasoner()
    result = reasoner.reason(problem, context)
    
    print(result.final_synthesis)
    print(f"\nTotal iterations: {result.total_iterations}")
    print(f"Converged: {result.converged}")
    print(f"Reason: {result.convergence_reason}")
    
    if "--trace" in sys.argv:
        print("\n\n=== REASONING TRACE ===")
        print(json.dumps(result.trace, indent=2))


if __name__ == "__main__":
    main()

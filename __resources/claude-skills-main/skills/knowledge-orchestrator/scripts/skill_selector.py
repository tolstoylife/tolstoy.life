#!/usr/bin/env python3
"""
Skill Selection Logic Tester for Knowledge Orchestrator

Tests skill selection decision logic on sample inputs.
Useful for validating orchestrator behavior before deployment.

Usage:
    python skill_selector.py "Create a comprehensive note about microservices"
    python skill_selector.py --test-suite
"""

import argparse
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any

# Import task classifier
from task_classifier import TaskClassifier, TaskFeatures


@dataclass
class SkillSelection:
    """Result of skill selection process"""
    type: str  # single_skill, multi_skill_workflow, no_match
    skill: Optional[str] = None
    skills: Optional[List[str]] = None
    workflow: Optional[str] = None
    confidence: float = 0.0
    alternatives: Optional[Dict[str, float]] = None
    reason: Optional[str] = None


class SkillSelector:
    """Implements skill selection decision logic"""

    def __init__(self):
        self.classifier = TaskClassifier()

    def select(self, request: str) -> SkillSelection:
        """Select appropriate skill(s) for request"""
        # Analyze task features
        features = self.classifier.analyze(request)

        # Apply decision rules
        candidates = self._apply_decision_rules(features)

        # Detect workflow patterns if multiple candidates
        if len(candidates) >= 2:
            workflow = self._detect_workflow_pattern(candidates, features)
            if workflow:
                return SkillSelection(
                    type="multi_skill_workflow",
                    skills=list(candidates.keys()),
                    workflow=workflow,
                    confidence=min(candidates.values())
                )

        # Single skill selection
        if len(candidates) == 1:
            skill = list(candidates.keys())[0]
            return SkillSelection(
                type="single_skill",
                skill=skill,
                confidence=candidates[skill]
            )

        # Multiple candidates without workflow - select highest
        if len(candidates) > 1:
            best_skill = max(candidates.items(), key=lambda x: x[1])
            return SkillSelection(
                type="single_skill",
                skill=best_skill[0],
                confidence=best_skill[1],
                alternatives=candidates
            )

        # No match
        return SkillSelection(
            type="no_match",
            reason="No skill meets confidence threshold",
            confidence=0.0
        )

    def _apply_decision_rules(self, features: TaskFeatures) -> Dict[str, float]:
        """Apply confidence-weighted decision rules"""
        candidates = {}

        # RULE SET 1: Explicit Triggers (0.90-1.0)

        # Obsidian-Markdown
        if features.creates_md_file:
            candidates["obsidian-markdown"] = 0.95
        elif features.obsidian_signals >= 3:
            candidates["obsidian-markdown"] = max(
                candidates.get("obsidian-markdown", 0), 0.92
            )

        # Knowledge-Graph
        if features.requires_extraction and features.content_type != "code":
            candidates["knowledge-graph"] = 0.90
        elif features.graph_signals >= 2:
            candidates["knowledge-graph"] = max(
                candidates.get("knowledge-graph", 0), 0.88
            )

        # Hierarchical-Reasoning
        if features.complexity_score > 0.7 and features.requires_decomposition:
            candidates["hierarchical-reasoning"] = 0.90
        elif features.reasoning_signals >= 3:
            candidates["hierarchical-reasoning"] = max(
                candidates.get("hierarchical-reasoning", 0), 0.88
            )

        # RULE SET 2: Implicit Triggers (0.70-0.89)

        if features.artifact_type == "knowledge" and "knowledge-graph" not in candidates:
            candidates["knowledge-graph"] = 0.75

        if features.complexity_score > 0.5 and features.artifact_type == "analysis":
            candidates["hierarchical-reasoning"] = max(
                candidates.get("hierarchical-reasoning", 0), 0.72
            )

        if features.artifact_type == "file" and features.content_type == "prose":
            candidates["obsidian-markdown"] = max(
                candidates.get("obsidian-markdown", 0), 0.70
            )

        return candidates

    def _detect_workflow_pattern(self, candidates: Dict[str, float], features: TaskFeatures) -> Optional[str]:
        """Detect canonical workflow patterns"""
        skills_set = set(candidates.keys())

        # Pattern 1: Research → Structure → Document
        if all(skill in skills_set for skill in ["hierarchical-reasoning", "knowledge-graph", "obsidian-markdown"]):
            if features.complexity_score > 0.7 and features.creates_md_file:
                return "research_structure_document"

        # Pattern 2: Extract → Validate → Format
        if all(skill in skills_set for skill in ["knowledge-graph", "hierarchical-reasoning", "obsidian-markdown"]):
            if features.requires_extraction and features.artifact_type == "file":
                return "extract_validate_format"

        # Pattern 3: Analyze → Graph → Visualize
        if all(skill in skills_set for skill in ["hierarchical-reasoning", "knowledge-graph", "obsidian-markdown"]):
            if features.complexity_score > 0.6 and "visualiz" in features.raw_request.lower():
                return "analyze_graph_visualize"

        return None


# Test Suite
TEST_CASES = [
    {
        "name": "Simple Note Creation",
        "request": "Create a meeting note for today",
        "expected_skill": "obsidian-markdown",
        "expected_confidence_min": 0.90
    },
    {
        "name": "Complex Research Task",
        "request": "Research microservices patterns and create a comprehensive guide with architecture diagrams",
        "expected_type": "multi_skill_workflow",
        "expected_workflow": "research_structure_document"
    },
    {
        "name": "Entity Extraction",
        "request": "Extract entities and relationships from this research paper",
        "expected_skill": "knowledge-graph",
        "expected_confidence_min": 0.85
    },
    {
        "name": "Strategic Analysis",
        "request": "Analyze the strategic implications of this technology shift",
        "expected_skill": "hierarchical-reasoning",
        "expected_confidence_min": 0.85
    },
    {
        "name": "Multi-Skill Workflow",
        "request": "Create a note about neural networks with entity relationships and architectural breakdown",
        "expected_type": "multi_skill_workflow",
        "expected_skills": ["hierarchical-reasoning", "knowledge-graph", "obsidian-markdown"]
    },
    {
        "name": "Ambiguous Request",
        "request": "Help me understand this topic",
        "expected_type": "no_match"
    },
    {
        "name": "Explicit Skill Override",
        "request": "Use hierarchical-reasoning to decompose this problem",
        "expected_skill": "hierarchical-reasoning",
        "expected_confidence_min": 0.85
    },
    {
        "name": "Extract and Format",
        "request": "Extract knowledge from this document and create a structured Obsidian note",
        "expected_type": "multi_skill_workflow",
        "expected_workflow": "extract_validate_format"
    }
]


def run_test_suite(selector: SkillSelector):
    """Run test suite and report results"""
    print(f"\n{'='*80}")
    print("SKILL SELECTION TEST SUITE")
    print(f"{'='*80}\n")

    passed = 0
    failed = 0

    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"Request: {test_case['request']}")

        selection = selector.select(test_case['request'])

        # Validate expectations
        success = True

        if "expected_skill" in test_case:
            if selection.skill != test_case["expected_skill"]:
                print(f"  ❌ FAIL: Expected skill '{test_case['expected_skill']}', got '{selection.skill}'")
                success = False

        if "expected_type" in test_case:
            if selection.type != test_case["expected_type"]:
                print(f"  ❌ FAIL: Expected type '{test_case['expected_type']}', got '{selection.type}'")
                success = False

        if "expected_workflow" in test_case:
            if selection.workflow != test_case["expected_workflow"]:
                print(f"  ❌ FAIL: Expected workflow '{test_case['expected_workflow']}', got '{selection.workflow}'")
                success = False

        if "expected_confidence_min" in test_case:
            if selection.confidence < test_case["expected_confidence_min"]:
                print(f"  ❌ FAIL: Expected confidence >= {test_case['expected_confidence_min']}, got {selection.confidence:.2f}")
                success = False

        if "expected_skills" in test_case:
            if set(selection.skills or []) != set(test_case["expected_skills"]):
                print(f"  ❌ FAIL: Expected skills {test_case['expected_skills']}, got {selection.skills}")
                success = False

        if success:
            print(f"  ✅ PASS")
            if selection.type == "single_skill":
                print(f"     Skill: {selection.skill} (confidence: {selection.confidence:.2f})")
            elif selection.type == "multi_skill_workflow":
                print(f"     Workflow: {selection.workflow}")
                print(f"     Skills: {selection.skills}")
                print(f"     Confidence: {selection.confidence:.2f}")
            passed += 1
        else:
            failed += 1

        print()

    print(f"{'='*80}")
    print(f"Results: {passed} passed, {failed} failed out of {len(TEST_CASES)} tests")
    print(f"{'='*80}\n")

    return passed, failed


def main():
    """CLI interface for skill selection testing"""
    parser = argparse.ArgumentParser(
        description="Test skill selection logic on sample inputs"
    )
    parser.add_argument(
        "request",
        nargs="?",
        help="User request to analyze for skill selection"
    )
    parser.add_argument(
        "--test-suite",
        action="store_true",
        help="Run complete test suite"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    selector = SkillSelector()

    if args.test_suite:
        run_test_suite(selector)
    elif args.request:
        selection = selector.select(args.request)

        if args.json:
            print(json.dumps(asdict(selection), indent=2))
        else:
            print(f"\n{'='*80}")
            print(f"Request: {args.request}")
            print(f"{'='*80}\n")
            print_selection(selection)
    else:
        parser.print_help()


def print_selection(selection: SkillSelection):
    """Pretty-print skill selection"""
    print(f"Selection Type: {selection.type}")

    if selection.type == "single_skill":
        print(f"Selected Skill: {selection.skill}")
        print(f"Confidence: {selection.confidence:.2f}")
        if selection.alternatives:
            print(f"\nAlternatives:")
            for skill, conf in selection.alternatives.items():
                if skill != selection.skill:
                    print(f"  - {skill}: {conf:.2f}")

    elif selection.type == "multi_skill_workflow":
        print(f"Workflow Pattern: {selection.workflow}")
        print(f"Skills: {', '.join(selection.skills)}")
        print(f"Confidence: {selection.confidence:.2f}")

    elif selection.type == "no_match":
        print(f"Reason: {selection.reason}")
        print("\nSuggestion: Ask user to clarify or specify skill")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Workflow Router — matches problem descriptions to the right orchestration workflow.

Usage:
    python workflow_router.py "description of your problem"
    python workflow_router.py --list
    python workflow_router.py --json "description"
"""

import json
import re
import sys
from dataclasses import dataclass


@dataclass
class Workflow:
    number: int
    name: str
    problem_type: str
    primary_skill: str
    supporting_skills: list[str]
    keywords: list[str]
    negative_keywords: list[str]


WORKFLOWS = [
    Workflow(
        number=1,
        name="Parallel Debugging Orchestration",
        problem_type="Multiple independent bugs",
        primary_skill="dispatching-parallel-agents",
        supporting_skills=["root-cause-tracing", "systematic-debugging"],
        keywords=["multiple failures", "multiple tests", "independent bugs",
                   "several tests failing", "several failures", "different modules",
                   "parallel debug", "unrelated failures", "different modules failing",
                   "multiple bugs", "many failures", "tests failing in"],
        negative_keywords=["single", "one bug", "one test"],
    ),
    Workflow(
        number=2,
        name="TDD-Driven Root Cause Resolution",
        problem_type="Regression / single bug",
        primary_skill="test-driven-development",
        supporting_skills=["root-cause-tracing", "verification-before-completion"],
        keywords=["regression", "bug", "broke", "failing test", "intermittent",
                   "flaky", "started failing", "used to work", "single failure"],
        negative_keywords=["multiple", "several", "migration", "pipeline"],
    ),
    Workflow(
        number=3,
        name="Multi-Agent Feature Development",
        problem_type="Large feature",
        primary_skill="dispatching-parallel-agents",
        supporting_skills=["test-driven-development", "writing-plans"],
        keywords=["large feature", "big feature", "multiple domains", "multi-module",
                   "feature spanning", "new system", "full stack feature", "epic"],
        negative_keywords=["bug", "fix", "broken", "incident"],
    ),
    Workflow(
        number=4,
        name="Emergency Debug Escalation",
        problem_type="Production issue (escalating)",
        primary_skill="root-cause-tracing",
        supporting_skills=["systematic-debugging", "verification-before-completion"],
        keywords=["production", "emergency", "escalat", "sev1", "sev2", "outage",
                   "down", "critical", "urgent", "pages", "alert firing"],
        negative_keywords=["data pipeline", "etl", "migration"],
    ),
    Workflow(
        number=5,
        name="Continuous Quality Pipeline",
        problem_type="Quality gates / CI",
        primary_skill="test-driven-development",
        supporting_skills=["verification-before-completion", "condition-based-waiting"],
        keywords=["quality gate", "ci pipeline", "pre-commit", "coverage",
                   "lint", "continuous", "deploy check", "merge check"],
        negative_keywords=["bug", "broken", "incident"],
    ),
    Workflow(
        number=6,
        name="Context Engineering Orchestration",
        problem_type="Context saturation",
        primary_skill="dispatching-parallel-agents",
        supporting_skills=["memory", "retrieval", "compaction"],
        keywords=["context window", "context limit", "token budget", "too much context",
                   "sub-agent", "context rot", "memory management", "compaction",
                   "multi-agent context", "information retrieval", "rag"],
        negative_keywords=[],
    ),
    Workflow(
        number=7,
        name="Safe Migration & Large-Scale Refactor",
        problem_type="Codebase migration",
        primary_skill="test-driven-development",
        supporting_skills=["writing-plans", "dispatching-parallel-agents", "verification-before-completion"],
        keywords=["migration", "refactor", "rename", "upgrade", "framework swap",
                   "library upgrade", "api change", "breaking change", "monolith",
                   "restructure", "move files", "large-scale rename", "version upgrade"],
        negative_keywords=["data pipeline", "etl"],
    ),
    Workflow(
        number=8,
        name="Incident Response & Production Triage",
        problem_type="Production outage",
        primary_skill="root-cause-tracing",
        supporting_skills=["verification-before-completion", "condition-based-waiting"],
        keywords=["incident", "outage", "triage", "rollback", "postmortem",
                   "users affected", "error rate", "latency spike", "service down",
                   "status page", "on-call", "pager"],
        negative_keywords=["data pipeline", "etl", "migration"],
    ),
    Workflow(
        number=9,
        name="Data Pipeline Debugging",
        problem_type="Data quality issues",
        primary_skill="root-cause-tracing",
        supporting_skills=["systematic-debugging", "dispatching-parallel-agents"],
        keywords=["data pipeline", "etl", "elt", "data quality", "missing records",
                   "duplicate records", "schema drift", "transform", "null values",
                   "data corruption", "backfill", "ingestion", "staging table"],
        negative_keywords=[],
    ),
    Workflow(
        number=10,
        name="Agent Evaluation & Comparison",
        problem_type="Model/agent comparison",
        primary_skill="test-driven-development",
        supporting_skills=["verification-before-completion", "dispatching-parallel-agents"],
        keywords=["evaluate", "comparison", "benchmark", "a/b test", "which model",
                   "which agent", "scoring", "rubric", "bandit", "variant",
                   "prompt comparison", "model selection"],
        negative_keywords=[],
    ),
]


def score_workflow(workflow: Workflow, query: str) -> float:
    """Score a workflow against a query string. Higher = better match."""
    query_lower = query.lower()
    score = 0.0

    # Positive keyword matches (weighted by specificity)
    for kw in workflow.keywords:
        if kw in query_lower:
            # Multi-word keywords are more specific → higher weight
            word_count = len(kw.split())
            score += 1.0 * word_count

    # Negative keyword penalties
    for nkw in workflow.negative_keywords:
        if nkw in query_lower:
            score -= 0.5

    return score


def route(query: str, top_n: int = 3) -> list[dict]:
    """Route a problem description to matching workflows."""
    scored = []
    for wf in WORKFLOWS:
        s = score_workflow(wf, query)
        if s > 0:
            scored.append((s, wf))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    for s, wf in scored[:top_n]:
        results.append({
            "workflow": wf.number,
            "name": wf.name,
            "problem_type": wf.problem_type,
            "primary_skill": wf.primary_skill,
            "supporting_skills": wf.supporting_skills,
            "confidence": round(min(s / 4.0, 1.0), 2),  # normalize to 0-1
        })

    # If nothing matched, return generic guidance
    if not results:
        results.append({
            "workflow": 2,
            "name": "TDD-Driven Root Cause Resolution",
            "problem_type": "Unknown — defaulting to TDD root cause",
            "primary_skill": "test-driven-development",
            "supporting_skills": ["root-cause-tracing"],
            "confidence": 0.0,
            "note": "No strong match. Describe: bug, feature, migration, incident, data, or evaluation?",
        })

    return results


def list_workflows() -> list[dict]:
    """List all available workflows."""
    return [
        {
            "workflow": wf.number,
            "name": wf.name,
            "problem_type": wf.problem_type,
            "primary_skill": wf.primary_skill,
        }
        for wf in WORKFLOWS
    ]


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        sys.exit(0)

    if sys.argv[1] == "--list":
        for wf in list_workflows():
            print(f"  [{wf['workflow']:2d}] {wf['name']}")
            print(f"       Type: {wf['problem_type']} | Skill: {wf['primary_skill']}")
        sys.exit(0)

    output_json = False
    query_args = sys.argv[1:]
    if query_args[0] == "--json":
        output_json = True
        query_args = query_args[1:]

    query = " ".join(query_args)
    results = route(query)

    if output_json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\n  Query: \"{query}\"\n")
        for i, r in enumerate(results):
            marker = "→" if i == 0 else " "
            conf_bar = "█" * int(r["confidence"] * 10) + "░" * (10 - int(r["confidence"] * 10))
            print(f"  {marker} Workflow {r['workflow']}: {r['name']}")
            print(f"    Confidence: [{conf_bar}] {r['confidence']}")
            print(f"    Primary:    {r['primary_skill']}")
            print(f"    Supporting: {', '.join(r['supporting_skills'])}")
            if "note" in r:
                print(f"    Note:       {r['note']}")
            print()


if __name__ == "__main__":
    main()

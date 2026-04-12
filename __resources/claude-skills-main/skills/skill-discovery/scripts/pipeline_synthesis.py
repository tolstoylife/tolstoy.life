#!/usr/bin/env python3
"""
Synthesize a pipeline from multiple skills using architectural reasoning
Outputs a homoiconic, Pareto-optimized pipeline representation
"""
import sys
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Tuple


ROLE_ORDER = ["discover", "decide", "design", "build", "verify", "deliver"]
ROLE_KEYWORDS = {
    "discover": ["discover", "explore", "research", "audit", "diagnose", "inspect"],
    "decide": ["decide", "prioritize", "review", "select", "triage", "plan"],
    "design": ["design", "architecture", "pattern", "interface", "model", "blueprint"],
    "build": ["build", "implement", "develop", "refactor", "code", "create"],
    "verify": ["verify", "test", "validate", "debug", "check", "troubleshoot"],
    "deliver": ["deliver", "deploy", "release", "ship", "document", "publish", "finish", "merge", "ci", "cd", "pipeline"],
}

STOPWORDS = {
    "the", "and", "or", "to", "of", "in", "for", "with", "a", "an", "on",
    "by", "from", "is", "are", "be", "this", "that", "as", "it", "its",
    "your", "you", "we", "our", "their", "they", "use", "using", "when",
    "before", "after", "any"
}


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str) -> List[str]:
    return [t for t in normalize_text(text).split() if t and t not in STOPWORDS]


def cosine_similarity(text1: str, text2: str) -> float:
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    if not tokens1 or not tokens2:
        return 0.0
    counter1 = Counter(tokens1)
    counter2 = Counter(tokens2)
    all_words = set(counter1.keys()) | set(counter2.keys())
    dot = sum(counter1[w] * counter2[w] for w in all_words)
    mag1 = math.sqrt(sum(c * c for c in counter1.values()))
    mag2 = math.sqrt(sum(c * c for c in counter2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def parse_date(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        try:
            return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            return None


def skill_text(skill: Dict) -> str:
    return f"{skill.get('name', '')} {skill.get('description', '')}".strip()


def extract_capabilities(skill: Dict, limit: int = 8) -> List[str]:
    tokens = tokenize(skill_text(skill))
    counts = Counter(tokens)
    return [w for w, _ in counts.most_common(limit)]


def classify_role(skill: Dict) -> str:
    text = skill_text(skill)
    tokens = set(tokenize(text))
    best_role = None
    best_score = 0
    for role in ROLE_ORDER:
        score = sum(1 for kw in ROLE_KEYWORDS[role] if kw in tokens)
        if score > best_score:
            best_score = score
            best_role = role
    return best_role if best_role else "build"


def relevance_score(skill: Dict, query: str) -> float:
    if not query:
        return 0.5
    base = cosine_similarity(skill_text(skill), query)
    query_tokens = set(tokenize(query))
    skill_tokens = set(tokenize(skill_text(skill)))
    if "skill" in skill_tokens and "skill" not in query_tokens:
        base *= 0.6
    return base


def popularity_score(skill: Dict, max_downloads: int) -> float:
    downloads = skill.get("downloads")
    if downloads is None:
        return 0.5
    try:
        downloads = max(int(downloads), 0)
    except (TypeError, ValueError):
        return 0.5
    denom = math.log(max_downloads + 1) if max_downloads > 0 else 1
    return math.log(downloads + 1) / denom if denom else 0.5


def recency_score(skill: Dict) -> float:
    date_value = skill.get("last_update") or skill.get("updated_at") or skill.get("updated")
    if not date_value:
        return 0.5
    parsed = parse_date(str(date_value))
    if not parsed:
        return 0.5
    days = (datetime.now(timezone.utc) - parsed).days
    return math.exp(-days / 180.0)


def diversity_score(skill: Dict, selected: List[Dict]) -> float:
    if not selected:
        return 1.0
    sims = [cosine_similarity(skill_text(skill), skill_text(s)) for s in selected]
    max_sim = max(sims) if sims else 0.0
    return 1.0 - max_sim


def pareto_select(skills: List[Dict], query: str, limit: int) -> List[Dict]:
    if not skills:
        return []
    max_downloads = max([s.get("downloads", 0) or 0 for s in skills] + [1])
    selected = []
    remaining = skills[:]
    while remaining and len(selected) < limit:
        scored = []
        for skill in remaining:
            relevance = relevance_score(skill, query)
            if query and relevance < 0.1:
                continue
            score = (
                0.7 * relevance
                + 0.15 * popularity_score(skill, max_downloads)
                + 0.1 * recency_score(skill)
                + 0.05 * diversity_score(skill, selected)
            )
            scored.append((score, skill))
        if not scored and query:
            for skill in remaining:
                relevance = relevance_score(skill, query)
                score = (
                    0.7 * relevance
                    + 0.15 * popularity_score(skill, max_downloads)
                    + 0.1 * recency_score(skill)
                    + 0.05 * diversity_score(skill, selected)
                )
                scored.append((score, skill))
        scored.sort(key=lambda x: x[0], reverse=True)
        if not scored:
            break
        best = scored[0][1]
        selected.append(best)
        remaining = [s for s in remaining if s is not best]
    return selected


def build_pipeline(skills: List[Dict], query: str, limit_per_role: int) -> Dict:
    roles = defaultdict(list)
    for skill in skills:
        roles[classify_role(skill)].append(skill)

    pipeline = []
    selected_global = []
    capability_counts = Counter()
    for skill in skills:
        capability_counts.update(extract_capabilities(skill, limit=5))

    for role in ROLE_ORDER:
        selected = pareto_select(roles.get(role, []), query, limit_per_role)
        selected_global.extend(selected)
        stage_caps = Counter()
        for s in selected:
            stage_caps.update(extract_capabilities(s, limit=5))
        micro = "Focus on " + ", ".join([c for c, _ in stage_caps.most_common(3)]) if selected else "No strong candidates"
        pipeline.append({
            "stage": role,
            "skills": [summarize_skill(s) for s in selected],
            "micro_instruction": micro,
        })

    top_caps = ", ".join([c for c, _ in capability_counts.most_common(5)])
    loop = "discover -> decide -> design -> build -> verify -> deliver"
    meta = f"Run the loop ({loop}) with emphasis on {top_caps}."
    for stage in pipeline:
        stage["holographic_summary"] = f"{stage['stage']}: {stage['micro_instruction']} | loop: {loop}"

    return {
        "pipeline": pipeline,
        "meta_instruction": meta,
        "capability_index": top_caps,
        "input_count": len(skills),
        "selected_count": len(selected_global),
    }


def summarize_skill(skill: Dict) -> Dict:
    return {
        "name": skill.get("name"),
        "identifier": skill.get("identifier"),
        "description": skill.get("description"),
        "downloads": skill.get("downloads"),
    }


def build_synthesized_skill(payload: Dict, query: str) -> Dict:
    slug = re.sub(r"[^a-z0-9]+", "-", normalize_text(query)).strip("-") if query else "pipeline"
    name = f"synth-{slug}" if slug else "synth-pipeline"
    description = f"Synthesized pipeline from {payload['input_count']} skills for '{query}'." if query else f"Synthesized pipeline from {payload['input_count']} skills."
    return {
        "name": name,
        "description": description,
        "stages": payload["pipeline"],
        "meta_instruction": payload["meta_instruction"],
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: pipeline_synthesis.py <skills.json|-> --query='...' [--limit-per-role=2]")
        print("Example: pipeline_synthesis.py results.json --query='improve code quality'")
        sys.exit(1)

    input_file = sys.argv[1]
    query = ""
    limit_per_role = 2

    for arg in sys.argv[2:]:
        if arg.startswith("--query="):
            query = arg.split("=", 1)[1]
        elif arg.startswith("--limit-per-role="):
            limit_per_role = int(arg.split("=", 1)[1])

    try:
        if input_file == "-":
            skills = json.load(sys.stdin)
        else:
            with open(input_file, "r") as f:
                skills = json.load(f)

        if not isinstance(skills, list):
            raise ValueError("Input JSON must be a list of skill objects")

        payload = build_pipeline(skills, query, limit_per_role)
        synthesized = build_synthesized_skill(payload, query)
        output = {
            "synthesized_skill": synthesized,
            "pipeline": payload["pipeline"],
            "meta_instruction": payload["meta_instruction"],
            "capability_index": payload["capability_index"],
            "input_count": payload["input_count"],
            "selected_count": payload["selected_count"],
        }
        print(json.dumps(output, indent=2))

    except FileNotFoundError:
        print(f"❌ File not found: {input_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

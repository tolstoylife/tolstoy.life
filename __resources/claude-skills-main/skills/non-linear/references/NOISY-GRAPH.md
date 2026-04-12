# NoisyGraph Schema Reference

Complete specification for uncertainty-aware knowledge graph scaffolds.

## Design Philosophy

**Core Principle:** Preserve uncertainty rather than hiding it. A deliberately noisy graph with explicit placeholders, low-confidence elements, and represented gaps is more valuable for deep study than a falsely confident structure.

**Why Noise Matters:**
- Represents frontiers of knowledge
- Guides further research by posing explicit questions
- Represents nascent hypotheses that may evolve
- Supports critical, deep study of complex topics

## Complete JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "meta": {
      "type": "object",
      "properties": {
        "mode": {
          "type": "string",
          "description": "Reasoning mode: 'non-linear-reasoning', 'semantic', 'compact'"
        },
        "topic": {
          "type": "string",
          "description": "Primary topic of the scaffold"
        },
        "timestamp_utc": {
          "type": "string",
          "format": "date-time"
        },
        "iteration": {
          "type": "integer",
          "minimum": 0,
          "description": "Current iteration number"
        },
        "noise_budget": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "default": 0.25,
          "description": "Minimum fraction of elements with confidence ≤ 0.5"
        },
        "assumptions": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Explicit assumptions guiding the reasoning"
        },
        "caveats": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Limitations and warnings about the scaffold"
        }
      },
      "required": ["mode", "topic", "timestamp_utc", "iteration", "noise_budget"]
    },
    "core": {
      "type": "object",
      "properties": {
        "entities_and_concepts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "label": {"type": "string"},
              "why_relevant": {"type": "string"},
              "confidence": {"type": "number", "minimum": 0, "maximum": 1}
            },
            "required": ["label", "why_relevant", "confidence"]
          }
        },
        "implied_relationships_and_gaps": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "hint": {"type": "string"},
              "gap": {"type": "string"},
              "provisional_placeholders": {
                "type": "array",
                "items": {"type": "string"}
              }
            },
            "required": ["hint", "gap", "provisional_placeholders"]
          }
        },
        "hypotheses_for_structure": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "rationale": {"type": "string"},
              "placeholders": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "label": {"type": "string"},
                    "reason": {"type": "string"}
                  },
                  "required": ["label", "reason"]
                }
              }
            },
            "required": ["name", "rationale", "placeholders"]
          }
        }
      },
      "required": ["entities_and_concepts", "implied_relationships_and_gaps", "hypotheses_for_structure"]
    },
    "graph": {
      "type": "object",
      "properties": {
        "nodes": {
          "type": "array",
          "items": {"$ref": "#/definitions/node"}
        },
        "edges": {
          "type": "array",
          "items": {"$ref": "#/definitions/edge"}
        }
      },
      "required": ["nodes", "edges"]
    },
    "agents": {
      "type": "array",
      "items": {"$ref": "#/definitions/agent"}
    },
    "graph_question": {
      "type": "array",
      "items": {"$ref": "#/definitions/graphQuestion"}
    },
    "graph_answer": {"$ref": "#/definitions/graphAnswer"},
    "self_correction": {"$ref": "#/definitions/selfCorrection"}
  },
  "required": ["meta", "core", "graph", "agents", "graph_question", "graph_answer", "self_correction"],
  "definitions": {
    "node": {
      "type": "object",
      "properties": {
        "id": {"type": "string"},
        "label": {"type": "string"},
        "description": {"type": "string"},
        "type": {
          "type": "string",
          "enum": ["entity", "concept", "process", "dataset", "claim", "placeholder"]
        },
        "confidence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "constraints": {
          "type": "array",
          "items": {"type": "string"}
        },
        "status": {
          "type": "string",
          "enum": ["new", "updated", "unchanged", "removed"]
        },
        "evidence": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "result_id": {"type": "string"},
              "note": {"type": "string"}
            },
            "required": ["result_id", "note"]
          }
        }
      },
      "required": ["id", "label", "description", "type", "confidence", "status"]
    },
    "edge": {
      "type": "object",
      "properties": {
        "id": {"type": "string"},
        "source": {"type": "string"},
        "target": {"type": "string"},
        "type": {
          "type": "string",
          "enum": ["causes", "correlates_with", "is_a", "part_of", "supports", "contradicts", "similar_to"]
        },
        "description": {"type": "string"},
        "strength": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "evidence": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "result_id": {"type": "string"},
              "note": {"type": "string"}
            },
            "required": ["result_id", "note"]
          }
        },
        "status": {
          "type": "string",
          "enum": ["new", "updated", "unchanged", "removed"]
        }
      },
      "required": ["id", "source", "target", "type", "description", "strength", "status"]
    },
    "agent": {
      "type": "object",
      "properties": {
        "id": {"type": "string"},
        "role": {"type": "string"},
        "goal": {"type": "string"},
        "questions": {
          "type": "array",
          "items": {"type": "string"}
        },
        "notes": {"type": "string"}
      },
      "required": ["id", "role", "goal", "questions"]
    },
    "graphQuestion": {
      "type": "object",
      "properties": {
        "agent_id": {"type": "string"},
        "question": {"type": "string"},
        "why_this_question": {"type": "string"},
        "expected_signal": {
          "type": "string",
          "enum": ["confirm", "disconfirm", "differentiate", "discover_gap", "refine_placeholder_confidence", "select_for_noise_budget"]
        },
        "targets": {
          "type": "object",
          "properties": {
            "node_ids": {"type": "array", "items": {"type": "string"}},
            "edge_ids": {"type": "array", "items": {"type": "string"}}
          },
          "required": ["node_ids", "edge_ids"]
        }
      },
      "required": ["agent_id", "question", "why_this_question", "expected_signal", "targets"]
    },
    "graphAnswer": {
      "type": "object",
      "properties": {
        "q1_what_information_does_the_question_seek": {"type": "string"},
        "q2_what_relevant_data_exists_in_search_results": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "result_id": {"type": "string"},
              "relevance_note": {"type": "string"}
            },
            "required": ["result_id", "relevance_note"]
          }
        },
        "q3_existing_nodes_needing_updates": {
          "type": "array",
          "items": {"type": "string"}
        },
        "q4_nodes_clearly_wrong_or_redundant_to_remove": {
          "type": "array",
          "items": {"type": "string"}
        },
        "q5_new_nodes_or_edges_to_add": {
          "type": "object",
          "properties": {
            "nodes": {"type": "array", "items": {"$ref": "#/definitions/node"}},
            "edges": {"type": "array", "items": {"$ref": "#/definitions/edge"}}
          },
          "required": ["nodes", "edges"]
        },
        "direct_answers": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "graph_question_index": {"type": "integer"},
              "agent_id": {"type": "string"},
              "answer": {"type": "string"},
              "confidence": {"type": "number", "minimum": 0, "maximum": 1}
            },
            "required": ["graph_question_index", "agent_id", "answer", "confidence"]
          }
        }
      },
      "required": ["q1_what_information_does_the_question_seek", "q2_what_relevant_data_exists_in_search_results", "q3_existing_nodes_needing_updates", "q4_nodes_clearly_wrong_or_redundant_to_remove", "q5_new_nodes_or_edges_to_add", "direct_answers"]
    },
    "selfCorrection": {
      "type": "object",
      "properties": {
        "checklist": {
          "type": "array",
          "items": {"type": "string"}
        },
        "issues_found": {
          "type": "array",
          "items": {"type": "string"}
        },
        "actions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "action": {"type": "string", "enum": ["add", "update", "remove"]},
              "target_type": {"type": "string", "enum": ["node", "edge"]},
              "target_id": {"type": "string"},
              "reason": {"type": "string"}
            },
            "required": ["action", "target_type", "target_id", "reason"]
          }
        }
      },
      "required": ["checklist", "issues_found", "actions"]
    }
  }
}
```

## Workflow Per Iteration

### A) Identify Core Entities and Concepts

Extract concise candidates; rate confidence; include low-confidence items to satisfy noise_budget.

```typescript
interface EntityExtraction {
    label: string;           // Compact, meaningful label
    why_relevant: string;    // Rationale for inclusion
    confidence: number;      // 0-1, with some ≤ 0.5
}

// Example
const entities: EntityExtraction[] = [
    { label: "Thermodilution", why_relevant: "Primary CO measurement method", confidence: 0.9 },
    { label: "Indicator dilution", why_relevant: "Theoretical basis", confidence: 0.85 },
    { label: "Cold-induced vasoconstriction", why_relevant: "Potential confounder (uncertain)", confidence: 0.4 }
];
```

### B) Identify Implied Relationships and Gaps

Infer likely relationships and missing links; propose placeholders.

```typescript
interface RelationshipGap {
    hint: string;                      // What suggests this relationship
    gap: string;                       // What is unknown
    provisional_placeholders: string[]; // Candidates for gap filling
}

// Example
const gaps: RelationshipGap[] = [
    {
        hint: "Stewart-Hamilton equation assumes complete mixing",
        gap: "Conditions where mixing assumption fails",
        provisional_placeholders: ["Incomplete mixing factor", "Mixing time variable"]
    }
];
```

### C) Formulate Graph Hypotheses

Offer 1-3 alternative structures with justifications.

```typescript
interface StructureHypothesis {
    name: string;
    rationale: string;
    placeholders: Array<{ label: string; reason: string }>;
}

// Example
const hypotheses: StructureHypothesis[] = [
    {
        name: "Linear causation model",
        rationale: "Temperature injection → dilution curve → CO calculation",
        placeholders: [
            { label: "Temperature measurement error", reason: "Uncertainty in input" },
            { label: "Curve integration method", reason: "Algorithm-dependent" }
        ]
    },
    {
        name: "Feedback model",
        rationale: "CO influences downstream temperature, creating feedback",
        placeholders: [
            { label: "Feedback coefficient", reason: "Magnitude unknown" }
        ]
    }
];
```

### D) Structure the Graph

Create nodes and edges per schema with constraints.

```typescript
function createNode(
    id: string,
    label: string,
    description: string,
    type: NodeType,
    confidence: number,
    evidence?: Evidence[]
): Node {
    return {
        id,
        label,
        description,
        type,
        confidence,
        constraints: inferConstraints(type, description),
        status: "new",
        evidence: evidence || []
    };
}

function createEdge(
    source: string,
    target: string,
    type: EdgeType,
    description: string,
    strength: number,
    evidence?: Evidence[]
): Edge {
    return {
        id: `${source}_${type}_${target}`,
        source,
        target,
        type,
        description,
        strength,
        evidence: evidence || [],
        status: "new"
    };
}
```

### E) Ensure Noisiness and Uncertainty

Maintain noise budget by keeping sufficient low-confidence elements.

```typescript
function enforceNoiseBudget(scaffold: NoisyGraphScaffold): void {
    const { nodes, edges } = scaffold.graph;
    const budget = scaffold.meta.noise_budget;
    
    const totalElements = nodes.length + edges.length;
    const lowConfCount = 
        nodes.filter(n => n.confidence <= 0.5).length +
        edges.filter(e => e.strength <= 0.5).length;
    
    const currentRatio = lowConfCount / totalElements;
    
    if (currentRatio < budget) {
        // Add uncertainty: reduce confidence on least-supported elements
        const needMore = Math.ceil(budget * totalElements) - lowConfCount;
        
        // Sort by evidence count (ascending) and reduce confidence
        const leastSupported = [...nodes]
            .sort((a, b) => (a.evidence?.length || 0) - (b.evidence?.length || 0))
            .slice(0, needMore);
        
        for (const node of leastSupported) {
            node.confidence = Math.min(node.confidence, 0.45);
            node.status = "updated";
            scaffold.self_correction.actions.push({
                action: "update",
                target_type: "node",
                target_id: node.id,
                reason: "Reduced confidence to satisfy noise budget"
            });
        }
    }
}
```

### F) Multi-Agent Questioning

Each agent proposes questions targeting decision-informative uncertainties.

```typescript
function generateAgentQuestions(
    agent: Agent,
    scaffold: NoisyGraphScaffold
): GraphQuestion[] {
    const questions: GraphQuestion[] = [];
    
    switch (agent.id) {
        case "mapper_agent":
            // Focus on entity and relationship extraction
            questions.push({
                agent_id: agent.id,
                question: `What entities from search results connect to ${scaffold.meta.topic}?`,
                why_this_question: "Expand entity coverage",
                expected_signal: "discover_gap",
                targets: { node_ids: [], edge_ids: [] }
            });
            break;
            
        case "skeptic_agent":
            // Challenge high-confidence elements
            const highConf = scaffold.graph.nodes.filter(n => n.confidence > 0.8);
            for (const node of highConf.slice(0, 3)) {
                questions.push({
                    agent_id: agent.id,
                    question: `What evidence would disconfirm ${node.label}?`,
                    why_this_question: "Identify potential falsifiers",
                    expected_signal: "disconfirm",
                    targets: { node_ids: [node.id], edge_ids: [] }
                });
            }
            break;
            
        case "placeholder_generator":
            // Fill identified gaps
            for (const gap of scaffold.core.implied_relationships_and_gaps) {
                questions.push({
                    agent_id: agent.id,
                    question: `What form would fill the gap: ${gap.gap}?`,
                    why_this_question: "Generate provisional placeholder",
                    expected_signal: "discover_gap",
                    targets: { node_ids: [], edge_ids: [] }
                });
            }
            break;
            
        case "uncertainty_quantifier":
            // Assess confidence for new elements
            const newNodes = scaffold.graph.nodes.filter(n => n.status === "new");
            for (const node of newNodes) {
                questions.push({
                    agent_id: agent.id,
                    question: `What confidence does ${node.label} merit given evidence?`,
                    why_this_question: "Calibrate uncertainty",
                    expected_signal: "refine_placeholder_confidence",
                    targets: { node_ids: [node.id], edge_ids: [] }
                });
            }
            break;
            
        case "hypothesizer_agent":
            // Generate structural alternatives
            questions.push({
                agent_id: agent.id,
                question: `What alternative graph structure would explain ${scaffold.meta.topic}?`,
                why_this_question: "Explore structural hypotheses",
                expected_signal: "differentiate",
                targets: { node_ids: [], edge_ids: [] }
            });
            break;
    }
    
    return questions;
}
```

### G) Answering

Process each question through the answer pipeline.

```typescript
function processGraphAnswer(
    question: GraphQuestion,
    evidence: Evidence[],
    scaffold: NoisyGraphScaffold
): GraphAnswer {
    return {
        q1_what_information_does_the_question_seek: question.question,
        q2_what_relevant_data_exists_in_search_results: evidence.map(e => ({
            result_id: e.id,
            relevance_note: e.relevance
        })),
        q3_existing_nodes_needing_updates: findNodesToUpdate(question, scaffold),
        q4_nodes_clearly_wrong_or_redundant_to_remove: findNodesToRemove(question, scaffold),
        q5_new_nodes_or_edges_to_add: generateNewElements(question, evidence, scaffold),
        direct_answers: [{
            graph_question_index: 0,
            agent_id: question.agent_id,
            answer: synthesizeAnswer(question, evidence),
            confidence: estimateConfidence(evidence)
        }]
    };
}
```

### H) Self-Correct

Run checklist and log corrections.

```typescript
const SELF_CORRECTION_CHECKLIST = [
    "Duplicate labels merged or made distinct?",
    "Any edge without both endpoints?",
    "Any claim without at least one possible falsifier?",
    "Noise budget respected (≥25% low-confidence elements)?",
    "Contradictions explicitly represented (contradicts edges)?",
    "Evidence provenance preserved (result_ids linked)?",
    "Topology target met (|E|/|N| ≥ 4)?"
];

function runSelfCorrection(scaffold: NoisyGraphScaffold): void {
    scaffold.self_correction.checklist = SELF_CORRECTION_CHECKLIST;
    scaffold.self_correction.issues_found = [];
    scaffold.self_correction.actions = [];
    
    // Check 1: Duplicate labels
    const labels = scaffold.graph.nodes.map(n => n.label);
    const duplicates = labels.filter((l, i) => labels.indexOf(l) !== i);
    if (duplicates.length > 0) {
        scaffold.self_correction.issues_found.push(`Duplicate labels: ${duplicates.join(', ')}`);
        // Merge or distinguish
        for (const dup of [...new Set(duplicates)]) {
            const dupeNodes = scaffold.graph.nodes.filter(n => n.label === dup);
            for (let i = 1; i < dupeNodes.length; i++) {
                dupeNodes[i].label = `${dup} (${i + 1})`;
                scaffold.self_correction.actions.push({
                    action: "update",
                    target_type: "node",
                    target_id: dupeNodes[i].id,
                    reason: `Renamed duplicate label to '${dupeNodes[i].label}'`
                });
            }
        }
    }
    
    // Check 2: Dangling edges
    const nodeIds = new Set(scaffold.graph.nodes.map(n => n.id));
    const danglingEdges = scaffold.graph.edges.filter(
        e => !nodeIds.has(e.source) || !nodeIds.has(e.target)
    );
    if (danglingEdges.length > 0) {
        scaffold.self_correction.issues_found.push(`Dangling edges: ${danglingEdges.map(e => e.id).join(', ')}`);
        for (const edge of danglingEdges) {
            edge.status = "removed";
            scaffold.self_correction.actions.push({
                action: "remove",
                target_type: "edge",
                target_id: edge.id,
                reason: "Endpoint node not found"
            });
        }
    }
    
    // Check 3: Falsifiability
    const unfalsifiable = scaffold.graph.nodes.filter(
        n => n.type === "claim" && !scaffold.graph.edges.some(
            e => e.target === n.id && e.type === "contradicts"
        )
    );
    if (unfalsifiable.length > 0) {
        scaffold.self_correction.issues_found.push(`Claims without falsifiers: ${unfalsifiable.map(n => n.label).join(', ')}`);
        // Add placeholder contradicts edge
        for (const claim of unfalsifiable) {
            const falsifier: Node = {
                id: `falsifier_${claim.id}`,
                label: `[FALSIFIER] ${claim.label}`,
                description: `Potential falsifying evidence for ${claim.label}`,
                type: "placeholder",
                confidence: 0.2,
                status: "new"
            };
            scaffold.graph.nodes.push(falsifier);
            scaffold.graph.edges.push({
                id: `contradicts_${claim.id}`,
                source: falsifier.id,
                target: claim.id,
                type: "contradicts",
                description: "Potential disconfirmation",
                strength: 0.3,
                status: "new"
            });
        }
    }
    
    // Check 4: Noise budget
    enforceNoiseBudget(scaffold);
    
    // Check 5: Topology
    const ratio = scaffold.graph.edges.length / scaffold.graph.nodes.length;
    if (ratio < 4.0) {
        scaffold.self_correction.issues_found.push(`Topology ratio ${ratio.toFixed(2)} < 4.0 target`);
    }
}
```

### I) Prepare for Recursion

Check stopping conditions.

```typescript
function shouldContinue(scaffold: NoisyGraphScaffold): boolean {
    const { iteration } = scaffold.meta;
    const { iteration_limit } = DEFAULT_CONFIG;
    
    // Condition 1: Under iteration limit
    if (iteration >= iteration_limit) {
        return false;
    }
    
    // Condition 2: Material changes in last iteration
    const materialChanges = scaffold.graph.nodes.some(n => n.status !== "unchanged") ||
                           scaffold.graph.edges.some(e => e.status !== "unchanged");
    
    // Condition 3: Noise budget and uncertainty representation
    const noiseSatisfied = checkNoiseBudget(scaffold).satisfied;
    const uncertaintiesRepresented = scaffold.core.implied_relationships_and_gaps
        .every(gap => gap.provisional_placeholders.length > 0);
    
    return materialChanges && (!noiseSatisfied || !uncertaintiesRepresented);
}
```

## Topology Targets

| Metric | Target | Rationale |
|--------|--------|-----------|
| Edge-to-Node Ratio | ≥ 4.0 | Dense connectivity enables emergence |
| Min Nodes (R2) | 5 | Sufficient concept coverage |
| Min Nodes (R3) | 10 | Complex topic representation |
| Min Edges (R2) | 20 | Relationship richness |
| Min Edges (R3) | 40 | Comprehensive structure |
| Max Nodes | 60 | Context window constraints |
| Max Edges | 240 | Manageable complexity |

## Confidence Calibration

```typescript
const CONFIDENCE_GUIDELINES = {
    // Very high: Multiple peer-reviewed sources agree
    0.95: "Strong consensus with multiple independent confirmations",
    
    // High: Peer-reviewed or authoritative source
    0.85: "Single authoritative source or expert consensus",
    
    // Medium-high: Credible source with some support
    0.70: "Credible non-peer-reviewed source with corroboration",
    
    // Medium: Reasonable inference
    0.55: "Logical inference from established facts",
    
    // Medium-low: Plausible but unverified
    0.45: "Plausible hypothesis without direct evidence",
    
    // Low: Speculative placeholder
    0.30: "Speculative placeholder for identified gap",
    
    // Very low: Pure speculation
    0.15: "Highly speculative, minimal evidentiary basis"
};
```

## Edge Strength Calibration

```typescript
const STRENGTH_GUIDELINES = {
    // Very strong: Causal mechanism established
    0.95: "Causal mechanism experimentally verified",
    
    // Strong: Strong evidence
    0.80: "Consistent correlational evidence with theoretical basis",
    
    // Medium-strong: Good evidence
    0.65: "Multiple correlational studies support",
    
    // Medium: Some evidence
    0.50: "Single study or theoretical argument supports",
    
    // Medium-weak: Weak evidence
    0.35: "Anecdotal or theoretical suggestion",
    
    // Weak: Very weak evidence
    0.20: "Speculative connection based on domain similarity",
    
    // Very weak: Placeholder
    0.10: "Placeholder for potential relationship"
};
```

## Example Scaffold

```json
{
  "meta": {
    "mode": "non-linear-reasoning",
    "topic": "Cardiac output measurement via thermodilution",
    "timestamp_utc": "2025-12-07T10:30:00Z",
    "iteration": 2,
    "noise_budget": 0.25,
    "assumptions": [
      "Stewart-Hamilton equation accurately models indicator dilution",
      "Temperature measurement is sufficiently accurate"
    ],
    "caveats": [
      "Clinical conditions may violate assumptions",
      "Some relationships are provisional pending evidence"
    ]
  },
  "core": {
    "entities_and_concepts": [
      {"label": "Thermodilution", "why_relevant": "Primary measurement method", "confidence": 0.95},
      {"label": "Stewart-Hamilton equation", "why_relevant": "Mathematical basis", "confidence": 0.90},
      {"label": "Cold injectate bolus", "why_relevant": "Standard indicator", "confidence": 0.85},
      {"label": "Incomplete mixing", "why_relevant": "Potential error source", "confidence": 0.40}
    ],
    "implied_relationships_and_gaps": [
      {
        "hint": "Equation assumes complete mixing in RV",
        "gap": "Conditions where mixing assumption fails",
        "provisional_placeholders": ["Mixing efficiency coefficient", "RV dysfunction marker"]
      }
    ],
    "hypotheses_for_structure": [
      {
        "name": "Linear signal flow",
        "rationale": "Injection → measurement → calculation → output",
        "placeholders": [
          {"label": "Signal noise factor", "reason": "Measurement uncertainty"}
        ]
      }
    ]
  },
  "graph": {
    "nodes": [
      {
        "id": "n001",
        "label": "Thermodilution",
        "description": "Method measuring CO via temperature-time curve integration",
        "type": "process",
        "confidence": 0.95,
        "constraints": ["Requires PAC placement", "Assumes complete mixing"],
        "status": "unchanged",
        "evidence": [{"result_id": "r001", "note": "Standard clinical method"}]
      },
      {
        "id": "n002",
        "label": "Stewart-Hamilton equation",
        "description": "CO = V_i × (T_b - T_i) / ∫ΔT(t)dt",
        "type": "concept",
        "confidence": 0.90,
        "status": "unchanged",
        "evidence": [{"result_id": "r002", "note": "Classic indicator dilution theory"}]
      },
      {
        "id": "n003",
        "label": "[PLACEHOLDER] Mixing efficiency",
        "description": "Factor representing incomplete mixing in RV",
        "type": "placeholder",
        "confidence": 0.35,
        "status": "new"
      }
    ],
    "edges": [
      {
        "id": "e001",
        "source": "n002",
        "target": "n001",
        "type": "supports",
        "description": "Provides mathematical basis",
        "strength": 0.90,
        "status": "unchanged",
        "evidence": [{"result_id": "r002", "note": "Derivation from S-H"}]
      },
      {
        "id": "e002",
        "source": "n003",
        "target": "n001",
        "type": "correlates_with",
        "description": "May affect measurement accuracy",
        "strength": 0.40,
        "status": "new"
      }
    ]
  },
  "agents": [
    {
      "id": "mapper_agent",
      "role": "Entity extraction",
      "goal": "Identify key concepts",
      "questions": ["What are primary measurement components?"]
    },
    {
      "id": "skeptic_agent",
      "role": "Challenge assumptions",
      "goal": "Surface uncertainty",
      "questions": ["What assumptions may fail clinically?"]
    }
  ],
  "graph_question": [],
  "graph_answer": {},
  "self_correction": {
    "checklist": [],
    "issues_found": [],
    "actions": []
  }
}
```

## Integration Points

### With Think Skill

- Use `thoughtbox` for reasoning about graph structure
- Use `mental_models` for selecting analysis frameworks
- Use `notebook` for validation code execution

### With Agent-Core

- Emit events for graph modifications
- Subscribe to external evidence events
- Coordinate subagent lifecycle

### With MCP Tools

- `infranodus` for gap detection
- `exa` for current information
- `Scholar Gateway` for academic evidence

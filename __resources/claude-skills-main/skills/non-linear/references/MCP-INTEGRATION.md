# MCP Integration Reference

Detailed patterns for coordinating MCP tools within NLR recursive loops.

## Tool Inventory

### Primary Reasoning Tools (think skill)

| Tool | Purpose | Call Pattern |
|------|---------|--------------|
| `think:thoughtbox` | Extended step reasoning | Per-step reflection |
| `think:mental_models` | Structured schemas | Framework selection |
| `think:notebook` | Executable validation | Code verification |

### Evidence Gathering Tools

| Tool | Purpose | Call Pattern |
|------|---------|--------------|
| `infranodus:getGraphAndAdvice` | Graph analysis + gap detection | Each iteration |
| `infranodus:getGraphAndStatements` | Extract knowledge graph | Initial mapping |
| `exa:web_search_exa` | Current web information | As needed |
| `exa:get_code_context_exa` | Code documentation | Technical queries |
| `Scholar Gateway:semanticSearch` | Academic literature | Research queries |

### Reasoning Enhancement Tools

| Tool | Purpose | Call Pattern |
|------|---------|--------------|
| `atom-of-thoughts:AoT` | Deep atomic reasoning | Complex decomposition |
| `atom-of-thoughts:AoT-light` | Quick atomic reasoning | Time-sensitive |
| `context7:get-library-docs` | Library documentation | Technical implementation |

## Tool Coordination Patterns

### Pattern 1: Parallel Evidence Gathering

Execute multiple MCP tools concurrently for efficient evidence collection:

```typescript
async function gatherEvidence(questions: GraphQuestion[]): Promise<Evidence[]> {
    // Classify questions by tool affinity
    const webQuestions = questions.filter(q => q.needs_current_info);
    const academicQuestions = questions.filter(q => q.needs_scholarly);
    const graphQuestions = questions.filter(q => q.needs_structure);
    
    // Parallel execution
    const [webResults, scholarResults, graphResults] = await Promise.all([
        // Web search for current information
        webQuestions.length > 0 
            ? exa.web_search_exa({
                query: synthesizeQuery(webQuestions),
                numResults: 8,
                type: "deep"
              })
            : Promise.resolve(null),
        
        // Academic search for scholarly evidence
        academicQuestions.length > 0
            ? scholarGateway.semanticSearch({
                query: synthesizeQuery(academicQuestions),
                topN: 10,
                start_year: 2020
              })
            : Promise.resolve(null),
        
        // Graph analysis for structural insights
        graphQuestions.length > 0
            ? infranodus.getGraphAndAdvice({
                text: scaffold.meta.topic,
                name: "nlr_analysis",
                optimize: "gaps",
                doNotSave: true,
                extendedGraphSummary: true
              })
            : Promise.resolve(null)
    ]);
    
    return mergeEvidence(webResults, scholarResults, graphResults);
}
```

### Pattern 2: Sequential Reasoning Chain

Chain tools for progressive understanding:

```typescript
async function sequentialReasoningChain(query: string, scaffold: NoisyGraphScaffold) {
    // Step 1: Initial understanding via thoughtbox
    const understanding = await thoughtbox({
        thought: `Initial decomposition of: ${query}`,
        thoughtNumber: 1,
        totalThoughts: 5,
        nextThoughtNeeded: true,
        includeGuide: true
    });
    
    // Step 2: Get relevant mental model
    const model = await mental_models({
        operation: "get_model",
        args: { model: selectModel(query) }  // e.g., "decomposition", "five-whys"
    });
    
    // Step 3: Apply model in next thought
    const application = await thoughtbox({
        thought: `Applying ${model.name}: ${applyModel(model, query)}`,
        thoughtNumber: 2,
        totalThoughts: 5,
        nextThoughtNeeded: true
    });
    
    // Step 4: Gather external evidence
    const evidence = await infranodus.getGraphAndAdvice({
        text: extractClaims(application),
        name: "evidence_graph",
        optimize: "develop",
        doNotSave: true
    });
    
    // Step 5: Synthesize in final thought
    const synthesis = await thoughtbox({
        thought: `Synthesis with evidence: ${integrate(application, evidence)}`,
        thoughtNumber: 3,
        totalThoughts: 5,
        nextThoughtNeeded: true
    });
    
    return { understanding, model, application, evidence, synthesis };
}
```

### Pattern 3: Interleaved Reasoning-Action

Alternate between reasoning (think) and action (MCP tools):

```typescript
async function interleavedLoop(scaffold: NoisyGraphScaffold): Promise<void> {
    for (let i = 0; i < scaffold.meta.iteration_limit; i++) {
        // REASON: Use thoughtbox for current state analysis
        await thoughtbox({
            thought: `Iteration ${i}: Analyzing ${scaffold.graph.nodes.length} nodes, ${scaffold.graph.edges.length} edges`,
            thoughtNumber: i * 2 + 1,
            totalThoughts: scaffold.meta.iteration_limit * 2,
            nextThoughtNeeded: true
        });
        
        // ACT: Query infranodus for gap analysis
        const gaps = await infranodus.getGraphAndAdvice({
            text: serializeGraph(scaffold.graph),
            name: `iteration_${i}`,
            optimize: "gaps",
            gapDepth: i % 4,  // Cycle through gap depths
            doNotSave: true
        });
        
        // REASON: Process gaps
        await thoughtbox({
            thought: `Gap analysis: Found ${gaps.advice?.gaps?.length || 0} structural gaps`,
            thoughtNumber: i * 2 + 2,
            totalThoughts: scaffold.meta.iteration_limit * 2,
            nextThoughtNeeded: i < scaffold.meta.iteration_limit - 1
        });
        
        // UPDATE: Integrate gaps into scaffold
        integrateGaps(scaffold, gaps);
    }
}
```

## InfraNodus Integration

### getGraphAndAdvice Configuration

```typescript
interface InfranodusAdviceConfig {
    text: string;              // Text to analyze
    name: string;              // Graph name
    optimize: OptimizeMode;    // Strategy selection
    doNotSave: boolean;        // Don't persist graph
    gapDepth: number;          // 0-3, deeper explores periphery
    extendedAdvice: boolean;   // Multiple gap analysis
    extendedGraphSummary: boolean;  // Detailed topology
    pinnedNodes?: string[];    // Focus on specific nodes
}

type OptimizeMode = 
    | "develop"   // Balance exploration and reinforcement
    | "reinforce" // Strengthen existing connections
    | "gaps"      // Focus on structural gaps
    | "imagine"   // Creative extrapolation
    | "latent";   // Hidden pattern detection
```

### Using InfraNodus Results

```typescript
async function processInfranodusResults(
    result: InfranodusResult,
    scaffold: NoisyGraphScaffold
): Promise<void> {
    // Extract top concepts for node candidates
    if (result.graph?.attributes?.top_nodes) {
        for (const node of result.graph.attributes.top_nodes) {
            scaffold.graph.nodes.push({
                id: `infra_${node.key}`,
                label: node.label,
                description: `InfraNodus importance: ${node.value}`,
                type: "concept",
                confidence: normalizeImportance(node.value),
                status: "new",
                evidence: [{ result_id: "infranodus", note: `Centrality: ${node.value}` }]
            });
        }
    }
    
    // Extract gaps for placeholder generation
    if (result.graph?.attributes?.gaps) {
        for (const gap of result.graph.attributes.gaps) {
            scaffold.graph.nodes.push({
                id: `gap_${gap.id}`,
                label: `[GAP] ${gap.between?.join(' ↔ ')}`,
                description: gap.description || "Structural gap identified",
                type: "placeholder",
                confidence: 0.3,  // Low confidence by design
                status: "new"
            });
        }
    }
    
    // Extract clusters for relationship patterns
    if (result.graph?.attributes?.top_clusters) {
        for (let i = 0; i < result.graph.attributes.top_clusters.length - 1; i++) {
            const clusterA = result.graph.attributes.top_clusters[i];
            const clusterB = result.graph.attributes.top_clusters[i + 1];
            
            scaffold.graph.edges.push({
                id: `cluster_edge_${i}`,
                source: clusterA.nodes[0],
                target: clusterB.nodes[0],
                type: "correlates_with",
                description: "Inter-cluster connection",
                strength: 0.5,
                status: "new"
            });
        }
    }
}
```

### Optimize Mode Selection

```typescript
function selectOptimizeMode(
    iteration: number,
    scaffold: NoisyGraphScaffold
): OptimizeMode {
    const noiseStatus = checkNoiseBudget(scaffold);
    const topology = calculateTopology(scaffold);
    
    // Early iterations: explore broadly
    if (iteration < 3) {
        return "develop";
    }
    
    // Noise budget not met: find gaps
    if (!noiseStatus.satisfied) {
        return "gaps";
    }
    
    // Sparse graph: reinforce connections
    if (topology.ratio < 4.0) {
        return "reinforce";
    }
    
    // Late iterations: explore hidden patterns
    if (iteration >= scaffold.meta.iteration_limit - 2) {
        return "latent";
    }
    
    return "develop";
}
```

## Exa Integration

### Web Search Pattern

```typescript
async function searchCurrentInformation(
    questions: GraphQuestion[]
): Promise<WebEvidence[]> {
    const results = await exa.web_search_exa({
        query: synthesizeSearchQuery(questions),
        numResults: 8,
        type: "deep",
        livecrawl: "fallback"
    });
    
    return results.results.map(r => ({
        source: r.url,
        title: r.title,
        content: r.text,
        date: r.publishedDate,
        relevance: r.score
    }));
}
```

### Code Context Pattern

```typescript
async function getCodeDocumentation(
    technical_query: string
): Promise<CodeEvidence> {
    return await exa.get_code_context_exa({
        query: technical_query,
        tokensNum: 5000
    });
}
```

## Scholar Gateway Integration

### Academic Search Pattern

```typescript
async function searchAcademicLiterature(
    research_query: string,
    constraints?: { start_year?: number; end_year?: number }
): Promise<AcademicEvidence[]> {
    const results = await scholarGateway.semanticSearch({
        query: research_query,
        topN: 10,
        start_year: constraints?.start_year,
        end_year: constraints?.end_year
    });
    
    return results.map(r => ({
        title: r.title,
        authors: r.authors,
        year: r.year,
        doi: r.doi,
        abstract: r.abstract,
        content: r.chunk_text,
        confidence: 0.8  // Higher baseline for peer-reviewed
    }));
}
```

## Think Skill Deep Integration

### Thoughtbox Patterns

```typescript
// Pattern A: Forward reasoning (default)
async function forwardReasoning(steps: string[]): Promise<void> {
    for (let i = 0; i < steps.length; i++) {
        await thoughtbox({
            thought: steps[i],
            thoughtNumber: i + 1,
            totalThoughts: steps.length,
            nextThoughtNeeded: i < steps.length - 1
        });
    }
}

// Pattern B: Backward reasoning (goal-directed)
async function backwardReasoning(goal: string, prerequisites: string[]): Promise<void> {
    const total = prerequisites.length + 1;
    
    // Start with goal
    await thoughtbox({
        thought: `Goal: ${goal}`,
        thoughtNumber: total,
        totalThoughts: total,
        nextThoughtNeeded: true
    });
    
    // Work backwards through prerequisites
    for (let i = prerequisites.length - 1; i >= 0; i--) {
        await thoughtbox({
            thought: `Prerequisite ${i + 1}: ${prerequisites[i]}`,
            thoughtNumber: i + 1,
            totalThoughts: total,
            nextThoughtNeeded: i > 0
        });
    }
}

// Pattern C: Branching for alternatives
async function branchingReasoning(
    base: string,
    alternatives: string[]
): Promise<void> {
    // Base thought
    await thoughtbox({
        thought: base,
        thoughtNumber: 1,
        totalThoughts: alternatives.length + 1,
        nextThoughtNeeded: true
    });
    
    // Branch for each alternative
    for (let i = 0; i < alternatives.length; i++) {
        await thoughtbox({
            thought: alternatives[i],
            thoughtNumber: 2,
            totalThoughts: alternatives.length + 1,
            branchFromThought: 1,
            branchId: `alt_${i}`,
            nextThoughtNeeded: i < alternatives.length - 1
        });
    }
}

// Pattern D: Revision for self-correction
async function revisionReasoning(
    original: string,
    revision: string,
    originalThought: number
): Promise<void> {
    await thoughtbox({
        thought: revision,
        thoughtNumber: originalThought,
        totalThoughts: originalThought,
        isRevision: true,
        revisesThought: originalThought,
        nextThoughtNeeded: false
    });
}
```

### Mental Models Selection

```typescript
function selectMentalModel(queryType: QueryType): string {
    const modelMap: Record<QueryType, string> = {
        "debugging": "five-whys",
        "risk": "pre-mortem",
        "decision": "trade-off-matrix",
        "estimation": "fermi-estimation",
        "abstraction": "abstraction-laddering",
        "decomposition": "decomposition",
        "adversarial": "adversarial-thinking",
        "constraints": "constraint-relaxation",
        "temporal": "time-horizon-shifting",
        "prioritization": "impact-effort-grid",
        "inverse": "inversion",
        "assumptions": "assumption-surfacing",
        "steelman": "steelmanning",
        "opportunity": "opportunity-cost",
        "rubber_duck": "rubber-duck"
    };
    
    return modelMap[queryType] || "decomposition";
}

// Usage
const model = await mental_models({
    operation: "get_model",
    args: { model: selectMentalModel(classifyQuery(query)) }
});
```

### Notebook Validation

```typescript
async function createValidationNotebook(
    scaffold: NoisyGraphScaffold
): Promise<string> {
    // Create notebook
    const nb = await notebook({
        operation: "create",
        args: {
            title: `NLR Validation: ${scaffold.meta.topic}`,
            language: "typescript"
        }
    });
    
    // Add validation cell
    await notebook({
        operation: "add_cell",
        args: {
            notebookId: nb.notebookId,
            cellType: "code",
            content: generateValidationCode(scaffold),
            filename: "validate.ts"
        }
    });
    
    // Execute validation
    const result = await notebook({
        operation: "run_cell",
        args: {
            notebookId: nb.notebookId,
            cellId: nb.cells[0].id
        }
    });
    
    return result.output;
}

function generateValidationCode(scaffold: NoisyGraphScaffold): string {
    return `
// NLR Scaffold Validation
const scaffold = ${JSON.stringify(scaffold, null, 2)};

// Check topology target
const nodeCount = scaffold.graph.nodes.length;
const edgeCount = scaffold.graph.edges.length;
const ratio = edgeCount / nodeCount;
console.log(\`Topology ratio: \${ratio.toFixed(2)} (target: >= 4.0)\`);

// Check noise budget
const lowConfNodes = scaffold.graph.nodes.filter(n => n.confidence <= 0.5).length;
const lowConfEdges = scaffold.graph.edges.filter(e => e.strength <= 0.5).length;
const noiseRatio = (lowConfNodes + lowConfEdges) / (nodeCount + edgeCount);
console.log(\`Noise ratio: \${(noiseRatio * 100).toFixed(1)}% (target: >= 25%)\`);

// Check edge integrity
const nodeIds = new Set(scaffold.graph.nodes.map(n => n.id));
const danglingEdges = scaffold.graph.edges.filter(
    e => !nodeIds.has(e.source) || !nodeIds.has(e.target)
);
console.log(\`Dangling edges: \${danglingEdges.length}\`);

// Summary
const valid = ratio >= 4.0 && noiseRatio >= 0.25 && danglingEdges.length === 0;
console.log(\`Validation: \${valid ? 'PASSED' : 'FAILED'}\`);
`;
}
```

## Atom of Thoughts Integration

For deep decomposition requiring atomic verification:

```typescript
async function atomicReasoning(claim: string): Promise<AtomResult> {
    // Premise atoms
    const p1 = await AoT({
        atomId: "P1",
        atomType: "premise",
        content: extractPremise(claim, 1),
        dependencies: [],
        confidence: 0.9
    });
    
    const p2 = await AoT({
        atomId: "P2",
        atomType: "premise",
        content: extractPremise(claim, 2),
        dependencies: [],
        confidence: 0.85
    });
    
    // Reasoning atom
    const r1 = await AoT({
        atomId: "R1",
        atomType: "reasoning",
        content: `If ${p1.content} and ${p2.content}, then...`,
        dependencies: ["P1", "P2"],
        confidence: 0.8
    });
    
    // Hypothesis
    const h1 = await AoT({
        atomId: "H1",
        atomType: "hypothesis",
        content: deriveHypothesis(r1),
        dependencies: ["R1"],
        confidence: 0.7
    });
    
    // Verification
    const v1 = await AoT({
        atomId: "V1",
        atomType: "verification",
        content: `Testing H1 against evidence...`,
        dependencies: ["H1"],
        confidence: 0.75,
        isVerified: true
    });
    
    // Conclusion
    const c1 = await AoT({
        atomId: "C1",
        atomType: "conclusion",
        content: synthesizeConclusion(v1),
        dependencies: ["V1"],
        confidence: v1.confidence
    });
    
    return c1;
}
```

## Error Handling

```typescript
class MCPToolError extends Error {
    constructor(
        public tool: string,
        public originalError: Error,
        public recoverable: boolean
    ) {
        super(`MCP tool ${tool} failed: ${originalError.message}`);
    }
}

async function safeToolCall<T>(
    toolName: string,
    call: () => Promise<T>,
    fallback?: T
): Promise<T | null> {
    try {
        return await call();
    } catch (error) {
        const mcpError = new MCPToolError(
            toolName,
            error as Error,
            fallback !== undefined
        );
        
        // Log error for debugging
        console.error(`[NLR] ${mcpError.message}`);
        
        // Return fallback if available
        if (fallback !== undefined) {
            return fallback;
        }
        
        // Otherwise propagate
        throw mcpError;
    }
}

// Usage
const results = await safeToolCall(
    "infranodus:getGraphAndAdvice",
    () => infranodus.getGraphAndAdvice({...}),
    { advice: null, graph: null }  // Fallback
);
```

## Rate Limiting and Batching

```typescript
const RATE_LIMITS = {
    exa: { calls: 10, window: 60000 },          // 10 per minute
    infranodus: { calls: 20, window: 60000 },   // 20 per minute
    scholarGateway: { calls: 30, window: 60000 } // 30 per minute
};

class RateLimiter {
    private callLog: Map<string, number[]> = new Map();
    
    async throttle(tool: string): Promise<void> {
        const limit = RATE_LIMITS[tool];
        if (!limit) return;
        
        const now = Date.now();
        const calls = this.callLog.get(tool) || [];
        const recentCalls = calls.filter(t => now - t < limit.window);
        
        if (recentCalls.length >= limit.calls) {
            const waitTime = limit.window - (now - recentCalls[0]);
            await sleep(waitTime);
        }
        
        this.callLog.set(tool, [...recentCalls, now]);
    }
}
```

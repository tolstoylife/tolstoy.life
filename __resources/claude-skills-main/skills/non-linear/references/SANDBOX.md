# Sandbox Execution Reference

Patterns for code execution, validation, and computational verification within NLR.

## Execution Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SANDBOX EXECUTION                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   NOTEBOOK MANAGER                       │    │
│  │   create | add_cell | update_cell | run_cell | export   │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────────────┐    │
│  │                  EXECUTION ENGINE                        │    │
│  │        TypeScript/JavaScript runtime (Node.js)          │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────────────┐    │
│  │                 VALIDATION PIPELINE                      │    │
│  │   Topology | Noise Budget | Integrity | Self-Correction │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Notebook Operations

### Create Notebook

```typescript
const notebookResponse = await notebook({
    operation: "create",
    args: {
        title: `NLR Validation: ${scaffold.meta.topic}`,
        language: "typescript"  // Use TypeScript for type safety
    }
});

const notebookId = notebookResponse.notebookId;
```

### Add Validation Cell

```typescript
await notebook({
    operation: "add_cell",
    args: {
        notebookId: notebookId,
        cellType: "code",
        content: generateValidationCode(scaffold),
        filename: "validate.ts"
    }
});
```

### Execute Cell

```typescript
const result = await notebook({
    operation: "run_cell",
    args: {
        notebookId: notebookId,
        cellId: cellId
    }
});

// Parse results
const validationOutput = parseValidationOutput(result.output);
```

### Install Dependencies

```typescript
await notebook({
    operation: "install_deps",
    args: {
        notebookId: notebookId,
        packages: ["lodash", "mathjs"]  // If needed
    }
});
```

## Validation Code Templates

### Template 1: Topology Validation

```typescript
// topology_validation.ts
interface Node {
    id: string;
    confidence: number;
}

interface Edge {
    id: string;
    source: string;
    target: string;
    strength: number;
}

interface ValidationResult {
    passed: boolean;
    metrics: {
        nodeCount: number;
        edgeCount: number;
        ratio: number;
        targetRatio: number;
    };
    issues: string[];
}

function validateTopology(nodes: Node[], edges: Edge[], targetRatio: number = 4.0): ValidationResult {
    const nodeCount = nodes.length;
    const edgeCount = edges.length;
    const ratio = nodeCount > 0 ? edgeCount / nodeCount : 0;
    
    const issues: string[] = [];
    
    if (ratio < targetRatio) {
        issues.push(`Edge-to-node ratio ${ratio.toFixed(2)} below target ${targetRatio}`);
    }
    
    if (nodeCount < 5) {
        issues.push(`Node count ${nodeCount} below minimum 5`);
    }
    
    if (edgeCount < 20) {
        issues.push(`Edge count ${edgeCount} below minimum 20`);
    }
    
    return {
        passed: issues.length === 0,
        metrics: { nodeCount, edgeCount, ratio, targetRatio },
        issues
    };
}

// Execute with scaffold data
const scaffold = ${JSON.stringify(scaffold)};
const result = validateTopology(scaffold.graph.nodes, scaffold.graph.edges);
console.log(JSON.stringify(result, null, 2));
```

### Template 2: Noise Budget Validation

```typescript
// noise_budget_validation.ts
interface NoiseBudgetResult {
    satisfied: boolean;
    current: number;
    target: number;
    deficit: number;
    lowConfidenceNodes: string[];
    lowStrengthEdges: string[];
}

function validateNoiseBudget(
    nodes: Node[],
    edges: Edge[],
    targetBudget: number = 0.25
): NoiseBudgetResult {
    const lowConfNodes = nodes.filter(n => n.confidence <= 0.5);
    const lowStrengthEdges = edges.filter(e => e.strength <= 0.5);
    
    const totalElements = nodes.length + edges.length;
    const lowConfCount = lowConfNodes.length + lowStrengthEdges.length;
    const currentRatio = totalElements > 0 ? lowConfCount / totalElements : 0;
    
    return {
        satisfied: currentRatio >= targetBudget,
        current: currentRatio,
        target: targetBudget,
        deficit: Math.max(0, targetBudget - currentRatio),
        lowConfidenceNodes: lowConfNodes.map(n => n.id),
        lowStrengthEdges: lowStrengthEdges.map(e => e.id)
    };
}

// Execute
const scaffold = ${JSON.stringify(scaffold)};
const result = validateNoiseBudget(
    scaffold.graph.nodes,
    scaffold.graph.edges,
    scaffold.meta.noise_budget
);
console.log(JSON.stringify(result, null, 2));
```

### Template 3: Edge Integrity Validation

```typescript
// edge_integrity_validation.ts
interface IntegrityResult {
    valid: boolean;
    danglingEdges: Array<{
        edgeId: string;
        missingNode: string;
        position: 'source' | 'target';
    }>;
    orphanNodes: string[];
}

function validateEdgeIntegrity(nodes: Node[], edges: Edge[]): IntegrityResult {
    const nodeIds = new Set(nodes.map(n => n.id));
    const connectedNodeIds = new Set<string>();
    
    const danglingEdges: IntegrityResult['danglingEdges'] = [];
    
    for (const edge of edges) {
        if (!nodeIds.has(edge.source)) {
            danglingEdges.push({
                edgeId: edge.id,
                missingNode: edge.source,
                position: 'source'
            });
        } else {
            connectedNodeIds.add(edge.source);
        }
        
        if (!nodeIds.has(edge.target)) {
            danglingEdges.push({
                edgeId: edge.id,
                missingNode: edge.target,
                position: 'target'
            });
        } else {
            connectedNodeIds.add(edge.target);
        }
    }
    
    const orphanNodes = nodes
        .filter(n => !connectedNodeIds.has(n.id))
        .map(n => n.id);
    
    return {
        valid: danglingEdges.length === 0,
        danglingEdges,
        orphanNodes
    };
}

// Execute
const scaffold = ${JSON.stringify(scaffold)};
const result = validateEdgeIntegrity(scaffold.graph.nodes, scaffold.graph.edges);
console.log(JSON.stringify(result, null, 2));
```

### Template 4: Self-Correction Validation

```typescript
// self_correction_validation.ts
interface SelfCorrectionResult {
    allChecksRun: boolean;
    checksPassed: number;
    checksFailed: number;
    details: Array<{
        check: string;
        passed: boolean;
        issue?: string;
    }>;
}

function runSelfCorrectionChecks(scaffold: any): SelfCorrectionResult {
    const checks = [
        {
            name: "Duplicate labels merged or made distinct",
            check: () => {
                const labels = scaffold.graph.nodes.map(n => n.label);
                const duplicates = labels.filter((l, i) => labels.indexOf(l) !== i);
                return { passed: duplicates.length === 0, issue: duplicates.length > 0 ? `Duplicates: ${duplicates.join(', ')}` : undefined };
            }
        },
        {
            name: "No edge without both endpoints",
            check: () => {
                const nodeIds = new Set(scaffold.graph.nodes.map(n => n.id));
                const dangling = scaffold.graph.edges.filter(
                    e => !nodeIds.has(e.source) || !nodeIds.has(e.target)
                );
                return { passed: dangling.length === 0, issue: dangling.length > 0 ? `Dangling: ${dangling.map(e => e.id).join(', ')}` : undefined };
            }
        },
        {
            name: "Noise budget respected",
            check: () => {
                const total = scaffold.graph.nodes.length + scaffold.graph.edges.length;
                const lowConf = 
                    scaffold.graph.nodes.filter(n => n.confidence <= 0.5).length +
                    scaffold.graph.edges.filter(e => e.strength <= 0.5).length;
                const ratio = total > 0 ? lowConf / total : 0;
                return { 
                    passed: ratio >= scaffold.meta.noise_budget, 
                    issue: ratio < scaffold.meta.noise_budget ? `Ratio ${(ratio * 100).toFixed(1)}% < ${(scaffold.meta.noise_budget * 100).toFixed(1)}%` : undefined 
                };
            }
        },
        {
            name: "Topology target met",
            check: () => {
                const ratio = scaffold.graph.edges.length / scaffold.graph.nodes.length;
                return { 
                    passed: ratio >= 4.0, 
                    issue: ratio < 4.0 ? `Ratio ${ratio.toFixed(2)} < 4.0` : undefined 
                };
            }
        },
        {
            name: "Claims have potential falsifiers",
            check: () => {
                const claims = scaffold.graph.nodes.filter(n => n.type === 'claim');
                const contradictEdges = scaffold.graph.edges.filter(e => e.type === 'contradicts');
                const claimsWithFalsifiers = new Set(contradictEdges.map(e => e.target));
                const unfalsifiable = claims.filter(c => !claimsWithFalsifiers.has(c.id));
                return { 
                    passed: unfalsifiable.length === 0, 
                    issue: unfalsifiable.length > 0 ? `Unfalsifiable: ${unfalsifiable.map(c => c.label).join(', ')}` : undefined 
                };
            }
        }
    ];
    
    const details = checks.map(({ name, check }) => {
        const result = check();
        return { check: name, passed: result.passed, issue: result.issue };
    });
    
    return {
        allChecksRun: true,
        checksPassed: details.filter(d => d.passed).length,
        checksFailed: details.filter(d => !d.passed).length,
        details
    };
}

// Execute
const scaffold = ${JSON.stringify(scaffold)};
const result = runSelfCorrectionChecks(scaffold);
console.log(JSON.stringify(result, null, 2));
```

### Template 5: Comprehensive Validation

```typescript
// comprehensive_validation.ts
interface ComprehensiveResult {
    summary: {
        passed: boolean;
        totalChecks: number;
        passedChecks: number;
        failedChecks: number;
    };
    topology: any;
    noiseBudget: any;
    integrity: any;
    selfCorrection: any;
    recommendations: string[];
}

function runComprehensiveValidation(scaffold: any): ComprehensiveResult {
    // Run all validations
    const topologyResult = validateTopology(scaffold.graph.nodes, scaffold.graph.edges);
    const noiseResult = validateNoiseBudget(
        scaffold.graph.nodes,
        scaffold.graph.edges,
        scaffold.meta.noise_budget
    );
    const integrityResult = validateEdgeIntegrity(scaffold.graph.nodes, scaffold.graph.edges);
    const selfCorrectionResult = runSelfCorrectionChecks(scaffold);
    
    // Aggregate results
    const checks = [
        topologyResult.passed,
        noiseResult.satisfied,
        integrityResult.valid,
        selfCorrectionResult.checksFailed === 0
    ];
    
    const passedChecks = checks.filter(Boolean).length;
    const totalChecks = checks.length;
    
    // Generate recommendations
    const recommendations: string[] = [];
    
    if (!topologyResult.passed) {
        const deficit = Math.ceil(4.0 * scaffold.graph.nodes.length - scaffold.graph.edges.length);
        recommendations.push(`Add ~${deficit} more edges to meet topology target`);
    }
    
    if (!noiseResult.satisfied) {
        const deficit = Math.ceil(noiseResult.deficit * (scaffold.graph.nodes.length + scaffold.graph.edges.length));
        recommendations.push(`Reduce confidence on ~${deficit} elements to meet noise budget`);
    }
    
    if (!integrityResult.valid) {
        recommendations.push(`Fix ${integrityResult.danglingEdges.length} dangling edges`);
    }
    
    if (integrityResult.orphanNodes.length > 0) {
        recommendations.push(`Connect ${integrityResult.orphanNodes.length} orphan nodes`);
    }
    
    return {
        summary: {
            passed: passedChecks === totalChecks,
            totalChecks,
            passedChecks,
            failedChecks: totalChecks - passedChecks
        },
        topology: topologyResult,
        noiseBudget: noiseResult,
        integrity: integrityResult,
        selfCorrection: selfCorrectionResult,
        recommendations
    };
}

// Execute
const scaffold = ${JSON.stringify(scaffold)};

// Include helper functions
function validateTopology(nodes, edges, targetRatio = 4.0) { /* ... */ }
function validateNoiseBudget(nodes, edges, targetBudget = 0.25) { /* ... */ }
function validateEdgeIntegrity(nodes, edges) { /* ... */ }
function runSelfCorrectionChecks(scaffold) { /* ... */ }

const result = runComprehensiveValidation(scaffold);
console.log(JSON.stringify(result, null, 2));
```

## Execution Patterns

### Pattern 1: Sequential Validation

Run validations in sequence with early exit on failure:

```typescript
async function sequentialValidation(scaffold: NoisyGraphScaffold): Promise<ValidationReport> {
    // Create notebook
    const nb = await notebook({
        operation: "create",
        args: { title: "NLR Validation", language: "typescript" }
    });
    
    const validations = [
        { name: "topology", template: generateTopologyValidation },
        { name: "noiseBudget", template: generateNoiseBudgetValidation },
        { name: "integrity", template: generateIntegrityValidation }
    ];
    
    const results: ValidationReport = { passed: true, details: {} };
    
    for (const { name, template } of validations) {
        // Add validation cell
        await notebook({
            operation: "add_cell",
            args: {
                notebookId: nb.notebookId,
                cellType: "code",
                content: template(scaffold),
                filename: `${name}.ts`
            }
        });
        
        // Execute
        const result = await notebook({
            operation: "run_cell",
            args: { notebookId: nb.notebookId, cellId: `cell_${name}` }
        });
        
        // Parse and store
        results.details[name] = JSON.parse(result.output);
        
        // Early exit on critical failure
        if (!results.details[name].passed && name === "integrity") {
            results.passed = false;
            break;
        }
    }
    
    return results;
}
```

### Pattern 2: Parallel Validation

Run independent validations concurrently:

```typescript
async function parallelValidation(scaffold: NoisyGraphScaffold): Promise<ValidationReport> {
    // Create separate notebooks for parallel execution
    const [topologyNb, noiseNb, integrityNb] = await Promise.all([
        notebook({ operation: "create", args: { title: "Topology", language: "typescript" } }),
        notebook({ operation: "create", args: { title: "Noise", language: "typescript" } }),
        notebook({ operation: "create", args: { title: "Integrity", language: "typescript" } })
    ]);
    
    // Add cells in parallel
    await Promise.all([
        notebook({
            operation: "add_cell",
            args: {
                notebookId: topologyNb.notebookId,
                cellType: "code",
                content: generateTopologyValidation(scaffold),
                filename: "topology.ts"
            }
        }),
        notebook({
            operation: "add_cell",
            args: {
                notebookId: noiseNb.notebookId,
                cellType: "code",
                content: generateNoiseBudgetValidation(scaffold),
                filename: "noise.ts"
            }
        }),
        notebook({
            operation: "add_cell",
            args: {
                notebookId: integrityNb.notebookId,
                cellType: "code",
                content: generateIntegrityValidation(scaffold),
                filename: "integrity.ts"
            }
        })
    ]);
    
    // Execute in parallel
    const [topologyResult, noiseResult, integrityResult] = await Promise.all([
        notebook({ operation: "run_cell", args: { notebookId: topologyNb.notebookId, cellId: topologyNb.cells[0].id } }),
        notebook({ operation: "run_cell", args: { notebookId: noiseNb.notebookId, cellId: noiseNb.cells[0].id } }),
        notebook({ operation: "run_cell", args: { notebookId: integrityNb.notebookId, cellId: integrityNb.cells[0].id } })
    ]);
    
    return {
        passed: [topologyResult, noiseResult, integrityResult].every(r => JSON.parse(r.output).passed),
        details: {
            topology: JSON.parse(topologyResult.output),
            noiseBudget: JSON.parse(noiseResult.output),
            integrity: JSON.parse(integrityResult.output)
        }
    };
}
```

### Pattern 3: Iterative Refinement

Execute validation and apply fixes iteratively:

```typescript
async function iterativeRefinement(
    scaffold: NoisyGraphScaffold,
    maxIterations: number = 3
): Promise<NoisyGraphScaffold> {
    let currentScaffold = scaffold;
    let iteration = 0;
    
    while (iteration < maxIterations) {
        // Run validation
        const validationResult = await runComprehensiveValidation(currentScaffold);
        
        if (validationResult.summary.passed) {
            console.log(`Validation passed after ${iteration} refinement iterations`);
            return currentScaffold;
        }
        
        // Apply recommendations
        currentScaffold = await applyRecommendations(
            currentScaffold,
            validationResult.recommendations
        );
        
        iteration++;
    }
    
    console.warn(`Validation did not pass after ${maxIterations} iterations`);
    return currentScaffold;
}

async function applyRecommendations(
    scaffold: NoisyGraphScaffold,
    recommendations: string[]
): Promise<NoisyGraphScaffold> {
    const updated = { ...scaffold };
    
    for (const recommendation of recommendations) {
        if (recommendation.includes("Add") && recommendation.includes("edges")) {
            // Generate additional edges
            const newEdges = generateAdditionalEdges(updated);
            updated.graph.edges.push(...newEdges);
        }
        
        if (recommendation.includes("Reduce confidence")) {
            // Lower confidence on least-supported elements
            reduceConfidenceForNoiseBudget(updated);
        }
        
        if (recommendation.includes("Fix") && recommendation.includes("dangling")) {
            // Remove dangling edges
            removeDanglingEdges(updated);
        }
        
        if (recommendation.includes("Connect") && recommendation.includes("orphan")) {
            // Connect orphan nodes
            connectOrphanNodes(updated);
        }
    }
    
    return updated;
}
```

## Graph Analysis Code

### Centrality Analysis

```typescript
// centrality_analysis.ts
interface CentralityResult {
    degreeCentrality: Record<string, number>;
    betweennessCentrality: Record<string, number>;
    hubs: string[];
    bridges: string[];
}

function analyzeCentrality(nodes: Node[], edges: Edge[]): CentralityResult {
    // Degree centrality: count of edges per node
    const degreeCentrality: Record<string, number> = {};
    for (const node of nodes) {
        degreeCentrality[node.id] = edges.filter(
            e => e.source === node.id || e.target === node.id
        ).length;
    }
    
    // Simple betweenness approximation (not full Brandes algorithm)
    // Count paths through each node
    const betweennessCentrality: Record<string, number> = {};
    for (const node of nodes) {
        let pathCount = 0;
        for (const other1 of nodes) {
            for (const other2 of nodes) {
                if (other1.id !== node.id && other2.id !== node.id && other1.id !== other2.id) {
                    // Check if path exists through node
                    const hasPath1 = edges.some(
                        e => (e.source === other1.id && e.target === node.id) ||
                             (e.target === other1.id && e.source === node.id)
                    );
                    const hasPath2 = edges.some(
                        e => (e.source === node.id && e.target === other2.id) ||
                             (e.target === node.id && e.source === other2.id)
                    );
                    if (hasPath1 && hasPath2) pathCount++;
                }
            }
        }
        betweennessCentrality[node.id] = pathCount;
    }
    
    // Identify hubs (high degree) and bridges (high betweenness)
    const avgDegree = Object.values(degreeCentrality).reduce((a, b) => a + b, 0) / nodes.length;
    const avgBetweenness = Object.values(betweennessCentrality).reduce((a, b) => a + b, 0) / nodes.length;
    
    const hubs = nodes
        .filter(n => degreeCentrality[n.id] > avgDegree * 1.5)
        .map(n => n.id);
    
    const bridges = nodes
        .filter(n => betweennessCentrality[n.id] > avgBetweenness * 1.5)
        .map(n => n.id);
    
    return { degreeCentrality, betweennessCentrality, hubs, bridges };
}
```

### Cluster Detection

```typescript
// cluster_detection.ts
interface ClusterResult {
    clusters: Array<{
        id: string;
        nodes: string[];
        density: number;
    }>;
    modularity: number;
}

function detectClusters(nodes: Node[], edges: Edge[]): ClusterResult {
    // Simple community detection via connected components
    const adjacency: Record<string, Set<string>> = {};
    
    for (const node of nodes) {
        adjacency[node.id] = new Set();
    }
    
    for (const edge of edges) {
        adjacency[edge.source]?.add(edge.target);
        adjacency[edge.target]?.add(edge.source);
    }
    
    const visited = new Set<string>();
    const clusters: ClusterResult['clusters'] = [];
    
    for (const node of nodes) {
        if (visited.has(node.id)) continue;
        
        const cluster: string[] = [];
        const queue = [node.id];
        
        while (queue.length > 0) {
            const current = queue.shift()!;
            if (visited.has(current)) continue;
            
            visited.add(current);
            cluster.push(current);
            
            for (const neighbor of adjacency[current]) {
                if (!visited.has(neighbor)) {
                    queue.push(neighbor);
                }
            }
        }
        
        // Calculate cluster density
        const clusterNodes = new Set(cluster);
        const internalEdges = edges.filter(
            e => clusterNodes.has(e.source) && clusterNodes.has(e.target)
        ).length;
        const maxEdges = cluster.length * (cluster.length - 1) / 2;
        const density = maxEdges > 0 ? internalEdges / maxEdges : 0;
        
        clusters.push({
            id: `cluster_${clusters.length}`,
            nodes: cluster,
            density
        });
    }
    
    // Calculate modularity (simplified)
    const m = edges.length;
    let modularity = 0;
    
    for (const cluster of clusters) {
        const clusterNodes = new Set(cluster.nodes);
        const e_ii = edges.filter(
            e => clusterNodes.has(e.source) && clusterNodes.has(e.target)
        ).length / m;
        
        let a_i = 0;
        for (const nodeId of cluster.nodes) {
            a_i += (adjacency[nodeId]?.size || 0);
        }
        a_i = a_i / (2 * m);
        
        modularity += e_ii - a_i * a_i;
    }
    
    return { clusters, modularity };
}
```

## Error Handling

```typescript
async function safeNotebookExecution(
    notebookId: string,
    cellId: string
): Promise<{ success: boolean; output?: string; error?: string }> {
    try {
        const result = await notebook({
            operation: "run_cell",
            args: { notebookId, cellId }
        });
        
        return { success: true, output: result.output };
    } catch (error) {
        console.error(`Notebook execution failed: ${error.message}`);
        return { 
            success: false, 
            error: error.message || "Unknown execution error" 
        };
    }
}
```

## Integration with NLR Workflow

### Validation Checkpoint

Insert validation checkpoints in the NLR loop:

```typescript
async function nlrLoopWithValidation(scaffold: NoisyGraphScaffold): Promise<NoisyGraphScaffold> {
    for (let i = 0; i < scaffold.meta.iteration_limit; i++) {
        // ... existing loop logic ...
        
        // Validation checkpoint every 3 iterations
        if ((i + 1) % 3 === 0) {
            const validationResult = await runComprehensiveValidation(scaffold);
            
            if (!validationResult.summary.passed) {
                // Log issues
                for (const rec of validationResult.recommendations) {
                    scaffold.self_correction.issues_found.push(rec);
                }
                
                // Apply fixes
                scaffold = await applyRecommendations(scaffold, validationResult.recommendations);
            }
        }
    }
    
    // Final validation
    const finalValidation = await runComprehensiveValidation(scaffold);
    
    return scaffold;
}
```

### Export Final Notebook

```typescript
async function exportValidationNotebook(
    notebookId: string,
    outputPath: string = "/mnt/user-data/outputs"
): Promise<string> {
    const exported = await notebook({
        operation: "export",
        args: { notebookId }
    });
    
    // Notebook is exported as markdown with embedded code
    return exported.path;
}
```

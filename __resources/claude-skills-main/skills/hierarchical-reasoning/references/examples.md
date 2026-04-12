# Hierarchical Reasoning Usage Examples

## Example 1: System Design Problem

### Problem
"Design a distributed database system for a social media platform handling 1B+ users"

### Application

**Strategic Level:**
- Identify core requirements: consistency, availability, partition tolerance (CAP theorem)
- Define success metrics: latency < 100ms, 99.99% uptime, cost efficiency
- Establish constraints: budget, team expertise, regulatory compliance

**Tactical Level:**
- Choose architecture: Eventually consistent, partition-tolerant (AP from CAP)
- Select technologies: Cassandra for storage, Redis for caching, Kafka for streaming
- Design sharding strategy: Consistent hashing with virtual nodes

**Operational Level:**
- Calculate shard counts: 1B users / 10M per shard = 100 shards
- Estimate storage: 10KB/user × 1B = 10TB raw, 30TB with replication
- Design replication: RF=3 across availability zones

### Convergence
All levels converge around distributed, eventually consistent architecture with specific implementation parameters.

---

## Example 2: Business Strategy Question

### Problem
"Should our SaaS company pivot from B2B to B2C?"

### Application

**Strategic Level:**
- Frame decision: Market opportunity vs. execution risk
- Identify key factors: TAM size, competition, core competencies, unit economics
- Define decision criteria: 3-year ROI, strategic alignment, risk tolerance

**Tactical Level:**
- Approach: Build decision matrix with weighted criteria
- Method: Conduct market analysis, competitive assessment, financial modeling
- Validation: Pilot program before full pivot

**Operational Level:**
- Market sizing: B2C TAM = $50B vs B2B TAM = $10B
- Customer acquisition cost: B2C $50 vs B2B $1000
- Lifetime value: B2C $200 vs B2B $5000
- CAC/LTV ratio: B2C 4:1 vs B2B 5:1 (both healthy)

### Synthesis
Strategic goals inform tactical analysis method, which guides operational calculations. Results flow back up: operational metrics refine tactical approach, tactical insights reshape strategic framing.

---

## Example 3: Scientific Research Design

### Problem
"Design an experiment to test the effectiveness of a new drug for Alzheimer's"

### Application

**Strategic Level:**
- Research question: Does drug X slow cognitive decline in early-stage Alzheimer's?
- Hypothesis: Drug X reduces decline by ≥30% vs placebo over 18 months
- Ethics framework: IRB approval, informed consent, safety monitoring

**Tactical Level:**
- Study design: Randomized controlled trial, double-blind
- Population: N=500, age 60-75, MMSE 20-26, stratified by APOE4 status
- Outcome measures: Primary (ADAS-Cog), secondary (MRI biomarkers, ADLs)
- Statistical plan: Intent-to-treat analysis, mixed-effects models

**Operational Level:**
- Power calculation: α=0.05, β=0.20, effect size d=0.35 → N=500
- Randomization: Computer-generated, block size 4, concealed allocation
- Dosing protocol: 10mg BID, titration schedule, adherence monitoring
- Data collection: Baseline, 6mo, 12mo, 18mo assessments

### Convergence
Iterative refinement: operational power calculations inform tactical sample size, tactical design choices constrained by strategic ethics requirements.

---

## Example 4: Software Architecture Decision

### Problem
"Choose between microservices vs monolith for new e-commerce platform"

### Application

**Strategic Level:**
- Business goal: Launch MVP in 6 months, scale to 100K users in year 1
- Team context: 8 developers, varied experience, limited DevOps expertise
- Technical vision: Modular, maintainable, cost-effective

**Tactical Level:**
- Decision framework: Start with modular monolith, extract services later
- Architecture pattern: Hexagonal architecture with clear bounded contexts
- Deployment strategy: Containerized monolith with horizontal scaling

**Operational Level:**
- Module boundaries: User service, Product catalog, Order management, Payment
- Inter-module communication: Direct function calls with defined interfaces
- Data strategy: Single database with schema separation per bounded context
- Migration path: Extract high-traffic modules to services when needed

### Reasoning Trace
- Initial strategic push toward microservices for "scalability"
- Tactical analysis reveals team constraints and timeline pressure
- Operational assessment shows monolith sufficient for year-1 scale
- Strategic framing updated: "modular monolith with service extraction path"
- Convergence achieved when all levels aligned on pragmatic approach

---

## Example 5: Policy Analysis

### Problem
"Evaluate the impact of universal basic income (UBI) policy"

### Application

**Strategic Level:**
- Policy objective: Reduce poverty, provide economic security
- Evaluation dimensions: Economic impact, social outcomes, political feasibility
- Time horizon: 10-year longitudinal analysis

**Tactical Level:**
- Methodology: Mixed-methods combining econometric analysis and case studies
- Data sources: Pilot programs (Kenya, Finland, Stockton CA), economic models
- Comparison: UBI vs. existing welfare programs vs. status quo

**Operational Level:**
- Economic modeling: $12K/year × 250M adults = $3T annual cost
- Funding mechanisms: VAT tax (4%), wealth tax (2%), reduced programs ($500B)
- Labor participation: Meta-analysis shows -2% to +1% effect (not significant)
- Poverty reduction: Lift 20M above poverty line (40% reduction)
- Multiplier effect: $1 → $1.45 GDP via increased consumption

### Multi-Level Insights

**Strategic ← Operational:**
Operational cost analysis reveals funding feasibility challenges → refines strategic framing to "partial UBI" or "negative income tax"

**Tactical ← Strategic:**
Strategic focus on poverty reduction → tactical emphasis on targeting mechanisms

**Operational ← Tactical:**
Tactical choice of pilot program comparisons → operational analysis of Finland's lack of work disincentive

---

## Pattern Recognition Across Examples

### Common Strategic Elements
- Problem framing and goal clarification
- Constraint identification
- Success criteria definition
- Risk assessment

### Common Tactical Elements
- Method and approach selection
- Framework construction
- Validation strategy
- Decomposition plan

### Common Operational Elements
- Detailed calculations
- Evidence gathering
- Specific implementation steps
- Quantitative analysis

### Bidirectional Flow
In all cases:
1. Strategic goals constrain and guide tactical choices
2. Tactical approaches structure operational execution
3. Operational findings inform tactical refinements
4. Tactical insights update strategic understanding
5. Iteration continues until convergence

---

## Convergence Patterns

### Fast Convergence (2-4 cycles)
- Well-defined problems
- Clear constraints
- Standard methodologies
- Example: Database system design

### Medium Convergence (5-8 cycles)
- Multiple valid approaches
- Trade-off analysis required
- Moderate uncertainty
- Example: Business pivot decision

### Slow Convergence (10+ cycles)
- High complexity
- Novel problem space
- Conflicting objectives
- Example: Policy analysis with many stakeholders

### Non-Convergence Indicators
- Contradictory goals at strategic level
- Impossible constraints
- Insufficient information at operational level
- Misalignment between abstraction levels

When non-convergence detected, iterate on problem formulation rather than increasing cycles indefinitely.

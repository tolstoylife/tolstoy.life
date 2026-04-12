# Changelog

All notable changes to the dialectical skill are documented in this file.

## [2.0.0] - 2025-12-29

### Added

**Atomic Composition Framework** (`references/atomic-composition.md`)
- Three universal atomic primitives with etymological grounding:
  - **AGONAL (α)**: Persuasion via paradox accumulation (from Greek *agon* = contest)
  - **MAIEUTIC (β)**: Discovery via Socratic dialogue (from Greek *maieutikos* = midwifery)
  - **APOPHATIC (γ)**: Authority via self-negation (from Greek *apophasis* = denial)

- 12 sub-attributes with independent plithogenic values (T, F, I, C):
  - α₁-α₄: Paradox Density, Recursive Anchoring, Forced Dilemma, Transformed Return
  - β₁-β₄: Character Embodiment, Phenomenological Grounding, Triumphant Revelation, Grudging Acknowledgment
  - γ₁-γ₄: Parenthetical Subversion, Hostile Sympathy, Preemptive Apology, Citation Triangulation

- Four composition operators for dynamic style interleaving:
  - Sequential (∘): `(α ∘ β)ο = α(β(ο))`
  - Parallel (⊗): `α ⊗ β = λο.(α(ο), β(ο))`
  - Recursive (*): `α* = fix(α)` — fixpoint iteration
  - Conditional (|): `α | c` — context-dependent activation

- Phase-locking rules for co-occurring sub-attributes
- Phase-exclusion rules with dominance hierarchy resolution
- 10-scenario matrix with weighted compositions:
  - Exam SAQ, Viva Defence, Formal Academic Paper, Tutorial Teaching
  - Editorial/Opinion, Literature Review, Clinical Case Report
  - Entertaining Academic, Apologetics/Persuasion, Exam Commentary

- Perpetual constraints (Π) and initial conditions (ι) system
- Python composition algorithm with constraint propagation
- Legacy alias mapping for backward compatibility

**SKILL.md Updates**
- Added "Atomic Composition Framework" section with quick reference tables
- Updated frontmatter description to include atomic primitives
- Added atomic-composition.md to References section

### Changed
- Framework architecture now supports hypersoft plithogenic composition
- Style modes extended from 6 combinations to unlimited dynamic interleaving
- Scenario-based composition replaces fixed hybrid modes for complex use cases

### Compatibility
- Full backward compatibility maintained via Legacy Alias Mapping
- Existing `style:` directives map to pure primitive compositions
- All original hybrid modes preserved as operator compositions

---

## [1.1.0] - 2025-12-29

### Added

**Writing Style Modes**
- Three pure writing style modes with distinct λο.τ transformations:
  - `dialectical`: Cultural-Common-Ground → Paradox-Accumulation → Irreducible-Mystery
  - `gerry`: Question → Narrative-Grounding → Discovery-Through-Dialogue (Socratic pedagogy)
  - `yartzev`: Assertion → Parenthetical-Subversion → Acknowledged-Inadequacy (editorial first-person)

- Three hybrid style combinations:
  - `dialectical+gerry`: Dialectical structure delivered through Socratic dialogue
  - `dialectical+yartzev`: Dialectical structure with editorial first-person voice
  - `gerry+yartzev`: Clinical narrative with conversational pedagogy and editorial meta-commentary

**Style Selection Mechanism**
- Frontmatter parameter: `style: gerry` or `style: dialectical+yartzev`
- Inline directive for mid-composition switching: `<!-- style:gerry -->`
- Default behavior: `dialectical` mode when no style specified (backward compatible)

**New Reference Files**
- `references/gerry-style-guide.md`: Operational directives for Socratic pedagogical dialogue
  - Character-based pedagogy (Bob/Gerry/Mrs. Dolore pattern)
  - Signature moves: conversational deflection, triumphant revelation, grudging acknowledgment
  - Table deployment strategies and circulation time as narrative device

- `references/yartzev-style-guide.md`: Operational directives for editorial first-person style
  - Multi-track audience addressing (trainee/examiner/self/reader)
  - Signature moves: hostile sympathy, preemptive apology, qualified disclaimer
  - Citation triangulation and parenthetical subversion patterns

- `references/style-integration-patterns.md`: Hybrid mode combination guidelines
  - Phase-by-phase integration patterns for each hybrid mode
  - Voice calibration across modes (pronoun strategy, register, humility markers)
  - Style switching guidelines and transition management
  - Quality verification checklists for hybrid modes

**SKILL.md Updates**
- Added "Writing Style Modes" section with mode selection table
- Added "Style-Specific Execution" section with conditional directives for each mode
- Updated description to mention three style modes and hybrid combinations
- Added references to new style guide files

### Changed
- Expanded skill description to reflect multi-mode capability
- Enhanced Integration section to reference style-integration-patterns.md

### Compatibility
- Full backward compatibility maintained
- Existing usage (no style parameter) defaults to original dialectical mode
- All original dialectical execution protocol preserved

---

## [1.0.0] - Initial Release

### Added
- Core dialectical persuasion framework
- Four-phase execution protocol (Establish → Critique → Synthesize → Return)
- Paradox accumulation methodology
- Recursive anchoring patterns
- Voice calibration with register oscillation
- Quality gates for structural, voice, and rhythm verification
- Reference files: pattern-analysis.md, execution-protocol.md, examples.md

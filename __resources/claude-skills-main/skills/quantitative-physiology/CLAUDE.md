# Quantitative Physiology Skill System

## Overview

Complete Claude skill system for quantitative human physiology, based on "Quantitative Human Physiology: An Introduction, 3rd Edition" by Joseph J. Feher (Elsevier 2026). **Version 3.2.0** implements hierarchical equation ID system across all 279 equations, eliminating ID collision risks with namespace-based identifiers.

## Quick Start

```bash
# Deploy to Claude skills directory
./deploy.sh

# Load skill (automatically loads SKILL.md orchestrator)
skill: quantitative-physiology

# Import equations directly from modular scripts
from scripts.cardiovascular.cardiac import cardiac_output
from scripts.respiratory.gas_exchange import alveolar_gas_equation
```

## Project Structure

```
quantitative-physiology/
├── SKILL.md                       # Entry point orchestrator - always loaded
├── CLAUDE.md                      # Project documentation
├── scripts/                       # 279 atomic equation modules (hierarchical IDs)
│   ├── base.py                    # AtomicEquation base class
│   ├── index.py                   # Multi-dimensional indexing
│   ├── registry.py                # Cross-domain equation registry
│   ├── context.py                 # Parameter resolution layer
│   ├── foundations/               # Transport, electrical, diffusion, thermodynamics, kinetics, biophysics, sensory, body composition
│   │   ├── transport/             # Poiseuille, Laplace, drag force
│   │   ├── electrical/            # Coulomb, capacitance, dipole moment
│   │   ├── diffusion/             # Fick's laws, Stokes-Einstein
│   │   ├── thermodynamics/        # Gibbs, Nernst, enthalpy, ideal gas, Henry's law
│   │   ├── kinetics/              # First-order decay, Arrhenius, Beer-Lambert
│   │   ├── biophysics/            # Viscoelasticity, sedimentation, partition coefficient
│   │   ├── sensory/               # Optics, psychophysics, acoustics
│   │   └── body_composition/      # ICF/ISF volumes, lean body mass, total body water
│   ├── membrane/                  # 18 equations: channels, pumps, potential
│   ├── excitable/                 # 22 equations: action potentials, muscle
│   │   ├── membrane_potential/    # GHK, chord conductance, slope conductance
│   │   ├── action_potential/      # Hodgkin-Huxley, cable theory, strength-duration
│   │   ├── muscle/                # Force-velocity, cross-bridge, Ca-force
│   │   ├── synapse/               # Neuromuscular junction
│   │   └── energetics/            # ATP consumption, efficiency
│   ├── nervous/                   # 27 equations: synapses, sensory, motor
│   ├── cardiovascular/            # 31 equations: heart, circulation, hemodynamics
│   │   ├── blood/                 # Viscosity, hematocrit, Hill saturation, O₂ content/delivery
│   │   ├── cardiac/               # Cardiac output/index, ejection fraction, Fick, BSA, EDPVR/ESPVR
│   │   ├── ecg/                   # Heart rate, QTc (Bazett/Fridericia), funny current
│   │   ├── hemodynamics/          # MAP, compliance, Bramwell-Hill, Moens-Korteweg
│   │   └── microcirculation/      # Starling filtration, NFP, baroreceptor, shear stress, Fick diffusion
│   ├── respiratory/               # 41 equations: ventilation, gas exchange
│   ├── renal/                     # 30 equations: filtration, clearance
│   ├── gastrointestinal/          # 34 equations: digestion, absorption
│   └── endocrine/                 # 25 equations: hormones, feedback
└── graph/                         # Dependency visualization
    ├── dependency-graph.json      # Full equation dependency DAG
    ├── clusters.json              # Functional equation clusters
    └── visualization.md           # Mermaid diagrams
```

## Architecture (v3.2.0)

**Atomic Equation Pattern**: Each equation is a standalone Python module with metadata, compute function, and dependency tracking.

### Key Architectural Components

1. **AtomicEquation** (`scripts/base.py`):
   - Self-contained equation with parameters, compute function, metadata
   - Signature-metadata validation prevents configuration errors
   - Unit conversion system for physiological parameters
   - Dependency tracking for cross-domain equations
   - **Hierarchical ID system**: `{domain}.{subdomain}.{equation_name}` format

2. **Multi-Dimensional Indexing** (`scripts/index.py`):
   - Index by equation ID, category, units, dependencies
   - Global registry for equation discovery
   - Lazy imports for context minimization
   - **Namespace-based ID lookup**: IDs match file path structure exactly

3. **Cross-Domain Registry** (`scripts/registry.py`):
   - Tracks shared equations (Nernst, Fick, Poiseuille, etc.)
   - Maps foundational equations to dependent domains
   - Example: Nernst equation used in membrane, excitable, nervous, cardiovascular, renal

4. **Parameter Resolution** (`scripts/context.py`):
   - ComputeContext for smart parameter management
   - Alias normalization (Hb/hemoglobin, S_O2/saturation)
   - Auto-resolved parameters for multi-equation workflows

### Hierarchical Equation ID System (v3.2.0)

All 279 equations now use **namespaced hierarchical IDs** that match their file path structure:

**Pattern**: `{domain}.{subdomain}.{equation_name}`

**Examples by Domain**:
```
foundations.transport.poiseuille_flow
foundations.thermodynamics.nernst_equation
foundations.kinetics.first_order_decay
foundations.biophysics.kelvin_voigt_stress
foundations.sensory.sound_intensity_level
foundations.body_composition.total_body_water

membrane.transport.passive_flux
membrane.potential.nernst_potential
membrane.osmosis.osmotic_pressure

excitable.action_potential.hodgkin_huxley_sodium_current
excitable.membrane_potential.slope_conductance
excitable.muscle.hill_force_velocity
excitable.synapse.quantal_content

nervous.synaptic.synaptic_current
nervous.sensory.weber_fraction
nervous.motor.motor_unit_tension

cardiovascular.cardiac.cardiac_output
cardiovascular.hemodynamics.mean_arterial_pressure
cardiovascular.blood.blood_oxygen_content
cardiovascular.ecg.heart_rate_from_rr
cardiovascular.microcirculation.capillary_filtration_coefficient

respiratory.mechanics.lung_compliance
respiratory.gas_exchange.alveolar_gas_equation
respiratory.oxygen_transport.hill_saturation
respiratory.acid_base.henderson_hasselbalch
respiratory.vq_matching.ventilation_perfusion_ratio

renal.glomerular.glomerular_filtration_rate
renal.clearance.clearance
renal.tubular.glucose_transport_maximum
renal.concentration.free_water_clearance

gastrointestinal.secretion.gastric_acid_secretion_rate
gastrointestinal.absorption.glucose_absorption_rate
gastrointestinal.liver.urea_synthesis_rate

endocrine.kinetics.metabolic_clearance_rate
endocrine.feedback.negative_feedback_gain
endocrine.receptor.receptor_occupancy
```

**Benefits**:
- **Zero ID collisions**: Namespace prevents conflicts across 279 equations
- **Explicit domain context**: ID reveals equation's physiological domain
- **File path alignment**: ID structure matches directory structure exactly
- **Enhanced discoverability**: Clear hierarchy aids navigation and search
- **Migration complete**: All 150+ flat ID warnings eliminated

### Domain Reference Mapping

| Unit | Reference File | Key Topics |
|------|----------------|------------|
| 1 | `references/physical-foundations.md` | Poiseuille, Laplace, diffusion, thermodynamics |
| 2 | `references/membranes-transport.md` | Channels, pumps, osmosis, Donnan equilibrium |
| 3 | `references/excitable-cells.md` | Action potentials, Hodgkin-Huxley, muscle mechanics |
| 4 | `references/nervous-system.md` | Synapses, sensory transduction, motor control |
| 5 | `references/cardiovascular.md` | Frank-Starling, hemodynamics, ECG, microcirculation |
| 6 | `references/respiratory.md` | Lung mechanics, V/Q matching, oxygen transport, acid-base |
| 7 | `references/renal.md` | GFR, tubular function, countercurrent, RAAS |
| 8 | `references/gastrointestinal.md` | Secretion, absorption, motility, hepatic metabolism |
| 9 | `references/endocrine.md` | Hormone kinetics, HPA/HPT/HPG axes, glucose homeostasis |

## Key Equations Reference

### Transport
```
J_V = Q_V/A                    # Volume flux
J_S = -D × (∂C/∂x)            # Fick's first law (diffusion)
Q_V = (πr⁴/8η) × (ΔP/L)       # Poiseuille's law
```

### Membrane
```
E = (RT/zF) × ln(C_out/C_in)  # Nernst potential
V_m = (RT/F) × ln[(P_K[K]_o + P_Na[Na]_o + P_Cl[Cl]_i) / ...]  # GHK
```

### Cardiovascular
```
CO = HR × SV                   # Cardiac output
MAP = DBP + (1/3) × PP         # Mean arterial pressure
EF = (EDV - ESV) / EDV         # Ejection fraction
```

### Respiratory
```
P_AO2 = P_iO2 - P_ACO2/R       # Alveolar gas equation
S_O2 = P_O2^n / (P_50^n + P_O2^n)  # Hill saturation
```

### Renal
```
GFR = K_f × NFP                # Glomerular filtration
C_x = (U_x × V̇) / P_x         # Clearance
FF = GFR / RPF                 # Filtration fraction
```

## Equation Module System

**279 atomic equations** across 9 domains with hierarchical subdomain organization and namespace-based IDs. Each module contains:
- **Hierarchical equation ID**: Format `{domain}.{subdomain}.{equation_name}` matching file path
- Compute function with type annotations and physiological context
- Parameter metadata (units, ranges, symbols)
- LaTeX and simplified equation representations
- Dependency tracking with namespaced ID references
- Clinical relevance documentation
- Physiological reference values

**Equation Count by Domain** (all using hierarchical IDs):
- **Foundations**: 44 equations (transport, electrical, diffusion, thermodynamics, kinetics, biophysics, sensory, body_composition)
- **Membrane**: 18 equations (structure, potential, transport, osmosis, signaling, metabolism)
- **Excitable**: 31 equations (membrane_potential, action_potential, muscle, synapse, energetics)
- **Nervous**: 24 equations (synaptic, integration, sensory, motor, plasticity)
- **Cardiovascular**: 31 equations (blood, cardiac, ecg, hemodynamics, microcirculation)
- **Respiratory**: 43 equations (mechanics, gas_exchange, volumes, oxygen_transport, co2_transport, ventilatory_control, acid_base, vq_matching)
- **Renal**: 29 equations (blood_flow, glomerular, clearance, tubular, concentration, acid_base, potassium)
- **Gastrointestinal**: 34 equations (motility, secretion, digestion, absorption, hormones, liver)
- **Endocrine**: 25 equations (adrenal, calcium, feedback, kinetics, pancreatic, receptor, reproductive, thyroid)

### Import Patterns

```python
# Import entire domains
from scripts import cardiovascular, respiratory, renal

# Import specific equations
from scripts.cardiovascular.cardiac import cardiac_output, ejection_fraction
from scripts.respiratory.gas_exchange import alveolar_gas_equation
from scripts.renal.clearance import clearance, filtered_load

# Import foundations used across domains
from scripts.foundations.transport import poiseuille_flow
from scripts.foundations.thermodynamics import nernst_equation
from scripts.foundations.kinetics import first_order_decay, arrhenius_rate
from scripts.foundations.biophysics import sedimentation_rate, kelvin_voigt_stress
from scripts.foundations.sensory import snell_law, sound_intensity_level
from scripts.foundations.body_composition import total_body_water, lean_body_mass_from_tbw

# Import from reorganized excitable domain
from scripts.excitable.membrane_potential import slope_conductance
from scripts.excitable.action_potential import threshold_current, electrotonus_decay

# Import cross-domain registry
from scripts.registry import CROSS_DOMAIN_EQUATIONS
```

### Usage Examples

**Direct computation:**
```python
from scripts.cardiovascular.cardiac import cardiac_output

# Access the equation object
eq = cardiac_output
print(eq.metadata.latex)  # Display LaTeX
print(eq.metadata.simplified)  # Display simplified form

# Compute
result = cardiac_output.compute(HR=70, SV=70)  # 4.9 L/min
```

**Smart context with parameter resolution:**
```python
from scripts.context import ComputeContext

ctx = ComputeContext()
ctx.set(Hb=15, S_O2=0.97, PO2=100)  # Aliases auto-normalized

# Compute with auto-resolved parameters
result = ctx.compute("blood_oxygen_content")
```

**Dependency chains with hierarchical IDs:**
```python
from scripts.index import get_global_index

idx = get_global_index()

# Query by hierarchical ID (matches file path structure)
deps = idx.get_dependencies("cardiovascular.cardiac.cardiac_output")
# Returns: equations that cardiac_output depends on

# Cross-domain dependency resolution
deps = idx.get_dependencies("respiratory.oxygen_transport.hill_saturation")
# Returns: ['foundations.thermodynamics.nernst_equation'] (if applicable)

# All equations now use namespace-based IDs - zero collision risk
```

## Physical Constants

| Constant | Symbol | Value | Units |
|----------|--------|-------|-------|
| Gas constant | R | 8.314 | J/(mol·K) |
| Faraday constant | F | 96,485 | C/mol |
| Boltzmann constant | k | 1.38×10⁻²³ | J/K |
| Body temperature | T | 310 | K (37°C) |
| Water viscosity | η | 0.001 | Pa·s |

## Physiological Reference Values

### Ion Concentrations
| Ion | Intracellular | Extracellular | E_eq (mV) |
|-----|---------------|---------------|-----------|
| K⁺ | 140 mM | 4-5 mM | -90 |
| Na⁺ | 10-15 mM | 145 mM | +67 |
| Ca²⁺ | 0.0001 mM | 1-2 mM | +129 |
| Cl⁻ | 10-30 mM | 110 mM | -89 |

### Cardiovascular
- Cardiac output: 5 L/min (rest)
- Blood pressure: 120/80 mmHg
- Heart rate: 60-100 bpm
- Ejection fraction: 55-70%

### Respiratory
- Tidal volume: 500 mL
- Vital capacity: ~4600 mL
- Minute ventilation: 6 L/min
- P_aO2: 100 mmHg, P_aCO2: 40 mmHg

### Renal
- GFR: 125 mL/min
- RPF: 660 mL/min
- Urine output: 1-2 L/day
- Filtration fraction: 20%

## Deployment

### Automated Installation
```bash
./deploy.sh
```

Deployment script:
- Creates `~/.claude/skills/quantitative-physiology/`
- Copies `SKILL.md`, `CLAUDE.md`
- Copies `scripts/*.py`
- Copies `references/*.md`
- Reports file counts and structure

### Optional: Semantic Search Index
```bash
leann index create quantitative-physiology ~/.claude/skills/quantitative-physiology
```

## Source Attribution

All content derived from:
**"Quantitative Human Physiology: An Introduction, 3rd Edition"**
Joseph J. Feher, Elsevier 2026

Equation numbering follows source text format: `Eq X.Y.Z` = Chapter X, Section Y, Equation Z

## Dependency Graph & Clusters

**Location**: `graph/` directory

### Functional Clusters (`clusters.json`)

Equations grouped by physiological function:
- **Transport & Fluid Mechanics**: Poiseuille, hydraulic resistance, Laplace laws
- **Electrochemical Gradients**: Nernst, Donnan, GHK, chord conductance
- **Excitation-Contraction Coupling**: HH currents, cable equation, Ca-force, Hill force-velocity
- **Oxygen Transport Cascade**: Alveolar gas → diffusing capacity → Hill saturation → O₂ content → O₂ delivery
- **Acid-Base Homeostasis**: Henderson-Hasselbalch, anion gap, Winters, net acid excretion
- **Renal Filtration & Clearance**: NFP → GFR → clearance → fractional excretion
- **Hormone Kinetics & Feedback**: Kd, MCR, fractional occupancy, feedback gain
- **Synaptic & Neural Signaling**: Quantal content, synaptic current, EPSP, STDP
- **GI Secretion & Absorption**: Enzyme kinetics, transporter models, absorption efficiency
- **Cardiovascular Regulation**: Cardiac output, hemodynamics, microcirculation, baroreceptors

### Dependency Chains (`dependency-graph.json`)

Key physiological workflows:
1. **Membrane → Action Potential**: Nernst → GHK → HH membrane current → Na/K currents
2. **Oxygen Cascade**: Alveolar gas → diffusing capacity → Hill saturation → O₂ content → O₂ delivery → Fick principle
3. **Renal Clearance**: RPF → filtration fraction → GFR → clearance → fractional excretion
4. **HPA Axis**: CRH dynamics → ACTH dynamics → Cortisol dynamics → feedback gain

### Visualization (`visualization.md`)

Mermaid diagrams showing:
- Unit dependency DAG (9 units across 5 layers)
- Cross-domain equation flow
- Foundational equations with multiple dependents

## Version History

**v3.2.0** (2025-12-18): Hierarchical equation ID migration
- **Migrated all 279 equations to hierarchical ID system**: `{domain}.{subdomain}.{equation_name}`
- **Zero breaking changes**: Function names and imports unchanged, only internal equation IDs updated
- **Eliminated 150+ flat ID warnings**: All equations now use namespace-based identifiers
- **Enhanced discoverability**: IDs match file path structure exactly for intuitive navigation
- **Cross-domain safety**: Namespace prevents ID collisions across all 9 physiological domains
- **Migration coverage**:
  - Foundations (44 equations): transport, electrical, diffusion, thermodynamics, kinetics, biophysics, sensory, body_composition
  - Membrane (18 equations): structure, potential, transport, osmosis, signaling, metabolism
  - Excitable (31 equations): membrane_potential, action_potential, muscle, synapse, energetics
  - Nervous (24 equations): synaptic, integration, sensory, motor, plasticity
  - Cardiovascular (31 equations): blood, cardiac, ecg, hemodynamics, microcirculation
  - Respiratory (43 equations): mechanics, gas_exchange, volumes, oxygen_transport, co2_transport, ventilatory_control, acid_base, vq_matching
  - Renal (29 equations): blood_flow, glomerular, clearance, tubular, concentration, acid_base, potassium
  - Gastrointestinal (34 equations): motility, secretion, digestion, absorption, hormones, liver
  - Endocrine (25 equations): adrenal, calcium, feedback, kinetics, pancreatic, receptor, reproductive, thyroid

**v3.1.0** (2025-12-18): Hierarchical subdomain expansion
- Expanded to 317+ atomic equation modules
- Enhanced hierarchical organization with specialized subdomains
- New foundation subdomains (all from Appendix I equations):
  - `kinetics/`: First-order decay, half-life, Arrhenius temperature dependence, Beer-Lambert absorption law
  - `biophysics/`: Kelvin-Voigt and Maxwell viscoelastic models (creep, stress relaxation), sedimentation rate, partition coefficient
  - `sensory/`: Acoustics (decibel scale, sound intensity/pressure), optics (Snell's law, lens equation), psychophysics (Weber, Fechner, Stevens)
  - `body_composition/`: ICF/ISF volume calculations, lean body mass, total body water estimation
- Enhanced excitable cell subdomains:
  - `action_potential/`: Added strength-duration curves (Weiss equation, rheobase, chronaxie), electrotonus (decay constants, cable theory)
  - `membrane_potential/`: Added slope conductance and transmembrane/axoplasmic resistance equations
- Improved clinical context documentation across all new modules
- Enhanced physiological relevance descriptions in compute functions

**v3.0.0** (2025-12-17): Atomic equation architecture
- 248 equations as standalone Python modules
- AtomicEquation base class with signature-metadata validation
- Multi-dimensional indexing (by ID, category, units, dependencies)
- Cross-domain registry for shared equations
- Parameter resolution layer with alias normalization
- Dependency graph and functional clusters (JSON + Mermaid)
- Unit conversion system for physiological parameters
- Lazy imports for context minimization

**v2.0.0** (2025-12-17): Modular refactor with progressive disclosure
- Lean orchestrator: `SKILL.md` (828 words vs 10,000+ lines)
- Extracted Python code to `scripts/physiology_core.py` (930 lines)
- Moved domain knowledge to `references/*.md` (on-demand loading)
- 95% reduction in always-loaded context
- Added `deploy.sh` for automated installation

**v1.0.0** (2025-12-17): Initial comprehensive skill system
- 1 orchestrator + 9 domain sub-skills
- Total 10,181 lines across 11 markdown files

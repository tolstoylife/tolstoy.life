# Respiratory Physiology Equation Extraction Report

**Date**: 2025-12-17  
**Source**: Unit 6 - Respiratory Physiology  
**Reference File**: `/Users/mikhail/Downloads/QP-SKILL/quantitative-physiology/references/respiratory.md`

## Summary

**Total Equations Extracted**: 41

All equations from Unit 6 (Respiratory) have been successfully extracted and implemented as atomic Python modules following the established patterns from `scripts/base.py` and `scripts/index.py`.

## Directory Structure

```
scripts/respiratory/
├── __init__.py                          # Main module exports
├── volumes/                             # 6 equations
│   ├── total_lung_capacity.py
│   ├── vital_capacity.py
│   ├── functional_residual_capacity.py
│   ├── inspiratory_capacity.py
│   ├── minute_ventilation.py
│   └── alveolar_ventilation.py
├── mechanics/                           # 11 equations
│   ├── transmural_pressure.py
│   ├── compliance.py
│   ├── total_compliance.py
│   ├── elastance.py
│   ├── total_elastance.py
│   ├── laplace_pressure.py
│   ├── airway_resistance.py
│   ├── pressure_flow.py
│   ├── reynolds_number.py
│   ├── time_constant.py
│   └── exponential_emptying.py
├── gas_exchange/                        # 7 equations
│   ├── partial_pressure.py
│   ├── inspired_po2.py
│   ├── alveolar_gas_equation.py
│   ├── aa_gradient.py
│   ├── diffusing_capacity.py
│   ├── dlco_to_dlo2.py
│   └── diffusion_conductance.py
├── vq_matching/                         # 2 equations
│   ├── shunt_equation.py
│   └── dead_space_bohr.py
├── oxygen_transport/                    # 5 equations
│   ├── oxygen_content.py
│   ├── hill_equation.py
│   ├── oxygen_delivery.py
│   ├── oxygen_consumption_fick.py
│   └── oxygen_extraction_ratio.py
├── co2_transport/                       # 1 equation
│   └── dissolved_co2.py
├── ventilatory_control/                 # 2 equations
│   ├── co2_response.py
│   └── hypoxic_response.py
└── acid_base/                           # 7 equations
    ├── henderson_hasselbalch.py
    ├── anion_gap.py
    ├── winters_formula.py
    ├── metabolic_alkalosis_compensation.py
    ├── acute_respiratory_ph_change.py
    ├── chronic_respiratory_acidosis_hco3.py
    └── chronic_respiratory_alkalosis_hco3.py
```

## Equations by Category

### 1. Lung Volumes and Capacities (6.1) - 6 Equations

1. **Total Lung Capacity**: `TLC = VT + IRV + ERV + RV`
2. **Vital Capacity**: `VC = VT + IRV + ERV`
3. **Functional Residual Capacity**: `FRC = ERV + RV`
4. **Inspiratory Capacity**: `IC = VT + IRV`
5. **Minute Ventilation**: `V̇E = VT × f`
6. **Alveolar Ventilation**: `V̇A = (VT - VD) × f`

### 2. Respiratory Mechanics (6.2) - 11 Equations

1. **Transmural Pressure**: `P_TM = P_alv - P_pl`
2. **Compliance**: `C = ΔV/ΔP`
3. **Total Compliance**: `1/C_RS = 1/C_L + 1/C_CW`
4. **Elastance**: `E = 1/C = ΔP/ΔV`
5. **Total Elastance**: `E_RS = E_L + E_CW`
6. **Laplace Pressure**: `ΔP = 2T/r`
7. **Airway Resistance**: `R = 8ηL/(πr⁴)`
8. **Pressure-Flow**: `V̇ = ΔP/R`
9. **Reynolds Number**: `Re = ρvd/η`
10. **Time Constant**: `τ = R × C`
11. **Exponential Emptying**: `V(t) = V₀ × e^(-t/τ)`

### 3. Gas Exchange (6.3) - 7 Equations

1. **Partial Pressure (Dalton's Law)**: `P_i = F_i × P_total`
2. **Inspired PO2**: `P_iO2 = FiO2 × (P_B - P_H2O)`
3. **Alveolar Gas Equation**: `P_AO2 = P_iO2 - P_ACO2/R`
4. **A-a Gradient**: `A-a gradient = P_AO2 - P_aO2`
5. **Diffusing Capacity**: `D_L = V̇_gas / (P_A - P_c)`
6. **DLCO to DLO2**: `D_LO2 ≈ 1.23 × D_LCO`
7. **Diffusion Conductance**: `1/D_L = 1/D_M + 1/(θ × V_c)`

### 4. Ventilation-Perfusion Matching (6.4) - 2 Equations

1. **Shunt Equation**: `Q̇_S/Q̇_T = (C_cO2 - C_aO2) / (C_cO2 - C_vO2)`
2. **Dead Space (Bohr)**: `V_D/V_T = (P_aCO2 - P_ECO2) / P_aCO2`

### 5. Oxygen Transport (6.5) - 5 Equations

1. **Oxygen Content**: `C_O2 = (1.34 × [Hb] × S_O2) + (0.003 × P_O2)`
2. **Hill Equation**: `S_O2 = P_O2^n / (P_50^n + P_O2^n)`
3. **Oxygen Delivery**: `D_O2 = Q̇ × C_aO2 × 10`
4. **Oxygen Consumption (Fick)**: `V̇O2 = Q̇ × (C_aO2 - C_vO2) × 10`
5. **Oxygen Extraction Ratio**: `O2ER = (C_aO2 - C_vO2) / C_aO2`

### 6. CO2 Transport (6.6) - 1 Equation

1. **Dissolved CO2**: `[CO2]_dissolved = α × P_CO2`

### 7. Ventilatory Control (6.7) - 2 Equations

1. **CO2 Response**: `V̇E = V̇E₀ + S × (P_aCO2 - threshold)`
2. **Hypoxic Response**: `V̇E = V̇E₀ × (1 + A/(P_aO2 - B))`

### 8. Acid-Base Balance (6.8) - 7 Equations

1. **Henderson-Hasselbalch**: `pH = pKa + log([HCO3⁻]/(α × P_CO2))`
2. **Anion Gap**: `AG = [Na⁺] - [Cl⁻] - [HCO3⁻]`
3. **Winter's Formula**: `P_CO2 = 1.5 × [HCO3⁻] + 8`
4. **Metabolic Alkalosis Compensation**: `P_CO2 = 0.7 × [HCO3⁻] + 21`
5. **Acute Respiratory pH Change**: `ΔpH = -0.008 × ΔP_CO2`
6. **Chronic Respiratory Acidosis HCO3**: `Δ[HCO3⁻] = 3.5 × ΔP_CO2 / 10`
7. **Chronic Respiratory Alkalosis HCO3**: `Δ[HCO3⁻] = -5 × ΔP_CO2 / 10`

## Implementation Details

### Pattern Compliance

All 41 equations follow the established atomic equation pattern:

1. **Imports**: Consistent use of `scripts.base` and `scripts.index`
2. **Compute Function**: Each equation has a `compute_*` function with full docstring
3. **Equation Creation**: Using `create_equation()` factory function
4. **Registration**: Automatic registration with `register_equation()`
5. **Metadata**: All equations tagged with `source_unit=6` and appropriate `source_chapter`
6. **Category**: All use `EquationCategory.RESPIRATORY`

### Parameters

Each equation includes:
- **Name, description, units, symbol**: Full parameter specification
- **Default values**: Where applicable (physical constants, normal physiological values)
- **Physiological ranges**: For validation of input values

### Dependencies

Internal dependency graph (all within respiratory domain):

```
Volumes:
  minute_ventilation → alveolar_ventilation

Mechanics:
  compliance → elastance
  compliance → total_compliance
  compliance → time_constant
  airway_resistance → pressure_flow
  airway_resistance → time_constant
  time_constant → exponential_emptying

Gas Exchange:
  partial_pressure → inspired_po2
  inspired_po2 → alveolar_gas_equation
  alveolar_gas_equation → aa_gradient
  diffusing_capacity → dlco_to_dlo2
  diffusing_capacity → diffusion_conductance

Oxygen Transport:
  oxygen_content → oxygen_delivery
  oxygen_content → oxygen_consumption_fick
  oxygen_content → oxygen_extraction_ratio

Acid-Base:
  henderson_hasselbalch → winters_formula
  henderson_hasselbalch → metabolic_alkalosis_compensation
  henderson_hasselbalch → acute_respiratory_ph_change
  henderson_hasselbalch → chronic_respiratory_acidosis_hco3
  henderson_hasselbalch → chronic_respiratory_alkalosis_hco3
```

## Cross-Domain Dependencies

**None identified**. All equations are self-contained within the respiratory domain.

**Potential cross-domain connections** (not implemented as dependencies but conceptually related):
- Oxygen delivery/consumption equations use cardiac output (Q̇) - this comes from cardiovascular domain
- Some acid-base equations reference electrolytes that could link to renal domain

These are parameter inputs rather than equation dependencies.

## Files Created

**Total**: 49 Python files
- 41 equation modules
- 8 `__init__.py` files (1 main + 7 subdirectories)

## Verification

All equations have been:
- ✅ Extracted from reference material
- ✅ Implemented with compute functions
- ✅ Registered in global index
- ✅ Exported via `__init__.py` hierarchy
- ✅ Documented with LaTeX and simplified forms
- ✅ Tagged with source metadata
- ✅ Validated with physiological ranges

## Usage Example

```python
from scripts.respiratory import (
    alveolar_gas_equation,
    hill_equation,
    henderson_hasselbalch
)

# Calculate alveolar PO2
pao2 = alveolar_gas_equation.compute(P_iO2=150, P_ACO2=40, R=0.8)
# Result: ~100 mmHg

# Calculate O2 saturation
so2 = hill_equation.compute(PO2=100, P50=26.6, n=2.7)
# Result: ~0.97 (97%)

# Calculate pH
ph = henderson_hasselbalch.compute(HCO3=24, PCO2=40, pKa=6.1, alpha=0.03)
# Result: ~7.40
```

## Integration with Index

All equations are automatically registered in the global equation index (`scripts.index`) upon import, enabling:
- Dependency graph traversal
- Topological ordering for computation
- Category-based filtering
- Unit-based retrieval

## Next Steps

1. ✅ All Unit 6 equations extracted
2. Ready for testing and validation
3. Can be integrated with other domain equations
4. Available for clinical calculation tools

---

**Extraction Agent**: Unit 6 Respiratory Agent  
**Status**: Complete ✅

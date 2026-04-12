"""Chronic Respiratory Acidosis HCO3 Change equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_chronic_respiratory_acidosis_hco3(delta_PCO2: float) -> float:
    """
    Calculate HCO3 change in chronic respiratory acidosis.

    Δ[HCO3⁻] = 3.5 × ΔP_CO2 / 10

    Parameters
    ----------
    delta_PCO2 : float
        Change in PCO2 from normal (mmHg)

    Returns
    -------
    float
        Change in bicarbonate (mEq/L)
    """
    return 3.5 * delta_PCO2 / 10.0


# Create equation
chronic_respiratory_acidosis_hco3 = create_equation(
    id="respiratory.acid_base.chronic_respiratory_acidosis_hco3",
    name="Chronic Respiratory Acidosis HCO3 Change",
    category=EquationCategory.RESPIRATORY,
    latex=r"\Delta[HCO_3^-] = 3.5 \times \frac{\Delta P_{CO2}}{10}",
    simplified="Δ[HCO3⁻] = 3.5 × ΔP_CO2 / 10",
    description="Renal compensation: HCO3 rises 3.5 mEq/L per 10 mmHg ↑PCO2",
    compute_func=compute_chronic_respiratory_acidosis_hco3,
    parameters=[
        Parameter(
            name="delta_PCO2",
            description="Change in PCO2 from normal",
            units="mmHg",
            symbol=r"\Delta P_{CO2}",
            physiological_range=(0.0, 40.0)
        )
    ],
    depends_on=["respiratory.acid_base.henderson_hasselbalch"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.8"
    )
)

# Register in global index
register_equation(chronic_respiratory_acidosis_hco3)

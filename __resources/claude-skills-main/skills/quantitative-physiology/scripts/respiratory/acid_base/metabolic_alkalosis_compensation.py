"""Metabolic Alkalosis Compensation equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_metabolic_alkalosis_compensation(HCO3: float) -> float:
    """
    Calculate expected PCO2 in metabolic alkalosis.

    P_CO2 = 0.7 × [HCO3⁻] + 21

    Parameters
    ----------
    HCO3 : float
        Bicarbonate concentration (mEq/L)

    Returns
    -------
    float
        Expected PCO2 (mmHg)
    """
    return 0.7 * HCO3 + 21.0


# Create equation
metabolic_alkalosis_compensation = create_equation(
    id="respiratory.acid_base.metabolic_alkalosis_compensation",
    name="Metabolic Alkalosis Compensation",
    category=EquationCategory.RESPIRATORY,
    latex=r"P_{CO2} = 0.7 \times [HCO_3^-] + 21",
    simplified="P_CO2 = 0.7 × [HCO3⁻] + 21",
    description="Expected respiratory compensation for metabolic alkalosis",
    compute_func=compute_metabolic_alkalosis_compensation,
    parameters=[
        Parameter(
            name="HCO3",
            description="Bicarbonate concentration",
            units="mEq/L",
            symbol="[HCO_3^-]",
            physiological_range=(10.0, 50.0)
        )
    ],
    depends_on=["respiratory.acid_base.henderson_hasselbalch"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.8"
    )
)

# Register in global index
register_equation(metabolic_alkalosis_compensation)

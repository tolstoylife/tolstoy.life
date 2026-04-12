"""Winter's Formula equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_winters_formula(HCO3: float) -> float:
    """
    Calculate expected PCO2 in metabolic acidosis.

    P_CO2 = 1.5 × [HCO3⁻] + 8 (± 2)

    Parameters
    ----------
    HCO3 : float
        Bicarbonate concentration (mEq/L)

    Returns
    -------
    float
        Expected PCO2 (mmHg)
    """
    return 1.5 * HCO3 + 8.0


# Create equation
winters_formula = create_equation(
    id="respiratory.acid_base.winters_formula",
    name="Winter's Formula",
    category=EquationCategory.RESPIRATORY,
    latex=r"P_{CO2} = 1.5 \times [HCO_3^-] + 8",
    simplified="P_CO2 = 1.5 × [HCO3⁻] + 8",
    description="Expected respiratory compensation for metabolic acidosis",
    compute_func=compute_winters_formula,
    parameters=[
        Parameter(
            name="HCO3",
            description="Bicarbonate concentration",
            units="mEq/L",
            symbol="[HCO_3^-]",
            physiological_range=(5.0, 40.0)
        )
    ],
    depends_on=["respiratory.acid_base.henderson_hasselbalch"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.8"
    )
)

# Register in global index
register_equation(winters_formula)

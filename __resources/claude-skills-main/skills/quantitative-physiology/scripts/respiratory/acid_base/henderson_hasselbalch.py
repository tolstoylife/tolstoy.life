"""Henderson-Hasselbalch Equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import math


def compute_henderson_hasselbalch(HCO3: float, PCO2: float, pKa: float, alpha: float) -> float:
    """
    Calculate pH using Henderson-Hasselbalch equation.

    pH = pKa + log([HCO3⁻]/(α × P_CO2))

    Parameters
    ----------
    HCO3 : float
        Bicarbonate concentration (mEq/L)
    PCO2 : float
        Partial pressure of CO2 (mmHg)
    pKa : float
        pKa of carbonic acid
    alpha : float
        CO2 solubility coefficient (mEq/L/mmHg)

    Returns
    -------
    float
        pH
    """
    return pKa + math.log10(HCO3 / (alpha * PCO2))


# Create equation
henderson_hasselbalch = create_equation(
    id="respiratory.acid_base.henderson_hasselbalch",
    name="Henderson-Hasselbalch Equation",
    category=EquationCategory.RESPIRATORY,
    latex=r"pH = pKa + \log\left(\frac{[HCO_3^-]}{\alpha \times P_{CO2}}\right)",
    simplified="pH = pKa + log([HCO3⁻]/(α × P_CO2))",
    description="Relationship between pH, bicarbonate, and PCO2 in blood",
    compute_func=compute_henderson_hasselbalch,
    parameters=[
        Parameter(
            name="HCO3",
            description="Bicarbonate concentration",
            units="mEq/L",
            symbol="[HCO_3^-]",
            default_value=24.0,
            physiological_range=(10.0, 40.0)
        ),
        Parameter(
            name="PCO2",
            description="Partial pressure of CO2",
            units="mmHg",
            symbol="P_{CO2}",
            default_value=40.0,
            physiological_range=(20.0, 80.0)
        ),
        Parameter(
            name="pKa",
            description="pKa of carbonic acid",
            units="dimensionless",
            symbol="pKa",
            default_value=6.1,
            physiological_range=(6.1, 6.1)
        ),
        Parameter(
            name="alpha",
            description="CO2 solubility",
            units="mEq/L/mmHg",
            symbol=r"\alpha",
            default_value=0.03,
            physiological_range=(0.03, 0.03)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.8"
    )
)

# Register in global index
register_equation(henderson_hasselbalch)

"""Alveolar Gas Equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_alveolar_gas_equation(P_iO2: float, P_ACO2: float, RQ: float) -> float:
    """
    Calculate alveolar PO2 (simplified form).

    P_AO2 = P_iO2 - P_ACO2/RQ

    Parameters
    ----------
    P_iO2 : float
        Inspired PO2 (mmHg)
    P_ACO2 : float
        Alveolar PCO2 (mmHg)
    RQ : float
        Respiratory quotient/exchange ratio (dimensionless, VCO2/VO2)

    Returns
    -------
    float
        Alveolar PO2 (mmHg)
    """
    return P_iO2 - (P_ACO2 / RQ)


# Create equation
alveolar_gas_equation = create_equation(
    id="respiratory.gas_exchange.alveolar_gas_equation",
    name="Alveolar Gas Equation",
    category=EquationCategory.RESPIRATORY,
    latex=r"P_{AO2} = P_{iO2} - \frac{P_{ACO2}}{R}",
    simplified="P_AO2 = P_iO2 - P_ACO2/R",
    description="Calculate alveolar oxygen partial pressure from inspired air and CO2",
    compute_func=compute_alveolar_gas_equation,
    parameters=[
        Parameter(
            name="P_iO2",
            description="Inspired PO2",
            units="mmHg",
            symbol="P_{iO2}",
            default_value=150.0,
            physiological_range=(50.0, 700.0)
        ),
        Parameter(
            name="P_ACO2",
            description="Alveolar PCO2",
            units="mmHg",
            symbol="P_{ACO2}",
            default_value=40.0,
            physiological_range=(20.0, 80.0)
        ),
        Parameter(
            name="RQ",
            description="Respiratory quotient/exchange ratio (VCO2/VO2)",
            units="dimensionless",
            symbol="R",
            default_value=0.8,
            physiological_range=(0.7, 1.0)
        )
    ],
    depends_on=["respiratory.gas_exchange.inspired_po2"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.3"
    )
)

# Register in global index
register_equation(alveolar_gas_equation)

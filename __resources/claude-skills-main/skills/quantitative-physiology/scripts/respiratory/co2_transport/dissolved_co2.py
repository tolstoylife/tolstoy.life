"""Dissolved CO2 equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_dissolved_co2(PCO2: float, alpha: float) -> float:
    """
    Calculate dissolved CO2 content.

    [CO2]_dissolved = α × P_CO2

    Parameters
    ----------
    PCO2 : float
        Partial pressure of CO2 (mmHg)
    alpha : float
        CO2 solubility coefficient (mL CO2/(dL·mmHg))

    Returns
    -------
    float
        Dissolved CO2 content (mL CO2/dL)
    """
    return alpha * PCO2


# Create equation
dissolved_co2 = create_equation(
    id="respiratory.co2_transport.dissolved_co2",
    name="Dissolved CO2",
    category=EquationCategory.RESPIRATORY,
    latex=r"[CO_2]_{dissolved} = \alpha \times P_{CO2}",
    simplified="[CO2]_dissolved = α × P_CO2",
    description="CO2 dissolved in plasma (~5% of total CO2)",
    compute_func=compute_dissolved_co2,
    parameters=[
        Parameter(
            name="PCO2",
            description="Partial pressure of CO2",
            units="mmHg",
            symbol="P_{CO2}",
            default_value=40.0,
            physiological_range=(20.0, 80.0)
        ),
        Parameter(
            name="alpha",
            description="CO2 solubility coefficient",
            units="mL CO2/(dL·mmHg)",
            symbol=r"\alpha",
            default_value=0.03,
            physiological_range=(0.03, 0.03)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.6"
    )
)

# Register in global index
register_equation(dissolved_co2)

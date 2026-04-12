"""Diffusing Capacity equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_diffusing_capacity(V_gas: float, P_A: float, P_c: float) -> float:
    """
    Calculate diffusing capacity of the lung.

    D_L = V̇_gas / (P_A - P_c)

    Parameters
    ----------
    V_gas : float
        Gas transfer rate (mL/min)
    P_A : float
        Alveolar partial pressure (mmHg)
    P_c : float
        Capillary partial pressure (mmHg)

    Returns
    -------
    float
        Diffusing capacity (mL/(min·mmHg))
    """
    return V_gas / (P_A - P_c)


# Create equation
diffusing_capacity = create_equation(
    id="respiratory.gas_exchange.diffusing_capacity",
    name="Diffusing Capacity",
    category=EquationCategory.RESPIRATORY,
    latex=r"D_L = \frac{\dot{V}_{gas}}{P_A - P_c}",
    simplified="D_L = V̇_gas / (P_A - P_c)",
    description="Measure of gas transfer efficiency across alveolar-capillary membrane",
    compute_func=compute_diffusing_capacity,
    parameters=[
        Parameter(
            name="V_gas",
            description="Gas transfer rate",
            units="mL/min",
            symbol=r"\dot{V}_{gas}",
            physiological_range=(1.0, 500.0)
        ),
        Parameter(
            name="P_A",
            description="Alveolar partial pressure",
            units="mmHg",
            symbol="P_A",
            physiological_range=(0.0, 150.0)
        ),
        Parameter(
            name="P_c",
            description="Capillary partial pressure",
            units="mmHg",
            symbol="P_c",
            physiological_range=(0.0, 100.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.3"
    )
)

# Register in global index
register_equation(diffusing_capacity)

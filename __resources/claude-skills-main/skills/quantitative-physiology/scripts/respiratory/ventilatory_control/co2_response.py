"""CO2 Ventilatory Response equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_co2_response(PaCO2: float, VE0: float, S: float, threshold: float) -> float:
    """
    Calculate ventilatory response to CO2.

    V̇E = V̇E₀ + S × (P_aCO2 - threshold)

    Parameters
    ----------
    PaCO2 : float
        Arterial PCO2 (mmHg)
    VE0 : float
        Baseline ventilation (L/min)
    S : float
        CO2 sensitivity (L/min/mmHg)
    threshold : float
        Apneic threshold (mmHg)

    Returns
    -------
    float
        Minute ventilation (L/min)
    """
    VE = VE0 + S * (PaCO2 - threshold)
    return max(0.0, VE)


# Create equation
co2_response = create_equation(
    id="respiratory.ventilatory_control.co2_response",
    name="CO2 Ventilatory Response",
    category=EquationCategory.RESPIRATORY,
    latex=r"\dot{V}_E = \dot{V}_{E0} + S \times (P_{aCO2} - threshold)",
    simplified="V̇E = V̇E₀ + S × (P_aCO2 - threshold)",
    description="Linear increase in ventilation with rising CO2",
    compute_func=compute_co2_response,
    parameters=[
        Parameter(
            name="PaCO2",
            description="Arterial PCO2",
            units="mmHg",
            symbol="P_{aCO2}",
            default_value=40.0,
            physiological_range=(20.0, 80.0)
        ),
        Parameter(
            name="VE0",
            description="Baseline ventilation",
            units="L/min",
            symbol=r"\dot{V}_{E0}",
            default_value=5.0,
            physiological_range=(3.0, 10.0)
        ),
        Parameter(
            name="S",
            description="CO2 sensitivity",
            units="L/min/mmHg",
            symbol="S",
            default_value=2.5,
            physiological_range=(1.0, 5.0)
        ),
        Parameter(
            name="threshold",
            description="Apneic threshold",
            units="mmHg",
            symbol="threshold",
            default_value=40.0,
            physiological_range=(30.0, 45.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.7"
    )
)

# Register in global index
register_equation(co2_response)

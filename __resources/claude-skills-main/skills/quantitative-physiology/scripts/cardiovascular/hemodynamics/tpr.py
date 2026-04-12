"""Total peripheral resistance equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_tpr(MAP: float, CVP: float, CO: float) -> float:
    """
    Calculate total peripheral resistance.

    Parameters
    ----------
    MAP : float
        Mean arterial pressure (mmHg)
    CVP : float
        Central venous pressure (mmHg)
    CO : float
        Cardiac output (L/min)

    Returns
    -------
    float
        Total peripheral resistance (Wood units = mmHg/(L/min))
    """
    return (MAP - CVP) / CO


tpr = create_equation(
    id="cardiovascular.hemodynamics.total_peripheral_resistance",
    name="Total Peripheral Resistance",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{TPR} = \frac{\text{MAP} - \text{CVP}}{\text{CO}}",
    simplified="TPR = (MAP - CVP) / CO",
    description="Systemic vascular resistance in Wood units",
    compute_func=compute_tpr,
    parameters=[
        Parameter(
            name="MAP",
            description="Mean arterial pressure",
            units="mmHg",
            symbol="MAP",
            physiological_range=(70.0, 105.0)
        ),
        Parameter(
            name="CVP",
            description="Central venous pressure",
            units="mmHg",
            symbol="CVP",
            default_value=0.0,
            physiological_range=(0.0, 8.0)
        ),
        Parameter(
            name="CO",
            description="Cardiac output",
            units="L/min",
            symbol="CO",
            physiological_range=(4.0, 8.0)
        )
    ],
    depends_on=["cardiovascular.cardiac.cardiac_output"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(tpr)

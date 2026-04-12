"""Windkessel time constant equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_windkessel_tau(R: float, C: float) -> float:
    """
    Calculate arterial windkessel time constant.

    Parameters
    ----------
    R : float
        Arterial resistance (Wood units)
    C : float
        Arterial compliance (mL/mmHg)

    Returns
    -------
    float
        Time constant (s)
    """
    # Convert Wood units (mmHg/(L/min)) to (mmHg·s/mL)
    # 1 Wood unit = 1 mmHg/(L/min) = 60 mmHg·s/L = 0.06 mmHg·s/mL
    R_converted = R * 0.06
    return R_converted * C


windkessel_tau = create_equation(
    id="cardiovascular.hemodynamics.windkessel_time_constant",
    name="Windkessel Time Constant",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\tau = R \times C",
    simplified="τ = R × C",
    description="Exponential decay time constant for arterial pressure",
    compute_func=compute_windkessel_tau,
    parameters=[
        Parameter(
            name="R",
            description="Arterial resistance",
            units="Wood units",
            symbol="R",
            physiological_range=(15.0, 25.0)
        ),
        Parameter(
            name="C",
            description="Arterial compliance",
            units="mL/mmHg",
            symbol="C",
            physiological_range=(1.0, 2.5)
        )
    ],
    depends_on=["cardiovascular.hemodynamics.vascular_compliance", "cardiovascular.hemodynamics.total_peripheral_resistance"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(windkessel_tau)

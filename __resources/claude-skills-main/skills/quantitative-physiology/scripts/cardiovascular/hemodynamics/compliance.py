"""Vascular compliance definition."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_compliance(dV: float, dP: float) -> float:
    """
    Calculate vascular compliance.

    Parameters
    ----------
    dV : float
        Change in volume (mL)
    dP : float
        Change in pressure (mmHg)

    Returns
    -------
    float
        Compliance (mL/mmHg)
    """
    return dV / dP


compliance = create_equation(
    id="cardiovascular.hemodynamics.vascular_compliance",
    name="Vascular Compliance",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"C = \frac{\Delta V}{\Delta P}",
    simplified="C = ΔV / ΔP",
    description="Change in vessel volume per unit change in pressure",
    compute_func=compute_compliance,
    parameters=[
        Parameter(
            name="dV",
            description="Change in volume",
            units="mL",
            symbol=r"\Delta V",
            physiological_range=(0.1, 100.0)
        ),
        Parameter(
            name="dP",
            description="Change in pressure",
            units="mmHg",
            symbol=r"\Delta P",
            physiological_range=(1.0, 50.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(compliance)

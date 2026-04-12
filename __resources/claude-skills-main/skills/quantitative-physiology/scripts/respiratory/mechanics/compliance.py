"""Compliance equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_compliance(delta_V: float, delta_P: float) -> float:
    """
    Calculate compliance (change in volume per unit pressure).

    C = ΔV / ΔP

    Parameters
    ----------
    delta_V : float
        Change in volume (L)
    delta_P : float
        Change in pressure (cmH2O)

    Returns
    -------
    float
        Compliance (L/cmH2O)
    """
    return delta_V / delta_P


# Create equation
compliance = create_equation(
    id="respiratory.mechanics.compliance",
    name="Compliance",
    category=EquationCategory.RESPIRATORY,
    latex=r"C = \frac{\Delta V}{\Delta P}",
    simplified="C = ΔV / ΔP",
    description="Measure of lung distensibility - change in volume per unit pressure change",
    compute_func=compute_compliance,
    parameters=[
        Parameter(
            name="delta_V",
            description="Change in volume",
            units="L",
            symbol=r"\Delta V",
            physiological_range=(0.0, 5.0)
        ),
        Parameter(
            name="delta_P",
            description="Change in pressure",
            units="cmH2O",
            symbol=r"\Delta P",
            physiological_range=(0.0, 30.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(compliance)

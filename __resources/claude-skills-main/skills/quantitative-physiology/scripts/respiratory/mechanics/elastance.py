"""Elastance equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_elastance(C: float) -> float:
    """
    Calculate elastance (inverse of compliance).

    E = 1/C = ΔP/ΔV

    Parameters
    ----------
    C : float
        Compliance (L/cmH2O)

    Returns
    -------
    float
        Elastance (cmH2O/L)
    """
    return 1.0 / C


# Create equation
elastance = create_equation(
    id="respiratory.mechanics.elastance",
    name="Elastance",
    category=EquationCategory.RESPIRATORY,
    latex=r"E = \frac{1}{C} = \frac{\Delta P}{\Delta V}",
    simplified="E = 1/C = ΔP/ΔV",
    description="Elastic recoil tendency - inverse of compliance",
    compute_func=compute_elastance,
    parameters=[
        Parameter(
            name="C",
            description="Compliance",
            units="L/cmH2O",
            symbol="C",
            default_value=0.2,
            physiological_range=(0.05, 0.4)
        )
    ],
    depends_on=["respiratory.mechanics.compliance"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(elastance)

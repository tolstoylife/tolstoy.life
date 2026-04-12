"""Partial Pressure (Dalton's Law) equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_partial_pressure(F_i: float, P_total: float) -> float:
    """
    Calculate partial pressure using Dalton's Law.

    P_i = F_i × P_total

    Parameters
    ----------
    F_i : float
        Fraction of gas i (0-1)
    P_total : float
        Total pressure (mmHg)

    Returns
    -------
    float
        Partial pressure of gas i (mmHg)
    """
    return F_i * P_total


# Create equation
partial_pressure = create_equation(
    id="respiratory.gas_exchange.partial_pressure",
    name="Dalton's Law of Partial Pressures",
    category=EquationCategory.RESPIRATORY,
    latex=r"P_i = F_i \times P_{total}",
    simplified="P_i = F_i × P_total",
    description="Partial pressure of a gas in a mixture equals its fraction times total pressure",
    compute_func=compute_partial_pressure,
    parameters=[
        Parameter(
            name="F_i",
            description="Fraction of gas i",
            units="dimensionless",
            symbol="F_i",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="P_total",
            description="Total pressure",
            units="mmHg",
            symbol="P_{total}",
            default_value=760.0,
            physiological_range=(200.0, 800.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.3"
    )
)

# Register in global index
register_equation(partial_pressure)

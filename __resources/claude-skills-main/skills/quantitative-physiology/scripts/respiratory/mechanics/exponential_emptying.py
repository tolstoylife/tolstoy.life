"""Exponential Emptying equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import math


def compute_exponential_emptying(V0: float, t: float, tau: float) -> float:
    """
    Calculate lung volume during passive expiration.

    V(t) = V₀ × e^(-t/τ)

    Parameters
    ----------
    V0 : float
        Initial volume (L)
    t : float
        Time (s)
    tau : float
        Time constant (s)

    Returns
    -------
    float
        Volume at time t (L)
    """
    return V0 * math.exp(-t / tau)


# Create equation
exponential_emptying = create_equation(
    id="respiratory.mechanics.exponential_emptying",
    name="Exponential Emptying",
    category=EquationCategory.RESPIRATORY,
    latex=r"V(t) = V_0 \times e^{-t/\tau}",
    simplified="V(t) = V₀ × e^(-t/τ)",
    description="Volume decay during passive expiration",
    compute_func=compute_exponential_emptying,
    parameters=[
        Parameter(
            name="V0",
            description="Initial volume",
            units="L",
            symbol="V_0",
            physiological_range=(0.5, 6.0)
        ),
        Parameter(
            name="t",
            description="Time",
            units="s",
            symbol="t",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="tau",
            description="Time constant",
            units="s",
            symbol=r"\tau",
            default_value=0.5,
            physiological_range=(0.1, 2.0)
        )
    ],
    depends_on=["respiratory.mechanics.time_constant"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(exponential_emptying)

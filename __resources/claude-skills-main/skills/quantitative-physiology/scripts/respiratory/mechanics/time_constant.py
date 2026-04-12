"""Time Constant equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_time_constant(R: float, C: float) -> float:
    """
    Calculate time constant for exponential filling/emptying.

    τ = R × C

    Parameters
    ----------
    R : float
        Resistance (cmH2O/(L/s))
    C : float
        Compliance (L/cmH2O)

    Returns
    -------
    float
        Time constant (s)
    """
    return R * C


# Create equation
time_constant = create_equation(
    id="respiratory.mechanics.time_constant",
    name="Respiratory Time Constant (τ = RC)",
    category=EquationCategory.RESPIRATORY,
    latex=r"\tau = R \times C",
    simplified="τ = R × C",
    description="Time constant for exponential lung filling/emptying (3τ ≈ 95% complete)",
    compute_func=compute_time_constant,
    parameters=[
        Parameter(
            name="R",
            description="Airway resistance",
            units="cmH2O/(L/s)",
            symbol="R",
            default_value=1.5,
            physiological_range=(0.5, 5.0)
        ),
        Parameter(
            name="C",
            description="Compliance",
            units="L/cmH2O",
            symbol="C",
            default_value=0.1,
            physiological_range=(0.05, 0.3)
        )
    ],
    depends_on=["respiratory.mechanics.airway_resistance", "respiratory.mechanics.compliance"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(time_constant)

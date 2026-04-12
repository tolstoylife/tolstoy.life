"""
Hormone half-life from volume of distribution and clearance.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_half_life(Vd: float, CL: float) -> float:
    """
    Calculate hormone half-life.

    Parameters
    ----------
    Vd : float
        Volume of distribution (L)
    CL : float
        Clearance rate (L/time)

    Returns
    -------
    float
        Half-life (same time units as CL)

    Notes
    -----
    Typical half-lives:
    - Epinephrine: 1-2 min
    - Insulin: 5-10 min
    - Cortisol: 60-90 min
    - T4: 6-7 days
    - T3: 1 day
    """
    return 0.693 * Vd / CL


# Create equation
half_life_equation = create_equation(
    id="endocrine.kinetics.half_life",
    name="Hormone Half-Life",
    category=EquationCategory.ENDOCRINE,
    latex=r"t_{1/2} = \frac{0.693 \times V_d}{CL}",
    simplified="t_half = 0.693 × V_d / CL",
    description="Half-life of hormone in circulation, determined by volume of distribution "
                "and clearance rate. Factor 0.693 = ln(2).",
    compute_func=compute_half_life,
    parameters=[
        Parameter(
            name="Vd",
            description="Volume of distribution",
            units="L",
            symbol="V_d",
            physiological_range=(1.0, 100.0)
        ),
        Parameter(
            name="CL",
            description="Clearance rate",
            units="L/min or L/hour",
            symbol="CL",
            physiological_range=(0.01, 100.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.1"
    )
)

# Register globally
register_equation(half_life_equation)

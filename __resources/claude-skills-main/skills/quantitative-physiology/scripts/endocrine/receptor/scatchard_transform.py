"""
Scatchard plot transformation for linearizing binding data.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_scatchard_y(B: float, H: float) -> float:
    """
    Calculate y-axis value for Scatchard plot (B/[H]).

    Parameters
    ----------
    B : float
        Bound hormone concentration (M)
    H : float
        Free hormone concentration (M)

    Returns
    -------
    float
        B/[H] ratio (dimensionless)

    Notes
    -----
    Scatchard equation: B/[H] = B_max/K_d - B/K_d
    Plot B/[H] vs B gives:
    - Slope = -1/K_d
    - x-intercept = B_max
    - y-intercept = B_max/K_d
    """
    return B / H


# Create equation
scatchard_equation = create_equation(
    id="endocrine.receptor.scatchard_transform",
    name="Scatchard Plot Transformation",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{B}{[H]} = \frac{B_{max}}{K_d} - \frac{B}{K_d}",
    simplified="B/[H] = B_max/K_d - B/K_d",
    description="Scatchard analysis linearizes binding data. Plot of B/[H] vs B yields "
                "slope = -1/K_d and x-intercept = B_max.",
    compute_func=compute_scatchard_y,
    parameters=[
        Parameter(
            name="B",
            description="Bound hormone concentration",
            units="M",
            symbol="B",
            physiological_range=(1e-12, 1e-6)
        ),
        Parameter(
            name="H",
            description="Free hormone concentration",
            units="M",
            symbol="[H]",
            physiological_range=(1e-12, 1e-6)
        )
    ],
    depends_on=["endocrine.receptor.saturation_binding"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.2"
    )
)

# Register globally
register_equation(scatchard_equation)

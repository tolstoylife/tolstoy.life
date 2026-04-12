"""
Diffusion Time - Characteristic time for diffusion over distance

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_diffusion_time(x: float, D: float) -> float:
    """
    Calculate characteristic time for diffusion over distance x.

    Formula: t = x²/(2D)

    Parameters:
    -----------
    x : float - Distance (m)
    D : float - Diffusion coefficient (m²/s)

    Returns:
    --------
    t : float - Diffusion time (s)
    """
    return x**2 / (2 * D)


# Create and register atomic equation
diffusion_time = create_equation(
    id="foundations.diffusion.diffusion_time",
    name="Diffusion Time",
    category=EquationCategory.FOUNDATIONS,
    latex=r"t = \frac{x^2}{2D}",
    simplified="t = x^2 / (2*D)",
    description="Time for diffusion scales as distance squared - explains why circulation is needed for large organisms",
    compute_func=compute_diffusion_time,
    parameters=[
        Parameter(
            name="x",
            description="Diffusion distance",
            units="m",
            symbol="x",
            physiological_range=(1e-9, 1e-2)  # nm to cm
        ),
        Parameter(
            name="D",
            description="Diffusion coefficient",
            units="m²/s",
            symbol="D",
            physiological_range=(1e-11, 1e-8)
        )
    ],
    depends_on=["foundations.diffusion.fick_first_law"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.3")
)

register_equation(diffusion_time)

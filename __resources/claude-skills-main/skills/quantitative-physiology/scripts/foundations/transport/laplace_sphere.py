"""
Law of Laplace (Sphere) - Wall tension in alveoli and cells

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_laplace_sphere_pressure(T: float, r: float) -> float:
    """
    Calculate transmural pressure from wall tension (sphere geometry).

    Formula: ΔP = 2T/r

    Parameters:
    -----------
    T : float - Surface tension (N/m)
    r : float - Sphere radius (m)

    Returns:
    --------
    delta_P : float - Transmural pressure (Pa)
    """
    return 2 * T / r


def compute_laplace_sphere_tension(delta_P: float, r: float) -> float:
    """
    Calculate surface tension from transmural pressure (sphere geometry).

    Formula: T = ΔP × r/2

    Parameters:
    -----------
    delta_P : float - Transmural pressure (Pa)
    r : float - Sphere radius (m)

    Returns:
    --------
    T : float - Surface tension (N/m)
    """
    return delta_P * r / 2


# Create and register atomic equation
laplace_sphere = create_equation(
    id="foundations.transport.laplace_sphere",
    name="Law of Laplace (Sphere)",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\Delta P = \frac{2T}{r} \quad \text{or} \quad T = \frac{\Delta P \times r}{2}",
    simplified="delta_P = 2*T / r  or  T = delta_P * r / 2",
    description="Relates surface tension to transmural pressure in spherical structures (e.g., alveoli, cells)",
    compute_func=compute_laplace_sphere_pressure,
    parameters=[
        Parameter(
            name="T",
            description="Surface tension",
            units="N/m",
            symbol="T",
            physiological_range=(0.0, 0.1)  # surfactant reduces to ~0.025 N/m
        ),
        Parameter(
            name="r",
            description="Sphere radius",
            units="m",
            symbol="r",
            physiological_range=(1e-7, 1e-3)  # cells to alveoli
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.1")
)

register_equation(laplace_sphere)

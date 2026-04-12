"""
Law of Laplace (Cylinder) - Wall tension in blood vessels

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_laplace_cylinder_pressure(T: float, r: float) -> float:
    """
    Calculate transmural pressure from wall tension (cylinder geometry).

    Formula: ΔP = T/r

    Parameters:
    -----------
    T : float - Wall tension (N/m)
    r : float - Vessel radius (m)

    Returns:
    --------
    delta_P : float - Transmural pressure (Pa)
    """
    return T / r


def compute_laplace_cylinder_tension(delta_P: float, r: float) -> float:
    """
    Calculate wall tension from transmural pressure (cylinder geometry).

    Formula: T = ΔP × r

    Parameters:
    -----------
    delta_P : float - Transmural pressure (Pa)
    r : float - Vessel radius (m)

    Returns:
    --------
    T : float - Wall tension (N/m)
    """
    return delta_P * r


# Create and register atomic equation
laplace_cylinder = create_equation(
    id="foundations.transport.laplace_cylinder",
    name="Law of Laplace (Cylinder)",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\Delta P = \frac{T}{r} \quad \text{or} \quad T = \Delta P \times r",
    simplified="delta_P = T / r  or  T = delta_P * r",
    description="Relates wall tension to transmural pressure in cylindrical vessels (e.g., blood vessels)",
    compute_func=compute_laplace_cylinder_pressure,
    parameters=[
        Parameter(
            name="T",
            description="Wall tension",
            units="N/m",
            symbol="T",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="r",
            description="Vessel radius",
            units="m",
            symbol="r",
            physiological_range=(1e-6, 1e-2)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.1")
)

register_equation(laplace_cylinder)

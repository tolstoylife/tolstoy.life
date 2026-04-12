"""
Coulomb's Law in Medium - Electrostatic force in dielectric medium

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_coulomb_force_medium(q1: float, q2: float, r: float, epsilon: float,
                                epsilon_0: float = 8.85e-12) -> float:
    """
    Calculate electrostatic force in a dielectric medium.

    Formula: F = (q₁q₂)/(4πεε₀r²)

    Parameters:
    -----------
    q1 : float - Charge 1 (C)
    q2 : float - Charge 2 (C)
    r : float - Separation distance (m)
    epsilon : float - Relative permittivity (dielectric constant)
    epsilon_0 : float - Permittivity of free space (C²/(J·m))

    Returns:
    --------
    F : float - Electrostatic force (N)
    """
    return (q1 * q2) / (4 * np.pi * epsilon * epsilon_0 * r**2)


# Create and register atomic equation
coulomb_law_medium = create_equation(
    id="foundations.electrical.coulomb_law_medium",
    name="Coulomb's Law in Medium",
    category=EquationCategory.FOUNDATIONS,
    latex=r"F = \frac{q_1 q_2}{4\pi\epsilon\epsilon_0 r^2}",
    simplified="F = (q1 * q2) / (4 * pi * epsilon * epsilon_0 * r^2)",
    description="Electrostatic force between charges in dielectric medium (e.g., water, ε≈80)",
    compute_func=compute_coulomb_force_medium,
    parameters=[
        Parameter(
            name="q1",
            description="Charge 1",
            units="C",
            symbol=r"q_1",
            physiological_range=(-1e-15, 1e-15)
        ),
        Parameter(
            name="q2",
            description="Charge 2",
            units="C",
            symbol=r"q_2",
            physiological_range=(-1e-15, 1e-15)
        ),
        Parameter(
            name="r",
            description="Separation distance",
            units="m",
            symbol="r",
            physiological_range=(1e-10, 1e-6)
        ),
        Parameter(
            name="epsilon",
            description="Relative permittivity (dielectric constant)",
            units="dimensionless",
            symbol=r"\epsilon",
            default_value=80.0,  # water
            physiological_range=(1.0, 80.0)
        ),
        Parameter(
            name="epsilon_0",
            description="Permittivity of free space",
            units="C²/(J·m)",
            symbol=r"\epsilon_0",
            default_value=8.85e-12
        )
    ],
    depends_on=["foundations.electrical.coulomb_law"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.2")
)

register_equation(coulomb_law_medium)

"""
Stokes-Einstein Equation - Diffusion coefficient for spherical particles

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation
import numpy as np


def compute_stokes_einstein(T: float, eta: float, a: float, k_B: float = 1.38e-23) -> float:
    """
    Calculate diffusion coefficient for spherical particle.

    Formula: D = kT/(6πηa)

    Parameters:
    -----------
    T : float - Temperature (K)
    eta : float - Viscosity (Pa·s)
    a : float - Particle radius (m)
    k_B : float - Boltzmann constant (J/K)

    Returns:
    --------
    D : float - Diffusion coefficient (m²/s)
    """
    return (k_B * T) / (6 * np.pi * eta * a)


# Create and register atomic equation
stokes_einstein = create_equation(
    id="foundations.diffusion.stokes_einstein",
    name="Stokes-Einstein Equation",
    category=EquationCategory.FOUNDATIONS,
    latex=r"D = \frac{kT}{6\pi\eta a}",
    simplified="D = (k*T) / (6*pi*eta*a)",
    description="Diffusion coefficient for spherical particle - inversely proportional to particle size",
    compute_func=compute_stokes_einstein,
    parameters=[
        Parameter(
            name="T",
            description="Temperature",
            units="K",
            symbol="T",
            default_value=310.0,
            physiological_range=(273.0, 320.0)
        ),
        Parameter(
            name="eta",
            description="Fluid viscosity",
            units="Pa·s",
            symbol=r"\eta",
            default_value=7e-4,  # water at 37°C
            physiological_range=(1e-4, 1e-2)
        ),
        Parameter(
            name="a",
            description="Particle radius",
            units="m",
            symbol="a",
            physiological_range=(1e-10, 1e-7)  # ions to proteins
        ),
        PHYSICAL_CONSTANTS["k_B"]
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.3")
)

register_equation(stokes_einstein)

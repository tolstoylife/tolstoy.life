"""
Fick's First Law - Diffusive flux proportional to concentration gradient

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_fick_first_law(D: float, dC_dx: float) -> float:
    """
    Calculate diffusive flux from concentration gradient.

    Formula: J_S = -D(∂C/∂x)

    Parameters:
    -----------
    D : float - Diffusion coefficient (m²/s)
    dC_dx : float - Concentration gradient (mol/m⁴)

    Returns:
    --------
    J_S : float - Diffusive flux (mol/(m²·s))
    """
    return -D * dC_dx


# Create and register atomic equation
fick_first_law = create_equation(
    id="foundations.diffusion.fick_first_law",
    name="Fick's First Law",
    category=EquationCategory.FOUNDATIONS,
    latex=r"J_S = -D\frac{\partial C}{\partial x}",
    simplified="J_S = -D * (dC/dx)",
    description="Diffusive flux proportional to concentration gradient - negative sign means flow down gradient",
    compute_func=compute_fick_first_law,
    parameters=[
        Parameter(
            name="D",
            description="Diffusion coefficient",
            units="m²/s",
            symbol="D",
            physiological_range=(1e-11, 1e-8)  # proteins to small ions
        ),
        Parameter(
            name="dC_dx",
            description="Concentration gradient",
            units="mol/m⁴",
            symbol=r"\frac{\partial C}{\partial x}",
            physiological_range=(-1e6, 1e6)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.3")
)

register_equation(fick_first_law)

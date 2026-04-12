"""
Solute Flux - Amount of solute per unit area per unit time

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_solute_flux(Q_S: float, A: float) -> float:
    """
    Calculate solute flux from solute flow rate and area.

    Formula: J_S = Q_S / A

    Parameters:
    -----------
    Q_S : float - Solute flow rate (mol/s)
    A : float - Cross-sectional area (m²)

    Returns:
    --------
    J_S : float - Solute flux (mol/(m²·s))
    """
    return Q_S / A


# Create and register atomic equation
solute_flux = create_equation(
    id="foundations.transport.solute_flux",
    name="Solute Flux",
    category=EquationCategory.FOUNDATIONS,
    latex=r"J_S = \frac{Q_S}{A}",
    simplified="J_S = Q_S / A",
    description="Amount of solute per unit area per unit time",
    compute_func=compute_solute_flux,
    parameters=[
        Parameter(
            name="Q_S",
            description="Solute flow rate",
            units="mol/s",
            symbol=r"Q_S",
            physiological_range=(0.0, 1e-3)
        ),
        Parameter(
            name="A",
            description="Cross-sectional area",
            units="m²",
            symbol="A",
            physiological_range=(1e-12, 1e-3)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.1")
)

register_equation(solute_flux)

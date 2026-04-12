"""
Receptor Fractional Occupancy - Ligand-receptor binding equilibrium

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_receptor_occupancy(L: float, K_d: float) -> float:
    """
    Calculate fractional receptor occupancy (ligand binding).

    Formula: f = [L] / (K_d + [L])

    Based on equilibrium: R + L ⇌ RL, K_d = [R][L]/[RL]

    Parameters:
    -----------
    L : float
        Ligand concentration (mol/m³, nM, or μM)
    K_d : float
        Dissociation constant (same units as L)

    Returns:
    --------
    f : float
        Fractional occupancy (0-1)
        0 = no receptors bound
        1 = all receptors saturated

    Notes:
        At [L] = K_d, f = 0.5 (half-maximal binding)
        Similar to Michaelis-Menten form
    """
    return L / (K_d + L)


# Create and register atomic equation
receptor_occupancy = create_equation(
    id="membrane.signaling.receptor_occupancy",
    name="Receptor Fractional Occupancy",
    category=EquationCategory.MEMBRANE,
    latex=r"f = \frac{[L]}{K_d + [L]}",
    simplified="f = [L] / (K_d + [L])",
    description="Fractional occupancy of receptors by ligand at equilibrium, following hyperbolic binding.",
    compute_func=compute_receptor_occupancy,
    parameters=[
        Parameter(
            name="L",
            description="Ligand concentration",
            units="mol/m³",
            symbol="[L]",
            default_value=None,
            physiological_range=(0.0, 1e6)  # Wide range (nM to mM)
        ),
        Parameter(
            name="K_d",
            description="Dissociation constant",
            units="mol/m³",
            symbol="K_d",
            default_value=None,
            physiological_range=(1e-3, 1e6)  # pM to mM
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.6")
)

register_equation(receptor_occupancy)

"""
Nernst potential for potassium in renal tubular cells.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

import math
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation


def compute_k_nernst(K_lumen: float, K_cell: float, T: float = 310.0) -> float:
    """
    Calculate Nernst potential for K+ across tubular cell membrane.

    Args:
        K_lumen: Luminal K+ concentration (mM)
        K_cell: Intracellular K+ concentration (mM)
        T: Temperature (K, default 310 = 37°C)

    Returns:
        E_K: K+ equilibrium potential (mV)
    """
    R = PHYSICAL_CONSTANTS["R"].default_value
    F = PHYSICAL_CONSTANTS["F"].default_value

    return (R * T / F) * math.log(K_lumen / K_cell) * 1000  # Convert to mV


# Create equation
k_nernst_potential = create_equation(
    id="renal.potassium.k_nernst_potential",
    name="K+ Nernst Potential (Renal)",
    category=EquationCategory.RENAL,
    latex=r"E_K = \frac{RT}{F} \ln\left(\frac{[K^+]_{lumen}}{[K^+]_{cell}}\right)",
    simplified="E_K = (RT/F) × ln([K+]_lumen / [K+]_cell)",
    description="Equilibrium potential for K+ across tubular epithelial cell membrane",
    compute_func=compute_k_nernst,
    parameters=[
        Parameter(
            name="K_lumen",
            description="Luminal K+ concentration",
            units="mM",
            symbol="[K^+]_{lumen}",
            physiological_range=(1, 100)
        ),
        Parameter(
            name="K_cell",
            description="Intracellular K+ concentration",
            units="mM",
            symbol="[K^+]_{cell}",
            physiological_range=(120, 150)
        ),
        Parameter(
            name="T",
            description="Temperature",
            units="K",
            symbol="T",
            default_value=310.0,
            physiological_range=(306, 315)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.8"
    )
)

# Register equation
register_equation(k_nernst_potential)

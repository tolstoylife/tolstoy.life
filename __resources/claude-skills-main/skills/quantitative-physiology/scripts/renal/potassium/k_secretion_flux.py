"""
Potassium secretion flux through ROMK channels.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_k_secretion_flux(g_K: float, V_m: float, E_K: float) -> float:
    """
    Calculate K+ secretion flux.

    Args:
        g_K: K+ conductance (S or mS)
        V_m: Membrane potential (mV)
        E_K: K+ equilibrium potential (mV)

    Returns:
        J_K: K+ flux (current or flux units depending on g_K)
    """
    return g_K * (V_m - E_K)


# Create equation
k_secretion_flux = create_equation(
    id="renal.potassium.k_secretion_flux",
    name="K+ Secretion Flux",
    category=EquationCategory.RENAL,
    latex=r"J_K = g_K \times (V_m - E_K)",
    simplified="J_K = g_K × (V_m - E_K)",
    description="K+ flux through ROMK channels driven by electrochemical gradient",
    compute_func=compute_k_secretion_flux,
    parameters=[
        Parameter(
            name="g_K",
            description="K+ conductance",
            units="S or mS",
            symbol="g_K",
            physiological_range=(0.001, 1.0)
        ),
        Parameter(
            name="V_m",
            description="Membrane potential",
            units="mV",
            symbol="V_m",
            physiological_range=(-80, -20)
        ),
        Parameter(
            name="E_K",
            description="K+ equilibrium potential",
            units="mV",
            symbol="E_K",
            physiological_range=(-100, -50)
        )
    ],
    depends_on=["renal.potassium.k_secretion_driving_force", "renal.potassium.k_nernst_potential"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.8"
    )
)

# Register equation
register_equation(k_secretion_flux)

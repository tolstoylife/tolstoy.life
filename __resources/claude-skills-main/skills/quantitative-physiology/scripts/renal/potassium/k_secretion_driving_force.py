"""
Electrochemical driving force for potassium secretion.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_k_driving_force(V_m: float, E_K: float) -> float:
    """
    Calculate electrochemical driving force for K+ secretion.

    Args:
        V_m: Membrane potential (mV)
        E_K: K+ equilibrium potential (mV)

    Returns:
        Driving force (mV), positive = secretion favored
    """
    return V_m - E_K


# Create equation
k_secretion_driving_force = create_equation(
    id="renal.potassium.k_secretion_driving_force",
    name="K+ Secretion Driving Force",
    category=EquationCategory.RENAL,
    latex=r"DF_K = V_m - E_K",
    simplified="DF_K = V_m - E_K",
    description="Electrochemical gradient driving K+ secretion from principal cells into tubular lumen",
    compute_func=compute_k_driving_force,
    parameters=[
        Parameter(
            name="V_m",
            description="Membrane potential",
            units="mV",
            symbol="V_m",
            physiological_range=(-80, -20)
        ),
        Parameter(
            name="E_K",
            description="K+ equilibrium potential (Nernst)",
            units="mV",
            symbol="E_K",
            physiological_range=(-100, -50)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.8"
    )
)

# Register equation
register_equation(k_secretion_driving_force)

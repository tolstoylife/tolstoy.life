"""
Actual Free Energy - Free energy under non-standard conditions

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation
import numpy as np


def compute_actual_free_energy(delta_G0: float, Q: float, R: float = 8.314, T_body: float = 310.0) -> float:
    """
    Calculate actual free energy change from standard conditions.

    Formula: ΔG = ΔG° + RT ln(Q)

    Parameters:
    -----------
    delta_G0 : float - Standard free energy change (J/mol)
    Q : float - Reaction quotient (dimensionless)
    R : float - Gas constant (J/(mol·K))
    T_body : float - Body temperature (K)

    Returns:
    --------
    delta_G : float - Actual free energy change (J/mol)
    """
    return delta_G0 + R * T_body * np.log(Q)


# Create and register atomic equation
actual_free_energy = create_equation(
    id="foundations.thermodynamics.actual_free_energy",
    name="Actual Free Energy",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\Delta G = \Delta G^\circ + RT \ln(Q)",
    simplified="delta_G = delta_G0 + R*T*ln(Q)",
    description="Free energy change under actual cellular conditions - Q is reaction quotient",
    compute_func=compute_actual_free_energy,
    parameters=[
        Parameter(
            name="delta_G0",
            description="Standard free energy change",
            units="J/mol",
            symbol=r"\Delta G^\circ",
            physiological_range=(-1e6, 1e6)
        ),
        Parameter(
            name="Q",
            description="Reaction quotient",
            units="dimensionless",
            symbol="Q",
            physiological_range=(1e-10, 1e10)
        ),
        PHYSICAL_CONSTANTS["R"],
        PHYSICAL_CONSTANTS["T_body"]
    ],
    depends_on=["foundations.thermodynamics.standard_free_energy"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.4")
)

register_equation(actual_free_energy)

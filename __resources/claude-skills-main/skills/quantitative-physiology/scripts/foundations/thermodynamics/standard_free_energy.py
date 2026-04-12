"""
Standard Free Energy - Relationship to equilibrium constant

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation
import numpy as np


def compute_standard_free_energy(K_eq: float, R: float = 8.314, T_body: float = 310.0) -> float:
    """
    Calculate standard free energy from equilibrium constant.

    Formula: ΔG° = -RT ln(K_eq)

    Parameters:
    -----------
    K_eq : float - Equilibrium constant (dimensionless)
    R : float - Gas constant (J/(mol·K))
    T_body : float - Body temperature (K)

    Returns:
    --------
    delta_G0 : float - Standard free energy change (J/mol)
    """
    return -R * T_body * np.log(K_eq)


# Create and register atomic equation
standard_free_energy = create_equation(
    id="foundations.thermodynamics.standard_free_energy",
    name="Standard Free Energy",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\Delta G^\circ = -RT \ln(K_{eq})",
    simplified="delta_G0 = -R*T*ln(K_eq)",
    description="Standard free energy at 1M concentrations, 1 atm, 25°C",
    compute_func=compute_standard_free_energy,
    parameters=[
        Parameter(
            name="K_eq",
            description="Equilibrium constant",
            units="dimensionless",
            symbol=r"K_{eq}",
            physiological_range=(1e-10, 1e10)
        ),
        PHYSICAL_CONSTANTS["R"],
        PHYSICAL_CONSTANTS["T_body"]
    ],
    depends_on=["foundations.thermodynamics.gibbs_free_energy"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.4")
)

register_equation(standard_free_energy)

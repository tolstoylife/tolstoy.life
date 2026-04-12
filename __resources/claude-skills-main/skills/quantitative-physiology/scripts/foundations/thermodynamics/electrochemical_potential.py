"""
Electrochemical Potential - Unified chemical and electrical driving forces

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation
import numpy as np


def compute_electrochemical_potential(mu_0: float, C: float, z: float, psi: float,
                                     R: float = 8.314, T_body: float = 310.0, F: float = 96485.0) -> float:
    """
    Calculate electrochemical potential.

    Formula: μ̃ = μ° + RT ln(C) + zFψ

    Parameters:
    -----------
    mu_0 : float - Standard chemical potential (J/mol)
    C : float - Concentration (M)
    z : float - Valence (charge number)
    psi : float - Electric potential (V)
    R : float - Gas constant (J/(mol·K))
    T_body : float - Body temperature (K)
    F : float - Faraday constant (C/mol)

    Returns:
    --------
    mu_tilde : float - Electrochemical potential (J/mol)
    """
    return mu_0 + R * T_body * np.log(C) + z * F * psi


# Create and register atomic equation
electrochemical_potential = create_equation(
    id="foundations.thermodynamics.electrochemical_potential",
    name="Electrochemical Potential",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\tilde{\mu} = \mu^\circ + RT \ln(C) + zF\psi",
    simplified="mu_tilde = mu_0 + R*T*ln(C) + z*F*psi",
    description="Unifies electrical and chemical driving forces - equilibrium when Δμ̃ = 0",
    compute_func=compute_electrochemical_potential,
    parameters=[
        Parameter(
            name="mu_0",
            description="Standard chemical potential",
            units="J/mol",
            symbol=r"\mu^\circ",
            physiological_range=(-1e6, 1e6)
        ),
        Parameter(
            name="C",
            description="Concentration",
            units="M",
            symbol="C",
            physiological_range=(1e-6, 1.0)
        ),
        Parameter(
            name="z",
            description="Valence (charge number)",
            units="dimensionless",
            symbol="z",
            physiological_range=(-3.0, 3.0)
        ),
        Parameter(
            name="psi",
            description="Electric potential",
            units="V",
            symbol=r"\psi",
            physiological_range=(-0.2, 0.2)
        ),
        PHYSICAL_CONSTANTS["R"],
        PHYSICAL_CONSTANTS["T_body"],
        PHYSICAL_CONSTANTS["F"]
    ],
    depends_on=["foundations.thermodynamics.gibbs_free_energy"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.5")
)

register_equation(electrochemical_potential)

"""
Gibbs Free Energy - Maximum useful work from a process

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_gibbs_free_energy(H: float, T: float, S: float) -> float:
    """
    Calculate Gibbs free energy.

    Formula: G = H - TS

    Parameters:
    -----------
    H : float - Enthalpy (J/mol)
    T : float - Temperature (K)
    S : float - Entropy (J/(mol·K))

    Returns:
    --------
    G : float - Gibbs free energy (J/mol)
    """
    return H - T * S


def compute_gibbs_change(delta_H: float, T: float, delta_S: float) -> float:
    """
    Calculate change in Gibbs free energy.

    Formula: ΔG = ΔH - TΔS

    Parameters:
    -----------
    delta_H : float - Enthalpy change (J/mol)
    T : float - Temperature (K)
    delta_S : float - Entropy change (J/(mol·K))

    Returns:
    --------
    delta_G : float - Gibbs free energy change (J/mol)
    """
    return delta_H - T * delta_S


# Create and register atomic equation
gibbs_free_energy = create_equation(
    id="foundations.thermodynamics.gibbs_free_energy",
    name="Gibbs Free Energy",
    category=EquationCategory.FOUNDATIONS,
    latex=r"G = H - TS \quad ; \quad \Delta G = \Delta H - T\Delta S",
    simplified="G = H - T*S  ;  delta_G = delta_H - T*delta_S",
    description="Maximum useful work from a process - ΔG < 0 means spontaneous",
    compute_func=compute_gibbs_change,
    parameters=[
        Parameter(
            name="delta_H",
            description="Enthalpy change",
            units="J/mol",
            symbol=r"\Delta H",
            physiological_range=(-1e6, 1e6)
        ),
        Parameter(
            name="T",
            description="Temperature",
            units="K",
            symbol="T",
            default_value=310.0,
            physiological_range=(273.0, 320.0)
        ),
        Parameter(
            name="delta_S",
            description="Entropy change",
            units="J/(mol·K)",
            symbol=r"\Delta S",
            physiological_range=(-1000.0, 1000.0)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.4")
)

register_equation(gibbs_free_energy)

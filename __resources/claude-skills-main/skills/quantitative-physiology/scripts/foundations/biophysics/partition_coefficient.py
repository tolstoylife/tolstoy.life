"""
Partition Coefficient and Distribution Equilibrium

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equation 44)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def partition_coefficient(C_phase1: float, C_phase2: float) -> float:
    """
    Calculate partition coefficient between two phases at equilibrium.

    Formula: K = C₁ / C₂

    The partition coefficient describes how a solute distributes between
    two immiscible phases (e.g., oil/water, membrane/aqueous). Critical for
    understanding drug absorption, membrane permeability, and lipophilicity.

    Parameters:
    -----------
    C_phase1 : float - Concentration in phase 1 (mol/L or other)
    C_phase2 : float - Concentration in phase 2 (same units as C_phase1)

    Returns:
    --------
    K : float - Partition coefficient (dimensionless ratio)
    """
    return C_phase1 / C_phase2


def log_partition_coefficient(C_octanol: float, C_water: float) -> float:
    """
    Calculate log P (octanol-water partition coefficient).

    Formula: log P = log₁₀(C_octanol / C_water)

    Log P is the standard measure of lipophilicity in pharmacology.
    - Log P < 0: Hydrophilic (water-preferring)
    - Log P > 0: Lipophilic (fat-preferring)
    - Optimal drug absorption: log P ≈ 1-3

    Parameters:
    -----------
    C_octanol : float - Concentration in octanol phase
    C_water : float - Concentration in water phase (same units)

    Returns:
    --------
    log_P : float - Logarithm of partition coefficient
    """
    return np.log10(C_octanol / C_water)


def concentration_from_partition(K: float, C_total: float,
                                  V_phase1: float, V_phase2: float) -> tuple:
    """
    Calculate equilibrium concentrations given partition coefficient.

    At equilibrium: K = C₁/C₂ and C₁V₁ + C₂V₂ = C_total × (V₁ + V₂)

    Parameters:
    -----------
    K : float - Partition coefficient (C₁/C₂)
    C_total : float - Total concentration if mixed
    V_phase1 : float - Volume of phase 1
    V_phase2 : float - Volume of phase 2

    Returns:
    --------
    (C1, C2) : tuple - Equilibrium concentrations in each phase
    """
    V_total = V_phase1 + V_phase2
    total_amount = C_total * V_total

    # Solve: C1 = K × C2 and C1×V1 + C2×V2 = total_amount
    # C2 × (K×V1 + V2) = total_amount
    C2 = total_amount / (K * V_phase1 + V_phase2)
    C1 = K * C2

    return (C1, C2)


# Create and register partition coefficient equation
partition_coefficient_eq = create_equation(
    id="foundations.biophysics.partition_coefficient",
    name="Partition Coefficient",
    category=EquationCategory.FOUNDATIONS,
    latex=r"K = \frac{C_1}{C_2}",
    simplified="K = C₁ / C₂",
    description="Distribution ratio of solute between two immiscible phases",
    compute_func=partition_coefficient,
    parameters=[
        Parameter(
            name="C_phase1",
            description="Concentration in phase 1 (e.g., lipid)",
            units="mol/L",
            symbol="C_1",
            physiological_range=(1e-12, 1.0)  # Very wide range
        ),
        Parameter(
            name="C_phase2",
            description="Concentration in phase 2 (e.g., aqueous)",
            units="mol/L",
            symbol="C_2",
            physiological_range=(1e-12, 1.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.3",
        textbook_equation_number="A.44"
    )
)
register_equation(partition_coefficient_eq)

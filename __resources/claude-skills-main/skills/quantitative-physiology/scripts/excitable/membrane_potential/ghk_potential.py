"""
Goldman-Hodgkin-Katz (GHK) Equation

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation
import numpy as np

def ghk_potential(P_K: float, P_Na: float, P_Cl: float,
                  K_out: float, K_in: float,
                  Na_out: float, Na_in: float,
                  Cl_out: float, Cl_in: float,
                  R: float = 8.314, T_body: float = 310.0, F: float = 96485.0) -> float:
    """
    Goldman-Hodgkin-Katz equation for membrane potential with multiple ions.

    Formula: V_m = (RT/F) × ln[(P_K[K⁺]_o + P_Na[Na⁺]_o + P_Cl[Cl⁻]_i) /
                                (P_K[K⁺]_i + P_Na[Na⁺]_i + P_Cl[Cl⁻]_o)]

    This extends the Nernst equation to multiple permeant ion species.

    Parameters:
    -----------
    P_K : float - Potassium permeability (dimensionless relative)
    P_Na : float - Sodium permeability (dimensionless relative)
    P_Cl : float - Chloride permeability (dimensionless relative)
    K_out : float - Extracellular potassium concentration (mM)
    K_in : float - Intracellular potassium concentration (mM)
    Na_out : float - Extracellular sodium concentration (mM)
    Na_in : float - Intracellular sodium concentration (mM)
    Cl_out : float - Extracellular chloride concentration (mM)
    Cl_in : float - Intracellular chloride concentration (mM)
    R : float - Gas constant (J/(mol·K)), default: 8.314
    T_body : float - Body temperature (K), default: 310.0 (37°C)
    F : float - Faraday constant (C/mol), default: 96485.0

    Returns:
    --------
    V_m : float - Membrane potential (V)
    """
    numerator = P_K * K_out + P_Na * Na_out + P_Cl * Cl_in
    denominator = P_K * K_in + P_Na * Na_in + P_Cl * Cl_out

    return (R * T_body / F) * np.log(numerator / denominator)

# Create and register atomic equation
ghk_potential_eq = create_equation(
    id="excitable.membrane_potential.ghk_potential",
    name="Goldman-Hodgkin-Katz Potential",
    category=EquationCategory.EXCITABLE,
    latex=r"V_m = \frac{RT}{F} \ln\left[\frac{P_K[K^+]_o + P_{Na}[Na^+]_o + P_{Cl}[Cl^-]_i}{P_K[K^+]_i + P_{Na}[Na^+]_i + P_{Cl}[Cl^-]_o}\right]",
    simplified="V_m = (RT/F) × ln[(P_K[K⁺]_o + P_Na[Na⁺]_o + P_Cl[Cl⁻]_i) / (P_K[K⁺]_i + P_Na[Na⁺]_i + P_Cl[Cl⁻]_o)]",
    description="Membrane potential accounting for multiple permeant ion species",
    compute_func=ghk_potential,
    parameters=[
        Parameter(
            name="P_K",
            description="Potassium permeability (relative)",
            units="dimensionless",
            symbol="P_K",
            default_value=1.0,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="P_Na",
            description="Sodium permeability (relative)",
            units="dimensionless",
            symbol="P_{Na}",
            default_value=0.04,
            physiological_range=(0.01, 0.5)
        ),
        Parameter(
            name="P_Cl",
            description="Chloride permeability (relative)",
            units="dimensionless",
            symbol="P_{Cl}",
            default_value=0.45,
            physiological_range=(0.1, 1.0)
        ),
        Parameter(
            name="K_out",
            description="Extracellular potassium concentration",
            units="mM",
            symbol="[K^+]_o",
            default_value=5.0,
            physiological_range=(3.5, 5.5)
        ),
        Parameter(
            name="K_in",
            description="Intracellular potassium concentration",
            units="mM",
            symbol="[K^+]_i",
            default_value=140.0,
            physiological_range=(120.0, 155.0)
        ),
        Parameter(
            name="Na_out",
            description="Extracellular sodium concentration",
            units="mM",
            symbol="[Na^+]_o",
            default_value=145.0,
            physiological_range=(135.0, 150.0)
        ),
        Parameter(
            name="Na_in",
            description="Intracellular sodium concentration",
            units="mM",
            symbol="[Na^+]_i",
            default_value=12.0,
            physiological_range=(10.0, 15.0)
        ),
        Parameter(
            name="Cl_out",
            description="Extracellular chloride concentration",
            units="mM",
            symbol="[Cl^-]_o",
            default_value=120.0,
            physiological_range=(100.0, 130.0)
        ),
        Parameter(
            name="Cl_in",
            description="Intracellular chloride concentration",
            units="mM",
            symbol="[Cl^-]_i",
            default_value=4.0,
            physiological_range=(2.0, 10.0)
        ),
        PHYSICAL_CONSTANTS['R'],
        PHYSICAL_CONSTANTS['T_body'],
        PHYSICAL_CONSTANTS['F'],
    ],
    depends_on=["foundations.thermodynamics.nernst_equation"],  # GHK generalizes Nernst
    metadata=EquationMetadata(source_unit=3, source_chapter="3.1")
)
register_equation(ghk_potential_eq)

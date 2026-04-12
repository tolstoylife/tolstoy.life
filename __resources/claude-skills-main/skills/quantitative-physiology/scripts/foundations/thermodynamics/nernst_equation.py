"""
Nernst Equation - Equilibrium potential for ions

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation
import numpy as np


def compute_nernst_potential(z: float, C_out: float, C_in: float,
                             R: float = 8.314, T_body: float = 310.0, F: float = 96485.0) -> float:
    """
    Calculate Nernst equilibrium potential for an ion.

    Formula: E = (RT/zF) ln(C_out/C_in)

    Parameters:
    -----------
    z : float - Ion valence
    C_out : float - Extracellular concentration (M)
    C_in : float - Intracellular concentration (M)
    R : float - Gas constant (J/(mol·K))
    T_body : float - Body temperature (K)
    F : float - Faraday constant (C/mol)

    Returns:
    --------
    E : float - Equilibrium potential (V)
    """
    return (R * T_body) / (z * F) * np.log(C_out / C_in)


def compute_nernst_potential_log10(z: float, C_out: float, C_in: float, T: float = 310.0) -> float:
    """
    Calculate Nernst potential using log10 form (more convenient).

    At 37°C (310 K): E ≈ (61.5 mV/z) log₁₀(C_out/C_in)

    Parameters:
    -----------
    z : float - Ion valence
    C_out : float - Extracellular concentration (M)
    C_in : float - Intracellular concentration (M)
    T : float - Temperature (K)

    Returns:
    --------
    E : float - Equilibrium potential (V)
    """
    # At 310 K: RT/F ≈ 0.0267 V, factor of ln(10) ≈ 2.303
    RT_over_F = 8.314 * T / 96485.0
    return (RT_over_F / z) * np.log10(C_out / C_in) * 2.303


# Create and register atomic equation
nernst_equation = create_equation(
    id="foundations.thermodynamics.nernst_equation",
    name="Nernst Equation",
    category=EquationCategory.FOUNDATIONS,
    latex=r"E = \frac{RT}{zF} \ln\left(\frac{C_{out}}{C_{in}}\right) \approx \frac{61.5\text{ mV}}{z} \log_{10}\left(\frac{C_{out}}{C_{in}}\right)",
    simplified="E = (R*T/z*F) * ln(C_out/C_in)  or  E ≈ (61.5 mV/z) * log10(C_out/C_in)",
    description="Equilibrium potential where electrical gradient balances concentration gradient",
    compute_func=compute_nernst_potential,
    parameters=[
        Parameter(
            name="z",
            description="Ion valence",
            units="dimensionless",
            symbol="z",
            physiological_range=(-3.0, 3.0)
        ),
        Parameter(
            name="C_out",
            description="Extracellular concentration",
            units="M",
            symbol=r"C_{out}",
            physiological_range=(1e-6, 1.0)
        ),
        Parameter(
            name="C_in",
            description="Intracellular concentration",
            units="M",
            symbol=r"C_{in}",
            physiological_range=(1e-6, 1.0)
        ),
        PHYSICAL_CONSTANTS["R"],
        PHYSICAL_CONSTANTS["T_body"],
        PHYSICAL_CONSTANTS["F"]
    ],
    depends_on=["foundations.thermodynamics.electrochemical_potential"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.5")
)

register_equation(nernst_equation)

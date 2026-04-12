"""
Chemiosmotic Coupling - Free energy from proton gradient (Mitchell hypothesis)

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation
import numpy as np

def compute_chemiosmotic_free_energy(delta_psi: float, delta_pH: float,
                                     F: float = 96485.0, R: float = 8.314,
                                     T_body: float = 310.0) -> float:
    """
    Calculate free energy from proton gradient (chemiosmotic coupling).

    Formula: ΔG = F × Δψ + 2.3RT × ΔpH

    This is the Mitchell hypothesis: ATP synthesis driven by proton gradient

    Parameters:
    -----------
    delta_psi : float
        Membrane potential difference (V)
    delta_pH : float
        pH difference across membrane (pH_in - pH_out)
    F : float
        Faraday constant (C/mol), default: 96485
    R : float
        Gas constant (J/(mol·K)), default: 8.314
    T_body : float
        Body temperature (K), default: 310 K (37°C)

    Returns:
    --------
    delta_G : float
        Free energy per mole of H+ (J/mol)

    Notes:
        Mitochondrial gradient: Δψ ≈ 150-180 mV, ΔpH ≈ 0.5-1.0
        Total ΔG ≈ 20-25 kJ/mol H+
    """
    electrical = F * delta_psi
    chemical = 2.3 * R * T_body * delta_pH
    return electrical + chemical


# Create and register atomic equation
chemiosmotic_coupling = create_equation(
    id="membrane.metabolism.chemiosmotic_coupling",
    name="Chemiosmotic Coupling (Mitchell Hypothesis)",
    category=EquationCategory.MEMBRANE,
    latex=r"\Delta G = F \Delta \psi + 2.3RT \Delta pH",
    simplified="delta_G = F*delta_psi + 2.3*R*T*delta_pH",
    description="Free energy available from proton gradient for ATP synthesis in oxidative phosphorylation.",
    compute_func=compute_chemiosmotic_free_energy,
    parameters=[
        Parameter(
            name="delta_psi",
            description="Membrane potential difference",
            units="V",
            symbol=r"\Delta \psi",
            default_value=None,
            physiological_range=(0.1, 0.2)  # 100-200 mV
        ),
        Parameter(
            name="delta_pH",
            description="pH difference (inside - outside)",
            units="dimensionless",
            symbol=r"\Delta pH",
            default_value=None,
            physiological_range=(0.0, 2.0)
        ),
        PHYSICAL_CONSTANTS["F"],
        PHYSICAL_CONSTANTS["R"],
        PHYSICAL_CONSTANTS["T_body"],
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.7")
)

register_equation(chemiosmotic_coupling)

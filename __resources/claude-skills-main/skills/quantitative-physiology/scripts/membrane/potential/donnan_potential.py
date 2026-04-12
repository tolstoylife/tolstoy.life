"""
Gibbs-Donnan Potential - Potential difference due to impermeant charged species

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation
import numpy as np

def compute_donnan_potential(r: float, R: float = 8.314, T_body: float = 310.0, F: float = 96485.0) -> float:
    """
    Calculate Gibbs-Donnan potential.

    Formula: E_Donnan = (RT/F) × ln(r)

    Parameters:
    -----------
    r : float
        Donnan ratio ([K+]_1/[K+]_2)
    R : float
        Gas constant (J/(mol·K)), default: 8.314
    T_body : float
        Body temperature (K), default: 310 K (37°C)
    F : float
        Faraday constant (C/mol), default: 96485

    Returns:
    --------
    E_Donnan : float
        Donnan potential (V)
        Convert to mV by multiplying by 1000

    Consequences:
        - Unequal ion distributions
        - Osmotic imbalance (requires pump compensation)
        - Contributes to resting membrane potential
    """
    return (R * T_body / F) * np.log(r)


# Create and register atomic equation
donnan_potential = create_equation(
    id="membrane.potential.donnan_potential",
    name="Gibbs-Donnan Potential",
    category=EquationCategory.MEMBRANE,
    latex=r"E_{Donnan} = \frac{RT}{F} \ln(r)",
    simplified="E_Donnan = (RT/F) * ln(r)",
    description="Membrane potential arising from unequal ion distribution due to impermeant charged species.",
    compute_func=compute_donnan_potential,
    parameters=[
        Parameter(
            name="r",
            description="Donnan ratio",
            units="dimensionless",
            symbol="r",
            default_value=None,
            physiological_range=(0.1, 10.0)
        ),
        PHYSICAL_CONSTANTS["R"],
        PHYSICAL_CONSTANTS["T_body"],
        PHYSICAL_CONSTANTS["F"],
    ],
    depends_on=["membrane.potential.donnan_ratio"],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.5")
)

register_equation(donnan_potential)

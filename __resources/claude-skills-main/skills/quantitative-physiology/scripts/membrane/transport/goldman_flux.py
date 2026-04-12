"""
Goldman Flux Equation - Electrodiffusion of charged species

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation
import numpy as np

def compute_goldman_flux(P: float, z: int, V_m: float, C_in: float, C_out: float,
                         T_body: float = 310.0, R: float = 8.314, F: float = 96485.0) -> float:
    """
    Calculate ion flux using Goldman flux equation.

    Formula: J_S = P × z × F × V_m / (RT) × (C_in - C_out × e^(zFV_m/RT)) / (1 - e^(zFV_m/RT))

    Parameters:
    -----------
    P : float
        Permeability coefficient (m/s)
    z : int
        Ion valence (charge number)
    V_m : float
        Membrane potential (V)
    C_in : float
        Intracellular concentration (mol/m³)
    C_out : float
        Extracellular concentration (mol/m³)
    T_body : float
        Body temperature (K), default: 310 K (37°C)
    R : float
        Gas constant (J/(mol·K)), default: 8.314
    F : float
        Faraday constant (C/mol), default: 96485

    Returns:
    --------
    J_S : float
        Ion flux (mol/(m²·s))
        Positive flux is into the cell
    """
    u = z * F * V_m / (R * T_body)

    # Handle near-zero potential to avoid division by zero
    if abs(u) < 1e-6:
        return P * (C_in - C_out)

    return P * u * (C_in - C_out * np.exp(u)) / (1 - np.exp(u))


# Create and register atomic equation
goldman_flux = create_equation(
    id="membrane.transport.goldman_flux",
    name="Goldman Flux Equation",
    category=EquationCategory.MEMBRANE,
    latex=r"J_S = P \cdot \frac{zFV_m}{RT} \cdot \frac{C_{in} - C_{out} e^{zFV_m/RT}}{1 - e^{zFV_m/RT}}",
    simplified="J_S = P * (zFV_m/RT) * (C_in - C_out*exp(zFV_m/RT)) / (1 - exp(zFV_m/RT))",
    description="Flux equation for charged species considering both concentration and electrical gradients (electrodiffusion).",
    compute_func=compute_goldman_flux,
    parameters=[
        Parameter(
            name="P",
            description="Permeability coefficient",
            units="m/s",
            symbol="P",
            default_value=None
        ),
        Parameter(
            name="z",
            description="Ion valence",
            units="dimensionless",
            symbol="z",
            default_value=None
        ),
        Parameter(
            name="V_m",
            description="Membrane potential",
            units="V",
            symbol="V_m",
            default_value=None,
            physiological_range=(-0.1, 0.05)  # -100 mV to +50 mV
        ),
        Parameter(
            name="C_in",
            description="Intracellular concentration",
            units="mol/m³",
            symbol="C_{in}",
            default_value=None
        ),
        Parameter(
            name="C_out",
            description="Extracellular concentration",
            units="mol/m³",
            symbol="C_{out}",
            default_value=None
        ),
        PHYSICAL_CONSTANTS["T_body"],
        PHYSICAL_CONSTANTS["R"],
        PHYSICAL_CONSTANTS["F"],
    ],
    depends_on=["membrane.structure.permeability_coefficient"],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.2")
)

register_equation(goldman_flux)

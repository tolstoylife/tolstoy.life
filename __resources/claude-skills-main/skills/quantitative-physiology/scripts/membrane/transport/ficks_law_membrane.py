"""
Fick's Law for Membrane Flux - Simple diffusion across membrane

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_ficks_membrane_flux(P: float, C_out: float, C_in: float) -> float:
    """
    Calculate membrane flux using Fick's law.

    Formula: J_S = P × (C_out - C_in)

    Parameters:
    -----------
    P : float
        Permeability coefficient (m/s or cm/s)
    C_out : float
        Extracellular concentration (mol/m³ or mM)
    C_in : float
        Intracellular concentration (mol/m³ or mM)

    Returns:
    --------
    J_S : float
        Solute flux (mol/(m²·s) or mol/(cm²·s))
        Positive flux is into the cell
    """
    return P * (C_out - C_in)


# Create and register atomic equation
ficks_membrane_flux = create_equation(
    id="membrane.transport.ficks_membrane_flux",
    name="Fick's Law for Membrane Flux",
    category=EquationCategory.MEMBRANE,
    latex=r"J_S = P \cdot (C_{out} - C_{in})",
    simplified="J_S = P * (C_out - C_in)",
    description="Simple diffusion flux across a membrane for uncharged species, proportional to the concentration gradient.",
    compute_func=compute_ficks_membrane_flux,
    parameters=[
        Parameter(
            name="P",
            description="Permeability coefficient",
            units="m/s",
            symbol="P",
            default_value=None
        ),
        Parameter(
            name="C_out",
            description="Extracellular concentration",
            units="mol/m³",
            symbol="C_{out}",
            default_value=None
        ),
        Parameter(
            name="C_in",
            description="Intracellular concentration",
            units="mol/m³",
            symbol="C_{in}",
            default_value=None
        ),
    ],
    depends_on=["membrane.structure.permeability_coefficient"],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.2")
)

register_equation(ficks_membrane_flux)

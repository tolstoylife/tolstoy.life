"""
Osmotic Water Flux - Water flow driven by osmotic and hydrostatic gradients

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_water_flux(L_p: float, delta_P: float, delta_pi: float, sigma: float = 1.0) -> float:
    """
    Calculate osmotic water flow (Starling equation).

    Formula: J_V = L_p × (ΔP - σΔπ)

    Parameters:
    -----------
    L_p : float
        Hydraulic conductivity (m/(s·Pa) or cm/(s·mmHg))
    delta_P : float
        Hydrostatic pressure difference (Pa or mmHg)
    delta_pi : float
        Osmotic pressure difference (Pa or mmHg)
    sigma : float
        Reflection coefficient (0-1), default: 1.0

    Returns:
    --------
    J_V : float
        Volume flux (m/s or cm/s)
        Positive flux follows positive ΔP

    Notes:
        Driving force = hydrostatic - osmotic
        Water flows from low to high osmolarity
    """
    return L_p * (delta_P - sigma * delta_pi)


# Create and register atomic equation
water_flux = create_equation(
    id="membrane.osmosis.water_flux",
    name="Osmotic Water Flux (Starling)",
    category=EquationCategory.MEMBRANE,
    latex=r"J_V = L_p \cdot (\Delta P - \sigma \Delta \pi)",
    simplified="J_V = L_p * (delta_P - sigma * delta_pi)",
    description="Water flow across membrane driven by hydrostatic and osmotic pressure gradients.",
    compute_func=compute_water_flux,
    parameters=[
        Parameter(
            name="L_p",
            description="Hydraulic conductivity",
            units="m/(s·Pa)",
            symbol="L_p",
            default_value=None
        ),
        Parameter(
            name="delta_P",
            description="Hydrostatic pressure difference",
            units="Pa",
            symbol=r"\Delta P",
            default_value=None
        ),
        Parameter(
            name="delta_pi",
            description="Osmotic pressure difference",
            units="Pa",
            symbol=r"\Delta \pi",
            default_value=None
        ),
        Parameter(
            name="sigma",
            description="Reflection coefficient",
            units="dimensionless",
            symbol=r"\sigma",
            default_value=1.0,
            physiological_range=(0.0, 1.0)
        ),
    ],
    depends_on=["membrane.osmosis.osmotic_pressure"],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.4")
)

register_equation(water_flux)

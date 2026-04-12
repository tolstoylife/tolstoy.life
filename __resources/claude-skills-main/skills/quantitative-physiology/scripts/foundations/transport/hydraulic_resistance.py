"""
Hydraulic Resistance - Resistance to fluid flow

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_hydraulic_resistance(eta: float, L: float, r: float) -> float:
    """
    Calculate hydraulic resistance of a cylindrical tube.

    Formula: R = 8ηL/(πr⁴)

    Parameters:
    -----------
    eta : float - Fluid viscosity (Pa·s)
    L : float - Tube length (m)
    r : float - Tube radius (m)

    Returns:
    --------
    R : float - Hydraulic resistance (Pa·s/m³)
    """
    return (8 * eta * L) / (np.pi * r**4)


def compute_flow_from_resistance(delta_P: float, R: float) -> float:
    """
    Calculate flow from pressure difference and resistance.

    Formula: Q_V = ΔP/R (analogous to Ohm's law)

    Parameters:
    -----------
    delta_P : float - Pressure difference (Pa)
    R : float - Hydraulic resistance (Pa·s/m³)

    Returns:
    --------
    Q_V : float - Volume flow rate (m³/s)
    """
    return delta_P / R


# Create and register atomic equation
hydraulic_resistance = create_equation(
    id="foundations.transport.hydraulic_resistance",
    name="Hydraulic Resistance",
    category=EquationCategory.FOUNDATIONS,
    latex=r"R = \frac{8\eta L}{\pi r^4}",
    simplified="R = (8 * eta * L) / (pi * r^4)",
    description="Resistance to fluid flow - analogous to electrical resistance",
    compute_func=compute_hydraulic_resistance,
    parameters=[
        Parameter(
            name="eta",
            description="Fluid viscosity",
            units="Pa·s",
            symbol=r"\eta",
            default_value=3.5e-3,
            physiological_range=(1e-3, 1e-2)
        ),
        Parameter(
            name="L",
            description="Tube length",
            units="m",
            symbol="L",
            physiological_range=(1e-6, 1.0)
        ),
        Parameter(
            name="r",
            description="Tube radius",
            units="m",
            symbol="r",
            physiological_range=(1e-6, 1e-2)
        )
    ],
    depends_on=["foundations.transport.poiseuille_flow"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.1")
)

register_equation(hydraulic_resistance)

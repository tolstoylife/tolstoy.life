"""
Volume Flux - Volume flowing per unit area per unit time

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_volume_flux(Q_V: float, A: float) -> float:
    """
    Calculate volume flux from volume flow rate and area.

    Formula: J_V = Q_V / A

    Parameters:
    -----------
    Q_V : float - Volume flow rate (m³/s)
    A : float - Cross-sectional area (m²)

    Returns:
    --------
    J_V : float - Volume flux (m/s)
    """
    return Q_V / A


# Create and register atomic equation
volume_flux = create_equation(
    id="foundations.transport.volume_flux",
    name="Volume Flux",
    category=EquationCategory.FOUNDATIONS,
    latex=r"J_V = \frac{Q_V}{A}",
    simplified="J_V = Q_V / A",
    description="Volume flowing per unit area per unit time",
    compute_func=compute_volume_flux,
    parameters=[
        Parameter(
            name="Q_V",
            description="Volume flow rate",
            units="m³/s",
            symbol=r"Q_V",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="A",
            description="Cross-sectional area",
            units="m²",
            symbol="A",
            physiological_range=(1e-12, 1e-3)  # from capillary to aorta
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.1")
)

register_equation(volume_flux)

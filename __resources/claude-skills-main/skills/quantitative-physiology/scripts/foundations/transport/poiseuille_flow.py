"""
Poiseuille's Law - Laminar flow through cylindrical tube

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_poiseuille_flow(r: float, eta: float, delta_P: float, L: float) -> float:
    """
    Calculate volume flow rate through cylindrical tube.

    Formula: Q_V = (πr⁴/8η) × (ΔP/L)

    Parameters:
    -----------
    r : float - Tube radius (m)
    eta : float - Fluid viscosity (Pa·s)
    delta_P : float - Pressure difference (Pa)
    L : float - Tube length (m)

    Returns:
    --------
    Q_V : float - Volume flow rate (m³/s)
    """
    return (np.pi * r**4 / (8 * eta)) * (delta_P / L)


# Create and register atomic equation
poiseuille_flow = create_equation(
    id="foundations.transport.poiseuille_flow",
    name="Poiseuille's Law",
    category=EquationCategory.FOUNDATIONS,
    latex=r"Q_V = \frac{\pi r^4}{8\eta} \cdot \frac{\Delta P}{L}",
    simplified="Q_V = (pi * r^4 / (8 * eta)) * (delta_P / L)",
    description="Laminar flow through cylindrical tube - flow proportional to r⁴",
    compute_func=compute_poiseuille_flow,
    parameters=[
        Parameter(
            name="r",
            description="Tube radius",
            units="m",
            symbol="r",
            physiological_range=(1e-6, 1e-2)  # capillary to aorta
        ),
        Parameter(
            name="eta",
            description="Fluid viscosity",
            units="Pa·s",
            symbol=r"\eta",
            default_value=3.5e-3,  # blood viscosity
            physiological_range=(1e-3, 1e-2)
        ),
        Parameter(
            name="delta_P",
            description="Pressure difference",
            units="Pa",
            symbol=r"\Delta P",
            physiological_range=(0.0, 20000.0)  # up to ~150 mmHg
        ),
        Parameter(
            name="L",
            description="Tube length",
            units="m",
            symbol="L",
            physiological_range=(1e-6, 1.0)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.1")
)

register_equation(poiseuille_flow)

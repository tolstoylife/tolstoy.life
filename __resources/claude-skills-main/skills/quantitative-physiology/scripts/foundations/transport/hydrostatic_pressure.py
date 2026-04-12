"""
Hydrostatic Pressure - Pressure at depth in fluid

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_hydrostatic_pressure(rho: float, g: float, h: float) -> float:
    """
    Calculate hydrostatic pressure at depth h in fluid.

    Formula: P = ρgh

    Parameters:
    -----------
    rho : float - Fluid density (kg/m³)
    g : float - Gravitational acceleration (m/s²)
    h : float - Height of fluid column (m)

    Returns:
    --------
    P : float - Pressure (Pa)
    """
    return rho * g * h


# Create and register atomic equation
hydrostatic_pressure = create_equation(
    id="foundations.transport.hydrostatic_pressure",
    name="Hydrostatic Pressure",
    category=EquationCategory.FOUNDATIONS,
    latex=r"P = \rho g h",
    simplified="P = rho * g * h",
    description="Pressure at depth h in fluid column",
    compute_func=compute_hydrostatic_pressure,
    parameters=[
        Parameter(
            name="rho",
            description="Fluid density",
            units="kg/m³",
            symbol=r"\rho",
            default_value=1055.0,  # blood density
            physiological_range=(1000.0, 1100.0)
        ),
        Parameter(
            name="g",
            description="Gravitational acceleration",
            units="m/s²",
            symbol="g",
            default_value=9.8,
            physiological_range=(9.8, 9.8)
        ),
        Parameter(
            name="h",
            description="Height of fluid column",
            units="m",
            symbol="h",
            physiological_range=(0.0, 2.0)  # max ~2m for human height
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.1")
)

register_equation(hydrostatic_pressure)

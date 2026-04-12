"""
Parallel Plate Capacitor - Membrane capacitance model

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_parallel_plate_capacitance(epsilon: float, epsilon_0: float, A: float, d: float) -> float:
    """
    Calculate capacitance of parallel plate capacitor.

    Formula: C = εε₀A/d

    Parameters:
    -----------
    epsilon : float - Relative permittivity
    epsilon_0 : float - Permittivity of free space (C²/(J·m))
    A : float - Plate area (m²)
    d : float - Separation distance (m)

    Returns:
    --------
    C : float - Capacitance (F)
    """
    return epsilon * epsilon_0 * A / d


# Create and register atomic equation
parallel_plate_capacitor = create_equation(
    id="foundations.electrical.parallel_plate_capacitor",
    name="Parallel Plate Capacitor",
    category=EquationCategory.FOUNDATIONS,
    latex=r"C = \frac{\epsilon\epsilon_0 A}{d}",
    simplified="C = (epsilon * epsilon_0 * A) / d",
    description="Membrane as capacitor - typical membrane capacitance ~1 μF/cm²",
    compute_func=compute_parallel_plate_capacitance,
    parameters=[
        Parameter(
            name="epsilon",
            description="Relative permittivity of membrane",
            units="dimensionless",
            symbol=r"\epsilon",
            default_value=3.0,  # lipid bilayer
            physiological_range=(2.0, 5.0)
        ),
        Parameter(
            name="epsilon_0",
            description="Permittivity of free space",
            units="C²/(J·m)",
            symbol=r"\epsilon_0",
            default_value=8.85e-12
        ),
        Parameter(
            name="A",
            description="Membrane area",
            units="m²",
            symbol="A",
            physiological_range=(1e-12, 1e-6)
        ),
        Parameter(
            name="d",
            description="Membrane thickness",
            units="m",
            symbol="d",
            default_value=4e-9,  # ~4 nm
            physiological_range=(3e-9, 10e-9)
        )
    ],
    depends_on=["foundations.electrical.capacitance"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.2")
)

register_equation(parallel_plate_capacitor)

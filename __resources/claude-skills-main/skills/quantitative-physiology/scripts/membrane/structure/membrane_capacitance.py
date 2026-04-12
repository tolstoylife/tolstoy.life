"""
Membrane Capacitance - Capacitance of lipid bilayer membrane

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation
import numpy as np

def compute_membrane_capacitance(epsilon_m: float = 2.5, delta: float = 4e-9) -> float:
    """
    Calculate membrane capacitance per unit area.

    Formula: C_m = ε_m × ε_0 / δ

    Parameters:
    -----------
    epsilon_m : float
        Membrane dielectric constant (dimensionless), typical: 2-3
    delta : float
        Membrane thickness (m), typical: 4-5 nm

    Returns:
    --------
    C_m : float
        Membrane capacitance (F/m²)
        Typical value: ~0.01 F/m² = 1 μF/cm²
    """
    epsilon_0 = 8.85e-12  # Permittivity of free space (F/m)
    return epsilon_m * epsilon_0 / delta


# Create and register atomic equation
membrane_capacitance = create_equation(
    id="membrane.structure.membrane_capacitance",
    name="Membrane Capacitance",
    category=EquationCategory.MEMBRANE,
    latex=r"C_m = \frac{\varepsilon_m \varepsilon_0}{\delta}",
    simplified="C_m = (epsilon_m * epsilon_0) / delta",
    description="Capacitance of lipid bilayer membrane per unit area, arising from charge separation across the thin insulating membrane.",
    compute_func=compute_membrane_capacitance,
    parameters=[
        Parameter(
            name="epsilon_m",
            description="Membrane dielectric constant",
            units="dimensionless",
            symbol=r"\varepsilon_m",
            default_value=2.5,
            physiological_range=(2.0, 3.0)
        ),
        Parameter(
            name="delta",
            description="Membrane thickness (hydrophobic core)",
            units="m",
            symbol=r"\delta",
            default_value=4e-9,
            physiological_range=(3e-9, 5e-9)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.1")
)

register_equation(membrane_capacitance)

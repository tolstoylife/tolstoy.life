"""Poiseuille's law for hydraulic resistance."""

import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_poiseuille_resistance(eta: float, L: float, r: float) -> float:
    """
    Calculate hydraulic resistance using Poiseuille's law.

    Parameters
    ----------
    eta : float
        Blood viscosity (mPa·s)
    L : float
        Vessel length (cm)
    r : float
        Vessel radius (cm)

    Returns
    -------
    float
        Hydraulic resistance (mmHg·s/mL)
    """
    # Convert units: eta in mPa·s = 0.001 Pa·s, need mmHg·s/mL
    # 1 Pa = 0.0075 mmHg, 1 mL = 1 cm³
    # R = 8ηL/(πr⁴)
    return (8 * eta * L) / (np.pi * r**4) * 0.0075


poiseuille_resistance = create_equation(
    id="cardiovascular.hemodynamics.poiseuille_resistance",
    name="Poiseuille's Law for Resistance",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"R = \frac{8\eta L}{\pi r^4}",
    simplified="R = 8ηL / (πr⁴)",
    description="Hydraulic resistance for laminar flow in cylindrical vessels",
    compute_func=compute_poiseuille_resistance,
    parameters=[
        Parameter(
            name="eta",
            description="Blood viscosity",
            units="mPa·s",
            symbol=r"\eta",
            physiological_range=(3.0, 5.0)
        ),
        Parameter(
            name="L",
            description="Vessel length",
            units="cm",
            symbol="L",
            physiological_range=(0.1, 100.0)
        ),
        Parameter(
            name="r",
            description="Vessel radius",
            units="cm",
            symbol="r",
            physiological_range=(0.001, 1.5)
        )
    ],
    depends_on=["cardiovascular.blood.blood_viscosity"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(poiseuille_resistance)

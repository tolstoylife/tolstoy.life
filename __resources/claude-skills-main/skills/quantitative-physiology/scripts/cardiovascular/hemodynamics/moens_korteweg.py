"""Moens-Korteweg equation for pulse wave velocity."""

import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_moens_korteweg(E: float, h: float, d: float, rho: float = 1060.0) -> float:
    """
    Calculate pulse wave velocity using Moens-Korteweg equation.

    Parameters
    ----------
    E : float
        Elastic modulus of vessel wall (Pa)
    h : float
        Wall thickness (m)
    d : float
        Vessel diameter (m)
    rho : float, optional
        Blood density (kg/m³, default: 1060)

    Returns
    -------
    float
        Pulse wave velocity (m/s)
    """
    return np.sqrt((E * h) / (rho * d))


moens_korteweg = create_equation(
    id="cardiovascular.hemodynamics.moens_korteweg_pwv",
    name="Moens-Korteweg Pulse Wave Velocity",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{PWV} = \sqrt{\frac{E h}{\rho d}}",
    simplified="PWV = √(E·h / ρ·d)",
    description="Pulse wave velocity from vessel wall elastic properties",
    compute_func=compute_moens_korteweg,
    parameters=[
        Parameter(
            name="E",
            description="Elastic modulus of vessel wall",
            units="Pa",
            symbol="E",
            physiological_range=(1e5, 1e6)
        ),
        Parameter(
            name="h",
            description="Wall thickness",
            units="m",
            symbol="h",
            physiological_range=(0.001, 0.005)
        ),
        Parameter(
            name="d",
            description="Vessel diameter",
            units="m",
            symbol="d",
            physiological_range=(0.02, 0.03)
        ),
        Parameter(
            name="rho",
            description="Blood density",
            units="kg/m³",
            symbol=r"\rho",
            default_value=1060.0,
            physiological_range=(1050.0, 1070.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(moens_korteweg)

"""Womersley number for pulsatile flow."""

import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_womersley_number(r: float, omega: float, rho: float, eta: float) -> float:
    """
    Calculate Womersley number for pulsatile flow.

    Parameters
    ----------
    r : float
        Vessel radius (m)
    omega : float
        Angular frequency (rad/s) = 2π × heart rate (Hz)
    rho : float
        Blood density (kg/m³)
    eta : float
        Dynamic viscosity (Pa·s)

    Returns
    -------
    float
        Womersley number (dimensionless)
    """
    return r * np.sqrt((omega * rho) / eta)


womersley_number = create_equation(
    id="cardiovascular.hemodynamics.womersley_number",
    name="Womersley Number",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\alpha = r \sqrt{\frac{\omega \rho}{\eta}}",
    simplified="α = r × √(ω·ρ / η)",
    description="Dimensionless parameter characterizing pulsatile flow velocity profile",
    compute_func=compute_womersley_number,
    parameters=[
        Parameter(
            name="r",
            description="Vessel radius",
            units="m",
            symbol="r",
            physiological_range=(0.0005, 0.015)
        ),
        Parameter(
            name="omega",
            description="Angular frequency",
            units="rad/s",
            symbol=r"\omega",
            physiological_range=(4.0, 10.0)
        ),
        Parameter(
            name="rho",
            description="Blood density",
            units="kg/m³",
            symbol=r"\rho",
            physiological_range=(1050.0, 1070.0)
        ),
        Parameter(
            name="eta",
            description="Dynamic viscosity",
            units="Pa·s",
            symbol=r"\eta",
            physiological_range=(0.003, 0.005)
        )
    ],
    depends_on=["cardiovascular.blood.blood_viscosity"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(womersley_number)

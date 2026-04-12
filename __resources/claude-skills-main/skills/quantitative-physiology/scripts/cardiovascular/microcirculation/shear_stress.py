"""Wall shear stress in vessels."""

import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_shear_stress(eta: float, Q: float, r: float) -> float:
    """
    Calculate wall shear stress in a cylindrical vessel.

    Parameters
    ----------
    eta : float
        Blood viscosity (Pa·s)
    Q : float
        Flow rate (m³/s)
    r : float
        Vessel radius (m)

    Returns
    -------
    float
        Wall shear stress (Pa)
    """
    return (4 * eta * Q) / (np.pi * r**3)


shear_stress = create_equation(
    id="cardiovascular.microcirculation.wall_shear_stress",
    name="Wall Shear Stress",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\tau = \frac{4\eta Q}{\pi r^3}",
    simplified="τ = 4ηQ / (πr³)",
    description="Frictional force per unit area exerted by flowing blood on vessel wall",
    compute_func=compute_shear_stress,
    parameters=[
        Parameter(
            name="eta",
            description="Blood viscosity",
            units="Pa·s",
            symbol=r"\eta",
            physiological_range=(0.003, 0.005)
        ),
        Parameter(
            name="Q",
            description="Flow rate",
            units="m³/s",
            symbol="Q",
            physiological_range=(1e-7, 1e-4)
        ),
        Parameter(
            name="r",
            description="Vessel radius",
            units="m",
            symbol="r",
            physiological_range=(0.0001, 0.015)
        )
    ],
    depends_on=["cardiovascular.blood.blood_viscosity"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.6"
    )
)

register_equation(shear_stress)

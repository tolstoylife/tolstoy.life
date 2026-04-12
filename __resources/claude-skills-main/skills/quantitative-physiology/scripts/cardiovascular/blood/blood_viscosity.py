"""Blood viscosity as function of hematocrit."""

import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_blood_viscosity(Hct: float, eta_plasma: float = 1.2) -> float:
    """
    Calculate blood viscosity based on hematocrit.

    Parameters
    ----------
    Hct : float
        Hematocrit (0-1)
    eta_plasma : float, optional
        Plasma viscosity in mPa·s (default: 1.2)

    Returns
    -------
    float
        Blood viscosity (mPa·s)
    """
    k = 2.5
    return eta_plasma * np.exp(k * Hct)


blood_viscosity = create_equation(
    id="cardiovascular.blood.blood_viscosity",
    name="Blood Viscosity",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\eta_{\text{blood}} = \eta_{\text{plasma}} \times e^{k \times \text{Hct}}",
    simplified="η_blood = η_plasma × exp(2.5 × Hct)",
    description="Blood viscosity increases exponentially with hematocrit",
    compute_func=compute_blood_viscosity,
    parameters=[
        Parameter(
            name="Hct",
            description="Hematocrit",
            units="dimensionless",
            symbol=r"\text{Hct}",
            physiological_range=(0.36, 0.54)
        ),
        Parameter(
            name="eta_plasma",
            description="Plasma viscosity",
            units="mPa·s",
            symbol=r"\eta_{\text{plasma}}",
            default_value=1.2,
            physiological_range=(1.1, 1.3)
        )
    ],
    depends_on=["cardiovascular.blood.hematocrit"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.1"
    )
)

register_equation(blood_viscosity)

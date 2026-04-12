"""End-diastolic pressure-volume relationship (EDPVR)."""

import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_edpvr(EDV: float, A: float, k: float) -> float:
    """
    Calculate end-diastolic pressure from EDPVR.

    Parameters
    ----------
    EDV : float
        End-diastolic volume (mL)
    A : float
        Scaling constant (mmHg)
    k : float
        Stiffness constant (1/mL)

    Returns
    -------
    float
        End-diastolic pressure (mmHg)
    """
    return A * (np.exp(k * EDV) - 1)


edpvr = create_equation(
    id="cardiovascular.cardiac.edpvr",
    name="End-Diastolic Pressure-Volume Relationship",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{EDP} = A \times (e^{k \times \text{EDV}} - 1)",
    simplified="EDP = A × (exp(k × EDV) - 1)",
    description="Exponential EDPVR reflecting chamber stiffness",
    compute_func=compute_edpvr,
    parameters=[
        Parameter(
            name="EDV",
            description="End-diastolic volume",
            units="mL",
            symbol="EDV",
            physiological_range=(80.0, 180.0)
        ),
        Parameter(
            name="A",
            description="Scaling constant",
            units="mmHg",
            symbol="A",
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="k",
            description="Stiffness constant",
            units="1/mL",
            symbol="k",
            physiological_range=(0.01, 0.05)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.3"
    )
)

register_equation(edpvr)

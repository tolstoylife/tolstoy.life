"""Hematocrit definition equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_hematocrit(V_RBC: float, V_blood: float) -> float:
    """
    Calculate hematocrit as volume fraction of red blood cells.

    Parameters
    ----------
    V_RBC : float
        Volume of red blood cells (mL)
    V_blood : float
        Total blood volume (mL)

    Returns
    -------
    float
        Hematocrit (0-1)
    """
    return V_RBC / V_blood


hematocrit = create_equation(
    id="cardiovascular.blood.hematocrit",
    name="Hematocrit",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{Hct} = \frac{V_{\text{RBC}}}{V_{\text{blood}}}",
    simplified="Hct = V_RBC / V_blood",
    description="Volume fraction of red blood cells in whole blood",
    compute_func=compute_hematocrit,
    parameters=[
        Parameter(
            name="V_RBC",
            description="Volume of red blood cells",
            units="mL",
            symbol="V_{RBC}",
            physiological_range=(1500, 3000)
        ),
        Parameter(
            name="V_blood",
            description="Total blood volume",
            units="mL",
            symbol="V_{blood}",
            physiological_range=(4000, 6000)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.1"
    )
)

register_equation(hematocrit)

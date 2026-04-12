"""End-systolic pressure-volume relationship (ESPVR)."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_espvr(ESV: float, E_es: float, V_0: float) -> float:
    """
    Calculate end-systolic pressure from ESPVR.

    Parameters
    ----------
    ESV : float
        End-systolic volume (mL)
    E_es : float
        End-systolic elastance (mmHg/mL)
    V_0 : float
        Volume axis intercept (mL)

    Returns
    -------
    float
        End-systolic pressure (mmHg)
    """
    return E_es * (ESV - V_0)


espvr = create_equation(
    id="cardiovascular.cardiac.espvr",
    name="End-Systolic Pressure-Volume Relationship",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{ESP} = E_{es} \times (\text{ESV} - V_0)",
    simplified="ESP = E_es × (ESV - V_0)",
    description="Linear ESPVR defining contractility; E_es is index of contractility",
    compute_func=compute_espvr,
    parameters=[
        Parameter(
            name="ESV",
            description="End-systolic volume",
            units="mL",
            symbol="ESV",
            physiological_range=(30.0, 80.0)
        ),
        Parameter(
            name="E_es",
            description="End-systolic elastance",
            units="mmHg/mL",
            symbol="E_{es}",
            physiological_range=(1.5, 4.0)
        ),
        Parameter(
            name="V_0",
            description="Volume axis intercept",
            units="mL",
            symbol="V_0",
            physiological_range=(5.0, 20.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.3"
    )
)

register_equation(espvr)

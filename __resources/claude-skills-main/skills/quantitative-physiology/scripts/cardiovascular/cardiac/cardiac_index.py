"""Cardiac index equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_cardiac_index(CO: float, BSA: float) -> float:
    """
    Calculate cardiac index normalized to body surface area.

    Parameters
    ----------
    CO : float
        Cardiac output (L/min)
    BSA : float
        Body surface area (m²)

    Returns
    -------
    float
        Cardiac index (L/min/m²)
    """
    return CO / BSA


cardiac_index = create_equation(
    id="cardiovascular.cardiac.cardiac_index",
    name="Cardiac Index",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{CI} = \frac{\text{CO}}{\text{BSA}}",
    simplified="CI = CO / BSA",
    description="Cardiac output normalized to body surface area",
    compute_func=compute_cardiac_index,
    parameters=[
        Parameter(
            name="CO",
            description="Cardiac output",
            units="L/min",
            symbol="CO",
            physiological_range=(4.0, 8.0)
        ),
        Parameter(
            name="BSA",
            description="Body surface area",
            units="m²",
            symbol="BSA",
            physiological_range=(1.5, 2.5)
        )
    ],
    depends_on=["cardiovascular.cardiac.cardiac_output", "cardiovascular.cardiac.body_surface_area_dubois"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.3"
    )
)

register_equation(cardiac_index)

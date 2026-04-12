"""Cardiac output equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_cardiac_output(HR: float, SV: float) -> float:
    """
    Calculate cardiac output from heart rate and stroke volume.

    Parameters
    ----------
    HR : float
        Heart rate (bpm)
    SV : float
        Stroke volume (mL)

    Returns
    -------
    float
        Cardiac output (L/min)
    """
    return (HR * SV) / 1000.0


cardiac_output = create_equation(
    id="cardiovascular.cardiac.cardiac_output",
    name="Cardiac Output",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{CO} = \text{HR} \times \text{SV}",
    simplified="CO = HR × SV",
    description="Cardiac output as product of heart rate and stroke volume",
    compute_func=compute_cardiac_output,
    parameters=[
        Parameter(
            name="HR",
            description="Heart rate",
            units="bpm",
            symbol="HR",
            physiological_range=(60.0, 100.0)
        ),
        Parameter(
            name="SV",
            description="Stroke volume",
            units="mL",
            symbol="SV",
            physiological_range=(60.0, 100.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.3"
    )
)

register_equation(cardiac_output)

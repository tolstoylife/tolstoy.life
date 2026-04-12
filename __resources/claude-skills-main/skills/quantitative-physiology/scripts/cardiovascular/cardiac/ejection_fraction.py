"""Ejection fraction equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_ejection_fraction(EDV: float, ESV: float) -> float:
    """
    Calculate ejection fraction from end-diastolic and end-systolic volumes.

    Parameters
    ----------
    EDV : float
        End-diastolic volume (mL)
    ESV : float
        End-systolic volume (mL)

    Returns
    -------
    float
        Ejection fraction (0-1)
    """
    return (EDV - ESV) / EDV


ejection_fraction = create_equation(
    id="cardiovascular.cardiac.ejection_fraction",
    name="Ejection Fraction",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{EF} = \frac{\text{EDV} - \text{ESV}}{\text{EDV}} = \frac{\text{SV}}{\text{EDV}}",
    simplified="EF = (EDV - ESV) / EDV",
    description="Fraction of end-diastolic volume ejected per heartbeat",
    compute_func=compute_ejection_fraction,
    parameters=[
        Parameter(
            name="EDV",
            description="End-diastolic volume",
            units="mL",
            symbol="EDV",
            physiological_range=(100.0, 150.0)
        ),
        Parameter(
            name="ESV",
            description="End-systolic volume",
            units="mL",
            symbol="ESV",
            physiological_range=(40.0, 60.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.3"
    )
)

register_equation(ejection_fraction)

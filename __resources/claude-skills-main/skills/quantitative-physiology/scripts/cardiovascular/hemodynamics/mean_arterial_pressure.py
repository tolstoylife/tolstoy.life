"""Mean arterial pressure equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_mean_arterial_pressure(SBP: float, DBP: float) -> float:
    """
    Calculate mean arterial pressure from systolic and diastolic pressures.

    Parameters
    ----------
    SBP : float
        Systolic blood pressure (mmHg)
    DBP : float
        Diastolic blood pressure (mmHg)

    Returns
    -------
    float
        Mean arterial pressure (mmHg)
    """
    return DBP + (SBP - DBP) / 3.0


mean_arterial_pressure = create_equation(
    id="cardiovascular.hemodynamics.mean_arterial_pressure",
    name="Mean Arterial Pressure",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{MAP} = \text{DBP} + \frac{1}{3}(\text{SBP} - \text{DBP})",
    simplified="MAP = DBP + (SBP - DBP) / 3",
    description="Time-weighted average arterial pressure during cardiac cycle",
    compute_func=compute_mean_arterial_pressure,
    parameters=[
        Parameter(
            name="SBP",
            description="Systolic blood pressure",
            units="mmHg",
            symbol="SBP",
            physiological_range=(90.0, 140.0)
        ),
        Parameter(
            name="DBP",
            description="Diastolic blood pressure",
            units="mmHg",
            symbol="DBP",
            physiological_range=(60.0, 90.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(mean_arterial_pressure)

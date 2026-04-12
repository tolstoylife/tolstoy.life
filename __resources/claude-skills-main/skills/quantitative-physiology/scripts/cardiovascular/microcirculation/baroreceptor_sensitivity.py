"""Baroreceptor sensitivity equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_baroreceptor_sensitivity(dRR: float, dSBP: float) -> float:
    """
    Calculate baroreceptor sensitivity.

    Parameters
    ----------
    dRR : float
        Change in RR interval (ms)
    dSBP : float
        Change in systolic blood pressure (mmHg)

    Returns
    -------
    float
        Baroreceptor sensitivity (ms/mmHg)
    """
    return dRR / dSBP


baroreceptor_sensitivity = create_equation(
    id="cardiovascular.microcirculation.baroreceptor_sensitivity",
    name="Baroreceptor Sensitivity",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{BRS} = \frac{\Delta RR}{\Delta SBP}",
    simplified="BRS = ΔRR / ΔSBP",
    description="Measure of baroreceptor reflex responsiveness",
    compute_func=compute_baroreceptor_sensitivity,
    parameters=[
        Parameter(
            name="dRR",
            description="Change in RR interval",
            units="ms",
            symbol=r"\Delta RR",
            physiological_range=(1.0, 100.0)
        ),
        Parameter(
            name="dSBP",
            description="Change in systolic blood pressure",
            units="mmHg",
            symbol=r"\Delta SBP",
            physiological_range=(1.0, 50.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.6"
    )
)

register_equation(baroreceptor_sensitivity)

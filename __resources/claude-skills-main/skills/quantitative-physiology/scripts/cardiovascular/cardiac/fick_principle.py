"""Fick principle for cardiac output measurement."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_cardiac_output_fick(VO2: float, C_aO2: float, C_vO2: float) -> float:
    """
    Calculate cardiac output using the Fick principle.

    Parameters
    ----------
    VO2 : float
        Oxygen consumption (mL O2/min)
    C_aO2 : float
        Arterial oxygen content (mL O2/dL)
    C_vO2 : float
        Mixed venous oxygen content (mL O2/dL)

    Returns
    -------
    float
        Cardiac output (L/min)
    """
    # Convert to L/min (C_aO2 and C_vO2 in dL units)
    return VO2 / ((C_aO2 - C_vO2) * 10.0)


cardiac_output_fick = create_equation(
    id="cardiovascular.cardiac.cardiac_output_fick",
    name="Cardiac Output (Fick Principle)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{CO} = \frac{\dot{V}O_2}{C_{aO_2} - C_{vO_2}}",
    simplified="CO = VO2 / (C_aO2 - C_vO2)",
    description="Cardiac output calculated from oxygen consumption and arteriovenous oxygen content difference",
    compute_func=compute_cardiac_output_fick,
    parameters=[
        Parameter(
            name="VO2",
            description="Oxygen consumption",
            units="mL O2/min",
            symbol=r"\dot{V}O_2",
            physiological_range=(200.0, 400.0)
        ),
        Parameter(
            name="C_aO2",
            description="Arterial oxygen content",
            units="mL O2/dL",
            symbol="C_{aO_2}",
            physiological_range=(18.0, 22.0)
        ),
        Parameter(
            name="C_vO2",
            description="Mixed venous oxygen content",
            units="mL O2/dL",
            symbol="C_{vO_2}",
            physiological_range=(14.0, 16.0)
        )
    ],
    depends_on=["respiratory.oxygen_transport.oxygen_content"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.3"
    )
)

register_equation(cardiac_output_fick)

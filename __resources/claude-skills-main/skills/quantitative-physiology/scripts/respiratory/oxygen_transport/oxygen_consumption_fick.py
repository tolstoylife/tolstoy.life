"""Oxygen Consumption (Fick Principle) equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_oxygen_consumption_fick(Q: float, CaO2: float, CvO2: float) -> float:
    """
    Calculate oxygen consumption using Fick principle.

    V̇O2 = Q̇ × (C_aO2 - C_vO2) × 10

    Parameters
    ----------
    Q : float
        Cardiac output (L/min)
    CaO2 : float
        Arterial O2 content (mL O2/dL)
    CvO2 : float
        Venous O2 content (mL O2/dL)

    Returns
    -------
    float
        Oxygen consumption (mL O2/min)
    """
    return Q * (CaO2 - CvO2) * 10.0


# Create equation
oxygen_consumption_fick = create_equation(
    id="respiratory.oxygen_transport.oxygen_consumption_fick",
    name="Oxygen Consumption (Fick Principle)",
    category=EquationCategory.RESPIRATORY,
    latex=r"\dot{V}O_2 = \dot{Q} \times (C_{aO2} - C_{vO2}) \times 10",
    simplified="V̇O2 = Q̇ × (C_aO2 - C_vO2) × 10",
    description="Tissue oxygen consumption based on arteriovenous O2 difference",
    compute_func=compute_oxygen_consumption_fick,
    parameters=[
        Parameter(
            name="Q",
            description="Cardiac output",
            units="L/min",
            symbol=r"\dot{Q}",
            default_value=5.0,
            physiological_range=(3.0, 25.0)
        ),
        Parameter(
            name="CaO2",
            description="Arterial O2 content",
            units="mL O2/dL",
            symbol="C_{aO2}",
            default_value=20.0,
            physiological_range=(10.0, 23.0)
        ),
        Parameter(
            name="CvO2",
            description="Venous O2 content",
            units="mL O2/dL",
            symbol="C_{vO2}",
            default_value=15.0,
            physiological_range=(8.0, 18.0)
        )
    ],
    depends_on=["respiratory.oxygen_transport.oxygen_content"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.5"
    )
)

# Register in global index
register_equation(oxygen_consumption_fick)

"""Minute Ventilation equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_minute_ventilation(VT: float, f: float) -> float:
    """
    Calculate total minute ventilation.

    V_E = VT × f

    Parameters
    ----------
    VT : float
        Tidal volume (mL)
    f : float
        Respiratory frequency (breaths/min)

    Returns
    -------
    float
        Minute ventilation (mL/min)
    """
    return VT * f


# Create equation
minute_ventilation = create_equation(
    id="respiratory.volumes.minute_ventilation",
    name="Minute Ventilation",
    category=EquationCategory.RESPIRATORY,
    latex=r"\dot{V}_E = V_T \times f",
    simplified="V_E = VT × f",
    description="Total volume of air breathed per minute",
    compute_func=compute_minute_ventilation,
    parameters=[
        Parameter(
            name="VT",
            description="Tidal volume",
            units="mL",
            symbol="V_T",
            default_value=500.0,
            physiological_range=(400.0, 700.0)
        ),
        Parameter(
            name="f",
            description="Respiratory frequency",
            units="breaths/min",
            symbol="f",
            default_value=12.0,
            physiological_range=(10.0, 20.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.1"
    )
)

# Register in global index
register_equation(minute_ventilation)

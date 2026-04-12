"""Vital Capacity (VC) equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_vital_capacity(VT: float, IRV: float, ERV: float) -> float:
    """
    Calculate vital capacity.

    VC = VT + IRV + ERV

    Parameters
    ----------
    VT : float
        Tidal volume (mL)
    IRV : float
        Inspiratory reserve volume (mL)
    ERV : float
        Expiratory reserve volume (mL)

    Returns
    -------
    float
        Vital capacity (mL)
    """
    return VT + IRV + ERV


# Create equation
vital_capacity = create_equation(
    id="respiratory.volumes.vital_capacity",
    name="Vital Capacity",
    category=EquationCategory.RESPIRATORY,
    latex=r"VC = V_T + IRV + ERV",
    simplified="VC = VT + IRV + ERV",
    description="Vital capacity is the maximum volume that can be exhaled after maximum inhalation",
    compute_func=compute_vital_capacity,
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
            name="IRV",
            description="Inspiratory reserve volume",
            units="mL",
            symbol="IRV",
            default_value=3000.0,
            physiological_range=(2000.0, 3500.0)
        ),
        Parameter(
            name="ERV",
            description="Expiratory reserve volume",
            units="mL",
            symbol="ERV",
            default_value=1100.0,
            physiological_range=(800.0, 1500.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.1"
    )
)

# Register in global index
register_equation(vital_capacity)

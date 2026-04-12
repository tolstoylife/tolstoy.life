"""Inspiratory Capacity (IC) equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_inspiratory_capacity(VT: float, IRV: float) -> float:
    """
    Calculate inspiratory capacity.

    IC = VT + IRV

    Parameters
    ----------
    VT : float
        Tidal volume (mL)
    IRV : float
        Inspiratory reserve volume (mL)

    Returns
    -------
    float
        Inspiratory capacity (mL)
    """
    return VT + IRV


# Create equation
inspiratory_capacity = create_equation(
    id="respiratory.volumes.inspiratory_capacity",
    name="Inspiratory Capacity",
    category=EquationCategory.RESPIRATORY,
    latex=r"IC = V_T + IRV",
    simplified="IC = VT + IRV",
    description="Inspiratory capacity is the maximum volume that can be inhaled from resting level",
    compute_func=compute_inspiratory_capacity,
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
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.1"
    )
)

# Register in global index
register_equation(inspiratory_capacity)

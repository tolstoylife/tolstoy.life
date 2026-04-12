"""Total Lung Capacity (TLC) equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_total_lung_capacity(VT: float, IRV: float, ERV: float, RV: float) -> float:
    """
    Calculate total lung capacity.

    TLC = VT + IRV + ERV + RV

    Parameters
    ----------
    VT : float
        Tidal volume (mL)
    IRV : float
        Inspiratory reserve volume (mL)
    ERV : float
        Expiratory reserve volume (mL)
    RV : float
        Residual volume (mL)

    Returns
    -------
    float
        Total lung capacity (mL)
    """
    return VT + IRV + ERV + RV


# Create equation
total_lung_capacity = create_equation(
    id="respiratory.volumes.total_lung_capacity",
    name="Total Lung Capacity",
    category=EquationCategory.RESPIRATORY,
    latex=r"TLC = V_T + IRV + ERV + RV",
    simplified="TLC = VT + IRV + ERV + RV",
    description="Total lung capacity is the sum of all lung volumes",
    compute_func=compute_total_lung_capacity,
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
        ),
        Parameter(
            name="RV",
            description="Residual volume",
            units="mL",
            symbol="RV",
            default_value=1200.0,
            physiological_range=(1000.0, 1500.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.1"
    )
)

# Register in global index
register_equation(total_lung_capacity)

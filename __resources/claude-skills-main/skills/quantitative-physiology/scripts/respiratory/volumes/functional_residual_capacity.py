"""Functional Residual Capacity (FRC) equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_functional_residual_capacity(ERV: float, RV: float) -> float:
    """
    Calculate functional residual capacity.

    FRC = ERV + RV

    Parameters
    ----------
    ERV : float
        Expiratory reserve volume (mL)
    RV : float
        Residual volume (mL)

    Returns
    -------
    float
        Functional residual capacity (mL)
    """
    return ERV + RV


# Create equation
functional_residual_capacity = create_equation(
    id="respiratory.volumes.functional_residual_capacity",
    name="Functional Residual Capacity",
    category=EquationCategory.RESPIRATORY,
    latex=r"FRC = ERV + RV",
    simplified="FRC = ERV + RV",
    description="Functional residual capacity is the volume remaining in lungs after normal expiration",
    compute_func=compute_functional_residual_capacity,
    parameters=[
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
register_equation(functional_residual_capacity)

"""Pressure-Flow Relationship equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_pressure_flow(delta_P: float, R: float) -> float:
    """
    Calculate airflow from pressure gradient and resistance.

    V̇ = ΔP/R

    Parameters
    ----------
    delta_P : float
        Pressure gradient (cmH2O)
    R : float
        Airway resistance (cmH2O/(L/s))

    Returns
    -------
    float
        Flow rate (L/s)
    """
    return delta_P / R


# Create equation
pressure_flow = create_equation(
    id="respiratory.mechanics.pressure_flow",
    name="Pressure-Flow Relationship",
    category=EquationCategory.RESPIRATORY,
    latex=r"\dot{V} = \frac{\Delta P}{R}",
    simplified="V̇ = ΔP/R",
    description="Airflow driven by pressure gradient and limited by resistance",
    compute_func=compute_pressure_flow,
    parameters=[
        Parameter(
            name="delta_P",
            description="Pressure gradient",
            units="cmH2O",
            symbol=r"\Delta P",
            physiological_range=(-20.0, 20.0)
        ),
        Parameter(
            name="R",
            description="Airway resistance",
            units="cmH2O/(L/s)",
            symbol="R",
            default_value=1.5,
            physiological_range=(0.5, 5.0)
        )
    ],
    depends_on=["respiratory.mechanics.airway_resistance"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(pressure_flow)

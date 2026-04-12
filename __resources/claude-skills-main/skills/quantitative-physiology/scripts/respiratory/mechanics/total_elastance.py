"""Total Respiratory System Elastance equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_total_elastance(E_L: float, E_CW: float) -> float:
    """
    Calculate total respiratory system elastance (series addition).

    E_RS = E_L + E_CW

    Parameters
    ----------
    E_L : float
        Lung elastance (cmH2O/L)
    E_CW : float
        Chest wall elastance (cmH2O/L)

    Returns
    -------
    float
        Total respiratory system elastance (cmH2O/L)
    """
    return E_L + E_CW


# Create equation
total_elastance = create_equation(
    id="respiratory.mechanics.total_elastance",
    name="Total Respiratory System Elastance",
    category=EquationCategory.RESPIRATORY,
    latex=r"E_{RS} = E_L + E_{CW}",
    simplified="E_RS = E_L + E_CW",
    description="Combined elastance of lung and chest wall in series",
    compute_func=compute_total_elastance,
    parameters=[
        Parameter(
            name="E_L",
            description="Lung elastance",
            units="cmH2O/L",
            symbol="E_L",
            default_value=5.0,
            physiological_range=(3.0, 10.0)
        ),
        Parameter(
            name="E_CW",
            description="Chest wall elastance",
            units="cmH2O/L",
            symbol="E_{CW}",
            default_value=5.0,
            physiological_range=(3.0, 10.0)
        )
    ],
    depends_on=["respiratory.mechanics.elastance"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(total_elastance)

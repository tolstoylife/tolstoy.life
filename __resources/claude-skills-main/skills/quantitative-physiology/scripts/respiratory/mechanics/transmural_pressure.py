"""Transmural Pressure equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_transmural_pressure(P_alv: float, P_pl: float) -> float:
    """
    Calculate transmural (transpulmonary) pressure.

    P_TM = P_alv - P_pl

    Parameters
    ----------
    P_alv : float
        Alveolar pressure (cmH2O)
    P_pl : float
        Pleural pressure (cmH2O)

    Returns
    -------
    float
        Transmural pressure (cmH2O)
    """
    return P_alv - P_pl


# Create equation
transmural_pressure = create_equation(
    id="respiratory.mechanics.transmural_pressure",
    name="Transmural Pressure",
    category=EquationCategory.RESPIRATORY,
    latex=r"P_{TM} = P_{alv} - P_{pl}",
    simplified="P_TM = P_alv - P_pl",
    description="Pressure difference across lung wall driving lung expansion",
    compute_func=compute_transmural_pressure,
    parameters=[
        Parameter(
            name="P_alv",
            description="Alveolar pressure",
            units="cmH2O",
            symbol="P_{alv}",
            default_value=0.0,
            physiological_range=(-10.0, 10.0)
        ),
        Parameter(
            name="P_pl",
            description="Pleural pressure",
            units="cmH2O",
            symbol="P_{pl}",
            default_value=-5.0,
            physiological_range=(-10.0, 0.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(transmural_pressure)

"""Salivary flow rate equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_salivary_flow(stimulation: float, basal: float = 0.1, max_flow: float = 4.0) -> float:
    """
    Calculate salivary flow rate based on stimulation level.

    Parameters
    ----------
    stimulation : float
        Stimulation level (0-1 scale)
    basal : float
        Basal flow rate (mL/min), default 0.1 mL/min
    max_flow : float
        Maximum stimulated flow rate (mL/min), default 4 mL/min

    Returns
    -------
    float
        Salivary flow rate (mL/min)
    """
    return basal + (max_flow - basal) * stimulation


salivary_flow = create_equation(
    id="gastrointestinal.secretion.salivary_flow",
    name="Salivary Flow Rate",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"Q_{\text{saliva}} = Q_{\text{basal}} + (Q_{\text{max}} - Q_{\text{basal}}) \times S",
    simplified="Q_saliva = Q_basal + (Q_max - Q_basal) × S",
    description="Salivary flow rate as function of stimulation (daily volume ~1-1.5 L/day)",
    compute_func=compute_salivary_flow,
    parameters=[
        Parameter(
            name="stimulation",
            description="Stimulation level",
            units="dimensionless",
            symbol="S",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="basal",
            description="Basal flow rate",
            units="mL/min",
            symbol=r"Q_{\text{basal}}",
            default_value=0.1,
            physiological_range=(0.05, 0.2)
        ),
        Parameter(
            name="max_flow",
            description="Maximum stimulated flow rate",
            units="mL/min",
            symbol=r"Q_{\text{max}}",
            default_value=4.0,
            physiological_range=(3.0, 5.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.2"
    )
)

register_equation(salivary_flow)

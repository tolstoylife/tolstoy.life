"""Bile acid synthesis and pool dynamics."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_bile_acid_synthesis_rate(fecal_loss: float) -> float:
    """
    Calculate bile acid synthesis rate at steady state.

    At steady state: synthesis = fecal loss

    Parameters
    ----------
    fecal_loss : float
        Fecal bile acid loss (g/day)

    Returns
    -------
    float
        Bile acid synthesis rate (g/day)
    """
    return fecal_loss


bile_acid_synthesis = create_equation(
    id="gastrointestinal.secretion.bile_acid_synthesis",
    name="Bile Acid Synthesis Rate",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{Synthesis} = \text{Fecal loss}",
    simplified="Synthesis = Fecal loss",
    description="At steady state, bile acid synthesis equals fecal loss (~0.3-0.6 g/day). Pool size ~2-4 g, cycles 6-10×/day",
    compute_func=compute_bile_acid_synthesis_rate,
    parameters=[
        Parameter(
            name="fecal_loss",
            description="Fecal bile acid loss",
            units="g/day",
            symbol=r"\text{Fecal loss}",
            default_value=0.45,
            physiological_range=(0.3, 0.6)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.2"
    )
)

register_equation(bile_acid_synthesis)

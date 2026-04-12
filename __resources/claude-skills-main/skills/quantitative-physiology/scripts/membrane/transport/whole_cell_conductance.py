"""
Whole-Cell Conductance - Total conductance from population of channels

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_whole_cell_conductance(N: float, P_open: float, gamma: float) -> float:
    """
    Calculate whole-cell conductance from channel population.

    Formula: G = N × P_open × γ

    Parameters:
    -----------
    N : float
        Number of channels in membrane
    P_open : float
        Open probability (0-1)
    gamma : float
        Single channel conductance (pS)

    Returns:
    --------
    G : float
        Total membrane conductance (pS or nS)
    """
    return N * P_open * gamma


# Create and register atomic equation
whole_cell_conductance = create_equation(
    id="membrane.transport.whole_cell_conductance",
    name="Whole-Cell Conductance",
    category=EquationCategory.MEMBRANE,
    latex=r"G = N \cdot P_{open} \cdot \gamma",
    simplified="G = N * P_open * gamma",
    description="Total membrane conductance for a population of ion channels with given open probability.",
    compute_func=compute_whole_cell_conductance,
    parameters=[
        Parameter(
            name="N",
            description="Number of channels",
            units="dimensionless",
            symbol="N",
            default_value=None,
            physiological_range=(1.0, 1e9)
        ),
        Parameter(
            name="P_open",
            description="Open probability",
            units="dimensionless",
            symbol="P_{open}",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="gamma",
            description="Single channel conductance",
            units="pS",
            symbol=r"\gamma",
            default_value=None,
            physiological_range=(1.0, 300.0)
        ),
    ],
    depends_on=["membrane.transport.single_channel_conductance"],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.2")
)

register_equation(whole_cell_conductance)

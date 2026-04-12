"""
Quantal Variance - Variance in synaptic response amplitude

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_quantal_variance(n: int, p: float, q: float) -> float:
    """
    Calculate variance in synaptic response using binomial statistics.

    Formula: Variance = n × p × (1-p) × q²

    Parameters:
    -----------
    n : int
        Number of release sites
    p : float
        Probability of release per site (0-1)
    q : float
        Quantal size (amplitude of single vesicle response, mV or pA)

    Returns:
    --------
    variance : float
        Variance in synaptic response amplitude (mV² or pA²)

    Notes:
    ------
    Used in variance-mean analysis to estimate n and p:
    Mean = n × p × q
    Variance = n × p × (1-p) × q²
    Therefore: p = 1 - (Variance/Mean)/q
    """
    return n * p * (1 - p) * q**2


# Create and register atomic equation
quantal_variance = create_equation(
    id="nervous.synaptic.quantal_variance",
    name="Quantal Variance",
    category=EquationCategory.NERVOUS,
    latex=r"\text{Variance} = n \times p \times (1-p) \times q^2",
    simplified="Variance = n × p × (1-p) × q²",
    description="Variance in synaptic response amplitude based on binomial statistics of vesicle release. Used with mean quantal content for variance-mean analysis.",
    compute_func=compute_quantal_variance,
    parameters=[
        Parameter(
            name="n",
            description="Number of release sites",
            units="dimensionless",
            symbol="n",
            default_value=None,
            physiological_range=(1.0, 1000.0)
        ),
        Parameter(
            name="p",
            description="Probability of release per site",
            units="dimensionless",
            symbol="p",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="q",
            description="Quantal size (single vesicle response)",
            units="mV or pA",
            symbol="q",
            default_value=None,
            physiological_range=(0.001, 10.0)
        ),
    ],
    depends_on=["nervous.synaptic.quantal_content"],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(quantal_variance)

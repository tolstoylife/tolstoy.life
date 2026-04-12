"""
Quantal Content - Mean number of vesicles released per action potential

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_quantal_content(n: int, p: float) -> float:
    """
    Calculate mean quantal content (average vesicles released).

    Formula: m = n × p

    Parameters:
    -----------
    n : int
        Number of release sites (readily releasable pool size)
    p : float
        Probability of release per site (0-1)

    Returns:
    --------
    m : float
        Mean quantal content (average vesicles released)

    Notes:
    ------
    Typical values:
    - Neuromuscular junction: m ~ 20-200
    - Central synapses: m ~ 0.1-5
    - p ranges from 0.1 to 0.9 depending on synapse type
    """
    return n * p


# Create and register atomic equation
quantal_content = create_equation(
    id="nervous.synaptic.quantal_content",
    name="Quantal Content",
    category=EquationCategory.NERVOUS,
    latex=r"m = n \times p",
    simplified="m = n × p",
    description="Mean number of vesicles (quanta) released per action potential, determined by the number of release sites and release probability.",
    compute_func=compute_quantal_content,
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
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(quantal_content)

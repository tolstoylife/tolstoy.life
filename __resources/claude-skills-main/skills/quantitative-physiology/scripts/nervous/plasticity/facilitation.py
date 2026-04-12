"""
Short-Term Facilitation - Enhancement of release probability

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_facilitation(P_n: float, F: float) -> float:
    """
    Calculate facilitated release probability after spike.

    Formula: P_n+1 = P_n + F × (1 - P_n)

    Parameters:
    -----------
    P_n : float
        Current release probability (0-1)
    F : float
        Facilitation increment (0-1)

    Returns:
    --------
    P_next : float
        Release probability after next spike (0-1)

    Notes:
    ------
    Facilitation due to residual calcium accumulation.
    Each spike adds increment F × (1-P), approaching P=1.
    Time constant τ_fac ≈ 50-500 ms.
    Prominent at synapses with low initial P.
    """
    return P_n + F * (1 - P_n)


# Create and register atomic equation
facilitation = create_equation(
    id="nervous.plasticity.facilitation",
    name="Short-Term Facilitation",
    category=EquationCategory.NERVOUS,
    latex=r"P_{n+1} = P_n + F \times (1 - P_n)",
    simplified="P_n+1 = P_n + F × (1 - P_n)",
    description="Short-term facilitation of release probability due to residual calcium. Each spike increases P by F×(1-P), enhancing subsequent release.",
    compute_func=compute_facilitation,
    parameters=[
        Parameter(
            name="P_n",
            description="Current release probability",
            units="dimensionless",
            symbol="P_n",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="F",
            description="Facilitation increment",
            units="dimensionless",
            symbol="F",
            default_value=None,
            physiological_range=(0.0, 0.5)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.6")
)

register_equation(facilitation)

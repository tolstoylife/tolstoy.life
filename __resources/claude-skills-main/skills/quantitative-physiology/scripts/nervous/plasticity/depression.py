"""
Short-Term Depression - Depletion of readily releasable pool

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_depression(R_n: float, u: float, tau_rec: float, dt: float) -> float:
    """
    Calculate available resources after depression and recovery.

    Formula: R_n+1 = R_n × (1 - u) + (1 - R_n) / τ_rec × dt

    Parameters:
    -----------
    R_n : float
        Current fraction of available resources (0-1)
    u : float
        Utilization factor (fraction released per spike)
    tau_rec : float
        Recovery time constant (ms)
    dt : float
        Time step (ms)

    Returns:
    --------
    R_next : float
        Available resources after update (0-1)

    Notes:
    ------
    Depression from vesicle depletion.
    Each spike releases fraction u, reducing R by u×R.
    Recovery with time constant τ_rec ≈ 100-800 ms.
    Prominent at high-release probability synapses.
    """
    depletion = R_n * (1 - u)
    recovery = (1 - R_n) / tau_rec * dt
    return depletion + recovery


# Create and register atomic equation
depression = create_equation(
    id="nervous.plasticity.depression",
    name="Short-Term Depression",
    category=EquationCategory.NERVOUS,
    latex=r"R_{n+1} = R_n \times (1 - u) + \frac{1 - R_n}{\tau_{rec}} \times dt",
    simplified="R_n+1 = R_n × (1 - u) + (1 - R_n)/τ_rec × dt",
    description="Short-term depression from vesicle pool depletion. Each spike releases fraction u, with recovery time constant τ_rec.",
    compute_func=compute_depression,
    parameters=[
        Parameter(
            name="R_n",
            description="Available resources",
            units="dimensionless",
            symbol="R_n",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="u",
            description="Utilization factor",
            units="dimensionless",
            symbol="u",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="tau_rec",
            description="Recovery time constant",
            units="ms",
            symbol=r"\tau_{rec}",
            default_value=None,
            physiological_range=(10.0, 2000.0)
        ),
        Parameter(
            name="dt",
            description="Time step",
            units="ms",
            symbol="dt",
            default_value=1.0,
            physiological_range=(0.01, 100.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.6")
)

register_equation(depression)

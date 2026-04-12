"""
Rate-Force Relation - Force output as function of firing rate

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_rate_force_relation(f: float, F_0: float, k: float) -> float:
    """
    Calculate muscle force as function of motor neuron firing rate.

    Formula: F(f) = F_0 × [1 - e^(-k×f)]

    Parameters:
    -----------
    f : float
        Firing frequency (Hz)
    F_0 : float
        Maximum force (N or arbitrary units)
    k : float
        Rate constant (1/Hz)

    Returns:
    --------
    F : float
        Force output (N or arbitrary units)

    Notes:
    ------
    Describes force summation with increasing firing rate.
    At low frequencies: twitches sum linearly
    At high frequencies: approaches tetanic fusion
    k depends on twitch kinetics (faster for fast fibers)
    """
    return F_0 * (1 - np.exp(-k * f))


# Create and register atomic equation
rate_force_relation = create_equation(
    id="nervous.motor.rate_force_relation",
    name="Rate-Force Relation",
    category=EquationCategory.NERVOUS,
    latex=r"F(f) = F_0 \times [1 - e^{-k \times f}]",
    simplified="F(f) = F_0 × [1 - e^(-k×f)]",
    description="Relationship between motor neuron firing rate and muscle force output. Force increases exponentially toward maximum as rate increases.",
    compute_func=compute_rate_force_relation,
    parameters=[
        Parameter(
            name="f",
            description="Firing frequency",
            units="Hz",
            symbol="f",
            default_value=None,
            physiological_range=(0.0, 200.0)
        ),
        Parameter(
            name="F_0",
            description="Maximum force",
            units="N",
            symbol="F_0",
            default_value=None,
            physiological_range=(0.001, 1000.0)
        ),
        Parameter(
            name="k",
            description="Rate constant",
            units="1/Hz",
            symbol="k",
            default_value=None,
            physiological_range=(0.01, 1.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.4")
)

register_equation(rate_force_relation)

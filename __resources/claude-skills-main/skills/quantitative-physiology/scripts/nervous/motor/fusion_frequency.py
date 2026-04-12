"""
Fusion Frequency - Frequency for complete tetanic fusion

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_fusion_frequency(tau_twitch: float) -> float:
    """
    Calculate fusion frequency from twitch time constant.

    Formula: f_fusion ≈ 3/τ_twitch

    Parameters:
    -----------
    tau_twitch : float
        Twitch duration (time constant, s)

    Returns:
    --------
    f_fusion : float
        Fusion frequency (Hz)

    Notes:
    ------
    Frequency at which individual twitches fuse into smooth tetanus.
    Slow fibers: τ ≈ 0.1 s → f_fusion ≈ 20-30 Hz
    Fast fibers: τ ≈ 0.02 s → f_fusion ≈ 50-100 Hz
    Rule of thumb: fusion occurs when interpulse interval < τ/3
    """
    return 3.0 / tau_twitch


# Create and register atomic equation
fusion_frequency = create_equation(
    id="nervous.motor.fusion_frequency",
    name="Fusion Frequency",
    category=EquationCategory.NERVOUS,
    latex=r"f_{fusion} \approx \frac{3}{\tau_{twitch}}",
    simplified="f_fusion ≈ 3/τ_twitch",
    description="Frequency at which muscle twitches fuse into smooth tetanic contraction. Depends inversely on twitch duration. Fast fibers have higher fusion frequencies.",
    compute_func=compute_fusion_frequency,
    parameters=[
        Parameter(
            name="tau_twitch",
            description="Twitch time constant",
            units="s",
            symbol=r"\tau_{twitch}",
            default_value=None,
            physiological_range=(0.01, 0.2)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.4")
)

register_equation(fusion_frequency)

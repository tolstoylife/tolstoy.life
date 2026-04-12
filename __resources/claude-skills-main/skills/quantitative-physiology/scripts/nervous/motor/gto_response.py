"""
Golgi Tendon Organ Response - Ib afferent firing rate

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_gto_response(force: float, k_gto: float) -> float:
    """
    Calculate Golgi tendon organ Ib afferent firing rate.

    Formula: f_Ib = k_GTO × Force

    Parameters:
    -----------
    force : float
        Muscle force (N)
    k_gto : float
        GTO sensitivity (Hz/N)

    Returns:
    --------
    f_Ib : float
        Ib afferent firing rate (Hz)

    Notes:
    ------
    Golgi tendon organs are in series with muscle fibers.
    Encode muscle force/tension, not length.
    Provide feedback for force control.
    Mediate autogenic inhibition (protect against excessive force).
    More sensitive to active than passive tension.
    """
    return k_gto * force


# Create and register atomic equation
gto_response = create_equation(
    id="nervous.motor.gto_response",
    name="Golgi Tendon Organ Response",
    category=EquationCategory.NERVOUS,
    latex=r"f_{Ib} = k_{GTO} \times Force",
    simplified="f_Ib = k_GTO × Force",
    description="Golgi tendon organ Ib afferent response encoding muscle force. Located in series with muscle, provides force feedback for motor control and autogenic inhibition.",
    compute_func=compute_gto_response,
    parameters=[
        Parameter(
            name="force",
            description="Muscle force",
            units="N",
            symbol="Force",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="k_gto",
            description="GTO sensitivity",
            units="Hz/N",
            symbol="k_{GTO}",
            default_value=None,
            physiological_range=(0.1, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.4")
)

register_equation(gto_response)

"""
Muscle Spindle Response - Ia afferent firing rate

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_spindle_response(L: float, L_0: float, dL_dt: float,
                              k_static: float, k_dynamic: float) -> float:
    """
    Calculate muscle spindle Ia afferent firing rate.

    Formula: f_Ia = k_static × (L - L₀) + k_dynamic × (dL/dt)

    Parameters:
    -----------
    L : float
        Current muscle length (mm)
    L_0 : float
        Reference length (mm)
    dL_dt : float
        Rate of length change (mm/s)
    k_static : float
        Static sensitivity (Hz/mm)
    k_dynamic : float
        Dynamic sensitivity (Hz/(mm/s))

    Returns:
    --------
    f_Ia : float
        Ia afferent firing rate (Hz)

    Notes:
    ------
    Muscle spindle Ia afferents encode both position and velocity.
    Static component: sustained response to stretch
    Dynamic component: transient response to velocity
    Used for proprioception and stretch reflex
    """
    return k_static * (L - L_0) + k_dynamic * dL_dt


# Create and register atomic equation
spindle_response = create_equation(
    id="nervous.motor.spindle_response",
    name="Muscle Spindle Response",
    category=EquationCategory.NERVOUS,
    latex=r"f_{Ia} = k_{static} \times (L - L_0) + k_{dynamic} \times \frac{dL}{dt}",
    simplified="f_Ia = k_static × (L - L₀) + k_dynamic × (dL/dt)",
    description="Muscle spindle Ia afferent response encoding both muscle length (position) and velocity of stretch. Provides proprioceptive feedback for motor control.",
    compute_func=compute_spindle_response,
    parameters=[
        Parameter(
            name="L",
            description="Current muscle length",
            units="mm",
            symbol="L",
            default_value=None,
            physiological_range=(0.0, 500.0)
        ),
        Parameter(
            name="L_0",
            description="Reference length",
            units="mm",
            symbol="L_0",
            default_value=None,
            physiological_range=(0.0, 500.0)
        ),
        Parameter(
            name="dL_dt",
            description="Rate of length change",
            units="mm/s",
            symbol=r"\frac{dL}{dt}",
            default_value=None,
            physiological_range=(-1000.0, 1000.0)
        ),
        Parameter(
            name="k_static",
            description="Static sensitivity",
            units="Hz/mm",
            symbol="k_{static}",
            default_value=None,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="k_dynamic",
            description="Dynamic sensitivity",
            units="Hz/(mm/s)",
            symbol="k_{dynamic}",
            default_value=None,
            physiological_range=(0.01, 1.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.4")
)

register_equation(spindle_response)

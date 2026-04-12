"""
Stretch Reflex Gain - Overall gain of stretch reflex loop

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_reflex_gain(k_spindle: float, g_synapse: float, k_motor: float) -> float:
    """
    Calculate stretch reflex gain (change in force per unit length change).

    Formula: G = ΔForce / ΔLength = k_spindle × g_synapse × k_motor

    Parameters:
    -----------
    k_spindle : float
        Spindle sensitivity (Hz/mm)
    g_synapse : float
        Synaptic gain (motor neuron spikes per Ia spike)
    k_motor : float
        Motor neuron to force conversion (N/Hz)

    Returns:
    --------
    G : float
        Reflex gain (N/mm)

    Notes:
    ------
    Determines stiffness added by stretch reflex.
    High gain: muscle resists length changes (postural control)
    Low gain: muscle more compliant (fine motor control)
    Modulated by descending control and gamma motor neurons
    """
    return k_spindle * g_synapse * k_motor


# Create and register atomic equation
reflex_gain = create_equation(
    id="nervous.motor.reflex_gain",
    name="Stretch Reflex Gain",
    category=EquationCategory.NERVOUS,
    latex=r"G = \frac{\Delta Force}{\Delta Length} = k_{spindle} \times g_{synapse} \times k_{motor}",
    simplified="G = ΔForce/ΔLength = k_spindle × g_synapse × k_motor",
    description="Overall gain of stretch reflex loop, determining how much force is generated in response to length perturbation. Product of spindle, synaptic, and motor gains.",
    compute_func=compute_reflex_gain,
    parameters=[
        Parameter(
            name="k_spindle",
            description="Spindle sensitivity",
            units="Hz/mm",
            symbol="k_{spindle}",
            default_value=None,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="g_synapse",
            description="Synaptic gain",
            units="dimensionless",
            symbol="g_{synapse}",
            default_value=None,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="k_motor",
            description="Motor to force conversion",
            units="N/Hz",
            symbol="k_{motor}",
            default_value=None,
            physiological_range=(0.001, 1.0)
        ),
    ],
    depends_on=["nervous.motor.spindle_response"],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.4")
)

register_equation(reflex_gain)

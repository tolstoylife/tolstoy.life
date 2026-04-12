"""
Double Exponential Synaptic Conductance - More realistic synaptic time course

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_double_exponential(t: float, g_max: float, tau_rise: float, tau_decay: float) -> float:
    """
    Calculate synaptic conductance using double exponential.

    Formula: g(t) = g_max × [e^(-t/τ_decay) - e^(-t/τ_rise)]

    Parameters:
    -----------
    t : float
        Time after synapse activation (ms)
    g_max : float
        Peak conductance (nS)
    tau_rise : float
        Rise time constant (ms)
    tau_decay : float
        Decay time constant (ms)

    Returns:
    --------
    g : float
        Conductance at time t (nS)

    Notes:
    ------
    More realistic than alpha function, with separate rise and decay phases.
    Requires τ_decay > τ_rise for proper shape.
    AMPA: τ_rise ≈ 0.2-1 ms, τ_decay ≈ 2-5 ms
    NMDA: τ_rise ≈ 5-10 ms, τ_decay ≈ 50-200 ms
    """
    if t < 0:
        return 0.0
    return g_max * (np.exp(-t / tau_decay) - np.exp(-t / tau_rise))


# Create and register atomic equation
double_exponential = create_equation(
    id="nervous.synaptic.double_exponential_synapse",
    name="Double Exponential Synaptic Conductance",
    category=EquationCategory.NERVOUS,
    latex=r"g(t) = g_{max} \times [e^{-t/\tau_{decay}} - e^{-t/\tau_{rise}}]",
    simplified="g(t) = g_max × [e^(-t/τ_decay) - e^(-t/τ_rise)]",
    description="Double exponential function for synaptic conductance with separate rise and decay time constants, providing more realistic waveform than alpha function.",
    compute_func=compute_double_exponential,
    parameters=[
        Parameter(
            name="t",
            description="Time after synapse activation",
            units="ms",
            symbol="t",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="g_max",
            description="Peak conductance",
            units="nS",
            symbol="g_{max}",
            default_value=None,
            physiological_range=(0.001, 100.0)
        ),
        Parameter(
            name="tau_rise",
            description="Rise time constant",
            units="ms",
            symbol=r"\tau_{rise}",
            default_value=None,
            physiological_range=(0.1, 20.0)
        ),
        Parameter(
            name="tau_decay",
            description="Decay time constant",
            units="ms",
            symbol=r"\tau_{decay}",
            default_value=None,
            physiological_range=(1.0, 500.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(double_exponential)

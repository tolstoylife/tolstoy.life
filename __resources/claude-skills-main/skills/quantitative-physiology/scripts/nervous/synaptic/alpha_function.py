"""
Alpha Function Synaptic Conductance - Time course of synaptic conductance

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_alpha_function(t: float, g_max: float, tau: float) -> float:
    """
    Calculate synaptic conductance using alpha function time course.

    Formula: g(t) = g_max × (t/τ) × e^(1-t/τ)

    Parameters:
    -----------
    t : float
        Time after synapse activation (ms)
    g_max : float
        Peak conductance (nS)
    tau : float
        Time constant (ms)

    Returns:
    --------
    g : float
        Conductance at time t (nS)

    Notes:
    ------
    The alpha function peaks at t = τ with amplitude g_max.
    Provides simple, realistic synaptic waveform with single time constant.
    For AMPA: τ ≈ 2-5 ms
    For NMDA: τ ≈ 50-200 ms
    For GABA_A: τ ≈ 10-30 ms
    """
    if t < 0:
        return 0.0
    return g_max * (t / tau) * np.exp(1 - t / tau)


# Create and register atomic equation
alpha_function = create_equation(
    id="nervous.synaptic.alpha_function",
    name="Alpha Function Synaptic Conductance",
    category=EquationCategory.NERVOUS,
    latex=r"g(t) = g_{max} \times \frac{t}{\tau} \times e^{1-t/\tau}",
    simplified="g(t) = g_max × (t/τ) × e^(1-t/τ)",
    description="Alpha function describing the time course of synaptic conductance. Peaks at t=τ and provides a simple, realistic synaptic waveform.",
    compute_func=compute_alpha_function,
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
            name="tau",
            description="Time constant",
            units="ms",
            symbol=r"\tau",
            default_value=None,
            physiological_range=(0.1, 500.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(alpha_function)

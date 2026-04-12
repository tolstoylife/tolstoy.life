"""
EPSP Amplitude - Peak excitatory postsynaptic potential amplitude

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_epsp_amplitude(g_syn: float, R_in: float, V_m: float, E_rev: float) -> float:
    """
    Calculate EPSP amplitude from synaptic conductance and input resistance.

    Formula: EPSP = g_syn × R_in × (E_rev - V_m)

    Parameters:
    -----------
    g_syn : float
        Peak synaptic conductance (nS)
    R_in : float
        Input resistance of postsynaptic cell (MΩ)
    V_m : float
        Resting membrane potential (mV)
    E_rev : float
        Reversal potential for excitatory synapse (mV)

    Returns:
    --------
    EPSP : float
        EPSP amplitude (mV)

    Notes:
    ------
    Derived from I_syn = g_syn × (V_m - E_rev) and V = I × R
    For excitatory synapses: E_rev > V_m, so EPSP is positive (depolarizing)
    Typical EPSP amplitudes: 0.1-10 mV
    """
    # Convert units: nS × MΩ = 10^-3 (dimensionless factor)
    return g_syn * R_in * (E_rev - V_m) * 1e-3


# Create and register atomic equation
epsp_amplitude = create_equation(
    id="nervous.synaptic.epsp_amplitude",
    name="EPSP Amplitude",
    category=EquationCategory.NERVOUS,
    latex=r"EPSP = g_{syn} \times R_{in} \times (E_{rev} - V_m)",
    simplified="EPSP = g_syn × R_in × (E_rev - V_m)",
    description="Peak amplitude of excitatory postsynaptic potential, determined by synaptic conductance, input resistance, and driving force.",
    compute_func=compute_epsp_amplitude,
    parameters=[
        Parameter(
            name="g_syn",
            description="Peak synaptic conductance",
            units="nS",
            symbol="g_{syn}",
            default_value=None,
            physiological_range=(0.001, 100.0)
        ),
        Parameter(
            name="R_in",
            description="Input resistance",
            units="MΩ",
            symbol="R_{in}",
            default_value=None,
            physiological_range=(1.0, 1000.0)
        ),
        Parameter(
            name="V_m",
            description="Resting membrane potential",
            units="mV",
            symbol="V_m",
            default_value=-70.0,
            physiological_range=(-90.0, -50.0)
        ),
        Parameter(
            name="E_rev",
            description="Reversal potential",
            units="mV",
            symbol="E_{rev}",
            default_value=0.0,
            physiological_range=(-20.0, 20.0)
        ),
    ],
    depends_on=["nervous.synaptic.synaptic_current"],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(epsp_amplitude)

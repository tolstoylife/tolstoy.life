"""
Synaptic Current - Current flowing through synaptic receptors

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_synaptic_current(g_syn: float, V_m: float, E_rev: float) -> float:
    """
    Calculate synaptic current through postsynaptic receptors.

    Formula: I_syn = g_syn × (V_m - E_rev)

    Parameters:
    -----------
    g_syn : float
        Synaptic conductance (nS)
    V_m : float
        Membrane potential (mV)
    E_rev : float
        Reversal potential for the synapse (mV)

    Returns:
    --------
    I_syn : float
        Synaptic current (pA)

    Notes:
    ------
    Typical reversal potentials:
    - Glutamate (AMPA): E_rev ≈ 0 mV
    - GABA_A: E_rev ≈ -70 to -80 mV (E_Cl)
    - Nicotinic ACh: E_rev ≈ 0 mV
    """
    return g_syn * (V_m - E_rev)


# Create and register atomic equation
synaptic_current = create_equation(
    id="nervous.synaptic.synaptic_current",
    name="Synaptic Current",
    category=EquationCategory.NERVOUS,
    latex=r"I_{syn} = g_{syn} \times (V_m - E_{rev})",
    simplified="I_syn = g_syn × (V_m - E_rev)",
    description="Current flowing through open synaptic receptors, determined by synaptic conductance and driving force (difference between membrane potential and reversal potential).",
    compute_func=compute_synaptic_current,
    parameters=[
        Parameter(
            name="g_syn",
            description="Synaptic conductance",
            units="nS",
            symbol="g_{syn}",
            default_value=None,
            physiological_range=(0.001, 100.0)
        ),
        Parameter(
            name="V_m",
            description="Membrane potential",
            units="mV",
            symbol="V_m",
            default_value=None,
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="E_rev",
            description="Reversal potential",
            units="mV",
            symbol="E_{rev}",
            default_value=None,
            physiological_range=(-100.0, 100.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(synaptic_current)

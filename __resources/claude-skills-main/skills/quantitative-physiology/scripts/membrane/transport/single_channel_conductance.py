"""
Single Channel Conductance - Conductance of an individual ion channel

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_single_channel_conductance(i: float, V_m: float, E_ion: float) -> float:
    """
    Calculate single channel conductance.

    Formula: γ = i / (V_m - E_ion)

    Parameters:
    -----------
    i : float
        Single channel current (pA)
    V_m : float
        Membrane potential (mV)
    E_ion : float
        Reversal (equilibrium) potential for the ion (mV)

    Returns:
    --------
    gamma : float
        Single channel conductance (pS = pA/mV)

    Typical values: 1-300 pS depending on channel type
    """
    return i / (V_m - E_ion)


# Create and register atomic equation
single_channel_conductance = create_equation(
    id="membrane.transport.single_channel_conductance",
    name="Single Channel Conductance",
    category=EquationCategory.MEMBRANE,
    latex=r"\gamma = \frac{i}{V_m - E_{ion}}",
    simplified="gamma = i / (V_m - E_ion)",
    description="Conductance of an individual ion channel, relating single-channel current to driving force.",
    compute_func=compute_single_channel_conductance,
    parameters=[
        Parameter(
            name="i",
            description="Single channel current",
            units="pA",
            symbol="i",
            default_value=None,
            physiological_range=(-100.0, 100.0)
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
            name="E_ion",
            description="Ion reversal potential",
            units="mV",
            symbol="E_{ion}",
            default_value=None,
            physiological_range=(-100.0, 100.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.2")
)

register_equation(single_channel_conductance)

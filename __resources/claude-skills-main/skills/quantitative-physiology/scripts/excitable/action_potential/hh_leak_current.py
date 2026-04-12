"""
Hodgkin-Huxley Leak Current

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def hh_leak_current(V: float, g_L_bar: float = 0.3, E_L: float = -54.4) -> float:
    """
    Leak current in the Hodgkin-Huxley model.

    Formula: I_L = g̅_L × (V - E_L)

    The leak current represents non-specific conductances.

    Parameters:
    -----------
    V : float - Membrane potential (mV)
    g_L_bar : float - Leak conductance (mS/cm²), default: 0.3
    E_L : float - Leak reversal potential (mV), default: -54.4

    Returns:
    --------
    I_L : float - Leak current (μA/cm²)
    """
    return g_L_bar * (V - E_L)

# Create and register atomic equation
hh_leak_current_eq = create_equation(
    id="excitable.action_potential.hh_leak_current",
    name="Hodgkin-Huxley Leak Current",
    category=EquationCategory.EXCITABLE,
    latex=r"I_L = \bar{g}_L (V - E_L)",
    simplified="I_L = g̅_L × (V - E_L)",
    description="Non-gated leak current representing baseline membrane permeability",
    compute_func=hh_leak_current,
    parameters=[
        Parameter(
            name="g_L_bar",
            description="Leak conductance",
            units="mS/cm²",
            symbol=r"\bar{g}_L",
            default_value=0.3,
            physiological_range=(0.1, 1.0)
        ),
        Parameter(
            name="V",
            description="Membrane potential",
            units="mV",
            symbol="V",
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="E_L",
            description="Leak reversal potential",
            units="mV",
            symbol="E_L",
            default_value=-54.4,
            physiological_range=(-70.0, -40.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.2")
)
register_equation(hh_leak_current_eq)

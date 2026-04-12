"""
Hodgkin-Huxley Potassium Current

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def hh_potassium_current(n: float, V: float, g_K_bar: float = 36.0, E_K: float = -77.0) -> float:
    """
    Potassium current in the Hodgkin-Huxley model.

    Formula: I_K = g̅_K × n⁴ × (V - E_K)

    The potassium current depends on maximal conductance, activation (n⁴),
    and driving force (V - E_K).

    Parameters:
    -----------
    n : float - Potassium activation gating variable (0-1)
    V : float - Membrane potential (mV)
    g_K_bar : float - Maximum potassium conductance (mS/cm²), default: 36.0
    E_K : float - Potassium reversal potential (mV), default: -77.0

    Returns:
    --------
    I_K : float - Potassium current (μA/cm²)
    """
    return g_K_bar * (n ** 4) * (V - E_K)

# Create and register atomic equation
hh_potassium_current_eq = create_equation(
    id="excitable.action_potential.hh_potassium_current",
    name="Hodgkin-Huxley Potassium Current",
    category=EquationCategory.EXCITABLE,
    latex=r"I_K = \bar{g}_K n^4 (V - E_K)",
    simplified="I_K = g̅_K × n⁴ × (V - E_K)",
    description="Voltage-gated potassium current with fourth-order activation",
    compute_func=hh_potassium_current,
    parameters=[
        Parameter(
            name="g_K_bar",
            description="Maximum potassium conductance",
            units="mS/cm²",
            symbol=r"\bar{g}_K",
            default_value=36.0,
            physiological_range=(20.0, 50.0)
        ),
        Parameter(
            name="n",
            description="Potassium activation gating variable",
            units="dimensionless",
            symbol="n",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="V",
            description="Membrane potential",
            units="mV",
            symbol="V",
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="E_K",
            description="Potassium reversal potential",
            units="mV",
            symbol="E_K",
            default_value=-77.0,
            physiological_range=(-95.0, -70.0)
        ),
    ],
    depends_on=["foundations.thermodynamics.nernst_equation"],  # E_K typically calculated from Nernst
    metadata=EquationMetadata(source_unit=3, source_chapter="3.2")
)
register_equation(hh_potassium_current_eq)

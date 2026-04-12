"""
Hodgkin-Huxley Sodium Current

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def hh_sodium_current(m: float, h: float, V: float, g_Na_bar: float = 120.0, E_Na: float = 50.0) -> float:
    """
    Sodium current in the Hodgkin-Huxley model.

    Formula: I_Na = g̅_Na × m³ × h × (V - E_Na)

    The sodium current depends on maximal conductance, activation (m³),
    inactivation (h), and driving force (V - E_Na).

    Parameters:
    -----------
    m : float - Sodium activation gating variable (0-1)
    h : float - Sodium inactivation gating variable (0-1)
    V : float - Membrane potential (mV)
    g_Na_bar : float - Maximum sodium conductance (mS/cm²), default: 120.0
    E_Na : float - Sodium reversal potential (mV), default: 50.0

    Returns:
    --------
    I_Na : float - Sodium current (μA/cm²)
    """
    return g_Na_bar * (m ** 3) * h * (V - E_Na)

# Create and register atomic equation
hh_sodium_current_eq = create_equation(
    id="excitable.action_potential.hh_sodium_current",
    name="Hodgkin-Huxley Sodium Current",
    category=EquationCategory.EXCITABLE,
    latex=r"I_{Na} = \bar{g}_{Na} m^3 h (V - E_{Na})",
    simplified="I_Na = g̅_Na × m³ × h × (V - E_Na)",
    description="Voltage-gated sodium current with cubic activation and linear inactivation",
    compute_func=hh_sodium_current,
    parameters=[
        Parameter(
            name="g_Na_bar",
            description="Maximum sodium conductance",
            units="mS/cm²",
            symbol=r"\bar{g}_{Na}",
            default_value=120.0,
            physiological_range=(80.0, 150.0)
        ),
        Parameter(
            name="m",
            description="Sodium activation gating variable",
            units="dimensionless",
            symbol="m",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="h",
            description="Sodium inactivation gating variable",
            units="dimensionless",
            symbol="h",
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
            name="E_Na",
            description="Sodium reversal potential",
            units="mV",
            symbol="E_{Na}",
            default_value=50.0,
            physiological_range=(40.0, 70.0)
        ),
    ],
    depends_on=["foundations.thermodynamics.nernst_equation"],  # E_Na typically calculated from Nernst
    metadata=EquationMetadata(source_unit=3, source_chapter="3.2")
)
register_equation(hh_sodium_current_eq)

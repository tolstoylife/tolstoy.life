"""
Shunting Inhibition - Membrane potential with excitation and inhibition

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_shunting_inhibition(g_e: float, E_e: float, g_i: float, E_i: float,
                                 g_L: float, E_L: float) -> float:
    """
    Calculate membrane potential with excitatory and inhibitory inputs.

    Formula: V_m = (g_e × E_e + g_i × E_i + g_L × E_L) / (g_e + g_i + g_L)

    Parameters:
    -----------
    g_e : float
        Excitatory synaptic conductance (nS)
    E_e : float
        Excitatory reversal potential (mV), typically 0 mV
    g_i : float
        Inhibitory synaptic conductance (nS)
    E_i : float
        Inhibitory reversal potential (mV), typically -70 to -80 mV (E_Cl)
    g_L : float
        Leak conductance (nS)
    E_L : float
        Leak reversal potential (mV), typically -70 mV

    Returns:
    --------
    V_m : float
        Membrane potential (mV)

    Notes:
    ------
    Shunting inhibition occurs when inhibitory conductance increases total
    conductance, reducing the effect of excitation even if E_i ≈ V_rest.
    This is more effective than hyperpolarizing inhibition in many cases.
    """
    return (g_e * E_e + g_i * E_i + g_L * E_L) / (g_e + g_i + g_L)


# Create and register atomic equation
shunting_inhibition = create_equation(
    id="nervous.synaptic.shunting_inhibition",
    name="Shunting Inhibition",
    category=EquationCategory.NERVOUS,
    latex=r"V_m = \frac{g_e \times E_e + g_i \times E_i + g_L \times E_L}{g_e + g_i + g_L}",
    simplified="V_m = (g_e × E_e + g_i × E_i + g_L × E_L) / (g_e + g_i + g_L)",
    description="Membrane potential with combined excitatory and inhibitory synaptic inputs. Demonstrates shunting inhibition where increased conductance reduces excitatory drive.",
    compute_func=compute_shunting_inhibition,
    parameters=[
        Parameter(
            name="g_e",
            description="Excitatory synaptic conductance",
            units="nS",
            symbol="g_e",
            default_value=None,
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="E_e",
            description="Excitatory reversal potential",
            units="mV",
            symbol="E_e",
            default_value=0.0,
            physiological_range=(-20.0, 20.0)
        ),
        Parameter(
            name="g_i",
            description="Inhibitory synaptic conductance",
            units="nS",
            symbol="g_i",
            default_value=None,
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="E_i",
            description="Inhibitory reversal potential",
            units="mV",
            symbol="E_i",
            default_value=-75.0,
            physiological_range=(-90.0, -60.0)
        ),
        Parameter(
            name="g_L",
            description="Leak conductance",
            units="nS",
            symbol="g_L",
            default_value=None,
            physiological_range=(0.1, 100.0)
        ),
        Parameter(
            name="E_L",
            description="Leak reversal potential",
            units="mV",
            symbol="E_L",
            default_value=-70.0,
            physiological_range=(-90.0, -50.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.2")
)

register_equation(shunting_inhibition)

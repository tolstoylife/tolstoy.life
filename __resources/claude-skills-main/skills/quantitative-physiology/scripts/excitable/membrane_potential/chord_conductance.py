"""
Chord Conductance Equation

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def chord_conductance(g_K: float, g_Na: float, g_Cl: float,
                      E_K: float = -90.0, E_Na: float = 67.0, E_Cl: float = -89.0) -> float:
    """
    Chord conductance equation for membrane potential.

    Formula: V_m = (g_K × E_K + g_Na × E_Na + g_Cl × E_Cl) / (g_K + g_Na + g_Cl)

    This represents the membrane as a parallel combination of ion channels,
    each with its own conductance and equilibrium potential.

    Parameters:
    -----------
    g_K : float - Potassium conductance (mS/cm²)
    g_Na : float - Sodium conductance (mS/cm²)
    g_Cl : float - Chloride conductance (mS/cm²)
    E_K : float - Potassium equilibrium potential (mV), default: -90.0
    E_Na : float - Sodium equilibrium potential (mV), default: 67.0
    E_Cl : float - Chloride equilibrium potential (mV), default: -89.0

    Returns:
    --------
    V_m : float - Membrane potential (mV)
    """
    numerator = g_K * E_K + g_Na * E_Na + g_Cl * E_Cl
    denominator = g_K + g_Na + g_Cl

    return numerator / denominator

# Create and register atomic equation
chord_conductance_eq = create_equation(
    id="excitable.membrane_potential.chord_conductance",
    name="Chord Conductance Equation",
    category=EquationCategory.EXCITABLE,
    latex=r"V_m = \frac{g_K E_K + g_{Na} E_{Na} + g_{Cl} E_{Cl}}{g_K + g_{Na} + g_{Cl}}",
    simplified="V_m = (g_K × E_K + g_Na × E_Na + g_Cl × E_Cl) / (g_K + g_Na + g_Cl)",
    description="Membrane potential from weighted average of equilibrium potentials",
    compute_func=chord_conductance,
    parameters=[
        Parameter(
            name="g_K",
            description="Potassium conductance",
            units="mS/cm²",
            symbol="g_K",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="g_Na",
            description="Sodium conductance",
            units="mS/cm²",
            symbol="g_{Na}",
            physiological_range=(0.0, 150.0)
        ),
        Parameter(
            name="g_Cl",
            description="Chloride conductance",
            units="mS/cm²",
            symbol="g_{Cl}",
            physiological_range=(0.0, 20.0)
        ),
        Parameter(
            name="E_K",
            description="Potassium equilibrium potential",
            units="mV",
            symbol="E_K",
            default_value=-90.0,
            physiological_range=(-95.0, -80.0)
        ),
        Parameter(
            name="E_Na",
            description="Sodium equilibrium potential",
            units="mV",
            symbol="E_{Na}",
            default_value=67.0,
            physiological_range=(50.0, 70.0)
        ),
        Parameter(
            name="E_Cl",
            description="Chloride equilibrium potential",
            units="mV",
            symbol="E_{Cl}",
            default_value=-89.0,
            physiological_range=(-95.0, -80.0)
        ),
    ],
    depends_on=["foundations.thermodynamics.nernst_equation"],  # E values from Nernst
    metadata=EquationMetadata(source_unit=3, source_chapter="3.1")
)
register_equation(chord_conductance_eq)

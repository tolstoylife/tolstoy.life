"""
Hodgkin-Huxley Membrane Current Equation

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def hh_membrane_current(I_ext: float, I_Na: float, I_K: float, I_L: float, C_m: float = 1.0) -> float:
    """
    Hodgkin-Huxley membrane current equation.

    Formula: C_m × dV/dt = I_ext - I_Na - I_K - I_L

    This is the fundamental equation describing membrane potential dynamics
    in the Hodgkin-Huxley model. It represents the capacitive current balance.

    Parameters:
    -----------
    I_ext : float - External current (μA/cm²)
    I_Na : float - Sodium current (μA/cm²)
    I_K : float - Potassium current (μA/cm²)
    I_L : float - Leak current (μA/cm²)
    C_m : float - Membrane capacitance (μF/cm²), default: 1.0

    Returns:
    --------
    dV_dt : float - Rate of change of membrane potential (mV/ms)
    """
    return (I_ext - I_Na - I_K - I_L) / C_m

# Create and register atomic equation
hh_membrane_current_eq = create_equation(
    id="excitable.action_potential.hh_membrane_current",
    name="Hodgkin-Huxley Membrane Current",
    category=EquationCategory.EXCITABLE,
    latex=r"C_m \frac{dV}{dt} = I_{ext} - I_{Na} - I_K - I_L",
    simplified="C_m × dV/dt = I_ext - I_Na - I_K - I_L",
    description="Rate of change of membrane potential based on capacitive current balance",
    compute_func=hh_membrane_current,
    parameters=[
        Parameter(
            name="C_m",
            description="Membrane capacitance",
            units="μF/cm²",
            symbol="C_m",
            default_value=1.0,
            physiological_range=(0.5, 2.0)
        ),
        Parameter(
            name="I_ext",
            description="External applied current",
            units="μA/cm²",
            symbol="I_{ext}",
            physiological_range=(-100.0, 100.0)
        ),
        Parameter(
            name="I_Na",
            description="Sodium current",
            units="μA/cm²",
            symbol="I_{Na}",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="I_K",
            description="Potassium current",
            units="μA/cm²",
            symbol="I_K",
            physiological_range=(0.0, 500.0)
        ),
        Parameter(
            name="I_L",
            description="Leak current",
            units="μA/cm²",
            symbol="I_L",
            physiological_range=(0.0, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.2")
)
register_equation(hh_membrane_current_eq)

"""
Membrane Time Constant

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def time_constant(R_m: float = 1000.0, C_m: float = 1e-6) -> float:
    """
    Membrane time constant.

    Formula: τ = R_m × C_m

    The time constant determines how quickly the membrane potential
    responds to changes in current.

    Parameters:
    -----------
    R_m : float - Specific membrane resistance (Ω·cm²), default 1000.0
    C_m : float - Specific membrane capacitance (F/cm²), default 1e-6

    Returns:
    --------
    tau : float - Time constant (s)
    """
    return R_m * C_m

# Create and register atomic equation
time_constant_eq = create_equation(
    id="excitable.action_potential.membrane_time_constant",
    name="Membrane Time Constant (τ = R_m × C_m)",
    category=EquationCategory.EXCITABLE,
    latex=r"\tau = R_m C_m",
    simplified="τ = R_m × C_m",
    description="Characteristic time for membrane potential changes",
    compute_func=time_constant,
    parameters=[
        Parameter(
            name="R_m",
            description="Specific membrane resistance",
            units="Ω·cm²",
            symbol="R_m",
            default_value=1000.0,
            physiological_range=(500.0, 10000.0)
        ),
        Parameter(
            name="C_m",
            description="Specific membrane capacitance",
            units="F/cm²",
            symbol="C_m",
            default_value=1e-6,  # 1 μF/cm²
            physiological_range=(0.5e-6, 2e-6)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.3")
)
register_equation(time_constant_eq)

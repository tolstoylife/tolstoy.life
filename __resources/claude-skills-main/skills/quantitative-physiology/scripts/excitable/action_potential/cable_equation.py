"""
Cable Equation for Passive Spread

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def cable_equation(lambda_const: float, tau: float, V: float, d2V_dx2: float = 0.0, dV_dt: float = 0.0) -> float:
    """
    Cable equation for passive voltage spread along an axon.

    Formula: λ² × ∂²V/∂x² - τ × ∂V/∂t = V

    This partial differential equation describes how voltage spreads
    passively along a cable-like structure (axon or dendrite).

    Note: This is a PDE. The compute function returns the steady-state
    spatial decay coefficient for instructional purposes.

    Parameters:
    -----------
    lambda_const : float - Space constant (cm)
    tau : float - Time constant (ms)
    V : float - Voltage deviation from rest (mV)
    d2V_dx2 : float - Second spatial derivative (mV/cm²), default 0.0
    dV_dt : float - Temporal derivative (mV/ms), default 0.0

    Returns:
    --------
    residual : float - PDE residual (should be 0 at solution)
    """
    return lambda_const**2 * d2V_dx2 - tau * dV_dt - V

# Create and register atomic equation
cable_equation_eq = create_equation(
    id="excitable.action_potential.cable_equation",
    name="Cable Equation",
    category=EquationCategory.EXCITABLE,
    latex=r"\lambda^2 \frac{\partial^2 V}{\partial x^2} - \tau \frac{\partial V}{\partial t} = V",
    simplified="λ² × ∂²V/∂x² - τ × ∂V/∂t = V",
    description="Partial differential equation describing passive voltage spread along axons",
    compute_func=cable_equation,
    parameters=[
        Parameter(
            name="lambda_const",
            description="Space constant",
            units="cm",
            symbol=r"\lambda",
            physiological_range=(0.01, 1.0)
        ),
        Parameter(
            name="tau",
            description="Time constant",
            units="ms",
            symbol=r"\tau",
            physiological_range=(1.0, 20.0)
        ),
        Parameter(
            name="V",
            description="Voltage deviation from rest",
            units="mV",
            symbol="V",
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="d2V_dx2",
            description="Second spatial derivative of voltage",
            units="mV/cm²",
            symbol=r"\frac{\partial^2 V}{\partial x^2}",
            physiological_range=(-1000.0, 1000.0)
        ),
        Parameter(
            name="dV_dt",
            description="Temporal derivative of voltage",
            units="mV/ms",
            symbol=r"\frac{\partial V}{\partial t}",
            physiological_range=(-100.0, 100.0)
        ),
    ],
    depends_on=["excitable.action_potential.space_constant", "respiratory.mechanics.time_constant"],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.3")
)
register_equation(cable_equation_eq)

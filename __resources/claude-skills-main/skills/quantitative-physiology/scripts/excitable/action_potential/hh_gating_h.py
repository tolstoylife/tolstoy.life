"""
Hodgkin-Huxley Sodium Inactivation Gating (h)

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def hh_gating_h(V: float, h: float) -> float:
    """
    Rate of change of sodium inactivation gating variable h.

    Formula: dh/dt = α_h(V) × (1-h) - β_h(V) × h

    Where:
    α_h = 0.07 × exp(-(V+65)/20)
    β_h = 1 / [1 + exp(-(V+35)/10)]

    Parameters:
    -----------
    V : float - Membrane potential (mV)
    h : float - Current h value (0-1)

    Returns:
    --------
    dh_dt : float - Rate of change of h (1/ms)
    """
    # Rate constants
    alpha_h = 0.07 * np.exp(-(V + 65) / 20)
    beta_h = 1 / (1 + np.exp(-(V + 35) / 10))

    return alpha_h * (1 - h) - beta_h * h

# Create and register atomic equation
hh_gating_h_eq = create_equation(
    id="excitable.action_potential.hh_gating_h",
    name="Hodgkin-Huxley Sodium Inactivation (h)",
    category=EquationCategory.EXCITABLE,
    latex=r"\frac{dh}{dt} = \alpha_h(V)(1-h) - \beta_h(V)h",
    simplified="dh/dt = α_h(V) × (1-h) - β_h(V) × h",
    description="Dynamics of sodium channel inactivation gating variable",
    compute_func=hh_gating_h,
    parameters=[
        Parameter(
            name="V",
            description="Membrane potential",
            units="mV",
            symbol="V",
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="h",
            description="Sodium inactivation gating variable",
            units="dimensionless",
            symbol="h",
            physiological_range=(0.0, 1.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.2")
)
register_equation(hh_gating_h_eq)

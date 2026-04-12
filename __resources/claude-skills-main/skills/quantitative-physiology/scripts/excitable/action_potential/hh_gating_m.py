"""
Hodgkin-Huxley Sodium Activation Gating (m)

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def hh_gating_m(V: float, m: float) -> float:
    """
    Rate of change of sodium activation gating variable m.

    Formula: dm/dt = α_m(V) × (1-m) - β_m(V) × m

    Where:
    α_m = 0.1(V+40) / [1 - exp(-(V+40)/10)]
    β_m = 4 × exp(-(V+65)/18)

    Parameters:
    -----------
    V : float - Membrane potential (mV)
    m : float - Current m value (0-1)

    Returns:
    --------
    dm_dt : float - Rate of change of m (1/ms)
    """
    # Rate constants
    alpha_m = 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
    beta_m = 4 * np.exp(-(V + 65) / 18)

    return alpha_m * (1 - m) - beta_m * m

# Create and register atomic equation
hh_gating_m_eq = create_equation(
    id="excitable.action_potential.hh_gating_m",
    name="Hodgkin-Huxley Sodium Activation (m)",
    category=EquationCategory.EXCITABLE,
    latex=r"\frac{dm}{dt} = \alpha_m(V)(1-m) - \beta_m(V)m",
    simplified="dm/dt = α_m(V) × (1-m) - β_m(V) × m",
    description="Dynamics of sodium channel activation gating variable",
    compute_func=hh_gating_m,
    parameters=[
        Parameter(
            name="V",
            description="Membrane potential",
            units="mV",
            symbol="V",
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="m",
            description="Sodium activation gating variable",
            units="dimensionless",
            symbol="m",
            physiological_range=(0.0, 1.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.2")
)
register_equation(hh_gating_m_eq)

"""
Hodgkin-Huxley Potassium Activation Gating (n)

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def hh_gating_n(V: float, n: float) -> float:
    """
    Rate of change of potassium activation gating variable n.

    Formula: dn/dt = α_n(V) × (1-n) - β_n(V) × n

    Where:
    α_n = 0.01(V+55) / [1 - exp(-(V+55)/10)]
    β_n = 0.125 × exp(-(V+65)/80)

    Parameters:
    -----------
    V : float - Membrane potential (mV)
    n : float - Current n value (0-1)

    Returns:
    --------
    dn_dt : float - Rate of change of n (1/ms)
    """
    # Rate constants
    alpha_n = 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10))
    beta_n = 0.125 * np.exp(-(V + 65) / 80)

    return alpha_n * (1 - n) - beta_n * n

# Create and register atomic equation
hh_gating_n_eq = create_equation(
    id="excitable.action_potential.hh_gating_n",
    name="Hodgkin-Huxley Potassium Activation (n)",
    category=EquationCategory.EXCITABLE,
    latex=r"\frac{dn}{dt} = \alpha_n(V)(1-n) - \beta_n(V)n",
    simplified="dn/dt = α_n(V) × (1-n) - β_n(V) × n",
    description="Dynamics of potassium channel activation gating variable",
    compute_func=hh_gating_n,
    parameters=[
        Parameter(
            name="V",
            description="Membrane potential",
            units="mV",
            symbol="V",
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="n",
            description="Potassium activation gating variable",
            units="dimensionless",
            symbol="n",
            physiological_range=(0.0, 1.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.2")
)
register_equation(hh_gating_n_eq)

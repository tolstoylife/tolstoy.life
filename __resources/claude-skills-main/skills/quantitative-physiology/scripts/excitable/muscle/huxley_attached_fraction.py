"""
Huxley Attached Cross-Bridge Fraction

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def huxley_attached_fraction(f: float, g: float, n: float = 0.0, compute_steady_state: bool = False) -> float:
    """
    Rate of change of attached cross-bridge fraction.

    Formula: dn/dt = (1-n) × f(x) - n × g(x)

    Steady-state: n = f / (f + g)

    Parameters:
    -----------
    f : float - Attachment rate (s⁻¹)
    g : float - Detachment rate (s⁻¹)
    n : float - Current fraction of attached bridges (0-1), default: 0.0
    compute_steady_state : bool - If True, return steady-state value, default: False

    Returns:
    --------
    dn_dt or n_ss : float - Rate of change (1/s) or steady-state fraction
    """
    if compute_steady_state:
        # Steady-state value
        if f + g > 0:
            return f / (f + g)
        else:
            return 0.0
    else:
        # Time derivative
        return (1 - n) * f - n * g

# Create and register atomic equation
huxley_attached_fraction_eq = create_equation(
    id="excitable.muscle.huxley_attached_fraction",
    name="Huxley Attached Cross-Bridge Fraction",
    category=EquationCategory.EXCITABLE,
    latex=r"\frac{dn}{dt} = (1-n)f(x) - n g(x)",
    simplified="dn/dt = (1-n) × f(x) - n × g(x)",
    description="Dynamics of cross-bridge attachment during muscle contraction",
    compute_func=huxley_attached_fraction,
    parameters=[
        Parameter(
            name="n",
            description="Fraction of attached cross-bridges",
            units="dimensionless",
            symbol="n",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="f",
            description="Attachment rate",
            units="s⁻¹",
            symbol="f",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="g",
            description="Detachment rate",
            units="s⁻¹",
            symbol="g",
            physiological_range=(0.0, 300.0)
        ),
        Parameter(
            name="compute_steady_state",
            description="Flag to compute steady-state value",
            units="boolean",
            symbol="",
            default_value=False
        ),
    ],
    depends_on=["excitable.muscle.huxley_attachment_rate", "excitable.muscle.huxley_detachment_rate"],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.5")
)
register_equation(huxley_attached_fraction_eq)

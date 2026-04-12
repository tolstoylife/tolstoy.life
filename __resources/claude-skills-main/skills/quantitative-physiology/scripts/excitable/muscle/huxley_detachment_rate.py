"""
Huxley Cross-Bridge Detachment Rate

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def huxley_detachment_rate(x: float, g1: float = 10.0, g2: float = 209.0, h: float = 10.0) -> float:
    """
    Huxley 1957 cross-bridge detachment rate function.

    Formula: g(x) = g₂ × (-x)/h      for x < 0
                  = g₁               for 0 ≤ x < h
                  = g₂ × (x-h)/h     for x ≥ h

    Parameters:
    -----------
    x : float - Cross-bridge displacement (nm)
    g1 : float - Detachment rate constant in power stroke region (s⁻¹), default: 10.0
    g2 : float - Rapid detachment rate constant outside region (s⁻¹), default: 209.0
    h : float - Cross-bridge stroke distance (nm), default: 10.0

    Returns:
    --------
    g : float - Detachment rate (s⁻¹)
    """
    if x < 0:
        return g2 * (-x) / h
    elif 0 <= x < h:
        return g1
    else:  # x >= h
        return g2 * (x - h) / h

# Create and register atomic equation
huxley_detachment_rate_eq = create_equation(
    id="excitable.muscle.huxley_detachment_rate",
    name="Huxley Cross-Bridge Detachment Rate",
    category=EquationCategory.EXCITABLE,
    latex=r"g(x) = \begin{cases} g_2 \frac{-x}{h} & x < 0 \\ g_1 & 0 \le x < h \\ g_2 \frac{x-h}{h} & x \ge h \end{cases}",
    simplified="g(x) = g₁ for 0≤x<h, g₂×(±displacement)/h otherwise",
    description="Rate of cross-bridge detachment as function of displacement",
    compute_func=huxley_detachment_rate,
    parameters=[
        Parameter(
            name="x",
            description="Cross-bridge displacement",
            units="nm",
            symbol="x",
            physiological_range=(-20.0, 20.0)
        ),
        Parameter(
            name="g1",
            description="Detachment rate in power stroke region",
            units="s⁻¹",
            symbol="g_1",
            default_value=10.0,
            physiological_range=(5.0, 20.0)
        ),
        Parameter(
            name="g2",
            description="Rapid detachment rate outside region",
            units="s⁻¹",
            symbol="g_2",
            default_value=209.0,
            physiological_range=(100.0, 300.0)
        ),
        Parameter(
            name="h",
            description="Cross-bridge stroke distance",
            units="nm",
            symbol="h",
            default_value=10.0,
            physiological_range=(5.0, 15.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.5")
)
register_equation(huxley_detachment_rate_eq)

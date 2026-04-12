"""
Huxley Cross-Bridge Attachment Rate

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def huxley_attachment_rate(x: float, f1: float = 43.3, h: float = 10.0) -> float:
    """
    Huxley 1957 cross-bridge attachment rate function.

    Formula: f(x) = f₁ × (h-x)/h  for 0 < x < h
                  = 0              otherwise

    Where x is the displacement of the cross-bridge from its
    unstrained position.

    Parameters:
    -----------
    x : float - Cross-bridge displacement (nm)
    f1 : float - Maximum attachment rate constant (s⁻¹), default: 43.3
    h : float - Cross-bridge stroke distance (nm), default: 10.0

    Returns:
    --------
    f : float - Attachment rate (s⁻¹)
    """
    if 0 < x < h:
        return f1 * (h - x) / h
    else:
        return 0.0

# Create and register atomic equation
huxley_attachment_rate_eq = create_equation(
    id="excitable.muscle.huxley_attachment_rate",
    name="Huxley Cross-Bridge Attachment Rate",
    category=EquationCategory.EXCITABLE,
    latex=r"f(x) = \begin{cases} f_1 \frac{h-x}{h} & 0 < x < h \\ 0 & \text{otherwise} \end{cases}",
    simplified="f(x) = f₁ × (h-x)/h for 0 < x < h",
    description="Rate of cross-bridge attachment as function of displacement",
    compute_func=huxley_attachment_rate,
    parameters=[
        Parameter(
            name="x",
            description="Cross-bridge displacement",
            units="nm",
            symbol="x",
            physiological_range=(-20.0, 20.0)
        ),
        Parameter(
            name="f1",
            description="Maximum attachment rate constant",
            units="s⁻¹",
            symbol="f_1",
            default_value=43.3,
            physiological_range=(10.0, 100.0)
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
register_equation(huxley_attachment_rate_eq)

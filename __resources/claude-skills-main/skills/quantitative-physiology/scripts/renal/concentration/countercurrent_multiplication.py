"""
Countercurrent multiplication factor.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

import math
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_multiplication_factor(loop_length: float, lambda_char: float) -> float:
    """
    Calculate countercurrent multiplication factor.

    Args:
        loop_length: Length of loop of Henle
        lambda_char: Characteristic length for concentration

    Returns:
        M: Multiplication factor (π_tip / π_base)
    """
    return math.exp(loop_length / lambda_char)


# Create equation
countercurrent_multiplication = create_equation(
    id="renal.concentration.countercurrent_multiplication",
    name="Countercurrent Multiplication Factor",
    category=EquationCategory.RENAL,
    latex=r"M = \frac{\pi_{tip}}{\pi_{base}} = e^{L/\lambda}",
    simplified="M = π_tip / π_base = e^(L/λ)",
    description="Amplification of osmotic gradient achieved by countercurrent loop structure",
    compute_func=compute_multiplication_factor,
    parameters=[
        Parameter(
            name="loop_length",
            description="Length of loop of Henle",
            units="mm",
            symbol="L",
            physiological_range=(2, 15)
        ),
        Parameter(
            name="lambda_char",
            description="Characteristic length for concentration",
            units="mm",
            symbol=r"\lambda",
            physiological_range=(1, 5)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.4"
    )
)

# Register equation
register_equation(countercurrent_multiplication)

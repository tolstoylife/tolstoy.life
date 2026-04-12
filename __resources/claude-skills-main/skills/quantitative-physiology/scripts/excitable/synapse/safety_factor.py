"""
Neuromuscular Junction Safety Factor

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def safety_factor(EPP: float = 75.0, threshold: float = 20.0) -> float:
    """
    Safety factor for neuromuscular transmission.

    Formula: Safety Factor = EPP / Threshold

    The safety factor indicates how much the EPP exceeds the threshold
    needed to trigger an action potential in the muscle fiber.

    Parameters:
    -----------
    EPP : float - End-plate potential amplitude (mV), default: 75.0
    threshold : float - Threshold for muscle action potential (mV), default: 20.0

    Returns:
    --------
    SF : float - Safety factor (dimensionless)
    """
    return EPP / threshold

# Create and register atomic equation
safety_factor_eq = create_equation(
    id="excitable.synapse.safety_factor",
    name="Neuromuscular Junction Safety Factor",
    category=EquationCategory.EXCITABLE,
    latex=r"\text{SF} = \frac{\text{EPP}}{\text{Threshold}}",
    simplified="SF = EPP / Threshold",
    description="Margin of safety for successful neuromuscular transmission",
    compute_func=safety_factor,
    parameters=[
        Parameter(
            name="EPP",
            description="End-plate potential amplitude",
            units="mV",
            symbol="EPP",
            default_value=75.0,
            physiological_range=(50.0, 100.0)
        ),
        Parameter(
            name="threshold",
            description="Threshold for muscle action potential",
            units="mV",
            symbol="V_{th}",
            default_value=20.0,
            physiological_range=(15.0, 30.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.6")
)
register_equation(safety_factor_eq)

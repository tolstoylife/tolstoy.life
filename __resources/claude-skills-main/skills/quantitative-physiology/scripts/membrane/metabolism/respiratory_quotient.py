"""
Respiratory Quotient - Ratio of CO2 production to O2 consumption

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_respiratory_quotient(CO2_produced: float, O2_consumed: float) -> float:
    """
    Calculate respiratory quotient (RQ).

    Formula: RQ = CO₂ produced / O₂ consumed

    RQ indicates which substrate is being oxidized:

    Parameters:
    -----------
    CO2_produced : float
        Rate of CO2 production (mol/time)
    O2_consumed : float
        Rate of O2 consumption (mol/time)

    Returns:
    --------
    RQ : float
        Respiratory quotient (dimensionless)

    Typical values:
        Carbohydrates: RQ = 1.0
            C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O
        Fats: RQ ≈ 0.7
            C₁₆H₃₂O₂ + 23O₂ → 16CO₂ + 16H₂O
        Proteins: RQ ≈ 0.8
        Mixed diet: RQ ≈ 0.8-0.85
    """
    return CO2_produced / O2_consumed


# Create and register atomic equation
respiratory_quotient = create_equation(
    id="membrane.metabolism.respiratory_quotient",
    name="Respiratory Quotient",
    category=EquationCategory.MEMBRANE,
    latex=r"RQ = \frac{CO_2 \text{ produced}}{O_2 \text{ consumed}}",
    simplified="RQ = CO2_produced / O2_consumed",
    description="Ratio of CO2 production to O2 consumption, indicating fuel substrate being oxidized.",
    compute_func=compute_respiratory_quotient,
    parameters=[
        Parameter(
            name="CO2_produced",
            description="Rate of CO2 production",
            units="mol/time",
            symbol=r"\dot{V}_{CO_2}",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="O2_consumed",
            description="Rate of O2 consumption",
            units="mol/time",
            symbol=r"\dot{V}_{O_2}",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.7")
)

register_equation(respiratory_quotient)

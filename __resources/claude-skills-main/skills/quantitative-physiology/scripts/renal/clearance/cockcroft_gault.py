"""
Cockcroft-Gault equation for creatinine clearance estimation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_cockcroft_gault(age: float, weight: float, S_Cr: float, female: bool = False) -> float:
    """
    Estimate creatinine clearance using Cockcroft-Gault equation.

    Args:
        age: Patient age (years)
        weight: Body weight (kg)
        S_Cr: Serum creatinine (mg/dL)
        female: True if patient is female

    Returns:
        C_Cr: Estimated creatinine clearance (mL/min)
    """
    C_Cr = ((140 - age) * weight) / (72 * S_Cr)
    if female:
        C_Cr *= 0.85
    return C_Cr


# Create equation
cockcroft_gault = create_equation(
    id="renal.clearance.cockcroft_gault",
    name="Cockcroft-Gault Equation",
    category=EquationCategory.RENAL,
    latex=r"C_{Cr} = \frac{(140 - age) \times weight}{72 \times S_{Cr}} \times [0.85 \text{ if female}]",
    simplified="C_Cr = [(140 - age) × weight] / (72 × S_Cr) × [0.85 if female]",
    description="Clinical estimate of creatinine clearance from age, weight, and serum creatinine",
    compute_func=compute_cockcroft_gault,
    parameters=[
        Parameter(
            name="age",
            description="Patient age",
            units="years",
            symbol="age",
            physiological_range=(18, 100)
        ),
        Parameter(
            name="weight",
            description="Body weight",
            units="kg",
            symbol="weight",
            physiological_range=(40, 150)
        ),
        Parameter(
            name="S_Cr",
            description="Serum creatinine",
            units="mg/dL",
            symbol="S_{Cr}",
            physiological_range=(0.5, 5.0)
        ),
        Parameter(
            name="female",
            description="Sex (True for female)",
            units="boolean",
            symbol="female",
            default_value=False
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.2"
    )
)

# Register equation
register_equation(cockcroft_gault)

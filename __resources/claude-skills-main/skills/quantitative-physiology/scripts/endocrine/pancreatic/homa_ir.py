"""
HOMA-IR: Homeostatic Model Assessment of Insulin Resistance.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_homa_ir(fasting_glucose_mmol: float, fasting_insulin_uU: float) -> float:
    """
    Calculate HOMA-IR insulin resistance index.

    Parameters
    ----------
    fasting_glucose_mmol : float
        Fasting glucose concentration (mmol/L)
    fasting_insulin_uU : float
        Fasting insulin concentration (μU/mL)

    Returns
    -------
    float
        HOMA-IR (dimensionless)

    Notes
    -----
    Normal HOMA-IR: <2.5
    Insulin resistance: >2.5
    Conversion: glucose (mg/dL) ÷ 18 = mmol/L
    """
    return (fasting_glucose_mmol * fasting_insulin_uU) / 22.5


# Create equation
homa_ir_equation = create_equation(
    id="endocrine.pancreatic.homa_ir",
    name="HOMA-IR Insulin Resistance Index",
    category=EquationCategory.ENDOCRINE,
    latex=r"\text{HOMA-IR} = \frac{\text{Glucose}_{mmol/L} \times \text{Insulin}_{\mu U/mL}}{22.5}",
    simplified="HOMA-IR = (Glucose_mmol × Insulin_μU) / 22.5",
    description="Homeostatic Model Assessment of Insulin Resistance. "
                "Calculated from fasting glucose and insulin. Normal <2.5.",
    compute_func=compute_homa_ir,
    parameters=[
        Parameter(
            name="fasting_glucose_mmol",
            description="Fasting glucose concentration",
            units="mmol/L",
            symbol="Glucose",
            physiological_range=(3.0, 15.0)
        ),
        Parameter(
            name="fasting_insulin_uU",
            description="Fasting insulin concentration",
            units="μU/mL",
            symbol="Insulin",
            physiological_range=(2.0, 50.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.6"
    )
)

# Register globally
register_equation(homa_ir_equation)

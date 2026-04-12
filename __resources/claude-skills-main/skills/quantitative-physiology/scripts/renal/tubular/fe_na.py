"""
Fractional excretion of sodium (FE_Na).

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_fe_na(U_Na: float, P_Cr: float, P_Na: float, U_Cr: float) -> float:
    """
    Calculate fractional excretion of sodium.

    Uses creatinine to normalize for GFR without directly measuring it.

    Args:
        U_Na: Urine sodium concentration (mmol/L)
        P_Cr: Plasma creatinine concentration (mg/dL)
        P_Na: Plasma sodium concentration (mmol/L)
        U_Cr: Urine creatinine concentration (mg/dL)

    Returns:
        FE_Na: Fractional excretion of sodium (%)
    """
    return (U_Na * P_Cr) / (P_Na * U_Cr) * 100


# Create equation
fe_na = create_equation(
    id="renal.tubular.fe_na",
    name="Fractional Excretion of Sodium",
    category=EquationCategory.RENAL,
    latex=r"FE_{Na} = \frac{U_{Na} \times P_{Cr}}{P_{Na} \times U_{Cr}} \times 100\%",
    simplified="FE_Na = (U_Na × P_Cr) / (P_Na × U_Cr) × 100%",
    description="Fraction of filtered sodium excreted; distinguishes prerenal from intrinsic renal failure",
    compute_func=compute_fe_na,
    parameters=[
        Parameter(
            name="U_Na",
            description="Urine sodium concentration",
            units="mmol/L",
            symbol="U_{Na}",
            physiological_range=(10, 200)
        ),
        Parameter(
            name="P_Cr",
            description="Plasma creatinine concentration",
            units="mg/dL",
            symbol="P_{Cr}",
            physiological_range=(0.5, 5.0)
        ),
        Parameter(
            name="P_Na",
            description="Plasma sodium concentration",
            units="mmol/L",
            symbol="P_{Na}",
            physiological_range=(135, 145)
        ),
        Parameter(
            name="U_Cr",
            description="Urine creatinine concentration",
            units="mg/dL",
            symbol="U_{Cr}",
            physiological_range=(20, 300)
        )
    ],
    depends_on=["renal.tubular.fractional_excretion"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Register equation
register_equation(fe_na)

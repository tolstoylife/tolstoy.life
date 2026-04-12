"""
Fractional excretion calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_fractional_excretion(C_x: float, GFR: float) -> float:
    """
    Calculate fractional excretion from clearance.

    Args:
        C_x: Clearance of substance x (mL/min)
        GFR: Glomerular filtration rate (mL/min)

    Returns:
        FE_x: Fractional excretion (dimensionless, as fraction)
    """
    return C_x / GFR


def compute_fractional_excretion_direct(U_x: float, V_dot: float, GFR: float, P_x: float) -> float:
    """
    Calculate fractional excretion directly from measurements.

    Args:
        U_x: Urine concentration of substance
        V_dot: Urine flow rate (mL/min)
        GFR: Glomerular filtration rate (mL/min)
        P_x: Plasma concentration of substance

    Returns:
        FE_x: Fractional excretion (dimensionless, as fraction)
    """
    return (U_x * V_dot) / (GFR * P_x)


# Create equation (clearance method)
fractional_excretion = create_equation(
    id="renal.tubular.fractional_excretion",
    name="Fractional Excretion",
    category=EquationCategory.RENAL,
    latex=r"FE_x = \frac{C_x}{GFR}",
    simplified="FE_x = C_x / GFR",
    description="Fraction of filtered substance that is excreted in urine",
    compute_func=compute_fractional_excretion,
    parameters=[
        Parameter(
            name="C_x",
            description="Clearance of substance x",
            units="mL/min",
            symbol="C_x",
            physiological_range=(0, 200)
        ),
        Parameter(
            name="GFR",
            description="Glomerular filtration rate",
            units="mL/min",
            symbol="GFR",
            physiological_range=(90, 140)
        )
    ],
    depends_on=["renal.clearance.clearance"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Create direct calculation equation
fractional_excretion_direct = create_equation(
    id="renal.tubular.fractional_excretion_direct",
    name="Fractional Excretion (Direct)",
    category=EquationCategory.RENAL,
    latex=r"FE_x = \frac{U_x \times \dot{V}}{GFR \times P_x}",
    simplified="FE_x = (U_x × V̇) / (GFR × P_x)",
    description="Direct calculation of fractional excretion from urine and plasma measurements",
    compute_func=compute_fractional_excretion_direct,
    parameters=[
        Parameter(
            name="U_x",
            description="Urine concentration of substance",
            units="mg/dL or mmol/L",
            symbol="U_x",
            physiological_range=(0, 1000)
        ),
        Parameter(
            name="V_dot",
            description="Urine flow rate",
            units="mL/min",
            symbol=r"\dot{V}",
            physiological_range=(0.5, 20)
        ),
        Parameter(
            name="GFR",
            description="Glomerular filtration rate",
            units="mL/min",
            symbol="GFR",
            physiological_range=(90, 140)
        ),
        Parameter(
            name="P_x",
            description="Plasma concentration of substance",
            units="mg/dL or mmol/L",
            symbol="P_x",
            physiological_range=(0, 1000)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Register equations
register_equation(fractional_excretion)
register_equation(fractional_excretion_direct)

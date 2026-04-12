"""
General clearance equation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_clearance(U_x: float, V_dot: float, P_x: float) -> float:
    """
    Calculate clearance of substance x.

    Args:
        U_x: Urine concentration of substance (mg/dL or mmol/L)
        V_dot: Urine flow rate (mL/min)
        P_x: Plasma concentration of substance (same units as U_x)

    Returns:
        C_x: Clearance of substance x (mL/min)
    """
    return (U_x * V_dot) / P_x


# Create equation
clearance = create_equation(
    id="renal.clearance.clearance",
    name="General Clearance Equation",
    category=EquationCategory.RENAL,
    latex=r"C_x = \frac{U_x \times \dot{V}}{P_x}",
    simplified="C_x = (U_x × V̇) / P_x",
    description="Volume of plasma completely cleared of a substance per unit time",
    compute_func=compute_clearance,
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
            name="P_x",
            description="Plasma concentration of substance",
            units="mg/dL or mmol/L",
            symbol="P_x",
            physiological_range=(0, 100)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.2"
    )
)

# Register equation
register_equation(clearance)

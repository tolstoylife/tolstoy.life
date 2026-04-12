"""
Filtered load calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_filtered_load(GFR: float, P_x: float) -> float:
    """
    Calculate amount of substance filtered per unit time.

    Args:
        GFR: Glomerular filtration rate (mL/min)
        P_x: Plasma concentration of substance (mg/dL or mmol/L)

    Returns:
        FL: Filtered load (mg/min or mmol/min)
    """
    return GFR * P_x


# Create equation
filtered_load = create_equation(
    id="renal.clearance.filtered_load",
    name="Filtered Load",
    category=EquationCategory.RENAL,
    latex=r"FL = GFR \times P_x",
    simplified="FL = GFR × P_x",
    description="Amount of substance filtered at the glomerulus per unit time",
    compute_func=compute_filtered_load,
    parameters=[
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
        source_chapter="7.2"
    )
)

# Register equation
register_equation(filtered_load)

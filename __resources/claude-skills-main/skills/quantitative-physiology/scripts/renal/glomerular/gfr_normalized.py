"""
GFR normalization for body surface area.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_gfr_normalized(GFR: float, BSA: float) -> float:
    """
    Normalize GFR to standard body surface area (1.73 m²).

    Args:
        GFR: Measured glomerular filtration rate (mL/min)
        BSA: Body surface area (m²)

    Returns:
        GFR_normalized: GFR normalized to 1.73 m² (mL/min/1.73m²)
    """
    return GFR * (1.73 / BSA)


# Create equation
gfr_normalized = create_equation(
    id="renal.glomerular.gfr_normalized",
    name="GFR Normalized for Body Surface Area",
    category=EquationCategory.RENAL,
    latex=r"GFR_{normalized} = GFR \times \frac{1.73}{BSA}",
    simplified="GFR_normalized = GFR × (1.73 / BSA)",
    description="Adjusts GFR to standardized body surface area for comparison",
    compute_func=compute_gfr_normalized,
    parameters=[
        Parameter(
            name="GFR",
            description="Measured glomerular filtration rate",
            units="mL/min",
            symbol="GFR",
            physiological_range=(60, 180)
        ),
        Parameter(
            name="BSA",
            description="Body surface area",
            units="m²",
            symbol="BSA",
            physiological_range=(1.2, 2.5)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.2"
    )
)

# Register equation
register_equation(gfr_normalized)

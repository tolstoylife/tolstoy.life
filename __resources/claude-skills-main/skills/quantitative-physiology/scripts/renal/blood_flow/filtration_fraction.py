"""
Filtration Fraction (FF) calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_filtration_fraction(GFR: float, RPF: float) -> float:
    """
    Calculate filtration fraction.

    Args:
        GFR: Glomerular filtration rate (mL/min)
        RPF: Renal plasma flow (mL/min)

    Returns:
        FF: Filtration fraction (dimensionless, typically ~0.20)
    """
    return GFR / RPF


# Create equation
filtration_fraction = create_equation(
    id="renal.blood_flow.filtration_fraction",
    name="Filtration Fraction",
    category=EquationCategory.RENAL,
    latex=r"FF = \frac{GFR}{RPF}",
    simplified="FF = GFR / RPF",
    description="Fraction of renal plasma flow that is filtered at the glomerulus",
    compute_func=compute_filtration_fraction,
    parameters=[
        Parameter(
            name="GFR",
            description="Glomerular filtration rate",
            units="mL/min",
            symbol="GFR",
            physiological_range=(90, 140)
        ),
        Parameter(
            name="RPF",
            description="Renal plasma flow",
            units="mL/min",
            symbol="RPF",
            physiological_range=(600, 700)
        )
    ],
    depends_on=["renal.blood_flow.renal_plasma_flow"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.1"
    )
)

# Register equation
register_equation(filtration_fraction)

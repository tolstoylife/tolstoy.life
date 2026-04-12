"""
Renal Plasma Flow (RPF) calculation from Renal Blood Flow.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_rpf(RBF: float, Hct: float = 0.45) -> float:
    """
    Calculate renal plasma flow from renal blood flow.

    Args:
        RBF: Renal blood flow (L/min)
        Hct: Hematocrit (fraction, default 0.45)

    Returns:
        RPF: Renal plasma flow (L/min)
    """
    return RBF * (1 - Hct)


# Create equation
renal_plasma_flow = create_equation(
    id="renal.blood_flow.renal_plasma_flow",
    name="Renal Plasma Flow",
    category=EquationCategory.RENAL,
    latex=r"RPF = RBF \times (1 - Hct)",
    simplified="RPF = RBF × (1 - Hct)",
    description="Calculates renal plasma flow from renal blood flow and hematocrit",
    compute_func=compute_rpf,
    parameters=[
        Parameter(
            name="RBF",
            description="Renal blood flow",
            units="L/min",
            symbol="RBF",
            physiological_range=(0.8, 1.5)
        ),
        Parameter(
            name="Hct",
            description="Hematocrit (fraction)",
            units="dimensionless",
            symbol="Hct",
            default_value=0.45,
            physiological_range=(0.35, 0.52)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.1"
    )
)

# Register equation
register_equation(renal_plasma_flow)

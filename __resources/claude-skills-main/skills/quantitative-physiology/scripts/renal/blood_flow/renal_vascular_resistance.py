"""
Renal Vascular Resistance (RVR) calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_rvr(P_a: float, P_v: float, RBF: float) -> float:
    """
    Calculate renal vascular resistance.

    Args:
        P_a: Arterial pressure (mmHg)
        P_v: Venous pressure (mmHg)
        RBF: Renal blood flow (mL/min)

    Returns:
        RVR: Renal vascular resistance (mmHg·min/mL)
    """
    return (P_a - P_v) / RBF


# Create equation
renal_vascular_resistance = create_equation(
    id="renal.blood_flow.renal_vascular_resistance",
    name="Renal Vascular Resistance",
    category=EquationCategory.RENAL,
    latex=r"RVR = \frac{P_a - P_v}{RBF}",
    simplified="RVR = (P_a - P_v) / RBF",
    description="Resistance to blood flow through the renal vasculature",
    compute_func=compute_rvr,
    parameters=[
        Parameter(
            name="P_a",
            description="Arterial pressure",
            units="mmHg",
            symbol="P_a",
            physiological_range=(80, 120)
        ),
        Parameter(
            name="P_v",
            description="Venous pressure",
            units="mmHg",
            symbol="P_v",
            physiological_range=(0, 10)
        ),
        Parameter(
            name="RBF",
            description="Renal blood flow",
            units="mL/min",
            symbol="RBF",
            physiological_range=(800, 1500)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.1"
    )
)

# Register equation
register_equation(renal_vascular_resistance)

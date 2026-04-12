"""
Net acid excretion (NAE) calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_net_acid_excretion(TA: float, NH4: float, HCO3_excreted: float) -> float:
    """
    Calculate net acid excretion.

    Args:
        TA: Titratable acid excretion (mEq/day)
        NH4: Ammonium excretion (mEq/day)
        HCO3_excreted: Bicarbonate excreted in urine (mEq/day)

    Returns:
        NAE: Net acid excretion (mEq/day), normally 50-100 mEq/day
    """
    return TA + NH4 - HCO3_excreted


# Create equation
net_acid_excretion = create_equation(
    id="renal.acid_base.net_acid_excretion",
    name="Net Acid Excretion",
    category=EquationCategory.RENAL,
    latex=r"NAE = TA + NH_4^+ - HCO_3^-_{excreted}",
    simplified="NAE = TA + NH4⁺ - HCO3⁻_excreted",
    description="Total acid excreted by kidney, matching daily metabolic acid production",
    compute_func=compute_net_acid_excretion,
    parameters=[
        Parameter(
            name="TA",
            description="Titratable acid (primarily phosphate buffer)",
            units="mEq/day",
            symbol="TA",
            physiological_range=(10, 50)
        ),
        Parameter(
            name="NH4",
            description="Ammonium excretion",
            units="mEq/day",
            symbol="NH_4^+",
            physiological_range=(20, 80)
        ),
        Parameter(
            name="HCO3_excreted",
            description="Bicarbonate excreted in urine",
            units="mEq/day",
            symbol="HCO_3^-_{excreted}",
            physiological_range=(0, 10)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.7"
    )
)

# Register equation
register_equation(net_acid_excretion)

"""
Urine-to-plasma osmolality ratio.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_urine_osm_ratio(U_osm: float, P_osm: float) -> float:
    """
    Calculate urine-to-plasma osmolality ratio.

    Args:
        U_osm: Urine osmolality (mOsm/kg)
        P_osm: Plasma osmolality (mOsm/kg)

    Returns:
        ratio: U/P osmolality ratio (0.2-4.0, dilute to concentrated)
    """
    return U_osm / P_osm


# Create equation
urine_osmolality_ratio = create_equation(
    id="renal.concentration.urine_osmolality_ratio",
    name="Urine-to-Plasma Osmolality Ratio",
    category=EquationCategory.RENAL,
    latex=r"\frac{U_{osm}}{P_{osm}}",
    simplified="U_osm / P_osm",
    description="Ratio indicating kidney's concentration/dilution capability; range 0.2 (maximally dilute) to 4.0 (maximally concentrated)",
    compute_func=compute_urine_osm_ratio,
    parameters=[
        Parameter(
            name="U_osm",
            description="Urine osmolality",
            units="mOsm/kg",
            symbol="U_{osm}",
            physiological_range=(50, 1200)
        ),
        Parameter(
            name="P_osm",
            description="Plasma osmolality",
            units="mOsm/kg",
            symbol="P_{osm}",
            physiological_range=(280, 300)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.6"
    )
)

# Register equation
register_equation(urine_osmolality_ratio)

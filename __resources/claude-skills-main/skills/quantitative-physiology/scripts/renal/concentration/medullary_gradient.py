"""
Medullary osmolality gradient calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_medullary_gradient(depth: float, osm_cortex: float = 300.0, osm_tip: float = 1200.0) -> float:
    """
    Calculate medullary osmolality at a given depth.

    Args:
        depth: Fractional depth into medulla (0 = cortex, 1 = papillary tip)
        osm_cortex: Cortical osmolality (mOsm/kg, default 300)
        osm_tip: Papillary tip osmolality (mOsm/kg, default 1200)

    Returns:
        osm: Osmolality at given depth (mOsm/kg)
    """
    return osm_cortex + (osm_tip - osm_cortex) * depth


# Create equation
medullary_gradient = create_equation(
    id="renal.concentration.medullary_gradient",
    name="Medullary Osmolality Gradient",
    category=EquationCategory.RENAL,
    latex=r"\pi(d) = \pi_{cortex} + (\pi_{tip} - \pi_{cortex}) \times d",
    simplified="π(d) = π_cortex + (π_tip - π_cortex) × d",
    description="Linear approximation of osmolality gradient from cortex to medullary tip",
    compute_func=compute_medullary_gradient,
    parameters=[
        Parameter(
            name="depth",
            description="Fractional depth into medulla",
            units="dimensionless",
            symbol="d",
            physiological_range=(0, 1)
        ),
        Parameter(
            name="osm_cortex",
            description="Cortical osmolality",
            units="mOsm/kg",
            symbol=r"\pi_{cortex}",
            default_value=300.0,
            physiological_range=(280, 310)
        ),
        Parameter(
            name="osm_tip",
            description="Papillary tip osmolality",
            units="mOsm/kg",
            symbol=r"\pi_{tip}",
            default_value=1200.0,
            physiological_range=(900, 1400)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.4"
    )
)

# Register equation
register_equation(medullary_gradient)

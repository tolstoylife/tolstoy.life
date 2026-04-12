"""
ADH-dependent water permeability in collecting duct.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_water_permeability(P_0: float, P_max: float, ADH: float, K_ADH: float) -> float:
    """
    Calculate ADH-dependent water permeability.

    Args:
        P_0: Baseline water permeability (without ADH)
        P_max: Maximum additional permeability from ADH
        ADH: ADH concentration
        K_ADH: Half-maximal ADH concentration

    Returns:
        P_water: Total water permeability
    """
    return P_0 + P_max * ADH / (K_ADH + ADH)


# Create equation
adh_water_permeability = create_equation(
    id="renal.concentration.adh_water_permeability",
    name="ADH-Dependent Water Permeability",
    category=EquationCategory.RENAL,
    latex=r"P_{water} = P_0 + \frac{P_{max} \times [ADH]}{K_{ADH} + [ADH]}",
    simplified="P_water = P_0 + P_max × [ADH] / (K_ADH + [ADH])",
    description="Collecting duct water permeability regulated by ADH through aquaporin-2 insertion",
    compute_func=compute_water_permeability,
    parameters=[
        Parameter(
            name="P_0",
            description="Baseline water permeability",
            units="cm/s",
            symbol="P_0",
            physiological_range=(1e-6, 1e-4)
        ),
        Parameter(
            name="P_max",
            description="Maximum ADH-stimulated permeability increase",
            units="cm/s",
            symbol="P_{max}",
            physiological_range=(1e-5, 1e-3)
        ),
        Parameter(
            name="ADH",
            description="ADH concentration",
            units="pg/mL",
            symbol="[ADH]",
            physiological_range=(0, 20)
        ),
        Parameter(
            name="K_ADH",
            description="Half-maximal ADH concentration",
            units="pg/mL",
            symbol="K_{ADH}",
            physiological_range=(1, 5)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.6"
    )
)

# Register equation
register_equation(adh_water_permeability)

"""
Free water clearance calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_free_water_clearance(V_dot: float, U_osm: float, P_osm: float) -> float:
    """
    Calculate free water clearance.

    Args:
        V_dot: Urine flow rate (mL/min)
        U_osm: Urine osmolality (mOsm/kg)
        P_osm: Plasma osmolality (mOsm/kg)

    Returns:
        C_H2O: Free water clearance (mL/min)
               > 0: dilute urine (water excess)
               < 0: concentrated urine (water deficit) = T^c_H2O
    """
    C_osm = (U_osm * V_dot) / P_osm
    return V_dot - C_osm


# Create equation
free_water_clearance = create_equation(
    id="renal.concentration.free_water_clearance",
    name="Free Water Clearance",
    category=EquationCategory.RENAL,
    latex=r"C_{H_2O} = \dot{V} - C_{osm} = \dot{V} - \frac{U_{osm} \times \dot{V}}{P_{osm}}",
    simplified="C_H2O = V̇ - C_osm = V̇ - (U_osm × V̇) / P_osm",
    description="Volume of solute-free water cleared per unit time; positive in dilute urine, negative in concentrated urine",
    compute_func=compute_free_water_clearance,
    parameters=[
        Parameter(
            name="V_dot",
            description="Urine flow rate",
            units="mL/min",
            symbol=r"\dot{V}",
            physiological_range=(0.5, 20)
        ),
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
    depends_on=["renal.clearance.clearance"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.6"
    )
)

# Register equation
register_equation(free_water_clearance)

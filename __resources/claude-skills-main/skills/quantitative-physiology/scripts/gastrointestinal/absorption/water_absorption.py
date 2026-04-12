"""Water absorption coupled to Na+ transport."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_water_absorption(Na_absorbed: float, osmotic_coeff: float = 260.0) -> float:
    """
    Calculate water absorption coupled to Na+ transport.

    Via SGLT1: ~260 H2O molecules per Na+ absorbed.

    Parameters
    ----------
    Na_absorbed : float
        Na+ absorbed (mmol/min)
    osmotic_coeff : float
        Water molecules per Na+ (dimensionless), default 260

    Returns
    -------
    float
        Water absorption (mmol H2O/min)
    """
    return Na_absorbed * osmotic_coeff


water_absorption = create_equation(
    id="gastrointestinal.absorption.water_absorption",
    name="Water Absorption (GI)",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"J_{H_2O} = J_{Na^+} \times n_{H_2O}",
    simplified="J_H2O = J_Na+ × n_H2O",
    description="Water absorption coupled to Na+ transport. Via SGLT1: ~260 H2O per Na+. Total GI absorption ~8.8 L/day (>98% of 9 L input)",
    compute_func=compute_water_absorption,
    parameters=[
        Parameter(
            name="Na_absorbed",
            description="Na+ absorbed",
            units="mmol/min",
            symbol=r"J_{Na^+}",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="osmotic_coeff",
            description="Water molecules per Na+",
            units="dimensionless",
            symbol=r"n_{H_2O}",
            default_value=260.0,
            physiological_range=(200.0, 300.0)
        )
    ],
    depends_on=["gastrointestinal.absorption.sglt1_glucose"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.4"
    )
)

register_equation(water_absorption)

"""Bohr Dead Space Equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_dead_space_bohr(P_aCO2: float, P_ECO2: float) -> float:
    """
    Calculate physiological dead space fraction (Bohr equation).

    V_D/V_T = (P_aCO2 - P_ECO2) / P_aCO2

    Parameters
    ----------
    P_aCO2 : float
        Arterial PCO2 (mmHg)
    P_ECO2 : float
        Mixed expired PCO2 (mmHg)

    Returns
    -------
    float
        Dead space fraction (dimensionless, 0-1)
    """
    return (P_aCO2 - P_ECO2) / P_aCO2


# Create equation
dead_space_bohr = create_equation(
    id="respiratory.vq_matching.dead_space_bohr",
    name="Bohr Dead Space Equation",
    category=EquationCategory.RESPIRATORY,
    latex=r"\frac{V_D}{V_T} = \frac{P_{aCO2} - P_{ECO2}}{P_{aCO2}}",
    simplified="V_D/V_T = (P_aCO2 - P_ECO2) / P_aCO2",
    description="Fraction of tidal volume that does not participate in gas exchange (V̇A/Q̇ = ∞)",
    compute_func=compute_dead_space_bohr,
    parameters=[
        Parameter(
            name="P_aCO2",
            description="Arterial PCO2",
            units="mmHg",
            symbol="P_{aCO2}",
            default_value=40.0,
            physiological_range=(20.0, 80.0)
        ),
        Parameter(
            name="P_ECO2",
            description="Mixed expired PCO2",
            units="mmHg",
            symbol="P_{ECO2}",
            default_value=28.0,
            physiological_range=(10.0, 40.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.4"
    )
)

# Register in global index
register_equation(dead_space_bohr)

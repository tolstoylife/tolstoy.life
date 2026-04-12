"""Iron absorption regulation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_iron_absorption_fraction(Fe_intake: float, stores_depleted: bool = False, hepcidin_level: float = 1.0) -> float:
    """
    Calculate fractional iron absorption.

    Fe3+ → Fe2+ (ferrireductase)
    DMT1 (apical) → ferroportin (basolateral)
    Regulated by hepcidin (blocks ferroportin)

    Parameters
    ----------
    Fe_intake : float
        Dietary iron intake (mg)
    stores_depleted : bool
        Whether iron stores are depleted, default False
    hepcidin_level : float
        Hepcidin level (relative, 1.0 = normal), default 1.0

    Returns
    -------
    float
        Fractional iron absorption (0-1)
    """
    if stores_depleted:
        base_fraction = 0.25
    else:
        base_fraction = 0.10

    return base_fraction / hepcidin_level


iron_absorption = create_equation(
    id="gastrointestinal.absorption.iron_absorption",
    name="Iron Absorption (GI)",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"f_{Fe} = \frac{f_{\text{base}}}{\text{hepcidin}}",
    simplified="f_Fe = f_base / hepcidin",
    description="Fractional Fe absorption. DMT1 (apical) → ferroportin (basolateral). ~1-2 mg/day absorbed (10-20% of intake). Regulated by hepcidin",
    compute_func=compute_iron_absorption_fraction,
    parameters=[
        Parameter(
            name="Fe_intake",
            description="Dietary iron intake",
            units="mg",
            symbol=r"\text{Fe}_{\text{intake}}",
            physiological_range=(5.0, 30.0)
        ),
        Parameter(
            name="stores_depleted",
            description="Iron stores depleted (increases absorption)",
            units="boolean",
            symbol=r"\text{depleted}",
            default_value=0.0
        ),
        Parameter(
            name="hepcidin_level",
            description="Hepcidin level (relative to normal)",
            units="dimensionless",
            symbol=r"\text{hepcidin}",
            default_value=1.0,
            physiological_range=(0.1, 10.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.4"
    )
)

register_equation(iron_absorption)

"""Anion Gap equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_anion_gap(Na: float, Cl: float, HCO3: float) -> float:
    """
    Calculate anion gap.

    AG = [Na⁺] - [Cl⁻] - [HCO3⁻]

    Parameters
    ----------
    Na : float
        Sodium concentration (mEq/L)
    Cl : float
        Chloride concentration (mEq/L)
    HCO3 : float
        Bicarbonate concentration (mEq/L)

    Returns
    -------
    float
        Anion gap (mEq/L)
    """
    return Na - Cl - HCO3


# Create equation
anion_gap = create_equation(
    id="respiratory.acid_base.anion_gap",
    name="Anion Gap",
    category=EquationCategory.RESPIRATORY,
    latex=r"AG = [Na^+] - [Cl^-] - [HCO_3^-]",
    simplified="AG = [Na⁺] - [Cl⁻] - [HCO3⁻]",
    description="Difference between measured cations and anions (normal: 8-12 mEq/L)",
    compute_func=compute_anion_gap,
    parameters=[
        Parameter(
            name="Na",
            description="Sodium concentration",
            units="mEq/L",
            symbol="[Na^+]",
            default_value=140.0,
            physiological_range=(135.0, 145.0)
        ),
        Parameter(
            name="Cl",
            description="Chloride concentration",
            units="mEq/L",
            symbol="[Cl^-]",
            default_value=104.0,
            physiological_range=(98.0, 108.0)
        ),
        Parameter(
            name="HCO3",
            description="Bicarbonate concentration",
            units="mEq/L",
            symbol="[HCO_3^-]",
            default_value=24.0,
            physiological_range=(22.0, 26.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.8"
    )
)

# Register in global index
register_equation(anion_gap)

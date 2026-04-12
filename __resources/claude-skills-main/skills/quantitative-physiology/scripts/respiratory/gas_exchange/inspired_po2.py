"""Inspired PO2 equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_inspired_po2(FiO2: float, P_B: float, P_H2O: float) -> float:
    """
    Calculate inspired PO2 (humidified air).

    P_iO2 = FiO2 × (P_B - P_H2O)

    Parameters
    ----------
    FiO2 : float
        Fraction of inspired oxygen (0-1)
    P_B : float
        Barometric pressure (mmHg)
    P_H2O : float
        Water vapor pressure (mmHg)

    Returns
    -------
    float
        Inspired PO2 (mmHg)
    """
    return FiO2 * (P_B - P_H2O)


# Create equation
inspired_po2 = create_equation(
    id="respiratory.gas_exchange.inspired_po2",
    name="Inspired PO2",
    category=EquationCategory.RESPIRATORY,
    latex=r"P_{iO2} = FiO_2 \times (P_B - P_{H_2O})",
    simplified="P_iO2 = FiO2 × (P_B - P_H2O)",
    description="Partial pressure of oxygen in humidified inspired air",
    compute_func=compute_inspired_po2,
    parameters=[
        Parameter(
            name="FiO2",
            description="Fraction of inspired oxygen",
            units="dimensionless",
            symbol="FiO_2",
            default_value=0.21,
            physiological_range=(0.21, 1.0)
        ),
        Parameter(
            name="P_B",
            description="Barometric pressure",
            units="mmHg",
            symbol="P_B",
            default_value=760.0,
            physiological_range=(200.0, 800.0)
        ),
        Parameter(
            name="P_H2O",
            description="Water vapor pressure at 37°C",
            units="mmHg",
            symbol="P_{H_2O}",
            default_value=47.0,
            physiological_range=(47.0, 47.0)
        )
    ],
    depends_on=["respiratory.gas_exchange.partial_pressure"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.3"
    )
)

# Register in global index
register_equation(inspired_po2)

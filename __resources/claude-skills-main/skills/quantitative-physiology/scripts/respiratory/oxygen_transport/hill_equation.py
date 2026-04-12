"""Hill Equation for O2-Hb Dissociation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_hill_equation(PO2: float, P50: float, n: float) -> float:
    """
    Calculate oxygen saturation using Hill equation.

    S_O2 = P_O2^n / (P_50^n + P_O2^n)

    Parameters
    ----------
    PO2 : float
        Partial pressure of oxygen (mmHg)
    P50 : float
        PO2 at 50% saturation (mmHg)
    n : float
        Hill coefficient (cooperativity)

    Returns
    -------
    float
        Oxygen saturation (0-1)
    """
    return PO2**n / (P50**n + PO2**n)


# Create equation
hill_equation = create_equation(
    id="respiratory.oxygen_transport.hill_equation",
    name="Hill Equation (O2-Hb Dissociation)",
    category=EquationCategory.RESPIRATORY,
    latex=r"S_{O2} = \frac{P_{O2}^n}{P_{50}^n + P_{O2}^n}",
    simplified="S_O2 = P_O2^n / (P_50^n + P_O2^n)",
    description="Oxygen-hemoglobin dissociation curve with cooperative binding",
    compute_func=compute_hill_equation,
    parameters=[
        Parameter(
            name="PO2",
            description="Partial pressure of oxygen",
            units="mmHg",
            symbol="P_{O2}",
            physiological_range=(0.0, 150.0)
        ),
        Parameter(
            name="P50",
            description="PO2 at 50% saturation",
            units="mmHg",
            symbol="P_{50}",
            default_value=26.6,
            physiological_range=(20.0, 35.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient",
            units="dimensionless",
            symbol="n",
            default_value=2.7,
            physiological_range=(2.0, 3.5)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.5"
    )
)

# Register in global index
register_equation(hill_equation)

"""Hill equation for hemoglobin oxygen saturation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_hill_saturation(P_O2: float, P_50: float = 26.0, n: float = 2.7) -> float:
    """
    Calculate hemoglobin oxygen saturation using Hill equation.

    Parameters
    ----------
    P_O2 : float
        Partial pressure of oxygen (mmHg)
    P_50 : float, optional
        Half-saturation pressure (mmHg, default: 26)
    n : float, optional
        Hill coefficient (default: 2.7)

    Returns
    -------
    float
        Oxygen saturation (0-1)
    """
    return (P_O2 ** n) / (P_50 ** n + P_O2 ** n)


hill_saturation = create_equation(
    id="cardiovascular.blood.hill_saturation",
    name="Hill Equation for Hemoglobin",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"S_{O_2} = \frac{P_{O_2}^n}{P_{50}^n + P_{O_2}^n}",
    simplified="S_O2 = P_O2^n / (P_50^n + P_O2^n)",
    description="Sigmoid oxygen-hemoglobin dissociation curve",
    compute_func=compute_hill_saturation,
    parameters=[
        Parameter(
            name="P_O2",
            description="Partial pressure of oxygen",
            units="mmHg",
            symbol="P_{O_2}",
            physiological_range=(0.0, 150.0)
        ),
        Parameter(
            name="P_50",
            description="Half-saturation pressure",
            units="mmHg",
            symbol="P_{50}",
            default_value=26.0,
            physiological_range=(20.0, 30.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient (cooperativity)",
            units="dimensionless",
            symbol="n",
            default_value=2.7,
            physiological_range=(2.0, 3.5)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.1"
    )
)

register_equation(hill_saturation)

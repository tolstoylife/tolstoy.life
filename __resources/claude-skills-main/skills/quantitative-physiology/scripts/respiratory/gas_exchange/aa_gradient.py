"""Alveolar-arterial O2 Gradient equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_aa_gradient(P_AO2: float, P_aO2: float) -> float:
    """
    Calculate alveolar-arterial oxygen gradient.

    A-a gradient = P_AO2 - P_aO2

    Parameters
    ----------
    P_AO2 : float
        Alveolar PO2 (mmHg)
    P_aO2 : float
        Arterial PO2 (mmHg)

    Returns
    -------
    float
        A-a gradient (mmHg)
    """
    return P_AO2 - P_aO2


# Create equation
aa_gradient = create_equation(
    id="respiratory.gas_exchange.aa_gradient",
    name="Alveolar-Arterial O2 Gradient",
    category=EquationCategory.RESPIRATORY,
    latex=r"A-a \text{ gradient} = P_{AO2} - P_{aO2}",
    simplified="A-a gradient = P_AO2 - P_aO2",
    description="Difference between alveolar and arterial PO2, indicates gas exchange efficiency",
    compute_func=compute_aa_gradient,
    parameters=[
        Parameter(
            name="P_AO2",
            description="Alveolar PO2",
            units="mmHg",
            symbol="P_{AO2}",
            default_value=100.0,
            physiological_range=(50.0, 150.0)
        ),
        Parameter(
            name="P_aO2",
            description="Arterial PO2",
            units="mmHg",
            symbol="P_{aO2}",
            default_value=95.0,
            physiological_range=(40.0, 100.0)
        )
    ],
    depends_on=["respiratory.gas_exchange.alveolar_gas_equation"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.3"
    )
)

# Register in global index
register_equation(aa_gradient)

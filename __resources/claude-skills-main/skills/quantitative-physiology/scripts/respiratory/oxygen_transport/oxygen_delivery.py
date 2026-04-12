"""Oxygen Delivery equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_oxygen_delivery(Q: float, CaO2: float) -> float:
    """
    Calculate oxygen delivery to tissues.

    D_O2 = Q̇ × C_aO2 × 10

    Parameters
    ----------
    Q : float
        Cardiac output (L/min)
    CaO2 : float
        Arterial O2 content (mL O2/dL)

    Returns
    -------
    float
        Oxygen delivery (mL O2/min)
    """
    return Q * CaO2 * 10.0


# Create equation
oxygen_delivery = create_equation(
    id="respiratory.oxygen_transport.oxygen_delivery",
    name="Tissue Oxygen Delivery (Respiratory)",
    category=EquationCategory.RESPIRATORY,
    latex=r"D_{O2} = \dot{Q} \times C_{aO2} \times 10",
    simplified="D_O2 = Q̇ × C_aO2 × 10",
    description="Total oxygen delivery to tissues per minute",
    compute_func=compute_oxygen_delivery,
    parameters=[
        Parameter(
            name="Q",
            description="Cardiac output",
            units="L/min",
            symbol=r"\dot{Q}",
            default_value=5.0,
            physiological_range=(3.0, 25.0)
        ),
        Parameter(
            name="CaO2",
            description="Arterial O2 content",
            units="mL O2/dL",
            symbol="C_{aO2}",
            default_value=20.0,
            physiological_range=(10.0, 23.0)
        )
    ],
    depends_on=["respiratory.oxygen_transport.oxygen_content"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.5"
    )
)

# Register in global index
register_equation(oxygen_delivery)

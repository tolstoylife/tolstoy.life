"""Oxygen delivery rate equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_oxygen_delivery(CO: float, Hb: float, S_O2: float) -> float:
    """
    Calculate systemic oxygen delivery rate.

    Parameters
    ----------
    CO : float
        Cardiac output (L/min)
    Hb : float
        Hemoglobin concentration (g/dL)
    S_O2 : float
        Arterial oxygen saturation (0-1)

    Returns
    -------
    float
        Oxygen delivery (mL O2/min)
    """
    HUFNER_CONSTANT = 1.34  # mL O2/g Hb

    # CO in L/min, Hb in g/dL → multiply by 10 to get mL/min
    return CO * HUFNER_CONSTANT * Hb * S_O2 * 10


oxygen_delivery = create_equation(
    id="cardiovascular.blood.systemic_oxygen_delivery",
    name="Systemic Oxygen Delivery (Cardiovascular)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"DO_2 = CO \times 1.34 \times \text{Hb} \times S_{O_2}",
    simplified="DO2 = CO × 1.34 × Hb × S_O2",
    description="Systemic oxygen delivery rate, product of cardiac output and arterial oxygen content",
    compute_func=compute_oxygen_delivery,
    parameters=[
        Parameter(
            name="CO",
            description="Cardiac output",
            units="L/min",
            symbol="CO",
            physiological_range=(4.0, 8.0)
        ),
        Parameter(
            name="Hb",
            description="Hemoglobin concentration",
            units="g/dL",
            symbol=r"\text{Hb}",
            physiological_range=(12.0, 18.0)
        ),
        Parameter(
            name="S_O2",
            description="Arterial oxygen saturation",
            units="dimensionless",
            symbol="S_{O_2}",
            physiological_range=(0.95, 1.0)
        )
    ],
    depends_on=["cardiovascular.blood.blood_oxygen_content"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.1"
    )
)

register_equation(oxygen_delivery)

"""Blood oxygen content equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_oxygen_content(Hb: float, S_O2: float, P_O2: float) -> float:
    """
    Calculate total oxygen content in blood.

    Parameters
    ----------
    Hb : float
        Hemoglobin concentration (g/dL)
    S_O2 : float
        Oxygen saturation (0-1)
    P_O2 : float
        Partial pressure of oxygen (mmHg)

    Returns
    -------
    float
        Oxygen content (mL O2/dL blood)
    """
    HUFNER_CONSTANT = 1.34  # mL O2/g Hb
    SOLUBILITY = 0.003  # mL O2/(dL·mmHg)

    bound = HUFNER_CONSTANT * Hb * S_O2
    dissolved = SOLUBILITY * P_O2

    return bound + dissolved


oxygen_content = create_equation(
    id="cardiovascular.blood.blood_oxygen_content",
    name="Blood Oxygen Content (Cardiovascular)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"C_{O_2} = (1.34 \times \text{Hb} \times S_{O_2}) + (0.003 \times P_{O_2})",
    simplified="C_O2 = (1.34 × Hb × S_O2) + (0.003 × P_O2)",
    description="Total oxygen content in blood: bound to hemoglobin plus dissolved",
    compute_func=compute_oxygen_content,
    parameters=[
        Parameter(
            name="Hb",
            description="Hemoglobin concentration",
            units="g/dL",
            symbol=r"\text{Hb}",
            physiological_range=(12.0, 18.0)
        ),
        Parameter(
            name="S_O2",
            description="Oxygen saturation",
            units="dimensionless",
            symbol="S_{O_2}",
            physiological_range=(0.7, 1.0)
        ),
        Parameter(
            name="P_O2",
            description="Partial pressure of oxygen",
            units="mmHg",
            symbol="P_{O_2}",
            physiological_range=(35.0, 100.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.1"
    )
)

register_equation(oxygen_content)

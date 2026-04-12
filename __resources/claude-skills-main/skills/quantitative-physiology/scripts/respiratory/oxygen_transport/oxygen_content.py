"""Oxygen Content equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_oxygen_content(Hb: float, SO2: float, PO2: float) -> float:
    """
    Calculate total oxygen content in blood.

    C_O2 = (1.34 × [Hb] × S_O2) + (0.003 × P_O2)

    Parameters
    ----------
    Hb : float
        Hemoglobin concentration (g/dL)
    SO2 : float
        Oxygen saturation (0-1)
    PO2 : float
        Partial pressure of oxygen (mmHg)

    Returns
    -------
    float
        Total O2 content (mL O2/dL)
    """
    return (1.34 * Hb * SO2) + (0.003 * PO2)


# Create equation
oxygen_content = create_equation(
    id="respiratory.oxygen_transport.oxygen_content",
    name="Oxygen Content (Respiratory)",
    category=EquationCategory.RESPIRATORY,
    latex=r"C_{O2} = (1.34 \times [Hb] \times S_{O2}) + (0.003 \times P_{O2})",
    simplified="C_O2 = (1.34 × [Hb] × S_O2) + (0.003 × P_O2)",
    description="Total oxygen content: bound to hemoglobin plus dissolved",
    compute_func=compute_oxygen_content,
    parameters=[
        Parameter(
            name="Hb",
            description="Hemoglobin concentration",
            units="g/dL",
            symbol="[Hb]",
            default_value=15.0,
            physiological_range=(10.0, 18.0)
        ),
        Parameter(
            name="SO2",
            description="Oxygen saturation",
            units="dimensionless",
            symbol="S_{O2}",
            default_value=0.97,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="PO2",
            description="Partial pressure of oxygen",
            units="mmHg",
            symbol="P_{O2}",
            default_value=100.0,
            physiological_range=(20.0, 600.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.5"
    )
)

# Register in global index
register_equation(oxygen_content)

"""Oxygen Extraction Ratio equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_oxygen_extraction_ratio(CaO2: float, CvO2: float) -> float:
    """
    Calculate oxygen extraction ratio.

    O2ER = (C_aO2 - C_vO2) / C_aO2

    Parameters
    ----------
    CaO2 : float
        Arterial O2 content (mL O2/dL)
    CvO2 : float
        Venous O2 content (mL O2/dL)

    Returns
    -------
    float
        O2 extraction ratio (dimensionless, 0-1)
    """
    return (CaO2 - CvO2) / CaO2


# Create equation
oxygen_extraction_ratio = create_equation(
    id="respiratory.oxygen_transport.oxygen_extraction_ratio",
    name="Oxygen Extraction Ratio",
    category=EquationCategory.RESPIRATORY,
    latex=r"O_2ER = \frac{C_{aO2} - C_{vO2}}{C_{aO2}}",
    simplified="O2ER = (C_aO2 - C_vO2) / C_aO2",
    description="Fraction of delivered oxygen extracted by tissues",
    compute_func=compute_oxygen_extraction_ratio,
    parameters=[
        Parameter(
            name="CaO2",
            description="Arterial O2 content",
            units="mL O2/dL",
            symbol="C_{aO2}",
            default_value=20.0,
            physiological_range=(10.0, 23.0)
        ),
        Parameter(
            name="CvO2",
            description="Venous O2 content",
            units="mL O2/dL",
            symbol="C_{vO2}",
            default_value=15.0,
            physiological_range=(8.0, 18.0)
        )
    ],
    depends_on=["respiratory.oxygen_transport.oxygen_content"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.5"
    )
)

# Register in global index
register_equation(oxygen_extraction_ratio)

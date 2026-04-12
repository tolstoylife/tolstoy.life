"""First-pass effect and bioavailability."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_first_pass_bioavailability(E: float) -> float:
    """
    Calculate bioavailability after hepatic first-pass metabolism.

    Bioavailability = 1 - E

    High extraction (E close to 1) → low bioavailability
    Low extraction (E close to 0) → high bioavailability

    Parameters
    ----------
    E : float
        Hepatic extraction ratio (0-1)

    Returns
    -------
    float
        Bioavailability (0-1)
    """
    return 1.0 - E


first_pass_effect = create_equation(
    id="gastrointestinal.liver.first_pass_effect",
    name="First-Pass Effect",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"F = 1 - E",
    simplified="F = 1 - E",
    description="Bioavailability after hepatic first-pass metabolism. High E → low F (extensive first-pass)",
    compute_func=compute_first_pass_bioavailability,
    parameters=[
        Parameter(
            name="E",
            description="Hepatic extraction ratio",
            units="dimensionless",
            symbol="E",
            physiological_range=(0.0, 1.0)
        )
    ],
    depends_on=["gastrointestinal.liver.extraction_ratio"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.6"
    )
)

register_equation(first_pass_effect)

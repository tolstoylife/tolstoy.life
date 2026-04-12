"""
Albumin-corrected total calcium.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_corrected_calcium(measured_Ca: float, albumin: float) -> float:
    """
    Calculate albumin-corrected total calcium.

    Parameters
    ----------
    measured_Ca : float
        Measured total calcium (mg/dL)
    albumin : float
        Serum albumin (g/dL)

    Returns
    -------
    float
        Corrected calcium (mg/dL)

    Notes
    -----
    Plasma calcium distribution:
    - 45% ionized (free) - physiologically active
    - 40% protein-bound (mostly albumin)
    - 15% complexed (citrate, phosphate)

    Normal total Ca: 9-10.5 mg/dL
    Normal ionized Ca: 4.5-5.3 mg/dL (1.1-1.3 mM)
    Normal albumin: 3.5-5.0 g/dL

    Correction accounts for hypo/hyperalbuminemia affecting total Ca measurement
    while ionized Ca remains normal.
    """
    return measured_Ca + 0.8 * (4.0 - albumin)


# Create equation
corrected_calcium_equation = create_equation(
    id="endocrine.calcium.albumin_correction",
    name="Albumin-Corrected Calcium",
    category=EquationCategory.ENDOCRINE,
    latex=r"\text{Corrected Ca} = \text{Measured Ca} + 0.8 \times (4 - [\text{Albumin}])",
    simplified="Corrected_Ca = Measured_Ca + 0.8 × (4 - Albumin)",
    description="Corrects total calcium for albumin concentration. Accounts for protein-binding "
                "effects when albumin is abnormal while ionized Ca is normal.",
    compute_func=compute_corrected_calcium,
    parameters=[
        Parameter(
            name="measured_Ca",
            description="Measured total calcium",
            units="mg/dL",
            symbol="Ca_{measured}",
            physiological_range=(5.0, 15.0)
        ),
        Parameter(
            name="albumin",
            description="Serum albumin concentration",
            units="g/dL",
            symbol="Albumin",
            physiological_range=(2.0, 6.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.7"
    )
)

# Register globally
register_equation(corrected_calcium_equation)

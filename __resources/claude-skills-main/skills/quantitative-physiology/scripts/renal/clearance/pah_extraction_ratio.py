"""
PAH extraction ratio and true RPF calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_extraction_ratio(P_a: float, P_v: float) -> float:
    """
    Calculate extraction ratio for PAH.

    Args:
        P_a: Arterial plasma PAH concentration
        P_v: Venous plasma PAH concentration

    Returns:
        E: Extraction ratio (dimensionless, ~0.9 for PAH)
    """
    return (P_a - P_v) / P_a


def compute_true_rpf(C_PAH: float, E_PAH: float) -> float:
    """
    Calculate true RPF from PAH clearance and extraction ratio.

    Args:
        C_PAH: PAH clearance (mL/min)
        E_PAH: PAH extraction ratio (dimensionless)

    Returns:
        RPF: True renal plasma flow (mL/min)
    """
    return C_PAH / E_PAH


# Create extraction ratio equation
pah_extraction_ratio = create_equation(
    id="renal.clearance.pah_extraction_ratio",
    name="PAH Extraction Ratio",
    category=EquationCategory.RENAL,
    latex=r"E_{PAH} = \frac{P_a - P_v}{P_a}",
    simplified="E_PAH = (P_a - P_v) / P_a",
    description="Fraction of PAH removed from arterial blood in single pass through kidney",
    compute_func=compute_extraction_ratio,
    parameters=[
        Parameter(
            name="P_a",
            description="Arterial plasma PAH concentration",
            units="mg/dL",
            symbol="P_a",
            physiological_range=(0, 10)
        ),
        Parameter(
            name="P_v",
            description="Venous plasma PAH concentration",
            units="mg/dL",
            symbol="P_v",
            physiological_range=(0, 2)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Create true RPF equation
true_rpf_from_pah = create_equation(
    id="renal.clearance.true_rpf_from_pah",
    name="True RPF from PAH",
    category=EquationCategory.RENAL,
    latex=r"RPF = \frac{C_{PAH}}{E_{PAH}}",
    simplified="RPF = C_PAH / E_PAH",
    description="Calculate true renal plasma flow correcting for incomplete PAH extraction",
    compute_func=compute_true_rpf,
    parameters=[
        Parameter(
            name="C_PAH",
            description="PAH clearance",
            units="mL/min",
            symbol="C_{PAH}",
            physiological_range=(500, 800)
        ),
        Parameter(
            name="E_PAH",
            description="PAH extraction ratio",
            units="dimensionless",
            symbol="E_{PAH}",
            default_value=0.9,
            physiological_range=(0.85, 0.95)
        )
    ],
    depends_on=["renal.clearance.pah_extraction_ratio", "renal.clearance.clearance"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Register equations
register_equation(pah_extraction_ratio)
register_equation(true_rpf_from_pah)

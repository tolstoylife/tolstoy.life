"""Hepatic extraction ratio."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_extraction_ratio(C_in: float, C_out: float) -> float:
    """
    Calculate hepatic extraction ratio.

    E = (C_in - C_out) / C_in

    High extraction (E > 0.7): flow-limited clearance
    Low extraction (E < 0.3): capacity-limited clearance

    Parameters
    ----------
    C_in : float
        Inlet concentration (any units)
    C_out : float
        Outlet concentration (same units as C_in)

    Returns
    -------
    float
        Extraction ratio (0-1)
    """
    if C_in > 0:
        return (C_in - C_out) / C_in
    else:
        return 0.0


extraction_ratio = create_equation(
    id="gastrointestinal.liver.extraction_ratio",
    name="Hepatic Extraction Ratio",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"E = \frac{C_{\text{in}} - C_{\text{out}}}{C_{\text{in}}}",
    simplified="E = (C_in - C_out) / C_in",
    description="Hepatic extraction ratio. High E (>0.7): flow-limited. Low E (<0.3): capacity-limited",
    compute_func=compute_extraction_ratio,
    parameters=[
        Parameter(
            name="C_in",
            description="Inlet concentration",
            units="variable",
            symbol=r"C_{\text{in}}",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="C_out",
            description="Outlet concentration",
            units="variable",
            symbol=r"C_{\text{out}}",
            physiological_range=(0.0, 1000.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.6"
    )
)

register_equation(extraction_ratio)

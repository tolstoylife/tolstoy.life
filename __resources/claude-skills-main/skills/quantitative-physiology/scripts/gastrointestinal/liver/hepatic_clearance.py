"""Hepatic clearance."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_hepatic_clearance(Q_H: float, E: float) -> float:
    """
    Calculate hepatic clearance.

    CL_H = Q_H × E

    For high-extraction drugs: CL_H ≈ Q_H (flow-limited)
    For low-extraction drugs: CL_H << Q_H (capacity-limited)

    Parameters
    ----------
    Q_H : float
        Hepatic blood flow (L/min)
    E : float
        Extraction ratio (0-1)

    Returns
    -------
    float
        Hepatic clearance (L/min)
    """
    return Q_H * E


hepatic_clearance = create_equation(
    id="gastrointestinal.liver.hepatic_clearance",
    name="Hepatic Clearance",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"CL_H = Q_H \times E",
    simplified="CL_H = Q_H × E",
    description="Hepatic clearance. For high E drugs: CL_H ≈ Q_H (flow-limited)",
    compute_func=compute_hepatic_clearance,
    parameters=[
        Parameter(
            name="Q_H",
            description="Hepatic blood flow",
            units="L/min",
            symbol=r"Q_H",
            physiological_range=(1.0, 2.0)
        ),
        Parameter(
            name="E",
            description="Extraction ratio",
            units="dimensionless",
            symbol="E",
            physiological_range=(0.0, 1.0)
        )
    ],
    depends_on=["gastrointestinal.liver.hepatic_blood_flow", "gastrointestinal.liver.extraction_ratio"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.6"
    )
)

register_equation(hepatic_clearance)

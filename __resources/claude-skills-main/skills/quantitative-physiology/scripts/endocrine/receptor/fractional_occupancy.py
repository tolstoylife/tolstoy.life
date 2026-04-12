"""
Fractional receptor occupancy.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_fractional_occupancy(H: float, Kd: float) -> float:
    """
    Calculate fractional receptor occupancy.

    Parameters
    ----------
    H : float
        Free hormone concentration (M)
    Kd : float
        Dissociation constant (M)

    Returns
    -------
    float
        Fractional occupancy θ (0-1, dimensionless)

    Notes
    -----
    Many hormone systems achieve maximal response at <10% receptor occupancy
    due to spare receptors and signal amplification.
    EC50 (half-maximal effect) often < K_d.
    """
    return H / (Kd + H)


# Create equation
fractional_occupancy_equation = create_equation(
    id="endocrine.receptor.fractional_occupancy",
    name="Receptor Fractional Occupancy",
    category=EquationCategory.ENDOCRINE,
    latex=r"\theta = \frac{[H]}{K_d + [H]}",
    simplified="θ = [H] / (K_d + [H])",
    description="Fraction of receptors occupied by hormone (0-1). "
                "Due to signal amplification, maximal response often occurs at <10% occupancy.",
    compute_func=compute_fractional_occupancy,
    parameters=[
        Parameter(
            name="H",
            description="Free hormone concentration",
            units="M",
            symbol="[H]",
            physiological_range=(1e-12, 1e-6)
        ),
        Parameter(
            name="Kd",
            description="Dissociation constant",
            units="M",
            symbol="K_d",
            physiological_range=(1e-12, 1e-6)
        )
    ],
    depends_on=["endocrine.kinetics.dissociation_constant"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.2"
    )
)

# Register globally
register_equation(fractional_occupancy_equation)

"""
Hormone-protein binding equilibrium dissociation constant.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_kd(H_free: float, P_free: float, HP_bound: float) -> float:
    """
    Calculate dissociation constant from equilibrium concentrations.

    Parameters
    ----------
    H_free : float
        Free hormone concentration (M)
    P_free : float
        Free binding protein concentration (M)
    HP_bound : float
        Hormone-protein complex concentration (M)

    Returns
    -------
    float
        Dissociation constant K_d (M)
    """
    return (H_free * P_free) / HP_bound


# Create equation
kd_equation = create_equation(
    id="endocrine.kinetics.dissociation_constant",
    name="Hormone-Protein Dissociation Constant",
    category=EquationCategory.ENDOCRINE,
    latex=r"K_d = \frac{[H][P]}{[HP]}",
    simplified="K_d = [H][P]/[HP]",
    description="Equilibrium dissociation constant for hormone-binding protein interaction. "
                "Lower K_d indicates higher affinity binding.",
    compute_func=compute_kd,
    parameters=[
        Parameter(
            name="H_free",
            description="Free hormone concentration",
            units="M",
            symbol="[H]",
            physiological_range=(1e-12, 1e-6)
        ),
        Parameter(
            name="P_free",
            description="Free binding protein concentration",
            units="M",
            symbol="[P]",
            physiological_range=(1e-9, 1e-3)
        ),
        Parameter(
            name="HP_bound",
            description="Hormone-protein complex concentration",
            units="M",
            symbol="[HP]",
            physiological_range=(1e-12, 1e-6)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.1"
    )
)

# Register globally
register_equation(kd_equation)

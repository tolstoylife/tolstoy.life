"""
Receptor saturation binding (Langmuir isotherm).

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_saturation_binding(H: float, Bmax: float, Kd: float) -> float:
    """
    Calculate bound hormone at equilibrium (saturation binding).

    Parameters
    ----------
    H : float
        Free hormone concentration (M)
    Bmax : float
        Maximum binding capacity (M)
    Kd : float
        Dissociation constant (M)

    Returns
    -------
    float
        Bound hormone concentration (M)

    Notes
    -----
    This is the Langmuir isotherm for receptor binding.
    At [H] = K_d, binding is 50% of maximum.
    """
    return Bmax * H / (Kd + H)


# Create equation
saturation_binding_equation = create_equation(
    id="endocrine.receptor.saturation_binding",
    name="Receptor Saturation Binding",
    category=EquationCategory.ENDOCRINE,
    latex=r"B = \frac{B_{max} \times [H]}{K_d + [H]}",
    simplified="B = B_max × [H] / (K_d + [H])",
    description="Equilibrium receptor binding following Langmuir isotherm. "
                "B_max is maximum binding capacity, K_d is concentration at 50% saturation.",
    compute_func=compute_saturation_binding,
    parameters=[
        Parameter(
            name="H",
            description="Free hormone concentration",
            units="M",
            symbol="[H]",
            physiological_range=(1e-12, 1e-6)
        ),
        Parameter(
            name="Bmax",
            description="Maximum binding capacity",
            units="M",
            symbol="B_{max}",
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
register_equation(saturation_binding_equation)

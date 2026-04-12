"""
Fraction of hormone that is free (unbound) from binding proteins.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_fraction_free(P_conc: float, Kd: float) -> float:
    """
    Calculate fraction of hormone that is free (biologically active).

    Parameters
    ----------
    P_conc : float
        Binding protein concentration (M)
    Kd : float
        Dissociation constant (M)

    Returns
    -------
    float
        Fraction free (0-1, dimensionless)

    Notes
    -----
    Free hormone hypothesis: only free (unbound) hormone is biologically active.
    Examples:
    - Cortisol: 90-95% bound (5-10% free)
    - T4: 99.97% bound (0.03% free)
    """
    return 1.0 / (1.0 + P_conc / Kd)


# Create equation
fraction_free_equation = create_equation(
    id="endocrine.kinetics.fraction_free",
    name="Free Hormone Fraction",
    category=EquationCategory.ENDOCRINE,
    latex=r"f_{free} = \frac{1}{1 + \frac{[P]}{K_d}}",
    simplified="f_free = 1/(1 + [P]/K_d)",
    description="Fraction of hormone that is free (unbound) and biologically active. "
                "Depends on binding protein concentration and affinity (K_d).",
    compute_func=compute_fraction_free,
    parameters=[
        Parameter(
            name="P_conc",
            description="Binding protein concentration",
            units="M",
            symbol="[P]",
            physiological_range=(1e-9, 1e-3)
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
        source_chapter="9.1"
    )
)

# Register globally
register_equation(fraction_free_equation)

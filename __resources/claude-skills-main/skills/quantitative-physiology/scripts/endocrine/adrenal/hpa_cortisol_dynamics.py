"""
Cortisol dynamics in HPA axis.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_cortisol_derivative(ACTH: float, cortisol: float,
                                k_ACTH: float, k_clear: float) -> float:
    """
    Calculate rate of change of cortisol concentration.

    Parameters
    ----------
    ACTH : float
        ACTH concentration (stimulation)
    cortisol : float
        Cortisol concentration
    k_ACTH : float
        ACTH stimulation constant
    k_clear : float
        Cortisol clearance rate constant

    Returns
    -------
    float
        d[Cortisol]/dt

    Notes
    -----
    Daily cortisol production: 10-20 mg/day
    Stress response can increase 10-fold
    Half-life: 60-90 minutes
    """
    return k_ACTH * ACTH - k_clear * cortisol


# Create equation
cortisol_dynamics_equation = create_equation(
    id="endocrine.adrenal.hpa_cortisol_dynamics",
    name="HPA Axis Cortisol Dynamics",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{d[Cortisol]}{dt} = k_{ACTH} \times [ACTH] - k_{clear} \times [Cortisol]",
    simplified="d[Cortisol]/dt = k_ACTH × [ACTH] - k_clear × [Cortisol]",
    description="Cortisol secretion from adrenal cortex. Stimulated by ACTH, "
                "cleared by hepatic metabolism. Half-life ~60-90 minutes.",
    compute_func=compute_cortisol_derivative,
    parameters=[
        Parameter(
            name="ACTH",
            description="ACTH concentration",
            units="pg/mL",
            symbol="[ACTH]",
            physiological_range=(0.0, 200.0)
        ),
        Parameter(
            name="cortisol",
            description="Cortisol concentration",
            units="μg/dL",
            symbol="[Cortisol]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="k_ACTH",
            description="ACTH stimulation constant",
            units="1/time",
            symbol="k_{ACTH}",
            physiological_range=(0.01, 1.0)
        ),
        Parameter(
            name="k_clear",
            description="Cortisol clearance rate",
            units="1/time",
            symbol="k_{clear}",
            physiological_range=(0.01, 0.5)
        )
    ],
    depends_on=["endocrine.adrenal.hpa_acth_dynamics"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.5"
    )
)

# Register globally
register_equation(cortisol_dynamics_equation)

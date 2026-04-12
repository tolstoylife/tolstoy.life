"""
CRH dynamics in HPA axis with stress and cortisol feedback.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_crh_derivative(CRH: float, cortisol: float, k_stress: float,
                           k_cort: float, k_deg: float) -> float:
    """
    Calculate rate of change of CRH concentration.

    Parameters
    ----------
    CRH : float
        CRH concentration
    cortisol : float
        Cortisol concentration (feedback)
    k_stress : float
        Stress-induced secretion rate
    k_cort : float
        Cortisol feedback inhibition constant
    k_deg : float
        CRH degradation rate constant

    Returns
    -------
    float
        d[CRH]/dt
    """
    return k_stress - k_cort * cortisol - k_deg * CRH


# Create equation
crh_dynamics_equation = create_equation(
    id="endocrine.adrenal.hpa_crh_dynamics",
    name="HPA Axis CRH Dynamics",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{d[CRH]}{dt} = k_{stress} - k_{cort} \times [Cortisol] - k_{deg} \times [CRH]",
    simplified="d[CRH]/dt = k_stress - k_cort × [Cortisol] - k_deg × [CRH]",
    description="CRH (corticotropin-releasing hormone) dynamics in hypothalamus. "
                "Stimulated by stress, inhibited by cortisol negative feedback.",
    compute_func=compute_crh_derivative,
    parameters=[
        Parameter(
            name="CRH",
            description="CRH concentration",
            units="arbitrary units",
            symbol="[CRH]",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="cortisol",
            description="Cortisol concentration",
            units="μg/dL",
            symbol="[Cortisol]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="k_stress",
            description="Stress-induced secretion rate",
            units="concentration/time",
            symbol="k_{stress}",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="k_cort",
            description="Cortisol feedback constant",
            units="1/time",
            symbol="k_{cort}",
            physiological_range=(0.01, 1.0)
        ),
        Parameter(
            name="k_deg",
            description="CRH degradation rate",
            units="1/time",
            symbol="k_{deg}",
            physiological_range=(0.1, 2.0)
        )
    ],
    depends_on=["endocrine.feedback.negative_feedback_tropic"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.5"
    )
)

# Register globally
register_equation(crh_dynamics_equation)

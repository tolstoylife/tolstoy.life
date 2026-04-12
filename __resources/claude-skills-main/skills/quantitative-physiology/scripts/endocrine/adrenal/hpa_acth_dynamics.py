"""
ACTH dynamics in HPA axis.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_acth_derivative(CRH: float, ACTH: float, cortisol: float,
                            k_CRH: float, k_fb: float, k_deg: float) -> float:
    """
    Calculate rate of change of ACTH concentration.

    Parameters
    ----------
    CRH : float
        CRH concentration (stimulation)
    ACTH : float
        ACTH concentration
    cortisol : float
        Cortisol concentration (feedback)
    k_CRH : float
        CRH stimulation constant
    k_fb : float
        Cortisol feedback constant
    k_deg : float
        ACTH degradation rate constant

    Returns
    -------
    float
        d[ACTH]/dt
    """
    return k_CRH * CRH - k_fb * cortisol - k_deg * ACTH


# Create equation
acth_dynamics_equation = create_equation(
    id="endocrine.adrenal.hpa_acth_dynamics",
    name="HPA Axis ACTH Dynamics",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{d[ACTH]}{dt} = k_{CRH} \times [CRH] - k_{fb} \times [Cortisol] - k_{deg} \times [ACTH]",
    simplified="d[ACTH]/dt = k_CRH × [CRH] - k_fb × [Cortisol] - k_deg × [ACTH]",
    description="ACTH (adrenocorticotropic hormone) dynamics in anterior pituitary. "
                "Stimulated by CRH, inhibited by cortisol.",
    compute_func=compute_acth_derivative,
    parameters=[
        Parameter(
            name="CRH",
            description="CRH concentration",
            units="arbitrary units",
            symbol="[CRH]",
            physiological_range=(0.0, 10.0)
        ),
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
            name="k_CRH",
            description="CRH stimulation constant",
            units="1/time",
            symbol="k_{CRH}",
            physiological_range=(0.1, 5.0)
        ),
        Parameter(
            name="k_fb",
            description="Cortisol feedback constant",
            units="1/time",
            symbol="k_{fb}",
            physiological_range=(0.01, 1.0)
        ),
        Parameter(
            name="k_deg",
            description="ACTH degradation rate",
            units="1/time",
            symbol="k_{deg}",
            physiological_range=(0.1, 2.0)
        )
    ],
    depends_on=["endocrine.adrenal.hpa_crh_dynamics"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.5"
    )
)

# Register globally
register_equation(acth_dynamics_equation)

"""
TSH secretion as function of free T4 (negative feedback).

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_tsh_response(fT4: float, Kd: float = 1.0, n: float = 2.0,
                         TSH_max: float = 10.0) -> float:
    """
    Calculate TSH secretion as inverse function of free T4.

    Parameters
    ----------
    fT4 : float
        Free T4 concentration (ng/dL)
    Kd : float
        Feedback setpoint (ng/dL)
    n : float
        Hill coefficient (steepness of feedback)
    TSH_max : float
        Maximum TSH concentration (mU/L)

    Returns
    -------
    float
        TSH concentration (mU/L)

    Notes
    -----
    Steep negative feedback (n ≈ 2) provides tight regulation.
    Normal TSH: 0.4-4.0 mU/L
    Normal free T4: 0.8-1.8 ng/dL
    """
    return TSH_max / (1.0 + (fT4 / Kd) ** n)


# Create equation
tsh_response_equation = create_equation(
    id="endocrine.thyroid.tsh_response",
    name="TSH Response to T4 Feedback",
    category=EquationCategory.ENDOCRINE,
    latex=r"TSH = \frac{TSH_{max}}{1 + \left(\frac{fT4}{K_d}\right)^n}",
    simplified="TSH = TSH_max / (1 + (fT4/K_d)^n)",
    description="TSH secretion from pituitary as inverse function of free T4 (negative feedback). "
                "Hill coefficient n ≈ 2 creates steep, sensitive response.",
    compute_func=compute_tsh_response,
    parameters=[
        Parameter(
            name="fT4",
            description="Free T4 concentration",
            units="ng/dL",
            symbol="fT4",
            physiological_range=(0.0, 5.0)
        ),
        Parameter(
            name="Kd",
            description="Feedback setpoint",
            units="ng/dL",
            symbol="K_d",
            default_value=1.0,
            physiological_range=(0.5, 2.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient (feedback steepness)",
            units="dimensionless",
            symbol="n",
            default_value=2.0,
            physiological_range=(1.0, 4.0)
        ),
        Parameter(
            name="TSH_max",
            description="Maximum TSH concentration",
            units="mU/L",
            symbol="TSH_{max}",
            default_value=10.0,
            physiological_range=(5.0, 20.0)
        )
    ],
    depends_on=["endocrine.feedback.negative_feedback_tropic"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.4"
    )
)

# Register globally
register_equation(tsh_response_equation)

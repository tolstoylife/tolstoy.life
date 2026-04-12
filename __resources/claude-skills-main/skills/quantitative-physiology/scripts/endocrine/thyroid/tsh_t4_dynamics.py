"""
Coupled TSH-T4 dynamics with feedback.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_tsh_derivative(fT4: float, TSH: float, k_TRH: float,
                           k_T4: float, n: float, k_deg: float) -> float:
    """
    Calculate rate of change of TSH with T4 feedback.

    Parameters
    ----------
    fT4 : float
        Free T4 concentration
    TSH : float
        TSH concentration
    k_TRH : float
        TRH-stimulated basal secretion
    k_T4 : float
        T4 feedback strength
    n : float
        Hill coefficient (~2 for steep feedback)
    k_deg : float
        TSH degradation rate

    Returns
    -------
    float
        d[TSH]/dt
    """
    return k_TRH - k_T4 * (fT4 ** n) - k_deg * TSH


# Create equation
tsh_dynamics_equation = create_equation(
    id="endocrine.thyroid.tsh_t4_dynamics",
    name="TSH Dynamics with T4 Feedback",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{d[TSH]}{dt} = k_{TRH} - k_{T4} \times [fT4]^n - k_{deg} \times [TSH]",
    simplified="d[TSH]/dt = k_TRH - k_T4 × [fT4]^n - k_deg × [TSH]",
    description="TSH secretion dynamics with steep negative feedback from free T4. "
                "Power term (n ≈ 2) creates high-gain regulation.",
    compute_func=compute_tsh_derivative,
    parameters=[
        Parameter(
            name="fT4",
            description="Free T4 concentration",
            units="ng/dL",
            symbol="[fT4]",
            physiological_range=(0.0, 5.0)
        ),
        Parameter(
            name="TSH",
            description="TSH concentration",
            units="mU/L",
            symbol="[TSH]",
            physiological_range=(0.0, 20.0)
        ),
        Parameter(
            name="k_TRH",
            description="TRH-stimulated basal secretion",
            units="mU/(L·time)",
            symbol="k_{TRH}",
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="k_T4",
            description="T4 feedback strength",
            units="1/time",
            symbol="k_{T4}",
            physiological_range=(0.01, 1.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient",
            units="dimensionless",
            symbol="n",
            default_value=2.0,
            physiological_range=(1.5, 3.0)
        ),
        Parameter(
            name="k_deg",
            description="TSH degradation rate",
            units="1/time",
            symbol="k_{deg}",
            physiological_range=(0.1, 2.0)
        )
    ],
    depends_on=["endocrine.thyroid.tsh_response"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.4"
    )
)

# Register globally
register_equation(tsh_dynamics_equation)

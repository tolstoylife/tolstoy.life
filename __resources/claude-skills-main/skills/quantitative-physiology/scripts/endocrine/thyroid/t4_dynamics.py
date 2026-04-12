"""
T4 dynamics with TSH stimulation and peripheral conversion.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_t4_derivative(TSH: float, T4: float, k_TSH: float,
                         k_conv: float, k_clear: float) -> float:
    """
    Calculate rate of change of T4 concentration.

    Parameters
    ----------
    TSH : float
        TSH concentration (stimulation)
    T4 : float
        T4 concentration
    k_TSH : float
        TSH stimulation constant
    k_conv : float
        Conversion to T3 rate (deiodinase)
    k_clear : float
        Direct clearance rate

    Returns
    -------
    float
        d[T4]/dt

    Notes
    -----
    T4 half-life: 6-7 days
    ~80% of circulating T3 comes from peripheral T4→T3 conversion
    """
    return k_TSH * TSH - k_conv * T4 - k_clear * T4


# Create equation
t4_dynamics_equation = create_equation(
    id="endocrine.thyroid.t4_dynamics",
    name="T4 Dynamics",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{d[T4]}{dt} = k_{TSH} \times [TSH] - k_{conv} \times [T4] - k_{clear} \times [T4]",
    simplified="d[T4]/dt = k_TSH × [TSH] - k_conv × [T4] - k_clear × [T4]",
    description="T4 dynamics: TSH-stimulated production, peripheral conversion to T3, "
                "and direct clearance. Half-life ~6-7 days.",
    compute_func=compute_t4_derivative,
    parameters=[
        Parameter(
            name="TSH",
            description="TSH concentration",
            units="mU/L",
            symbol="[TSH]",
            physiological_range=(0.0, 20.0)
        ),
        Parameter(
            name="T4",
            description="T4 concentration",
            units="μg/dL",
            symbol="[T4]",
            physiological_range=(0.0, 20.0)
        ),
        Parameter(
            name="k_TSH",
            description="TSH stimulation constant",
            units="1/time",
            symbol="k_{TSH}",
            physiological_range=(0.1, 5.0)
        ),
        Parameter(
            name="k_conv",
            description="T4→T3 conversion rate",
            units="1/time",
            symbol="k_{conv}",
            physiological_range=(0.001, 0.1)
        ),
        Parameter(
            name="k_clear",
            description="T4 clearance rate",
            units="1/time",
            symbol="k_{clear}",
            physiological_range=(0.001, 0.1)
        )
    ],
    depends_on=["endocrine.thyroid.t4_production", "endocrine.thyroid.tsh_t4_dynamics"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.4"
    )
)

# Register globally
register_equation(t4_dynamics_equation)

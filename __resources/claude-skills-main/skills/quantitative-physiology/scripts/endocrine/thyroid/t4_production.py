"""
T4 production rate as function of TSH.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_t4_production(TSH: float, Vmax: float = 100.0, Km: float = 2.0) -> float:
    """
    Calculate T4 production rate using Michaelis-Menten kinetics.

    Parameters
    ----------
    TSH : float
        TSH concentration (mU/L)
    Vmax : float
        Maximum production rate (μg/day)
    Km : float
        Michaelis constant (mU/L)

    Returns
    -------
    float
        T4 production rate (μg/day)

    Notes
    -----
    Daily T4 production: ~80-100 μg/day (all from thyroid)
    Daily T3 production: ~30-40 μg/day (20% thyroid, 80% peripheral conversion)
    """
    return Vmax * TSH / (Km + TSH)


# Create equation
t4_production_equation = create_equation(
    id="endocrine.thyroid.t4_production",
    name="T4 Production Rate",
    category=EquationCategory.ENDOCRINE,
    latex=r"\text{T4 production} = \frac{V_{max} \times TSH}{K_m + TSH}",
    simplified="T4_production = V_max × TSH / (K_m + TSH)",
    description="T4 synthesis and secretion from thyroid follicular cells. "
                "Follows Michaelis-Menten kinetics with TSH stimulation.",
    compute_func=compute_t4_production,
    parameters=[
        Parameter(
            name="TSH",
            description="TSH concentration",
            units="mU/L",
            symbol="TSH",
            physiological_range=(0.0, 20.0)
        ),
        Parameter(
            name="Vmax",
            description="Maximum production rate",
            units="μg/day",
            symbol="V_{max}",
            default_value=100.0,
            physiological_range=(50.0, 200.0)
        ),
        Parameter(
            name="Km",
            description="Michaelis constant",
            units="mU/L",
            symbol="K_m",
            default_value=2.0,
            physiological_range=(1.0, 5.0)
        )
    ],
    depends_on=["endocrine.thyroid.tsh_response"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.4"
    )
)

# Register globally
register_equation(t4_production_equation)

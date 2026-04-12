"""
Glucose-stimulated insulin secretion (GSIS).

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_gsis(glucose: float, I_basal: float = 5.0, I_max: float = 50.0,
                EC50: float = 6.0, n: float = 2.5) -> float:
    """
    Calculate insulin secretion rate from glucose concentration.

    Parameters
    ----------
    glucose : float
        Blood glucose concentration (mM)
    I_basal : float
        Basal insulin secretion rate (μU/mL/min)
    I_max : float
        Maximum insulin secretion above basal (μU/mL/min)
    EC50 : float
        Glucose concentration for half-maximal response (mM)
    n : float
        Hill coefficient (cooperativity)

    Returns
    -------
    float
        Insulin secretion rate (μU/mL/min)

    Notes
    -----
    EC50 ≈ 5-6 mM glucose
    n ≈ 2-3 (sigmoidal dose-response)
    I_max ≈ 10× I_basal
    Biphasic response: first phase 2-5 min, second phase 10-60+ min
    """
    stimulation = (glucose ** n) / (EC50 ** n + glucose ** n)
    return I_basal + I_max * stimulation


# Create equation
gsis_equation = create_equation(
    id="endocrine.pancreatic.gsis",
    name="Glucose-Stimulated Insulin Secretion",
    category=EquationCategory.ENDOCRINE,
    latex=r"\text{Insulin} = I_{basal} + I_{max} \times \frac{[Glucose]^n}{EC_{50}^n + [Glucose]^n}",
    simplified="Insulin = I_basal + I_max × [Glucose]^n / (EC50^n + [Glucose]^n)",
    description="Insulin secretion from pancreatic β-cells as sigmoidal function of glucose. "
                "Hill equation captures cooperative glucose sensing (n ≈ 2-3).",
    compute_func=compute_gsis,
    parameters=[
        Parameter(
            name="glucose",
            description="Blood glucose concentration",
            units="mM",
            symbol="[Glucose]",
            physiological_range=(2.0, 20.0)
        ),
        Parameter(
            name="I_basal",
            description="Basal insulin secretion",
            units="μU/mL/min",
            symbol="I_{basal}",
            default_value=5.0,
            physiological_range=(1.0, 10.0)
        ),
        Parameter(
            name="I_max",
            description="Maximum insulin above basal",
            units="μU/mL/min",
            symbol="I_{max}",
            default_value=50.0,
            physiological_range=(20.0, 100.0)
        ),
        Parameter(
            name="EC50",
            description="Half-maximal glucose concentration",
            units="mM",
            symbol="EC_{50}",
            default_value=6.0,
            physiological_range=(4.0, 8.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient",
            units="dimensionless",
            symbol="n",
            default_value=2.5,
            physiological_range=(2.0, 3.5)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.6"
    )
)

# Register globally
register_equation(gsis_equation)

"""SGLT1-mediated glucose absorption."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_sglt1_glucose(glucose_lumen: float, Vmax: float = 6.0, Km: float = 0.3) -> float:
    """
    Calculate SGLT1-mediated glucose absorption rate.

    SGLT1 is a Na+/glucose cotransporter (2 Na+ : 1 glucose).

    Parameters
    ----------
    glucose_lumen : float
        Luminal glucose concentration (mM)
    Vmax : float
        Maximum absorption rate (mM/min), default 6.0
    Km : float
        Michaelis constant (mM), default 0.3 mM

    Returns
    -------
    float
        Glucose absorption rate (mM/min)
    """
    return Vmax * glucose_lumen / (Km + glucose_lumen)


sglt1_glucose = create_equation(
    id="gastrointestinal.absorption.sglt1_glucose",
    name="SGLT1 Glucose Absorption",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"J_{\text{glucose}} = \frac{V_{\max} \times [\text{Glucose}]}{K_m + [\text{Glucose}]}",
    simplified="J_glucose = V_max × [Glucose] / (K_m + [Glucose])",
    description="SGLT1-mediated glucose absorption (apical). 2 Na+ : 1 glucose cotransport. K_m ≈ 0.3 mM. Electrogenic.",
    compute_func=compute_sglt1_glucose,
    parameters=[
        Parameter(
            name="glucose_lumen",
            description="Luminal glucose concentration",
            units="mM",
            symbol=r"[\text{Glucose}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="Vmax",
            description="Maximum absorption rate",
            units="mM/min",
            symbol=r"V_{\max}",
            default_value=6.0,
            physiological_range=(4.0, 8.0)
        ),
        Parameter(
            name="Km",
            description="Michaelis constant",
            units="mM",
            symbol="K_m",
            default_value=0.3,
            physiological_range=(0.2, 0.5)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.4"
    )
)

register_equation(sglt1_glucose)

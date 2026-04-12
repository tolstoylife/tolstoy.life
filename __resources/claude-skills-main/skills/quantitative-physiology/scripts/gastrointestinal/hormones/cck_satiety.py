"""CCK satiety effect."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_cck_satiety(CCK_pM: float, k: float = 1.0) -> float:
    """
    Calculate food intake inhibition by CCK.

    CCK satiety effect is proportional to log([CCK]).
    Half-life ~2-3 min (rapid peptidase degradation).

    Parameters
    ----------
    CCK_pM : float
        CCK concentration (pM)
    k : float
        Satiety coefficient, default 1.0

    Returns
    -------
    float
        Satiety signal (log scale)
    """
    if CCK_pM <= 0:
        return 0.0
    return k * np.log(CCK_pM)


cck_satiety = create_equation(
    id="gastrointestinal.hormones.cck_satiety",
    name="CCK Satiety Effect",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{Satiety} = k \times \ln([\text{CCK}])",
    simplified="Satiety = k × ln([CCK])",
    description="CCK-induced satiety (food intake inhibition) proportional to log([CCK]). Half-life ~2-3 min",
    compute_func=compute_cck_satiety,
    parameters=[
        Parameter(
            name="CCK_pM",
            description="CCK concentration",
            units="pM",
            symbol=r"[\text{CCK}]",
            physiological_range=(1.0, 1000.0)
        ),
        Parameter(
            name="k",
            description="Satiety coefficient",
            units="dimensionless",
            symbol="k",
            default_value=1.0,
            physiological_range=(0.5, 2.0)
        )
    ],
    depends_on=["gastrointestinal.hormones.cck_response"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.5"
    )
)

register_equation(cck_satiety)

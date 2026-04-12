"""Incretin effect on insulin secretion."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_incretin_effect(insulin_oral: float, insulin_iv: float) -> float:
    """
    Calculate incretin effect: ratio of insulin response to oral vs IV glucose.

    Oral glucose triggers 2-3× more insulin than IV glucose at same plasma glucose.
    Due to GIP (~60%) and GLP-1 (~40%).

    Parameters
    ----------
    insulin_oral : float
        Insulin response to oral glucose (pmol/L)
    insulin_iv : float
        Insulin response to IV glucose (pmol/L)

    Returns
    -------
    float
        Incretin effect ratio (normally 2-3)
    """
    if insulin_iv > 0:
        return insulin_oral / insulin_iv
    else:
        return float('inf')


incretin_effect = create_equation(
    id="gastrointestinal.hormones.incretin_effect",
    name="Incretin Effect",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{Incretin ratio} = \frac{\text{Insulin}_{\text{oral}}}{\text{Insulin}_{\text{IV}}}",
    simplified="Incretin ratio = Insulin_oral / Insulin_IV",
    description="Incretin effect: oral glucose → 2-3× more insulin than IV glucose. Due to GIP (60%) + GLP-1 (40%)",
    compute_func=compute_incretin_effect,
    parameters=[
        Parameter(
            name="insulin_oral",
            description="Insulin response to oral glucose",
            units="pmol/L",
            symbol=r"\text{Insulin}_{\text{oral}}",
            physiological_range=(50.0, 500.0)
        ),
        Parameter(
            name="insulin_iv",
            description="Insulin response to IV glucose",
            units="pmol/L",
            symbol=r"\text{Insulin}_{\text{IV}}",
            physiological_range=(20.0, 200.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.5"
    )
)

register_equation(incretin_effect)

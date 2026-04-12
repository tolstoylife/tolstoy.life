"""Lithogenic index for gallstone risk."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_lithogenic_index(cholesterol: float, bile_acids: float, phospholipids: float) -> float:
    """
    Calculate lithogenic index for gallstone risk.

    LI = Actual cholesterol / Maximum soluble cholesterol
    LI > 1: supersaturated bile → gallstone risk
    LI < 1: undersaturated bile → no gallstone risk

    Maximum cholesterol solubility (simplified):
    Max_chol = 0.07 × bile_acids + 0.26 × phospholipids

    Parameters
    ----------
    cholesterol : float
        Cholesterol concentration (mM)
    bile_acids : float
        Bile acid concentration (mM)
    phospholipids : float
        Phospholipid concentration (mM)

    Returns
    -------
    float
        Lithogenic index (>1 indicates supersaturation)
    """
    max_cholesterol = 0.07 * bile_acids + 0.26 * phospholipids
    if max_cholesterol > 0:
        return cholesterol / max_cholesterol
    else:
        return float('inf')


lithogenic_index = create_equation(
    id="gastrointestinal.liver.lithogenic_index",
    name="Lithogenic Index",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"LI = \frac{[\text{Chol}]_{\text{actual}}}{[\text{Chol}]_{\max}} = \frac{[\text{Chol}]}{0.07 \times [\text{BA}] + 0.26 \times [\text{PL}]}",
    simplified="LI = [Chol] / (0.07×[BA] + 0.26×[PL])",
    description="Lithogenic index for gallstone risk. LI > 1: supersaturated bile → gallstone formation",
    compute_func=compute_lithogenic_index,
    parameters=[
        Parameter(
            name="cholesterol",
            description="Cholesterol concentration",
            units="mM",
            symbol=r"[\text{Chol}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="bile_acids",
            description="Bile acid concentration",
            units="mM",
            symbol=r"[\text{BA}]",
            physiological_range=(10.0, 150.0)
        ),
        Parameter(
            name="phospholipids",
            description="Phospholipid concentration",
            units="mM",
            symbol=r"[\text{PL}]",
            physiological_range=(5.0, 50.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.6"
    )
)

register_equation(lithogenic_index)

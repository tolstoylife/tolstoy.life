"""Lipase activity dependence on bile salt concentration."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_lipase_activity_bile(bile_salt_conc: float, CMC: float = 3.0) -> float:
    """
    Calculate lipase effectiveness based on bile salt concentration.

    Micelle formation (requires [bile salt] > CMC) is necessary for optimal lipase activity.

    Parameters
    ----------
    bile_salt_conc : float
        Bile salt concentration (mM)
    CMC : float
        Critical micellar concentration (mM), default 3.0 mM

    Returns
    -------
    float
        Lipase effectiveness (0-1)
    """
    if bile_salt_conc >= CMC:
        return 1.0
    else:
        return bile_salt_conc / CMC


lipase_activity_bile = create_equation(
    id="gastrointestinal.digestion.lipase_activity_bile",
    name="Lipase Activity vs Bile Salts",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{Effectiveness} = \begin{cases} 1.0 & [\text{bile}] \geq \text{CMC} \\ \frac{[\text{bile}]}{\text{CMC}} & [\text{bile}] < \text{CMC} \end{cases}",
    simplified="Effectiveness = 1.0 if [bile] ≥ CMC, else [bile]/CMC",
    description="Lipase effectiveness depends on bile salt concentration. Full activity when [bile salt] > CMC (~3 mM)",
    compute_func=compute_lipase_activity_bile,
    parameters=[
        Parameter(
            name="bile_salt_conc",
            description="Bile salt concentration",
            units="mM",
            symbol=r"[\text{bile}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="CMC",
            description="Critical micellar concentration",
            units="mM",
            symbol=r"\text{CMC}",
            default_value=3.0,
            physiological_range=(2.0, 5.0)
        )
    ],
    depends_on=["gastrointestinal.secretion.critical_micellar_concentration"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.3"
    )
)

register_equation(lipase_activity_bile)

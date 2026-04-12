"""Fat absorption efficiency."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_fat_absorption_efficiency(bile_salt_conc: float, CMC: float = 3.0, lipase_activity: float = 1.0) -> float:
    """
    Calculate fat absorption efficiency.

    Requires: bile salts > CMC for micelle formation, lipase activity.
    Normal efficiency: >95% for typical diet.

    Parameters
    ----------
    bile_salt_conc : float
        Bile salt concentration (mM)
    CMC : float
        Critical micellar concentration (mM), default 3.0
    lipase_activity : float
        Lipase activity (0-1 scale), default 1.0

    Returns
    -------
    float
        Fat absorption efficiency (0-1)
    """
    if bile_salt_conc >= CMC:
        micellar_efficiency = 1.0
    else:
        micellar_efficiency = bile_salt_conc / CMC

    return 0.95 * micellar_efficiency * lipase_activity


fat_absorption_efficiency = create_equation(
    id="gastrointestinal.absorption.fat_absorption_efficiency",
    name="Fat Absorption Efficiency",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\eta_{\text{fat}} = 0.95 \times \eta_{\text{micelle}} \times A_{\text{lipase}}",
    simplified="η_fat = 0.95 × η_micelle × A_lipase",
    description="Fat absorption efficiency. Requires bile salts > CMC for micelle formation. Normal: >95% absorption",
    compute_func=compute_fat_absorption_efficiency,
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
        ),
        Parameter(
            name="lipase_activity",
            description="Lipase activity (0-1 scale)",
            units="dimensionless",
            symbol=r"A_{\text{lipase}}",
            default_value=1.0,
            physiological_range=(0.0, 1.0)
        )
    ],
    depends_on=["gastrointestinal.secretion.critical_micellar_concentration", "gastrointestinal.digestion.lipase_activity_bile"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.4"
    )
)

register_equation(fat_absorption_efficiency)

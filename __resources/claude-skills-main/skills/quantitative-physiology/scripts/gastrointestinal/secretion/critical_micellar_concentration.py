"""Critical micellar concentration for bile salts."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_micelle_formation(bile_salt_conc: float, CMC: float = 3.0) -> bool:
    """
    Determine if micelle formation occurs based on bile salt concentration.

    Parameters
    ----------
    bile_salt_conc : float
        Bile salt concentration (mM)
    CMC : float
        Critical micellar concentration (mM), default 3 mM

    Returns
    -------
    bool
        True if micelles can form ([bile salt] > CMC)
    """
    return bile_salt_conc > CMC


critical_micellar_concentration = create_equation(
    id="gastrointestinal.secretion.critical_micellar_concentration",
    name="Critical Micellar Concentration",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{Micelle formation: } [\text{bile salt}] > \text{CMC}",
    simplified="Micelle formation: [bile salt] > CMC",
    description="Micelle formation requires bile salt concentration above CMC (~2-5 mM for bile salts)",
    compute_func=compute_micelle_formation,
    parameters=[
        Parameter(
            name="bile_salt_conc",
            description="Bile salt concentration",
            units="mM",
            symbol=r"[\text{bile salt}]",
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
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.2"
    )
)

register_equation(critical_micellar_concentration)

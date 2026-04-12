"""Amylase kinetics for starch digestion."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_amylase_rate(starch_conc: float, J_max: float = 10.0, Km: float = 1.5) -> float:
    """
    Calculate amylase digestion rate for starch.

    Amylase (salivary + pancreatic) breaks starch into maltose, maltotriose, and α-limit dextrins.

    Parameters
    ----------
    starch_conc : float
        Starch concentration (mg/mL)
    J_max : float
        Maximum digestion rate, default 10 mg/(mL·min)
    Km : float
        Michaelis constant (mg/mL), default 1.5 mg/mL

    Returns
    -------
    float
        Digestion rate (mg/(mL·min))
    """
    return J_max * starch_conc / (Km + starch_conc)


amylase_kinetics = create_equation(
    id="gastrointestinal.digestion.amylase_kinetics",
    name="Amylase Kinetics",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"J = \frac{J_{\max} \times [\text{Starch}]}{K_m + [\text{Starch}]}",
    simplified="J = J_max × [Starch] / (K_m + [Starch])",
    description="α-Amylase kinetics for starch digestion to maltose, maltotriose, and α-limit dextrins. K_m ≈ 1-2 mg/mL",
    compute_func=compute_amylase_rate,
    parameters=[
        Parameter(
            name="starch_conc",
            description="Starch concentration",
            units="mg/mL",
            symbol=r"[\text{Starch}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="J_max",
            description="Maximum digestion rate",
            units="mg/(mL·min)",
            symbol=r"J_{\max}",
            default_value=10.0,
            physiological_range=(5.0, 20.0)
        ),
        Parameter(
            name="Km",
            description="Michaelis constant",
            units="mg/mL",
            symbol="K_m",
            default_value=1.5,
            physiological_range=(1.0, 2.0)
        )
    ],
    depends_on=["gastrointestinal.digestion.enzyme_kinetics"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.3"
    )
)

register_equation(amylase_kinetics)

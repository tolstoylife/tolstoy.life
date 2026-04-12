"""Pancreatic lipase kinetics for triglyceride digestion."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_lipase_rate(TG_conc: float, J_max: float = 15.0, Km: float = 2.0) -> float:
    """
    Calculate pancreatic lipase digestion rate for triglycerides.

    Lipase requires colipase to anchor to emulsion surface.
    TG + H2O → 2 FFA + 2-monoglyceride

    Parameters
    ----------
    TG_conc : float
        Triglyceride concentration (mM)
    J_max : float
        Maximum digestion rate (mM/min), default 15
    Km : float
        Michaelis constant (mM), default 2.0

    Returns
    -------
    float
        Digestion rate (mM/min)
    """
    return J_max * TG_conc / (Km + TG_conc)


lipase_kinetics = create_equation(
    id="gastrointestinal.digestion.lipase_kinetics",
    name="Pancreatic Lipase Kinetics",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"J = \frac{J_{\max} \times [\text{TG}]}{K_m + [\text{TG}]}",
    simplified="J = J_max × [TG] / (K_m + [TG])",
    description="Pancreatic lipase kinetics for triglyceride hydrolysis. Requires colipase for anchoring. Produces 2 FFA + 2-MG",
    compute_func=compute_lipase_rate,
    parameters=[
        Parameter(
            name="TG_conc",
            description="Triglyceride concentration",
            units="mM",
            symbol=r"[\text{TG}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="J_max",
            description="Maximum digestion rate",
            units="mM/min",
            symbol=r"J_{\max}",
            default_value=15.0,
            physiological_range=(10.0, 25.0)
        ),
        Parameter(
            name="Km",
            description="Michaelis constant",
            units="mM",
            symbol="K_m",
            default_value=2.0,
            physiological_range=(1.0, 5.0)
        )
    ],
    depends_on=["gastrointestinal.digestion.enzyme_kinetics"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.3"
    )
)

register_equation(lipase_kinetics)

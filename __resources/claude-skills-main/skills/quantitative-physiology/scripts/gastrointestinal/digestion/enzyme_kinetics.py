"""Michaelis-Menten enzyme kinetics for digestion."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_enzyme_kinetics(S: float, Vmax: float, Km: float) -> float:
    """
    Calculate enzyme reaction rate using Michaelis-Menten kinetics.

    Parameters
    ----------
    S : float
        Substrate concentration
    Vmax : float
        Maximum reaction rate
    Km : float
        Michaelis constant (substrate concentration at half Vmax)

    Returns
    -------
    float
        Reaction rate (same units as Vmax)
    """
    return Vmax * S / (Km + S)


enzyme_kinetics = create_equation(
    id="gastrointestinal.digestion.enzyme_kinetics",
    name="Enzyme Kinetics (Michaelis-Menten)",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"v = \frac{V_{\max} \times [S]}{K_m + [S]}",
    simplified="v = V_max × [S] / (K_m + [S])",
    description="Michaelis-Menten enzyme kinetics for digestive enzymes (amylase, pepsin, lipase, etc.)",
    compute_func=compute_enzyme_kinetics,
    parameters=[
        Parameter(
            name="S",
            description="Substrate concentration",
            units="variable",
            symbol="[S]",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="Vmax",
            description="Maximum reaction rate",
            units="variable",
            symbol=r"V_{\max}",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="Km",
            description="Michaelis constant",
            units="variable",
            symbol="K_m",
            physiological_range=(0.01, 100.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.3"
    )
)

register_equation(enzyme_kinetics)

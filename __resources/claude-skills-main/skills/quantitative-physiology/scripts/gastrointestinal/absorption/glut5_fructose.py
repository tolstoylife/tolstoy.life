"""GLUT5-mediated fructose absorption."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_glut5_fructose(fructose_lumen: float, Vmax: float = 3.0, Km: float = 8.0) -> float:
    """
    Calculate GLUT5-mediated fructose absorption rate.

    GLUT5 is a facilitated diffusion transporter (not Na+-dependent).

    Parameters
    ----------
    fructose_lumen : float
        Luminal fructose concentration (mM)
    Vmax : float
        Maximum absorption rate (mM/min), default 3.0
    Km : float
        Michaelis constant (mM), default 8.0 mM

    Returns
    -------
    float
        Fructose absorption rate (mM/min)
    """
    return Vmax * fructose_lumen / (Km + fructose_lumen)


glut5_fructose = create_equation(
    id="gastrointestinal.absorption.glut5_fructose",
    name="GLUT5 Fructose Absorption",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"J_{\text{fructose}} = \frac{V_{\max} \times [\text{Fructose}]}{K_m + [\text{Fructose}]}",
    simplified="J_fructose = V_max × [Fructose] / (K_m + [Fructose])",
    description="GLUT5-mediated fructose absorption (apical). Facilitated diffusion. K_m ≈ 6-11 mM. Not Na+-dependent.",
    compute_func=compute_glut5_fructose,
    parameters=[
        Parameter(
            name="fructose_lumen",
            description="Luminal fructose concentration",
            units="mM",
            symbol=r"[\text{Fructose}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="Vmax",
            description="Maximum absorption rate",
            units="mM/min",
            symbol=r"V_{\max}",
            default_value=3.0,
            physiological_range=(2.0, 5.0)
        ),
        Parameter(
            name="Km",
            description="Michaelis constant",
            units="mM",
            symbol="K_m",
            default_value=8.0,
            physiological_range=(6.0, 11.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.4"
    )
)

register_equation(glut5_fructose)

"""Pepsin activity as function of pH."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_pepsin_activity(pH: float, H_conc: float, A_max: float = 1.0, K_H: float = 5.0, n: float = 2.0) -> float:
    """
    Calculate pepsin activity based on pH and H+ concentration.

    Pepsin has optimal pH of 1.8-3.5. Activity follows Hill equation.

    Parameters
    ----------
    pH : float
        pH value
    H_conc : float
        H+ concentration (mM)
    A_max : float
        Maximum activity (normalized), default 1.0
    K_H : float
        Half-maximal H+ concentration (mM), default 5.0
    n : float
        Hill coefficient, default 2.0

    Returns
    -------
    float
        Pepsin activity (normalized, 0-1)
    """
    activity = A_max * (H_conc ** n) / (K_H ** n + H_conc ** n)
    return activity


pepsin_activity = create_equation(
    id="gastrointestinal.digestion.pepsin_activity",
    name="Pepsin Activity",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"A = \frac{A_{\max} \times [H^+]^n}{K_H^n + [H^+]^n}",
    simplified="A = A_max × [H+]^n / (K_H^n + [H+]^n)",
    description="Pepsin activity as function of H+ concentration. Optimal pH: 1.8-3.5. Cleaves aromatic amino acids (Phe, Tyr, Trp)",
    compute_func=compute_pepsin_activity,
    parameters=[
        Parameter(
            name="pH",
            description="pH value",
            units="dimensionless",
            symbol="pH",
            physiological_range=(0.8, 7.0)
        ),
        Parameter(
            name="H_conc",
            description="H+ concentration",
            units="mM",
            symbol="[H^+]",
            physiological_range=(0.001, 150.0)
        ),
        Parameter(
            name="A_max",
            description="Maximum activity",
            units="dimensionless",
            symbol=r"A_{\max}",
            default_value=1.0,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="K_H",
            description="Half-maximal H+ concentration",
            units="mM",
            symbol="K_H",
            default_value=5.0,
            physiological_range=(1.0, 10.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient",
            units="dimensionless",
            symbol="n",
            default_value=2.0,
            physiological_range=(1.0, 4.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.3"
    )
)

register_equation(pepsin_activity)

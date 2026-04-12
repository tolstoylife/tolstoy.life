"""Gastric emptying equation for liquids (first-order kinetics)."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_gastric_emptying_liquid(t: float, V0: float, k: float) -> float:
    """
    Calculate gastric volume remaining using first-order kinetics (liquids).

    Parameters
    ----------
    t : float
        Time (minutes)
    V0 : float
        Initial volume (mL)
    k : float
        Emptying rate constant (1/min)

    Returns
    -------
    float
        Remaining volume (mL)
    """
    return V0 * np.exp(-k * t)


gastric_emptying_liquid = create_equation(
    id="gastrointestinal.motility.gastric_emptying_liquid",
    name="Gastric Emptying (Liquids)",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"V(t) = V_0 \times e^{-kt}",
    simplified="V(t) = V₀ × e^(-k×t)",
    description="First-order gastric emptying kinetics for liquids, with half-life t₁/₂ = ln(2)/k ≈ 10-20 min",
    compute_func=compute_gastric_emptying_liquid,
    parameters=[
        Parameter(
            name="t",
            description="Time",
            units="min",
            symbol="t",
            physiological_range=(0.0, 180.0)
        ),
        Parameter(
            name="V0",
            description="Initial volume",
            units="mL",
            symbol="V_0",
            physiological_range=(100.0, 1000.0)
        ),
        Parameter(
            name="k",
            description="Emptying rate constant (k = ln(2)/t₁/₂)",
            units="1/min",
            symbol="k",
            default_value=0.05,
            physiological_range=(0.03, 0.07)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.1"
    )
)

register_equation(gastric_emptying_liquid)

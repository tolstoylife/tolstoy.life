"""First-order starch digestion kinetics."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_starch_remaining(t: float, starch_0: float, k: float = 0.1) -> float:
    """
    Calculate remaining starch using first-order digestion kinetics.

    Parameters
    ----------
    t : float
        Time (minutes)
    starch_0 : float
        Initial starch amount (g)
    k : float
        Digestion rate constant (1/min), default 0.1

    Returns
    -------
    float
        Remaining starch (g)
    """
    return starch_0 * np.exp(-k * t)


starch_digestion_first_order = create_equation(
    id="gastrointestinal.digestion.starch_digestion_first_order",
    name="First-Order Starch Digestion",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"[\text{Starch}](t) = [\text{Starch}]_0 \times e^{-kt}",
    simplified="[Starch](t) = [Starch]_0 × e^(-kt)",
    description="First-order starch digestion kinetics by amylase",
    compute_func=compute_starch_remaining,
    parameters=[
        Parameter(
            name="t",
            description="Time",
            units="min",
            symbol="t",
            physiological_range=(0.0, 300.0)
        ),
        Parameter(
            name="starch_0",
            description="Initial starch amount",
            units="g",
            symbol=r"[\text{Starch}]_0",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="k",
            description="Digestion rate constant",
            units="1/min",
            symbol="k",
            default_value=0.1,
            physiological_range=(0.05, 0.2)
        )
    ],
    depends_on=["gastrointestinal.digestion.amylase_kinetics"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.3"
    )
)

register_equation(starch_digestion_first_order)

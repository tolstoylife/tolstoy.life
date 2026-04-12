"""Funny current (If) equation for pacemaker cells."""

import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_funny_current(V_m: float, E_f: float, g_f: float, y: float) -> float:
    """
    Calculate funny current (HCN channel current) in pacemaker cells.

    Parameters
    ----------
    V_m : float
        Membrane potential (mV)
    E_f : float
        Reversal potential for funny current (mV)
    g_f : float
        Maximum conductance (nS)
    y : float
        Gating variable (0-1)

    Returns
    -------
    float
        Funny current (pA)
    """
    return g_f * (V_m - E_f) * y


funny_current = create_equation(
    id="cardiovascular.ecg.funny_current",
    name="Funny Current (If)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"I_f = g_f \times (V_m - E_f) \times y",
    simplified="I_f = g_f × (V_m - E_f) × y",
    description="HCN channel current responsible for phase 4 depolarization in pacemaker cells",
    compute_func=compute_funny_current,
    parameters=[
        Parameter(
            name="V_m",
            description="Membrane potential",
            units="mV",
            symbol="V_m",
            physiological_range=(-70.0, 40.0)
        ),
        Parameter(
            name="E_f",
            description="Reversal potential for funny current",
            units="mV",
            symbol="E_f",
            default_value=-20.0,
            physiological_range=(-30.0, -10.0)
        ),
        Parameter(
            name="g_f",
            description="Maximum funny current conductance",
            units="nS",
            symbol="g_f",
            physiological_range=(0.5, 5.0)
        ),
        Parameter(
            name="y",
            description="Gating variable",
            units="dimensionless",
            symbol="y",
            physiological_range=(0.0, 1.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.2"
    )
)

register_equation(funny_current)

"""Pancreatic bicarbonate concentration equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_pancreatic_bicarbonate(flow_rate: float, max_HCO3: float = 140.0, max_flow: float = 4.0) -> float:
    """
    Calculate pancreatic bicarbonate concentration as function of flow rate.

    Parameters
    ----------
    flow_rate : float
        Pancreatic flow rate (mL/min)
    max_HCO3 : float
        Maximum HCO3- concentration (mM), default 140 mM
    max_flow : float
        Flow rate at which max HCO3- approached (mL/min), default 4 mL/min

    Returns
    -------
    float
        HCO3- concentration (mM)
    """
    fraction = 1 - np.exp(-flow_rate / max_flow)
    return max_HCO3 * fraction + 20 * (1 - fraction)


pancreatic_bicarbonate = create_equation(
    id="gastrointestinal.secretion.pancreatic_bicarbonate",
    name="Pancreatic Bicarbonate Concentration",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"[\text{HCO}_3^-] = 140 \times f + 20 \times (1-f), \quad f = 1 - e^{-Q/Q_{\text{max}}}",
    simplified="[HCO3-] = 140×f + 20×(1-f), f = 1 - e^(-Q/Q_max)",
    description="Pancreatic HCO3- concentration varies with flow: high flow→140 mM, low flow→20 mM. Sum [HCO3-]+[Cl-]≈160 mM constant",
    compute_func=compute_pancreatic_bicarbonate,
    parameters=[
        Parameter(
            name="flow_rate",
            description="Pancreatic flow rate",
            units="mL/min",
            symbol="Q",
            physiological_range=(0.5, 5.0)
        ),
        Parameter(
            name="max_HCO3",
            description="Maximum HCO3- concentration",
            units="mM",
            symbol=r"[\text{HCO}_3^-]_{\text{max}}",
            default_value=140.0,
            physiological_range=(120.0, 150.0)
        ),
        Parameter(
            name="max_flow",
            description="Flow rate approaching maximum HCO3-",
            units="mL/min",
            symbol=r"Q_{\text{max}}",
            default_value=4.0,
            physiological_range=(3.0, 5.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.2"
    )
)

register_equation(pancreatic_bicarbonate)

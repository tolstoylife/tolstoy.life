"""
Capacitance - Charge storage capacity

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_capacitance(Q: float, V: float) -> float:
    """
    Calculate capacitance from charge and voltage.

    Formula: C = Q/V

    Parameters:
    -----------
    Q : float - Stored charge (C)
    V : float - Voltage difference (V)

    Returns:
    --------
    C : float - Capacitance (F)
    """
    return Q / V


# Create and register atomic equation
capacitance = create_equation(
    id="foundations.electrical.capacitance",
    name="Capacitance",
    category=EquationCategory.FOUNDATIONS,
    latex=r"C = \frac{Q}{V}",
    simplified="C = Q / V",
    description="Capacitance definition - charge per unit voltage",
    compute_func=compute_capacitance,
    parameters=[
        Parameter(
            name="Q",
            description="Stored charge",
            units="C",
            symbol="Q",
            physiological_range=(0.0, 1e-9)
        ),
        Parameter(
            name="V",
            description="Voltage difference",
            units="V",
            symbol="V",
            physiological_range=(0.0, 0.2)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.2")
)

register_equation(capacitance)

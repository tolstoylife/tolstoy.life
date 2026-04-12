"""
Electric Field - Force per unit charge

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_electric_field(F: float, q: float) -> float:
    """
    Calculate electric field from force and charge.

    Formula: E = F/q

    Parameters:
    -----------
    F : float - Force on test charge (N)
    q : float - Test charge (C)

    Returns:
    --------
    E : float - Electric field (N/C or V/m)
    """
    return F / q


# Create and register atomic equation
electric_field = create_equation(
    id="foundations.electrical.electric_field",
    name="Electric Field",
    category=EquationCategory.FOUNDATIONS,
    latex=r"E = \frac{F}{q} = -\nabla U",
    simplified="E = F / q",
    description="Electric field strength - force per unit charge, points from high to low potential",
    compute_func=compute_electric_field,
    parameters=[
        Parameter(
            name="F",
            description="Force on test charge",
            units="N",
            symbol="F",
            physiological_range=(-1e-12, 1e-12)
        ),
        Parameter(
            name="q",
            description="Test charge",
            units="C",
            symbol="q",
            physiological_range=(1e-19, 1e-15)
        )
    ],
    depends_on=["foundations.electrical.coulomb_law"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.2")
)

register_equation(electric_field)

"""Permeability-surface area product from extraction ratio."""

import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_ps_product(Q: float, E: float) -> float:
    """
    Calculate permeability-surface area product from extraction ratio.

    Parameters
    ----------
    Q : float
        Blood flow rate (mL/min)
    E : float
        Extraction ratio (0-1)

    Returns
    -------
    float
        PS product (mL/min)
    """
    if E >= 1.0:
        raise ValueError("Extraction ratio must be < 1.0")
    return -Q * np.log(1 - E)


ps_product = create_equation(
    id="cardiovascular.microcirculation.ps_product",
    name="Permeability-Surface Area Product",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{PS} = -Q \times \ln(1 - E)",
    simplified="PS = -Q × ln(1 - E)",
    description="Permeability-surface area product derived from extraction ratio",
    compute_func=compute_ps_product,
    parameters=[
        Parameter(
            name="Q",
            description="Blood flow rate",
            units="mL/min",
            symbol="Q",
            physiological_range=(1.0, 1000.0)
        ),
        Parameter(
            name="E",
            description="Extraction ratio",
            units="dimensionless",
            symbol="E",
            physiological_range=(0.0, 0.99)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.5"
    )
)

register_equation(ps_product)

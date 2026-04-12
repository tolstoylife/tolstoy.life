"""
Muscle ATP Consumption Rate

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def atp_consumption(isometric_rate: float, shortening_rate: float, v: float) -> float:
    """
    ATP consumption rate during muscle contraction.

    Formula: ATP rate = (isometric rate) + (shortening rate) × v

    The ATP consumption has a baseline isometric component plus
    a velocity-dependent shortening component.

    Parameters:
    -----------
    isometric_rate : float - ATP consumption during isometric contraction (mol/s)
    shortening_rate : float - Additional ATP rate per unit velocity (mol/s per m/s)
    v : float - Shortening velocity (m/s)

    Returns:
    --------
    ATP_rate : float - ATP consumption rate (mol/s)
    """
    return isometric_rate + shortening_rate * v

# Create and register atomic equation
atp_consumption_eq = create_equation(
    id="excitable.energetics.atp_consumption",
    name="Muscle ATP Consumption Rate",
    category=EquationCategory.EXCITABLE,
    latex=r"\dot{ATP} = \dot{ATP}_{iso} + \dot{ATP}_{short} \cdot v",
    simplified="ATP rate = (isometric rate) + (shortening rate) × v",
    description="Rate of ATP hydrolysis during muscle contraction",
    compute_func=atp_consumption,
    parameters=[
        Parameter(
            name="isometric_rate",
            description="ATP consumption during isometric contraction",
            units="mol/s",
            symbol=r"\dot{ATP}_{iso}",
            physiological_range=(0.0, 1e-3)
        ),
        Parameter(
            name="shortening_rate",
            description="Additional ATP rate per unit velocity",
            units="mol/s per m/s",
            symbol=r"\dot{ATP}_{short}",
            physiological_range=(0.0, 1e-3)
        ),
        Parameter(
            name="v",
            description="Shortening velocity",
            units="m/s",
            symbol="v",
            physiological_range=(0.0, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.4")
)
register_equation(atp_consumption_eq)
